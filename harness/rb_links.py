"""Per-game Fig 3 link, measured from the agent's own ledger; definitions fixed before reading.
argv: outdir. A link is credited only if every link above it holds (the chain is ordered by dependency)."""
import collections
import json
import os
import re
import sys

out = sys.argv[1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rb_heads
print(f"commit {rb_heads.one_commit(out)}")
TESTS = [
    # Fig 3: "the system can tell what is in front of it, and tell it apart from what was there before".
    # Identity kept (objects carried forward outnumber re-issued ones after frame 0) AND most change
    # readings resolved (a bet with prediction and actual whose channel was readable). "most" = majority.
    ("perception", lambda c, w: c["kept"] > c["births"] and c["resolved"] * 2 > c["bets"],
     "identity kept and most change readings resolved"),
    ("vocabulary", lambda c, w: sum(c[("ACCEPT", e)] for e in ("accept", "rebind", "compete")) > 0,
     "ACCEPT accept/rebind/compete"),
    ("objective", lambda c, w: w.get("composed", 0) > 0, "want by=composed (its own goal)"),
    # Fig 3: "a route to THAT objective": a plan adopted on a slot the agent itself chose as its goal.
    ("planning", lambda c, w: c["aimed_plans"] > 0, "a plan adopted on its own goal's slot"),
    ("learn", lambda c, w: c[("PROMOTE", "promote")] > 0 and c[("SETTLE", "settle")] > 0,
     "SETTLE settle + PROMOTE promote"),
]


def levels_of(path: str) -> str:
    if not os.path.exists(path):
        return "?"
    txt = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r'"levels": "(.*?)",\s*\n', txt)
    if not m:
        return "?"
    entries = len(re.findall(r"'level': ", m.group(1)))
    adv = re.search(r"'advanced': (True|False)", m.group(1))
    return f"{entries}{'+' if adv and adv.group(1) == 'True' else ''}"


print(f"{'game':6} {'lvl':>4} {'link reached':12} {'present':44} {'cyc':>4}  first missing")
for f in sorted(x for x in os.listdir(out) if x.endswith(".jsonl")):
    g = f[:-6]
    c, w, cyc, goals = collections.Counter(), collections.Counter(), 0, set()
    for line in open(os.path.join(out, f), encoding="utf-8"):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        c[(r.get("step"), r.get("event"))] += 1
        cyc = max(cyc, r.get("cycle") or 0)
        d, ev = r.get("detail") or {}, r.get("event")
        if ev == "want":
            w[str(d.get("by"))] += 1
            if d.get("by") == "composed":
                goals.add(r.get("slot"))
        elif ev == "matches" and (r.get("cycle") or 0) > 0:
            for k, v in (d.get("routes") or {}).items():
                c["births" if k == "birth" else "kept"] += v
        elif ev == "bet":
            c["bets"] += 1
            c["resolved"] += "predicted" in d and "actual" in d and d.get("cause") != "channel_closed"
        elif ev == "routine" and r.get("step") == "PLAN" and r.get("slot") in goals:
            c["aimed_plans"] += 1
    held = [name for name, t, _ in TESTS if t(c, w)]
    reached = "none"
    for name, t, _ in TESTS:
        if not t(c, w):
            break
        reached = name
    nxt = next((d for _, t, d in TESTS if not t(c, w)), "-")
    print(f"{g:6} {levels_of(os.path.join(out, g + '.out')):>4} {reached:12} {','.join(held):44} "
          f"{cyc:>4}  {nxt}")
