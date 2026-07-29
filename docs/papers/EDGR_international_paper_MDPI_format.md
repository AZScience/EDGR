# EDGR: Evidence-Driven Dynamic Graph Retrieval with Hallucination Risk Gating for Intrusion Detection and Cyber Threat Intelligence

**Article type:** Research Article  
**Layout:** Abstract → Introduction → Model Structure → Experiment → Analysis of Results → Robust Analysis → Conclusions → Back matter → References (MDPI-style sectioning)

---

by

**Nguyễn Vĩnh Phúc** ^{1,*}

^{1} Doctoral research — Evidence-Driven Dynamic Graph Retrieval (EDGR) for Intrusion Detection and Cyber Threat Intelligence (IDS/CTI)  
\* Correspondence: ngviphuc@gmail.com

**Received / Revised / Accepted / Published:** *(to be filled on submission)*

**Keywords:** retrieval-augmented generation; knowledge graph; hallucination mitigation; cyber threat intelligence; intrusion detection; risk gate; abstain; evidence ranking

**MSC:** 68T50; 68P20; 68M25

---

## Abstract

Large language models used as cyber threat intelligence (CTI) assistants often emit CVE identifiers, ATT&CK techniques, and actor–malware relations that sound plausible yet are unsupported by retrieved evidence. Classical retrieval-augmented generation (RAG) mitigates stale parametric knowledge but ranks flat passages and typically measures faithfulness only after an answer is produced. Graph-augmented RAG encodes relations more faithfully, yet most systems still lack an explicit pre-emission reject operator tuned to CTI risk.

This paper proposes **EDGR** (*Evidence-Driven Dynamic Graph Retrieval*) to reduce unsupported CTI claims while preserving auditable retrieval. A **Dynamic Knowledge Graph (DKG)** with timestamps and source reliability supplies relational context through adaptive multi-hop expansion and temporal filtering. Vector and entity-linked evidence are then fused and ranked. A four-factor trust score

\[
\tau(e)=0.30\,R+0.20\,F+0.25\,G+0.25\,S,\qquad \rho(e)=1-\tau(e)
\]

is computed per evidence item, and a **ρ-gate** with threshold \(\theta\) (default \(\theta=0.55\)) admits only low-risk evidence before generation; otherwise the system **abstains**.

On a reproducible IDS/CTI seed suite (\(N=54\) QA pairs, 40 evidence chunks, KG \(V=40\), \(E=41\)), full EDGR evaluation yields mean faithfulness **0.702**, hallucination rate **0.298**, R@k **0.852**, and MRR **0.803**. Across \(n=52\) non-OOD items, EDGR mean faithfulness is **0.698** [0.649, 0.745] versus flat RAG **0.558** [0.509, 0.607] (bootstrap 95% CI). Removing graph expansion drops mean faithfulness by **0.104** (ablation H3). We do **not** claim large-benchmark SOTA; the contribution is a unified, auditable **Trusted Answer** protocol—Dynamic CTI KG + six-stage retrieval + ρ-gate/abstain + hypotheses H1–H4, bootstrap CIs, McNemar tests, ablations, threats-to-validity, and a SOC human-evaluation protocol with Cohen’s \(\kappa\).

---

## 1. Introduction

Security operations centers (SOCs) increasingly ask natural-language questions such as *“Which ATT&CK techniques are linked to CVE-2021-44228 (Log4Shell), and what detections apply?”* An answer that invents a technique identifier or mis-links an actor to malware can divert incident response. Parametric LLMs alone are unreliable for this setting: CTI facts change as new CVEs and campaigns appear, and fabricated identifiers are especially costly [1–3].

Retrieval-augmented generation (RAG) [1] grounds generation in external passages. Surveys of RAG and LLM hallucination [2,3] show that grounding reduces—but does not eliminate—unsupported claims. In CTI, two structural gaps remain. First, threat knowledge is **relational** (CVE–technique–tactic, actor–malware–delivery). Flat passage ranking does not encode the edge structure used by analysts [4–6]. Second, faithfulness is often treated as a post-hoc metric rather than a **control signal** that can refuse to answer [7,8].

