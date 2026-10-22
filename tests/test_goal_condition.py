"""Objective build 2, the goal condition (TETHER_GOAL_CONDITION; the reviewer 2026-10-11 02:19Z). At
a completion, conditions over readings (the library's templates) are priced against the history of
WHEN the world's objective held -- the flag is the then-side, never the subject.

A hand history on the ARC atom set: 40 steps; the world's objective holds on 4 of them, exactly
where o0.col == o1.col.

  must-pass: a zero-error member of the exact tie is the pick (A1_TIES decides the member; the
     condition above is one of several), held in-episode, and its carry verdict recorded;
  1. the flag is never the minted subject: no condition reads a goal slot, none compiles onto one;
  2. nothing priced by a quantity the frame produces: emptying bound, owed and the book changes
     no price;
  3. no reading of the target is published: the world's slot set is unchanged;
  4. restating does not pay (M6-a): one condition per reached step costs more than it explains;
  5. the goal's NEGATION never pays (the price is monotone in mistakes);
  OFF: a completion with the arm OFF writes no goal_condition row.

    python tests/test_goal_condition.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gamma
import ledger
import tether
import world

sys.dont_write_bytecode = True
sys.path.insert(0, "conform")
import panel  # noqa: E402

HIT = (5, 15, 25, 35)


def _agent():
    g, seed = panel._gridworld("gridworld_arc_s1")
    env = world.bind(g)
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"gc_{seed}"), tether.Config(),
                      ledger.Ledger())
    for _ in range(6):          # _hist reads the last transition; a first step may record none
        ag.step()
        if ag.trace:
            break
    return ag


def _hist(ag, n=40):
    base = dict(ag.trace[-1][0])
    rows = []
    for i in range(n):
        st = dict(base)
        for o in range(6):
            st[f"o{o}.col"] = o % 4
        # the off-goal pairs CYCLE so o0.col == o1.col is the one zero-error single: each column
        # alone shows the goal's value off-goal too, and o0 never equals o1 off-goal (with a
        # constant (0, 3) every comparison against a constant column tied it, 2026-10-20)
        st["o0.col"], st["o1.col"] = ((2, 2) if i in HIT
                                      else ((0, 3), (3, 0), (1, 2), (2, 1))[i % 4])
        rows.append((st, i in HIT))
    return rows


def _compiled(ag, text):
    atoms = {a.name: a for a in ag.gamma.atoms}
    c = tether.compile_term.compile_candidate({"condition": text}, atoms)
    assert not isinstance(c, tether.compile_term.Refusal), (text, c)
    return c


if __name__ == "__main__":
    tether._GOAL_CONDITION = True
    ag = _agent()
    slots0 = set(ag.env.observe())
    ag._reach_hist = _hist(ag)
    ag._goal_condition()
    row = [r["detail"] for r in ag.led.rows() if r["event"] == "goal_condition"][-1]
    # the candidates TIE EXACTLY here and an exact tie is A1's (TETHER_A1_TIES, Isaiah 10-15: the
    # least-known, then the recorded draw), so the PROPERTY is asserted, never one member: the
    # pick is the cheapest row, it pays with zero errors, and it is true exactly on the met rows
    assert row["cheapest"][0]["if"] == row["pick"] and row["cheapest"][0]["errors"] == 0, row
    held = next(iter(ag._goal_conds.values()))
    assert all((tether.compile_term.run(held, st) is True) == hit
               for st, hit in ag._reach_hist), row["pick"]
    assert ag._goal_conds and "carry" in row
    print(f"  must-pass: '{row['pick']}' picked over {row['conditions']} conditions; base "
          f"{row['base_bits']} (4 steps named in 40), cheapest {row['cheapest'][0]}; carry: "
          f"{row['carry']}")
    for text in ag._inv_conditions(ag._reach_hist[-1][0]):
        assert "@" not in text and "goal" not in text
    assert all(not c.slot.startswith("@") for c in ag._goal_conds.values())
    print("  1: no condition reads a goal slot; the held one is a zero-error member of the tie")
    c = _compiled(ag, "o0.col == o1.col")
    p0 = ag._goal_price([c], ag._reach_hist)
    ag.bound, ag.owed_import = {}, set()
    ag.gamma.book["bargain_paid"] = ag.gamma.book.get("bargain_paid", 0) + 999
    assert ag._goal_price([c], ag._reach_hist) == p0
    print(f"  2: price {tuple(round(x, 3) for x in p0)} unchanged when bound, owed and the book "
          "are emptied or moved")
    assert set(ag.env.observe()) == slots0
    print("  3: the world's slot set is unchanged; nothing about the target was published")
    base = len(HIT) * tether.math.log2(40)
    per_row = [_compiled(ag, f"o0.col == o{o}.col") for o in (1, 2, 3, 4)]
    cost, _left, _e = ag._goal_price(per_row, ag._reach_hist)
    assert cost >= base, (cost, base)
    print(f"  4: one condition per reached step costs {round(cost, 3)} before any error, >= "
          f"base {round(base, 3)}: a restatement cannot pay even if it is never wrong")
    neg = _compiled(ag, "o0.col != o1.col")
    cost, left, e = ag._goal_price([neg], ag._reach_hist)
    assert e == 40 and not tether.pays(cost, left, base)
    print(f"  5: the negation is wrong on all 40 steps, {round(cost + left, 3)} >= "
          f"{round(base, 3)}: it never pays")
    tether._GOAL_CONDITION = False
    off = _agent()
    off._reach_hist = _hist(off)
    was = tether._COMPLETION_SWEEP
    tether._COMPLETION_SWEEP = True
    off._deg_prev = 0.0
    off._completion_sweep(1.0)
    tether._COMPLETION_SWEEP = was
    assert not [r for r in off.led.rows() if r["event"] == "goal_condition"]
    print("  OFF: a completion with the arm OFF writes no goal_condition row")
    print("ok")
