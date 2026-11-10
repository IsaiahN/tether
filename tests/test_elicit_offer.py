"""41 (3) AT EVERY ELICIT OFFER (the reviewer 2026-11-07 r1386; TETHER_ELICIT_NO_REFUSED): on a live
board a RESET offered to ELICIT is refused by RESET_REASON, so it is never pressed, its destination
stays unrecorded, and Design A's reach reads it 1 against a known no-change's 0: it wins again. A
gridworld agent with RESET added to its actions, every other action realised here and known to do
nothing, so ELICIT reaches the chooser with RESET the one option reading a reach.

check_orient   the orient reflex fires on a grown slot: its realised action is not RESET, and
               elicit_reset_left_out is booked. MUST-FAIL, run: the old offer realises RESET
check_unaimed  the step's unaimed re-realise (r669 1), ELICIT over the unpositioned actions: not
               RESET. MUST-FAIL, run: the old offer realises RESET

    python tests/test_elicit_offer.py [check ...]
"""
from __future__ import annotations

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
    """Every action but RESET realised here and known to do nothing, so ELICIT reaches Design A's
    chooser, where a live RESET (never pressed, its destination unrecorded) reads reach 1 against
    0 -- the su15 path (c20: orient's RESET, refused)."""
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(3):
        ag.step()
    ag.actions = tuple(ag.actions) + (IFace.RESET,)
    ag.iface.realised_board.setdefault(ag.iface.board_n, set()).update(
        a for a in ag.actions if a != IFace.RESET)
    known = ag.iface._known_now
    ag.iface._known_now = lambda a, ctx: known(a, ctx) if a == IFace.RESET else IFace.NO_EFFECT
    assert ag._alive and ag._attempt_actions > 0, "precondition: live, an attempt under way"
    assert tether._ELICIT_NO_REFUSED and tether._RESET_REASON and tether._A1_CHOOSE, "precondition"
    return ag


def _old(fn):
    keep = tether.Agent._elicit_offer
    tether.Agent._elicit_offer = lambda _self, offered: offered
    try:
        return fn()
    finally:
        tether.Agent._elicit_offer = keep


def _orient():
    ag = _agent()
    ag._rf_out = dict.fromkeys(ag._rf_out, 0.0)
    n0 = ag.gamma.book.get("elicit_reset_left_out", 0)
    ag._reflex(ag.env.observe())
    rows = [r["detail"] for r in ag.led.rows()
            if r["event"] == "reflex" and r["detail"]["form"] == "orient"]
    assert rows and rows[-1]["fired"], ("precondition: orient fires", rows[-1:])
    return rows[-1]["action"], ag.gamma.book.get("elicit_reset_left_out", 0) - n0


def check_orient() -> None:
    act, booked = _orient()
    assert act != IFace.RESET and booked >= 1, (act, booked)
    old, _ = _old(_orient)
    assert old == IFace.RESET, ("MF: the old offer did not realise RESET", old)
    print(f"  orient fired: {act}, booked {booked}; MF, the old offer: {old}")


def _unaimed():
    # the step's unaimed re-realise (r669 1), as its site calls it: ELICIT over the unpositioned
    ag = _agent()
    offer = ag._elicit_offer(tuple(a for a in ag.actions if a not in IFace.POSITIONED))
    r = ag.iface.realise(IFace.Intent(IFace.ELICIT), offer, IFace.Interface.context(ag.env),
                         ag.env.observe(), ag.env, withheld=ag._withheld)
    return r.action


def check_unaimed() -> None:
    act = _unaimed()
    assert act != IFace.RESET, act
    old = _old(_unaimed)
    assert old == IFace.RESET, ("MF: the old offer did not realise RESET", old)
    print(f"  unaimed re-realise: {act}; MF, the old offer: {old}")


def main() -> int:
    want = set(sys.argv[1:])
    for c in (check_orient, check_unaimed):
        if not want or c.__name__ in want:
            c()
            print("ok  ", c.__name__)
    print("test_elicit_offer OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
