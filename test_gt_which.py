"""Which None, and one row per refusal (the reviewer 2026-10-11 06:24Z). `_goal_target`
names the exit it took in `_gt_which`; `split_refused why=no_goal_target` carries it as `which`;
the routine mint's dry call (`_goal_split(commit=False)`) writes no split_refused row (5a'). The
data is the recorded gridworld_arc_s1 history at c89 (tests/fixtures), the pair linked.

  1. one refusal occasion gives exactly one split_refused row: none on the dry call, one on
     the acting call;
  3. each exit that can be built from a real state is reached and named: no_obj_term,
     not_applies, not_resolved, already_holds; no_operands and not_int are reported, not
     authored (see the prints).

    python test_gt_which.py
"""
from __future__ import annotations

import sys

import tether
from test_goal_condition import _agent, _compiled
from test_goal_pair import C89, ROWS

sys.dont_write_bytecode = True


def _linked():
    tether._GOAL_CONDITION = tether._GOAL_PAIR = tether._GOAL_LINK = True
    try:
        ag = _agent()
        for sl in ("o0.col", "o0.row"):
            ag.wants.pop(sl, None)
            ag._want_terms.pop(sl, None)
        ag._reach_hist = ROWS[:C89 + 1]
        ag._goal_condition()
        # the recorded history's candidates TIE EXACTLY and the member is A1's (TETHER_A1_TIES,
        # Isaiah 10-15): the PROPERTY is checked (the pick is the cheapest row, zero errors), then
        # the pair the exits are built around is linked explicitly (2026-10-20)
        row = [r["detail"] for r in ag.led.rows() if r["event"] == "goal_condition"][-1]
        assert row["cheapest"][0]["if"] == row["pick"] and row["cheapest"][0]["errors"] == 0, row
        for key in list(ag._goal_links):
            ag._release_link(key)
        ag._goal_conds.clear()
        ag._goal_text.clear()
        for sl in ("o0.col", "o0.row"):
            ag.wants.pop(sl, None)
            ag._want_terms.pop(sl, None)
        pair = tether._Pair((_compiled(ag, "o0.col == o3.col"), _compiled(ag, "o0.row < o3.row")))
        ag._goal_conds["test_pair"] = pair
        ag._goal_text["test_pair"] = "o0.col == o3.col and o0.row < o3.row"
        link = ag._link_goal("test_pair", pair)
        assert link["linked"], link
    finally:
        tether._GOAL_CONDITION = tether._GOAL_PAIR = tether._GOAL_LINK = False
    return ag


def _which(ag, slot, st):
    assert ag._goal_target(slot, st) is None
    return ag._gt_which


if __name__ == "__main__":
    tether._WANT_TARGET = True
    try:
        ag = _linked()
        away = next(st for st, hit in ROWS if not hit and st["o0.col"] != st["o3.col"])
        held = dict(away, **{"o0.col": away["o3.col"]})
        assert _which(ag, "o5.col", away) == "no_obj_term"
        assert _which(ag, "o0.col", {k: v for k, v in away.items() if k != "o3.col"}) \
            == "not_applies"
        assert _which(ag, "o0.col", dict(away, **{"o3.col": 10 ** 6})) == "not_resolved"
        # GQ3 (TETHER_ARRIVAL): the subject at its target is a means read, renamed subject_met
        assert _which(ag, "o0.col", held) == ("subject_met" if tether._ARRIVAL
                                              else "already_holds")
        print("  3: no_obj_term (o5.col, no want), not_applies (o3.col absent), not_resolved "
              "(o3.col outside o0.col's domain: nothing satisfies), already_holds (o0 in o3's "
              "column) -- each reached and named")
        print("     no_operands: needs an operand term that reads NOT_RESOLVED on a present "
              "value; none in this fixture, NOT AUTHORED")
        print("     not_int: an OBJ term's value is objective_step's, an int of the domain or "
              "NOT_RESOLVED; not reached here, NOT AUTHORED")
        ag._goal_choice = lambda _why=None: "o0.col"
        n0 = sum(1 for r in ag.led.rows() if r["event"] == "split_refused")
        assert ag._goal_split(held, commit=False) is None
        assert ag._split_why == "no_goal_target"
        n1 = sum(1 for r in ag.led.rows() if r["event"] == "split_refused")
        assert n1 == n0, (n0, n1)
        assert ag._goal_split(held, commit=True) is None
        rows = [r for r in ag.led.rows() if r["event"] == "split_refused"]
        assert len(rows) == n0 + 1 and rows[-1]["detail"]["which"] == (
            "subject_met" if tether._ARRIVAL else "already_holds"), rows[-1]
        print(f"  1: dry call: _split_why {ag._split_why}, 0 split_refused rows; acting call: "
              f"1 row, which={rows[-1]['detail']['which']}")
    finally:
        tether._WANT_TARGET = False
    print("ok")
