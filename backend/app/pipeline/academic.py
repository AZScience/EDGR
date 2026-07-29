"""
Academic blocks for every parent step and child task:
CSDL, Mathematical model, Algorithm model, Operating model,
Citations, Evidence, Assessment.
"""

from __future__ import annotations

import re
from typing import Any

from app.core.knowledge_graph import kg
from app.core.vector_store import vector_store
from app.data.cti_seed import QA_DATASET
from app.data.literature_corpus import PAPERS
from app.pipeline.definition import PIPELINE_STEPS, get_step, get_task
from app.pipeline.assess_i18n import enrich_assessment
from app.pipeline.math_specs import (
    FACTOR_MATH,
    METRIC_MATH,
    SOURCE_MATH,
    STAGE_MATH,
    STEP_MATH,
    analysis_math_for,
    formula,
    legacy_math_to_pack,
    math_model,
    var,
)
from app.pipeline.scientific import ensure_scientific_package
from app.pipeline.step_guides import enrich_csdl, get_purpose
from app.pipeline.theory_guides import get_theory
from app.pipeline.graph_viz import academic_graph_viz
from app.pipeline.publication_papers import (
    get_paper_academic_overlay,
    publication_plan_doc,
)
from app.pipeline.topic_scientific import TOPIC_CITES, build_topic_overlay

# Shared citation pool (real bibliographic records)
CITE = {p["id"]: p for p in PAPERS}


def _cite(*ids: str) -> list[dict[str, Any]]:
    out = []
    for i in ids:
        p = CITE.get(i)
        if p:
            out.append(
                {
                    "id": p["id"],
                    "text": f"{p['authors']} ({p['year']}). {p['title']}. {p['venue']}.",
                    "doi": p.get("doi"),
                    "year": p["year"],
                }
            )
    return out


def _strip_leading_index(label: str) -> str:
    """Task titles may already be '1. …' — avoid '1. 1. …' in step flow."""
    return re.sub(r"^\s*\d+\.\s*", "", (label or "").strip())


def _step_operating_model(step: dict[str, Any]) -> dict[str, Any]:
    """
    Step-overview operating model = research workflow across child tabs.
    Distinct from the algorithm execution pipeline shown on task tabs.
    """
    tasks = list(step.get("tasks") or [])
    flow_vi = [
        _strip_leading_index(str(t.get("title") or t.get("id") or ""))
        for t in tasks
    ]
    flow_en = [
        _strip_leading_index(
            str(t.get("title_en") or t.get("title") or t.get("id") or "")
        )
        for t in tasks
    ]
    if not flow_vi:
        flow_vi = ["Đọc mục đích bước", "Chạy công việc (nếu có)", "Tổng hợp minh chứng"]
        flow_en = ["Read step purpose", "Run tasks (if any)", "Synthesize evidence"]
    return {
        "kind": "step",
        "caption_vi": (
            "Luồng vận hành bước nghiên cứu: thứ tự các công việc con. "
            "Không phải pipeline thực thi thuật toán — pipeline đó nằm ở tab công việc "
            "(khối «Mô hình hoạt động của thuật toán»)."
        ),
        "caption_en": (
            "Step research workflow: ordered child tasks. "
            "This is not the algorithm execution pipeline — that appears on task tabs "
            "(«Algorithm operating model»)."
        ),
        "flow_vi": flow_vi,
        "flow_en": flow_en,
        "flow": flow_vi,  # fallback for older clients
        "io": {
            "in_vi": "Mục tiêu bước + trạng thái CSDL/KG hiện có",
            "in_en": "Step goal + current DB/KG state",
            "in": "Mục tiêu bước + trạng thái CSDL/KG hiện có",
            "out_vi": "Minh chứng từng công việc → tổng hợp đánh giá bước",
            "out_en": "Per-task evidence → step-level assessment",
            "out": "Minh chứng từng công việc → tổng hợp đánh giá bước",
        },
        "actors_vi": ["Nghiên cứu viên", "Tổng quan bước", "Các tab công việc con"],
        "actors_en": ["Researcher", "Step overview", "Child task tabs"],
        "modules": ["StepOverview", "ChildTasks"],
    }


def _mark_algorithm_ops(ops: dict[str, Any] | None) -> dict[str, Any]:
    """Tag task-level flows as algorithm execution (not step workflow)."""
    out = dict(ops or {})
    if out.get("kind") in ("step", "publication", "app", "plan", "product"):
        return out
    # Special document payloads keep their own renderers
    if any(
        k in out
        for k in (
            "manuscript",
            "papers",
            "product_name",
            "apps",
            "timeline",
            "venues",
        )
    ):
        return out
    out.setdefault("kind", "algorithm")
    out.setdefault(
        "caption_vi",
        "Luồng thực thi thuật toán: các giai đoạn I/O quan sát được khi chạy.",
    )
    out.setdefault(
        "caption_en",
        "Algorithm execution flow: observable I/O stages at runtime.",
    )
    return out


def _block(
    csdl: dict[str, Any],
    math: dict[str, Any],
    algorithm: dict[str, Any],
    operating: dict[str, Any],
    citations: list[dict[str, Any]],
    evidence: dict[str, Any],
    assessment: dict[str, Any],
) -> dict[str, Any]:
    return {
        "csdl": csdl,
        "mo_hinh_toan": math,
        "mo_hinh_thuat_toan": algorithm,
        "mo_hinh_hoat_dong": operating,
        "trich_dan": citations,
        "minh_chung": evidence,
        "nhan_dinh_danh_gia": assessment,
    }


# ─── Step-level defaults ──────────────────────────────────────────────

