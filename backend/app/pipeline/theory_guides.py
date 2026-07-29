"""Cơ sở lý thuyết (theoretical foundations) for every step overview and child task."""

from __future__ import annotations

from typing import Any


def _t(
    name_vi: str,
    name_en: str,
    what_vi: str,
    what_en: str,
    why_vi: str,
    why_en: str,
    ideas_vi: list[str],
    ideas_en: list[str],
    refs: str = "",
) -> dict[str, Any]:
    return {
        "name_vi": name_vi,
        "name_en": name_en,
        "what_vi": what_vi,
        "what_en": what_en,
        "why_vi": why_vi,
        "why_en": why_en,
        "ideas_vi": ideas_vi,
        "ideas_en": ideas_en,
        "refs": refs,
    }


# (step_id, task_id|None) -> theory pack
THEORY: dict[tuple[int, str | None], dict[str, Any]] = {
    # ── Step 1 ────────────────────────────────────────────────────────
    (1, None): {
        **_t(
            "Khảo sát tài liệu có hệ thống (systematic literature survey)",
            "Systematic literature survey",
            (
                "Khảo sát tài liệu ở đây được hiểu theo nghĩa học thuật: tổng hợp có cấu trúc các "
                "hướng nghiên cứu liên quan (RAG, GraphRAG, KG-LLM, hallucination, CTI, IDS/NIDS) "
                "để xác định (i) khái niệm và giả định hình thức, (ii) limitation lặp lại trong "
                "literature, và (iii) tín hiệu khoảng trống đo được (độ phủ C(t), đồng xuất hiện Pair(a,b)). "
                "Đây không phải danh mục thư mục thuần túy, mà là bước tạo bản đồ lý thuyết cho luận án."
            ),
            (
                "Literature survey here is academic: a structured synthesis of related lines "
                "(RAG, GraphRAG, KG-LLM, hallucination, CTI, IDS/NIDS) to establish (i) concepts and "
                "formal assumptions, (ii) recurring limitations in the literature, and (iii) measurable "
                "gap signals (coverage C(t), co-occurrence Pair(a,b)). It is not a bare bibliography — "
                "it builds the theoretical map for the thesis."
            ),
            (
                "Trước khi đề xuất EDGR, luận án phải chứng minh đã nắm baseline hình thức (RAG/GraphRAG) "
                "và miền ứng dụng (CTI/IDS), nếu không đóng góp sẽ bị coi là engineering ad-hoc. "
                "Khảo sát cung cấp tiền đề khoa học: mỗi module EDGR phải được phát biểu như sửa một "
                "giả định toán/thuật toán đã chỉ ra trong literature."
            ),
            (
                "Before proposing EDGR, the thesis must show mastery of formal baselines (RAG/GraphRAG) "
                "and the application domain (CTI/IDS); otherwise contributions look like ad-hoc engineering. "
                "The survey supplies the scientific premise: each EDGR module must be stated as revising "
                "a math/algorithm assumption identified in the literature."
            ),
            [
                "Sáu trục khảo sát: RAG, GraphRAG, KG, hallucination, CTI, IDS — mỗi trục có tab riêng",
                "Phép đo phủ: C(t)=|{p:t∈tags(p)}|; Pair(a,b) cho giao chủ đề mỏng → tín hiệu gap",
                "Limitation từ papers là đầu vào hình thức cho bước 2 (gap analysis), không chỉ ghi chú",
                "Catalog APA (≥300) phục vụ coverage; core papers phục vụ trích dẫn trọng tâm",
            ],
            [
                "Six survey axes: RAG, GraphRAG, KG, hallucination, CTI, IDS — each with its own tab",
                "Coverage measures: C(t)=|{p:t∈tags(p)}|; Pair(a,b) for thin intersections → gap signal",
                "Paper limitations are formal inputs to step 2 (gap analysis), not mere notes",
                "APA catalog (≥300) for coverage; core papers for key citations",
            ],
            "Lewis et al., NeurIPS 2020 (RAG); Gao et al. 2024 (RAG survey); "
            "Edge et al. 2024 (GraphRAG); Ji et al. 2023 (hallucination); "
            "Wagner et al. 2019 (CTI); Khraisat et al. 2019 (IDS)",
        ),
        "intro_vi": (
            "Dẫn nhập Bước 1 — Khảo sát tài liệu. Trước khi xác định gap hay đề xuất EDGR, luận án cần "
            "một bản đồ lý thuyết có kiểm chứng: các baseline (RAG/GraphRAG), khung tri thức (KG), "
            "đối tượng rủi ro (hallucination), và miền ứng dụng (CTI, IDS/NIDS). Tổng quan bước này "
            "giới thiệu khung chung; các tab lớn bên dưới lần lượt khảo sát từng trục và công cụ định lượng phủ."
        ),
        "intro_en": (
            "Lead-in for Step 1 — Literature review. Before gaps or EDGR, the thesis needs a testable "
            "theory map: baselines (RAG/GraphRAG), knowledge structure (KG), the risk object (hallucination), "
            "and the application domain (CTI, IDS/NIDS). This step overview frames the whole; the major "
            "child tabs then survey each axis and the quantitative coverage tools."
        ),
        "argument_vi": (
            "Lập luận trung tâm của Bước 1: (1) RAG/GraphRAG là lời giải đúng hướng cho tri thức động, "
            "nhưng (2) literature chưa giải quyết đồng thời quan hệ đa bước CTI, tín hiệu tin cậy/độ mới, "
            "và toán tử từ chối an toàn; (3) do đó khảo sát phải đo gap (C, Pair) chứ không dừng ở tóm tắt. "
            "Kết quả khảo sát là tiền đề bắt buộc để bước 2–4 đề xuất EDGR một cách có kiểm chứng."
        ),
        "argument_en": (
            "Central argument of Step 1: (1) RAG/GraphRAG correctly attack dynamic knowledge, but "
            "(2) the literature does not jointly solve multi-hop CTI relations, trust/freshness signals, "
            "and safe abstention; (3) hence the survey must measure gaps (C, Pair), not only summarize. "
            "Survey outcomes are mandatory premises for steps 2–4 to propose EDGR in a testable way."
        ),
        "assumptions_vi": [
            "Corpus khảo sát đủ phủ 6 trục; thiếu trục ⇒ bản đồ lý thuyết lệch.",
            "Limitation của paper phản ánh ràng buộc phương pháp, không chỉ thiếu dữ liệu ngẫu nhiên.",
            "C(t) và Pair(a,b) là proxy hợp lệ cho độ sâu/giao chủ đề trong giai đoạn survey.",
        ],
        "assumptions_en": [
            "The survey corpus covers all six axes; a missing axis skews the theory map.",
            "Paper limitations reflect method constraints, not only random data gaps.",
            "C(t) and Pair(a,b) are valid proxies for topic depth/intersection at survey time.",
        ],
    },
    (1, "rag"): {
        **_t(
            "RAG — Retrieval-Augmented Generation",
            "RAG — Retrieval-Augmented Generation",
            (
                "RAG (Lewis et al., NeurIPS 2020) là mô hình trả lời có điều kiện trên bằng chứng ngoài: "
                "retriever xây tập R(q) từ kho tài liệu D (bộ nhớ phi tham số), generator G sinh câu trả lời a "
                "điều kiện trên (q, R(q)) (bộ nhớ tham số). Mục tiêu khoa học là giảm lỗi kiến thức và bịa nguồn "
                "so với LLM thuần bằng cách neo a vào R(q), đo bằng faithfulness F và hallucination rate H≈1−F."
            ),
            (
                "RAG (Lewis et al., NeurIPS 2020) is evidence-conditioned answering: "
                "a retriever builds R(q) from document store D (non-parametric memory), and a generator G produces "
                "answer a conditioned on (q, R(q)) (parametric memory). The scientific goal is to reduce knowledge "
                "errors and fabricated sources versus a bare LLM by grounding a in R(q), measured by faithfulness F "
                "and hallucination rate H≈1−F."
            ),
            (
                "RAG là baseline hình thức bắt buộc của luận án: mọi đóng góp EDGR (đồ thị động, lọc thời gian, "
                "xếp hạng đa tín hiệu, cổng risk) phải được phát biểu như sửa giả định toán/thuật toán của RAG, "
                "và phải vượt RAG trên cùng metric F/H/P@k trong miền IDS/CTI — nơi một claim sai về CVE/TTP "
                "có chi phí vận hành cao."
            ),
            (
                "RAG is the thesis’s mandatory formal baseline: every EDGR contribution (dynamic graph, temporal "
                "filter, multi-signal ranking, risk gate) must be stated as a revision of RAG’s math/algorithm "
                "assumptions, and must beat RAG on the same F/H/P@k metrics in IDS/CTI — where one wrong CVE/TTP "
                "claim is operationally costly."
            ),
            [
                "Ba trụ cột toán: R(q)=TopK sim(q,d); a=G(q,R(q)); F(a,R) với H≈1−F — chi tiết trong khối Mô hình toán.",
                "Thuật toán cổ điển Retrieve-then-Generate (BM25/dense + LLM) ánh xạ 1–1 sang các công thức trên.",
                "Ưu điểm cấu trúc: cập nhật D không fine-tune θ_G; baseline đo được; module hóa retriever/generator.",
                "Nhược điểm cấu trúc: sim phẳng (không cạnh quan hệ); thiếu trust/fresh trong R; F hậu kiểm, không có reject.",
                "Cải tiến hình thức → EDGR: R_G=Expand; R_τ=TemporalFilter; s(e) đa tín hiệu; emit chỉ khi ρ<θ.",
            ],
            [
                "Three math pillars: R(q)=TopK sim(q,d); a=G(q,R(q)); F(a,R) with H≈1−F — details in the Math model block.",
                "Classic Retrieve-then-Generate (BM25/dense + LLM) maps 1–1 onto those formulas.",
                "Structural pros: update D without finetuning θ_G; measurable baseline; modular retriever/generator.",
                "Structural cons: flat sim (no relation edges); no trust/fresh in R; post-hoc F, no reject operator.",
                "Formal path → EDGR: R_G=Expand; R_τ=TemporalFilter; multi-signal s(e); emit only if ρ<θ.",
            ],
            "Lewis et al., NeurIPS 2020 (RAG); Gao et al. 2024 (RAG survey); Ji et al. 2023 (hallucination)",
        ),
        "argument_vi": (
            "Lập luận trung tâm của tab: (1) RAG là lời giải đúng hướng cho tri thức động, nhưng (2) giả định "
            "“quan hệ CTI nằm trong độ gần đoạn văn” là sai trong IDS/CTI đa bước, và (3) thiếu toán tử từ chối "
            "làm F hậu kiểm không đủ an toàn. Do đó cần thuật toán mới (EDGR) giữ G nhưng đổi R và thêm ρ-gate — "
            "không dừng ở tinh chỉnh siêu tham số của RAG."
        ),
        "argument_en": (
            "Central argument of this tab: (1) RAG correctly attacks dynamic knowledge, but (2) the assumption that "
            "“CTI relations live in passage proximity” fails on multi-hop IDS/CTI, and (3) missing abstention makes "
            "post-hoc F unsafe. Hence a new algorithm (EDGR) should keep G but change R and add a ρ-gate — "
            "not merely retune RAG hyperparameters."
        ),
        "assumptions_vi": [
            "Kho D chứa đoạn văn đủ để trả lời; quan hệ CTI đa bước không bắt buộc nằm trên cạnh đồ thị.",
            "sim(q,d) (BM25/dense) là đủ gần đúng cho R(q) trong miền tổng quát.",
            "Faithfulness F đo được sau generation là proxy an toàn — chưa có toán tử reject trước emit.",
        ],
        "assumptions_en": [
            "Store D holds passages sufficient to answer; multi-hop CTI relations need not live on graph edges.",
            "sim(q,d) (BM25/dense) is an adequate proxy for R(q) in the general domain.",
            "Post-generation faithfulness F is a safety proxy — no reject operator before emit.",
        ],
    },
    (1, "graphrag"): {
        **_t(
            "GraphRAG — truy hồi có cấu trúc đồ thị",
            "GraphRAG — structure-aware retrieval",
            (
                "GraphRAG (Edge et al., 2024) thay giả định “đoạn văn phẳng đủ mang quan hệ” bằng đồ thị thực thể/"
                "cộng đồng: corpus → KG → phân cộng đồng / đường đi → retrieval và tóm tắt theo cấu trúc. "
                "Về hình thức, tập ứng viên không chỉ R(q)=TopK sim(q,d) mà còn R_G(q) phụ thuộc lân cận/cộng đồng "
                "trên G=(V,E). Đây là bước trung gian học thuật giữa RAG phẳng và EDGR (đồ thị động + tín hiệu tin cậy)."
            ),
            (
                "GraphRAG (Edge et al., 2024) replaces the “flat passages carry relations” assumption with an "
                "entity/community graph: corpus → KG → communities/paths → structure-aware retrieval and summarization. "
                "Formally, candidates are not only R(q)=TopK sim(q,d) but also R_G(q) depending on neighborhoods/"
                "communities on G=(V,E). It is the scholarly bridge between flat RAG and EDGR (dynamic graph + trust)."
            ),
            (
                "Trong CTI (CVE–APT–TTP), quan hệ đa bước là đối tượng khoa học chính; GraphRAG chứng minh đồ thị "
                "cải thiện multi-hop so với RAG. EDGR kế thừa Expand trên KG nhưng bổ sung giả định còn thiếu: "
                "đồ thị động theo thời gian, ranking đa tín hiệu, và ρ-gate trước generation."
            ),
            (
                "In CTI (CVE–APT–TTP), multi-hop relations are the core scientific object; GraphRAG shows graphs "
                "improve multi-hop over RAG. EDGR inherits Expand on the KG but adds missing assumptions: "
                "a time-varying graph, multi-signal ranking, and a ρ-gate before generation."
            ),
            [
                "Giả định hình thức: quan hệ nằm trên cạnh/cộng đồng của G, không chỉ trong độ gần đoạn văn",
                "Thuật toán điển hình: extract entities → cluster/community → retrieve + map-reduce summary",
                "Đối chứng liên quan: LightRAG (dual-level), HippoRAG (PPR) — cùng họ graph-augmented",
                "Khoảng trống so với EDGR: thường tĩnh theo snapshot; thiếu trust/fresh và toán tử reject",
            ],
            [
                "Formal assumption: relations live on edges/communities of G, not only passage proximity",
                "Typical algorithm: extract entities → cluster/community → retrieve + map-reduce summary",
                "Related controls: LightRAG (dual-level), HippoRAG (PPR) — same graph-augmented family",
                "Gap vs EDGR: often snapshot-static; lacks trust/fresh and a reject operator",
            ],
            "Edge et al. 2024; Guo et al. 2024 (LightRAG); Gutiérrez et al. 2024 (HippoRAG)",
        ),
        "argument_vi": (
            "Lập luận: GraphRAG đúng hướng khi đưa cấu trúc vào R, nhưng (1) KG thường coi là gần tĩnh, "
            "(2) ranking ít gắn trust/freshness CTI, (3) vẫn thiếu cổng risk trước emit. Do đó GraphRAG là "
            "baseline graph bắt buộc, chưa phải lời giải đủ cho IDS/CTI grounded."
        ),
        "argument_en": (
            "Argument: GraphRAG correctly puts structure into R, but (1) the KG is often near-static, "
            "(2) ranking rarely ties to CTI trust/freshness, and (3) a pre-emit risk gate is still missing. "
            "Hence GraphRAG is a mandatory graph baseline, not yet a sufficient IDS/CTI grounded solution."
        ),
        "assumptions_vi": [
            "KG/cộng đồng xây từ corpus phản ánh đủ quan hệ cần cho multi-hop.",
            "Snapshot G đủ ổn định trong cửa sổ đánh giá (chưa nhấn mạnh ΔV,ΔE theo thời gian).",
            "Tóm tắt cộng đồng không làm mất ràng buộc evidence có thể kiểm chứng.",
        ],
        "assumptions_en": [
            "The corpus-built KG/communities capture relations needed for multi-hop.",
            "Snapshot G is stable enough in the evaluation window (ΔV,ΔE over time under-emphasized).",
            "Community summaries preserve verifiable evidence constraints.",
        ],
    },
    (1, "kg"): _t(
        "Đồ thị tri thức (Knowledge Graph)",
        "Knowledge Graph (KG)",
        "KG biểu diễn tri thức dạng đỉnh–cạnh–quan hệ (u −[r]→ v), hỗ trợ suy luận cấu trúc và truy vấn quan hệ.",
        "A KG represents knowledge as nodes–edges–relations (u −[r]→ v), enabling structural reasoning and relational queries.",
        "CTI vốn mang tính quan hệ (actor–malware–CVE–technique); KG là xương sống của EDGR.",
        "CTI is inherently relational (actor–malware–CVE–technique); the KG is EDGR’s backbone.",
        [
            "Thành phần: entities, relations, attributes, thời gian (temporal KG)",
            "Cập nhật gia tăng quan trọng với threat intel thay đổi theo thời gian",
            "Consistency trên KG dùng làm tín hiệu chống bịa quan hệ",
        ],
        [
            "Components: entities, relations, attributes, time (temporal KG)",
            "Incremental updates matter as threat intel changes over time",
            "KG consistency is a signal against fabricated relations",
        ],
        "Peng et al.; Wagner et al. 2019 (CTI sharing)",
    ),
    (1, "hallucination"): {
        **_t(
            "Ảo giác LLM (Hallucination)",
            "LLM Hallucination",
            (
                "Theo literature (Ji et al., 2023), hallucination là hiện tượng mô hình sinh nội dung "
                "không được bằng chứng hỗ trợ: intrinsic (mâu thuẫn nội tại) hoặc extrinsic (bịa sự kiện/"
                "định danh ngoài nguồn). Trong khung đánh giá grounded QA, faithfulness F đo mức a được "
                "hỗ trợ bởi R; hallucination rate thường lấy proxy H≈1−F. Đây là đối tượng khoa học trung tâm "
                "của luận án — không chỉ lỗi UX."
            ),
            (
                "Per the literature (Ji et al., 2023), hallucination is generating content unsupported by "
                "evidence: intrinsic (self-contradiction) or extrinsic (fabricated facts/IDs outside sources). "
                "In grounded QA evaluation, faithfulness F measures how much a is supported by R; hallucination "
                "rate often uses proxy H≈1−F. This is the thesis’s central scientific object — not merely a UX bug."
            ),
            (
                "Trong IDS/CTI, bịa CVE/ATT&CK/TTP có chi phí vận hành cao. EDGR đặt giả thuyết: kết hợp "
                "retrieval cấu trúc + tín hiệu tin cậy/độ mới + toán tử reject (ρ<θ) giảm H so với RAG/GraphRAG "
                "trên cùng bộ câu hỏi — giả thuyết phải được kiểm chứng ở bước đánh giá."
            ),
            (
                "In IDS/CTI, fabricated CVE/ATT&CK/TTP IDs are operationally costly. EDGR hypothesizes that "
                "structure-aware retrieval + trust/freshness + a reject operator (ρ<θ) lowers H versus "
                "RAG/GraphRAG on the same questions — a hypothesis to be tested in evaluation steps."
            ),
            [
                "Phân loại học thuật: intrinsic vs extrinsic; factuality vs faithfulness",
                "Giảm thiểu trong literature: retrieval, grounding, self-critique, corrective loops",
                "EDGR: thêm risk score ρ và abstain — biến an toàn thành toán tử trước emit",
                "Metric bắt buộc: F↑, H↓, kèm P@k/MRR để tách lỗi retrieval khỏi lỗi generation",
            ],
            [
                "Academic taxonomy: intrinsic vs extrinsic; factuality vs faithfulness",
                "Mitigations in literature: retrieval, grounding, self-critique, corrective loops",
                "EDGR: adds risk score ρ and abstain — safety as a pre-emit operator",
                "Required metrics: F↑, H↓, plus P@k/MRR to separate retrieval vs generation error",
            ],
            "Ji et al. 2023; Huang et al. 2025; Lewis et al. 2020",
        ),
        "argument_vi": (
            "Lập luận: nếu chỉ tối ưu fluency của LLM thì H vẫn cao trên CTI; cần ràng buộc evidence "
            "và cổng từ chối. Survey tab này cố định định nghĩa F/H trước khi EDGR đề xuất giải pháp."
        ),
        "argument_en": (
            "Argument: optimizing LLM fluency alone leaves H high on CTI; evidence constraints and "
            "abstention are required. This survey tab fixes the F/H definitions before EDGR proposes a fix."
        ),
        "assumptions_vi": [
            "F và H đo được ổn định trên bộ QA có gold evidence_ids.",
            "Bịa định danh (CVE/TTP) thuộc lớp extrinsic hallucination cần phạt nặng trong đánh giá.",
        ],
        "assumptions_en": [
            "F and H are stably measurable on a QA set with gold evidence_ids.",
            "Fabricated identifiers (CVE/TTP) are extrinsic hallucinations that must be heavily penalized.",
        ],
    },
    (1, "cti"): _t(
        "Tình báo mối đe dọa mạng (CTI)",
        "Cyber Threat Intelligence (CTI)",
        "CTI là tri thức có cấu trúc về mối đe dọa: actor, malware, vulnerability, TTP — thường chuẩn hóa bằng ATT&CK, STIX/TAXII, CVE/CWE.",
        "CTI is structured knowledge about threats: actors, malware, vulnerabilities, TTPs — often standardized via ATT&CK, STIX/TAXII, CVE/CWE.",
        "Miền ứng dụng của luận án; đòi hỏi độ tin cậy nguồn và tính thời gian của evidence.",
        "The thesis application domain; requires source reliability and evidence temporality.",
        [
            "Nguồn: NVD, MITRE, CISA KEV, threat feeds, báo cáo",
            "Thách thức: nhiễu OSINT, trùng lặp, stale intel",
            "LLM+CTI dễ bịa định danh nếu không có cổng evidence",
        ],
        [
            "Sources: NVD, MITRE, CISA KEV, threat feeds, reports",
            "Challenges: OSINT noise, duplication, stale intel",
            "LLM+CTI easily fabricates IDs without an evidence gate",
        ],
        "Wagner et al. 2019; Strom et al. 2018 (ATT&CK)",
    ),
    (1, "ids"): _t(
        "IDS / NIDS — Phát hiện xâm nhập",
        "IDS / NIDS — Intrusion Detection",
        "IDS/NIDS giám sát hệ thống/mạng để phát hiện tấn công hoặc bất thường (signature, anomaly, ML-based).",
        "IDS/NIDS monitors systems/networks to detect attacks or anomalies (signature, anomaly, ML-based).",
        "Analyst cần giải thích alert bằng CTI tin cậy; EDGR hỗ trợ QA grounded cho SOC/IDS.",
        "Analysts need trusted CTI explanations of alerts; EDGR supports grounded QA for SOC/IDS.",
        [
            "Dataset điển hình: CIC-IDS, UNSW-NB15, KDD-family",
            "Đầu ra IDS thường là alert — cần tri thức ngoài để diễn giải",
            "Kết hợp IDS telemetry + CTI KG là kịch bản thực tiễn của EDGR",
        ],
        [
            "Typical datasets: CIC-IDS, UNSW-NB15, KDD-family",
            "IDS outputs are often alerts — external knowledge is needed to interpret them",
            "Combining IDS telemetry + CTI KG is EDGR’s practical scenario",
        ],
        "Khraisat et al. 2019; Ring et al. 2019",
    ),
    (1, "catalog"): _t(
        "Danh mục tài liệu tham khảo",
        "Reference catalog",
        "Danh mục bibliography dùng làm khung trích dẫn khảo sát; định dạng xuất là APA 7th.",
        "A bibliography catalog used as the survey citation frame; export format is APA 7th.",
        "Cần quy mô đủ lớn để phủ sáu trục — không chỉ vài paper tiêu biểu.",
        "Needs enough scale to cover six axes — not only a few flagship papers.",
        [
            "Core = trích dẫn trọng tâm; Extended = phủ rộng",
            "Sắp xếp A–Z theo tác giả (chuẩn References)",
            "Số liệu đếm thuộc khối CSDL/kết quả chạy — không nhắc lại ở đây",
        ],
        [
            "Core = key citations; Extended = broad coverage",
            "Sort A–Z by author (References convention)",
            "Counts belong in CSDL/run results — not restated here",
        ],
    ),
    (1, "matrix"): _t(
        "Ma trận khảo sát (Coverage Matrix)",
        "Coverage matrix",
        "Công cụ định lượng độ phủ chủ đề và đồng xuất hiện giữa các trục khảo sát.",
        "A quantitative tool for topic coverage and co-occurrence across survey axes.",
        "Cung cấp bằng chứng số cho khoảng trống (ví dụ giao CTI–Graph–Hallucination).",
        "Provides numeric evidence for gaps (e.g. CTI–Graph–Hallucination intersection).",
        [
            "Ô ma trận đánh dấu paper thuộc chủ đề nào",
            "Giao mỏng = tín hiệu gap (chi tiết công thức ở khối Toán)",
            "Đầu ra chuyển sang bước 2 Identify Gaps",
        ],
        [
            "Matrix cells mark which topics a paper covers",
            "Thin intersections signal gaps (formulas live in the Math block)",
            "Output feeds step 2 Identify Gaps",
        ],
    ),
    # ── Step 2 ────────────────────────────────────────────────────────
    (2, None): _t(
        "Xác định khoảng trống",
        "Identify gaps",
        "Từ hạn chế của phương pháp hiện có, suy ra gap và cơ hội đóng góp.",
        "From limitations of existing methods, infer gaps and contribution opportunities.",
        "Bảo đảm EDGR giải quyết khoảng trống có căn cứ, không đề xuất trùng lặp.",
        "Ensures EDGR addresses evidenced gaps rather than redundant proposals.",
        ["Inventory methods", "Theme limitations", "Rank gaps", "Map contributions"],
        ["Inventory methods", "Theme limitations", "Rank gaps", "Map contributions"],
    ),
    (2, "methods"): _t(
        "Phương pháp hiện có",
        "Existing methods",
        "Liệt kê các họ phương pháp RAG/GraphRAG/Self-RAG/CRAG… đã khảo sát.",
        "List surveyed method families: RAG/GraphRAG/Self-RAG/CRAG…",
        "Làm khung so sánh và baseline cho bước thực nghiệm.",
        "Frames comparison and baselines for experiments.",
        ["Phân họ theo cơ chế retrieval/critique", "Gắn paper đại diện"],
        ["Family by retrieval/critique mechanism", "Attach representative papers"],
    ),
    (2, "limitations"): _t(
        "Hạn chế",
        "Limitations",
        "Tổng hợp limitation từ papers theo theme (temporal, trust, CTI, graph).",
        "Aggregate paper limitations by theme (temporal, trust, CTI, graph).",
        "Limitation có theme mới suy ra được gap có cấu trúc.",
        "Themed limitations enable structured gap inference.",
        ["Tag theme", "Đếm tần suất", "Ưu tiên theme liên quan EDGR"],
        ["Theme-tag", "Count frequency", "Prioritize EDGR-relevant themes"],
    ),
    (2, "gaps"): _t(
        "Khoảng trống nghiên cứu",
        "Research gaps",
        "Các khoảng trống G1…Gk suy từ giao mỏng + limitation (vd. thiếu trust gate trên CTI graph).",
        "Gaps G1…Gk inferred from thin intersections + limitations (e.g. missing trust gate on CTI graphs).",
        "Là luận điểm then chốt biện minh cho EDGR.",
        "The key argument justifying EDGR.",
        ["Gắn severity", "Liên kết bằng chứng bibliographic"],
        ["Attach severity", "Link bibliographic evidence"],
    ),
    (2, "contrib"): _t(
        "Cơ hội đóng góp",
        "Contribution opportunities",
        "Chuyển gap thành đóng góp cụ thể C1…C4 (algorithm, KG, scoring, evaluation).",
        "Turn gaps into concrete contributions C1…C4 (algorithm, KG, scoring, evaluation).",
        "Định hướng nội dung đóng góp chính của luận án.",
        "Guides the dissertation’s main contribution content.",
        ["C1 EDGR pipeline", "C2 Dynamic KG", "C3 Hallucination scoring", "C4 Evaluation"],
        ["C1 EDGR pipeline", "C2 Dynamic KG", "C3 Hallucination scoring", "C4 Evaluation"],
    ),
    # ── Step 3 ────────────────────────────────────────────────────────
    (3, None): _t(
        "Xây dựng bài toán",
        "Problem definition",
        "Formal hóa bài toán giảm hallucination miền IDS/CTI: I/O, ràng buộc, tiêu chí tối ưu.",
        "Formalize hallucination reduction for IDS/CTI: I/O, constraints, optimization criteria.",
        "Biến gap thành bài toán toán học/thuật toán có thể giải bằng EDGR.",
        "Turns gaps into a mathematical/algorithmic problem solvable by EDGR.",
        ["Định nghĩa I/O", "Hàm mục tiêu Faith↑ Hall↓", "Ràng buộc CVE/ATT&CK"],
        ["Define I/O", "Objective Faith↑ Hall↓", "CVE/ATT&CK constraints"],
    ),
    (3, "io"): _t(
        "Đầu vào / đầu ra",
        "Input / Output",
        "Input: query CTI/IDS, KG, corpus; Output: Trusted Answer + evidence E* + risk scores.",
        "Input: CTI/IDS query, KG, corpus; Output: Trusted Answer + evidence E* + risk scores.",
        "Chốt biên hệ thống trước khi thiết kế thuật toán.",
        "Fixes system boundaries before algorithm design.",
        ["q, G_t, D → a, E*, ρ"],
        ["q, G_t, D → a, E*, ρ"],
    ),
    (3, "model"): _t(
        "Mô hình hóa bài toán",
        "Problem modeling",
        "Viết bài toán tối ưu chọn evidence tin cậy dưới ràng buộc risk và top-k.",
        "Write the optimization problem of selecting trusted evidence under risk and top-k constraints.",
        "Cầu nối giữa lý thuyết và thuật toán EDGR.",
        "Bridge between theory and the EDGR algorithm.",
        ["max Faith(a,E*)", "s.t. ρ(e)≤θ, |E*|≤k"],
        ["max Faith(a,E*)", "s.t. ρ(e)≤θ, |E*|≤k"],
    ),
    (3, "goal"): _t(
        "Mục tiêu giảm ảo giác",
        "Hallucination-reduction goal",
        "Mục tiêu: tăng faithfulness, giảm hallucination rate, giữ P@k/MRR và latency chấp nhận được.",
        "Goal: raise faithfulness, lower hallucination rate, keep acceptable P@k/MRR and latency.",
        "Là tiêu chí thành công cho evaluation và ablation.",
        "Success criteria for evaluation and ablation.",
        ["Faith↑", "Hall↓", "Retrieval không sụt mạnh"],
        ["Faith↑", "Hall↓", "Retrieval must not collapse"],
    ),
    # ── Step 4 EDGR ───────────────────────────────────────────────────
    (4, None): _t(
        "Thuật toán EDGR",
        "EDGR algorithm",
        "EDGR = Evidence-Driven Dynamic Graph Retrieval: 6 giai từ entity đến Trusted Answer có cổng risk.",
        "EDGR = Evidence-Driven Dynamic Graph Retrieval: six stages from entities to a risk-gated Trusted Answer.",
        "Đóng góp chính của luận án — khác RAG phẳng bởi graph động + trust gate.",
        "Main thesis contribution — unlike flat RAG via dynamic graph + trust gate.",
        ["φ1…φ6", "E* = TopK({e: ρ(e)≤θ})", "a = Gen(q,E*)"],
        ["φ1…φ6", "E* = TopK({e: ρ(e)≤θ})", "a = Gen(q,E*)"],
    ),
    (4, "s1"): _t(
        "Trích entity từ truy vấn",
        "Query entity extraction",
        "Nhận diện seed entities (CVE, Txxxx, nhãn KG) từ câu hỏi để neo truy hồi.",
        "Recognize seed entities (CVE, Txxxx, KG labels) from the query to anchor retrieval.",
        "Không có seed đúng thì graph expansion lệch hướng.",
        "Without correct seeds, graph expansion drifts.",
        ["Regex CTI IDs", "Dictionary match", "S ⊆ V"],
        ["Regex CTI IDs", "Dictionary match", "S ⊆ V"],
    ),
    (4, "s2"): _t(
        "Mở rộng đa bước thích ứng",
        "Adaptive multi-step expansion",
        "BFS/h-hop quanh seed với h thích ứng theo |S| để lấy ngữ cảnh quan hệ.",
        "BFS/h-hop around seeds with adaptive h based on |S| to gather relational context.",
        "Bổ sung quan hệ CTI mà retrieval văn bản dễ bỏ sót.",
        "Adds CTI relations that text retrieval often misses.",
        ["h=1 nếu |S|>2 else 2", "Giới hạn max_nodes"],
        ["h=1 if |S|>2 else 2", "Cap max_nodes"],
    ),
    (4, "s3"): _t(
        "Lọc thời gian",
        "Temporal filtering",
        "Loại hàng xóm quá cũ theo cửa sổ W nhưng luôn giữ seed từ query (kể cả CVE lịch sử).",
        "Drop neighbors older than window W but always keep query seeds (including historical CVEs).",
        "CTI vừa cần độ mới vừa không được mất neo lịch sử.",
        "CTI needs freshness without losing historical anchors.",
        ["N' = S ∪ {v: age(v)≤W}", "Seeds never dropped"],
        ["N' = S ∪ {v: age(v)≤W}", "Seeds never dropped"],
    ),
    (4, "s4"): _t(
        "Xếp hạng bằng chứng",
        "Evidence ranking",
        "Hợp nhất điểm vector (TF-IDF/sim) với thưởng chồng entity đồ thị.",
        "Fuse vector scores (TF-IDF/sim) with a graph-entity overlap bonus.",
        "Ưu tiên chunk vừa giống query vừa gắn KG.",
        "Prefer chunks that match the query and attach to the KG.",
        ["score(d)=sim(q,d)+λ|Ent(d)∩N'|"],
        ["score(d)=sim(q,d)+λ|Ent(d)∩N'|"],
    ),
    (4, "s5"): _t(
        "Chấm điểm ảo giác / risk",
        "Hallucination / risk scoring",
        "Tính ρ(e)=1−τ(e) từ R,F,G,S để ước lượng rủi ro dùng evidence.",
        "Compute ρ(e)=1−τ(e) from R,F,G,S to estimate evidence risk.",
        "Cổng lý thuyết trước generation — khác Self-RAG (critique nội tại).",
        "Theoretical gate before generation — unlike Self-RAG (internal critique).",
        ["τ=0.3R+0.2F+0.25G+0.25S", "ρ=1−τ"],
        ["τ=0.3R+0.2F+0.25G+0.25S", "ρ=1−τ"],
    ),
    (4, "s6"): _t(
        "Chọn evidence tin cậy & sinh câu trả lời",
        "Trusted evidence selection & generation",
        "Giữ E*=TopK({e:ρ≤θ}) rồi sinh câu trả lời grounded trên E*.",
        "Keep E*=TopK({e:ρ≤θ}) then generate a grounded answer on E*.",
        "Đảm bảo output bám bằng chứng đã qua cổng risk.",
        "Ensures the output sticks to risk-gated evidence.",
        ["Threshold θ", "Entity-overlap tie-break", "Grounded Gen"],
        ["Threshold θ", "Entity-overlap tie-break", "Grounded Gen"],
    ),
    (4, "full"): _t(
        "Pipeline EDGR đầy đủ",
        "Full EDGR pipeline",
        "Chạy end-to-end φ1…φ6 trên một query CTI và trả metrics Faith/Hall.",
        "Run end-to-end φ1…φ6 on a CTI query and return Faith/Hall metrics.",
        "Minh chứng runtime cho đóng góp thuật toán.",
        "Runtime evidence for the algorithmic contribution.",
        ["Một API call", "Full stage trace"],
        ["Single API call", "Full stage trace"],
    ),
    # ── Step 5 ────────────────────────────────────────────────────────
    (5, None): _t(
        "Dynamic Knowledge Graph",
        "Dynamic Knowledge Graph",
        "KG cập nhật theo thời gian G_{t+1}=G_t⊕(ΔV,ΔE) từ đa nguồn CTI.",
        "A time-evolving KG G_{t+1}=G_t⊕(ΔV,ΔE) from multi-source CTI.",
        "Threat intel thay đổi; KG tĩnh làm retrieval lỗi thời.",
        "Threat intel changes; a static KG makes retrieval stale.",
        ["Incremental update", "Đa nguồn", "Schema CTI"],
        ["Incremental update", "Multi-source", "CTI schema"],
    ),
    (5, "sources"): _t(
        "Nguồn dữ liệu",
        "Data sources",
        "MITRE, NVD/CVE, CISA, feeds, báo cáo — đầu vào xây KG.",
        "MITRE, NVD/CVE, CISA, feeds, reports — inputs to build the KG.",
        "Độ tin cậy nguồn ảnh hưởng R(e) ở bước scoring.",
        "Source reliability affects R(e) in scoring.",
        ["Nguồn chuẩn vs OSINT"],
        ["Authoritative vs OSINT sources"],
    ),
    (5, "extract"): _t(
        "Trích entity & quan hệ",
        "Entity & relation extraction",
        "Biến văn bản/CTI records thành đỉnh và cạnh có nhãn quan hệ.",
        "Turn text/CTI records into labeled nodes and edges.",
        "Chất lượng extraction quyết định chất lượng graph retrieval.",
        "Extraction quality determines graph-retrieval quality.",
        ["NER/RE", "Chuẩn hóa CVE/ATT&CK IDs"],
        ["NER/RE", "Normalize CVE/ATT&CK IDs"],
    ),
    (5, "update"): _t(
        "Cập nhật gia tăng",
        "Incremental update",
        "Chèn ΔV,ΔE mà không xây lại toàn bộ đồ thị.",
        "Insert ΔV,ΔE without rebuilding the whole graph.",
        "Phù hợp SOC realtime / feed mới.",
        "Fits realtime SOC / new feeds.",
        ["⊕ incremental", "Idempotent keys"],
        ["⊕ incremental", "Idempotent keys"],
    ),
    (5, "store"): _t(
        "Lưu trữ đồ thị",
        "Graph storage",
        "Lưu nodes/edges trong bộ nhớ quá trình (demo) với thống kê quy mô.",
        "Store nodes/edges in process memory (demo) with scale stats.",
        "Cần quan sát |V|,|E| cho phân tích độ phức tạp.",
        "Need |V|,|E| observables for complexity analysis.",
        ["V,E counts", "Storage backend"],
        ["V,E counts", "Storage backend"],
    ),
    # ── Step 6 ────────────────────────────────────────────────────────
    (6, None): _t(
        "Mô hình chấm điểm ảo giác",
        "Hallucination scoring model",
        "Hợp nhất 4 nhân tố tin cậy thành risk ρ∈[0,1] để cổng lọc evidence.",
        "Fuse four trust factors into risk ρ∈[0,1] to gate evidence.",
        "Cơ sở lý thuyết cho Trusted Evidence Selection.",
        "Theoretical basis for Trusted Evidence Selection.",
        ["R,F,G,S", "τ=∑w f", "ρ=1−τ"],
        ["R,F,G,S", "τ=∑w f", "ρ=1−τ"],
    ),
    (6, "reliability"): _t(
        "Độ tin cậy nguồn (R)",
        "Source reliability (R)",
        "Prior theo nguồn: NVD/MITRE/CISA cao hơn blog không xác thực.",
        "Source prior: NVD/MITRE/CISA higher than unverified blogs.",
        "CTI phụ thuộc mạnh vào uy tín nguồn.",
        "CTI depends strongly on source reputation.",
        ["R(e)=source_prior(e)∈[0,1]"],
        ["R(e)=source_prior(e)∈[0,1]"],
    ),
    (6, "freshness"): _t(
        "Độ mới (F)",
        "Freshness (F)",
        "Giảm theo tuổi evidence; CVE lịch sử vẫn có sàn để không loại nhầm seed.",
        "Decays with age; historical CVEs keep a floor so seeds are not dropped wrongly.",
        "Cân bằng freshness và trí nhớ lịch sử tấn công.",
        "Balances freshness with historical attack memory.",
        ["F=f(age)", "floor cho hist. CVE"],
        ["F=f(age)", "floor for hist. CVE"],
    ),
    (6, "consistency"): _t(
        "Nhất quán đồ thị (G)",
        "Graph consistency (G)",
        "Đo entity trong evidence gắn kết với seed trên KG (hop ngắn).",
        "Measures how evidence entities cohere with seeds on the KG (short hops).",
        "Phạt evidence rời rạc / quan hệ bịa.",
        "Penalizes fragmented / fabricated relations.",
        ["path_consistency(Ent∪S)"],
        ["path_consistency(Ent∪S)"],
    ),
    (6, "relevance"): _t(
        "Liên quan ngữ nghĩa (S)",
        "Semantic relevance (S)",
        "Cosine TF-IDF (hoặc tương đương) giữa query và evidence.",
        "TF-IDF cosine (or equivalent) between query and evidence.",
        "Tránh evidence tin cậy nhưng lệch chủ đề.",
        "Avoid trusted but off-topic evidence.",
        ["S=cos(TFIDF(q),TFIDF(e))"],
        ["S=cos(TFIDF(q),TFIDF(e))"],
    ),
    (6, "score"): _t(
        "Điểm tổng hợp ρ",
        "Composite score ρ",
        "ρ=1−∑ w_i f_i — risk dùng để quyết định e∈E* hay bị loại.",
        "ρ=1−∑ w_i f_i — risk deciding whether e∈E* or is dropped.",
        "Tham số θ điều chỉnh độ chặt của cổng.",
        "Threshold θ controls gate strictness.",
        ["w=(0.30,0.20,0.25,0.25)", "θ≈0.55"],
        ["w=(0.30,0.20,0.25,0.25)", "θ≈0.55"],
    ),
    # ── Step 7–15 (compact but real theory) ───────────────────────────
    (7, None): _t(
        "Chuẩn bị dữ liệu",
        "Data preparation",
        "Thu thập CTI/IDS và dựng QA gắn gold evidence để đánh giá retrieval/faithfulness.",
        "Collect CTI/IDS data and build QA with gold evidence for retrieval/faithfulness eval.",
        "Không có dataset chuẩn thì không đo được đóng góp EDGR.",
        "Without a proper dataset, EDGR gains cannot be measured.",
        ["MITRE/CVE/CISA", "QA + evidence_ids"],
        ["MITRE/CVE/CISA", "QA + evidence_ids"],
    ),
    (7, "mitre"): _t("MITRE ATT&CK", "MITRE ATT&CK", "Khung TTP chuẩn hóa hành vi adversary.", "Standardized adversary TTP framework.", "Neo kỹ thuật tấn công trong KG/QA.", "Anchors attack techniques in KG/QA.", ["Tactic/Technique IDs"], ["Tactic/Technique IDs"], "Strom et al. 2018"),
    (7, "cve"): _t("CVE / NVD", "CVE / NVD", "Danh mục lỗ hổng chuẩn với định danh CVE.", "Standard vulnerability catalog with CVE IDs.", "Tránh LLM bịa mã CVE.", "Prevents LLM-fabricated CVE codes.", ["NVD JSON", "CPE"], ["NVD JSON", "CPE"]),
    (7, "cwe"): _t("CWE / CAPEC", "CWE / CAPEC", "Phân loại điểm yếu và pattern tấn công.", "Weakness classes and attack patterns.", "Bổ ngữ nghĩa cho liên kết CVE–technique.", "Semantics linking CVE–technique.", ["CWE ids"], ["CWE ids"]),
    (7, "cisa"): _t("CISA / CERT", "CISA / CERT", "Cảnh báo và KEV — lỗ hổng đang bị khai thác.", "Advisories and KEV — actively exploited vulns.", "Tín hiệu ưu tiên vận hành cho CTI.", "Operational priority signal for CTI.", ["KEV catalog"], ["KEV catalog"]),
    (7, "feeds"): _t("Threat feeds", "Threat feeds", "Luồng IOC/OSINT cập nhật liên tục.", "Continuous IOC/OSINT streams.", "Nguồn ΔV,ΔE cho KG động.", "Source of ΔV,ΔE for the dynamic KG.", ["IOC freshness"], ["IOC freshness"]),
    (7, "ids"): _t("IDS datasets", "IDS datasets", "Tập dữ liệu giao thông/alert để gắn kịch bản phát hiện xâm nhập.", "Traffic/alert datasets for intrusion scenarios.", "Neo miền IDS của luận án.", "Anchors the thesis IDS domain.", ["CIC-IDS", "UNSW-NB15"], ["CIC-IDS", "UNSW-NB15"]),
    (7, "qa"): _t("QA Dataset", "QA Dataset", "Cặp hỏi–đáp gắn evidence_ids vàng cho đánh giá.", "QA pairs with gold evidence_ids for evaluation.", "Bắt buộc cho P@k/MRR/Faith.", "Required for P@k/MRR/Faith.", ["gold evidence"], ["gold evidence"]),
    (8, None): _t(
        "Triển khai hệ thống",
        "System implementation",
        "Kiến trúc Query → EDGR ↔ KG/Vector/LLM → Trusted Answer.",
        "Architecture Query → EDGR ↔ KG/Vector/LLM → Trusted Answer.",
        "Chứng minh tính khả thi engineering của mô hình lý thuyết.",
        "Shows engineering feasibility of the theoretical model.",
        ["Services", "E2E path"],
        ["Services", "E2E path"],
    ),
    (8, "architecture"): _t("Kiến trúc", "Architecture", "Sơ đồ module và luồng dữ liệu hệ thống.", "Module diagram and data flow.", "Định nghĩa biên dịch vụ.", "Defines service boundaries.", ["API", "Pipeline"], ["API", "Pipeline"]),
    (8, "kg_svc"): _t("KG service", "KG service", "API truy vấn/cập nhật đồ thị.", "API to query/update the graph.", "Phục vụ expansion & consistency.", "Serves expansion & consistency.", ["neighbors", "upsert"], ["neighbors", "upsert"]),
    (8, "vec_svc"): _t("Vector DB", "Vector DB", "Chỉ mục TF-IDF/vector cho retrieval văn bản.", "TF-IDF/vector index for text retrieval.", "Nhánh sim(q,d) của ranking.", "The sim(q,d) branch of ranking.", ["top-k"], ["top-k"]),
    (8, "llm_svc"): _t("LLM grounded", "Grounded LLM", "Sinh câu trả lời chỉ từ evidence đã chọn.", "Generate answers only from selected evidence.", "Giảm bịa bằng ràng buộc context.", "Reduces fabrication via constrained context.", ["grounded prompt"], ["grounded prompt"]),
    (8, "e2e"): _t("E2E Trusted Answer", "E2E Trusted Answer", "Chạy một query xuyên suốt hệ thống.", "Run one query through the full system.", "Smoke-test tích hợp.", "Integration smoke test.", ["latency", "Faith/Hall"], ["latency", "Faith/Hall"]),
    (9, None): _t(
        "Thực nghiệm so sánh",
        "Comparative experiments",
        "So sánh EDGR với họ RAG trên cùng q,D,G và metric thống nhất.",
        "Compare EDGR with RAG-family methods on the same q,D,G and metrics.",
        "Chứng minh vượt trội có kiểm soát — không chỉnh điểm giả.",
        "Controlled superiority evidence — no fake score tweaks.",
        ["Fair protocol", "Same index"],
        ["Fair protocol", "Same index"],
    ),
    (9, "rag"): _t("Baseline RAG", "Baseline RAG", "Retriever phẳng + generator.", "Flat retriever + generator.", "Baseline cổ điển.", "Classic baseline.", ["no graph gate"], ["no graph gate"], "Lewis 2020"),
    (9, "graphrag"): _t("Baseline GraphRAG", "Baseline GraphRAG", "Retrieval theo cộng đồng/đồ thị.", "Community/graph retrieval.", "Đối chứng graph-based.", "Graph-based control.", ["community summaries"], ["community summaries"], "Edge 2024"),
    (9, "lightrag"): _t("Baseline LightRAG", "Baseline LightRAG", "Graph RAG nhẹ dual-level.", "Lightweight dual-level Graph RAG.", "Đối chứng hiệu năng.", "Efficiency control.", ["dual-level"], ["dual-level"], "Guo 2024"),
    (9, "hipporag"): _t("Baseline HippoRAG", "Baseline HippoRAG", "Personalized PageRank trên KG.", "Personalized PageRank on a KG.", "Đối chứng multi-hop.", "Multi-hop control.", ["PPR"], ["PPR"], "Gutiérrez 2024"),
    (9, "selfrag"): _t("Baseline Self-RAG", "Baseline Self-RAG", "Self-reflection tokens quyết định retrieve/critique.", "Self-reflection tokens decide retrieve/critique.", "Đối chứng critique nội tại.", "Internal-critique control.", ["reflection"], ["reflection"], "Asai 2024"),
    (9, "crag"): _t("Baseline Corrective-RAG", "Baseline Corrective-RAG", "Đánh giá retrieval và sửa/web khi kém.", "Evaluate retrieval and correct/web when weak.", "Đối chứng corrective loop.", "Corrective-loop control.", ["corrective"], ["corrective"], "Yan 2024"),
    (9, "edgr"): _t("EDGR (Ours)", "EDGR (Ours)", "Pipeline đề xuất: graph động + temporal + trust gate.", "Proposed pipeline: dynamic graph + temporal + trust gate.", "Phương pháp chính cần thắng trên Faith/Hall.", "Main method expected to win on Faith/Hall.", ["ρ-gate"], ["ρ-gate"]),
    (9, "compare"): _t("Bảng so sánh", "Comparison table", "Tổng hợp metric mọi method.", "Aggregate metrics across methods.", "Báo cáo thực nghiệm.", "Experimental report.", ["Δ Faith"], ["Δ Faith"]),
    (10, None): _t(
        "Đánh giá",
        "Evaluation",
        "Đo generation (Faith/Hall/F1), retrieval (P@k/MRR) và hệ thống (latency/resource).",
        "Measure generation (Faith/Hall/F1), retrieval (P@k/MRR), and system (latency/resource).",
        "Cơ sở kết luận khoa học có số liệu.",
        "Basis for data-backed scientific conclusions.",
        ["Offline evaluator", "QA gold"],
        ["Offline evaluator", "QA gold"],
    ),
    (10, "accuracy"): _t("Accuracy", "Accuracy", "Tỷ lệ trả lời đúng (proxy entity/F1).", "Correct-answer rate (entity/F1 proxy).", "Metric tổng quát.", "General metric.", ["0–1"], ["0–1"]),
    (10, "prf1"): _t("P / R / F1", "P / R / F1", "Precision, Recall, F1 trên token/entity.", "Precision, Recall, F1 on tokens/entities.", "Cân bằng đúng–đủ.", "Balance correctness–coverage.", ["F1=2PR/(P+R)"], ["F1=2PR/(P+R)"]),
    (10, "faith"): _t("Faithfulness", "Faithfulness", "Mức câu trả lời được evidence hỗ trợ.", "How much the answer is supported by evidence.", "Metric chính chống ảo giác.", "Primary anti-hallucination metric.", ["support(answer,E*)"], ["support(answer,E*)"]),
    (10, "hall"): _t("Hallucination Rate", "Hallucination Rate", "Phần nội dung không grounded ≈ 1−Faith (proxy).", "Ungrounded content fraction ≈ 1−Faith (proxy).", "Càng thấp càng tốt.", "Lower is better.", ["Hall↓"], ["Hall↓"]),
    (10, "retrieval"): _t("P@k / R@k / MRR", "P@k / R@k / MRR", "Chất lượng xếp hạng evidence so với gold.", "Evidence ranking quality vs gold.", "Đánh giá riêng nhánh retrieval.", "Evaluates the retrieval branch.", ["MRR=1/rank*"], ["MRR=1/rank*"]),
    (10, "latency"): _t("Latency", "Latency", "Thời gian đáp ứng trung bình (ms).", "Average response time (ms).", "Ràng buộc thực dụng SOC.", "Practical SOC constraint.", ["p50/p95"], ["p50/p95"]),
    (10, "resource"): _t("CPU / Memory", "CPU / Memory", "Tài nguyên chạy pipeline.", "Runtime resource usage.", "Phụ trợ scalability.", "Supports scalability claims.", ["RSS", "CPU%"], ["RSS", "CPU%"]),
    (10, "full"): _t("Báo cáo đầy đủ", "Full report", "Gộp mọi metric thành báo cáo đánh giá.", "Merge all metrics into an evaluation report.", "Input chương Experiments.", "Input to Experiments chapter.", ["summary table"], ["summary table"]),
    (10, "stats"): _t(
        "Thống kê cặp",
        "Paired statistics",
        "Bootstrap CI cho faithfulness và McNemar exact trên proxy đúng/sai từng QA (EDGR vs baseline stub).",
        "Bootstrap CIs for faithfulness and McNemar exact on per-QA correctness proxies (EDGR vs stub baseline).",
        "Tránh kết luận chỉ từ mean một query; gắn giả thuyết H1.",
        "Avoid single-query means; ties to hypothesis H1.",
        ["bootstrap CI", "McNemar", "H1"],
        ["bootstrap CI", "McNemar", "H1"],
    ),
    (10, "validity"): _t(
        "Threats to validity",
        "Threats to validity",
        "Internal / external / construct / conclusion validity — bắt buộc trong paper quốc tế.",
        "Internal / external / construct / conclusion validity — required in international papers.",
        "Công khai giới hạn seed và family stub.",
        "Disclose seed limits and family stubs.",
        ["internal", "external", "construct", "conclusion"],
        ["internal", "external", "construct", "conclusion"],
    ),
    (10, "human_eval"): _t(
        "Human-eval SOC",
        "SOC human evaluation",
        (
            "Protocol đánh giá người: rubric Likert + panel hai annotator (soc_a/soc_b) + Cohen’s κ "
            "trên groundedness / unsupported IDs / actionability / abstain. "
            "Demo có seed_soc_panel để tính κ ngay; API nhận nhãn SOC hiện trường."
        ),
        (
            "Human evaluation protocol: Likert rubric + dual annotators (soc_a/soc_b) + Cohen’s κ "
            "on groundedness / unsupported IDs / actionability / abstain. "
            "Demo ships seed_soc_panel to compute κ immediately; API accepts field SOC labels."
        ),
        "Bằng chứng human-eval cho luận án/paper — disclosure seed vs field annotators.",
        "Human-eval evidence for thesis/paper — disclose seed vs field annotators.",
        ["Cohen’s κ", "seed_soc_panel", "POST /api/human-eval/annotations"],
        ["Cohen’s κ", "seed_soc_panel", "POST /api/human-eval/annotations"],
    ),
    (10, "human_session"): _t(
        "Phiên chấm SOC",
        "SOC rating session",
        "Chạy EDGR trên subset QA → hàng đợi (question, system_answer, evidence) để hai SOC chấm độc lập.",
        "Run EDGR on a QA subset → queue (question, system_answer, evidence) for two independent SOC raters.",
        "Thu thập nhãn thật hoặc đối chiếu panel seed.",
        "Collect field labels or compare against the seed panel.",
        ["live queue", "dual rating"],
        ["live queue", "dual rating"],
    ),
    (10, "rigor"): _t(
        "Báo cáo hàm lượng khoa học",
        "Scientific rigor report",
        "Gói H1–H4, novelty claim, corpus scale, paired stats, ablation dataset, OOD abstain, validity, gate theory.",
        "Bundle of H1–H4, novelty claim, corpus scale, paired stats, dataset ablation, OOD abstain, validity, gate theory.",
        "Artifact trung tâm để chứng minh đề tài đủ khung TS / paper.",
        "Central artifact showing the topic meets thesis/paper scientific framing.",
        ["H1–H4", "phd_readiness checklist"],
        ["H1–H4", "phd_readiness checklist"],
    ),
    (9, "dataset_means"): _t(
        "Trung bình dataset + CI",
        "Dataset means + CI",
        "Mean faithfulness/hallucination trên toàn bộ QA (trừ OOD) kèm bootstrap CI; disclosure family stub.",
        "Mean faithfulness/hallucination over all QA (excl. OOD) with bootstrap CIs; family-stub disclosure.",
        "Bảng so sánh công bằng hơn single-query.",
        "Fairer than single-query comparison tables.",
        ["dataset mean", "CI", "stub disclosure"],
        ["dataset mean", "CI", "stub disclosure"],
    ),
    (11, None): _t(
        "Ablation study",
        "Ablation study",
        "Tắt từng thành phần để đo Δ metric — chứng minh đóng góp nhân quả.",
        "Disable each component to measure Δ metrics — causal contribution evidence.",
        "Bắt buộc trong paper thuật toán.",
        "Required in algorithm papers.",
        ["full vs w/o X", "ΔFaith"],
        ["full vs w/o X", "ΔFaith"],
    ),
    (11, "full"): _t("Full EDGR", "Full EDGR", "Cấu hình đủ module làm mốc.", "Full-module configuration as baseline.", "Đối chứng trên cùng query.", "Control on the same queries.", ["all on"], ["all on"]),
    (11, "wo_temporal"): _t("w/o Temporal", "w/o Temporal", "Tắt lọc thời gian.", "Disable temporal filter.", "Đo đóng góp freshness window.", "Measure freshness-window gain.", ["Δ"], ["Δ"]),
    (11, "wo_graph"): _t("w/o Graph", "w/o Graph", "Tắt nhánh đồ thị.", "Disable graph branch.", "Đo đóng góp KG expansion.", "Measure KG-expansion gain.", ["Δ"], ["Δ"]),
    (11, "wo_trust"): _t("w/o Trust", "w/o Trust", "Tắt cổng tin cậy.", "Disable trust gate.", "Đo đóng góp risk scoring.", "Measure risk-scoring gain.", ["Δ"], ["Δ"]),
    (11, "wo_ranking"): _t("w/o Ranking", "w/o Ranking", "Tắt xếp hạng lai.", "Disable hybrid ranking.", "Đo đóng góp entity boost.", "Measure entity-boost gain.", ["Δ"], ["Δ"]),
    (11, "wo_scoring"): _t("w/o Scoring", "w/o Scoring", "Tắt hallucination scoring.", "Disable hallucination scoring.", "Đo đóng góp ρ.", "Measure ρ contribution.", ["Δ"], ["Δ"]),
    (11, "summary"): _t("Tổng hợp ablation", "Ablation summary", "Bảng Δ theo module.", "Δ table by module.", "Kết luận module nào cần thiết.", "Conclude which modules are necessary.", ["bar/table"], ["bar/table"]),
    (12, None): _t(
        "Phân tích thuật toán",
        "Algorithm analysis",
        "Phân tích T(n), S(n), invariant, hội tụ và scalability thực nghiệm.",
        "Analyze T(n), S(n), invariants, convergence, and empirical scalability.",
        "Bổ sung cam kết lý thuyết ngoài số liệu thực nghiệm.",
        "Adds theoretical claims beyond empirical scores.",
        ["O(E log V)", "invariants"],
        ["O(E log V)", "invariants"],
    ),
    (12, "time"): _t("Time complexity", "Time complexity", "T(n)≈O(E log V) cho phần đồ thị/ranking.", "T(n)≈O(E log V) for graph/ranking work.", "Ước lượng chi phí tăng theo quy mô.", "Estimate cost growth with scale.", ["dominant terms"], ["dominant terms"]),
    (12, "space"): _t("Space complexity", "Space complexity", "S(n)=O(V+E+|D|) cho KG + index.", "S(n)=O(V+E+|D|) for KG + index.", "Giới hạn bộ nhớ.", "Memory bound.", ["V,E,D"], ["V,E,D"]),
    (12, "correctness"): _t("Correctness", "Correctness", "Invariant: seed giữ; E* thỏa ρ≤θ và |E*|≤k.", "Invariants: keep seeds; E* satisfies ρ≤θ and |E*|≤k.", "Đảm bảo an toàn logic của cổng.", "Ensures logical safety of the gate.", ["invariants"], ["invariants"]),
    (12, "convergence"): _t(
        "Hội tụ thực nghiệm",
        "Empirical convergence",
        (
            "Hội tụ ở đây nghĩa thực nghiệm: khi tăng top_k, tập evidence chọn ra ổn định "
            "(prefix_stability) và faithfulness không dao động hỗn loạn. "
            "Sau khi Chạy, biểu đồ hai đường (stability + Faith theo k) nằm ở khối Kết quả."
        ),
        (
            "Convergence here is empirical: as top_k grows, the selected evidence set stabilizes "
            "(prefix_stability) and faithfulness does not oscillate chaotically. "
            "After Run, a two-series chart (stability + Faith vs k) appears in Results."
        ),
        "Chứng minh pipeline tái lập được trước khi báo cáo Experiments.",
        "Shows the pipeline is reproducible before reporting Experiments.",
        [
            "Đo series k=1…7 trên cùng query",
            "Biểu đồ: prefix_stability(k) và faithfulness(k)",
            "Verdict converged nếu stability ≥ 0.5 từ các mốc k≥3",
        ],
        [
            "Measure series k=1…7 on the same query",
            "Chart: prefix_stability(k) and faithfulness(k)",
            "Converged if stability ≥ 0.5 from checkpoints k≥3",
        ],
    ),
    (12, "scalability"): _t("Scalability", "Scalability", "Latency thực nghiệm theo |D| / |V|.", "Empirical latency vs |D| / |V|.", "Kiểm chứng asymptotic.", "Checks asymptotics.", ["scale curves"], ["scale curves"]),
    (12, "report"): _t("Báo cáo phân tích", "Analysis report", "Gộp asymptotic + empirical.", "Merge asymptotic + empirical.", "Mục phân tích luận án.", "Thesis analysis section.", ["summary"], ["summary"]),
    (13, None): {
        **_t(
            "Công bố khoa học từ kết quả EDGR",
            "Scientific publication from EDGR results",
            (
                "Công bố khoa học ở đây không phải “viết lại demo bằng văn hoa”, mà là đóng gói "
                "từng đóng góp thành manuscript có contribution claim một câu, related work paraphrase "
                "sau khi đọc, và Results lấy từ artifact pipeline (Steps 9–11). "
                "Bốn bài: EDGR Algorithm, Dynamic KG, Hallucination Scoring, Comprehensive Evaluation."
            ),
            (
                "Publication here is not “rewriting the demo in ornate prose”; it means packaging "
                "each contribution into a manuscript with a one-sentence claim, related work paraphrased "
                "after reading, and Results from pipeline artifacts (Steps 9–11). "
                "Four papers: EDGR Algorithm, Dynamic KG, Hallucination Scoring, Comprehensive Evaluation."
            ),
            (
                "Hội đồng và reviewer đọc claim hẹp + số liệu tái lập được. "
                "Outline rõ Paper↔Steps chứng minh nghiên cứu đã chuyển từ prototype sang sản phẩm học thuật."
            ),
            (
                "Committees and reviewers read a narrow claim plus reproducible numbers. "
                "A clear Paper↔Steps outline shows the work moved from prototype to a scholarly product."
            ),
            [
                "Mỗi paper một contribution claim đo được",
                "Chống tự đạo văn giữa 4 bài (overlap control)",
                "Số liệu từ pipeline — không minh họa tay",
                "Checklist chống đạo văn / AI-tone trước nộp",
            ],
            [
                "One measurable contribution claim per paper",
                "Self-plagiarism control across 4 papers",
                "Numbers from the pipeline — not hand-drawn demos",
                "Anti-plagiarism / AI-tone checklist before submit",
            ],
            "Lewis 2020; Edge 2024; Ji 2023; Wagner 2019 — đọc rồi paraphrase, không dán dịch",
        ),
        "argument_vi": (
            "Luận án cần chứng minh đóng góp đã được “đóng gói” theo chuẩn peer-review: "
            "claim hẹp, baseline rõ, hạn chế thành thật. "
            "Bước 13 buộc gắn artifact runtime, nên khó viết theo kiểu liệt kê module chung chung."
        ),
        "argument_en": (
            "A thesis must show contributions packaged to peer-review standards: "
            "narrow claims, clear baselines, honest limits. "
            "Step 13 requires runtime artifacts, which blocks generic module-list writing."
        ),
    },
    (13, "p1"): _t(
        "Paper 1 — Thuật toán EDGR",
        "Paper 1 — EDGR algorithm",
        "Manuscript thuật toán: 6 giai φ1–φ6, cổng risk, so sánh baseline và ablation.",
        "Algorithm manuscript: six stages φ1–φ6, risk gate, baselines and ablations.",
        "Đây là bài gánh đóng góp thuật toán trung tâm của luận án.",
        "This paper carries the thesis’s central algorithmic contribution.",
        ["Claim EDGR", "Stages φi", "Results từ Step 9–11"],
        ["EDGR claim", "Stages φi", "Results from Steps 9–11"],
        "lewis2020rag; edge2024graphrag; ji2023survey",
    ),
    (13, "p2"): _t(
        "Paper 2 — Dynamic KG",
        "Paper 2 — Dynamic KG",
        "Manuscript lớp đồ thị CTI động: schema, ingest, cập nhật gia tăng, interface Expand.",
        "Dynamic CTI-KG manuscript: schema, ingest, incremental updates, Expand interface.",
        "Tách nền tri thức khỏi thuật toán xếp hạng/risk để tránh trùng Paper 1/3.",
        "Separates the knowledge layer from ranking/risk to avoid overlap with Papers 1/3.",
        ["Schema (u,r,v)", "G←G∪Δ", "Case study KG stats"],
        ["Schema (u,r,v)", "G←G∪Δ", "KG stats case study"],
        "strom2018attack; wagner2019cti; edge2024graphrag",
    ),
    (13, "p3"): _t(
        "Paper 3 — Hallucination Scoring",
        "Paper 3 — Hallucination Scoring",
        "Manuscript chấm điểm rủi ro: τ=0.30R+0.20F+0.25G+0.25S, ρ=1−τ, ngưỡng θ và abstain.",
        "Risk-scoring manuscript: τ=0.30R+0.20F+0.25G+0.25S, ρ=1−τ, threshold θ and abstain.",
        "Làm rõ cổng tin cậy — trọng số là hyper-parameter, không ngụy trang thành học sâu đã tối ưu.",
        "Clarifies the trust gate — weights are hyperparameters, not a pretence of globally optimized deep learning.",
        ["R,F,G,S", "ρ-gate", "Đối vị Self-RAG/CRAG"],
        ["R,F,G,S", "ρ-gate", "vs Self-RAG/CRAG"],
        "ji2023survey; asai2024selfrag; yan2024crag",
    ),
    (13, "p4"): _t(
        "Paper 4 — Comprehensive Evaluation",
        "Paper 4 — Comprehensive Evaluation",
        "Manuscript protocol đánh giá: dataset, baseline, metric, ablation, threats to validity.",
        "Evaluation-protocol manuscript: dataset, baselines, metrics, ablations, threats to validity.",
        "Có thể là bài riêng hoặc rút thành mục Evaluation của Paper 1 tùy venue.",
        "May stand alone or collapse into Paper 1’s Evaluation section depending on venue.",
        ["QA protocol", "P@k/MRR/Faith", "Ablation Δ"],
        ["QA protocol", "P@k/MRR/Faith", "Ablation Δ"],
        "gao2024ragsurvey; khraisat2019ids",
    ),
    (13, "plan"): {
        **_t(
            "Kế hoạch công bố tổng hợp (4 bài)",
            "Combined publication plan (4 papers)",
            (
                "Điều phối thứ tự nộp, venue, timeline và chống tự đạo văn giữa bốn manuscript. "
                "Không phải thư chấp nhận của venue."
            ),
            (
                "Coordinates submission order, venues, timeline, and self-plagiarism control across "
                "four manuscripts. Not a venue acceptance letter."
            ),
            "Giúp nhóm hướng dẫn và hội đồng theo dõi tiến độ viết từng bài.",
            "Helps advisors and committees track writing progress per paper.",
            ["Strategy + overlap control", "Timeline P1–P4", "Committee readiness checklist"],
            ["Strategy + overlap control", "Timeline P1–P4", "Committee readiness checklist"],
        ),
        "argument_vi": (
            "Kế hoạch tốt giảm rủi ro tự đạo văn. Mỗi milestone chỉ cam kết một claim chính đã có artifact."
        ),
        "argument_en": (
            "A good plan reduces self-plagiarism risk. Each milestone commits to one main claim that already has artifacts."
        ),
    },
    (14, None): _t(
        "Viết luận án",
        "Dissertation writing",
        "Cấu trúc 8 chương khớp quy trình A→Z và đóng góp EDGR.",
        "Eight-chapter structure aligned with A→Z process and EDGR contributions.",
        "Tổng hợp toàn bộ nghiên cứu thành văn bản bảo vệ.",
        "Synthesizes the whole study into a defendable manuscript.",
        ["Ch1–Ch8"],
        ["Ch1–Ch8"],
    ),
    (14, "ch1"): _t("Ch1 Introduction", "Ch1 Introduction", "Động lực, mục tiêu, đóng góp.", "Motivation, goals, contributions.", "Mở đầu luận án.", "Thesis opening.", ["problem statement"], ["problem statement"]),
    (14, "ch2"): _t("Ch2 Overview", "Ch2 Overview", "Tổng quan lĩnh vực và khái niệm nền.", "Field overview and background concepts.", "Nền tảng lý thuyết chung.", "Shared theoretical background.", ["RAG/CTI/IDS"], ["RAG/CTI/IDS"]),
    (14, "ch3"): _t("Ch3 Problem & Gaps", "Ch3 Problem & Gaps", "Bài toán và khoảng trống.", "Problem and gaps.", "Từ khảo sát → formal problem.", "From survey → formal problem.", ["G1–Gk"], ["G1–Gk"]),
    (14, "ch4"): _t("Ch4 EDGR", "Ch4 EDGR", "Chi tiết thuật toán EDGR.", "EDGR algorithm details.", "Chương đóng góp chính.", "Main contribution chapter.", ["stages"], ["stages"]),
    (14, "ch5"): _t("Ch5 Dynamic KG", "Ch5 Dynamic KG", "Xây/cập nhật KG.", "KG build/update.", "Nền dữ liệu.", "Data foundation.", ["incremental"], ["incremental"]),
    (14, "ch6"): _t("Ch6 Scoring", "Ch6 Scoring", "Mô hình hallucination scoring.", "Hallucination scoring model.", "Cổng tin cậy.", "Trust gate.", ["R,F,G,S"], ["R,F,G,S"]),
    (14, "ch7"): _t("Ch7 Experiments", "Ch7 Experiments", "Thực nghiệm, metric, ablation.", "Experiments, metrics, ablation.", "Bằng chứng thực nghiệm.", "Empirical evidence.", ["tables"], ["tables"]),
    (14, "ch8"): _t("Ch8 Conclusion", "Ch8 Conclusion", "Kết luận và hướng phát triển.", "Conclusion and future work.", "Đóng luận án.", "Closes the thesis.", ["limitations"], ["limitations"]),
    (14, "toc"): _t("Mục lục", "TOC", "Mục lục đầy đủ và word budget.", "Full TOC and word budget.", "Khung soạn thảo.", "Drafting frame.", ["chapters"], ["chapters"]),
    (15, None): _t(
        "Bảo vệ luận án",
        "Dissertation defense",
        "Chuẩn bị trình bày, Q&A và checklist sẵn sàng bảo vệ.",
        "Prepare presentation, Q&A, and defense-readiness checklist.",
        "Chuyển kết quả nghiên cứu thành thuyết trình phản biện.",
        "Turns research results into a defendable presentation.",
        ["Ready%", "demo metrics"],
        ["Ready%", "demo metrics"],
    ),
    (15, "present"): _t("Presentation", "Presentation", "Slide bảo vệ: động lực → EDGR → kết quả.", "Defense slides: motivation → EDGR → results.", "Kênh truyền đạt chính.", "Main communication channel.", ["storyline"], ["storyline"]),
    (15, "defend"): _t("Defense Q&A", "Defense Q&A", "Ngân hàng câu hỏi phản biện và câu trả lời.", "Committee Q&A bank and answers.", "Ứng phó phản biện.", "Handle committee critique.", ["FAQ"], ["FAQ"]),
    (15, "checklist"): _t("Checklist", "Checklist", "Hạng mục bắt buộc trước bảo vệ.", "Mandatory pre-defense items.", "Đo Ready%.", "Measure Ready%.", ["checks"], ["checks"]),
    (15, "success"): _t("Success summary", "Success summary", "Tổng kết hoàn thành và metric demo cuối.", "Completion summary and final demo metrics.", "Đóng quy trình A→Z.", "Closes the A→Z process.", ["final metrics"], ["final metrics"]),
    (16, None): {
        **_t(
            "Ứng dụng «Phát hiện xâm nhập và tình báo»",
            "«Intrusion Detection and Threat Intelligence» application",
            (
                "Đây là sản phẩm ứng dụng (console SOC), không phải bước quy trình nghiên cứu: "
                "analyst nhập cảnh báo hoặc câu hỏi CTI, hệ thống gọi EDGR trên KG và trả "
                "Trusted Answer kèm evidence / điểm tin cậy."
            ),
            (
                "This is an application product (SOC console), not a research-process step: "
                "an analyst enters an alert or CTI question; the system runs EDGR on the KG and "
                "returns a Trusted Answer with evidence / trust scores."
            ),
            "Chứng minh nghiên cứu EDGR đã đóng gói thành phần mềm dùng được trên miền IDS/CTI.",
            "Shows EDGR research packaged into usable IDS/CTI software.",
            [
                "Console: nhập → phân tích → trả lời",
                "EDGR + KG CTI + cổng ρ",
                "Không thay IDS engine — lớp giải thích/truy hồi",
            ],
            [
                "Console: input → analyze → answer",
                "EDGR + CTI KG + ρ-gate",
                "Does not replace IDS engines — explanation/retrieval layer",
            ],
            "wagner2019cti; khraisat2019ids; edge2024graphrag",
        ),
        "argument_vi": (
            "Bước 16 trả lời câu “ứng dụng ở đâu?” bằng phần mềm chạy được, "
            "không bằng sơ đồ quy trình thêm."
        ),
        "argument_en": (
            "Step 16 answers “where is the application?” with runnable software, "
            "not with another process diagram."
        ),
    },
    (16, "console"): {
        **_t(
            "Console ứng dụng IDS/CTI",
            "IDS/CTI application console",
            "Giao diện dùng: phân tích alert/câu hỏi và xem Trusted Answer + evidence.",
            "User-facing UI: analyze alerts/questions and view Trusted Answer + evidence.",
            "Điểm vào duy nhất của ứng dụng thực tế.",
            "The sole entry point of the practical application.",
            ["Query/alert", "EDGR live", "Evidence + graph"],
            ["Query/alert", "EDGR live", "Evidence + graph"],
        ),
    },
}


