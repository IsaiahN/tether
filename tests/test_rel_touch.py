"""BUILD 5 ITEM 19 Q3 (ii), A RELATION'S ROUTE IS A TOUCH (TETHER_REL_TOUCH; the reviewer 2026-11-05
r1216). A goal hypothesis wanting a declared-derived pair relation true (o0.touches_o2 == 1: the
mover o0 to touch the static o2) is admitted with TOUCH(o2) as its route and held; the TOUCH is
formed for 16b. Seconds: test_group_row's agent, the proposer's candidates narrowed to the one text.

MF-R1  RED FIRST, NAMED: OFF, "o0.touches_o2 == 1" is refused "route first: no slot of it has an
       entry" (read at the proposer's own tally, not inferred); ON it is the pick, held on
       o0.touches_o2 with TOUCH o2's realised action as its route, "TOUCH o2" formed for 16b
MF-R2  "o0.touches_o2 == 0" (the relation wanted false) is refused as before, ON and OFF alike
The red is behavioural: TETHER_REL_TOUCH=0 fails MF-R1's ON half.

    python tests/test_rel_touch.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether


def propose(text: str, on: bool | None):
    """`on` None: the arm as configured (so TETHER_REL_TOUCH=0 turns the ON half red)."""
    ag, _atoms, _st = G.agent()
    before = ag.trace[-1][2]
    assert ag._rel_partner("o0.touches_o2") == "o2" and before.get("o0.touches_o2") == 0, (
        "the panel: o0 does not touch o2")
    ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, {}, None
    ag._inv_conditions = lambda _b: [text]
    was = tether._REL_TOUCH
    tether._REL_TOUCH = was if on is None else on
    try:
        ag._hyp_propose(before)
    finally:
        tether._REL_TOUCH = was
    row = [r for r in ag.led.rows() if r["event"] == "goal_hypotheses"][-1]["detail"]
    return ag, before, row


def main():
    want = "o0.touches_o2 == 1"
    _ag, _b, off = propose(want, on=False)
    assert off.get("pick") is None and off.get("refused") == {
        "route first: no slot of it has an entry": 1}, ("MF-R1 (red first): OFF refusal", off)

    ag, before, on = propose(want, on=None)
    touch = ag.iface.realise(tether.IFace.Intent(tether.IFace.TOUCH, object="o2"),
                             tuple(ag.actions), tether.IFace.Interface.context(ag.env), before,
                             ag.env)
    assert on.get("pick") == want and ag._hyp is not None and ag._hyp["slots"] == [
        "o0.touches_o2"], ("MF-R1: not held", on)
    assert on.get("route") == touch.action, ("MF-R1: the route is not TOUCH o2", on.get("route"))
    said = ag._route_said(tether.IFace.Intent(tether.IFace.TOUCH, object="o2"))
    assert said in ag._formed and any(r["event"] == "lever_formed" for r in ag.led.rows()), (
        "MF-R1: TOUCH o2 not formed for 16b", list(ag._formed))

    for arm in (False, None):
        _a, _b2, neg = propose("o0.touches_o2 == 0", on=arm)
        assert neg.get("pick") is None and neg.get("refused") == {
            "route first: no slot of it has an entry": 1}, ("MF-R2", arm, neg)
    print(f"test_rel_touch: pass (MF-R1 OFF refused {off['refused']}; ON held {want!r}, route "
          f"{on['route']!r} = TOUCH o2, formed for 16b; MF-R2 the relation wanted false refused as "
          f"before, ON and OFF)")


if __name__ == "__main__":
    main()
