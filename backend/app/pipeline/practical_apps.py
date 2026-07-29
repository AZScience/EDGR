"""
Step 16 — practical application product:

  «Phát hiện xâm nhập và tình báo» / Intrusion Detection & Threat Intelligence

Child tabs: product brief, success cases, failure cases, live demo.
"""

from __future__ import annotations

from typing import Any


APP_NAME_VI = "Phát hiện xâm nhập và tình báo"
APP_NAME_EN = "Intrusion Detection and Threat Intelligence"


def app_product_doc() -> dict[str, Any]:
    return {
        "kind": "ids_cti_app_product",
        "app_name_vi": APP_NAME_VI,
        "app_name_en": APP_NAME_EN,
        "tagline_vi": (
            "Trợ lý SOC gắn alert / câu hỏi CTI vào đồ thị ATT&CK–CVE–evidence, "
            "truy hồi bằng EDGR và chỉ phát câu trả lời khi rủi ro ảo giác dưới ngưỡng."
        ),
        "tagline_en": (
            "A SOC assistant that binds alerts / CTI questions to an ATT&CK–CVE–evidence graph, "
            "retrieves with EDGR, and emits answers only when hallucination risk is below threshold."
        ),
        "problem_vi": (
            "Nhà phân tích IDS nhận hàng loạt cảnh báo và phải nối nhanh sang kỹ thuật ATT&CK, "
            "CVE liên quan và advisory còn hạn. Trả lời “nghe giống CTI” nhưng không neo bằng chứng "
            "dễ đẩy hướng xử lý sai."
        ),
        "problem_en": (
            "IDS analysts face alert floods and must quickly link ATT&CK techniques, "
            "related CVEs, and in-window advisories. CTI-sounding answers without evidence "
            "steer response the wrong way."
        ),
        "users_vi": ["SOC tier-1/2", "CTI analyst", "Nghiên cứu sinh demo luận án"],
        "users_en": ["SOC tier-1/2", "CTI analyst", "Thesis demo operator"],
        "capabilities_vi": [
            "Nhận câu hỏi hoặc mô tả alert (CVE, technique, lateral movement…)",
            "Trích entity → Expand KG CTI → lọc thời gian → xếp hạng evidence",
            "Chấm ρ và cổng từ chối trước khi trả Trusted Answer",
            "Hiển thị evidence + (khi có) đồ thị lân cận phục vụ kiểm tra tay",
        ],
        "capabilities_en": [
            "Accept a question or alert description (CVE, technique, lateral movement…)",
            "Extract entities → Expand CTI KG → temporal filter → rank evidence",
            "Score ρ and gate emission before a Trusted Answer",
            "Show evidence and (when available) a neighborhood graph for human check",
        ],
        "architecture_flow": [
            "Alert / Query",
            "EDGR φ1–φ6",
            "Dynamic CTI KG + Vector store",
            "Hallucination gate (ρ, θ)",
            "Trusted Answer + Evidence",
        ],
        "depends_on_steps": [4, 5, 6, 7, 8],
        "non_goals_vi": [
            "Không thay thế IDS engine (Snort/Suricata/…) — chỉ lớp giải thích/truy hồi tri thức",
            "Không cam kết production SLA; đây là ứng dụng demo khoa học có kiểm soát giả định",
        ],
        "non_goals_en": [
            "Does not replace an IDS engine (Snort/Suricata/…) — knowledge retrieval/explanation layer only",
            "No production SLA claim; a scientific demo with stated assumptions",
        ],
        "how_to_use_vi": (
            "Tab này chốt sản phẩm ứng dụng. Tab «Ứng dụng được / thất» nêu biên triển khai; "
            "tab «Chạy thử» gọi pipeline EDGR trên truy vấn mẫu."
        ),
        "how_to_use_en": (
            "This tab locks the product definition. Success/failure tabs state deployment bounds; "
            "the demo tab runs the EDGR pipeline on a sample query."
        ),
    }


