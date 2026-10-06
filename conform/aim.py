"""aim: every commit names the DECLARED ITEM it serves, and untracked work is acknowledged.

Reviewer, 2026-09-22, on Isaiah's *"please make sure it doesn't do that"*: **a rule you have to
remember is not a control.** The failure it stops has repeated three times in one session, and
each time the individual step was justified:

  - I measured per-board properties and chose an evaluation set by them, on boards whose answers
    the record already holds (`F277`);
  - I spent a session widening perception, which is on no declared item (`F279`);
  - three times I filed a documented-correct state as a defect because I grepped the CODE and
    not the PLAN (`F280`).

**AND THE PLAN ITSELF TOLD ME TO DO SOME OF IT.** `TRAINING_PLAN` §7, §10 and §13 still describe a
per-game reverse-engineering loop and a diagnostician map from the public replays, written before
the current direction. **So the drift was following a stale section, not wandering off** — which is
exactly why the control has to be mechanical rather than remembered.

**THE TEST ANY WORK MUST PASS, and it is the reviewer's:** *if this succeeds, does the agent get
better at games it has never seen?* A route, a solution, a per-game fix answers no. **"Look at the
games" maps to no item below, so it cannot be committed** — the boundary stops being willpower.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

# THE DECLARED ITEM, one line, so `--tick` and the commit check read the SAME source. A
# self-check that recomputes what the current item is would drift from the commits.
CURRENT = Path(__file__).parent / "ITEM"

# THE IDLE PROTOCOL (reviewer 17:18). Three legal moves and no fourth. The failure it
# stops is the one that filled a session: with nothing obviously to do, find something --
# and what gets found is a board, because a board always has something wrong with it.
LEGAL = ("advance the current declared item",
         "the carry-over audit, WHILE a run is going",
         "answer a reviewer doc")

# THE DECLARED ORDER (reviewer 14:19, as amended). Nothing else is committable work.
ITEMS = {
    "step1.item1": "the observer's remaining pieces",
    "step1.run": "the declared step-1 evaluation",
    "step1.item6": "route (b) re-keyed on this frame's delta -- its own step",
    "structure.hash": "layout hash + the IMPORTED origin->status refactor",
    "mechanics.signature": "from route (a); nearest-match distance is a corpus search first",
    "condition.compiler": "5.9.5 option C -- the parse, and the agent-formed half",
    # the declared order of 2026-09-22 21:45 names these and the list did not carry them
    "generators": "5.9.1-5.9.4 -- schema factory, `bind` with the bond a PARAMETER, trees",
    "six.tests": "`settle(bond, ...)` reading the delta -- True/False/None",
    "type.widening": "the 18 OBJECT-typed atoms; map/fold, never a bare re-type",
    "ranking": "5.10 -- confidence/relevance, youth bonus, decay in games",
    "invention": "`owed_import` -> atom creation",
    "delete.enumerate_closure": "only after Part 6.5's five checks",
    "carryover.audit": "the superseded-docs table",
    # reviewer 17:44 -- marking a contested passage is WORK, and work that cannot be
    # spelled gets done under a wrong item or not at all.
    "doc.consistency": "mark a contradiction CONTESTED; repair only once Isaiah rules",
    # ISAIAH, 2026-09-23: "can you build the missing sensors and also check because we had a
    # sensor heavy thing before was it not wired or turned on?" -- a direct order, which is
    # how an item enters the declared list. Reviewer ordered it the same tick: the two
    # deltas and the extraction first, then the arm I measurement.
    "sensors": "what perception EMITS -- a reading the agent cannot compose for itself",
    # ISAIAH, 2026-09-23, reviewer-signed 07:42. The reframe REPLACED the declared order rather
    # than adding to it: library as what the agent thinks with, recipes as its programming
    # language, we supply the floor. `LIBRARY_RETRIEVAL` Part 12 carries the new order.
    "reframe": "Part 12 -- the plan of record itself, and the rulings that set it",
    # Part 12 item 2. The agent could HOLD a cell set and not walk it; §12.0 rules the
    # MEANS to iterate is inheritance where a solved case would be an answer.
    "iteration": "the agent's ability to walk a collection and close it",
    # THE GATES NAME THEMSELVES, the way `focus.py`'s own commits are L3 under its own rule.
    # Without this the control could not be introduced by a commit that obeys it.
    # ISAIAH'S REUSE RULINGS, 2026-09-30, reviewer-ordered the same day. THE ITEM WAS ADDED
    # ONE COMMIT LATE AND THAT IS RECORDED RATHER THAN TIDIED: `6fe40ed` (an IMPORTED term can
    # reach candidacy) and `8aaa776` (a candidate survives a level, dormant until bound here)
    # BOTH BELONG TO THIS ITEM and both rode under `structure.hash`, each saying so in its own
    # message. The comment on `m2.goal` below is why the substitution was declared instead of
    # silent: that chain rode under `step1.item1` for sixteen commits, flagged every time and
    # fixed none. Two, declared, then the item.
    "reuse": "carried terms, routines and subroutines: reuse without re-deriving, bury on "
             "failure, dormancy across levels",
    "seat": "a check, a guard, or the aim discipline itself",
    "escalated": "a real escalation, posted",
    # THE M2 GOAL CHAIN, DECLARED -- reviewer's ruling, 2026-09-26, and it is a repair rather
    # than an addition. The chain `goal_residual -> _goal_choice -> _mint_routine -> the shelf`
    # RODE UNDER `step1.item1` FOR SIXTEEN COMMITS, flagged in every one and fixed in none.
    #
    # `step1.item1` is *the observer's remaining pieces*. The goal chain is not that, and the
    # two were never confused by anyone reading the work -- they were confused by the FILING,
    # which is worse: a reader auditing what item1 cost cannot separate perception work from
    # planning work, and the `Item:` line exists precisely so that separation survives.
    #
    # **THIS IS THE ADJACENT-REFERENCE CLASS AND THAT IS WHY IT IS NOT COSMETIC** -- a lookup
    # that SUCCEEDS and returns the wrong neighbour. `step1.item1` is a real item, the commits
    # were real work, and `aim` was green on every one of the sixteen. Nothing could have
    # caught it except naming the thing it was not.
    "m2.goal": "the goal chain -- residual, selector, routine mint, the shelf",
    # ISAIAH, 2026-10-06, a direct order: ALWAYS USE THE TETHER -- the code is to be the
    # highest-fidelity instantiation of the figures, departures found and removed, and the
    # audit includes clutter. Its first commit (`act` leaves the vocabulary, F459) is the one
    # that introduces the item, declared in that commit's own message.
    "fidelity": "the figure-fidelity audit and its repairs -- departures and clutter",
}


def _msg(path: str) -> int:
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    named = [ln.split(":", 1)[1].strip().split()[0]
             for ln in text.splitlines()
             if ln.lower().startswith("item:") and ":" in ln and ln.split(":", 1)[1].strip()]
    if not named:
        print("aim: no `Item:` line. Every commit names the declared-order item it serves.")
        print("aim: " + ", ".join(sorted(ITEMS)))
        return 1
    bad = [n for n in named if n not in ITEMS]
    if bad:
        print(f"aim: `Item: {bad[0]}` is not in the declared order.")
        print("aim: " + ", ".join(sorted(ITEMS)))
        return 1

    # UNTRACKED WORK IS ACKNOWLEDGED, NOT FORBIDDEN -- and the difference is the point. The
    # reviewer's clause is *invisible work is a reporting problem regardless of its content*, so
    # a hard refusal would be wrong twice: it would block on files that are legitimately parked
    # (`arc_online.py`, `close_card.py` -- submission, "at the bottom of the list"), and it would
    # teach the seat to be worked around rather than read. Requiring the commit to NAME them
    # makes them visible every time, which is the property that was missing.
    out = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    untracked = [ln[3:] for ln in out.stdout.splitlines() if ln.startswith("??")]
    if untracked and not any(ln.lower().startswith("untracked:") for ln in text.splitlines()):
        print(f"aim: {len(untracked)} untracked file(s) and no `Untracked:` line naming them:")
        for u in untracked:
            print(f"aim:   {u}")
        print("aim: add `Untracked: <why they are not in this commit>`.")
        return 1
    return 0


def _selftest() -> int:
    """REINTRODUCE THE DEFECT, NEVER DISABLE THE CHECK."""
    import tempfile
    bad = 0

    def run(body: str) -> int:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(body)
            p = fh.name
        return _msg(p)

    # the failure this seat exists for: work that names no item
    if run("Focus: L1 perception -- widen the attribute set\n") == 0:
        print("aim: a commit naming NO item was accepted")
        bad += 1
    # "look at the games" maps to nothing, so it cannot be spelled
    if run("Focus: L2\n\nItem: solve-sk48\n") == 0:
        print("aim: an item outside the declared order was accepted")
        bad += 1
    # a real one passes -- the control must not refuse the work it exists to permit
    out = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    ack = "\nUntracked: parked\n" if any(
        ln.startswith("??") for ln in out.stdout.splitlines()) else "\n"
    if run(f"Focus: L1 perception\n\nItem: step1.item1{ack}") != 0:
        print("aim: a correctly-named commit was REFUSED")
        bad += 1

    # the declared item must itself be legal, or every tick self-check reads a wrong name
    if _tick() != 0:
        print("aim: conform/ITEM is not a declared item")
        bad += 1

    print("aim: ok" if not bad else f"aim: {bad} FAILED")
    return 1 if bad else 0


def _tick() -> int:
    """THE TICK STATES ITS ITEM BEFORE IT DOES ANYTHING. Reviewer: *the drift was never
    announced, because nothing asked.*"""
    item = CURRENT.read_text(encoding="utf-8").strip() if CURRENT.exists() else ""
    if item not in ITEMS:
        print(f"aim: conform/ITEM holds {item!r}, which is not in the declared order.")
        return 1
    print(f"aim: current item  {item} -- {ITEMS[item]}")
    print("aim: this tick must do one of:")
    for m in LEGAL:
        print(f"aim:   - {m}")
    print("aim: none of the three -> post `queue empty, waiting on X` and STOP.")
    return 0


if __name__ == "__main__":
    if "--tick" in sys.argv:
        raise SystemExit(_tick())
    if "--msg" in sys.argv:
        raise SystemExit(_msg(sys.argv[sys.argv.index("--msg") + 1]))
    raise SystemExit(_selftest())