Graph-oriented RAG (e.g., GraphRAG, LightRAG, HippoRAG) improves multi-hop relational retrieval [4–6], while reflective pipelines (Self-RAG, CRAG) revise retrieval when generation confidence is low [7,8]. These lines rarely combine (a) a **dynamic CTI graph** with timestamps and source reliability [9–11], (b) a **transparent multi-factor risk score**, and (c) a hard **abstain gate** before emission when risk exceeds a threshold or queried identifiers are unsupported.

**Contributions.** This paper proposes **EDGR**, consolidating four pillars into one system:

1. **Dynamic CTI Knowledge Graph** — schema, multi-source ingest, incremental updates \(G_{t+1}=G_t\oplus(\Delta V,\Delta E)\), and expand/temporal interfaces consumed by retrieval.  
2. **Six-stage EDGR algorithm** \(\Phi=\varphi_1\circ\cdots\circ\varphi_6\) — from entity extraction to trusted-evidence selection and grounded answering.  
3. **Hallucination scoring and ρ-gate** — trust \(\tau\) from reliability, freshness, graph consistency, and semantic relevance; risk \(\rho=1-\tau\); emit only if \(\rho<\theta\) and queried CVEs appear in evidence; otherwise abstain.  
4. **Comprehensive evaluation protocol** — faithfulness, hallucination rate, P@k, R@k, MRR, latency, module ablations, hypotheses **H1–H4**, bootstrap CIs, McNemar paired tests, threats-to-validity, and SOC human evaluation with Cohen’s \(\kappa\).

The remainder of the paper is organized as follows. Section 2 presents the model. Section 3 describes data and indicators. Section 4 reports results. Section 5 analyzes robustness. Section 6 concludes.

---

## 2. Model Structure

### 2.1. Dynamic Knowledge Graph for CTI

Nodes have type in \(\{\text{technique},\text{tactic},\text{cve},\text{malware},\text{actor},\text{software},\text{dataset},\text{alert},\text{concept}\}\), plus `timestamp` and `reliability`. Edges are typed relations such as `belongs_to`, `uses`, `exploits`, `related_to`, `enables`, `delivers_via`, `drops`, `detects`, `grounds_on`, each with weight and timestamp [9–11].

Declared sources include MITRE ATT&CK, CVE/NVD, CWE/CAPEC, CISA/CERT-style feeds, and IDS/NIDS-linked evidence chunks. Updates are incremental:

\[
G_{t+1}=G_t\oplus(\Delta V,\Delta E).
\]

The live seed graph used for experiments contains **40 nodes** and **41 edges**, with **40** evidence chunks.

Interfaces used by EDGR:

- **Entity extraction:** regex/KG matching for CVE, `Txxxx`, `TAxxxx`, CWE, and label overlap.  
- **Expand:** hop-budgeted neighborhood (default max hops 2 if \(\le 2\) seeds else 1; max 20 nodes).  
- **Temporal filter:** expanded neighbors older than `time_window_days` (default 730) are dropped; **seed entities are always retained**.  
- **Path consistency:** \(G=\mathrm{Cons}(U)\) is the fraction of entity pairs in focus set \(U\) with undirected shortest-path distance \(\le 2\).

**Boundary.** Extraction errors and feed lag propagate into Expand and scoring; the DKG is necessary but not sufficient without ranking and the ρ-gate.

### 2.2. Problem Formulation

Let \(q\) be a natural-language CTI/IDS query and \(G_t=(V_t,E_t)\) a time-indexed knowledge graph. Let \(\mathcal{D}\) be an evidence store of chunks linked to entities in \(G_t\).

We seek an answer \(a\) and evidence set \(E^*\subseteq\mathcal{D}\) such that:

