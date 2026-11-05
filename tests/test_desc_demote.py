"""BUILD 5 ITEM 19 (a) + (b): DEMOTION BY THE DESCRIPTION, AND WHAT A STALL SURFACED
(TETHER_DESC_DEMOTE, TETHER_STALL_SURFACE; the reviewer 2026-11-05 r1227). A stall is evidence
against the held family under the readings that held, on this board; what it surfaced becomes this
board's readings, seeded toward the family that does not need what failed; one price, no branch.
Seconds: test_board_desc's played gridworld agent (avatar o0; o2, o3, o4 never move).

MF-D1  two navigate shapes stall under avatar: navigate's price rises above placement's, and two
       family_demoted rows carry the losses
MF-D2  the board's record cleared (new_board's call): navigate's price is back to the seed's
MF-D3  a win restores: after the losses, a won navigate shape lowers navigate's price again
MF-S1  RED FIRST, ls20's shape: X "o0.row == o4.row" (o4 static under every press, never touched)
       stalls; stall_untouched / stall_unmoved surface and the next proposal, over a navigate X2
       and a contact C "o0.touches_o2 == 1" on one mv tier, holds C by the price. OFF (both arms):
       X2 is held
MF-S2  with the record against contact on this board (C stalled too), contact falls back and the
       next proposal holds the navigate shape over a second contact shape, by the same price
The red is behavioural: TETHER_STALL_SURFACE=0 fails MF-S1; TETHER_DESC_DEMOTE=0 fails MF-D1.

    python tests/test_desc_demote.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_board_desc as B  # noqa: E402

tether = B.tether
X, X2, X3 = "o0.row == o4.row", "o0.col == o3.col", "o0.row == o2.row"
C, C2 = "o0.touches_o2 == 1", "o0.touches_o3 == 1"


def propose(ag, texts: list) -> dict:
    before = ag.trace[-1][2]
    ag.wants.clear()
    ag._hyp, ag._hyp_exhausted = None, None
    ag._inv_conditions = lambda _b: list(texts)
    ag._hyp_route = lambda *_a: "a route"
    ag._route_first_set = lambda _b: None
    was = tether._GROUP_PROPOSE
    tether._GROUP_PROPOSE = False
    try:
        ag._hyp_propose(before)
    finally:
        tether._GROUP_PROPOSE = was
    return [r for r in ag.led.rows() if r["event"] == "goal_hypotheses"][-1]["detail"]


def demoted(ag) -> list:
    return [r["detail"] for r in ag.led.rows() if r["event"] == "family_demoted"]


def s1_off() -> dict:
    """MF-S1's red: both arms OFF, the same stall and the same two candidates."""
    was = tether._STALL_SURFACE, tether._DESC_DEMOTE
    tether._STALL_SURFACE = tether._DESC_DEMOTE = False
    try:
        ag = B.played()
        propose(ag, [X])
        B.stall(ag)
        return propose(ag, [X2, C])
    finally:
        tether._STALL_SURFACE, tether._DESC_DEMOTE = was


def main():
    off = s1_off()
    assert off.get("pick") == X2, ("MF-S1 (red first): OFF", off)
    ag = B.played()
    b = ag.trace[-1][2]
    assert b["o0.row"] != b["o4.row"] and b["o0.col"] != b["o3.col"] and b["o0.touches_o2"] == 0, (
        "the panel")
    seed = ag._desc_prior(["avatar"])
    n0 = len(demoted(ag))          # the played board's own stalls are its record, not the fixture's
    for t in (X, X2):
        a = propose(ag, [t])
        assert a.get("pick") == t, ("MF-D1: not held", t, a)
        B.stall(ag)
    rows = demoted(ag)[n0:]
    after = ag._desc_prior(["avatar"])
    assert len(rows) == 2 and all(r["family"] == "navigate" for r in rows) and (
        rows[-1]["losses"]["avatar"] == 2), ("MF-D1: rows", rows)
    assert after["navigate"] > after["placement"] and after["navigate"] > seed["navigate"], (
        "MF-D1: navigate not demoted", seed, after)

    a = propose(ag, [X3])
    assert a.get("pick") == X3, ("MF-D3: X3 not held", a)
    ag._hyp_end("level_cleared", won=True)
    won = ag._desc_prior(["avatar"])
    assert won["navigate"] < after["navigate"], ("MF-D3: a win did not restore", after, won)
    ag._desc_board()
    assert ag._desc_prior(["avatar"])["navigate"] < won["navigate"], "MF-D2: the board's losses"

    ag = B.played()
    a = propose(ag, [X])
    assert a.get("pick") == X
    B.stall(ag)
    s = demoted(ag)[-1]
    assert {"stall_untouched", "stall_unmoved"} <= set(s["surfaced"]), ("MF-S1: surfaced", s)
    s1 = propose(ag, [X2, C])
    fam = {x["if"]: x["bits"] for x in s1["ranked"]}
    assert s1.get("pick") == C and fam[C] < fam[X2], ("MF-S1: contact not held", s1)
    assert {"stall_untouched", "stall_unmoved"} <= set(s1["desc"]["holding"]), s1["desc"]

    B.stall(ag)
    s2 = propose(ag, [X2, C2])
    assert s2.get("pick") == X2 and s2["desc"]["prior"]["contact"] > s1["desc"]["prior"][
        "contact"], ("MF-S2: contact did not fall back", s1["desc"], s2)
    print(f"test_desc_demote: pass (MF-D1 navigate {seed['navigate']} -> {after['navigate']} bits "
          f"over placement {after['placement']}; D3 a win -> {won['navigate']}; D2 the board's "
          f"record cleared; MF-S1 surfaced {s['surfaced']}, {C!r} held at {fam[C]} bits over "
          f"{X2!r} {fam[X2]} (OFF: {off['pick']!r}); MF-S2 contact "
          f"{s1['desc']['prior']['contact']} -> {s2['desc']['prior']['contact']}, {X2!r} held)")


if __name__ == "__main__":
    main()
