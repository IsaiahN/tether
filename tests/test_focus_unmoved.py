"""BUILD 5 ITEM 19 (d), FOCUS OFF AN UNMOVED SLOT (TETHER_FOCUS_UNMOVED; the reviewer 2026-11-05
r1215). The mirror of r674 1's indifferent() filter at the focal pick: a slot no press has moved,
under EVERY action the agent has tried (at least two), leaves the readable set while a moved one
remains. Seconds: test_group_row's agent, Agency's own counters set directly.

MF-F1  o4.row tried under ACTION1 and ACTION2, never moved; o1.row moved: o4.row is not readable for
       focus, one focus_unmoved row with its denominator, not rewritten on the next pick
MF-F2  after ONE action tried, o4.row is still eligible
MF-F3  the step after o4.row moves, it is eligible again
And when every readable slot is unmoved, nothing is dropped. OFF: as before.
The red is behavioural: TETHER_FOCUS_UNMOVED=0 fails MF-F1.

    python tests/test_focus_unmoved.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether
R = ["o1.row", "o4.row"]


def counts(ag, tried: dict, moved: dict) -> None:
    ag.agency.tried.clear()
    ag.agency.moved.clear()
    ag.agency.tried.update(tried)
    ag.agency.moved.update(moved)


def main():
    ag, _atoms, _st = G.agent()
    two = {("o1.row", "ACTION1"): 2, ("o1.row", "ACTION2"): 1,
           ("o4.row", "ACTION1"): 2, ("o4.row", "ACTION2"): 1}
    counts(ag, two, {("o1.row", "ACTION1"): 2})
    got = ag._focus_off_unmoved(list(R))
    rows = [r for r in ag.led.rows() if r["event"] == "focus_unmoved"]
    assert got == ["o1.row"] and len(rows) == 1 and rows[0]["slot"] == "o4.row" and rows[0][
        "detail"]["actions"] == {"ACTION1": 2, "ACTION2": 1}, ("MF-F1", got, rows)
    ag._focus_off_unmoved(list(R))
    assert len([r for r in ag.led.rows() if r["event"] == "focus_unmoved"]) == 1, (
        "MF-F1: booked again")
    assert ag._focus_off_unmoved(["o4.row"]) == ["o4.row"], "dropped the only readable slot"

    counts(ag, {("o1.row", "ACTION1"): 2, ("o4.row", "ACTION1"): 2}, {("o1.row", "ACTION1"): 2})
    assert ag._focus_off_unmoved(list(R)) == R, "MF-F2: dropped after one action tried"

    counts(ag, two, {("o1.row", "ACTION1"): 2, ("o4.row", "ACTION2"): 1})
    assert ag._focus_off_unmoved(list(R)) == R, "MF-F3: not eligible again after it moved"

    counts(ag, two, {("o1.row", "ACTION1"): 2})
    tether._FOCUS_UNMOVED = False
    try:
        off = ag._focus_off_unmoved(list(R))
    finally:
        tether._FOCUS_UNMOVED = True
    assert off == R, ("OFF", off)
    print(f"test_focus_unmoved: pass (MF-F1 o4.row off focus under "
          f"{rows[0]['detail']['actions']}, booked once; MF-F2 eligible after one action; MF-F3 "
          f"eligible again once moved; the only readable slot kept; OFF as before)")


if __name__ == "__main__":
    main()
