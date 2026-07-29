"""
Rich per-topic scientific frames for Step-1 survey tabs.

Each topic pack makes the method itself explicit:
theory (elsewhere) → overall math → algorithm + linked formulas →
pros/cons → improvements (math + algo) → corpus evidence with explanation.
"""

from __future__ import annotations

from typing import Any

from app.data.literature_corpus import papers_by_tag
from app.pipeline.math_specs import formula, math_model, var


def _algo(
    *,
    name_vi: str,
    name_en: str,
    math_ids: list[str],
    steps: list[str],
    complexity: str,
    pros_vi: list[str],
    pros_en: list[str],
    cons_vi: list[str],
    cons_en: list[str],
    improve_math_vi: list[str],
    improve_math_en: list[str],
    improve_algo_vi: list[str],
    improve_algo_en: list[str],
    **extra: Any,
) -> dict[str, Any]:
    return {
        "name_vi": name_vi,
        "name_en": name_en,
        "math_ids": math_ids,
        "pseudocode": steps,
        "complexity": complexity,
        "pros_vi": pros_vi,
        "pros_en": pros_en,
        "cons_vi": cons_vi,
        "cons_en": cons_en,
        "improve_math_vi": improve_math_vi,
        "improve_math_en": improve_math_en,
        "improve_algo_vi": improve_algo_vi,
        "improve_algo_en": improve_algo_en,
        **extra,
    }


def _critique_on_math(
    pack: dict[str, Any],
    *,
    role_vi: str,
    role_en: str,
    pros_vi: list[str],
    pros_en: list[str],
    cons_vi: list[str],
    cons_en: list[str],
    improve_vi: list[str],
    improve_en: list[str],
    **extra: Any,
) -> dict[str, Any]:
    return {
        **pack,
        "role_vi": role_vi,
        "role_en": role_en,
        "pros_vi": pros_vi,
        "pros_en": pros_en,
        "cons_vi": cons_vi,
        "cons_en": cons_en,
        "improve_vi": improve_vi,
        "improve_en": improve_en,
        **extra,
    }


def _seq_step(
    *,
    id: str,
    title_vi: str,
    title_en: str,
    explain_vi: str,
    explain_en: str,
    anchor: str,
) -> dict[str, str]:
    return {
        "id": id,
        "title_vi": title_vi,
        "title_en": title_en,
        "explain_vi": explain_vi,
        "explain_en": explain_en,
        "anchor": anchor,
    }


