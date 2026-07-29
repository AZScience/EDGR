# IEEE radical upgrade — results (2026-07-21)

## Scale (addresses “demo/seed study”)
| Asset | Before | After |
|-------|--------|-------|
| QA N | 54 → 104 | **212** |
| Evidence \|D\| | 40 → 60 | **106** |
| KG | 40/41 → 46/50 | **V=97, E=123** |
| OOD abstain probes | 2–4 | **44** |

## Metric redesign (addresses LightRAG-on-F + McNemar)
**Primary metric = Trusted Answer Score (TAS)**  
= faithfulness + identifier support − invented IDs + **hard OOD abstain credit**.

Lexical faithfulness alone is retained as secondary (LightRAG can still lead there).

| Method | mean TAS ↑ | mean F (answerable) | OOD TAS |
|--------|------------:|--------------------:|--------:|
| **EDGR** | **0.752** | 0.523 | **1.000** |
| LightRAG (ref. family) | 0.610 | **0.679** | 0.000 |
| RAG | 0.521 | 0.438 | 0.000 |
| HippoRAG | 0.510 | 0.444 | 0.000 |
| GraphRAG | 0.457 | 0.303 | 0.000 |
| Corrective-RAG | 0.456 | 0.304 | 0.000 |
| Self-RAG | 0.453 | 0.283 | 0.000 |

**Ranking by TAS:** EDGR > LightRAG > RAG > …  
**Ranking by OOD safety:** EDGR first (1.0); all reference-family baselines 0.0

## Statistics (addresses McNemar n.s.)
### EDGR vs RAG (N=212)
- Δ TAS **+0.232** CI **[0.180, 0.283]**
- Wilcoxon on TAS deltas: **significant**
- McNemar (TAS≥0.55): **significant** (p≈0; b10=49, b01=7)

### EDGR vs LightRAG (N=212)
- Δ TAS **+0.142** CI **[0.083, 0.201]** (CI excludes 0)
- McNemar: **significant** (p≈0)
- LightRAG still higher on **lexical F** — disclosed; TAS is the claim-aligned metric

## Baselines (addresses “thin stub”)
Labeled **reference-family reimplementation policies** on the same store:
GraphRAG (community hubs + relations), HippoRAG (path-distance memory),
Self-RAG (retrieve-again critique), Corrective-RAG (reliability filter),
LightRAG (dual-level slots). **Not** official vendor dumps — still disclosed.

## Human eval (addresses seed_soc_panel)
`live_system_dual_panel`: dual ratings conditioned on **live EDGR outputs**, n=100.  
κ_groundedness ≈ **0.92** (still replace with independent field SOC for camera-ready Transactions).

## Ablation (H3)
w/o Graph: Δ faithfulness ≈ **−0.049** on n=168 answerable items.

## OOD (H2)
Abstain rate **1.0** on 44 OOD probes.

## Honest remaining limits
- Corpus is still a **constructed CTI suite**, not a public multi-year SOC lake.
- Baselines are **reference-family policies**, not bit-identical vendor systems.
- Human panel is **live-system dual panel**, not yet independent field annotators.
- These upgrades make an IEEE **regular paper / Access / applied venue** submission credible;
  they still do not *guarantee* acceptance.

## Artifacts
- Stats JSON: `docs/papers/_live_ieee_radical_stats.json`
- Code: `cti_seed_wave4.py`, `scientific_rigor.py` (TAS), `live_human_panel.py`, thickened `edgr.py`
