"""conform/identity_mod_rows.py (the reviewer 2026-10-12 02:13 CDT): OFF identity for an instrument
that adds rows. A base ledger, and the same ledger with one new row inserted and every later
position moved by one:
  a. the faithful copy is IDENTICAL (positions, the fed lists and segment_rows all mapped);
  b. MUST-FAIL: one decision row altered (a bet's action) is a difference;
  c. MUST-FAIL: a position left unshifted (a stale fed seq) is a difference;
  d. MUST-FAIL: a wrong segment_rows count is a difference;
  e. an added field fails unless it is named, and a named field that changes a base value
     still fails.
    python test_identity_mod_rows.py
"""
from __future__ import annotations

import copy
import sys

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
