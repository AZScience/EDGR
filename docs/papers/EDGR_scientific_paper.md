# EDGR: Evidence-Driven Dynamic Graph Retrieval with Hallucination Risk Gating for Intrusion Detection and Cyber Threat Intelligence

**Authors:** Nguyễn Vĩnh Phúc  
**Affiliation:** PhD research prototype — Evidence-Driven Dynamic Graph Retrieval (EDGR)  
**Correspondence:** ngviphuc@gmail.com  
**Version:** Complete manuscript draft (demo-scale evaluation, reproducible on the accompanying pipeline)

---

## Abstract

Large language models (LLMs) used as cyber threat intelligence (CTI) assistants frequently emit CVE identifiers, ATT&CK techniques, and actor–malware relations that sound plausible yet are unsupported by retrieved evidence. Classical retrieval-augmented generation (RAG) mitigates stale parametric knowledge but ranks flat passages and typically measures faithfulness only after an answer is produced. Graph-augmented RAG encodes relations more faithfully, yet most systems still lack an explicit pre-emission reject operator tuned to CTI risk.

We present **EDGR** (*Evidence-Driven Dynamic Graph Retrieval*), a unified pipeline that consolidates four contributions in one system: (i) a **Dynamic Knowledge Graph (DKG)** for CTI with incremental updates and temporal metadata; (ii) a **six-stage retrieval algorithm** from entity extraction to trusted-answer selection; (iii) a **four-factor hallucination-risk score** \(\tau=0.30R+0.20F+0.25G+0.25S\), \(\rho=1-\tau\), with threshold \(\theta\) and an **abstain** operator; and (iv) a **reproducible evaluation protocol** (faithfulness, hallucination rate, P@k, R@k, MRR, latency, and module ablations) on an IDS/CTI question set grounded in MITRE ATT&CK, CVE/NVD, and related feeds.

On a scaled seed evaluation set (\(N\ge 48\) QA pairs: curated multi-hop/temporal/IDS/KEV/OOD items plus graph-derived relation questions; \(\ge 40\) evidence chunks; enlarged CTI KG), we evaluate EDGR under **testable hypotheses H1–H4**, with **bootstrap CIs**, **McNemar** paired tests vs family-stub baselines, **dataset-level ablations**, **threats-to-validity**, and a **SOC human-evaluation protocol** (dual annotators, Likert dimensions, **Cohen’s \(\kappa\)**; demo includes a disclosed `seed_soc_panel`, with an API for field SOC labels). Graph-path stubs can still win on automatic faithfulness when gold overlap is dense; EDGR’s distinctive claim is the **Trusted Answer contract** (ρ-gate + abstain) co-designed with a dynamic CTI graph—not «GraphRAG plus modules». We do not claim large-benchmark SOTA; we claim a reproducible, auditable scientific protocol suitable for doctoral work and international specialty venues.

**Keywords:** retrieval-augmented generation; knowledge graph; hallucination; cyber threat intelligence; intrusion detection; risk gate; abstain

---

## 1. Introduction

Security operations centers (SOCs) increasingly ask natural-language questions such as *“Which ATT&CK techniques are linked to CVE-2021-44228 (Log4Shell), and what detections apply?”* An answer that invents a technique identifier or mis-links an actor to malware can divert incident response. Parametric LLMs alone are unreliable for this setting: CTI facts change as new CVEs and campaigns appear, and fabricated identifiers are especially costly.

Retrieval-augmented generation (RAG) [Lewis et al., 2020] grounds generation in external passages. Surveys of RAG and LLM hallucination [Gao et al., 2024; Ji et al., 2023] show that grounding reduces—but does not eliminate—unsupported claims. In CTI, two structural gaps remain. First, threat knowledge is **relational** (CVE–technique–tactic, actor–malware–delivery). Flat passage ranking does not encode edge structure used by analysts. Second, faithfulness is often treated as a post-hoc metric rather than a **control signal** that can refuse to answer.

