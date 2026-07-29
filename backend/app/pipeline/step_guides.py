"""Bilingual purpose, CSDL explanations, and runtime result reviews for pipeline steps."""

from __future__ import annotations

from typing import Any


STEP_PURPOSE: dict[int, dict[str, str]] = {
    1: {
        # Intent only — definition lives in theory card; formulas in math block.
        "vi": "Mục tiêu vận hành: lập bản đồ phủ tài liệu và chỉ ra giao chủ đề mỏng trước khi sang bước gap.",
        "en": "Operational goal: map literature coverage and flag thin topic intersections before the gap step.",
        "does_vi": "Chạy lần lượt các tab con: chủ đề → danh mục APA → ma trận phủ.",
        "does_en": "Run child tabs in order: topics → APA catalog → coverage matrix.",
    },
    2: {
        "vi": "Từ hạn chế trong papers, suy ra khoảng trống nghiên cứu và cơ hội đóng góp cho EDGR.",
        "en": "From paper limitations, infer research gaps and contribution opportunities for EDGR.",
        "does_vi": "Trích limitation → gắn chủ đề → xếp hạng gap → đề xuất đóng góp C1–C4.",
        "does_en": "Extract limitations → theme-tag → rank gaps → propose contributions C1–C4.",
    },
    3: {
        "vi": "Định nghĩa bài toán giảm ảo giác miền IDS/CTI: đầu vào/đầu ra, ràng buộc và tiêu chí thành công.",
        "en": "Formalize hallucination reduction for IDS/CTI: I/O, constraints, and success criteria.",
        "does_vi": "Chốt I/O → viết mô hình tối ưu → nêu mục tiêu Faith↑ / Hall↓.",
        "does_en": "Fix I/O → write optimization model → state Faith↑ / Hall↓ goals.",
    },
    4: {
        "vi": "Đề xuất và chạy EDGR — 6 giai truy hồi đồ thị động dựa trên bằng chứng trước khi sinh câu trả lời.",
        "en": "Propose and run EDGR — six evidence-driven dynamic-graph stages before answer generation.",
        "does_vi": "Entity → mở rộng KG → lọc thời gian → xếp hạng → chấm risk → chọn E* → sinh Trusted Answer.",
        "does_en": "Entity → KG expand → temporal filter → rank → risk score → select E* → Trusted Answer.",
    },
    5: {
        "vi": "Xây và cập nhật Dynamic Knowledge Graph từ đa nguồn CTI để EDGR truy hồi có cấu trúc.",
        "en": "Build and update a Dynamic Knowledge Graph from multi-source CTI for structured EDGR retrieval.",
        "does_vi": "Nạp nguồn → trích entity/quan hệ → cập nhật gia tăng → thống kê lưu trữ.",
        "does_en": "Ingest sources → extract entities/relations → incremental update → storage stats.",
    },
    6: {
        "vi": "Chấm điểm ảo giác 0–1 từ bốn nhân tố tin cậy để cổng lọc evidence trước generation.",
        "en": "Score hallucination risk 0–1 from four trust factors to gate evidence before generation.",
        "does_vi": "Tính R,F,G,S → hợp τ → ρ=1−τ → lọc theo ngưỡng θ.",
        "does_en": "Compute R,F,G,S → fuse τ → ρ=1−τ → filter by threshold θ.",
    },
    7: {
        "vi": "Chuẩn bị dữ liệu MITRE/CVE/CISA/IDS và sinh QA dataset gắn gold evidence.",
        "en": "Prepare MITRE/CVE/CISA/IDS data and build a QA dataset linked to gold evidence.",
        "does_vi": "Ingest nguồn → chuẩn hóa → sinh cặp hỏi–đáp → gắn evidence_ids.",
        "does_en": "Ingest sources → normalize → generate QA pairs → attach evidence_ids.",
    },
    8: {
        "vi": "Triển khai hệ thống end-to-end: Query → EDGR ↔ KG/Vector/LLM → Trusted Answer.",
        "en": "Deploy the end-to-end system: Query → EDGR ↔ KG/Vector/LLM → Trusted Answer.",
        "does_vi": "Ghép kiến trúc → kiểm tra từng service → chạy E2E một truy vấn CTI.",
        "does_en": "Wire architecture → smoke-test services → run one CTI query E2E.",
    },
    9: {
        "vi": "Thực nghiệm so sánh EDGR với họ RAG trên cùng query/dataset, không chỉnh điểm giả.",
        "en": "Compare EDGR with RAG-family methods on the same query/dataset without fake score tweaks.",
        "does_vi": "Chạy từng method → thu Faith/Hall/P@k/MRR/latency → bảng so sánh.",
        "does_en": "Run each method → collect Faith/Hall/P@k/MRR/latency → comparison table.",
    },
    10: {
        "vi": "Đánh giá đa metric: generation, retrieval và hệ thống trên QA dataset.",
        "en": "Multi-metric evaluation: generation, retrieval, and system cost on the QA dataset.",
        "does_vi": "Chạy evaluator → xuất Accuracy/F1/Faith/Hall/P@k/MRR/Latency/Resource.",
        "does_en": "Run evaluator → emit Accuracy/F1/Faith/Hall/P@k/MRR/Latency/Resource.",
    },
    11: {
        "vi": "Ablation: tắt từng thành phần để chứng minh đóng góp Temporal/Graph/Trust/Ranking/Scoring.",
        "en": "Ablation: disable each component to prove Temporal/Graph/Trust/Ranking/Scoring gains.",
        "does_vi": "Chạy full → chạy biến thể w/o X → đo Δ Faith/Hall → kết luận module hữu ích.",
        "does_en": "Run full → run w/o-X variants → measure Δ Faith/Hall → conclude module utility.",
    },
    12: {
        "vi": "Phân tích độ phức tạp, tính đúng, hội tụ và khả năng mở rộng của EDGR.",
        "en": "Analyze EDGR complexity, correctness, convergence, and scalability.",
        "does_vi": "Phân tích T(n)/S(n) → invariant → đo latency thực nghiệm theo quy mô.",
        "does_en": "Analyze T(n)/S(n) → invariants → measure empirical latency vs scale.",
    },
    13: {
        "vi": (
            "Đóng gói từng đóng góp EDGR thành manuscript khoa học: claim một câu, "
            "outline section có đoạn nháp định hướng, venue, artifact pipeline, "
            "và kỷ luật chống đạo văn — rồi điều phối kế hoạch 4 bài."
        ),
        "en": (
            "Package each EDGR contribution into a scientific manuscript: one-sentence claim, "
            "section outline with directional drafts, venues, pipeline artifacts, "
            "and anti-plagiarism discipline — then coordinate the four-paper plan."
        ),
        "does_vi": (
            "Đọc khung + draft từng paper → Chạy để gắn live_artifacts (metrics/KG) → "
            "áp checklist integrity → theo dõi plan chống trùng giữa các bài."
        ),
        "does_en": (
            "Read each paper’s frame + drafts → Run to attach live_artifacts (metrics/KG) → "
            "apply the integrity checklist → track the plan against cross-paper overlap."
        ),
    },
    14: {
        "vi": "Tổ chức luận án 8 chương khớp quy trình nghiên cứu A→Z.",
        "en": "Organize an 8-chapter dissertation aligned with the A→Z research process.",
        "does_vi": "Sinh mục lục → phác thảo từng chương → ước lượng khối lượng.",
        "does_en": "Generate TOC → draft each chapter → estimate word budget.",
    },
    15: {
        "vi": "Chuẩn bị bảo vệ: slide, Q&A, checklist và tổng kết hoàn thành.",
        "en": "Prepare defense: slides, Q&A, checklist, and completion summary.",
        "does_vi": "Lập checklist → rehearsal metrics → kịch bản trả lời phản biện.",
        "does_en": "Build checklist → rehearsal metrics → defense Q&A script.",
    },
    16: {
        "vi": (
            "Mở ứng dụng «Phát hiện xâm nhập và tình báo» — nhập cảnh báo/câu hỏi CTI, "
            "nhận Trusted Answer và evidence từ EDGR."
        ),
        "en": (
            "Open the «Intrusion Detection and Threat Intelligence» app — enter an alert/CTI question, "
            "get a Trusted Answer and evidence from EDGR."
        ),
        "does_vi": "Dùng console ứng dụng (không phải quy trình nghiên cứu).",
        "does_en": "Use the application console (not a research workflow).",
    },
}


