"""Objective build 3, the link to composition (TETHER_GOAL_LINK; the reviewer 2026-10-11 02:19Z,
03:14Z). A held goal condition becomes one of the agent's composed objectives -- closed into the
objective stream with `all` -- so `_goal_choice` and `_mint_routine` can pick it.

The hand history of test_goal_condition (ARC atoms, 40 steps, objective held where o0.col ==
o1.col).

  must-pass: the condition is linked as o0.col's want, `goal_residual` reads it as a number, and
     after steps o0.col is in `_goal_choice`'s candidate population (`_res`);
  must-fail (ruled): with the arm OFF, the wants -- `_goal_choice`'s candidate source -- are
     unchanged;
  no overwrite: a slot that already wants something keeps its want, and the row says so.

    python test_goal_link.py
"""
from __future__ import annotations

import sys

import tether
from test_goal_condition import _agent, _hist

sys.dont_write_bytecode = True
SLOT = "o0.col"


def _held(link_on: bool, occupied: str | None = None):
    was = (tether._GOAL_CONDITION, tether._GOAL_LINK)
    tether._GOAL_CONDITION, tether._GOAL_LINK = True, link_on
    try:
        ag = _agent()
        ag.wants.pop(SLOT, None)
        ag._want_terms.pop(SLOT, None)
        if occupied:
            ag.wants[SLOT] = occupied
        before = dict(ag.wants)
        ag._reach_hist = _hist(ag)
        ag._goal_condition()
    finally:
        tether._GOAL_CONDITION, tether._GOAL_LINK = was
    row = [r["detail"] for r in ag.led.rows() if r["event"] == "goal_condition"][-1]
    return ag, before, row


if __name__ == "__main__":
    ag, before, row = _held(True)
    link = row["link"]
    assert link["linked"] and link["slot"] == SLOT and ag.wants[SLOT] == link["want"], row
    state = ag.trace[-1][0]
    g = ag.goal_residual(SLOT, state)
    assert isinstance(g, (int, float)), g
    for _ in range(3):
        ag.step()
    assert SLOT in ag._res, sorted(ag._res)
    print(f"  must-pass: '{row['pick']}' linked as {SLOT}'s want '{link['want']}'; goal_residual "
          f"reads {g}; after 3 steps {SLOT} is in _goal_choice's population "
          f"({len(ag._res[SLOT])} readings)")
    off, before, row = _held(False)
    assert off.wants == before and "link" not in row
    print("  must-fail: arm OFF, the wants (the candidate source) are unchanged and no link row")
    occ, before, row = _held(True, occupied="some . other<want>")
    assert occ.wants[SLOT] == "some . other<want>" and row["link"]["linked"] is False, row
    print(f"  no overwrite: {SLOT} already wanted 'some . other<want>'; kept, and the row says "
          f"'{row['link']['why']}'")
    print("ok")
