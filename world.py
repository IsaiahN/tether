"""The world, and the eight-slot contract an adapter must satisfy.

If a domain cannot fill all eight members, the framework has not been instantiated there;
it has been mentioned there. So a partial adapter fails at construction, not at run time.

The env here is a symbolic transition world: named slots holding typed values, each with a
hidden per-slot rule, and a ground that is exact match on the next state -- mechanical,
instant, constitutive. There is deliberately no perception layer: a gridworld would test
perception and the loop at once, and then a failure is ambiguous.

One slot's rule is provably outside closure(Gamma) for any budget: every atom below is
affine-with-a-modulus, and OPAQUE is quadratic. The agent is told nothing about this.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from gamma import NOT_RESOLVED, Atom, Ctx

sys.dont_write_bytecode = True

# THE GOAL SLOT'S NAME, SHARED WITH `arc_world` BY SPELLING AND NOT BY IMPORT -- the two
# worlds must not depend on each other, and the fixture asserts the string, so a drift between
# them fails the seat rather than going quiet.
GOAL_SLOT = "@goal.completed"

M = 7   # anchor: prime, and small enough that the harness can sweep the whole
#         domain exhaustively -- which is what makes unreachable_slots a proof
ACTIONS = ("A", "B", "C")
DELTA = {"A": 1, "B": 2, "C": 4}

# Ten members. `actions` and `alphabet` were the two the loop used to reach past the
# contract for, which is why its action set could not grow: a language-level import is a
# step-7 IMPORT executed by the import system instead of by the loop.
REQUIRED = ("substrate", "environment", "actors", "currency", "ground",
            "slots", "atoms", "transform", "actions", "alphabet")


@runtime_checkable
class Env(Protocol):
    """The eight members. Q26 as an import error rather than a paragraph."""

    def substrate(self) -> str: ...
    def environment(self) -> str: ...
    def actors(self) -> str: ...
    def currency(self) -> str: ...
    def ground(self) -> str: ...
    def slots(self) -> list[str]: ...
    def atoms(self) -> list[Atom]: ...
    def transform(self) -> Any: ...
    def actions(self) -> tuple[str, ...]: ...
    def alphabet(self) -> int | dict[str, int]: ...


def bind(env: Any) -> Any:
    """Refuse an adapter that cannot fill all eight."""
    missing = [m for m in REQUIRED if not callable(getattr(env, m, None))]
    if missing:
        raise TypeError(f"env fills {len(REQUIRED) - len(missing)}/{len(REQUIRED)} "
                        f"of the contract; missing: {missing}")
    return env


def _atoms() -> list[Atom]:
    def idn(v, _c):
        return v

    def inc(v, _c):
        return v + 1

    def dec(v, _c):
        return v - 1

    def dbl(v, _c):
        return v * 2

    def neg(v, _c):
        return -v

    def wrap(v, _c):
        return v % M

    fns = [idn, inc, dec, dbl, neg, wrap]
    out = [Atom(f.__name__, f, "val", "val", same_as_slot=True) for f in fns]

    def take(v, c):
        """Read the bound operand slot instead of my own value. The one atom that makes
        an interaction expressible at all."""
        return c.operands[0] if c.operands else v

    out.append(Atom("take", take, "val", "val", same_as_slot=True, reads_operand=True))

    # -- THE OBJECTIVE VOCABULARY -- Isaiah, 2026-09-24, option A --------------------------
    #
    # **THE FIXTURE FOUND THAT THIS WORLD COULD NOT EXPRESS A WANT AT ALL.** Every atom above
    # is `val -> val`, so the type graph was a single node: no chain could end at `OBJ`, the
    # objective stream was asked 17 times and answered 0, and `objective_step` -- the
    # decomposer -- could never run. Three stages of the chain were dead on one cause.
    #
    # **`EXTENT -> PRED -> OBJ`, mirroring `arc_atoms`' relate/quantify split.** Same names and
    # same semantics on purpose, so the fixture asserts ONE vocabulary across both worlds --
    # **and they are DECLARED TWICE, which is a real hazard**: `arc_atoms` records the same
    # risk for `ATTRIBUTE_TYPE`, *two producers of one fact, harmless exactly until one side
    # changes.* This world may not import `arc_atoms` (one registry, and the toy must not
    # depend on the domain), so the duplication is the price and it is named rather than hidden.
    #
    # **AND THE COST OF GROWING THIS WORLD IS REAL -- reviewer, 2026-09-24, recorded at the
    # site rather than left to pass.** *The toy world's value was being SMALL ENOUGH TO REASON
    # ABOUT COMPLETELY.* Every atom added here is a thing that **can be true here and false on
    # a board**, and enough of them turn this from a minimal reference into **a second
    # agent-world with its own quirks** -- at which point a green seat stops meaning what it
    # means today. **Weigh each addition against that, not against whether a stage goes green.**
    #
    # **NOT ONE OF THESE KNOWS ANYTHING ABOUT THE GOAL, AND THAT IS THE WHOLE CARE TAKEN.**
    # This world's objective is *ALL slots at zero*, so an `is_zero` predicate would have BEEN
    # the answer -- `all . is_zero` is the goal, written out. **Every predicate here is
    # RELATIONAL: it compares this slot to ANOTHER slot.** The agent can say *these two agree*
    # and must still discover that agreeing on zero is what wins.

    def same(v, c):
        return int(v == c.operands[0]) if c.operands else NOT_RESOLVED

    def other(v, c):
        return int(v != c.operands[0]) if c.operands else NOT_RESOLVED

    def above(v, c):
        return int(v > c.operands[0]) if c.operands else NOT_RESOLVED

    for f in (same, other, above):
        out.append(Atom(f.__name__, f, "EXTENT", "PRED", reads_operand=True,
                        operand_type="EXTENT", reads_ctx=("operands",)))
    # WHAT CLOSES A STATEMENT BACK INTO SOMETHING BETTABLE. `arc_atoms._quantify`, verbatim.
    out.append(Atom("all", lambda v, _c: int(bool(v)), "PRED", "OBJ"))
    out.append(Atom("any", lambda v, _c: int(bool(v)), "PRED", "OBJ"))
    out.append(Atom("none", lambda v, _c: int(not v), "PRED", "OBJ"))
    return out


# the hidden rules. Names are for the harness's report, never shown to the agent.
def _steady(v, _a, _s):
    return v


def _climb(v, _a, _s):
    return (v + 1) % M


def _swing(v, _a, _s):
    return (-v + 1) % M


def _driven(v, a, _s):
    return (v + DELTA[a]) % M


def _opaque(v, _a, _s):
    return (v * v + 3) % M      # quadratic: no composition of affine atoms reaches it


def _ladder(v, _a, _s):
    """Four atoms deep -- `dbl . neg . inc . wrap` -- which is PAST max_depth, so it is
    unreachable in atoms. It is `dbl` applied to SWING's rule, so once swing settles and
    becomes one unit it is two units deep and reachable. Nothing was added to the closure;
    only the grain of the search changed. This slot is the chunking claim's falsifier.

    **AND IT DOES NOT FALSIFY -- `F349`, 2026-09-24.** The four-atom decomposition above is
    correct and is NOT THE SHORTEST ONE. `dbl . dec . neg` is `-(2v - 1)` = `-2v + 1`, which is
    this rule exactly, and it is **THREE** atoms: measured in `closure("val","val", d=3)` over
    ATOMS ALONE, with no settled unit. **The demo binds that chain.**

    So the slot that exists to show chunking reached something atoms could not **is reached by
    atoms**, and the claim was resting on the decomposition rather than on the closure.

    NOT REPAIRED HERE. Every fix -- drop `dec`, lower the depth, change this rule -- alters what
    the falsifier CAN SHOW rather than what the agent does, which is `F341`'s CALIBRATION
    category and not the seat's to take. **When it stopped holding is undetermined; the obvious
    git grep is the wrong instrument for those revisions and its zero is not evidence.**"""
    return (-(v * 2) + 1) % M


def _chase(_v, _a, s):
    """An INTERACTION: this slot's next value is a function of ANOTHER slot's current one,
    and its own value is irrelevant. Unreachable without operand arity, by construction."""
    return (s["climb"] + 1) % M


RULES = {"steady": _steady, "climb": _climb, "swing": _swing,
         "driven": _driven, "opaque": _opaque, "chase": _chase, "ladder": _ladder}

# what the harness knows and the agent does not. Used only to score the demo.
TRUTH = {"steady": "idn (an atom: the answer was already known)",
         "climb": "inc . wrap",
         "swing": "neg . inc . wrap",
         "driven": "act . wrap",
         "opaque": "UNREACHABLE from these atoms -- quadratic, they are all affine",
         "chase": "take<climb> . inc -- an interaction; needs operand arity",
         "ladder": "dbl . neg . inc . wrap -- 4 atoms, past max_depth; 2 units after swing"}


@dataclass
class Transitions:
    """The symbolic transition world."""

    start: dict[str, int] | None = None

    def __post_init__(self) -> None:
        self.state: dict[str, int] = dict(self.start or
                                          {"steady": 3, "climb": 0, "swing": 2,
                                           "driven": 1, "opaque": 2, "chase": 5,
                                           "ladder": 4})

    # -- the eight -------------------------------------------------------------------

    def substrate(self) -> str:
        return f"named slots holding integers mod {M}"

    def environment(self) -> str:
        return f"a hidden per-slot rule; the shaping medium is arithmetic mod {M}"

    def actors(self) -> str:
        return f"the actions {ACTIONS}, which move one slot and are contact for the rest"

    def currency(self) -> str:
        return "prediction error in bits, per slot"

    def ground(self) -> str:
        return "exact match on the next state. Mechanical, instant, and it does not negotiate"

    def slots(self) -> list[str]:
        return sorted([*self.state, GOAL_SLOT])

    def atoms(self) -> list[Atom]:
        return _atoms()

    def actions(self) -> tuple[str, ...]:
        """What the domain advertises. Growth in this set is an IMPORT, and it can only
        be one if the loop asks rather than reads a module global."""
        return ACTIONS

    def alphabet(self) -> int | dict[str, int]:
        """|V|, the number of distinguishable values. The loop declares the code's FORM
        -- uniform over the alphabet -- and the domain supplies its size; a correction
        therefore costs log2(alphabet) bits and a value normalises mod alphabet.

        ONE NUMBER OR ONE PER SLOT. Every slot here holds an integer mod M, so one number
        says it. A domain whose slots differ -- a position, a colour, a boolean -- says so
        per slot, and each is then charged its own code rather than the widest one in the
        world. Charging a boolean log2(7) inflates its residual by the factor its
        information was reduced, and the bargain comes out loosest where least is at
        stake.

        **AND THIS WORLD NOW DIFFERS, SO IT SAYS SO -- 2026-09-24.** `@goal.completed` counts
        slots-at-goal, so it ranges `0..len(state)` -- **EIGHT values against M's SEVEN.** The
        uniform number would not merely be loose here, it would be WRONG: `correction_bits`
        normalises mod the alphabet, so a 7 would wrap to 0 and a full solve would read as no
        progress. **The paragraph above anticipated exactly this case and this is it.**
        """
        a: dict[str, int] = dict.fromkeys(self.state, M)
        a[GOAL_SLOT] = len(self.state) + 1
        return a

    def slot_types(self) -> dict[str, str]:
        """What KIND of quantity each slot holds. **THE DOMAIN DECLARES; THE LOOP MAY NOT
        DERIVE IT** -- the same contract `arc_world` has always met and this world never did.

        **AND THAT OMISSION MADE A WHOLE SUBSYSTEM UNTESTABLE IN CI -- found 2026-09-24 by the
        end-to-end fixture.** `mint` appends the objective stream only `if stype`, so with no
        types declared **no `OBJ` candidate is ever enumerated, nothing ever binds one, and
        `objective_step` -- the decomposer -- can never run.** The seat suite's only world could
        not express an objective, so every objective mechanism built since has been green in CI
        and unexercised by it. **Not a design choice: a missing member of the domain contract.**

        EXTENT FOR ALL SEVEN, AND IT IS THE HONEST FIT RATHER THAN A CONVENIENCE. Each slot
        holds a non-negative integer produced by arithmetic (`inc`, `neg`, `dbl`, `wrap`,
        `act`, `take`), and the world's own goal -- *ALL slots at zero* -- treats the value as a
        MAGNITUDE with a target, which is what an extent is. `COUNT` is not in the importable
        set, exactly as `arc_atoms` records for `contact`.

        **THE CAVEAT, STATED BECAUSE IT IS REAL: the values are MOD M, so the order is CYCLIC
        and not linear.** `objective_step`'s ordered arm walks outward from the current value,
        which is meaningful locally and does not know the wrap. **It is the right declaration
        and it is not a perfect one**, and a later reader should know that before trusting a
        distance here.
        """
        return dict.fromkeys(self.slots(), "EXTENT")

    def transform(self) -> Any:
        """No coarse view is defined for this env, so the bracket channel is inert here.
        Stated rather than omitted: the channel exists and this world does not feed it."""
        return None

    # -- running ---------------------------------------------------------------------

    def _completed(self) -> int:
        """HOW MANY SLOTS ARE AT THE GOAL. **ONE SITE, because `objective()` and the published
        `@goal.completed` slot are the SAME QUANTITY** -- two computations of one number is the
        `A6i` collision waiting to happen, and this is the cheapest place to refuse it."""
        return sum(1 for v in self.state.values() if v % M == 0)

    def objective(self) -> tuple[str, float]:
        """ALL slots at zero. Returns (name, degree in [0,1]); R_goal is 1 - degree."""
        return "ALL(BECOME(slot, 0))", self._completed() / len(self.state)

    def observe(self) -> dict[str, int]:
        """**AND THE GOAL IS A SLOT HERE TOO -- Isaiah 2026-09-24.** The fixture's GOAL stage
        read DEAD on this world because `@goal.completed` was added to `arc_world` and not to
        the harness the fixture actually runs on. **A capability wired into one world is the
        orphan class this whole seat exists to catch**, and it caught mine.

        DERIVED, NEVER STORED. It is not in `self.state`, so `step`'s `% M` cannot mutate it
        and no rule can write it -- the agent PERCEIVES the count and nothing here lets it
        set the count.
        """
        return {**self.state, GOAL_SLOT: self._completed()}

    def step(self, action: str) -> None:
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        before = dict(self.state)
        self.state = {k: RULES[k](v, action, before) % M for k, v in before.items()}


def unreachable_slots(env: Transitions, gam, max_depth: int, budget: int) -> list[str]:
    """What the HARNESS knows by exhaustive check, and the agent never sees. Used only to
    score abstention: a slot no term in the enumerated closure predicts on every action,
    under any operand binding."""
    # **A DERIVED SLOT HAS NO RULE, AND THAT IS NOT THE SAME AS BEING UNREACHABLE.**
    # `@goal.completed` is a function of the OTHER slots, so there is no transition for a term
    # to match and no honest verdict to return -- including it as unreachable would score the
    # agent for failing to predict something this checker cannot state a target for. Excluded
    # on a CHECKABLE FACT (absent from `RULES`), never on judgement, and the exclusion expires
    # the moment the slot acquires a rule.
    slots = [s for s in env.slots() if s in RULES]
    out = []
    for slot in slots:
        rule = RULES[slot]
        binds = [None] + [s for s in slots if s != slot]
        ok = False
        for term in gam.enumerate_closure("val", "val", max_depth, budget):
            for b in binds:
                good = True
                for v in range(M):
                    for a in ACTIONS:
                        st = {s: (v if s == slot else (v + 1) % M) for s in slots}
                        ops = (st[b],) if b else ()
                        if term.apply(v, Ctx(action=a, operands=ops)) % M != rule(v, a, st) % M:
                            good = False
                            break
                    if not good:
                        break
                if good:
                    ok = True
                    break
            if ok:
                break
        if not ok:
            out.append(slot)
    return out