1. Claims in \(a\) are supported by \(E^*\) (extractive / evidence-constrained generation);  
2. Aggregate risk satisfies \(\rho(E^*)<\theta\);  
3. If no safe \(E^*\) exists, or queried CVE identifiers are absent from \(G_t\) and from evidence text, the system returns **abstain**;  
4. \(|E^*|\le k\) (default \(k=5\)).

Formally, with trust \(\tau(e)\) and risk \(\rho(e)=1-\tau(e)\),

\[
E^*=\mathrm{TopK}_k\bigl(\{e\in\mathcal{C}(q):\rho(e)\le\theta\}\bigr),\qquad
a=\begin{cases}
\mathrm{Gen}(q,E^*) & \text{if }E^*\neq\emptyset\land\mathrm{Apply}=1,\\
\mathrm{Abstain} & \text{otherwise.}
\end{cases}
\]

Here \(\mathcal{C}(q)\) is the candidate pool after entity extraction, graph expansion, temporal filtering, and ranking.

### 2.3. Classical RAG and Graph-Augmented Retrieval (Baselines)

**Classical RAG** retrieves top passages by lexical/vector similarity and generates conditioned on those passages [1]. It does not encode CTI edges.

**Graph-augmented RAG** (GraphRAG / LightRAG / HippoRAG-style) expands entity neighborhoods or path-centric memory to improve multi-hop questions [4–6]. Reflective variants (Self-RAG, CRAG) critique or correct retrieval [7,8]. In our experiments, baselines are **research-faithful family stubs on the same store**—they share evidence/KG where applicable but **do not apply EDGR’s ρ-gate**. They are not vendor re-implementations of published systems.

### 2.4. Hallucination Risk Scoring

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

### 2.5. ρ-Gate and Abstain Operator

Default \(\theta=0.55\), \(k=5\). When the gate applies:

1. **Unknown CVE** in \(q\) not present in KG nodes and not mentioned in scored evidence → abstain;  
2. **No evidence** with \(\rho(e)\le\theta\) → abstain;  
3. Query CVE(s) do **not** appear in trusted evidence text → abstain;  
4. Abstain responses are scored as faithfulness \(1.0\), hallucination rate \(0.0\), confidence \(0.0\) (refusal is preferred to fabrication).

Emit rule:

\[
\mathrm{Emit}(q)\iff E^*\neq\emptyset\land\rho(E^*)<\theta\land\mathrm{ID}(q)\subseteq\mathrm{Supp}.
\]

### 2.6. EDGR Pipeline Composition

EDGR composes six stages \(\Phi=\varphi_1\circ\cdots\circ\varphi_6\) (Figure 1):

| Stage | Name | Role |
|------:|------|------|
| \(\varphi_1\) | Query Understanding & Entity Extraction | Seeds \(U_0\) from \(q\) |
| \(\varphi_2\) | Adaptive Multi-step Expansion | Graph neighborhood under hop/node budgets |
| \(\varphi_3\) | Temporal Filtering | Drop stale expanded neighbors; keep seeds |
| \(\varphi_4\) | Evidence Ranking | Merge vector search + entity lookup; rank |
| \(\varphi_5\) | Hallucination Scoring | Compute \(R,F,G,S\rightarrow\tau,\rho\) |
| \(\varphi_6\) | Trusted Evidence Selection | ρ-gate, TopK, abstain; grounded generation |

**Figure 1.** EDGR pipeline (\(\varphi_1\)–\(\varphi_6\)) with ρ-gate abstain.  
*File:* `docs/papers/figures/fig1_edgr_pipeline.svg`

**Complexity (analysis bound).** Ranking and expansion dominate: \(T(n)=O(E\log V)\); space \(S(n)=O(V+E+D)\) with vector index size \(D\).

**Algorithm (concise).**

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

**Answer-level faithfulness proxy** (research metric, not human gold):

