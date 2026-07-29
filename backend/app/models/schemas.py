from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.defaults import DEFAULT_TOP_K


class EntityType(str, Enum):
    TECHNIQUE = "technique"
    TACTIC = "tactic"
    CVE = "cve"
    MALWARE = "malware"
    ACTOR = "actor"
    SOFTWARE = "software"
    DATASET = "dataset"
    ALERT = "alert"
    CONCEPT = "concept"


class GraphNode(BaseModel):
    id: str
    label: str
    type: EntityType
    properties: dict[str, Any] = Field(default_factory=dict)
    timestamp: Optional[str] = None
    reliability: float = 0.8


class GraphEdge(BaseModel):
    source: str
    target: str
    relation: str
    weight: float = 1.0
    timestamp: Optional[str] = None


class EvidenceItem(BaseModel):
    id: str
    content: str
    source: str
    entities: list[str] = Field(default_factory=list)
    score: float = 0.0
    reliability: float = 0.0
    freshness: float = 0.0
    graph_consistency: float = 0.0
    semantic_relevance: float = 0.0
    hallucination_risk: float = 0.0
    timestamp: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EDGRStageResult(BaseModel):
    stage: int
    name: str
    name_vi: str
    description: str
    output: dict[str, Any] = Field(default_factory=dict)
    duration_ms: float = 0.0


class QueryRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "query": "What is CVE-2021-44228 and how is it exploited?",
                    "top_k": 5,
                    "enable_temporal": True,
                    "enable_graph": True,
                    "enable_trust_score": True,
                }
            ]
        }
    )

    query: str = Field(
        default="What is CVE-2021-44228 and how is it exploited?",
        description="Câu hỏi CTI/IDS mẫu — có thể sửa hoặc giữ nguyên.",
    )
    top_k: int = DEFAULT_TOP_K
    enable_temporal: bool = True
    enable_graph: bool = True
    enable_trust_score: bool = True
    time_window_days: int = 730
    ablation_mode: Optional[str] = None


class TrustedAnswer(BaseModel):
    answer: str
    confidence: float
    hallucination_rate: float
    faithfulness: float
    evidence: list[EvidenceItem]
    entities: list[str]
    stages: list[EDGRStageResult]
    method: str = "EDGR"
    latency_ms: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExperimentRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "query": "What is CVE-2021-44228 and how is it exploited?",
                    "top_k": 5,
                    "methods": ["EDGR", "RAG", "GraphRAG"],
                }
            ]
        }
    )

    query: str = Field(
        default="What is CVE-2021-44228 and how is it exploited?",
    )
    methods: list[str] = Field(
        default_factory=lambda: [
            "EDGR",
            "RAG",
            "GraphRAG",
            "LightRAG",
            "HippoRAG",
            "Self-RAG",
            "Corrective-RAG",
        ]
    )
    top_k: int = DEFAULT_TOP_K


class ExperimentResult(BaseModel):
    method: str
    answer: str
    faithfulness: float
    hallucination_rate: float
    precision_at_k: float
    recall_at_k: float
    mrr: float
    latency_ms: float
    evidence_count: int


class AblationConfig(BaseModel):
    query: str
    variants: list[str] = Field(
        default_factory=lambda: [
            "full",
            "w/o Temporal",
            "w/o Graph",
            "w/o Trust Score",
        ]
    )


class MetricSummary(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1: float
    faithfulness: float
    hallucination_rate: float
    p_at_k: float
    r_at_k: float
    mrr: float
    avg_latency_ms: float


class ResearchStep(BaseModel):
    id: int
    title: str
    title_vi: str
    status: str  # pending | in_progress | done
    description: str
    artifacts: list[str] = Field(default_factory=list)


class KGStats(BaseModel):
    nodes: int
    edges: int
    entity_types: dict[str, int]
    last_updated: str
    sources: list[str]
