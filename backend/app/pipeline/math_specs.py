"""Bilingual mathematical formula packs with explanations and optimality conditions."""

from __future__ import annotations

from typing import Any


def var(
    symbol: str,
    vi: str,
    en: str,
    domain: str = "",
    good: str = "",
) -> dict[str, str]:
    return {
        "symbol": symbol,
        "vi": vi,
        "en": en,
        "domain": domain,
        "good": good,  # when this variable is "good"
    }


def formula(
    *,
    id: str,
    label_vi: str,
    label_en: str,
    latex: str,
    explain_vi: str,
    explain_en: str,
    variables: list[dict[str, str]] | None = None,
    optimize_vi: str = "",
    optimize_en: str = "",
) -> dict[str, Any]:
    return {
        "id": id,
        "label_vi": label_vi,
        "label_en": label_en,
        "latex": latex,
        "explain_vi": explain_vi,
        "explain_en": explain_en,
        "variables": variables or [],
        "optimize_vi": optimize_vi,
        "optimize_en": optimize_en,
    }


def math_model(*formulas: dict[str, Any], note_vi: str = "", note_en: str = "") -> dict[str, Any]:
    return {
        "lang": "vi-en",
        "formulas": list(formulas),
        "note_vi": note_vi,
        "note_en": note_en,
    }


# ── Per-step packs ────────────────────────────────────────────────────

