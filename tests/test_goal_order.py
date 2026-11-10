"""BUILD 5 ITEM 17 (iv), ORDER AS A PLAN (TETHER_GOAL_ORDER; the reviewer 2026-11-05 r1206;
Fig 12 :112 "A plan is a sequence. A goal is a comparison."). "A then B" is true at a row where B
holds and A held at an earlier row (one pass), priced by the one bargain at |A| + |B| + 1; held,
A is adopted as the 4g subgoal of B. Seconds: test_group_row's agent; a history forced from its
own state.

The history: B ("o3.colour == 3") holds on rows 0-9 before A ever held -- not met; A ("o1.row ==
o2.row") holds on row 10 only; B holds on rows 11+ (every third off) -- met exactly where B holds.
MF-O1  "A then B" is offered with errors 0 and the cheapest that pays is an order whose second
       step is B; the single B errs on the ten rows before A
MF-O2  holding it adopts the subgoal (sub = A's slot, parent = B's slot, row subgoal_adopted read
       "ordered goal") and _goal_choice selects A's slot while A's want is open
MF-O3  with A never holding before B, no "A then B" is offered
OFF: no order offered. The red is behavioural: TETHER_GOAL_ORDER=0 fails MF-O1.

    python tests/test_goal_order.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether
A, B = "o1.row == o2.row", "o3.colour == 3"


def history(st: dict, a_row: int | None = 10) -> list:
    rows = []
    for i in range(37):
        s = dict(st)
        if i == a_row:
            s["o2.row"] = st["o1.row"]                  # A, once
        elif i < 10 or i % 3:
            s["o3.colour"] = 3                          # B
        b = s["o3.colour"] == 3
        rows.append((s, b and a_row is not None and i > a_row))
    return rows


def main():
    ag, atoms, st = G.agent()
    assert st["o1.row"] != st["o2.row"] and st["o3.colour"] != 3, "the panel: A and B start false"
    rows = history(st)
    best, detail = ag._goal_candidates(rows)
    conds = {t: ag._compile_cache.get(t) for t in (A, B)}
    assert all(isinstance(c, tether.compile_term.Compiled) for c in conds.values()), conds

    def singles(h: list) -> list:      # the single's row as _goal_candidates writes it
        out = []
        for t, c in conds.items():
            cost, left, e = ag._goal_price([c], h)
            out.append((cost + left, cost, left, e, t, c))
        return out
    orders = {x[4]: x for x in ag._goal_orders(singles(rows), rows)}
    assert f"{A} then {B}" in orders and orders[f"{A} then {B}"][3] == 0, (
        "MF-O1: 'A then B' not offered exact", orders)
    single_b = ag._goal_price([conds[B]], rows)[2]
    assert single_b >= 10, ("MF-O1: the single B does not err before A", single_b)
    assert detail["offered"].get("order", 0) >= 1 and best is not None and isinstance(
        best[5], tether._Order) and best[3] == 0, ("MF-O1: no order is the cheapest that pays",
                                                   detail["cheapest"])

    order = orders[f"{A} then {B}"][5]
    ag.wants.clear()
    ag._subgoal = None
    link = ag._link_order("@order", order)
    adopted = [r for r in ag.led.rows() if r["event"] == "subgoal_adopted"]
    assert link.get("subgoal") == order.first.slot and ag._subgoal == {
        "parent": link["slots"][0], "sub": order.first.slot} and adopted and adopted[-1][
        "detail"]["read"] == "ordered goal", ("MF-O2: the subgoal is not adopted", link)
    ag._res = {order.first.slot: [2, 1], link["slots"][0]: [3, 2, 1]}
    ag._hyp = None
    pick = ag._goal_choice()
    assert pick == order.first.slot, ("MF-O2: the first step is not selected first", pick)
    parent = link["slots"][0]
    ag._res = {order.first.slot: [2, 1, 0], parent: [3, 2, 1]}     # A arrives
    pick2 = ag._goal_choice()
    assert ag._subgoal is None and parent in ag.wants and pick2 == parent, (
        "MF-O4 (ii): ending the sub ended or dropped the parent", ag._subgoal, pick2)

    # MF-O4 (i) (r1208): one slot, two targets -- "become same, then different"
    same = tether._Order((ag._compile_cache["o3.colour == o4.colour"],
                          ag._compile_cache["o3.colour != o4.colour"]))
    ag.wants.clear()
    ag._subgoal = None
    link1 = ag._link_order("@one-slot", same)
    sl = link1["slots"][0]
    assert link1.get("linked") and "same" in ag.wants[sl], (
        "MF-O4 (i): A's target is not wanted first", link1, ag.wants)
    ag._order_advance({**st, "o3.colour": 1, "o4.colour": 1})                 # A holds
    nxt = [r for r in ag.led.rows() if r["event"] == "order_next"]
    assert nxt and "other" in ag.wants.get(nxt[-1]["slot"], ""), (
        "MF-O4 (i): the want did not switch to B's target when A held", ag.wants)
    assert "@one-slot" in ag._goal_links, "MF-O4 (i): the goal's key was dropped"

    never = history(st, a_row=None)
    never[-1] = (never[-1][0], True)                    # one met row, A never held at all
    none = {x[4] for x in ag._goal_orders(singles(never), never)}
    assert f"{A} then {B}" not in none, ("MF-O3: offered with A never before B", none)

    tether._GOAL_ORDER = False
    try:
        _b, d_off = ag._goal_candidates(rows)
    finally:
        tether._GOAL_ORDER = True
    assert "order" not in d_off["offered"] and not any(
        " then " in x["if"] for x in d_off["cheapest"]), ("OFF: an order offered", d_off)
    print(f"test_goal_order: pass (MF-O1 '{A} then {B}' errors 0, the single B errs {single_b}, "
          f"best {best[4]!r} of {detail['offered']['order']} orders; MF-O2 subgoal "
          f"adopted 'ordered goal', selected {pick}; MF-O4 sub ended on arrival, parent {pick2} "
          f"kept and selected, one-slot want switched to {ag.wants[nxt[-1]['slot']]!r}; MF-O3 "
          f"none with A never first; OFF none offered)")


if __name__ == "__main__":
    main()
