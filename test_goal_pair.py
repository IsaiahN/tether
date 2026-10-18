"""Objective build 2a, the goal pair (TETHER_GOAL_PAIR; the reviewer 2026-10-11 05:14Z). A held goal
condition may be the AND of two conditions, priced once as one term (both parts + the `both`
joiner). The data is the recorded objective-panel history of gridworld_arc_s1 (120 steps, the
objective held at 2, 16, 18, 20, 21, 89; o0-o5 rows and columns), tests/fixtures.

  must-pass: at its 6th completion (c89) the pair "o0.col == o3.col and o0.row < o3.row" is held;
     re-priced on every later step to c119 (L1), it still pays and stays held;
  1. a restating pair does not pay (one pair per reached step costs more than the base);
  2. a pair of identical parts is refused (never formed);
  3. the negation never pays;
  4. arm OFF changes nothing: no pair is priced and the pick is the single-condition one;
  (b) (the reviewer 05:14Z, 05:29Z): with the link ON, the held pair links as TWO subject-scoped
     wants -- on o0.col and o0.row (under TETHER_RELATION_SET, default ON since 10-15, the "<"
     conjunct compiles on o0's own row by CONVERSE, `below`; it compiled on o3.row by the
     reversed binding before) -- whose
     R_goal the avatar's own move takes from 1 to 0; an occupied slot refuses the WHOLE pair,
     counted once; unholding releases both wants and only those.

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
# THE REGIME THESE c89 FIXTURES WERE WRITTEN IN (B O1, the reviewer 2026-10-18 09:24): an exact
# tie in the goal pick goes by text order (TETHER_A1_TIES, a recorded draw since 0996891) and
# every birth has one temperament (TETHER_AGENT_SEED, cab5bd5). An OLD regime, so a green here
# does not cover the default (LEDGER: B 2026-10-18, O1)
tether._A1_TIES = tether._AGENT_SEED = False
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
    tether._GOAL_CONDITION = tether._GOAL_PAIR = tether._GOAL_LINK = True
    try:
        lk = _agent()
        for sl in ("o0.col", "o0.row"):
            lk.wants.pop(sl, None)
            lk._want_terms.pop(sl, None)
        bound_on = {sl: lk.bound.get(sl) for sl in ("o0.col", "o0.row")}
        lk._reach_hist = ROWS[:C89 + 1]
        lk._goal_condition()
        link = [r["detail"] for r in lk.led.rows() if r["event"] == "goal_condition"][-1]["link"]
        # "o0.row < o3.row" compiles on o0's own row by CONVERSE (`below`, TETHER_RELATION_SET);
        # before the arm it compiled by the REVERSED binding on o3.row, a row the avatar does not
        # move (the arm-on reading, the reviewer 2026-10-18 09:24 O2). Subjects: o0.col, o0.row
        assert link["linked"] and link["slots"] == ["o0.col", "o0.row"], link
        assert all(lk._want_scope[sl] == lk.wants[sl] for sl in link["slots"])
        away = next(st for st, hit in ROWS if not hit and st["o0.col"] != st["o3.col"]
                    and st["o0.row"] >= st["o3.row"])
        home = dict(away, **{"o0.col": away["o3.col"], "o0.row": away["o3.row"] - 1})
        # b-0 amended (08:34Z, 08:48Z): a subject want on an ordered slot reads its distance
        # from holding over the alphabet, gap / (alphabet - 1); 0 exactly at home
        unit = lk.alphabet["o0.col"] - 1
        assert lk.goal_residual("o0.col", away) == abs(away["o0.col"] - away["o3.col"]) / unit
        assert lk.goal_residual("o0.col", home) == 0.0
        rr = lk.goal_residual("o0.row", away)
        assert 0 < rr <= 1 and lk.goal_residual("o0.row", home) == 0.0, rr
        tc = lk._goal_target("o0.col", away)
        tr = lk._goal_target("o0.row", away)
        assert tc == away["o3.col"], tc
        print(f"  (b) linked as two subject wants {link['want']} on {link['slots']}; bound "
              f"before: {bound_on}")
        print(f"      both R_goal read 1 with o0 at ({away['o0.row']},{away['o0.col']}) and 0 with "
              f"o0 moved to ({home['o0.row']},{home['o0.col']}): the avatar moves both")
        print(f"      objective targets: o0.col -> {tc} (o3's column); o0.row -> {tr} (o0's own "
              f"row, below o3's)")
        unlinked0 = lk.gamma.book.get("goal_unlinked", 0)
        key = next(iter(lk._goal_conds))
        assert lk._release_link(key) and not ({"o0.col", "o0.row"} & set(lk.wants))
        assert lk.gamma.book.get("goal_unlinked") == unlinked0 + 1
        print("  (b) release: both wants released together, goal_unlinked +1")
        oc = _agent()
        oc.wants.pop("o0.col", None)
        oc.wants["o0.row"] = "some . other<want>"
        oc._reach_hist = ROWS[:C89 + 1]
        oc._goal_condition()
        ol = [r["detail"] for r in oc.led.rows() if r["event"] == "goal_condition"][-1]["link"]
        assert ol["linked"] is False and "o0.col" not in oc.wants, ol
        assert oc.gamma.book.get("goal_link_refused_wants") == 1
        print("  (b) refusal: o0.row already wanted, so the WHOLE pair is refused (no half-link), "
              "counted once")
    finally:
        tether._GOAL_CONDITION = tether._GOAL_PAIR = tether._GOAL_LINK = False
    print("ok")
