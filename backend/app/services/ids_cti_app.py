"""
Practical IDS/CTI application service — live EDGR, not a scripted mock.

- Answers are computed at request time via EDGREngine on the running KG + vector store.
- Optional: enrich with a live NVD lookup when the query names a CVE (network-dependent).
- No pre-written per-query answer table.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

from app.core.edgr import edgr_engine
from app.core.knowledge_graph import kg
from app.core.vector_store import vector_store
from app.models.schemas import QueryRequest
from app.pipeline.graph_viz import attach_viz, kg_viz
from app.pipeline.practical_apps import APP_NAME_EN, APP_NAME_VI

_CVE_RE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)


def app_status() -> dict[str, Any]:
    from app.services.alert_ingest import list_alerts

    stats = kg.stats()
    queue = list_alerts(limit=1)
    return {
        "app_name_vi": APP_NAME_VI,
        "app_name_en": APP_NAME_EN,
        "mode": "live_edgr",
        "simulated": False,
        "scripted_answers": False,
        "kg_nodes": stats.nodes,
        "kg_edges": stats.edges,
        "evidence_chunks": len(vector_store.chunks),
        "alert_queue_size": queue.get("queue_size", 0),
        "engine": "app.core.edgr.EDGREngine",
        "generator": "extractive_grounded (evidence-constrained)",
        "realtime_ingest": "POST /api/app/alerts (Suricata eve.json–style)",
        "note_vi": (
            "Mỗi lần Phân tích chạy EDGR thật trên KG/vector đang sống — "
            "không lấy câu trả lời viết sẵn theo query. "
            "Alert realtime: POST /api/app/alerts rồi Analyze."
        ),
        "note_en": (
            "Each Analyze run executes live EDGR on the running KG/vector store — "
            "not a pre-written answer keyed by query. "
            "Realtime alerts: POST /api/app/alerts then Analyze."
        ),
    }


def _fetch_nvd_cve(cve_id: str, timeout_s: float = 4.0) -> dict[str, Any] | None:
    """Best-effort live NVD enrichment. Returns None on any failure."""
    url = (
        "https://services.nvd.nist.gov/rest/json/cves/2.0?"
        f"cveId={urllib.request.quote(cve_id)}"
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "EDGR-IDS-CTI-App/1.0 (research; local)",
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None

    vulns = data.get("vulnerabilities") or []
    if not vulns:
        return None
    cve = (vulns[0] or {}).get("cve") or {}
    descriptions = cve.get("descriptions") or []
    en = next(
        (d.get("value") for d in descriptions if (d.get("lang") or "").lower() == "en"),
        None,
    )
    if not en:
        en = descriptions[0].get("value") if descriptions else None
    if not en:
        return None
    published = cve.get("published") or datetime.now(timezone.utc).date().isoformat()
    return {
        "id": f"nvd_live_{cve_id.upper().replace('-', '_')}",
        "content": f"{cve_id.upper()}: {en.strip()}",
        "source": "NVD (live)",
        "entities": [cve_id.upper()],
        "timestamp": str(published)[:10],
        "reliability": 0.96,
        "type": "cve",
        "live": True,
    }


def _maybe_enrich_live_cve(query: str) -> dict[str, Any]:
    """Inject NVD live chunk into vector store when a CVE is present."""
    found = _CVE_RE.findall(query or "")
    if not found:
        return {"attempted": False, "injected": [], "errors": []}
    injected: list[str] = []
    errors: list[str] = []
    for cve in dict.fromkeys(x.upper() for x in found):
        chunk = _fetch_nvd_cve(cve)
        if not chunk:
            errors.append(cve)
            continue
        # upsert into live vector store + ensure KG node
        existing = {c.get("id") for c in vector_store.chunks}
        if chunk["id"] not in existing:
            vector_store.add(chunk)
        try:
            from app.models.schemas import EntityType, GraphNode

            kg.add_node(
                GraphNode(
                    id=cve,
                    label=cve,
                    type=EntityType.CVE,
                    properties={"source": "NVD live"},
                    reliability=0.96,
                )
            )
        except Exception:  # noqa: BLE001
            pass
        injected.append(cve)
    return {
        "attempted": True,
        "injected": injected,
        "errors": errors,
        "source": "NVD REST API 2.0",
    }


def analyze(
    query: str,
    *,
    top_k: int = 5,
    enable_temporal: bool = True,
    enable_graph: bool = True,
    enable_trust_score: bool = True,
    live_enrich: bool = True,
) -> dict[str, Any]:
    q = (query or "").strip()
    if not q:
        raise ValueError("Query is required")

    enrich_meta: dict[str, Any] = {"attempted": False}
    if live_enrich:
        enrich_meta = _maybe_enrich_live_cve(q)

    ans = edgr_engine.run(
        QueryRequest(
            query=q,
            top_k=top_k,
            enable_temporal=enable_temporal,
            enable_graph=enable_graph,
            enable_trust_score=enable_trust_score,
        )
    )
    data = ans.model_dump()
    ents = list(ans.entities or [])
    stage_summary = [
        {
            "stage": s.get("stage"),
            "name": s.get("name"),
            "name_vi": s.get("name_vi"),
            "duration_ms": s.get("duration_ms"),
        }
        for s in (data.get("stages") or [])
        if isinstance(s, dict)
    ]

    status = app_status()
    meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    payload = {
        "kind": "ids_cti_app_console",
        "app_name_vi": APP_NAME_VI,
        "app_name_en": APP_NAME_EN,
        "mode": "live_edgr",
        "simulated": False,
        "scripted_answers": False,
        "query": q,
        "answer": data.get("answer"),
        "confidence": data.get("confidence"),
        "faithfulness": data.get("faithfulness"),
        "hallucination_rate": data.get("hallucination_rate"),
        "latency_ms": data.get("latency_ms"),
        "entities": data.get("entities"),
        "evidence": data.get("evidence"),
        "stages": data.get("stages"),
        "stage_summary": stage_summary,
        "method": data.get("method", "EDGR"),
        "metadata": meta,
        "abstained": bool(meta.get("abstained")),
        "apply": meta.get("apply", 1),
        "abstain_reason_vi": meta.get("abstain_reason_vi", ""),
        "abstain_reason_en": meta.get("abstain_reason_en", ""),
        "live_enrichment": enrich_meta,
        "runtime": {
            "kg_nodes": status["kg_nodes"],
            "kg_edges": status["kg_edges"],
            "evidence_chunks": status["evidence_chunks"],
            "engine": status["engine"],
            "generator": status["generator"],
        },
        "provenance_vi": (
            "Câu trả lời được tổng hợp extractive từ evidence EDGR vừa truy hồi "
            "(không phải bảng đáp án giả lập)."
        ),
        "provenance_en": (
            "The answer is extractively synthesized from evidence just retrieved by EDGR "
            "(not a mocked answer table)."
        ),
        "computation_kind": "live_edgr",
    }
    return attach_viz(
        payload,
        kg_viz(
            title_vi="Đồ thị liên quan — ứng dụng IDS/CTI (live)",
            title_en="Related graph — IDS/CTI app (live)",
            center=ents[:6] or None,
            limit=28,
            seed_ids=ents,
        ),
    )


def analyze_alert(
    alert_id: str,
    *,
    top_k: int = 5,
    live_enrich: bool = True,
) -> dict[str, Any]:
    """Run live EDGR on a queued realtime alert (no ML training)."""
    from app.services.alert_ingest import get_alert, mark_analyzed

    item = get_alert(alert_id)
    if not item:
        raise ValueError(f"Unknown alert_id: {alert_id}")
    result = analyze(
        str(item.get("query") or ""),
        top_k=top_k,
        live_enrich=live_enrich,
    )
    mark_analyzed(alert_id, analysis_ref=alert_id)
    result["alert_id"] = alert_id
    result["alert"] = {k: v for k, v in item.items() if k != "raw"}
    result["input_mode"] = "realtime_alert"
    result["provenance_vi"] = (
        f"Phân tích từ alert realtime `{alert_id}` → chuẩn hoá thành query → EDGR live."
    )
    result["provenance_en"] = (
        f"Analyzed from realtime alert `{alert_id}` → normalized query → live EDGR."
    )
    return result
