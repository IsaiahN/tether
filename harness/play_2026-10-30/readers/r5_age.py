"""R5 read-only: per-press deltas of o21.age and o15.age from the bet rows, grouped by the action pressed.
argv: run dir. The action for a cycle-c bet is actions.tsv row index c+1 (R3's mapping), checked against
the hypothesis_test rows (before/after) printed alongside."""
import collections
import json
import os
import sys

RUN = sys.argv[1]
SLOTS = ("o21.age", "o15.age")
acts = {}
with open(os.path.join(RUN, "actions.tsv"), encoding="utf-8") as fh:
    hdr = next(fh).rstrip("\n").split("\t")
    for ln in fh:
        r = dict(zip(hdr, ln.rstrip("\n").split("\t"), strict=True))
        acts[int(r["i"])] = (r["action"], r["h0"] == r["h1"])
bets, tests = collections.defaultdict(dict), {}
with open(os.path.join(RUN, "game", "ls20.jsonl"), encoding="utf-8") as fh:
    for ln in fh:
        if '"o21.age"' not in ln and '"o15.age"' not in ln:
            continue
        r = json.loads(ln)
        d = r.get("detail") or {}
        if r.get("event") == "bet" and r.get("slot") in SLOTS:
            bets[r["cycle"]][r["slot"]] = (d.get("from_value"), d.get("actual"), d.get("bound"), d.get("alphabet"))
        if r.get("event") == "hypothesis_test" and r.get("slot") == "o21.age":
            tests[r["cycle"]] = (d.get("before"), d.get("after"))
by = {s: collections.defaultdict(list) for s in SLOTS}
print("cycle action(idx c+1) nochange | o21.age from->actual d bound alph | o15.age ... | 7j test")
for c in sorted(bets):
    a, same = acts.get(c + 1, ("?", None))
    cells = []
    for s in SLOTS:
        v = bets[c].get(s)
        if v is None:
            cells.append(f"{s} -")
            continue
        f, x, b, al = v
        dd = x - f if isinstance(f, int) and isinstance(x, int) else None
        if dd is not None:
            by[s][a].append(dd)
        cells.append(f"{s} {f}->{x} d{dd} {b} a{al}")
    print(f"c{c} {a} {same} | " + " | ".join(cells) + f" | {tests.get(c, '')}")
print("== grouped by action (the rule at tether.py:6510-6514 counts the SET of deltas per action)")
for s in SLOTS:
    for a in sorted(by[s]):
        ds = by[s][a]
        print(f"   {s} {a}: n {len(ds)} deltas {sorted(collections.Counter(ds).items())}")
    allset = {x for v in by[s].values() for x in v}
    print(f"   {s}: union of deltas {sorted(allset)}; actions seen {sorted(by[s])}")
