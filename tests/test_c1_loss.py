"""C1 PART 7: A GAME LOSS AS A SHARE, NEVER A BAN (the reviewer 2026-11-09 r1584 (c), r1600), arm
TETHER_GAME_LOSS_SHARE.

  L1  MF: among kinds that lost, 1 loss in 8 presses is in S2's first tier ahead of 1 in 1; OFF
      offers no tier (both carry a vote)
  L2  MF (r1600 Q1): a never-lost pressed kind and an untried kind share the first tier; a kind
      that lost is behind them
  L3  MF (S3): a vetoed press is realised when it is the only one that realises, its why saying
      so; OFF (no Withheld.last) nothing realises
  L4  MF (extinction): a vetoed press taken and survived is lifted (the record kept) and no longer
      withheld; a new game loss on it restores it
  L5  the goal side: a game loss ends the held hypothesis with loss=True; OFF, neutrally
  L6  MF (r1601): ON, a game loss books the shelf record lost 1 and leaves _goal_refuted
      unchanged (it tested the route, not the goal's direction)

    python tests/test_c1_loss.py
"""
from __future__ import annotations

import os
import sys
from collections import Counter

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="c1_loss"), tether.Config(),
                      ledger.Ledger())
    ag.step()
    return ag


def _arm(on: bool):
    keep = tether._GAME_LOSS_SHARE
    tether._GAME_LOSS_SHARE = on
    return keep


def _vote(ag: tether.Agent, slot: str, a: str, losses: int, presses: int) -> None:
    k = ag._press_kind(a, (), slot)
    ag._game_loss_n[k] = losses
    ag._press_n[k] = presses


def check_l1_l2() -> None:
    ag = _agent()
    slot = ag.slots[0]
    a, b, c, d = ag.actions[:4]
    _vote(ag, slot, a, 1, 8)
    _vote(ag, slot, b, 1, 1)
    keep = _arm(True)
    try:
        assert ag._danger_safe(slot, (a, b), ()) == (a,), "MUST-FAIL: 1 in 8 not ahead of 1 in 1"
        _vote(ag, slot, c, 0, 5)
        tier = ag._danger_safe(slot, (a, b, c, d), ())
        assert tier == (c, d), f"MUST-FAIL (Q1): never-lost and untried not one tier: {tier}"
        _arm(False)
        assert ag._danger_safe(slot, (a, b), ()) == ()
    finally:
        _arm(keep)
    print(f"  L1: 1 in 8 ({a}) ahead of 1 in 1 ({b}); OFF no tier between two voted kinds")
    print(f"  L2: never-lost pressed ({c}) and untried ({d}) share the first tier")


def check_l3() -> None:
    ag = _agent()
    env, iface = ag.env, ag.iface
    fp = IFace.fingerprint(env, env.observe())[0]
    a, b = ag.actions[:2]
    real = iface._choose

    def only_a(_intent, offered, *_args, **_kw):
        return IFace.Realisation(action=a, mode="test", why="test") if a in offered else None
    iface._choose = only_a
    try:
        want = IFace.Intent(IFace.ELICIT)
        held = frozenset({(a, None)})
        r = iface.realise(want, (a, b), (), env.observe(), env, IFace.Withheld(fp, held, last=held))
        assert r is not None and r.action == a and IFace.VETO_ORDERED in r.why, r
        r0 = iface.realise(want, (a, b), (), env.observe(), env, IFace.Withheld(fp, held))
        assert r0 is None, f"OFF realised a withheld press: {r0}"
    finally:
        iface._choose = real
    print(f"  L3: the vetoed {a} is realised last when nothing else realises ({r.why!r}); "
          f"OFF none")


def check_l4() -> None:
    ag = _agent()
    keep = _arm(True)
    try:
        fp, a = "fp0", ag.actions[0]
        key = (fp, a, None)
        ag._vetoes.add(key)
        ag._veto_taken = key
        ag._veto_lift()
        assert key in ag._vetoes and key in ag._veto_lifted, "MUST-FAIL: survived, not lifted"
        assert [r for r in ag.led.rows() if r["event"] == "veto_lifted"]
        ag._ruin_step = (fp, None, a, None, ag.cycle)
        ag._ending_counted = None
        ag._note_ending("game_loss", "s")
        assert key not in ag._veto_lifted, "a new game loss did not restore the veto"
    finally:
        _arm(keep)
    print("  L4: taken and survived: lifted (the record kept, row veto_lifted); lost on again: "
          "restored")


def check_l5() -> None:
    for on in (True, False):
        ag = _agent()
        seen = {}

        def end(why, loss=False, _s=seen, **_kw):
            _s.update(why=why, loss=loss)
        ag._hyp_end = end
        ag._hyp = {"held": True}
        keep = _arm(on)
        try:
            ag.retarget(ag.env, ag.level, how="game_loss")
        finally:
            _arm(keep)
        if tether._GOAL_HYP:
            assert seen.get("loss") is on, (on, seen)
    print("  L5: a game loss ends the held hypothesis loss=True ON, neutrally OFF")


def _held(ag: tether.Agent) -> None:
    """A held goal hypothesis with a shelf entry, in the shape _goal_hypothesis builds it."""
    ag._goal_shelf["sh"] = {"record": {"won": 0, "lost": 0}}
    ag._hyp = {"key": "k", "text": "o0.row < 3", "slots": [ag.slots[0]],
               "tkey": ("o0.row < 3",), "cond": None, "source": "sh", "shelf": "sh",
               "steps": 1, "r0": 1.0, "budget": 4, "born": 0, "displaced": {}, "reads": {},
               "seg": {}, "touches": 0, "losses": 0, "held_unreadable": 0, "acted": Counter()}


def check_l6() -> None:
    """r1601: ON, a game loss books the shelf record lost and leaves the goal's sign unrefuted
    (a loss on the way tests the route; only arriving tests the direction)."""
    if not tether._GOAL_HYP:
        print("  L6: skipped, TETHER_GOAL_HYPOTHESES OFF")
        return
    ag = _agent()
    _held(ag)
    keep = _arm(True)
    try:
        ag.retarget(ag.env, ag.level, how="game_loss")
    finally:
        _arm(keep)
    assert ag._goal_shelf["sh"]["record"]["lost"] == 1, ag._goal_shelf["sh"]
    assert not ag._goal_refuted, f"MUST-FAIL (r1601): a game loss refuted the goal's sign: " \
                                 f"{ag._goal_refuted}"
    print("  L6: ON, a game loss books the shelf record lost 1 and leaves _goal_refuted empty")


def main() -> int:
    check_l1_l2()
    check_l3()
    check_l4()
    check_l5()
    check_l6()
    print("c1_loss: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