def _parse_refs(refs: str) -> list[dict[str, str]]:
    if not refs or not str(refs).strip():
        return []
    # Prefer semicolon separators so "Author et al., Year" stays intact.
    raw = str(refs).strip()
    parts = (
        [p.strip() for p in raw.split(";") if p.strip()]
        if ";" in raw
        else [p.strip() for p in raw.split("|") if p.strip()]
    )
    if not parts:
        parts = [raw]
    out: list[dict[str, str]] = []
    for p in parts:
        out.append(
            {
                "cite": p,
                "role_vi": "Nền tảng / đối chứng trong related work",
                "role_en": "Foundation / baseline in related work",
            }
        )
    return out


def _short_blurb(text: str, limit: int = 180) -> str:
    s = " ".join(str(text or "").split())
    if len(s) <= limit:
        return s
    cut = s[: limit - 1].rsplit(" ", 1)[0]
    return (cut or s[: limit - 1]) + "…"


def _attach_step_overview_intro(out: dict[str, Any], step_id: int) -> None:
    """Lead-in + child-tab map for the step-overview theory card."""
    from app.pipeline.definition import get_step

    step = get_step(step_id) or {}
    title_vi = str(step.get("title") or f"Bước {step_id}")
    title_en = str(step.get("title_en") or title_vi)
    goal_vi = str(step.get("goal") or "").strip()
    goal_en = str(step.get("goal_en") or goal_vi).strip()
    tasks = list(step.get("tasks") or [])

    if not str(out.get("intro_vi") or "").strip():
        out["intro_vi"] = (
            f"Dẫn nhập — Bước {step_id}. {title_vi}. "
            f"{goal_vi} "
            "Tab «Tổng quan bước» đặt khung lý thuyết chung của cả bước: khái niệm, giả định và "
            "lập luận liên kết các tab lớn bên dưới. Đọc dẫn nhập này trước, rồi lần lượt mở từng tab con "
            "để đi sâu (định nghĩa → toán → thuật toán → minh chứng)."
        )
    if not str(out.get("intro_en") or "").strip():
        out["intro_en"] = (
            f"Lead-in — Step {step_id}. {title_en}. "
            f"{goal_en} "
            "The «Step overview» tab sets the shared theoretical frame for the whole step: concepts, "
            "assumptions, and the argument that links the major child tabs below. Read this lead-in first, "
            "then open each child tab for depth (definition → math → algorithm → evidence)."
        )

    if out.get("child_tabs"):
        return

    children: list[dict[str, Any]] = []
    for i, t in enumerate(tasks):
        tid = str(t.get("id") or "")
        if not tid:
            continue
        tpack = THEORY.get((step_id, tid)) or {}
        blurb_vi = _short_blurb(
            str(tpack.get("what_vi") or tpack.get("why_vi") or t.get("title") or tid)
        )
        blurb_en = _short_blurb(
            str(
                tpack.get("what_en")
                or tpack.get("why_en")
                or t.get("title_en")
                or t.get("title")
                or tid
            )
        )
        children.append(
            {
                "id": tid,
                "index": i + 1,
                "title_vi": str(t.get("title") or tid),
                "title_en": str(t.get("title_en") or t.get("title") or tid),
                "blurb_vi": blurb_vi,
                "blurb_en": blurb_en,
            }
        )
    out["child_tabs"] = children


