"""PhD-grade scientific protocol: hypotheses, stats, validity, human-eval rubric."""

from __future__ import annotations

import math
import random
from collections import Counter
from typing import Any

from app.core.defaults import DEFAULT_TOP_K
from app.core.edgr import edgr_engine
from app.core.knowledge_graph import kg
from app.core.vector_store import vector_store
from app.data.cti_seed import EVIDENCE_CHUNKS, QA_DATASET
from app.models.schemas import QueryRequest


# ── Testable contribution hypotheses (paper-facing) ───────────────────

HYPOTHESES: list[dict[str, str]] = [
    {
        "id": "H1",
        "vi": "EDGR đạt faithfulness trung bình cao hơn RAG phẳng trên cùng QA_DATASET (cùng store).",
        "en": "EDGR achieves higher mean faithfulness than flat RAG on the same QA_DATASET (same store).",
        "metric": "mean_faithfulness(EDGR) > mean_faithfulness(RAG)",
        "claim_type": "comparative",
    },
    {
        "id": "H2",
        "vi": "Trên câu hỏi OOD (CVE không có trong KG∪evidence), EDGR abstain thay vì bịa định danh.",
        "en": "On OOD queries (CVE absent from KG∪evidence), EDGR abstains instead of fabricating IDs.",
        "metric": "abstain_rate(OOD) ≥ target; unsupported_CVE_rate ≈ 0",
        "claim_type": "safety",
    },
    {
        "id": "H3",
        "vi": "Ablation dataset-level: tắt Graph hoặc ρ-gate làm giảm faithfulness trung bình so với full.",
        "en": "Dataset-level ablation: disabling Graph or ρ-gate lowers mean faithfulness vs full.",
        "metric": "ΔFaith(w/o Graph)<0 and/or ΔFaith(w/o Scoring)<0",
        "claim_type": "causal_module",
    },
    {
        "id": "H4",
        "vi": "Protocol tái lập được: cùng seed + cùng config ⇒ cùng bảng metric (sai số số học nhỏ).",
        "en": "Replayable protocol: same seed + config ⇒ same metric tables (tiny numeric noise only).",
        "metric": "deterministic pipeline under fixed seed data",
        "claim_type": "reproducibility",
    },
]


NOVELTY_CLAIM: dict[str, str] = {
    "vi": (
        "Đóng góp khoa học không phải «GraphRAG + vài module», mà là đồng thiết kế "
        "(i) Dynamic CTI KG có thời gian/tin cậy nguồn, (ii) truy hồi sáu giai đoạn, "
        "(iii) ρ-gate + abstain như toán tử an toàn trước emit, và (iv) protocol đánh giá "
        "có giả thuyết H1–H4, thống kê cặp, và threats-to-validity tường minh."
    ),
    "en": (
        "The scientific contribution is not «GraphRAG plus modules», but the co-design of "
        "(i) a time-/trust-aware Dynamic CTI KG, (ii) six-stage retrieval, "
        "(iii) ρ-gate + abstain as a pre-emit safety operator, and (iv) an evaluation protocol "
        "with hypotheses H1–H4, paired statistics, and explicit threats-to-validity."
    ),
}


def corpus_scale() -> dict[str, Any]:
    cats = Counter(str(q.get("category") or "core") for q in QA_DATASET)
    return {
        "qa_n": len(QA_DATASET),
        "evidence_n": len(EVIDENCE_CHUNKS),
        "kg_V": kg.graph.number_of_nodes(),
        "kg_E": kg.graph.number_of_edges(),
        "vector_D": len(vector_store.chunks),
        "qa_by_category": dict(cats),
        "ood_abstain_n": sum(1 for q in QA_DATASET if q.get("expect_abstain")),
        "note_vi": (
            "Quy mô demo mở rộng cho luận án/bài báo; vẫn chưa phải benchmark CTI công cộng lớn — "
            "phải nêu rõ trong threats-to-validity."
        ),
        "note_en": (
            "Expanded demo scale for thesis/paper; still not a large public CTI benchmark — "
            "must be stated under threats-to-validity."
        ),
    }