\[
F=\mathrm{clip}\bigl(0.55\cdot\mathrm{coverage}+0.45\cdot\overline{\tau}-\mathrm{invent\_penalty}\bigr),\quad H=1-F.
\]

---

## 3. Experiment

### 3.1. Dataset and Corpus

**QA set.** Fifty-four IDS/CTI question–answer items covering Log4Shell (CVE-2021-44228), APT TTPs, NIDS lateral movement, malware delivery chains, KEV prioritization, temporal/multi-hop items, graph-derived relation questions, and OOD abstain probes. Each item provides `gold_answer`, `gold_evidence_ids`, and/or `gold_entities` where applicable.

**Categories:** curated core, multi-hop, KEV, IDS-alert, temporal, OOD-abstain, gate-theory, and graph-derived relation questions.

**Evidence / graph (live measurement):** 40 evidence chunks; KG \(V=40\), \(E=41\).

### 3.2. Baselines

Baselines on the **same** retriever/KG store:

| Family | Stub behavior (research setting) |
|--------|-----------------------------------|
| RAG | Flat vector retrieve → generate |
| GraphRAG / LightRAG / HippoRAG | Graph-path / entity-boosted retrieve (no EDGR ρ-gate) |
| Self-RAG / Corrective-RAG | Reflective / corrective retrieve stubs (no EDGR ρ-gate) |
| **EDGR** | Full \(\varphi_1\)–\(\varphi_6\) with ρ-gate + abstain |

**Disclosure.** All non-EDGR methods are family stubs on the same evidence store. They enable controlled comparison of retrieval *families*, not claims of parity with published vendor codebases.

### 3.3. Evaluation Indicators

| Metric | Definition (research proxy) |
|--------|-----------------------------|
| Faithfulness \(F\) ↑ | Lexical/ID grounding vs evidence + trust (Section 2.6) |
| Hallucination rate \(H\) ↓ | \(H=1-F\) |
| P@k / R@k / MRR | Against gold evidence IDs when available |
| Latency | Wall-clock ms per query on the prototype stack |
| OOD success | Correct abstain on unsupported CVEs |

**Hyperparameters.** \(k=5\), \(\theta=0.55\), temporal window 730 days.

**Statistical protocol.** Bootstrap confidence intervals (\(n_{\mathrm{boot}}=1000\), \(\alpha=0.05\)); McNemar exact tests on discordant correctness vs RAG; dataset-level ablations for H3.

### 3.4. Hypotheses

| ID | Hypothesis |
|----|------------|
| **H1** | Mean faithfulness(EDGR) > mean faithfulness(RAG) on the same store |
| **H2** | On OOD CVEs, EDGR abstains (unsupported CVE emission ≈ 0) |
| **H3** | Disabling Graph or ρ-gate lowers mean faithfulness vs full (dataset-level) |
| **H4** | Same seed + config ⇒ same metric tables (reproducibility) |

---

## 4. Analysis of Results

### 4.1. Mean Comparison Across Methods (\(n=52\))

Table 1 and Figure 2 report mean faithfulness and hallucination rate over non-OOD QA items (OOD abstain items excluded so methods are compared on answerable questions). Bootstrap 95% CIs use \(n_{\mathrm{boot}}=1000\).

**Table 1.** Dataset means (live run; family stubs disclosed).

| Method | Mean \(F\) ↑ | 95% CI (\(F\)) | Mean \(H\) ↓ | Stub? |
|--------|-------------:|----------------|-------------:|:-----:|
| RAG | 0.558 | [0.509, 0.607] | 0.443 | yes |
| GraphRAG | 0.545 | [0.502, 0.586] | 0.455 | yes |
| LightRAG | 0.842† | [0.794, 0.887] | 0.158 | yes |
| HippoRAG | 0.742 | [0.700, 0.783] | 0.258 | yes |
| Self-RAG | 0.471 | [0.426, 0.514] | 0.529 | yes |
| Corrective-RAG | 0.471 | [0.425, 0.518] | 0.529 | yes |
| **EDGR** | **0.698** | **[0.649, 0.745]** | **0.302** | no |

