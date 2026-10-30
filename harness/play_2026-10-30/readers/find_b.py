"""Read-only: print every Drive post (create_file textContent) and Drive read whose text holds the
needle, from this session's transcript. argv: transcript, needle, out."""
import json
import sys

sys.dont_write_bytecode = True
src, needle, out = sys.argv[1], sys.argv[2], sys.argv[3]
hits = []


def walk(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if isinstance(v, str) and needle in v:
                hits.append((k, v))
            else:
                walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)


with open(src, encoding="utf-8") as fh:
    for line in fh:
        if needle in line:
            try:
                walk(json.loads(line))
            except ValueError:
                pass
seen = set()
with open(out, "w", encoding="utf-8") as fo:
    for k, v in hits:
        if v in seen:
            continue
        seen.add(v)
        fo.write(f"===== {k} ({len(v)} chars)\n{v}\n")
print(len(hits), len(seen))
