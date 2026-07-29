"""15-step PhD research process A → Z."""

from __future__ import annotations

from app.models.schemas import ResearchStep

RESEARCH_STEPS: list[ResearchStep] = [
    ResearchStep(
        id=1,
        title="Literature Review",
        title_vi="Khảo sát tài liệu",
        status="done",
        description="RAG, GraphRAG, Hallucination mitigation, CTI, IDS/NIDS.",
        artifacts=["survey_notes.md", "related_work_matrix.csv"],
    ),
    ResearchStep(
        id=2,
        title="Identify Gaps",
        title_vi="Xác định khoảng trống",
        status="done",
        description="Stale CTI edges, weak trust signals, high hallucination in IDS/CTI QA.",
        artifacts=["gap_analysis.md"],
    ),
    ResearchStep(
        id=3,
        title="Problem Definition",
        title_vi="Xây dựng bài toán",
        status="done",
        description="Formalize inputs/outputs; goal: reduce hallucinations in IDS/CTI answers.",
        artifacts=["problem_formulation.md"],
    ),
    ResearchStep(
        id=4,
        title="Propose EDGR Algorithm",
        title_vi="Đề xuất thuật toán EDGR",
        status="in_progress",
        description="6-stage evidence-driven dynamic graph retrieval (main contribution).",
        artifacts=["edgr_algorithm.py", "pipeline_diagram.png"],
    ),
    ResearchStep(
        id=5,
        title="Build Dynamic Knowledge Graph",
        title_vi="Xây dựng Dynamic Knowledge Graph",
        status="in_progress",
        description="Multi-source CTI KG with incremental updates (Neo4j-ready).",
        artifacts=["knowledge_graph.py", "cti_seed.py"],
    ),
    ResearchStep(
        id=6,
        title="Hallucination Scoring Model",
        title_vi="Mô hình chấm điểm ảo giác",
        status="in_progress",
        description="Reliability, freshness, graph consistency, semantic relevance → score 0–1.",
        artifacts=["hallucination.py"],
    ),
    ResearchStep(
        id=7,
        title="Data Preparation",
        title_vi="Xây dựng dữ liệu",
        status="done",
        description="MITRE, CVE/NVD, CWE/CAPEC, CISA, threat feeds, IDS datasets → QA set.",
        artifacts=["cti_seed.py", "qa_dataset"],
    ),
    ResearchStep(
        id=8,
        title="System Implementation",
        title_vi="Triển khai hệ thống",
        status="in_progress",
        description="User query → EDGR ↔ KG / Vector DB / LLM → Trusted Answer.",
        artifacts=["FastAPI backend", "React frontend"],
    ),
    ResearchStep(
        id=9,
        title="Experiments & Comparison",
        title_vi="Thực nghiệm & So sánh",
        status="pending",
        description="EDGR vs RAG, GraphRAG, LightRAG, HippoRAG, Self-RAG, Corrective-RAG.",
        artifacts=["/api/experiments"],
    ),
    ResearchStep(
        id=10,
        title="Evaluation",
        title_vi="Đánh giá",
        status="pending",
        description="Accuracy, P/R/F1, Faithfulness, Hallucination Rate, P@k, R@k, MRR, Latency.",
        artifacts=["/api/evaluate"],
    ),
    ResearchStep(
        id=11,
        title="Ablation Study",
        title_vi="Nghiên cứu cắt bỏ thành phần",
        status="pending",
        description="w/o Temporal, w/o Graph, w/o Trust Score.",
        artifacts=["/api/ablation"],
    ),
    ResearchStep(
        id=12,
        title="Algorithm Analysis",
        title_vi="Phân tích thuật toán",
        status="pending",
        description="Complexity T(n)=O(E log V), correctness, convergence, scalability.",
        artifacts=["complexity notes in /api/evaluate"],
    ),
    ResearchStep(
        id=13,
        title="Scientific Publication",
        title_vi="Công bố khoa học",
        status="pending",
        description="4 papers: EDGR, Dynamic KG, Hallucination Scoring, Comprehensive Evaluation.",
        artifacts=["paper_outline.md"],
    ),
    ResearchStep(
        id=14,
        title="Dissertation Writing",
        title_vi="Viết luận án",
        status="pending",
        description="8 chapters from Introduction to Conclusion & Future Work.",
        artifacts=["dissertation_outline"],
    ),
    ResearchStep(
        id=15,
        title="Dissertation Defense",
        title_vi="Bảo vệ luận án",
        status="pending",
        description="Presentation, Q&A, and successful PhD completion.",
        artifacts=["defense_slides"],
    ),
]

DISSERTATION_CHAPTERS = [
    {"ch": 1, "title": "Introduction", "title_vi": "Mở đầu"},
    {"ch": 2, "title": "Overview", "title_vi": "Tổng quan"},
    {"ch": 3, "title": "Problem & Gaps", "title_vi": "Bài toán & khoảng trống"},
    {"ch": 4, "title": "EDGR Algorithm", "title_vi": "Thuật toán EDGR"},
    {"ch": 5, "title": "Dynamic KG", "title_vi": "Đồ thị tri thức động"},
    {"ch": 6, "title": "Hallucination Scoring", "title_vi": "Chấm điểm ảo giác"},
    {"ch": 7, "title": "Experiments & Evaluation", "title_vi": "Thực nghiệm & đánh giá"},
    {"ch": 8, "title": "Conclusion & Future Work", "title_vi": "Kết luận & hướng phát triển"},
]

PAPER_PLAN = [
    {
        "id": 1,
        "title": "EDGR: Evidence-Driven Dynamic Graph Retrieval",
        "focus": "Core 6-stage algorithm for hallucination mitigation",
    },
    {
        "id": 2,
        "title": "Dynamic Knowledge Graph for CTI/IDS",
        "focus": "Incremental multi-source graph construction and updates",
    },
    {
        "id": 3,
        "title": "Hallucination Scoring for Trusted CTI Generation",
        "focus": "Reliability, freshness, consistency, relevance fusion",
    },
    {
        "id": 4,
        "title": "Comprehensive Evaluation against RAG Family",
        "focus": "Benchmarks, ablation, and operational metrics",
    },
]

SUMMARY_FLOW = [
    "Idea",
    "Literature Review",
    "Research",
    "New Algorithm (EDGR)",
    "Experiment",
    "Evaluation",
    "Publication",
    "Dissertation",
    "Defense",
]


def get_research_overview() -> dict:
    done = sum(1 for s in RESEARCH_STEPS if s.status == "done")
    progress = round(100 * done / len(RESEARCH_STEPS), 1)
    return {
        "topic": (
            "An Evidence-Driven Dynamic Graph Retrieval Algorithm for Hallucination "
            "Mitigation in Large Language Models for Intrusion Detection and Cyber Threat Intelligence"
        ),
        "topic_vi": "Thuật toán truy hồi đồ thị động dựa trên bằng chứng để giảm ảo giác LLM trong IDS và CTI",
        "algorithm": "EDGR",
        "progress_percent": progress,
        "steps": [s.model_dump() for s in RESEARCH_STEPS],
        "chapters": DISSERTATION_CHAPTERS,
        "papers": PAPER_PLAN,
        "summary_flow": SUMMARY_FLOW,
    }