def _success_cases() -> list[dict[str, Any]]:
    return [
        {
            "id": "S1",
            "title_vi": "Hỏi chuỗi quan hệ CVE → kỹ thuật ATT&CK → tác động",
            "title_en": "Relational queries: CVE → ATT&CK technique → impact",
            "scenario_vi": (
                "Analyst hỏi CVE-2021-44228 gắn kỹ thuật nào và chuỗi khai thác công cộng "
                "trông như thế nào — cần cạnh quan hệ, không chỉ đoạn văn chứa mã CVE."
            ),
            "scenario_en": (
                "An analyst asks which technique CVE-2021-44228 maps to and what a public "
                "exploit chain looks like — relational edges matter, not only passages naming the CVE."
            ),
            "why_works_vi": (
                "Expand trên KG giữ cạnh enables/uses; TemporalFilter giữ seed CVE lịch sử "
                "nếu còn liên quan; EvidenceRank ưu tiên đoạn neo entity; ρ-gate chặn claim TTP không có trong E*."
            ),
            "why_works_en": (
                "Graph Expand keeps enables/uses edges; TemporalFilter retains historical CVE seeds "
                "when still relevant; EvidenceRank boosts entity-grounded passages; "
                "the ρ-gate blocks TTP claims absent from E*."
            ),
            "boundary_vi": "Cần schema CTI đủ cạnh CVE–technique; IE kém sẽ làm Expand lệch.",
            "boundary_en": "Needs a CTI schema with CVE–technique edges; weak IE skews Expand.",
            "pipeline_artifacts": ["Step5 KG", "Step4 Expand/Rank", "Step9 compare (relational slice)"],
            "demo_query_hint": "What is CVE-2021-44228 and how is it exploited?",
        },
        {
            "id": "S2",
            "title_vi": "Trả lời CTI khi bằng chứng có tuổi khác nhau",
            "title_en": "CTI answers when evidence ages differ",
            "scenario_vi": (
                "Cùng entity trong advisory cũ và feed mới; ưu tiên bằng chứng còn hạn "
                "mà không xóa ngữ cảnh lịch sử của seed truy vấn."
            ),
            "scenario_en": (
                "Same entity in an old advisory and a new feed; prefer in-window evidence "
                "without wiping historical context of query seeds."
            ),
            "why_works_vi": "φ3 TemporalFilter + freshness trong scoring tách stale noise khỏi seed.",
            "why_works_en": "φ3 TemporalFilter plus freshness scoring separates stale noise from seeds.",
            "boundary_vi": "Thiếu timestamp → lọc thời gian gần như vô hiệu.",
            "boundary_en": "Missing timestamps nearly disable temporal filtering.",
            "pipeline_artifacts": ["Step6 freshness", "Step4 TemporalFilter", "Step5 sources"],
            "demo_query_hint": "Which CVE did Cl0p exploit in MOVEit campaigns?",
        },
        {
            "id": "S3",
            "title_vi": "Từ chối trả lời khi rủi ro ảo giác cao",
            "title_en": "Abstain when hallucination risk is high",
            "scenario_vi": "Evidence mỏng hoặc mâu thuẫn — trả lời tự tin lúc này nguy hiểm hơn im lặng có kiểm soát.",
            "scenario_en": "Thin or conflicting evidence — a confident guess is more dangerous than controlled silence.",
            "why_works_vi": "ρ-gate biến “không chắc” thành reject/abstain thay vì sinh câu CTI nghe có vẻ đúng.",
            "why_works_en": "The ρ-gate turns uncertainty into reject/abstain instead of a CTI-sounding guess.",
            "boundary_vi": "θ quá thấp → từ chối nhiều; θ quá cao → vẫn lọt claim yếu.",
            "boundary_en": "θ too low → over-abstain; θ too high → weak claims still pass.",
            "pipeline_artifacts": ["Step6 composite score", "Step4 RiskGate", "Step10 hall metric"],
            "demo_query_hint": "How does EDGR reduce hallucination in CTI answers?",
        },
        {
            "id": "S4",
            "title_vi": "Diễn giải cảnh báo IDS gắn tri thức ngoài",
            "title_en": "Explaining IDS alerts with external CTI knowledge",
            "scenario_vi": (
                "Cảnh báo NIDS về lateral movement cần gắn kỹ thuật ATT&CK và CVE liên quan "
                "để ưu tiên — không chỉ lặp chữ trong log."
            ),
            "scenario_en": (
                "A NIDS lateral-movement alert needs ATT&CK techniques and related CVEs "
                "for prioritization — not merely repeating log tokens."
            ),
            "why_works_vi": "Ingest IDS + CTI vào cùng KG; truy vấn từ alert entities mở rộng sang technique/CVE.",
            "why_works_en": "IDS + CTI land in one KG; queries from alert entities expand into technique/CVE.",
            "boundary_vi": "Alert thiếu entity extractable → seed yếu, Expand không khởi động được.",
            "boundary_en": "Alerts without extractable entities yield weak seeds; Expand cannot start.",
            "pipeline_artifacts": ["Step7 IDS ingest", "Step8 e2e", "Step1 ids topic"],
            "demo_query_hint": "How can NIDS detect lateral movement?",
        },
    ]


