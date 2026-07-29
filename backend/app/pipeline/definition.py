"""16-step PhD research pipeline with nested work items (from process diagram A→Z)."""

from __future__ import annotations

from typing import Any

PIPELINE_STEPS: list[dict[str, Any]] = [
    {
        "id": 1,
        "key": "literature",
        "title": "Khảo sát tài liệu",
        "title_en": "Literature Review",
        "icon": "📚",
        "goal": "Phạm vi Step 1: sáu trục RAG · GraphRAG · KG · hallucination · CTI · IDS/NIDS (+ catalog APA, ma trận phủ).",
        "goal_en": "Step-1 scope: six axes RAG · GraphRAG · KG · hallucination · CTI · IDS/NIDS (+ APA catalog, coverage matrix).",
        "tasks": [
            {"id": "rag", "title": "RAG", "title_en": "RAG", "action": "analyze_topic"},
            {"id": "graphrag", "title": "GraphRAG", "title_en": "GraphRAG", "action": "analyze_topic"},
            {"id": "kg", "title": "Đồ thị tri thức", "title_en": "Knowledge Graph", "action": "analyze_topic"},
            {"id": "hallucination", "title": "Ảo giác LLM", "title_en": "Hallucination", "action": "analyze_topic"},
            {"id": "cti", "title": "Tình báo mối đe dọa mạng", "title_en": "Cyber Threat Intelligence", "action": "analyze_topic"},
            {"id": "ids", "title": "IDS / NIDS", "title_en": "IDS/NIDS", "action": "analyze_topic"},
            {
                "id": "catalog",
                "title": "Danh mục tài liệu tham khảo (≥300)",
                "title_en": "Reference catalog (≥300)",
                "action": "list_bibliography",
            },
            {"id": "matrix", "title": "Ma trận khảo sát", "title_en": "Coverage Matrix", "action": "coverage_matrix"},
        ],
    },
    {
        "id": 2,
        "key": "gaps",
        "title": "Xác định khoảng trống",
        "title_en": "Identify Gaps",
        "icon": "🔍",
        "goal": "Phân tích phương pháp hiện có, hạn chế, khoảng trống và cơ hội đóng góp.",
        "goal_en": "Analyze existing methods, limitations, research gaps, and contribution opportunities.",
        "tasks": [
            {"id": "methods", "title": "Phương pháp hiện có", "title_en": "Existing Methods", "action": "list_methods"},
            {"id": "limitations", "title": "Hạn chế", "title_en": "Limitations", "action": "extract_limitations"},
            {"id": "gaps", "title": "Khoảng trống nghiên cứu", "title_en": "Research Gaps", "action": "compute_gaps"},
            {"id": "contrib", "title": "Cơ hội đóng góp", "title_en": "Contribution Opportunities", "action": "propose_contributions"},
        ],
    },
    {
        "id": 3,
        "key": "problem",
        "title": "Xây dựng bài toán",
        "title_en": "Problem Definition",
        "icon": "🧩",
        "goal": "Định nghĩa I/O, mô hình hóa bài toán, mục tiêu giảm hallucination miền IDS/CTI.",
        "goal_en": "Define I/O, formalize the problem, and set hallucination-reduction goals for IDS/CTI.",
        "tasks": [
            {"id": "io", "title": "Định nghĩa đầu vào / đầu ra", "title_en": "Input/Output", "action": "define_io"},
            {"id": "model", "title": "Mô hình hóa bài toán", "title_en": "Problem Modeling", "action": "formalize"},
            {"id": "goal", "title": "Mục tiêu giảm ảo giác", "title_en": "Hallucination reduction goal", "action": "define_goal"},
        ],
    },
    {
        "id": 4,
        "key": "edgr",
        "title": "Đề xuất thuật toán EDGR",
        "title_en": "Propose EDGR Algorithm",
        "icon": "⚙️",
        "goal": "Đóng góp chính: 6 giai Evidence-Driven Dynamic Graph Retrieval.",
        "goal_en": "Main contribution: 6-stage Evidence-Driven Dynamic Graph Retrieval.",
        "badge": "Đóng góp chính",
        "badge_en": "Main contribution",
        "tasks": [
            {
                "id": "s1",
                "title": "1. Hiểu truy vấn & trích entity",
                "title_en": "1. Query understanding & entity extraction",
                "action": "stage_1",
            },
            {
                "id": "s2",
                "title": "2. Mở rộng đa bước thích ứng",
                "title_en": "2. Adaptive multi-step expansion",
                "action": "stage_2",
            },
            {
                "id": "s3",
                "title": "3. Lọc thời gian",
                "title_en": "3. Temporal filtering",
                "action": "stage_3",
            },
            {
                "id": "s4",
                "title": "4. Xếp hạng bằng chứng",
                "title_en": "4. Evidence Ranking",
                "action": "stage_4",
            },
            {
                "id": "s5",
                "title": "5. Chấm điểm ảo giác",
                "title_en": "5. Hallucination Scoring",
                "action": "stage_5",
            },
            {
                "id": "s6",
                "title": "6. Chọn evidence tin cậy",
                "title_en": "6. Trusted evidence selection",
                "action": "stage_6",
            },
            {
                "id": "full",
                "title": "Chạy full pipeline EDGR",
                "title_en": "Run full EDGR pipeline",
                "action": "run_full",
            },
        ],
    },
    {
        "id": 5,
        "key": "dkg",
        "title": "Xây dựng Dynamic Knowledge Graph",
        "title_en": "Build Dynamic KG",
        "icon": "🕸️",
        "goal": "Xây KG động từ đa nguồn CTI, cập nhật gia tăng, lưu trữ đồ thị.",
        "goal_en": "Build a dynamic KG from diverse CTI sources with incremental updates and graph storage.",
        "tasks": [
            {"id": "sources", "title": "Nguồn dữ liệu đa dạng", "title_en": "Data Sources", "action": "list_sources"},
            {
                "id": "extract",
                "title": "Trích xuất entity & quan hệ",
                "title_en": "Entity/Relation Extraction",
                "action": "extract_graph",
            },
            {
                "id": "update",
                "title": "Cập nhật động (gia tăng)",
                "title_en": "Dynamic incremental update",
                "action": "incremental_update",
            },
            {"id": "store", "title": "Lưu trữ đồ thị", "title_en": "Graph Storage", "action": "storage_stats"},
        ],
    },
    {
        "id": 6,
        "key": "scoring",
        "title": "Mô hình chấm điểm ảo giác",
        "title_en": "Hallucination Scoring Model",
        "icon": "📊",
        "goal": "Tính điểm ảo giác 0–1 từ độ tin cậy nguồn, độ mới, nhất quán đồ thị, liên quan ngữ nghĩa.",
        "goal_en": "Compute a 0–1 hallucination score from reliability, freshness, consistency, and relevance.",
        "tasks": [
            {
                "id": "reliability",
                "title": "Độ tin cậy nguồn",
                "title_en": "Source reliability",
                "action": "factor_reliability",
            },
            {"id": "freshness", "title": "Độ mới", "title_en": "Freshness", "action": "factor_freshness"},
            {
                "id": "consistency",
                "title": "Nhất quán đồ thị",
                "title_en": "Graph consistency",
                "action": "factor_consistency",
            },
            {
                "id": "relevance",
                "title": "Liên quan ngữ nghĩa",
                "title_en": "Semantic relevance",
                "action": "factor_relevance",
            },
            {
                "id": "score",
                "title": "Điểm ảo giác (0–1)",
                "title_en": "Hallucination Score (0–1)",
                "action": "composite_score",
            },
        ],
    },
    {
        "id": 7,
        "key": "data",
        "title": "Xây dựng dữ liệu",
        "title_en": "Data Preparation",
        "icon": "🗄️",
        "goal": "Thu thập MITRE/CVE/CWE/CISA/feeds/IDS và dựng QA Dataset.",
        "goal_en": "Collect MITRE/CVE/CWE/CISA/feeds/IDS data and build the QA dataset.",
        "tasks": [
            {"id": "mitre", "title": "MITRE ATT&CK", "title_en": "MITRE ATT&CK", "action": "ingest_mitre"},
            {"id": "cve", "title": "CVE / NVD", "title_en": "CVE/NVD", "action": "ingest_cve"},
            {"id": "cwe", "title": "CWE / CAPEC", "title_en": "CWE/CAPEC", "action": "ingest_cwe"},
            {"id": "cisa", "title": "CISA / CERT", "title_en": "CISA/CERT", "action": "ingest_cisa"},
            {"id": "feeds", "title": "Nguồn threat feed", "title_en": "Threat Feeds", "action": "ingest_feeds"},
            {"id": "ids", "title": "Tập dữ liệu IDS / NIDS", "title_en": "IDS / NIDS Datasets", "action": "ingest_ids"},
            {"id": "qa", "title": "Sinh QA Dataset", "title_en": "Build QA Dataset", "action": "build_qa"},
        ],
    },
    {
        "id": 8,
        "key": "system",
        "title": "Triển khai hệ thống",
        "title_en": "System Implementation",
        "icon": "🖥️",
        "goal": "Truy vấn người dùng → EDGR ↔ KG / Vector DB / LLM → Câu trả lời tin cậy.",
        "goal_en": "User Query → EDGR ↔ KG / Vector DB / LLM → Trusted Answer.",
        "tasks": [
            {"id": "architecture", "title": "Kiến trúc hệ thống", "title_en": "Architecture", "action": "architecture"},
            {
                "id": "kg_svc",
                "title": "Dịch vụ Knowledge Graph",
                "title_en": "Knowledge Graph service",
                "action": "svc_kg",
            },
            {
                "id": "vec_svc",
                "title": "Dịch vụ Vector DB",
                "title_en": "Vector DB service",
                "action": "svc_vector",
            },
            {
                "id": "llm_svc",
                "title": "Bộ sinh LLM có neo bằng chứng",
                "title_en": "LLM grounded generator",
                "action": "svc_llm",
            },
            {
                "id": "e2e",
                "title": "End-to-end câu trả lời tin cậy",
                "title_en": "End-to-end Trusted Answer",
                "action": "e2e_query",
            },
        ],
    },
    {
        "id": 9,
        "key": "experiments",
        "title": "Thực nghiệm & So sánh",
        "title_en": "Experiments & Comparison",
        "icon": "🧪",
        "goal": "So sánh EDGR với họ RAG trên cùng truy vấn/dataset.",
        "goal_en": "Compare EDGR with the RAG family on the same queries/dataset.",
        "tasks": [
            {"id": "rag", "title": "RAG", "title_en": "RAG", "action": "run_method"},
            {"id": "graphrag", "title": "GraphRAG", "title_en": "GraphRAG", "action": "run_method"},
            {"id": "lightrag", "title": "LightRAG", "title_en": "LightRAG", "action": "run_method"},
            {"id": "hipporag", "title": "HippoRAG", "title_en": "HippoRAG", "action": "run_method"},
            {"id": "selfrag", "title": "Self-RAG", "title_en": "Self-RAG", "action": "run_method"},
            {"id": "crag", "title": "Corrective RAG", "title_en": "Corrective-RAG", "action": "run_method"},
            {"id": "edgr", "title": "EDGR (của chúng tôi)", "title_en": "EDGR (Ours)", "action": "run_method"},
            {"id": "compare", "title": "Bảng so sánh tổng hợp", "title_en": "Aggregate comparison table", "action": "compare_all"},
            {
                "id": "dataset_means",
                "title": "Trung bình dataset + CI (mọi method)",
                "title_en": "Dataset means + CI (all methods)",
                "action": "compare_dataset",
            },
        ],
    },
    {
        "id": 10,
        "key": "evaluation",
        "title": "Đánh giá",
        "title_en": "Evaluation",
        "icon": "📈",
        "goal": "Đo Accuracy, P/R/F1, Faithfulness, Hallucination Rate, P@k/R@k/MRR, Latency, Resource; kèm thống kê cặp, validity, human-eval rubric.",
        "goal_en": "Measure Accuracy, P/R/F1, Faithfulness, Hallucination Rate, P@k/R@k/MRR, Latency, Resources; plus paired stats, validity, human-eval rubric.",
        "tasks": [
            {"id": "accuracy", "title": "Độ chính xác", "title_en": "Accuracy", "action": "metric_accuracy"},
            {"id": "prf1", "title": "Precision / Recall / F1", "title_en": "Precision / Recall / F1", "action": "metric_prf1"},
            {"id": "faith", "title": "Faithfulness", "title_en": "Faithfulness", "action": "metric_faith"},
            {"id": "hall", "title": "Tỷ lệ ảo giác", "title_en": "Hallucination Rate", "action": "metric_hall"},
            {
                "id": "retrieval",
                "title": "Truy hồi P@k / R@k / MRR",
                "title_en": "Retrieval P@k / R@k / MRR",
                "action": "metric_retrieval",
            },
            {"id": "latency", "title": "Độ trễ", "title_en": "Latency", "action": "metric_latency"},
            {
                "id": "resource",
                "title": "Tài nguyên (CPU / Bộ nhớ)",
                "title_en": "Resources (CPU / Memory)",
                "action": "metric_resource",
            },
            {
                "id": "stats",
                "title": "Thống kê cặp (McNemar + bootstrap CI)",
                "title_en": "Paired stats (McNemar + bootstrap CI)",
                "action": "stats_report",
            },
            {
                "id": "validity",
                "title": "Threats to validity",
                "title_en": "Threats to validity",
                "action": "threats_validity",
            },
            {
                "id": "human_eval",
                "title": "Human-eval SOC (rubric + κ + panel)",
                "title_en": "SOC human-eval (rubric + κ + panel)",
                "action": "human_eval_report",
            },
            {
                "id": "human_session",
                "title": "Phiên chấm SOC (hàng đợi live)",
                "title_en": "SOC rating session (live queue)",
                "action": "human_eval_session",
            },
            {
                "id": "rigor",
                "title": "Báo cáo hàm lượng khoa học (H1–H4)",
                "title_en": "Scientific rigor report (H1–H4)",
                "action": "scientific_rigor",
            },
            {"id": "full", "title": "Báo cáo đánh giá đầy đủ", "title_en": "Full evaluation report", "action": "full_report"},
        ],
    },
    {
        "id": 11,
        "key": "ablation",
        "title": "Nghiên cứu cắt bỏ (Ablation)",
        "title_en": "Ablation Study",
        "icon": "🔬",
        "goal": "Loại từng thành phần để chứng minh đóng góp: Temporal, Graph, Trust, Ranking, Scoring.",
        "goal_en": "Remove each component to prove contribution: Temporal, Graph, Trust, Ranking, Scoring.",
        "tasks": [
            {"id": "full", "title": "EDGR đầy đủ", "title_en": "Full EDGR", "action": "ablate"},
            {"id": "wo_temporal", "title": "Không lọc thời gian", "title_en": "w/o Temporal", "action": "ablate"},
            {"id": "wo_graph", "title": "Không đồ thị", "title_en": "w/o Graph", "action": "ablate"},
            {"id": "wo_trust", "title": "Không điểm tin cậy", "title_en": "w/o Trust Score", "action": "ablate"},
            {
                "id": "wo_ranking",
                "title": "Không xếp hạng evidence",
                "title_en": "w/o Evidence Ranking",
                "action": "ablate",
            },
            {
                "id": "wo_scoring",
                "title": "Không chấm điểm ảo giác",
                "title_en": "w/o Hallucination Scoring",
                "action": "ablate",
            },
            {"id": "summary", "title": "Tổng hợp Ablation", "title_en": "Ablation Summary", "action": "ablation_summary"},
        ],
    },
    {
        "id": 12,
        "key": "analysis",
        "title": "Phân tích thuật toán",
        "title_en": "Algorithm Analysis",
        "icon": "🧮",
        "goal": "Phân tích độ phức tạp thời gian/không gian, tính đúng, hội tụ và khả năng mở rộng. T(n)=O(E log V).",
        "goal_en": "Analyze time/space complexity, correctness, convergence, and scalability. T(n)=O(E log V).",
        "tasks": [
            {"id": "time", "title": "Độ phức tạp thời gian", "title_en": "Time complexity", "action": "analyze_time"},
            {"id": "space", "title": "Độ phức tạp không gian", "title_en": "Space complexity", "action": "analyze_space"},
            {"id": "correctness", "title": "Tính đúng", "title_en": "Correctness", "action": "analyze_correctness"},
            {"id": "convergence", "title": "Hội tụ", "title_en": "Convergence", "action": "analyze_convergence"},
            {"id": "scalability", "title": "Khả năng mở rộng", "title_en": "Scalability", "action": "analyze_scalability"},
            {
                "id": "report",
                "title": "Báo cáo phân tích tổng hợp",
                "title_en": "Aggregate analysis report",
                "action": "analysis_report",
            },
        ],
    },
    {
        "id": 13,
        "key": "publication",
        "title": "Công bố khoa học",
        "title_en": "Scientific Publication",
        "icon": "📄",
        "goal": "Lập 4 bài báo: EDGR Algorithm, Dynamic KG, Hallucination Scoring, Comprehensive Evaluation.",
        "goal_en": "Plan 4 papers: EDGR Algorithm, Dynamic KG, Hallucination Scoring, Comprehensive Evaluation.",
        "tasks": [
            {"id": "p1", "title": "Bài 1: Thuật toán EDGR", "title_en": "Paper 1: EDGR Algorithm", "action": "paper_outline"},
            {"id": "p2", "title": "Bài 2: Dynamic KG", "title_en": "Paper 2: Dynamic KG", "action": "paper_outline"},
            {
                "id": "p3",
                "title": "Bài 3: Chấm điểm ảo giác",
                "title_en": "Paper 3: Hallucination Scoring",
                "action": "paper_outline",
            },
            {
                "id": "p4",
                "title": "Bài 4: Đánh giá toàn diện",
                "title_en": "Paper 4: Comprehensive Evaluation",
                "action": "paper_outline",
            },
            {"id": "plan", "title": "Kế hoạch công bố tổng hợp", "title_en": "Publication Plan", "action": "publication_plan"},
        ],
    },
    {
        "id": 14,
        "key": "dissertation",
        "title": "Viết luận án",
        "title_en": "Dissertation Writing",
        "icon": "📘",
        "goal": "Viết 8 chương luận án từ Introduction đến Conclusion & Future Work.",
        "goal_en": "Write 8 dissertation chapters from Introduction to Conclusion & Future Work.",
        "tasks": [
            {"id": "ch1", "title": "Ch1: Mở đầu", "title_en": "Ch1: Introduction", "action": "chapter_draft"},
            {"id": "ch2", "title": "Ch2: Tổng quan", "title_en": "Ch2: Overview", "action": "chapter_draft"},
            {
                "id": "ch3",
                "title": "Ch3: Bài toán & khoảng trống",
                "title_en": "Ch3: Problem & Gaps",
                "action": "chapter_draft",
            },
            {"id": "ch4", "title": "Ch4: Thuật toán EDGR", "title_en": "Ch4: EDGR Algorithm", "action": "chapter_draft"},
            {"id": "ch5", "title": "Ch5: Dynamic KG", "title_en": "Ch5: Dynamic KG", "action": "chapter_draft"},
            {
                "id": "ch6",
                "title": "Ch6: Chấm điểm ảo giác",
                "title_en": "Ch6: Hallucination Scoring",
                "action": "chapter_draft",
            },
            {
                "id": "ch7",
                "title": "Ch7: Thực nghiệm & đánh giá",
                "title_en": "Ch7: Experiments & Evaluation",
                "action": "chapter_draft",
            },
            {
                "id": "ch8",
                "title": "Ch8: Kết luận & hướng phát triển",
                "title_en": "Ch8: Conclusion & Future Work",
                "action": "chapter_draft",
            },
            {"id": "toc", "title": "Mục lục luận án đầy đủ", "title_en": "Full dissertation TOC", "action": "dissertation_toc"},
        ],
    },
    {
        "id": 15,
        "key": "defense",
        "title": "Bảo vệ luận án",
        "title_en": "Dissertation Defense",
        "icon": "🎓",
        "goal": "Chuẩn bị presentation, trả lời phản biện và hoàn tất bảo vệ thành công.",
        "goal_en": "Prepare the presentation, answer committee questions, and complete a successful defense.",
        "tasks": [
            {
                "id": "present",
                "title": "Trình bày — slide bảo vệ",
                "title_en": "Present — defense slides",
                "action": "defense_present",
            },
            {
                "id": "defend",
                "title": "Bảo vệ — hỏi đáp phản biện",
                "title_en": "Defend — Q&A",
                "action": "defense_qa",
            },
            {
                "id": "checklist",
                "title": "Checklist trước bảo vệ",
                "title_en": "Pre-defense checklist",
                "action": "defense_checklist",
            },
            {
                "id": "success",
                "title": "Thành công — tổng kết hoàn thành",
                "title_en": "Success — completion summary",
                "action": "defense_success",
            },
        ],
    },
    {
        "id": 16,
        "key": "practical_app",
        "title": "Ứng dụng thực tế",
        "title_en": "Practical Application",
        "icon": "🛡️",
        "badge": "App",
        "badge_en": "App",
        "goal": (
            "Ứng dụng «Phát hiện xâm nhập và tình báo» — trợ lý SOC phân tích cảnh báo/câu hỏi CTI "
            "bằng EDGR, trả Trusted Answer kèm evidence (không phải bước quy trình nghiên cứu)."
        ),
        "goal_en": (
            "The «Intrusion Detection and Threat Intelligence» app — a SOC assistant that analyzes "
            "alerts/CTI questions with EDGR and returns a Trusted Answer with evidence "
            "(not a research-process step)."
        ),
        "tasks": [
            {
                "id": "console",
                "title": "Phát hiện xâm nhập và tình báo",
                "title_en": "Intrusion Detection and Threat Intelligence",
                "action": "app_console",
            },
        ],
    },
]


