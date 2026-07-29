from pathlib import Path

p = Path(__file__).with_name("_build_full_docx.py")
t = p.read_text(encoding="utf-8")

# Python '\a' is BEL (0x07). Any non-raw string containing \approx was corrupted.
# Replace remaining broken sequences and BEL chars.
t = t.replace("\x07", "")
t = t.replace("$p\\approx 0$", "p approx 0")
t = t.replace("p\\approx 0", "p approx 0")
t = t.replace(
    "$p=0.664$ (n.s.); Wilcoxon on $F$ deltas significant ($p\\approx 0$))",
    "p=0.664 (n.s.); Wilcoxon on faithfulness deltas significant (p approx 0))",
)
t = t.replace(
    "$p=0.664$ (n.s.); Wilcoxon on $F$ deltas significant ($p\\approx 0$)",
    "p=0.664 (n.s.); Wilcoxon on faithfulness deltas significant (p approx 0)",
)
# After BEL strip, residual fragments like '$ppprox'
t = t.replace("$ppprox 0$", "p approx 0")
t = t.replace("ppprox 0", "p approx 0")
t = t.replace(
    r'r"F=\mathrm{clip}(0.55\cdot\mathrm{coverage}+0.45\cdot\bar{\tau}-\mathrm{penalty}),\quad H=1-F."',
    r'r"F=\mathrm{clip}(0.50\cdot\mathrm{cov}+0.35\cdot\tau_{avg}+0.15\cdot ID-p),\ H=1-F"',
)

# Guard: no control chars left except whitespace
bad = [(i, ord(ch)) for i, ch in enumerate(t) if ord(ch) < 32 and ch not in "\n\r\t"]
print("control_left", len(bad))
p.write_text(t, encoding="utf-8")
print("fixed")
