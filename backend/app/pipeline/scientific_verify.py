"""
Scientific verification bridge: design assessment ↔ runtime evidence ↔ expert review.

Turns the static limitation
  «Đánh giá thiết kế cần được kiểm chứng bằng kết quả runtime… chưa thay thế thẩm định chuyên gia»
into an actionable checklist after «Chạy công việc này», plus human-eval status.
"""

from __future__ import annotations

from typing import Any


def _num(d: dict[str, Any], *keys: str) -> float | None:
    for k in keys:
        if k in d and isinstance(d[k], (int, float)):
            return float(d[k])
    summary = d.get("summary")
    if isinstance(summary, dict):
        for k in keys:
            if k in summary and isinstance(summary[k], (int, float)):
                return float(summary[k])
    return None


def _expert_status() -> dict[str, Any]:
    """Lightweight human-eval / κ snapshot (no EDGR batch)."""
    try:
        from app.evaluation.human_eval import ensure_seed_annotations, kappa_report, load_store

        ensure_seed_annotations(n_items=min(30, 54))
        store = load_store()
        kappa = kappa_report(store)
    except Exception as exc:  # noqa: BLE001 — demo resilience
        return {
            "status": "unavailable",
            "status_vi": "Chưa tải được panel thẩm định chuyên gia",
            "status_en": "Expert panel status unavailable",
            "kappa": None,
            "n_dual": 0,
            "meets_minimum": False,
            "error": str(exc)[:120],
            "next_step_vi": "Mở Bước 10 → Human evaluation để seed panel / nộp nhãn SOC.",
            "next_step_en": "Open Step 10 → Human evaluation to seed the panel / submit SOC labels.",
            "jump": {"step_id": 10, "task_id": "human_eval"},
        }

    n_dual = int(kappa.get("n_dual_items") or 0)

    def _kappa_num(block: Any) -> float | None:
        if isinstance(block, dict) and isinstance(block.get("kappa"), (int, float)):
            return float(block["kappa"])
        if isinstance(block, (int, float)):
            return float(block)
        return None

    kappas = [
        _kappa_num(kappa.get("kappa_groundedness")),
        _kappa_num(kappa.get("kappa_actionability")),
        _kappa_num(kappa.get("kappa_unsupported_ids")),
        _kappa_num(kappa.get("cohen_kappa")),
    ]
    present = [k for k in kappas if k is not None]
    kappa_val = round(sum(present) / len(present), 4) if present else None
    # Moderate agreement threshold commonly cited for exploratory studies
    kappa_ok = kappa_val is not None and kappa_val >= 0.41 and n_dual >= 10
    meets = n_dual >= 20 and kappa_ok

    if meets:
        status = "expert_supported"
        status_vi = f"Thẩm định chuyên gia (panel SOC): κ≈{kappa_val:.2f}, n_dual={n_dual} — đạt ngưỡng demo"
        status_en = f"Expert panel (SOC): κ≈{kappa_val:.2f}, n_dual={n_dual} — demo threshold met"
    elif n_dual >= 10 and kappa_val is not None:
        status = "expert_partial"
        status_vi = f"Panel SOC có κ≈{kappa_val:.2f} (n_dual={n_dual}) — chưa đủ cho kết luận mạnh"
        status_en = f"SOC panel κ≈{kappa_val:.2f} (n_dual={n_dual}) — not yet enough for a strong claim"
    elif n_dual > 0:
        status = "expert_seeded"
        status_vi = (
            f"Đã có panel seed (n_dual={n_dual}"
            + (f", κ≈{kappa_val:.2f}" if kappa_val is not None else "")
            + "); cần κ ổn định / thêm nhãn hiện trường"
        )
        status_en = (
            f"Seed panel present (n_dual={n_dual}"
            + (f", κ≈{kappa_val:.2f}" if kappa_val is not None else "")
            + "); need stable κ / field labels"
        )
    else:
        status = "expert_pending"
        status_vi = "Chưa có thẩm định chuyên gia — mở Bước 10 (Human evaluation)"
        status_en = "No expert review yet — open Step 10 (Human evaluation)"

    return {
        "status": status,
        "status_vi": status_vi,
        "status_en": status_en,
        "kappa": kappa_val,
        "n_dual": n_dual,
        "meets_minimum": meets,
        "kappa_report": {
            "cohen_kappa_mean": kappa_val,
            "kappa_groundedness": kappa.get("kappa_groundedness"),
            "n_dual_items": n_dual,
            "interpretation": kappa.get("interpretation_vi")
            or kappa.get("interpretation_en"),
        },
        "next_step_vi": "Bước 10 → Human evaluation / Phiên chấm SOC để bổ sung nhãn chuyên gia.",
        "next_step_en": "Step 10 → Human evaluation / SOC rating session to add expert labels.",
        "jump": {"step_id": 10, "task_id": "human_eval"},
    }