STEP_MATH: dict[int, dict[str, Any]] = {
    1: math_model(
        formula(
            id="corpus",
            label_vi="Tập công bố",
            label_en="Publication set",
            latex=r"P=\{p_1,\ldots,p_n\}",
            explain_vi="P là tập bài báo đã khảo sát; mỗi p mang tags chủ đề.",
            explain_en="P is the surveyed paper set; each p carries topic tags.",
            variables=[
                var("P", "tập papers", "paper set", "|P|≥1", "lớn và đa nguồn"),
                var("p_i", "bài báo thứ i", "i-th paper", "", "có DOI/venue rõ"),
                var("n", "số lượng papers", "number of papers", "n∈ℕ", "n đủ lớn để phủ T"),
            ],
            optimize_vi="Tốt khi n lớn và phân bố đều theo năm/venue — tránh thiên lệch một hội nghị.",
            optimize_en="Good when n is large and balanced across years/venues.",
        ),
        formula(
            id="topics",
            label_vi="Tập chủ đề khảo sát",
            label_en="Survey topic set",
            latex=r"T=\{\mathrm{rag},\mathrm{graphrag},\mathrm{kg},\mathrm{hallucination},\mathrm{cti},\mathrm{ids}\}",
            explain_vi="T gồm 6 trục đúng sơ đồ quy trình nghiên cứu.",
            explain_en="T has six axes matching the research process diagram.",
            variables=[var("T", "tập chủ đề", "topic set", "|T|=6", "đủ 6 trục")],
            optimize_vi="Tốt khi mọi t∈T đều có ít nhất một paper (C(t)>0).",
            optimize_en="Good when every t∈T has C(t)>0.",
        ),
        formula(
            id="coverage",
            label_vi="Độ phủ chủ đề",
            label_en="Topic coverage",
            latex=r"C(t)=\lvert\{p\in P:t\in\mathrm{tags}(p)\}\rvert",
            explain_vi="C(t) đếm số paper gắn tag t — đo mức độ khảo sát chủ đề.",
            explain_en="C(t) counts papers tagged t — measures topic survey depth.",
            variables=[
                var("t", "một chủ đề trong T", "a topic in T", "t∈T", ""),
                var("C(t)", "độ phủ", "coverage count", "C(t)≥0", "C(t) cao hơn = khảo sát sâu hơn"),
            ],
            optimize_vi="Kết quả khảo sát tốt khi min_t C(t) không quá nhỏ so với max_t C(t).",
            optimize_en="Survey quality is good when min_t C(t) is not much smaller than max_t C(t).",
        ),
        formula(
            id="pair",
            label_vi="Đồng xuất hiện cặp chủ đề",
            label_en="Topic co-occurrence",
            latex=r"\mathrm{Pair}(a,b)=\lvert\{p:a,b\in\mathrm{tags}(p)\}\rvert",
            explain_vi="Pair(a,b) nhỏ ⇒ giao chủ đề mỏng ⇒ tín hiệu khoảng trống nghiên cứu.",
            explain_en="Small Pair(a,b) means thin intersection ⇒ research-gap signal.",
            variables=[
                var("a,b", "hai chủ đề", "two topics", "a≠b", ""),
                var("Pair", "số paper giao", "co-occurrence count", "≥0", "thấp = gap mạnh hơn"),
            ],
            optimize_vi="Gap đáng chú ý khi Pair(a,b)≤1 với (a,b) liên quan CTI/IDS + graph/hallucination.",
            optimize_en="Notable gap when Pair(a,b)≤1 for CTI/IDS × graph/hallucination pairs.",
        ),
        note_vi="Mục tiêu bước 1: xây C và Pair đủ tin cậy để bước 2 suy gap.",
        note_en="Step-1 goal: build reliable C and Pair for step-2 gap inference.",
    ),
    2: math_model(
        formula(
            id="gap_score",
            label_vi="Điểm khoảng trống",
            label_en="Gap score",
            latex=r"\mathrm{GapScore}(a,b)=\frac{1}{1+\mathrm{Pair}(a,b)}",
            explain_vi="Pair càng nhỏ thì GapScore càng gần 1 — khoảng trống càng rõ.",
            explain_en="Smaller Pair ⇒ GapScore closer to 1 — clearer gap.",
            variables=[
                var("GapScore", "mức độ trống", "gap magnitude", "[0,1]", "cao = gap rõ"),
                var("Pair(a,b)", "đồng xuất hiện", "co-occurrence", "≥0", "thấp làm tăng GapScore"),
            ],
            optimize_vi="Ưu tiên cặp có GapScore cao VÀ liên quan miền CTI∪IDS.",
            optimize_en="Prioritize high GapScore pairs that also touch CTI∪IDS.",
        ),
        formula(
            id="priority",
            label_vi="Độ ưu tiên gap",
            label_en="Gap priority",
            latex=r"\mathrm{priority}(a,b)\propto \mathrm{GapScore}(a,b)\cdot w_{\mathrm{domain}}(a,b)",
            explain_vi="w_domain tăng trọng số nếu cặp chạm CTI/IDS/hallucination.",
            explain_en="w_domain upweights pairs touching CTI/IDS/hallucination.",
            variables=[
                var("w_domain", "trọng số miền", "domain weight", ">0", "cao với CTI/IDS"),
            ],
            optimize_vi="Chọn top gaps theo priority để ánh xạ sang đóng góp C1–C4.",
            optimize_en="Select top gaps by priority to map onto contributions C1–C4.",
        ),
    ),
    3: math_model(
        formula(
            id="objective",
            label_vi="Hàm mục tiêu",
            label_en="Objective function",
            latex=r"\min_{E'\subseteq\mathrm{Retrieve}(q,G_t,D)}\mathrm{HallucinationRisk}(\mathrm{LLM}(q\mid E'))",
            explain_vi="Chọn tập evidence E' để giảm rủi ro ảo giác của câu trả lời LLM.",
            explain_en="Choose evidence set E' to minimize LLM answer hallucination risk.",
            variables=[
                var("q", "câu hỏi CTI/IDS", "CTI/IDS query", "", "rõ ràng, chứa entity"),
                var("G_t", "KG tại thời điểm t", "KG at time t", "(V,E)", "đủ entity liên quan"),
                var("D", "kho evidence", "evidence corpus", "", "|D| đủ lớn"),
                var("E'", "tập evidence ứng viên", "candidate evidence", "E'⊆D", "nhỏ nhưng đủ phủ"),
            ],
            optimize_vi="Tốt khi risk thấp mà vẫn giữ đủ evidence liên quan (không cắt quá tay).",
            optimize_en="Good when risk is low while keeping enough relevant evidence.",
        ),
        formula(
            id="constraint",
            label_vi="Ràng buộc",
            label_en="Constraints",
            latex=r"\lvert E'\rvert\le k\land \rho(E')\le\theta",
            explain_vi="Giới hạn top-k và ngưỡng rủi ro θ trước khi sinh câu trả lời.",
            explain_en="Limit top-k and risk threshold θ before generation.",
            variables=[
                var("k", "số evidence tối đa", "max evidence count", "k∈ℕ⁺", "thường 3–5"),
                var("θ", "ngưỡng risk", "risk threshold", "θ∈(0,1)", "≈0.55 cân bằng tốt"),
                var("ρ", "rủi ro ảo giác", "hallucination risk", "[0,1]", "thấp hơn tốt hơn"),
            ],
            optimize_vi="θ quá thấp ⇒ thiếu evidence; θ quá cao ⇒ lọt evidence kém tin cậy. k quá lớn tăng nhiễu.",
            optimize_en="Too-low θ drops recall; too-high θ admits weak evidence. Too-large k adds noise.",
        ),
    ),
    4: math_model(
        formula(
            id="pipeline",
            label_vi="Pipeline EDGR",
            label_en="EDGR pipeline composition",
            latex=r"\Phi=\varphi_1\circ\varphi_2\circ\varphi_3\circ\varphi_4\circ\varphi_5\circ\varphi_6",
            explain_vi="Sáu giai đoạn nối tiếp: entity→expand→temporal→rank→score→select.",
            explain_en="Six stages in series: entity→expand→temporal→rank→score→select.",
            variables=[
                var(r"\varphi_i", "giai đoạn i", "stage i", "i=1..6", "mỗi stage có I/O rõ"),
                var(r"\Phi", "toàn pipeline", "full pipeline", "", "chạy end-to-end"),
            ],
            optimize_vi="Tốt khi mọi φ_i đóng góp dương trong ablation (ΔFaith>0 khi có mặt).",
            optimize_en="Good when each φ_i shows positive ablation delta.",
        ),
        formula(
            id="trust",
            label_vi="Điểm tin cậy evidence",
            label_en="Evidence trust score",
            latex=r"\tau(e)=0.30R+0.20F+0.25G+0.25S",
            explain_vi="Hợp nhất độ tin cậy nguồn (R), độ mới (F), nhất quán đồ thị (G), liên quan ngữ nghĩa (S).",
            explain_en="Fuses source reliability (R), freshness (F), graph consistency (G), semantic relevance (S).",
            variables=[
                var("R", "độ tin cậy nguồn", "source reliability", "[0,1]", "cao với NVD/MITRE/CISA"),
                var("F", "độ mới", "freshness", "[0,1]", "cao nếu mới; CVE lịch sử vẫn có sàn"),
                var("G", "nhất quán KG", "graph consistency", "[0,1]", "cao nếu entity gần nhau trên KG"),
                var("S", "liên quan ngữ nghĩa", "semantic relevance", "[0,1]", "cao nếu giống query"),
                var(r"\tau", "trust", "trust", "[0,1]", "càng cao càng tốt"),
            ],
            optimize_vi="Evidence tốt khi τ cao (ví dụ ≥0.75) đồng thời S không thấp — tránh tin cậy nhưng lệch chủ đề.",
            optimize_en="Good evidence has high τ (e.g. ≥0.75) and non-low S — avoid trusted-but-off-topic chunks.",
        ),
        formula(
            id="risk",
            label_vi="Rủi ro ảo giác",
            label_en="Hallucination risk",
            latex=r"\rho(e)=1-\tau(e)\in[0,1]",
            explain_vi="Risk là phần bù của trust — dùng để cổng lọc trước generation.",
            explain_en="Risk is the complement of trust — used as a pre-generation gate.",
            variables=[var(r"\rho", "rủi ro", "risk", "[0,1]", "thấp tốt")],
            optimize_vi="Chọn e với ρ≤θ; tập E* tốt khi mean(ρ) thấp và faithfulness cao.",
            optimize_en="Keep e with ρ≤θ; good E* has low mean(ρ) and high faithfulness.",
        ),
        formula(
            id="select",
            label_vi="Chọn evidence tin cậy",
            label_en="Trusted evidence selection",
            latex=r"E^{*}=\mathrm{TopK}(\{e:\rho(e)\le\theta\})",
            explain_vi="Giữ tối đa k evidence vượt cổng risk, ưu tiên khớp entity seed.",
            explain_en="Keep up to k evidence passing the risk gate, preferring seed-entity overlap.",
            variables=[
                var("E^{*}", "evidence đã chọn", "selected evidence", "|E*|≤k", "đủ phủ câu hỏi"),
                var("k", "top-k", "top-k", "3–5", "cân recall/noise"),
                var(r"\theta", "ngưỡng", "threshold", "≈0.55", "tune theo validation"),
            ],
            optimize_vi="Tốt khi E* chứa evidence gold (MRR/P@k cao) và hallucination_rate thấp.",
            optimize_en="Good when E* hits gold evidence (high MRR/P@k) and low hallucination_rate.",
        ),
        formula(
            id="complexity",
            label_vi="Độ phức tạp thời gian",
            label_en="Time complexity",
            latex=r"T(n)=O(E\log V)",
            explain_vi="Phần trội đến từ mở rộng/lân cận đồ thị kết hợp xếp hạng evidence.",
            explain_en="Dominated by graph neighborhood work plus evidence ranking.",
            variables=[
                var("V", "số đỉnh KG", "#nodes", "V≥1", ""),
                var("E", "số cạnh KG", "#edges", "E≥0", ""),
            ],
            optimize_vi="Tốt khi latency thực nghiệm tăng gần tuyến tính với |D|, không bùng nổ theo V.",
            optimize_en="Good when empirical latency scales near-linear in |D|, not explosively in V.",
        ),
    ),
    5: math_model(
        formula(
            id="graph",
            label_vi="Đồ thị động",
            label_en="Dynamic graph",
            latex=r"G_t=(V_t,E_t),\quad G_{t+1}=G_t\oplus(\Delta V,\Delta E)",
            explain_vi="KG cập nhật gia tăng bằng tập đỉnh/cạnh mới ΔV,ΔE.",
            explain_en="KG updates incrementally via new node/edge sets ΔV,ΔE.",
            variables=[
                var("V_t", "đỉnh tại t", "nodes at t", "", "phủ CVE/ATT&CK cần dùng"),
                var("E_t", "cạnh tại t", "edges at t", "", "quan hệ đúng ngữ nghĩa"),
                var(r"\Delta V,\Delta E", "phần cập nhật", "incremental delta", "", "không phá vỡ schema"),
            ],
            optimize_vi="Tốt khi incremental update tăng độ phủ mà không làm giảm consistency G.",
            optimize_en="Good when updates raise coverage without harming consistency G.",
        ),
        formula(
            id="consistency",
            label_vi="Độ nhất quán cục bộ",
            label_en="Local consistency",
            latex=r"\mathrm{Cons}(U)=\frac{|\{(u,v)\subseteq U:\mathrm{dist}(u,v)\le 2\}|}{\binom{|U|}{2}}",
            explain_vi="Tỷ lệ cặp entity trong U nối nhau trong ≤2 hop trên KG.",
            explain_en="Fraction of entity pairs in U connected within ≤2 hops.",
            variables=[
                var("U", "tập entity", "entity set", "|U|≥2", "liên quan query"),
                var("dist", "khoảng cách hop", "hop distance", "≥0", "nhỏ = gắn kết hơn"),
            ],
            optimize_vi="Cons cao hỗ trợ giảm bịa quan hệ CTI; quá thấp ⇒ evidence rời rạc.",
            optimize_en="High Cons supports fewer fabricated CTI links; too low means fragmented evidence.",
        ),
    ),
    6: math_model(
        formula(
            id="trust6",
            label_vi="Mô hình trust 4 nhân tố",
            label_en="Four-factor trust model",
            latex=r"\tau(e)=w_R R+w_F F+w_G G+w_S S,\quad w=(0.30,0.20,0.25,0.25)",
            explain_vi="Trọng số cố định phản ánh ưu tiên tin cậy nguồn và nhất quán đồ thị trong CTI.",
            explain_en="Fixed weights emphasize source trust and graph consistency for CTI.",
            variables=[
                var("w_R..w_S", "trọng số", "weights", "∑w=1", "có thể học sau này"),
                var("R,F,G,S", "nhân tố", "factors", "[0,1]", "đồng thời cao là lý tưởng"),
            ],
            optimize_vi="Evidence tối ưu: cả 4 nhân tố cao; nếu phải đánh đổi, ưu tiên R và G cho CTI.",
            optimize_en="Optimal evidence: all four high; if trade-off, prefer R and G for CTI.",
        ),
        formula(
            id="risk6",
            label_vi="Risk cổng lọc",
            label_en="Gating risk",
            latex=r"\rho(e)=1-\tau(e)",
            explain_vi="Dùng ρ để loại evidence trước khi LLM sinh câu trả lời.",
            explain_en="Use ρ to drop evidence before LLM generation.",
            variables=[var(r"\rho", "risk", "risk", "[0,1]", "<θ")],
            optimize_vi="Ngưỡng θ≈0.55 thường cân bằng tốt trên QA demo; chỉnh theo validation.",
            optimize_en="θ≈0.55 balances well on the demo QA; tune on validation.",
        ),
        formula(
            id="emit_contract",
            label_vi="Hợp đồng Trusted Answer (emit/abstain)",
            label_en="Trusted Answer contract (emit/abstain)",
            latex=r"\mathrm{Emit}(q)\iff E^{*}\neq\emptyset\land\rho(E^{*})<\theta\land\mathrm{ID}(q)\subseteq\mathrm{Supp}(E^{*},G_t)",
            explain_vi=(
                "Chỉ phát câu trả lời khi có evidence vượt cổng và định danh truy vấn "
                "(CVE/TTP) được hỗ trợ bởi E* hoặc KG; nếu không → abstain."
            ),
            explain_en=(
                "Emit only if gated evidence exists and queried IDs (CVE/TTP) are supported "
                "by E* or the KG; otherwise abstain."
            ),
            variables=[
                var(r"\theta", "ngưỡng risk", "risk threshold", "≈0.55", "tune validation"),
                var(r"\mathrm{Supp}", "tập hỗ trợ", "support set", "", "text∪KG"),
                var(r"\mathrm{ID}(q)", "định danh trong q", "IDs in query", "", "CVE/TTP…"),
            ],
            optimize_vi="Ưu tiên giảm false-emit (bịa CVE) hơn maximize answer rate — giả thuyết H2.",
            optimize_en="Prefer fewer false-emits (fabricated CVEs) over max answer rate — hypothesis H2.",
        ),
        formula(
            id="theta_tradeoff",
            label_vi="Tradeoff ngưỡng θ",
            label_en="Threshold θ tradeoff",
            latex=r"\mathrm{FR}(\theta)\uparrow\Leftarrow\theta\downarrow,\quad \mathrm{FE}(\theta)\uparrow\Leftarrow\theta\uparrow",
            explain_vi="θ thấp → từ chối nhiều hơn (FR); θ cao → dễ emit câu rủi ro (FE).",
            explain_en="Lower θ → more false rejects (FR); higher θ → more false emits (FE).",
            variables=[
                var(r"\mathrm{FR}", "false reject", "false reject", "", "abstain nhầm"),
                var(r"\mathrm{FE}", "false emit", "false emit", "", "trả lời rủi ro"),
            ],
            optimize_vi="Chọn θ trên validation để FE thấp trên OOD và Faith cao trên in-distribution.",
            optimize_en="Pick θ on validation for low FE on OOD and high Faith in-distribution.",
        ),
    ),
    7: math_model(
        formula(
            id="qa_gen",
            label_vi="Sinh QA từ cạnh KG",
            label_en="QA generation from KG edges",
            latex=r"\forall (u,r,v)\in E_{KG}:\; Q=\mathrm{ask}(u,r,v),\; A=u\!-\![r]\!\rightarrow\!v",
            explain_vi="Mỗi quan hệ KG sinh một cặp hỏi–đáp và liên kết evidence chứa u hoặc v.",
            explain_en="Each KG relation yields a QA pair linked to evidence mentioning u or v.",
            variables=[
                var("u,v", "thực thể", "entities", "∈V", "có trong evidence"),
                var("r", "quan hệ", "relation", "", "chuẩn hóa schema"),
            ],
            optimize_vi="QA tốt khi gold_evidence_ids không rỗng và câu hỏi không mơ hồ.",
            optimize_en="Good QA has non-empty gold_evidence_ids and unambiguous questions.",
        ),
    ),
    8: math_model(
        formula(
            id="serving",
            label_vi="Hàm phục vụ Trusted Answer",
            label_en="Trusted-answer serving map",
            latex=r"a=\mathrm{Gen}\big(q,\mathrm{Select}(\mathrm{Score}(\mathrm{Rank}(\mathrm{Temp}(\mathrm{Expand}(\mathrm{Extract}(q)))))))\big)",
            explain_vi="Luồng serving khớp kiến trúc: Query→EDGR↔KG/Vector→Generator→Answer.",
            explain_en="Serving flow matches architecture: Query→EDGR↔KG/Vector→Generator→Answer.",
            variables=[
                var("a", "câu trả lời tin cậy", "trusted answer", "", "bám evidence"),
                var("Gen", "bộ sinh ràng buộc evidence", "grounded generator", "", "không bịa CVE"),
            ],
            optimize_vi="Tốt khi faithfulness cao và latency chấp nhận được cho SOC assist.",
            optimize_en="Good when faithfulness is high and latency is acceptable for SOC assist.",
        ),
    ),
    9: math_model(
        formula(
            id="delta",
            label_vi="Chênh lệch so với baseline",
            label_en="Delta versus baseline",
            latex=r"\Delta_m=\mathrm{Faith}(\mathrm{EDGR})-\mathrm{Faith}(m)",
            explain_vi="So cùng query/dataset/KG; Δ>0 nghĩa là EDGR trung thực hơn method m.",
            explain_en="Same query/dataset/KG; Δ>0 means EDGR is more faithful than method m.",
            variables=[
                var("m", "baseline", "baseline method", "RAG…CRAG", ""),
                var(r"\Delta_m", "chênh faithfulness", "faithfulness delta", "", ">0 là tốt cho EDGR"),
            ],
            optimize_vi="Thành công thực nghiệm khi Δ_m≥0 trên đa số query và hallucination_rate(EDGR) thấp hơn.",
            optimize_en="Experimental success when Δ_m≥0 on most queries and EDGR hall. rate is lower.",
        ),
    ),
    10: math_model(
        formula(
            id="pk",
            label_vi="Precision@k",
            label_en="Precision@k",
            latex=r"P@k=\frac{\lvert Rel\cap TopK\rvert}{k}",
            explain_vi="Tỷ lệ evidence trong top-k thuộc tập liên quan (gold).",
            explain_en="Fraction of top-k evidence that is relevant (gold).",
            variables=[
                var("Rel", "tập gold", "gold set", "", "đúng evidence_ids"),
                var("k", "cắt top-k", "cutoff", "", "cùng k khi so sánh"),
            ],
            optimize_vi="Tốt khi P@k cao mà không đánh đổi R@k quá mạnh.",
            optimize_en="Good when P@k is high without severe R@k loss.",
        ),
        formula(
            id="mrr",
            label_vi="MRR",
            label_en="Mean Reciprocal Rank",
            latex=r"\mathrm{MRR}=\frac{1}{\mathrm{rank}^{*}}",
            explain_vi="rank* là hạng evidence gold đầu tiên; MRR=1 nếu đúng ngay vị trí 1.",
            explain_en="rank* is the first gold evidence rank; MRR=1 if gold is at rank 1.",
            variables=[var(r"\mathrm{rank}^{*}", "hạng gold đầu", "first gold rank", "≥1", "càng nhỏ càng tốt")],
            optimize_vi="Hệ retrieval tốt khi MRR gần 1.",
            optimize_en="Good retrieval pushes MRR toward 1.",
        ),
        formula(
            id="f1",
            label_vi="F1 token",
            label_en="Token F1",
            latex=r"F1=\frac{2PR}{P+R}",
            explain_vi="Cân bằng precision/recall mức token giữa answer và gold answer.",
            explain_en="Balances token-level precision/recall vs gold answer.",
            variables=[
                var("P", "precision", "precision", "[0,1]", "cao"),
                var("R", "recall", "recall", "[0,1]", "cao"),
            ],
            optimize_vi="Tối ưu khi F1 cao đồng thời faithfulness cao (tránh match từ vựng nhưng bịa ID).",
            optimize_en="Optimize for high F1 with high faithfulness (avoid lexical match with invented IDs).",
        ),
    ),
    11: math_model(
        formula(
            id="ablation_delta",
            label_vi="Delta ablation",
            label_en="Ablation delta",
            latex=r"\Delta_v=\mathrm{Faith}(\mathrm{full})-\mathrm{Faith}(v)",
            explain_vi="v là biến thể tắt một thành phần; Δ_v>0 ⇒ thành phần đó hữu ích.",
            explain_en="v disables one component; Δ_v>0 ⇒ that component is useful.",
            variables=[
                var("v", "biến thể ablation", "ablation variant", "", "w/o Graph, …"),
                var(r"\Delta_v", "đóng góp thành phần", "component contribution", "", ">0 mong muốn"),
            ],
            optimize_vi="Thiết kế tốt khi hầu hết thành phần có Δ_v>0; nếu Δ≈0 có thể đơn giản hóa.",
            optimize_en="Good design: most components have Δ_v>0; Δ≈0 suggests removable complexity.",
        ),
    ),
    12: math_model(
        formula(
            id="time",
            label_vi="Thời gian",
            label_en="Time",
            latex=r"T(n)=O(E\log V)",
            explain_vi="Cận trên tiệm cận cho expansion+ranking trên đồ thị.",
            explain_en="Asymptotic bound for expansion+ranking on the graph.",
            variables=[var("V,E", "quy mô KG", "KG scale", "", "")],
            optimize_vi="Thực nghiệm tốt nếu latency ~ tuyến tính theo |D| trong scale test.",
            optimize_en="Empirically good if latency is ~linear in |D| in scale tests.",
        ),
        formula(
            id="space",
            label_vi="Không gian",
            label_en="Space",
            latex=r"S(n)=O(V+E+D)",
            explain_vi="Bộ nhớ tỷ lệ với đỉnh, cạnh và số evidence chunks.",
            explain_en="Memory scales with nodes, edges, and evidence chunks.",
            variables=[var("D", "số chunks", "#chunks", "", "")],
            optimize_vi="Tốt khi RSS ổn định, không leak khi chạy lặp evaluation.",
            optimize_en="Good when RSS is stable with no leak across repeated evaluations.",
        ),
        formula(
            id="inv",
            label_vi="Bất biến đúng đắn",
            label_en="Correctness invariants",
            latex=r"\lvert E^{*}\rvert\le k\land \forall e\in E^{*}:\rho(e)\le\theta",
            explain_vi="Tập chọn không vượt k và mọi evidence vượt cổng risk.",
            explain_en="Selected set respects k and every item passes the risk gate.",
            variables=[],
            optimize_vi="Tốt khi invariants luôn holds trên toàn QA dataset.",
            optimize_en="Good when invariants hold on the full QA dataset.",
        ),
    ),
    13: math_model(
        formula(
            id="map",
            label_vi="Ánh xạ công bố",
            label_en="Publication mapping",
            latex=r"\mathrm{Paper}_i \leftrightarrow \mathrm{Contribution}_i \leftrightarrow \mathrm{Steps}(S_i)",
            explain_vi="Mỗi paper đóng gói một đóng góp và các bước pipeline tương ứng.",
            explain_en="Each paper packages one contribution and its pipeline steps.",
            variables=[
                var("i", "chỉ số paper", "paper index", "1..4", ""),
                var("S_i", "tập bước", "step set", "", "artifacts sẵn sàng"),
            ],
            optimize_vi="Tốt khi mỗi paper có artifact chạy thật (metrics/KG) đính kèm outline.",
            optimize_en="Good when each paper outline attaches live artifacts (metrics/KG).",
        ),
    ),
    14: math_model(
        formula(
            id="toc",
            label_vi="Cấu trúc luận án",
            label_en="Dissertation structure",
            latex=r"\mathrm{Dissertation}=\bigoplus_{c=1}^{8}\mathrm{Chapter}_c",
            explain_vi="Tám chương phủ survey→method→KG→score→experiments→conclusion.",
            explain_en="Eight chapters cover survey→method→KG→score→experiments→conclusion.",
            variables=[var("c", "số chương", "chapter no.", "1..8", "")],
            optimize_vi="Tốt khi mỗi chương map sang steps và có wordcount target rõ.",
            optimize_en="Good when each chapter maps to steps with clear wordcount targets.",
        ),
    ),
    15: math_model(
        formula(
            id="ready",
            label_vi="Mức sẵn sàng bảo vệ",
            label_en="Defense readiness",
            latex=r"\mathrm{Ready\%}=100\cdot\frac{\lvert\{c:\mathrm{ok}(c)\}\rvert}{\lvert\mathrm{checks}\rvert}",
            explain_vi="Tỷ lệ hạng mục checklist hoàn tất trước bảo vệ.",
            explain_en="Fraction of checklist items completed before defense.",
            variables=[
                var("checks", "danh mục kiểm", "checklist", "", "phủ các bước A→Z"),
                var(r"\mathrm{ok}(c)", "hạng mục đạt", "item done", "bool", "true"),
            ],
            optimize_vi="Sẵn sàng rehearsal khi Ready% cao (ví dụ ≥90) và demo metrics ổn định.",
            optimize_en="Ready for rehearsal when Ready% is high (e.g. ≥90) and demo metrics are stable.",
        ),
    ),
    16: math_model(
        formula(
            id="app",
            label_vi="Hàm ứng dụng IDS/CTI",
            label_en="IDS/CTI application function",
            latex=r"a=\mathrm{App}(q)=\mathrm{Gate}_\theta(\mathrm{EDGR}(q;G))",
            explain_vi=(
                "Ứng dụng «Phát hiện xâm nhập và tình báo» gọi EDGR trên KG G rồi "
                "chỉ emit khi ρ(a,E*)<θ."
            ),
            explain_en=(
                "The «Intrusion Detection and Threat Intelligence» app runs EDGR on graph G "
                "and emits only when ρ(a,E*)<θ."
            ),
            variables=[
                var("q", "truy vấn/alert", "query/alert", "", "IDS/CTI"),
                var("G", "KG+corpus", "KG+corpus", "", "CTI"),
                var(r"\theta", "ngưỡng rủi ro", "risk threshold", "0..1", "hyper-param"),
            ],
            optimize_vi="Tốt khi Apply(q,G)=1 đúng trên case quan hệ CTI và abstain khi OOD/evidence mỏng.",
            optimize_en="Good when Apply(q,G)=1 on relational CTI cases and abstains on OOD/thin evidence.",
        ),
        formula(
            id="apply",
            label_vi="Phân vùng triển khai",
            label_en="Deployment partition",
            latex=r"\mathrm{Apply}(q,G)\in\{0,1\}",
            explain_vi="1 = ứng dụng được (đáng EDGR); 0 = thất / fallback / abstain.",
            explain_en="1 = applicable (EDGR worth it); 0 = fail / fallback / abstain.",
            variables=[],
            optimize_vi="Liệt kê điều kiện quan sát được ở tab Ứng dụng được / thất.",
            optimize_en="List observable conditions on the success / failure tabs.",
        ),
    ),
}