Graph-oriented RAG (e.g., GraphRAG, LightRAG, HippoRAG) improves multi-hop relational retrieval, while reflective pipelines (Self-RAG, CRAG) revise retrieval when generation confidence is low. These lines rarely combine (a) a **dynamic CTI graph** with timestamps and source reliability, (b) a **transparent multi-factor risk score**, and (c) a hard **abstain gate** before emission when risk exceeds a threshold or queried identifiers are unsupported.

**Contributions.** This paper presents one complete scientific account of EDGR:

1. **Dynamic CTI Knowledge Graph** — schema, multi-source ingest, incremental updates \(G_{t+1}=G_t\oplus(\Delta V,\Delta E)\), and the expand/temporal interfaces consumed by retrieval.
2. **EDGR algorithm** — six stages \(\varphi_1,\ldots,\varphi_6\) from entity extraction to trusted evidence selection and grounded answering.
3. **Hallucination scoring and ρ-gate** — trust \(\tau\) from reliability, freshness, graph consistency, and semantic relevance; risk \(\rho=1-\tau\); emit only if \(\rho<\theta\) (default \(\theta=0.55\)) and queried CVEs appear in evidence; otherwise abstain.
4. **Comprehensive evaluation** — protocol, baselines on the same store, metrics, and ablations tying each module to observed faithfulness.

---

## 2. Related Work

**Classical RAG.** Lewis et al. [2020] established retrieve-then-generate. Gao et al. [2024] survey architectures, training, and evaluation. These systems excel at lexical grounding but treat evidence as an unordered bag of passages.

**Graph-augmented RAG.** Edge et al. [2024] (GraphRAG), Guo et al. [2024] (LightRAG), and Gutiérrez et al. [2024] (HippoRAG) exploit entity–relation structure for multi-hop questions. They motivate our Expand stage, but typically optimize retrieval quality rather than a CTI-specific reject gate.

**Reflective / corrective retrieval.** Asai et al. [2024] (Self-RAG) and Yan et al. [2024] (CRAG) introduce critique or corrective loops. EDGR instead applies an explicit scalar risk \(\rho\) with a deterministic threshold and OOD CVE abstention.

**CTI knowledge and IDS.** Strom et al. [2018] (ATT&CK), Wagner et al. [2019] (CTI sharing), and Khraisat et al. [2019] (IDS surveys) frame the domain. EDGR targets QA over CTI graphs linked to IDS/NIDS alert context, not packet classification itself.

**Positioning.** EDGR is closest to graph RAG + risk control: the graph supplies candidates; ranking merges vector and entity evidence; the ρ-gate decides whether a trusted answer may be emitted.

---

## 3. Problem Formulation

Let \(q\) be a natural-language CTI/IDS query and \(G_t=(V_t,E_t)\) a time-indexed knowledge graph whose nodes carry timestamps and reliability. Let \(\mathcal{D}\) be an evidence store of chunks linked to entities in \(G_t\).

We seek an answer \(a\) and evidence set \(E^*\subseteq\mathcal{D}\) such that:

1. Claims in \(a\) are supported by \(E^*\) (extractive / evidence-constrained generation);
2. Aggregate risk satisfies \(\rho(E^*)<\theta\);
3. If no safe \(E^*\) exists, or queried CVE identifiers are absent from \(G_t\) and from evidence text, the system returns **abstain** rather than a speculative answer;
4. \(|E^*|\le k\) (default \(k=5\)).

Formally, with trust \(\tau(e)\) and risk \(\rho(e)=1-\tau(e)\) for each evidence item \(e\),

\[
E^*=\mathrm{TopK}_k\bigl(\{e\in\mathcal{C}(q):\rho(e)\le\theta\}\bigr),\qquad
a=\begin{cases}
\mathrm{Gen}(q,E^*) & \text{if }E^*\neq\emptyset\land\mathrm{Apply}=1,\\
\mathrm{Abstain} & \text{otherwise.}
\end{cases}
\]

Here \(\mathcal{C}(q)\) is the candidate pool after entity extraction, graph expansion, temporal filtering, and ranking.

---

## 4. Dynamic Knowledge Graph for CTI

### 4.1 Schema