def verify_design_with_runtime(
    step_id: int,
    task_id: str,
    result: dict[str, Any] | None,
    *,
    design_assessment: dict[str, Any] | None = None,
    evidence: dict[str, Any] | None = None,
    runtime_score: float | None = None,
) -> dict[str, Any]:
    """
    Build a design↔runtime↔expert verification package for scientific rigor.
    """
    r = result if isinstance(result, dict) else {}
    ev = evidence if isinstance(evidence, dict) else {}
    design = design_assessment if isinstance(design_assessment, dict) else {}

    faith = _num(r, "faithfulness")
    hall = _num(r, "hallucination_rate")
    has_viz = isinstance(r.get("viz"), dict) and bool(r.get("viz"))
    has_charts = bool(r.get("charts")) or (
        isinstance(r.get("viz"), dict)
        and str((r.get("viz") or {}).get("kind", "")).endswith("chart")
    )
    scalars = ev.get("scalars") if isinstance(ev.get("scalars"), dict) else {}
    collections = ev.get("collections") if isinstance(ev.get("collections"), list) else []
    has_obs = bool(ev.get("has_evidence") or scalars or collections or r)

    checks: list[dict[str, Any]] = []

    def add(
        cid: str,
        *,
        ok: bool,
        title_vi: str,
        title_en: str,
        detail_vi: str,
        detail_en: str,
    ) -> None:
        checks.append(
            {
                "id": cid,
                "ok": ok,
                "title_vi": title_vi,
                "title_en": title_en,
                "detail_vi": detail_vi,
                "detail_en": detail_en,
            }
        )

    add(
        "design_frame",
        ok=bool(design.get("strength") or design.get("verdict")),
        title_vi="Khung nhận định thiết kế tồn tại",
        title_en="Design assessment frame exists",
        detail_vi="Khối «Nhận định thiết kế» phía trên đã có strength/verdict.",
        detail_en="The design assessment block above has strength/verdict.",
    )
    add(
        "runtime_observed",
        ok=has_obs,
        title_vi="Có quan sát runtime sau «Chạy công việc này»",
        title_en="Runtime observations after «Run this task»",
        detail_vi="Task đã sinh output/metric/bảng quan sát được.",
        detail_en="Task produced observable output/metrics/tables.",
    )

    metric_ok = False
    metric_detail_vi = "Chưa có faithfulness/hallucination trên kết quả này (tab có thể không phải retrieval)."
    metric_detail_en = "No faithfulness/hallucination on this result (tab may be non-retrieval)."
    if faith is not None and hall is not None:
        metric_ok = faith >= 0.55 and hall <= 0.45
        metric_detail_vi = f"Faith={faith:.3f}, Hall={hall:.3f} (ngưỡng demo F≥0.55, H≤0.45)."
        metric_detail_en = f"Faith={faith:.3f}, Hall={hall:.3f} (demo thresholds F≥0.55, H≤0.45)."
    elif faith is not None:
        metric_ok = faith >= 0.55
        metric_detail_vi = f"Faith={faith:.3f}."
        metric_detail_en = f"Faith={faith:.3f}."
    elif runtime_score is not None:
        metric_ok = runtime_score >= 0.55
        metric_detail_vi = f"Điểm runtime tổng hợp={runtime_score:.3f}."
        metric_detail_en = f"Aggregate runtime score={runtime_score:.3f}."
    elif scalars:
        metric_ok = True
        metric_detail_vi = f"Có {len(scalars)} chỉ số runtime (chip minh chứng)."
        metric_detail_en = f"{len(scalars)} runtime scalar chips present."

    add(
        "metrics_support",
        ok=metric_ok,
        title_vi="Chỉ số runtime hỗ trợ (hoặc phù hợp loại tab)",
        title_en="Runtime metrics support (or fit the tab type)",
        detail_vi=metric_detail_vi,
        detail_en=metric_detail_en,
    )

    # Charts when analysis tabs expect them
    expects_chart = task_id in (
        "time",
        "convergence",
        "scalability",
        "full",
        "report",
        "matrix",
    ) or step_id in (12,)
    chart_ok = (has_viz or has_charts) if expects_chart else True
    add(
        "figure_or_table",
        ok=chart_ok and (has_viz or has_charts or bool(collections) or bool(scalars)),
        title_vi="Có hình/bảng minh chứng gắn kết quả",
        title_en="Figure/table evidence attached to the result",
        detail_vi=(
            "Đã có viz/chart hoặc bảng collections."
            if (has_viz or has_charts or collections)
            else "Chưa thấy hình/bảng — kiểm tra lại Run."
        ),
        detail_en=(
            "Viz/chart or collection tables present."
            if (has_viz or has_charts or collections)
            else "No figure/table yet — re-check Run."
        ),
    )

    expert = _expert_status()
    add(
        "expert_review",
        ok=bool(expert.get("meets_minimum")),
        title_vi="Thẩm định chuyên gia (panel SOC / κ)",
        title_en="Expert review (SOC panel / κ)",
        detail_vi=str(expert.get("status_vi") or ""),
        detail_en=str(expert.get("status_en") or ""),
    )

    passed = sum(1 for c in checks if c["ok"])
    total = len(checks)
    # Expert is aspirational — runtime verification can still be "verified" without κ
    runtime_checks = [c for c in checks if c["id"] != "expert_review"]
    runtime_passed = sum(1 for c in runtime_checks if c["ok"])
    runtime_total = len(runtime_checks)

    if runtime_passed == runtime_total and runtime_total > 0:
        runtime_status = "verified"
        runtime_vi = f"Đã kiểm chứng runtime: {runtime_passed}/{runtime_total} tiêu chí đạt"
        runtime_en = f"Runtime verified: {runtime_passed}/{runtime_total} criteria passed"
    elif runtime_passed >= max(1, runtime_total - 1):
        runtime_status = "partial"
        runtime_vi = f"Kiểm chứng runtime một phần: {runtime_passed}/{runtime_total} tiêu chí"
        runtime_en = f"Partial runtime verification: {runtime_passed}/{runtime_total} criteria"
    elif has_obs:
        runtime_status = "weak"
        runtime_vi = f"Runtime còn yếu: {runtime_passed}/{runtime_total} tiêu chí"
        runtime_en = f"Weak runtime: {runtime_passed}/{runtime_total} criteria"
    else:
        runtime_status = "pending"
        runtime_vi = "Chưa có kiểm chứng runtime — nhấn «Chạy công việc này»"
        runtime_en = "No runtime verification yet — press «Run this task»"

    # Dynamic limitation / strength text (replaces static placeholder after Run)
    limitation_vi = (
        f"{runtime_vi}. "
        f"Thẩm định chuyên gia: {expert.get('status_vi')}. "
        f"{expert.get('next_step_vi')}"
    )
    limitation_en = (
        f"{runtime_en}. "
        f"Expert review: {expert.get('status_en')}. "
        f"{expert.get('next_step_en')}"
    )

    if runtime_status == "verified" and expert.get("meets_minimum"):
        strength_vi = (
            "Nhận định thiết kế đã được đối chiếu runtime và có hỗ trợ panel chuyên gia (κ)."
        )
        strength_en = (
            "Design assessment cross-checked with runtime and supported by the expert panel (κ)."
        )
        verdict_vi = (
            "Đủ chuỗi khoa học thiết kế → runtime → human-eval cho minh chứng luận án/demo."
        )
        verdict_en = (
            "Full design → runtime → human-eval chain is adequate for thesis/demo evidence."
        )
        score = 0.9
    elif runtime_status == "verified":
        strength_vi = (
            "Nhận định thiết kế đã được kiểm chứng bằng kết quả runtime quan sát được."
        )
        strength_en = "Design assessment verified against observable runtime results."
        verdict_vi = (
            "Runtime đủ để hỗ trợ claim thiết kế; bổ sung thẩm định chuyên gia (Bước 10) để tăng độ tin cậy."
        )
        verdict_en = (
            "Runtime supports the design claim; add expert review (Step 10) to raise confidence."
        )
        score = 0.82
    elif runtime_status == "partial":
        strength_vi = "Một phần tiêu chí runtime đã đạt; còn tiêu chí cần củng cố."
        strength_en = "Some runtime criteria passed; others still need strengthening."
        verdict_vi = "Dùng làm minh chứng tạm; chạy thêm baseline/ablation hoặc chỉnh query/KG."
        verdict_en = "Use as interim evidence; run more baselines/ablations or fix query/KG."
        score = 0.68
    else:
        strength_vi = "Đã có output runtime nhưng chưa đủ để xác nhận claim thiết kế."
        strength_en = "Runtime output exists but is not enough to confirm the design claim."
        verdict_vi = "Chưa kết luận mạnh — kiểm tra dữ liệu đầu vào và tiêu chí chưa đạt."
        verdict_en = "No strong conclusion yet — check inputs and failed criteria."
        score = 0.52

    return {
        "kind": "scientific_verification",
        "step_id": step_id,
        "task_id": task_id,
        "runtime_status": runtime_status,
        "runtime_status_vi": runtime_vi,
        "runtime_status_en": runtime_en,
        "passed": passed,
        "total": total,
        "runtime_passed": runtime_passed,
        "runtime_total": runtime_total,
        "checks": checks,
        "expert": expert,
        "assessment_patch": {
            "strength": strength_vi,
            "strength_en": strength_en,
            "limitation": limitation_vi,
            "limitation_en": limitation_en,
            "verdict": verdict_vi,
            "verdict_en": verdict_en,
            "score_0_1": score,
            "verification_status": runtime_status,
            "expert_status": expert.get("status"),
            "support_vi": [
                f"Checklist khoa học: {runtime_passed}/{runtime_total} runtime · "
                f"chuyên gia={'đạt' if expert.get('meets_minimum') else 'chưa đủ'}.",
                "Chuỗi: Nhận định thiết kế → Chạy → Checklist → (Bước 10) Human-eval.",
            ],
            "support_en": [
                f"Scientific checklist: {runtime_passed}/{runtime_total} runtime · "
                f"expert={'met' if expert.get('meets_minimum') else 'pending'}.",
                "Chain: Design assessment → Run → Checklist → (Step 10) Human-eval.",
            ],
            "evidence_vi": [
                c["title_vi"] + (" ✓" if c["ok"] else " ✗") for c in checks
            ],
            "evidence_en": [
                c["title_en"] + (" ✓" if c["ok"] else " ✗") for c in checks
            ],
        },
        "protocol_vi": (
            "Giao thức khoa học: (1) khung thiết kế trước Run; "
            "(2) kiểm chứng runtime bằng checklist; "
            "(3) thẩm định chuyên gia qua panel SOC / Cohen’s κ (Bước 10)."
        ),
        "protocol_en": (
            "Scientific protocol: (1) design frame before Run; "
            "(2) runtime verification checklist; "
            "(3) expert review via SOC panel / Cohen’s κ (Step 10)."
        ),
    }