def _failure_cases() -> list[dict[str, Any]]:
    return [
        {
            "id": "F1",
            "title_vi": "Câu hỏi single-hop thuần lexical",
            "title_en": "Purely lexical single-hop questions",
            "scenario_vi": "Định nghĩa ngắn hoặc tra cứu một mã đã nằm gọn trong một đoạn vàng — không cần đa hop.",
            "scenario_en": "Short definition or lookup already in one gold passage — no multi-hop needed.",
            "why_fails_vi": (
                "Chi phí Expand + ranking đa tín hiệu không đổi lấy lại độ chính xác; "
                "RAG phẳng thường đủ và nhanh hơn."
            ),
            "why_fails_en": (
                "Expand + multi-signal ranking cost is not repaid; flat RAG is often enough and faster."
            ),
            "mitigation_vi": "Router: nếu không có quan hệ/seed KG → fallback RAG.",
            "mitigation_en": "Router: if no relation/KG seed → fall back to RAG.",
            "pipeline_artifacts": ["Step9 compare (lexical slice)", "Step11 w/o graph"],
            "honest_line_vi": "Ứng dụng không thắng baseline trên mọi câu hỏi.",
            "honest_line_en": "The app does not beat baselines on every question.",
        },
        {
            "id": "F2",
            "title_vi": "KG thiếu cạnh hoặc IE nhiễu",
            "title_en": "Missing graph edges or noisy IE",
            "scenario_vi": "Nguồn mới chưa ingest; hoặc trích xuất gán sai quan hệ CVE–technique.",
            "scenario_en": "New sources not ingested; or extraction assigns a wrong CVE–technique link.",
            "why_fails_vi": "Expand khuếch đại lỗi cấu trúc; ρ-gate giảm hại nhưng không sửa đồ thị.",
            "why_fails_en": "Expand amplifies structural error; the ρ-gate reduces harm but does not repair the graph.",
            "mitigation_vi": "Ưu tiên chất lượng ingest; giám sát ΔV/ΔE; human-in-loop cho cạnh critical.",
            "mitigation_en": "Prioritize ingest quality; monitor ΔV/ΔE; human-in-loop for critical edges.",
            "pipeline_artifacts": ["Step5 extract/incremental", "Step12 threats"],
            "honest_line_vi": "Lớp ứng dụng không thay thế curation CTI.",
            "honest_line_en": "The app layer does not replace CTI curation.",
        },
        {
            "id": "F3",
            "title_vi": "Generator / nhãn faithfulness ngoài giả định demo",
            "title_en": "Generator / faithfulness labels outside demo assumptions",
            "scenario_vi": "Triển khai LLM API tự do hoặc chấm F bằng model nhiễu.",
            "scenario_en": "Unconstrained LLM API, or scoring F with a noisy automatic judge.",
            "why_fails_vi": (
                "Demo dùng generator ràng buộc evidence; số F/H trên pipeline "
                "không chuyển nguyên xi sang production LLM tự do."
            ),
            "why_fails_en": (
                "The demo uses an evidence-constrained generator; F/H numbers do not transfer "
                "unchanged to unconstrained production LLMs."
            ),
            "mitigation_vi": "Tách claim: app cải thiện E* + cổng emit; generator đo lại độc lập.",
            "mitigation_en": "Split the claim: the app improves E* + emit gate; re-measure the generator separately.",
            "pipeline_artifacts": ["Step10 metrics", "Paper 1 Limitations"],
            "honest_line_vi": "Không viết như đã production-harden mọi LLM.",
            "honest_line_en": "Do not write as if every LLM were production-hardened.",
        },
        {
            "id": "F4",
            "title_vi": "Truy vấn ngoài miền / entity không có trong KG",
            "title_en": "Out-of-domain queries / entities absent from the KG",
            "scenario_vi": "Malware/CVE chưa có trong đồ thị demo, hoặc câu hỏi ngoài CTI/IDS.",
            "scenario_en": "Malware/CVEs absent from the demo graph, or questions outside CTI/IDS.",
            "why_fails_vi": "Seed rỗng → Expand trống → thoái hóa retrieval yếu hoặc abstain hàng loạt.",
            "why_fails_en": "Empty seeds → empty Expand → weak retrieval or mass abstention.",
            "mitigation_vi": "Phát hiện OOD; trả “không đủ bằng chứng” + gợi ý nguồn cần bổ sung.",
            "mitigation_en": "Detect OOD; answer “insufficient evidence” and suggest sources to ingest.",
            "pipeline_artifacts": ["Step4 Understand/Extract", "Step6 gate"],
            "honest_line_vi": "Phạm vi ứng dụng = phạm vi KG + corpus đã phủ.",
            "honest_line_en": "Application scope equals KG + corpus coverage.",
        },
    ]


