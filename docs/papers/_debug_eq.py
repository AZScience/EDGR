import re
from pathlib import Path

import latex2mathml.converter as c
import mathml2omml
from lxml import etree

text = Path(__file__).with_name("_build_full_docx.py").read_text(encoding="utf-8")
eqs = re.findall(r'add_display_eq\(\s*doc,\s*r?"([^"]+)"', text)
eqs += re.findall(r"add_display_eq\(\s*doc,\s*r?'([^']+)'", text)
print("neq", len(eqs))
for eq in eqs:
    try:
        m = c.convert(eq)
        o = mathml2omml.convert(m)
        if any(ord(ch) < 32 and ch not in "\n\t" for ch in o):
            print("BAD OMML", eq[:120])
        wrapped = o
        if not o.strip().startswith("<"):
            wrapped = (
                '<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
                + o
                + "</m:oMath>"
            )
        elif "xmlns:m=" not in o:
            wrapped = o.replace(
                "<m:oMath>",
                '<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">',
                1,
            )
        etree.fromstring(wrapped)
    except Exception as e:
        print("FAIL", eq[:120], type(e).__name__, e)

# scan source for literal control chars introduced by patch
raw = text.encode("utf-8")
if b"\x00" in raw:
    print("NUL in source at", raw.find(b"\x00"))
# find suspicious backslash sequences in non-raw strings near numbers
for m in re.finditer(r"p=0\.664.{0,100}", text):
    print("CTX", repr(m.group(0)))