def _enrich_theory(
    pack: dict[str, Any], step_id: int, task_id: str | None
) -> dict[str, Any]:
    """Normalize every theory pack into an academic frame for the UI."""
    out = dict(pack or {})
    what_vi = str(out.get("what_vi") or "").strip()
    what_en = str(out.get("what_en") or "").strip()
    why_vi = str(out.get("why_vi") or "").strip()
    why_en = str(out.get("why_en") or "").strip()
    ideas_vi = list(out.get("ideas_vi") or [])
    ideas_en = list(out.get("ideas_en") or [])

    out.setdefault(
        "frame_vi",
        "Khung lý thuyết học thuật: dẫn nhập · tab lớn · định nghĩa · giả định · lập luận · related work"
        if not task_id
        else "Khung lý thuyết học thuật: định nghĩa khoa học · giả định · lập luận · related work",
    )
    out.setdefault(
        "frame_en",
        "Academic theory frame: lead-in · major tabs · definition · assumptions · argument · related work"
        if not task_id
        else "Academic theory frame: scientific definition · assumptions · argument · related work",
    )

    if not task_id:
        _attach_step_overview_intro(out, step_id)

    # Formal claim / scientific argument (required for scholarly tone)
    if not str(out.get("argument_vi") or "").strip():
        idea_join = "; ".join(ideas_vi[:3]) if ideas_vi else "các điểm kiểm chứng của tab"
        out["argument_vi"] = (
            f"Lập luận khoa học: {what_vi} "
            f"Trong luận án EDGR, điều này quan trọng vì {why_vi} "
            f"Do đó tab này phải làm rõ và (khi chạy) kiểm chứng: {idea_join}. "
            f"Khối Mô hình toán / Thuật toán bên dưới cụ thể hóa giả định thành công thức và thủ tục."
        )
    if not str(out.get("argument_en") or "").strip():
        idea_join_en = "; ".join(ideas_en[:3]) if ideas_en else "this tab’s testable points"
        out["argument_en"] = (
            f"Scientific argument: {what_en} "
            f"In the EDGR thesis this matters because {why_en} "
            f"Hence this tab must clarify and (when run) test: {idea_join_en}. "
            f"The Math / Algorithm blocks below turn assumptions into formulas and procedures."
        )

    # Explicit assumptions (hypothesis layer)
    if not out.get("assumptions_vi"):
        out["assumptions_vi"] = [
            "Giả định miền: bài toán gắn IDS/CTI có thể neo bằng evidence + quan hệ trên KG.",
            "Giả định đánh giá: Faith/Hall và/hoặc P@k–MRR là proxy hợp lệ cho chất lượng grounded.",
            *(
                [f"Giả định kiểm chứng tại tab: {ideas_vi[0]}"]
                if ideas_vi
                else []
            ),
        ]
    if not out.get("assumptions_en"):
        out["assumptions_en"] = [
            "Domain assumption: IDS/CTI tasks can be grounded via evidence + KG relations.",
            "Evaluation assumption: Faith/Hall and/or P@k–MRR are valid proxies for grounded quality.",
            *(
                [f"Tab-level testable assumption: {ideas_en[0]}"]
                if ideas_en
                else []
            ),
        ]

    # Related-work structure from free-text refs
    if not out.get("related_work"):
        out["related_work"] = _parse_refs(str(out.get("refs") or ""))

    out["scope_vi"] = (
        f"Bước {step_id}" + (f" · công việc `{task_id}`" if task_id else " · tổng quan bước")
    )
    out["scope_en"] = (
        f"Step {step_id}" + (f" · task `{task_id}`" if task_id else " · step overview")
    )
    return out


