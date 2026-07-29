"""Expanded CTI seed for PhD-scale demo evaluation (appended to cti_seed).

Adds multi-hop, temporal, IDS-alert, OOD-abstain, and KEV-priority items.
Target after merge: ~24 QA, ~32 evidence chunks, richer KG.
"""

from __future__ import annotations

from typing import Any

EXTRA_EVIDENCE: list[dict[str, Any]] = [
    {
        "id": "ev_017",
        "content": (
            "Technique T1021.002 (SMB/Windows Admin Shares) supports lateral movement after "
            "valid credentials are obtained. NIDS should flag unusual admin$ or C$ access "
            "from workstations and correlate with T1078 Valid Accounts."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1021.002", "T1078", "TA0008"],
        "timestamp": "2024-09-15",
        "reliability": 0.93,
        "type": "technique",
    },
    {
        "id": "ev_018",
        "content": (
            "CVE-2024-3400 is a command injection vulnerability in Palo Alto Networks PAN-OS "
            "GlobalProtect gateway. CISA added it to the KEV catalog; exploitation enables "
            "unauthenticated remote code execution on vulnerable firewalls."
        ),
        "source": "NVD/CVE",
        "entities": ["CVE-2024-3400", "PAN-OS", "CISA KEV"],
        "timestamp": "2024-04-12",
        "reliability": 0.97,
        "type": "cve",
    },
    {
        "id": "ev_019",
        "content": (
            "SolarWinds supply-chain compromise (SUNBURST) is attributed to APT29. Related "
            "ATT&CK techniques include T1195.002 Compromise Software Supply Chain and "
            "T1078 Valid Accounts for persistence in victim networks."
        ),
        "source": "CISA/CTI",
        "entities": ["APT29", "SUNBURST", "T1195.002", "T1078"],
        "timestamp": "2021-01-10",
        "reliability": 0.94,
        "type": "actor",
    },
    {
        "id": "ev_020",
        "content": (
            "DNS tunneling often implements T1048 Exfiltration Over Alternative Protocol. "
            "High entropy subdomain queries, long query names, and periodic beaconing in "
            "Zeek dns.log are primary IDS indicators."
        ),
        "source": "IDS/NIDS Guide",
        "entities": ["T1048", "Zeek", "TA0010"],
        "timestamp": "2024-10-01",
        "reliability": 0.9,
        "type": "technique",
    },
    {
        "id": "ev_021",
        "content": (
            "TrickBot modules support credential dumping and lateral movement after Emotet "
            "delivery. Observed follow-on techniques include T1003 OS Credential Dumping "
            "and T1021 Remote Services."
        ),
        "source": "Threat Feed",
        "entities": ["TrickBot", "Emotet", "T1003", "T1021"],
        "timestamp": "2024-07-22",
        "reliability": 0.87,
        "type": "malware",
    },
    {
        "id": "ev_022",
        "content": (
            "Stale CTI: a 2019 advisory claiming CVE-2021-44228 remediation via Log4j 2.12 "
            "alone is incomplete for modern deployments; current guidance requires 2.17.1+ "
            "or equivalent mitigations listed in NVD/CISA."
        ),
        "source": "Research Note",
        "entities": ["CVE-2021-44228", "Log4j"],
        "timestamp": "2019-06-01",
        "reliability": 0.55,
        "type": "concept",
    },
    {
        "id": "ev_023",
        "content": (
            "IDS alert signature ET POLICY SMB2 NT Create AndX Request For An Executable File "
            "may indicate T1021.002 lateral movement when combined with unusual source hosts. "
            "Analysts should pivot to ATT&CK TA0008 and validate with host telemetry."
        ),
        "source": "IDS/NIDS Guide",
        "entities": ["T1021.002", "TA0008", "Suricata"],
        "timestamp": "2024-11-20",
        "reliability": 0.86,
        "type": "alert",
    },
    {
        "id": "ev_024",
        "content": (
            "CAPEC-242 (Code Injection) generalizes injection flaws including those enabling "
            "T1190 Exploit Public-Facing Application. Log4Shell (CVE-2021-44228) is a "
            "well-known instance used for initial access."
        ),
        "source": "CWE/CAPEC",
        "entities": ["CAPEC-242", "T1190", "CVE-2021-44228"],
        "timestamp": "2024-02-01",
        "reliability": 0.92,
        "type": "concept",
    },
    {
        "id": "ev_025",
        "content": (
            "ProxyLogon (CVE-2021-26855) is a Microsoft Exchange SSRF used with related CVEs "
            "for unauthenticated RCE. Hafnium-style campaigns mapped initial access to T1190 "
            "and persistence via web shells (T1505.003)."
        ),
        "source": "NVD/CVE",
        "entities": ["CVE-2021-26855", "T1190", "T1505.003", "Hafnium"],
        "timestamp": "2021-03-02",
        "reliability": 0.96,
        "type": "cve",
    },
    {
        "id": "ev_026",
        "content": (
            "Trusted Answer contract: if a queried CVE identifier is absent from both the "
            "Dynamic KG and retrieved evidence text, EDGR must abstain rather than invent "
            "CVSS scores, vendors, or ATT&CK mappings."
        ),
        "source": "Research Note",
        "entities": ["EDGR", "Hallucination", "CTI"],
        "timestamp": "2025-03-01",
        "reliability": 0.9,
        "type": "concept",
    },
    {
        "id": "ev_027",
        "content": (
            "UNSW-NB15 includes nine attack families and a large number of features for "
            "flow-based NIDS research. It complements CIC-IDS2017 when evaluating detection "
            "generalization under class imbalance."
        ),
        "source": "IDS Dataset",
        "entities": ["UNSW-NB15", "CIC-IDS2017", "NIDS"],
        "timestamp": "2023-01-15",
        "reliability": 0.9,
        "type": "dataset",
    },
    {
        "id": "ev_028",
        "content": (
            "Technique T1059.003 (Windows Command Shell) is frequently chained after phishing "
            "(T1566) for execution. Process-creation logging of cmd.exe with encoded commands "
            "supports detection alongside PowerShell (T1059.001)."
        ),
        "source": "MITRE ATT&CK",
        "entities": ["T1059.003", "T1566", "T1059.001", "TA0002"],
        "timestamp": "2024-11-01",
        "reliability": 0.94,
        "type": "technique",
    },
    {
        "id": "ev_029",
        "content": (
            "Multi-hop CTI path: Cl0p exploits CVE-2023-34362 (CWE-89 / CAPEC-66), enabling "
            "data theft from MOVEit Transfer. Analyst questions should connect actor → CVE → "
            "weakness → detection signature, not bag-of-passages alone."
        ),
        "source": "Research Note",
        "entities": ["Cl0p", "CVE-2023-34362", "CWE-89", "CAPEC-66", "MOVEit"],
        "timestamp": "2024-08-01",
        "reliability": 0.88,
        "type": "concept",
    },
    {
        "id": "ev_030",
        "content": (
            "Freshness window: for actively exploited KEV CVEs, evidence newer than the KEV "
            "listing date should outrank older blog speculation when EDGR applies temporal "
            "filtering before generation."
        ),
        "source": "CISA KEV",
        "entities": ["CISA KEV", "EDGR"],
        "timestamp": "2024-12-15",
        "reliability": 0.95,
        "type": "concept",
    },
    {
        "id": "ev_031",
        "content": (
            "Lazarus Group has used ingress tool transfer (T1105) after supply-chain footholds "
            "(T1195). Financial-sector detections should correlate signed-binary abuse with "
            "unusual outbound transfers."
        ),
        "source": "CERT/CTI",
        "entities": ["Lazarus", "T1105", "T1195"],
        "timestamp": "2024-05-12",
        "reliability": 0.9,
        "type": "actor",
    },
    {
        "id": "ev_032",
        "content": (
            "ρ-gate decision theory: lowering θ increases false rejects (abstain when evidence "
            "exists) while raising θ increases false emits (answers with high hallucination risk). "
            "EDGR tunes θ on a validation split under a fixed Trusted Answer contract."
        ),
        "source": "Research Note",
        "entities": ["EDGR", "Hallucination"],
        "timestamp": "2025-03-15",
        "reliability": 0.87,
        "type": "concept",
    },
]

EXTRA_NODES: list[dict[str, Any]] = [
    {"id": "T1021.002", "label": "SMB/Windows Admin Shares", "type": "technique",
     "timestamp": "2024-09-15", "reliability": 0.93, "properties": {"tactic": "TA0008"}},
    {"id": "T1195.002", "label": "Compromise Software Supply Chain", "type": "technique",
     "timestamp": "2021-01-10", "reliability": 0.93, "properties": {"tactic": "TA0001"}},
    {"id": "T1003", "label": "OS Credential Dumping", "type": "technique",
     "timestamp": "2024-07-22", "reliability": 0.9, "properties": {"tactic": "TA0006"}},
    {"id": "T1505.003", "label": "Web Shell", "type": "technique",
     "timestamp": "2021-03-02", "reliability": 0.92, "properties": {"tactic": "TA0003"}},
    {"id": "T1059.003", "label": "Windows Command Shell", "type": "technique",
     "timestamp": "2024-11-01", "reliability": 0.94, "properties": {"tactic": "TA0002"}},
    {"id": "CVE-2024-3400", "label": "PAN-OS GlobalProtect RCE", "type": "cve",
     "timestamp": "2024-04-12", "reliability": 0.97, "properties": {"kev": True}},
    {"id": "CVE-2021-26855", "label": "ProxyLogon SSRF", "type": "cve",
     "timestamp": "2021-03-02", "reliability": 0.96, "properties": {"kev": True}},
    {"id": "Hafnium", "label": "Hafnium", "type": "actor",
     "timestamp": "2021-03-02", "reliability": 0.9, "properties": {}},
    {"id": "CAPEC-242", "label": "Code Injection", "type": "concept",
     "timestamp": "2024-02-01", "reliability": 0.92, "properties": {}},
    {"id": "UNSW-NB15", "label": "UNSW-NB15", "type": "dataset",
     "timestamp": "2023-01-15", "reliability": 0.9, "properties": {}},
    {"id": "SUNBURST", "label": "SUNBURST", "type": "malware",
     "timestamp": "2021-01-10", "reliability": 0.93, "properties": {}},
]

EXTRA_EDGES: list[dict[str, Any]] = [
    {"source": "T1021.002", "target": "TA0008", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-09-15"},
    {"source": "T1059.003", "target": "TA0002", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-11-01"},
    {"source": "T1195.002", "target": "TA0001", "relation": "belongs_to", "weight": 1.0, "timestamp": "2021-01-10"},
    {"source": "APT29", "target": "T1195.002", "relation": "uses", "weight": 0.9, "timestamp": "2021-01-10"},
    {"source": "APT29", "target": "SUNBURST", "relation": "uses", "weight": 0.92, "timestamp": "2021-01-10"},
    {"source": "SUNBURST", "target": "T1195.002", "relation": "related_to", "weight": 0.9, "timestamp": "2021-01-10"},
    {"source": "CVE-2024-3400", "target": "T1190", "relation": "enables", "weight": 0.93, "timestamp": "2024-04-12"},
    {"source": "CVE-2021-26855", "target": "T1190", "relation": "enables", "weight": 0.94, "timestamp": "2021-03-02"},
    {"source": "Hafnium", "target": "CVE-2021-26855", "relation": "exploits", "weight": 0.9, "timestamp": "2021-03-02"},
    {"source": "Hafnium", "target": "T1505.003", "relation": "uses", "weight": 0.88, "timestamp": "2021-03-02"},
    {"source": "TrickBot", "target": "T1003", "relation": "uses", "weight": 0.86, "timestamp": "2024-07-22"},
    {"source": "CAPEC-242", "target": "T1190", "relation": "related_to", "weight": 0.85, "timestamp": "2024-02-01"},
    {"source": "Suricata", "target": "T1021.002", "relation": "detects", "weight": 0.8, "timestamp": "2024-11-20"},
    {"source": "EDGR", "target": "CVE-2024-3400", "relation": "grounds_on", "weight": 0.7, "timestamp": "2025-03-01"},
]

EXTRA_QA: list[dict[str, Any]] = [
    {
        "id": "qa_009",
        "question": "Which ATT&CK technique covers SMB admin share lateral movement?",
        "gold_answer": (
            "T1021.002 (SMB/Windows Admin Shares) covers lateral movement via admin shares; "
            "correlate with T1078 Valid Accounts and TA0008."
        ),
        "gold_entities": ["T1021.002", "T1078", "TA0008"],
        "gold_evidence_ids": ["ev_017", "ev_023"],
        "category": "multi_hop",
    },
    {
        "id": "qa_010",
        "question": "What is CVE-2024-3400 and why is it high priority?",
        "gold_answer": (
            "CVE-2024-3400 is a PAN-OS GlobalProtect command injection enabling unauthenticated "
            "RCE; CISA KEV listing makes it a high-priority patch target."
        ),
        "gold_entities": ["CVE-2024-3400", "PAN-OS", "CISA KEV"],
        "gold_evidence_ids": ["ev_018", "ev_030"],
        "category": "kev",
    },
    {
        "id": "qa_011",
        "question": "How is APT29 linked to the SolarWinds SUNBURST supply-chain attack?",
        "gold_answer": (
            "SolarWinds SUNBURST supply-chain compromise is attributed to APT29, involving "
            "T1195.002 and T1078 for persistence."
        ),
        "gold_entities": ["APT29", "SUNBURST", "T1195.002", "T1078"],
        "gold_evidence_ids": ["ev_019"],
        "category": "multi_hop",
    },
    {
        "id": "qa_012",
        "question": "What IDS signals indicate DNS tunneling exfiltration?",
        "gold_answer": (
            "DNS tunneling aligns with T1048; look for high-entropy subdomains, long query names, "
            "and periodic beaconing in Zeek dns.log."
        ),
        "gold_entities": ["T1048", "Zeek", "TA0010"],
        "gold_evidence_ids": ["ev_020", "ev_015"],
        "category": "ids_alert",
    },
    {
        "id": "qa_013",
        "question": "After Emotet infection, which techniques does TrickBot commonly enable?",
        "gold_answer": (
            "TrickBot commonly enables T1003 OS Credential Dumping and T1021 Remote Services "
            "after Emotet delivery."
        ),
        "gold_entities": ["TrickBot", "Emotet", "T1003", "T1021"],
        "gold_evidence_ids": ["ev_021", "ev_009"],
        "category": "multi_hop",
    },
    {
        "id": "qa_014",
        "question": "Why should stale 2019 Log4Shell remediation advice be down-ranked?",
        "gold_answer": (
            "A 2019 claim that Log4j 2.12 alone remediates CVE-2021-44228 is incomplete; "
            "current guidance requires 2.17.1+ or equivalent CISA/NVD mitigations, so EDGR "
            "temporal filtering should prefer fresher evidence."
        ),
        "gold_entities": ["CVE-2021-44228", "Log4j", "EDGR"],
        "gold_evidence_ids": ["ev_022", "ev_003", "ev_013"],
        "category": "temporal",
    },
    {
        "id": "qa_015",
        "question": "An IDS alert shows unusual SMB executable create — which ATT&CK tactic should analysts pivot to?",
        "gold_answer": (
            "Unusual SMB executable create can indicate T1021.002 lateral movement; analysts "
            "should pivot to TA0008 and validate with host telemetry."
        ),
        "gold_entities": ["T1021.002", "TA0008", "Suricata"],
        "gold_evidence_ids": ["ev_023"],
        "category": "ids_alert",
    },
    {
        "id": "qa_016",
        "question": "How does CAPEC-242 relate to Log4Shell initial access?",
        "gold_answer": (
            "CAPEC-242 Code Injection generalizes flaws enabling T1190; Log4Shell "
            "(CVE-2021-44228) is a well-known initial-access instance."
        ),
        "gold_entities": ["CAPEC-242", "T1190", "CVE-2021-44228"],
        "gold_evidence_ids": ["ev_024", "ev_003"],
        "category": "multi_hop",
    },
    {
        "id": "qa_017",
        "question": "What is ProxyLogon CVE-2021-26855 used for?",
        "gold_answer": (
            "ProxyLogon (CVE-2021-26855) is an Exchange SSRF used with related CVEs for "
            "unauthenticated RCE; Hafnium-style campaigns map to T1190 and web shells T1505.003."
        ),
        "gold_entities": ["CVE-2021-26855", "T1190", "T1505.003", "Hafnium"],
        "gold_evidence_ids": ["ev_025"],
        "category": "kev",
    },
    {
        "id": "qa_018",
        "question": "What is the CVSS score and vendor patch URL for CVE-2099-99999?",
        "gold_answer": (
            "[ABSTAIN] Queried CVE-2099-99999 is not present in the Dynamic KG or evidence; "
            "EDGR must abstain rather than invent CVSS or vendor details."
        ),
        "gold_entities": ["EDGR"],
        "gold_evidence_ids": ["ev_026"],
        "category": "ood_abstain",
        "expect_abstain": True,
    },
    {
        "id": "qa_019",
        "question": "How does UNSW-NB15 complement CIC-IDS2017 for NIDS evaluation?",
        "gold_answer": (
            "UNSW-NB15 provides nine attack families and many flow features; it complements "
            "CIC-IDS2017 when studying generalization under class imbalance."
        ),
        "gold_entities": ["UNSW-NB15", "CIC-IDS2017", "NIDS"],
        "gold_evidence_ids": ["ev_027", "ev_014"],
        "category": "dataset",
    },
    {
        "id": "qa_020",
        "question": "Which command-shell technique is often chained after phishing?",
        "gold_answer": (
            "T1059.003 Windows Command Shell is frequently chained after T1566 phishing, "
            "alongside PowerShell T1059.001 under TA0002 Execution."
        ),
        "gold_entities": ["T1059.003", "T1566", "T1059.001", "TA0002"],
        "gold_evidence_ids": ["ev_028", "ev_011"],
        "category": "multi_hop",
    },
    {
        "id": "qa_021",
        "question": "Connect Cl0p to CWE-89 through the MOVEit vulnerability path.",
        "gold_answer": (
            "Cl0p exploits CVE-2023-34362 in MOVEit Transfer, which relates to CWE-89 and "
            "CAPEC-66 — an actor→CVE→weakness multi-hop CTI path."
        ),
        "gold_entities": ["Cl0p", "CVE-2023-34362", "CWE-89", "CAPEC-66", "MOVEit"],
        "gold_evidence_ids": ["ev_029", "ev_004", "ev_008"],
        "category": "multi_hop",
    },
    {
        "id": "qa_022",
        "question": "Why should KEV-listed CVE evidence prefer fresher sources in EDGR?",
        "gold_answer": (
            "For actively exploited KEV CVEs, evidence newer than the KEV listing should "
            "outrank older speculation when EDGR applies temporal filtering."
        ),
        "gold_entities": ["CISA KEV", "EDGR"],
        "gold_evidence_ids": ["ev_030", "ev_013"],
        "category": "temporal",
    },
    {
        "id": "qa_023",
        "question": "Which Lazarus techniques follow a supply-chain foothold?",
        "gold_answer": (
            "After supply-chain footholds (T1195), Lazarus has used ingress tool transfer "
            "(T1105); detections should correlate signed-binary abuse with unusual outbound transfers."
        ),
        "gold_entities": ["Lazarus", "T1105", "T1195"],
        "gold_evidence_ids": ["ev_031", "ev_006"],
        "category": "multi_hop",
    },
    {
        "id": "qa_024",
        "question": "What tradeoff does the EDGR ρ-gate threshold θ encode?",
        "gold_answer": (
            "Lowering θ increases false rejects (abstain despite usable evidence); raising θ "
            "increases false emits (high-risk answers). θ is tuned under the Trusted Answer contract."
        ),
        "gold_entities": ["EDGR", "Hallucination"],
        "gold_evidence_ids": ["ev_032", "ev_010"],
        "category": "gate_theory",
    },
]