def practical_apps_doc(*, bucket: str | None = None) -> dict[str, Any]:
    """Full S+F doc, or filtered by bucket 'success' | 'failure'."""
    successes = _success_cases()
    failures = _failure_cases()
    if bucket == "success":
        failures = []
    elif bucket == "failure":
        successes = []

    title_vi = f"Ứng dụng «{APP_NAME_VI}»"
    title_en = f"Application «{APP_NAME_EN}»"
    if bucket == "success":
        title_vi += " — ứng dụng được"
        title_en += " — where it works"
    elif bucket == "failure":
        title_vi += " — ứng dụng thất"
        title_en += " — where it fails"

    return {
        "kind": "practical_applications",
        "app_name_vi": APP_NAME_VI,
        "app_name_en": APP_NAME_EN,
        "bucket": bucket or "all",
        "title_vi": title_vi,
        "title_en": title_en,
        "lead_vi": (
            f"Ứng dụng thực tế «{APP_NAME_VI}» chỉ thuyết phục khi nói rõ tình huống đáng triển khai "
            "và khi nào nên fallback/abstain. "
            + (
                "Tab này liệt kê các case ứng dụng được."
                if bucket == "success"
                else (
                    "Tab này liệt kê các case ứng dụng thất / không đáng — kèm mitigation."
                    if bucket == "failure"
                    else "Hai nhóm dưới đây đưa vào Discussion và trả lời hội đồng."
                )
            )
        ),
        "lead_en": (
            f"The practical app «{APP_NAME_EN}» is persuasive only when it states where deployment "
            "is worthwhile and when to fall back/abstain. "
            + (
                "This tab lists success cases."
                if bucket == "success"
                else (
                    "This tab lists failure / not-worth-it cases with mitigations."
                    if bucket == "failure"
                    else "The two groups below feed Discussion and committee Q&A."
                )
            )
        ),
        "how_to_use_vi": (
            "Mỗi case: bối cảnh → vì sao khớp/không → điều kiện biên hoặc mitigation → artifact. "
            "Không phóng đại “ứng dụng được mọi nơi”."
        ),
        "how_to_use_en": (
            "Each case: context → why it fits/does not → boundary or mitigation → artifact. "
            "Do not claim “works everywhere”."
        ),
        "successes": successes,
        "failures": failures,
        "committee_takeaway_vi": [
            f"Sản phẩm: trợ lý «{APP_NAME_VI}» trên pipeline EDGR + KG CTI.",
            "Ứng dụng được: quan hệ CTI, bằng chứng đa tuổi, cần cổng từ chối, diễn giải alert→TTP/CVE.",
            "Ứng dụng thất: lexical đơn giản, KG hỏng, OOD, generator ngoài giả định.",
        ],
        "committee_takeaway_en": [
            f"Product: «{APP_NAME_EN}» assistant on EDGR + CTI KG.",
            "Works: relational CTI, mixed-age evidence, abstain gate, alert→TTP/CVE.",
            "Fails: simple lexical, broken KG, OOD, generator outside assumptions.",
        ],
        "maps_to_steps": [4, 5, 6, 8, 9, 10, 11],
    }


