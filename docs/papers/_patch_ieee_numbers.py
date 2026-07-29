from pathlib import Path

p = Path(__file__).with_name("_build_full_docx.py")
t = p.read_text(encoding="utf-8")
repls = {
    "$N=54$": "$N=104$",
    "40 evidence chunks": "60 evidence chunks",
    "$V=40$, $E=41$": "$V=46$, $E=50$",
    "mean faithfulness $0.702$": "mean faithfulness $0.599$",
    "hallucination rate $0.298$": "hallucination rate $0.401$",
    "R@$k=0.852$": "R@$k=0.809$",
    "MRR $0.803$": "MRR $0.692$",
    "$n=52$": "$n=100$",
    "0.698": "0.583",
    "0.558": "0.510",
    "[0.649,0.745]": "[0.548, 0.620]",
    "[0.509,0.607]": "[0.46, 0.54]",
    "+0.150": "+0.087",
    "[0.107,0.197]": "[0.057, 0.123]",
    "$p=0.375$": "$p=0.664$ (n.s.); Wilcoxon on $F$ deltas significant ($p\\approx 0$)",
    "$\\Delta=-0.104$": "$\\Delta=-0.088$",
    "0.594": "0.495",
    "-0.104": "-0.088",
    "0.842": "0.774",
    "0.742": "0.462",
    "approximately $0.39$": "approximately $0.83$",
    "$0.76$ for unsupported": "$0.75$ for unsupported",
    "$0.59$ for actionability": "$0.77$ for actionability",
}
n = 0
for a, b in repls.items():
    if a in t:
        t = t.replace(a, b)
        n += 1
p.write_text(t, encoding="utf-8")
print("replaced", n)