CSDL_GUIDE: dict[int, dict[str, Any]] = {
    1: {
        "name_vi": "CSDL Corpus tài liệu",
        "name_en": "Literature Corpus DB",
        "explain_vi": (
            "Bảng papers + tags; live_count / min_references thể hiện quy mô khảo sát. "
            "Chi tiết APA nằm ở tab Danh mục; công thức phủ ở tab Ma trận / khối Toán."
        ),
        "explain_en": (
            "papers table + tags; live_count / min_references show survey scale. "
            "APA details live on the Catalog tab; coverage formulas on Matrix / Math."
        ),
        "role_vi": "Kho lưu trữ bibliography phục vụ Step 1–2.",
        "role_en": "Bibliography store for Steps 1–2.",
        "tables_vi": [
            "papers(id, tiêu đề, tác giả, năm, venue, tags, doi, tóm tắt, hạn chế, catalog)",
            "bibliography_view",
        ],
        "tables_en": [
            "papers(id,title,authors,year,venue,tags,doi,summary,limitations,catalog)",
            "bibliography_view",
        ],
    },
    2: {
        "name_vi": "CSDL phân tích khoảng trống",
        "name_en": "Gap Analysis Store",
        "explain_vi": "Lưu methods, limitations theo chủ đề và gaps có độ ưu tiên/severity.",
        "explain_en": "Stores methods, themed limitations, and prioritized gaps with severity.",
        "role_vi": "Biến kết quả khảo sát thành căn cứ đóng góp EDGR.",
        "role_en": "Turns survey outputs into EDGR contribution rationale.",
        "tables_vi": ["methods", "limitations(theme,paper_id,text)", "gaps(id,statement,severity)"],
        "tables_en": ["methods", "limitations(theme,paper_id,text)", "gaps(id,statement,severity)"],
    },
    3: {
        "name_vi": "CSDL đặc tả bài toán",
        "name_en": "Problem Spec Registry",
        "explain_vi": "Lưu I/O, ràng buộc CVE/ATT&CK và tiêu chí thành công (Faith/Hall).",
        "explain_en": "Stores I/O, CVE/ATT&CK constraints, and success criteria (Faith/Hall).",
        "role_vi": "Hợp đồng khoa học giữa bài toán và thuật toán EDGR.",
        "role_en": "Scientific contract between the problem and the EDGR algorithm.",
        "tables_vi": ["io_spec", "constraints", "success_criteria"],
        "tables_en": ["io_spec", "constraints", "success_criteria"],
    },
    4: {
        "name_vi": "CSDL vận hành EDGR",
        "name_en": "EDGR Runtime Store",
        "explain_vi": "Gắn KG động, vector index evidence và nhật ký stage φ1…φ6 cho mỗi truy vấn.",
        "explain_en": "Links dynamic KG, evidence vector index, and stage logs φ1…φ6 per query.",
        "role_vi": "Kho thực thi chính để sinh Trusted Answer có bằng chứng.",
        "role_en": "Primary execution store for evidence-backed Trusted Answers.",
        "tables_vi": ["queries", "stage_traces", "evidence_chunks", "kg_nodes/edges"],
        "tables_en": ["queries", "stage_traces", "evidence_chunks", "kg_nodes/edges"],
    },
    5: {
        "name_vi": "CSDL đồ thị tri thức động",
        "name_en": "Dynamic KG Store",
        "explain_vi": "Lưu đỉnh/cạnh CTI (CVE, ATT&CK, APT…) và delta cập nhật gia tăng.",
        "explain_en": "Stores CTI nodes/edges (CVE, ATT&CK, APT…) and incremental deltas.",
        "role_vi": "Xương sống cấu trúc cho mở rộng lân cận và consistency G.",
        "role_en": "Structural backbone for neighborhood expansion and consistency G.",
        "tables_vi": ["nodes(id,label,type,time)", "edges(src,rel,dst)", "updates(ΔV,ΔE)"],
        "tables_en": ["nodes(id,label,type,time)", "edges(src,rel,dst)", "updates(ΔV,ΔE)"],
    },
    6: {
        "name_vi": "CSDL điểm tin cậy / risk",
        "name_en": "Trust / Risk Score Store",
        "explain_vi": "Lưu nhân tố R,F,G,S, trust τ và risk ρ cho từng evidence chunk.",
        "explain_en": "Stores factors R,F,G,S, trust τ and risk ρ per evidence chunk.",
        "role_vi": "Cổng lọc trước generation — quyết định e có vào E* hay không.",
        "role_en": "Pre-generation gate — decides whether e enters E*.",
        "tables_vi": ["evidence_scores(e,R,F,G,S,τ,ρ)", "thresholds(θ)"],
        "tables_en": ["evidence_scores(e,R,F,G,S,τ,ρ)", "thresholds(θ)"],
    },
    7: {
        "name_vi": "CSDL CTI & QA",
        "name_en": "CTI & QA Dataset Store",
        "explain_vi": "Lưu bản ghi MITRE/CVE/CISA/IDS và cặp QA gắn gold evidence_ids.",
        "explain_en": "Stores MITRE/CVE/CISA/IDS records and QA pairs with gold evidence_ids.",
        "role_vi": "Nền tảng train/eval retrieval và faithfulness.",
        "role_en": "Foundation for retrieval and faithfulness evaluation.",
        "tables_vi": ["cti_records", "qa_pairs(q,a,evidence_ids)", "sources"],
        "tables_en": ["cti_records", "qa_pairs(q,a,evidence_ids)", "sources"],
    },
    8: {
        "name_vi": "CSDL dịch vụ hệ thống",
        "name_en": "System Services Registry",
        "explain_vi": "Mô tả endpoints KG, Vector, LLM grounded và cấu hình pipeline.",
        "explain_en": "Describes KG, Vector, grounded-LLM endpoints and pipeline config.",
        "role_vi": "Blueprint triển khai để chạy E2E ổn định.",
        "role_en": "Deployment blueprint for stable E2E runs.",
        "tables_vi": ["services", "configs", "health_checks"],
        "tables_en": ["services", "configs", "health_checks"],
    },
    9: {
        "name_vi": "CSDL sổ thực nghiệm",
        "name_en": "Experiment Ledger",
        "explain_vi": "Ghi nhận mỗi lần chạy method với metric thống nhất trên cùng q,D,G.",
        "explain_en": "Logs each method run with unified metrics on the same q,D,G.",
        "role_vi": "Bằng chứng so sánh công bằng EDGR vs baselines.",
        "role_en": "Evidence for fair EDGR vs baseline comparison.",
        "tables_vi": ["runs(method,query,faith,hall,p_at_k,mrr,latency)"],
        "tables_en": ["runs(method,query,faith,hall,p_at_k,mrr,latency)"],
    },
    10: {
        "name_vi": "CSDL kết quả đánh giá",
        "name_en": "Evaluation Results DB",
        "explain_vi": "Lưu bảng metric generation/retrieval/system cho báo cáo luận án.",
        "explain_en": "Stores generation/retrieval/system metric tables for the thesis report.",
        "role_vi": "Nguồn số liệu cho chương Experiments & Evaluation.",
        "role_en": "Numeric source for the Experiments & Evaluation chapter.",
        "tables_vi": ["metrics", "per_query_scores", "summaries"],
        "tables_en": ["metrics", "per_query_scores", "summaries"],
    },
    11: {
        "name_vi": "CSDL ablation",
        "name_en": "Ablation Ledger",
        "explain_vi": "Lưu điểm full EDGR và từng biến thể tắt module, kèm Δ metric.",
        "explain_en": "Stores full EDGR and each disabled-module variant with Δ metrics.",
        "role_vi": "Chứng minh đóng góp nhân quả của từng thành phần.",
        "role_en": "Causal evidence of each component's contribution.",
        "tables_vi": ["ablation_runs(variant,faith,hall,Δ)", "component_defs"],
        "tables_en": ["ablation_runs(variant,faith,hall,Δ)", "component_defs"],
    },
    12: {
        "name_vi": "CSDL hồ sơ phân tích",
        "name_en": "Analysis Profile Store",
        "explain_vi": "Lưu asymptotic bounds, invariant và latency thực nghiệm theo quy mô.",
        "explain_en": "Stores asymptotic bounds, invariants, and empirical latency vs scale.",
        "role_vi": "Hỗ trợ nhận định correctness/scalability.",
        "role_en": "Supports correctness/scalability claims.",
        "tables_vi": ["complexity", "invariants", "timing_profiles"],
        "tables_en": ["complexity", "invariants", "timing_profiles"],
    },
    13: {
        "name_vi": "CSDL gói công bố & kế hoạch nộp",
        "name_en": "Publication package & submission-plan store",
        "explain_vi": (
            "Lưu working title, contribution claim, abstract/section drafts, venue targets, "
            "maps_to_steps, integrity checklist, và live_artifacts sau khi Chạy "
            "(evaluation summary / KG stats / scoring weights tùy bài)."
        ),
        "explain_en": (
            "Stores working title, contribution claim, abstract/section drafts, venue targets, "
            "maps_to_steps, integrity checklist, and live_artifacts after Run "
            "(evaluation summary / KG stats / scoring weights per paper)."
        ),
        "role_vi": "Nguồn soạn manuscript và điều phối 4 bài không trùng claim.",
        "role_en": "Source for manuscript drafting and coordinating four non-overlapping claims.",
        "tables_vi": [
            "paper_outline(claim, abstract, sections, venues)",
            "section_drafts(goal, draft, must_cite, artifacts)",
            "live_artifacts",
            "publication_plan(timeline, overlap_control)",
        ],
        "tables_en": [
            "paper_outline(claim, abstract, sections, venues)",
            "section_drafts(goal, draft, must_cite, artifacts)",
            "live_artifacts",
            "publication_plan(timeline, overlap_control)",
        ],
    },
    14: {
        "name_vi": "CSDL cấu trúc luận án",
        "name_en": "Dissertation Structure Store",
        "explain_vi": "Lưu 8 chương, mục tiêu wordcount và liên kết tới bước nghiên cứu.",
        "explain_en": "Stores 8 chapters, wordcount targets, and links to research steps.",
        "role_vi": "Khung viết luận án đồng bộ với pipeline.",
        "role_en": "Writing frame aligned with the research pipeline.",
        "tables_vi": ["chapters", "toc", "word_budget"],
        "tables_en": ["chapters", "toc", "word_budget"],
    },
    15: {
        "name_vi": "CSDL chuẩn bị bảo vệ",
        "name_en": "Defense Prep Store",
        "explain_vi": "Checklist, slide outline, Q&A và mức Ready% trước bảo vệ.",
        "explain_en": "Checklist, slide outline, Q&A, and Ready% before defense.",
        "role_vi": "Theo dõi sẵn sàng bảo vệ và demo metrics.",
        "role_en": "Tracks defense readiness and demo metrics.",
        "tables_vi": ["checklist", "qa_bank", "demo_metrics"],
        "tables_en": ["checklist", "qa_bank", "demo_metrics"],
    },
    16: {
        "name_vi": "CSDL ứng dụng IDS/CTI",
        "name_en": "IDS/CTI application store",
        "explain_vi": (
            "Lưu hồ sơ sản phẩm «Phát hiện xâm nhập và tình báo», case được/thất, "
            "và nhật ký chạy thử trợ lý."
        ),
        "explain_en": (
            "Stores the «Intrusion Detection and Threat Intelligence» product profile, "
            "success/failure cases, and assistant demo logs."
        ),
        "role_vi": "Đóng gói nghiên cứu thành ứng dụng demo có biên rõ.",
        "role_en": "Packages research into a bounded demo application.",
        "tables_vi": ["app_profile", "app_success", "app_failure", "demo_run"],
        "tables_en": ["app_profile", "app_success", "app_failure", "demo_run"],
    },
}


