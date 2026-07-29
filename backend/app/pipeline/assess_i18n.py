"""English assessment texts + evidence/figure/citation support for academic blocks."""

from __future__ import annotations

from typing import Any

# step_id -> English assessment fields
STEP_ASSESS_EN: dict[int, dict[str, str]] = {
    1: {
        "strength_en": "Covers all six RAG–IDS axes in the research process diagram",
        "limitation_en": "Curated corpus; not a full Web of Science crawl",
        "verdict_en": "Sufficient for quantitative gap analysis in step 2",
    },
    2: {
        "strength_en": "Gaps are tied to bibliographic evidence, not pure speculation",
        "limitation_en": "No expert Delphi validation yet",
        "verdict_en": "Solid basis for formal problem definition (step 3)",
    },
    3: {
        "strength_en": "Clear optimization objective with CVE/ATT&CK constraints",
        "limitation_en": "HallucinationRisk is a measurable proxy, not full human gold",
        "verdict_en": "Enough to design EDGR as the solver",
    },
    4: {
        "strength_en": "Main contribution: trust gate before generation on a CTI graph",
        "limitation_en": "Extractive generator; an LLM API can replace it later",
        "verdict_en": "Core contribution of the dissertation",
    },
    5: {
        "strength_en": "Multi-source plus real incremental updates in process memory",
        "limitation_en": "Not yet a production Neo4j deployment",
        "verdict_en": "Adequate for EDGR retrieval experiments",
    },
    6: {
        "strength_en": "Multi-signal scoring (source, time, graph, semantics)",
        "limitation_en": "Fixed weights; could be learned via regression",
        "verdict_en": "Suitable for trusted CTI evidence selection",
    },
    7: {
        "strength_en": "QA pairs linked to gold evidence_ids for retrieval metrics",
        "limitation_en": "Demo scale; needs larger annotated gold",
        "verdict_en": "Enough to evaluate EDGR vs baselines",
    },
    8: {
        "strength_en": "Architecture matches the system deployment diagram",
        "limitation_en": "Single-process demo; needs containerization",
        "verdict_en": "Ready for step-9 experiments",
    },
    9: {
        "strength_en": "Fair protocol with unified metrics",
        "limitation_en": "Baselines are research-faithful re-implementations, not official dumps",
        "verdict_en": "Valid for dissertation-demo comparison",
    },
    10: {
        "strength_en": "Multi-metric: generation + retrieval + system",
        "limitation_en": "Accuracy is a proxy from F1/entity hit",
        "verdict_en": "Enough for the Experiments chapter",
    },
    11: {
        "strength_en": "Demonstrates each module's contribution",
        "limitation_en": "Higher-order component interactions not fully analyzed",
        "verdict_en": "Required for the EDGR paper",
    },
    12: {
        "strength_en": "Combines asymptotic analysis with empirical timing",
        "limitation_en": "Scalability tested on demo-sized graphs",
        "verdict_en": "Supports the algorithm-analysis claim",
    },
    13: {
        "strength_en": "Clear four-paper publication roadmap with overlap control",
        "limitation_en": "Venue targeting still tentative",
        "verdict_en": "Executable publication plan",
    },
    14: {
        "strength_en": "Eight-chapter structure aligned with the research process",
        "limitation_en": "Draft depth varies by chapter",
        "verdict_en": "Ready for iterative dissertation writing",
    },
    15: {
        "strength_en": "Defense checklist covers demo, metrics, and Q&A",
        "limitation_en": "Live rehearsal still required",
        "verdict_en": "Prepared for final defense",
    },
    16: {
        "strength_en": "Runnable IDS/CTI app with honest success/failure bounds",
        "limitation_en": "Still a scientific demo, not a production SOC deploy",
        "verdict_en": "Credible practical-application step for the thesis",
    },
}


def _as_str_list(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, str):
        s = v.strip()
        return [s] if s else []
    if isinstance(v, (list, tuple)):
        out: list[str] = []
        for x in v:
            if isinstance(x, str) and x.strip():
                out.append(x.strip())
            elif isinstance(x, dict):
                t = x.get("text") or x.get("label") or x.get("name") or ""
                if t:
                    out.append(str(t).strip())
        return out
    if isinstance(v, dict):
        # Flatten short scalar fields
        parts: list[str] = []
        for k, val in v.items():
            if k in {"live", "tables", "trace", "raw"}:
                continue
            if isinstance(val, (str, int, float)) and str(val).strip():
                parts.append(f"{k}={val}")
            elif isinstance(val, list) and val and all(isinstance(x, str) for x in val[:5]):
                parts.append(f"{k}: " + "; ".join(val[:5]))
        return parts[:8]
    return []


