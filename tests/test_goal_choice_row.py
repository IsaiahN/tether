"""The selector, every cycle (the reviewer 2026-10-11 20:58 CDT; widened 2026-10-12 01:45 CDT).
`progress` names the selected want only when something got closer, so a read of it saw survivors
only. `goal_choice` is written every cycle whatever the outcome.
  a. a short live run writes exactly one goal_choice row per cycle, null cycles included;
  b. a shrinking series is selected: the tally says qualified, and the selected slot carries
     movable (by sources), closer and changed (did this cycle's action change it);
  c. a flat series selects nothing, and the row says why (flat), with the series counted.
    python tests/test_goal_choice_row.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_goal_condition import _agent

sys.dont_write_bytecode = True


def _rows(ag):
    return [r for r in ag.led.rows() if r["event"] == "goal_choice"]


if __name__ == "__main__":
    ag = _agent()                                   # one step taken
    for _ in range(3):
        ag.step()
    cycles = sorted({r["cycle"] for r in ag.led.rows() if r["step"] == "PERCEIVE"})
    got = _rows(ag)
    assert [r["cycle"] for r in got] == cycles, f"a: one row per cycle, got {len(got)} for {cycles}"
    for r in got:
        d = r["detail"]
        for k in ("selected", "too_short", "flat", "rose", "qualified", "arrived", "longest",
                  "series", "wants_held", "action"):
            assert k in d, f"a: {k} missing from cycle {r['cycle']}"
    print(f"a. one goal_choice row per cycle ({len(got)}): ok")

    slot = "o0.col"
    before = dict(ag.trace[-1][0])
    after = dict(before, **{slot: before[slot] + 1})
    ag._res = {slot: [3.0, 2.0, 1.0]}
    n0 = len(_rows(ag))
    ag._note_goal_choice("ACTION1", before, after)
    d = _rows(ag)[n0]["detail"]
    assert d["selected"] == slot and d["qualified"] == 1, f"b: {d}"
    assert d["changed"] is True and isinstance(d["movable"], bool) and "closer" in d, f"b: {d}"
    assert d["movable"] == ag._moves_by_sources(slot), "b: movable is not the agent's own test"
    print("b. a shrinking series is selected, with movable / closer / changed: ok")

    ag._res = {slot: [2.0, 2.0, 2.0]}
    n0 = len(_rows(ag))
    ag._note_goal_choice("ACTION1", before, before)
    d = _rows(ag)[n0]["detail"]
    assert d["selected"] is None and d["flat"] == 1 and d["series"] == 1, f"c: {d}"
    assert "movable" not in d, f"c: a null selection carries no per-slot fields: {d}"
    print("c. a flat series selects nothing and says why: ok")