def enrich_csdl(step_id: int, csdl: dict[str, Any] | None) -> dict[str, Any]:
    base = dict(csdl or {})
    guide = CSDL_GUIDE.get(step_id, {})
    for k, v in guide.items():
        base.setdefault(k, v)
    if "name" not in base and guide.get("name_en"):
        base["name"] = guide["name_en"]
    if "tables" not in base and guide.get("tables_en"):
        base["tables"] = guide["tables_en"]
    return base


# Task-level purpose: tab-specific intent (never paste the whole-step purpose).
TASK_PURPOSE: dict[tuple[int, str], dict[str, str]] = {
    (1, "rag"): {
        "vi": (
            "Xây dựng chuỗi lập luận khoa học cho RAG: lý thuyết → mô hình toán tổng thể "
            "(R(q), G, F/H) → thuật toán Retrieve-then-Generate ánh xạ công thức → "
            "ưu/nhược chi tiết → công thức & pseudo-code cải tiến EDGR → minh chứng corpus "
            "có ánh xạ limitation↔công thức."
        ),
        "en": (
            "Build a scientific argument chain for RAG: theory → overall math "
            "(R(q), G, F/H) → Retrieve-then-Generate mapped to formulas → "
            "detailed pros/cons → EDGR improvement formulas & pseudocode → corpus evidence "
            "with limitation↔formula mapping."
        ),
        "does_vi": (
            "Đọc lập luận + 3 công thức + thuật toán + cải tiến → Chạy analyze_topic → "
            "giải thích limitations khớp nhược điểm mô hình (đầu vào gap Step 2)."
        ),
        "does_en": (
            "Read the argument + 3 formulas + algorithm + improvements → Run analyze_topic → "
            "explain limitations matching model weaknesses (input to Step 2 gaps)."
        ),
    },
    (1, "graphrag"): {
        "vi": "Trình bày GraphRAG (toán G/R_G, thuật toán, ưu/nhược, cải tiến) và khảo sát corpus.",
        "en": "Present GraphRAG (G/R_G math, algorithm, pros/cons, improvements) and survey the corpus.",
        "does_vi": "Đối chiếu mô hình graph retrieval → chạy topic → trích hạn chế đa bước.",
        "does_en": "Review graph-retrieval model → run topic → extract multi-hop limits.",
    },
    (1, "kg"): {
        "vi": "Trình bày KG (bộ ba, N_h, ưu/nhược, cải tiến) và khảo sát papers tag=kg.",
        "en": "Present KG (triples, N_h, pros/cons, improvements) and survey kg-tagged papers.",
        "does_vi": "Đối chiếu mô hình KG → chạy topic → hạn chế update/temporal.",
        "does_en": "Review KG model → run topic → note update/temporal limits.",
    },
    (1, "hallucination"): {
        "vi": "Trình bày mô hình đo ảo giác (F,H,ρ) và khảo sát papers mitigation.",
        "en": "Present hallucination metrics (F,H,ρ) and survey mitigation papers.",
        "does_vi": "Đối chiếu F/H/ρ → chạy topic → trích hạn chế mitigation.",
        "does_en": "Review F/H/ρ → run topic → extract mitigation limits.",
    },
    (1, "cti"): {
        "vi": "Trình bày mô hình CTI (thực thể, freshness) và khảo sát ATT&CK/CVE literature.",
        "en": "Present the CTI model (entities, freshness) and survey ATT&CK/CVE literature.",
        "does_vi": "Đối chiếu E/fresh → chạy topic → hạn chế nhiễu/stale.",
        "does_en": "Review E/fresh → run topic → noise/stale limits.",
    },
    (1, "ids"): {
        "vi": "Trình bày mô hình IDS→CTI (alert, μ) và khảo sát nhu cầu diễn giải cảnh báo.",
        "en": "Present the IDS→CTI model (alert, μ) and survey alert-explanation needs.",
        "does_vi": "Đối chiếu A/μ → chạy topic → hạn chế gắn alert–tri thức.",
        "does_en": "Review A/μ → run topic → alert–knowledge linking limits.",
    },
    (1, "catalog"): {
        "vi": "Xuất danh mục ≥300 tài liệu theo chuẩn APA 7th để trích dẫn khảo sát.",
        "en": "Emit a ≥300-item reference list in APA 7th for the survey bibliography.",
        "does_vi": "Chạy list_bibliography → duyệt danh sách APA (A–Z theo tác giả).",
        "does_en": "Run list_bibliography → browse the APA list (A–Z by author).",
    },
    (1, "matrix"): {
        "vi": "Đo độ phủ C(t) và đồng xuất hiện Pair(a,b) để phát hiện giao mỏng.",
        "en": "Measure coverage C(t) and co-occurrence Pair(a,b) to find thin intersections.",
        "does_vi": "Tính ma trận paper×chủ đề → xếp Pair thấp → báo hiệu gap.",
        "does_en": "Build paper×topic matrix → rank low Pair → flag gaps.",
    },
    (2, "methods"): {
        "vi": "Liệt kê họ phương pháp baseline (RAG/GraphRAG/Self-RAG/CRAG…).",
        "en": "List baseline method families (RAG/GraphRAG/Self-RAG/CRAG…).",
        "does_vi": "Xuất inventory methods từ corpus/khảo sát.",
        "does_en": "Emit method inventory from the survey corpus.",
    },
    (2, "limitations"): {
        "vi": "Gom hạn chế đã gắn từ papers làm tiền đề gap.",
        "en": "Collect tagged paper limitations as gap premises.",
        "does_vi": "Trích limitations → nhóm theo chủ đề.",
        "does_en": "Extract limitations → group by theme.",
    },
    (2, "gaps"): {
        "vi": "Xếp hạng khoảng trống nghiên cứu có căn cứ từ limitations.",
        "en": "Rank evidenced research gaps from limitations.",
        "does_vi": "Chấm gap → sắp xếp → chọn gap trọng tâm EDGR.",
        "does_en": "Score gaps → sort → select EDGR-critical gaps.",
    },
    (2, "contrib"): {
        "vi": "Ánh xạ gap → cơ hội đóng góp C1–C4 của luận án.",
        "en": "Map gaps → thesis contribution opportunities C1–C4.",
        "does_vi": "Đề xuất đóng góp khớp từng gap đã xếp hạng.",
        "does_en": "Propose contributions aligned to ranked gaps.",
    },
    (13, "p1"): {
        "vi": "Soạn Paper 1 (EDGR): claim, abstract, 6 giai + risk gate, results/ablation.",
        "en": "Draft Paper 1 (EDGR): claim, abstract, six stages + risk gate, results/ablation.",
        "does_vi": "Đọc khung P1 → Chạy gắn evaluation_summary → điền Results.",
        "does_en": "Read P1 frame → Run to attach evaluation_summary → fill Results.",
    },
    (13, "p2"): {
        "vi": "Soạn Paper 2 (Dynamic KG): schema, ingest, ΔV·ΔE, case study — không lặp full EDGR.",
        "en": "Draft Paper 2 (Dynamic KG): schema, ingest, ΔV·ΔE, case study — do not repeat full EDGR.",
        "does_vi": "Đọc khung P2 → Chạy gắn kg_stats → viết case study.",
        "does_en": "Read P2 frame → Run to attach kg_stats → write the case study.",
    },
    (13, "p3"): {
        "vi": "Soạn Paper 3 (scoring/ρ): bốn yếu tố, ngưỡng θ, abstain; nêu rõ trọng số là hyper-parameter.",
        "en": "Draft Paper 3 (scoring/ρ): four factors, threshold θ, abstain; state weights are hyperparameters.",
        "does_vi": "Đọc khung P3 → Chạy gắn weights + sample → phân tích cổng.",
        "does_en": "Read P3 frame → Run to attach weights + sample → analyze the gate.",
    },
    (13, "p4"): {
        "vi": "Soạn Paper 4 (evaluation protocol): dataset, baseline, metric, ablation, threats — hoặc ghi chú gộp P1.",
        "en": "Draft Paper 4 (evaluation protocol): dataset, baselines, metrics, ablations, threats — or note merge into P1.",
        "does_vi": "Đọc khung P4 → Chạy gắn evaluation_summary → chốt protocol.",
        "does_en": "Read P4 frame → Run to attach evaluation_summary → lock the protocol.",
    },
    (13, "plan"): {
        "vi": (
            "Kế hoạch 4 bài: thứ tự nộp, venue, timeline, chống tự đạo văn — "
            "không phải quyết định venue cuối của thầy hướng dẫn."
        ),
        "en": (
            "Four-paper plan: submission order, venues, timeline, self-plagiarism control — "
            "not the advisor’s final venue decision."
        ),
        "does_vi": "Chạy plan → đối chiếu 4 papers + timeline + integrity với tiến độ thí nghiệm.",
        "does_en": "Run plan → align 4 papers + timeline + integrity with experiment progress.",
    },
    (16, "console"): {
        "vi": (
            "Console ứng dụng «Phát hiện xâm nhập và tình báo»: phân tích alert/câu hỏi CTI "
            "và trả Trusted Answer + evidence."
        ),
        "en": (
            "«Intrusion Detection and Threat Intelligence» app console: analyze an alert/CTI "
            "question and return a Trusted Answer + evidence."
        ),
        "does_vi": "Nhập truy vấn → Phân tích → đọc câu trả lời và bằng chứng.",
        "does_en": "Enter a query → Analyze → read the answer and evidence.",
    },
}


