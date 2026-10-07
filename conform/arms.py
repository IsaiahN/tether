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
    "TETHER_ACTED_GUARD": "a term may be guarded on `ACTED_SELF` -- true when the press "
                          "LANDED ON this slot's object, resolved per slot by the caller so "
                          "no object NAME ever crosses into a term. **DEFAULT OFF, AND THE "
                          "DEFAULT IS A REFUTER THAT FIRED.** The semantics are confirmed "
                          "(60/60 against the world, `conform/landed.py`) and the "
                          "pre-registered test failed: payments up and TOTAL refusals down "
                          "on 6 of 6, refusal rate 19.67% -> 0.40% on three. Kept because "
                          "`buttons` seed 1 settled two guarded terms under a PRICED guard. "
                          "Returns ON only under Isaiah's settled/unsettled rule",
    "TETHER_AIMED_CURIOSITY": "the CURIOSITY exit names a subject -- the slot with the "
                              "most unexplained surprise that it has also watched move "
                              "(Figure 5's *large and compressible*) -- instead of "
                              "exploring with none. **ON BY DEFAULT, and the flag exists "
                              "so the before/after is ONE SCRIPT WITH ONE FLAG rather "
                              "than two code states.** The `bored()` exit is NOT behind "
                              "it and never becomes aimed: that draw's uninformedness is "
                              "a safety property, not an arm. `F401`: 3 of 3 seeds on "
                              "`buttons` bind a slot where none ever bound. Spelled "
                              "`get(..., \"1\") != \"0\"`, read here as default-on",
    "TETHER_BARGAIN_FIT": "library fit priced by the bargain rather than by fit alone. "
                          "**ON BY DEFAULT SINCE 2026-09-30 -- Isaiah's ruling, and the "
                          "flip LANDED** once the four M2 failures holding it were "
                          "diagnosed. None was a capability the flip removed: one check "
                          "was vacuous, two were green only on a phantom scope and are "
                          "owed under ruling 6, and one was not isolated from the want "
                          "state. Spelled `get(..., \"1\") != \"0\"`, which this census "
                          "reads as default-on",
    "TETHER_DOWNRATE": "the agent discounts a scope member it has watched through at "
                       "least one press of every action it has and never once seen move. "
                       "**DEFAULT OFF, AND THE DEFAULT IS THE OPEN QUESTION.** The "
                       "arithmetic is ruled (Isaiah, 2026-10-01: an all-inert scope makes "
                       "downrating STEP ASIDE to the unweighted degree -- never silence a "
                       "goal on inertness alone) and the policy is built. What is NOT "
                       "settled is whether discounting makes the agent choose better or "
                       "makes it disturb goals that already hold: with it on, the toy "
                       "fixture loses 3 refusal rows and gains 8 `decision` rows while NO "
                       "residual differs at the final state. **That is a behaviour question "
                       "and it is Isaiah's, to be ruled on a gridworld A/B rather than on "
                       "the toy** -- so the switch exists to make that A/B one script with "
                       "one flag. Spelled `get(..., \"0\") != \"0\"`, default-off",
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
    "TETHER_CELL_CHANGE": "WHERE a matched object's cells changed -- added/removed counts and "
                          "centroids, read only where identity is sure. OFF until measured: it "
                          "adds six slots per object and six atoms, so it prices every term "
                          "(F492)",
    "TETHER_DELTA_KEY": "route (b) re-keyed on this frame's delta",
    "TETHER_NOT_ATOM": "not-t priced as one atom slot instead of the bits to name which "
                       "predicting term is wrong (the default, reviewer 2026-10-07). The figures "
                       "leave the price OPEN; this arm keeps the alternative readable (F496)",
    "TETHER_DELTA_OPERANDS": "deltas offered as operands",
    "TETHER_GUARD_AXIS": "the guard axis in the reject key",
    "TETHER_INSTRUMENTS": "the embedded instrument set -- Part 12 item 3, PAID BILLS from "
                          "frame 0. Off at a COSTED price: a new attribute widens the slot "
                          "set and §12.12 prices that in EPISODES FORGONE",
    "TETHER_HOLD": "THE RANDOMISED HOLD -- MEASUREMENT ONLY, the reviewer 2026-10-03 "
                   "ruling 3. Withholds the ACTED_SELF offer on a seeded ~half of "
                   "ELIGIBLE (cycle, slot) occasions so a measurement run carries its "
                   "own within-run control. OFF in the shipping agent: a control that "
                   "changes what the agent is OFFERED is an instrument, and leaving it "
                   "on would make every later reading a reading of the instrument",
    "TETHER_HOLD_SEED": "the hold's seed, so the withheld pattern is REPRODUCIBLE and "
                        "a row can be replayed. An unseeded flip makes the treatment "
                        "unrecoverable, and a row whose treatment cannot be "
                        "reconstructed cannot be checked",
    "TETHER_ITERATE": "the fold constructs -- `cells`/`cell_row`/`cell_col`/`count_true`. "
                      "§12.0 rules the MEANS to iterate is INHERITANCE where a solved case "
                      "would be an answer, and the agent could hold a cell set and not walk it. "
                      "**RULED ON by Isaiah 2026-09-24 and set in `arc_holdout.play` for the "
                      "ARC path, so the env census below reads OFF while the capability is "
                      "LIVE.** A ruling turned it on, not a measurement -- the house rule is "
                      "his to override. The toy world is untouched: it has its own atoms",
    "TETHER_NO_RESUME": "**INVERTED POLARITY, the THIRD such row.** A DEFAULT-ON frontier in "
                        "`_mint`: under an unchanged scope key a chain already priced is not "
                        "priced again, and a search that stopped at the budget resumes past "
                        "what it refused (plan item 7, F485). A BEHAVIOUR change, not only an "
                        "optimisation: on gridworld it adds binds. The variable turns it OFF, "
                        "so the A/B is one script with one flag. Inert on the ARC path while "
                        "the shape-decode arm puts the cycle in the key",
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


