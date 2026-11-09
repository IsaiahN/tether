"""C1 BOARD_UNTRIED (the reviewer 2026-11-01 r725-r728; Isaiah 18:00): "untried" is read on THIS
board, and the record lives in the interface; the agent reads a count.

On the gridworld fixture: every offered non-RESET action starts untried; presses bring the count to
zero; a game loss keeps it, a new_board boundary (the agent's situate(new_board=True)) brings every
action back; and realise(ELICIT) then takes an action the game series' table already maps as
unmapped, so System 0's untried-first rule fires on the second board of a game series. The seam:
tether.py names no action and keeps no action-keyed store for this (grepped from the diff, not
asserted here). 
    python tests/test_board_untried.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")


def main():
    import gamma
    import gridworld
    import interface as IFace
    import ledger
    import tether
    import world
    assert IFace._BOARD_UNTRIED, "the arm is ON by default"
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    offered = tuple(a for a in ag.actions if a != IFace.RESET)
    assert offered and ag._board_untried_n() == len(offered), (ag._board_untried_n(), offered)
    for _ in range(12):
        ag.step()
    left = ag._board_untried_n()
    assert left < len(offered), ("occasions: no press reached the record", left)
    mapped = [a for a in offered if a in ag.iface.table]
    assert mapped, "occasions: the life's table maps an action"
    ag.retarget(env, ag.level, how="game_loss")
    assert ag._board_untried_n() == left, "a game loss is not a new board"
    ag.retarget(env, ag.level, how=tether.NEW_BOARD)
    assert ag._board_untried_n() == len(offered), "a new board's buttons are untried again"
    r = ag.iface.realise(IFace.Intent(IFace.ELICIT), offered, IFace.Interface.context(env),
                         env.observe(), env)
    assert r is not None and r.action in ag.iface.table and r.unmapped, r
    print(f"test_board_untried: {len(offered)} offered, {len(offered) - left} pressed on board 1, "
          f"kept at game loss, all untried again at new_board; ELICIT takes mapped {r.action} as "
          f"unmapped")


if __name__ == "__main__":
    main()