def legacy_math_to_pack(math: Any) -> dict[str, Any]:
    """Upgrade old {key: latex_string} dicts into bilingual formula packs."""
    if isinstance(math, dict) and isinstance(math.get("formulas"), list) and math["formulas"]:
        return math
    if isinstance(math, str):
        return math_model(
            formula(
                id="formula",
                label_vi="Công thức",
                label_en="Formula",
                latex=math,
                explain_vi="Biểu thức gắn với tab hiện tại.",
                explain_en="Expression attached to the current tab.",
            )
        )
    formulas = []
    for key, val in (math or {}).items() if isinstance(math, dict) else []:
        if key in {"lang", "note_vi", "note_en", "formulas"}:
            continue
        if not isinstance(val, str):
            continue
        label = key.replace("_", " ")
        formulas.append(
            formula(
                id=key,
                label_vi=label,
                label_en=label,
                latex=val,
                explain_vi=f"Biểu thức `{key}` trong mô hình bước hiện tại.",
                explain_en=f"Expression `{key}` in the current step model.",
                variables=[],
                optimize_vi="Xem điều kiện tối ưu ở tổng quan bước.",
                optimize_en="See optimality notes in the step overview.",
            )
        )
    return math_model(*formulas) if formulas else math_model(
        formula(
            id="empty",
            label_vi="Chưa có công thức",
            label_en="No formula",
            latex=r"\emptyset",
            explain_vi="Tab này chưa gắn công thức chi tiết.",
            explain_en="This tab has no detailed formula yet.",
        )
    )


