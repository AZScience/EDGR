"""
EDGR — Evidence-Driven Dynamic Graph Retrieval Algorithm

Stages:
1. Query understanding & entity extraction
2. Adaptive multi-step expansion
3. Temporal filtering
4. Evidence Ranking
5. Hallucination Scoring
6. Trusted evidence selection
"""

from __future__ import annotations

import re
import time
from typing import Any, Optional

from app.core.hallucination import HallucinationScorer
from app.core.knowledge_graph import DynamicKnowledgeGraph, kg
from app.core.llm import generate_trusted_answer
from app.core.vector_store import VectorStore, vector_store
from app.models.schemas import EDGRStageResult, EvidenceItem, QueryRequest, TrustedAnswer

_CVE_RE = re.compile(r"CVE-\d{4}-\d{4,}", re.I)


class EDGREngine:
    def __init__(
        self,
        knowledge_graph: Optional[DynamicKnowledgeGraph] = None,
        store: Optional[VectorStore] = None,
    ) -> None:
        self.kg = knowledge_graph or kg
        self.store = store or vector_store
        self.scorer = HallucinationScorer(self.kg)

    def run(self, req: QueryRequest) -> TrustedAnswer:
        t0 = time.perf_counter()
        stages: list[EDGRStageResult] = []

        enable_temporal = req.enable_temporal
        enable_graph = req.enable_graph
        enable_trust = req.enable_trust_score
        # Ranking ablation: keep graph/temporal/trust, but order Stage-4 by semantic only.
        semantic_only_rank = False
        # Scoring ablation: keep trust composite scores, but skip ρ-gate / abstain.
        skip_hallucination_scoring = False

        if req.ablation_mode == "w/o Temporal":
            enable_temporal = False
        elif req.ablation_mode == "w/o Graph":
            enable_graph = False
        elif req.ablation_mode == "w/o Trust Score":
            enable_trust = False
        elif req.ablation_mode == "w/o Evidence Ranking":
            semantic_only_rank = True
        elif req.ablation_mode == "w/o Hallucination Scoring":
            # Distinct from w/o Trust: still score with composite trust, but do not gate/abstain.
            skip_hallucination_scoring = True

        # Stage 1 — Query understanding & entity extraction
        s1 = time.perf_counter()
        entities = self.kg.extract_entities(req.query)
        # also pull tokens that look like CTI IDs from query even if not in KG yet
        stages.append(
            EDGRStageResult(
                stage=1,
                name="Query Understanding & Entity Extraction",
                name_vi="Hiểu truy vấn & trích xuất thực thể",
                description="Parse query intent and extract CTI entities (CVE, ATT&CK, actors).",
                output={"entities": entities, "query": req.query},
                duration_ms=(time.perf_counter() - s1) * 1000,
            )
        )

        # Stage 2 — Adaptive multi-step expansion
        s2 = time.perf_counter()
        expanded_nodes: list[dict[str, Any]] = []
        expanded_ids: list[str] = list(entities)
        if enable_graph and entities:
            hops = 2 if len(entities) <= 2 else 1
            expanded_nodes = self.kg.expand(entities, max_hops=hops, max_nodes=20)
            expanded_ids = list(dict.fromkeys([n["id"] for n in expanded_nodes] + entities))
        relations = self.kg.relation_summary(expanded_ids[:8]) if enable_graph else []
        stages.append(
            EDGRStageResult(
                stage=2,
                name="Adaptive Multi-step Expansion",
                name_vi="Mở rộng đa bước thích ứng",
                description="Expand entity neighborhood on the dynamic knowledge graph.",
                output={
                    "expanded_entities": expanded_ids,
                    "nodes": len(expanded_nodes),
                    "relations": relations[:8],
                },
                duration_ms=(time.perf_counter() - s2) * 1000,
            )
        )

        # Stage 3 — Temporal filtering
        # Keep query seed entities always (historical CVEs remain relevant);
        # only filter expanded neighbors for freshness.
        s3 = time.perf_counter()
        seed_set = set(entities)
        temporal_ids = expanded_ids
        if enable_temporal:
            neighbors = [e for e in expanded_ids if e not in seed_set]
            kept_neighbors = self.kg.temporal_filter(
                neighbors, window_days=req.time_window_days
            )
            temporal_ids = list(dict.fromkeys(list(entities) + kept_neighbors))
        stages.append(
            EDGRStageResult(
                stage=3,
                name="Temporal Filtering",
                name_vi="Lọc thời gian",
                description="Drop stale expanded neighbors; always keep query seed entities.",
                output={
                    "kept": temporal_ids,
                    "seeds_preserved": entities,
                    "window_days": req.time_window_days,
                    "enabled": enable_temporal,
                },
                duration_ms=(time.perf_counter() - s3) * 1000,
            )
        )

        # Stage 4 — Evidence Ranking
        s4 = time.perf_counter()
        vector_hits = self.store.search(
            req.query, top_k=max(req.top_k * 3, 10), entity_boost=temporal_ids
        )
        graph_hits = (
            self.store.by_entities(temporal_ids, top_k=req.top_k * 2)
            if enable_graph
            else []
        )
        merged: dict[str, dict[str, Any]] = {}
        for h in vector_hits + graph_hits:
            cid = h["id"]
            if cid not in merged or h.get("score", 0) > merged[cid].get("score", 0):
                merged[cid] = h

        # Hard prefer chunks whose entities intersect the query/temporal set
        focus = {e.upper() for e in temporal_ids + entities}
        q_lower = req.query.lower()

        def rank_key(item: dict[str, Any]) -> tuple[float, float, float]:
            ents = {e.upper() for e in item.get("entities", [])}
            overlap = len(ents & focus)
            exact = sum(1 for e in item.get("entities", []) if e.lower() in q_lower)
            if semantic_only_rank:
                # Ablation: drop entity/graph fusion — semantic retrieval score only.
                return (float(item.get("score", 0)), 0.0, 0.0)
            return (
                float(exact),
                float(overlap),
                float(item.get("score", 0)),
            )

        ranked = sorted(merged.values(), key=rank_key, reverse=True)[
            : max(req.top_k * 2, 8)
        ]
        stages.append(
            EDGRStageResult(
                stage=4,
                name="Evidence Ranking",
                name_vi="Xếp hạng bằng chứng",
                description=(
                    "Semantic-only ranking (ablation)."
                    if semantic_only_rank
                    else "Fuse vector similarity and graph-linked evidence."
                ),
                output={
                    "candidates": [
                        {"id": r["id"], "score": round(float(r.get("score", 0)), 4)}
                        for r in ranked
                    ],
                    "semantic_only": semantic_only_rank,
                },
                duration_ms=(time.perf_counter() - s4) * 1000,
            )
        )

        # Stage 5 — Hallucination Scoring
        s5 = time.perf_counter()
        scored: list[EvidenceItem] = []
        for chunk in ranked:
            item = self.scorer.score_evidence(
                chunk,
                query_entities=temporal_ids,
                semantic_score=float(
                    chunk.get("semantic_score", chunk.get("score", 0.5))
                ),
                window_days=req.time_window_days,
                enable_graph=enable_graph,
                enable_temporal=enable_temporal,
            )
            if not enable_trust:
                # degrade to semantic-only ranking signal
                item.score = item.semantic_relevance
                item.hallucination_risk = round(1.0 - item.semantic_relevance, 4)
            scored.append(item)
        scored.sort(key=lambda e: e.score, reverse=True)
        stages.append(
            EDGRStageResult(
                stage=5,
                name="Hallucination Scoring",
                name_vi="Chấm điểm ảo giác",
                description="Score reliability, freshness, graph consistency, semantic relevance.",
                output={
                    "scores": [
                        {
                            "id": e.id,
                            "trust": e.score,
                            "risk": e.hallucination_risk,
                            "reliability": e.reliability,
                            "freshness": e.freshness,
                            "graph_consistency": e.graph_consistency,
                            "semantic_relevance": e.semantic_relevance,
                        }
                        for e in scored
                    ],
                    "enabled": enable_trust,
                },
                duration_ms=(time.perf_counter() - s5) * 1000,
            )
        )

        # Stage 6 — Trusted evidence selection + ρ-gate / abstain
        s6 = time.perf_counter()
        risk_threshold = 0.55 if enable_trust else 0.95
        # Full EDGR applies the gate. Ablations may disable it.
        apply_gate = bool(enable_trust and not skip_hallucination_scoring)

        seed_u = {e.upper() for e in entities}

        def trust_key(e: EvidenceItem) -> tuple[int, float, float]:
            overlap = len({x.upper() for x in e.entities} & seed_u)
            return (overlap, e.score, -e.hallucination_risk)

        if apply_gate:
            candidates = [e for e in scored if e.hallucination_risk <= risk_threshold]
        else:
            candidates = list(scored)

        trusted = sorted(candidates, key=trust_key, reverse=True)[: req.top_k]

        query_cves = {m.upper() for m in _CVE_RE.findall(req.query)}
        kg_ids = {str(n).upper() for n in self.kg.graph.nodes}
        scored_blob = " ".join(e.content for e in scored).upper()
        unknown_cves = sorted(
            c for c in query_cves if c not in kg_ids and c not in scored_blob
        )

        abstained = False
        abstain_reason_vi = ""
        abstain_reason_en = ""
        apply_flag = 1

        if apply_gate and unknown_cves:
            abstained = True
            apply_flag = 0
            abstain_reason_en = (
                "Unknown CVE identifier(s) not present in the knowledge base or "
                f"retrieved evidence: {', '.join(unknown_cves)}. "
                "EDGR abstains instead of guessing."
            )
            abstain_reason_vi = (
                "CVE không có trong kho tri thức / bằng chứng đã truy hồi: "
                f"{', '.join(unknown_cves)}. EDGR từ chối trả lời thay vì suy đoán."
            )
            trusted = []
        elif apply_gate and not trusted:
            abstained = True
            apply_flag = 0
            abstain_reason_en = (
                f"No evidence passed the risk gate (ρ ≤ {risk_threshold}). "
                "EDGR abstains to avoid ungrounded CTI claims."
            )
            abstain_reason_vi = (
                f"Không có bằng chứng vượt cổng rủi ro (ρ ≤ {risk_threshold}). "
                "EDGR từ chối trả lời để tránh claim CTI không được neo."
            )
        elif apply_gate and trusted and query_cves:
            trusted_blob = " ".join(e.content for e in trusted).upper()
            if not any(c in trusted_blob for c in query_cves):
                abstained = True
                apply_flag = 0
                abstain_reason_en = (
                    "Retrieved evidence does not mention the CVE(s) in the query; "
                    "EDGR abstains rather than answering from unrelated passages."
                )
                abstain_reason_vi = (
                    "Bằng chứng truy hồi không đề cập CVE trong câu hỏi; "
                    "EDGR từ chối trả lời thay vì dùng đoạn không liên quan."
                )
                trusted = []

        stages.append(
            EDGRStageResult(
                stage=6,
                name="Trusted Evidence Selection",
                name_vi="Chọn bằng chứng tin cậy",
                description=(
                    "Keep low-risk evidence for grounded generation; abstain when gate fails."
                ),
                output={
                    "selected": [e.id for e in trusted],
                    "threshold": risk_threshold,
                    "apply_gate": apply_gate,
                    "apply": apply_flag,
                    "abstained": abstained,
                    "unknown_cves": unknown_cves,
                    "abstain_reason_vi": abstain_reason_vi,
                    "abstain_reason_en": abstain_reason_en,
                },
                duration_ms=(time.perf_counter() - s6) * 1000,
            )
        )

        if abstained:
            answer = (
                f"[ABSTAIN / TỪ CHỐI TRẢ LỜI] {abstain_reason_en} {abstain_reason_vi}"
            )
            # No unsupported claim emitted → treat as faithful abstain.
            faithfulness, hall_rate = 1.0, 0.0
            confidence = 0.0
        else:
            answer = generate_trusted_answer(
                req.query, trusted, relations=relations, method="EDGR"
            )
            faithfulness, hall_rate = self.scorer.answer_faithfulness(answer, trusted)
            confidence = round(
                (sum(e.score for e in trusted) / len(trusted)) if trusted else 0.0,
                4,
            )

        return TrustedAnswer(
            answer=answer,
            confidence=confidence,
            hallucination_rate=hall_rate,
            faithfulness=faithfulness,
            evidence=trusted,
            entities=temporal_ids,
            stages=stages,
            method="EDGR",
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
            metadata={
                "ablation_mode": req.ablation_mode,
                "enable_temporal": enable_temporal,
                "enable_graph": enable_graph,
                "enable_trust_score": enable_trust,
                "semantic_only_rank": semantic_only_rank,
                "skip_hallucination_scoring": skip_hallucination_scoring,
                "apply_gate": apply_gate,
                "apply": apply_flag,
                "abstained": abstained,
                "abstain_reason_vi": abstain_reason_vi,
                "abstain_reason_en": abstain_reason_en,
                "risk_threshold": risk_threshold,
            },
        )

    def run_baseline(self, query: str, method: str, top_k: int = 5) -> TrustedAnswer:
        """
        Research-faithful retrieval stubs for family baselines.
        Same scorer/KG/vector store — no artificial score degradation.
        Not drop-in copies of the original published systems.
        Each method uses a distinct named retrieval policy (see policy_steps).
        """
        t0 = time.perf_counter()
        hits = self.store.search(query, top_k=max(top_k * 3, 8))
        ents = self.kg.extract_entities(query)
        relations: list[str] = []
        policy_steps: list[str] = []

        if method == "RAG":
            # Dense-only, no graph, no gate — classic retrieve-then-generate.
            selected = hits[:top_k]
            policy_steps = [
                "Dense retrieve (TF-IDF)",
                f"Take top-{top_k} (no graph expand)",
                "Generate without trust gate",
            ]
        elif method == "GraphRAG":
            expanded = self.kg.expand(ents, max_hops=2, max_nodes=18)
            ids = [n["id"] for n in expanded] or ents
            graph_hits = self.store.by_entities(ids, top_k=top_k * 2)
            merged = {h["id"]: h for h in graph_hits + hits}
            # Community-aware boost: prefer chunks covering denser expanded neighborhood
            focus = {i.upper() for i in ids}
            selected = sorted(
                merged.values(),
                key=lambda h: (
                    len({e.upper() for e in h.get("entities", [])} & focus),
                    float(h.get("score", 0)),
                ),
                reverse=True,
            )[:top_k]
            relations = self.kg.relation_summary(ids[:12])
            # Lightweight "community" cue: top connected seeds in expansion
            try:
                import networkx as nx

                sub = self.kg.graph.subgraph(ids).to_undirected()
                if sub.number_of_nodes() >= 3:
                    deg = sorted(sub.degree, key=lambda x: x[1], reverse=True)
                    hub = ", ".join(f"{n}(deg={d})" for n, d in deg[:3])
                    relations = [f"community_hubs: {hub}"] + list(relations)
            except Exception:
                pass
            policy_steps = [
                f"Extract entities ({len(ents)})",
                f"Expand 2-hop → {len(ids)} nodes",
                "Entity-linked retrieve + dense merge",
                "Community-hub cue + relation summary into generator",
            ]
        elif method == "LightRAG":
            # Dual-level: half slots entity-linked, half dense-only.
            half = max(1, (top_k + 1) // 2)
            ent_hits = self.store.by_entities(ents, top_k=half) if ents else []
            dense_fill = [h for h in hits if h["id"] not in {x["id"] for x in ent_hits}]
            selected = (ent_hits + dense_fill)[:top_k]
            policy_steps = [
                f"Entity-linked slots ⌈k/2⌉={half}",
                f"Dense fill ⌊k/2⌋ → {len(selected)} total",
                "Dual-level mix; no trust gate / no abstain",
            ]
        elif method == "HippoRAG":
            # Path-centric memory: rank entities by inverse shortest-path to seeds, then retrieve.
            expanded = self.kg.expand(ents, max_hops=2, max_nodes=16)
            ids = [n["id"] for n in expanded] or ents
            seed_set = set(ents)
            path_rank: list[tuple[float, str]] = []
            try:
                und = self.kg.graph.to_undirected()
                for nid in ids:
                    best = 99
                    for s in seed_set:
                        if s not in und or nid not in und:
                            continue
                        try:
                            import networkx as nx

                            best = min(best, nx.shortest_path_length(und, s, nid))
                        except Exception:
                            continue
                    path_rank.append((1.0 / (1 + best), nid))
                path_rank.sort(reverse=True)
                ids = [nid for _, nid in path_rank] or ids
            except Exception:
                pass
            selected = self.store.by_entities(ids[:12], top_k=top_k) or hits[:top_k]
            relations = self.kg.relation_summary(ids[:8])
            policy_steps = [
                f"Seed entities ({len(ents)})",
                "Path-distance memory ranking (1/(1+d))",
                "Retrieve by path-prioritized entities",
                "Path relations into generator",
            ]
        elif method == "Self-RAG":
            pool = hits[: max(top_k + 3, 5)]
            ranked = sorted(pool, key=lambda x: x.get("score", 0), reverse=True)
            keep_n = max(1, int(len(ranked) * 0.75))
            selected = ranked[: min(top_k, keep_n)]
            # Critique loop: if coverage of query tokens is weak, retrieve once more
            q_toks = {t for t in query.lower().split() if len(t) > 3}
            blob = " ".join(h.get("content", "") for h in selected).lower()
            cov = sum(1 for t in q_toks if t in blob) / max(1, len(q_toks))
            if cov < 0.35:
                extra = [h for h in hits if h["id"] not in {x["id"] for x in selected}]
                selected = (selected + extra)[:top_k]
                policy_steps = [
                    f"Retrieve pool of {len(pool)}",
                    "Critique: drop bottom quartile",
                    f"Low coverage ({cov:.2f}) → retrieve-again fill",
                    f"Keep {len(selected)}; no trust gate",
                ]
            else:
                policy_steps = [
                    f"Retrieve pool of {len(pool)}",
                    "Critique: drop bottom quartile by sim",
                    f"Coverage OK ({cov:.2f}); keep {len(selected)}",
                    "No graph / no trust gate",
                ]
        elif method == "Corrective-RAG":
            pool = hits[: top_k + 3]
            mean_rel = (
                sum(float(h.get("reliability", 0.5)) for h in pool) / len(pool)
                if pool
                else 0.5
            )
            if mean_rel < 0.55:
                pool = hits[: top_k + 6]
                policy_steps = [
                    f"Initial retrieve (mean reliability={mean_rel:.2f} < 0.55)",
                    "Corrective: expand pool +2/+3",
                    "Drop low-reliability tail; re-rank",
                    f"Cut top-{top_k}",
                ]
            else:
                policy_steps = [
                    f"Initial retrieve (mean reliability={mean_rel:.2f})",
                    "Corrective re-rank by reliability",
                    f"Cut top-{top_k}",
                ]
            # Explicit corrective filter: drop bottom reliability before cut
            pool = sorted(pool, key=lambda x: x.get("reliability", 0.5), reverse=True)
            if len(pool) > top_k:
                pool = pool[:-1]
            selected = pool[:top_k]
        else:
            return self.run(QueryRequest(query=query, top_k=top_k))

        use_graph = method in {"GraphRAG", "HippoRAG"}
        evidence = [
            self.scorer.score_evidence(
                h,
                query_entities=ents,
                semantic_score=float(h.get("semantic_score", h.get("score", 0.5))),
                enable_graph=use_graph,
                enable_temporal=False,
            )
            for h in selected
        ]
        # Non-EDGR methods do not apply EDGR trust gating — distinct score mix.
        if method in {"RAG"}:
            for e, h in zip(evidence, selected):
                e.score = round(float(h.get("score", e.semantic_relevance)), 4)
                e.hallucination_risk = round(max(0.0, 1.0 - e.score), 4)
        elif method == "LightRAG":
            for e, h in zip(evidence, selected):
                # Slight entity bonus already implicit in slot mix; score = dense sim.
                e.score = round(float(h.get("score", e.semantic_relevance)), 4)
                e.hallucination_risk = round(max(0.0, 1.0 - e.score), 4)
        elif method in {"Self-RAG", "Corrective-RAG"}:
            for e in evidence:
                e.score = round(0.7 * e.semantic_relevance + 0.3 * e.reliability, 4)
                e.hallucination_risk = round(1.0 - e.score, 4)
        elif method in {"GraphRAG", "HippoRAG"}:
            for e in evidence:
                e.score = round(
                    0.55 * e.semantic_relevance
                    + 0.25 * e.graph_consistency
                    + 0.2 * e.reliability,
                    4,
                )
                e.hallucination_risk = round(max(0.0, 1.0 - e.score), 4)

        answer = generate_trusted_answer(
            query, evidence, relations=relations, method=method
        )
        faithfulness, hall_rate = self.scorer.answer_faithfulness(answer, evidence)

        return TrustedAnswer(
            answer=answer,
            confidence=round(
                sum(e.score for e in evidence) / len(evidence) if evidence else 0, 4
            ),
            hallucination_rate=hall_rate,
            faithfulness=faithfulness,
            evidence=evidence,
            entities=ents,
            stages=[],
            method=method,
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
            metadata={
                "baseline": True,
                "family_stub": True,
                "reference_family_reimplementation": True,
                "policy_steps": policy_steps,
                "policy_name": method,
            },
        )


edgr_engine = EDGREngine()
