"""
Step 13 — scientific publication packages.

Content is original framing of THIS thesis (EDGR / IDS–CTI). It is not copied from
Lewis/Edge/Ji/etc.; those works appear only as citation targets the student must
read and paraphrase. Draft prose is intentionally imperfect in places (hedges,
concrete pipeline anchors) so it reads like a working academic note, not a
generic LLM essay.
"""

from __future__ import annotations

from typing import Any


def _integrity() -> dict[str, Any]:
    return {
        "title_vi": "Kỷ luật viết & chống đạo văn (bắt buộc)",
        "title_en": "Writing integrity & anti-plagiarism (mandatory)",
        "rules_vi": [
            "Không dán đoạn văn từ bài báo khác, kể cả đã dịch. Mọi ý từ tài liệu ngoài phải được diễn đạt lại bằng lời của mình sau khi đọc kỹ, rồi gắn citation.",
            "Không dùng cụm “AI-sounding” rỗng: “trong kỷ nguyên số”, “bùng nổ trí tuệ nhân tạo”, “cải thiện đáng kể mọi mặt” nếu không có số liệu pipeline đính kèm.",
            "Mỗi claim thực nghiệm phải trỏ về artifact đã chạy (Step 9–11): bảng metric, ablation, hoặc KG stats — không bịa số.",
            "Related work: mỗi nhóm (RAG / GraphRAG / Self-RAG / CRAG / CTI KG) tối thiểu 1–2 citation có DOI; mô tả bằng câu chủ động của mình.",
            "Khi nghi ngờ trùng ý: đổi cấu trúc đoạn, thêm điều kiện miền IDS/CTI, và giữ citation — đừng chỉ thay từ đồng nghĩa.",
        ],
        "rules_en": [
            "Never paste prose from other papers, even after translation. Outside ideas must be rewritten in your own words after careful reading, then cited.",
            "Avoid empty AI-ish fillers (“in the digital era”, “AI is booming”, “significantly improves everything”) unless tied to a pipeline number.",
            "Every empirical claim must point to a run artifact (Steps 9–11): metric table, ablation, or KG stats — never invent figures.",
            "Related work: each family (RAG / GraphRAG / Self-RAG / CRAG / CTI KG) needs at least 1–2 DOI citations; describe them in your own active voice.",
            "If overlap is suspected: restructure the paragraph, add IDS/CTI conditions, keep the citation — do not just synonym-swap.",
        ],
        "self_check_vi": [
            "Đã đọc full-text (hoặc ít nhất abstract+method+limits) của mọi citation then chốt?",
            "Abstract có nêu gap cụ thể + contribution đo được, không chỉ liệt kê module?",
            "Có đoạn “Limitations” thành thật (dataset demo, generator extractive, quy mô KG)?",
            "Đã chạy similarity/self-check nội bộ trước khi nộp (Turnitin/iThenticate theo quy định trường)?",
        ],
        "self_check_en": [
            "Have you read full text (or at least abstract+method+limits) of every key citation?",
            "Does the abstract state a concrete gap + measurable contribution, not just a module list?",
            "Is there an honest Limitations section (demo dataset, extractive generator, KG scale)?",
            "Will you run the institution’s similarity check before submission?",
        ],
    }


def _sec(
    name_vi: str,
    name_en: str,
    *,
    goal_vi: str,
    goal_en: str,
    draft_vi: str,
    draft_en: str,
    must_cite: list[str],
    artifacts: list[str],
    pitfalls_vi: str = "",
    pitfalls_en: str = "",
) -> dict[str, Any]:
    return {
        "name_vi": name_vi,
        "name_en": name_en,
        "goal_vi": goal_vi,
        "goal_en": goal_en,
        "draft_vi": draft_vi,
        "draft_en": draft_en,
        "must_cite": must_cite,
        "pipeline_artifacts": artifacts,
        "pitfalls_vi": pitfalls_vi,
        "pitfalls_en": pitfalls_en,
    }


