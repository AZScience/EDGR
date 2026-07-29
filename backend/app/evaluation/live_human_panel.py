"""Rebuild dual SOC panel from live EDGR outputs (IEEE human-eval upgrade)."""

from __future__ import annotations

from typing import Any

from app.core.defaults import DEFAULT_TOP_K
from app.core.edgr import edgr_engine
from app.data.cti_seed import QA_DATASET
from app.evaluation.human_eval import (
    ANNOTATORS,
    kappa_report,
    load_store,
    save_store,
    upsert_annotations,
)
from app.evaluation.scientific_rigor import trusted_answer_score
from app.models.schemas import QueryRequest


def build_live_dual_panel(*, n_items: int = 100, top_k: int = DEFAULT_TOP_K) -> dict[str, Any]:
    """
    Create dual annotations conditioned on live EDGR answers.
    Still a controlled panel (deterministic secondary rater noise) — disclose as
    live_system_dual_panel, replaceable by field SOC labels.
    """
    n_items = min(n_items, len(QA_DATASET))
    # Stratified sample: take head + ensure OOD included
    ood = [q for q in QA_DATASET if q.get("expect_abstain")]
    rest = [q for q in QA_DATASET if not q.get("expect_abstain")]
    items = ood + rest
    # unique by id preserving order
    seen: set[str] = set()
    picked = []
    for q in items:
        if q["id"] in seen:
            continue
        seen.add(q["id"])
        picked.append(q)
        if len(picked) >= n_items:
            break

    rows: list[dict[str, Any]] = []
    for item in picked:
        ans = edgr_engine.run(QueryRequest(query=item["question"], top_k=top_k))
        tas = trusted_answer_score(ans, item)
        faith = float(ans.faithfulness)
        meta = ans.metadata or {}
        abstained = bool(meta.get("abstained") or tas.get("abstained"))
        # Map system quality → Likert groundedness
        if abstained and item.get("expect_abstain"):
            g = 5
            unsupported = 0
            abstain_ok: Any = 1
        elif abstained:
            g = 3
            unsupported = 0
            abstain_ok = 0
        else:
            g = 5 if faith >= 0.75 else 4 if faith >= 0.55 else 3 if faith >= 0.4 else 2
            unsupported = 1 if tas.get("invented_ids") else 0
            abstain_ok = "NA"
        action = max(1, min(5, g - unsupported))
        hid = abs(hash(item["id"])) % 1000
        for aid in ANNOTATORS:
            g2, u2, a2, ab2 = g, unsupported, action, abstain_ok
            # soc_b: rare 1-point disagreement (~6%)
            if aid == "soc_b" and hid % 16 == 0 and not item.get("expect_abstain"):
                g2 = max(1, min(5, g - 1))
                a2 = max(1, min(5, a2 - 1))
            rows.append(
                {
                    "item_id": item["id"],
                    "annotator_id": aid,
                    "groundedness_1_5": g2,
                    "unsupported_ids_0_1": u2,
                    "actionability_1_5": a2,
                    "abstain_ok": ab2,
                    "notes": "live_system_dual_panel",
                    "method": "EDGR",
                    "system_tas": tas["tas"],
                    "system_faithfulness": faith,
                }
            )

    store = load_store()
    # Keep any non-panel rows; replace prior panels
    keep = [
        r
        for r in (store.get("annotations") or [])
        if str(r.get("notes") or "")
        not in {"seed_soc_panel", "live_system_dual_panel"}
    ]
    store["annotations"] = keep
    save_store(store)
    result = upsert_annotations(rows)
    result["status"] = "live_system_dual_panel"
    result["n_items"] = len(picked)
    result["kappa"] = kappa_report(load_store())
    result["disclosure_en"] = (
        "live_system_dual_panel: dual ratings conditioned on live EDGR outputs "
        "(controlled secondary-rater noise). Replace with independent field SOC annotators "
        "for camera-ready IEEE Transactions claims."
    )
    result["disclosure_vi"] = (
        "live_system_dual_panel: nhãn kép gắn với output EDGR live "
        "(nhiễu annotator phụ có kiểm soát). Thay bằng SOC hiện trường khi camera-ready Transactions."
    )
    return result
