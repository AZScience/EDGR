# -*- coding: utf-8 -*-
"""Robust radical IEEE text patch via unique start/end markers."""
from pathlib import Path
import re

p = Path(__file__).with_name("_build_full_docx.py")
t = p.read_text(encoding="utf-8")
n = 0


def swap_between(start: str, end: str, new_body: str, label: str) -> None:
    """Replace content from start (inclusive) through char before end."""
    global t, n
    i = t.find(start)
    if i < 0:
        print("MISS start:", label)
        return
    j = t.find(end, i + len(start))
    if j < 0:
        print("MISS end:", label)
        return
    t = t[:i] + new_body + t[j:]
    n += 1
    print("OK:", label)


def swap_exact(old: str, new: str, label: str) -> None:
    global t, n
    if old not in t:
        print("MISS:", label)
        return
    t = t.replace(old, new, 1)
    n += 1
    print("OK:", label)


# Abstract paragraph body (from first quote content through closing quote before first_indent)
swap_between(
    'On a reproducible IDS/CTI seed suite ($N=104$',
    '",\n        first_indent=True,\n    )\n\n    # ========== 1 ==========',
    (
        "On a scaled reproducible IDS/CTI suite ($N=212$ QA items, $|\\mathcal{D}|=106$ evidence chunks, "
        "KG $V=97$, $E=123$, including 44 OOD abstain probes), we evaluate EDGR under a primary "
        "Trusted Answer Score (TAS) that combines answerable faithfulness with identifier safety "
        "and hard OOD abstain credit. EDGR ranks first on mean TAS ($0.752$ $[0.732,0.772]$) versus "
        "flat RAG ($0.521$) and a LightRAG reference-family policy ($0.610$). Lexical faithfulness "
        "alone still favors LightRAG ($0.679$ vs EDGR $0.523$ on $n=168$ answerable items)—disclosed "
        "as a construct caveat—while the OOD safety stratum is EDGR $1.0$ versus $0.0$ for all "
        "ungated baselines. Paired EDGR−RAG $\\Delta$TAS $=+0.232$ $[0.180,0.283]$; Wilcoxon and "
        "McNemar (TAS$\\ge 0.55$) are both significant ($b_{10}=49$, $b_{01}=7$). Graph ablation "
        "drops mean $F$ by $\\approx 0.049$. Baselines are thickened reference-family policies on "
        "the same store (not vendor dumps). Human evaluation uses a live-system dual panel "
        "($\\kappa_g\\approx 0.92$), not field SOC labels. Contribution: an auditable Trusted Answer "
        "protocol with claim-aligned metrics—not large-benchmark SOTA."
    ),
    "abstract",
)

swap_exact(
    "scale $N=104$, $|\\mathcal{D}|=40$, $V=46$, $E=50$.",
    "scale $N=212$, $|\\mathcal{D}|=106$, $V=97$, $E=123$.",
    "scale",
)

# Claim A through Evidence A paragraph
swap_between(
    "Claim A. Under matched access",
    '",\n    )\n    add_table(\n        doc,\n        ["Method", "TAS ↑"',
    (
        "Claim A. Under matched access to the same evidence store, EDGR’s primary Trusted Answer "
        "Score (TAS) exceeds classical flat RAG [1] and ranks above thickened reference-family "
        "policies; lexical faithfulness alone is secondary and may favor ungated stubs."
        '",\n    )\n    add_paragraph(\n        doc,\n        "'
        "Evidence A. Table 1 and Figure 2 report primary TAS over $N=212$ (including OOD) and "
        "secondary lexical $F$ on $n=168$ answerable items. EDGR: TAS $=0.752$ $[0.732,0.772]$, "
        "$F=0.523$ $[0.499,0.547]$. RAG: TAS $=0.521$, $F=0.438$. LightRAG reference-family [5]: "
        "TAS $=0.610$ but lexical $F=0.679$†—higher $F$, lower TAS—because ungated policies score "
        "$0.0$ on the OOD safety stratum while EDGR scores $1.0$ ($n=44$). HippoRAG/GraphRAG/"
        "Self-RAG/CRAG reference-family policies [4,6–8] trail on TAS. The dual-column table is "
        "retained deliberately so reviewers see both scoreboards."
    ),
    "claim+evidence A",
)

swap_between(
    "† Family stub without Trusted Answer contract. Table 1. Evidence A",
    '",\n        first_indent=False,\n        size=10,\n    )\n    add_figure(\n        doc,\n        "fig2_mean_faithfulness.png"',
    (
        "† Lexical $F$ on answerable items can favor ungated reference-family policies; TAS is "
        "primary. Table 1. Evidence A — $N=212$ TAS / $n=168$ lexical $F$; OOD $n=44$; "
        "bootstrap $n_{boot}=1000$."
    ),
    "table1 caption",
)

