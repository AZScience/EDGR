"""EDGR PhD Research Pipeline API — research workbench + live IDS/CTI app."""

from __future__ import annotations

from pathlib import Path as FsPath
from typing import Annotated, Any, Optional

from fastapi import Body, FastAPI, HTTPException, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from app.core.edgr import edgr_engine
from app.core.knowledge_graph import kg
from app.core.vector_store import vector_store
from app.data.cti_seed import QA_DATASET
from app.evaluation.metrics import evaluation_service
from app.models.schemas import (
    ExperimentRequest,
    GraphEdge,
    GraphNode,
    QueryRequest,
)
from app.pipeline.service import pipeline_service
from app.services.alert_ingest import SAMPLE_SURICATA_ALERT

# Prefill examples for Swagger «Examples» dropdown (no need to invent JSON).
_EX_CVE = {
    "query": "What is CVE-2021-44228 and how is it exploited?",
    "top_k": 5,
    "enable_temporal": True,
    "enable_graph": True,
    "enable_trust_score": True,
}
_EX_APT = {
    "query": "Which ATT&CK techniques does APT29 commonly use?",
    "top_k": 5,
    "enable_temporal": True,
    "enable_graph": True,
    "enable_trust_score": True,
}
_EX_LATERAL = {
    "query": "How can NIDS detect lateral movement?",
    "top_k": 5,
    "enable_temporal": True,
    "enable_graph": True,
    "enable_trust_score": True,
}
_EX_MATRIX = {
    "query": "What is CVE-2021-44228 and how is it exploited?",
    "top_k": 5,
}
_EX_ABLATION_OFF = {
    "query": "What is CVE-2021-44228 and how is it exploited?",
    "top_k": 5,
    "enable_temporal": False,
    "enable_graph": False,
    "enable_trust_score": True,
}

_TASK_RUN_EXAMPLES = {
    "cve_log4j": {
        "summary": "① CVE-2021-44228 (khuyến nghị)",
        "description": "Query CTI mẫu — chọn cái này rồi bấm Execute.",
        "value": _EX_CVE,
    },
    "apt29": {
        "summary": "② APT29 / ATT&CK",
        "description": "Hỏi TTP của APT29.",
        "value": _EX_APT,
    },
    "lateral": {
        "summary": "③ Lateral movement / NIDS",
        "description": "Hỏi phát hiện lateral movement.",
        "value": _EX_LATERAL,
    },
    "ablation_no_graph": {
        "summary": "④ Ablation: tắt graph + temporal",
        "description": "Dùng khi thử Step 11 / so sánh cổng EDGR.",
        "value": _EX_ABLATION_OFF,
    },
    "minimal": {
        "summary": "⑤ Tối giản (chỉ query + top_k)",
        "description": "Đủ cho hầu hết task pipeline (catalog/matrix không bắt buộc query).",
        "value": _EX_MATRIX,
    },
}

