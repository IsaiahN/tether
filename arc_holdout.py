"""The holdout runner. SEAT-SIDE — the agent does not import this.

One game, played LOCALLY, and `OFFLINE` BY DEFAULT. Stepping is a local
`LocalEnvironmentWrapper` under every mode -- MEASURED at ~2,420 steps/s under both `NORMAL` and
`OFFLINE`, identical within noise -- so the mode buys nothing at run time and costs two network
calls at construction: an anonymous key and a fetch of the environment list. `OFFLINE` skips both
and constructs in 0.02s against 1.31s.

**AND THE SCORECARD IS LOCAL IN BOTH.** `base.py`'s own comment is *"Local scorecard (NORMAL or
OFFLINE)"*; the `session.post` path is `ONLINE`/`COMPETITION` only. **Nothing was ever posted, and
a claim that it was is corrected here rather than left standing.**

**A GAME NOT YET IN `environment_files/` NEEDS ONE `NORMAL` RUN TO FETCH IT.** Override with
`OPERATION_MODE=normal`. That is the whole cost of the default, and it is one run per game ever.

**NOT RUN BY `conform/check.py`.** It downloads content on first sight of a game; the checkers
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
from pathlib import Path

from arcengine import GameAction

import arc_atoms
import arc_percept
import arc_predict
import arc_run
import behaviour
import experiment
import gamma
import gate
import habitat
import ledger
import summary
import tether
from arc_world import ArcWorld

sys.dont_write_bytecode = True


def _mode():
    """`OFFLINE` unless `OPERATION_MODE` says otherwise. The package reads that variable itself
    and defaults to `NORMAL`; passing a mode explicitly overrides it, so the default is inverted
    here and the variable still works."""
    import os

    from arc_agi.base import OperationMode
    env = os.getenv("OPERATION_MODE", "").strip().lower()
    ok = ("normal", "online", "offline", "competition")
    return OperationMode(env) if env in ok else OperationMode.OFFLINE


def play(game: str = "ls20", cycles: int = 40, library: str | None = None) -> dict:
    """Download one game, run the loop on it, and report where the chain stops.

    **`library` IS §17.8's SWITCH, and the default is cold.** *State it, and make it switchable
    so the ablation is runnable* -- so persistence is something the SEAT turns on by naming a
    path, never something the agent does or a process lifetime decides. Pass one and the
    library loads before play and saves after; pass nothing and the run starts cold, which is
    what makes the ablation a matter of not passing an argument.

    **THE SAVE IS THE SEAT's AND OUT OF THE AGENT's REACH** -- `play` calls it, the loop never
    does, and nothing in `tether.py` knows the path exists.
    """
    logging.disable(logging.INFO)
    from arc_agi import Arcade

    arc = Arcade(operation_mode=_mode())
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
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=game), tether.Config(), led)
    loaded = ag.gamma.load(library) if library and Path(library).exists() else None
    # Q25 needs the set BEFORE play and there is exactly one moment it exists
    inherited = ({summary._chain(t) for t in ag.gamma.library.values()} if loaded else set())
    bud = arc_run.Budget()
    bud.level_starts()

    # DRIVEN STEP-WISE so the ending can be read per step. THE CONTACT READING MOVED INTO THE
    # WORLD: it needs a before/after pair, the world already has one in `step`, and a local
    # here sat OUTSIDE the boundary `retarget` triggers -- which is the placement the colour
    # ruling was about.
    aff = env.aff
    endings = collections.Counter()
    was_terminal = ""
    for _ in range(cycles):
        state = env.observe()
        ag.step()          # the world notes contact inside `step`, on its own before/after
        # §21.1's control: the state BEFORE the action, the action, and what it cost. A
        # repeat of the same state under a different action is the only re-run the loop gets.
        # The action is read AFTER the step -- it is chosen inside it, so reading it before
        # gives the previous step's, which would pair a state with the wrong action.
        _ = state
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
            # NO RESTART HERE, AND THE FIRST VERSION HAD ONE. `retarget` keeps `gamma`, so
            # restarting into this agent hands it the level again WITH WHAT IT LEARNED --
            # which is an ATTEMPT, and the scorecard counts it whichever hand pressed the
            # button. The seat restarting on the agent's behalf is the same purchase
            # against the same resource as the agent doing it. The controlled experiment
            # is a SEPARATE seat measurement with no Gamma in it -- see `controlled()`.
        was_terminal = end

    rows = led.rows()
    g = ag.gamma
    saved = g.save(library) if library else None

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
        # ABSENT, RENDERED AS ABSENT. `Chain.close()` has two callers -- `snaps.py` and
        # `tether.run()` -- and this driver calls `ag.step()` directly, so NO SEGMENT EVER
        # CLOSES HERE and the stage is never computed. `last_stage: None` read as *no stall*
        # for a whole exchange and was compared against a `snaps` reading as though both were
        # measurements. **A reading against an absence whose name looked like a reading.**
        "stalls": dict(ag.chain.stalls), "last_stage": ag.chain.last_stage,
        "stage_reads": ("UNCOMPUTED on this path -- `close()` is never called, so `None` here "
                        "means the instrument did not run, NOT that nothing stalled"),
        "reuse_funnel": dict(ag.chain.reuse_branch),
        "mints": sum(1 for r in rows if r["event"] == "mint"),
        "library": len(g.library), "admissions": g.admissions(),
        # §17.8's decision, visible in the report rather than in a process lifetime.
        "persistence": {"switch": library or "cold (default)",
                        "loaded": loaded, "saved": saved,
                        "handles": len(g.handles)},
        "lambda": g.type_report(), "atoms": len(g.atoms),
        "unexpressible": arc_predict.unexpressible(),
        "events": dict(collections.Counter(r["event"] for r in rows)),
        # WHICH BRANCH CHOSE THE ACTION. `by` is written on every ACT row and was read by
        # nothing -- and the ruled-budget run could not say whether a 96%-one-action policy
        # came from `discriminate`, `discriminate:learned` or the draw.
        "by": dict(collections.Counter(
            r["detail"]["by"] for r in rows
            if isinstance(r.get("detail"), dict) and r["detail"].get("by"))),
        "habitat": hab.report() if hab else "no residual to seed from",
        "habitat_residuals": len(hab.residuals()) if hab else 0,
        # what the terms have DONE, per (term, slot), read from the ledger rather than
        # accumulated on the term -- the events were always there and nothing asked.
        "behaviour": behaviour.report(rows),
        # THE END-OF-RUN SUMMARY. 14.7's three inherited plus MINTED, read off the ledger and
        # Gamma rather than accumulated anywhere.
        "summary": summary.report(rows, g),
        # Q25's VERDICT IS UNINTERPRETABLE ALONE, so it never travels alone. *No divergence*
        # is a copy loop only if there WAS something left to explain -- otherwise the level
        # had nothing to add and retrieving was correct. `outstanding` is that reading, and
        # the pair is the claim.
        "branching": summary.branching(g, inherited),
        "catalysts": summary.catalysts(g),
        "levels": summary.levels(rows),
        "reach": summary.reach(rows, g),
        "residual": {"pe_integral": round(ag.pe_integral(), 3),
                     "outstanding": round(ag.outstanding(), 3),
                     "reads": ("no divergence WITH outstanding surprise is a level that "
                               "failed to compose; no divergence with none left is a level "
                               "that had nothing to add")},
        "affordance_kinds": aff.report()["kinds"],
        # §16.1's precondition lattice, which was fed every step and read only by a conform
        # print -- and an instrument read only by a test is indistinguishable, from outside,
        # from one that does not exist.
        "preconditions": ag.pre.report(),
        "ties": ag.ties(),
        "keys_carrying_two_colours": aff.report()["keys_carrying_two_colours"],
        "unobserved_steps": env.unobserved,
        # 18.3's family. DIAGNOSTIC-ONLY TODAY, and 18.4 names that as a measured failure:
        # *the sensorium found the right self and changed nothing, because the only consumer
        # was the post-hoc veto.* Nothing reads `selected()` yet -- the consumer is the
        # proposer, which is its own item, and shipping one here would be half a mechanism.
        "selves": env.selves.report(),
        "endings": dict(endings),
        # §21.2's number, published rather than inferred: *if that is 40%, someone should
        # see it rather than infer it.*
        "budget_to_deaths": (round(endings.get("death", 0) / cycles, 4) if cycles else 0.0),

    }


def controlled(game: str = "ls20", trials: int = 4) -> dict:
    """§21.1's controlled experiment, run as APPARATUS. **No agent. No Gamma. Nothing carried.**

    **RULED 2026-08-28: the seat may restart for its OWN reasons and may not restart to help
    the agent learn.** Apparatus is *the seat setting up its own measurement*; farming is
    *restarting so the agent gets another go at a level* — **and who pressed the button does
    not change what it bought.** The check is not intent, it is carriage: ***does the agent
    carry anything across the restart?*** Here there is no agent to carry anything, so the
    question does not arise rather than being answered well.

    That is why this is not `play()` with a restart in it. **The first version restarted into
    a live agent, and `retarget` keeps `gamma`** — the level again, with what it learned,
    which is an attempt however it is labelled.

    **BORROWED, AND IT DOES NOT TRAVEL.** The seat restarts the bench; on a scored run nobody
    restarts anything. **Strictly more borrowed than determinism, which survives the port.**
    """
    logging.disable(logging.INFO)
    from arc_agi import Arcade

    arc = Arcade(operation_mode=_mode())
    w = arc.make(game)
    if w is None:
        return {"error": f"{game} did not resolve"}
    ctrl = experiment.Controlled()
    acts: list[str] = []
    for i in range(trials):
        fr = w.reset()                       # THE BENCH, RESET. Nothing survives it.
        seg = arc_percept.Objects()          # a fresh tracker: identity does not cross a trial
        board = fr.frame[-1]
        before = dict(seg(board))
        acts = acts or [GameAction.from_id(a).name for a in (fr.available_actions or ())
                        if GameAction.from_id(a).is_simple()
                        and GameAction.from_id(a) is not GameAction.RESET]
        if not acts:
            break
        act = acts[i % len(acts)]            # ONE action varied; the seat chooses, not a policy
        nxt = w.step(GameAction[act])
        after = dict(seg(nxt.frame[-1])) if nxt is not None and nxt.frame else {}
        ctrl.visit(before, act, after)
    r = ctrl.report()
    r["trials"] = trials
    r["actions_available"] = acts
    r["borrowed"] = ("the pairs exist only because the SEAT restarts the bench, for its own "
                     "measurement and with no agent in the run. On a scored run nobody "
                     "restarts anything, and nothing here is a capability the agent has.")
    return r


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "ls20"
    for k, v in play(name).items():
        print(f"  {k:<14}: {v}")
    print("")
    print("  -- 21.1 CONTROLLED, run as apparatus: no agent, no Gamma --")
    for k, v in controlled(name).items():
        print(f"  {k:<18}: {v}")