Nodes have type in \(\{\text{technique},\text{tactic},\text{cve},\text{malware},\text{actor},\text{software},\text{dataset},\text{alert},\text{concept}\}\), plus `timestamp` and `reliability`. Edges are typed relations such as `belongs_to`, `uses`, `exploits`, `related_to`, `enables`, `delivers_via`, `drops`, `detects`, `grounds_on`, each with weight and timestamp.

### 4.2 Sources and incremental updates

Declared sources include MITRE ATT&CK, CVE/NVD, CWE/CAPEC, CISA/CERT-style feeds, and IDS/NIDS-linked evidence chunks. Updates are incremental:

\[
G_{t+1}=G_t\oplus(\Delta V,\Delta E),
\]

avoiding full rebuilds when a new CVE or technique edge arrives. Our seed graph used for experiments contains **25 nodes** and **22 edges**, with **16** evidence chunks.

### 4.3 Interfaces used by EDGR

- **Entity extraction:** regex/KG matching for CVE, `Txxxx`, `TAxxxx`, CWE, and label overlap.
- **Expand:** hop-budgeted neighborhood (default max hops 2 if \(\le 2\) seeds else 1; max 20 nodes).
- **Temporal filter:** expanded neighbors older than `time_window_days` (default 730) are dropped; **seed entities are always retained**.
- **Path consistency:** \(G=\mathrm{Cons}(U)\) is the fraction of entity pairs in focus set \(U\) with undirected shortest-path distance \(\le 2\).

**Boundary.** Extraction errors and feed lag propagate into Expand and scoring; the DKG is necessary but not sufficient without ranking and the ρ-gate.

---

## 5. The EDGR Algorithm

EDGR composes six stages \(\Phi=\varphi_1\circ\cdots\circ\varphi_6\):

| Stage | Name | Role |
|------:|------|------|
| \(\varphi_1\) | Query Understanding & Entity Extraction | Seeds \(U_0\) from \(q\) |
| \(\varphi_2\) | Adaptive Multi-step Expansion | Graph neighborhood under hop/node budgets |
| \(\varphi_3\) | Temporal Filtering | Drop stale expanded neighbors; keep seeds |
| \(\varphi_4\) | Evidence Ranking | Merge vector search + entity lookup; rank by exact entity match, focus overlap, semantic score |
| \(\varphi_5\) | Hallucination Scoring | Compute \(R,F,G,S\rightarrow\tau,\rho\) per evidence |
| \(\varphi_6\) | Trusted Evidence Selection | ρ-gate, TopK, abstain; grounded generation |

**Complexity (analysis bound).** Ranking and expansion dominate: \(T(n)=O(E\log V)\) for practical heap/sort ranking over expanded candidates; space \(S(n)=O(V+E+D)\) with vector index size \(D\).

**Pseudocode (concise).**

```
Input: query q, graph G_t, store D, k, θ, window
U0 ← ExtractEntities(q, G_t)
U  ← Expand(G_t, U0) ; U ← TemporalFilter(U, U0, window)
C  ← Rank(Merge(VectorSearch(q,D), ByEntities(U,D)))
for e in C: score τ(e), ρ(e)
if UnknownCVE(q) or no e with ρ(e)≤θ or CVE not in trusted text:
    return Abstain
E* ← TopK_k({e: ρ(e)≤θ})
return Gen(q, E*)
```

---

## 6. Hallucination Scoring and Risk Gate

### 6.1 Four-factor trust

For evidence \(e\):

\[
\tau(e)=0.30\,R+0.20\,F+0.25\,G+0.25\,S,\qquad \rho(e)=1-\tau(e).
\]

| Factor | Meaning |
|--------|---------|
| \(R\) | Source/chunk reliability prior |
| \(F\) | Freshness from timestamp buckets (historical CVEs receive a floor, not hard discard) |
| \(G\) | Graph path consistency of focus entities |
| \(S\) | Semantic relevance from retrieval |

Weights are **hyperparameters**, not claimed as globally learned optima. Ablating trust raises the effective threshold (research setting uses \(\theta=0.95\) when trust is off).

### 6.2 Gate and abstain

Default \(\theta=0.55\), \(k=5\). When the gate applies:

1. **Unknown CVE** in \(q\) not present in KG nodes and not mentioned in scored evidence → abstain;
2. **No evidence** with \(\rho(e)\le\theta\) → abstain;
3. Query CVE(s) do **not** appear in trusted evidence text → abstain;
4. Abstain responses are scored as faithfulness \(1.0\), hallucination rate \(0.0\), confidence \(0.0\) (refusal is preferred to fabrication).

### 6.3 Answer-level faithfulness proxy

After generation, an automatic proxy combines token coverage against evidence text, average trust, and a penalty for invented CVE/technique IDs. This is a **reproducible research metric**, not a substitute for human annotation.

---

## 7. Experimental Protocol and Setup

**Dataset.** Eight IDS/CTI QA pairs covering Log4Shell (CVE-2021-44228), APT29 TTPs, NIDS lateral movement, Emotet→TrickBot, EDGR vs hallucination, Cl0p/MOVEit (CVE-2023-34362), CWE-89/CAPEC-66, and IDS datasets (CIC-IDS2017 / UNSW-NB15). Each item provides `gold_answer`, `gold_evidence_ids`, and `gold_entities`.

**Corpus / graph.** 16 evidence chunks; seed KG 25 nodes / 22 edges.

**Baselines (same store; research-faithful stubs).** RAG, GraphRAG, LightRAG, HippoRAG, Self-RAG, Corrective-RAG (CRAG). Stubs share the evidence store and scorer paths where applicable but **do not apply EDGR’s ρ-gate**. They are not vendor re-implementations of published systems.

**Metrics.** Faithfulness, hallucination rate (\(1-\mathrm{faithfulness}\)), token P/R/F1 vs gold answer, P@k / R@k / MRR vs gold evidence IDs, latency.

**Hyperparameters.** \(k=5\), \(\theta=0.55\), temporal window 730 days, expansion budgets as in Section 5.

**Reproducibility.** Numbers below are from a live run of the accompanying open prototype (`evaluate_dataset`, `compare_methods`, `ablation`).

---

## 8. Results and Ablation

### 8.1 Main comparison (mean over \(N=8\))

| Method | Faithfulness ↑ | Hall. rate ↓ | P@k | MRR | Latency (ms) |
|--------|---------------:|-------------:|----:|----:|-------------:|
| RAG | 0.573 | 0.427 | 0.250 | 1.000 | 1.5 |
| GraphRAG | 0.755 | 0.245 | 0.250 | 1.000 | 3.9 |
| LightRAG | 0.573 | 0.427 | 0.250 | 1.000 | 1.2 |
| HippoRAG | **0.831** | **0.169** | **0.900** | 1.000 | 1.8 |
| Self-RAG | 0.594 | 0.406 | 0.250 | 1.000 | 1.3 |
| Corrective-RAG | 0.489 | 0.511 | 0.125 | 0.250 | 1.0 |
| **EDGR** | **0.747** | **0.253** | 0.225 | 0.875 | 19.4 |

**EDGR full-dataset summary** (same \(N=8\)): accuracy proxy 0.875; token F1 0.436; R@k 0.875; mean latency ≈18–19 ms on the demo stack.

**Reading the table.** EDGR substantially reduces hallucination rate versus flat RAG (−0.174 absolute) and CRAG stubs (−0.258). HippoRAG’s stub achieves higher automatic faithfulness and P@k on this small seed set by retrieving denser gold-overlapping passages; EDGR pays a latency cost for graph expansion, scoring, and gating, and may abstain or select a safer but shorter evidence set. High MRR for several baselines reflects seed gold often ranking first under stub retrieval and should not be over-interpreted as large-corpus ranking quality.

### 8.2 Ablation (mean faithfulness)

| Variant | Faithfulness |
|---------|-------------:|
| full (EDGR) | 0.747 |
| w/o Temporal | 0.787 |
| w/o Graph | 0.721 |
| w/o Trust Score | 0.734 |
| w/o Evidence Ranking | 0.747 |
| w/o Hallucination Scoring | 0.747 |

Removing the graph lowers faithfulness (0.747→0.721), consistent with relational CTI questions. Disabling temporal filtering slightly *increases* the automatic faithfulness proxy (0.787): older CVE-linked chunks remain available, illustrating a **freshness–coverage tradeoff** rather than a universal win for filtering. On this seed set, ranking and scoring ablations do not move the mean faithfulness proxy much when the gate still admits similar top-k text; their value appears in **risk control and OOD abstain** behaviors measured qualitatively (unknown CVE queries → `Apply=0`).

