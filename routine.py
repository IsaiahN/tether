"""The ACT space: `state -> action`, with sequence, condition and repetition.

§14.3, whose whole point is that this is a **new object kind and not another pipeline**:

    sensor    state -> attr
    predicate state -> bool
    term      slot x action -> slot

*All three are pipelines, and pipelines compose by chaining. But "go to the door, press the
button, come back" is none of those.* **You cannot build it by chaining functions**, which is
why the composition story felt thin -- half the objects the agent needs were not in the algebra.

    Routine ::= Act(a) | Seq(R1, R2) | When(P, R) | Until(P, R)

**THE REMAINDER IS ITSELF A ROUTINE, AND THAT IS THE WHOLE OF HOW THIS SURVIVES A STEP.**
`advance` returns *what to do now* and *what is left*, and what is left is a `Routine` -- so a
behaviour spanning many cycles needs ONE field in the loop, not a program counter with an index
into a script. It also means a routine caught mid-execution is a routine, so it can be recorded,
inspected and priced like any other.

**THE ALGEBRA NEVER TOUCHES A TERM.** Guards are opaque here; the caller supplies `holds`. That
is Guard B by construction -- the pricing bypass was `t.apply` called directly at a site that
should have gone through `_value_of`, and this module has no way to call either.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

sys.dont_write_bytecode = True

# THE THREE TERMINATIONS, AND THEY ARE THREE BECAUSE THEY ARE THREE CLAIMS. Collapsing
# `EXHAUSTED` into `DONE` would report a routine that ran out of budget as one that achieved its
# guard, which is the failure `M2_STANDARD` calls looking like planning while looping on a bad
# guard. Collapsing `BLOCKED` into `DONE` is check 3 again: *I could not read the guard* is not
# *the guard is satisfied*.
DONE, BLOCKED, EXHAUSTED = "done", "blocked", "exhausted"
_ENDS = (DONE, BLOCKED, EXHAUSTED)


@dataclass(frozen=True)
class Act:
    """One primitive action, named as the environment advertises it."""
    action: str


@dataclass(frozen=True)
class Seq:
    """Do, then do."""
    first: Any
    then: Any


@dataclass(frozen=True)
class When:
    """Guarded: run the body only if the guard holds. A false guard COMPLETES the routine --
    there is nothing to do -- and an unreadable one BLOCKS it, which are different claims."""
    guard: Any
    body: Any


@dataclass(frozen=True)
class Until:
    """Repeat the body until the guard holds.

    **THE ONE THAT MATTERS.** §14.3: *it turns a one-step action into a behaviour with a
    termination condition, which is what "navigate to X" actually is. Without it every routine
    is a fixed-length script and depth explodes on the first navigation problem.*

    `budget` IS DERIVED AT CONSTRUCTION, NEVER PICKED -- the caller passes the objective's own
    gap, because a guard `g` units away that closes needs at most `g` iterations. **It is the
    difference between a bound and a magic number**, and the constructor cannot supply it
    itself, which is why it is a field rather than a default.

    **AND IT IS THE SECOND GUARD, NOT THE FIRST.** The first is `CAN(P) == yes` at the point of
    construction: a satisfiable-but-unreachable guard is the loop that never ends, and no
    budget makes that safe -- it makes it silent. The budget catches the case `CAN` said yes to
    and the world did not honour.
    """
    guard: Any
    body: Any
    budget: int


def advance(r: Any, holds: Callable[[Any], bool | None]) -> tuple[str, Any]:
    """`(emit, rest)` -- the action to take now and the routine that remains.

    `emit` is an action name, or one of `DONE` / `BLOCKED` / `EXHAUSTED`. `rest` is `None` when
    nothing remains. **A step of a routine is itself total**: every shape returns, and the three
    terminations are the only ways out that are not an action.

    `holds(guard) -> True | False | None`, and `None` is *I could not read it*. The caller owns
    that; this module never evaluates a predicate.
    """
    if isinstance(r, Act):
        return r.action, None

    if isinstance(r, Seq):
        emit, rest = advance(r.first, holds)
        if emit == DONE:
            return advance(r.then, holds)          # the first part had nothing left to do
        if emit in _ENDS:
            return emit, None                      # blocked or exhausted stops the sequence
        return emit, (Seq(rest, r.then) if rest is not None else r.then)

    if isinstance(r, When):
        h = holds(r.guard)
        if h is None:
            return BLOCKED, None
        if not h:
            return DONE, None
        return advance(r.body, holds)

    if isinstance(r, Until):
        # ITERATIVE, NOT RECURSIVE. A body that completes without emitting would recurse once
        # per iteration, so a large derived budget would hit the interpreter's stack before it
        # hit its own bound -- a termination failure caused by the termination guard.
        guard, body, budget = r.guard, r.body, r.budget
        while True:
            h = holds(guard)
            if h is None:
                return BLOCKED, None
            if h:
                return DONE, None                  # the guard holds: this is what terminates
            if budget <= 0:
                return EXHAUSTED, None
            emit, rest = advance(body, holds)
            if emit == DONE:
                budget -= 1                        # one iteration bought nothing; go again
                continue
            if emit in _ENDS:
                return emit, None
            nxt = Until(guard, body, budget - 1)
            return emit, (Seq(rest, nxt) if rest is not None else nxt)

    raise TypeError(f"not a routine: {r!r}")


def length(r: Any, chunks: tuple = ()) -> int:
    """How many constructors the routine is made of. **The cost side of the one bargain.**

    §14.4 prices all three spaces with `pays(cost, left, base)`, so a routine needs a length the
    way a term does -- and it is counted the same way, over the object rather than over its
    behaviour. **A loop counts once, not once per iteration**: `Until` is what makes *navigate*
    ONE chunk of depth 2, and charging it per iteration would price away the thing it exists for.

    `chunks` IS ACT CHUNKING, AND IT IS `gamma.units()`'s RULE RATHER THAN A SECOND ONE. There:
    *the atoms, plus every SETTLED term as one unit -- **only what the ground has paid for
    becomes a shortcut.*** Here: a settled routine counts as ONE, so a composition that was too
    long to pay becomes affordable **exactly when the ground has already paid for its parts**.
    The closure does not change and no constructor is added; what changes is what a given budget
    can reach. §14.4: *a settled routine becomes a callable step inside a bigger routine -- that
    is stacking, and it is the same rule three times.*
    """
    if r in chunks:
        return 1
    if isinstance(r, Act):
        return 1
    if isinstance(r, Seq):
        return 1 + length(r.first, chunks) + length(r.then, chunks)
    if isinstance(r, (When, Until)):
        return 1 + length(r.body, chunks)
    raise TypeError(f"not a routine: {r!r}")


def guards(r: Any) -> tuple:
    """Every guard in the routine, so a caller can check `CAN` on all of them.

    **`M2_STANDARD` 3: trace the route at EVERY constructor, not just the first.** A nested
    `Until` whose guard nobody checked is the durable contamination the standard names.
    """
    if isinstance(r, Act):
        return ()
    if isinstance(r, Seq):
        return guards(r.first) + guards(r.then)
    if isinstance(r, (When, Until)):
        return (r.guard,) + guards(r.body)
    raise TypeError(f"not a routine: {r!r}")


def actions(r: Any) -> tuple:
    """Every primitive action the routine can emit. Used to check a routine against what the
    environment currently advertises -- a routine that survives a level boundary may name an
    action the new level does not offer."""
    if isinstance(r, Act):
        return (r.action,)
    if isinstance(r, Seq):
        return actions(r.first) + actions(r.then)
    if isinstance(r, (When, Until)):
        return actions(r.body)
    raise TypeError(f"not a routine: {r!r}")


def render(r: Any) -> str:
    """One line, readable in a ledger row. The legibility rule applies to the ACT space too."""
    if isinstance(r, Act):
        return r.action
    if isinstance(r, Seq):
        return f"{render(r.first)} ; {render(r.then)}"
    if isinstance(r, When):
        return f"when({r.guard}) {{{render(r.body)}}}"
    if isinstance(r, Until):
        return f"until({r.guard}/{r.budget}) {{{render(r.body)}}}"
    raise TypeError(f"not a routine: {r!r}")


def enumerate_routines(actions: tuple, guards: tuple, chunks: tuple = (),
                       loop_budget: int = 1, cap: int = 200) -> list:
    """Type-valid routines over the ACT space, **shortest first, capped by budget** -- the
    same discipline as `gamma.enumerate_closure` and deliberately not a second one.

    **NAMED FOR THE ONE IT PARALLELS, AND IT WAS `compose` UNTIL A SWEEP TRIPPED OVER IT.**
    `grammar.compose` type-checks an utterance; this enumerates routine SHAPES. Two
    operations, one word, in one codebase -- `A6i`, and mine. **The rename also makes the
    ACT space's relationship to the PREDICT space readable**: `enumerate_closure` walks
    type-valid pipelines over units, this walks type-valid routines over actions and
    guards, and the shared name says the shared discipline.

    **THE COMPOSER WAS A TEMPLATE.** `_mint_routine` built `Until(guard, Act(a), n)` and
    nothing else: `When` was constructed NOWHERE, and `Seq` only inside `advance` as a
    remainder. **§14.4 says the ACT space composes by `Seq / When / Until` and it composed by
    one** -- which is the defect `WANT` had, the seat hand-building the single shape the agent
    was supposed to reach.

    SHORTEST FIRST FOR `enumerate_closure`'s REASON: the bargain prices length, so a cheap
    shape that pays should be found before an expensive one is built. And **capped**, because
    the space is a product of actions x guards and grows without a bound of its own.

    **NO NEW CONSTRUCTORS AND NO NEW TYPES.** This enumerates what §14.3 already declared,
    over the actions the environment advertises and the guards the agent has objectives for.
    A chunk enters as a unit exactly as a settled term does in `gamma.units`.
    """
    base = [Act(a) for a in actions] + list(chunks)
    out = list(base)
    for b in base:
        for g in guards:
            out.append(Until(g, b, loop_budget))
            out.append(When(g, b))
    for b in base:                       # depth 2 sequences, over primitives only
        for c in base:
            out.append(Seq(b, c))
    seen, uniq = set(), []
    for r in out:
        k = render(r)
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    uniq.sort(key=length)
    return uniq[:cap]


def reach(r: Any) -> int:
    """How many members of a scope this routine can address before it ends.

    **`left` IN THE BARGAIN, AND IT WAS BEING ASSERTED AS ZERO.** Every candidate was priced
    with `pays(cost, 0.0, base)` -- *this routine closes the entire goal residual* -- which was
    defensible only while the single shape on offer was an `Until` whose budget was derived to
    close it. **The moment the composer offered a bare `Act`, the cheapest candidate claimed to
    close a residual of five with one action, and won.**

    So the reach is counted from the object: one action does one, a sequence does the sum, a
    loop does its budget's worth, and a guard passes its body's through. **`left` is then the
    part of the residual the candidate does NOT reach**, which is what the two-part bargain
    means by it -- and pricing a plan against a residual it cannot close is exactly the *term
    that explains everything by saying nothing* the bargain exists to refuse.
    """
    if isinstance(r, Act):
        return 1
    if isinstance(r, Seq):
        return reach(r.first) + reach(r.then)
    if isinstance(r, When):
        return reach(r.body)
    if isinstance(r, Until):
        return max(r.budget, 0) * reach(r.body)
    raise TypeError(f"not a routine: {r!r}")