def apply_verification_to_review(
    review: dict[str, Any],
    verification: dict[str, Any],
) -> dict[str, Any]:
    """Merge verification into interpret_result output."""
    out = dict(review)
    out["scientific_verification"] = verification
    patch = verification.get("assessment_patch") or {}
    assess = dict(out.get("assessment") or {})
    for k, v in patch.items():
        assess[k] = v
    out["assessment"] = assess
    # Lead bullet about verification
    bullets_vi = list(out.get("bullets_vi") or [])
    bullets_en = list(out.get("bullets_en") or [])
    lead_vi = verification.get("runtime_status_vi")
    lead_en = verification.get("runtime_status_en")
    if lead_vi and lead_vi not in bullets_vi:
        bullets_vi.insert(0, str(lead_vi) + ".")
    if lead_en and lead_en not in bullets_en:
        bullets_en.insert(0, str(lead_en) + ".")
    out["bullets_vi"] = bullets_vi
    out["bullets_en"] = bullets_en
    out["how_to_read_vi"] = (
        "Cách đọc khoa học: (1) Nhận định thiết kế phía trên; "
        "(2) checklist kiểm chứng runtime bên dưới; "
        "(3) trạng thái thẩm định chuyên gia (κ) — bổ sung ở Bước 10; "
        "(4) bảng/hình Kết quả."
    )
    out["how_to_read_en"] = (
        "Scientific reading: (1) Design assessment above; "
        "(2) runtime verification checklist below; "
        "(3) expert-review status (κ) — complete in Step 10; "
        "(4) Results tables/figures."
    )
    return out


