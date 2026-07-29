"""Hallucination scoring model (0–1 risk / trust)."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from app.core.knowledge_graph import DynamicKnowledgeGraph
from app.models.schemas import EvidenceItem


CVE_RE = re.compile(r"CVE-\d{4}-\d{4,}", re.I)
TECH_RE = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")


class HallucinationScorer:
    """
    Composite score from:
    - source reliability
    - freshness
    - graph consistency
    - semantic relevance
    """

    WEIGHTS = {
        "reliability": 0.30,
        "freshness": 0.20,
        "graph_consistency": 0.25,
        "semantic_relevance": 0.25,
    }

    def __init__(self, kg: DynamicKnowledgeGraph) -> None:
        self.kg = kg

    def freshness_score(self, timestamp: str | None, window_days: int = 730) -> float:
        """Freshness prior — historical CVEs stay usable, not discarded."""
        if not timestamp:
            return 0.55
        try:
            dt = datetime.fromisoformat(timestamp).replace(tzinfo=timezone.utc)
            age = (datetime.now(timezone.utc) - dt).days
            if age <= 90:
                return 1.0
            if age <= 365:
                return 0.9
            if age <= window_days:
                return 0.78
            if age <= 365 * 5:
                return 0.62  # still valid CTI (e.g. Log4Shell)
            return 0.45
        except ValueError:
            return 0.5

    def score_evidence(
        self,
        chunk: dict[str, Any],
        query_entities: list[str],
        semantic_score: float,
        window_days: int = 730,
        enable_graph: bool = True,
        enable_temporal: bool = True,
    ) -> EvidenceItem:
        reliability = float(chunk.get("reliability", 0.7))
        freshness = (
            self.freshness_score(chunk.get("timestamp"), window_days)
            if enable_temporal
            else 0.75
        )
        ents = list(chunk.get("entities", []))
        all_ents = list(dict.fromkeys(query_entities + ents))
        graph_consistency = (
            self.kg.path_consistency(all_ents) if enable_graph else 0.7
        )
        semantic = float(max(0.0, min(1.0, semantic_score)))

        trust = (
            self.WEIGHTS["reliability"] * reliability
            + self.WEIGHTS["freshness"] * freshness
            + self.WEIGHTS["graph_consistency"] * graph_consistency
            + self.WEIGHTS["semantic_relevance"] * semantic
        )
        hallucination_risk = round(1.0 - trust, 4)

        return EvidenceItem(
            id=chunk["id"],
            content=chunk["content"],
            source=chunk.get("source", "unknown"),
            entities=ents,
            score=round(trust, 4),
            reliability=round(reliability, 4),
            freshness=round(freshness, 4),
            graph_consistency=round(graph_consistency, 4),
            semantic_relevance=round(semantic, 4),
            hallucination_risk=hallucination_risk,
            timestamp=chunk.get("timestamp"),
            metadata={"type": chunk.get("type")},
        )

    def answer_faithfulness(
        self, answer: str, evidence: list[EvidenceItem]
    ) -> tuple[float, float]:
        """Estimate faithfulness and hallucination rate of generated answer."""
        if not evidence:
            return 0.2, 0.8

        evidence_text = " ".join(e.content for e in evidence).lower()
        answer_tokens = [t for t in re.findall(r"[a-zA-Z0-9.\-]{3,}", answer.lower())]
        if not answer_tokens:
            return 0.3, 0.7

        supported = sum(1 for t in answer_tokens if t in evidence_text)
        coverage = supported / len(answer_tokens)

        # Penalize invented CVE / technique IDs not in evidence
        claimed_cves = set(CVE_RE.findall(answer))
        claimed_techs = set(TECH_RE.findall(answer))
        evidence_ids = set(CVE_RE.findall(evidence_text)) | set(
            TECH_RE.findall(evidence_text)
        )
        invented = (claimed_cves | claimed_techs) - evidence_ids
        invent_penalty = min(0.5, 0.15 * len(invented))

        avg_trust = sum(e.score for e in evidence) / len(evidence)
        # Identifier precision bonus when claimed CTI IDs are supported
        id_precision = 1.0
        if claimed_cves | claimed_techs:
            supported_ids = (claimed_cves | claimed_techs) & evidence_ids
            id_precision = len(supported_ids) / max(1, len(claimed_cves | claimed_techs))
        faithfulness = max(
            0.0,
            min(
                1.0,
                0.50 * coverage
                + 0.35 * avg_trust
                + 0.15 * id_precision
                - invent_penalty,
            ),
        )
        hallucination_rate = round(1.0 - faithfulness, 4)
        return round(faithfulness, 4), hallucination_rate
