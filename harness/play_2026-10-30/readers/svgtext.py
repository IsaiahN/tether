import re, html, sys
sys.dont_write_bytecode = True
s = re.sub(r'<metadata.*?</metadata>', '', open(sys.argv[1], encoding='utf-8', errors='replace').read(), flags=re.S)
s = re.sub(r'</?tspan[^>]*>', '', s)
t = [html.unescape(x).strip() for x in re.findall(r'<text[^>]*>([^<]*)</text>', s) if x.strip()]
t = [x for x in t if not re.fullmatch(r'[A-Za-z0-9+/=]{24,}', x)]
with open(sys.argv[2], 'w', encoding='utf-8') as fh:
    for i, x in enumerate(t, 1):
        fh.write(f"{i} {x}\n")