def classify_query_hint(query: str) -> dict[str, Any]:
    """Lightweight heuristic for demo Run — not a trained router."""
    q = (query or "").lower()
    hits: list[str] = []
    if any(x in q for x in ("cve-", "att&ck", "apt", "ttp", "exploit", "technique")):
        hits.append("S1")
    if any(x in q for x in ("cl0p", "moveit", "kev", "fresh", "recent", "2023", "2024")):
        hits.append("S2")
    if any(x in q for x in ("hallucin", "edgr", "trusted", "risk")):
        hits.append("S3")
    if any(x in q for x in ("nids", "ids", "lateral", "alert", "detect")):
        hits.append("S4")
    if any(x in q for x in ("what is ", "define ", "definition")) and "cve-" not in q:
        hits.append("F1")
    if any(x in q for x in ("legal", "gdpr", "privacy law", "outside")):
        hits.append("F4")

    doc = practical_apps_doc()
    by_id = {c["id"]: c for c in doc["successes"] + doc["failures"]}
    matched = [by_id[i] for i in hits if i in by_id]
    if not matched:
        matched = [by_id["S1"], by_id["F1"]]
        hits = ["S1", "F1"]
        note_vi = "Không khớp mạnh rule demo — gợi ý cặp S1 (quan hệ) vs F1 (lexical)."
        note_en = "No strong demo-rule match — suggesting S1 (relational) vs F1 (lexical)."
    else:
        note_vi = "Gợi ý case theo từ khóa truy vấn (heuristic demo)."
        note_en = "Case hints from query keywords (demo heuristic)."

    success_ids = [i for i in hits if i.startswith("S")]
    failure_ids = [i for i in hits if i.startswith("F")]
    return {
        "query": query,
        "matched_ids": hits,
        "lean_vi": (
            "Nghiêng ứng dụng được"
            if len(success_ids) > len(failure_ids)
            else ("Nghiêng ứng dụng thất / thận trọng" if failure_ids else "Cần xem xét thủ công")
        ),
        "lean_en": (
            "Leans toward applicable"
            if len(success_ids) > len(failure_ids)
            else ("Leans toward failure / caution" if failure_ids else "Needs manual review")
        ),
        "matched_cases": [
            {
                "id": c["id"],
                "title_vi": c["title_vi"],
                "title_en": c["title_en"],
                "bucket": "success" if c["id"].startswith("S") else "failure",
            }
            for c in matched
        ],
        "note_vi": note_vi,
        "note_en": note_en,
    }


def get_practical_apps_package(
    params: dict[str, Any] | None = None,
    *,
    bucket: str | None = None,
) -> dict[str, Any]:
    params = params or {}
    doc = practical_apps_doc(bucket=bucket)
    q = str(params.get("query") or "")
    out = dict(doc)
    out["status"] = "apps_ready"
    out["counts"] = {
        "successes": len(doc["successes"]),
        "failures": len(doc["failures"]),
    }
    out["query_classification"] = classify_query_hint(q) if q.strip() else None
    out["computation_kind"] = "practical_applications"
    return out


