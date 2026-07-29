"""Research defaults for EDGR / IDS–CTI experiments."""

# Final trusted-evidence budget after EDGR ranking/risk gate.
# Rationale for this thesis demo (seed KG + 16 evidence chunks, QA gold usually 1–2 ids,
# queries often mention 2–4 CTI entities):
#   k=3  — high precision, may miss supporting TTP/context passages
#   k=5  — recommended: enough multi-hop context, still small enough to keep F high
#   k≥8  — more noise into G(q,R); hallucination risk rises on thin CTI answers
# Candidate pools inside EDGR still use larger multipliers (2k–3k); only the emit set is k.
DEFAULT_TOP_K = 5
RECOMMENDED_TOP_K_CHOICES = (3, 5, 8)
