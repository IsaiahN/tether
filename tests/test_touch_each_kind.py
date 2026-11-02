"""C2 FINISH (the reviewer 2026-11-01 r736, r741): TOUCH_EACH_KIND and S0_BEFORE_BORED on the
gridworld fixture.

  TOUCH_EACH_KIND: on a fresh board the untouched kinds are listed rarest first, System 0 is active
  while one remains, and the hold ENDS within the board's own bound (offered actions + kinds + a
  slack of the same size) -- also on this world, whose actions are not positioned, so a TOUCH the
  interface cannot realise must still mark its object tried.
  S0_BEFORE_BORED: with the drive bored and no starved aim, choose() does not fall to the bored
  probe while TRY_FIRST is open; with the arm OFF it does (the must-fail).

    python tests/test_touch_each_kind.py
"""
from __future__ import annotations

import os
import sys

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


def main():
    import tether
    assert tether._TOUCH_EACH_KIND and tether._S0_BEFORE_BORED, "both arms ON by default"
    env, ag = _agent()
    ag.step()
    kinds = ag._untouched_kinds(env.observe())
    assert kinds, "occasions: no untouched kind on the fixture"
    assert [len(k) for k in kinds] == sorted(len(k) for k in kinds), ("rarest first", kinds)
    assert ag._system0_active(), "System 0 inactive with a kind untouched"
    bound = 2 * (len(ag.actions) + len(kinds))
    n = 0
    while ag._try_first_open() and n < bound:
        ag.step()
        n += 1
    assert not ag._try_first_open(), ("the hold did not end within the board's bound", n, bound,
                                      ag._untouched_kinds(env.observe()))
    # S0_BEFORE_BORED: a bored drive and no starved aim, TRY_FIRST open (a fresh board)
    for arm_on in (True, False):
        env2, ag2 = _agent()
        tether._S0_BEFORE_BORED = arm_on
        try:
            ag2.drive.bored = lambda: True
            ag2._aims = lambda: set()
            assert ag2._try_first_open(), "occasions: TRY_FIRST not open on a fresh board"
            _act, by = ag2.choose(env2.observe())
        finally:
            tether._S0_BEFORE_BORED = True
        if arm_on:
            assert by != "probe", ("bored probe took the turn while TRY_FIRST was open", by)
        else:
            assert by == "probe", ("must-fail: with the arm OFF a bored drive takes the probe", by)
    print(f"test_touch_each_kind: {len(kinds)} kinds untouched at start, rarest first; the hold "
          f"ended after {n} steps (bound {bound}); bored + TRY_FIRST open -> not the probe "
          f"(OFF -> probe)")


if __name__ == "__main__":
    main()