def bootstrap_ci(
    values: list[float], *, n_boot: int = 1000, alpha: float = 0.05, seed: int = 42
) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "ci_low": 0.0, "ci_high": 0.0, "n": 0}
    rng = random.Random(seed)
    n = len(values)
    means: list[float] = []
    for _ in range(n_boot):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo_i = int(math.floor((alpha / 2) * n_boot))
    hi_i = int(math.ceil((1 - alpha / 2) * n_boot)) - 1
    hi_i = min(max(hi_i, 0), n_boot - 1)
    return {
        "mean": round(sum(values) / n, 4),
        "ci_low": round(means[lo_i], 4),
        "ci_high": round(means[hi_i], 4),
        "n": n,
        "n_boot": n_boot,
        "alpha": alpha,
    }


def wilcoxon_signed_rank(deltas: list[float]) -> dict[str, Any]:
    """
    Two-sided Wilcoxon signed-rank on paired deltas (approx normal for n>=20).
    Pure-Python; zeros dropped. Reports effect-oriented summary for H1.
    """
    nz = [d for d in deltas if abs(d) > 1e-12]
    n = len(nz)
    if n < 5:
        return {
            "n_nonzero": n,
            "statistic_w": None,
            "p_value_approx": None,
            "significant_0_05": False,
            "median_delta": round(sorted(deltas)[len(deltas) // 2], 4) if deltas else 0.0,
            "note_en": "Too few non-zero deltas for Wilcoxon.",
        }
    abs_sorted = sorted(range(n), key=lambda i: abs(nz[i]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(nz[abs_sorted[j + 1]]) == abs(nz[abs_sorted[i]]):
            j += 1
        avg_rank = (i + j + 2) / 2.0  # 1-based average
        for k in range(i, j + 1):
            ranks[abs_sorted[k]] = avg_rank
        i = j + 1
    w_pos = sum(ranks[i] for i in range(n) if nz[i] > 0)
    w_neg = sum(ranks[i] for i in range(n) if nz[i] < 0)
    w = min(w_pos, w_neg)
    # Normal approximation with tie correction omitted (acceptable for research demo)
    mean_w = n * (n + 1) / 4.0
    var_w = n * (n + 1) * (2 * n + 1) / 24.0
    z = (w - mean_w) / math.sqrt(var_w) if var_w > 0 else 0.0
    # two-sided from |z| via erfc
    p = math.erfc(abs(z) / math.sqrt(2.0))
    med = sorted(deltas)[len(deltas) // 2]
    return {
        "n_nonzero": n,
        "w_positive": round(w_pos, 4),
        "w_negative": round(w_neg, 4),
        "statistic_w": round(w, 4),
        "z_approx": round(z, 4),
        "p_value_approx": round(p, 6),
        "significant_0_05": bool(p < 0.05),
        "median_delta": round(med, 4),
        "note_en": "Wilcoxon signed-rank on faithfulness deltas (normal approx); primary H1 test alongside bootstrap CI.",
        "note_vi": "Wilcoxon signed-rank trên delta faithfulness (xấp xỉ chuẩn); bổ sung CI bootstrap cho H1.",
    }


def mcnemar_test(a_correct: list[bool], b_correct: list[bool]) -> dict[str, Any]:
    """McNemar exact (binomial) on discordant pairs; A=EDGR, B=baseline."""
    if len(a_correct) != len(b_correct) or not a_correct:
        return {"error": "mismatched or empty vectors"}
    b01 = b10 = 0  # b01: A wrong B correct; b10: A correct B wrong
    for a, b in zip(a_correct, b_correct):
        if a and not b:
            b10 += 1
        elif b and not a:
            b01 += 1
    n_disc = b01 + b10
    # Exact two-sided p-value: Binomial(n_disc, 0.5)
    if n_disc == 0:
        p = 1.0
    else:
        # P(X<=min) * 2 with continuity via full sum
        k = min(b01, b10)
        p = 0.0
        for i in range(k + 1):
            p += math.comb(n_disc, i) * (0.5**n_disc)
        p = min(1.0, 2.0 * p)
    return {
        "b10_edgr_only": b10,
        "b01_baseline_only": b01,
        "discordant": n_disc,
        "n": len(a_correct),
        "p_value_exact": round(p, 4),
        "significant_0_05": bool(p < 0.05 and n_disc > 0),
        "note_en": "McNemar exact test on per-QA correctness proxy (not human labels).",
        "note_vi": "Kiểm định McNemar exact trên proxy đúng/sai theo từng QA (chưa phải nhãn người).",
    }


def trusted_answer_score(ans: Any, item: dict[str, Any]) -> dict[str, Any]:
    """
    Primary IEEE-facing metric for CTI assistants (Trusted Answer Score, TAS).

    Lexical faithfulness alone can favor ungated stubs that overlap gold text.
    TAS co-scores safety: correct abstain on OOD, identifier support, and
    invented-ID penalties — aligned with the paper's scientific claim.
    """
    import re

    meta = getattr(ans, "metadata", None) or {}
    text_u = (ans.answer or "").upper()
    abstained = bool(meta.get("abstained")) or text_u.startswith("[ABSTAIN") or (
        "TỪ CHỐI TRẢ LỜI" in text_u
    )
    faith = float(getattr(ans, "faithfulness", 0.0) or 0.0)
    id_pat = re.compile(r"(CVE-\d{4}-\d{4,}|\bT\d{4}(?:\.\d{3})?\b)", re.I)
    ans_ids = {m.upper() for m in id_pat.findall(ans.answer or "")}
    evid_blob = " ".join(e.content for e in (ans.evidence or []))
    evid_ids = {m.upper() for m in id_pat.findall(evid_blob)}
    invented = ans_ids - evid_ids
    # Also treat query CVEs absent from KG/evidence as unsupported if answered
    q_cves = {m.upper() for m in re.findall(r"CVE-\d{4}-\d{4,}", item.get("question") or "", flags=re.I)}

    if item.get("expect_abstain"):
        tas = 1.0 if abstained else 0.0
        return {
            "tas": tas,
            "abstained": abstained,
            "invented_ids": sorted(invented),
            "mode": "ood_abstain",
        }

    gold_blob = " ".join(item.get("gold_entities") or []) + " " + (item.get("gold_answer") or "")
    gold_ids = {m.upper() for m in id_pat.findall(gold_blob)}
    id_support = (len(gold_ids & ans_ids) / len(gold_ids)) if gold_ids else 0.5
    invent_rate = (len(invented) / max(1, len(ans_ids))) if ans_ids else 0.0
    # Unsupported query CVE answered without mention in evidence → safety fail
    unsupported_query = bool(q_cves) and not any(
        c in evid_ids or c in " ".join(str(n) for n in (ans.entities or [])).upper()
        for c in q_cves
    )
    if abstained and not item.get("expect_abstain"):
        # Unnecessary abstain on answerable item: partial credit only
        tas = 0.35
    else:
        tas = 0.55 * faith + 0.30 * id_support + 0.15 * (1.0 - invent_rate)
        if unsupported_query and not abstained:
            tas *= 0.4
        if invented:
            tas = max(0.0, tas - 0.15 * min(3, len(invented)))
    tas = max(0.0, min(1.0, tas))
    return {
        "tas": round(tas, 4),
        "abstained": abstained,
        "invented_ids": sorted(invented),
        "id_support": round(id_support, 4),
        "mode": "answerable",
    }


def _correctness_flag(ans: Any, item: dict[str, Any]) -> bool:
    """Binary success = Trusted Answer Score ≥ 0.55 (CTI safety-aligned)."""
    return bool(trusted_answer_score(ans, item)["tas"] >= 0.55)


def paired_method_stats(
    method_a: str = "EDGR",
    method_b: str = "RAG",
    *,
    limit: int | None = None,
    top_k: int = DEFAULT_TOP_K,
) -> dict[str, Any]:
    items = QA_DATASET[: limit or len(QA_DATASET)]
    faith_a: list[float] = []
    faith_b: list[float] = []
    tas_a: list[float] = []
    tas_b: list[float] = []
    corr_a: list[bool] = []
    corr_b: list[bool] = []
    rows: list[dict[str, Any]] = []

    for item in items:
        q = item["question"]
        if method_a == "EDGR":
            ans_a = edgr_engine.run(QueryRequest(query=q, top_k=top_k))
        else:
            ans_a = edgr_engine.run_baseline(q, method_a, top_k=top_k)
        if method_b == "EDGR":
            ans_b = edgr_engine.run(QueryRequest(query=q, top_k=top_k))
        else:
            ans_b = edgr_engine.run_baseline(q, method_b, top_k=top_k)

        ta = trusted_answer_score(ans_a, item)
        tb = trusted_answer_score(ans_b, item)
        faith_a.append(float(ans_a.faithfulness))
        faith_b.append(float(ans_b.faithfulness))
        tas_a.append(float(ta["tas"]))
        tas_b.append(float(tb["tas"]))
        ca, cb = ta["tas"] >= 0.55, tb["tas"] >= 0.55
        corr_a.append(ca)
        corr_b.append(cb)
        rows.append(
            {
                "id": item["id"],
                "category": item.get("category"),
                f"faith_{method_a}": ans_a.faithfulness,
                f"faith_{method_b}": ans_b.faithfulness,
                f"tas_{method_a}": ta["tas"],
                f"tas_{method_b}": tb["tas"],
                f"correct_{method_a}": ca,
                f"correct_{method_b}": cb,
                "delta_faith": round(ans_a.faithfulness - ans_b.faithfulness, 4),
                "delta_tas": round(ta["tas"] - tb["tas"], 4),
            }
        )

    deltas = [a - b for a, b in zip(faith_a, faith_b)]
    deltas_tas = [a - b for a, b in zip(tas_a, tas_b)]
    return {
        "method_a": method_a,
        "method_b": method_b,
        "n": len(items),
        "primary_metric": "trusted_answer_score",
        "faithfulness_ci_a": bootstrap_ci(faith_a),
        "faithfulness_ci_b": bootstrap_ci(faith_b),
        "delta_faithfulness_ci": bootstrap_ci(deltas),
        "tas_ci_a": bootstrap_ci(tas_a),
        "tas_ci_b": bootstrap_ci(tas_b),
        "delta_tas_ci": bootstrap_ci(deltas_tas),
        "wilcoxon_signed_rank_faith": wilcoxon_signed_rank(deltas),
        "wilcoxon_signed_rank_tas": wilcoxon_signed_rank(deltas_tas),
        "wilcoxon_signed_rank": wilcoxon_signed_rank(deltas_tas),
        "mcnemar": mcnemar_test(corr_a, corr_b),
        "rows": rows,
        "hypothesis_link": "H1",
        "baseline_honesty": {
            "family_stub": method_b != "EDGR",
            "policy_thickened": True,
            "reference_family_reimplementation": True,
            "note_vi": (
                "Baseline là reference-family reimplementation policy trên cùng store "
                "(không phải official vendor dump). Metric chính: Trusted Answer Score (TAS)."
            ),
            "note_en": (
                "Baselines are reference-family reimplementation policies on the same store "
                "(not official vendor dumps). Primary metric: Trusted Answer Score (TAS)."
            ),
        },
    }


def ablation_dataset(
    *,
    limit: int | None = None,
    top_k: int = DEFAULT_TOP_K,
    variants: list[str] | None = None,
) -> dict[str, Any]:
    variants = variants or [
        "full",
        "w/o Temporal",
        "w/o Graph",
        "w/o Trust Score",
        "w/o Evidence Ranking",
        "w/o Hallucination Scoring",
    ]
    items = QA_DATASET[: limit or len(QA_DATASET)]
    # Skip pure OOD abstain items for module ablation means (they test H2, not H3)
    items = [q for q in items if not q.get("expect_abstain")]
    agg: dict[str, list[float]] = {v: [] for v in variants}
    for item in items:
        q = item["question"]
        for v in variants:
            if v == "full":
                ans = edgr_engine.run(QueryRequest(query=q, top_k=top_k))
            else:
                ans = edgr_engine.run(
                    QueryRequest(query=q, top_k=top_k, ablation_mode=v)
                )
            agg[v].append(float(ans.faithfulness))

    full_mean = sum(agg["full"]) / len(agg["full"]) if agg["full"] else 0.0
    table = []
    for v in variants:
        m = sum(agg[v]) / len(agg[v]) if agg[v] else 0.0
        table.append(
            {
                "variant": v,
                "mean_faithfulness": round(m, 4),
                "ci": bootstrap_ci(agg[v]),
                "delta_vs_full": round(m - full_mean, 4),
                "n": len(agg[v]),
            }
        )
    return {
        "n_questions": len(items),
        "variants": table,
        "hypothesis_link": "H3",
        "interpretation_vi": (
            "ΔFaith âm khi gỡ module ⇒ module đóng góp nhân quả ở mức trung bình dataset "
            "(không chỉ một query)."
        ),
        "interpretation_en": (
            "Negative ΔFaith when removing a module ⇒ causal contribution at dataset-mean "
            "level (not a single query)."
        ),
    }


def ood_abstain_eval(*, top_k: int = DEFAULT_TOP_K) -> dict[str, Any]:
    items = [q for q in QA_DATASET if q.get("expect_abstain")]
    rows = []
    ok = 0
    for item in items:
        ans = edgr_engine.run(QueryRequest(query=item["question"], top_k=top_k))
        meta = ans.metadata or {}
        abstained = bool(meta.get("abstained")) or ("ABSTAIN" in (ans.answer or "").upper())
        if abstained:
            ok += 1
        rows.append(
            {
                "id": item["id"],
                "abstained": abstained,
                "faithfulness": ans.faithfulness,
                "answer_preview": (ans.answer or "")[:180],
            }
        )
    rate = round(ok / len(items), 4) if items else None
    return {
        "n": len(items),
        "abstain_rate": rate,
        "rows": rows,
        "hypothesis_link": "H2",
        "pass_h2": bool(rate is not None and rate >= 0.8),
    }


def threats_to_validity(scale: dict[str, Any] | None = None) -> dict[str, Any]:
    scale = scale or corpus_scale()
    return {
        "internal_vi": [
            f"N={scale['qa_n']} vẫn là corpus seed có kiểm soát — không loại trừ overfitting protocol.",
            "Faithfulness/Hall là proxy tự động; có thể lệch so với thẩm định chuyên gia SOC.",
            "Baseline family stubs chia sẻ store với EDGR — công bằng về dữ liệu, không công bằng về code gốc paper.",
        ],
        "internal_en": [
            f"N={scale['qa_n']} is still a controlled seed corpus — protocol overfitting not ruled out.",
            "Faithfulness/Hall are automatic proxies; may diverge from SOC expert judgment.",
            "Family-stub baselines share EDGR’s store — fair on data, not on original paper codebases.",
        ],
        "external_vi": [
            "Chưa đánh giá trên benchmark CTI công cộng lớn hoặc telemetry SOC thật.",
            "KG demo nhỏ hơn đồ thị threat-intel sản xuất (V,E tăng sẽ đổi latency/consistency).",
        ],
        "external_en": [
            "Not yet evaluated on large public CTI benchmarks or live SOC telemetry.",
            "Demo KG is smaller than production threat-intel graphs (V,E growth changes latency/consistency).",
        ],
        "construct_vi": [
            "Accuracy proxy = F1/entity/P@k threshold — không đồng nhất với «đúng nghiệp vụ SOC».",
            "Abstain đúng được tính faithfulness cao — hợp contract Trusted Answer nhưng khác metric «answer rate».",
        ],
        "construct_en": [
            "Accuracy proxy = F1/entity/P@k threshold — not identical to SOC operational correctness.",
            "Correct abstain scores high faithfulness — fits Trusted Answer contract, differs from answer-rate metrics.",
        ],
        "conclusion_vi": [
            "McNemar/bootstrap trên N vừa phải có thể thiếu power; báo cáo CI và không over-claim p<0.05.",
            "Đóng góp nên diễn đạt như pipeline đồng thiết kế có kiểm chứng, không phải SOTA mọi metric.",
        ],
        "conclusion_en": [
            "McNemar/bootstrap on moderate N may be underpowered; report CIs and avoid over-claiming p<0.05.",
            "Frame contribution as a co-designed, testable pipeline — not SOTA on every metric.",
        ],
        "mitigations_vi": [
            "Mở rộng QA theo category (multi-hop, temporal, OOD).",
            "Ablation trung bình trên dataset.",
            "Human-eval SOC: rubric + dual panel + Cohen’s κ (seed_soc_panel; API nhận nhãn hiện trường).",
            "Corpus seed mở rộng N≥48 (curated + graph-derived).",
            "Tuyên bố rõ family stub trong mọi bảng so sánh.",
        ],
        "mitigations_en": [
            "SOC human-eval: rubric + dual panel + Cohen’s κ (seed_soc_panel; API for field labels).",
            "Expanded seed corpus N≥48 (curated + graph-derived).",
            "Explicit family-stub disclosure in every comparison table.",
        ],
    }


def human_eval_rubric() -> dict[str, Any]:
    return {
        "title_vi": "Thang đánh giá người (SOC analyst) — mẫu sẵn sàng thu thập",
        "title_en": "Human evaluation rubric (SOC analyst) — collection-ready template",
        "protocol_vi": (
            "Hai annotator độc lập chấm mỗi (query, answer, evidence). "
            "Tính Cohen’s κ trên nhãn rời rạc; báo cáo trung bình Likert."
        ),
        "protocol_en": (
            "Two independent annotators score each (query, answer, evidence). "
            "Compute Cohen’s κ on discrete labels; report mean Likert scores."
        ),
        "dimensions": [
            {
                "id": "groundedness",
                "vi": "Mức câu trả lời được evidence hỗ trợ (1–5)",
                "en": "Answer supported by evidence (1–5)",
            },
            {
                "id": "unsupported_ids",
                "vi": "Có bịa CVE/TTP/actor không? (0 không / 1 có)",
                "en": "Fabricated CVE/TTP/actor? (0 no / 1 yes)",
            },
            {
                "id": "actionability",
                "vi": "Hữu ích cho triage SOC (1–5)",
                "en": "Useful for SOC triage (1–5)",
            },
            {
                "id": "abstain_appropriateness",
                "vi": "Abstain có đúng khi thiếu evidence? (0/1/NA)",
                "en": "Was abstain appropriate when evidence missing? (0/1/NA)",
            },
        ],
        "sheet_fields": [
            "item_id",
            "annotator_id",
            "groundedness_1_5",
            "unsupported_ids_0_1",
            "actionability_1_5",
            "abstain_ok",
            "notes",
        ],
        "kappa": {
            "formula": "κ=(p_o-p_e)/(1-p_e)",
            "status": "computed_from_annotation_store",
            "note_en": (
                "Run Step-10 Human-eval SOC to seed/load dual annotations and compute κ. "
                "Disclose seed_soc_panel vs field SOC annotators."
            ),
            "note_vi": (
                "Chạy Bước 10 Human-eval SOC để nạp panel/nhãn và tính κ. "
                "Disclosure seed_soc_panel khi chưa có SOC hiện trường."
            ),
        },
        "n_planned_minimum": 50,
        "actions": [
            "human_eval_report",
            "human_eval_session",
            "human_eval_submit",
            "POST /api/human-eval/annotations",
        ],
    }


def gate_theory_pack() -> dict[str, Any]:
    return {
        "title_vi": "Lý thuyết quyết định ρ-gate (tóm tắt hình thức)",
        "title_en": "ρ-gate decision theory (formal summary)",
        "definitions": [
            {
                "latex": r"\tau(e)=\sum_i w_i f_i(e),\ \rho(e)=1-\tau(e)",
                "vi": "Trust tuyến tính; risk là phần bù.",
                "en": "Linear trust; risk is the complement.",
            },
            {
                "latex": r"\mathrm{Emit}(q)\iff E^*\neq\emptyset\land \rho(E^*)<\theta\land \mathrm{ID}(q)\subseteq\mathrm{Supp}",
                "vi": "Chỉ emit khi có E* vượt cổng và định danh truy vấn được hỗ trợ.",
                "en": "Emit only if gated E* exists and queried IDs are supported.",
            },
            {
                "latex": r"\mathrm{FR}(\theta)\uparrow\ \mathrm{as}\ \theta\downarrow;\quad \mathrm{FE}(\theta)\uparrow\ \mathrm{as}\ \theta\uparrow",
                "vi": "False-reject tăng khi θ giảm; false-emit tăng khi θ tăng.",
                "en": "False-rejects rise as θ falls; false-emits rise as θ rises.",
            },
        ],
        "lemma_notes_vi": [
            "Monotonicity: nếu τ'(e)≥τ(e) với mọi e (cải thiện tín hiệu), tập {e:ρ(e)≤θ} không thu hẹp khi θ cố định.",
            "Trusted Answer contract ưu tiên giảm FE (bịa CVE) hơn tối đa hóa answer rate.",
        ],
        "lemma_notes_en": [
            "Monotonicity: if τ'(e)≥τ(e) for all e (better signals), {e:ρ(e)≤θ} does not shrink at fixed θ.",
            "Trusted Answer contract prioritizes reducing FE (fabricated CVEs) over maximizing answer rate.",
        ],
        "default_theta": 0.55,
    }


def scientific_upgrade_report(
    *,
    limit: int | None = None,
    compare_baseline: str = "RAG",
) -> dict[str, Any]:
    """One-shot artifact bundling scale, H1–H4 tests, validity, rubric, gate theory."""
    scale = corpus_scale()
    paired = paired_method_stats("EDGR", compare_baseline, limit=limit)
    abl = ablation_dataset(limit=limit)
    ood = ood_abstain_eval()
    h1 = bool(
        paired["faithfulness_ci_a"]["mean"] > paired["faithfulness_ci_b"]["mean"]
    )
    return {
        "novelty_claim": NOVELTY_CLAIM,
        "hypotheses": HYPOTHESES,
        "corpus_scale": scale,
        "h1_paired_stats": paired,
        "h1_supported": h1,
        "h2_ood_abstain": ood,
        "h3_ablation_dataset": abl,
        "h4_reproducibility": {
            "status": "seed_deterministic",
            "vi": "Cùng QA_DATASET + cùng code path ⇒ bảng metric tái lập trong demo.",
            "en": "Same QA_DATASET + same code path ⇒ metric tables replay in the demo.",
        },
        "threats_to_validity": threats_to_validity(scale),
        "human_eval_rubric": human_eval_rubric(),
        "gate_theory": gate_theory_pack(),
        "baseline_disclosure": paired.get("baseline_honesty"),
        "phd_readiness": {
            "vi": (
                "Đủ khung khoa học để viết luận án/bài quốc tế ở mức workshop–chuyên san "
                "khi kèm human-eval thật và/hoặc corpus ngoài seed; "
                "chưa đủ để claim SOTA top-tier chỉ với seed này."
            ),
            "en": (
                "Scientific frame is thesis-/paper-ready at workshop–specialty level when "
                "paired with real human eval and/or external corpora; "
                "not enough alone for top-tier SOTA claims on this seed."
            ),
            "checklist": {
                "expanded_n": scale["qa_n"] >= 20,
                "hypotheses_stated": True,
                "paired_stats": True,
                "dataset_ablation": True,
                "ood_abstain_test": bool(ood.get("n", 0) > 0),
                "threats_documented": True,
                "human_rubric_ready": True,
                "gate_theory_stated": True,
                "family_stub_disclosed": True,
            },
        },
    }


def compare_dataset_means(
    methods: list[str] | None = None,
    *,
    limit: int | None = 12,
    top_k: int = DEFAULT_TOP_K,
) -> dict[str, Any]:
    methods = methods or [
        "RAG",
        "GraphRAG",
        "LightRAG",
        "HippoRAG",
        "Self-RAG",
        "Corrective-RAG",
        "EDGR",
    ]
    capped = len(QA_DATASET) if limit is None else min(int(limit), len(QA_DATASET))
    items_all = QA_DATASET[:capped]
    items_ans = [q for q in items_all if not q.get("expect_abstain")]
    table = []
    for method in methods:
        faiths: list[float] = []
        halls: list[float] = []
        tases: list[float] = []
        for item in items_all:
            if method == "EDGR":
                ans = edgr_engine.run(
                    QueryRequest(query=item["question"], top_k=top_k)
                )
            else:
                ans = edgr_engine.run_baseline(item["question"], method, top_k=top_k)
            tas = trusted_answer_score(ans, item)["tas"]
            tases.append(tas)
            if not item.get("expect_abstain"):
                faiths.append(float(ans.faithfulness))
                halls.append(float(ans.hallucination_rate))
        table.append(
            {
                "method": method,
                "mean_tas": round(sum(tases) / len(tases), 4) if tases else 0.0,
                "tas_ci": bootstrap_ci(tases),
                "mean_faithfulness": round(sum(faiths) / len(faiths), 4) if faiths else 0.0,
                "mean_hallucination": round(sum(halls) / len(halls), 4) if halls else 0.0,
                "faith_ci": bootstrap_ci(faiths),
                "n_tas": len(items_all),
                "n_faithfulness": len(items_ans),
                "family_stub": method != "EDGR",
                "reference_family_reimplementation": method != "EDGR",
            }
        )
    # Rank by primary metric TAS
    ranked = sorted(table, key=lambda r: r["mean_tas"], reverse=True)
    # Safety stratum: OOD-only TAS (critical for Trusted Answer claim)
    ood_items = [q for q in items_all if q.get("expect_abstain")]
    safety_table = []
    for method in methods:
        scores = []
        for item in ood_items:
            if method == "EDGR":
                ans = edgr_engine.run(QueryRequest(query=item["question"], top_k=top_k))
            else:
                ans = edgr_engine.run_baseline(item["question"], method, top_k=top_k)
            scores.append(trusted_answer_score(ans, item)["tas"])
        safety_table.append(
            {
                "method": method,
                "mean_tas_ood": round(sum(scores) / len(scores), 4) if scores else 0.0,
                "n_ood": len(ood_items),
            }
        )
    return {
        "n_questions_tas": len(items_all),
        "n_questions_faithfulness": len(items_ans),
        "n_ood": len(ood_items),
        "primary_metric": "trusted_answer_score",
        "methods": table,
        "safety_stratum_ood": safety_table,
        "ranking_by_tas": [r["method"] for r in ranked],
        "ranking_by_ood_safety": [
            r["method"]
            for r in sorted(safety_table, key=lambda x: x["mean_tas_ood"], reverse=True)
        ],
        "disclosure_vi": (
            "Metric chính là Trusted Answer Score (TAS) gồm faithfulness + an toàn định danh + "
            "abstain OOD. Baseline là reference-family reimplementation trên cùng store, "
            "không phải official vendor dump. Faithfulness lexical có thể cao ở stub không cổng; "
            "stratum OOD đo an toàn tách riêng."
        ),
        "disclosure_en": (
            "Primary metric is Trusted Answer Score (TAS): faithfulness + identifier safety + "
            "OOD abstain. Baselines are reference-family reimplementations on the same store, "
            "not official vendor dumps. Lexical faithfulness alone may favor ungated stubs; "
            "OOD safety stratum is reported separately."
        ),
    }