def get_theory(step_id: int, task_id: str | None = None) -> dict[str, Any]:
    key = (step_id, task_id)
    if key in THEORY and THEORY[key] is not None:
        return _enrich_theory(dict(THEORY[key]), step_id, task_id)
    # fallback: step overview
    if (step_id, None) in THEORY:
        base = dict(THEORY[(step_id, None)])
        if task_id:
            base["name_vi"] = f"{base.get('name_vi', f'Bước {step_id}')} · `{task_id}`"
            base["name_en"] = f"{base.get('name_en', f'Step {step_id}')} · `{task_id}`"
            base["what_vi"] = (
                str(base.get("what_vi", ""))
                + f" Tab con `{task_id}` thao tác một phần hình thức của bước {step_id} "
                f"trong chuỗi lập luận luận án."
            )
            base["what_en"] = (
                str(base.get("what_en", ""))
                + f" Child tab `{task_id}` executes a formal part of step {step_id} "
                f"in the thesis argument chain."
            )
        return _enrich_theory(base, step_id, task_id)
    return _enrich_theory(
        _t(
            f"Bước {step_id}",
            f"Step {step_id}",
            "Nội dung lý thuyết của bước nghiên cứu trong pipeline EDGR.",
            "Theoretical content of this research step in the EDGR pipeline.",
            "Phục vụ chuỗi lập luận luận án (survey → method → evaluation).",
            "Serves the thesis argument chain (survey → method → evaluation).",
            [],
            [],
        ),
        step_id,
        task_id,
    )
