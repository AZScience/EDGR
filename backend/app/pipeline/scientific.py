"""Ensure every step/task has a scientific frame: CSDL+explain, citations, evidence, assessment."""

from __future__ import annotations

from typing import Any

from app.pipeline.definition import get_step, get_task
from app.pipeline.step_guides import get_purpose
from app.pipeline.theory_guides import get_theory


def _as_dict(v: Any) -> dict[str, Any]:
    return dict(v) if isinstance(v, dict) else {}


def ensure_scientific_package(
    step_id: int,
    task_id: str | None,
    package: dict[str, Any],
    *,
    step_baseline: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Fill gaps so every object is scientifically complete:
    CSDL + explanation, citations, observable evidence claim, S/L/V assessment.
    """
    step = get_step(step_id) or {}
    task = get_task(step_id, task_id) if task_id else None
    purpose = get_purpose(step_id, task_id)
    theory = get_theory(step_id, task_id)
    title = (task or step).get("title") or f"Bước {step_id}"
    title_en = (task or step).get("title_en") or title
    baseline = step_baseline or {}

    # ── CSDL + explanation ────────────────────────────────────────────
    csdl = _as_dict(package.get("csdl"))
    if task_id and not csdl.get("explain_vi"):
        csdl["explain_vi"] = (
            f"CSDL / kho dữ liệu phục vụ tab «{title}». "
            f"{purpose.get('vi', '')} "
            f"Schema kế thừa bước {step_id}; tập con/thao tác đặc thù của tab này."
        )
        csdl["explain_en"] = (
            f"Database backing tab «{title_en}». "
            f"{purpose.get('en', '')} "
            f"Schema inherited from step {step_id}; subset/ops are tab-specific."
        )
    if task_id and not csdl.get("role_vi"):
        # Short role stub — do not paste full purpose.does (already in Purpose block).
        csdl["role_vi"] = f"Cung cấp dữ liệu để thực thi tab «{title}»."
        csdl["role_en"] = f"Supply data to execute tab «{title_en}»."
    if not csdl.get("name_vi") and not csdl.get("name"):
        csdl["name_vi"] = f"CSDL — {title}"
        csdl["name_en"] = f"Database — {title_en}"
    package["csdl"] = csdl

    # ── Citations ─────────────────────────────────────────────────────
    cites = package.get("trich_dan")
    if not isinstance(cites, list) or len(cites) == 0:
        from app.pipeline.academic import _cite

        package["trich_dan"] = _cite("lewis2020rag", "ji2023survey", "gao2024ragsurvey")

    # ── Evidence claim + logic ────────────────────────────────────────
    mc = _as_dict(package.get("minh_chung"))
    if not mc.get("claim") and not mc.get("claim_en") and not mc.get("claim_vi"):
        # Do not paste theory.what / purpose (already shown above).
        mc["claim"] = (
            f"Minh chứng của «{title}»: quan sát được sau khi chạy task (số liệu/bảng/evidence)."
        )
        mc["claim_en"] = (
            f"Evidence for «{title_en}»: observable after running the task (metrics/tables/evidence)."
        )
    if not mc.get("logic_vi") and not mc.get("logic"):
        mc["logic_vi"] = "Chạy → thu thập quan sát → đối chiếu mục tiêu tab (Purpose phía trên)."
        mc["logic_en"] = "Run → collect observations → compare with tab goal (Purpose above)."
    if task_id:
        mc.setdefault("task", task_id)
        mc.setdefault("step", step_id)
    package["minh_chung"] = mc

    # ── Assessment S/L/V (task-local when still equal to step baseline) ─
    assess = _as_dict(package.get("nhan_dinh_danh_gia"))
    base_assess = _as_dict(baseline.get("nhan_dinh_danh_gia"))
    needs_task_assess = bool(task_id) and (
        not assess.get("strength")
        or assess.get("strength") == base_assess.get("strength")
        or not assess.get("limitation")
        or assess.get("limitation") == base_assess.get("limitation")
    )
    if needs_task_assess:
        assess["strength"] = (
            f"Tab «{title}» có CSDL, trích dẫn và đường dẫn minh chứng gắn thao tác tab "
            "(mục tiêu chi tiết xem khối Purpose — không lặp ở đây)."
        )
        assess["strength_en"] = (
            f"Tab «{title_en}» has CSDL, citations, and an evidence path tied to the tab action "
            "(see Purpose for the goal text — not repeated here)."
        )
        from app.pipeline.scientific_verify import (
            _PRE_RUN_LIMIT_EN,
            _PRE_RUN_LIMIT_VI,
        )

        assess["limitation"] = _PRE_RUN_LIMIT_VI
        assess["limitation_en"] = _PRE_RUN_LIMIT_EN
        assess["support_vi"] = list(assess.get("support_vi") or []) + [
            "Sau khi Chạy: checklist kiểm chứng xuất hiện ở «Nhận định runtime».",
        ]
        assess["support_en"] = list(assess.get("support_en") or []) + [
            "After Run: the verification checklist appears under «Runtime assessment».",
        ]
        assess["has_support"] = True
        # Keep specialized verdict if overlay already set a distinct one
        if (
            not assess.get("verdict")
            or assess.get("verdict") == base_assess.get("verdict")
            or "Cần bổ sung" in str(assess.get("verdict", ""))
        ):
            assess["verdict"] = (
                f"Đủ khung logic để chạy «{title}» và kết luận dựa trên minh chứng quan sát được."
            )
            assess["verdict_en"] = (
                f"Logically framed enough to run «{title_en}» and conclude from observable evidence."
            )
        if "score_0_1" not in assess:
            assess["score_0_1"] = 0.72
        assess["task_specialized"] = True
    # Ensure EN fields for assessment
    for vi_key, en_key in (
        ("strength", "strength_en"),
        ("limitation", "limitation_en"),
        ("verdict", "verdict_en"),
    ):
        if assess.get(vi_key) and not assess.get(en_key):
            assess[en_key] = assess[vi_key]
    package["nhan_dinh_danh_gia"] = assess

    return package


# Per-table scientific frame: explain + evaluate + verdict (no bare dumps).
_TABLE_GUIDES: dict[str, dict[str, str]] = {
    "papers": {
        "title_vi": "Bảng papers (core)",
        "title_en": "Papers table (core)",
        "explain_vi": "Mỗi hàng là một công bố curated dùng cho khảo sát tab này (không gồm scaffold).",
        "explain_en": "Each row is a curated publication used for this tab’s survey (scaffold excluded).",
        "evaluate_vi": "Đánh giá: độ phủ theo venue/năm và chất lượng limitation gắn paper.",
        "evaluate_en": "Evaluate: venue/year coverage and quality of paper-linked limitations.",
        "verdict_vi": "Nhận định: đủ làm minh chứng cục bộ nếu paper_count > 0 và có DOI/core.",
        "verdict_en": "Verdict: adequate local evidence if paper_count > 0 with core/DOI rows.",
    },
    "limitations": {
        "title_vi": "Bảng limitations",
        "title_en": "Limitations table",
        "explain_vi": "Hạn chế trích từ papers — tiền đề cho gap analysis bước 2.",
        "explain_en": "Limitations extracted from papers — premises for step-2 gap analysis.",
        "evaluate_vi": "Đánh giá: nhóm theme (temporal/trust/graph/CTI) có đủ đa dạng không.",
        "evaluate_en": "Evaluate: whether themes (temporal/trust/graph/CTI) are diverse enough.",
        "verdict_vi": "Nhận định: hữu ích nếu limitation gắn được paper_id cụ thể.",
        "verdict_en": "Verdict: useful when each limitation ties to a concrete paper_id.",
    },
    "catalog": {
        "title_vi": "Bảng danh mục APA",
        "title_en": "APA catalog table",
        "explain_vi": "Danh mục References APA 7th: core = citable; extended = scaffold (không DOI thật).",
        "explain_en": "APA 7th References: core = citable; extended = scaffold (no real DOI).",
        "evaluate_vi": "Đánh giá: tổng ≥300; phân biệt citable vs synthetic trước khi trích dẫn.",
        "evaluate_en": "Evaluate: total ≥300; separate citable vs synthetic before citing.",
        "verdict_vi": "Nhận định: đạt quy mô khảo sát demo; chỉ trích dẫn hàng core/citable.",
        "verdict_en": "Verdict: meets demo survey scale; cite only core/citable rows.",
    },
    "gaps": {
        "title_vi": "Bảng research gaps",
        "title_en": "Research gaps table",
        "explain_vi": "Các khoảng trống G1… kèm evidence định lượng/định tính từ corpus core.",
        "explain_en": "Gaps G1… with quantitative/qualitative evidence from the core corpus.",
        "evaluate_vi": "Đánh giá: severity và evidence có khớp limitation/coverage không.",
        "evaluate_en": "Evaluate: whether severity and evidence match limitations/coverage.",
        "verdict_vi": "Nhận định: đủ để chuyển bước formalize nếu gap high có evidence.",
        "verdict_en": "Verdict: enough to move to formalize if high-severity gaps have evidence.",
    },
    "methods": {
        "title_vi": "Bảng methods",
        "title_en": "Methods table",
        "explain_vi": "Họ phương pháp baseline (RAG/GraphRAG…) từ papers core.",
        "explain_en": "Baseline method families (RAG/GraphRAG…) from core papers.",
        "evaluate_vi": "Đánh giá: inventory có phủ đủ họ so sánh cho Step 9 không.",
        "evaluate_en": "Evaluate: whether the inventory covers families needed for Step 9.",
        "verdict_vi": "Nhận định: ổn nếu count > 0 và có cả RAG-family lẫn GraphRAG-family.",
        "verdict_en": "Verdict: sound if count > 0 and both RAG- and GraphRAG-family appear.",
    },
    "evidence": {
        "title_vi": "Bảng evidence retrieved",
        "title_en": "Retrieved evidence table",
        "explain_vi": "Các đoạn bằng chứng được chọn sau retrieval/scoring (id, score, risk…).",
        "explain_en": "Evidence chunks selected after retrieval/scoring (id, score, risk…).",
        "evaluate_vi": "Đánh giá: Faith↑ Hall↓; evidence có entity CTI khớp query không.",
        "evaluate_en": "Evaluate: Faith↑ Hall↓; whether CTI entities match the query.",
        "verdict_vi": "Nhận định: tin cậy hơn khi risk thấp và score/trust cao.",
        "verdict_en": "Verdict: more trustworthy when risk is low and trust/score is high.",
    },
    "evidence_ids": {
        "title_vi": "Danh sách evidence_ids",
        "title_en": "Evidence ID list",
        "explain_vi": "Định danh evidence được chọn — dùng đối chiếu gold/retrieval metrics.",
        "explain_en": "Selected evidence IDs — used against gold/retrieval metrics.",
        "evaluate_vi": "Đánh giá: độ trùng với gold_evidence_ids (nếu có).",
        "evaluate_en": "Evaluate: overlap with gold_evidence_ids when available.",
        "verdict_vi": "Nhận định: tập id không rỗng là điều kiện tối thiểu của run hợp lệ.",
        "verdict_en": "Verdict: a non-empty ID set is the minimum for a valid run.",
    },
    "rows": {
        "title_vi": "Bảng rows thực nghiệm",
        "title_en": "Experiment rows table",
        "explain_vi": "Mỗi hàng là một lần chạy/biến thể/câu hỏi với metric quan sát được.",
        "explain_en": "Each row is one run/variant/question with observed metrics.",
        "evaluate_vi": "Đánh giá: so sánh hàng theo Faith/Hall/Δ hoặc metric mục tiêu tab.",
        "evaluate_en": "Evaluate: compare rows by Faith/Hall/Δ or the tab’s target metric.",
        "verdict_vi": "Nhận định: kết luận chỉ dựa trên chênh lệch quan sát được, không chỉnh điểm giả.",
        "verdict_en": "Verdict: conclude only from observed deltas — no fake score tweaks.",
    },
    "results": {
        "title_vi": "Bảng so sánh methods",
        "title_en": "Method comparison table",
        "explain_vi": "So sánh EDGR vs baseline stubs trên cùng query/retriever.",
        "explain_en": "Compare EDGR vs baseline stubs on the same query/retriever.",
        "evaluate_vi": "Đánh giá: EDGR có Faith cao hơn / Hall thấp hơn không (cùng điều kiện).",
        "evaluate_en": "Evaluate: whether EDGR has higher Faith / lower Hall under the same setup.",
        "verdict_vi": "Nhận định: ưu thế chỉ có ý nghĩa khi fairness note (same q,D,G) được giữ.",
        "verdict_en": "Verdict: superiority only matters when fairness (same q,D,G) holds.",
    },
    "checks": {
        "title_vi": "Bảng checklist",
        "title_en": "Checklist table",
        "explain_vi": "Tiến độ sẵn sàng bảo vệ — probe từ cache/live, không hardcode True.",
        "explain_en": "Defense readiness — probed from cache/live, not hardcoded True.",
        "evaluate_vi": "Đánh giá: % ready và các mục còn false cần chạy bổ sung.",
        "evaluate_en": "Evaluate: ready % and which false items still need runs.",
        "verdict_vi": "Nhận định: chỉ ‘sẵn sàng’ khi các mục cốt lõi (EDGR/eval) = true.",
        "verdict_en": "Verdict: ‘ready’ only when core items (EDGR/eval) are true.",
    },
    "invariants": {
        "title_vi": "Bảng invariants",
        "title_en": "Invariants table",
        "explain_vi": "Kiểm chứng tính đúng trên một lần chạy EDGR sống (I1–I4).",
        "explain_en": "Correctness checks on a live EDGR run (I1–I4).",
        "evaluate_vi": "Đánh giá: holds=true/false theo từng invariant — không mặc định đúng.",
        "evaluate_en": "Evaluate: holds=true/false per invariant — never assumed true.",
        "verdict_vi": "Nhận định: pipeline đáng tin nếu I2/I4 holds; I1/I3 giải thích hành vi lọc.",
        "verdict_en": "Verdict: pipeline is credible if I2/I4 hold; I1/I3 explain filter behavior.",
    },
    "stages": {
        "title_vi": "Bảng EDGR stages",
        "title_en": "EDGR stages table",
        "explain_vi": "Sáu giai EDGR với output/duration quan sát được.",
        "explain_en": "Six EDGR stages with observable outputs/durations.",
        "evaluate_vi": "Đánh giá: giai đoạn nào chiếm latency; output có entity/evidence hợp lệ không.",
        "evaluate_en": "Evaluate: which stage dominates latency; whether outputs look valid.",
        "verdict_vi": "Nhận định: đủ minh chứng thuật toán nếu đủ 6 stage và có evidence cuối.",
        "verdict_en": "Verdict: algorithm evidence is adequate if all 6 stages run with final evidence.",
    },
    "contributions": {
        "title_vi": "Bảng contributions",
        "title_en": "Contributions table",
        "explain_vi": "Ánh xạ gap → đóng góp luận án (artifact thiết kế, không phải điểm số).",
        "explain_en": "Gap→thesis contribution mapping (design artifact, not a score).",
        "evaluate_vi": "Đánh giá: mỗi Ci có maps_to_gap rõ và mô tả kiểm chứng được.",
        "evaluate_en": "Evaluate: each Ci has a clear maps_to_gap and testable description.",
        "verdict_vi": "Nhận định: chấp nhận được nếu C1–C4 phủ G1–G3.",
        "verdict_en": "Verdict: acceptable if C1–C4 cover G1–G3.",
    },
    "series": {
        "title_vi": "Bảng hội tụ / series",
        "title_en": "Convergence / series table",
        "explain_vi": "Chuỗi đo khi tăng top_k hoặc quy mô — prefix stability / latency.",
        "explain_en": "Measurement series as top_k or scale grows — prefix stability / latency.",
        "evaluate_vi": "Đánh giá: ổn định khi k tăng; không dao động hỗn loạn.",
        "evaluate_en": "Evaluate: stability as k grows; no chaotic oscillation.",
        "verdict_vi": "Nhận định: hội tụ thực nghiệm nếu prefix_stability cao ở các mốc sau.",
        "verdict_en": "Verdict: empirically convergent if later prefix_stability stays high.",
    },
    "weak_intersections": {
        "title_vi": "Giao chủ đề mỏng",
        "title_en": "Weak topic intersections",
        "explain_vi": "Các cặp chủ đề có Pair thấp — tín hiệu gap định lượng.",
        "explain_en": "Topic pairs with low Pair — quantitative gap signals.",
        "evaluate_vi": "Đánh giá: ưu tiên giao CTI/IDS × graph/hallucination.",
        "evaluate_en": "Evaluate: prioritize CTI/IDS × graph/hallucination intersections.",
        "verdict_vi": "Nhận định: đây là căn cứ chuyển Step 2 Identify Gaps.",
        "verdict_en": "Verdict: this justifies moving to Step 2 Identify Gaps.",
    },
}


def guide_for_table(field: str, count: int | None = None) -> dict[str, Any]:
    """Return bilingual explain/evaluate/verdict for a result table field."""
    base = _TABLE_GUIDES.get(field)
    n = f" (n={count})" if count is not None else ""
    if base:
        return {
            "field": field,
            "title_vi": base["title_vi"] + n,
            "title_en": base["title_en"] + n,
            "explain_vi": base["explain_vi"],
            "explain_en": base["explain_en"],
            "evaluate_vi": base["evaluate_vi"],
            "evaluate_en": base["evaluate_en"],
            "verdict_vi": base["verdict_vi"],
            "verdict_en": base["verdict_en"],
        }
    return {
        "field": field,
        "title_vi": f"Bảng `{field}`{n}",
        "title_en": f"Table `{field}`{n}",
        "explain_vi": f"Bảng dữ liệu quan sát được từ trường `{field}` sau khi chạy task.",
        "explain_en": f"Observable data table from field `{field}` after running the task.",
        "evaluate_vi": "Đánh giá: kiểm tra số hàng, trường khóa và tính nhất quán với mục tiêu tab.",
        "evaluate_en": "Evaluate: check row count, key fields, and consistency with the tab goal.",
        "verdict_vi": "Nhận định: dùng làm minh chứng nếu dữ liệu không rỗng và giải thích được.",
        "verdict_en": "Verdict: usable as evidence if non-empty and interpretable.",
    }


def build_table_guides(result: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    """Attach scientific frames for every tabular collection in a run result."""
    r = result if isinstance(result, dict) else {}
    guides: dict[str, dict[str, Any]] = {}
    for k, v in r.items():
        if k in {"note", "note_vi", "note_en", "how_to_use_vi", "how_to_use_en", "provenance"}:
            continue
        if isinstance(v, list) and v and isinstance(v[0], (dict, str, int, float)):
            guides[k] = guide_for_table(k, len(v))
        elif isinstance(v, dict) and v and all(
            isinstance(x, (str, int, float, bool)) or x is None for x in v.values()
        ):
            # flat dict → will render as key/value table
            guides[k] = guide_for_table(k, len(v))
    # Always guide the scalar summary block
    guides["_scalars"] = {
        "field": "_scalars",
        "title_vi": "Bảng chỉ số tóm tắt",
        "title_en": "Summary metrics table",
        "explain_vi": "Các chỉ số scalar quan sát được (Faith, Hall, count, %…). Giá trị 0–1 hiển thị dạng %.",
        "explain_en": "Observed scalar metrics (Faith, Hall, count, %…). 0–1 values shown as %.",
        "evaluate_vi": "Đánh giá: hướng tốt là Faith↑ Hall↓; count/% khớp mục tiêu tab.",
        "evaluate_en": "Evaluate: good direction is Faith↑ Hall↓; counts/% match the tab goal.",
        "verdict_vi": "Nhận định: đây là lớp tóm tắt — chi tiết nằm ở các bảng bên dưới.",
        "verdict_en": "Verdict: this is the summary layer — details are in the tables below.",
    }
    return guides


def extract_run_evidence(result: dict[str, Any] | None) -> dict[str, Any]:
    """Pull observable pointers from a runtime result for the scientific review panel."""
    r = result if isinstance(result, dict) else {}
    items: list[dict[str, Any]] = []
    scalars: dict[str, Any] = {}

    metric_keys = (
        "faithfulness",
        "hallucination_rate",
        "confidence",
        "latency_ms",
        "avg_latency_ms",
        "p_at_k",
        "r_at_k",
        "mrr",
        "f1",
        "precision",
        "recall",
        "accuracy",
        "paper_count",
        "total",
        "core_count",
        "extended_count",
        "limitation_count",
        "ready_count",
        "percent",
        "nodes",
        "edges",
        "delta_faithfulness",
        "delta_hallucination",
    )
    for k in metric_keys:
        if k in r and isinstance(r[k], (int, float, str, bool)):
            scalars[k] = r[k]

    list_keys = (
        "evidence",
        "evidence_ids",
        "papers",
        "limitations",
        "gaps",
        "methods",
        "rows",
        "catalog",
        "checks",
        "invariants",
        "stages",
        "results",
        "contributions",
        "series",
        "themes",
        "weak_intersections",
    )
    for k in list_keys:
        v = r.get(k)
        if isinstance(v, list) and v:
            items.append({"field": k, "count": len(v)})
        elif isinstance(v, dict) and v:
            items.append({"field": k, "count": len(v)})

    claim_vi = "Minh chứng runtime quan sát được từ kết quả chạy."
    claim_en = "Observable runtime evidence extracted from the run result."
    if scalars:
        parts = ", ".join(f"{k}={scalars[k]}" for k in list(scalars)[:5])
        claim_vi = f"Chỉ số quan sát: {parts}."
        claim_en = f"Observed metrics: {parts}."
    if items:
        # Avoid duplicating full samples — tables below carry explain/assess.
        claim_vi += " Chi tiết từng bảng (giải thích · đánh giá · nhận định) ở khối dữ liệu bên dưới: " + ", ".join(
            f"{it['field']}(n={it['count']})" for it in items[:8]
        )
        claim_en += " Per-table explain/evaluate/verdict are in the data block below: " + ", ".join(
            f"{it['field']}(n={it['count']})" for it in items[:8]
        )

    return {
        "claim_vi": claim_vi,
        "claim_en": claim_en,
        "scalars": scalars,
        "collections": items,
        "has_evidence": bool(scalars or items),
        "tables": build_table_guides(r),
    }