# EDGR stage overlays (step 4 child tasks)
STAGE_MATH: dict[str, dict[str, Any]] = {
    "s1": math_model(
        formula(
            id="extract",
            label_vi="Trích entity từ truy vấn",
            label_en="Entity extraction from query",
            latex=r"S=\mathrm{Extract}(q)\subseteq V\cup\mathrm{Regex}(\mathrm{CVE}|\mathrm{Txxxx})",
            explain_vi="S là tập seed entity: khớp nhãn trên KG hoặc regex CVE/ATT&CK.",
            explain_en="S is the seed entity set: KG label match or CVE/ATT&CK regex.",
            variables=[
                var("q", "câu hỏi", "query", "chuỗi", "có CVE/Txxxx hoặc tên kỹ thuật"),
                var("S", "seed set", "seed set", "|S|≥1 tốt", "đủ neo CTI"),
                var("V", "đỉnh KG", "KG nodes", "", ""),
            ],
            optimize_vi="Tốt khi |S|≥1 và S chứa đúng thực thể CTI trong câu hỏi (không seed nhiễu).",
            optimize_en="Good when |S|≥1 and S matches the CTI entities in the query (no noisy seeds).",
        ),
    ),
    "s2": math_model(
        formula(
            id="expand",
            label_vi="Mở rộng lân cận đồ thị",
            label_en="Graph neighborhood expansion",
            latex=r"N_h=\bigcup_{s\in S}N_h(s);\quad h=1\ \mathrm{if}\ |S|>2\ \mathrm{else}\ 2",
            explain_vi="BFS h-hop quanh seed; h thích ứng để tránh phình đồ thị khi nhiều seed.",
            explain_en="h-hop BFS around seeds; adaptive h avoids explosion when many seeds.",
            variables=[
                var("h", "số hop", "hop depth", "1 hoặc 2", "nhỏ khi |S| lớn"),
                var("N_h", "lân cận", "neighborhood", "", "liên quan CTI, không quá lớn"),
            ],
            optimize_vi="Tốt khi N_h phủ quan hệ cần thiết mà |N_h| không vượt max_nodes.",
            optimize_en="Good when N_h covers needed relations without exceeding max_nodes.",
        ),
    ),
    "s3": math_model(
        formula(
            id="temporal",
            label_vi="Lọc thời gian (giữ seed)",
            label_en="Temporal filter (keep seeds)",
            latex=r"N'=S\cup\{v\in N\setminus S:\mathrm{age}(v)\le W\}",
            explain_vi="Hàng xóm cũ hơn cửa sổ W bị loại; seed từ query luôn giữ.",
            explain_en="Neighbors older than window W are dropped; query seeds are always kept.",
            variables=[
                var("W", "cửa sổ thời gian", "time window", "ngày/tháng", "đủ cho CTI lịch sử liên quan"),
                var("N'", "tập sau lọc", "filtered set", "S⊆N'", "giữ CVE lịch sử nếu là seed"),
            ],
            optimize_vi="Tốt khi seed CVE lịch sử vẫn còn trong N' và nhiễu cũ bị loại.",
            optimize_en="Good when historical CVE seeds remain in N' and stale noise is removed.",
        ),
    ),
    "s4": math_model(
        formula(
            id="fuse",
            label_vi="Xếp hạng lai vector–đồ thị",
            label_en="Hybrid vector–graph ranking",
            latex=r"\mathrm{score}(d)=\mathrm{sim}(q,d)+\lambda\cdot\lvert\mathrm{Ent}(d)\cap N'\rvert",
            explain_vi="Cộng điểm TF-IDF với thưởng chồng entity đồ thị.",
            explain_en="TF-IDF similarity plus a bonus for graph-entity overlap.",
            variables=[
                var(r"\mathrm{sim}", "độ tương đồng", "similarity", "[0,1]", "cao với chunk đúng"),
                var(r"\lambda", "hệ số thưởng", "boost weight", ">0", "vừa phải, không át sim"),
                var("d", "chunk", "chunk", "", "có Ent(d)∩N'"),
            ],
            optimize_vi="Tốt khi top-k chứa evidence gold (P@k/MRR cao) nhờ entity boost đúng chỗ.",
            optimize_en="Good when top-k hits gold evidence (high P@k/MRR) via a well-tuned entity boost.",
        ),
    ),
    "s5": math_model(
        formula(
            id="risk_stage",
            label_vi="Chấm rủi ro ảo giác",
            label_en="Hallucination risk scoring",
            latex=r"\rho(e)=1-(0.3R+0.2F+0.25G+0.25S)",
            explain_vi="Risk = 1 − trust; trust gồm tin cậy nguồn, độ mới, nhất quán KG, liên quan.",
            explain_en="Risk = 1 − trust; trust fuses reliability, freshness, consistency, relevance.",
            variables=[
                var("R,F,G,S", "4 nhân tố", "four factors", "[0,1]", "đồng thời cao"),
                var(r"\rho", "rủi ro", "risk", "[0,1]", "thấp tốt"),
            ],
            optimize_vi="Evidence tốt khi ρ thấp (ví dụ ≤0.55) và S không thấp.",
            optimize_en="Good evidence has low ρ (e.g. ≤0.55) and non-low S.",
        ),
    ),
    "s6": math_model(
        formula(
            id="gate_gen",
            label_vi="Cổng lọc và sinh câu trả lời",
            label_en="Gate and generate answer",
            latex=r"E^{*}=\mathrm{TopK}(\{e:\rho(e)\le\theta\});\quad a=\mathrm{Gen}(q,E^{*})",
            explain_vi="Chỉ evidence qua ngưỡng θ được đưa vào generator grounded.",
            explain_en="Only evidence passing threshold θ enters the grounded generator.",
            variables=[
                var(r"\theta", "ngưỡng", "threshold", "≈0.55", "tune validation"),
                var("E^{*}", "evidence tin cậy", "trusted evidence", "|E*|≤k", "phủ câu hỏi"),
                var("a", "câu trả lời", "answer", "", "faithfulness cao"),
            ],
            optimize_vi="Tốt khi faithfulness cao, hallucination_rate thấp, và a bám E*.",
            optimize_en="Good when faithfulness is high, hallucination_rate is low, and a sticks to E*.",
        ),
    ),
    "full": math_model(
        formula(
            id="edgr",
            label_vi="Pipeline EDGR end-to-end",
            label_en="End-to-end EDGR pipeline",
            latex=r"(a,E^{*},\rho)=\mathrm{EDGR}(q,G_t,D,k,\theta)",
            explain_vi="Ánh xạ truy vấn + KG động + corpus → câu trả lời, evidence tin cậy, điểm risk.",
            explain_en="Maps query + dynamic KG + corpus → answer, trusted evidence, risk scores.",
            variables=[
                var("q", "truy vấn", "query", "", "rõ ràng, có neo CTI"),
                var("G_t", "KG tại t", "KG at t", "", "cập nhật đủ"),
                var("D", "corpus", "corpus", "", "phủ CTI"),
                var("k,θ", "siêu tham số", "hyperparams", "k≈5, θ≈0.55", "ổn định trên QA"),
            ],
            optimize_vi="Tốt khi Faith↑, Hall↓, P@k/MRR↑ so với baselines trên cùng q,D,G.",
            optimize_en="Good when Faith↑, Hall↓, P@k/MRR↑ vs baselines on the same q,D,G.",
        ),
    ),
}


