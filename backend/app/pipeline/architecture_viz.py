"""System architecture diagram payload for Step 8 (and runtime architecture tab)."""

from __future__ import annotations

from typing import Any


def system_architecture_viz() -> dict[str, Any]:
    """Frontend-ready architecture figure: Query → API → EDGR ↔ services → Answer."""
    return {
        "kind": "architecture",
        "title_vi": "Sơ đồ kiến trúc hệ thống EDGR",
        "title_en": "EDGR system architecture diagram",
        "caption_vi": (
            "Luồng serving: User Query → FastAPI → EDGR Engine "
            "(mở rộng KG · vector · chấm risk) → Grounded Generator → Trusted Answer."
        ),
        "caption_en": (
            "Serving flow: User Query → FastAPI → EDGR Engine "
            "(KG expand · vector · risk score) → Grounded Generator → Trusted Answer."
        ),
        "nodes": [
            {"id": "query", "label_vi": "User Query", "label_en": "User Query", "role": "input"},
            {"id": "api", "label_vi": "FastAPI\n/api/query", "label_en": "FastAPI\n/api/query", "role": "gateway"},
            {
                "id": "edgr",
                "label_vi": "EDGR Engine\nExpand · Temporal · Rank · ρ-gate",
                "label_en": "EDGR Engine\nExpand · Temporal · Rank · ρ-gate",
                "role": "core",
            },
            {"id": "kg", "label_vi": "Dynamic KG", "label_en": "Dynamic KG", "role": "service"},
            {"id": "vec", "label_vi": "Vector Store\n(TF-IDF)", "label_en": "Vector Store\n(TF-IDF)", "role": "service"},
            {
                "id": "scorer",
                "label_vi": "Hallucination\nScorer",
                "label_en": "Hallucination\nScorer",
                "role": "service",
            },
            {
                "id": "gen",
                "label_vi": "Grounded\nGenerator",
                "label_en": "Grounded\nGenerator",
                "role": "generator",
            },
            {
                "id": "answer",
                "label_vi": "Trusted Answer\n+ Faith / Hall",
                "label_en": "Trusted Answer\n+ Faith / Hall",
                "role": "output",
            },
        ],
        "edges": [
            {"from": "query", "to": "api", "label": ""},
            {"from": "api", "to": "edgr", "label": "q"},
            {"from": "edgr", "to": "kg", "label": "expand", "bidirectional": True},
            {"from": "edgr", "to": "vec", "label": "sim", "bidirectional": True},
            {"from": "edgr", "to": "scorer", "label": "ρ", "bidirectional": True},
            {"from": "edgr", "to": "gen", "label": "E*"},
            {"from": "gen", "to": "answer", "label": "a"},
        ],
        "modules": {
            "api": "FastAPI /api/query /api/pipeline/*",
            "edgr": "app.core.edgr.EDGREngine",
            "kg": "app.core.knowledge_graph.DynamicKnowledgeGraph",
            "vector": "app.core.vector_store.VectorStore",
            "scorer": "app.core.hallucination.HallucinationScorer",
            "generator": "app.core.llm (evidence-constrained)",
        },
        "flow": [
            "User Query",
            "FastAPI",
            "EDGR Engine",
            "Dynamic KG",
            "Vector Store",
            "Hallucination Scorer",
            "Grounded Generator",
            "Trusted Answer",
        ],
    }
