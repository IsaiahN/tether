"""Read-only (the reviewer r267 item 1): what each life of a PLAY loaded, from each round's load_report.json, every
numeric leaf side by side (list lengths as counts), changed rows marked; plus chain.log's per-round load/write lines.
argv: PLAY dir name, rounds."""
import json
import sys

sys.dont_write_bytecode = True
P = f"C:/TETHER_RUNS/S6_2026-10-19/{sys.argv[1]}"
rounds = sys.argv[2:]


def leaves(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        yield f"{path}[len]", len(node)
    elif isinstance(node, (int, float)) and not isinstance(node, bool):
        yield path, node
    elif isinstance(node, str) and len(node) <= 24:
        yield path, node


cols = {}
for r in rounds:
    d = json.load(open(f"{P}/{r}/load_report.json", encoding="utf-8"))
    for k, v in leaves(d):
        cols.setdefault(k, {})[r] = v
print("key | " + " | ".join(rounds) + " | changed")
for k in sorted(cols):
    vals = [cols[k].get(r) for r in rounds]
    print(f"{k} | " + " | ".join(str(v) for v in vals) + (" | *" if len(set(map(str, vals))) > 1 else " |"))
print("== chain.log load/write lines")
for ln in open(f"{P}/chain.log", encoding="utf-8"):
    if any(t in ln for t in (" START seed ", " WRITE_CHECK ", "WRITE VERIFIED", " RUN rc ")):
        print(ln.rstrip()[:260])
