"""Grounded answer generator (template LLM) for offline demo."""

from __future__ import annotations

from typing import Any

from app.models.schemas import EvidenceItem


def generate_trusted_answer(
    query: str,
    evidence: list[EvidenceItem],
    relations: list[str],
    method: str = "EDGR",
) -> str:
    if not evidence:
        return (
            "Insufficient trusted evidence was retrieved to answer this CTI/IDS question "
            "without risking hallucination. Please refine the query or expand the knowledge graph."
        )

    synthesis = _synthesize(query, evidence)

    if method == "EDGR":
        return synthesis

    # Method-specific grounded prefixes (still extractive; no free invention)
    if method == "GraphRAG" and relations:
        cue = relations[0] if relations else ""
        return f"{synthesis} Graph context: {cue}." if cue else synthesis
    if method == "HippoRAG" and relations:
        cue = "; ".join(relations[:2])
        return f"{synthesis} Path memory: {cue}." if cue else synthesis
    if method == "Self-RAG":
        return f"{synthesis} [self-critique: retained top semantic evidence only]"
    if method == "Corrective-RAG":
        return f"{synthesis} [corrective: reliability-reranked evidence]"
    if method == "LightRAG":
        return synthesis

    return synthesis


def _synthesize(query: str, evidence: list[EvidenceItem]) -> str:
    """Extractive synthesis preferring entity-aligned evidence."""
    q_l = query.lower()
    ranked = sorted(
        evidence,
        key=lambda e: (
            sum(1 for ent in e.entities if ent.lower() in q_l),
            e.score,
        ),
        reverse=True,
    )
    if not ranked:
        return "No grounded statement available."

    primary = ranked[0].content.strip()
    parts = [primary]

    for ev in ranked[1:3]:
        if not any(ent.lower() in q_l for ent in ev.entities):
            continue
        # add one short supporting clause from another matching source
        first = ev.content.split(". ")
        if not first:
            continue
        s = first[0].strip()
        if not s.endswith("."):
            s += "."
        if s.lower() not in primary.lower():
            parts.append(s)
            break

    return " ".join(parts)


def generate_baseline_answer(
    query: str,
    passages: list[dict[str, Any]],
    method: str,
) -> str:
    evidence = [
        EvidenceItem(
            id=p.get("id", f"p{i}"),
            content=p.get("content", ""),
            source=p.get("source", "retrieval"),
            entities=p.get("entities", []),
            score=float(p.get("score", 0.5)),
            reliability=float(p.get("reliability", 0.7)),
            freshness=0.6,
            graph_consistency=0.5,
            semantic_relevance=float(p.get("semantic_score", p.get("score", 0.5))),
            hallucination_risk=0.4,
            timestamp=p.get("timestamp"),
        )
        for i, p in enumerate(passages)
    ]
    return generate_trusted_answer(query, evidence, relations=[], method=method)
