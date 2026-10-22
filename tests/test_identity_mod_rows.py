"""conform/identity_mod_rows.py (the reviewer 2026-10-12 02:13 CDT): OFF identity for an instrument
that adds rows. A base ledger, and the same ledger with one new row inserted and every later
position moved by one:
  a. the faithful copy is IDENTICAL (positions, the fed lists and segment_rows all mapped);
  b. MUST-FAIL: one decision row altered (a bet's action) is a difference;
  c. MUST-FAIL: a position left unshifted (a stale fed seq) is a difference;
  d. MUST-FAIL: a wrong segment_rows count is a difference;
  e. an added field fails unless it is named, and a named field that changes a base value
     still fails.
  f. the arms row's birth seed is masked; g. MUST-FAIL: the effective @run seed differs;
  h. MUST-FAIL: with no @run seed row the arms seed is the effective one (the reviewer
     2026-10-20 12:23).
  i. a field in TIMINGS (goal_hypotheses' wall_s) is masked; j. MUST-FAIL: a non-timing field
     beside it still differs (the reviewer 2026-10-21 23:16: one list, every comparer imports it).
    python tests/test_identity_mod_rows.py
"""
from __future__ import annotations

import copy
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.path.insert(0, "conform")
from identity_mod_rows import compare  # noqa: E402

sys.dont_write_bytecode = True


def _row(n, event, **detail):
    return {"seq": n, "cycle": 1, "step": "PERCEIVE", "slot": "o0.col", "event": event,
            "mode": "specified", "detail": detail}


BASE = [
    _row(0, "bet", action="ACTION1"),
    _row(1, "accept", seq=1),
    _row(2, "process_settle", bet_seq=0),
    _row(3, "resolution", signal_seq=0, fed=[[1, "goal"]]),
    _row(4, "repeat", gamma_read={"fed": [{"seq": 1}, {"seq": None}]}),
    _row(5, "completion_sweep", segment_rows=5),
]


def _new():
    """BASE with one goal_choice row inserted after row 0: every later position moves by one."""
    b = [copy.deepcopy(BASE[0]), _row(1, "goal_choice", selected=None)]
    for r in copy.deepcopy(BASE[1:]):
        r["seq"] += 1
        b.append(r)
    b[2]["detail"]["seq"] = 2
    b[3]["detail"]["bet_seq"] = 0
    b[4]["detail"]["fed"] = [[2, "goal"]]
    b[5]["detail"]["gamma_read"]["fed"][0]["seq"] = 2
    b[6]["detail"]["segment_rows"] = 6
    return b


if __name__ == "__main__":
    drop = {"goal_choice"}
    assert compare(BASE, _new(), drop) == [], f"a: {compare(BASE, _new(), drop)}"
    print("a. a faithful copy with one inserted row is identical: ok")

    b = _new()
    b[0]["detail"]["action"] = "ACTION2"
    assert compare(BASE, b, drop), "b: an altered decision row passed"
    print("b. an altered action fails: ok")

    b = _new()
    b[4]["detail"]["fed"] = [[1, "goal"]]
    assert compare(BASE, b, drop), "c: an unshifted position passed"
    print("c. an unshifted position fails: ok")

    b = _new()
    b[6]["detail"]["segment_rows"] = 5
    assert compare(BASE, b, drop), "d: a wrong segment_rows passed"
    print("d. a wrong row count fails: ok")

    b = _new()
    b[3]["detail"]["offered"] = {"plain": 0}
    assert compare(BASE, b, drop), "e: an unnamed new field passed"
    assert compare(BASE, b, drop, {"process_settle:offered"}) == [], "e: a named new field failed"
    b[3]["detail"]["bet_seq"] = 2
    assert compare(BASE, b, drop, {"process_settle:offered"}), "e: naming a field hid a change"
    print("e. an added field passes only when named, and never hides a changed value: ok")

    def _seeded(birth, eff):
        def run(n, event, **d):
            return {"seq": n, "cycle": 0, "step": "PLAN", "slot": "@run", "event": event,
                    "mode": "specified", "detail": d}
        r = [run(-2, "arms", seed=birth, seed_source="birth", generation=0)]
        if eff:
            r.append(run(-1, "seed", seed=eff, seed_source="lineage:t", generation=3))
        return r + copy.deepcopy(BASE)

    def _eff(x, y):
        return any("effective seed" in s for s in compare(x, y, set()))

    assert compare(_seeded("b1", "e"), _seeded("b2", "e"), set()) == [], "f: birth seed failed"
    print("f. two ledgers differing only in the arms row's birth seed are identical: ok")
    assert _eff(_seeded("b1", "e"), _seeded("b1", "e2")), "g: an effective seed difference passed"
    print("g. MUST-FAIL: ledgers differing only in the effective @run seed are different: ok")
    assert _eff(_seeded("b1", None), _seeded("b2", None)), "h: a lineage-less seed passed"
    print("h. MUST-FAIL: with no @run seed row the arms seed is the effective one: ok")
    hyp = [_row(0, "goal_hypotheses", checked=3, group_n=2, wall_s=0.0123)]
    other = copy.deepcopy(hyp)
    other[0]["detail"]["wall_s"] = 0.9876
    assert compare(hyp, other, set()) == [], "i: a TIMINGS field alone failed"
    print("i. ledgers differing only in goal_hypotheses' wall_s (TIMINGS) are identical: ok")
    other[0]["detail"]["group_n"] = 3
    assert compare(hyp, other, set()), "j: a non-timing field beside a timing passed"
    print("j. MUST-FAIL: a non-timing field (group_n) beside the masked wall_s is a difference: ok")
