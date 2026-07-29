"""Step 13 — complete scientific paper (EDGR + DKG + scoring + evaluation).

Loads the full manuscripts from docs/papers/ (not process outlines).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PAPER_EN = _REPO_ROOT / "docs" / "papers" / "EDGR_scientific_paper.md"
_PAPER_VI = _REPO_ROOT / "docs" / "papers" / "EDGR_scientific_paper_vi.md"


def _integrity() -> dict[str, Any]:
    return {
        "title_vi": "Kỷ luật học thuật (khi chỉnh sửa bản thảo)",
        "title_en": "Academic integrity (when editing the draft)",
        "rules_vi": [
            "Bản dưới đây đã là bài báo hoàn chỉnh trên số liệu demo tái lập được; khi sửa, mọi claim số phải khớp pipeline Steps 9–11.",
            "Không dán đoạn văn từ bài khác; paraphrase sau khi đọc và gắn citation.",
            "Baseline là stub nghiên cứu trên cùng store — nêu rõ khi nộp venue.",
        ],
        "rules_en": [
            "The text below is a complete paper on reproducible demo metrics; when editing, keep numeric claims aligned with Steps 9–11.",
            "Do not paste prose from other papers; paraphrase after reading and cite.",
            "Baselines are research stubs on the same store — state this when submitting.",
        ],
        "self_check_vi": [
            "Abstract khớp bảng kết quả §8?",
            "Limitations đã nêu quy mô demo và stub baseline?",
            "Đã chạy lại evaluate_dataset trước khi đổi số?",
        ],
        "self_check_en": [
            "Abstract matches §8 tables?",
            "Limitations mention demo scale and stub baselines?",
            "Re-ran evaluate_dataset before changing numbers?",
        ],
    }


def _read_paper(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _strip_title_block(md: str) -> tuple[str, str]:
    """Return (title, body_without_leading_h1)."""
    lines = md.strip().splitlines()
    title = ""
    rest: list[str] = []
    for i, line in enumerate(lines):
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            rest = lines[i + 1 :]
            break
    else:
        rest = lines
    return title, "\n".join(rest).strip()


def _extract_abstract(md: str) -> str:
    m = re.search(
        r"## (?:Abstract|Tóm tắt)\s*\n+(.*?)(?=\n## |\n\*\*Keywords|\n\*\*Từ khóa|\Z)",
        md,
        flags=re.S | re.I,
    )
    if not m:
        return ""
    text = m.group(1).strip()
    # Drop trailing Keywords block if captured
    text = re.split(r"\n\*\*(?:Keywords|Từ khóa)", text, maxsplit=1)[0].strip()
    return text


def _extract_keywords(md: str) -> list[str]:
    m = re.search(
        r"\*\*(?:Keywords|Từ khóa):\*\*\s*(.+)",
        md,
        flags=re.I,
    )
    if not m:
        return []
    raw = m.group(1).strip()
    return [x.strip() for x in re.split(r"[;]", raw) if x.strip()]


def _parse_sections(md: str) -> list[dict[str, str]]:
    """Split markdown into ## sections (skip Abstract/Tóm tắt — shown separately)."""
    body = md
    # Normalize
    parts = re.split(r"\n(?=## )", body)
    sections: list[dict[str, str]] = []
    for part in parts:
        part = part.strip()
        if not part.startswith("## "):
            continue
        lines = part.splitlines()
        name = lines[0][3:].strip()
        content = "\n".join(lines[1:]).strip()
        low = name.lower()
        if low in {"abstract", "tóm tắt"}:
            continue
        if low.startswith("references") or low.startswith("tài liệu"):
            sections.append({"name": name, "body": content})
            continue
        if low.startswith("appendix") or low.startswith("phụ lục"):
            sections.append({"name": name, "body": content})
            continue
        sections.append({"name": name, "body": content})
    return sections


def _sec(
    name_vi: str,
    name_en: str,
    *,
    draft_vi: str,
    draft_en: str,
    goal_vi: str = "",
    goal_en: str = "",
    must_cite: list[str] | None = None,
    artifacts: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "name_vi": name_vi,
        "name_en": name_en,
        "goal_vi": goal_vi,
        "goal_en": goal_en,
        "draft_vi": draft_vi,
        "draft_en": draft_en,
        "must_cite": must_cite or [],
        "pipeline_artifacts": artifacts or [],
        "pitfalls_vi": "",
        "pitfalls_en": "",
    }


def _align_sections(secs_vi: list[dict[str, str]], secs_en: list[dict[str, str]]) -> list[dict[str, Any]]:
    n = max(len(secs_vi), len(secs_en))
    out: list[dict[str, Any]] = []
    for i in range(n):
        vi = secs_vi[i] if i < len(secs_vi) else {"name": f"§{i+1}", "body": ""}
        en = secs_en[i] if i < len(secs_en) else {"name": f"§{i+1}", "body": ""}
        out.append(
            _sec(
                vi["name"],
                en["name"],
                draft_vi=vi["body"],
                draft_en=en["body"],
                goal_vi="Nội dung bài báo (bản hoàn chỉnh).",
                goal_en="Full paper body (complete manuscript).",
            )
        )
    return out