def get_app_product_package() -> dict[str, Any]:
    doc = app_product_doc()
    return {
        **doc,
        "status": "product_ready",
        "computation_kind": "ids_cti_app_product",
    }


def _mirror_seq(overlay: dict[str, Any]) -> dict[str, Any]:
    seq = overlay.get("scientific_sequence_vi")
    if isinstance(seq, list):
        overlay["scientific_sequence_en"] = seq
    return overlay


def get_app_product_academic_overlay() -> dict[str, Any]:
    doc = app_product_doc()
    return _mirror_seq(
        {
            "_standalone_task": True,
            "scientific_sequence_vi": [
                {
                    "id": "theory",
                    "title_vi": "Sản phẩm ứng dụng IDS/CTI",
                    "title_en": "IDS/CTI application product",
                    "explain_vi": doc["tagline_vi"],
                    "explain_en": doc["tagline_en"],
                    "anchor": "sci-theory",
                },
                {
                    "id": "arch",
                    "title_vi": "Kiến trúc vận hành",
                    "title_en": "Operating architecture",
                    "explain_vi": "Alert/Query → EDGR → KG/Vector → ρ-gate → Trusted Answer.",
                    "explain_en": "Alert/Query → EDGR → KG/Vector → ρ-gate → Trusted Answer.",
                    "anchor": "sci-ops",
                },
                {
                    "id": "bounds",
                    "title_vi": "Biên triển khai (tab được/thất)",
                    "title_en": "Deployment bounds (success/failure tabs)",
                    "explain_vi": "Sang tab Ứng dụng được / thất để nêu điều kiện Apply∈{0,1}.",
                    "explain_en": "Use success/failure tabs for Apply∈{0,1} conditions.",
                    "anchor": "sci-ev",
                },
            ],
            "csdl": {
                "name_vi": f"Hồ sơ ứng dụng — {APP_NAME_VI}",
                "name_en": f"Application profile — {APP_NAME_EN}",
                "explain_vi": "Lưu mô tả sản phẩm, user, năng lực, non-goals, phụ thuộc bước pipeline.",
                "explain_en": "Stores product brief, users, capabilities, non-goals, pipeline dependencies.",
                "tables_vi": ["app_profile", "capabilities", "depends_on_steps"],
                "tables_en": ["app_profile", "capabilities", "depends_on_steps"],
                "role_vi": "Chốt đối tượng demo khoa học của luận án.",
                "role_en": "Locks the thesis’s scientific demo product.",
            },
            "mo_hinh_toan": {
                "lang": "vi-en",
                "role_vi": "Ánh xạ sản phẩm → pipeline: App = EDGR ∘ (KG, Vector, Gate).",
                "role_en": "Product map: App = EDGR ∘ (KG, Vector, Gate).",
                "narrative_vi": (
                    f"Ứng dụng «{APP_NAME_VI}» không invent thuật toán mới ở bước này; "
                    "nó đóng gói Steps 4–8 thành trải nghiệm SOC có I/O rõ và giả định biên."
                ),
                "narrative_en": (
                    f"The «{APP_NAME_EN}» app does not invent a new algorithm here; "
                    "it packages Steps 4–8 into a SOC experience with clear I/O and bounds."
                ),
                "formulas": [
                    {
                        "id": "app",
                        "label_vi": "Hàm ứng dụng",
                        "label_en": "Application function",
                        "latex": r"a=\mathrm{App}(q)=\mathrm{Gate}_\theta(\mathrm{EDGR}(q;G))",
                        "explain_vi": "Chỉ emit khi ρ(a,E*)<θ; ngược lại abstain.",
                        "explain_en": "Emit only if ρ(a,E*)<θ; otherwise abstain.",
                        "variables": [],
                    }
                ],
            },
            "mo_hinh_thuat_toan": {
                "name_vi": f"Luồng ứng dụng «{APP_NAME_VI}»",
                "name_en": f"«{APP_NAME_EN}» application flow",
                "math_ids": ["app"],
                "pseudocode": [
                    "Nhận alert hoặc câu hỏi CTI q",
                    "Gọi EDGR φ1–φ6 trên KG/Vector",
                    "Nếu ρ ≥ θ → trả abstain + lý do",
                    "Ngược lại → Trusted Answer + evidence ids",
                    "Ghi log case S/F cho cải tiến sau",
                ],
                "complexity": r"O(\mathrm{EDGR})",
                "narrative_vi": "Thuật toán lõi vẫn là EDGR; bước 16 là lớp sản phẩm.",
                "narrative_en": "The core algorithm remains EDGR; step 16 is the product layer.",
                "pros_vi": ["I/O rõ cho SOC", "Neo artifact Steps 4–8"],
                "pros_en": ["Clear SOC I/O", "Tied to Steps 4–8 artifacts"],
                "cons_vi": ["Phụ thuộc chất lượng KG", "Chưa phải bản production"],
                "cons_en": ["Depends on KG quality", "Not a production build"],
                "improve_algo_vi": ["Thêm router Apply(q,G) học từ log"],
                "improve_algo_en": ["Add a learned Apply(q,G) router from logs"],
                "improve_math_vi": [],
                "improve_math_en": [],
            },
            "mo_hinh_hoat_dong": {
                **doc,
                "kind": "ids_cti_app_product",
                "flow": doc["architecture_flow"],
                "explain_vi": doc["how_to_use_vi"],
                "explain_en": doc["how_to_use_en"],
                "io": {
                    "in": "alert text / CTI question",
                    "out": "trusted answer | abstain + evidence",
                },
            },
            "minh_chung": {
                "claim_vi": (
                    f"Luận án có một ứng dụng demo đóng gói: «{APP_NAME_VI}», "
                    "dùng EDGR trên KG CTI với cổng ρ."
                ),
                "claim_en": (
                    f"The thesis packages one demo application: «{APP_NAME_EN}», "
                    "using EDGR on a CTI KG with a ρ-gate."
                ),
                "explain_vi": "Minh chứng thiết kế = hồ sơ sản phẩm; runtime = tab Chạy thử.",
                "explain_en": "Design evidence = product profile; runtime = Demo tab.",
            },
            "nhan_dinh_danh_gia": {
                "strength": "Chốt tên sản phẩm, user, năng lực và non-goals rõ",
                "strength_en": "Clear product name, users, capabilities, and non-goals",
                "limitation": "Chưa phải triển khai SOC production",
                "limitation_en": "Not a production SOC deployment",
                "verdict": "Đủ làm ứng dụng thực tế cho demo luận án",
                "verdict_en": "Enough as a thesis demo practical application",
                "score_0_1": 0.86,
            },
        }
    )


