"""R1, THE GRADED-SURPRISE READ (the reviewer 2026-10-21 16:48). Over one game's ledger: every
transition bet that MISSED (mass > 0, not suspended), classed by where its actual value sits
against the slot's own observed values before it (every earlier bet's from_value and actual, and
this bet's from_value):
  seen     the value was observed on this slot before
  inside   unseen, numeric, within the slot's observed min..max (per component for a vector)
  outside  unseen, numeric, beyond that range
  unseen   unseen, not numeric (no range to be inside)
  gone     the object vanished under the bet
Then, per class, what the same (cycle, slot) did: the route bin, whether the library was asked
(ROUTE reach) or owed (budget_owed), and what came of it: pull, ACCEPT (rebind / compete / accept),
MINT mint (a find), want_only, park.   argv: ledger.jsonl [...]"""
import collections
import json
import sys

CLASSES = ("seen", "inside", "outside", "unseen", "gone")


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def vec(v):
    return isinstance(v, list) and v and all(num(x) for x in v)


def klass(a, prior, gone):
    if gone:
        return "gone"
    k = json.dumps(a, sort_keys=True)
    if k in prior["keys"]:
        return "seen"
    vals = prior["vals"]
    if num(a):
        ns = [x for x in vals if num(x)]
        if not ns:
            return "unseen"
        return "inside" if min(ns) <= a <= max(ns) else "outside"
    if vec(a):
        vs = [x for x in vals if vec(x) and len(x) == len(a)]
        if not vs:
            return "unseen"
        return "inside" if all(min(v[i] for v in vs) <= a[i] <= max(v[i] for v in vs)
                               for i in range(len(a))) else "outside"
    return "unseen"


def note(prior, v):
    k = json.dumps(v, sort_keys=True)
    if k not in prior["keys"]:
        prior["keys"].add(k)
        prior["vals"].append(v)


def read(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                rows.append(json.loads(ln))
    bets = collections.defaultdict(list)      # cycle -> [(slot, detail)]
    after = collections.defaultdict(lambda: collections.defaultdict(list))  # (cycle, slot) -> events
    route = {}
    for r in rows:
        c, s, e, d = r.get("cycle"), r.get("slot"), r.get("event"), r.get("detail") or {}
        st = r.get("step")
        if st == "PERCEIVE" and e == "bet" and d.get("channel") is not None:
            bets[c].append((s, d))
        elif st == "ROUTE" and e == "route":
            route[(c, s)] = d.get("bin")
        elif (st, e) in (("ROUTE", "reach"), ("ROUTE", "budget_owed"), ("MINT", "mint"),
                         ("MINT", "want_only"), ("MINT", "park"), ("MINT", "derived_asked")) \
                or e == "pull" or st == "ACCEPT":
            after[(c, s)][e if st != "ACCEPT" else "ACCEPT:" + e].append(d)
    prior = collections.defaultdict(lambda: {"keys": set(), "vals": []})
    tab = {k: collections.Counter() for k in CLASSES}
    n_bets = n_susp = 0
    for c in sorted(bets):
        for s, d in bets[c]:
            n_bets += 1
            if d.get("suspended"):
                n_susp += 1
                continue
            p = prior[s]
            note(p, d.get("from_value"))
            if (d.get("mass") or 0.0) > 0.0:
                k = klass(d.get("actual"), p, bool(d.get("gone")))
                t = tab[k]
                t["miss"] += 1
                t["bin:" + str(route.get((c, s)))] += 1
                ev = after.get((c, s), {})
                if "reach" in ev:
                    t["asked"] += 1
                if "budget_owed" in ev:
                    t["owed"] += 1
                for name in ("pull", "mint", "want_only", "park", "ACCEPT:rebind",
                             "ACCEPT:compete", "ACCEPT:accept", "ACCEPT:retro"):
                    if name in ev:
                        t[name] += 1
                if "pull" in ev or "mint" in ev or any(x.startswith("ACCEPT:") for x in ev):
                    t["pull|accept|find"] += 1
        for s, d in bets[c]:                  # this cycle's actuals join the range after it
            if not d.get("suspended") and not d.get("gone"):
                note(prior[s], d.get("actual"))
    return n_bets, n_susp, tab


for path in sys.argv[1:]:
    n_bets, n_susp, tab = read(path)
    print(f"== {path}: {n_bets} transition bets, {n_susp} suspended")
    keys = sorted({k for t in tab.values() for k in t})
    keys = ["miss"] + [k for k in keys if k != "miss"]
    print("class    " + " ".join(f"{k:>16}" for k in keys))
    for c in CLASSES:
        print(f"{c:8} " + " ".join(f"{tab[c][k]:>16}" for k in keys))
