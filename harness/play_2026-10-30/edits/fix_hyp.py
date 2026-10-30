import sys
p = sys.argv[1]
src = open(p, encoding="utf-8").read()
pairs = [
('"""GQ2, GOAL HYPOTHESES (TETHER_GOAL_HYPOTHESES; the reviewer 2026-10-20 14:27 CDT). gridworld_arc_s1\n(the panel world',
 '"""GQ2, GOAL HYPOTHESES (TETHER_GOAL_HYPOTHESES; the reviewer 2026-10-20 14:27 CDT).\ngridworld_arc_s1 (the panel world'),
('  H3 ON: the routine path is reached past CAN (a routine row past the gate: routine / routine_inert /\n     routine_cut)',
 '  H3 ON: the routine path is reached past CAN (a routine row past the gate: routine /\n     routine_inert / routine_cut)'),
('        scoped += [ag._want_scope.get(sl) == ag.wants.get(sl) is not None for sl in ag._hyp["slots"]]',
 '        scoped += [ag._want_scope.get(sl) == ag.wants.get(sl) is not None\n                   for sl in ag._hyp["slots"]]'),
('    chk(not r["proposals"] or r["proposals"][0]["pick"] or "System 0" in str(r["proposals"][0]["why"]),',
 '    first = r["proposals"][0] if r["proposals"] else None\n    chk(first is None or first["pick"] or "System 0" in str(first["why"]),'),
]
for a, b in pairs:
    assert src.count(a) == 1, a[:60]
    src = src.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(src)
print("ok")
