"""Totals over the E4a ledgers in e8_agg.json, games counted where each fired; plus the 3a verdicts and the invent
picks / accept examples. argv: json prefix"""
import collections
import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
tags = [t for t in d if t.startswith(sys.argv[2])]
tot, games = collections.Counter(), collections.Counter()
for t in tags:
    a = d[t]["agg"]
    for grp, kv in a.items():
        for k, v in kv.items():
            tot[f"{grp}.{k}"] += v
            if v:
                games[f"{grp}.{k}"] += 1
print("ledgers", len(tags))
for k in sorted(tot):
    print(f"  {k:32s} total {tot[k]:7d}  games {games[k]:2d}")
for t in tags:
    for e in ("invent_pick", "accept"):
        for x in d[t]["ex"].get(e, [])[:2]:
            print(e, t.split("/")[-1], json.dumps(x)[:300])
