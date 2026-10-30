"""Read-only: PLAY14 r1 against PLAY13 r1, per game (steps / first action), plus PLAY14's A1/A2/urgent counts."""
import collections
import json
import sys

sys.dont_write_bytecode = True
B = "C:/TETHER_RUNS/S6_2026-10-19"


def games(r):
    out = {}
    for ln in open(f"{B}/{r}/round_01/switch.tsv", encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if len(f) > 17 and f[0].isdigit():
            out[f[1]] = (int(f[5]), float(f[14]) if f[14] != "None" else None, f[15] == "True",
                         float(f[17]), int(f[6]), int(f[0]))
    return out


a, b = games("PLAY13"), games("PLAY14")
single13 = sorted(g for g, v in a.items() if v[0] == 1)
print("game   PLAY14 steps/first(pos)   PLAY13 steps/first(pos)")
more = fewer = same = 0
for g in sorted(b):
    s14, f14, e14, _o, _l, p14 = b[g]
    s13, f13, e13, _o2, _l2, p13 = a[g]
    more += s14 > s13
    fewer += s14 < s13
    same += s14 == s13
    print(f"{g}  {s14}/{f14}{'*' if e14 else ''} ({p14})   {s13}/{f13}{'*' if e13 else ''} ({p13})")
print(f"steps: PLAY14 {sum(v[0] for v in b.values())} vs PLAY13 {sum(v[0] for v in a.values())}; "
      f"games more {more} / fewer {fewer} / same {same}")
print("PLAY13 single-step:", single13, "-> PLAY14:", {g: b[g][:2] for g in single13})
print("PLAY14 single-step:", sorted(g for g, v in b.items() if v[0] == 1))
print("levels PLAY14:", sum(v[4] for v in b.values()))
why = collections.Counter()
c = collections.Counter()
for ln in open(f"{B}/PLAY14/round_01/stream.jsonl", encoding="utf-8"):
    try:
        r = json.loads(ln)
    except ValueError:
        continue
    e, d = r.get("event"), r.get("detail") or {}
    if e == "lookup_deferred":
        why[d.get("why")] += 1
    elif e == "walk_cut":
        c["walk_cut"] += 1
    elif e == "step_act":
        c["step_act rows"] += 1
        c["lookups_walked"] += d.get("lookups_walked", 0)
    elif e == "agent_fault":
        c["agent_fault"] += 1
    elif e == "guard_object_lost":
        c["guard_object_lost"] += 1
    for k in ("gate", "why"):
        if d.get(k) == "urgent_declined":
            c[f"urgent_declined ({e}.{k})"] += 1
print("lookup_deferred by why:", dict(why))
print(dict(c))
