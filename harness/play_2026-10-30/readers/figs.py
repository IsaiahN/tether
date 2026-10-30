import glob
import html
import os
import re
import sys

pat = re.compile(sys.argv[1], re.I)
for fn in sorted(glob.glob("C:/Users/Admin/Desktop/figures/*.svg")):
    s = re.sub(r"<metadata.*?</metadata>", "", open(fn, encoding="utf-8", errors="replace").read(), flags=re.S)
    s = re.sub(r"</?tspan[^>]*>", "", s)
    t = [html.unescape(x).strip() for x in re.findall(r"<text[^>]*>([^<]*)</text>", s) if x.strip()]
    t = [x for x in t if not re.fullmatch(r"[A-Za-z0-9+/=]{24,}", x)]
    for i, x in enumerate(t):
        if pat.search(x):
            print(os.path.basename(fn)[:40], i, "|", " ".join(t[max(0, i - 1):i + 2])[:260])