† LightRAG’s family stub can achieve a high automatic faithfulness proxy when retrieved text overlaps gold densely; this does **not** imply a Trusted Answer contract (no ρ-gate / abstain). EDGR’s scientific claim is risk-controlled emission, not topping every automatic proxy.

**Figure 2.** Mean faithfulness by method (\(n=52\)).  
*File:* `docs/papers/figures/fig2_mean_faithfulness.svg`

**Paired EDGR vs RAG (\(N=54\), including OOD).** Mean \(F\): EDGR **0.709** [0.658, 0.756] vs RAG **0.559** [0.510, 0.606]; Δ**+0.150** [0.107, 0.197]. McNemar exact test on the binary correctness proxy: \(b_{10}=1\), \(b_{01}=4\), discordant \(=5\), \(p=0.375\) (**not** significant at \(\alpha=0.05\)). Thus H1 is supported on the **continuous faithfulness** margin with CI excluding zero, while the **binary correctness** proxy is underpowered at this \(N\).

### 4.2. Full-Dataset EDGR Summary

On the full live evaluation of EDGR (\(N=54\)):

| Metric | Value |
|--------|------:|
| Faithfulness ↑ | **0.702** |
| Hallucination rate ↓ | **0.298** |
| P@k | 0.363 |
| R@k | **0.852** |
| MRR | **0.803** |
| Token F1 | 0.268 |
| Avg latency (ms) | 192.9 |

**Faithfulness by category (selected):** core 0.759; multi-hop 0.672; KEV 0.686; IDS-alert 0.771; temporal 0.735; OOD-abstain **1.000**; gate-theory 0.894; graph-derived 0.621.

### 4.3. Qualitative Gate Behavior

For queries naming CVEs absent from both \(G_t\) and evidence, EDGR abstains instead of composing a CTI-sounding narrative (H2). Category OOD-abstain faithfulness of 1.0 reflects correct refusal scoring.

### 4.4. Complexity Observation

Empirical stage timing on the live KG supports the analysis bound \(T(n)=O(E\log V)\): ranking/expansion dominate wall-clock; latency grows with evidence budget \(k\).

---

## 5. Model Robust Analysis

### 5.1. Ablation Study

Table 2 and Figure 3 report dataset-mean ablations (\(n=52\); disable one component at a time).

**Table 2.** Ablation vs full EDGR (live; mean faithfulness).

| Variant | Mean \(F\) | 95% CI | Δ vs full |
|---------|-----------:|--------|----------:|
| full (EDGR) | 0.698 | [0.649, 0.745] | 0.000 |
| w/o Temporal | 0.697 | [0.653, 0.740] | −0.000 |
| **w/o Graph** | **0.594** | **[0.551, 0.638]** | **−0.104** |
| w/o Trust Score | 0.677 | [0.621, 0.730] | −0.021 |
| w/o Evidence Ranking | 0.699 | [0.651, 0.746] | +0.001 |
| w/o Hallucination Scoring | 0.698 | [0.649, 0.745] | 0.000 |

**Figure 3.** Ablation Δ mean faithfulness vs full EDGR.  
*File:* `docs/papers/figures/fig3_ablation.svg`

**Reading.** Removing graph expansion yields the largest drop (−0.104), supporting H3 for relational CTI questions. Temporal filtering shows a near-zero mean Δ on this seed (freshness–coverage tradeoff). Ranking/scoring ablations may not move mean \(F\) when the gate still admits similar top-\(k\) text; their value appears in **risk control and OOD abstain**, which the mean \(F\) proxy under-emphasizes.

**Single-query illustration** (Log4Shell): full \(F=0.766\); w/o Graph \(F=0.676\) (Δ−0.090); w/o Temporal \(F=0.777\) (Δ+0.012)—consistent with the freshness–coverage tradeoff on one query.