# Representative colors aligned with UI StepIcon palette
STEP_COLORS: dict[int, str] = {
    1: "#2563EB",
    2: "#EA580C",
    3: "#0D9488",
    4: "#16A34A",
    5: "#7C3AED",
    6: "#DC2626",
    7: "#0891B2",
    8: "#4338CA",
    9: "#D97706",
    10: "#059669",
    11: "#DB2777",
    12: "#475569",
    13: "#0284C7",
    14: "#B45309",
    15: "#CA8A04",
    16: "#0F766E",
}


def get_pipeline_definition() -> dict[str, Any]:
    from app.pipeline.academic import attach_academic_to_definition

    steps = attach_academic_to_definition()
    for item in steps:
        item["color"] = STEP_COLORS.get(item["id"], "#0D7377")
    return {
        "topic": (
            "An Evidence-Driven Dynamic Graph Retrieval Algorithm for Hallucination "
            "Mitigation in Large Language Models for Intrusion Detection and Cyber Threat Intelligence"
        ),
        "topic_vi": (
            "Thuật toán truy hồi đồ thị động dựa trên bằng chứng để giảm ảo giác "
            "trong LLM cho phát hiện xâm nhập và tình báo mối đe dọa mạng"
        ),
        "steps": steps,
        "step_count": len(PIPELINE_STEPS),
        "academic_blocks": [
            "csdl",
            "mo_hinh_toan",
            "mo_hinh_thuat_toan",
            "mo_hinh_hoat_dong",
            "trich_dan",
            "minh_chung",
            "nhan_dinh_danh_gia",
        ],
    }


def get_step(step_id: int) -> dict[str, Any] | None:
    for s in PIPELINE_STEPS:
        if s["id"] == step_id:
            return s
    return None


# Step 16 is a single product console; accept legacy/alias task ids from older UIs.
_STEP16_TASK_ALIASES = frozenset(
    {"console", "demo", "product", "success", "failure", "app", "analyze", "apps"}
)


def get_task(step_id: int, task_id: str) -> dict[str, Any] | None:
    step = get_step(step_id)
    if not step:
        return None
    for t in step["tasks"]:
        if t["id"] == task_id:
            return t
    # Older frontends may still call 16/demo or 16/product — map to the live console.
    if step_id == 16 and task_id in _STEP16_TASK_ALIASES:
        for t in step["tasks"]:
            if t["id"] == "console":
                return t
    return None