def get_purpose(step_id: int, task_id: str | None = None) -> dict[str, str]:
    if task_id:
        keyed = TASK_PURPOSE.get((step_id, task_id))
        if keyed:
            return dict(keyed)
        # Fallback: tab-local intent only (do NOT paste whole-step purpose).
        from app.pipeline.definition import get_task

        task = get_task(step_id, task_id) or {}
        title = task.get("title") or task_id
        title_en = task.get("title_en") or task_id
        return {
            "vi": f"Trọng tâm tab: «{title}» — thực hiện đúng công việc này.",
            "en": f"Tab focus: «{title_en}» — execute this task only.",
            "does_vi": f"Chạy `{task_id}` → đọc kết quả runtime (không lặp mục tiêu cả bước).",
            "does_en": f"Run `{task_id}` → read the runtime result (not the whole-step goal).",
        }
    return dict(
        STEP_PURPOSE.get(
            step_id,
            {
                "vi": "Thực hiện công việc nghiên cứu của bước này.",
                "en": "Execute this research step.",
                "does_vi": "Chạy các tab con theo thứ tự khoa học.",
                "does_en": "Run child tabs in scientific order.",
            },
        )
    )


def _num(d: dict[str, Any], *keys: str) -> float | None:
    for k in keys:
        if k in d and isinstance(d[k], (int, float)):
            return float(d[k])
    summary = d.get("summary")
    if isinstance(summary, dict):
        for k in keys:
            if k in summary and isinstance(summary[k], (int, float)):
                return float(summary[k])
    return None


