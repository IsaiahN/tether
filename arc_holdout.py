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
import experiment
import gamma
import gate
import habitat
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

    # DRIVEN STEP-WISE so `Affordances` can learn. §16.4 reads behaviour under contact, which
    # needs a before/after pair per step -- `run()` gives no hook, and the alternative was to
    # put a domain reader inside the loop, which is the wrong side of the wall.
    seg = ag.env._decompose
    aff = arc_percept.Affordances()
    ctrl = experiment.Controlled()
    endings = collections.Counter()
    was_terminal = ""
    restarts = 0
    for _ in range(cycles):
        before = {k: dict(v) for k, v in seg.tracked.items()}
        state = env.observe()
        ag.step()
        aff.note(before, dict(seg.tracked), mover=None)
        # §21.1's control: the state BEFORE the action, the action, and what it cost. A
        # repeat of the same state under a different action is the only re-run the loop gets.
        # The action is read AFTER the step -- it is chosen inside it, so reading it before
        # gives the previous step's, which would pair a state with the wrong action.
        act = getattr(ag, "_last_action", None)
        # AND NOT ON A BOARDLESS FRAME. After death `observe()` is `{}`, so every such
        # frame shares the signature `()` and two absences read as the same state
        # revisited -- a determinism reading over nothing. **An absence is not a state of
        # the world**, which is the same rule that made `components` return NOT_RESOLVED
        # rather than `[]` this morning, arriving one layer out.
        if act and state:
            ctrl.visit(state, act, sum(ag._last_mass.values()))
        # 4e. `terminal()` was built as *read by the harness, never by the loop* and read by
        # nothing since. A GAME_OVER that nobody reads is a level-resetting loss the agent
        # cannot exploit -- and the loss is the ONLY controlled experiment available.
        # AN ENDING IS A TRANSITION, NOT A STATE, AND THE FIRST VERSION COUNTED THE STATE.
        # `terminal()` reports the CURRENT frame, so once `ls20` is GAME_OVER it answers
        # `death` on every later step -- and retargeting on each of them recorded 32
        # endings for one death and published `budget_to_deaths` as 0.200 when one death
        # in 160 cycles is 0.006. **The same misreading as taking 172-of-300 GAME_OVER
        # frames for abundant deaths, arriving in code an hour after it was caught in
        # prose.** Edge-triggered: the ending fires where the state CHANGES.
        end = env.terminal()
        if end and end != was_terminal:
            endings[end] += 1
            ag.retarget(env, env.levels()[0], how=end)
            # THE EXPERIMENTER RESETS THE BENCH. Ruled seat-side and BORROWED: it does not
            # travel to a scored run. The tracker is reset with it -- carrying object
            # identity across a death would assert continuity the world does not offer,
            # and on the same board the names re-found identically anyway.
            env.restart()
            seg.tracked, seg._next = {}, 0
            restarts += 1
        was_terminal = end

    rows = led.rows()
    g = ag.gamma

    # §16.5. SEEDED FROM THE RESIDUAL, which is what Figure 11 says: *everything in contact
    # with the residual*, not with an arbitrary object. The slot carrying the most
    # unexplained mass names its object, and the cascade runs outward from there.
    tracked = getattr(ag.env, "_decompose", None)
    objs = dict(getattr(tracked, "tracked", {}) or {})
    worst = max(ag._last_mass, key=ag._last_mass.get, default=None) if ag._last_mass else None
    hab = None
    if worst and objs:
        hab = habitat.enumerate_from(objs, worst.split(".")[0], aff=aff)
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
        "habitat": hab.report() if hab else "no residual to seed from",
        "habitat_residuals": len(hab.residuals()) if hab else 0,
        "affordance_kinds": aff.report()["kinds"],
        "endings": dict(endings),
        "experiment": ctrl.report(),
        # §21.2's number, published rather than inferred: *if that is 40%, someone should
        # see it rather than infer it.*
        "budget_to_deaths": (round(endings.get("death", 0) / cycles, 4) if cycles else 0.0),
        "restarts": restarts,
        "borrowed": ("the controlled pairs exist only because the SEAT restarts the bench; "
                     "on a scored run nobody restarts anything, so the pair count is not a "
                     "capability the agent has"),
    }


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "ls20"
    out = play(name)
    for k, v in out.items():
        print(f"  {k:<14}: {v}")
