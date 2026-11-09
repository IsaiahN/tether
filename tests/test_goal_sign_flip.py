"""G CONTENT, GOAL_SIGN_FLIP (the reviewer 2026-11-01 r744, r745), on the gridworld fixture.

  An ordered goal ended "arrived_no_clear" (loss, not won) refutes its (subject, sign) for this
  board; an "==" goal refutes nothing by sign (it is refused next as tried this level); a stalled
  goal refutes nothing; a game loss keeps the refutations and a new_board boundary clears them; with
  the arm OFF nothing is refuted (the must-fail). _goal_sign reads only "<" and ">".

    python tests/test_goal_sign_flip.py
"""
from __future__ import annotations

import os
import sys
from collections import Counter

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    env = world.bind(gridworld.family("default", 0))
    return env, tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                             ledger.Ledger())


def _end(ag, text: str, why: str, loss: bool, n: int):
    ag._hyp = {"key": f"@t{n}", "displaced": {}, "steps": 2, "touches": 1,
               "tkey": (text, "s", None), "text": text, "shelf": None,
               "slots": [text.split()[0]], "source": "library",
               "held_unreadable": 0, "losses": 0, "reads": {}, "seg": {}, "acted": Counter(),
               "tests": {}}
    ag._hyp_end(why, loss=loss)


def main():
    import tether
    assert tether._GOAL_SIGN_FLIP, "the arm is ON by default"
    assert tether._goal_sign("o40.row > o25.row") == ("o40.row", ">")
    assert tether._goal_sign("o0.rem_n < o14.rem_n") == ("o0.rem_n", "<")
    assert tether._goal_sign("o33.colour == o19.colour") is None
    env, ag = _agent()
    _end(ag, "o40.row > o25.row", "arrived_no_clear", True, 1)
    _end(ag, "o33.colour == o19.colour", "arrived_no_clear", True, 2)
    _end(ag, "o0.rem_n < o14.rem_n", "stalled", False, 3)
    assert ag._goal_refuted == {("o40.row", ">")}, ag._goal_refuted
    ag.retarget(env, ag.level, how="game_loss")
    assert ag._goal_refuted == {("o40.row", ">")}, "a game loss keeps the refutations"
    ag.retarget(env, ag.level, how=tether.NEW_BOARD)
    assert not ag._goal_refuted, "a new board's refutations start empty"
    tether._GOAL_SIGN_FLIP = False
    try:
        _e, ag2 = _agent()
        _end(ag2, "o40.row > o25.row", "arrived_no_clear", True, 4)
    finally:
        tether._GOAL_SIGN_FLIP = True
    assert not ag2._goal_refuted, ("must-fail: refuted with the arm OFF", ag2._goal_refuted)
    print("test_goal_sign_flip: an arrived ordered goal refutes its sign; == and stalled goals do "
          "not; kept at game loss, cleared at new_board; nothing with the arm OFF")


if __name__ == "__main__":
    main()
