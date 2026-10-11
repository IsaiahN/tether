"""Objective build 3, the link to composition (TETHER_GOAL_LINK; the reviewer 2026-10-11 02:19Z,
03:14Z). A held goal condition becomes one of the agent's composed objectives -- closed into the
objective stream with `all` -- so `_goal_choice` and `_mint_routine` can pick it.

The hand history of test_goal_condition (ARC atoms, 40 steps, objective held where o0.col ==
o1.col).

  must-pass: the condition is linked as o0.col's want, `goal_residual` reads it as a number, and
     after steps o0.col is in `_goal_choice`'s candidate population (`_res`);
  must-fail (ruled): with the arm OFF, the wants -- `_goal_choice`'s candidate source -- are
     unchanged;
  no overwrite: a slot that already wants something keeps its want, and the row says so;
  L2 (the reviewer 03:28Z): links made and refused ("slot already wants") are counted;
  L1 must-fail: a held condition that still pays stays held on a recheck;
  L1 must-pass: once it stops paying on the longer history it is unheld and its own want
     released; a want the agent composed itself is never released;
  already held: a later completion picking the same condition does not hold it again;
  E1 (the reviewer 03:38Z): at a retarget a held condition CLOSES with its level -- one
     goal_closed row naming how, and after one more step no goal_unheld row and goal_unlinked
     unchanged (an empty history is no verdict).

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
    assert ag.gamma.book.get("goal_link_made") == 1
    assert occ.gamma.book.get("goal_link_refused_wants") == 1
    print("  L2: goal_link_made 1 on the linked agent, goal_link_refused_wants 1 on the "
          "occupied one")
    tether._GOAL_CONDITION = tether._GOAL_LINK = True
    try:
        ag._reach_hist = _hist(ag)
        ag._goal_recheck()
        assert ag._goal_conds and SLOT in ag.wants
        print("  L1 must-fail: on the same history the condition still pays and stays held")
        ag._goal_condition()
        again = [r["detail"] for r in ag.led.rows() if r["event"] == "goal_condition"][-1]
        assert again["pick"].startswith("already held") and len(ag._goal_conds) == 1
        print(f"  already held: a second completion reads '{again['pick']}'; one condition held")
        bad = [(dict(st, **{"o0.col": 1, "o1.col": 1}), False) for st, _ in _hist(ag)]
        ag._reach_hist = _hist(ag) + bad
        ag._goal_recheck()
        un = [r["detail"] for r in ag.led.rows() if r["event"] == "goal_unheld"]
        assert not ag._goal_conds and SLOT not in ag.wants and un and un[-1]["want_released"]
        assert ag.gamma.book.get("goal_unlinked") == 1
        print(f"  L1 must-pass: 40 more steps where the condition holds and the objective "
              f"does not: cost {un[-1]['cost']} + left {un[-1]['left']} >= base "
              f"{un[-1]['base_bits']}; unheld, its want released, goal_unlinked 1")
        occ._reach_hist = _hist(occ) + bad
        occ._goal_recheck()
        assert not occ._goal_conds and occ.wants[SLOT] == "some . other<want>"
        print("  L1, the agent's own want: the unlinked condition on the occupied slot is "
              "dropped and the agent's want 'some . other<want>' stays")
        e1, _b, _r = _held(True)
        was_sweep = tether._COMPLETION_SWEEP
        tether._COMPLETION_SWEEP = True
        try:
            unlinked0 = e1.gamma.book.get("goal_unlinked", 0)
            e1.retarget(e1.env, 1, "advance")
            e1.step()
        finally:
            tether._COMPLETION_SWEEP = was_sweep
        rows = e1.led.rows()
        closed = [r["detail"] for r in rows if r["event"] == "goal_closed"]
        assert not [r for r in rows if r["event"] == "goal_unheld"]
        assert e1.gamma.book.get("goal_unlinked", 0) == unlinked0 and not e1._goal_conds
        assert len(closed) == 1 and closed[0]["how"] == "advance", closed
        print(f"  E1: a retarget ('advance') then one step: one goal_closed row "
              f"('{closed[0]['condition']}', how {closed[0]['how']}, no verdict), no goal_unheld, "
              f"goal_unlinked unchanged")
    finally:
        tether._GOAL_CONDITION = tether._GOAL_LINK = False
    print("ok")
