import glob, html, re, sys
sys.dont_write_bytecode = True
for fn in sorted(glob.glob('c:/Users/Admin/Desktop/figures/*.svg')):
    s = re.sub(r'<metadata.*?</metadata>', '', open(fn, encoding='utf-8', errors='replace').read(), flags=re.S)
    s = re.sub(r'</?tspan[^>]*>', '', s)
    t = [html.unescape(x).strip() for x in re.findall(r'<text[^>]*>([^<]*)</text>', s) if x.strip()]
    t = [x for x in t if not re.fullmatch(r'[A-Za-z0-9+/=]{24,}', x)]
    name = __import__('os').path.basename(fn)
    for i, x in enumerate(t, 1):
        print(f"{name}:{i}: {x}")