STEP_ACADEMIC: dict[int, dict[str, Any]] = {
    1: _block(
        csdl={
            "name": "Literature Corpus DB",
            "tables": ["papers(id,title,authors,year,venue,tags,doi,summary,limitations)"],
            "sources": ["NeurIPS", "ICLR", "SIGIR", "ACM CSUR", "arXiv", "MITRE TR", "IEEE S&P", "USENIX Security"],
            "live_count": len(PAPERS),
            "min_references": 300,
            "storage": "app/data/literature_corpus.py",
            "access": "Step 1 → task «Danh mục tài liệu tham khảo (≥300)»",
        },
        math=STEP_MATH[1],
        algorithm={
            "name_vi": "Khảo sát chủ đề có hệ thống",
            "name_en": "Systematic Topic Survey",
            "pseudocode": [
                "1. Load corpus P / Nạp tập P",
                "2. Filter by topic tag t / Lọc theo chủ đề t",
                "3. Aggregate venues, years, limitations / Tổng hợp",
                "4. Build coverage matrix C and pair counts / Ma trận phủ",
            ],
            "complexity": "O(|P| · |T|)",
        },
        operating={
            "flow": [
                "Mở Bước 1 → chọn tab con",
                "Bấm Chạy trên tab đang chọn",
                "Đọc kết quả runtime (không trùng khối lý thuyết)",
                "Sang tab tiếp theo trong sequence",
            ],
            "io": {
                "in": "topic tag / thẻ chủ đề",
                "out": "paper list + coverage / danh sách paper + độ phủ",
            },
            "actors": ["Researcher / NCS", "Literature DB"],
        },
        citations=_cite("lewis2020rag", "edge2024graphrag", "gao2024ragsurvey", "ji2023survey"),
        evidence={
            "type": "corpus_statistics",
            "metric": f"|P|={len(PAPERS)}",
            "axes": 6,
        },
        assessment={
            "strength": "Phủ đủ 6 trục theo sơ đồ quy trình",
            "limitation": "Corpus curated, chưa crawl toàn phần Web of Science",
            "verdict": "Đủ làm tiền đề gap analysis bước 2",
            "score_0_1": 0.82,
        },
    ),
    2: _block(
        csdl={
            "name": "Gap Analysis Store",
            "tables": ["methods", "limitations(theme,paper_id,text)", "gaps(id,statement,severity)"],
            "derived_from": "Literature Corpus + limitation NLP tagging",
        },
        math=STEP_MATH[2],
        algorithm={
            "name": "Limitation Thematic Clustering + Gap Ranking",
            "pseudocode": [
                "Extract limitations from papers",
                "Theme-tag: temporal|trust|cti|graph",
                "Compute weak intersections",
                "Emit G1..Gk with priority",
            ],
        },
        operating={
            "flow": ["Methods inventory", "Limitation extract", "Gap compute", "Contribution map"],
            "io": {"in": "coverage matrix", "out": "G1–G3 + C1–C4"},
        },
        citations=_cite("gao2024ragsurvey", "huang2025hallu", "rahman2024llmsoc", "edge2024graphrag"),
        evidence={
            "type": "derived_gaps",
            "gaps": ["G1 temporal+trust CTI", "G2 graph without risk gate", "G3 critique ≠ consistency"],
        },
        assessment={
            "strength": "Gaps gắn bằng chứng bibliographic, không suy diễn suông",
            "limitation": "Chưa có expert Delphi validation",
            "verdict": "Căn cứ vững cho formal problem (bước 3)",
            "score_0_1": 0.8,
        },
    ),
    3: _block(
        csdl={
            "name": "Problem Spec Registry",
            "tables": ["io_spec", "constraints", "success_criteria"],
            "domain": "IDS/CTI QA",
        },
        math=STEP_MATH[3],
        algorithm={
            "name": "Problem Formalization Checklist",
            "pseudocode": ["Define I/O", "Write objective", "List constraints", "Set success metrics"],
        },
        operating={
            "flow": ["I/O define", "Model", "Goal & non-goals"],
            "io": {"in": "gaps G1–G3", "out": "formal problem statement"},
        },
        citations=_cite("lewis2020rag", "ji2023survey", "strom2018attack"),
        evidence={"type": "spec", "artifacts": ["define_io", "formalize", "define_goal"]},
        assessment={
            "strength": "Objective tối ưu rõ, ràng buộc CVE/ATT&CK",
            "limitation": "HallucinationRisk là proxy đo được, không phải human gold đầy đủ",
            "verdict": "Đủ để thiết kế EDGR như solver",
            "score_0_1": 0.85,
        },
    ),
    4: _block(
        csdl={
            "name": "EDGR Runtime Stores",
            "stores": ["DynamicKG(V,E)", "VectorIndex(D)", "EvidenceScoreTable"],
            "live": {"V": "kg.nodes", "E": "kg.edges", "D": "vector_store.chunks"},
        },
        math=STEP_MATH[4],
        algorithm={
            "name_vi": "EDGR — Truy hồi đồ thị động dựa trên bằng chứng",
            "name_en": "EDGR — Evidence-Driven Dynamic Graph Retrieval",
            "pseudocode": [
                "φ1 EntityExtract(q)→S",
                "φ2 Expand(S,G_t,h)→N",
                "φ3 TemporalFilter(N\\S)∪S→N'",
                "φ4 Rank(q,N',D)→C",
                "φ5 Score(C)→risk",
                "φ6 Select(risk,θ,k)→E*; Answer=Gen(q,E*)",
            ],
            "complexity": "T(n)=O(E log V)",
        },
        operating={
            "kind": "algorithm",
            "caption_vi": "Pipeline thực thi EDGR φ1–φ6 → Trusted Answer.",
            "caption_en": "EDGR execution pipeline φ1–φ6 → Trusted Answer.",
            "flow": [
                "Query / Truy vấn",
                "Entity / Thực thể",
                "Expand / Mở rộng",
                "Temporal / Lọc thời gian",
                "Rank / Xếp hạng",
                "Score / Chấm điểm",
                "Select / Chọn",
                "Trusted Answer / Câu trả lời tin cậy",
            ],
            "modules": ["EDGREngine", "HallucinationScorer", "GroundedGenerator"],
        },
        citations=_cite("lewis2020rag", "edge2024graphrag", "gutierrez2024hipporag", "asai2024selfrag", "yan2024crag"),
        evidence={"type": "pipeline_stages", "stage_count": 6, "claim": "Mỗi stage có output đo được"},
        assessment={
            "strength": "Đóng góp chính: trust gate trước generation trên CTI graph",
            "limitation": "Generator extractive; LLM API có thể thay thế",
            "verdict": "Core contribution của luận án",
            "score_0_1": 0.9,
        },
    ),
    5: _block(
        csdl={
            "name": "Dynamic CTI Knowledge Graph",
            "schema": "Node(id,type,label,timestamp,reliability); Edge(src,tgt,rel,w,ts)",
            "sources": ["MITRE ATT&CK", "CVE/NVD", "CWE/CAPEC", "CISA", "Threat feeds", "IDS"],
            "backend": "NetworkX DiGraph (Neo4j-compatible export)",
        },
        math=STEP_MATH[5],
        algorithm={
            "name": "Incremental CTI Graph Builder",
            "pseudocode": ["Ingest source", "Extract entities/relations", "Upsert nodes/edges", "Reindex evidence"],
        },
        operating={
            "flow": ["Sources", "Extract", "Incremental update", "Store/query"],
            "api": ["/api/kg", "/api/pipeline/5/*/run"],
        },
        citations=_cite("strom2018attack", "wagner2019cti", "peng2023kgllm", "edge2024graphrag"),
        evidence={"type": "live_kg", "description": "Thống kê V,E lấy từ KG đang chạy"},
        assessment={
            "strength": "Đa nguồn + incremental thật vào process memory",
            "limitation": "Chưa deploy Neo4j production",
            "verdict": "Đủ cho EDGR retrieval experiments",
            "score_0_1": 0.84,
        },
    ),
    6: _block(
        csdl={
            "name": "Evidence Feature Store",
            "features": ["reliability", "freshness", "graph_consistency", "semantic_relevance"],
            "range": "[0,1] → hallucination_risk",
        },
        math=STEP_MATH[6],
        algorithm={
            "name": "HallucinationScorer",
            "pseudocode": ["Compute R,F,G,S", "τ=weighted sum", "ρ=1-τ", "Rank by τ"],
        },
        operating={
            "flow": ["Retrieve candidates", "Score factors", "Composite risk", "Gate by θ"],
        },
        citations=_cite("ji2023survey", "huang2025hallu", "asai2024selfrag", "yan2024crag"),
        evidence={"type": "factor_breakdown", "claim": "Mỗi evidence có 4 nhân tố + risk"},
        assessment={
            "strength": "Đa tín hiệu (nguồn, thời gian, đồ thị, ngữ nghĩa)",
            "limitation": "Trọng số cố định; có thể học bằng regression",
            "verdict": "Phù hợp trusted selection CTI",
            "score_0_1": 0.86,
        },
    ),
    7: _block(
        csdl={
            "name": "CTI/IDS Data Lake + QA Dataset",
            "sources": ["MITRE", "CVE/NVD", "CWE/CAPEC", "CISA/CERT", "Feeds", "CIC-IDS/UNSW"],
            "qa_table": "qa(id,question,gold_answer,gold_entities,gold_evidence_ids)",
            "live_qa": len(QA_DATASET),
        },
        math=STEP_MATH[7],
        algorithm={
            "name": "Multi-source Ingest + QA Construction",
            "pseudocode": ["Ingest each source", "Normalize entities", "Build evidence chunks", "Emit QA pairs"],
        },
        operating={
            "flow": ["MITRE→CVE→CWE→CISA→Feeds→IDS→QA"],
        },
        citations=_cite("strom2018attack", "khraisat2019ids", "ring2019nids", "wagner2019cti"),
        evidence={"type": "dataset", "seed_qa": len(QA_DATASET), "evidence_chunks": "vector_store"},
        assessment={
            "strength": "QA gắn gold evidence_ids cho retrieval metrics",
            "limitation": "Quy mô demo; cần mở rộng annotated gold",
            "verdict": "Đủ evaluate EDGR vs baselines",
            "score_0_1": 0.8,
        },
    ),
    8: _block(
        csdl={
            "name": "System Runtime",
            "components": ["API", "EDGR", "KG", "VectorDB", "Generator"],
            "endpoints": ["/api/query", "/api/pipeline/*", "/api/kg"],
        },
        math=STEP_MATH[8],
        algorithm={
            "name": "Trusted Answer Serving Pipeline",
            "pseudocode": ["Receive q", "Run EDGR", "Return a,E*,metrics"],
        },
        operating={
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
            "diagram": "system_architecture",
            "architecture": None,  # filled in get_academic_block
        },
        citations=_cite("lewis2020rag", "gao2024ragsurvey", "edge2024graphrag"),
        evidence={"type": "e2e", "claim": "E2E query trả faithfulness/hallucination thật"},
        assessment={
            "strength": "Kiến trúc khớp sơ đồ triển khai hệ thống (xem hình kiến trúc)",
            "limitation": "Single-process demo; cần containerize",
            "verdict": "Sẵn sàng cho experiments bước 9",
            "score_0_1": 0.83,
            "figures_vi": [
                "Sơ đồ kiến trúc hệ thống EDGR (Query → API → EDGR ↔ KG/Vector/Scorer → Generator → Answer)",
            ],
            "figures_en": [
                "EDGR system architecture diagram (Query → API → EDGR ↔ KG/Vector/Scorer → Generator → Answer)",
            ],
        },
    ),
    9: _block(
        csdl={
            "name": "Experiment Ledger",
            "tables": ["runs(method,query,faithfulness,hall_rate,p_at_k,mrr,latency)"],
            "methods": ["RAG", "GraphRAG", "LightRAG", "HippoRAG", "Self-RAG", "Corrective-RAG", "EDGR"],
        },
        math=STEP_MATH[9],
        algorithm={
            "name": "Controlled Baseline Comparison",
            "pseudocode": ["For each method m", "Retrieve with m-policy", "Generate", "Score same metrics"],
            "note": "Không degrade điểm giả / No artificial score degradation",
        },
        operating={
            "flow": ["Fix query/dataset", "Run each method", "Aggregate table"],
        },
        citations=_cite("lewis2020rag", "edge2024graphrag", "guo2024lightrag", "gutierrez2024hipporag", "asai2024selfrag", "yan2024crag"),
        evidence={"type": "comparison_table", "claim": "Cùng KG+index, khác retrieval policy"},
        assessment={
            "strength": "Protocol công bằng, metrics thống nhất",
            "limitation": "Baselines là re-implementation research-faithful, không phải official code dump",
            "verdict": "Hợp lệ cho so sánh trong luận án demo",
            "score_0_1": 0.81,
        },
    ),
    10: _block(
        csdl={
            "name": "Evaluation Results DB",
            "metrics": ["Accuracy", "P/R/F1", "Faithfulness", "HallucinationRate", "P@k", "R@k", "MRR", "Latency", "CPU/Mem"],
        },
        math=STEP_MATH[10],
        algorithm={
            "name": "Offline Evaluator",
            "pseudocode": ["For each QA", "Run EDGR", "Compute metrics", "Aggregate mean"],
        },
        operating={
            "flow": ["Load QA", "Infer", "Score", "Resource probe", "Report"],
        },
        citations=_cite("ji2023survey", "gao2024ragsurvey", "khraisat2019ids"),
        evidence={"type": "metric_report", "claim": "psutil đo resource thật"},
        assessment={
            "strength": "Đa metric: generation + retrieval + system",
            "limitation": "Accuracy proxy từ F1/entity hit",
            "verdict": "Đủ cho chương Experiments",
            "score_0_1": 0.84,
        },
    ),
    11: _block(
        csdl={
            "name": "Ablation Run Store",
            "variants": ["full", "w/o Temporal", "w/o Graph", "w/o Trust", "w/o Ranking", "w/o Scoring"],
        },
        math=STEP_MATH[11],
        algorithm={
            "name": "Component Ablation",
            "pseudocode": ["Disable component c", "Rerun EDGR", "Compare metrics to full"],
        },
        operating={
            "flow": ["Select variant", "Run", "Delta table", "Interpret"],
        },
        citations=_cite("asai2024selfrag", "yan2024crag", "edge2024graphrag"),
        evidence={"type": "ablation_deltas", "claim": "Tắt thành phần thật trong engine"},
        assessment={
            "strength": "Chứng minh đóng góp từng module",
            "limitation": "Tương tác bậc cao giữa components chưa phân tích đầy đủ",
            "verdict": "Bắt buộc cho paper EDGR",
            "score_0_1": 0.85,
        },
    ),
    12: _block(
        csdl={
            "name": "Complexity Profile Store",
            "fields": ["V", "E", "D", "stage_latency_ms", "scale_rows"],
        },
        math=STEP_MATH[12],
        algorithm={
            "name": "Analytical + Empirical Profiler",
            "pseudocode": ["Derive bounds", "Time stages", "Scale |D|", "Check invariants"],
        },
        operating={
            "flow": ["Time", "Space", "Correctness", "Convergence", "Scalability", "Report"],
        },
        citations=_cite("gutierrez2024hipporag", "edge2024graphrag", "gao2024ragsurvey"),
        evidence={"type": "empirical_timing", "claim": "Đo latency stage trên KG live"},
        assessment={
            "strength": "Vừa asymptotic vừa empirical",
            "limitation": "Chưa chứng minh formal theorem prover",
            "verdict": "Đáp ứng yêu cầu phân tích thuật toán",
            "score_0_1": 0.83,
        },
    ),
    13: _block(
        csdl={
            "name": "Complete manuscript store",
            "papers": 1,
            "fields": ["title", "sections", "themes", "venues", "maps_to_steps", "live_artifacts"],
        },
        math=STEP_MATH[13],
        algorithm={
            "name": "Publication Packaging",
            "pseudocode": [
                "Lock one contribution claim",
                "Map four pillars → sections",
                "Attach live metrics/KG/weights",
                "Emit complete outline + venue targets",
            ],
        },
        operating={
            "flow": ["Complete paper (9 sections)", "Submission & venue plan"],
        },
        citations=_cite("lewis2020rag", "edge2024graphrag", "ji2023survey", "wagner2019cti"),
        evidence={"type": "outlines", "claim": "One complete paper outline tied to live pipeline artifacts"},
        assessment={
            "strength": "Một bài gộp đủ bốn trụ đóng góp",
            "limitation": "Chưa submit — mới ở mức kế hoạch+outline hoàn chỉnh",
            "verdict": "Sẵn sàng soạn thảo một manuscript",
            "score_0_1": 0.82,
        },
    ),
    14: _block(
        csdl={
            "name": "Dissertation Chapter Store",
            "chapters": 8,
            "fields": ["outline", "source_steps", "artifacts", "wordcount_target"],
        },
        math=STEP_MATH[14],
        algorithm={
            "name": "Chapter Draft Assembler",
            "pseudocode": ["Map chapter→pipeline steps", "Pull live artifacts", "Emit draft notes"],
        },
        operating={
            "flow": ["Ch1…Ch8", "TOC", "Wordcount plan"],
        },
        citations=_cite("gao2024ragsurvey", "strom2018attack", "khraisat2019ids", "huang2025hallu"),
        evidence={"type": "toc", "claim": "TOC 8 chương theo sơ đồ luận án"},
        assessment={
            "strength": "Cấu trúc chuẩn luận án kỹ thuật",
            "limitation": "Nội dung prose chưa viết full",
            "verdict": "Khung viết hoàn chỉnh",
            "score_0_1": 0.8,
        },
    ),
    15: _block(
        csdl={
            "name": "Defense Pack Store",
            "artifacts": ["slides", "qa_bank", "checklist", "final_metrics"],
        },
        math=STEP_MATH[15],
        algorithm={
            "name": "Defense Preparation Workflow",
            "pseudocode": ["Build slides from metrics", "Prepare Q&A", "Checklist", "Success summary"],
        },
        operating={
            "flow": ["Present", "Defend", "Checklist", "Success"],
            "summary_flow": [
                "Idea",
                "Literature",
                "Research",
                "EDGR",
                "Experiment",
                "Evaluation",
                "Publication",
                "Dissertation",
                "Defense",
            ],
        },
        citations=_cite("rahman2024llmsoc", "gao2024ragsurvey", "edge2024graphrag"),
        evidence={"type": "checklist", "claim": "Checklist map quy trình A→Z"},
        assessment={
            "strength": "Đóng vòng quy trình nghiên cứu đầy đủ",
            "limitation": "Bảo vệ thật phụ thuộc hội đồng",
            "verdict": "Pipeline sẵn sàng rehearsal bảo vệ",
            "score_0_1": 0.88,
        },
    ),
    16: _block(
        csdl={
            "name": "IDS/CTI Practical App Store",
            "artifacts": ["app_profile", "success_cases", "failure_cases", "demo_runs"],
        },
        math=STEP_MATH[16],
        algorithm={
            "name": "IDS/CTI App Packaging",
            "pseudocode": [
                "Define product I/O",
                "Bind EDGR+KG+Gate",
                "Enumerate Apply=1 / Apply=0 cases",
                "Run live demo query",
            ],
        },
        operating={
            "flow": ["Product", "Success cases", "Failure cases", "Live demo"],
        },
        citations=_cite(
            "wagner2019cti",
            "khraisat2019ids",
            "lewis2020rag",
            "edge2024graphrag",
            "ji2023survey",
        ),
        evidence={
            "type": "application",
            "claim": "Ứng dụng «Phát hiện xâm nhập và tình báo» đóng gói EDGR",
        },
        assessment={
            "strength": "Có sản phẩm demo + biên được/thất + chạy thử sống",
            "limitation": "Chưa phải triển khai SOC production",
            "verdict": "Bước ứng dụng thực tế đủ cho luận án demo",
            "score_0_1": 0.86,
        },
    ),
}


