"""BUILD 5 ITEM 19 Q2, A SLOTLESS GOAL'S TOUCH (TETHER_SLOTLESS_TOUCH; the reviewer 2026-11-05
r1216, r1217). A completion-held goal that names no slot (count NONE, connected) gets TOUCH
intents through 16b's formed / tried machinery, keyed (goal key, situation), offered when no
hypothesis drives. Seconds: test_group_row's agent, its own state, the held goals planted as the
completion holds them.

MF-S1  count NONE of the held kind: _untried_ready offers TOUCH on a present member, its
       lever_formed row reads as an ATTEMPT; once taken (untried_intent, slotless) the next offer
       in the same situation is a DIFFERENT member
MF-S2  connected(o0, o2) with o2 joined to no chain: TOUCH o2 is offered; a held hypothesis takes
       the 16b path as before (no slotless offer)
OFF: no slotless offer. The red is behavioural: TETHER_SLOTLESS_TOUCH=0 fails MF-S1.

    python tests/test_slotless_touch.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether
C = G.C


def main():
    ag, atoms, st = G.agent()
    before = ag.trace[-1][2]
    kind = ag._kind("o0")
    ag._hyp = None
    ag._slotless = {"@none": tether._Count(parts=(), kinds=(kind,), check=ag._count_holds)}
    got = ag._untried_ready(before)
    assert got is not None and got[0] == "@none" and got[1].startswith("TOUCH o"), ("MF-S1", got)
    first = got[1]
    formed = [r for r in ag.led.rows() if r["event"] == "lever_formed"]
    assert formed and formed[-1]["detail"]["reads"].startswith("an attempt"), (
        "MF-S1 attempt", formed)
    ag._untried_best = got
    ag._untried_take()
    took = [r for r in ag.led.rows() if r["event"] == "untried_intent"][-1]
    assert took["detail"].get("slotless") and took["detail"]["intent"] == first, took
    nxt = ag._untried_ready(before)
    assert nxt is not None and nxt[1] != first, ("MF-S1: the same member offered again", nxt)

    conn = C.compile_candidate({"condition": "connected(o0, o2) == 1"}, atoms)
    assert C.connected(before, "o0", "o2") == 0, "the panel: o2 joins o0's chain"
    ag2, _a, _s = G.agent()
    ag2._hyp = None
    ag2._slotless = {"@conn": tether._Connect((conn,))}
    got2 = ag2._untried_ready(ag2.trace[-1][2])
    assert got2 is not None and got2[1] == "TOUCH o2", ("MF-S2", got2)
    ag2._hyp = {"slots": ["o0.row"]}
    held = ag2._untried_ready(ag2.trace[-1][2])
    assert held is None or held[0] != "@conn", ("MF-S2: slotless offered under a hypothesis", held)

    ag3, _a, _s = G.agent()
    ag3._hyp = None
    ag3._slotless = {"@none": tether._Count(parts=(), kinds=(kind,), check=ag3._count_holds)}
    tether._SLOTLESS_TOUCH = False
    try:
        off = ag3._untried_ready(ag3.trace[-1][2])
    finally:
        tether._SLOTLESS_TOUCH = True
    assert off is None, ("OFF", off)
    print(f"test_slotless_touch: pass (MF-S1 {first!r} offered as an attempt, then {nxt[1]!r}; "
          f"MF-S2 {got2[1]!r} for the missing link, none under a hypothesis; OFF none)")


if __name__ == "__main__":
    main()