def _evidence_from_minh_chung(mc: dict[str, Any]) -> tuple[list[str], list[str]]:
    vi: list[str] = []
    en: list[str] = []

    claim_vi = str(mc.get("claim_vi") or mc.get("claim") or "").strip()
    claim_en = str(mc.get("claim_en") or mc.get("claim") or "").strip()
    if claim_vi:
        vi.append(f"Claim thiết kế: {claim_vi}")
    if claim_en:
        en.append(f"Design claim: {claim_en}")

    expl_vi = str(mc.get("explain_vi") or mc.get("explain") or "").strip()
    expl_en = str(mc.get("explain_en") or mc.get("explain") or "").strip()
    if expl_vi:
        vi.append(expl_vi)
    if expl_en:
        en.append(expl_en)

    logic_vi = str(mc.get("logic_vi") or mc.get("logic") or "").strip()
    logic_en = str(mc.get("logic_en") or mc.get("logic") or "").strip()
    if logic_vi:
        vi.append(f"Logic: {logic_vi}")
    if logic_en:
        en.append(f"Logic: {logic_en}")

    metric = mc.get("metric")
    if metric:
        # Chip-friendly; avoid KaTeX-triggering wrappers around |P|.
        vi.append(f"metric · {metric}")
        en.append(f"metric · {metric}")

    for key in ("gaps", "axes", "type", "paper", "chapter", "task"):
        if key in mc and mc[key] not in (None, "", []):
            val = mc[key]
            if isinstance(val, list):
                shown = ", ".join(str(x) for x in val[:6])
            else:
                shown = str(val)
            vi.append(f"{key} · {shown}")
            en.append(f"{key} · {shown}")

    live = mc.get("live") if isinstance(mc.get("live"), dict) else {}
    if live:
        # Prefer compact live facts
        for k in (
            "kg_nodes",
            "kg_edges",
            "qa_count",
            "chunk_count",
            "paper_count",
            "faithfulness",
            "hallucination_rate",
            "mrr",
            "p_at_k",
            "latency_ms",
            "total",
            "V",
            "E",
        ):
            if k in live and live[k] is not None:
                vi.append(f"Live `{k}` = {live[k]}")
                en.append(f"Live `{k}` = {live[k]}")
        # Generic fallback from live summary fields
        if len(vi) < 2:
            for k, val in list(live.items())[:6]:
                if isinstance(val, (str, int, float, bool)):
                    vi.append(f"Live `{k}` = {val}")
                    en.append(f"Live `{k}` = {val}")

    # Dedup preserve order
    def uniq(xs: list[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for x in xs:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out[:10]

    return uniq(vi), uniq(en)


def _figures_from_package(package: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Short pointers to design blocks — do not dump full LaTeX (avoids clutter + KaTeX mishaps)."""
    vi: list[str] = []
    en: list[str] = []

    math = package.get("mo_hinh_toan") if isinstance(package.get("mo_hinh_toan"), dict) else {}
    formulas = math.get("formulas") if isinstance(math.get("formulas"), list) else []
    if formulas:
        labels = []
        for f in formulas[:4]:
            if isinstance(f, dict):
                lab = str(f.get("label_vi") or f.get("label_en") or f.get("id") or "").strip()
                if lab:
                    labels.append(lab)
        n = len(formulas)
        if labels:
            vi.append(f"Mô hình toán phía trên ({n} công thức): " + "; ".join(labels) + ".")
            en.append(f"Math model above ({n} formulas): " + "; ".join(labels) + ".")
        else:
            vi.append(f"Mô hình toán phía trên — {n} công thức (xem khối Math).")
            en.append(f"Math model above — {n} formulas (see Math block).")

    algo = package.get("mo_hinh_thuat_toan") if isinstance(package.get("mo_hinh_thuat_toan"), dict) else {}
    name_vi = str(algo.get("name_vi") or algo.get("name") or "").strip()
    name_en = str(algo.get("name_en") or algo.get("name") or "").strip()
    pseudo = algo.get("pseudocode") if isinstance(algo.get("pseudocode"), list) else []
    if name_vi or name_en or pseudo:
        vi.append(
            f"Thuật toán: «{name_vi or name_en or 'procedure'}»"
            + (f" · {len(pseudo)} bước" if pseudo else "")
            + " (khối Algorithm)."
        )
        en.append(
            f"Algorithm: «{name_en or name_vi or 'procedure'}»"
            + (f" · {len(pseudo)} steps" if pseudo else "")
            + " (Algorithm block)."
        )

    ops = package.get("mo_hinh_hoat_dong") if isinstance(package.get("mo_hinh_hoat_dong"), dict) else {}
    flow = ops.get("flow") if isinstance(ops.get("flow"), list) else []
    if flow:
        vi.append(f"Luồng vận hành: {len(flow)} bước (khối Operating model).")
        en.append(f"Operating flow: {len(flow)} steps (Operating model block).")

    csdl = package.get("csdl") if isinstance(package.get("csdl"), dict) else {}
    csdl_name = str(csdl.get("name_vi") or csdl.get("name") or csdl.get("name_en") or "").strip()
    if csdl_name:
        vi.append(f"CSDL: {csdl_name} (khối Database).")
        en.append(f"Database: {csdl_name} (Database block).")

    if not vi:
        vi.append("Xem các khối Math / Algorithm / Operating / Graph phía trên.")
        en.append("See the Math / Algorithm / Operating / Graph blocks above.")
    return vi[:5], en[:5]


def _cites_from_package(package: dict[str, Any]) -> list[dict[str, Any]]:
    raw = package.get("trich_dan")
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for c in raw[:8]:
        if isinstance(c, dict):
            text = str(c.get("text") or "").strip()
            if not text:
                continue
            out.append(
                {
                    "id": c.get("id"),
                    "text": text,
                    "doi": c.get("doi"),
                }
            )
        elif isinstance(c, str) and c.strip():
            out.append({"text": c.strip()})
    return out


def attach_assessment_support(
    assess: dict[str, Any],
    package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Attach minh chứng / hình / dẫn chứng so design assessment is not bare prose."""
    out = dict(assess or {})
    pkg = package or {}

    mc = pkg.get("minh_chung") if isinstance(pkg.get("minh_chung"), dict) else {}
    ev_vi, ev_en = _evidence_from_minh_chung(mc)
    # Keep author-supplied lists if present
    if not out.get("evidence_vi"):
        out["evidence_vi"] = ev_vi
    if not out.get("evidence_en"):
        out["evidence_en"] = ev_en or ev_vi

    fig_vi, fig_en = _figures_from_package(pkg)
    if not out.get("figures_vi"):
        out["figures_vi"] = fig_vi
    if not out.get("figures_en"):
        out["figures_en"] = fig_en or fig_vi

    # Explicit grounding (before cite tips). Do not clone bibliography into assessment.
    if not out.get("support_vi"):
        out["support_vi"] = [
            "Neo vào Minh chứng / toán / thuật toán phía trên — không sao chép lại toàn bộ Purpose.",
            "Hạn chế: điều kiện biên CSDL/demo; đối chiếu live sau Chạy.",
        ]
    if not out.get("support_en"):
        out["support_en"] = [
            "Grounded in Evidence / math / algorithm above — Purpose is not re-copied here.",
            "Limitation: CSDL/demo bounds; verify with live results after Run.",
        ]

    cites = _cites_from_package(pkg)
    if cites:
        n = len(cites)
        support_vi = list(out.get("support_vi") or [])
        support_en = list(out.get("support_en") or [])
        tip_vi = f"Dẫn chứng DOI: xem khối Trích dẫn phía trên ({n} mục)."
        tip_en = f"DOI citations: see the Citations block above ({n} items)."
        if tip_vi not in support_vi:
            support_vi.append(tip_vi)
        if tip_en not in support_en:
            support_en.append(tip_en)
        out["support_vi"] = support_vi
        out["support_en"] = support_en
    out.pop("citations", None)

    out["has_support"] = bool(
        out.get("evidence_vi")
        or out.get("evidence_en")
        or out.get("figures_vi")
        or out.get("figures_en")
        or out.get("citations")
    )
    return out


def enrich_assessment(
    step_id: int,
    assess: dict[str, Any] | None,
    package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    out = dict(assess or {})
    en = STEP_ASSESS_EN.get(step_id)
    if en:
        for k, v in en.items():
            out.setdefault(k, v)
    # Normalize packed "VI / EN" verdict overlays into explicit EN when missing
    for vi_key, en_key in (
        ("strength", "strength_en"),
        ("limitation", "limitation_en"),
        ("verdict", "verdict_en"),
    ):
        vi = out.get(vi_key)
        if isinstance(vi, str) and " / " in vi and not out.get(en_key):
            parts = [p.strip() for p in vi.split(" / ") if p.strip()]
            if len(parts) >= 2:
                out[vi_key] = parts[0]
                out[en_key] = parts[-1]
    return attach_assessment_support(out, package)
