"""Seed Cyber Threat Intelligence knowledge for Dynamic KG + retrieval."""

from __future__ import annotations

from typing import Any

# Evidence chunks used by vector retrieval and answer grounding
EVIDENCE_CHUNKS: list[dict[str, Any]] = [
    {
        "id": "ev_001",
        "content": (
            "MITRE ATT&CK technique T1059.001 (PowerShell) enables adversaries to execute "
            "commands and scripts. Detection sources include process creation events, "
            "ScriptBlock logging, and command-line auditing. Common parent processes include "
            "cmd.exe, wscript.exe, and office applications."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1059.001", "PowerShell", "TA0002"],
        "timestamp": "2024-11-01",
        "reliability": 0.95,
        "type": "technique",
    },
    {
        "id": "ev_002",
        "content": (
            "Technique T1078 (Valid Accounts) abuses legitimate credentials for initial access "
            "and persistence. Indicators include anomalous login locations, impossible travel, "
            "and privilege escalation without corresponding change tickets."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1078", "Valid Accounts", "TA0001"],
        "timestamp": "2024-10-15",
        "reliability": 0.94,
        "type": "technique",
    },
    {
        "id": "ev_003",
        "content": (
            "CVE-2021-44228 (Log4Shell) is a remote code execution vulnerability in Apache Log4j2 "
            "(versions 2.0-beta9 through 2.14.1). Exploitation uses JNDI lookup strings such as "
            "${jndi:ldap://...}. Mitigations include upgrading to Log4j 2.17.1+ and blocking "
            "outbound LDAP/RMI."
        ),
        "source": "NVD/CVE",
        "entities": ["CVE-2021-44228", "Log4Shell", "Log4j"],
        "timestamp": "2021-12-10",
        "reliability": 0.98,
        "type": "cve",
    },
    {
        "id": "ev_004",
        "content": (
            "CVE-2023-34362 is a SQL injection vulnerability in Progress MOVEit Transfer that "
            "allows unauthenticated attackers to escalate privileges and steal data. Cl0p "
            "ransomware operators widely exploited this CVE in 2023 campaigns."
        ),
        "source": "NVD/CVE",
        "entities": ["CVE-2023-34362", "MOVEit", "Cl0p"],
        "timestamp": "2023-06-02",
        "reliability": 0.97,
        "type": "cve",
    },
    {
        "id": "ev_005",
        "content": (
            "APT29 (Cozy Bear) commonly uses spearphishing, legitimate cloud services, and "
            "living-off-the-land binaries. Mapped ATT&CK techniques include T1566 (Phishing), "
            "T1078 (Valid Accounts), and T1059 (Command and Scripting Interpreter)."
        ),
        "source": "CISA/CTI",
        "entities": ["APT29", "T1566", "T1078", "T1059"],
        "timestamp": "2024-08-20",
        "reliability": 0.92,
        "type": "actor",
    },
    {
        "id": "ev_006",
        "content": (
            "Lazarus Group campaigns frequently target financial institutions and cryptocurrency "
            "exchanges. Observed TTPs include supply-chain compromise, custom malware droppers, "
            "and abuse of signed binaries. Related techniques: T1195, T1105, T1055."
        ),
        "source": "CERT/CTI",
        "entities": ["Lazarus", "T1195", "T1105", "T1055"],
        "timestamp": "2024-05-12",
        "reliability": 0.91,
        "type": "actor",
    },
    {
        "id": "ev_007",
        "content": (
            "Network Intrusion Detection Systems (NIDS) such as Suricata and Zeek detect "
            "lateral movement via anomalous SMB, RDP, and DNS tunneling patterns. Alert "
            "correlation with MITRE ATT&CK improves analyst triage and reduces false positives."
        ),
        "source": "IDS/NIDS Guide",
        "entities": ["NIDS", "Suricata", "Zeek", "TA0008"],
        "timestamp": "2024-09-01",
        "reliability": 0.88,
        "type": "concept",
    },
    {
        "id": "ev_008",
        "content": (
            "CWE-89 (SQL Injection) occurs when untrusted input is concatenated into SQL queries. "
            "CAPEC-66 describes exploitation patterns. Detection signatures look for UNION SELECT, "
            "OR 1=1, and comment-based payloads in HTTP parameters."
        ),
        "source": "CWE/CAPEC",
        "entities": ["CWE-89", "CAPEC-66", "SQL Injection"],
        "timestamp": "2024-03-18",
        "reliability": 0.96,
        "type": "concept",
    },
    {
        "id": "ev_009",
        "content": (
            "Emotet malware uses malspam attachments and links to deliver payloads, then downloads "
            "secondary malware such as TrickBot or ransomware. Detection focuses on Office macro "
            "execution, suspicious PowerShell downloads, and C2 beaconing intervals."
        ),
        "source": "Threat Feed",
        "entities": ["Emotet", "TrickBot", "T1566.001", "T1059.001"],
        "timestamp": "2024-07-22",
        "reliability": 0.89,
        "type": "malware",
    },
    {
        "id": "ev_010",
        "content": (
            "Hallucination in LLM-based CTI assistants often appears as fabricated CVE IDs, "
            "incorrect ATT&CK mappings, or invented remediation steps. Evidence-driven retrieval "
            "with graph consistency checks reduces unsupported claims before answer generation."
        ),
        "source": "Research Note",
        "entities": ["Hallucination", "EDGR", "CTI"],
        "timestamp": "2025-01-10",
        "reliability": 0.85,
        "type": "concept",
    },
    {
        "id": "ev_011",
        "content": (
            "Tactic TA0001 Initial Access covers techniques adversaries use to gain a foothold, "
            "including phishing (T1566), exploit public-facing application (T1190), and external "
            "remote services (T1133)."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["TA0001", "T1566", "T1190", "T1133"],
        "timestamp": "2024-11-01",
        "reliability": 0.95,
        "type": "tactic",
    },
    {
        "id": "ev_012",
        "content": (
            "Tactic TA0002 Execution includes T1059 Command and Scripting Interpreter and "
            "T1204 User Execution. IDS rules should alert on encoded PowerShell (-enc), "
            "mshta javascript URLs, and unusual WMI process creation."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["TA0002", "T1059", "T1204"],
        "timestamp": "2024-11-01",
        "reliability": 0.95,
        "type": "technique",
    },
    {
        "id": "ev_013",
        "content": (
            "CISA KEV catalog lists actively exploited vulnerabilities. Organizations should "
            "prioritize patching KEV entries within mandated timelines. Log4Shell "
            "(CVE-2021-44228) and MOVEit (CVE-2023-34362) appear as high-priority examples."
        ),
        "source": "CISA KEV",
        "entities": ["CISA KEV", "CVE-2021-44228", "CVE-2023-34362"],
        "timestamp": "2024-12-01",
        "reliability": 0.97,
        "type": "concept",
    },
    {
        "id": "ev_014",
        "content": (
            "CIC-IDS2017 and UNSW-NB15 are widely used NIDS datasets for evaluating intrusion "
            "detection models. Features include flow duration, packet rates, and protocol flags. "
            "Class imbalance and concept drift remain open evaluation challenges."
        ),
        "source": "IDS Dataset",
        "entities": ["CIC-IDS2017", "UNSW-NB15", "NIDS"],
        "timestamp": "2023-01-15",
        "reliability": 0.9,
        "type": "dataset",
    },
    {
        "id": "ev_015",
        "content": (
            "Technique T1048 Exfiltration Over Alternative Protocol moves data via DNS, ICMP, "
            "or non-standard ports. Zeek dns.log and Suricata DNS anomaly rules help detect "
            "tunneling. Correlate with T1041 Exfiltration Over C2 Channel."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1048", "T1041", "TA0010"],
        "timestamp": "2024-06-30",
        "reliability": 0.93,
        "type": "technique",
    },
    {
        "id": "ev_016",
        "content": (
            "GraphRAG retrieves community summaries from knowledge graphs, but may still "
            "surface stale CTI edges. EDGR adds temporal filtering and hallucination scoring "
            "to prefer fresh, consistent, multi-source evidence before LLM generation."
        ),
        "source": "Research Note",
        "entities": ["GraphRAG", "EDGR", "Hallucination"],
        "timestamp": "2025-02-01",
        "reliability": 0.86,
        "type": "concept",
    },
]

NODES: list[dict[str, Any]] = [
    {"id": "T1059.001", "label": "PowerShell", "type": "technique", "timestamp": "2024-11-01", "reliability": 0.95,
     "properties": {"tactic": "TA0002", "platform": "Windows"}},
    {"id": "T1078", "label": "Valid Accounts", "type": "technique", "timestamp": "2024-10-15", "reliability": 0.94,
     "properties": {"tactic": "TA0001"}},
    {"id": "T1566", "label": "Phishing", "type": "technique", "timestamp": "2024-11-01", "reliability": 0.95,
     "properties": {"tactic": "TA0001"}},
    {"id": "T1190", "label": "Exploit Public-Facing Application", "type": "technique", "timestamp": "2024-11-01",
     "reliability": 0.95, "properties": {"tactic": "TA0001"}},
    {"id": "T1048", "label": "Exfiltration Over Alternative Protocol", "type": "technique", "timestamp": "2024-06-30",
     "reliability": 0.93, "properties": {"tactic": "TA0010"}},
    {"id": "T1055", "label": "Process Injection", "type": "technique", "timestamp": "2024-05-12", "reliability": 0.92,
     "properties": {"tactic": "TA0005"}},
    {"id": "T1195", "label": "Supply Chain Compromise", "type": "technique", "timestamp": "2024-05-12", "reliability": 0.91,
     "properties": {"tactic": "TA0001"}},
    {"id": "T1105", "label": "Ingress Tool Transfer", "type": "technique", "timestamp": "2024-05-12", "reliability": 0.91,
     "properties": {"tactic": "TA0011"}},
    {"id": "TA0001", "label": "Initial Access", "type": "tactic", "timestamp": "2024-11-01", "reliability": 0.96,
     "properties": {}},
    {"id": "TA0002", "label": "Execution", "type": "tactic", "timestamp": "2024-11-01", "reliability": 0.96,
     "properties": {}},
    {"id": "TA0008", "label": "Lateral Movement", "type": "tactic", "timestamp": "2024-09-01", "reliability": 0.95,
     "properties": {}},
    {"id": "TA0010", "label": "Exfiltration", "type": "tactic", "timestamp": "2024-06-30", "reliability": 0.95,
     "properties": {}},
    {"id": "CVE-2021-44228", "label": "Log4Shell", "type": "cve", "timestamp": "2021-12-10", "reliability": 0.98,
     "properties": {"cvss": 10.0, "kev": True}},
    {"id": "CVE-2023-34362", "label": "MOVEit Transfer SQLi", "type": "cve", "timestamp": "2023-06-02", "reliability": 0.97,
     "properties": {"cvss": 9.8, "kev": True}},
    {"id": "APT29", "label": "APT29 / Cozy Bear", "type": "actor", "timestamp": "2024-08-20", "reliability": 0.92,
     "properties": {"origin": "RU"}},
    {"id": "Lazarus", "label": "Lazarus Group", "type": "actor", "timestamp": "2024-05-12", "reliability": 0.91,
     "properties": {"origin": "KP"}},
    {"id": "Cl0p", "label": "Cl0p", "type": "actor", "timestamp": "2023-06-02", "reliability": 0.9,
     "properties": {"type": "ransomware"}},
    {"id": "Emotet", "label": "Emotet", "type": "malware", "timestamp": "2024-07-22", "reliability": 0.89,
     "properties": {}},
    {"id": "TrickBot", "label": "TrickBot", "type": "malware", "timestamp": "2024-07-22", "reliability": 0.88,
     "properties": {}},
    {"id": "Suricata", "label": "Suricata", "type": "software", "timestamp": "2024-09-01", "reliability": 0.9,
     "properties": {"role": "NIDS"}},
    {"id": "Zeek", "label": "Zeek", "type": "software", "timestamp": "2024-09-01", "reliability": 0.9,
     "properties": {"role": "NIDS"}},
    {"id": "CWE-89", "label": "SQL Injection", "type": "concept", "timestamp": "2024-03-18", "reliability": 0.96,
     "properties": {}},
    {"id": "CAPEC-66", "label": "SQL Injection CAPEC", "type": "concept", "timestamp": "2024-03-18", "reliability": 0.95,
     "properties": {}},
    {"id": "CIC-IDS2017", "label": "CIC-IDS2017", "type": "dataset", "timestamp": "2023-01-15", "reliability": 0.9,
     "properties": {}},
    {"id": "EDGR", "label": "EDGR Algorithm", "type": "concept", "timestamp": "2025-02-01", "reliability": 0.9,
     "properties": {"role": "main_contribution"}},
]

EDGES: list[dict[str, Any]] = [
    {"source": "T1059.001", "target": "TA0002", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-11-01"},
    {"source": "T1078", "target": "TA0001", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-10-15"},
    {"source": "T1566", "target": "TA0001", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-11-01"},
    {"source": "T1190", "target": "TA0001", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-11-01"},
    {"source": "T1048", "target": "TA0010", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-06-30"},
    {"source": "APT29", "target": "T1566", "relation": "uses", "weight": 0.9, "timestamp": "2024-08-20"},
    {"source": "APT29", "target": "T1078", "relation": "uses", "weight": 0.85, "timestamp": "2024-08-20"},
    {"source": "APT29", "target": "T1059.001", "relation": "uses", "weight": 0.8, "timestamp": "2024-08-20"},
    {"source": "Lazarus", "target": "T1195", "relation": "uses", "weight": 0.88, "timestamp": "2024-05-12"},
    {"source": "Lazarus", "target": "T1105", "relation": "uses", "weight": 0.86, "timestamp": "2024-05-12"},
    {"source": "Lazarus", "target": "T1055", "relation": "uses", "weight": 0.84, "timestamp": "2024-05-12"},
    {"source": "Cl0p", "target": "CVE-2023-34362", "relation": "exploits", "weight": 0.95, "timestamp": "2023-06-02"},
    {"source": "CVE-2023-34362", "target": "CWE-89", "relation": "related_to", "weight": 0.9, "timestamp": "2023-06-02"},
    {"source": "CWE-89", "target": "CAPEC-66", "relation": "related_to", "weight": 0.95, "timestamp": "2024-03-18"},
    {"source": "CVE-2021-44228", "target": "T1190", "relation": "enables", "weight": 0.92, "timestamp": "2021-12-10"},
    {"source": "Emotet", "target": "T1566", "relation": "delivers_via", "weight": 0.9, "timestamp": "2024-07-22"},
    {"source": "Emotet", "target": "T1059.001", "relation": "uses", "weight": 0.88, "timestamp": "2024-07-22"},
    {"source": "Emotet", "target": "TrickBot", "relation": "drops", "weight": 0.85, "timestamp": "2024-07-22"},
    {"source": "Suricata", "target": "TA0008", "relation": "detects", "weight": 0.8, "timestamp": "2024-09-01"},
    {"source": "Zeek", "target": "T1048", "relation": "detects", "weight": 0.85, "timestamp": "2024-09-01"},
    {"source": "EDGR", "target": "CVE-2021-44228", "relation": "grounds_on", "weight": 0.7, "timestamp": "2025-02-01"},
    {"source": "EDGR", "target": "T1059.001", "relation": "grounds_on", "weight": 0.7, "timestamp": "2025-02-01"},
]

# Gold QA pairs for evaluation
QA_DATASET: list[dict[str, Any]] = [
    {
        "id": "qa_001",
        "question": "What is CVE-2021-44228 and how is it exploited?",
        "gold_answer": (
            "CVE-2021-44228 (Log4Shell) is an RCE vulnerability in Apache Log4j2 "
            "exploited via JNDI lookup strings; mitigate by upgrading Log4j and blocking outbound LDAP/RMI."
        ),
        "gold_entities": ["CVE-2021-44228", "Log4Shell", "Log4j"],
        "gold_evidence_ids": ["ev_003", "ev_013"],
    },
    {
        "id": "qa_002",
        "question": "Which ATT&CK techniques does APT29 commonly use?",
        "gold_answer": (
            "APT29 commonly uses T1566 Phishing, T1078 Valid Accounts, and T1059 Command and Scripting Interpreter."
        ),
        "gold_entities": ["APT29", "T1566", "T1078", "T1059"],
        "gold_evidence_ids": ["ev_005"],
    },
    {
        "id": "qa_003",
        "question": "How can NIDS detect lateral movement?",
        "gold_answer": (
            "NIDS such as Suricata and Zeek detect lateral movement via anomalous SMB, RDP, "
            "and DNS tunneling; correlating alerts with ATT&CK improves triage."
        ),
        "gold_entities": ["NIDS", "Suricata", "Zeek", "TA0008"],
        "gold_evidence_ids": ["ev_007"],
    },
    {
        "id": "qa_004",
        "question": "What malware does Emotet typically deliver?",
        "gold_answer": (
            "Emotet delivers secondary malware such as TrickBot or ransomware after initial malspam infection."
        ),
        "gold_entities": ["Emotet", "TrickBot"],
        "gold_evidence_ids": ["ev_009"],
    },
    {
        "id": "qa_005",
        "question": "How does EDGR reduce hallucination in CTI answers?",
        "gold_answer": (
            "EDGR uses temporal filtering, graph consistency, and hallucination scoring to select "
            "trusted evidence before LLM generation, reducing fabricated CVE IDs and incorrect ATT&CK mappings."
        ),
        "gold_entities": ["EDGR", "Hallucination", "CTI"],
        "gold_evidence_ids": ["ev_010", "ev_016"],
    },
    {
        "id": "qa_006",
        "question": "Which CVE did Cl0p exploit in MOVEit campaigns?",
        "gold_answer": (
            "Cl0p exploited CVE-2023-34362, a SQL injection in Progress MOVEit Transfer."
        ),
        "gold_entities": ["Cl0p", "CVE-2023-34362", "MOVEit"],
        "gold_evidence_ids": ["ev_004"],
    },
    {
        "id": "qa_007",
        "question": "What is CWE-89 related CAPEC pattern?",
        "gold_answer": (
            "CWE-89 SQL Injection relates to CAPEC-66; detection looks for UNION SELECT and tautology payloads."
        ),
        "gold_entities": ["CWE-89", "CAPEC-66"],
        "gold_evidence_ids": ["ev_008"],
    },
    {
        "id": "qa_008",
        "question": "What datasets are used to evaluate NIDS models?",
        "gold_answer": (
            "CIC-IDS2017 and UNSW-NB15 are widely used NIDS evaluation datasets."
        ),
        "gold_entities": ["CIC-IDS2017", "UNSW-NB15", "NIDS"],
        "gold_evidence_ids": ["ev_014"],
    },
]

# PhD rigor expansion: multi-hop / temporal / IDS / OOD-abstain / gate-theory items
from app.data.cti_seed_expand import (  # noqa: E402
    EXTRA_EDGES,
    EXTRA_EVIDENCE,
    EXTRA_NODES,
    EXTRA_QA,
)

EVIDENCE_CHUNKS.extend(EXTRA_EVIDENCE)
NODES.extend(EXTRA_NODES)
EDGES.extend(EXTRA_EDGES)
QA_DATASET.extend(EXTRA_QA)

# Tag original items for stratified reporting
for _qa in QA_DATASET:
    _qa.setdefault("category", "core")
    _qa.setdefault("expect_abstain", False)

# Wave-2 scale-up for PhD / human-eval (N≥48)
from app.data.cti_seed_scale import (  # noqa: E402
    SCALE_EDGES,
    SCALE_EVIDENCE,
    SCALE_NODES,
    SCALE_QA_HAND,
    attach_evidence_ids_for_graph_qa,
    build_graph_qa,
)

EVIDENCE_CHUNKS.extend(SCALE_EVIDENCE)
NODES.extend(SCALE_NODES)
EDGES.extend(SCALE_EDGES)
QA_DATASET.extend(SCALE_QA_HAND)

# Wave-3 IEEE-oriented scale-up (larger KG/evidence + stratified hand QA)
from app.data.cti_seed_wave3 import (  # noqa: E402
    WAVE3_EDGES,
    WAVE3_EVIDENCE,
    WAVE3_NODES,
    WAVE3_QA_HAND,
)

EVIDENCE_CHUNKS.extend(WAVE3_EVIDENCE)
NODES.extend(WAVE3_NODES)
EDGES.extend(WAVE3_EDGES)
QA_DATASET.extend(WAVE3_QA_HAND)

# Wave-4 IEEE-scale programmatic CTI expansion
from app.data.cti_seed_wave4 import (  # noqa: E402
    WAVE4_EDGES,
    WAVE4_EVIDENCE,
    WAVE4_NODES,
    WAVE4_QA_HAND,
)

EVIDENCE_CHUNKS.extend(WAVE4_EVIDENCE)
NODES.extend(WAVE4_NODES)
EDGES.extend(WAVE4_EDGES)
QA_DATASET.extend(WAVE4_QA_HAND)

# Graph-derived QA (bounded so categories stay stratified)
_GRAPH_QA = build_graph_qa(EDGES, start_index=200, limit=50)
attach_evidence_ids_for_graph_qa(_GRAPH_QA, EVIDENCE_CHUNKS)
QA_DATASET.extend(_GRAPH_QA)
for _qa in QA_DATASET:
    _qa.setdefault("category", "core")
    _qa.setdefault("expect_abstain", False)
