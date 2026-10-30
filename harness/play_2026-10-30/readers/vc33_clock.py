"""Read-only: per slot, its change at each cycle up to c10 (bet rows: from_value -> actual), the action taken that
cycle; list slots that changed on EVERY cycle, by the same mean delta per action. argv: ledger"""
import collections, json, sys
rows = [json.loads(x) for x in open(sys.argv[1], encoding="utf-8") if x.strip()]
act = {r["cycle"]: r["detail"].get("action") for r in rows if r["event"] == "repeat"}
ch = collections.defaultdict(dict)   # slot -> cycle -> delta
for r in rows:
    d = r["detail"]
    if r["event"] == "bet" and r["cycle"] <= 10 and isinstance(d.get("actual"), int) \
            and isinstance(d.get("from_value"), int):
        ch[r["slot"]][r["cycle"]] = d["actual"] - d["from_value"]
cyc = sorted(c for c in act if c <= 10)
print("cycles", cyc, "actions", [act[c] for c in cyc])
clock = []
for sl, dd in sorted(ch.items()):
    if all(dd.get(c, 0) != 0 for c in cyc if c in dd) and len(dd) >= len(cyc) - 1:
        per = collections.defaultdict(list)
        for c, v in dd.items():
            per[act.get(c)].append(v)
        means = {a: round(sum(v) / len(v), 3) for a, v in per.items()}
        if len(set(means.values())) == 1:
            clock.append((sl, means, len(dd)))
print("slots moved on every read cycle by one mean delta per action:", len(clock))
for c in clock[:40]:
    print(" ", c)
