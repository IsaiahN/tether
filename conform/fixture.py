"""fixture: ONE PASS THROUGH EVERY STAGE, END TO END, ON THE TOY WORLD. No game, no score.

**ISAIAH, 2026-09-24:** *"I need this stuff wired together and not orphaned. Why can't the
system be built out end to end without games? Once we prove everything is firing as it should,
and all the problems that can be worked out get worked out, then we can start testing on games."*

    A FIXTURE IS NOT A GAME. *Is this wired* is a YES/NO about REACHABILITY.
    *How well does it play* is a NUMBER about BEHAVIOUR. Only the second is stopped,
    and only the second is what drift feeds on.

**THE HONEST LIMIT, AND IT IS WRITTEN HERE SO NO FUTURE READER CAN MISTAKE IT:**

> **A FIXTURE PROVES WIRED. IT NEVER PROVES CAPABLE.**

**AND IT PROVES IT ON A NON-GRID WORLD, WHICH IS A SECOND LIMIT AND A SHARPER ONE -- reviewer,
2026-09-24, written down now rather than remembered later.**

> **THE TOY WORLD IS SEVEN SCALAR SLOTS WITH ARITHMETIC RULES. THE AGENT'S PURPOSE IS VISUAL
> GRID PUZZLES.** A stage lighting up here proves THE STAGE IS WIRED. **It does not show the
> mechanism works on a board shaped like the actual job** -- *a decomposition that only works on
> scalars would pass this fixture and fail the first grid.*

**THE SYNTHETIC GRID FIXTURE IS OWED AT ITEM 6.5**, immediately before real ARC games and after
everything else: Isaiah, *"B can be done as a test before testing against real ARC games again,
but it's only before the ARC game testing in priority."* **It is the last gate between that
defect and real games, and it is recorded here so it cannot quietly die of being remembered.**

**This seat is MECHANISM EVIDENCE ONLY and must never be reported as `M2` done.**
`M2_STANDARD` clause 7 exists precisely to stop mechanism being reported as capability --
*report against the DEFINITION, forms and pursues a bounded multi-step behaviour, not against
the work, a routine ran once.* **A green fixture would mean every stage EXECUTES. It would say
nothing whatever about whether the agent is any good.**

**WHY IT FAILS ON A TRANSITION RATHER THAN ON THE STANDING STATE, WHICH IS A DEVIATION FROM THE
LETTER OF THE RULING AND IS FLAGGED AS ONE.** The ruling says *orphaned machinery fails it by
construction*. Taken literally the seat is RED today -- and `.git/hooks/pre-commit` blocks any
commit that fails any seat, **so a literally-red fixture would block the very commits that fix
what it reports.** A deadlock is not a gate.

**So the dead stages are DECLARED in `fixture.json` and PRINTED ON EVERY RUN**, exactly as the
`wiring` seat handles the same problem: nothing is hidden, the list is a standing accusation,
and **the seat goes RED the moment a stage changes state without the manifest moving** -- in
either direction. Repairing a stage and not recording it fails, which is the point: the record
moves with the capability or the seat says so.
"""

from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
MANIFEST = Path(__file__).parent / "fixture.json"

# THE CHAIN, IN ORDER. Isaiah's ordering rule: *do not fix a lower stage while a higher one is
# unreached -- that is how the ACT space got built behind a gate nothing passes.* The order is
# load-bearing, so it is a tuple and the report walks it rather than a dict's iteration order.
STAGES = (
    ("PERCEIVE",  "a fixture grid is read, and the world names its win condition"),
    ("GOAL",      "`@goal.completed` appears among the slots and holds a value"),
    ("DECOMPOSE", "the goal yields a NEARER want -- `objective_step` returns a step"),
    ("COMPOSE",   "a routine is FORMED -- `routine.py` entered, not merely present"),
    ("RUN",       "the routine advances, with an expectation attached"),
    ("EXPRESS",   "the DECLARED self-account is narrated, and every sentence traces"),
    ("CORRECT",   "the expectation is compared against the ground and recorded"),
)