# Step-7 source tabs (avoid inheriting only QA-gen formula)
SOURCE_MATH: dict[str, dict[str, Any]] = {
    "mitre": math_model(
        formula(
            id="mitre_cov",
            label_vi="Phủ ATT&CK trong KG",
            label_en="ATT&CK coverage in KG",
            latex=r"C_{\mathrm{ATT\&CK}}=\lvert\{v\in V:\mathrm{type}(v)\in\{\mathrm{technique},\mathrm{tactic}\}\}\rvert",
            explain_vi="Đếm nút technique/tactic đã nạp (seed replay) — nền cho Expand/path CTI.",
            explain_en="Counts technique/tactic nodes loaded (seed replay) — basis for CTI Expand/paths.",
            variables=[var("V", "đỉnh KG", "KG nodes", "", "có ATT&CK")],
            optimize_vi="Tốt khi C_ATT&CK đủ để path CVE–TTP không rỗng trên query mẫu.",
            optimize_en="Good when C_ATT&CK supports non-empty CVE–TTP paths on sample queries.",
        ),
    ),
    "cve": math_model(
        formula(
            id="cve_map",
            label_vi="Ánh xạ CVE→evidence",
            label_en="CVE→evidence map",
            latex=r"M_{\mathrm{CVE}}(c)=\lvert\{d\in D:c\in\mathrm{Ent}(d)\}\rvert",
            explain_vi="Số chunk chứa CVE c — đo độ phủ evidence quanh mỗi CVE node.",
            explain_en="Chunks mentioning CVE c — evidence coverage around each CVE node.",
            variables=[
                var("c", "CVE-ID", "CVE-ID", "", "có trong KG"),
                var("D", "corpus", "corpus", "", ""),
            ],
            optimize_vi="Tốt khi M_CVE(c)≥1 cho CVE trong QA gold.",
            optimize_en="Good when M_CVE(c)≥1 for CVEs in gold QA.",
        ),
    ),
    "cwe": math_model(
        formula(
            id="cwe_link",
            label_vi="Liên kết CWE–CAPEC",
            label_en="CWE–CAPEC link",
            latex=r"L=\lvert\{(u,v):u\sim\mathrm{CWE},v\sim\mathrm{CAPEC}\}\rvert",
            explain_vi="Số liên kết/weakness pattern hữu ích cho giải thích tấn.",
            explain_en="Useful weakness-pattern links for exploit explanation.",
            variables=[],
            optimize_vi="Tốt khi L>0 và CWE xuất hiện trong evidence CTI.",
            optimize_en="Good when L>0 and CWEs appear in CTI evidence.",
        ),
    ),
    "cisa": math_model(
        formula(
            id="cisa_adv",
            label_vi="Advisory → chunk",
            label_en="Advisory → chunk",
            latex=r"A_{\mathrm{CISA}}=\lvert\{d\in D:\mathrm{src}(d)\in\{\mathrm{CISA},\mathrm{CERT}\}\}\rvert",
            explain_vi="Số evidence từ advisory CISA/CERT trong seed.",
            explain_en="Evidence count from CISA/CERT advisories in the seed.",
            variables=[],
            optimize_vi="Tốt khi advisory gắn được CVE entities trong text.",
            optimize_en="Good when advisories link to CVE entities in text.",
        ),
    ),
    "feeds": math_model(
        formula(
            id="feed_act",
            label_vi="Actor/malware seed",
            label_en="Actor/malware seed",
            latex=r"F_{\mathrm{threat}}=\lvert V_{\mathrm{actor}}\rvert+\lvert V_{\mathrm{malware}}\rvert",
            explain_vi="Quy mô actor+malware trên KG threat-feed seed.",
            explain_en="Actor+malware size on the threat-feed seed KG.",
            variables=[],
            optimize_vi="Tốt khi query APT/malware expand được sang TTP liên quan.",
            optimize_en="Good when APT/malware queries expand to related TTPs.",
        ),
    ),
    "ids": math_model(
        formula(
            id="ids_ds",
            label_vi="Dataset IDS trong KG",
            label_en="IDS datasets in KG",
            latex=r"N_{\mathrm{IDS}}=\lvert\{v:\mathrm{type}(v)\in\{\mathrm{dataset},\mathrm{software}\}\}\rvert",
            explain_vi="Metadata dataset/tool IDS — không phải PCAP thô.",
            explain_en="IDS dataset/tool metadata — not raw PCAP.",
            variables=[],
            optimize_vi="Tốt khi N_IDS≥1 và có chunk mô tả khả năng phát hiện.",
            optimize_en="Good when N_IDS≥1 with chunks describing detection capability.",
        ),
    ),
    "qa": math_model(
        formula(
            id="qa_gen",
            label_vi="Sinh QA từ cạnh KG",
            label_en="QA generation from KG edges",
            latex=r"\forall (u,r,v)\in E_{KG}:\; Q=\mathrm{ask}(u,r,v),\; A=u\!-\![r]\!\rightarrow\!v",
            explain_vi="Mỗi quan hệ KG sinh một cặp hỏi–đáp gắn evidence chứa u hoặc v.",
            explain_en="Each KG relation yields a QA pair linked to evidence mentioning u or v.",
            variables=[
                var("u,v", "thực thể", "entities", "∈V", "có trong evidence"),
                var("r", "quan hệ", "relation", "", "chuẩn hóa schema"),
            ],
            optimize_vi="QA tốt khi gold_evidence_ids không rỗng và câu hỏi không mơ hồ.",
            optimize_en="Good QA has non-empty gold_evidence_ids and unambiguous questions.",
        ),
    ),
}


