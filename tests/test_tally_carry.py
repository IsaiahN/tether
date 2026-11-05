"""BUILD 5 ITEM 20, THE TALLIES CARRY (TETHER_TALLY_CARRY; the reviewer 2026-11-05 r1232 Q1, Q2).
At a clear credited to a held shape's family Y, a tally record joins the ONE M7 path: (reading, Y)
won, and this board's stall losses (reading, X), X != Y -- a loss crosses only when the ground
witnessed the contrast. On load the next agent's prior moves by the same p. Seconds:
test_desc_demote's played gridworld agent (avatar o0).

MF-C6  RED FIRST: X "o0.row == o4.row" (navigate) stalls, then Y "o1.colour == o3.colour"
       (placement) is held through a clear: one tally record carries (avatar, placement) won and
       (avatar, navigate) lost. OFF: no tally record. A board that stalls X and never clears
       carries no record
MF-C7  a fresh agent loads the record: under "avatar" navigate is dearer and placement cheaper
       than on an agent that loaded nothing, by the same p; the invention_carried row names it
MF-C3  the won tally moves the prior on its own: a record with wins only lowers placement
The red is behavioural: TETHER_TALLY_CARRY=0 fails MF-C6.

    python tests/test_tally_carry.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_board_desc as B  # noqa: E402
import test_desc_demote as D  # noqa: E402

tether = B.tether
X, Y = "o0.row == o4.row", "o1.colour == o3.colour"


def tallies(ag) -> list:
    return [r for r in ag._inv_carry if r.get("kind") == "tally"]


def board(clear: bool, on: bool | None = None) -> list:
    was = tether._TALLY_CARRY
    tether._TALLY_CARRY = was if on is None else on
    try:
        ag = B.played()
        assert D.propose(ag, [X]).get("pick") == X, "the hold of X"
        B.stall(ag)
        n0 = len(tallies(ag))
        if clear:
            assert D.propose(ag, [Y]).get("pick") == Y, "the hold of Y"
            ag._hyp_end("level_cleared", won=True)
        return tallies(ag)[n0:]
    finally:
        tether._TALLY_CARRY = was


def loaded(recs: list) -> tuple:
    ag = B.played()
    base = ag._desc_prior(["avatar"])
    ag._reinvent_carried(recs)
    row = [r for r in ag.led.rows() if r["event"] == "invention_carried"][-1]["detail"]
    return base, ag._desc_prior(["avatar"]), row


def main():
    assert board(True, on=False) == [], "MF-C6 (red first): OFF tallied"
    recs = board(True)
    assert len(recs) == 1, ("MF-C6: one tally record", recs)
    t = recs[0]
    assert ["avatar", "placement", 1] in t["won"] and ["avatar", "navigate", 1] in t["lost"], (
        "MF-C6: the contrast", t)
    assert board(False) == [], "MF-C6: a board that never cleared carried a loss"

    base, after, row = loaded(recs)
    assert after["navigate"] > base["navigate"] and after["placement"] < base["placement"], (
        "MF-C7: the prior did not move", base, after)
    assert row.get("tallied") == [t["name"]], ("MF-C7: the row", row)

    wins = [{**t, "name": "wins_only", "lost": []}]
    _b, w_after, _r = loaded(wins)
    assert w_after["placement"] < base["placement"] and w_after["navigate"] == base["navigate"], (
        "MF-C3: wins alone", base, w_after)
    print(f"test_tally_carry: pass (MF-C6 OFF none; won {t['won']} lost {t['lost']}; never "
          f"cleared: none; MF-C7 avatar navigate {base['navigate']} -> {after['navigate']}, "
          f"placement {base['placement']} -> {after['placement']}; MF-C3 wins alone placement "
          f"-> {w_after['placement']})")


if __name__ == "__main__":
    main()
