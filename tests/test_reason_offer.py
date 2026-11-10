"""RESET_REASON BEFORE THE PRESS (the reviewer 2026-11-07 r1387; TETHER_RESET_REASON): on a live
board only terminal or a routine may press RESET, so untried:goal (16b) is not offered it. A
gridworld agent with RESET added, every action sent on the board (RESET too, as an ARC board opens
with one) and the others known to do nothing (the su15 c47 path: a formed "BECOME OTHER" realised
RESET and the veto refused it), a held hypothesis on a static slot and one formed intent untried
there.

check_untried  _untried_ready's realisation is not RESET, and reason_reset_left_out is booked.
               MUST-FAIL, run: the old offer realises RESET

    python tests/test_reason_offer.py [check ...]
"""
from __future__ import annotations

import collections
import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _agent():
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(3):
        ag.step()
    ag.actions = tuple(ag.actions) + (IFace.RESET,)
    # every action sent on this board, RESET too: an ARC board opens with one (note_sent, C1), so
    # untried's ELICIT reads RESET as mapped -- on gridworld, which opens with none, it would not
    ag.iface.realised_board.setdefault(ag.iface.board_n, set()).update(ag.actions)
    known = ag.iface._known_now
    ag.iface._known_now = lambda a, ctx: known(a, ctx) if a == IFace.RESET else IFace.NO_EFFECT
    before = ag.env.observe()
    sl = sorted(s for s in ag.slots if s in before)[0]
    ag._hyp = {"key": "k", "text": f"{sl} == 1", "slots": [sl], "tkey": ("x == 1", sl, None),
               "cond": None, "source": "library", "shelf": None, "steps": 0, "r0": 1.0,
               "budget": 3, "born": ag.cycle, "displaced": {}, "reads": {}, "seg": {},
               "touches": 0, "losses": 0, "held_unreadable": 0, "acted": collections.Counter(),
               "out0": {sl: 0.0}}
    ag._goal_static = {sl}
    w = IFace.Intent(IFace.ELICIT)
    ag._formed = {ag._route_said(w): (ag.cycle, w)}
    ag._tried_in = {}
    assert ag._alive and ag._attempt_actions > 0, "precondition: live, an attempt under way"
    assert tether._RESET_REASON and tether._A1_CHOOSE, "precondition"
    return ag, before


def _untried():
    ag, before = _agent()
    n0 = ag.gamma.book.get("reason_reset_left_out", 0)
    got = ag._untried_ready(before)
    assert got is not None, "precondition: the formed intent realises"
    return got[3].action, ag.gamma.book.get("reason_reset_left_out", 0) - n0


def _old(fn):
    keep = tether.Agent._reason_offer
    tether.Agent._reason_offer = lambda _self, offered: offered
    try:
        return fn()
    finally:
        tether.Agent._reason_offer = keep


def check_untried() -> None:
    act, booked = _untried()
    assert act != IFace.RESET and booked >= 1, (act, booked)
    old, _ = _old(_untried)
    assert old == IFace.RESET, ("MF: the old offer did not realise RESET", old)
    print(f"  untried:goal realised {act}, booked {booked}; MF, the old offer: {old}")


def main() -> int:
    want = set(sys.argv[1:])
    for c in (check_untried,):
        if not want or c.__name__ in want:
            c()
            print("ok  ", c.__name__)
    print("test_reason_offer OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
