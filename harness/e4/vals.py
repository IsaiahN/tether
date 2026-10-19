"""Value census of the rows collect.py reads (read only). argv: ledgers..."""
import collections
import json
import sys

want = {("SETTLE", "settle"): ("verdict", "status"), ("ACCEPT", "accept"): ("origin", "status"),
        ("MINT", "pull"): ("origin", "via"), ("ROUTE", "pull"): ("origin", "admitted"),
        ("PROMOTE", "promote"): ("verdict", "primitive"), ("SETTLE", "memo_sizes"): ("exempt",),
        ("ACCEPT", "rebind"): ("status",), ("SETTLE", "consolidate"): ("trigger",),
        ("PLAN", "routine_refused"): ("reason",), ("PERCEIVE", "goal_choice"): ("wants_held",),
        ("IMPORT", "ground_record"): ("level", "how")}
c = collections.defaultdict(collections.Counter)
ex = {}
for p in sys.argv[1:]:
    with open(p, encoding="utf-8") as fh:
        for ln in fh:
            r = json.loads(ln)
            e = (r.get("step"), r.get("event"))
            if r.get("event") == "routine_refused":
                e = ("PLAN", "routine_refused") if e[0] == "PLAN" else e
            if e in want:
                d = r.get("detail") or {}
                for k in want[e]:
                    c[(e, k)][json.dumps(d.get(k))[:80]] += 1
                ex.setdefault(e, (r.get("slot"), json.dumps(d)[:300]))
for k, v in c.items():
    print(k, dict(v.most_common(6)))
for e, s in ex.items():
    print("EX", e, s)
