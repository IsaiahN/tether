"""THE GOAL-PAIR REPAIR, TETHER_RELATION_SET (the reviewer 2026-10-11 13:40 CDT): under the arm two
pair slots of the same RELATION read the same quantity on the goal side, as the mint already takes
them; different relations, pair vs non-pair and a cross-slot lag stay refused in both states.

  g1 OFF: "o0.dist_o3 < o0.dist_o4" refused (the must-fail that proves the gate);
  g2 ON: it compiles to below<o0.dist_o4> on o0.dist_o3 -- the spelling the mint reaches -- and
     holds at gaps 1 vs 3, not at 3 vs 1;
  g3 ON: "o0.dist_o3 == o1.dist_o4" compiles to same<o1.dist_o4> and holds at 2 vs 2, not 2 vs 3;
     linked with nothing moving the want stays on o0.dist_o3; a derived slot moves when ANY of its
     SOURCES is contingent (13:49): o1 moving -> o1.dist_o4 (g3a); o3, a partner, moving ->
     o0.dist_o3 (g3b), and on the mirrored spelling too (g3b', the must-fail for owner-only);
  g4 refused in BOTH states: dist vs drow, dist vs row, inside vs touches.

    python test_relation_goalpair.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
import compile_term as C
from test_goal_condition import _agent
ag = _agent()
atoms = {a.name: a for a in ag.gamma.atoms}
def comp(t):
    c = C.compile_candidate({"condition": t}, atoms)
    if not isinstance(c, C.Compiled):
        return c.reason
    return [c.slot, [a.name for a in c.term.atoms], c.operand]
out = {"near": comp("o0.dist_o3 < o0.dist_o4"), "same": comp("o0.dist_o3 == o1.dist_o4"),
       "refused": [comp(t) for t in ("o0.dist_o3 < o0.drow_o4", "o0.dist_o3 < o0.row",
                                     "o0.inside_o3 == o0.touches_o4")]}
n = C.compile_candidate({"condition": "o0.dist_o3 < o0.dist_o4"}, atoms)
s = C.compile_candidate({"condition": "o0.dist_o3 == o1.dist_o4"}, atoms)
if isinstance(n, C.Compiled):
    out["near_scene"] = [C.run(n, {"o0.dist_o3": 1, "o0.dist_o4": 3}),
                         C.run(n, {"o0.dist_o3": 3, "o0.dist_o4": 1})]
if isinstance(s, C.Compiled):
    out["same_scene"] = [C.run(s, {"o0.dist_o3": 2, "o1.dist_o4": 2}),
                         C.run(s, {"o0.dist_o3": 2, "o1.dist_o4": 3})]
    s2 = C.compile_candidate({"condition": "o1.dist_o4 == o0.dist_o3"}, atoms)
    link = {}
    for label, moving, cond in (("none", (), s), ("o1", ("o1.row",), s), ("o3", ("o3.row",), s),
                                ("o3_mirror", ("o3.row",), s2)):
        ag.agency = type(ag.agency)()
        for sl in moving:
            ag.agency.note("A", {sl}, sorted(ag.slots))
            ag.agency.note("B", set(), sorted(ag.slots))
        for sl in ("o0.dist_o3", "o1.dist_o4"):
            ag.wants.pop(sl, None); ag._want_terms.pop(sl, None); ag._want_scope.pop(sl, None)
        ag._goal_links.clear()
        ag._link_goal("gp-" + label, cond)
        link[label] = sorted(sl for sl in ("o0.dist_o3", "o1.dist_o4") if sl in ag._want_scope)
    out["link"] = link
print(json.dumps(out))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_RELATION_SET="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=os.path.dirname(os.path.abspath(__file__)), timeout=300)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    off = _run(False)
    assert isinstance(off["near"], str) and isinstance(off["same"], str), off
    print(f"  g1 OFF: refused -- {off['near']!r}")
    assert all(isinstance(r, str) for r in off["refused"]), off
    on = _run(True)
    assert on["near"] == ["o0.dist_o3", ["below"], "o0.dist_o4"], on
    assert on["near_scene"] == [True, False], on
    print(f"  g2 ON: near/far -> below<o0.dist_o4> on o0.dist_o3; scene {on['near_scene']}")
    assert on["same"] == ["o0.dist_o3", ["same"], "o1.dist_o4"], on
    assert on["same_scene"] == [True, False], on
    # g3a the OWNER of o1.dist_o4 moves -> o1's side; g3b o3, a PARTNER, moves -> o0.dist_o3 (as
    # written); g3b' the mirrored spelling with o3 moving -> o0.dist_o3 by its SOURCES, where an
    # owner-only test would have kept o1.dist_o4 -- the must-fail for owner-only (13:49 CDT)
    assert on["link"] == {"none": ["o0.dist_o3"], "o1": ["o1.dist_o4"], "o3": ["o0.dist_o3"],
                          "o3_mirror": ["o0.dist_o3"]}, on
    print(f"  g3 ON: same-relation-as -> same<o1.dist_o4>; scene {on['same_scene']}; "
          f"link {on['link']}")
    assert all(isinstance(r, str) and "different quantities" in r for r in on["refused"]), on
    print(f"  g4 both states refused: dist/drow, dist/row, inside/touches -- {on['refused'][0]!r}")
    print("relation goalpair: OK")
