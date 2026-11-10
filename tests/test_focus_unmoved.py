"""BUILD 5 ITEM 19 (d), FOCUS OFF AN UNMOVED SLOT (TETHER_FOCUS_UNMOVED; the reviewer 2026-11-05
r1215, r1216). The mirror of r674 1's indifferent() filter at the focal pick: a slot no press has
moved, under EVERY action available this level (self.actions) each tried on it, leaves the readable
set while a moved one remains. Seconds: test_group_row's agent (gridworld: up, down, left, right),
Agency's own counters set directly.

MF-F1  o4.row tried under all four available actions, never moved; o1.row moved: o4.row is not
       readable for focus, one focus_unmoved row with its denominator, not rewritten the next pick
MF-F2  while any available action is untried on it (left and right only), o4.row is still eligible
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
    assert set(ag.actions) == {"up", "down", "left", "right"}, ("the panel", ag.actions)
    every = {(s, a): 1 for s in R for a in ag.actions}
    counts(ag, every, {("o1.row", "up"): 1})
    got = ag._focus_off_unmoved(list(R))
    rows = [r for r in ag.led.rows() if r["event"] == "focus_unmoved"]
    assert got == ["o1.row"] and len(rows) == 1 and rows[0]["slot"] == "o4.row" and set(rows[0][
        "detail"]["actions"]) == set(ag.actions), ("MF-F1", got, rows)
    ag._focus_off_unmoved(list(R))
    assert len([r for r in ag.led.rows() if r["event"] == "focus_unmoved"]) == 1, (
        "MF-F1: booked again")
    assert ag._focus_off_unmoved(["o4.row"]) == ["o4.row"], "dropped the only readable slot"

    two = {(s, a): 1 for s in R for a in ("left", "right")}
    counts(ag, two, {("o1.row", "left"): 1})
    assert ag._focus_off_unmoved(list(R)) == R, "MF-F2: dropped with up / down untried on it"

    counts(ag, every, {("o1.row", "up"): 1, ("o4.row", "down"): 1})
    assert ag._focus_off_unmoved(list(R)) == R, "MF-F3: not eligible again after it moved"

    counts(ag, every, {("o1.row", "up"): 1})
    tether._FOCUS_UNMOVED = False
    try:
        off = ag._focus_off_unmoved(list(R))
    finally:
        tether._FOCUS_UNMOVED = True
    assert off == R, ("OFF", off)
    print(f"test_focus_unmoved: pass (MF-F1 o4.row off focus under every available action "
          f"{sorted(rows[0]['detail']['actions'])}, booked once; MF-F2 eligible while up / down "
          f"untried; MF-F3 eligible again once moved; the only readable slot kept; OFF as before)")


if __name__ == "__main__":
    main()
