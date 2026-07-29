"""
Wave-4 IEEE scale-up: programmatic CTI graph + stratified QA.
Targets: N≥200 QA, |D|≥100 evidence, KG V≥100 / E≥150 (combined with prior waves).
"""

from __future__ import annotations

from typing import Any

# Real-ish ATT&CK / CVE building blocks for reproducible expansion
_TECHS = [
    ("T1047", "Windows Management Instrumentation", "TA0002"),
    ("T1053", "Scheduled Task/Job", "TA0003"),
    ("T1055", "Process Injection", "TA0005"),
    ("T1082", "System Information Discovery", "TA0007"),
    ("T1083", "File and Directory Discovery", "TA0007"),
    ("T1105", "Ingress Tool Transfer", "TA0011"),
    ("T1110", "Brute Force", "TA0006"),
    ("T1218", "System Binary Proxy Execution", "TA0005"),
    ("T1490", "Inhibit System Recovery", "TA0040"),
    ("T1543", "Create or Modify System Process", "TA0003"),
    ("T1547", "Boot or Logon Autostart Execution", "TA0003"),
    ("T1550", "Use Alternate Authentication Material", "TA0005"),
    ("T1562", "Impair Defenses", "TA0005"),
    ("T1570", "Lateral Tool Transfer", "TA0008"),
    ("T1573", "Encrypted Channel", "TA0011"),
    ("T1588", "Obtain Capabilities", "TA0042"),
    ("T1595", "Active Scanning", "TA0043"),
    ("T1608", "Stage Capabilities", "TA0042"),
    ("T1620", "Reflective Code Loading", "TA0005"),
    ("T1651", "Cloud Administration Command", "TA0002"),
]

_CVES = [
    ("CVE-2020-1472", "Zerologon", "T1550"),
    ("CVE-2021-34527", "PrintNightmare", "T1218"),
    ("CVE-2021-40444", "MSHTML engine", "T1203"),
    ("CVE-2022-30190", "Follina", "T1218"),
    ("CVE-2022-41040", "ProxyNotShell", "T1190"),
    ("CVE-2022-41082", "Exchange RCE companion", "T1190"),
    ("CVE-2023-23397", "Outlook NTLM", "T1550"),
    ("CVE-2023-28252", "CLFS privilege", "T1068"),
    ("CVE-2023-36884", "Office HTML", "T1203"),
    ("CVE-2024-21412", "Internet Shortcut SmartScreen", "T1204"),
    ("CVE-2024-30051", "Windows DWM", "T1068"),
    ("CVE-2024-38063", "IPv6 RCE", "T1190"),
]

_ACTORS = [
    ("APT28", ["T1566", "T1078", "T1059"]),
    ("APT41", ["T1190", "T1055", "T1105"]),
    ("FIN7", ["T1566", "T1059", "T1003"]),
    ("Sandworm", ["T1490", "T1486", "T1562"]),
    ("Wizard Spider", ["T1566", "T1003", "T1486"]),
    ("Volt Typhoon", ["T1078", "T1047", "T1021.002"]),
]

_MALWARE = [
    ("Cobalt Strike", ["T1055", "T1105", "T1573"]),
    ("Emotet", ["T1566", "T1059", "T1105"]),
    ("QakBot", ["T1566.001", "T1059", "T1003"]),
    ("TrickBot", ["T1003", "T1055", "T1105"]),
    ("BlackCat", ["T1486", "T1490", "T1489"]),
    ("LockBit", ["T1486", "T1490", "T1021"]),
]