def get_practical_apps_academic_overlay(*, bucket: str | None = None) -> dict[str, Any]:
    doc = practical_apps_doc(bucket=bucket)
    success_label = "Ứng dụng được" if bucket != "failure" else "— "
    fail_label = "Ứng dụng thất" if bucket != "success" else "—"
    return _mirror_seq(
        {
            "_standalone_task": True,
            "scientific_sequence_vi": [
                {
                    "id": "theory",
                    "title_vi": f"Biên của «{APP_NAME_VI}»",
                    "title_en": f"Bounds of «{APP_NAME_EN}»",
                    "explain_vi": doc["lead_vi"],
                    "explain_en": doc["lead_en"],
                    "anchor": "sci-theory",
                },
                {
                    "id": "cases",
                    "title_vi": success_label if bucket == "success" else (
                        fail_label if bucket == "failure" else "Case S/F"
                    ),
                    "title_en": "Success cases" if bucket == "success" else (
                        "Failure cases" if bucket == "failure" else "S/F cases"
                    ),
                    "explain_vi": doc["how_to_use_vi"],
                    "explain_en": doc["how_to_use_en"],
                    "anchor": "sci-ops",
                },
            ],
            "csdl": {
                "name_vi": "Kho case triển khai ứng dụng",
                "name_en": "Application deployment case store",
                "explain_vi": "Case successes/failures gắn sản phẩm IDS/CTI.",
                "explain_en": "Success/failure cases for the IDS/CTI product.",
                "tables_vi": ["app_success", "app_failure", "query_classification"],
                "tables_en": ["app_success", "app_failure", "query_classification"],
                "role_vi": "Discussion / Limitations / Defense Q&A.",
                "role_en": "Discussion / Limitations / Defense Q&A.",
            },
            "mo_hinh_toan": {
                "lang": "vi-en",
                "role_vi": "Phân vùng Apply(q,G)∈{0,1} cho sản phẩm.",
                "role_en": "Partition Apply(q,G)∈{0,1} for the product.",
                "narrative_vi": (
                    "Apply=1 khi lợi ích EDGR vượt chi phí/rủi so với RAG trên miền IDS/CTI; "
                    "Apply=0 khi fallback hoặc abstain an toàn hơn."
                ),
                "narrative_en": (
                    "Apply=1 when EDGR’s benefit beats RAG’s cost/risk on IDS/CTI; "
                    "Apply=0 when fallback or abstain is safer."
                ),
                "formulas": [
                    {
                        "id": "apply",
                        "label_vi": "Phân vùng ứng dụng",
                        "label_en": "Application partition",
                        "latex": r"\mathrm{Apply}(q,G)\in\{0,1\}",
                        "explain_vi": "1 = ứng dụng được; 0 = thất / fallback.",
                        "explain_en": "1 = applicable; 0 = fail / fallback.",
                        "variables": [],
                    }
                ],
            },
            "mo_hinh_thuat_toan": {
                "name_vi": "Checklist chọn chế độ triển khai",
                "name_en": "Deployment-mode checklist",
                "math_ids": ["apply"],
                "pseudocode": [
                    "Nhận q + trạng thái G",
                    "OOD / seed rỗng → abstain",
                    "Lexical single-hop → cân nhắc RAG",
                    "Quan hệ CTI / đa tuổi / cần gate → EDGR (Apply=1)",
                    "Ghi case S/F",
                ],
                "complexity": r"O(1)\ \mathrm{rules}",
                "narrative_vi": "Không thay EDGR — chỉ quyết định có nên gọi đầy đủ pipeline.",
                "narrative_en": "Does not replace EDGR — only whether to invoke the full pipeline.",
                "pros_vi": ["Thành thật với hội đồng"],
                "pros_en": ["Honest for committees"],
                "cons_vi": ["Heuristic demo, chưa học từ log SOC"],
                "cons_en": ["Demo heuristic, not learned from SOC logs"],
                "improve_algo_vi": [],
                "improve_algo_en": [],
                "improve_math_vi": [],
                "improve_math_en": [],
            },
            "mo_hinh_hoat_dong": {
                **doc,
                "kind": "practical_applications",
                "flow": [
                    "Đọc lead",
                    "Duyệt case trong tab",
                    "Chạy với query (gợi ý S/F)",
                    "Đưa vào Discussion",
                ],
                "explain_vi": doc["how_to_use_vi"],
                "explain_en": doc["how_to_use_en"],
                "io": {"in": "query + KG assumptions", "out": "S/F frames"},
            },
            "minh_chung": {
                "claim_vi": doc["lead_vi"],
                "claim_en": doc["lead_en"],
                "explain_vi": "Thiết kế = bảng case; runtime = query_classification.",
                "explain_en": "Design = case tables; runtime = query_classification.",
            },
            "nhan_dinh_danh_gia": {
                "strength": "Gắn trực tiếp sản phẩm IDS/CTI với case được/thất",
                "strength_en": "Ties the IDS/CTI product directly to success/failure cases",
                "limitation": "Chưa phải field trial production",
                "limitation_en": "Not a production field trial",
                "verdict": "Đủ cho biên triển khai của Bước 16",
                "verdict_en": "Enough for Step-16 deployment bounds",
                "score_0_1": 0.85,
            },
        }
    )
