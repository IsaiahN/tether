"""b-0 amended (TETHER_GOAL_LINK; the reviewer 2026-10-11 08:34Z): a subject-scoped want on an
ORDERED slot is scored by how far it is from holding -- objective_gap over its domain's span
(Fig 12 :112, "progress is a subtraction") -- so the Sec 13.4 selector can see it shrink. A
comparable-only slot stays 0/1; a view keeps its group fraction. Data: the recorded
gridworld_arc_s1 history at c89, the pair linked (o0.col wants o3's column).

  a. approached over three steps (distance 3, 2, 1) the want QUALIFIES before it holds, and
     _goal_target yields the next step toward o3.col;
  b. drifted away from (1, 2, 3) it does not qualify: rose;
  c. R = 0 exactly at satisfaction;
  d. a comparable-only subject want (o0.colour) is still 0/1;
  e. a view want (o2.col, not subject-scoped) is scored exactly by its group fraction;
  (f, arm OFF identical, is the short live run.)

    python test_goal_distance.py
"""
from __future__ import annotations

import sys

import tether
from test_goal_condition import _compiled
from test_goal_pair import ROWS
from test_gt_which import _linked

sys.dont_write_bytecode = True


def _series(ag, base, cols):
    out = []
    for c in cols:
        st = dict(base, **{"o0.col": c})
        out.append(ag.goal_residual("o0.col", st))
    return out


def _choose(ag, series):
    ag._res = {"o0.col": list(series)}
    why: dict = {}
    return ag._goal_choice(why), why


if __name__ == "__main__":
    ag = _linked()
    base = dict(next(st for st, hit in ROWS if not hit), **{"o3.col": 3})
    near = _series(ag, base, (0, 1, 2))
    far = _series(ag, base, (2, 1, 0))
    print(f"  residuals approaching (o0.col 0,1,2 -> o3.col 3): {near}; drifting (2,1,0): {far}")
    pick, why = _choose(ag, near)
    assert pick == "o0.col" and all(r > 0 for r in near), (pick, why, near)
    tgt = ag._goal_target("o0.col", dict(base, **{"o0.col": 2}))
    assert tgt == 3, tgt
    print(f"  a: approached -> _goal_choice picks o0.col BEFORE it holds ({why}); "
          f"target from 2 is {tgt}")
    pick, why = _choose(ag, far)
    assert pick is None and why["rose"] == 1, (pick, why)
    print(f"  b: drifted away -> no pick, rose {why['rose']}")
    r0 = ag.goal_residual("o0.col", dict(base, **{"o0.col": 3}))
    assert r0 == 0.0, r0
    print(f"  c: R at o0.col == o3.col: {r0}")
    c = _compiled(ag, "o0.colour == o3.colour")
    link = ag._link_goal("colour-test", c)
    assert link["linked"] and ag._want_scope.get("o0.colour"), link
    assert ag.slot_types["o0.colour"] not in tether.ORDERED_TYPES
    vals = sorted({ag.goal_residual("o0.colour", dict(base, **{"o0.colour": v, "o3.colour": 5}))
                   for v in range(10)} - {None})
    assert set(vals) <= {0.0, 1.0}, vals
    print(f"  d: comparable-only subject want o0.colour reads only {vals}")
    own = ag._want_terms["o0.col"]
    ag.wants["o2.col"], ag._want_terms["o2.col"] = own.name, own
    assert "o2.col" not in ag._want_scope
    st = dict(base, **{"o2.col": 0})
    term = ag._objective_of("o2.col")[1]
    ops = ag._ops(term, st)
    ctx = ag._eval_ctx("o2.col", st, action=ag._last_action or "", operands=ops,
                       touching=ag._touching("o2.col"), shapes=False, landed=ag._last_landed)

    def _sat(v):
        r = term.apply(v, ctx)
        return None if r is tether.NOT_RESOLVED else bool(r)
    want = 1.0 - tether.objective_degree(_sat, ag._group("o2.col", st), None,
                                         ag._scope_weights("o2.col", st))
    got = ag.goal_residual("o2.col", st)
    assert got == want, (got, want)
    print(f"  e: view want o2.col scored by its group fraction: {got} == {want}")
    print("ok")
