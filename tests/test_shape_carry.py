"""BUILD 5 ITEM 20 PART 1, A SHAPE CARRIES AS ITS METHOD (TETHER_SHAPE_CARRY; the reviewer
2026-11-05 r1231, r1232; Fig 4 :22-24). A held completion goal's parts are shelved as their METHOD
form through the ONE M7 path (_goal_templates -> _shelve_one -> _inv_carry), with the reads a
form's text does not name, and re-invented on load by _reinvent_carried. Seconds: test_group_row's
agent and its private library; a second, fresh agent loads what the first shelved.

MF-C1  RED FIRST: a group "ALL kind(o5): o5.row == o1.row", an order "o0.row == o4.row then
       o0.col == o4.col" and a count "NONE of kind EXTENT remain" (reads came/gone) each shelve a
       METHOD form ("ALL kind({o}): {o}.row == {x}.row", ...) and each re-invents on a fresh agent,
       none refused. OFF: no template, nothing carried
MF-C4  a constant "o3.colour == 2" is refused by carry_check: no template, it stays in-game
(Connected is not carried yet: "connected" is no library reading, so carry_check refuses its form.)
The red is behavioural: TETHER_SHAPE_CARRY=0 fails MF-C1.

    python tests/test_shape_carry.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether
SHAPES = [("ALL kind(o5): o5.row == o1.row", "ALL kind({o}): {o}.row == {x}.row", None),
          ("o0.row == o4.row then o0.col == o4.col",
           "{o}.row == {x}.row then {o}.col == {x}.col", None),
          ("NONE of kind EXTENT remain", "NONE of kind EXTENT remain", ["came", "gone"])]
CONSTANT = "o3.colour == 2"


def shelve(ag, text: str, reads: list | None, n: int) -> list:
    """The write path a completion takes: _goal_templates, then _shelve_one."""
    lib = ag._inv_library()
    key = f"t_goal_{n}"
    ag._goal_text[key] = text
    ag._goal_meta[key] = {"met_state": "after", "level": ag.level, "parts": [text],
                          "templates": ag._goal_templates([text], {}, lib), "affects": []}
    if reads and tether._SHAPE_CARRY:
        ag._goal_meta[key]["reads"] = reads
    k0 = len(ag._inv_carry)
    ag._shelve_one(key, "test", {"won": 1, "lost": 0}, "test")
    return ag._inv_carry[k0:]


def carry(on: bool | None) -> tuple:
    was = tether._SHAPE_CARRY
    tether._SHAPE_CARRY = was if on is None else on
    try:
        ag, _atoms, _st = G.agent()
        rows = [r for i, (t, _f, rd) in enumerate(SHAPES) for r in shelve(ag, t, rd, i)]
        const = shelve(ag, CONSTANT, None, 9)
        ag2, _a2, _s2 = G.agent()
        got = ag2._reinvent_carried(rows) if rows else {"reinvented": 0, "refused": 0}
        last = [r for r in ag2.led.rows() if r["event"] == "invention_carried"]
        return rows, const, got, (last[-1]["detail"] if last else {})
    finally:
        tether._SHAPE_CARRY = was


def main():
    off, _c, _g, _d = carry(False)
    assert off == [], ("MF-C1 (red first): OFF carried", off)

    rows, const, got, detail = carry(None)
    forms = [r["template"] for r in rows]
    assert forms == [f for _t, f, _r in SHAPES], ("MF-C1: the method forms", forms)
    assert rows[2].get("reads") == ["came", "gone"], ("MF-C1: the count's reads", rows[2])
    names = [r["name"] for r in rows]
    assert detail.get("refused") == [] and set(names) <= set(detail.get("reinvented", [])), (
        "MF-C1: not re-invented", detail)
    assert const == [], ("MF-C4: a constant carried", const)
    print(f"test_shape_carry: pass (MF-C1 OFF none; ON {forms} shelved and re-invented "
          f"{got['reinvented']} (axis forms included), refused {detail.get('refused')}; MF-C4 "
          f"{CONSTANT!r} not carried)")


if __name__ == "__main__":
    main()