def full_scientific_paper() -> dict[str, Any]:
    """Complete manuscript consolidating EDGR + DKG + scoring + evaluation."""
    md_en = _read_paper(_PAPER_EN)
    md_vi = _read_paper(_PAPER_VI)
    title_en, _ = _strip_title_block(md_en) if md_en else ("", "")
    title_vi, _ = _strip_title_block(md_vi) if md_vi else ("", "")
    abstract_en = _extract_abstract(md_en)
    abstract_vi = _extract_abstract(md_vi)
    keywords = _extract_keywords(md_en) or _extract_keywords(md_vi)
    sections = _align_sections(_parse_sections(md_vi), _parse_sections(md_en))

    if not sections and md_en:
        # Fallback: single body section
        sections = [
            _sec(
                "Bài báo đầy đủ",
                "Full manuscript",
                draft_vi=md_vi or md_en,
                draft_en=md_en,
            )
        ]

    return {
        "id": 1,
        "task_id": "full",
        "status": "manuscript_complete",
        "kind": "publication_manuscript",
        "working_title": title_en
        or (
            "EDGR: Evidence-Driven Dynamic Graph Retrieval with Hallucination Risk Gating "
            "for Intrusion Detection and Cyber Threat Intelligence"
        ),
        "working_title_vi": title_vi
        or (
            "EDGR: Truy hồi đồ thị động dựa trên bằng chứng và cổng rủi ro ảo giác "
            "cho phát hiện xâm nhập và tình báo mối đe dọa mạng"
        ),
        "focus_vi": (
            "Bài báo khoa học hoàn chỉnh (không phải outline quy trình): "
            "Dynamic KG + EDGR 6 giai + Hallucination Scoring/ρ-gate + đánh giá toàn diện."
        ),
        "focus_en": (
            "Complete scientific paper (not a process outline): "
            "Dynamic KG + six-stage EDGR + hallucination scoring/ρ-gate + full evaluation."
        ),
        "contribution_claim_vi": (
            "Chúng tôi đề xuất EDGR — pipeline truy hồi trên đồ thị CTI động, kết thúc bằng cổng rủi ro ảo giác "
            "và toán tử abstain — cùng lớp Dynamic Knowledge Graph và mô hình chấm điểm bốn yếu tố; "
            "trên bộ QA IDS/CTI seed, EDGR giảm hallucination rate so với RAG phẳng "
            "(0,253 vs 0,427) và từ chối khi CVE ngoài phân bố không có bằng chứng."
        ),
        "contribution_claim_en": (
            "We propose EDGR — a retrieval pipeline over a dynamic CTI graph ending in a hallucination-risk "
            "gate and abstain operator — with a Dynamic Knowledge Graph layer and four-factor scoring; "
            "on the seed IDS/CTI QA set, EDGR reduces hallucination rate versus flat RAG "
            "(0.253 vs 0.427) and refuses when out-of-distribution CVEs lack supporting evidence."
        ),
        "abstract_draft_vi": abstract_vi,
        "abstract_draft_en": abstract_en,
        "keywords": keywords
        or [
            "retrieval-augmented generation",
            "knowledge graph",
            "hallucination",
            "cyber threat intelligence",
            "intrusion detection",
            "risk gate",
            "abstain",
        ],
        "manuscript_markdown_en": md_en,
        "manuscript_markdown_vi": md_vi,
        "manuscript_path_en": str(_PAPER_EN),
        "manuscript_path_vi": str(_PAPER_VI),
        "venue_targets": [
            {
                "name": "ACSAC",
                "why_vi": "Ứng dụng bảo mật có đánh giá thực nghiệm rõ.",
                "why_en": "Security applications with clear empirical evaluation.",
            },
            {
                "name": "RAID",
                "why_vi": "Thiên về hệ thống phát hiện/phản ứng xâm nhập.",
                "why_en": "Intrusion detection / response systems focus.",
            },
            {
                "name": "IEEE TIFS",
                "why_vi": "Nếu đóng góp thuật toán + KG + đánh giá đủ dày.",
                "why_en": "If algorithm + KG + evaluation depth fits a journal article.",
            },
            {
                "name": "Computers & Security",
                "why_vi": "Hợp bài hệ thống/tri thức bảo mật gộp KG + retrieval.",
                "why_en": "Fits security systems/knowledge papers combining KG + retrieval.",
            },
            {
                "name": "arXiv cs.CR / cs.CL",
                "why_vi": "Bản thảo sớm để lấy phản hồi.",
                "why_en": "Early preprint for feedback.",
            },
        ],
        "maps_to_steps": [4, 5, 6, 7, 9, 10, 11, 12],
        "themes_vi": [
            "EDGR Algorithm",
            "Dynamic KG",
            "Hallucination Scoring",
            "Comprehensive Evaluation",
        ],
        "themes_en": [
            "EDGR Algorithm",
            "Dynamic KG",
            "Hallucination Scoring",
            "Comprehensive Evaluation",
        ],
        "sections": sections,
        "novelty_bullets_vi": [
            "Một bài hoàn chỉnh: DKG + EDGR 6 giai + ρ-gate abstain + protocol đánh giá.",
            "Cổng ρ trước emit và abstain CVE OOD — khác hệ chỉ tối ưu retrieval rồi sinh tự do.",
            "Số liệu demo tái lập: Faith(EDGR)=0,747; Hall=0,253 vs RAG Hall=0,427.",
        ],
        "novelty_bullets_en": [
            "One complete paper: DKG + six-stage EDGR + ρ-gate abstain + evaluation protocol.",
            "ρ-gate before emit and OOD CVE abstain — unlike retrieve-then-freely-generate systems.",
            "Reproducible demo numbers: Faith(EDGR)=0.747; Hall=0.253 vs RAG Hall=0.427.",
        ],
        "how_to_use_vi": (
            "Đây là bản thảo bài báo khoa học hoàn chỉnh (file Markdown trong docs/papers/). "
            "Đọc từng mục bên dưới; khi Chạy sẽ gắn thêm live_artifacts từ Steps 9–11."
        ),
        "how_to_use_en": (
            "This is a complete scientific manuscript (Markdown under docs/papers/). "
            "Read each section below; Run attaches live_artifacts from Steps 9–11."
        ),
        "integrity": _integrity(),
    }
