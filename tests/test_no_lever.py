"""BUILD 5 ITEM 18, DETECTION (TETHER_NO_LEVER; the reviewer 2026-11-05 r1210, r1212, r1213; Fig 8
:39-42). Per held slot, presses counted per context on Agency; a no_lever row when no action tried
HERE moved it; the moving side's verdict, with a partner no action ever moved, forms TOUCH(partner)
for 16b. Seconds: test_group_row's agent; ls20's shape forced through the step's own two calls
(Agency.note, then _lever_note): a held pair, o1.row moving and o4.row static, o1.row stalling in a
second context.

MF-D1  o4.row pressed under four actions in context F, never moved: a no_lever row on o4.row with
       {action: presses} for those four, level and situation, everywhere True
MF-D2  o1.row, moved under ACTION1 in F: no verdict in F; a slot outside the held goal never
       gets a row, static or not
MF-D3  o1.row stalls under ACTION1 in context S: a no_lever row (here, everywhere False), then
       TOUCH o4 is formed for 16b (row lever_formed), and 16b's formed set holds it
OFF: no row, nothing formed. The red is behavioural: TETHER_NO_LEVER=0 fails MF-D1.

    python tests/test_no_lever.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether
F = (0, (("face", 2), ("@alive", 1)))
S = (0, (("face", 3), ("@alive", 1)))


def press(ag, action, here, moves, slots=("o1.row", "o4.row", "o2.row")):
    """One step's two calls, as tether's step makes them."""
    before = dict.fromkeys(slots, 10)
    after = {s: (11 if s in moves else 10) for s in slots}
    res = dict.fromkeys(slots)
    ag.agency.note(action, ag._moved(res, before, after), sorted(res))
    ag._press_here = dict.fromkeys(ag._hyp["slots"], here)
    ag._lever_note(action, res, before, after)


def rows(ag, event, slot=None):
    return [r for r in ag.led.rows() if r["event"] == event and (slot is None or r["slot"] == slot)]


def run(ag):
    ag._hyp = {"slots": ["o1.row", "o4.row"]}
    for a in ("ACTION1", "ACTION2", "ACTION3", "ACTION4"):
        press(ag, a, F, moves={"o1.row"} if a == "ACTION1" else set())
    press(ag, "ACTION1", F, moves={"o1.row"})
    press(ag, "ACTION1", S, moves=set())                     # o1.row stalls here


def main():
    ag, _atoms, _st = G.agent()
    n0 = len(ag.led.rows())
    run(ag)
    o4 = [r for r in rows(ag, "no_lever", "o4.row")
          if r["detail"]["situation"] == [list(c) for c in F[1]]]
    four = {"ACTION1": 1, "ACTION2": 1, "ACTION3": 1, "ACTION4": 1}
    assert o4 and o4[-1]["detail"]["actions"] == four and o4[-1]["detail"]["everywhere"], (
        "MF-D1: no verdict on the static held slot with its denominator", o4)
    assert len(o4) == 4, ("MF-D1: rewritten other than when a new action was tried", len(o4))
    assert {"level", "situation", "scope"} <= set(o4[-1]["detail"]), o4[-1]

    o1 = rows(ag, "no_lever", "o1.row")
    assert all(r["detail"]["situation"] == [list(c) for c in S[1]] for r in o1) and len(o1) == 1, (
        "MF-D2: a verdict where o1.row moved", o1)
    assert not rows(ag, "no_lever", "o2.row"), "MF-D2: a verdict outside the held goal"

    d = o1[0]["detail"]
    assert d["actions"] == {"ACTION1": 1} and d["everywhere"] is False, ("MF-D3", d)
    formed = rows(ag, "lever_formed", "o1.row")
    said = ag._route_said(tether.IFace.Intent(tether.IFace.TOUCH, object="o4"))
    assert formed and formed[-1]["detail"]["partner"] == "o4.row" and said in ag._formed, (
        "MF-D3: TOUCH o4 not formed for 16b", formed, list(ag._formed))
    ag._goal_static, ag._tried_in = {"o1.row"}, {}           # o1.row static here, as at ls20 c11
    offer = ag._untried_ready(ag.trace[-1][2])
    assert offer is not None and offer[0] == "o1.row" and offer[1] == said, (
        "MF-D3: 16b does not offer the formed TOUCH realised", offer)

    off, _a, _s = G.agent()
    tether._NO_LEVER = False
    try:
        run(off)
    finally:
        tether._NO_LEVER = True
    assert not rows(off, "no_lever") and not rows(off, "lever_formed"), "OFF: a verdict written"
    print(f"test_no_lever: pass (MF-D1 o4.row no lever under {o4[-1]['detail']['actions']}, "
          f"everywhere; MF-D2 none where o1.row moved, none outside the held goal; MF-D3 o1.row "
          f"stalled here {d['actions']} -> {said!r} formed, 16b offers it as {offer[3].action!r}; "
          f"OFF none; "
          f"{len(ag.led.rows()) - n0} rows)")


if __name__ == "__main__":
    main()
