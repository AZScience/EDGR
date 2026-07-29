# EDGR — Accuracy note & submission files (updated)

## Are the results “accurate and good”?

**Accurate for the prototype protocol — yes.** Numbers are live, reproducible on the seed (`N=54`, `|D|=40`, `V=40`, `E=41`).

**Good as absolute SOC truth — no (and the paper says so).**

| Claim strength | Verdict |
|----------------|---------|
| EDGR > flat RAG on mean faithfulness (CI Δ excludes 0) | Supported |
| Graph ablation hurts (~−0.10) | Supported (strongest causal signal) |
| OOD abstain works on seed probes | Supported |
| Binary McNemar vs RAG significant | **Not** supported (`p=0.375`) |
| EDGR beats all stubs on auto‑F | **No** — LightRAG stub can score higher |
| Ready as Q1 SOTA paper | **No** — specialty / doctoral protocol paper |

## Latest persuasive manuscript (open this)

**`EDGR_international_paper_PERSUASIVE_SUBMIT.docx`** (~20 pp @ 1.5 spacing)

**Radical IEEE upgrade (2026-07-21):** see `IEEE_UPGRADE_NOTES.md` — N=212, TAS primary, McNemar sig., live dual panel κ≈0.92.

Logical spine:
1. Literature premise [1–12] → gap (no CTI-native pre-emit gate)
2. Method (τ/ρ + abstain) → Hypotheses H1–H4 with evidence map (Table H)
3. **Evidence A** Fig.2/Table1 — H1 vs RAG (CI)
4. **Evidence D** Fig.4 — paired Δ=+0.150; McNemar n.s. disclosed
5. **Evidence C** Table2/Fig.4 — full profile + OOD=1.0 (H2)
6. Cases — Log4Shell emit + OOD abstain
7. **Evidence B** Fig.3/Table3 — graph ablation Δ=−0.104 (H3)
8. Closing loop in Discussion (premise → mechanism → evidence → bound)

If `FULL_SUBMIT.docx` is open in Word, close it before rebuilding; regenerator writes `PERSUASIVE_SUBMIT.docx` first.