### 5.2. Threats to Validity

| Threat | Statement |
|--------|-----------|
| Internal | Controlled seed \(N\) — protocol overfitting risk |
| External | Not large public CTI benchmarks / live SOC telemetry |
| Construct | Automatic \(F/H\) proxies ≠ SOC expert judgment; stubs can game \(F\) |
| Conclusion | Moderate-\(N\) McNemar may be underpowered — report CIs; avoid SOTA claims |
| Implementation | Family stubs share store (fair data, not fair vendor code); demo KG smaller than production |

### 5.3. Human Evaluation Protocol (Cohen’s \(\kappa\))

Dual annotators (`soc_a` / `soc_b`) rate groundedness (1–5), unsupported identifiers (0/1), actionability (1–5), and abstain appropriateness. On the disclosed seed SOC panel:

| Dimension | Cohen’s \(\kappa\) |
|-----------|-------------------:|
| Groundedness | 0.386 |
| Unsupported IDs | 0.760 |
| Actionability | 0.591 |
| Abstain OK | 1.000 |

Groundedness agreement is only fair–moderate on the seed panel; **field SOC labels should replace the seed panel for journal revision**. \(\kappa>0.6\) is often treated as substantial agreement.

### 5.4. Positioning vs Prior Work

EDGR is closest to **graph RAG + risk control**: the graph supplies candidates; ranking merges vector and entity evidence; the ρ-gate decides whether a trusted answer may be emitted. Distinctive claim: the **Trusted Answer contract** (ρ-gate + abstain) co-designed with a dynamic CTI graph—not “GraphRAG plus modules.”

---

## 6. Conclusions and Future Work

We presented **EDGR**, consolidating four pillars—Dynamic CTI KG, six-stage evidence-driven graph retrieval, four-factor hallucination risk scoring with ρ-gate abstain, and a comprehensive evaluation protocol—into one scientific system for IDS/CTI question answering. Empirically, on a reproducible live seed suite (\(N=54\), \(|D|=40\), \(V=40\), \(E=41\)), EDGR achieves mean faithfulness **0.702** and hallucination rate **0.298**, with R@k **0.852** and MRR **0.803**. Versus flat RAG, the faithfulness margin is positive with bootstrap CI excluding zero (Δ≈+0.15); graph ablation confirms a **−0.104** contribution. Graph-path stubs may still win on automatic faithfulness when gold overlap is dense; EDGR’s primary scientific contribution is the **end-to-end risk-controlled retrieval contract** for high-stakes CTI assistance.

**Future work.** Learned \(\theta\) and factor weights; TAXII/feed adapters at scale; field SOC faithfulness labels replacing the seed panel; ANN indexes for production latency; joint evaluation with live Suricata-style alert→query traces; larger public CTI QA benchmarks.

---

## Author Contributions

Conceptualization, N.V.P.; methodology, N.V.P.; software, N.V.P.; validation, N.V.P.; formal analysis, N.V.P.; investigation, N.V.P.; data curation, N.V.P.; writing—original draft, N.V.P.; writing—review and editing, N.V.P.; supervision, *(advisor to be named)*; project administration, N.V.P. The author has read and agreed to the published version of the manuscript.

## Funding

This research received no external funding *(update if applicable)*.

## Data Availability Statement

The reproducible prototype, seed QA/evidence/KG, and evaluation scripts are available in the accompanying project repository. Core modules: EDGR algorithm, hallucination scoring, knowledge graph, metrics, scientific-rigor statistics, and human-evaluation protocol.

## Acknowledgments

The author thanks the open research community for RAG, GraphRAG, and hallucination literature that framed this work, and MITRE ATT&CK / public CVE descriptions used in the seed corpus.

## Conflicts of Interest

The author declares no conflicts of interest.

---

## References

