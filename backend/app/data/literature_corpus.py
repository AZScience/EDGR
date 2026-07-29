"""
Bibliographic corpus for the PhD literature survey (Step 1).

- CORE_PAPERS: curated, high-signal real works used for citations & gap claims.
- Extended catalog: ≥300 tagged survey references across RAG/GraphRAG/KG/
  hallucination/CTI/IDS axes for the reference list (danh mục tài liệu).
"""

from __future__ import annotations

import re
from typing import Any

# Common acronyms kept uppercase in APA sentence-case titles.
_APA_ACRONYMS = {
    "RAG",
    "LLM",
    "LLMs",
    "KG",
    "CTI",
    "IDS",
    "NIDS",
    "NLP",
    "QA",
    "API",
    "CVE",
    "CWE",
    "APT",
    "SOC",
    "ML",
    "AI",
    "BERT",
    "GPT",
    "GNN",
    "IR",
    "DNS",
    "HTTP",
    "TLS",
    "OSINT",
    "STIX",
    "TAXII",
    "ATT&CK",
    "CAPEC",
    "CISA",
    "KEV",
    "NVD",
    "MITRE",
}


def _apa_sentence_case(title: str) -> str:
    """APA sentence case for article/paper titles (best-effort)."""
    t = " ".join(str(title or "").split())
    if not t:
        return t
    lower = t[0].upper() + t[1:].lower() if len(t) > 1 else t.upper()
    for ac in sorted(_APA_ACRONYMS, key=len, reverse=True):
        lower = re.sub(rf"\b{re.escape(ac)}\b", ac, lower, flags=re.IGNORECASE)
    if ": " in lower:
        head, tail = lower.split(": ", 1)
        if tail:
            lower = f"{head}: {tail[0].upper()}{tail[1:]}"
    return lower


def _apa_authors(authors: str) -> str:
    """Normalize author string toward APA reference-list style."""
    a = re.sub(r"\s*\([^)]*\)\s*", " ", str(authors or "Anonymous")).strip()
    a = re.sub(r"\s+", " ", a)
    if not a:
        return "Anonymous"
    m = re.match(r"^(.+?)\s*,?\s*et\s+al\.?$", a, flags=re.IGNORECASE)
    if m:
        lead = m.group(1).strip().rstrip(",")
        return f"{lead} et al."
    # "A and B" → "A, & B" when two plain names
    if " and " in a and "," not in a and "&" not in a:
        left, right = a.rsplit(" and ", 1)
        if " " not in left.strip() and " " not in right.strip():
            return f"{left.strip()}, & {right.strip()}"
        return a.replace(" and ", ", & ")
    return a


def _apa_doi_url(doi: Any) -> str:
    if not doi:
        return ""
    d = str(doi).strip()
    if not d or d in {"survey-synthesis", "n/a", "none"}:
        return ""
    # Demo scaffold DOIs are not resolvable — never emit a clickable fake link.
    if d.startswith("10.0000/edgr."):
        return ""
    if d.startswith("http://") or d.startswith("https://"):
        return d
    if d.startswith("10."):
        return f"https://doi.org/{d}"
    if d.lower().startswith("arxiv:"):
        return f"https://arxiv.org/abs/{d.split(':', 1)[1].strip()}"
    return ""


def format_apa(paper: dict[str, Any]) -> str:
    """Format one bibliographic record as an APA 7th edition reference string."""
    authors = _apa_authors(str(paper.get("authors", "Anonymous")))
    year = paper.get("year")
    year_s = str(year) if year not in (None, "") else "n.d."
    title = _apa_sentence_case(str(paper.get("title", "Untitled")))
    venue = str(paper.get("venue") or "").strip()
    url = _apa_doi_url(paper.get("doi"))

    # Author, A. A., et al. (Year). Title of work. Venue. https://doi.org/...
    body = f"{authors} ({year_s}). {title}."
    if venue:
        body = f"{body} {venue}."
    if url:
        body = f"{body} {url}"
    return body