# Step-10 metric tabs — real formulas (not bare metric_id strings)
METRIC_MATH: dict[str, dict[str, Any]] = {
    "accuracy": math_model(
        formula(
            id="acc",
            label_vi="Accuracy",
            label_en="Accuracy",
            latex=r"\mathrm{Acc}=\frac{\lvert\{q:\mathrm{correct}(q)\}\rvert}{\lvert Q\rvert}",
            explain_vi="Tỷ lệ câu trả lời đúng trên tập QA (theo tiêu chí evaluation_service).",
            explain_en="Fraction of correct answers on the QA set (evaluation_service criterion).",
            variables=[var("Q", "tập QA", "QA set", "", "N≥1")],
            optimize_vi="Tốt khi Acc↑ đồng thời Faith↑ (không match từ vựng nhưng bịa ID).",
            optimize_en="Good when Acc↑ with Faith↑ (no lexical match with invented IDs).",
        ),
    ),
    "prf1": math_model(
        formula(
            id="f1",
            label_vi="F1 token",
            label_en="Token F1",
            latex=r"F1=\frac{2PR}{P+R}",
            explain_vi="Cân bằng precision/recall mức token giữa answer và gold.",
            explain_en="Balances token-level precision/recall vs gold answer.",
            variables=[
                var("P", "precision", "precision", "[0,1]", "cao"),
                var("R", "recall", "recall", "[0,1]", "cao"),
            ],
            optimize_vi="Tối ưu F1 kèm faithfulness cao.",
            optimize_en="Optimize F1 together with high faithfulness.",
        ),
    ),
    "faith": math_model(
        formula(
            id="faith",
            label_vi="Faithfulness",
            label_en="Faithfulness",
            latex=r"\mathrm{Faith}(a,E^{*})=1-\mathrm{Hall}(a,E^{*})",
            explain_vi="Độ trung thực = 1 − tỷ lệ ảo giác so với evidence đã chọn.",
            explain_en="Faithfulness = 1 − hallucination rate vs selected evidence.",
            variables=[
                var("a", "câu trả lời", "answer", "", "grounded"),
                var("E^{*}", "evidence chọn", "selected evidence", "", "qua cổng ρ"),
            ],
            optimize_vi="Mục tiêu chính của EDGR: Faith↑ trên miền CTI.",
            optimize_en="EDGR primary goal: Faith↑ on CTI domain.",
        ),
    ),
    "hall": math_model(
        formula(
            id="hall",
            label_vi="Hallucination rate",
            label_en="Hallucination rate",
            latex=r"\mathrm{Hall}(a,E^{*})=\mathrm{ungrounded\_claim\_rate}(a\mid E^{*})",
            explain_vi="Tỷ lệ claim không được evidence hỗ trợ (ID/CVE bịa, …).",
            explain_en="Rate of claims unsupported by evidence (invented IDs/CVEs, …).",
            variables=[],
            optimize_vi="Thành công khi Hall(EDGR) < Hall(baselines) trên cùng Q.",
            optimize_en="Success when Hall(EDGR) < Hall(baselines) on the same Q.",
        ),
    ),
    "retrieval": math_model(
        formula(
            id="pk",
            label_vi="Precision@k",
            label_en="Precision@k",
            latex=r"P@k=\frac{\lvert Rel\cap TopK\rvert}{k}",
            explain_vi="Tỷ lệ evidence top-k thuộc gold.",
            explain_en="Fraction of top-k evidence in the gold set.",
            variables=[var("k", "cắt", "cutoff", "", "cùng k khi so")],
            optimize_vi="Tốt khi P@k và MRR cùng cao.",
            optimize_en="Good when both P@k and MRR are high.",
        ),
        formula(
            id="mrr",
            label_vi="MRR",
            label_en="MRR",
            latex=r"\mathrm{MRR}=\frac{1}{\mathrm{rank}^{*}}",
            explain_vi="Hạng evidence gold đầu tiên.",
            explain_en="Rank of the first gold evidence.",
            variables=[],
            optimize_vi="MRR gần 1 là tốt.",
            optimize_en="MRR near 1 is good.",
        ),
    ),
    "latency": math_model(
        formula(
            id="lat",
            label_vi="Latency",
            label_en="Latency",
            latex=r"L=\sum_{s=1}^{6}t_s",
            explain_vi="Tổng thời gian 6 giai EDGR (ms) trên query.",
            explain_en="Sum of six EDGR stage times (ms) on a query.",
            variables=[var("t_s", "thời gian bước", "stage time", "ms", "nhỏ")],
            optimize_vi="Tốt khi L chấp nhận được cho SOC assist và scale ~ tuyến tính.",
            optimize_en="Good when L is acceptable for SOC assist and scales ~linearly.",
        ),
    ),
    "resource": math_model(
        formula(
            id="rss",
            label_vi="Bộ nhớ RSS",
            label_en="RSS memory",
            latex=r"\mathrm{RSS}\propto V+E+D",
            explain_vi="Bộ nhớ tiến trình tỷ lệ quy mô KG + corpus.",
            explain_en="Process memory scales with KG + corpus size.",
            variables=[],
            optimize_vi="Tốt khi RSS ổn định qua nhiều lần evaluate.",
            optimize_en="Good when RSS is stable across repeated evaluations.",
        ),
    ),
    "full": STEP_MATH[10],
}