1. Lewis, P.; Perez, E.; Piktus, A.; Petroni, F.; Karpukhin, V.; Goyal, N.; Küttler, H.; Lewis, M.; Yih, W.; Rocktäschel, T.; Riedel, S.; Kiela, D. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *Adv. Neural Inf. Process. Syst.* **2020**, *33*, 9459–9474.  
2. Ji, Z.; Lee, N.; Frieske, R.; Yu, T.; Su, D.; Xu, Y.; Ishii, E.; Bang, Y.J.; Madotto, A.; Fung, P. Survey of Hallucination in Natural Language Generation. *ACM Comput. Surv.* **2023**, *55*, 248. https://doi.org/10.1145/3571730  
3. Gao, Y.; Xiong, Y.; Gao, X.; Jia, K.; Pan, J.; Bi, Y.; Dai, Y.; Sun, J.; Wang, M.; Wang, H. Retrieval-Augmented Generation for Large Language Models: A Survey. *arXiv* **2023**, arXiv:2312.10997.  
4. Edge, D.; Trinh, H.; Cheng, N.; Bradley, J.; Chao, A.; Mody, A.; Truitt, S.; Larson, J. From Local to Global: A Graph RAG Approach to Query-Focused Summarization. *arXiv* **2024**, arXiv:2404.16130.  
5. Guo, Z.; Xia, L.; Yu, Y.; Ao, X.; Huang, C. LightRAG: Simple and Fast Retrieval-Augmented Generation. *arXiv* **2024**, arXiv:2410.05779.  
6. Gutiérrez, B.J.; Shu, Y.; Gu, Y.; Yasunaga, M.; Su, Y. HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models. *Adv. Neural Inf. Process. Syst.* **2024**.  
7. Asai, A.; Wu, Z.; Wang, Y.; Sil, A.; Hajishirzi, H. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. In *Proceedings of the International Conference on Learning Representations (ICLR)*, 2024.  
8. Yan, S.-Q.; Gu, J.-C.; Zhu, Y.; Ling, Z.-H. Corrective Retrieval Augmented Generation. *arXiv* **2024**, arXiv:2401.15884.  
9. Strom, B.E.; Applebaum, A.; Miller, D.P.; Nickels, K.C.; Pennington, A.G.; Thomas, C.B. *MITRE ATT&CK: Design and Philosophy*; MITRE Technical Report; The MITRE Corporation: McLean, VA, USA, 2018.  
10. Wagner, T.D.; Mahbub, K.; Palomar, E.; Abdallah, A.E. Cyber Threat Intelligence Sharing: Survey and Research Directions. *Comput. Secur.* **2019**, *87*, 101589.  
11. Khraisat, A.; Gondal, I.; Vamplew, P.; Kamruzzaman, J. Survey of Intrusion Detection Systems: Techniques, Datasets and Challenges. *Cybersecurity* **2019**, *2*, 20. https://doi.org/10.1186/s42400-019-0038-7  
12. Pan, S.; Luo, L.; Wang, Y.; Chen, C.; Wang, J.; Wu, X. Unifying Large Language Models and Knowledge Graphs: A Roadmap. *IEEE Trans. Knowl. Data Eng.* **2024**, *36*, 3580–3599.  

---

## Appendix A. Reproducibility Checklist

| Item | Default / note |
|------|----------------|
| Seed QA / evidence / KG | Accompanying repository data modules |
| Algorithm / scoring / graph | Core EDGR, hallucination, KG modules |
| Metrics / compare / ablation | Evaluation + scientific-rigor modules |
| Human eval / κ | Dual-annotator SOC protocol |
| Defaults | \(k=5\), \(\theta=0.55\), window \(=730\) days |
| Figures | `docs/papers/figures/fig1_edgr_pipeline.svg`, `fig2_mean_faithfulness.svg`, `fig3_ablation.svg` |

## Appendix B. Ethics and Dual-Use

CTI assistance can be misused for offense. This work targets defensive SOC workflows, refuses unsupported identifier claims via abstain, and uses only publicly described techniques/CVEs in the seed corpus.