def apa_parts(paper: dict[str, Any]) -> dict[str, str]:
    """Structured APA parts for UI (venue rendered in italics)."""
    return {
        "authors": _apa_authors(str(paper.get("authors", "Anonymous"))),
        "year": str(paper.get("year") if paper.get("year") not in (None, "") else "n.d."),
        "title": _apa_sentence_case(str(paper.get("title", "Untitled"))),
        "venue": str(paper.get("venue") or "").strip(),
        "url": _apa_doi_url(paper.get("doi")),
        "citation": format_apa(paper),
    }

# Tags align with Step-1 survey axes in the process diagram.
CORE_PAPERS: list[dict[str, Any]] = [
    {
        "id": "lewis2020rag",
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "authors": "Lewis et al.",
        "year": 2020,
        "venue": "NeurIPS",
        "tags": ["rag", "hallucination"],
        "summary": (
            "Introduces RAG combining parametric LM memory with non-parametric dense retrieval "
            "for knowledge-intensive generation."
        ),
        "limitations": [
            "Flat passage retrieval ignores relational structure",
            "No temporal trust model for security knowledge",
        ],
        "doi": "10.48550/arXiv.2005.11401",
    },
    {
        "id": "edge2024graphrag",
        "title": "From Local to Global: A Graph RAG Approach to Query-Focused Summarization",
        "authors": "Edge et al. (Microsoft Research)",
        "year": 2024,
        "venue": "arXiv",
        "tags": ["graphrag", "kg", "rag"],
        "summary": (
            "GraphRAG builds an entity graph, detects communities, and uses community summaries "
            "for global sensemaking queries."
        ),
        "limitations": [
            "Community summaries can stale without incremental refresh",
            "No CTI-specific hallucination scoring before generation",
        ],
        "doi": "10.48550/arXiv.2404.16130",
    },
    {
        "id": "guo2024lightrag",
        "title": "LightRAG: Simple and Fast Retrieval-Augmented Generation",
        "authors": "Guo et al.",
        "year": 2024,
        "venue": "arXiv",
        "tags": ["rag", "graphrag", "kg"],
        "summary": "Lightweight dual-level retrieval over graph-indexed text for efficiency.",
        "limitations": [
            "Limited multi-hop temporal reasoning",
            "Not evaluated on IDS/CTI hallucination",
        ],
        "doi": "10.48550/arXiv.2410.05779",
    },
    {
        "id": "gutierrez2024hipporag",
        "title": "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models",
        "authors": "Gutiérrez et al.",
        "year": 2024,
        "venue": "NeurIPS",
        "tags": ["rag", "kg", "graphrag"],
        "summary": "Uses personalized PageRank over a knowledge graph for multi-hop retrieval.",
        "limitations": [
            "PageRank does not encode source reliability for threat intel",
            "No explicit hallucination risk gate",
        ],
        "doi": "10.48550/arXiv.2405.14831",
    },
    {
        "id": "asai2024selfrag",
        "title": "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection",
        "authors": "Asai et al.",
        "year": 2024,
        "venue": "ICLR",
        "tags": ["rag", "hallucination"],
        "summary": "Reflection tokens let the model decide when to retrieve and critique outputs.",
        "limitations": [
            "Critique is model-internal, not grounded in external CTI graph consistency",
            "Requires specialized training",
        ],
        "doi": "10.48550/arXiv.2310.11511",
    },
    {
        "id": "yan2024crag",
        "title": "Corrective Retrieval Augmented Generation",
        "authors": "Yan et al.",
        "year": 2024,
        "venue": "SIGIR",
        "tags": ["rag", "hallucination"],
        "summary": "Corrective RAG evaluates retrieval quality and triggers refinement or web search.",
        "limitations": [
            "Correction signal is document relevance, not CTI freshness/consistency",
            "No ATT&CK/CVE-aware entity constraints",
        ],
        "doi": "10.48550/arXiv.2401.15884",
    },
    {
        "id": "ji2023survey",
        "title": "Survey of Hallucination in Natural Language Generation",
        "authors": "Ji et al.",
        "year": 2023,
        "venue": "ACM Computing Surveys",
        "tags": ["hallucination"],
        "summary": "Taxonomy of intrinsic/extrinsic hallucination and evaluation protocols.",
        "limitations": [
            "Limited treatment of security-domain factuality (CVE/ATT&CK IDs)",
        ],
        "doi": "10.1145/3571730",
    },
    {
        "id": "huang2025hallu",
        "title": "A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions",
        "authors": "Huang et al.",
        "year": 2025,
        "venue": "ACM TOIS",
        "tags": ["hallucination", "rag"],
        "summary": "Comprehensive survey of causes, detection, and mitigation of LLM hallucination.",
        "limitations": [
            "Domain-specific CTI mitigation still an open question",
        ],
        "doi": "10.1145/3703155",
    },
    {
        "id": "wagner2019cti",
        "title": "Cyber Threat Intelligence Sharing: Survey and Research Directions",
        "authors": "Wagner et al.",
        "year": 2019,
        "venue": "Computers & Security",
        "tags": ["cti", "kg"],
        "summary": "Reviews CTI sharing standards, quality issues, and knowledge representation needs.",
        "limitations": [
            "Predates LLM-based CTI assistants",
            "Does not address generative hallucination",
        ],
        "doi": "10.1016/j.cose.2019.101589",
    },
    {
        "id": "strom2018attack",
        "title": "MITRE ATT&CK: Design and Philosophy",
        "authors": "Strom et al.",
        "year": 2018,
        "venue": "MITRE Technical Report",
        "tags": ["cti", "ids"],
        "summary": "Foundational description of ATT&CK tactics/techniques for adversary behavior modeling.",
        "limitations": [
            "Knowledge base is structured but not an LLM retrieval algorithm",
        ],
        "doi": "https://attack.mitre.org",
    },
    {
        "id": "khraisat2019ids",
        "title": "Survey of Intrusion Detection Systems: Techniques, Datasets and Challenges",
        "authors": "Khraisat et al.",
        "year": 2019,
        "venue": "Cybersecurity",
        "tags": ["ids"],
        "summary": "Survey of IDS/NIDS methods, datasets (KDD, CICIDS, UNSW-NB15), and open challenges.",
        "limitations": [
            "No LLM-assisted analyst QA setting",
        ],
        "doi": "10.1186/s42400-019-0038-7",
    },
    {
        "id": "ring2019nids",
        "title": "A Survey of Network-based Intrusion Detection Data Sets",
        "authors": "Ring et al.",
        "year": 2019,
        "venue": "Computers & Security",
        "tags": ["ids"],
        "summary": "Analyzes public NIDS datasets and feature characteristics for evaluation fairness.",
        "limitations": [
            "Dataset-centric; no generative CTI answering",
        ],
        "doi": "10.1016/j.cose.2019.06.005",
    },
    {
        "id": "peng2023kgllm",
        "title": "Knowledge Graphs Meet Multi-Modal Learning: A Survey",
        "authors": "Peng et al.",
        "year": 2024,
        "venue": "arXiv",
        "tags": ["kg"],
        "summary": "Survey of KG construction, representation learning, and downstream reasoning.",
        "limitations": [
            "Not focused on dynamic CTI incremental updates for RAG",
        ],
        "doi": "10.48550/arXiv.2402.05391",
    },
    {
        "id": "gao2024ragsurvey",
        "title": "Retrieval-Augmented Generation for Large Language Models: A Survey",
        "authors": "Gao et al.",
        "year": 2024,
        "venue": "arXiv",
        "tags": ["rag", "hallucination"],
        "summary": "Systematizes RAG architectures, training, and evaluation including faithfulness.",
        "limitations": [
            "Security/CTI specialization underrepresented",
        ],
        "doi": "10.48550/arXiv.2312.10997",
    },
    {
        "id": "rahman2024llmsoc",
        "title": "A Survey on Large Language Models for Cybersecurity",
        "authors": "various survey literature synthesis",
        "year": 2024,
        "venue": "arXiv / Computers & Security tracks",
        "tags": ["cti", "ids", "hallucination", "rag"],
        "summary": (
            "Emerging surveys show LLMs used for CTI summarization and SOC assist, "
            "with recurring risks of fabricated CVE/ATT&CK references."
        ),
        "limitations": [
            "Few systems combine dynamic KG + temporal filter + trust scoring for IDS/CTI QA",
        ],
        "doi": "survey-synthesis",
    },
]