def analysis_math_for(task_id: str) -> dict[str, Any]:
    """Step-12 child tabs: keep rich STEP_MATH[12], highlight focus formula."""
    pack = STEP_MATH[12]
    focus_map = {
        "time": "time",
        "space": "space",
        "correctness": "inv",
        "convergence": "inv",
        "scalability": "time",
    }
    fid = focus_map.get(task_id)
    if not fid:
        return pack
    formulas = list(pack.get("formulas") or [])
    focused = [f for f in formulas if f.get("id") == fid]
    rest = [f for f in formulas if f.get("id") != fid]
    return {
        **pack,
        "formulas": (focused + rest) if focused else formulas,
        "note_vi": f"Trọng tâm tab: {task_id}.",
        "note_en": f"Tab focus: {task_id}.",
    }


FACTOR_MATH: dict[str, dict[str, Any]] = {
    "reliability": math_model(
        formula(
            id="R",
            label_vi="Độ tin cậy nguồn",
            label_en="Source reliability",
            latex=r"R(e)=\mathrm{source\_prior}(e)\in[0,1]",
            explain_vi="Prior theo nguồn (NVD/MITRE/CISA cao hơn blog không xác thực).",
            explain_en="Prior by source (NVD/MITRE/CISA higher than unverified blogs).",
            variables=[var("R", "tin cậy nguồn", "source reliability", "[0,1]", "cao với nguồn chuẩn")],
            optimize_vi="Tốt khi R gần 1 cho evidence từ nguồn chuẩn CTI.",
            optimize_en="Good when R is near 1 for evidence from authoritative CTI sources.",
        ),
    ),
    "freshness": math_model(
        formula(
            id="F",
            label_vi="Độ mới",
            label_en="Freshness",
            latex=r"F(e)=f(\mathrm{age}(e));\ \mathrm{hist.\ CVE}: F\ge 0.45",
            explain_vi="Giảm theo tuổi; CVE lịch sử vẫn có sàn để không loại nhầm.",
            explain_en="Decays with age; historical CVEs keep a floor so they are not dropped wrongly.",
            variables=[
                var("age", "tuổi evidence", "evidence age", "≥0", "nhỏ hơn thì F cao hơn"),
                var("F", "độ mới", "freshness", "[0,1]", "≥ sàn với CVE lịch sử"),
            ],
            optimize_vi="Tốt khi F phản ánh thời gian thực nhưng không diệt CVE lịch sử liên quan.",
            optimize_en="Good when F reflects recency without killing relevant historical CVEs.",
        ),
    ),
    "consistency": math_model(
        formula(
            id="G",
            label_vi="Nhất quán đồ thị",
            label_en="Graph consistency",
            latex=r"G(e)=\mathrm{path\_consistency}(\mathrm{Ent}(e)\cup S)",
            explain_vi="Entity trong evidence gắn kết với seed trên KG (khoảng cách hop ngắn).",
            explain_en="Evidence entities cohere with seeds on the KG (short hop distance).",
            variables=[var("G", "nhất quán", "consistency", "[0,1]", "cao khi gần seed")],
            optimize_vi="Tốt khi G cao — entity không rời rạc khỏi ngữ cảnh CTI của query.",
            optimize_en="Good when G is high — entities are not disconnected from the query CTI context.",
        ),
    ),
    "relevance": math_model(
        formula(
            id="S",
            label_vi="Liên quan ngữ nghĩa",
            label_en="Semantic relevance",
            latex=r"S(e)=\cos(\mathrm{TFIDF}(q),\mathrm{TFIDF}(e))",
            explain_vi="Cosine TF-IDF giữa query và evidence chunk.",
            explain_en="TF-IDF cosine between query and evidence chunk.",
            variables=[var("S", "liên quan", "relevance", "[0,1]", "cao với chunk đúng chủ đề")],
            optimize_vi="Tốt khi S cao đồng thời R/G không thấp — tránh chunk giống từ nhưng sai nguồn.",
            optimize_en="Good when S is high and R/G are not low — avoid lexically similar but wrong-source chunks.",
        ),
    ),
    "score": math_model(
        formula(
            id="rho_w",
            label_vi="Risk tổng hợp có trọng số",
            label_en="Weighted aggregate risk",
            latex=r"\rho(e)=1-\sum_i w_i f_i(e),\quad f\in\{R,F,G,S\}",
            explain_vi="Hợp nhất 4 nhân tố thành risk cổng lọc.",
            explain_en="Fuses the four factors into gating risk.",
            variables=[
                var("w_i", "trọng số", "weights", "∑w=1", "ưu tiên R,G cho CTI"),
                var(r"\rho", "risk", "risk", "[0,1]", "≤θ"),
            ],
            optimize_vi="Tốt khi ρ≤θ và các f_i cùng cao — không chỉ một nhân tố bù trừ.",
            optimize_en="Good when ρ≤θ and all f_i are jointly high — not one factor compensating alone.",
        ),
    ),
}