# **THE CENSUS WAS BLIND TO A DEFAULT-ON ARM AND THAT IS WHY THE NAMES HAD TO CARRY IT.**
# `on` is built from the ENVIRONMENT plus `_RULED`, so an arm whose DECLARATION defaults to
# true is reported OFF while the agent runs with it ON -- the one state a census must never
# get wrong. The project's answer had been spelling: `TETHER_NO_TALLY` and
# `TETHER_NO_CARRY_CANDIDATE` put the inversion in the NAME so a READER could see what the
# SEAT could not. **That is a convention holding up a blind spot**, and when Isaiah ruled
# `TETHER_BARGAIN_FIT` on by default there was no honest way to spell it -- the ruling names
# that arm, not its negation. So the seat learns to see the form instead.
#
# Two spellings, both already in the tree: `not os.environ.get("X")` and
# `os.environ.get("X", "1") != "0"`.
_DEFAULT_ON = re.compile(
    r'^\s*_[A-Z0-9_]+\s*=\s*(?:not\s+os\.environ\.get\(|os\.environ\.get\()')
_FALSY_DEFAULT = re.compile(r'''os\.environ\.get\(\s*["']TETHER_[A-Z0-9_]+["']\s*\)\s*$''')


def defaults_on() -> dict[str, str]:
    """`{arm: "file:line"}` for arms whose DECLARATION is true with nothing exported.

    Keyed on the ARM NAME IN THE LINE, not on the module variable, because the inverted
    spellings deliberately differ (`_TALLY` <- `TETHER_NO_TALLY`). Read from the code like
    every other census here: the table is the CLAIM and this is the WORLD.

    **DECIDED BY EVALUATING THE LINE, NOT BY PATTERN-MATCHING ITS SHAPE.** A regex over
    spellings would go stale the next time someone writes a third one, and the question --
    *is this true with an empty environment* -- has an exact answer.
    """
    out: dict[str, str] = {}
    for path in _tracked():
        if path.name == "arms.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for i, line in enumerate(text.split("\n"), 1):
            arms = _READ.findall(line)
            if not arms or "=" not in line:
                continue
            expr = line.split("=", 1)[1].strip()
            try:
                # NO ENVIRONMENT AT ALL, so the reading is of the DECLARATION and not of the
                # shell this seat happens to run in.
                val = eval(expr, {"os": type("o", (), {"environ": {}})()})  # noqa: S307
            except Exception:
                continue
            if val:
                for arm in arms:
                    out[arm] = f"{path.relative_to(ROOT).as_posix()}:{i}"
    return out


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

    # E -- RETIRED: a retired flag read anywhere is refused; and the control, so the case
    # cannot pass by refusing everything.
    bad = _judge(found, dict(table), on=set(), pairs=(), retired={"TETHER_A": "gone"})
    out["E retired read"] = ("ok" if any("RETIRED" in b for b in bad)
                             else f"UNWITNESSED ({bad})")
    bad = _judge(found, dict(table), on=set(), pairs=(), retired={"TETHER_GONE": "gone"})
    out["E control"] = ("ok" if not any("RETIRED" in b for b in bad)
                        else f"UNWITNESSED (an absent retired arm was refused: {bad})")

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


# RETIRED ARMS: the ruling that retired each, so the refusal carries its own reason.
RETIRED = {
    "TETHER_INVENT": "Isaiah 2026-10-04: inventing is just a bootleg composition -- fix "
                     "composition and imports and you will not need this crutch. Measured: "
                     "53 invented, 0 priced, 0 bound, 7 delta maps all fragments of `inc`.",
}


def _judge(found: dict, table: dict, on: set, pairs: tuple,
           retired: dict = RETIRED) -> list[str]:
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
    # **RETIRED MEANS GONE -- the reviewer, 2026-10-05.** The earlier guard only refused a
    # retired arm being ON while its code stayed in the tree. The code is now removed, so the
    # guard refuses the arm being READ ANYWHERE or DECLARED: a returning flag is a breach.
    for arm in sorted(retired):
        if arm in found:
            bad.append(f"RETIRED     {arm} is read at {found[arm][0]} and is retired. "
                       f"{retired[arm]}")
        if arm in table:
            bad.append(f"RETIRED     {arm} is retired and still has a registry row")
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
    dflt = defaults_on()
    # A DEFAULT-ON ARM IS ON. Three routes now, not two -- and the third is the one the
    # census could not see, so every count it printed was understating what the agent
    # runs with. An explicit falsy override still wins: `X=0` means off.
    on = ({a for a in found if os.environ.get(a)}
          | set(rule)
          | {a for a in dflt if os.environ.get(a, "1") != "0"})
    bad = _judge(found, ARMS, on, PAIRS)

    print(f"arms: {len(found)} switches at {sum(len(v) for v in found.values())} read sites; "
          f"{len(on)} ON -- environment, ruling and default together")
    if dflt:
        # **WORDED SO AN INVERTED NAME CANNOT BE READ BACKWARDS.** Saying
        # "TETHER_NO_TALLY is ON" invites exactly the wrong conclusion -- the BEHAVIOUR is
        # live and the variable turns it OFF. What is true of all three is that the
        # DECLARATION evaluates true with an empty environment, so that is what is printed.
        print(f"      {len(dflt)} LIVE WITH AN EMPTY ENVIRONMENT -- the declaration is true "
              f"and the variable turns the behaviour OFF:")
        for arm in sorted(dflt):
            print(f"        {arm:<26} {dflt[arm]}")
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