PAPERS: dict[str, dict[str, Any]] = {
    "p1": {
        "id": 1,
        "task_id": "p1",
        "working_title": (
            "EDGR: Evidence-Driven Dynamic Graph Retrieval to Reduce Hallucinated "
            "Cyber Threat Intelligence Answers"
        ),
        "working_title_vi": (
            "EDGR: Truy hồi đồ thị động dựa trên bằng chứng nhằm giảm câu trả lời "
            "CTI bị ảo giác"
        ),
        "focus_vi": "Đóng góp thuật toán trung tâm: pipeline 6 giai + cổng risk trước khi trả lời.",
        "focus_en": "Core algorithmic contribution: six-stage pipeline + pre-answer risk gate.",
        "contribution_claim_vi": (
            "Chúng tôi đề xuất EDGR — một pipeline truy hồi có điều kiện đồ thị và thời gian, "
            "kết thúc bằng cổng rủi ro ảo giác — và chỉ ra rằng, trên cùng bộ câu hỏi IDS/CTI, "
            "việc giữ generator nhưng thay cách xây tập bằng chứng R làm giảm tỷ lệ mệnh đề "
            "không được evidence hỗ trợ so với RAG phẳng và một số biến thể graph-RAG không có cổng reject."
        ),
        "contribution_claim_en": (
            "We propose EDGR — a retrieval pipeline conditioned on graph structure and time, "
            "ending in a hallucination-risk gate — and show that, on the same IDS/CTI question set, "
            "keeping the generator while changing how evidence set R is built reduces unsupported "
            "claims relative to flat RAG and graph-RAG variants without an abstain gate."
        ),
        "abstract_draft_vi": (
            "Các trợ lý trả lời trên nguồn CTI (CVE, ATT&CK, feed) dễ đưa ra định danh hoặc quan hệ "
            "trông hợp lý nhưng không có trong bằng chứng. Retrieval-Augmented Generation giảm "
            "một phần lỗi kiến thức lỗi thời, song hàm xếp hạng đoạn văn phẳng không mã hóa cạnh "
            "quan hệ, và faithfulness thường chỉ được đo sau khi câu trả lời đã sinh. "
            "Bài báo này trình bày EDGR (Evidence-Driven Dynamic Graph Retrieval): hiểu truy vấn "
            "và trích thực thể, mở rộng đồ thị thích ứng, lọc theo tuổi bằng chứng, xếp hạng đa tín hiệu, "
            "ước lượng rủi ro ảo giác, rồi chỉ phát câu trả lời khi rủi ro dưới ngưỡng. "
            "Chúng tôi đối chiếu với nhóm baseline RAG/GraphRAG-style trên bộ QA gắn IDS/CTI, "
            "báo cáo faithfulness, hallucination rate, P@k/MRR và ablation từng module. "
            "Kết quả và hạn chế (quy mô đồ thị demo, generator ràng buộc evidence) được thảo luận "
            "như điều kiện biên của đóng góp, không như lời kết tuyệt đối."
        ),
        "abstract_draft_en": (
            "Assistants that answer over CTI sources (CVE, ATT&CK, feeds) can emit identifiers or "
            "relations that look plausible yet are unsupported. Retrieval-Augmented Generation "
            "mitigates some stale-knowledge errors, but flat passage ranking does not encode relational "
            "edges, and faithfulness is often measured only after an answer is produced. "
            "This paper presents EDGR (Evidence-Driven Dynamic Graph Retrieval): query understanding "
            "and entity extraction, adaptive graph expansion, temporal filtering, multi-signal ranking, "
            "hallucination-risk estimation, and answer emission only when risk is below a threshold. "
            "We compare against RAG/GraphRAG-style baselines on an IDS/CTI QA set, reporting "
            "faithfulness, hallucination rate, P@k/MRR, and per-module ablations. "
            "Results and limits (demo-scale graph, evidence-constrained generator) are discussed as "
            "boundary conditions of the claim, not as an absolute closing statement."
        ),
        "keywords": [
            "retrieval-augmented generation",
            "knowledge graph",
            "hallucination",
            "cyber threat intelligence",
            "intrusion detection",
        ],
        "venue_targets": [
            {"name": "ACSAC", "why_vi": "Ứng dụng bảo mật có đánh giá thực nghiệm rõ.", "why_en": "Security applications with clear empirical evaluation."},
            {"name": "RAID", "why_vi": "Thiên về hệ thống phát hiện/phản ứng xâm nhập.", "why_en": "Intrusion detection / response systems focus."},
            {"name": "IEEE TIFS", "why_vi": "Nếu đóng góp thuật toán + đánh giá đủ dày.", "why_en": "If algorithmic + evaluation depth is sufficient."},
            {"name": "arXiv cs.CR / cs.CL", "why_vi": "Bản thảo sớm để lấy phản hồi, không thay peer-review.", "why_en": "Early draft for feedback; not a peer-review substitute."},
        ],
        "maps_to_steps": [4, 9, 11, 12],
        "sections": [
            _sec(
                "1. Introduction",
                "1. Introduction",
                goal_vi="Đặt vấn đề bằng một kịch bản SOC cụ thể, không mở đầu chung chung.",
                goal_en="Frame the problem with a concrete SOC scenario, not a generic opener.",
                draft_vi=(
                    "Mở bằng tình huống: analyst hỏi về CVE-2021-44228 và chuỗi kỹ thuật khai thác; "
                    "một câu trả lời “đúng phong cách CTI” nhưng gắn nhầm TTP sẽ đẩy hướng xử lý sai. "
                    "Chỉ ra rằng chi phí của một claim sai cao hơn nhiều so với QA mở. "
                    "Nêu ngắn gap: RAG neo được tài liệu nhưng không siết quan hệ đồ thị và không có "
                    "toán tử từ chối trước khi trả lời. Kết thúc mục bằng 3 đóng góp đo được "
                    "(pipeline EDGR; so sánh baseline; ablation)."
                ),
                draft_en=(
                    "Open with a scenario: an analyst asks about CVE-2021-44228 and the exploit chain; "
                    "a CTI-sounding answer that mis-links a TTP steers response the wrong way. "
                    "Argue that the cost of one wrong claim exceeds ordinary open-domain QA. "
                    "State the gap briefly: RAG can ground documents yet neither enforces graph relations "
                    "nor provides abstention before answering. Close with three measurable contributions "
                    "(EDGR pipeline; baseline comparison; ablation)."
                ),
                must_cite=["lewis2020rag", "ji2023survey", "wagner2019cti"],
                artifacts=["Step3 goal", "Step2 gaps G1–G3"],
                pitfalls_vi="Tránh đoạn mở dài về “LLM đang thay đổi thế giới”.",
                pitfalls_en="Avoid long openers about “LLMs changing the world”.",
            ),
            _sec(
                "2. Related work",
                "2. Related work",
                goal_vi="Định vị EDGR so với từng họ phương pháp; mỗi họ một đoạn, có citation.",
                goal_en="Position EDGR against each method family; one paragraph per family, with citations.",
                draft_vi=(
                    "Chia bốn cụm: (i) RAG cổ điển và survey; (ii) GraphRAG / LightRAG / HippoRAG — mạnh quan hệ "
                    "nhưng thường thiếu cổng risk CTI; (iii) Self-RAG / CRAG — có tự phản tư/sửa retrieval "
                    "nhưng không gắn ATT&CK–CVE; (iv) CTI knowledge sharing / IDS surveys — ngữ cảnh miền. "
                    "Với mỗi cụm, viết 4–6 câu bằng lời mình: họ giải quyết gì, còn thiếu gì cho bài toán của ta. "
                    "Không sao chép câu từ abstract gốc."
                ),
                draft_en=(
                    "Use four clusters: (i) classic RAG and surveys; (ii) GraphRAG / LightRAG / HippoRAG — strong "
                    "on relations, often without a CTI risk gate; (iii) Self-RAG / CRAG — reflection/correction "
                    "without ATT&CK–CVE binding; (iv) CTI sharing / IDS surveys — domain context. "
                    "For each cluster, write 4–6 sentences in your own words: what they solve, what they miss "
                    "for our problem. Do not copy sentences from source abstracts."
                ),
                must_cite=[
                    "lewis2020rag",
                    "gao2024ragsurvey",
                    "edge2024graphrag",
                    "guo2024lightrag",
                    "gutierrez2024hipporag",
                    "asai2024selfrag",
                    "yan2024crag",
                    "strom2018attack",
                    "khraisat2019ids",
                ],
                artifacts=["Step1 topic surveys", "Step1 matrix weak pairs"],
            ),
            _sec(
                "3. Problem formulation",
                "3. Problem formulation",
                goal_vi="Phát biểu bài toán bằng ký hiệu đã dùng trong pipeline (q, R, a, F, ρ, θ).",
                goal_en="State the problem with pipeline symbols (q, R, a, F, ρ, θ).",
                draft_vi=(
                    "Cho truy vấn q và kho bằng chứng gắn KG CTI, tìm câu trả lời a sao cho các mệnh đề "
                    "trong a được tập evidence E* hỗ trợ, đồng thời ρ(a,E*) < θ. "
                    "Nêu rõ input/output và giả định (seed entity giữ lại sau lọc thời gian). "
                    "Liên kết ngắn với mô hình toán ở Step 3–4 của demo — nhưng viết lại cho paper, "
                    "không dán nguyên khối từ UI."
                ),
                draft_en=(
                    "Given query q and a CTI-KG-backed evidence store, find answer a such that claims in a "
                    "are supported by evidence set E* and ρ(a,E*) < θ. "
                    "State I/O and assumptions (query seeds retained after temporal filtering). "
                    "Link briefly to the demo’s Step 3–4 math — rewrite for the paper; do not paste the UI block."
                ),
                must_cite=["ji2023survey"],
                artifacts=["Step3 I/O", "Step4 stage math"],
            ),
            _sec(
                "4. The EDGR algorithm",
                "4. The EDGR algorithm",
                goal_vi="Mô tả 6 giai đoạn với pseudo-code và độ phức tạp; mỗi giai đoạn một subsection.",
                goal_en="Describe six stages with pseudocode and complexity; one subsection per stage.",
                draft_vi=(
                    "φ1 Understand/Extract → φ2 Expand → φ3 TemporalFilter → φ4 EvidenceRank → "
                    "φ5 HallucinationScore → φ6 RiskGate/TrustedAnswer. "
                    "Với mỗi φi: đầu vào, đầu ra, vì sao cần trong CTI, chi phí tiệm cận. "
                    "Nhấn mạnh khác RAG: không gian ứng viên là lân cận đồ thị có ngân sách hop, "
                    "và emit bị chặn khi ρ ≥ θ. Đính kèm T(n)=O(E log V) như biên phân tích, "
                    "không khẳng định “nhanh nhất mọi hệ thống”."
                ),
                draft_en=(
                    "φ1 Understand/Extract → φ2 Expand → φ3 TemporalFilter → φ4 EvidenceRank → "
                    "φ5 HallucinationScore → φ6 RiskGate/TrustedAnswer. "
                    "For each φi: inputs, outputs, why CTI needs it, asymptotic cost. "
                    "Stress the RAG contrast: candidates are a hop-budgeted graph neighborhood, "
                    "and emission is blocked when ρ ≥ θ. Attach T(n)=O(E log V) as an analysis bound, "
                    "not a claim of being “fastest everywhere”."
                ),
                must_cite=["edge2024graphrag", "gutierrez2024hipporag"],
                artifacts=["Step4 full run", "Step12 complexity"],
            ),
            _sec(
                "5. Experimental setup",
                "5. Experimental setup",
                goal_vi="Protocol tái lập được: dataset, baselines, metrics, hyper-parameters (top_k=5).",
                goal_en="Reproducible protocol: dataset, baselines, metrics, hyperparameters (top_k=5).",
                draft_vi=(
                    "Mô tả bộ QA IDS/CTI (câu hỏi, gold evidence ids, entities), cách dựng từ MITRE/CVE/… "
                    "Baseline: RAG, GraphRAG-style, LightRAG/HippoRAG/Self-RAG/CRAG theo cùng top_k. "
                    "Metric chính: faithfulness, hallucination rate, P@k, R@k, MRR, latency. "
                    "Ghi rõ top_k=5 là ngân sách evidence cuối; ứng viên nội bộ có thể lớn hơn. "
                    "Công bố seed/config đủ để người khác chạy lại pipeline demo."
                ),
                draft_en=(
                    "Describe the IDS/CTI QA set (questions, gold evidence ids, entities) and how it is built "
                    "from MITRE/CVE/…. Baselines: RAG, GraphRAG-style, LightRAG/HippoRAG/Self-RAG/CRAG at the "
                    "same top_k. Primary metrics: faithfulness, hallucination rate, P@k, R@k, MRR, latency. "
                    "State top_k=5 as the final evidence budget; internal candidates may be larger. "
                    "Publish enough seed/config for others to rerun the demo pipeline."
                ),
                must_cite=["gao2024ragsurvey"],
                artifacts=["Step7 QA", "Step9 compare", "DEFAULT_TOP_K=5"],
            ),
            _sec(
                "6. Results and ablation",
                "6. Results and ablation",
                goal_vi="Bảng số từ pipeline thật; mỗi nhận định gắn một hàng số.",
                goal_en="Tables from real pipeline runs; each claim tied to a numeric row.",
                draft_vi=(
                    "Trình bày bảng so sánh method × metric, rồi ablation (w/o temporal, w/o graph, "
                    "w/o trust, …). Viết nhận xét kiểu: “Khi tắt Expand, P@k giảm trên nhóm câu hỏi "
                    "quan hệ CVE–TTP” — chỉ khi bảng ablation hỗ trợ. "
                    "Thảo luận trường hợp EDGR không thắng: câu hỏi single-hop thuần lexical."
                ),
                draft_en=(
                    "Show method × metric tables, then ablations (w/o temporal, w/o graph, w/o trust, …). "
                    "Write claims like: “Disabling Expand lowers P@k on CVE–TTP relational questions” — "
                    "only when the ablation table supports it. "
                    "Discuss cases where EDGR does not win: purely lexical single-hop questions."
                ),
                must_cite=[],
                artifacts=["Step9 compare_all", "Step11 ablation", "Step10 metrics"],
                pitfalls_vi="Không làm tròn hoặc chỉnh số cho “đẹp hơn”.",
                pitfalls_en="Do not round or edit numbers to look nicer.",
            ),
            _sec(
                "7. Discussion, limitations, conclusion",
                "7. Discussion, limitations, conclusion",
                goal_vi="Thành thật về giới hạn; kết luận đúng với evidence đã trình bày.",
                goal_en="Be honest about limits; conclude only what the evidence showed.",
                draft_vi=(
                    "Limitations: KG và corpus demo chưa phải production SOC; generator trong demo "
                    "ràng buộc evidence (không phải LLM API tùy ý); nhãn faithfulness tự động có nhiễu. "
                    "Kết luận nhắc lại contribution claim và hướng mở (học θ, mở rộng nguồn feed)."
                ),
                draft_en=(
                    "Limitations: demo KG/corpus are not a production SOC; the demo generator is "
                    "evidence-constrained (not an arbitrary LLM API); automatic faithfulness labels are noisy. "
                    "Conclude by restating the contribution claim and future work (learn θ, broaden feeds)."
                ),
                must_cite=[],
                artifacts=["Step12 threats/scalability notes"],
            ),
        ],
        "novelty_bullets_vi": [
            "Cổng ρ trước emit — khác các hệ chỉ tối ưu retrieval rồi sinh tự do.",
            "Lọc thời gian giữ seed truy vấn — phù hợp CVE lịch sử vẫn còn liên quan vận hành.",
            "Ablation gắn từng module φi, không chỉ báo cáo “EDGR tốt hơn” một dòng.",
        ],
        "novelty_bullets_en": [
            "ρ-gate before emit — unlike systems that only optimize retrieval then freely generate.",
            "Temporal filter that keeps query seeds — historical CVEs may still matter operationally.",
            "Ablations tied to each φi module, not a one-line “EDGR is better” claim.",
        ],
    },
    "p2": {
        "id": 2,
        "task_id": "p2",
        "working_title": "Incremental Dynamic Knowledge Graphs for Retrieving Cyber Threat Intelligence",
        "working_title_vi": "Đồ thị tri thức động cập nhật gia tăng cho truy hồi tình báo mối đe dọa",
        "focus_vi": "Biểu diễn CTI dạng KG, ingest đa nguồn, cập nhật ΔV/ΔE, lưu trữ và truy vấn.",
        "focus_en": "CTI-as-KG representation, multi-source ingest, ΔV/ΔE updates, storage and query.",
        "contribution_claim_vi": (
            "Chúng tôi mô tả một đồ thị CTI cập nhật gia tăng từ ATT&CK/CVE/CWE/CISA và evidence chunks, "
            "và chỉ ra rằng truy hồi có Expand trên đồ thị này cung cấp ngữ cảnh quan hệ mà kho đoạn văn "
            "phẳng không giữ được — làm nền cho EDGR chứ không thay thế toàn bộ bài toán chấm điểm ảo giác."
        ),
        "contribution_claim_en": (
            "We describe an incremental CTI graph built from ATT&CK/CVE/CWE/CISA and evidence chunks, "
            "and show that Expand-based retrieval on this graph supplies relational context that a flat "
            "passage store does not retain — a foundation for EDGR, not a replacement for hallucination scoring."
        ),
        "abstract_draft_vi": (
            "Tri thức CTI vốn là quan hệ: CVE kích hoạt kỹ thuật, kỹ thuật gắn tactic, actor dùng malware. "
            "Khi chỉ index đoạn văn, các cạnh này dễ mất. Bài báo tập trung lớp Dynamic Knowledge Graph: "
            "schema thực thể/quan hệ, đường ống trích xuất, cập nhật gia tăng khi có intel mới, "
            "và hình dạng lưu trữ/truy vấn dùng cho retrieval. "
            "Chúng tôi minh họa bằng thống kê đồ thị sống và case study truy vấn CVE–TTP, "
            "đồng thời nêu rõ ranh giới: chất lượng IE và độ trễ cập nhật vẫn là rủi ro vận hành."
        ),
        "abstract_draft_en": (
            "CTI knowledge is relational: CVEs enable techniques, techniques map to tactics, actors use malware. "
            "Passage-only indexes often drop those edges. This paper focuses on the Dynamic Knowledge Graph layer: "
            "entity/relation schema, extraction pipeline, incremental updates when intel arrives, "
            "and the storage/query shape used for retrieval. "
            "We illustrate with live graph statistics and a CVE–TTP query case study, "
            "and state boundaries clearly: IE quality and update lag remain operational risks."
        ),
        "keywords": [
            "knowledge graph",
            "cyber threat intelligence",
            "incremental update",
            "ATT&CK",
            "CVE",
        ],
        "venue_targets": [
            {"name": "Computers & Security", "why_vi": "Hợp bài hệ thống/tri thức bảo mật.", "why_en": "Fits security systems/knowledge papers."},
            {"name": "Journal of Information Security and Applications", "why_vi": "Ứng dụng CTI/IDS.", "why_en": "CTI/IDS applications."},
            {"name": "arXiv cs.CR", "why_vi": "Bản thảo kỹ thuật sớm.", "why_en": "Early technical preprint."},
        ],
        "maps_to_steps": [5, 7],
        "sections": [
            _sec(
                "1. Introduction",
                "1. Introduction",
                goal_vi="Vì sao CTI cần đồ thị, không chỉ corpus văn bản.",
                goal_en="Why CTI needs a graph, not only a text corpus.",
                draft_vi=(
                    "Lấy ví dụ chuỗi CVE→T1190→exploit public-facing app. "
                    "Nếu hệ chỉ retrieve đoạn chứa tên CVE, có thể bỏ mất cạnh “enables”. "
                    "Đặt contribution: schema + incremental update + retrieval interface cho EDGR."
                ),
                draft_en=(
                    "Use the CVE→T1190→exploit-public-facing-app chain. "
                    "If the system only retrieves passages naming the CVE, the “enables” edge may vanish. "
                    "State contribution: schema + incremental update + retrieval interface for EDGR."
                ),
                must_cite=["wagner2019cti", "strom2018attack", "peng2023kgllm"],
                artifacts=["Step5 sources", "Step5 extract"],
            ),
            _sec(
                "2. CTI sources and schema",
                "2. CTI sources and schema",
                goal_vi="Bảng nguồn → loại đỉnh/cạnh; nêu trường timestamp và reliability.",
                goal_en="Table of sources → node/edge types; include timestamp and reliability fields.",
                draft_vi=(
                    "ATT&CK (technique/tactic), NVD/CVE, CWE/CAPEC, CISA KEV, IDS logs/evidence chunks. "
                    "Schema: (u,r,v) kèm timestamp, reliability. "
                    "Giải thích vì sao thiếu timestamp làm hỏng TemporalFilter ở EDGR."
                ),
                draft_en=(
                    "ATT&CK (technique/tactic), NVD/CVE, CWE/CAPEC, CISA KEV, IDS logs/evidence chunks. "
                    "Schema: (u,r,v) with timestamp and reliability. "
                    "Explain why missing timestamps break EDGR’s TemporalFilter."
                ),
                must_cite=["strom2018attack"],
                artifacts=["Step7 ingest_*"],
            ),
            _sec(
                "3. Incremental update model",
                "3. Incremental update model",
                goal_vi="Định nghĩa ΔV, ΔE; quy trình upsert; ví dụ thêm CVE mới.",
                goal_en="Define ΔV, ΔE; upsert procedure; example of adding a new CVE.",
                draft_vi=(
                    "Khi có node/edge mới, cập nhật G ← G ∪ Δ mà không rebuild toàn bộ. "
                    "Minh họa bằng thao tác incremental_update trong demo (CVE mới → cạnh tới TTP). "
                    "Thảo luận xung đột trùng id và cần idempotent writes."
                ),
                draft_en=(
                    "When new nodes/edges arrive, update G ← G ∪ Δ without full rebuild. "
                    "Illustrate with the demo’s incremental_update (new CVE → edge to a TTP). "
                    "Discuss id collisions and the need for idempotent writes."
                ),
                must_cite=["peng2023kgllm"],
                artifacts=["Step5 update", "kg.stats before/after"],
            ),
            _sec(
                "4. Storage, query, case study",
                "4. Storage, query, case study",
                goal_vi="API subgraph/expand; case study một truy vấn; số liệu V/E sống.",
                goal_en="Subgraph/expand API; one query case study; live V/E stats.",
                draft_vi=(
                    "Mô tả lưu trữ in-process (NetworkX) và hình dạng xuất Neo4j-compatible. "
                    "Case study: extract_graph trên câu hỏi Log4Shell — vẽ subgraph, đếm quan hệ. "
                    "Không phóng đại “realtime toàn cầu” nếu demo chỉ là in-process."
                ),
                draft_en=(
                    "Describe in-process storage (NetworkX) and Neo4j-compatible export shape. "
                    "Case study: extract_graph on a Log4Shell question — draw the subgraph, count relations. "
                    "Do not overclaim “global realtime” for an in-process demo."
                ),
                must_cite=["edge2024graphrag"],
                artifacts=["Step5 store", "Step5 extract viz", "/api/kg"],
            ),
            _sec(
                "5. Limits and outlook",
                "5. Limits and outlook",
                goal_vi="IE lỗi, stale feeds, chi phí duy trì — và liên hệ Paper 1/3.",
                goal_en="IE errors, stale feeds, maintenance cost — link to Papers 1/3.",
                draft_vi=(
                    "KG tốt không đủ nếu không có ranking/risk (Paper 3) và đánh giá (Paper 4). "
                    "Hướng tới: entity linking chặt hơn, đồng bộ TAXII, đo độ trễ cập nhật."
                ),
                draft_en=(
                    "A good KG is insufficient without ranking/risk (Paper 3) and evaluation (Paper 4). "
                    "Next: tighter entity linking, TAXII sync, measuring update lag."
                ),
                must_cite=[],
                artifacts=["Step5 limitations notes"],
            ),
        ],
        "novelty_bullets_vi": [
            "Schema CTI có timestamp/reliability phục vụ trực tiếp TemporalFilter và trust.",
            "Cập nhật gia tăng có minh chứng trước/sau trên KG sống của demo.",
        ],
        "novelty_bullets_en": [
            "CTI schema with timestamp/reliability feeds TemporalFilter and trust directly.",
            "Incremental updates evidenced by before/after stats on the live demo KG.",
        ],
    },
    "p3": {
        "id": 3,
        "task_id": "p3",
        "working_title": "Four-Factor Hallucination Risk Scoring for Trusted CTI Answers",
        "working_title_vi": "Chấm điểm rủi ro ảo giác bốn yếu tố cho câu trả lời CTI đáng tin",
        "focus_vi": "Reliability, freshness, graph consistency, semantic relevance → ρ và cổng θ.",
        "focus_en": "Reliability, freshness, graph consistency, semantic relevance → ρ and threshold θ.",
        "contribution_claim_vi": (
            "Chúng tôi cụ thể hóa một hàm rủi ro ảo giác tổ hợp bốn tín hiệu quan sát được trên evidence "
            "và đồ thị, rồi dùng ngưỡng θ để quyết định trả lời hoặc báo insufficient evidence — "
            "chuyển faithfulness từ thước đo hậu kiểm thành một phần của vòng điều khiển."
        ),
        "contribution_claim_en": (
            "We instantiate a hallucination-risk function from four observable evidence/graph signals "
            "and use threshold θ to answer or return insufficient evidence — moving faithfulness from a "
            "post-hoc metric into the control loop."
        ),
        "abstract_draft_vi": (
            "Nhiều hệ RAG báo cáo faithfulness sau khi đã trả lời. Trong SOC, điều đó muộn. "
            "Bài báo này tách lớp chấm điểm: độ tin cậy nguồn, độ mới, nhất quán đồ thị, liên quan ngữ nghĩa; "
            "tổ hợp thành ρ; và mô tả cổng quyết định gắn EDGR. "
            "Chúng tôi trình bày trọng số dùng trong demo, ví dụ chấm trên evidence của một truy vấn CTI, "
            "và thảo luận độ nhạy của θ. Đóng góp nằm ở chỗ đưa tín hiệu miền bảo mật vào quyết định emit, "
            "không phải ở việc “phát minh” thêm một tên gọi cho cosine similarity."
        ),
        "abstract_draft_en": (
            "Many RAG systems report faithfulness only after answering. In a SOC, that is late. "
            "This paper isolates the scoring layer: source reliability, freshness, graph consistency, "
            "semantic relevance; aggregates them into ρ; and describes the decision gate used by EDGR. "
            "We present demo weights, a scored evidence example for a CTI query, and discuss θ sensitivity. "
            "The contribution is putting security-domain signals into the emit decision — not renaming "
            "cosine similarity."
        ),
        "keywords": [
            "hallucination",
            "faithfulness",
            "trust scoring",
            "cybersecurity QA",
            "risk gate",
        ],
        "venue_targets": [
            {"name": "EMNLP Findings / ACL workshops", "why_vi": "Thiên NLP về hallucination/evaluation.", "why_en": "NLP venues for hallucination/evaluation."},
            {"name": "IEEE Access", "why_vi": "Nếu nhấn ứng dụng CTI + công thức rõ.", "why_en": "If CTI application + clear formulas are emphasized."},
        ],
        "maps_to_steps": [6, 10],
        "sections": [
            _sec(
                "1. Introduction",
                "1. Introduction",
                goal_vi="Hậu kiểm F là chưa đủ cho quyết định vận hành.",
                goal_en="Post-hoc F is not enough for operational decisions.",
                draft_vi=(
                    "Phân biệt intrinsic/extrinsic hallucination (đọc Ji et al., viết lại bằng lời mình). "
                    "Trong CTI, extrinsic hallucination gắn CVE/TTP đặc biệt nguy hiểm. "
                    "Đặt câu hỏi nghiên cứu: tín hiệu nào quan sát được trước khi emit?"
                ),
                draft_en=(
                    "Distinguish intrinsic/extrinsic hallucination (read Ji et al.; rewrite in your words). "
                    "In CTI, extrinsic hallucinations about CVE/TTP are especially costly. "
                    "Research question: which signals are observable before emit?"
                ),
                must_cite=["ji2023survey", "huang2025hallu"],
                artifacts=["Step6 scoring overview"],
            ),
            _sec(
                "2. Four factors",
                "2. Four factors",
                goal_vi="Định nghĩa R, F_fresh, C_graph, S_sem; miền giá trị; trực giác CTI.",
                goal_en="Define R, F_fresh, C_graph, S_sem; ranges; CTI intuition.",
                draft_vi=(
                    "Reliability: nguồn NVD/ATT&CK vs blog chưa kiểm chứng. "
                    "Freshness: tuổi evidence so với cửa sổ τ. "
                    "Graph consistency: thực thể trong chunk có nối trong KG không. "
                    "Semantic relevance: khớp q. "
                    "Công thức tổ hợp ρ — nêu trọng số demo, nhấn là hyper-parameter, có thể học sau."
                ),
                draft_en=(
                    "Reliability: NVD/ATT&CK vs unchecked blogs. "
                    "Freshness: evidence age vs window τ. "
                    "Graph consistency: whether chunk entities connect in the KG. "
                    "Semantic relevance: match to q. "
                    "Aggregate ρ — state demo weights; stress they are hyperparameters, possibly learned later."
                ),
                must_cite=["asai2024selfrag", "yan2024crag"],
                artifacts=["Step6 factor_*", "HallucinationScorer.WEIGHTS"],
            ),
            _sec(
                "3. Gate and selection",
                "3. Gate and selection",
                goal_vi="Từ ranked evidence → ρ → emit/reject; liên hệ top_k.",
                goal_en="From ranked evidence → ρ → emit/reject; relate to top_k.",
                draft_vi=(
                    "E* = top_k evidence sau rank; ρ ước lượng trên (q,E*); nếu ρ≥θ trả insufficient evidence. "
                    "Giải thích vì sao reject cũng là kết quả đúng trong SOC."
                ),
                draft_en=(
                    "E* = top_k evidence after ranking; ρ estimated on (q,E*); if ρ≥θ return insufficient evidence. "
                    "Explain why reject is a correct SOC outcome."
                ),
                must_cite=[],
                artifacts=["Step4 s5–s6", "top_k=5"],
            ),
            _sec(
                "4. Empirical signals",
                "4. Empirical signals",
                goal_vi="Bảng score mẫu; tương quan với faithfulness ở Step 10 (cẩn thận overclaim).",
                goal_en="Sample score table; correlate with Step 10 faithfulness (avoid overclaim).",
                draft_vi=(
                    "Đưa 1 bảng evidence đã chấm từ pipeline. "
                    "Nếu có tương quan với F, nêu rõ cỡ mẫu nhỏ — đây là tín hiệu định hướng, "
                    "chưa phải chứng minh nhân quả quy mô lớn."
                ),
                draft_en=(
                    "Include one scored-evidence table from the pipeline. "
                    "If correlating with F, state the small sample — directional evidence, "
                    "not large-scale causal proof."
                ),
                must_cite=[],
                artifacts=["Step6 composite_score", "Step10 faith/hall"],
            ),
            _sec(
                "5. Limitations",
                "5. Limitations",
                goal_vi="Trọng số thủ công; nhãn tự động; phụ thuộc KG sạch.",
                goal_en="Manual weights; automatic labels; dependence on a clean KG.",
                draft_vi="Nêu hướng học trọng số và đánh giá người (analyst study) nếu có điều kiện.",
                draft_en="Point to learning weights and human (analyst) studies when feasible.",
                must_cite=[],
                artifacts=[],
            ),
        ],
        "novelty_bullets_vi": [
            "Đưa ρ vào vòng điều khiển, không chỉ dashboard sau cùng.",
            "Tín hiệu graph consistency gắn KG CTI — khác scoring thuần lexical.",
        ],
        "novelty_bullets_en": [
            "Puts ρ into the control loop, not only a final dashboard.",
            "Graph-consistency signal tied to a CTI KG — unlike purely lexical scoring.",
        ],
    },
    "p4": {
        "id": 4,
        "task_id": "p4",
        "working_title": (
            "An Empirical Study of Graph-Augmented Retrieval for IDS/CTI Question Answering"
        ),
        "working_title_vi": (
            "Nghiên cứu thực nghiệm truy hồi tăng cường đồ thị cho hỏi–đáp IDS/CTI"
        ),
        "focus_vi": "Protocol đánh giá, metric, baseline, ablation, tài nguyên, threats to validity.",
        "focus_en": "Evaluation protocol, metrics, baselines, ablations, resources, threats to validity.",
        "contribution_claim_vi": (
            "Chúng tôi cung cấp một protocol đánh giá tái lập được cho trợ lý IDS/CTI dựa trên retrieval, "
            "gồm cách dựng QA, bộ metric trung thực/ảo giác/truy hồi/hiệu năng, và ablation theo thành phần — "
            "để các phương pháp (gồm EDGR) có thể so sánh trên cùng điều kiện thay vì báo cáo rời rạc."
        ),
        "contribution_claim_en": (
            "We provide a reproducible evaluation protocol for retrieval-based IDS/CTI assistants, "
            "including QA construction, faithfulness/hallucination/retrieval/performance metrics, "
            "and component ablations — so methods (including EDGR) can be compared under shared conditions "
            "rather than fragmented reporting."
        ),
        "abstract_draft_vi": (
            "So sánh hệ RAG trong bảo mật thường khó đọc lại: khác dataset, khác định nghĩa hallucination, "
            "khác top_k. Bài báo này không cố “giành mọi SOTA”; mục tiêu là làm rõ protocol. "
            "Chúng tôi mô tả bộ QA gắn evidence CTI, cách chạy baseline và EDGR, "
            "các metric dùng trong pipeline, và bảng tổng hợp từ lần chạy demo. "
            "Phần threats to validity nêu giới hạn quy mô và độ tin cậy nhãn — "
            "để hội đồng và reviewer thấy ranh giới kết luận."
        ),
        "abstract_draft_en": (
            "Security RAG comparisons are often hard to replay: different datasets, different hallucination "
            "definitions, different top_k. This paper does not try to “claim all SOTA”; it clarifies protocol. "
            "We describe a CTI-evidence QA set, how baselines and EDGR are run, the metrics used in the pipeline, "
            "and summary tables from the demo runs. "
            "Threats to validity spell out scale and label reliability limits — so committees and reviewers "
            "see the boundary of the conclusions."
        ),
        "keywords": [
            "evaluation",
            "ablation study",
            "RAG benchmarks",
            "IDS",
            "CTI",
        ],
        "venue_targets": [
            {"name": "Empirical / measurement workshops", "why_vi": "Hợp bài protocol + số liệu.", "why_en": "Fits protocol + measurement papers."},
            {"name": "DIMVA / poster tracks", "why_vi": "Nếu nhấn case study bảo mật.", "why_en": "If security case-study angle is emphasized."},
            {"name": "Companion to Paper 1", "why_vi": "Có thể rút gọn thành section Evaluation của Paper 1 nếu venue yêu cầu một bài duy nhất.", "why_en": "May collapse into Paper 1’s Evaluation section if the venue wants a single paper."},
        ],
        "maps_to_steps": [7, 9, 10, 11],
        "sections": [
            _sec(
                "1. Why another evaluation paper?",
                "1. Why another evaluation paper?",
                goal_vi="Động lực: tái lập và so sánh công bằng trong miền CTI.",
                goal_en="Motivation: reproducibility and fair comparison in CTI.",
                draft_vi=(
                    "Chỉ ra 3 lệch phổ biến trong báo cáo RAG bảo mật: (1) metric không định nghĩa; "
                    "(2) không ablation; (3) không công bố cấu hình top_k/time window. "
                    "Paper này sửa ở mức protocol của demo luận án."
                ),
                draft_en=(
                    "Call out three common gaps in security RAG reports: (1) undefined metrics; "
                    "(2) no ablation; (3) unpublished top_k/time-window configs. "
                    "This paper fixes them at the level of the thesis demo protocol."
                ),
                must_cite=["gao2024ragsurvey", "ji2023survey"],
                artifacts=["Step10 metric list"],
            ),
            _sec(
                "2. Dataset construction",
                "2. Dataset construction",
                goal_vi="Từ nguồn Step 7 → QA pairs; thống kê quy mô; hạn chế nhãn.",
                goal_en="From Step 7 sources → QA pairs; scale stats; label limits.",
                draft_vi=(
                    "Mô tả gold_answer, gold_entities, gold_evidence_ids. "
                    "Nêu số câu hỏi hiện có và rằng đây là bộ định hướng, cần mở rộng trước production claim."
                ),
                draft_en=(
                    "Describe gold_answer, gold_entities, gold_evidence_ids. "
                    "State current question count and that this is a directional set — expand before production claims."
                ),
                must_cite=["strom2018attack", "khraisat2019ids"],
                artifacts=["Step7 build_qa", "QA_DATASET"],
            ),
            _sec(
                "3. Metrics and protocol",
                "3. Metrics and protocol",
                goal_vi="Định nghĩa F, H, P@k, MRR, latency; cố định top_k=5.",
                goal_en="Define F, H, P@k, MRR, latency; fix top_k=5.",
                draft_vi=(
                    "Viết công thức ngắn + cách đo trong code evaluation_service. "
                    "Tách metric chất lượng trả lời và metric hệ thống (GPU/memory nếu đo được)."
                ),
                draft_en=(
                    "Short formulas + how evaluation_service measures them. "
                    "Separate answer-quality metrics from system metrics (GPU/memory when measured)."
                ),
                must_cite=[],
                artifacts=["Step10 *", "DEFAULT_TOP_K"],
            ),
            _sec(
                "4. Baselines, results, ablations",
                "4. Baselines, results, ablations",
                goal_vi="Bảng từ Step 9 và 11; không chỉnh tay.",
                goal_en="Tables from Steps 9 and 11; no hand editing.",
                draft_vi=(
                    "Mỗi baseline một câu mô tả cách chạy trong demo (không bịa kiến trúc ngoài code). "
                    "Ablation: tắt từng thành phần EDGR, đọc delta metric."
                ),
                draft_en=(
                    "One sentence per baseline on how the demo runs it (do not invent architectures absent from code). "
                    "Ablation: disable each EDGR component, report metric deltas."
                ),
                must_cite=["lewis2020rag", "edge2024graphrag", "asai2024selfrag", "yan2024crag"],
                artifacts=["Step9 compare_all", "Step11 ablate"],
            ),
            _sec(
                "5. Threats to validity",
                "5. Threats to validity",
                goal_vi="Internal/external/construct validity — văn phong hội đồng thích ở đây.",
                goal_en="Internal/external/construct validity — committees expect this.",
                draft_vi=(
                    "Internal: nhãn tự động, seed ngẫu nhiên. "
                    "External: khác SOC thật, khác ngôn ngữ alert. "
                    "Construct: F xấp xỉ có thể không trùng đánh giá analyst. "
                    "Không giấu; đề xuất cách giảm đe dọa (thêm annotator, mở dataset)."
                ),
                draft_en=(
                    "Internal: automatic labels, RNG seeds. "
                    "External: not a live SOC; alert language differs. "
                    "Construct: approximate F may diverge from analyst judgments. "
                    "Do not hide these; propose mitigations (more annotators, larger dataset)."
                ),
                must_cite=[],
                artifacts=["Step12 scalability/correctness notes"],
            ),
        ],
        "novelty_bullets_vi": [
            "Protocol gắn trực tiếp pipeline luận án — reviewer có thể đối chiếu code/demo.",
            "Threats to validity viết đủ để bảo vệ trước hội đồng, không “né” hạn chế.",
        ],
        "novelty_bullets_en": [
            "Protocol tied to the thesis pipeline — reviewers can cross-check the demo/code.",
            "Threats to validity written for committee defense, not to hide limits.",
        ],
    },
}