def probe() -> dict[str, bool]:
    """Step the toy world once, end to end, and report which stages EXECUTED.

    SPIES, NEVER EDITS. Every wrapper calls through and returns the real value, so the run
    this observes is the run that would have happened -- the instrument must not be the
    treatment, which is the failure this project has filed against itself most often.
    """
    import routine
    import tether
    import world
    from demo import bind  # THE SAME CONSTRUCTION THE TOY SEAT ALREADY RUNS -- a fixture
    from gamma import Gamma  # that builds its own world is testing a world nobody uses
    from ledger import Ledger

    hit = {k: False for k, _ in STAGES}
    seen_events: set[str] = set()

    # -- COMPOSE / RUN: the ACT space, spied at its own module -------------------------
    _enum, _adv = routine.enumerate_routines, routine.advance

    def enum(*a, **k):
        out = _enum(*a, **k)
        hit["COMPOSE"] = True
        return out

    def adv(r, holds, lib, state=None, _depth=0):
        hit["RUN"] = True
        return _adv(r, holds, lib, state, _depth)

    routine.enumerate_routines, routine.advance = enum, adv

    # -- DECOMPOSE: a want that could not be acted on yielding one that can -------------
    _step = tether.objective_step

    def step(evaluate, current, ordered, alphabet):
        out = _step(evaluate, current, ordered, alphabet)
        if out is not tether.NOT_RESOLVED:
            hit["DECOMPOSE"] = True
        return out

    tether.objective_step = step

    try:
        env = bind(world.Transitions())
        ag = tether.Agent(env, Gamma(env.atoms()), tether.Config(),
                          Ledger(path="runs/fixture.jsonl"))

        # -- PERCEIVE + GOAL, read off the world BEFORE the loop moves anything --------
        obs = env.observe()
        name, _deg = env.objective()
        hit["PERCEIVE"] = bool(obs) and bool(name)
        hit["GOAL"] = "@goal.completed" in obs

        with redirect_stdout(io.StringIO()):
            ag.run(8)

        rows = [{"seq": e.seq, "cycle": e.cycle, "step": e.step, "slot": e.slot,
                 "event": e.event, **e.detail} for e in ag.led.entries]
        for r in rows:
            seen_events.add(str(r.get("event", "")))
        # -- CORRECT: the ground answering a claim, which is what `settle` IS ----------
        hit["CORRECT"] = any(v in seen_events for v in ("settle", "demote", "refute"))

        # -- EXPRESS, AND THE FIRST VERSION OF THIS STAGE CLAIMED A BAR THE PROJECT REFUSES.
        # It read *every event kind the run produced has a sentence*. **Measured: 24 kinds, 9
        # narrated, 15 silent -- including `bet` at 100 rows.** That looks damning and is not:
        # `test_m2`'s own narration check states it outright -- *`speak` does not narrate every
        # ledger event AND SHOULD NOT; most are internal bookkeeping. What it MUST narrate is
        # the agent's ACCOUNT OF ITSELF, and that is a LIST, not a rule.*
        #
        # **SO THE STAGE WAS ASSERTING TRACEABILITY AND ADVERTISING TOTALITY**, and the gap
        # between the two would have been read by the next person as an agent defect. It is the
        # `A6i` writing side: the summary written from the work rather than from the definition.
        #
        # THE REAL BAR IS BOTH HALVES. Every sentence TRACES (`speak.verify`'s own rule: *a
        # sentence that traces to nothing is a defect*), AND every event of the DECLARED
        # self-account that the run produced is narrated.
        #
        # **`SELF_ACCOUNT` IS DUPLICATED FROM `test_m2.py` AND THAT IS NAMED, NOT HIDDEN** --
        # a seat may not import a test's local, and two producers of one fact are harmless
        # exactly until one side changes. It is a pinned TABLE in both places for
        # `conform/lint.py`'s reason: a table can be pinned, logic widens quietly.
        import speak
        SELF_ACCOUNT = ("routine", "guard", "books")      # mirrors test_m2.py, deliberately
        said = speak.sentences(rows)
        traces = bool(said) and speak.verify(rows, said)["traceable"]
        cited = {i for seqs, _t in said for i in seqs}
        owed = [r for r in rows if str(r.get("event", "")).startswith(SELF_ACCOUNT)]
        accounted = not owed or all(r["seq"] in cited for r in owed)
        hit["EXPRESS"] = traces and accounted
    finally:
        routine.enumerate_routines, routine.advance = _enum, _adv
        tether.objective_step = _step
    return hit


def main() -> int:
    live = probe()
    want = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    moved = []
    print("  the chain, top first -- a lower stage is not worth fixing while a higher one is dead")
    for name, gloss in STAGES:
        now, was = live[name], want.get(name)
        mark = "REACHED" if now else "DEAD   "
        flag = ""
        if was is not None and was != now:
            flag = f"   <-- CHANGED: manifest says {'REACHED' if was else 'DEAD'}"
            moved.append(name)
        elif was is None:
            flag = "   <-- NOT IN THE MANIFEST"
            moved.append(name)
        print(f"    {mark}  {name:<10} {gloss}{flag}")
    if moved:
        print()
        print(f"  FIXTURE: {len(moved)} stage(s) the manifest does not "
              f"record: {', '.join(moved)}.")
        print("  A stage changing state is the event this seat exists for. Update `fixture.json`")
        print("  IN THE SAME COMMIT as the change, or say why it moved.")
        return 1
    dead = [n for n, _ in STAGES if not live[n]]
    if dead:
        print(f"\n  {len(dead)} of {len(STAGES)} stages DEAD and declared: {', '.join(dead)}.")
        print("  Declared is not excused -- this is the build order, top first.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
