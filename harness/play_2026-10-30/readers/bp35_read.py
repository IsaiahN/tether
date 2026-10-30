"""Read-only (the reviewer r267 item 2): one game's step-1 rows across rounds -- the PLAN goal_hypotheses row
(wall_s, candidates, group_n, open, checked, self_moving), the MINT parks (seen, tried, exhausted, verdict), row
counts by (step, event) for the lookup / reach / route / plan families, and routed slots. argv: PLAY, game, rounds."""
import collections
import json
import sys

sys.dont_write_bytecode = True
P, G = f"C:/TETHER_RUNS/S6_2026-10-19/{sys.argv[1]}", sys.argv[2]
for rnd in sys.argv[3:]:
    c0 = first = pos = None
    for ln in open(f"{P}/{rnd}/switch.tsv", encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if len(f) > 14 and f[0].isdigit() and f[1] == G:
            pos, c0, first = int(f[0]), int(f[3]), f[14]
    if c0 is None:
        print(f"== {rnd}: {G} not in switch.tsv")
        continue
    ev, hyp, parks, plan_ev = collections.Counter(), [], [], collections.Counter()
    for ln in open(f"{P}/{rnd}/stream.jsonl", encoding="utf-8"):
        if f'"cycle": {c0},' not in ln:
            continue
        try:
            r = json.loads(ln)
        except ValueError:
            continue
        if r.get("cycle") != c0:
            continue
        e, d, st = r.get("event"), r.get("detail") or {}, r.get("step")
        ev[(st, e)] += 1
        if st == "PLAN":
            plan_ev[e] += 1
        if e == "goal_hypotheses":
            hyp.append({k: d.get(k) for k in ("wall_s", "candidates", "group_n", "open", "checked", "budget",
                                               "pick_rank", "source")}
                       | {"self_moving": len(d.get("self_moving") or [])})
        elif e == "park":
            parks.append((r.get("slot"), d.get("candidates_seen"), d.get("candidates_tried"),
                          d.get("budget_exhausted"),
                          d.get("verdict"), d.get("wall_s")))
    fam = {k: v for k, v in ev.items() if any(t in str(k[1]) for t in ("lookup", "reach", "walk", "index", "tier"))}
    route_rows = sum(v for (st, _e), v in ev.items() if st == "ROUTE")
    print(f"== {rnd}: {G} position {pos} c{c0} first {first}; rows {sum(ev.values())}; ROUTE rows {route_rows}")
    print(f"   goal_hypotheses: {hyp or 'NONE'}")
    print(f"   PLAN events: {dict(plan_ev)}")
    print(f"   parks: {parks}")
    print(f"   lookup/reach/walk/index/tier rows: {dict(sorted(fam.items(), key=str))}")
    print(f"   rows by step: {dict(collections.Counter(st for st, _e in ev.elements()))}")
