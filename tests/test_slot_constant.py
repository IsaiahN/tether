"""BUILD 5 ITEM 17 (ii), A SLOT AGAINST A CONSTANT (TETHER_SLOT_CONSTANT; the reviewer 2026-11-05
r1200, r1203). "Make it red" is stateable: "o1.colour == 3" compiles, the constant typed by the
slot's own reading type through the slot-to-slot row, and the completion offers "slot == v" read
off its own history. Seconds: test_group_row's agent (gridworld, ARC's comparison atoms).

MF-K1  "o1.colour == 3" compiles on o1.colour, true when it is 3 and false otherwise; OFF it is
       refused "no template compares colour with the constant 3"
MF-K2  typed by the slot: "o1.colour > 3" refused (a colour takes == / != only), "o1.row == -1"
       refused (a position is never negative), "o1.row < 3" compiles
MF-K3  (reach) a history where the objective held exactly when o1's colour was 3, a value no other
       object holds: the completion offers "o1.colour == 3", it is the cheapest that pays, it is
       wanted on o1.colour, and the agent's goal target there is 3. OFF: not offered
The red is behavioural: TETHER_SLOT_CONSTANT=0 refuses the compile and MF-K1 fails.

    python tests/test_slot_constant.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

C = G.C


def main():
    ag, atoms, st = G.agent()
    c = C.compile_candidate({"condition": "o1.colour == 3"}, atoms)
    assert isinstance(c, C.Compiled) and c.slot == "o1.colour", ("MF-K1: not compiled", c)
    assert C.run(c, {**st, "o1.colour": 3}) is True and C.run(c, {**st, "o1.colour": 2}) is False, (
        "MF-K1: the constant is not what the term compares with")
    C._SLOT_CONSTANT = False
    try:
        off = C.compile_candidate({"condition": "o1.colour == 3"}, atoms)
    finally:
        C._SLOT_CONSTANT = True
    assert isinstance(off, C.Refusal) and "constant 3" in off.reason, ("MF-K1 OFF", off)

    for text in ("o1.colour > 3", "o1.row == -1"):
        assert isinstance(C.compile_candidate({"condition": text}, atoms), C.Refusal), (
            "MF-K2: not typed by the slot", text)
    assert isinstance(C.compile_candidate({"condition": "o1.row < 3"}, atoms), C.Compiled), (
        "MF-K2: an ordered position against a constant is refused")

    assert 3 not in {v for k, v in st.items() if k.endswith(".colour")}, "the panel: 3 is taken"
    rows = [({**st, "o1.colour": (3, 1, 2, 4)[i % 4]}, i % 4 == 0) for i in range(36)]
    rows.append(({**st, "o1.colour": 3}, True))
    best, detail = ag._goal_candidates(rows)
    assert best is not None and best[4] == "o1.colour == 3" and best[3] == 0, (
        "MF-K3: the constant goal is not the cheapest that pays", detail["cheapest"])
    ag.wants.clear()
    link = ag._link_goal("@const", best[5])
    assert link["linked"] and link["slots"] == ["o1.colour"], ("MF-K3: not wanted", link)
    tgt = ag._goal_target("o1.colour", {**st, "o1.colour": 2})
    assert tgt == 3, ("MF-K3: the goal target is not the constant", tgt, ag._gt_which)
    C._SLOT_CONSTANT = False
    try:
        ag._compile_cache.clear()
        b_off, d_off = ag._goal_candidates(rows)
    finally:
        C._SLOT_CONSTANT = True
    assert not any(x["if"] == "o1.colour == 3" for x in d_off["cheapest"]) and (
        b_off is None or b_off[4] != "o1.colour == 3"), ("MF-K3 OFF: offered", d_off["cheapest"])
    print(f"test_slot_constant: pass (MF-K1 'o1.colour == 3' {c.term.name}, OFF refused; MF-K2 "
          f"colour ordered and negative row refused, row < 3 compiles; MF-K3 cheapest that pays of "
          f"{detail['conditions']}, wanted on {link['slots']}, goal target {tgt}; OFF not offered)")


if __name__ == "__main__":
    main()