def publication_plan_doc() -> dict[str, Any]:
    return {
        "kind": "publication_plan",
        "strategy_vi": (
            "Thứ tự nộp nên theo độ “chín” của đóng góp và phụ thuộc dữ liệu: "
            "Paper 1 (EDGR) khi đã có so sánh + ablation ổn định; "
            "Paper 2 (KG) có thể song song sớm vì ít phụ thuộc metric sinh; "
            "Paper 3 (scoring) sau khi trọng số/ρ ổn; "
            "Paper 4 (evaluation) đóng gói protocol — hoặc rút thành mục Evaluation của Paper 1 "
            "nếu chỉ tiêu một bài duy nhất cho một milestone."
        ),
        "strategy_en": (
            "Submission order should follow contribution maturity and data dependence: "
            "Paper 1 (EDGR) once comparison + ablation are stable; "
            "Paper 2 (KG) can proceed early because it depends less on generation metrics; "
            "Paper 3 (scoring) after weights/ρ stabilize; "
            "Paper 4 (evaluation) packages the protocol — or collapses into Paper 1’s Evaluation "
            "section if a milestone allows only one paper."
        ),
        "overlap_control_vi": (
            "Tránh tự đạo văn giữa các bài: Paper 1 giữ thuật toán+kết quả chính; "
            "Paper 2 không lặp pseudo-code EDGR đầy đủ — chỉ interface Expand; "
            "Paper 3 không lặp toàn bộ baseline tables — chỉ bảng score/ρ; "
            "Paper 4 được phép trùng bảng nếu là bài protocol, nhưng phải viết lại lời dẫn."
        ),
        "overlap_control_en": (
            "Avoid self-plagiarism across papers: Paper 1 keeps algorithm + main results; "
            "Paper 2 must not repeat full EDGR pseudocode — only the Expand interface; "
            "Paper 3 must not repeat full baseline tables — only score/ρ tables; "
            "Paper 4 may reuse tables as a protocol paper, but the surrounding prose must be rewritten."
        ),
        "timeline_hint": [
            {"phase": "M1–M6", "output_vi": "Paper 1: draft method + experiments", "output_en": "Paper 1: method draft + experiments"},
            {"phase": "M3–M8", "output_vi": "Paper 2: KG schema + incremental case study", "output_en": "Paper 2: KG schema + incremental case study"},
            {"phase": "M6–M11", "output_vi": "Paper 3: scoring model + gate analysis", "output_en": "Paper 3: scoring model + gate analysis"},
            {"phase": "M9–M14", "output_vi": "Paper 4: protocol package / hoặc gộp vào P1", "output_en": "Paper 4: protocol package / or merge into P1"},
        ],
        "committee_readiness_vi": [
            "Mỗi paper có contribution claim một câu, kiểm chứng được.",
            "Related work có citation thật, paraphrase bằng lời mình.",
            "Limitations không trống.",
            "Số liệu lấy từ pipeline, không minh họa tay.",
            "Đã lên lịch similarity check trước nộp.",
        ],
        "committee_readiness_en": [
            "Each paper has a one-sentence, testable contribution claim.",
            "Related work uses real citations, paraphrased in your voice.",
            "Limitations are non-empty.",
            "Numbers come from the pipeline, not hand-drawn demos.",
            "Similarity check scheduled before submission.",
        ],
        "integrity": _integrity(),
    }