app = FastAPI(
    title="EDGR — PhD Research Pipeline",
    description=(
        "## Cách dùng trang /docs (không cần tự viết JSON)\n\n"
        "1. Chọn một API bên dưới → bấm **Try it out**.\n"
        "2. Nếu có **Examples** / dropdown: **chọn sẵn** (① CVE…, ② APT29…).\n"
        "3. Path `step_id` / `task_id`: chọn hoặc điền số/tab có sẵn (vd. `1` + `matrix`).\n"
        "4. Bấm **Execute** → xem **Response body**.\n\n"
        "**Demo hàng ngày:** giao diện http://127.0.0.1:5180 "
        "(tab + «Chạy công việc này»). Trang này chỉ để thử API.\n\n"
        "Evidence-Driven Dynamic Graph Retrieval — research workbench + live IDS/CTI app."
    ),
    version="2.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskRunRequest(BaseModel):
    """Body dùng chung cho chạy task pipeline và /api/app/analyze."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [_EX_CVE, _EX_APT, _EX_LATERAL, _EX_MATRIX, _EX_ABLATION_OFF],
        }
    )

    query: Optional[str] = Field(
        default="What is CVE-2021-44228 and how is it exploited?",
        description="Câu hỏi CTI / IDS. Có thể để trống với vài task (catalog, matrix).",
    )
    top_k: int = Field(default=5, description="Số evidence tin cậy (khuyến nghị 5).")
    enable_temporal: bool = Field(default=True, description="Lọc thời gian (EDGR).")
    enable_graph: bool = Field(default=True, description="Mở rộng đồ thị (EDGR).")
    enable_trust_score: bool = Field(
        default=True, description="Chấm điểm tin cậy / hallucination gate."
    )
    node_id: Optional[str] = Field(default=None, description="Tuỳ chọn — id nút KG.")
    label: Optional[str] = Field(default=None, description="Tuỳ chọn — nhãn nút.")
    timestamp: Optional[str] = Field(default=None, description="Tuỳ chọn — ISO time.")
    extra: dict[str, Any] = Field(
        default_factory=dict,
        description='Tuỳ chọn — vd. {"live_enrich": true} cho app analyze.',
    )


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "name": "EDGR Pipeline",
        "version": "2.2.0",
        "steps": 16,
        "docs": "/docs",
        "pipeline": "/api/pipeline",
        "app": "/api/app/analyze",
    }


@app.get("/api/health")
def health() -> dict[str, Any]:
    stats = kg.stats()
    return {
        "status": "ok",
        "kg_nodes": stats.nodes,
        "kg_edges": stats.edges,
        "evidence_chunks": len(vector_store.chunks),
        "qa_pairs": len(QA_DATASET),
        "pipeline_steps": 16,
    }


@app.get("/api/app/status")
def ids_cti_app_status() -> dict[str, Any]:
    from app.services.ids_cti_app import app_status

    return app_status()


@app.post(
    "/api/app/analyze",
    summary="Phân tích CTI/IDS (live EDGR)",
    description=(
        "Chọn **Examples** → Try it out → Execute. "
        "Không cần tự gõ JSON. Demo UI: http://127.0.0.1:5180 bước 16."
    ),
)
def ids_cti_app_analyze(
    body: Annotated[
        TaskRunRequest | None,
        Body(openapi_examples=_TASK_RUN_EXAMPLES),
    ] = None,
) -> dict[str, Any]:
    """Live IDS/CTI application endpoint — real EDGR computation, not a mock."""
    from app.services.ids_cti_app import analyze

    body = body or TaskRunRequest()
    try:
        return analyze(
            body.query or "",
            top_k=body.top_k,
            enable_temporal=body.enable_temporal,
            enable_graph=body.enable_graph,
            enable_trust_score=body.enable_trust_score,
            live_enrich=bool((body.extra or {}).get("live_enrich", True)),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/app/alerts/sample")
def ids_cti_alert_sample() -> dict[str, Any]:
    from app.services.alert_ingest import sample_alert_payload

    return sample_alert_payload()


@app.get("/api/app/alerts")
def ids_cti_list_alerts(limit: int = 50) -> dict[str, Any]:
    from app.services.alert_ingest import list_alerts

    return list_alerts(limit=limit)


@app.post(
    "/api/app/alerts",
    summary="Nhận alert Suricata (hàng đợi)",
    description="Chọn example mẫu Suricata → Execute. Sau đó GET /api/app/alerts để lấy alert_id.",
)
async def ids_cti_ingest_alerts(
    request: Request,
    body: Annotated[
        dict[str, Any] | None,
        Body(
            openapi_examples={
                "suricata_smb": {
                    "summary": "① Mẫu Suricata SMB lateral",
                    "description": "Alert eve.json mẫu — chọn rồi Execute.",
                    "value": SAMPLE_SURICATA_ALERT,
                },
                "wrapped": {
                    "summary": "② Bọc trong {alerts:[...]}",
                    "value": {"alerts": [SAMPLE_SURICATA_ALERT]},
                },
            },
        ),
    ] = None,
) -> dict[str, Any]:
    """
    Realtime alert ingest (Suricata eve.json–style).

    Body: one alert object, an array of events, or {\"alerts\":[...]} / {\"events\":[...]}.
    """
    from app.services.alert_ingest import ingest_alerts

    try:
        payload = body if body is not None else await request.json()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}") from e
    try:
        return ingest_alerts(payload, source="http")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class AlertAnalyzeBody(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "alert_id": "thay_bang_id_tu_GET_api_app_alerts",
                    "top_k": 5,
                    "live_enrich": True,
                }
            ]
        }
    )

    alert_id: str = Field(
        ...,
        description="Lấy từ GET /api/app/alerts sau khi POST /api/app/alerts.",
        examples=["paste_alert_id_here"],
    )
    top_k: int = 5
    live_enrich: bool = True


@app.post(
    "/api/app/alerts/analyze",
    summary="Phân tích 1 alert đã xếp hàng",
    description=(
        "Thứ tự: (1) POST /api/app/alerts với example Suricata → "
        "(2) GET /api/app/alerts copy `id` → (3) dán vào alert_id → Execute."
    ),
)
def ids_cti_analyze_alert(
    body: Annotated[
        AlertAnalyzeBody,
        Body(
            openapi_examples={
                "after_ingest": {
                    "summary": "① Sau khi ingest — dán alert_id",
                    "description": "Thay alert_id bằng id thật từ GET /api/app/alerts.",
                    "value": {
                        "alert_id": "paste_alert_id_from_GET_alerts",
                        "top_k": 5,
                        "live_enrich": True,
                    },
                }
            }
        ),
    ],
) -> dict[str, Any]:
    """Run live EDGR on a queued realtime alert."""
    from app.services.ids_cti_app import analyze_alert

    try:
        return analyze_alert(
            body.alert_id,
            top_k=body.top_k,
            live_enrich=body.live_enrich,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/pipeline")
def pipeline_def() -> dict[str, Any]:
    return pipeline_service.definition()


@app.get(
    "/api/pipeline/{step_id}/academic",
    summary="Gói học thuật tab cha",
)
def step_academic(
    step_id: Annotated[
        int,
        Path(
            description="Số bước 1–16",
            examples=[1, 4, 9, 16],
            openapi_examples={
                "step1": {"summary": "Bước 1 — Khảo sát", "value": 1},
                "step4": {"summary": "Bước 4 — EDGR", "value": 4},
                "step9": {"summary": "Bước 9 — Thực nghiệm", "value": 9},
            },
        ),
    ],
) -> dict[str, Any]:
    """7 khối học thuật cho tab cha (bước)."""
    try:
        return pipeline_service.academic(step_id, None)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.get(
    "/api/pipeline/{step_id}/{task_id}/academic",
    summary="Gói học thuật tab con",
)
def task_academic(
    step_id: Annotated[
        int,
        Path(
            openapi_examples={
                "s1": {"summary": "Bước 1", "value": 1},
                "s9": {"summary": "Bước 9", "value": 9},
            }
        ),
    ],
    task_id: Annotated[
        str,
        Path(
            openapi_examples={
                "matrix": {"summary": "matrix (ma trận)", "value": "matrix"},
                "catalog": {"summary": "catalog (APA)", "value": "catalog"},
                "compare": {"summary": "compare (Step 9)", "value": "compare"},
                "rag": {"summary": "rag topic", "value": "rag"},
            }
        ),
    ],
) -> dict[str, Any]:
    """7 khối học thuật cho tab con (công việc)."""
    try:
        return pipeline_service.academic(step_id, task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.post(
    "/api/pipeline/{step_id}/{task_id}/run",
    summary="Chạy 1 công việc pipeline",
    description=(
        "1) Chọn example path (vd. bước 1 + matrix). "
        "2) Chọn Examples body (① CVE…). "
        "3) Try it out → Execute."
    ),
)
def run_pipeline_task(
    step_id: Annotated[
        int,
        Path(
            openapi_examples={
                "step1_survey": {"summary": "Bước 1 — Khảo sát", "value": 1},
                "step7_data": {"summary": "Bước 7 — Dữ liệu", "value": 7},
                "step9_exp": {"summary": "Bước 9 — Thực nghiệm", "value": 9},
                "step14_thesis": {"summary": "Bước 14 — Luận án", "value": 14},
            }
        ),
    ],
    task_id: Annotated[
        str,
        Path(
            openapi_examples={
                "matrix": {"summary": "matrix", "value": "matrix"},
                "catalog": {"summary": "catalog", "value": "catalog"},
                "mitre": {"summary": "mitre (ingest)", "value": "mitre"},
                "compare": {"summary": "compare", "value": "compare"},
                "selfrag": {"summary": "selfrag baseline", "value": "selfrag"},
                "ch4": {"summary": "ch4 (luận án)", "value": "ch4"},
            }
        ),
    ],
    body: Annotated[
        TaskRunRequest | None,
        Body(openapi_examples=_TASK_RUN_EXAMPLES),
    ] = None,
) -> dict[str, Any]:
    body = body or TaskRunRequest()
    params = {
        "query": body.query,
        "top_k": body.top_k,
        "enable_temporal": body.enable_temporal,
        "enable_graph": body.enable_graph,
        "enable_trust_score": body.enable_trust_score,
        **body.extra,
    }
    if body.node_id:
        params["node_id"] = body.node_id
    if body.label:
        params["label"] = body.label
    if body.timestamp:
        params["timestamp"] = body.timestamp
    # drop Nones
    params = {k: v for k, v in params.items() if v is not None}
    try:
        return pipeline_service.run_task(step_id, task_id, params)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post(
    "/api/query",
    summary="EDGR query trực tiếp",
    description="Chọn Examples → Execute.",
)
def query_edgr(
    req: Annotated[
        QueryRequest,
        Body(
            openapi_examples={
                "cve": {
                    "summary": "① CVE-2021-44228",
                    "value": {
                        "query": "What is CVE-2021-44228 and how is it exploited?",
                        "top_k": 5,
                        "enable_temporal": True,
                        "enable_graph": True,
                        "enable_trust_score": True,
                    },
                },
                "apt": {
                    "summary": "② APT29",
                    "value": {
                        "query": "Which ATT&CK techniques does APT29 commonly use?",
                        "top_k": 5,
                        "enable_temporal": True,
                        "enable_graph": True,
                        "enable_trust_score": True,
                    },
                },
            }
        ),
    ],
) -> dict[str, Any]:
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query is required")
    return edgr_engine.run(req).model_dump()


@app.post(
    "/api/experiments",
    summary="So sánh EDGR vs baselines",
    description="Chọn Examples → Execute (chạy vài method — hơi lâu).",
)
def experiments(
    req: Annotated[
        ExperimentRequest,
        Body(
            openapi_examples={
                "full_compare": {
                    "summary": "① So sánh đủ methods",
                    "value": {
                        "query": "What is CVE-2021-44228 and how is it exploited?",
                        "top_k": 5,
                        "methods": [
                            "EDGR",
                            "RAG",
                            "GraphRAG",
                            "LightRAG",
                            "HippoRAG",
                            "Self-RAG",
                            "Corrective-RAG",
                        ],
                    },
                },
                "quick": {
                    "summary": "② Nhanh: EDGR + RAG + GraphRAG",
                    "value": {
                        "query": "What is CVE-2021-44228 and how is it exploited?",
                        "top_k": 5,
                        "methods": ["EDGR", "RAG", "GraphRAG"],
                    },
                },
            }
        ),
    ],
) -> dict[str, Any]:
    results = evaluation_service.compare_methods(req)
    return {"query": req.query, "results": [r.model_dump() for r in results]}


@app.get("/api/evaluate")
def evaluate(limit: int | None = None) -> dict[str, Any]:
    """Full QA_DATASET when limit omitted; pass limit for a quick subset."""
    return evaluation_service.evaluate_dataset(limit=limit)


@app.get("/api/human-eval")
def human_eval_get() -> dict[str, Any]:
    """SOC human-eval report: rubric, seed panel, Cohen’s κ (fast — no batch EDGR)."""
    from app.evaluation.human_eval import human_eval_full_report

    return human_eval_full_report(session_limit=0)


@app.get("/api/human-eval/session")
def human_eval_session(limit: int = 8) -> dict[str, Any]:
    from app.evaluation.human_eval import build_session, ensure_seed_annotations

    ensure_seed_annotations(n_items=min(30, len(QA_DATASET)))
    return build_session(limit=min(limit, 12))


@app.get("/api/human-eval/kappa")
def human_eval_kappa() -> dict[str, Any]:
    from app.evaluation.human_eval import kappa_report

    return kappa_report()


@app.post("/api/human-eval/annotations")
def human_eval_post_annotations(body: dict[str, Any]) -> dict[str, Any]:
    """
    Body: { "annotations": [ {item_id, annotator_id, groundedness_1_5,
    unsupported_ids_0_1, actionability_1_5, abstain_ok, notes?} ] }
    """
    from app.evaluation.human_eval import upsert_annotations

    rows = body.get("annotations") or body.get("rows") or []
    if not isinstance(rows, list) or not rows:
        return {"error": "annotations list required", "ok": False}
    return {"ok": True, **upsert_annotations(rows)}


@app.get("/api/kg")
def get_kg(center: str | None = None, limit: int = 40) -> dict[str, Any]:
    centers = [c.strip() for c in center.split(",")] if center else None
    payload = kg.subgraph_payload(centers, limit=limit)
    payload["stats"] = kg.stats().model_dump()
    return payload


@app.get("/api/kg/stats")
def kg_stats() -> dict[str, Any]:
    return kg.stats().model_dump()


@app.post("/api/kg/nodes")
def add_node(node: GraphNode) -> dict[str, Any]:
    kg.add_node(node)
    return {"ok": True, "node": node.model_dump()}


@app.post("/api/kg/edges")
def add_edge(edge: GraphEdge) -> dict[str, Any]:
    kg.add_edge(edge)
    return {"ok": True, "edge": edge.model_dump()}


@app.get("/api/qa")
def list_qa() -> dict[str, Any]:
    return {"count": len(QA_DATASET), "items": QA_DATASET}


# ── React SPA (built: frontend/dist) at /ui/ ─────────────────────────
# Used by Streamlit iframe embed for pixel-perfect React UI.
_DIST = FsPath(__file__).resolve().parents[2] / "frontend" / "dist"
if _DIST.is_dir():
    from fastapi.responses import FileResponse
    from fastapi.staticfiles import StaticFiles

    _ui_assets = _DIST / "assets"
    if _ui_assets.is_dir():
        app.mount("/ui/assets", StaticFiles(directory=str(_ui_assets)), name="ui-assets")

    @app.get("/ui")
    @app.get("/ui/")
    def ui_index() -> FileResponse:
        return FileResponse(_DIST / "index.html")

    @app.get("/ui/{asset_path:path}")
    def ui_spa(asset_path: str) -> FileResponse:
        candidate = _DIST / asset_path
        if candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(_DIST / "index.html")

    # React public assets referenced as absolute paths (e.g. /edgr-topic-banner.png,
    # /quy-trinh-a-z.png) are NOT prefixed with /ui/ in the source. Serve them from root.
    _PUBLIC_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".ico", ".gif", ".woff", ".woff2", ".ttf"}

    @app.get("/{pub_file:path}")
    def public_asset(pub_file: str) -> FileResponse:
        candidate = _DIST / pub_file
        if candidate.is_file() and candidate.suffix.lower() in _PUBLIC_EXTS:
            return FileResponse(candidate)
        # 404 for anything else (don't shadow /api/*)
        from fastapi import HTTPException as _HTTPException
        raise _HTTPException(status_code=404)