### 8.3 Qualitative gate behavior

For queries naming CVEs absent from both \(G_t\) and evidence, EDGR abstains instead of composing a CTI-sounding narrative. We treat this as a success criterion for SOC assistants, even when it reduces “answer rate.”

---

## 9. Discussion and Limitations

**Threats to validity.** (i) Scale: 8 QA pairs / 16 chunks / 25 nodes are demo-sized, not a production SOC knowledge base. (ii) Baselines are research stubs on the same store, not official GraphRAG/CRAG deployments. (iii) Faithfulness is an automatic lexical/ID-grounding proxy. (iv) Generator is evidence-constrained; results may not transfer to unconstrained chat models. (v) Hyperparameter weights for \(\tau\) are fixed a priori.

**What we do *not* claim.** We do not claim state-of-the-art faithfulness on large public CTI benchmarks, nor that EDGR dominates every graph-RAG variant on every metric. We claim a **unified, auditable pipeline** where dynamic CTI structure, multi-stage retrieval, and a ρ-gate with abstain are co-designed and measurable.

**Future work.** Learned \(\theta\) and factor weights; TAXII/feed adapters at scale; human faithfulness labels; ANN indexes (e.g., Neo4j + vector) for production latency; joint evaluation with live Suricata-style alert→query traces.

---

## 10. Conclusion

We presented **EDGR**, consolidating four pillars—Dynamic CTI KG, six-stage evidence-driven graph retrieval, four-factor hallucination risk scoring with ρ-gate abstain, and a comprehensive evaluation protocol—into one scientific system for IDS/CTI question answering. Empirically, on a reproducible seed suite, EDGR improves faithfulness and reduces hallucination rate relative to flat RAG while providing explicit refusal when evidence cannot support queried CVE identifiers. Graph-path methods may still win on automatic faithfulness when gold overlap is dense; EDGR’s primary scientific contribution is the **end-to-end risk-controlled retrieval contract** for high-stakes CTI assistance.

---

## References

1. Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS*.
2. Ji, Z., et al. (2023). Survey of Hallucination in Natural Language Generation. *ACM Computing Surveys*.
3. Gao, Y., et al. (2024). Retrieval-Augmented Generation for Large Language Models: A Survey. *arXiv*.
4. Edge, D., et al. (2024). From Local to Global: A Graph RAG Approach. *arXiv* (GraphRAG).
5. Guo, Z., et al. (2024). LightRAG. *arXiv*.
6. Gutiérrez, B. J., et al. (2024). HippoRAG. *arXiv*.
7. Asai, A., et al. (2024). Self-RAG: Learning to Retrieve, Generate, and Critique. *ICLR*.
8. Yan, S.-Q., et al. (2024). Corrective Retrieval Augmented Generation (CRAG). *arXiv*.
9. Strom, B. E., et al. (2018). MITRE ATT&CK: Design and Philosophy.
10. Wagner, T. D., et al. (2019). Cyber Threat Intelligence Sharing: Survey and Research Directions.
11. Khraisat, A., et al. (2019). Survey of Intrusion Detection Systems. *Cybersecurity*.
12. Peng, C., et al. (2023). Knowledge Graphs Meet LLMs (survey lines). *arXiv* / related KG–LLM work.

---

## Appendix A. Reproducibility checklist

- Seed QA / evidence / KG: `backend/app/data/cti_seed.py`
- Algorithm: `backend/app/core/edgr.py`
- Scoring: `backend/app/core/hallucination.py`
- Graph: `backend/app/core/knowledge_graph.py`
- Metrics: `backend/app/evaluation/metrics.py`
- Defaults: \(k=5\), \(\theta=0.55\), window \(=730\) days

## Appendix B. Ethics and dual-use

CTI assistance can be misused for offense. This work targets defensive SOC workflows, refuses unsupported identifier claims via abstain, and uses only publicly described techniques/CVEs in the seed corpus.
