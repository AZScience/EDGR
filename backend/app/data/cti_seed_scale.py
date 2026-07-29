"""Second-wave scale-up: graph-derived QA + extra evidence for PhD/human-eval N≥48."""

from __future__ import annotations

from typing import Any

# Extra evidence supporting graph-derived and SOC-style questions
SCALE_EVIDENCE: list[dict[str, Any]] = [
    {
        "id": "ev_033",
        "content": (
            "Technique T1133 External Remote Services covers VPN and VDI exposure used for "
            "initial access. Combine with T1078 when credential stuffing precedes remote login."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1133", "T1078", "TA0001"],
        "timestamp": "2024-10-20",
        "reliability": 0.93,
        "type": "technique",
    },
    {
        "id": "ev_034",
        "content": (
            "CVE-2023-23397 is an Outlook elevation-of-privilege flaw abused for Net-NTLM theft. "
            "Mapped often to initial access and credential access chains in enterprise SOC playbooks."
        ),
        "source": "NVD/CVE",
        "entities": ["CVE-2023-23397", "Outlook"],
        "timestamp": "2023-03-14",
        "reliability": 0.96,
        "type": "cve",
    },
    {
        "id": "ev_035",
        "content": (
            "SOC triage note: when Suricata fires on SMB admin share access and the host has a "
            "recent phishing alert, prioritize T1021.002 under TA0008 before closing as noise."
        ),
        "source": "IDS/NIDS Guide",
        "entities": ["T1021.002", "TA0008", "Suricata", "T1566"],
        "timestamp": "2024-12-01",
        "reliability": 0.84,
        "type": "alert",
    },
    {
        "id": "ev_036",
        "content": (
            "EDGR human-eval protocol scores groundedness, unsupported identifiers, actionability, "
            "and abstain appropriateness with two independent SOC annotators and Cohen’s κ."
        ),
        "source": "Research Note",
        "entities": ["EDGR", "Hallucination"],
        "timestamp": "2025-04-01",
        "reliability": 0.88,
        "type": "concept",
    },
    {
        "id": "ev_037",
        "content": (
            "Hafnium campaigns after ProxyLogon frequently planted ASPX web shells (T1505.003) "
            "on Exchange servers; hunt IIS logs for unusual .aspx under outlook directories."
        ),
        "source": "CISA/CTI",
        "entities": ["Hafnium", "T1505.003", "CVE-2021-26855"],
        "timestamp": "2021-03-10",
        "reliability": 0.93,
        "type": "actor",
    },
    {
        "id": "ev_038",
        "content": (
            "Large-scale CTI QA should mix multi-hop actor→CVE→TTP paths, temporal freshness "
            "conflicts, IDS alert pivots, and OOD abstain cases to stress Trusted Answer contracts."
        ),
        "source": "Research Note",
        "entities": ["EDGR", "CTI", "NIDS"],
        "timestamp": "2025-04-10",
        "reliability": 0.86,
        "type": "concept",
    },
    {
        "id": "ev_039",
        "content": (
            "CVE-2022-22965 (Spring4Shell) enables RCE via data binding on JDK 9+. "
            "Public-facing Spring apps map to T1190 similarly to Log4Shell."
        ),
        "source": "NVD/CVE",
        "entities": ["CVE-2022-22965", "Spring4Shell", "T1190"],
        "timestamp": "2022-03-31",
        "reliability": 0.95,
        "type": "cve",
    },
    {
        "id": "ev_040",
        "content": (
            "Technique T1003.001 LSASS Memory is a common credential dumping path after "
            "TrickBot or Cobalt Strike staging; monitor for access to lsass.exe from non-system processes."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1003.001", "T1003", "TrickBot"],
        "timestamp": "2024-08-01",
        "reliability": 0.92,
        "type": "technique",
    },
]

SCALE_NODES: list[dict[str, Any]] = [
    {"id": "T1133", "label": "External Remote Services", "type": "technique",
     "timestamp": "2024-10-20", "reliability": 0.93, "properties": {"tactic": "TA0001"}},
    {"id": "CVE-2023-23397", "label": "Outlook NTLM leak", "type": "cve",
     "timestamp": "2023-03-14", "reliability": 0.96, "properties": {"kev": True}},
    {"id": "CVE-2022-22965", "label": "Spring4Shell", "type": "cve",
     "timestamp": "2022-03-31", "reliability": 0.95, "properties": {"kev": True}},
    {"id": "T1003.001", "label": "LSASS Memory", "type": "technique",
     "timestamp": "2024-08-01", "reliability": 0.92, "properties": {"tactic": "TA0006"}},
]

SCALE_EDGES: list[dict[str, Any]] = [
    {"source": "T1133", "target": "TA0001", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-10-20"},
    {"source": "CVE-2023-23397", "target": "T1078", "relation": "enables", "weight": 0.88, "timestamp": "2023-03-14"},
    {"source": "CVE-2022-22965", "target": "T1190", "relation": "enables", "weight": 0.92, "timestamp": "2022-03-31"},
    {"source": "T1003.001", "target": "T1003", "relation": "related_to", "weight": 0.95, "timestamp": "2024-08-01"},
    {"source": "TrickBot", "target": "T1003.001", "relation": "uses", "weight": 0.84, "timestamp": "2024-08-01"},
    {"source": "Hafnium", "target": "T1505.003", "relation": "uses", "weight": 0.9, "timestamp": "2021-03-10"},
]

# Handcrafted scale QA (beyond graph templates)
SCALE_QA_HAND: list[dict[str, Any]] = [
    {
        "id": "qa_025",
        "question": "How does T1133 relate to initial access with valid accounts?",
        "gold_answer": (
            "T1133 External Remote Services covers VPN/VDI exposure for initial access; "
            "combine with T1078 when credential stuffing precedes remote login."
        ),
        "gold_entities": ["T1133", "T1078", "TA0001"],
        "gold_evidence_ids": ["ev_033", "ev_002"],
        "category": "multi_hop",
    },
    {
        "id": "qa_026",
        "question": "What is CVE-2023-23397 and how is it abused?",
        "gold_answer": (
            "CVE-2023-23397 is an Outlook elevation-of-privilege flaw abused for Net-NTLM theft "
            "in enterprise credential-access chains."
        ),
        "gold_entities": ["CVE-2023-23397", "Outlook"],
        "gold_evidence_ids": ["ev_034"],
        "category": "kev",
    },
    {
        "id": "qa_027",
        "question": "How should SOC prioritize Suricata SMB admin-share alerts after phishing?",
        "gold_answer": (
            "When Suricata fires on SMB admin share access after phishing, prioritize T1021.002 "
            "under TA0008 before closing as noise."
        ),
        "gold_entities": ["T1021.002", "TA0008", "Suricata", "T1566"],
        "gold_evidence_ids": ["ev_035", "ev_023"],
        "category": "ids_alert",
    },
    {
        "id": "qa_028",
        "question": "What dimensions does the EDGR SOC human-eval protocol score?",
        "gold_answer": (
            "It scores groundedness, unsupported identifiers, actionability, and abstain "
            "appropriateness with two annotators and Cohen’s κ."
        ),
        "gold_entities": ["EDGR", "Hallucination"],
        "gold_evidence_ids": ["ev_036"],
        "category": "gate_theory",
    },
    {
        "id": "qa_029",
        "question": "Where should analysts hunt for Hafnium web shells after ProxyLogon?",
        "gold_answer": (
            "Hunt IIS logs for unusual ASPX under Outlook directories corresponding to T1505.003 "
            "after ProxyLogon (CVE-2021-26855)."
        ),
        "gold_entities": ["Hafnium", "T1505.003", "CVE-2021-26855"],
        "gold_evidence_ids": ["ev_037", "ev_025"],
        "category": "multi_hop",
    },
    {
        "id": "qa_030",
        "question": "Why mix OOD abstain cases into large-scale CTI QA?",
        "gold_answer": (
            "Mixing multi-hop, temporal, IDS pivots, and OOD abstain cases stresses the "
            "Trusted Answer contract beyond bag-of-passages retrieval."
        ),
        "gold_entities": ["EDGR", "CTI", "NIDS"],
        "gold_evidence_ids": ["ev_038", "ev_026"],
        "category": "gate_theory",
    },
    {
        "id": "qa_031",
        "question": "What is Spring4Shell CVE-2022-22965 mapped to in ATT&CK?",
        "gold_answer": (
            "CVE-2022-22965 (Spring4Shell) enables RCE on vulnerable Spring apps and maps to "
            "T1190 Exploit Public-Facing Application, similar to Log4Shell."
        ),
        "gold_entities": ["CVE-2022-22965", "Spring4Shell", "T1190"],
        "gold_evidence_ids": ["ev_039", "ev_011"],
        "category": "kev",
    },
    {
        "id": "qa_032",
        "question": "Which LSASS technique follows TrickBot credential staging?",
        "gold_answer": (
            "T1003.001 LSASS Memory is a common credential dumping path after TrickBot staging; "
            "monitor non-system processes accessing lsass.exe."
        ),
        "gold_entities": ["T1003.001", "T1003", "TrickBot"],
        "gold_evidence_ids": ["ev_040", "ev_021"],
        "category": "multi_hop",
    },
    {
        "id": "qa_033",
        "question": "What is the vendor advisory URL and CVSS for CVE-2099-11111?",
        "gold_answer": (
            "[ABSTAIN] CVE-2099-11111 is not in the Dynamic KG or evidence; EDGR must abstain."
        ),
        "gold_entities": ["EDGR"],
        "gold_evidence_ids": ["ev_026"],
        "category": "ood_abstain",
        "expect_abstain": True,
    },
    {
        "id": "qa_034",
        "question": "Does CISA KEV include both Log4Shell and MOVEit as priority examples?",
        "gold_answer": (
            "Yes — CISA KEV lists actively exploited vulnerabilities; Log4Shell "
            "(CVE-2021-44228) and MOVEit (CVE-2023-34362) are high-priority examples."
        ),
        "gold_entities": ["CISA KEV", "CVE-2021-44228", "CVE-2023-34362"],
        "gold_evidence_ids": ["ev_013"],
        "category": "kev",
    },
]


def build_graph_qa(
    edges: list[dict[str, Any]],
    *,
    start_index: int = 35,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Derive relation QA from KG edges (reproducible scale-up without external APIs)."""
    out: list[dict[str, Any]] = []
    templates = [
        (
            "What ATT&CK/CTI relation links {src} to {tgt}?",
            "{src} is connected to {tgt} via relation '{rel}' in the CTI knowledge graph.",
        ),
        (
            "In the threat graph, how is {src} related to {tgt}?",
            "The seeded CTI graph records {src} -[{rel}]-> {tgt}.",
        ),
    ]
    for i, e in enumerate(edges[:limit]):
        src, tgt, rel = e["source"], e["target"], e.get("relation", "related_to")
        q_t, a_t = templates[i % len(templates)]
        qid = f"qa_{start_index + i:03d}"
        out.append(
            {
                "id": qid,
                "question": q_t.format(src=src, tgt=tgt),
                "gold_answer": a_t.format(src=src, tgt=tgt, rel=rel),
                "gold_entities": [src, tgt],
                "gold_evidence_ids": [],  # filled after evidence index exists
                "category": "graph_derived",
                "expect_abstain": False,
                "graph_edge": {"source": src, "target": tgt, "relation": rel},
            }
        )
    return out


def attach_evidence_ids_for_graph_qa(
    qa_items: list[dict[str, Any]],
    chunks: list[dict[str, Any]],
) -> None:
    """Best-effort link graph QA to any chunk mentioning both endpoints."""
    for item in qa_items:
        ge = item.get("graph_edge") or {}
        src, tgt = str(ge.get("source", "")), str(ge.get("target", ""))
        if not src or not tgt:
            continue
        hits = []
        for c in chunks:
            ents = set(c.get("entities") or [])
            text = str(c.get("content") or "")
            if (src in ents or src in text) and (tgt in ents or tgt in text):
                hits.append(c["id"])
            elif src in ents or src in text or tgt in ents or tgt in text:
                hits.append(c["id"])
        item["gold_evidence_ids"] = hits[:3] or item.get("gold_evidence_ids") or []