# ─── Task-specific overlays ───────────────────────────────────────────

def _task_overlay(step_id: int, task_id: str) -> dict[str, Any] | None:
    """Return task-specific academic specialization merged onto step defaults."""
    key = f"{step_id}:{task_id}"

    # Step 1 topics — full scientific frame (math, algo, pros/cons, improve, evidence)
    if step_id == 1 and task_id in TOPIC_CITES:
        pack = build_topic_overlay(task_id)
        if pack:
            cites = TOPIC_CITES[task_id]
            pack["trich_dan"] = _cite(*cites)
            return pack

    if key == "1:catalog":
        return {
            "csdl": {
                "name_vi": "Bảng bibliography (xuất APA)",
                "name_en": "Bibliography table (APA export)",
                "live_count": len(PAPERS),
                "min_references": 300,
                "citation_style": "APA 7th edition",
                "explain_vi": "Schema: id, authors, year, title, venue, doi, tags, catalog — xuất dạng APA.",
                "explain_en": "Schema: id, authors, year, title, venue, doi, tags, catalog — emitted as APA.",
                "role_vi": "Nguồn hàng cho danh sách References.",
                "role_en": "Row source for the References list.",
            },
            "mo_hinh_thuat_toan": {
                "name_vi": "Format APA & sắp xếp",
                "name_en": "APA format & sort",
                "steps": [
                    "Load PAPERS",
                    "format_apa(author, year, title, venue, DOI)",
                    "Sort A–Z by author",
                ],
            },
            "mo_hinh_hoat_dong": {
                "flow": [
                    "Mở tab Danh mục",
                    "Chạy list_bibliography",
                    "Cuộn danh sách APA / lọc tag nếu cần",
                ],
            },
            "minh_chung": {
                "type": "bibliography",
                "live_count": len(PAPERS),
                "min_references": 300,
                "style": "APA 7th",
            },
            "nhan_dinh_danh_gia": {
                "strength": "Core có DOI thật; pipeline APA chạy trên dữ liệu sống",
                "strength_en": "Core has real DOIs; APA pipeline runs on live data",
                "limitation": "Extended là scaffold tổng hợp (≥300) — không trích dẫn như paper thật",
                "limitation_en": "Extended is a synthetic scaffold (≥300) — not citable as real papers",
                "verdict": "Đủ quy mô demo; gap/phủ nghiên cứu chỉ dùng core",
                "verdict_en": "Adequate demo scale; research gaps/coverage use core only",
                "score_0_1": 0.9 if len(PAPERS) >= 300 else 0.5,
            },
        }

    if key == "1:matrix":
        return {
            "mo_hinh_toan": math_model(
                formula(
                    id="matrix",
                    label_vi="Ma trận phủ chủ đề",
                    label_en="Topic coverage matrix",
                    latex=r"M[p,t]=1\iff t\in\mathrm{tags}(p);\quad\mathrm{Pair}(a,b)=\sum_p M[p,a]M[p,b]",
                    explain_vi="M đánh dấu paper–chủ đề; Pair đếm đồng xuất hiện để phát hiện gap.",
                    explain_en="M marks paper–topic; Pair counts co-occurrence to surface gaps.",
                    variables=[
                        var("M", "ma trận nhị phân", "binary matrix", "{0,1}", "phủ đủ T"),
                        var("Pair", "đồng xuất hiện", "co-occurrence", "≥0", "thấp = gap"),
                    ],
                    optimize_vi="Tốt khi ma trận lộ Pair(CTI,GraphRAG) và Pair(IDS,hallucination) mỏng → biện minh EDGR.",
                    optimize_en="Good when the matrix shows thin Pair(CTI,GraphRAG) and Pair(IDS,hallucination) → justifies EDGR.",
                ),
            ),
            "mo_hinh_thuat_toan": {"name": "CoverageMatrixBuilder"},
            "minh_chung": {"weak_pairs_example": ["graphrag+cti", "graphrag+ids"]},
            "nhan_dinh_danh_gia": {
                "verdict": "Ma trận chỉ ra giao CTI∩GraphRAG∩Hallucination còn mỏng → gap EDGR / thin intersection justifies EDGR gap",
                "score_0_1": 0.86,
            },
        }

    # Step 4 EDGR stages
    stage_meta = {
        "s1": {
            "algo": ["Regex CTI IDs", "Dictionary match labels", "Return seed set S"],
            "ops": ["Input q", "Scan KG+patterns", "Output entities"],
            "cite": ("strom2018attack", "wagner2019cti"),
        },
        "s2": {
            "algo": ["BFS/frontier expand", "Cap max_nodes", "Collect relations"],
            "ops": ["Seeds→neighbors", "Multi-hop", "Relation summary"],
            "cite": ("edge2024graphrag", "gutierrez2024hipporag"),
        },
        "s3": {
            "algo": ["Split seeds/neighbors", "Filter neighbors by window", "Union"],
            "ops": ["Preserve query entities", "Drop stale neighbors"],
            "cite": ("wagner2019cti", "rahman2024llmsoc"),
        },
        "s4": {
            "algo": ["TF-IDF retrieve", "Graph-entity boost", "Merge+sort"],
            "ops": ["Vector hits", "Graph hits", "Fused ranking"],
            "cite": ("lewis2020rag", "guo2024lightrag"),
        },
        "s5": {
            "algo": ["Compute 4 factors", "Weighted trust", "Emit risk"],
            "ops": ["Feature extract", "Score", "Sort by trust"],
            "cite": ("ji2023survey", "huang2025hallu"),
        },
        "s6": {
            "algo": ["Threshold filter", "Entity-overlap tie-break", "Synthesize answer"],
            "ops": ["Gate", "Select", "Generate trusted answer"],
            "cite": ("asai2024selfrag", "yan2024crag"),
        },
        "full": {
            "algo": ["Run φ1..φ6 end-to-end", "Return metrics"],
            "ops": ["Single API call", "Full stage trace"],
            "cite": ("lewis2020rag", "edge2024graphrag", "asai2024selfrag"),
        },
    }
    if step_id == 4 and task_id in stage_meta and task_id in STAGE_MATH:
        sm = stage_meta[task_id]
        return {
            "mo_hinh_toan": STAGE_MATH[task_id],
            "mo_hinh_thuat_toan": {
                "name": f"EDGR-{task_id}",
                "name_vi": f"Giai đoạn EDGR {task_id}",
                "name_en": f"EDGR stage {task_id}",
                "steps": sm["algo"],
            },
            "mo_hinh_hoat_dong": {
                "kind": "algorithm",
                "caption_vi": f"Thực thi giai đoạn EDGR «{task_id}» — I/O quan sát được.",
                "caption_en": f"EDGR stage «{task_id}» execution — observable I/O.",
                "flow": sm["ops"],
            },
            "trich_dan": _cite(*sm["cite"]),
            "minh_chung": {"stage": task_id, "observable": "stage.output + duration_ms"},
            "nhan_dinh_danh_gia": {
                "verdict": f"Stage {task_id} là mắt xích bắt buộc của EDGR; có I/O quan sát được / mandatory EDGR stage with observable I/O",
                "score_0_1": 0.88,
            },
        }

    # Step 6 factors
    factor_cite = {
        "reliability": "yan2024crag",
        "freshness": "wagner2019cti",
        "consistency": "edge2024graphrag",
        "relevance": "lewis2020rag",
        "score": "ji2023survey",
    }
    if step_id == 6 and task_id in FACTOR_MATH:
        return {
            "mo_hinh_toan": FACTOR_MATH[task_id],
            "trich_dan": _cite(factor_cite[task_id], "huang2025hallu"),
            "minh_chung": {"factor": task_id, "output": "per-evidence rows"},
            "nhan_dinh_danh_gia": {
                "verdict": f"Nhân tố {task_id} đóng góp trực tiếp vào risk gate / factor feeds the risk gate",
                "score_0_1": 0.85,
            },
        }

    # Step 9 methods
    methods = {
        "rag": "RAG",
        "graphrag": "GraphRAG",
        "lightrag": "LightRAG",
        "hipporag": "HippoRAG",
        "selfrag": "Self-RAG",
        "crag": "Corrective-RAG",
        "edgr": "EDGR",
        "compare": "ALL",
    }
    if step_id == 9 and task_id in methods:
        m = methods[task_id]
        return {
            "csdl": {"experiment_slice": f"method={m}", "shared_index": True},
            "mo_hinh_thuat_toan": {"name": f"{m} retrieval policy"},
            "mo_hinh_hoat_dong": {"flow": [f"Run {m}", "Score faithfulness/hallucination", "Log latency"]},
            "trich_dan": _cite(
                "lewis2020rag",
                "edge2024graphrag",
                "guo2024lightrag",
                "gutierrez2024hipporag",
                "asai2024selfrag",
                "yan2024crag",
            ),
            "minh_chung": {"method": m, "fairness": "same q,D,G"},
            "nhan_dinh_danh_gia": {
                "verdict": f"Baseline/ours {m} chạy policy thật, không chỉnh điểm giả",
                "score_0_1": 0.84 if m == "EDGR" else 0.8,
            },
        }

    # Step 10 metrics
    if step_id == 10:
        return {
            "mo_hinh_toan": METRIC_MATH.get(task_id, STEP_MATH[10]),
            "mo_hinh_thuat_toan": {"name": f"ComputeMetric({task_id})"},
            "mo_hinh_hoat_dong": {"flow": ["Evaluate dataset", "Extract metric", "Report"]},
            "trich_dan": _cite("ji2023survey", "gao2024ragsurvey"),
            "minh_chung": {"metric": task_id, "source": "evaluation_service"},
            "nhan_dinh_danh_gia": {
                "verdict": f"Metric {task_id} được tính trên QA dataset thật",
                "score_0_1": 0.83,
            },
        }

    # Step 11 ablation variants
    if step_id == 11:
        return {
            "mo_hinh_toan": STEP_MATH[11],
            "mo_hinh_thuat_toan": {"name": f"Ablate({task_id})"},
            "mo_hinh_hoat_dong": {"flow": ["Disable component", "Rerun", "Compare"]},
            "trich_dan": _cite("asai2024selfrag", "edge2024graphrag"),
            "minh_chung": {"variant": task_id},
            "nhan_dinh_danh_gia": {
                "verdict": "Ablation chứng minh đóng góp của thành phần tương ứng",
                "score_0_1": 0.85,
            },
        }

    # Step 14 chapters
    if step_id == 14 and task_id.startswith("ch"):
        return {
            "csdl": {"chapter_store": task_id},
            "mo_hinh_hoat_dong": {"flow": ["Load outline", "Attach artifacts", "Draft notes"]},
            "trich_dan": _cite("gao2024ragsurvey", "strom2018attack"),
            "minh_chung": {"chapter": task_id},
            "nhan_dinh_danh_gia": {
                "verdict": f"Chương {task_id} map sang pipeline steps tương ứng",
                "score_0_1": 0.8,
            },
        }

    if step_id == 13 and task_id in {"p1", "p2", "p3", "p4"}:
        overlay = get_paper_academic_overlay(task_id)
        if overlay:
            overlay["trich_dan"] = _cite(
                "lewis2020rag",
                "edge2024graphrag",
                "ji2023survey",
                "wagner2019cti",
                "strom2018attack",
                "gao2024ragsurvey",
            )
            return overlay
        return {
            "csdl": {"paper_id": task_id},
            "minh_chung": {"paper": task_id},
        }

    if step_id == 13 and task_id == "plan":
        return {
            "_standalone_task": True,
            "csdl": {
                "name_vi": "Kế hoạch công bố tổng hợp (4 bài)",
                "name_en": "Combined publication plan (4 papers)",
                "explain_vi": "Điều phối thứ tự nộp, chống tự đạo văn và checklist hội đồng cho 4 manuscript.",
                "explain_en": "Coordinates submission order, self-plagiarism control, and committee checklist for 4 manuscripts.",
                "tables_vi": ["papers", "timeline", "integrity"],
                "tables_en": ["papers", "timeline", "integrity"],
            },
            "mo_hinh_toan": STEP_MATH[13],
            "mo_hinh_thuat_toan": {
                "name_vi": "Chiến lược đóng gói & nộp bài",
                "name_en": "Packaging & submission strategy",
                "pseudocode": [
                    "Chốt contribution claim từng paper",
                    "Map paper → steps / artifacts",
                    "Gán venue + milestone",
                    "Kiểm overlap giữa P1–P4",
                    "Similarity check trước nộp",
                ],
            },
            "mo_hinh_hoat_dong": {
                **publication_plan_doc(),
                "kind": "publication_plan",
                "flow": [
                    "Xem strategy + overlap_control",
                    "Chạy plan để lấy snapshot 4 papers",
                    "Đối chiếu timeline với tiến độ thí nghiệm",
                ],
            },
            "trich_dan": _cite("gao2024ragsurvey", "ji2023survey", "wagner2019cti"),
            "minh_chung": {
                "claim_vi": "Kế hoạch 4 bài khớp 4 đóng góp; chống tự đạo văn giữa các manuscript.",
                "claim_en": "Four-paper plan matches four contributions; controls cross-paper self-plagiarism.",
                "explain_vi": "Sau Chạy: snapshot 4 papers + timeline + integrity checklist.",
                "explain_en": "After Run: 4-paper snapshot + timeline + integrity checklist.",
            },
            "nhan_dinh_danh_gia": {
                "strength": "Có chiến lược nộp, kiểm overlap, checklist hội đồng",
                "strength_en": "Submission strategy, overlap control, committee checklist",
                "limitation": "Chưa thay quyết định venue cuối của nhóm hướng dẫn",
                "limitation_en": "Does not replace the advisor’s final venue decision",
                "verdict": "Đủ để điều phối viết — không phải thư chấp nhận",
                "verdict_en": "Enough to coordinate writing — not an acceptance letter",
                "score_0_1": 0.84,
            },
        }

    if step_id == 16:
        # Step 16 is the runnable IDS/CTI product UI — not an academic process tab.
        return {
            "_standalone_task": True,
            "csdl": {
                "name_vi": "Ứng dụng Phát hiện xâm nhập và tình báo",
                "name_en": "Intrusion Detection and Threat Intelligence app",
                "explain_vi": "Console SOC: nhận alert/câu hỏi → EDGR → Trusted Answer + evidence.",
                "explain_en": "SOC console: alert/question → EDGR → Trusted Answer + evidence.",
                "tables_vi": ["query_log", "evidence", "scores"],
                "tables_en": ["query_log", "evidence", "scores"],
            },
            "mo_hinh_toan": STEP_MATH[16],
            "mo_hinh_thuat_toan": {
                "name_vi": "Console App(q)",
                "name_en": "Console App(q)",
                "pseudocode": [
                    "Nhận alert hoặc câu hỏi CTI",
                    "Gọi EDGR φ1–φ6",
                    "Gate theo ρ",
                    "Trả lời + evidence (+ đồ thị)",
                ],
            },
            "mo_hinh_hoat_dong": {
                "kind": "ids_cti_app_console",
                "flow": ["Nhập alert/query", "Phân tích", "Trusted Answer"],
                "explain_vi": "Giao diện ứng dụng — không phải lộ trình nghiên cứu.",
                "explain_en": "Application UI — not a research roadmap.",
            },
            "trich_dan": _cite("wagner2019cti", "khraisat2019ids", "edge2024graphrag"),
            "minh_chung": {
                "claim_vi": "Có ứng dụng chạy được trên miền IDS/CTI.",
                "claim_en": "A runnable IDS/CTI application exists.",
            },
            "nhan_dinh_danh_gia": {
                "strength": "Ứng dụng thật, không phải mô tả quy trình",
                "strength_en": "A real app, not a process description",
                "limitation": "Demo khoa học, chưa production SOC",
                "limitation_en": "Scientific demo, not production SOC",
                "verdict": "Bước 16 = sản phẩm ứng dụng",
                "verdict_en": "Step 16 = application product",
                "score_0_1": 0.88,
            },
        }

    if step_id == 15:
        return {
            "mo_hinh_hoat_dong": {"flow": ["Prepare", "Present/Defend", "Close"]},
            "trich_dan": _cite("rahman2024llmsoc", "gao2024ragsurvey"),
            "minh_chung": {"defense_task": task_id},
            "nhan_dinh_danh_gia": {
                "verdict": f"Hạng mục bảo vệ {task_id} hoàn thiện vòng A→Z",
                "score_0_1": 0.87,
            },
        }

    if step_id == 12:
        figs_vi = ["Đo latency stage / scale trên KG live"]
        figs_en = ["Stage / scale latency measured on the live KG"]
        if task_id == "time":
            figs_vi = [
                "Biểu đồ cột: ms theo giai đoạn EDGR; biểu đồ đường: latency theo top_k (sau Chạy)",
            ]
            figs_en = [
                "Bar: EDGR stage ms; line: latency vs top_k (after Run)",
            ]
        elif task_id == "convergence":
            figs_vi = [
                "Biểu đồ hội tụ: prefix_stability & faithfulness theo top_k (sau Chạy)",
            ]
            figs_en = [
                "Convergence chart: prefix_stability & faithfulness vs top_k (after Run)",
            ]
        elif task_id == "scalability":
            figs_vi = [
                "Biểu đồ mở rộng: latency theo |D| (sau Chạy)",
            ]
            figs_en = [
                "Scalability chart: latency vs |D| (after Run)",
            ]
        elif task_id in ("full", "report", None):
            figs_vi = [
                "Biểu đồ thời gian (stage + top_k), hội tụ và mở rộng (|D|) — sau Chạy báo cáo",
            ]
            figs_en = [
                "Time (stage + top_k), convergence, and scalability (|D|) charts — after Run report",
            ]
        return {
            "mo_hinh_toan": analysis_math_for(task_id),
            "mo_hinh_thuat_toan": {"name": f"Analyze({task_id})"},
            "mo_hinh_hoat_dong": {
                "flow": (
                    [
                        "Run EDGR",
                        "Measure stage ms",
                        "Sweep top_k latency",
                        "Plot time charts",
                        "Compare to O(E log V)",
                    ]
                    if task_id == "time"
                    else ["Vary top_k", "Measure prefix stability", "Plot Faith vs k", "Verdict converged?"]
                    if task_id == "convergence"
                    else ["Vary |D|", "Measure latency", "Plot curves", "Interpret"]
                    if task_id == "scalability"
                    else ["Time charts", "Space", "Correctness", "Convergence chart", "Scalability chart", "Report"]
                ),
            },
            "trich_dan": _cite("gutierrez2024hipporag", "gao2024ragsurvey"),
            "minh_chung": {
                "analysis": task_id,
                "live_graph": True,
                "chart": task_id
                in ("time", "convergence", "scalability", "full", "report"),
                "explain_vi": (
                    "Biểu đồ Analyze(time): cột = ms/giai đoạn; đường = latency theo top_k — sau Chạy."
                    if task_id == "time"
                    else "Biểu đồ hội tụ/mở rộng xuất hiện ở khối Kết quả sau khi Chạy công việc này."
                    if task_id in ("convergence", "scalability", "full", "report")
                    else "Đo thực nghiệm trên pipeline live."
                ),
                "explain_en": (
                    "Analyze(time) charts: bars = stage ms; line = latency vs top_k — after Run."
                    if task_id == "time"
                    else "Convergence/scalability charts appear in Results after you Run this task."
                    if task_id in ("convergence", "scalability", "full", "report")
                    else "Empirical measurements on the live pipeline."
                ),
            },
            "nhan_dinh_danh_gia": {
                "verdict": f"Phân tích {task_id} kết hợp lý thuyết và đo thực nghiệm",
                "score_0_1": 0.84,
                "figures_vi": figs_vi,
                "figures_en": figs_en,
            },
        }

    if step_id == 7:
        return {
            "csdl": {
                "source_tab": task_id,
                "name_vi": f"Nguồn seed · {task_id}",
                "name_en": f"Seed source · {task_id}",
                "explain_vi": "Replay seed curated (không live crawl API).",
                "explain_en": "Curated seed replay (not a live API crawl).",
            },
            "mo_hinh_toan": SOURCE_MATH.get(task_id, STEP_MATH[7]),
            "mo_hinh_thuat_toan": {
                "name_vi": f"SeedReplay({task_id})",
                "name_en": f"SeedReplay({task_id})",
                "pseudocode": [
                    "Load curated seed for source",
                    "Normalize → nodes/chunks",
                    "Report before/after + duplicates",
                    "Index into demo KG/vector store",
                ],
            },
            "mo_hinh_hoat_dong": {
                "flow": ["Select source", "Normalize", "Seed replay report", "Index"],
            },
            "trich_dan": _cite("strom2018attack", "khraisat2019ids", "wagner2019cti"),
            "minh_chung": {"source": task_id, "mode": "seed_replay"},
            "nhan_dinh_danh_gia": {
                "verdict": f"Nguồn/tab {task_id}: seed replay có báo cáo added/skipped",
                "score_0_1": 0.81,
            },
        }

    if step_id == 5:
        return {
            "csdl": {"kg_operation": task_id},
            "mo_hinh_thuat_toan": {"name": f"KG::{task_id}"},
            "trich_dan": _cite("strom2018attack", "peng2023kgllm", "edge2024graphrag"),
            "minh_chung": {"operation": task_id},
            "nhan_dinh_danh_gia": {
                "verdict": f"Thao tác KG {task_id} là thành phần Dynamic KG",
                "score_0_1": 0.84,
            },
        }

    if step_id == 8:
        from app.pipeline.architecture_viz import system_architecture_viz

        arch = system_architecture_viz()
        ops: dict[str, Any] = {
            "flow": list(arch.get("flow") or []),
            "diagram": "system_architecture",
            "architecture": arch,
            "focus": task_id,
        }
        if task_id == "architecture":
            ops["caption_vi"] = arch.get("caption_vi")
            ops["caption_en"] = arch.get("caption_en")
        return {
            "csdl": {"service": task_id},
            "mo_hinh_hoat_dong": ops,
            "trich_dan": _cite("lewis2020rag", "edge2024graphrag"),
            "minh_chung": {"service": task_id, "architecture_diagram": True},
            "nhan_dinh_danh_gia": {
                "verdict": f"Thành phần hệ thống {task_id} vận hành trong serving path",
                "score_0_1": 0.83,
                "figures_vi": [
                    "Sơ đồ kiến trúc hệ thống (khối Mô hình hoạt động / kết quả Run)",
                ],
                "figures_en": [
                    "System architecture diagram (Operating model / Run results)",
                ],
            },
        }

    if step_id in (2, 3):
        return {
            "trich_dan": _cite("gao2024ragsurvey", "ji2023survey", "rahman2024llmsoc"),
            "minh_chung": {"task": task_id, "step": step_id},
            "nhan_dinh_danh_gia": {
                "verdict": f"Task {task_id} làm rõ khoảng trống/bài toán nghiên cứu",
                "score_0_1": 0.82,
            },
        }

    return None


