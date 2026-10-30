import glob
import html
import os
import re
import sys

out = []
for fn in sorted(glob.glob('c:/Users/Admin/Desktop/figures/*.svg')):
    s = re.sub(r'<metadata.*?</metadata>', '', open(fn, encoding='utf-8', errors='replace').read(), flags=re.S)
    s = re.sub(r'</?tspan[^>]*>', '', s)
    t = [html.unescape(x).strip() for x in re.findall(r'<text[^>]*>([^<]*)</text>', s) if x.strip()]
    t = [x for x in t if not re.fullmatch(r'[A-Za-z0-9+/=]{24,}', x)]
    name = os.path.basename(fn)
    for i, x in enumerate(t, 1):
        out.append(f"{name} :{i} {x}")
open(sys.argv[1], 'w', encoding='utf-8').write("\n".join(out))
print(len(out), 'lines')
