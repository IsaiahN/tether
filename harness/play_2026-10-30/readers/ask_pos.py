"""r445 (a READ): for every 'ask' row, its place in its game's slice (step k of n, from switch.tsv's cycle_start /
steps) and whether the next cycle belongs to the same game; chosen press and the step's own chooser (repeat row).
argv: round dir."""
import json
import os
import sys

sys.dont_write_bytecode = True
O = sys.argv[1]
games = []
for ln in open(os.path.join(O, "switch.tsv"), encoding="utf-8"):
    if ln.startswith("#"):
        continue
    f = ln.rstrip("\n").split("\t")
    games.append((f[1], int(f[3]), int(f[5])))
asks, rep = [], {}
for ln in open(os.path.join(O, "stream.jsonl"), encoding="utf-8"):
    if '"event": "ask"' in ln or '"event": "repeat"' in ln:
        r = json.loads(ln)
        if r["event"] == "ask":
            asks.append(r)
        elif r["event"] == "repeat":
            rep[r["cycle"]] = r["detail"]
print(f"== {O}: ask rows {len(asks)}")
for r in asks:
    c, d = r["cycle"], r["detail"]
    g = next((x for x in games if x[1] <= c < x[1] + x[2]), None)
    k = c - g[1] + 1 if g else None
    nxt_same = g is not None and c + 1 < g[1] + g[2]
    rp = rep.get(c, {})
    print(f"  c{c} {d.get('gap_asked')} chosen {d.get('chosen')} | game {g[0] if g else None} step {k} of "
          f"{g[2] if g else None} | next cycle same game: {nxt_same} | step by {rp.get('by')} {rp.get('action')}")
