"""Two k2_force.py results compared (the reviewer 2026-10-19 10:45 (d), (e)). READ ONLY. T2 (the slice of the output
list: keys, order and weights), the tier sizes, the whole output list, and the pair counts, each EQUAL or DIFFERS,
with the differing pair rows printed.
argv: force_a.json force_b.json"""
import json
import sys

with open(sys.argv[1], encoding="utf-8") as fh:
    a = json.load(fh)
with open(sys.argv[2], encoding="utf-8") as fh:
    b = json.load(fh)
print("RUNS", f"{a['mode']}/{a['variant']}", "vs", f"{b['mode']}/{b['variant']}", sep="\t")
for k in ("t2", "sizes", "out", "pair_counts"):
    print(k.upper(), "EQUAL" if a[k] == b[k] else "DIFFERS", sep="\t")
print("T2_A", json.dumps(a["t2"]), sep="\t")
print("T2_B", json.dumps(b["t2"]), sep="\t")
pa = {json.dumps(r[:2]): r[2:] for r in a["pair_counts"]}
pb = {json.dumps(r[:2]): r[2:] for r in b["pair_counts"]}
for k in sorted(set(pa) | set(pb)):
    if pa.get(k) != pb.get(k):
        print("PAIR_DIFF", k[:160], "a", pa.get(k), "b", pb.get(k), sep="\t")