def scientific_sequence_for(tag: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Rich roadmap (not a bare TOC): each step has a scientific explanation + UI anchor."""
    # Default generic explanations; RAG gets sharper wording below.
    common_vi = [
        _seq_step(
            id="theory",
            title_vi="Lý thuyết — khái niệm phương pháp",
            title_en="Theory — method concepts",
            explain_vi=(
                "Định nghĩa phương pháp là gì, giả định khoa học nào đang dùng, "
                "và vì sao phương pháp này là baseline/tiền đề cho EDGR trong miền IDS/CTI."
            ),
            explain_en=(
                "Define what the method is, which scientific assumptions it uses, "
                "and why it is a baseline/premise for EDGR in IDS/CTI."
            ),
            anchor="sci-theory",
        ),
        _seq_step(
            id="purpose",
            title_vi="Mục đích tab trong khảo sát corpus",
            title_en="Tab purpose in the corpus survey",
            explain_vi=(
                "Phân biệt hai việc: (A) trình bày mô hình phương pháp, "
                "(B) chạy lọc corpus để lấy limitations làm bằng chứng bibliographic cho gap."
            ),
            explain_en=(
                "Separate two jobs: (A) present the method model, "
                "(B) run a corpus filter to collect limitations as bibliographic evidence for gaps."
            ),
            anchor="sci-purpose",
        ),
        _seq_step(
            id="csdl",
            title_vi="CSDL / nguồn dữ liệu khảo sát",
            title_en="Database / survey data source",
            explain_vi=(
                "Xác định tập dữ liệu (subset tag) dùng làm quan sát bibliographic — "
                "schema đầy đủ nằm ở tổng quan bước, tab con chỉ dùng tập con liên quan."
            ),
            explain_en=(
                "Identify the dataset (tag subset) used as bibliographic observations — "
                "full schema lives on the step overview; the child tab uses the relevant subset."
            ),
            anchor="sci-csdl",
        ),
        _seq_step(
            id="math",
            title_vi="Mô hình toán tổng thể",
            title_en="Overall mathematical model",
            explain_vi=(
                "Nêu công thức trung tâm, giải thích từng biến, điều kiện tối ưu, "
                "và vai trò của từng biểu thức trong chuỗi Retrieve → Generate → Evaluate."
            ),
            explain_en=(
                "State the core formulas, explain each variable and optimality condition, "
                "and the role of each expression in Retrieve → Generate → Evaluate."
            ),
            anchor="sci-math",
        ),
        _seq_step(
            id="algo",
            title_vi="Mô hình thuật toán + công thức tương ứng",
            title_en="Algorithm model + linked formulas",
            explain_vi=(
                "Chỉ rõ thuật toán nào được dùng, từng bước ánh xạ sang công thức nào, "
                "độ phức tạp, và chỗ hallucination có thể phát sinh trong pipeline."
            ),
            explain_en=(
                "Name the algorithm, map each step to a formula, state complexity, "
                "and where hallucination can arise in the pipeline."
            ),
            anchor="sci-algo",
        ),
        _seq_step(
            id="critique",
            title_vi="Ưu điểm / nhược điểm (toán & thuật toán)",
            title_en="Pros / cons (math & algorithm)",
            explain_vi=(
                "Phân tích cấu trúc — không liệt kê cảm tính: ưu điểm module hóa/đo được; "
                "nhược điểm giả định phẳng, thiếu trust/time, thiếu toán tử từ chối."
            ),
            explain_en=(
                "Structural analysis — not vague bullets: modular/measurable strengths; "
                "weaknesses from flat assumptions, missing trust/time, missing abstain."
            ),
            anchor="sci-math",
        ),
        _seq_step(
            id="improve",
            title_vi="Hướng cải tiến (công thức & thuật toán → EDGR)",
            title_en="Improvements (formulas & algorithm → EDGR)",
            explain_vi=(
                "Sửa giả định bằng công thức mới (R_G, R_τ, s(e), ρ) và pseudo-code EDGR; "
                "mỗi module phải đo được bằng ablation trên cùng metric F/H."
            ),
            explain_en=(
                "Revise assumptions via new formulas (R_G, R_τ, s(e), ρ) and EDGR pseudocode; "
                "each module must be measurable by ablation on the same F/H metrics."
            ),
            anchor="sci-algo",
        ),
        _seq_step(
            id="ops",
            title_vi="Mô hình hoạt động (cách chạy tab)",
            title_en="Operating model (how to run the tab)",
            explain_vi=(
                "Luồng thao tác: đọc mô hình → chạy analyze_topic → đọc kết quả; "
                "tách minh chứng thiết kế (A) và minh chứng runtime (B)."
            ),
            explain_en=(
                "Operator flow: read the model → run analyze_topic → read outputs; "
                "keep design evidence (A) separate from runtime evidence (B)."
            ),
            anchor="sci-ops",
        ),
        _seq_step(
            id="cite",
            title_vi="Trích dẫn khoa học",
            title_en="Scientific citations",
            explain_vi="Các công trình gốc dùng để neo định nghĩa và lập luận của phương pháp.",
            explain_en="Foundational works that anchor the method’s definitions and arguments.",
            anchor="sci-cite",
        ),
        _seq_step(
            id="evidence",
            title_vi="Minh chứng khảo sát + giải thích",
            title_en="Survey evidence + explanation",
            explain_vi=(
                "Đọc số paper/năm/limitations như bằng chứng bibliographic: "
                "ánh xạ limitation quan sát được ngược lên nhược điểm công thức/thuật toán."
            ),
            explain_en=(
                "Read paper counts/years/limitations as bibliographic evidence: "
                "map observed limitations back onto formula/algorithm weaknesses."
            ),
            anchor="sci-ev",
        ),
        _seq_step(
            id="assess",
            title_vi="Nhận định thiết kế → sau Chạy: kết quả runtime",
            title_en="Design assessment → after Run: runtime results",
            explain_vi=(
                "Kết luận khung thiết kế có đủ thuyết phục không; sau «Chạy công việc này» "
                "bảng papers/limitations là minh chứng runtime — phải có giải thích từng bảng."
            ),
            explain_en=(
                "Judge whether the design frame is persuasive; after «Run this task» "
                "the papers/limitations tables are runtime evidence — each with explanations."
            ),
            anchor="sci-assess",
        ),
    ]

    if tag == "rag":
        common_vi[0]["explain_vi"] = (
            "RAG = bộ nhớ tham số (G) + phi tham số (D/R(q)). "
            "Tab này lập luận: RAG đúng hướng tri thức động, nhưng giả định "
            "«quan hệ CTI nằm trong độ gần đoạn văn» và F hậu kiểm là không đủ cho IDS/CTI."
        )
        common_vi[0]["explain_en"] = (
            "RAG = parametric memory (G) + non-parametric memory (D/R(q)). "
            "This tab argues: RAG correctly attacks dynamic knowledge, but the assumption that "
            "«CTI relations live in passage proximity» plus post-hoc F is insufficient for IDS/CTI."
        )
        common_vi[2]["explain_vi"] = (
            "Ba trụ: R(q)=TopK sim(q,d); a=G(q,R(q)); F(a,R) với H≈1−F. "
            "Mỗi công thức có biến, điều kiện tối ưu, và ý nghĩa trong chuỗi Retrieve→Generate→Evaluate."
        )
        common_vi[2]["explain_en"] = (
            "Three pillars: R(q)=TopK sim(q,d); a=G(q,R(q)); F(a,R) with H≈1−F. "
            "Each formula has variables, optimality notes, and a role in Retrieve→Generate→Evaluate."
        )
        common_vi[3]["explain_vi"] = (
            "Thuật toán Retrieve-then-Generate (BM25/dense + LLM): bước 2–3 ↔ R(q), bước 4 ↔ G, "
            "bước 5 chỉ đo F (không điều khiển reject). Pseudo-code EDGR nằm cuối khối thuật toán."
        )
        common_vi[3]["explain_en"] = (
            "Retrieve-then-Generate (BM25/dense + LLM): steps 2–3 ↔ R(q), step 4 ↔ G, "
            "step 5 only measures F (no reject control). EDGR pseudocode ends the algorithm block."
        )

    # Build EN list from the (possibly RAG-tuned) VI structure
    seq_en = [
        {
            "id": s["id"],
            "title_vi": s["title_vi"],
            "title_en": s["title_en"],
            "explain_vi": s["explain_vi"],
            "explain_en": s["explain_en"],
            "anchor": s["anchor"],
        }
        for s in common_vi
    ]
    return common_vi, seq_en




def _rag_pack(n: int, years: list[int], sample_ids: list[str]) -> dict[str, Any]:
    y0 = min(years) if years else None
    y1 = max(years) if years else None
    improve_formulas = [
        formula(
            id="edgr_expand",
            label_vi="Cải tiến (1): truy hồi trên đồ thị",
            label_en="Improvement (1): graph retrieval",
            latex=r"R_G(q)=\mathrm{Expand}\!\left(\mathrm{KG},\,\mathrm{ents}(q),\,h\right)",
            explain_vi=(
                "Thay không gian ứng viên phẳng D bằng lân cận đồ thị quanh thực thể CTI "
                "(CVE, TTP, actor). Hàm Expand mô hình hóa quan hệ đa bước mà sim(q,d) không biểu diễn được. "
                "Đây là bước φ1 trong EDGR / tinh thần GraphRAG."
            ),
            explain_en=(
                "Replace the flat candidate space D by a graph neighborhood around CTI entities "
                "(CVE, TTP, actor). Expand encodes multi-hop relations that sim(q,d) cannot express. "
                "This is EDGR φ1 / GraphRAG-style retrieval."
            ),
            variables=[
                var(r"\mathrm{ents}(q)", "thực thể trong truy vấn", "query entities", "", "đủ seed CTI"),
                var("h", "số hop", "hop budget", "h∈ℕ", "đủ quan hệ, tránh nổ"),
            ],
            optimize_vi="Tốt khi đường đi CVE→TTP→malware được giữ trong R_G và không lẫn đỉnh nhiễu.",
            optimize_en="Good when CVE→TTP→malware paths stay in R_G without noisy nodes.",
        ),
        formula(
            id="edgr_temporal",
            label_vi="Cải tiến (2): lọc thời gian",
            label_en="Improvement (2): temporal filter",
            latex=r"R_\tau=\{e\in R_G:\ \mathrm{age}(e)\le \tau\}\ \cup\ \mathrm{ents}(q)",
            explain_vi=(
                "Loại lân cận lỗi thời nhưng luôn giữ seed của truy vấn (CVE lịch sử vẫn có thể liên quan). "
                "Công thức này khắc phục việc RAG cổ điển coi mọi đoạn trong R(q) ngang hàng về thời gian."
            ),
            explain_en=(
                "Drop stale neighbors while always keeping query seeds (historical CVEs may still matter). "
                "This fixes classic RAG treating every passage in R(q) as temporally equal."
            ),
            variables=[
                var(r"\tau", "cửa sổ ngày", "day window", "τ>0", "khớp vận hành SOC"),
                var(r"\mathrm{age}", "tuổi bằng chứng", "evidence age", "ngày", "nhỏ hơn τ"),
            ],
            optimize_vi="Tối ưu khi giảm false context từ intel cũ mà không mất seed quan trọng.",
            optimize_en="Optimal when stale intel is cut without losing critical seeds.",
        ),
        formula(
            id="edgr_score_risk",
            label_vi="Cải tiến (3): xếp hạng đa tín hiệu + cổng risk",
            label_en="Improvement (3): multi-signal rank + risk gate",
            latex=(
                r"s(e)=\alpha\,\mathrm{sem}+\beta\,\mathrm{graph}+\gamma\,\mathrm{trust}+\delta\,\mathrm{fresh},"
                r"\quad \rho=w_H(1-F)+w_c(1-C_g)+w_t(1-\mathrm{fresh})"
            ),
            explain_vi=(
                "sim đơn được thay bằng tổ hợp có trọng số; ρ ước lượng rủi ro ảo giác trước khi trả lời. "
                "Quy tắc quyết định: chỉ emit a nếu ρ<θ — đây là khác biệt then chốt so với RAG hậu kiểm F."
            ),
            explain_en=(
                "Scalar sim is replaced by a weighted multi-signal score; ρ estimates hallucination risk "
                "before answering. Decision rule: emit a only if ρ<θ — the key difference vs post-hoc F in RAG."
            ),
            variables=[
                var("s(e)", "điểm bằng chứng", "evidence score", "ℝ", "xếp hạng ổn định"),
                var(r"\rho", "rủi ro ảo giác", "hallucination risk", "[0,1]", "→ 0"),
                var(r"\theta", "ngưỡng từ chối", "reject threshold", "(0,1)", "cân bằng phủ/an toàn"),
            ],
            optimize_vi="Tốt khi faithfulness tăng và tỷ lệ trả lời thiếu bằng chứng giảm trên bộ CTI/IDS.",
            optimize_en="Good when faithfulness rises and insufficient-evidence abstentions fall on CTI/IDS sets.",
        ),
    ]

    math = _critique_on_math(
        math_model(
            formula(
                id="rag_retrieve",
                label_vi="(1) Truy hồi top-k — Retriever",
                label_en="(1) Top-k retrieval — Retriever",
                latex=r"R(q)=\mathrm{TopK}_{d\in\mathcal{D}}\;\mathrm{sim}(q,d)",
                explain_vi=(
                    "Cho truy vấn q, hệ thống chấm mọi tài liệu d∈D bằng hàm tương đồng sim "
                    "(BM25 thưa hoặc embedding dày) rồi giữ k phần tử cao nhất. "
                    "Tập R(q) đóng vai trò bộ nhớ phi tham số: tri thức ngoài có thể cập nhật bằng cách "
                    "thêm/xóa tài liệu trong D mà không train lại LLM. "
                    "Giả định then chốt (và cũng là hạn chế): mọi quan hệ cần thiết để trả lời đều "
                    "nằm trong độ gần ngữ nghĩa giữa q và từng đoạn văn riêng lẻ."
                ),
                explain_en=(
                    "For query q, every document d∈D is scored by similarity sim "
                    "(sparse BM25 or dense embeddings) and the top-k items are kept. "
                    "R(q) is non-parametric memory: external knowledge updates by editing D "
                    "without retraining the LLM. "
                    "Key assumption (and limitation): relations needed to answer are assumed to lie "
                    "in the semantic proximity between q and each passage alone."
                ),
                variables=[
                    var("q", "truy vấn người dùng / alert", "user/alert query", "", "có thực thể CTI rõ"),
                    var(r"\mathcal{D}", "kho đoạn văn / tài liệu", "passage corpus", "|D|≫k", "cập nhật được, ít nhiễu"),
                    var("k", "ngân sách truy hồi", "retrieval budget", "k∈ℕ⁺", "đủ phủ, ít redundancy"),
                    var(r"\mathrm{sim}", "điểm xếp hạng", "ranking score", "ℝ hoặc [0,1]", "Precision@k cao"),
                ],
                optimize_vi=(
                    "Tối ưu khoa học khi Precision@k và Recall@k cao trên tập câu hỏi có gold evidence; "
                    "với CTI, còn cần R(q) chứa đúng định danh (CVE/ATT&CK) chứ không chỉ từ khóa gần nghĩa."
                ),
                optimize_en=(
                    "Scientifically optimal when Precision@k and Recall@k are high on gold-evidence QA; "
                    "for CTI, R(q) must also contain correct identifiers (CVE/ATT&CK), not mere near-synonyms."
                ),
            ),
            formula(
                id="rag_generate",
                label_vi="(2) Sinh có điều kiện — Generator",
                label_en="(2) Conditional generation — Generator",
                latex=r"a=G\!\left(q,\,R(q)\right)=\arg\max_{a'}\ P_G\!\left(a'\,|\,q,R(q)\right)",
                explain_vi=(
                    "Generator G (thường là LLM) xấp xỉ phân phối câu trả lời điều kiện trên cặp (q, R(q)). "
                    "Về mặt mô hình, đây là tách rời tham số θ_G (trong G) và kho D (ngoài G): "
                    "RAG không yêu cầu θ_G chứa mọi sự kiện CTI mới. "
                    "Tuy nhiên G vẫn có thể bịa chi tiết không có trong R(q) nếu không có ràng buộc "
                    "faithfulness / risk tường minh — đây là điểm EDGR sẽ siết bằng cổng ρ."
                ),
                explain_en=(
                    "Generator G (typically an LLM) approximates the answer distribution conditioned on (q, R(q)). "
                    "Model-wise this separates parameters θ_G (inside G) from store D (outside G): "
                    "RAG does not require θ_G to memorize every new CTI fact. "
                    "Yet G may still fabricate details absent from R(q) without an explicit faithfulness/risk "
                    "constraint — exactly what EDGR tightens with a ρ-gate."
                ),
                variables=[
                    var("G", "mô hình sinh có điều kiện", "conditional generator", "", "bám evidence"),
                    var(r"\theta_G", "tham số LLM", "LLM parameters", "", "ổn định, không cần retrain mỗi ngày"),
                    var("a", "câu trả lời tin cậy mục tiêu", "target trusted answer", "", "mỗi claim có hỗ trợ trong R"),
                ],
                optimize_vi="Tối ưu khi log-likelihood của câu trả lời đúng tăng đồng thời hallucination rate giảm trên bộ kiểm định.",
                optimize_en="Optimal when likelihood of correct answers rises while hallucination rate falls on a held-out set.",
            ),
            formula(
                id="rag_faith",
                label_vi="(3) Faithfulness — thước đo trung thực",
                label_en="(3) Faithfulness — grounding metric",
                latex=r"F(a,R)=\frac{|\{c\in\mathrm{Claims}(a):\, R\models c\}|}{\max\!\left(1,\,|\mathrm{Claims}(a)|\right)},\quad H\approx 1-F",
                explain_vi=(
                    "F là tỷ lệ mệnh đề trong a được R hỗ trợ logic/thực chứng; H≈1−F là hallucination rate "
                    "theo nghĩa extrinsic. RAG cổ điển tối ưu F chủ yếu gián tiếp (cải retrieval), "
                    "không đưa F hay H vào hàm quyết định trước khi trả lời. "
                    "Trong miền IDS/CTI, một claim sai về CVE/TTP có chi phí vận hành rất cao, "
                    "nên chỉ báo cáo F hậu kiểm là chưa đủ thuyết phục — cần cơ chế từ chối."
                ),
                explain_en=(
                    "F is the fraction of claims in a supported by R; H≈1−F is an extrinsic hallucination rate. "
                    "Classic RAG improves F mostly indirectly (better retrieval) and does not put F/H into a "
                    "pre-answer decision rule. In IDS/CTI, one wrong CVE/TTP claim is operationally costly, "
                    "so post-hoc F alone is scientifically insufficient — abstention is required."
                ),
                variables=[
                    var("F", "faithfulness", "faithfulness", "[0,1]", "→ 1"),
                    var("H", "hallucination rate", "hallucination rate", "[0,1]", "→ 0"),
                    var("c", "mệnh đề nguyên tử", "atomic claim", "", "kiểm chứng được trên R"),
                ],
                optimize_vi="Mục tiêu khảo sát: chứng minh rằng RAG phẳng làm F giảm trên câu hỏi quan hệ/đa bước CTI — từ đó biện minh EDGR.",
                optimize_en="Survey goal: show flat RAG loses F on relational/multi-hop CTI questions — justifying EDGR.",
            ),
            note_vi=(
                "Ba công thức trên là mô hình toán tổng thể của RAG (Lewis et al., NeurIPS 2020): "
                "Retrieve → Generate → Evaluate. Chúng không phải công thức lọc tag corpus; "
                "phần khảo sát corpus bên dưới chỉ cung cấp minh chứng bibliographic cho hạn chế của mô hình này."
            ),
            note_en=(
                "These three formulas are the overall mathematical model of RAG (Lewis et al., NeurIPS 2020): "
                "Retrieve → Generate → Evaluate. They are not corpus tag-filter formulas; "
                "the corpus survey below only supplies bibliographic evidence for this model’s limits."
            ),
        ),
        role_vi=(
            "Mô hình toán tổng thể đặt RAG như một hệ thống hai thành phần (retriever phi tham số + generator tham số) "
            "với tiêu chí chất lượng F/H. Mọi lập luận ưu/nhược và cải tiến EDGR phải bám vào các ký hiệu R(q), G, F."
        ),
        role_en=(
            "The overall math model casts RAG as a two-component system (non-parametric retriever + parametric generator) "
            "with quality criteria F/H. All pros/cons and EDGR improvements must refer to R(q), G, and F."
        ),
        narrative_vi=(
            "Về mặt khoa học, RAG giải bài toán tri thức động bằng cách tách memorization khỏi parameterization: "
            "sự kiện mới đi vào D, trong khi G chỉ cần điều kiện hóa trên R(q). "
            "Điều này thuyết phục cho QA mở và tài liệu dài. Tuy nhiên, hàm mục tiêu thực dụng của RAG thường là "
            "argmax sim rồi sinh tự do — thiếu ràng buộc cấu trúc trên không gian giả thuyết CTI "
            "(đồ thị CVE–TTP–actor) và thiếu kiểm soát rủi ro trước khi công bố câu trả lời cho analyst."
        ),
        narrative_en=(
            "Scientifically, RAG solves dynamic knowledge by separating memorization from parameterization: "
            "new facts enter D while G only conditions on R(q). "
            "This is compelling for open QA and long documents. Yet RAG’s practical objective is usually "
            "argmax-sim then free generation — lacking structural constraints on the CTI hypothesis space "
            "(CVE–TTP–actor graphs) and lacking pre-publication risk control for analysts."
        ),
        pros_vi=[
            "Tách bộ nhớ: cập nhật D không đòi hỏi fine-tune θ_G — phù hợp threat intel thay đổi theo tuần/ngày.",
            "Neo câu trả lời vào R(q) tạo điều kiện cần (không đủ) để giảm bịa kiến thức lỗi thời so với LLM thuần.",
            "Công thức R(q), a=G(q,R), F tạo baseline đo được — mọi phương pháp sau (GraphRAG, EDGR) phải vượt baseline này trên cùng metric.",
        ],
        pros_en=[
            "Memory split: updating D needs no θ_G finetune — fits week/day-changing threat intel.",
            "Grounding in R(q) is a necessary (not sufficient) condition to cut stale-knowledge fabrication vs a bare LLM.",
            "R(q), a=G(q,R), F yield a measurable baseline — later methods (GraphRAG, EDGR) must beat it on the same metrics.",
        ],
        pros_detail_vi=(
            "Ưu điểm then chốt của các công thức RAG là tính module hóa và kiểm chứng được. "
            "Retriever có thể đánh giá độc lập bằng P@k/R@k/MRR; generator đánh giá bằng F/H; "
            "toàn hệ thống đánh giá end-to-end trên QA. Nhờ đó luận án có chuẩn so sánh công bằng với EDGR. "
            "Trong vận hành, việc thêm báo cáo CVE mới vào D ngay lập tức mở rộng không gian bằng chứng "
            "mà không chờ chu kỳ train — đây là lý do RAG trở thành nền tảng hầu hết hệ thống CTI-QA hiện đại."
        ),
        pros_detail_en=(
            "The core advantage of RAG’s formulas is modularity and testability. "
            "The retriever can be judged via P@k/R@k/MRR; the generator via F/H; "
            "the full system via end-to-end QA. That gives the thesis a fair baseline against EDGR. "
            "Operationally, inserting a new CVE report into D immediately expands the evidence space "
            "without a training cycle — why RAG underpins most modern CTI-QA stacks."
        ),
        cons_vi=[
            "sim(q,d) là xếp hạng phẳng: không có biến cạnh quan hệ, nên câu hỏi kiểu “CVE X kích hoạt TTP nào của APT Y?” dễ lấy đoạn gần nghĩa nhưng đứt chuỗi suy luận.",
            "R(q) không mang tín hiệu trust(source) hay freshness(e) — đoạn kém tin cậy/cũ có thể thắng thuần vì lexical overlap.",
            "F/H là hậu kiểm: công thức không có toán tử quyết định “từ chối trả lời”, không an toàn cho SOC khi evidence mỏng.",
        ],
        cons_en=[
            "sim(q,d) is flat ranking: no edge variables, so questions like “which APT Y TTP does CVE X enable?” often retrieve near-synonym passages that break the reasoning chain.",
            "R(q) carries neither trust(source) nor freshness(e) — weak/stale passages can win on lexical overlap alone.",
            "F/H are post-hoc: the model has no abstain operator, unsafe for SOC when evidence is thin.",
        ],
        cons_detail_vi=(
            "Nhược điểm mang tính cấu trúc, không chỉ “thiếu dữ liệu”. "
            "Về toán: không gian giả thuyết của retriever là D^k (tổ hợp đoạn), không phải tập đường đi trên KG; "
            "do đó tối ưu sim không tương đương tối ưu đúng quan hệ CTI. "
            "Về đo lường: tối ưu F sau khi đã sinh a không ngăn được a nguy hiểm được đưa ra analyst. "
            "Các limitation lặp lại trong corpus RAG (retrieval phẳng, thiếu graph/trust gate) chính là "
            "bằng chứng bibliographic củng cố các nhược điểm công thức trên."
        ),
        cons_detail_en=(
            "These limitations are structural, not merely “missing data”. "
            "Mathematically, the retriever’s hypothesis space is D^k (passage tuples), not paths on a KG; "
            "hence optimizing sim is not equivalent to optimizing correct CTI relations. "
            "Metrologically, maximizing F after a is produced does not prevent a dangerous a from reaching analysts. "
            "Recurring RAG corpus limitations (flat retrieval, missing graph/trust gates) are bibliographic "
            "evidence reinforcing these formula-level weaknesses."
        ),
        improve_vi=[
            "Thay R(q) → R_G(q)=Expand(KG, ents(q), h) để mã hóa quan hệ đa bước (EDGR φ1 / GraphRAG).",
            "Thêm R_τ với ngưỡng tuổi τ, luôn bảo toàn seed truy vấn (EDGR φ2).",
            "Thay sim bằng s(e) đa tín hiệu và thêm cổng ρ<θ trước khi emit a (EDGR φ4–φ6).",
        ],
        improve_en=[
            "Replace R(q) → R_G(q)=Expand(KG, ents(q), h) to encode multi-hop relations (EDGR φ1 / GraphRAG).",
            "Add R_τ with age threshold τ, always preserving query seeds (EDGR φ2).",
            "Replace sim by multi-signal s(e) and add a ρ<θ gate before emitting a (EDGR φ4–φ6).",
        ],
        improve_detail_vi=(
            "Hướng cải tiến không phải “thêm mẹo engineering” mà là sửa giả định toán học: "
            "(i) mở rộng không gian bằng chứng từ đoạn phẳng sang đường đi đồ thị; "
            "(ii) đưa thời gian vào định nghĩa tập ứng viên; "
            "(iii) đưa rủi ro ảo giác vào quy tắc quyết định. "
            "Ba công thức cải tiến bên dưới là cầu nối hình thức từ RAG → EDGR; "
            "chúng giữ G nhưng thay đổi R và thêm toán tử reject — đủ để lập luận đóng góp luận án."
        ),
        improve_detail_en=(
            "Improvements are not engineering tips; they revise mathematical assumptions: "
            "(i) enlarge evidence from flat passages to graph paths; "
            "(ii) put time into the candidate-set definition; "
            "(iii) put hallucination risk into the decision rule. "
            "The three improvement formulas below formally bridge RAG → EDGR; "
            "they keep G but change R and add a reject operator — enough to argue the thesis contribution."
        ),
        improve_formulas=improve_formulas,
    )

    algo = _algo(
        name_vi="Retrieve-then-Generate (RAG cổ điển — Dense/BM25 + LLM)",
        name_en="Retrieve-then-Generate (classic RAG — Dense/BM25 + LLM)",
        math_ids=["rag_retrieve", "rag_generate", "rag_faith"],
        steps=[
            "1. Chuẩn hóa truy vấn q (tokenize / embed)",
            "2. ∀ d∈D: tính sim(q,d)  ↔ công thức rag_retrieve",
            "3. R ← TopK(sim)  ↔ R(q)",
            "4. a ← G(q, R)  ↔ công thức rag_generate",
            "5. (Tuỳ chọn, hậu kiểm) ước lượng F(a,R), H≈1−F  ↔ rag_faith",
        ],
        complexity=r"O(|D|\cdot c_{\mathrm{sim}}+c_G)",
        narrative_vi=(
            "Thuật toán chuẩn của RAG là pipeline tuần tự Retrieve-then-Generate "
            "(Lewis et al. 2020; biến thể DPR/BM25 + seq2seq/LLM). "
            "Từng bước ánh xạ 1–1 sang công thức toán: bước 2–3 hiện thực R(q); bước 4 hiện thực G; "
            "bước 5 (nếu có) chỉ đo F chứ không điều khiển việc có trả lời hay không. "
            "Đây là baseline thuật toán mà EDGR sẽ chèn thêm Expand / TemporalFilter / Rank / RiskGate."
        ),
        narrative_en=(
            "Classic RAG’s algorithm is the sequential Retrieve-then-Generate pipeline "
            "(Lewis et al. 2020; DPR/BM25 + seq2seq/LLM variants). "
            "Steps map 1–1 onto the math: steps 2–3 realize R(q); step 4 realizes G; "
            "step 5 (if present) only measures F and does not control whether to answer. "
            "This is the algorithmic baseline into which EDGR inserts Expand / TemporalFilter / Rank / RiskGate."
        ),
        step_explain_vi=[
            "Bước 1–3 tối ưu retrieval độc lập — có thể tinh chỉnh embedder/BM25 mà không đụng G.",
            "Bước 4 là điểm hallucination có thể phát sinh dù R đúng (generator over-generate).",
            "Bước 5 không nằm trong vòng điều khiển cổ điển: thiếu feedback “ρ cao → abort”.",
        ],
        step_explain_en=[
            "Steps 1–3 optimize retrieval independently — embedder/BM25 can be tuned without touching G.",
            "Step 4 is where hallucination can arise even with correct R (generator over-generation).",
            "Step 5 is outside the classic control loop: no “high ρ → abort” feedback.",
        ],
        pros_vi=[
            "Đơn giản, tái lập được, chi phí kỹ thuật thấp — chuẩn mực so sánh khoa học.",
            "Khớp chặt công thức R(q) và a=G(q,R(q)) — dễ chứng minh đúng đắn triển khai.",
            "Hiệu quả trên câu hỏi single-hop / đọc hiểu đoạn khi gold evidence nằm trong top-k.",
        ],
        pros_en=[
            "Simple, reproducible, low engineering cost — a scientific comparison standard.",
            "Tightly matches R(q) and a=G(q,R(q)) — easy to prove implementation fidelity.",
            "Effective on single-hop / passage QA when gold evidence is in the top-k.",
        ],
        pros_detail_vi=(
            "Về thuật toán, ưu điểm lớn nhất là tính tách lớp: có thể thay retriever (BM25↔dense) "
            "hoặc generator (T5↔LLM lớn) mà vẫn giữ cùng hợp đồng toán học. "
            "Điều này làm cho ablation và so sánh baseline trong luận án minh bạch."
        ),
        pros_detail_en=(
            "Algorithmically, the main strength is layering: swap retriever (BM25↔dense) "
            "or generator (T5↔large LLM) while keeping the same mathematical contract. "
            "That keeps ablations and baseline comparisons transparent in the thesis."
        ),
        cons_vi=[
            "Không có thao tác duyệt cạnh đồ thị — không hiện thực được suy luận CVE–TTP đa bước trong thuật toán.",
            "Không có bước xếp hạng theo trust/fresh — TopK(sim) có thể ưu tiên đoạn “giống từ” hơn đoạn “đúng quan hệ”.",
            "Không có RiskGate: thuật toán luôn emit a, kể cả khi R quá mỏng cho quyết định CTI.",
        ],
        cons_en=[
            "No edge-walk operator — cannot realize multi-hop CVE–TTP reasoning inside the algorithm.",
            "No trust/fresh ranking step — TopK(sim) may prefer lexically similar passages over relationally correct ones.",
            "No RiskGate: the algorithm always emits a, even when R is too thin for a CTI decision.",
        ],
        cons_detail_vi=(
            "Nhược điểm thuật toán song song với nhược điểm công thức: thiếu toán tử cấu trúc và toán tử từ chối. "
            "Pseudo-code cổ điển dừng ở Generate; mọi cơ chế an toàn (nếu có) nằm ngoài vòng lặp chính, "
            "nên không được tối ưu cùng mục tiêu F/H. Đây là lập luận then chốt để đề xuất EDGR như thuật toán mới, "
            "không chỉ như “RAG + vài heuristic”."
        ),
        cons_detail_en=(
            "Algorithmic weaknesses mirror formula weaknesses: missing structure and abstain operators. "
            "Classic pseudocode stops at Generate; any safety mechanism (if present) sits outside the main loop, "
            "so it is not co-optimized with F/H. This is the key argument for proposing EDGR as a new algorithm, "
            "not merely “RAG plus heuristics”."
        ),
        improve_math_vi=[
            "Đưa công thức R_G, R_τ, s(e), ρ vào đặc tả thuật toán (xem khối cải tiến toán).",
            "Thêm bất đẳng thức quyết định: emit(a) ⇔ ρ(a,R)<θ ∧ |R|≥k_min.",
        ],
        improve_math_en=[
            "Bring R_G, R_τ, s(e), ρ into the algorithm spec (see math improvement block).",
            "Add decision predicate: emit(a) ⇔ ρ(a,R)<θ ∧ |R|≥k_min.",
        ],
        improve_algo_vi=[
            "Pipeline EDGR: Understand→Expand-KG→TemporalFilter→EvidenceRank→HallucinationScore→RiskGate→TrustedAnswer.",
            "Thay bước 5 hậu kiểm bằng bước RiskGate trước khi trả lời; nếu reject thì trả 'insufficient evidence'.",
            "Giữ G nhưng đổi đầu vào từ R(q) phẳng sang evidence đã rank/risk-filter — đóng góp thuật toán đo được bằng ablation.",
        ],
        improve_algo_en=[
            "EDGR pipeline: Understand→Expand-KG→TemporalFilter→EvidenceRank→HallucinationScore→RiskGate→TrustedAnswer.",
            "Replace post-hoc step 5 by a RiskGate before answering; on reject, return 'insufficient evidence'.",
            "Keep G but feed ranked/risk-filtered evidence instead of flat R(q) — an algorithmic claim measurable by ablation.",
        ],
        improve_detail_vi=(
            "Cải tiến thuật toán phải kèm cải tiến công thức: mỗi module EDGR tương ứng một ký hiệu toán "
            "(Expand↔R_G, Temporal↔R_τ, Rank↔s(e), Risk↔ρ). "
            "Như vậy đóng góp không dừng ở sơ đồ hộp mực, mà có thể phát biểu định lý thực nghiệm: "
            "loại bỏ module X làm giảm F hoặc tăng H trên cùng tập CTI/IDS."
        ),
        improve_detail_en=(
            "Algorithm improvements must ship with formula improvements: each EDGR module maps to a math symbol "
            "(Expand↔R_G, Temporal↔R_τ, Rank↔s(e), Risk↔ρ). "
            "The contribution is then not a box diagram but an experimental claim: "
            "removing module X lowers F or raises H on the same CTI/IDS set."
        ),
        improved_pseudocode=[
            "ents ← ExtractEntities(q)",
            "R_G ← Expand(KG, ents, h)     ↔ edgr_expand",
            "R_τ ← TemporalFilter(R_G, τ)  ↔ edgr_temporal",
            "E ← Rank(R_τ, s(·))           ↔ edgr_score_risk",
            "ρ ← RiskScore(q, E)",
            "if ρ ≥ θ: return InsufficientEvidence",
            "a ← G(q, E); return TrustedAnswer(a, E, ρ)",
        ],
    )

    seq_vi, seq_en = scientific_sequence_for("rag")
    return {
        "_standalone_task": True,
        "scientific_sequence_vi": seq_vi,
        "scientific_sequence_en": seq_en,
        "csdl": {
            "name_vi": f"Corpus con — tag RAG (n={n} core)",
            "name_en": f"Corpus subset — tag RAG (n={n} core)",
            "subset": "papers WHERE 'rag' IN tags AND catalog=core",
            "count": n,
            "sample_ids": sample_ids,
            "tables": ["papers WHERE 'rag' IN tags (core subset)"],
            "tables_vi": ["papers lọc tag=rag, chỉ core citable"],
            "tables_en": ["papers filtered by tag=rag, core/citable only"],
            "explain_vi": (
                f"CSDL tab RAG là tập {n} bài core gắn tag rag"
                + (f" (năm {y0}–{y1})" if y0 and y1 else "")
                + ". Mỗi bản ghi mang summary + limitations — đây là đơn vị quan sát để lập luận hạn chế RAG, "
                "không trộn scaffold tổng hợp. Schema đầy đủ xem Tổng quan bước."
            ),
            "explain_en": (
                f"The RAG tab store is {n} core papers tagged rag"
                + (f" (years {y0}–{y1})" if y0 and y1 else "")
                + ". Each record carries summary + limitations — the observation unit for arguing RAG limits, "
                "excluding synthetic scaffold. Full schema is on the step overview."
            ),
            "role_vi": "Cung cấp bằng chứng bibliographic để biện minh gap → EDGR từ hạn chế RAG.",
            "role_en": "Provide bibliographic evidence to justify the gap → EDGR from RAG’s limits.",
        },
        "mo_hinh_toan": math,
        "mo_hinh_thuat_toan": algo,
        "mo_hinh_hoat_dong": {
            "flow": [
                "Đọc lý thuyết + lập luận khoa học RAG",
                "Đối chiếu 3 công thức tổng thể R(q), G, F/H",
                "Đọc ưu/nhược & 3 công thức cải tiến → EDGR",
                "Chạy analyze_topic(tag=rag) để lấy papers + limitations",
                "Giải thích kết quả: limitation nào khớp nhược điểm công thức/thuật toán",
            ],
            "io": {
                "in": "tag=rag, corpus core P",
                "out": "papers[], limitations[], counts — minh chứng khảo sát",
            },
            "actors": ["Researcher", "SurveyFilter", "Literature Corpus"],
            "explain_vi": (
                "Luồng hoạt động tách hai lớp minh chứng: (A) mô hình lý thuyết–toán–thuật toán RAG; "
                "(B) quan sát corpus sau khi Chạy. Lớp B không thay thế lớp A — nó kiểm chứng rằng "
                "các hạn chế mà công thức dự đoán thật sự xuất hiện trong tài liệu khảo sát."
            ),
            "explain_en": (
                "The operating flow separates two evidence layers: (A) RAG’s theory–math–algorithm model; "
                "(B) corpus observations after Run. Layer B does not replace A — it checks that the "
                "formula-predicted limitations actually appear in the surveyed literature."
            ),
        },
        "minh_chung": {
            "claim_vi": (
                f"Quan sát được {n} papers core tag=rag"
                + (f" (span {y0}–{y1})" if y0 and y1 else "")
                + f"; mẫu id: {', '.join(sample_ids[:4])}."
            ),
            "claim_en": (
                f"Observable: {n} core papers tagged rag"
                + (f" (span {y0}–{y1})" if y0 and y1 else "")
                + f"; sample ids: {', '.join(sample_ids[:4])}."
            ),
            "explain_vi": (
                "Minh chứng thiết kế (trước/đi kèm Run) là bibliographic: số lượng, năm, limitations. "
                "Cách đọc khoa học: mỗi limitation kiểu “flat retrieval / no graph / no trust gate” "
                "được ánh xạ ngược lên nhược điểm của sim(q,d) và thiếu RiskGate trong thuật toán. "
                "Sau khi nhấn Chạy, bảng papers và limitations là kết quả runtime — hãy dùng chúng để "
                "trích dẫn cụ thể khi viết gap Step 2, không chỉ nêu cảm tính rằng “RAG còn yếu”."
            ),
            "explain_en": (
                "Design evidence (before/with Run) is bibliographic: counts, years, limitations. "
                "Scientific reading: each limitation of the form “flat retrieval / no graph / no trust gate” "
                "maps back to weaknesses of sim(q,d) and the missing RiskGate. "
                "After Run, the papers and limitations tables are runtime results — cite them when writing "
                "Step-2 gaps, rather than vaguely claiming “RAG is weak”."
            ),
            "logic_vi": (
                "Luận lý chứng minh: (tiên đề) RAG = R(q)+G+F hậu kiểm → (quan sát) corpus ghi nhận hạn chế "
                "retrieval phẳng/thiếu graph-trust → (kết luận) cần thuật toán mở rộng có R_G, R_τ, ρ-gate (EDGR)."
            ),
            "logic_en": (
                "Proof sketch: (premise) RAG = R(q)+G+post-hoc F → (observation) corpus records flat-retrieval / "
                "missing graph-trust limits → (conclusion) need an extended algorithm with R_G, R_τ, ρ-gate (EDGR)."
            ),
            "paper_count": n,
            "year_min": y0,
            "year_max": y1,
            "sample_ids": sample_ids,
        },
        "nhan_dinh_danh_gia": {
            "strength": (
                "Tab RAG đã có đủ chuỗi khoa học: lý thuyết → 3 công thức tổng thể có giải thích biến → "
                "thuật toán Retrieve-then-Generate ánh xạ công thức → ưu/nhược chi tiết → 3 công thức cải tiến "
                "và pseudo-code EDGR → minh chứng corpus có luận lý ánh xạ limitation↔công thức."
            ),
            "strength_en": (
                "The RAG tab now has a full scientific chain: theory → 3 overall formulas with variable notes → "
                "Retrieve-then-Generate mapped to formulas → detailed pros/cons → 3 improvement formulas "
                "and EDGR pseudocode → corpus evidence with limitation↔formula mapping logic."
            ),
            "limitation": (
                "Tab này chưa chạy generator để đo F/H runtime trên câu hỏi CTI; "
                "điểm faithfulness thực nghiệm nằm ở các bước EDGR/đánh giá. "
                "Minh chứng tại đây là điều kiện cần (khảo sát + mô hình), chưa phải điều kiện đủ (benchmark)."
            ),
            "limitation_en": (
                "This tab does not run a generator to measure runtime F/H on CTI questions; "
                "empirical faithfulness lives in EDGR/evaluation steps. "
                "Evidence here is necessary (survey + model), not sufficient (benchmark)."
            ),
            "verdict": (
                "Đủ thuyết phục để dùng RAG làm baseline hình thức và động lực đóng góp EDGR; "
                "sau khi Chạy, hãy trích limitations cụ thể sang Step 2."
            ),
            "verdict_en": (
                "Persuasive enough to treat RAG as the formal baseline and motivation for EDGR; "
                "after Run, carry concrete limitations into Step 2."
            ),
            "score_0_1": min(0.95, 0.62 + 0.03 * n),
        },
    }


def _graphrag_pack(n: int, years: list[int], sample_ids: list[str]) -> dict[str, Any]:
    math = _critique_on_math(
        math_model(
            formula(
                id="gr_build",
                label_vi="Xây đồ thị từ corpus",
                label_en="Build graph from corpus",
                latex=r"G=(V,E),\quad V=\mathrm{Ent}(\mathcal{D}),\; E=\mathrm{Rel}(\mathcal{D})",
                explain_vi="Thực thể/quan hệ được trích từ tài liệu để tạo KG phục vụ truy hồi cấu trúc.",
                explain_en="Entities/relations are extracted from documents to form a KG for structure-aware retrieval.",
                variables=[
                    var("V", "đỉnh (thực thể)", "vertices", "", "phủ CVE/TTP"),
                    var("E", "cạnh quan hệ", "edges", "", "đúng quan hệ CTI"),
                ],
            ),
            formula(
                id="gr_retrieve",
                label_vi="Truy hồi theo đồ thị / cộng đồng",
                label_en="Graph / community retrieval",
                latex=r"R_G(q)=\mathrm{Subgraph}(G,\,\mathrm{seed}(q),\,h)",
                explain_vi="Mở rộng từ seed entities của q trong h hop (hoặc tóm tắt cộng đồng).",
                explain_en="Expand from q’s seed entities for h hops (or community summaries).",
                variables=[
                    var("h", "số hop", "hops", "h∈ℕ", "đủ quan hệ, tránh nổ"),
                ],
            ),
            formula(
                id="gr_gen",
                label_vi="Sinh có điều kiện trên đồ thị con",
                label_en="Generate conditioned on subgraph",
                latex=r"a=G(q,R_G(q))",
                explain_vi="Generator dùng bằng chứng cấu trúc thay vì chỉ đoạn văn phẳng.",
                explain_en="Generator uses structural evidence instead of flat passages only.",
            ),
            note_vi="GraphRAG = RAG + truy hồi cấu trúc trên G; vẫn thường thiếu cổng risk CTI.",
            note_en="GraphRAG = RAG + structure-aware retrieval on G; often still lacks a CTI risk gate.",
        ),
        role_vi="Mô hình toán tổng thể GraphRAG: dựng G → Subgraph → Generate.",
        role_en="Overall GraphRAG math: build G → Subgraph → Generate.",
        pros_vi=["Mạnh multi-hop / quan hệ", "Phù hợp CTI dạng đồ thị", "Cải thiện R so với sim phẳng"],
        pros_en=["Strong multi-hop / relations", "Fits graph-shaped CTI", "Improves R vs flat sim"],
        cons_vi=["Chi phí xây/duy trì G", "Ít tín hiệu trust/time", "Thiếu risk gate trước answer"],
        cons_en=["Cost to build/maintain G", "Weak trust/time signals", "No risk gate before answer"],
        improve_vi=["Thêm incremental update + temporal filter", "Thêm ranking đa tín hiệu và ρ-gate (EDGR)"],
        improve_en=["Add incremental update + temporal filter", "Add multi-signal ranking and ρ-gate (EDGR)"],
    )
    algo = _algo(
        name_vi="Graph-Retrieve-then-Generate",
        name_en="Graph-Retrieve-then-Generate",
        math_ids=["gr_build", "gr_retrieve", "gr_gen"],
        steps=["Extract Ent/Rel → G", "seed(q)", "Subgraph hops h", "Summarize paths", "a ← G(q,R_G)"],
        complexity=r"O(|E_local|+c_G)",
        pros_vi=["Bám cấu trúc quan hệ", "Khớp R_G(q)"],
        pros_en=["Respects relational structure", "Matches R_G(q)"],
        cons_vi=["Phụ thuộc chất lượng IE", "Dễ nổ subgraph"],
        cons_en=["Depends on IE quality", "Subgraph blow-up risk"],
        improve_math_vi=["Giới hạn Expand bằng budget + trust"],
        improve_math_en=["Budgeted Expand with trust"],
        improve_algo_vi=["EDGR: Expand → Temporal → Rank → RiskGate"],
        improve_algo_en=["EDGR: Expand → Temporal → Rank → RiskGate"],
    )
    seq_vi, seq_en = scientific_sequence_for("graphrag")
    return {
        "_standalone_task": True,
        "scientific_sequence_vi": seq_vi,
        "scientific_sequence_en": seq_en,
        "csdl": {
            "name_vi": f"Corpus con — GraphRAG (n={n})",
            "name_en": f"Corpus subset — GraphRAG (n={n})",
            "subset": "papers WHERE 'graphrag' IN tags",
            "count": n,
            "sample_ids": sample_ids,
            "tables": ["papers WHERE 'graphrag' IN tags (subset)"],
            "tables_vi": ["papers lọc tag=graphrag (tập con)"],
            "tables_en": ["papers filtered by tag=graphrag (subset)"],
            "explain_vi": "Tập papers GraphRAG làm minh chứng khảo sát; schema đầy đủ ở Tổng quan bước.",
            "explain_en": "GraphRAG papers as survey evidence; full schema on step overview.",
            "role_vi": "Nguồn hạn chế graph retrieval.",
            "role_en": "Source of graph-retrieval limitations.",
        },
        "mo_hinh_toan": math,
        "mo_hinh_thuat_toan": algo,
        "mo_hinh_hoat_dong": {
            "flow": [
                "Đọc lý thuyết GraphRAG",
                "Đối chiếu G, R_G, a=G(q,R_G)",
                "Chạy analyze_topic(tag=graphrag)",
                "Trích limitation quan hệ/đa bước",
            ],
            "io": {"in": "tag=graphrag", "out": "papers + limitations"},
        },
        "minh_chung": {
            "claim_vi": f"{n} papers tag=graphrag trong core.",
            "claim_en": f"{n} core papers tagged graphrag.",
            "explain_vi": "Minh chứng bibliographic cho trục GraphRAG; sau Run xem bảng limitations.",
            "explain_en": "Bibliographic evidence for GraphRAG; after Run see limitations table.",
            "logic_vi": "Limitations quan hệ → động lực EDGR φ1.",
            "logic_en": "Relational limitations → motivate EDGR φ1.",
            "paper_count": n,
            "year_min": min(years) if years else None,
            "year_max": max(years) if years else None,
            "sample_ids": sample_ids,
        },
        "nhan_dinh_danh_gia": {
            "strength": "Có mô hình G/R_G tường minh + corpus GraphRAG",
            "strength_en": "Explicit G/R_G model plus GraphRAG corpus",
            "limitation": "Chưa chạy Expand trên KG live trong tab này",
            "limitation_en": "Does not run Expand on the live KG in this tab",
            "verdict": "Đủ nối RAG phẳng → graph retrieval → EDGR",
            "verdict_en": "Enough to bridge flat RAG → graph retrieval → EDGR",
            "score_0_1": min(0.95, 0.58 + 0.04 * n),
        },
    }


def _generic_topic_pack(
    tag: str,
    *,
    title_vi: str,
    title_en: str,
    math: dict[str, Any],
    algo: dict[str, Any],
    flow: list[str],
    cites_claim_vi: str,
    cites_claim_en: str,
) -> dict[str, Any]:
    papers = papers_by_tag(tag)
    n = len(papers)
    years = sorted({p["year"] for p in papers})
    sample_ids = [p["id"] for p in papers[:5]]
    seq_vi, seq_en = scientific_sequence_for(tag)
    return {
        "_standalone_task": True,
        "scientific_sequence_vi": seq_vi,
        "scientific_sequence_en": seq_en,
        "csdl": {
            "name_vi": f"Corpus con — {title_vi} (n={n})",
            "name_en": f"Corpus subset — {title_en} (n={n})",
            "subset": f"papers WHERE '{tag}' IN tags",
            "count": n,
            "sample_ids": sample_ids,
            "tables": [f"papers WHERE '{tag}' IN tags (subset)"],
            "tables_vi": [f"papers lọc tag={tag} (tập con)"],
            "tables_en": [f"papers filtered by tag={tag} (subset)"],
            "explain_vi": f"Tập papers tag={tag}; schema đầy đủ ở Tổng quan bước.",
            "explain_en": f"Papers tagged {tag}; full schema on step overview.",
            "role_vi": f"Minh chứng khảo sát trục {title_vi}.",
            "role_en": f"Survey evidence for {title_en}.",
        },
        "mo_hinh_toan": math,
        "mo_hinh_thuat_toan": algo,
        "mo_hinh_hoat_dong": {
            "flow": flow,
            "io": {"in": f"tag={tag}", "out": "papers + limitations"},
        },
        "minh_chung": {
            "claim_vi": cites_claim_vi.format(n=n),
            "claim_en": cites_claim_en.format(n=n),
            "explain_vi": (
                "Minh chứng khảo sát (số paper/năm/limitations). "
                "Sau Chạy, bảng kết quả có giải thích/đánh giá theo từng bảng."
            ),
            "explain_en": (
                "Survey evidence (counts/years/limitations). "
                "After Run, result tables include per-table explanations."
            ),
            "logic_vi": "Quan sát corpus → hạn chế phương pháp → gap EDGR.",
            "logic_en": "Corpus observations → method limits → EDGR gaps.",
            "paper_count": n,
            "year_min": min(years) if years else None,
            "year_max": max(years) if years else None,
            "sample_ids": sample_ids,
        },
        "nhan_dinh_danh_gia": {
            "strength": f"Tab {tag}: có toán + thuật toán + minh chứng corpus",
            "strength_en": f"{tag} tab: math + algorithm + corpus evidence",
            "limitation": "Chưa thay thế đọc full-text ngoài corpus",
            "limitation_en": "Does not replace full-text reading outside the corpus",
            "verdict": "Đủ làm trục khảo sát tường minh trước bước gap",
            "verdict_en": "Enough as an explicit survey axis before the gap step",
            "score_0_1": min(0.95, 0.55 + 0.05 * n),
        },
    }


def build_topic_overlay(tag: str) -> dict[str, Any] | None:
    papers = papers_by_tag(tag)
    n = len(papers)
    years = sorted({p["year"] for p in papers})
    sample_ids = [p["id"] for p in papers[:5]]

    if tag == "rag":
        pack = _rag_pack(n, years, sample_ids)
    elif tag == "graphrag":
        pack = _graphrag_pack(n, years, sample_ids)
    elif tag == "kg":
        pack = _generic_topic_pack(
            tag,
            title_vi="Knowledge Graph",
            title_en="Knowledge Graph",
            math=_critique_on_math(
                math_model(
                    formula(
                        id="kg_triple",
                        label_vi="Bộ ba tri thức",
                        label_en="Knowledge triple",
                        latex=r"(u,r,v)\in \mathcal{T}",
                        explain_vi="Tri thức quan hệ: chủ thể u, quan hệ r, đối tượng v.",
                        explain_en="Relational knowledge: subject u, relation r, object v.",
                    ),
                    formula(
                        id="kg_query",
                        label_vi="Truy vấn / mở rộng lân cận",
                        label_en="Query / neighborhood expand",
                        latex=r"N_h(s)=\{v: \mathrm{dist}_G(s,v)\le h\}",
                        explain_vi="Tập đỉnh trong h hop từ seed s — nền của dynamic KG.",
                        explain_en="Nodes within h hops of seed s — basis of a dynamic KG.",
                    ),
                    note_vi="KG là xương sống biểu diễn; EDGR thêm cập nhật gia tăng và tín hiệu tin cậy.",
                    note_en="KG is the representation backbone; EDGR adds incremental update and trust signals.",
                ),
                role_vi="Mô hình toán tổng thể KG.",
                role_en="Overall KG mathematical model.",
                pros_vi=["Biểu diễn quan hệ rõ", "Hỗ trợ multi-hop"],
                pros_en=["Clear relations", "Supports multi-hop"],
                cons_vi=["IE lỗi → cạnh sai", "Stale nếu không update"],
                cons_en=["Bad IE → wrong edges", "Stale without updates"],
                improve_vi=["Incremental update", "Temporal + reliability trên cạnh"],
                improve_en=["Incremental update", "Temporal + reliability on edges"],
            ),
            algo=_algo(
                name_vi="Extract–Link–Store (KG pipeline)",
                name_en="Extract–Link–Store (KG pipeline)",
                math_ids=["kg_triple", "kg_query"],
                steps=["NER/RE → triples", "Link entities", "Upsert G", "Query N_h(s)"],
                complexity=r"O(|T|+|E_local|)",
                pros_vi=["Cấu trúc hóa CTI"],
                pros_en=["Structures CTI"],
                cons_vi=["Chi phí duy trì"],
                cons_en=["Maintenance cost"],
                improve_math_vi=["Thêm timestamp, reliability trên (u,r,v)"],
                improve_math_en=["Add timestamp, reliability on (u,r,v)"],
                improve_algo_vi=["EDGR Step 5: incremental + storage stats"],
                improve_algo_en=["EDGR Step 5: incremental + storage stats"],
            ),
            flow=["Đọc lý thuyết KG", "Đối chiếu (u,r,v), N_h", "Chạy analyze_topic(kg)", "Ghi hạn chế temporal/update"],
            cites_claim_vi="{n} papers tag=kg trong core.",
            cites_claim_en="{n} core papers tagged kg.",
        )
    elif tag == "hallucination":
        pack = _generic_topic_pack(
            tag,
            title_vi="Hallucination",
            title_en="Hallucination",
            math=_critique_on_math(
                math_model(
                    formula(
                        id="hall_rate",
                        label_vi="Hallucination rate",
                        label_en="Hallucination rate",
                        latex=r"H=1-F(a,R)",
                        explain_vi="Tỷ lệ bịa ≈ phần mệnh đề không được evidence hỗ trợ.",
                        explain_en="Hallucination rate ≈ fraction of unsupported claims.",
                    ),
                    formula(
                        id="risk",
                        label_vi="Risk score (hướng EDGR)",
                        label_en="Risk score (EDGR-bound)",
                        latex=r"\rho=w_H H+w_c(1-C_{\mathrm{graph}})+w_t(1-\mathrm{fresh})",
                        explain_vi="Gộp tín hiệu hallucination, inconsistency đồ thị và độ cũ.",
                        explain_en="Combines hallucination, graph inconsistency, and staleness.",
                    ),
                    note_vi="Khảo sát hallucination đặt mục tiêu giảm H; EDGR tối ưu ρ trước khi trả lời.",
                    note_en="Hallucination survey targets lower H; EDGR optimizes ρ before answering.",
                ),
                role_vi="Mô hình toán đo và giảm ảo giác.",
                role_en="Math model for measuring/reducing hallucination.",
                pros_vi=["F/H đo được", "Neo vào evidence"],
                pros_en=["F/H measurable", "Evidence-grounded"],
                cons_vi=["F hậu kiểm", "Khó với ID bịa (CVE)"],
                cons_en=["Post-hoc F", "Hard on fabricated IDs"],
                improve_vi=["Cổng ρ<θ trước generate/emit", "Graph consistency check"],
                improve_en=["ρ<θ gate before emit", "Graph consistency check"],
            ),
            algo=_algo(
                name_vi="Detect–Measure–Mitigate",
                name_en="Detect–Measure–Mitigate",
                math_ids=["hall_rate", "risk"],
                steps=["Collect claims(a)", "Check support in R", "Compute F,H", "Mitigate (retrieve/critique/gate)"],
                complexity=r"O(|claims|\cdot |R|)",
                pros_vi=["Định lượng được"],
                pros_en=["Quantifiable"],
                cons_vi=["Phụ thuộc chất lượng R"],
                cons_en=["Depends on R quality"],
                improve_math_vi=["Đưa ρ vào quyết định trả lời"],
                improve_math_en=["Feed ρ into answer decision"],
                improve_algo_vi=["EDGR RiskGate + Trusted Answer"],
                improve_algo_en=["EDGR RiskGate + Trusted Answer"],
            ),
            flow=["Đọc taxonomy hallucination", "Đối chiếu F,H,ρ", "Chạy analyze_topic", "Trích mitigation gaps"],
            cites_claim_vi="{n} papers tag=hallucination.",
            cites_claim_en="{n} papers tagged hallucination.",
        )
    elif tag == "cti":
        pack = _generic_topic_pack(
            tag,
            title_vi="CTI",
            title_en="CTI",
            math=_critique_on_math(
                math_model(
                    formula(
                        id="cti_entity",
                        label_vi="Không gian thực thể CTI",
                        label_en="CTI entity space",
                        latex=r"\mathcal{E}=\mathrm{CVE}\cup\mathrm{TTP}\cup\mathrm{Actor}\cup\mathrm{Malware}",
                        explain_vi="CTI chuẩn hóa quanh định danh và quan hệ ATT&CK/CVE.",
                        explain_en="CTI is organized around ATT&CK/CVE identifiers and relations.",
                    ),
                    formula(
                        id="cti_fresh",
                        label_vi="Độ tươi tin tức",
                        label_en="Intel freshness",
                        latex=r"\mathrm{fresh}(e)=\sigma\!\left(\frac{\tau-\mathrm{age}(e)}{\tau}\right)",
                        explain_vi="Tin cũ làm giảm độ tin cậy khi trả lời vận hành.",
                        explain_en="Stale intel lowers trust for operational answers.",
                    ),
                    note_vi="CTI đòi hỏi quan hệ + thời gian — vượt quá RAG phẳng.",
                    note_en="CTI needs relations + time — beyond flat RAG.",
                ),
                role_vi="Mô hình toán miền CTI cho EDGR.",
                role_en="CTI-domain math for EDGR.",
                pros_vi=["Chuẩn hóa ATT&CK/CVE", "Quan hệ rõ"],
                pros_en=["ATT&CK/CVE standards", "Clear relations"],
                cons_vi=["Nhiễu feed", "Stale intel"],
                cons_en=["Feed noise", "Stale intel"],
                improve_vi=["KG động + freshness trong ranking"],
                improve_en=["Dynamic KG + freshness in ranking"],
            ),
            algo=_algo(
                name_vi="Normalize–Link–Query CTI",
                name_en="Normalize–Link–Query CTI",
                math_ids=["cti_entity", "cti_fresh"],
                steps=["Ingest feeds", "Map to ATT&CK/CVE", "Link relations", "Query with freshness"],
                complexity=r"O(|E|+|R|)",
                pros_vi=["Chuẩn hóa được"],
                pros_en=["Normalizable"],
                cons_vi=["Chất lượng feed không đều"],
                cons_en=["Uneven feed quality"],
                improve_math_vi=["Gắn fresh vào s(e)"],
                improve_math_en=["Fold fresh into s(e)"],
                improve_algo_vi=["EDGR temporal filter trên CTI nodes"],
                improve_algo_en=["EDGR temporal filter on CTI nodes"],
            ),
            flow=["Đọc lý thuyết CTI", "Đối chiếu E, fresh", "Chạy analyze_topic(cti)", "Hạn chế nhiễu/stale"],
            cites_claim_vi="{n} papers tag=cti.",
            cites_claim_en="{n} papers tagged cti.",
        )
    elif tag == "ids":
        pack = _generic_topic_pack(
            tag,
            title_vi="IDS/NIDS",
            title_en="IDS/NIDS",
            math=_critique_on_math(
                math_model(
                    formula(
                        id="ids_alert",
                        label_vi="Không gian cảnh báo",
                        label_en="Alert space",
                        latex=r"A=\{a_i\},\; a_i=(\mathrm{sig},\mathrm{src},\mathrm{dst},t)",
                        explain_vi="IDS sinh alert; cần gắn tri thức CTI để giải thích.",
                        explain_en="IDS emits alerts; CTI knowledge is needed to explain them.",
                    ),
                    formula(
                        id="ids_map",
                        label_vi="Ánh xạ alert → TTP/CVE",
                        label_en="Alert → TTP/CVE mapping",
                        latex=r"\mu: A\to \mathcal{E}_{\mathrm{CTI}}",
                        explain_vi="Bài toán diễn giải: nối cảnh báo với thực thể đe dọa.",
                        explain_en="Explanation task: link alerts to threat entities.",
                    ),
                    note_vi="IDS+CTI là ngữ cảnh ứng dụng EDGR (Trusted Answer cho alert).",
                    note_en="IDS+CTI is EDGR’s application context (Trusted Answer for alerts).",
                ),
                role_vi="Mô hình toán gắn IDS với CTI/RAG.",
                role_en="Math linking IDS with CTI/RAG.",
                pros_vi=["Tín hiệu realtime", "Nhu cầu giải thích rõ"],
                pros_en=["Realtime signal", "Clear need for explanation"],
                cons_vi=["False positive", "Alert thiếu ngữ cảnh"],
                cons_en=["False positives", "Alerts lack context"],
                improve_vi=["RAG/EDGR giải thích alert bằng KG CTI"],
                improve_en=["RAG/EDGR explain alerts via CTI KG"],
            ),
            algo=_algo(
                name_vi="Detect–Enrich–Explain",
                name_en="Detect–Enrich–Explain",
                math_ids=["ids_alert", "ids_map"],
                steps=["Emit alert a", "Retrieve CTI context", "Map μ(a)", "Generate explanation"],
                complexity=r"O(c_{\mathrm{det}}+c_{\mathrm{RAG}})",
                pros_vi=["Khép vòng detect→explain"],
                pros_en=["Closes detect→explain loop"],
                cons_vi=["Phụ thuộc chất lượng μ"],
                cons_en=["Depends on μ quality"],
                improve_math_vi=["Thêm risk ρ trên explanation"],
                improve_math_en=["Add risk ρ on explanations"],
                improve_algo_vi=["EDGR Trusted Answer cho analyst"],
                improve_algo_en=["EDGR Trusted Answer for analysts"],
            ),
            flow=["Đọc lý thuyết IDS", "Đối chiếu A, μ", "Chạy analyze_topic(ids)", "Hạn chế gắn alert–tri thức"],
            cites_claim_vi="{n} papers tag=ids.",
            cites_claim_en="{n} papers tagged ids.",
        )
    else:
        return None

    return pack


TOPIC_CITES: dict[str, tuple[str, ...]] = {
    "rag": ("lewis2020rag", "gao2024ragsurvey"),
    "graphrag": ("edge2024graphrag", "guo2024lightrag"),
    "kg": ("peng2023kgllm", "edge2024graphrag"),
    "hallucination": ("ji2023survey", "huang2025hallu"),
    "cti": ("wagner2019cti", "strom2018attack"),
    "ids": ("khraisat2019ids", "ring2019nids"),
}
