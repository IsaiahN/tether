"""Numbered text lines of named figures (tspans joined, metadata stripped). argv: dir, then figure-name fragments."""
import glob
import html
import re
import sys

sys.dont_write_bytecode = True
D = sys.argv[1]
for frag in sys.argv[2:]:
    for fn in sorted(glob.glob(f"{D}/*{frag}*.svg")):
        s = re.sub(r"<metadata.*?</metadata>", "", open(fn, encoding="utf-8", errors="replace").read(), flags=re.S)
        s = re.sub(r"</?tspan[^>]*>", "", s)
        t = [html.unescape(x).strip() for x in re.findall(r"<text[^>]*>([^<]*)</text>", s) if x.strip()]
        t = [x for x in t if not re.fullmatch(r"[A-Za-z0-9+/=]{24,}", x)]
        print("=" * 10, fn.rsplit("/", 1)[-1])
        for i, x in enumerate(t):
            print(i, x)