def interpret_result(
    step_id: int,
    task_id: str,
    result: dict[str, Any] | None,
    *,
    design_assessment: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Produce scientific runtime review: explain + evidence + assessment + how-to-read."""
    from app.pipeline.scientific import extract_run_evidence
    from app.pipeline.scientific_verify import (
        apply_verification_to_review,
        verify_design_with_runtime,
    )

    r = result if isinstance(result, dict) else {}
    evidence = extract_run_evidence(r)

    faith = _num(r, "faithfulness")
    hall = _num(r, "hallucination_rate")
    conf = _num(r, "confidence")
    p_at_k = _num(r, "p_at_k")
    mrr = _num(r, "mrr")
    f1 = _num(r, "f1")
    paper_count = _num(r, "paper_count")
    total = _num(r, "total")
    latency = _num(r, "latency_ms", "avg_latency_ms")
    ready_pct = _num(r, "percent")

    # Keep explain lean: do NOT repeat AcademicPanel purpose, and do NOT list every
    # metric here (scalars/chips + ResultView tables already show numbers).
    bullets_vi: list[str] = []
    bullets_en: list[str] = []
    scalars = evidence.get("scalars") if isinstance(evidence.get("scalars"), dict) else {}
    cols = evidence.get("collections") or []

    if scalars:
        bullets_vi.append(
            "Chỉ số runtime nằm ở khối «Minh chứng» (chip) và bảng dữ liệu bên dưới — không nhắc lại từng số ở đây."
        )
        bullets_en.append(
            "Runtime metrics are in the Evidence chips and data tables below — not restated number-by-number here."
        )
    else:
        # Fallback when no scalar chips: one compact metric line only
        bits_vi: list[str] = []
        bits_en: list[str] = []
        if faith is not None:
            bits_vi.append(f"Faith={faith:.3f}")
            bits_en.append(f"Faith={faith:.3f}")
        if hall is not None:
            bits_vi.append(f"Hall={hall:.3f}")
            bits_en.append(f"Hall={hall:.3f}")
        if mrr is not None and mrr > 0:
            bits_vi.append(f"MRR={mrr:.3f}")
            bits_en.append(f"MRR={mrr:.3f}")
        if paper_count is not None:
            bits_vi.append(f"papers={int(paper_count)}")
            bits_en.append(f"papers={int(paper_count)}")
        if total is not None:
            bits_vi.append(f"n={int(total)}")
            bits_en.append(f"n={int(total)}")
        if ready_pct is not None:
            bits_vi.append(f"ready={ready_pct:.1f}%")
            bits_en.append(f"ready={ready_pct:.1f}%")
        if latency is not None:
            bits_vi.append(f"lat≈{latency:.0f}ms")
            bits_en.append(f"lat≈{latency:.0f}ms")
        if bits_vi:
            bullets_vi.append("Tóm tắt số liệu: " + " · ".join(bits_vi) + ".")
            bullets_en.append("Metric summary: " + " · ".join(bits_en) + ".")

    if cols:
        bullets_vi.append(
            "Bảng chi tiết bên dưới: "
            + ", ".join(c["field"] for c in cols[:6])
            + ("…" if len(cols) > 6 else "")
            + "."
        )
        bullets_en.append(
            "Detail tables below: "
            + ", ".join(c["field"] for c in cols[:6])
            + ("…" if len(cols) > 6 else "")
            + "."
        )

    if not bullets_vi:
        bullets_vi.append("Task đã chạy; đọc nhận định runtime và khối Kết quả bên dưới.")
        bullets_en.append("Task ran; read the runtime assessment and Results block below.")

    score = 0.55
    if faith is not None and hall is not None:
        score = max(0.05, min(0.98, 0.45 * faith + 0.45 * (1 - hall) + 0.1 * (conf or 0.5)))
    elif faith is not None:
        score = max(0.05, min(0.95, faith))
    elif paper_count is not None:
        score = max(0.4, min(0.9, 0.5 + 0.03 * min(paper_count, 15)))
    elif total is not None:
        score = max(0.45, min(0.92, 0.5 + 0.001 * min(total, 400)))
    elif evidence.get("has_evidence"):
        score = 0.68
    elif mrr is not None and mrr > 0:
        score = max(0.3, min(0.95, 0.4 + 0.5 * mrr))

    good = score >= 0.7
    mid = score >= 0.55
    if good:
        strength_vi = "Kết quả runtime hỗ trợ mục tiêu tab với chỉ số/minh chứng quan sát được."
        strength_en = "Runtime results support the tab goal with observable metrics/evidence."
        verdict_vi = "Có thể dùng làm minh chứng runtime trong luận án/demo — kèm bảng dữ liệu bên dưới."
        verdict_en = "Usable as runtime evidence in the thesis/demo — with data tables below."
    elif mid:
        strength_vi = "Có tín hiệu hữu ích khớp một phần mục tiêu tab."
        strength_en = "Useful signals partially match the tab goal."
        verdict_vi = "Cần đối chiếu thêm (baseline/ablation/CSDL) trước khi kết luận mạnh."
        verdict_en = "Cross-check further (baseline/ablation/CSDL) before a strong claim."
    else:
        strength_vi = "Task đã chạy và sinh output quan sát được (kể cả khi metric còn yếu)."
        strength_en = "Task ran and produced observable output (even if metrics are weak)."
        verdict_vi = "Metric/minh chứng còn mỏng — kiểm tra query, KG coverage hoặc dữ liệu đầu vào."
        verdict_en = "Thin metrics/evidence — check query, KG coverage, or inputs."

    # Placeholder only — overwritten by scientific_verification.assessment_patch below.
    limitation_vi = (
        "Đang đối chiếu nhận định thiết kế với kết quả runtime (checklist khoa học)."
    )
    limitation_en = (
        "Cross-checking the design assessment against runtime results (scientific checklist)."
    )

    how_vi = (
        "Cách đọc: (1) Purpose/Theory phía trên = khung thiết kế; "
        "(2) nhận định runtime + chip số liệu; (3) bảng Kết quả bên dưới."
    )
    how_en = (
        "How to read: (1) Purpose/Theory above = design frame; "
        "(2) runtime assessment + metric chips; (3) Results tables below."
    )

    review = {
        "explain_vi": " ".join(bullets_vi),
        "explain_en": " ".join(bullets_en),
        "bullets_vi": bullets_vi,
        "bullets_en": bullets_en,
        "how_to_read_vi": how_vi,
        "how_to_read_en": how_en,
        "evidence": evidence,
        "tables": evidence.get("tables") or {},
        "assessment": {
            "strength": strength_vi,
            "strength_en": strength_en,
            "limitation": limitation_vi,
            "limitation_en": limitation_en,
            "verdict": verdict_vi,
            "verdict_en": verdict_en,
            "score_0_1": round(score, 3),
            # Pointers only — do not clone explain bullets (that was a same-screen duplicate).
            "evidence_vi": [
                "Xem chip số liệu ở khối «Minh chứng» ngay trên và bảng Kết quả bên dưới.",
            ],
            "evidence_en": [
                "See metric chips in the Evidence block above and Results tables below.",
            ],
            "figures_vi": [
                "Hình/bảng runtime nằm trong khối Kết quả (không nhúng lại ở đây).",
            ],
            "figures_en": [
                "Runtime figures/tables live in the Results block (not re-embedded here).",
            ],
            "support_vi": [
                "Nhận định runtime bổ sung cho khung thiết kế phía trên — không thay Purpose/Theory.",
            ],
            "support_en": [
                "Runtime assessment complements the design frame above — it does not replace Purpose/Theory.",
            ],
            "has_support": True,
        },
    }

    verification = verify_design_with_runtime(
        step_id,
        task_id,
        r,
        design_assessment=design_assessment,
        evidence=evidence if isinstance(evidence, dict) else {},
        runtime_score=score,
    )
    return apply_verification_to_review(review, verification)
