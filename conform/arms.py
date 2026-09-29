"""arms: eighteen capability switches, all default OFF, and nothing computed the sum.

**ENVIRONMENT SWITCHES ONLY, AND THE COUNT ABOVE IS THEREFORE NOT THE AGENT'S TOTAL --
ANNOTATED 2026-09-28.** The detector is `os.environ.get("TETHER_X")`, so a capability switch
that is a `Config` FIELD is invisible here. There is exactly ONE: `Config.accumulate`.

**IT WAS TWO UNTIL 2026-09-29, AND THE SECOND WAS REMOVED RATHER THAN COUNTED -- ISAIAH:
*remove the "System 0 off" override. System 0 is always on.*** `Config.system0` is gone from
the dataclass, so the blind spot this paragraph describes no longer has it to hide. **That is
the stronger fix: a field-arm the census cannot see is dangerous because it can be OFF, and an
arm that does not exist cannot be.**

**AND THAT IS CHECKED RATHER THAN HEDGED, because a corrected count that is itself uncounted is
how the first one got here.** Every class in the repository was scanned for `bool`-annotated
fields: FOUR have them, and only `Config`'s are configuration -- `gamma.Atom`'s
`reads_operand`/`polymorphic` are per-atom DECLARATIONS, and `instruments.Segment` and
`instruments.Termination` hold recorded READINGS. Of everything `arc_holdout.play` constructs
(`ArcWorld`, `Ledger`, `Config`, `Gamma`, `Agent`, `Budget`) only `Config` carries a bool.

**AND `system0` WAS THE ONE THAT MATTERED** -- it was found OFF on the
ARC path against a standing ruling of Isaiah's, and it is exactly the class this file's
`UNDECLARED` check exists to prevent entering silently. *A new arm cannot enter silently* is
true of env arms and false of field arms.

**KEPT IN THE PAST TENSE RATHER THAN DELETED, because an error entry whose evidence is edited
away stops being evidence.** The instance is closed by removal; **the CLASS is not** -- a future
`Config` bool would be just as invisible to this census, and `accumulate` is one today.

Widening the census to cover them is FILED, NOT DONE, deliberately: an instrument is installed
once you know what it must measure, and the System 0 rulings are open. **But the count is a
statement about the agent, a reader meets it first, and it is wrong -- so it is annotated now
rather than left standing until the census is built.**

Every arm in this codebase is `bool(os.environ.get("TETHER_X"))` -- no default value, so OFF
unless the environment says otherwise -- and **the repository sets one only by a RULING, in
code, which the census below now detects rather than narrates**. The agent
that actually runs is therefore the most starved variant of itself, in eighteen independent
respects, and that was true without anyone deciding it.

**THE FINDING IS NOT THAT THEY ARE WRONGLY OFF.** Each site carries a real reason and several
are costed: `TETHER_INSTRUMENTS` is off because a new published attribute widens the slot set
and §12.12 prices that in EPISODES FORGONE; `TETHER_SHAPE_DELTA` says *both arms belong on
together; that is a measurement, not a default*. Turning any of them on is a measurement and
a ruling, and this seat does neither.

**THE FINDING IS THAT THE REASONS LIVE AT NINETEEN SCATTERED SITES AND NO PLACE HELD THE SUM.**
That is verbatim the ground-focus seat's own origin -- *each looked reasonable alone; the drift
was visible only in the sum, and nothing computed the sum* -- one level up, about configuration
instead of commits. **Eighteen individually-justified OFFs compose into an agent nobody chose.**

    python arms.py        the census, and it FAILS on the three things below

WHAT MAKES IT FAIL, and each is a fact rather than a judgement:

    UNDECLARED   an arm is read in code and absent from the table below. **A new arm cannot
                 enter silently**, which is how eighteen accumulated
    STALE        the table names an arm no code reads any more
    HALF A PAIR  an arm is ON and a partner its own site declares is OFF. `arc_percept` says
                 of the shape deltas: *the `holes` and `perimeter` ATOMS only resolve when
                 `TETHER_SHAPE_DECODE` is on, so with arm I off the agent reads a delta of a
                 quantity it cannot itself measure.* **That coupling was written in a comment
                 and nothing enforced it**

IT DECIDES NOTHING AND FLIPS NOTHING. The table is DATA -- `conform/lint.py`'s rule, *exemptions
as data, not logic* -- so it can be read, pinned and moved by the reviewer without touching code.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).parent.parent

# THE TABLE. One line per arm, taken from the arm's OWN SITE rather than summarised from what
# it looked like it did -- `A6i`'s writing side, which fires exactly where a row is authored.
# A pair means the two are declared at their site to belong on together.
ARMS: dict[str, str] = {
    "TETHER_BARGAIN_FIT": "library fit priced by the bargain rather than by fit alone",
    "TETHER_NO_CARRY_CANDIDATE": "**INVERTED POLARITY -- the SECOND row here that is, so "
                                 "the first is no longer the only one and both say so.** A "
                                 "DEFAULT-ON write: a term the agent BINDS becomes a candidate "
                                 "awaiting the ground, so an IMPORTED term can reach `settle`. "
                                 "`candidates` had one writer (mint), so a carried term could "
                                 "never settle on any board and `gamma.refute`'s promise that a "
                                 "demoted term *can settle again if it starts paying* was "
                                 "unmeetable for imports. IMPORTED ONLY: unscoped it also moved "
                                 "local terms' birth cycles and took M2 to 27/30. Spelled `NO_` "
                                 "so the inversion is in the NAME. The OFF arm is the non-zero "
                                 "control the null needs",
    "TETHER_DELTA_KEY": "route (b) re-keyed on this frame's delta",
    "TETHER_DELTA_OPERANDS": "deltas offered as operands",
    "TETHER_GUARD_AXIS": "the guard axis in the reject key",
    "TETHER_INSTRUMENTS": "the embedded instrument set -- Part 12 item 3, PAID BILLS from "
                          "frame 0. Off at a COSTED price: a new attribute widens the slot "
                          "set and §12.12 prices that in EPISODES FORGONE",
    "TETHER_INVENT": "atom invention from an unexplained delta",
    "TETHER_ITERATE": "the fold constructs -- `cells`/`cell_row`/`cell_col`/`count_true`. "
                      "§12.0 rules the MEANS to iterate is INHERITANCE where a solved case "
                      "would be an answer, and the agent could hold a cell set and not walk it. "
                      "**RULED ON by Isaiah 2026-09-24 and set in `arc_holdout.play` for the "
                      "ARC path, so the env census below reads OFF while the capability is "
                      "LIVE.** A ruling turned it on, not a measurement -- the house rule is "
                      "his to override. The toy world is untouched: it has its own atoms",
    "TETHER_NO_TALLY": "**INVERTED POLARITY. THIS SAID *THE ONLY ROW HERE THAT IS* AND IT "
                       "STOPPED BEING TRUE ON 2026-09-30**, when `TETHER_NO_CARRY_CANDIDATE` "
                       "was added -- correct when written and falsified by a later build, "
                       "which is the class this table cannot catch by passing. Every OTHER arm "
                       "is OFF and its variable turns it ON; this names a DEFAULT-ON incremental "
                       "tally in `_cannot_pay` and the variable turns it OFF. Spelled `NO_` so the "
                       "inversion is in the NAME and not only in this row. It exists for the "
                       "identity A/B -- one script, one flag -- because an exact optimisation has "
                       "to be provable against its own absence, and a default-off one is an "
                       "optimisation nobody runs",
    "TETHER_OBSERVER": "the corpus's cheap mutation set carried PER OBJECT, not counted",
    "TETHER_REBIND_HELD": "rebinding a slot whose term is already held",
    "TETHER_RECIPE_DEDUP": "one candidate per recipe rather than per instance",
    "TETHER_REFUTED_BIN": "refutations binned rather than flat",
    "TETHER_REL_GAP": "the relational gap reading",
    "TETHER_SHAPE_DECODE": "arm I -- `_as_shape`, the decoder eight SHAPE atoms need",
    "TETHER_SHAPE_DELTA": "`dholes`/`dperimeter` across frames. PERCEPTION: no atom accepts "
                          "OBJECT_BEFORE, so the agent cannot compose a cross-frame delta",
    "TETHER_STARVED_CONTACT": "the starved-contact reading",
    "TETHER_STREAM_WIDEN": "the widened candidate streams",
    "TETHER_TYPED_BIND": "binding filtered by type",
}

# DECLARED AT THE SITE, NOT INVENTED HERE. `arc_percept`'s shape-delta comment: *pairs with arm
# I rather than standing alone ... both arms belong on together; that is a measurement, not a
# default.* The comment could not fire; this can.
PAIRS: tuple[tuple[str, str], ...] = (
    ("TETHER_SHAPE_DELTA", "TETHER_SHAPE_DECODE"),
)

# BOTH QUOTE STYLES, AND THE SEAT IS WHY. This matched double quotes only, so an arm written
# with single quotes would enter SILENTLY -- past the one check whose entire purpose is that a
# new arm cannot. The codebase is double-quoted throughout and `ruff format` keeps it that way,
# **which is exactly the reasoning that makes a detector brittle**: it is true of the code today
# and is not a property anything enforces. A guard resting on a convention it does not check is
# the arms' own shape one level up -- reasonable, and nothing computes it.
_READ = re.compile(r'''os\.environ\.get\(\s*["'](TETHER_[A-Z0-9_]+)["']''')

# A RULING TURNS AN ARM ON BY ASSIGNING ITS MODULE FLAG, AND NOTHING SAW THAT. `_ITERATE` was
# set in `arc_holdout.play` on 2026-09-24 and this seat kept reporting `0 ON`, with the fact
# carried in a PRINTED SENTENCE naming that one arm -- so the second ruling (2026-09-27, the
# shape pair) made the sentence false the moment it landed. **Detected now instead of narrated,
# because a hardcoded name is stale by success the next time someone rules.**
#
# AND IT IS THE `HALF A PAIR` RULE THAT ACTUALLY NEEDED IT: that check reads `on`, `on` read the
# ENVIRONMENT, and the pair it exists for is set IN CODE -- so it could not fire on the one case
# it was written for, and setting just one of the two would have left the seat GREEN.
_RULED = re.compile(r'''^\s*[A-Za-z_][\w.]*\._([A-Z0-9_]+)\s*=\s*True\s*(?:#.*)?$''', re.M)


def _tracked() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "*.py"], cwd=ROOT,
                         capture_output=True, text=True, check=False).stdout
    return [ROOT / line for line in out.split("\n") if line.strip()]


def sites() -> dict[str, list[str]]:
    """`{arm: ["file:line", ...]}` -- READ FROM THE CODE, never from the table.

    A census built from the table would agree with the table by construction, which is the
    measurement that cannot fail. The table is the CLAIM and this is the WORLD."""
    found: dict[str, list[str]] = {}
    for path in _tracked():
        if path.name == "arms.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for i, line in enumerate(text.split("\n"), 1):
            for arm in _READ.findall(line):
                found.setdefault(arm, []).append(f"{path.relative_to(ROOT).as_posix()}:{i}")
    return found


def ruled() -> dict[str, str]:
    """`{arm: "file:line"}` for arms a RULING turned on in code, rather than the environment.

    The convention it rests on is that the module flag is the arm name without `TETHER_`, and
    that convention is CHECKED rather than assumed: a `_FOO = True` whose `TETHER_FOO` is not a
    declared arm is simply not an arm and is ignored, so this cannot invent one."""
    out: dict[str, str] = {}
    for path in _tracked():
        if path.name == "arms.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in _RULED.finditer(text):
            arm = f"TETHER_{m.group(1)}"
            if arm in ARMS:
                line = text[:m.start()].count("\n") + 1
                out.setdefault(arm, f"{path.relative_to(ROOT).as_posix()}:{line}")
    return out


def selftest() -> dict[str, str]:
    """THE THREE REFUSALS, REINTRODUCED -- `wiring.py`'s form, and for its reason.

    **Every other seat in this folder carries one and this one did not.** Its three guards were
    proven by an ad-hoc script the night it was written, which is *a suite nothing runs is a
    suite that rots* with the suite left out entirely. **A guard whose failure path is never
    exercised is indistinguishable from a guard that cannot fail** -- which is this seat's own
    subject, one level up.

    NOT A TEST OF THE WORLD. Each case perturbs the TABLE or the ENVIRONMENT and asks whether
    the rule notices; none of them depends on which arms happen to exist today, so adding or
    retiring an arm cannot make a case pass or fail for the wrong reason.
    """
    out: dict[str, str] = {}
    found = {"TETHER_A": ["x.py:1"], "TETHER_B": ["y.py:2"]}
    table = {"TETHER_A": "a", "TETHER_B": "b"}

    bad = _judge(found, dict(table), on=set(), pairs=())
    out["clean"] = "ok" if not bad else f"UNWITNESSED (refused a clean table: {bad})"

    bad = _judge(found, {"TETHER_A": "a"}, on=set(), pairs=())
    out["A undeclared"] = ("ok" if any("UNDECLARED" in b for b in bad)
                           else f"UNWITNESSED ({bad})")

    bad = _judge(found, {**table, "TETHER_GHOST": "g"}, on=set(), pairs=())
    out["B stale"] = "ok" if any("STALE" in b for b in bad) else f"UNWITNESSED ({bad})"

    bad = _judge(found, dict(table), on={"TETHER_A"},
                 pairs=(("TETHER_A", "TETHER_B"),))
    out["C half a pair"] = ("ok" if any("HALF A PAIR" in b for b in bad)
                            else f"UNWITNESSED ({bad})")

    # AND THE CONTROL FOR C, without which "half a pair" would pass by always complaining.
    bad = _judge(found, dict(table), on={"TETHER_A", "TETHER_B"},
                 pairs=(("TETHER_A", "TETHER_B"),))
    out["C control"] = ("ok" if not any("HALF A PAIR" in b for b in bad)
                        else f"UNWITNESSED (a WHOLE pair was refused: {bad})")

    # D -- THE RULING DETECTOR, over literal text so it needs no fixture file. It exists
    # because `HALF A PAIR` read the environment while the pair it was written for is set in
    # code, so the guard could not fire on its own case.
    hits = {m.group(1) for m in _RULED.finditer(
        "    arc_atoms._ITERATE = True\n"
        "    tether._SHAPE_DECODE = True  # a trailing comment must not hide it\n"
        "        self._NOT_AN_ARM = True\n"
        "    x._SHAPE_DELTA = False\n")}
    out["D ruling seen"] = ("ok" if {"ITERATE", "SHAPE_DECODE"} <= hits
                            else f"UNWITNESSED (missed a ruling: {sorted(hits)})")
    # AND ITS CONTROL: `= False` is not a ruling, and the regex must not claim it.
    out["D control"] = ("ok" if "SHAPE_DELTA" not in hits
                        else "UNWITNESSED (read `= False` as ON)")
    return out


def _judge(found: dict, table: dict, on: set, pairs: tuple) -> list[str]:
    """The three rules, over data handed in. Split out so `main` and `selftest` share ONE
    implementation -- a fixture that re-states the rule tests the restatement."""
    bad: list[str] = []
    for arm in sorted(found):
        if arm not in table:
            bad.append(f"UNDECLARED  {arm} is read at {found[arm][0]} and is not in the table")
    for arm in sorted(table):
        if arm not in found:
            bad.append(f"STALE       {arm} is in the table and no code reads it")
    for a, b in pairs:
        if (a in on) != (b in on):
            bad.append(f"HALF A PAIR {a}={a in on} {b}={b in on} -- their own site declares "
                       "they belong on together")
    return bad


def main() -> int:
    # **THE FIXTURES RUN ON EVERY INVOCATION, NOT BEHIND A FLAG.** `check.py` calls this seat
    # with no arguments, so a `--selftest` nobody passes is a suite nothing runs -- which is
    # the rot this folder's own docstrings name, and it would leave the guards unexercised
    # exactly as they were before the fixtures existed. They are pure data and cost nothing.
    worst = [c for c, v in selftest().items() if v != "ok"]
    if worst or "--selftest" in sys.argv:
        for case, verdict in sorted(selftest().items()):
            print(f"  {case:<16} {verdict}")
        if worst:
            print("  the seat's OWN guards are not firing; its green means nothing")
            return 1
        return 0

    found = sites()
    rule = ruled()
    # ON IS WHAT THE AGENT RUNS WITH, not what the shell exported. Both routes, one set, so
    # `HALF A PAIR` finally reads the state it was written to judge.
    on = {a for a in found if os.environ.get(a)} | set(rule)
    bad = _judge(found, ARMS, on, PAIRS)

    print(f"arms: {len(found)} switches at {sum(len(v) for v in found.values())} read sites; "
          f"{len(on)} ON -- environment and ruling together")
    if not on:
        # NOT A FAILURE, AND SAYING SO IS THE POINT. All-off is the honest default for an
        # unproven arm -- the house rule is that a measurement turns one on. **The line exists
        # so the sum is never invisible again**, which is the whole reason this file is a seat
        # rather than a note: eighteen reasonable OFFs were never once read as one number.
        print("      every arm is OFF by both routes -- environment and ruling")
    if rule:
        # A RULING CAN TURN AN ARM ON WHERE A MEASUREMENT DID NOT, and the arms it turned on
        # are READ FROM THE CODE rather than named here -- see `_RULED`.
        print(f"      {len(rule)} ON BY RULING, set in code rather than exported:")
        for arm in sorted(rule):
            print(f"        {arm:<24} {rule[arm]}")
    for line in bad:
        print("  " + line)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