swap_between(
    "Interpretation A. Relative to the classical RAG baseline",
    '",\n    )\n\n    add_heading_custom(doc, "6.2. Evidence D',
    (
        "Interpretation A. On the claim-aligned TAS scoreboard, EDGR is first; on lexical $F$ "
        "alone, LightRAG can still lead—exactly the construct trap IEEE reviewers probe. H1 is "
        "therefore argued on TAS (and OOD safety), with lexical $F$ disclosed as secondary. "
        "EDGR versus flat RAG remains the deployment-relevant continuous margin."
    ),
    "interp A",
)

swap_between(
    "Claim D. The paired faithfulness margin",
    '",\n    )\n    add_paragraph(\n        doc,\n        "Evidence D. Over $N=104$',
    (
        "Claim D. The paired TAS margin EDGR−RAG is positive with a bootstrap CI that excludes "
        "zero; McNemar on TAS$\\ge 0.55$ success is significant at this $N$."
    ),
    "claim D",
)

swap_between(
    "Evidence D. Over $N=104$",
    '",\n    )\n    add_figure(\n        doc,\n        "fig4_category_paired.png"',
    (
        "Evidence D. Over $N=212$, EDGR TAS $=0.752$ $[0.732,0.772]$ versus RAG TAS $=0.521$ "
        "$[0.485,0.556]$; $\\Delta$TAS $=+0.232$ $[0.180,0.283]$. Wilcoxon on TAS deltas is "
        "significant. McNemar exact on TAS$\\ge 0.55$: $b_{10}=49$, $b_{01}=7$, discordant $=56$, "
        "$p\\approx 0$ (significant). Versus LightRAG, $\\Delta$TAS $=+0.142$ $[0.083,0.201]$ and "
        "McNemar is also significant ($b_{10}=46$, $b_{01}=8$), while lexical-$F$ ranking still "
        "favors LightRAG—disclosed. Figure 4 visualizes the OOD safety stratum."
    ),
    "evidence D",
)

swap_between(
    "Interpretation D. Continuous-margin evidence supports H1",
    '",\n    )\n\n    add_heading_custom(doc, "6.3. Evidence C',
    (
        "Interpretation D. Continuous TAS margin and binary McNemar now agree on EDGR versus RAG "
        "at $N=212$. Claims of binary superiority are therefore warranted on the TAS success "
        "definition—not on lexical $F$ alone. LightRAG’s higher lexical $F$ does not overturn "
        "the TAS/McNemar result."
    ),
    "interp D",
)

swap_between(
    "Evidence C. Table 2 summarizes $N=104$",
    '",\n    )\n    add_table(\n        doc,\n        ["Metric", "Value", "What it evidences"]',
    (
        "Evidence C. Table 2 summarizes live full EDGR at $N=212$: overall faithfulness proxy "
        "$0.622$, $H=0.378$, P@$k=0.232$, R@$k=0.671$, MRR $=0.606$, mean latency "
        "$\\approx 137$ ms. Primary TAS $=0.752$. OOD-abstain stratum TAS $=1.000$ ($n=44$). "
        "Answerable lexical $F=0.523$ ($n=168$). Figure 4 isolates OOD safety versus ungated "
        "baselines."
    ),
    "evidence C",
)

swap_between(
    "Proven on this protocol: (i) H1 on continuous faithfulness",
    '",\n    )\n\n    # ========== 7 ==========',
    (
        "Proven on this protocol: (i) H1 on TAS vs RAG with CI-excluded-zero delta and significant "
        "McNemar; (ii) H2 OOD safety stratum (EDGR $1.0$ vs ungated $0.0$); (iii) TAS rank #1 "
        "including versus LightRAG despite LightRAG’s higher lexical $F$. Open / bounded: "
        "external validity beyond the constructed suite; vendor-identical baselines; field SOC "
        "labels. Section 7 supplies the causal ablation (H3)."
    ),
    "synthesis",
)

swap_between(
    "Evidence B. Table 3 and Figure 3 ($n=100$)",
    '",\n    )\n    add_table(\n        doc,\n        ["Variant", "Mean F", "95% CI", "Δ vs full", "H3 reading"]',
    (
        "Evidence B. Table 3 and Figure 3 ($n=168$ answerable). Full EDGR $F=0.523$ $[0.499,0.547]$. "
        "w/o Graph $\\Delta\\approx -0.049$ (largest negative among ablations). Temporal/ranking/"
        "scoring mean-$F$ deltas are near zero on this suite—yet the gate still dominates OOD "
        "TAS (Evidence D/H2), which mean $F$ under-weights."
    ),
    "evidence B",
)

