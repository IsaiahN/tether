"""R-dir (ii), TETHER_ROUTINE_STALE (the reviewer 2026-10-11 10:39Z): a held routine whose live
comparison reads the OPPOSITE sign to the one it was minted with ends "stale" before pressing
(Fig 12 :112, Fig 5, Fig 6, Fig 10). Agent: the recorded gridworld_arc_s1 pair, o0.col linked
to o3.col's column, so the operand is a slot the world can move.

  1. moving operand: minted "o0.col +" (o0.col 2, o3.col 3); o3.col now 1 -> ends `stale` at
     PLAN with minted +, live -, and the routine is not held; OFF, no stale row;
  2. still operand (o3.col stays 3): the choice and the ledger rows equal OFF's;
  3. a stale ending refuses nothing: the SAME shape passes the mint's refusal check after it
     (the reviewer 10:53Z), and the control -- that routine ended `exhausted` -- is refused;
  6. unreadable operand (o3.col absent) and a held comparison: equal OFF's (A1).

    python test_routine_stale.py
"""
from __future__ import annotations

import sys

import interface as IFace
import routine as Rt
import tether
from test_goal_pair import ROWS
from test_gt_which import _linked

sys.dont_write_bytecode = True


def _run(stale: bool, st: dict):
    tether._WANT_TARGET = True
    tether._ROUTINE_STALE = stale
    try:
        ag = _linked()
        r = Rt.Until("o0.col", Rt.Act(IFace.Intent(IFace.BECOME, "o0.col", "+")), 3)
        ag.routine, ag.routine_for, ag._routine_adopted, ag._routine_acts = r, "o0.col", r, 1
        n0 = len(ag.led.rows())
        frozen = (len(ag.refuted), len(ag._refusals), len(ag._reach_tested), len(ag.routines))
        got = ag.choose(dict(st))
        rows = ag.led.rows()[n0:]
        after = (len(ag.refuted), len(ag._refusals), len(ag._reach_tested), len(ag.routines))
        return ag, r, got, rows, frozen, after
    finally:
        tether._WANT_TARGET = tether._ROUTINE_STALE = False


def _ends(rows):
    return [r["detail"] for r in rows if r["event"] == "routine_end"]


if __name__ == "__main__":
    base = dict(next(st for st, hit in ROWS if not hit), **{"o0.col": 2, "o3.col": 3})
    moved = dict(base, **{"o3.col": 1})
    ag, r, got, rows, frozen, after = _run(True, moved)
    st = [e for e in _ends(rows) if e.get("outcome") == "stale"]
    assert len(st) == 1, _ends(rows)
    assert st[0]["minted_sign"] == "+" and st[0]["live_sign"] == "-" and st[0]["target"] == 1, st
    assert ag._routine_adopted is not r and ag.routine is not r, (ag.routine, r)
    off = _run(False, moved)
    assert not [e for e in _ends(off[3]) if e.get("outcome") == "stale"], _ends(off[3])
    oe = [e["outcome"] for e in _ends(off[3])]
    print(f"  1: moving operand -> stale {st[0]}; OFF: endings {oe}"
          f", choice {off[2]}")
    assert frozen == after, (frozen, after)
    key = ag._refusal_key(ag._characterise_gap("o0.col"), r)
    assert not ag._refused(key), key
    ag.routine, ag.routine_for, ag._routine_adopted = r, "o0.col", r
    ag._end_routine(Rt.EXHAUSTED, moved)
    assert ag._refused(key), key
    print(f"  3: after stale the same shape is admissible (refused False); control, the same "
          f"routine ended exhausted: refused True; counts {frozen} -> {after}")
    for name, s in (("2 still operand", base),
                    ("6 unreadable operand", {k: v for k, v in base.items() if k != "o3.col"}),
                    ("6 held comparison", dict(base, **{"o0.col": 3}))):
        on, of = _run(True, s), _run(False, s)
        assert on[2] == of[2] and on[3] == of[3], (name, on[2], of[2])
        assert not [e for e in _ends(on[3]) if e.get("outcome") == "stale"]
        print(f"  {name}: ON == OFF (choice {on[2]}, {len(on[3])} rows, endings "
              f"{[e['outcome'] for e in _ends(on[3])]})")
    print("routine stale: OK")
