"""STAGE 0b, THE PANEL PRECONDITION: can the stage-5 gate's quantity move AT ALL?

The gate reads *does re-derivation cost fall as the library grows*, and the
instrument for that is already specified rather than invented here: `chunk_reuse`,
`tether.py:506`, **a settled term inside a later mint**. A later mint that reuses a
settled term did not re-derive it from atoms, so the cost fell.

**WHY THIS RUNS BEFORE ANY HARVEST.** `CLAUDE.md` records `chunk_reuse` reading 0
across all fourteen board-depth readings. If it is 0 in the CONTROL on the Phase 2
panel too, then *falls as the library grows* has nowhere to fall from, and the gate
would read green by vacuity after four stages of work.

**AND THE ZERO NEEDS A DENOMINATOR, which is the whole reason this prints more than
one number.** `chunk_reuse = 0` with 0 settled terms is STRUCTURALLY FORCED -- there
was nothing to reuse -- and says nothing about the mechanism. `chunk_reuse = 0` with
20 settled terms is a real null about reuse. The two read identically at the counter.

THREE ARMS, ONE SCRIPT, ONE FLAG -- never three scripts. Two programs written at
different times differ in every way nobody wrote down.

    default      o0 mover / o1 pushed / o2 wall
    click_only   FIXTURE B -- no avatar, one positioned action
    remap_after  FIXTURE A -- up/down and left/right SWAP after N steps.
                 **CONSTRUCTED HERE FOR THE FIRST TIME.** Three occurrences in the
                 whole tree before this: a comment, the declaration, and the read
                 inside `step`. Zero call sites.

PER FIXTURE AND PER SEED, NEVER POOLED. Three fixtures are three worlds.
READ OFF THE OBJECT AFTER THE RUN, NEVER OFF A LEDGER ROW -- a row written at the
top of a step reports the state before that cycle ran, and `gamma.book` is the total.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[0]))

REPO = Path(r"C:\Users\Admin\Documents\GitHub\tether")
sys.path.insert(0, str(REPO))

import gamma as G  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

# anchor: not chosen here -- `boards()` makes seeds consecutive from 0, and 0/1/2 are the
# three the surfacing work already reported on, so these readings sit beside those.
SEEDS = (0, 1, 2)
# anchor: not chosen here -- 60 is `tieracc.py`'s population on this same world, so a
# reading taken here is comparable to the tier figures rather than to nothing.
CYCLES = 60

ARMS = ("default", "click_only", "remap_after")


def run(arm: str, seed: int, cycles: int) -> dict:
    """One arm, one seed. Returns what the OBJECT holds after the run.

    **THROUGH `gridworld.family()`, NOT BY CONSTRUCTING THE FIELDS HERE.** The first version
    of this script set `click_only` and `remap_after` inline, which would have left the
    habitat's new declaration with no caller -- the exact *built and never reached* shape
    this stage exists to report. The boards are identical either way: `family` places the
    swap at `cycles * 0.5` and the inline version used `CYCLES // 2`, which is 30 for both.
    """
    env = world.bind(gridworld.family(arm, seed, cycles))
    gam = G.Gamma(env.atoms())
    ag = tether.Agent(env, gam, tether.Config(max_depth=2), ledger.Ledger())
    err = ""
    steps = 0
    try:
        for _ in range(cycles):
            ag.step()
            steps += 1
    except Exception as exc:                                  # noqa: BLE001
        err = f"{type(exc).__name__}: {exc}"
    book = dict(ag.gamma.book)
    return {
        "arm": arm, "seed": seed, "steps": steps, "error": err,
        # `settled_terms` is a PROPERTY and `units` is a METHOD. Not symmetric, and
        # calling the first raised rather than reading wrong -- which is the good direction.
        "settled": len(ag.gamma.settled_terms),
        "units": len(ag.gamma.units()),
        "chunk_reuse": book.get("chunk_reuse", 0),
        "bargain_paid": book.get("bargain_paid", 0),
        "actions": len(env.actions()),
    }


def main(argv: list[str]) -> int:
    cycles = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else CYCLES
    # EVERY ROW IS PERSISTED AS IT LANDS, not summed at the end. A 30-minute run that is
    # killed with its output still in a buffer leaves nothing at all, and the first attempt
    # at this was piped through `tail`, which holds everything until EOF -- so the run WAS
    # invisible for 22 minutes and would have been lost entirely.
    out = Path(__file__).with_name("panel_rows.jsonl")
    out.write_text("", encoding="utf-8")
    print(f"WORLD gridworld, no ARC board. {cycles} cycles, seeds {SEEDS}.")
    print("POPULATION: every cycle of every (arm, seed). Read off gamma.book AFTER")
    print("the run, not off a ledger row. PER ARM PER SEED, NEVER POOLED.")
    print(f"  {'arm':12} {'seed':>4} {'acts':>4} {'steps':>5} "
          f"{'settled':>7} {'units':>5} {'paid':>6} {'chunk_reuse':>11}  note", flush=True)
    rows = []
    for arm in ARMS:
        for seed in SEEDS:
            r = run(arm, seed, cycles)
            rows.append(r)
            with out.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(r) + "\n")
            note = r["error"] or ("NO DENOMINATOR -- nothing settled, so a 0 here is "
                                  "forced" if r["settled"] == 0 else "")
            print(f"  {r['arm']:12} {r['seed']:4d} {r['actions']:4d} {r['steps']:5d} "
                  f"{r['settled']:7d} {r['units']:5d} {r['bargain_paid']:6d} "
                  f"{r['chunk_reuse']:11d}  {note}", flush=True)

    print()
    print("  THE PRECONDITION, stated as the question the gate needs answered:")
    for arm in ARMS:
        a = [r for r in rows if r["arm"] == arm]
        reuse = sum(r["chunk_reuse"] for r in a)
        settled = sum(r["settled"] for r in a)
        broke = [r for r in a if r["error"]]
        if broke:
            verdict = f"DID NOT RUN -- {broke[0]['error']}"
        elif settled == 0:
            verdict = ("UNREADABLE: 0 settled terms across all seeds, so chunk_reuse "
                       "could only be 0. The gate cannot show anything here")
        elif reuse == 0:
            verdict = (f"ZERO ON A REAL DENOMINATOR: {settled} settled terms and no "
                       f"reuse. A true null -- the gate has room but nothing moves it")
        else:
            verdict = f"LIVE: {reuse} reuses over {settled} settled terms"
        print(f"    {arm:12} {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