def build_wave4() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    qa: list[dict[str, Any]] = []

    seen_n: set[str] = set()

    def add_node(nid: str, label: str, ntype: str, ts: str, rel: float, **props: Any) -> None:
        if nid in seen_n:
            return
        seen_n.add(nid)
        nodes.append(
            {
                "id": nid,
                "label": label,
                "type": ntype,
                "timestamp": ts,
                "reliability": rel,
                "properties": props,
            }
        )

    # Tactics referenced
    for tid, name in [
        ("TA0002", "Execution"),
        ("TA0003", "Persistence"),
        ("TA0005", "Defense Evasion"),
        ("TA0006", "Credential Access"),
        ("TA0007", "Discovery"),
        ("TA0011", "Command and Control"),
        ("TA0040", "Impact"),
        ("TA0042", "Resource Development"),
        ("TA0043", "Reconnaissance"),
    ]:
        add_node(tid, name, "tactic", "2024-01-01", 0.95)

    for tech, label, tactic in _TECHS:
        add_node(tech, label, "technique", "2024-06-01", 0.93, tactic=tactic)
        edges.append(
            {
                "source": tech,
                "target": tactic,
                "relation": "belongs_to",
                "weight": 1.0,
                "timestamp": "2024-06-01",
            }
        )
        eid = f"ev_w4_{tech.replace('.', '_')}"
        evidence.append(
            {
                "id": eid,
                "content": (
                    f"MITRE ATT&CK technique {tech} ({label}) is commonly mapped under {tactic}. "
                    f"SOC detections should correlate process, network, and identity telemetry for {tech}."
                ),
                "source": "MITRE ATT&CK",
                "entities": [tech, tactic, label.split()[0]],
                "timestamp": "2024-06-01",
                "reliability": 0.94,
                "type": "technique",
            }
        )
        qa.append(
            {
                "id": f"qa_w4_tech_{tech.replace('.', '_')}",
                "question": f"What is ATT&CK technique {tech} and which tactic does it belong to?",
                "gold_answer": f"{tech} ({label}) belongs to tactic {tactic}.",
                "gold_entities": [tech, tactic],
                "gold_evidence_ids": [eid],
                "category": "core",
                "expect_abstain": False,
            }
        )

    # Extra technique used by CVEs
    add_node("T1203", "Exploitation for Client Execution", "technique", "2024-01-01", 0.92, tactic="TA0002")
    add_node("T1068", "Exploitation for Privilege Escalation", "technique", "2024-01-01", 0.92, tactic="TA0004")
    add_node("TA0004", "Privilege Escalation", "tactic", "2024-01-01", 0.95)
    add_node("T1204", "User Execution", "technique", "2024-01-01", 0.92, tactic="TA0002")
    add_node("T1489", "Service Stop", "technique", "2024-01-01", 0.9, tactic="TA0040")
    edges.append(
        {"source": "T1203", "target": "TA0002", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-01-01"}
    )
    edges.append(
        {"source": "T1068", "target": "TA0004", "relation": "belongs_to", "weight": 1.0, "timestamp": "2024-01-01"}
    )

    for cve, label, tech in _CVES:
        add_node(cve, label, "cve", "2023-01-01", 0.96, kev=True)
        if tech not in seen_n:
            add_node(tech, tech, "technique", "2024-01-01", 0.9)
        edges.append(
            {
                "source": cve,
                "target": tech,
                "relation": "enables",
                "weight": 0.9,
                "timestamp": "2023-01-01",
            }
        )
        eid = f"ev_w4_{cve.replace('-', '_')}"
        evidence.append(
            {
                "id": eid,
                "content": (
                    f"{cve} ({label}) is a high-priority vulnerability frequently linked to ATT&CK "
                    f"{tech}. CISA KEV-style prioritization treats actively exploited cases as urgent. "
                    f"Mitigations include vendor patches and compensating network controls."
                ),
                "source": "NVD/CVE",
                "entities": [cve, label, tech, "CISA KEV"],
                "timestamp": "2023-06-01",
                "reliability": 0.96,
                "type": "cve",
            }
        )
        qa.append(
            {
                "id": f"qa_w4_{cve.replace('-', '_')}",
                "question": f"What is {cve} ({label}) and which ATT&CK technique does it enable?",
                "gold_answer": f"{cve} ({label}) enables {tech}; prioritize patching under KEV-style urgency.",
                "gold_entities": [cve, tech],
                "gold_evidence_ids": [eid],
                "category": "kev",
                "expect_abstain": False,
            }
        )
        qa.append(
            {
                "id": f"qa_w4_mh_{cve.replace('-', '_')}",
                "question": f"How should SOC hunt activity after exploitation of {cve}?",
                "gold_answer": (
                    f"After {cve}, hunt for behaviors mapped to {tech} and correlated identity/network anomalies; "
                    f"prefer evidence-backed ATT&CK mapping over unverified attribution."
                ),
                "gold_entities": [cve, tech],
                "gold_evidence_ids": [eid],
                "category": "multi_hop",
                "expect_abstain": False,
            }
        )

    for actor, techs in _ACTORS:
        add_node(actor, actor, "actor", "2024-03-01", 0.9)
        for tech in techs:
            if tech not in seen_n:
                add_node(tech, tech, "technique", "2024-01-01", 0.9)
            edges.append(
                {
                    "source": actor,
                    "target": tech,
                    "relation": "uses",
                    "weight": 0.85,
                    "timestamp": "2024-03-01",
                }
            )
        eid = f"ev_w4_actor_{actor.replace(' ', '_')}"
        evidence.append(
            {
                "id": eid,
                "content": (
                    f"{actor} campaigns have been associated with techniques {', '.join(techs)}. "
                    f"Use technique-first hunting; avoid over-claiming attribution without multiple sources."
                ),
                "source": "CISA/CTI",
                "entities": [actor, *techs],
                "timestamp": "2024-03-01",
                "reliability": 0.9,
                "type": "actor",
            }
        )
        qa.append(
            {
                "id": f"qa_w4_actor_{actor.replace(' ', '_')}",
                "question": f"Which ATT&CK techniques are commonly linked to {actor} in the seeded CTI graph?",
                "gold_answer": f"{actor} is linked to {', '.join(techs)} in the seeded knowledge graph.",
                "gold_entities": [actor, *techs],
                "gold_evidence_ids": [eid],
                "category": "multi_hop",
                "expect_abstain": False,
            }
        )

    for mal, techs in _MALWARE:
        add_node(mal, mal, "malware", "2024-02-01", 0.88)
        for tech in techs:
            if tech not in seen_n:
                add_node(tech, tech, "technique", "2024-01-01", 0.9)
            edges.append(
                {
                    "source": mal,
                    "target": tech,
                    "relation": "uses",
                    "weight": 0.84,
                    "timestamp": "2024-02-01",
                }
            )
        eid = f"ev_w4_mal_{mal.replace(' ', '_')}"
        evidence.append(
            {
                "id": eid,
                "content": (
                    f"{mal} malware families frequently exhibit {', '.join(techs)}. "
                    f"NIDS/EDR correlations should focus on those techniques before naming the family alone."
                ),
                "source": "CISA/CTI",
                "entities": [mal, *techs],
                "timestamp": "2024-02-01",
                "reliability": 0.89,
                "type": "malware",
            }
        )
        qa.append(
            {
                "id": f"qa_w4_mal_{mal.replace(' ', '_')}",
                "question": f"What techniques are associated with {mal} in the CTI seed?",
                "gold_answer": f"{mal} is associated with {', '.join(techs)}.",
                "gold_entities": [mal, *techs],
                "gold_evidence_ids": [eid],
                "category": "multi_hop",
                "expect_abstain": False,
            }
        )

    # IDS / temporal / gate / OOD — expanded OOD bank (safety-critical stratum)
    ood_list = [f"CVE-2099-{70000+i}" for i in range(1, 41)]
    for i, cve in enumerate(ood_list):
        qa.append(
            {
                "id": f"qa_w4_ood_{i+1:02d}",
                "question": f"Give CVSS, exploit PoC, and vendor advisory URL for {cve}.",
                "gold_answer": f"[ABSTAIN] {cve} is not in the Dynamic KG or evidence; EDGR must abstain.",
                "gold_entities": ["EDGR"],
                "gold_evidence_ids": [],
                "category": "ood_abstain",
                "expect_abstain": True,
            }
        )

    evidence.append(
        {
            "id": "ev_w4_ids_01",
            "content": (
                "Suricata alert fusion: when brute-force SSH alerts co-occur with T1110 and unusual "
                "T1078 logins, escalate before closing as noise."
            ),
            "source": "IDS/NIDS Guide",
            "entities": ["Suricata", "T1110", "T1078", "NIDS"],
            "timestamp": "2025-01-15",
            "reliability": 0.85,
            "type": "alert",
        }
    )
    qa.append(
        {
            "id": "qa_w4_ids_01",
            "question": "How should SOC treat Suricata SSH brute-force with anomalous logins?",
            "gold_answer": (
                "Correlate Suricata brute-force with T1110 and T1078 before closing as noise; escalate when both fire."
            ),
            "gold_entities": ["Suricata", "T1110", "T1078"],
            "gold_evidence_ids": ["ev_w4_ids_01"],
            "category": "ids_alert",
            "expect_abstain": False,
        }
    )

    evidence.append(
        {
            "id": "ev_w4_gate_01",
            "content": (
                "Trusted Answer evaluation should report both lexical faithfulness and safety outcomes: "
                "correct abstain on unsupported CVEs, and low invented-identifier rate."
            ),
            "source": "Research Note",
            "entities": ["EDGR", "Hallucination"],
            "timestamp": "2025-07-01",
            "reliability": 0.9,
            "type": "concept",
        }
    )
    qa.append(
        {
            "id": "qa_w4_gate_01",
            "question": "Beyond lexical faithfulness, what safety outcomes should CTI assistants report?",
            "gold_answer": (
                "Report correct abstain on unsupported CVEs and low invented-identifier rate under a Trusted Answer contract."
            ),
            "gold_entities": ["EDGR", "Hallucination"],
            "gold_evidence_ids": ["ev_w4_gate_01", "ev_050"],
            "category": "gate_theory",
            "expect_abstain": False,
        }
    )

    # Cross-link high-value edges for denser graph
    for a, b in [
        ("APT28", "Emotet"),
        ("FIN7", "Cobalt Strike"),
        ("Wizard Spider", "TrickBot"),
        ("Wizard Spider", "LockBit"),
        ("Sandworm", "BlackCat"),
        ("Volt Typhoon", "T1047"),
        ("CVE-2021-34527", "T1218"),
        ("CVE-2022-30190", "T1218"),
    ]:
        if a in seen_n and b in seen_n:
            edges.append(
                {
                    "source": a,
                    "target": b,
                    "relation": "related_to",
                    "weight": 0.7,
                    "timestamp": "2024-08-01",
                }
            )

    return nodes, edges, evidence, qa


WAVE4_NODES, WAVE4_EDGES, WAVE4_EVIDENCE, WAVE4_QA_HAND = build_wave4()
