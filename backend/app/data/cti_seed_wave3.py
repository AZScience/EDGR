"""Wave-3 scale-up for IEEE-oriented evaluation: larger KG, evidence, and stratified QA."""

from __future__ import annotations

from typing import Any

# --- Evidence (ev_041+) ---
WAVE3_EVIDENCE: list[dict[str, Any]] = [
    {
        "id": "ev_041",
        "content": (
            "Technique T1190 Exploit Public-Facing Application covers attacks against internet-facing "
            "services. Log4Shell, ProxyLogon, and Spring4Shell campaigns commonly map to T1190 for "
            "initial access hunting."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1190", "TA0001", "CVE-2021-44228", "CVE-2021-26855", "CVE-2022-22965"],
        "timestamp": "2024-09-01",
        "reliability": 0.95,
        "type": "technique",
    },
    {
        "id": "ev_042",
        "content": (
            "Technique T1059 Command and Scripting Interpreter includes PowerShell (T1059.001) and "
            "Windows Command Shell. APT29 and many ransomware affiliates abuse living-off-the-land "
            "scripting after valid-account access."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1059", "T1059.001", "APT29", "TA0002"],
        "timestamp": "2024-11-01",
        "reliability": 0.94,
        "type": "technique",
    },
    {
        "id": "ev_043",
        "content": (
            "Technique T1021.002 SMB/Windows Admin Shares is a lateral-movement path after phishing. "
            "NIDS/Suricata rules on unexpected ADMIN$ or C$ access should escalate with T1566 context."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1021.002", "TA0008", "T1566", "Suricata"],
        "timestamp": "2024-12-01",
        "reliability": 0.93,
        "type": "technique",
    },
    {
        "id": "ev_044",
        "content": (
            "CVE-2021-26855 (ProxyLogon) is a Microsoft Exchange SSRF flaw. Hafnium operators chained "
            "it with web-shell planting (T1505.003). CISA KEV lists related Exchange CVEs as priority."
        ),
        "source": "NVD/CVE",
        "entities": ["CVE-2021-26855", "Hafnium", "T1505.003", "CISA KEV"],
        "timestamp": "2021-03-02",
        "reliability": 0.97,
        "type": "cve",
    },
    {
        "id": "ev_045",
        "content": (
            "Emotet historically delivered TrickBot or QakBot payloads via malspam. Post-compromise "
            "paths often include credential dumping (T1003) and Cobalt Strike staging."
        ),
        "source": "CISA/CTI",
        "entities": ["Emotet", "TrickBot", "QakBot", "T1003", "Cobalt Strike"],
        "timestamp": "2024-05-15",
        "reliability": 0.91,
        "type": "malware",
    },
    {
        "id": "ev_046",
        "content": (
            "Technique T1566 Phishing remains a dominant initial-access vector. Combine email "
            "gateway alerts with endpoint process trees for T1059 follow-on activity."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1566", "TA0001", "T1059"],
        "timestamp": "2024-10-01",
        "reliability": 0.94,
        "type": "technique",
    },
    {
        "id": "ev_047",
        "content": (
            "IDS alert fusion: correlate Suricata HTTP anomaly signatures with CISA KEV CVE tags "
            "before closing as false positive. Prefer abstain when CVE strings in tickets are unknown."
        ),
        "source": "IDS/NIDS Guide",
        "entities": ["Suricata", "CISA KEV", "EDGR", "NIDS"],
        "timestamp": "2025-01-20",
        "reliability": 0.86,
        "type": "alert",
    },
    {
        "id": "ev_048",
        "content": (
            "Technique T1078 Valid Accounts enables stealthy access. Monitor impossible travel, "
            "dormant account reuse, and MFA fatigue alongside T1133 remote services."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1078", "T1133", "TA0001"],
        "timestamp": "2024-10-15",
        "reliability": 0.94,
        "type": "technique",
    },
    {
        "id": "ev_049",
        "content": (
            "Cl0p ransomware affiliates exploited MOVEit CVE-2023-34362 for data theft and extortion. "
            "Hunt unusual MOVEit Transfer process trees and outbound large transfers."
        ),
        "source": "CISA/CTI",
        "entities": ["Cl0p", "CVE-2023-34362", "MOVEit"],
        "timestamp": "2023-06-15",
        "reliability": 0.95,
        "type": "actor",
    },
    {
        "id": "ev_050",
        "content": (
            "EDGR Trusted Answer contract: emit only if risk ρ ≤ θ and queried CVE identifiers appear "
            "in trusted evidence; otherwise abstain to avoid fabricated CTI dossiers."
        ),
        "source": "Research Note",
        "entities": ["EDGR", "Hallucination"],
        "timestamp": "2025-06-01",
        "reliability": 0.9,
        "type": "concept",
    },
    {
        "id": "ev_051",
        "content": (
            "Technique T1486 Data Encrypted for Impact is common in ransomware. Prioritize isolation "
            "when T1486 co-occurs with T1021 lateral movement on the same host cluster."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1486", "T1021", "TA0040"],
        "timestamp": "2024-07-01",
        "reliability": 0.92,
        "type": "technique",
    },
    {
        "id": "ev_052",
        "content": (
            "QakBot (QBot) campaigns used threaded email replies and HTML smuggling. Mapped techniques "
            "include T1566.001 and follow-on discovery before Cobalt Strike."
        ),
        "source": "CISA/CTI",
        "entities": ["QakBot", "T1566.001", "Cobalt Strike"],
        "timestamp": "2023-08-01",
        "reliability": 0.9,
        "type": "malware",
    },
    {
        "id": "ev_053",
        "content": (
            "Temporal CTI hygiene: historical CVEs such as CVE-2021-44228 remain operationally relevant; "
            "freshness should soft-weight trust rather than hard-delete seed entities."
        ),
        "source": "Research Note",
        "entities": ["CVE-2021-44228", "EDGR"],
        "timestamp": "2025-03-01",
        "reliability": 0.88,
        "type": "concept",
    },
    {
        "id": "ev_054",
        "content": (
            "Technique T1505.003 Web Shell is a persistence mechanism on compromised web servers. "
            "After Exchange ProxyLogon, hunt unusual ASPX under Outlook directories."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1505.003", "Hafnium", "CVE-2021-26855"],
        "timestamp": "2024-04-01",
        "reliability": 0.93,
        "type": "technique",
    },
    {
        "id": "ev_055",
        "content": (
            "CAPEC-66 SQL Injection relates to CWE-89. Detection looks for UNION SELECT, tautologies, "
            "and comment-terminated payloads in web logs."
        ),
        "source": "CAPEC/CWE",
        "entities": ["CAPEC-66", "CWE-89"],
        "timestamp": "2024-02-01",
        "reliability": 0.94,
        "type": "concept",
    },
    {
        "id": "ev_056",
        "content": (
            "UNSW-NB15 and CIC-IDS2017 remain standard NIDS benchmarks. Use them for detection "
            "model eval, not as substitutes for live CTI identifier grounding."
        ),
        "source": "IDS/NIDS Guide",
        "entities": ["UNSW-NB15", "CIC-IDS2017", "NIDS"],
        "timestamp": "2024-06-01",
        "reliability": 0.9,
        "type": "dataset",
    },
    {
        "id": "ev_057",
        "content": (
            "Lazarus Group targeting of crypto exchanges often combines supply-chain compromise "
            "with custom droppers. Map observed binaries to malware nodes before attribution claims."
        ),
        "source": "CISA/CTI",
        "entities": ["Lazarus", "TA0001"],
        "timestamp": "2024-09-15",
        "reliability": 0.89,
        "type": "actor",
    },
    {
        "id": "ev_058",
        "content": (
            "Technique T1003 Credential Dumping parent covers LSASS memory (T1003.001). After "
            "Emotet/TrickBot staging, monitor non-system access to lsass.exe."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1003", "T1003.001", "Emotet", "TrickBot"],
        "timestamp": "2024-08-01",
        "reliability": 0.93,
        "type": "technique",
    },
    {
        "id": "ev_059",
        "content": (
            "SOC false-positive note: unsigned PowerShell with encoded commands may be admin "
            "automation. Require T1059.001 plus suspicious parent/network before auto-blocking."
        ),
        "source": "IDS/NIDS Guide",
        "entities": ["T1059.001", "PowerShell", "Suricata"],
        "timestamp": "2025-02-10",
        "reliability": 0.84,
        "type": "alert",
    },
    {
        "id": "ev_060",
        "content": (
            "Multi-hop CTI reasoning example: APT29 → T1566 → T1078 → cloud living-off-the-land. "
            "Graph expansion should surface these edges before flat passage ranking alone."
        ),
        "source": "Research Note",
        "entities": ["APT29", "T1566", "T1078", "EDGR"],
        "timestamp": "2025-05-01",
        "reliability": 0.87,
        "type": "concept",
    },
]

WAVE3_NODES: list[dict[str, Any]] = [
    {"id": "Emotet", "label": "Emotet", "type": "malware", "timestamp": "2024-05-15", "reliability": 0.91, "properties": {}},
    {"id": "QakBot", "label": "QakBot", "type": "malware", "timestamp": "2023-08-01", "reliability": 0.9, "properties": {}},
    {"id": "Cobalt Strike", "label": "Cobalt Strike", "type": "software", "timestamp": "2024-01-01", "reliability": 0.88, "properties": {}},
    {"id": "T1486", "label": "Data Encrypted for Impact", "type": "technique", "timestamp": "2024-07-01", "reliability": 0.92, "properties": {"tactic": "TA0040"}},
    {"id": "T1566.001", "label": "Spearphishing Attachment", "type": "technique", "timestamp": "2023-08-01", "reliability": 0.93, "properties": {"tactic": "TA0001"}},
    {"id": "TA0040", "label": "Impact", "type": "tactic", "timestamp": "2024-01-01", "reliability": 0.95, "properties": {}},
    {"id": "CVE-2099-22222", "label": "Synthetic OOD CVE", "type": "concept", "timestamp": "2099-01-01", "reliability": 0.1, "properties": {"ood": True}},
]

WAVE3_EDGES: list[dict[str, Any]] = [
    {"source": "Emotet", "target": "TrickBot", "relation": "delivers_via", "weight": 0.86, "timestamp": "2024-05-15"},
    {"source": "Emotet", "target": "T1566", "relation": "uses", "weight": 0.9, "timestamp": "2024-05-15"},
    {"source": "QakBot", "target": "T1566.001", "relation": "uses", "weight": 0.88, "timestamp": "2023-08-01"},
    {"source": "QakBot", "target": "Cobalt Strike", "relation": "drops", "weight": 0.8, "timestamp": "2023-08-01"},
    {"source": "TrickBot", "target": "Cobalt Strike", "relation": "drops", "weight": 0.78, "timestamp": "2024-08-01"},
    {"source": "T1486", "target": "TA0040", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-07-01"},
    {"source": "Cl0p", "target": "T1486", "relation": "uses", "weight": 0.85, "timestamp": "2023-06-15"},
    {"source": "T1566.001", "target": "T1566", "relation": "related_to", "weight": 0.95, "timestamp": "2023-08-01"},
    {"source": "APT29", "target": "T1059", "relation": "uses", "weight": 0.84, "timestamp": "2024-08-20"},
    {"source": "T1190", "target": "TA0001", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-09-01"},
    {"source": "CVE-2021-26855", "target": "T1190", "relation": "enables", "weight": 0.9, "timestamp": "2021-03-02"},
    {"source": "Hafnium", "target": "CVE-2021-26855", "relation": "exploits", "weight": 0.92, "timestamp": "2021-03-02"},
    {"source": "Lazarus", "target": "T1566", "relation": "uses", "weight": 0.8, "timestamp": "2024-09-15"},
    {"source": "T1021.002", "target": "T1486", "relation": "enables", "weight": 0.7, "timestamp": "2024-12-01"},
    {"source": "Emotet", "target": "T1003", "relation": "enables", "weight": 0.75, "timestamp": "2024-05-15"},
]

def _qa(
    qid: str,
    question: str,
    gold: str,
    entities: list[str],
    evidence: list[str],
    category: str,
    *,
    abstain: bool = False,
) -> dict[str, Any]:
    return {
        "id": qid,
        "question": question,
        "gold_answer": gold,
        "gold_entities": entities,
        "gold_evidence_ids": evidence,
        "category": category,
        "expect_abstain": abstain,
    }


WAVE3_QA_HAND: list[dict[str, Any]] = [
    _qa("qa_061", "Which ATT&CK technique covers public-facing exploits like Log4Shell?",
        "T1190 Exploit Public-Facing Application covers internet-facing service exploitation including Log4Shell-like campaigns.",
        ["T1190", "CVE-2021-44228"], ["ev_041", "ev_003"], "multi_hop"),
    _qa("qa_062", "How do APT29 campaigns typically chain phishing to scripting?",
        "APT29 commonly uses T1566 phishing then living-off-the-land scripting under T1059 after valid-account style access.",
        ["APT29", "T1566", "T1059"], ["ev_005", "ev_042", "ev_060"], "multi_hop"),
    _qa("qa_063", "What Suricata SMB admin-share pattern maps to lateral movement?",
        "Unexpected ADMIN$/C$ access aligns with T1021.002 under TA0008 and should be correlated with phishing context.",
        ["T1021.002", "Suricata", "TA0008"], ["ev_043", "ev_035"], "ids_alert"),
    _qa("qa_064", "What is ProxyLogon CVE-2021-26855 and who abused web shells after it?",
        "CVE-2021-26855 is Exchange SSRF (ProxyLogon); Hafnium chained it with T1505.003 web shells.",
        ["CVE-2021-26855", "Hafnium", "T1505.003"], ["ev_044", "ev_054"], "kev"),
    _qa("qa_065", "How does Emotet relate to TrickBot and credential dumping?",
        "Emotet delivered TrickBot payloads; post-compromise often includes credential dumping under T1003.",
        ["Emotet", "TrickBot", "T1003"], ["ev_045", "ev_058"], "multi_hop"),
    _qa("qa_066", "Why keep historical CVE-2021-44228 in temporal CTI retrieval?",
        "Historical CVEs remain operationally relevant; freshness should soft-weight trust rather than hard-delete seeds.",
        ["CVE-2021-44228", "EDGR"], ["ev_053", "ev_003"], "temporal"),
    _qa("qa_067", "What is the EDGR emit/abstain Trusted Answer rule for CVEs?",
        "Emit only if risk ρ ≤ θ and queried CVEs appear in trusted evidence; otherwise abstain.",
        ["EDGR", "Hallucination"], ["ev_050", "ev_036"], "gate_theory"),
    _qa("qa_068", "Which technique covers ransomware encryption impact?",
        "T1486 Data Encrypted for Impact covers ransomware encryption under TA0040.",
        ["T1486", "TA0040"], ["ev_051"], "core"),
    _qa("qa_069", "How did QakBot typically enter enterprises before Cobalt Strike?",
        "QakBot used spearphishing attachments (T1566.001) and later dropped Cobalt Strike.",
        ["QakBot", "T1566.001", "Cobalt Strike"], ["ev_052"], "multi_hop"),
    _qa("qa_070", "When should SOC avoid auto-blocking encoded PowerShell?",
        "Unsigned encoded PowerShell may be admin automation; require T1059.001 plus suspicious parent/network context.",
        ["T1059.001", "PowerShell", "Suricata"], ["ev_059", "ev_001"], "ids_alert"),
    _qa("qa_071", "What CAPEC pattern maps to CWE-89 SQL injection?",
        "CAPEC-66 SQL Injection relates to CWE-89; look for UNION SELECT and tautology payloads.",
        ["CAPEC-66", "CWE-89"], ["ev_055", "ev_008"], "core"),
    _qa("qa_072", "Which datasets are standard for NIDS model evaluation?",
        "CIC-IDS2017 and UNSW-NB15 are widely used NIDS evaluation datasets.",
        ["CIC-IDS2017", "UNSW-NB15", "NIDS"], ["ev_056", "ev_014"], "dataset"),
    _qa("qa_073", "How should analysts fuse Suricata alerts with CISA KEV tags?",
        "Correlate Suricata anomalies with CISA KEV CVE tags before closing as FP; abstain if CVE strings are unknown.",
        ["Suricata", "CISA KEV", "EDGR"], ["ev_047", "ev_013"], "ids_alert"),
    _qa("qa_074", "What Cl0p technique pair follows MOVEit exploitation?",
        "Cl0p exploited CVE-2023-34362 and commonly uses impact/encryption paths such as T1486 in ransomware operations.",
        ["Cl0p", "CVE-2023-34362", "T1486"], ["ev_049", "ev_051", "ev_004"], "multi_hop"),
    _qa("qa_075", "What is the CVSS vector and patch URL for CVE-2099-55555?",
        "[ABSTAIN] CVE-2099-55555 is not present in the Dynamic KG or evidence store.",
        ["EDGR"], ["ev_050", "ev_026"], "ood_abstain", abstain=True),
    _qa("qa_076", "Provide exploit PoC details for CVE-2099-66666 from vendor blogs.",
        "[ABSTAIN] CVE-2099-66666 is unsupported in the local CTI store; EDGR must abstain.",
        ["EDGR"], ["ev_050"], "ood_abstain", abstain=True),
    _qa("qa_077", "How do T1078 and T1133 interact for remote initial access?",
        "T1133 covers VPN/VDI exposure; combine with T1078 when credential stuffing precedes remote login.",
        ["T1078", "T1133", "TA0001"], ["ev_048", "ev_033"], "multi_hop"),
    _qa("qa_078", "Where should hunters look for Hafnium ASPX web shells?",
        "Hunt unusual ASPX under Outlook directories corresponding to T1505.003 after ProxyLogon.",
        ["Hafnium", "T1505.003", "CVE-2021-26855"], ["ev_054", "ev_044"], "multi_hop"),
    _qa("qa_079", "Why is graph expansion useful for APT29 TTP chains?",
        "APT29 chains such as T1566→T1078 are relational; graph expansion surfaces edges before flat ranking alone.",
        ["APT29", "T1566", "T1078", "EDGR"], ["ev_060", "ev_005"], "gate_theory"),
    _qa("qa_080", "What LSASS technique follows TrickBot staging?",
        "T1003.001 LSASS Memory is a common credential dumping path after TrickBot staging.",
        ["T1003.001", "TrickBot", "T1003"], ["ev_040", "ev_058"], "multi_hop"),
    _qa("qa_081", "Is CVE-2022-22965 mapped to T1190 like Log4Shell?",
        "Yes — Spring4Shell CVE-2022-22965 maps to T1190 similarly to Log4Shell.",
        ["CVE-2022-22965", "T1190", "Spring4Shell"], ["ev_039", "ev_041"], "kev"),
    _qa("qa_082", "What Lazarus targeting pattern should precede strong attribution claims?",
        "Map observed binaries to malware nodes and known TTPs before strong attribution claims on Lazarus activity.",
        ["Lazarus"], ["ev_057", "ev_006"], "temporal"),
    _qa("qa_083", "Which parent technique covers T1003.001?",
        "T1003 Credential Dumping is the parent of T1003.001 LSASS Memory.",
        ["T1003", "T1003.001"], ["ev_058", "ev_040"], "core"),
    _qa("qa_084", "How should ransomware isolation prioritize T1486 with lateral movement?",
        "Prioritize isolation when T1486 co-occurs with T1021 lateral movement on the same host cluster.",
        ["T1486", "T1021"], ["ev_051", "ev_043"], "ids_alert"),
    _qa("qa_085", "What phishing sub-technique did QakBot use?",
        "QakBot used T1566.001 Spearphishing Attachment among other malspam patterns.",
        ["QakBot", "T1566.001"], ["ev_052"], "core"),
    _qa("qa_086", "Does CISA KEV prioritize Exchange ProxyLogon-class CVEs?",
        "CISA KEV lists actively exploited vulnerabilities; Exchange ProxyLogon-related CVEs are treated as priority.",
        ["CISA KEV", "CVE-2021-26855"], ["ev_044", "ev_013"], "kev"),
    _qa("qa_087", "What is the relationship between Emotet and Cobalt Strike via TrickBot?",
        "Emotet can deliver TrickBot which may later drop Cobalt Strike in staging chains.",
        ["Emotet", "TrickBot", "Cobalt Strike"], ["ev_045"], "multi_hop"),
    _qa("qa_088", "Why abstain when a ticket names an unknown CVE string?",
        "Unknown CVE identifiers risk fabricated dossiers; EDGR abstains when CVEs are absent from KG and evidence.",
        ["EDGR"], ["ev_047", "ev_050"], "gate_theory"),
    _qa("qa_089", "Which tactic does T1486 belong to?",
        "T1486 belongs to TA0040 Impact.",
        ["T1486", "TA0040"], ["ev_051"], "graph_derived"),
    _qa("qa_090", "What detection foci apply to T1059.001 PowerShell abuse?",
        "Detection includes process creation, ScriptBlock logging, and command-line auditing for T1059.001.",
        ["T1059.001", "PowerShell", "TA0002"], ["ev_001", "ev_042"], "core"),
]