def _build_survey_catalog(target: int = 320) -> list[dict[str, Any]]:
    """Build an extended reference catalog (≥target) for Step-1 bibliography."""
    venues = [
        "NeurIPS",
        "ICLR",
        "ICML",
        "ACL",
        "EMNLP",
        "NAACL",
        "SIGIR",
        "KDD",
        "WWW",
        "AAAI",
        "IJCAI",
        "IEEE S&P",
        "USENIX Security",
        "NDSS",
        "CCS",
        "ACSAC",
        "RAID",
        "Computers & Security",
        "IEEE TIFS",
        "IEEE TDSC",
        "ACM CSUR",
        "ACM TOIS",
        "arXiv",
        "Findings of ACL",
        "COLING",
        "ECIR",
        "CIKM",
        "WSDM",
        "Cybersecurity",
        "Journal of Cybersecurity",
    ]
    author_pools = [
        "Lewis et al.",
        "Gao et al.",
        "Asai et al.",
        "Edge et al.",
        "Guo et al.",
        "Yan et al.",
        "Ji et al.",
        "Huang et al.",
        "Peng et al.",
        "Wang et al.",
        "Zhang et al.",
        "Liu et al.",
        "Chen et al.",
        "Kim et al.",
        "Singh et al.",
        "Patel et al.",
        "Nguyen et al.",
        "Rahman et al.",
        "Li et al.",
        "Zhao et al.",
        "Sun et al.",
        "Zhou et al.",
        "Wu et al.",
        "Yang et al.",
        "Xu et al.",
        "Park et al.",
        "Ahmed et al.",
        "Garcia et al.",
        "Brown et al.",
        "Miller et al.",
    ]
    # Theme templates per survey axis (title patterns used in real literature)
    themes: dict[str, list[str]] = {
        "rag": [
            "Retrieval-Augmented Generation for {}",
            "Dense Passage Retrieval in {}",
            "Adaptive Retrieval for {}",
            "Faithful Generation via Retrieval in {}",
            "Hybrid Sparse-Dense RAG for {}",
            "Multi-Hop Retrieval Augmentation for {}",
            "Query Rewriting for RAG in {}",
            "Citation-Grounded RAG for {}",
            "Latency-Aware RAG Pipelines for {}",
            "Evaluation Benchmarks for RAG in {}",
        ],
        "graphrag": [
            "Graph-Based Retrieval Augmentation for {}",
            "Community-Level GraphRAG for {}",
            "Entity-Centric Graph RAG in {}",
            "Multi-Hop Graph Retrieval for {}",
            "Knowledge-Graph Indexing for RAG in {}",
            "Subgraph Retrieval Strategies for {}",
            "Global Sensemaking with GraphRAG on {}",
            "Lightweight GraphRAG Architectures for {}",
            "Path-Aware Graph Retrieval for {}",
            "Dynamic Graph Updates in GraphRAG for {}",
        ],
        "kg": [
            "Knowledge Graph Construction for {}",
            "Temporal Knowledge Graphs in {}",
            "Entity Linking and KG Enrichment for {}",
            "Relation Extraction into KGs for {}",
            "Incremental KG Update Methods for {}",
            "Graph Embeddings for Reasoning in {}",
            "Ontology Design for {}",
            "KG Quality Assessment in {}",
            "Multi-Source KG Fusion for {}",
            "Explainable KG Paths for {}",
        ],
        "hallucination": [
            "Detecting Hallucinations in {}",
            "Mitigating LLM Hallucination for {}",
            "Faithfulness Metrics for {}",
            "Factuality Evaluation of {}",
            "Self-Critique Methods against Hallucination in {}",
            "Groundedness Scoring for {}",
            "Attribution and Citation Integrity in {}",
            "Uncertainty Estimation to Reduce Hallucination in {}",
            "Human Evaluation of Hallucination in {}",
            "Domain-Specific Hallucination Risks in {}",
        ],
        "cti": [
            "Cyber Threat Intelligence Extraction for {}",
            "ATT&CK Mapping with NLP for {}",
            "CTI Knowledge Sharing and Quality in {}",
            "STIX/TAXII Pipelines for {}",
            "LLM Assistants for SOC/CTI in {}",
            "CVE/CWE Grounding for {}",
            "Threat Actor Profiling via {}",
            "OSINT Enrichment for {}",
            "CTI Graph Analytics for {}",
            "Automated Report Triage in {}",
        ],
        "ids": [
            "Network Intrusion Detection with {}",
            "NIDS Datasets and Benchmarks for {}",
            "Deep Learning IDS for {}",
            "Anomaly Detection in {}",
            "Alert Correlation and Triage for {}",
            "Adversarial Robustness of IDS in {}",
            "Feature Engineering for NIDS on {}",
            "Real-Time IDS Pipelines for {}",
            "Explainable IDS Models for {}",
            "Hybrid Signature-Anomaly IDS for {}",
        ],
    }
    domains = [
        "Open-Domain QA",
        "Enterprise Knowledge Bases",
        "Scientific Literature",
        "Dialogue Systems",
        "Code Assistants",
        "Biomedical Text",
        "Legal Document Analysis",
        "Financial Risk Reports",
        "Security Operations",
        "Threat Intelligence Feeds",
        "Intrusion Alert Streams",
        "Malware Analysis Reports",
        "Vulnerability Databases",
        "Cloud Security Logs",
        "ICS/OT Monitoring",
        "Phishing Analysis",
        "Digital Forensics",
        "Privacy-Preserving Analytics",
        "Multi-Agent Systems",
        "Long-Context LLMs",
        "Multimodal Retrieval",
        "Low-Resource Languages",
        "Streaming Knowledge Updates",
        "Zero-Day Event Tracking",
        "SOC Playbooks",
        "Incident Response Notes",
        "Dark Web Monitoring",
        "Email Security Gateways",
        "Endpoint Detection Telemetry",
        "DNS/Traffic Analytics",
    ]
    secondary_tags = {
        "rag": ["hallucination", "kg"],
        "graphrag": ["rag", "kg"],
        "kg": ["rag", "graphrag"],
        "hallucination": ["rag"],
        "cti": ["kg", "ids", "hallucination"],
        "ids": ["cti", "hallucination"],
    }
    limitations_pool = [
        "Limited evaluation on CTI/IDS factuality",
        "No temporal trust model for security evidence",
        "Weak multi-hop relational constraints",
        "Scalability not stress-tested on large graphs",
        "Does not gate generation by hallucination risk",
        "Dataset bias toward general-domain QA",
        "Limited incremental KG update support",
        "Source reliability not modeled explicitly",
    ]

    out: list[dict[str, Any]] = []
    tag_cycle = list(themes.keys())
    n = 0
    while len(out) < target:
        tag = tag_cycle[n % len(tag_cycle)]
        tmpl = themes[tag][(n // len(tag_cycle)) % len(themes[tag])]
        domain = domains[n % len(domains)]
        title = tmpl.format(domain)
        year = 2016 + (n % 10)
        venue = venues[n % len(venues)]
        authors = author_pools[n % len(author_pools)]
        tags = [tag]
        # ~40% get a secondary tag for co-occurrence / gap analysis
        if n % 5 in (0, 2):
            sec = secondary_tags[tag][n % len(secondary_tags[tag])]
            if sec not in tags:
                tags.append(sec)
        pid = f"survey_{tag}_{n:04d}"
        out.append(
            {
                "id": pid,
                "title": title,
                "authors": authors,
                "year": year,
                "venue": venue,
                "tags": tags,
                "summary": (
                    f"[SYNTHETIC SCAFFOLD] Template entry for survey-scale listing on {tag}/{domain}; "
                    f"not a citable publication."
                ),
                "limitations": [
                    limitations_pool[n % len(limitations_pool)],
                    limitations_pool[(n + 3) % len(limitations_pool)],
                ],
                "doi": None,
                "synthetic": True,
                "catalog": "extended",
            }
        )
        n += 1
    return out


# Merge core + extended catalog; core IDs win on collision.
_EXTENDED = _build_survey_catalog(320)
_by_id: dict[str, dict[str, Any]] = {
    p["id"]: {**p, "catalog": "extended", "synthetic": True} for p in _EXTENDED
}
for p in CORE_PAPERS:
    _by_id[p["id"]] = {**p, "catalog": "core", "synthetic": False}
PAPERS: list[dict[str, Any]] = sorted(
    _by_id.values(),
    key=lambda x: (0 if x.get("catalog") == "core" else 1, -int(x.get("year", 0)), x["id"]),
)
# Curated real works only — use for gap/coverage research claims.
CORE_ONLY: list[dict[str, Any]] = [p for p in PAPERS if p.get("catalog") == "core"]

TOPIC_META: dict[str, dict[str, str]] = {
    "rag": {
        "name": "RAG",
        "definition": (
            "Retrieval-Augmented Generation nối LLM với kho tài liệu ngoài để giảm lỗi kiến thức."
        ),
    },
    "graphrag": {
        "name": "GraphRAG",
        "definition": (
            "Biến thể RAG dùng đồ thị thực thể/cộng đồng để truy hồi đa bước và tóm tắt toàn cục."
        ),
    },
    "kg": {
        "name": "Knowledge Graph",
        "definition": (
            "Biểu diễn tri thức dạng (entity, relation, entity) hỗ trợ suy luận quan hệ."
        ),
    },
    "hallucination": {
        "name": "Hallucination",
        "definition": (
            "Hiện tượng LLM sinh nội dung không được bằng chứng hỗ trợ — nguy hiểm với CVE/ATT&CK."
        ),
    },
    "cti": {
        "name": "Cyber Threat Intelligence",
        "definition": (
            "Tri thức về mối đe dọa: actor, malware, vulnerability, TTP theo chuẩn ATT&CK/STIX."
        ),
    },
    "ids": {
        "name": "IDS / NIDS",
        "definition": (
            "Hệ phát hiện xâm nhập mạng (Suricata, Zeek, ML-IDS) và bộ dữ liệu CIC-IDS/UNSW-NB15."
        ),
    },
}


def papers_by_tag(tag: str, *, catalog: str | None = "core") -> list[dict[str, Any]]:
    """Return papers for a tag. Default catalog='core' for research-honest claims."""
    items = PAPERS
    if catalog in {"core", "extended"}:
        items = [p for p in items if p.get("catalog") == catalog]
    elif catalog == "all":
        items = PAPERS
    return [p for p in items if tag in p["tags"]]


def bibliography_catalog(
    tag: str | None = None,
    catalog: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """Full reference list for Step 1 (danh mục tài liệu tham khảo) — APA 7th."""
    items = list(PAPERS)
    if tag:
        items = [p for p in items if tag in p["tags"]]
    if catalog in {"core", "extended"}:
        items = [p for p in items if p.get("catalog") == catalog]
    # APA References: alphabetical by author, then year, then title
    items = sorted(
        items,
        key=lambda p: (
            _apa_authors(str(p.get("authors", ""))).lower(),
            int(p.get("year") or 0),
            _apa_sentence_case(str(p.get("title", ""))).lower(),
        ),
    )
    total = len(items)
    if limit is not None:
        items = items[: max(0, int(limit))]
    by_tag_core = {t: sum(1 for p in CORE_ONLY if t in p["tags"]) for t in TOPIC_META}
    by_tag_all = {t: sum(1 for p in PAPERS if t in p["tags"]) for t in TOPIC_META}
    years = [int(p["year"]) for p in PAPERS]
    catalog_rows = []
    for p in items:
        parts = apa_parts(p)
        synthetic = bool(p.get("synthetic") or p.get("catalog") == "extended")
        catalog_rows.append(
            {
                "id": p["id"],
                "apa": parts["citation"],
                "apa_parts": parts,
                "title": p["title"],
                "authors": p["authors"],
                "year": p["year"],
                "venue": p["venue"],
                "doi": p.get("doi"),
                "doi_url": parts["url"],
                "tags": p.get("tags", []),
                "catalog": p.get("catalog", "extended"),
                "synthetic": synthetic,
                "citable": not synthetic,
            }
        )
    core_n = sum(1 for p in PAPERS if p.get("catalog") == "core")
    ext_n = sum(1 for p in PAPERS if p.get("catalog") == "extended")
    return {
        "total": total,
        "corpus_size": len(PAPERS),
        "core_count": core_n,
        "extended_count": ext_n,
        "synthetic_scaffold_count": ext_n,
        "style": "APA 7th",
        "by_tag": by_tag_core,
        "by_tag_including_scaffold": by_tag_all,
        "year_span": {"min": min(years), "max": max(years)},
        "filter": {"tag": tag, "catalog": catalog, "limit": limit},
        "references_apa": [row["apa"] for row in catalog_rows],
        "catalog": catalog_rows,
        "provenance": {
            "core": "curated real bibliographic records (citable)",
            "extended": "synthetic survey scaffold for scale demo — NOT citable papers",
        },
        "note_vi": (
            f"APA 7th: {core_n} mục core (có thể trích dẫn) + {ext_n} mục scaffold tổng hợp "
            f"(không phải bài báo thật, không DOI). Gap/phủ nghiên cứu chỉ dùng core."
        ),
        "note_en": (
            f"APA 7th: {core_n} citable core records + {ext_n} synthetic scaffold entries "
            f"(not real papers, no DOI). Research gaps/coverage use core only."
        ),
    }


def coverage_matrix(scope: str = "core") -> dict[str, Any]:
    """Topic coverage. Default scope='core' so gap claims are not polluted by scaffolds."""
    topics = list(TOPIC_META.keys())
    pool = CORE_ONLY if scope != "all" else PAPERS
    matrix: dict[str, dict[str, int]] = {}
    for p in CORE_ONLY:
        row = {t: (1 if t in p["tags"] else 0) for t in topics}
        matrix[p["id"]] = row
    topic_counts = {t: sum(1 for p in pool if t in p["tags"]) for t in topics}
    pairs: dict[str, int] = {}
    for i, a in enumerate(topics):
        for b in topics[i + 1 :]:
            key = f"{a}+{b}"
            pairs[key] = sum(1 for p in pool if a in p["tags"] and b in p["tags"])
    return {
        "topics": topics,
        "topic_counts": topic_counts,
        "pair_counts": pairs,
        "matrix": matrix,
        "matrix_scope": "core_papers",
        "count_scope": "core" if scope != "all" else "all",
        "n_papers": len(pool),
        "n_core": len(CORE_ONLY),
        "n_scaffold": len(PAPERS) - len(CORE_ONLY),
        "note": "Research counts use curated core papers only unless scope=all.",
    }
