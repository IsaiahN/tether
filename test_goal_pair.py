"""Objective build 2a, the goal pair (TETHER_GOAL_PAIR; the reviewer 2026-10-11 05:14Z). A held goal
condition may be the AND of two conditions, priced once as one term (both parts + the `both`
joiner). The data is the recorded objective-panel history of gridworld_arc_s1 (120 steps, the
objective held at 2, 16, 18, 20, 21, 89; o0-o5 rows and columns), tests/fixtures.

  must-pass: at its 6th completion (c89) the pair "o0.col == o3.col and o0.row < o3.row" is held;
     re-priced on every later step to c119 (L1), it still pays and stays held;
  1. a restating pair does not pay (one pair per reached step costs more than the base);
  2. a pair of identical parts is refused (never formed);
  3. the negation never pays;
  4. arm OFF changes nothing: no pair is priced and the pick is the single-condition one.

    python test_goal_pair.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import tether
from test_goal_condition import _agent, _compiled

sys.dont_write_bytecode = True
DATA = json.loads((Path(__file__).parent / "tests" / "fixtures" / "goal_pair_arc_s1.json")
                  .read_text(encoding="utf-8"))
ROWS = [(r["state"], r["reached"]) for r in DATA["rows"]]
C89 = next(i for i, r in enumerate(DATA["rows"]) if r["cycle"] == 89)


def _run(pair_on: bool):
    was = (tether._GOAL_CONDITION, tether._GOAL_PAIR)
    tether._GOAL_CONDITION, tether._GOAL_PAIR = True, pair_on
    try:
        ag = _agent()
        ag._reach_hist = ROWS[:C89 + 1]
        ag._goal_condition()
    finally:
        tether._GOAL_CONDITION, tether._GOAL_PAIR = was
    return ag, [r["detail"] for r in ag.led.rows() if r["event"] == "goal_condition"][-1]


if __name__ == "__main__":
    ag, row = _run(True)
    want = {"o0.col == o3.col", "o0.row < o3.row"}
    assert set(row["pick"].split(" and ")) == want, row
    print(f"  must-pass: at c89 '{row['pick']}' is held (cost {row['cheapest'][0]['cost']}, "
          f"left {row['cheapest'][0]['left']}, base {row['base_bits']})")
    tether._GOAL_CONDITION = tether._GOAL_PAIR = True
    try:
        for i in range(C89 + 1, len(ROWS)):
            ag._reach_hist = ROWS[:i + 1]
            ag._goal_recheck()
        assert len(ag._goal_conds) == 1, "the pair was unheld before c119"
        assert not [r for r in ag.led.rows() if r["event"] == "goal_unheld"]
    finally:
        tether._GOAL_CONDITION = tether._GOAL_PAIR = False
    print(f"  must-pass (L1): re-priced on every step c90..c119, still paying at N "
          f"{len(ROWS)}; held throughout")
    hist = ROWS[:C89 + 1]
    n, k = len(hist), sum(h for _, h in hist)
    base = k * math.log2(n)
    a, b = _compiled(ag, "o0.col == o3.col"), _compiled(ag, "o0.row < o3.row")
    pair = tether._Pair((a, b))
    cost, _left, _e = ag._goal_price([pair] * k, hist)
    assert cost >= base, (cost, base)
    print(f"  1: one pair per reached step ({k}) costs {round(cost, 3)} before any error, >= base "
          f"{round(base, 3)}")
    singles = [(0, 0, 0, 0, "o0.col == o3.col", a), (0, 0, 0, 0, "o0.col == o3.col", a)]
    assert ag._goal_pairs(singles, hist) == []
    print("  2: two identical parts form no pair")
    neg = tether._Pair((_compiled(ag, "o0.col != o3.col"), _compiled(ag, "o0.row > o3.row")))
    cost, left, e = ag._goal_price([neg], hist)
    assert not tether.pays(cost, left, base), (cost, left, base)
    print(f"  3: the negated pair makes {e} errors, {round(cost + left, 3)} >= {round(base, 3)}")
    off, row = _run(False)
    assert " and " not in row["pick"] and not any(" and " in c["if"] for c in row["cheapest"])
    print(f"  4: arm OFF: no pair priced; the pick is '{row['pick']}'")
    print("ok")