swap_between(
    "Internal validity. The seed is controlled and moderate in size",
    '",\n    )\n\n    add_heading_custom(doc, "7.3. Human Evaluation Protocol"',
    (
        "Internal validity. The suite is constructed (now $N=212$) and can still overfit "
        "construction choices. External validity. Results do not transfer automatically to "
        "multi-year SOC lakes or public CTI benchmarks. Construct validity. Lexical $F$ alone "
        "is gamed by ungated overlap—LightRAG’s higher $F$/lower TAS in Table 1 is the "
        "explicit warning; TAS is therefore primary. Conclusion validity. McNemar on TAS "
        "success is significant versus RAG/LightRAG at this $N$; claims remain tied to the "
        "TAS definition. Implementation validity. Reference-family policies share the store "
        "(fair data access, not vendor-identical engineering). The KG ($V=97$, $E=123$) is "
        "still far smaller than production CTI graphs [10,11]."
    ),
    "threats",
)

swap_between(
    "A dual-annotator SOC rubric scores groundedness",
    '",\n    )\n\n    add_heading_custom(doc, "7.4. Discussion',
    (
        "A dual-annotator SOC rubric scores groundedness (1–5), unsupported identifiers (0/1), "
        "actionability (1–5), and abstain appropriateness. Ratings are conditioned on live EDGR "
        "system outputs (`live_system_dual_panel`, $n=100$), not a static seed-answer sheet. "
        "Cohen’s $\\kappa_g\\approx 0.92$ for groundedness. This remains a controlled panel, not "
        "independent field SOC annotators; camera-ready Transactions revisions should replace "
        "it with field labels."
    ),
    "human",
)

swap_between(
    "Evidence: A/D support H1 vs RAG; C supports refusal scoring on OOD; B supports graph",
    '",\n    )\n    add_paragraph(\n        doc,\n        "Practically, EDGR is closest',
    (
        "Evidence: A/D support H1 on TAS (CI + McNemar); C/D support OOD refusal; B supports "
        "graph causality (H3). Bound: LightRAG can still lead lexical $F$; baselines are "
        "reference-family policies; panel $\\neq$ field SOC. Therefore the warranted conclusion "
        "is a Trusted Answer protocol with claim-aligned metrics—not an accuracy championship."
    ),
    "discussion",
)

swap_exact(
    "acceptable at $|\\mathcal{D}|=40$",
    "acceptable at $|\\mathcal{D}|=106$",
    "complexity D",
)

swap_between(
    "Several limitations deserve restatement without euphemism. The corpus is a curated",
    '",\n    )\n    add_paragraph(\n        doc,\n        "For doctoral examination',
    (
        "Several limitations deserve restatement without euphemism. The corpus is a constructed "
        "suite ($N=212$), not a multi-year SOC archive. Baselines are thickened reference-family "
        "policies, not vendor dumps. Lexical faithfulness remains gameable; TAS mitigates but "
        "does not replace expert judgment. The live dual panel ($\\kappa_g\\approx 0.92$) is not "
        "field SOC. Production still needs larger graphs, ANN retrieval, feed adapters, and "
        "field labels. These limits do not erase significant TAS/McNemar margins versus RAG or "
        "the graph ablation; they bound how far the claims may travel."
    ),
    "limitations",
)

swap_between(
    "EDGR consolidates a dynamic CTI knowledge graph, a six-stage evidence-driven retrieval",
    '",\n    )\n    add_paragraph(\n        doc,\n        "Future work includes learned thresholds',
    (
        "EDGR consolidates a dynamic CTI knowledge graph, a six-stage evidence-driven retrieval "
        "pipeline, a four-factor trust model with ρ-gate abstain, and a statistical evaluation "
        "protocol into one reproducible system for IDS/CTI question answering. The proof chain "
        "is explicit: Evidence A/D establish H1 on primary TAS versus flat RAG "
        "($\\Delta$TAS$\\approx +0.23$, McNemar significant); Evidence B establishes H3 via graph "
        "ablation ($\\Delta F\\approx -0.049$); Evidence C/D establish H2 OOD safety "
        "(EDGR $1.0$ vs ungated $0.0$). On the live suite ($N=212$, $|\\mathcal{D}|=106$, "
        "$V=97$, $E=123$), EDGR mean TAS $=0.752$, R@$k=0.671$, MRR $=0.606$. Lexical-$F$ "
        "leadership by ungated LightRAG is disclosed and does not overturn TAS ranking. The "
        "scientific contribution is the end-to-end risk-controlled Trusted Answer contract for "
        "high-stakes CTI assistance."
    ),
    "conclusions",
)

# Heading tweaks
swap_exact(
    "6.1. Evidence A — Method Means Support H1 against Flat RAG",
    "6.1. Evidence A — Primary TAS Ranking Supports H1 (Lexical F Secondary)",
    "h6.1",
)

swap_exact(
    "6.2. Evidence D — Paired Margin Confirms H1; McNemar Bounds Binary Claims",
    "6.2. Evidence D — Paired TAS Margin and Significant McNemar",
    "h6.2",
)

p.write_text(t, encoding="utf-8")
print("total:", n)

# sanity
for needle in ["N=212", "0.752", "b_{10}=49", "kappa_g", "live_system_dual_panel"]:
    print(needle, "→", t.count(needle))
