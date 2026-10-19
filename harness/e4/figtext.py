"""The figures' text, tspans joined and base64 stripped (the derive-first recipe). argv: figure files"""
import html
import re
import sys

for fn in sys.argv[1:]:
    with open(fn, encoding="utf-8", errors="replace") as fh:
        s = re.sub(r"<metadata.*?</metadata>", "", fh.read(), flags=re.S)
    s = re.sub(r"</?tspan[^>]*>", "", s)
    t = [html.unescape(x).strip() for x in re.findall(r"<text[^>]*>([^<]*)</text>", s) if x.strip()]
    t = [x for x in t if not re.fullmatch(r"[A-Za-z0-9+/=]{24,}", x)]
    print("=" * 20, fn)
    print(" | ".join(t))