def get_paper_package(task_id: str) -> dict[str, Any] | None:
    paper = PAPERS.get(task_id)
    if not paper:
        return None
    out = dict(paper)
    out["kind"] = "publication_manuscript"
    out["integrity"] = _integrity()
    out["status"] = "outline_ready"
    out["how_to_use_vi"] = (
        "Đây là khung viết + đoạn nháp định hướng. Hãy viết lại toàn bộ bằng giọng của bạn, "
        "bổ sung số liệu sau khi Chạy các bước 9–11, và đọc kỹ mọi citation trước khi paraphrase."
    )
    out["how_to_use_en"] = (
        "This is a writing frame plus directional draft notes. Rewrite everything in your voice, "
        "fill numbers after running Steps 9–11, and read each citation carefully before paraphrasing."
    )
    return out


def academic_overlay_for_paper(task_id: str) -> dict[str, Any] | None:
    """Standalone academic package fragment for Step-13 paper tabs."""
    paper = get_paper_package(task_id)
    if not paper:
        return None
    title = paper["working_title"]
    return {
        "_standalone_task": True,
        "scientific_sequence_vi": [
            {
                "id": "theory",
                "title_vi": "Vai trò bài báo trong luận án",
                "title_en": "Role of this paper in the thesis",
                "explain_vi": paper["focus_vi"],
                "explain_en": paper["focus_en"],
                "anchor": "sci-theory",
            },
            {
                "id": "claim",
                "title_vi": "Contribution claim (một câu)",
                "title_en": "Contribution claim (one sentence)",
                "explain_vi": "Mọi mục sau phải phục vụ câu claim này; không viết lan man.",
                "explain_en": "Every later section must serve this claim; avoid sprawl.",
                "anchor": "sci-purpose",
            },
            {
                "id": "structure",
                "title_vi": "Cấu trúc section + đoạn nháp",
                "title_en": "Section structure + draft notes",
                "explain_vi": "Viết theo section; mỗi section có goal, draft, citation, artifact pipeline.",
                "explain_en": "Write section-by-section; each has goal, draft, citations, pipeline artifacts.",
                "anchor": "sci-ops",
            },
            {
                "id": "integrity",
                "title_vi": "Kỷ luật chống đạo văn",
                "title_en": "Anti-plagiarism discipline",
                "explain_vi": "Paraphrase sau khi đọc; không dán dịch; số liệu từ pipeline.",
                "explain_en": "Paraphrase after reading; no paste-translate; numbers from the pipeline.",
                "anchor": "sci-ev",
            },
        ],
        "scientific_sequence_en": None,  # filled same list bilingual fields
        "csdl": {
            "name_vi": f"Gói công bố — {task_id}",
            "name_en": f"Publication package — {task_id}",
            "explain_vi": "Lưu outline, venue, maps_to_steps, live_artifacts sau khi Chạy.",
            "explain_en": "Stores outline, venues, maps_to_steps, live_artifacts after Run.",
            "tables_vi": ["paper_outline", "venue_targets", "section_drafts"],
            "tables_en": ["paper_outline", "venue_targets", "section_drafts"],
            "role_vi": "Nguồn cho manuscript và kế hoạch nộp.",
            "role_en": "Source for the manuscript and submission plan.",
        },
        "mo_hinh_toan": {
            "lang": "vi-en",
            "role_vi": "Ánh xạ hình thức: Paper ↔ Contribution ↔ Steps ↔ Artifacts.",
            "role_en": "Formal map: Paper ↔ Contribution ↔ Steps ↔ Artifacts.",
            "narrative_vi": (
                f"Bài «{title}» đóng gói một contribution claim. "
                "Không có công thức “ảo” thay cho nội dung: chất lượng paper = rõ claim + "
                "related work trung thực + artifact đo được từ pipeline."
            ),
            "narrative_en": (
                f"The paper «{title}» packages one contribution claim. "
                "There is no fake formula substituting for substance: paper quality = clear claim + "
                "honest related work + measurable pipeline artifacts."
            ),
            "formulas": [
                {
                    "id": "map",
                    "label_vi": "Ánh xạ công bố",
                    "label_en": "Publication mapping",
                    "latex": r"\mathrm{Paper}\leftrightarrow \mathrm{Claim}\leftrightarrow \mathrm{Steps}(S)\leftrightarrow \mathrm{Artifacts}",
                    "explain_vi": "Mỗi mũi tên phải kiểm chứng được trong repo/demo.",
                    "explain_en": "Each arrow must be checkable in the repo/demo.",
                    "variables": [],
                    "optimize_vi": "Tốt khi Chạy tab gắn được live_artifacts (metrics/KG).",
                    "optimize_en": "Good when Run attaches live_artifacts (metrics/KG).",
                }
            ],
        },
        "mo_hinh_thuat_toan": {
            "name_vi": "Quy trình viết manuscript (không phải thuật toán EDGR)",
            "name_en": "Manuscript writing procedure (not the EDGR algorithm)",
            "math_ids": ["map"],
            "pseudocode": [
                "Chốt contribution claim một câu",
                "Lập outline section + artifact cần có",
                "Đọc citation then chốt → paraphrase",
                "Chạy pipeline lấy số liệu → điền Results",
                "Viết Limitations thành thật",
                "Self-check đạo văn / AI-tone / số liệu bịa",
            ],
            "complexity": r"O(\mathrm{sections}\cdot \mathrm{revision\ rounds})",
            "narrative_vi": (
                "“Thuật toán” ở đây là quy trình biên tập khoa học. "
                "Hội đồng đọc mạch lập luận; họ không cần văn hoa. "
                "Giữ câu ngắn khi nêu số; giữ câu dài khi biện minh giả định."
            ),
            "narrative_en": (
                "The “algorithm” here is the scholarly editing process. "
                "Committees read argument structure; they do not need ornament. "
                "Keep sentences short when stating numbers; longer when justifying assumptions."
            ),
            "pros_vi": ["Tách claim khỏi prose trang trí", "Bám artifact thật"],
            "pros_en": ["Separates claim from ornamental prose", "Tied to real artifacts"],
            "cons_vi": ["Tốn thời gian đọc full-text citation", "Không thay peer-review"],
            "cons_en": ["Costly citation reading", "Not a peer-review substitute"],
            "improve_algo_vi": ["Thêm checklist reviewer giả định trước khi nộp"],
            "improve_algo_en": ["Add an adversarial-reviewer checklist before submit"],
            "improve_math_vi": [],
            "improve_math_en": [],
        },
        "mo_hinh_hoat_dong": {
            # Full manuscript outline for design reading (AcademicPanel).
            # After Run, Results shows live_artifacts only — not a second full draft.
            "kind": "publication_manuscript",
            "working_title": paper["working_title"],
            "working_title_vi": paper.get("working_title_vi"),
            "contribution_claim_vi": paper["contribution_claim_vi"],
            "contribution_claim_en": paper["contribution_claim_en"],
            "abstract_draft_vi": paper.get("abstract_draft_vi"),
            "abstract_draft_en": paper.get("abstract_draft_en"),
            "keywords": paper.get("keywords", []),
            "venue_targets": paper.get("venue_targets", []),
            "maps_to_steps": paper.get("maps_to_steps", []),
            "novelty_bullets_vi": paper.get("novelty_bullets_vi", []),
            "novelty_bullets_en": paper.get("novelty_bullets_en", []),
            "sections": paper.get("sections", []),
            "integrity": paper.get("integrity"),
            "how_to_use_vi": (
                paper["how_to_use_vi"]
                + " Sau Chạy, khối Kết quả chỉ gắn live_artifacts (không lặp lại toàn văn manuscript)."
            ),
            "how_to_use_en": (
                paper["how_to_use_en"]
                + " After Run, Results attaches live_artifacts only (does not repeat the full manuscript)."
            ),
            "flow": [
                "Đọc theory + contribution claim",
                "Duyệt sections (goal → draft → cite → artifacts)",
                "Chạy tab để gắn live_artifacts ở Kết quả",
                "Áp integrity checklist",
                "Chuyển draft sang LaTeX/Word của venue",
            ],
            "explain_vi": paper["how_to_use_vi"],
            "explain_en": paper["how_to_use_en"],
            "io": {
                "in": "pipeline artifacts + citations",
                "out": "manuscript outline + draft notes",
            },
        },
        "minh_chung": {
            "claim_vi": (
                f"Tab «{task_id}»: sau Chạy phải thấy live_artifacts (metrics/KG/weights) khớp đóng góp bài."
            ),
            "claim_en": (
                f"Tab «{task_id}»: after Run, live_artifacts (metrics/KG/weights) must match the paper’s contribution."
            ),
            "explain_vi": (
                "Outline/claim nằm ở Mô hình hoạt động phía trên. Minh chứng runtime = live_artifacts sau Chạy. "
                "Không dùng số minh họa tay."
            ),
            "explain_en": (
                "Outline/claim is in the Operating model above. Runtime evidence = live_artifacts after Run. "
                "Do not use hand-drawn numbers."
            ),
            "logic_vi": "Đọc outline → Chạy → live_artifacts → điền Results/Limitations.",
            "logic_en": "Read outline → Run → live_artifacts → fill Results/Limitations.",
            "paper": task_id,
        },
        "nhan_dinh_danh_gia": {
            "strength": (
                "Có claim một câu, abstract nháp, section đủ goal/draft/cite/artifact, "
                "và checklist chống đạo văn — đủ để bắt đầu viết thật."
            ),
            "strength_en": (
                "One-sentence claim, abstract draft, sections with goal/draft/cite/artifact, "
                "and an anti-plagiarism checklist — enough to start real writing."
            ),
            "limitation": (
                "Chưa phải bản camera-ready; số liệu phải lấy sau khi Chạy; "
                "mọi đoạn draft phải được viết lại theo giọng tác giả trước khi nộp."
            ),
            "limitation_en": (
                "Not camera-ready; numbers must come from Run; "
                "all draft notes must be rewritten in the author’s voice before submission."
            ),
            "verdict": "Khung công bố dùng được cho hội đồng theo dõi tiến độ viết — không thay manuscript đã nộp.",
            "verdict_en": "A publication frame suitable for committee progress tracking — not a submitted manuscript.",
            "score_0_1": 0.86,
        },
    }


# Fix sequence_en mirror
for _pid, _pack in list(PAPERS.items()):
    pass

# Populate sequence_en for overlays at runtime
def _mirror_seq(overlay: dict[str, Any]) -> dict[str, Any]:
    seq = overlay.get("scientific_sequence_vi")
    if isinstance(seq, list):
        overlay["scientific_sequence_en"] = seq
    return overlay


def get_paper_academic_overlay(task_id: str) -> dict[str, Any] | None:
    o = academic_overlay_for_paper(task_id)
    return _mirror_seq(o) if o else None
