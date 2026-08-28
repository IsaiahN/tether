"""The holdout runner. SEAT-SIDE — the agent does not import this.

One game, played LOCALLY. `arc_agi`'s `NORMAL` mode downloads once and hands back a
`LocalEnvironmentWrapper`, so *get it from the API* and *play locally, fast* are one path and
not two. No key is required: an anonymous one is fetched automatically, which keeps a run
reproducible by anyone reading the repo rather than dependent on an account.

**NOT RUN BY `conform/check.py`.** It needs the network and it downloads content; the checkers
must stay offline and deterministic.

WHAT IS AND IS NOT IN THIS FILE. A game IDENTIFIER is a public name and is here. Nothing about
any game's mechanics is, and nothing read from a downloaded file enters the atom set, the
priors, the grammar or a decision — `environment_files/` is gitignored AND excluded from the
linter, because gitignore keeps content out of commits and does nothing about tools that walk
the tree.
"""
from __future__ import annotations

import collections
import logging
import sys

import arc_atoms
import arc_percept
import arc_predict
import arc_run
import gamma
import gate
import ledger
import tether
from arc_world import ArcWorld

sys.dont_write_bytecode = True


def play(game: str = "ls20", cycles: int = 40) -> dict:
    """Download one game, run the loop on it, and report where the chain stops."""
    logging.disable(logging.INFO)
    from arc_agi import Arcade
    from arc_agi.base import OperationMode

    arc = Arcade(operation_mode=OperationMode.NORMAL)
    w = arc.make(game)
    if w is None:
        return {"error": f"{game} did not resolve"}

    fr = w.reset()
    board = fr.frame[-1]
    # the palette is READ, never assumed: it is the domain's fact and a constant here would
    # be a magic number wearing an adapter's clothes.
    palette = int(max(int(v) for row in board for v in row)) + 1

    env = ArcWorld(w, arc_percept.Objects(), arc_atoms.three_spaces(arc_predict.predict()),
                   palette=palette, name=game)
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms()), tether.Config(), led)
    bud = arc_run.Budget()
    bud.level_starts()
    ag.run(cycles)

    rows = led.rows()
    g = ag.gamma
    return {
        "game": game, "board": list(getattr(board, "shape", (len(board), len(board[0])))),
        "palette": palette, "slots": len(env.slots()), "blind": env.blind,
        "cycles": ag.cycle, "rows": len(rows), "gate": gate.check(rows)["verdict"],
        # §22.6: the stage code is the DIAGNOSIS. `stalls` over CLOSED segments, never
        # `seg.stage()` -- the live segment is whatever is currently open, and a fresh one
        # reads DIED_PRE_DIFF by construction.
        "stalls": dict(ag.chain.stalls), "last_stage": ag.chain.last_stage,
        "reuse_funnel": dict(ag.chain.reuse_branch),
        "mints": sum(1 for r in rows if r["event"] == "mint"),
        "library": len(g.library), "admissions": g.admissions(),
        "lambda": g.type_report(), "atoms": len(g.atoms),
        "unexpressible": arc_predict.unexpressible(),
        "events": dict(collections.Counter(r["event"] for r in rows)),
    }


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "ls20"
    out = play(name)
    for k, v in out.items():
        print(f"  {k:<14}: {v}")