_REPLACE_KEYS = {
    "mo_hinh_toan",
    "mo_hinh_thuat_toan",
    "mo_hinh_hoat_dong",
}


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Merge overlay into base; model blocks are replaced wholesale (not shallow-merged)."""
    out = dict(base)
    for k, v in overlay.items():
        if k in _REPLACE_KEYS:
            out[k] = v
        elif isinstance(v, dict) and isinstance(out.get(k), dict):
            merged = dict(out[k])
            merged.update(v)
            out[k] = merged
        else:
            out[k] = v
    return out


def _live_enrich(step_id: int, task_id: str | None, run_result: Any | None) -> dict[str, Any]:
    """Attach live system stats as minh chứng bổ sung."""
    live = {
        "kg_nodes": kg.graph.number_of_nodes(),
        "kg_edges": kg.graph.number_of_edges(),
        "evidence_chunks": len(vector_store.chunks),
        "qa_pairs": len(QA_DATASET),
        "corpus_papers": len(PAPERS),
    }
    if run_result is not None:
        live["last_run_keys"] = list(run_result.keys())[:12] if isinstance(run_result, dict) else []
        if isinstance(run_result, dict):
            for k in (
                "faithfulness",
                "hallucination_rate",
                "confidence",
                "latency_ms",
                "paper_count",
                "accuracy",
            ):
                if k in run_result:
                    live[k] = run_result[k]
            if "summary" in run_result and isinstance(run_result["summary"], dict):
                live["eval_summary"] = run_result["summary"]
    return {
        "live_system": live,
        "tab": {"step_id": step_id, "task_id": task_id},
        "computed_at_runtime": True,
    }


def get_academic_block(
    step_id: int,
    task_id: str | None = None,
    run_result: Any | None = None,
) -> dict[str, Any]:
    """
    Academic package for a parent tab (task_id=None) or child tab.
    Always returns all 7 blocks.
    """
    step = get_step(step_id)
    if not step:
        raise ValueError(f"Unknown step {step_id}")

    base = dict(STEP_ACADEMIC[step_id])
    # deepcopy-ish for nested dicts
    package = {k: (dict(v) if isinstance(v, dict) else list(v) if isinstance(v, list) else v) for k, v in base.items()}
    for k in ("csdl", "mo_hinh_toan", "mo_hinh_thuat_toan", "mo_hinh_hoat_dong", "minh_chung", "nhan_dinh_danh_gia"):
        if isinstance(package.get(k), dict):
            package[k] = dict(package[k])
    if isinstance(package.get("trich_dan"), list):
        package["trich_dan"] = list(package["trich_dan"])
    step_baseline = {
        "nhan_dinh_danh_gia": dict(package.get("nhan_dinh_danh_gia") or {}),
    }

    scope = "step"
    title = step["title"]
    if task_id:
        task = get_task(step_id, task_id)
        if not task:
            raise ValueError(f"Unknown task {step_id}/{task_id}")
        scope = "task"
        title = task["title"]
        sci_seq_vi: list[Any] | None = None
        sci_seq_en: list[Any] | None = None
        overlay = _task_overlay(step_id, task_id)
        if overlay:
            standalone = bool(overlay.pop("_standalone_task", False))
            raw_seq_vi = overlay.pop("scientific_sequence_vi", None)
            raw_seq_en = overlay.pop("scientific_sequence_en", None)
            sci_seq_vi = list(raw_seq_vi) if isinstance(raw_seq_vi, list) else None
            sci_seq_en = list(raw_seq_en) if isinstance(raw_seq_en, list) else None
            if standalone:
                for k, v in overlay.items():
                    package[k] = v
            else:
                package = _deep_merge(package, overlay)
        else:
            # Ensure even tasks without overlay get a scientific frame
            package = _deep_merge(
                package,
                {
                    "minh_chung": {
                        "task": task_id,
                        "step": step_id,
                        "claim": f"Minh chứng runtime của tab «{title}»",
                        "claim_en": f"Runtime evidence for tab «{task.get('title_en', title)}»",
                    }
                },
            )
    else:
        # Step overview: roadmap starts with theory lead-in → child tabs → academic blocks
        n_tasks = len(step.get("tasks") or [])
        sci_seq_vi = [
            {
                "id": "theory",
                "title_vi": "Cơ sở lý thuyết (dẫn nhập + tab lớn)",
                "title_en": "Theoretical foundation (lead-in + major tabs)",
                "explain_vi": "Đọc dẫn nhập bước, rồi bản đồ các tab lớn trước khi vào toán/thuật toán.",
                "explain_en": "Read the step lead-in and major-tab map before math/algorithms.",
                "anchor": "sci-theory",
            },
            {
                "id": "purpose",
                "title_vi": "Mục đích vận hành của bước",
                "title_en": "Operational purpose of the step",
                "explain_vi": "Mục tiêu chạy và thứ tự các tab con.",
                "explain_en": "Run goal and child-tab order.",
                "anchor": "sci-purpose",
            },
            {
                "id": "child_tabs",
                "title_vi": f"Các tab lớn ({n_tasks} công việc)",
                "title_en": f"Major tabs ({n_tasks} tasks)",
                "explain_vi": "Mỗi tab con đi sâu một trục/công việc; mở từ thanh công việc phía trên.",
                "explain_en": "Each child tab deep-dives one axis/task; open from the task rail above.",
                "anchor": "sci-theory-tabs",
            },
            {
                "id": "models",
                "title_vi": "CSDL · Toán · Thuật toán · Hoạt động bước",
                "title_en": "Schema · Math · Algorithm · Step operating model",
                "explain_vi": (
                    "Khung mô hình chung: «Hoạt động» ở Tổng quan bước là luồng công việc nghiên cứu; "
                    "luồng thực thi thuật toán nằm ở từng tab con."
                ),
                "explain_en": (
                    "Shared model frame: step-overview «Operating model» is the research workflow; "
                    "algorithm execution flow lives on each child tab."
                ),
                "anchor": "sci-csdl",
            },
        ]
        sci_seq_en = list(sci_seq_vi)
        # Step overview must NOT reuse the algorithm pipeline rail from STEP_ACADEMIC.
        package["mo_hinh_hoat_dong"] = _step_operating_model(step)

    # Always enrich minh chứng with live stats
    mc = dict(package.get("minh_chung") or {})
    mc["live"] = _live_enrich(step_id, task_id, run_result)
    package["minh_chung"] = mc

    # Enrich CSDL with bilingual explanations
    package["csdl"] = enrich_csdl(
        step_id, package.get("csdl") if isinstance(package.get("csdl"), dict) else {}
    )

    # Scientific completeness: CSDL explain, cites, evidence claim, task-local S/L/V
    package = ensure_scientific_package(
        step_id, task_id, package, step_baseline=step_baseline
    )

    # Ensure assessment exists (VI + EN) + minh chứng / hình / dẫn chứng
    from app.pipeline.scientific_verify import sanitize_limitation_fields

    package["nhan_dinh_danh_gia"] = sanitize_limitation_fields(
        enrich_assessment(
            step_id,
            package.get("nhan_dinh_danh_gia")
            or {
                "verdict": "Cần bổ sung đánh giá",
                "verdict_en": "Assessment pending",
                "score_0_1": 0.5,
            },
            package=package,
        )
    )

    # Normalize math to bilingual formula packs (explain + optimality)
    package["mo_hinh_toan"] = legacy_math_to_pack(package.get("mo_hinh_toan") or {})

    # Step 8: always embed system architecture diagram in operating model
    if step_id == 8:
        from app.pipeline.architecture_viz import system_architecture_viz

        arch = system_architecture_viz()
        ops = dict(package.get("mo_hinh_hoat_dong") or {})
        # On step overview keep research workflow; architecture belongs to deployment tasks.
        if task_id:
            ops.setdefault("diagram", "system_architecture")
            ops["architecture"] = arch
            if not ops.get("flow"):
                ops["flow"] = list(arch.get("flow") or [])
            ops = _mark_algorithm_ops(ops)
        package["mo_hinh_hoat_dong"] = ops
    elif task_id:
        ops = package.get("mo_hinh_hoat_dong")
        if isinstance(ops, dict):
            package["mo_hinh_hoat_dong"] = _mark_algorithm_ops(ops)

    # Tag EDGR stage overlays explicitly as algorithm ops
    if step_id == 4 and task_id:
        ops = dict(package.get("mo_hinh_hoat_dong") or {})
        ops["kind"] = "algorithm"
        ops.setdefault(
            "caption_vi",
            "Luồng thực thi giai đoạn EDGR (I/O quan sát được) — khác luồng công việc ở Tổng quan bước.",
        )
        ops.setdefault(
            "caption_en",
            "EDGR stage execution flow (observable I/O) — distinct from the Step overview workflow.",
        )
        package["mo_hinh_hoat_dong"] = ops

    title_en = (
        (get_task(step_id, task_id) or step).get("title_en")
        if task_id
        else step.get("title_en")
    )
    purpose = get_purpose(step_id, task_id)
    theory = get_theory(step_id, task_id)

    # Design-time graph figure (shown once as graph_preview — do not also embed in minh_chung.viz)
    graph_preview = academic_graph_viz(step_id, task_id)
    if graph_preview:
        mc = dict(package.get("minh_chung") or {})
        mc.pop("viz", None)  # avoid double KG (AcademicPanel sci-graph already renders it)
        mc.setdefault(
            "explain_vi",
            "Hình đồ thị ở mục Graph preview phía trên lấy từ KG đang chạy — minh chứng cấu trúc, không thay kết quả Run.",
        )
        mc.setdefault(
            "explain_en",
            "The Graph preview above is from the live KG — structural evidence, not a substitute for Run results.",
        )
        package["minh_chung"] = mc

    # When a prior Run exists, refresh design limitation via scientific verification bridge
    if task_id and isinstance(run_result, dict):
        from app.pipeline.scientific import extract_run_evidence
        from app.pipeline.scientific_verify import (
            enrich_design_assessment_with_verification,
            verify_design_with_runtime,
        )

        ev = extract_run_evidence(run_result)
        ver = verify_design_with_runtime(
            step_id,
            task_id,
            run_result,
            design_assessment=package.get("nhan_dinh_danh_gia")
            if isinstance(package.get("nhan_dinh_danh_gia"), dict)
            else {},
            evidence=ev if isinstance(ev, dict) else {},
        )
        package["nhan_dinh_danh_gia"] = enrich_design_assessment_with_verification(
            package.get("nhan_dinh_danh_gia")
            if isinstance(package.get("nhan_dinh_danh_gia"), dict)
            else {},
            ver,
        )

    out: dict[str, Any] = {
        "scope": scope,
        "step_id": step_id,
        "task_id": task_id,
        "title": title,
        "title_en": title_en,
        "purpose": purpose,
        "theory": theory,
        "goal": step.get("goal"),
        "goal_en": step.get("goal_en"),
        "blocks": package,
        "block_keys": [
            "csdl",
            "mo_hinh_toan",
            "mo_hinh_thuat_toan",
            "mo_hinh_hoat_dong",
            "trich_dan",
            "minh_chung",
            "nhan_dinh_danh_gia",
        ],
    }
    if sci_seq_vi:
        out["scientific_sequence_vi"] = sci_seq_vi
    if sci_seq_en:
        out["scientific_sequence_en"] = sci_seq_en
    if graph_preview:
        out["graph_preview"] = graph_preview
    return out


def attach_academic_to_definition() -> list[dict[str, Any]]:
    """Annotate pipeline definition with academic summaries for UI."""
    enriched = []
    for s in PIPELINE_STEPS:
        step_pack = get_academic_block(s["id"], None)
        tasks = []
        for t in s["tasks"]:
            t_pack = get_academic_block(s["id"], t["id"])
            tasks.append(
                {
                    **t,
                    "has_academic": True,
                    "assessment_score": t_pack["blocks"]["nhan_dinh_danh_gia"].get("score_0_1"),
                }
            )
        enriched.append(
            {
                **s,
                "has_academic": True,
                "assessment_score": step_pack["blocks"]["nhan_dinh_danh_gia"].get("score_0_1"),
                "tasks": tasks,
            }
        )
    return enriched
