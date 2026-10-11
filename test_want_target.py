"""F2, one lookup for a slot's objective (TETHER_WANT_TARGET; the reviewer 2026-10-11 05:38Z).
`_objective_of(slot)`: the bound term if it is an objective, else the retained want (library
first, then `_want_terms`) -- goal_residual's order; `_goal_target` and `_term_of` read it under
the arm. The data is the recorded gridworld_arc_s1 history (tests/fixtures, as test_goal_pair).

  must-pass: at c89 the held pair links; o0.col is then bound to a val PREDICTOR. ON, the column
     want still yields its target, o3's column; OFF (today) the predictor masks it: None;
  1. arm OFF: _goal_target / _term_of are today's lookup (the masked None above);
  2. ON, a slot bound to an OBJ term: target and _term_of unchanged from OFF;
  3. ON, predictor bound + want: _term_of names the want, kind "want";
  4. ON, a slot with neither (predictor bound, no want): both None.

    python test_want_target.py
"""
from __future__ import annotations

import sys

import tether
from test_goal_condition import _agent
from test_goal_pair import C89, ROWS

sys.dont_write_bytecode = True
PRED = "translate"     # an atom in the library, out_type val: a predictor, not an objective


def _both(ag, slot, before):
    out = {}
    for on in (False, True):
        tether._WANT_TARGET = on
        out[on] = (ag._goal_target(slot, before), ag._term_of(slot))
    tether._WANT_TARGET = False
    return out


if __name__ == "__main__":
    tether._GOAL_CONDITION = tether._GOAL_PAIR = tether._GOAL_LINK = True
    try:
        ag = _agent()
        for sl in ("o0.col", "o0.row"):
            ag.wants.pop(sl, None)
            ag._want_terms.pop(sl, None)
        ag._reach_hist = ROWS[:C89 + 1]
        ag._goal_condition()
    finally:
        tether._GOAL_CONDITION = tether._GOAL_PAIR = tether._GOAL_LINK = False
    want = ag.wants["o0.col"]
    away = next(st for st, hit in ROWS if not hit and st["o0.col"] != st["o3.col"]
                and st["o0.row"] >= st["o3.row"])
    assert ag.gamma.library[PRED].out_type != tether.OBJ_TYPE
    ag.bound["o0.col"] = PRED
    r = _both(ag, "o0.col", away)
    assert r[True][0] == away["o3.col"] and r[False][0] is None, r
    # the selector already read the want: its distance, gap / (alphabet - 1) (b-0 amended)
    assert ag.goal_residual("o0.col", away) == (abs(away["o0.col"] - away["o3.col"])
                                                / (ag.alphabet["o0.col"] - 1))
    print(f"  must-pass: o0.col bound to a predictor, wanting '{want}': ON target "
          f"{r[True][0]} (o3's column), OFF {r[False][0]} -- the selector and target agree ON")
    print(f"  1: OFF reads today's lookup: target None, _term_of {r[False][1]}")
    assert r[True][1]["kind"] == "want" and r[True][1]["name"] == want, r[True][1]
    print(f"  3: ON _term_of names the want, kind '{r[True][1]['kind']}'")
    obj = ag._want_terms["o0.col"]
    ag.gamma.accept(obj, 0, "test_want_target")
    ag.bound["o0.col"] = obj.name
    r2 = _both(ag, "o0.col", away)
    assert r2[True] == r2[False] and r2[True][0] == away["o3.col"], r2
    print(f"  2: ON, bound to the OBJ term itself: unchanged from OFF {r2[False]}")
    ag.bound["o0.col"] = PRED
    ag.wants.pop("o0.col")
    ag._want_terms.pop("o0.col")
    r3 = _both(ag, "o0.col", away)
    assert r3[True] == (None, None), r3
    print(f"  4: ON, predictor bound and no want: {r3[True]} (OFF {r3[False][0]}, "
          f"{r3[False][1] and r3[False][1]['kind']})")
    print("ok")