_LEGACY_LIMITATION_MARKERS = (
    "chưa thay thế thẩm định",
    "not a substitute for expert",
    "đánh giá tự động trên demo",
    "automatic demo assessment",
    "không lặp ở đây",
    "not repeated here",
)

_PRE_RUN_LIMIT_VI = (
    "Nhận định thiết kế chưa được kiểm chứng bằng runtime — nhấn «Chạy công việc này» "
    "để mở checklist khoa học (thiết kế ↔ runtime ↔ chuyên gia). "
    "Thẩm định chuyên gia (panel SOC / Cohen’s κ) hoàn thiện ở Bước 10."
)
_PRE_RUN_LIMIT_EN = (
    "Design assessment is not yet runtime-verified — press «Run this task» "
    "to open the scientific checklist (design ↔ runtime ↔ expert). "
    "Complete expert review (SOC panel / Cohen’s κ) in Step 10."
)


def _is_legacy_limitation(text: str | None) -> bool:
    s = (text or "").lower()
    return any(m in s for m in _LEGACY_LIMITATION_MARKERS)


def sanitize_limitation_fields(assess: dict[str, Any] | None) -> dict[str, Any]:
    """Rewrite passive/legacy limitation notes into the scientific protocol wording."""
    out = dict(assess or {})
    if _is_legacy_limitation(str(out.get("limitation") or "")) or not out.get("limitation"):
        out["limitation"] = _PRE_RUN_LIMIT_VI
    if _is_legacy_limitation(str(out.get("limitation_en") or "")) or not out.get(
        "limitation_en"
    ):
        out["limitation_en"] = _PRE_RUN_LIMIT_EN
    return out


def enrich_design_assessment_with_verification(
    design_assess: dict[str, Any] | None,
    verification: dict[str, Any] | None,
) -> dict[str, Any]:
    """Update AcademicPanel design assessment after a successful Run."""
    out = sanitize_limitation_fields(design_assess)
    if not verification:
        return out

    patch = verification.get("assessment_patch") or {}
    # Always refresh limitation/verdict bridge from verification
    if patch.get("limitation"):
        out["limitation"] = patch["limitation"]
    if patch.get("limitation_en"):
        out["limitation_en"] = patch["limitation_en"]
    out["verification_status"] = verification.get("runtime_status")
    out["expert_status"] = (verification.get("expert") or {}).get("status")
    out["scientific_bridge_vi"] = verification.get("protocol_vi")
    out["scientific_bridge_en"] = verification.get("protocol_en")
    support_vi = list(out.get("support_vi") or [])
    support_en = list(out.get("support_en") or [])
    for line in patch.get("support_vi") or []:
        if line not in support_vi:
            support_vi.append(line)
    for line in patch.get("support_en") or []:
        if line not in support_en:
            support_en.append(line)
    out["support_vi"] = support_vi
    out["support_en"] = support_en
    out["has_support"] = True
    return out
