"""The ACT space: `state -> action`, with sequence, condition and repetition.

§14.3, whose whole point is that this is a **new object kind and not another pipeline**:

    sensor    state -> attr
    predicate state -> bool
    term      slot x action -> slot

*All three are pipelines, and pipelines compose by chaining. But "go to the door, press the
button, come back" is none of those.* **You cannot build it by chaining functions**, which is
why the composition story felt thin -- half the objects the agent needs were not in the algebra.

    Routine ::= Act(a) | Seq(R1, R2) | When(P, R) | Until(P, R)
              | Choose(P, R1, R2)      -- the branch; `When` with the false arm restored
              | Try(R1, R2)            -- the fallback; branches on the OUTCOME, not a guard

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
class Choose:
    """TWO ARMS ON ONE GUARD READ -- the branch point, and nothing here could hold one.

    **`When` COLLAPSES *the guard is false* INTO *there is nothing to do*.** That is right for a
    guarded step, and it is the whole of why the ACT space has no decision in it: every plan the
    agent can write says DO THIS IF ALLOWED and none says CHOOSE BETWEEN THESE. **One guard read
    is three claims, exactly as the three endings are -- and the false reading was the one with
    nowhere to go.**

    **NOT DERIVABLE FROM WHAT WAS HERE, WHICH IS WHY IT IS A CONSTRUCTOR AND NOT SUGAR.**
    `Seq(When(P, A), When(not P, B))` needs `not P`, and this module never looks inside a guard --
    the caller owns evaluation, and that is the invariant that keeps the ACT space legible. So the
    negation cannot be formed here and the branch cannot be spelled here. One guard read, two arms,
    evaluation still outside.

    **AN UNREADABLE GUARD STILL BLOCKS**, and this is the constructor where that matters most. A
    one-armed `When` that blocks does nothing, which is visibly nothing; a branch that treated
    `None` as *take the other arm* would RUN, act, and never report that the choice was never
    made. *I could not read it* is not *it is false* -- check 3, at the one site where getting it
    wrong is invisible.
    """
    guard: Any
    body: Any
    otherwise: Any


@dataclass(frozen=True)
class Try:
    """A FALLBACK ON AN OUTCOME -- the second kind of chooser, and the other half of `Choose`.

    **`Choose` BRANCHES ON A GUARD READ BEFORE ACTING; THIS BRANCHES ON WHAT HAPPENED.** Those
    are different information and neither substitutes for the other: a guard says what the
    world is like now, an ending says what this plan turned out to be able to do.

    **THE GAP IT CLOSES IS `F207`'s.** The first routine this project ever formed died at
    `routine_end: blocked` -- and a blocked routine is simply ABANDONED. Nothing in the ACT
    space could say *and if that does not work, do this instead*, so every plan was
    all-or-nothing and the agent's only response to failure was to stop.

    **IT RECOVERS FROM `BLOCKED` AND `EXHAUSTED`, NEVER FROM `DONE`.** Those three are three
    claims, which is why they are three; `DONE` is the body succeeding and there is nothing to
    recover from. Folding it in would run the fallback after every success.

    **AND THE RECOVERY IS PUBLISHED, WHICH IS NOT OPTIONAL.** A routine that quietly recovers
    has destroyed the BLOCKED signal -- the ending `F207` was diagnosed from, and the one the
    refutation machinery reads. This module cannot write a ledger, so it does what `Expect`
    does: it puts the fact in `state` and the caller records it. **Legibility is the
    instrument, and a fallback is exactly the shape of thing that hides a failure while
    looking like robustness.**

    **THE FALLBACK STAYS ARMED ACROSS STEPS**, because the remainder is re-wrapped. *Try this
    whole routine* is the useful reading, not *try only its first step*.
    """
    body: Any
    otherwise: Any


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


@dataclass(frozen=True)
class Call:
    """CALL ANOTHER ROUTINE BY NAME -- the subroutine, Isaiah's first construct.

    **A NAME, NOT A BODY, AND THAT IS THE WHOLE POINT.** Inlining a body makes a longer script;
    a name makes a routine the agent can REFER to without holding it, which is what lets one
    settled routine become a step inside a bigger one without paying its length again.
    `length` already had the rule (`chunks` counts a settled routine as ONE) and there was no
    constructor that could invoke one.

    Resolved against the `lib` the caller passes to `advance`. An unknown name BLOCKS -- it does
    not raise and it does not silently do nothing, because *I was told to run something I cannot
    find* is a readable failure and a no-op is not.
    """
    name: str


@dataclass(frozen=True)
class Let:
    """CARRY ONE VALUE ACROSS THE ROUTINE'S OWN STEPS -- declared local state.

    **DECLARED, NOT INFERRED, AND WRITTEN INTO THE REMAINDER.** `advance` returns the routine
    that REMAINS, so a binding that lived only in a Python frame would vanish between steps. The
    `Let` node rebuilds itself around the rest, which is what makes the value survive.

    **THIS MODULE STILL NEVER EVALUATES A PREDICATE.** The value is published into the caller's
    `state` dict and the caller's own `holds` reads it. Keeping evaluation outside is the
    invariant that lets the ACT space stay legible.
    """
    var: str
    value: Any
    body: Any


@dataclass(frozen=True)
class Expect:
    """WHAT THIS STEP EXPECTS TO HAPPEN -- metacognition's attach half.

    **A ROUTINE THAT CANNOT BE WRONG MID-FLIGHT SPENDS ITS WHOLE BUDGET BEFORE ANYONE NOTICES.**
    Every other ending here is structural -- the body ran out (`DONE`), a guard was unreadable
    (`BLOCKED`), the budget went (`EXHAUSTED`). **None of them says *this is not going how I
    said it would*.** That reading needs a claim made BEFORE the step and checked after, and
    there was nowhere to put the claim.

    ONE QUANTITY, ONE SLOT, deliberately: the MVP is *did the thing I named change*, not a
    predicted value. A predicted VALUE needs the term space; a predicted CHANGE needs only the
    delta the agent already publishes.

    **IT WRAPS RATHER THAN REPLACES**, exactly as `Bonded` wraps `Term`: the body is any
    routine, so an expectation can sit on a single `Act` or on a whole `Until`, and nothing
    that already walks routines needs to know which.
    """
    slot: str
    body: Any


# A CALL CANNOT RECURSE FOREVER. `Until` is bounded by a DERIVED budget; a call has no natural
# one, so this is a STOP rather than a bound -- it exists to make runaway recursion EXHAUSTED
# (a readable ending) instead of a stack overflow.
# anchor: DECLARED CONVENTION, not derived, and the seat was right to stop me. `Until`'s budget
# is DERIVED -- the caller passes the objective's own gap -- and this one CANNOT be, because a
# call has no gap to measure. So it is the same class as the focus seat's `STALL`: authored,
# visible, movable, and claimed correct by nobody. It is a STOP, not a bound: its only job is to
# turn runaway recursion into EXHAUSTED (a readable ending the ledger can carry) instead of a
# stack overflow. 16 exceeds the deepest routine any enumeration has produced by a wide margin,
# so it should never be reached; if it IS reached that is a finding about the composer.
CALL_DEPTH = 16


def advance(r: Any, holds: Callable[[Any], bool | None],
            lib: dict | None = None, state: dict | None = None,
            _depth: int = 0) -> tuple[str, Any]:
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
        emit, rest = advance(r.first, holds, lib, state, _depth)
        if emit == DONE:
            return advance(r.then, holds, lib, state, _depth)   # first part had nothing to do
        if emit in _ENDS:
            return emit, None                      # blocked or exhausted stops the sequence
        return emit, (Seq(rest, r.then) if rest is not None else r.then)

    if isinstance(r, When):
        h = holds(r.guard)
        if h is None:
            return BLOCKED, None
        if not h:
            return DONE, None
        return advance(r.body, holds, lib, state, _depth)

    if isinstance(r, Choose):
        # ONE READ, TWO ARMS. `When` above is this with the false arm missing.
        h = holds(r.guard)
        if h is None:
            return BLOCKED, None
        return advance(r.body if h else r.otherwise, holds, lib, state, _depth)

    if isinstance(r, Try):
        # **A CLAIM MADE BY A STEP THAT DID NOT RUN IS NOT A CLAIM ABOUT WHAT RAN.** `Expect`
        # publishes into `state` as it is walked, so a body that publishes and THEN fails would
        # leave its claim standing -- and the caller attributes the pending claim to whatever
        # action the step emits, which by then is the FALLBACK's. Metacognition would record
        # *I expected this slot to move* about a routine that was abandoned before acting.
        #
        # UNREACHABLE TODAY AND GUARDED ANYWAY: `Expect` is only ever the OUTERMOST node
        # (`tether` wraps the chosen candidate) and the composer never builds one, so nothing
        # can nest it inside a `Try` body. **The cost is three lines and the failure is a FALSE
        # ROW in the record**, which is the one kind this project refuses to leave to luck.
        #
        # A `Let` BINDING IS DELIBERATELY NOT RESTORED: the body's remainder is discarded with
        # it, so the rebuilt `Let` is gone and no later step can read the value. It goes stale,
        # not wrong.
        _claims = len(state.get("expect", ())) if state is not None else 0
        emit, rest = advance(r.body, holds, lib, state, _depth)
        if emit in (BLOCKED, EXHAUSTED):
            if state is not None and len(state.get("expect", ())) > _claims:
                del state["expect"][_claims:]
            # PUBLISHED BEFORE THE FALLBACK RUNS, so the caller records the failure even if
            # the fallback then succeeds. The other order loses exactly the case this exists
            # for -- a recovery nobody can see is a failure nobody can see.
            if state is not None:
                state.setdefault("recovered", []).append(emit)
            return advance(r.otherwise, holds, lib, state, _depth)
        if emit == DONE:
            return DONE, None                      # the body succeeded: nothing to recover
        return emit, (Try(rest, r.otherwise) if rest is not None else None)

    if isinstance(r, Call):
        if lib is None or r.name not in lib:
            return BLOCKED, None                   # named something that is not there
        if _depth >= CALL_DEPTH:
            return EXHAUSTED, None                 # readable ending, not a stack overflow
        return advance(lib[r.name], holds, lib, state, _depth + 1)

    if isinstance(r, Let):
        if state is not None:
            state[r.var] = r.value
        emit, rest = advance(r.body, holds, lib, state, _depth)
        # REBUILT AROUND THE REST so the binding survives to the next `advance`.
        return emit, (Let(r.var, r.value, rest) if rest is not None else None)

    if isinstance(r, Expect):
        # **TRANSPARENT TO EXECUTION, AND THAT IS THE DESIGN.** The expectation is a claim about
        # what the NEXT delta will show, and this module never evaluates a predicate -- so it
        # publishes the claim through `state` and the caller checks it after the action lands.
        # Advancing here must not stall, or an expectation would cost a step to hold.
        if state is not None:
            state.setdefault("expect", []).append(r.slot)
        emit, rest = advance(r.body, holds, lib, state, _depth)
        return emit, (Expect(r.slot, rest) if rest is not None else None)

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
            emit, rest = advance(body, holds, lib, state, _depth)
            if emit == DONE:
                budget -= 1                        # one iteration bought nothing; go again
                continue
            if emit in _ENDS:
                return emit, None
            nxt = Until(guard, body, budget - 1)
            return emit, (Seq(rest, nxt) if rest is not None else nxt)

    raise TypeError(f"not a routine: {r!r}")


def _guard_excess(guard: Any) -> int:
    """What a guard costs BEYOND the one every guard has always cost.

    **STRUCTURE STAYS OPAQUE HERE; ONLY SIZE CROSSES.** This module's invariant is that it
    never looks inside a guard -- the caller owns evaluation, which is what keeps the ACT space
    legible and is why `Choose` had to be a constructor. A guard that can report its own `size`
    is priced by it; anything else is a leaf worth 1. **The protocol carries a number, not a
    shape**, so nothing here learns what a guard is made of.

    **AND IT IS THE EXCESS RATHER THAN THE SIZE, WHICH IS WHAT MAKES IT ADDITIVE.** A bare
    slot-name guard has size 1 and excess 0, so every price this module has ever computed is
    unchanged. Only a guard that says MORE than one thing pays more.
    """
    n = getattr(guard, "size", 1)
    return max(0, int(n) - 1) if isinstance(n, int) else 0


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
        return 1 + _guard_excess(r.guard) + length(r.body, chunks)
    if isinstance(r, Choose):
        # BOTH ARMS, LIKE `Seq`, because the OBJECT carries both and the object is what is
        # priced. Charging only the arm that runs would price a branch by its behaviour, which
        # is the thing `Until`'s rule two lines up refuses.
        return (1 + _guard_excess(r.guard)
                + length(r.body, chunks) + length(r.otherwise, chunks))
    if isinstance(r, Try):
        return 1 + length(r.body, chunks) + length(r.otherwise, chunks)
    if isinstance(r, (Let, Expect)):
        return 1 + length(r.body, chunks)
    if isinstance(r, Call):
        return 1                                   # a NAME costs one, not its body's length
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
    if isinstance(r, Choose):
        return (r.guard,) + guards(r.body) + guards(r.otherwise)
    if isinstance(r, Try):
        return guards(r.body) + guards(r.otherwise)
    if isinstance(r, (Let, Expect)):
        return guards(r.body)
    if isinstance(r, Call):
        return ()                                  # the callee's guards are checked at its own site
    raise TypeError(f"not a routine: {r!r}")


def actions(r: Any, lib: dict | None = None, _seen: frozenset = frozenset()) -> tuple:
    """Every primitive action the routine can emit. Used to check a routine against what the
    environment currently advertises -- a routine that survives a level boundary may name an
    action the new level does not offer.

    **`lib` IS NOT OPTIONAL IN EFFECT, ONLY IN SIGNATURE, AND THE REASON IS A SILENT PASS I
    BUILT AND CAUGHT IN THE SAME HOUR.** `Call` was returning `()`, so a routine made entirely
    of calls advertised NO actions and the level-boundary check above passed it unconditionally
    -- the check going quiet rather than failing, which is the one thing `conform/lint.py`'s
    docstring is a list of. Pass the library and calls are resolved; omit it and an unresolved
    call is reported as `?<name>`, which cannot be mistaken for an environment action.
    """
    if isinstance(r, Act):
        return (r.action,)
    if isinstance(r, Seq):
        return actions(r.first, lib, _seen) + actions(r.then, lib, _seen)
    if isinstance(r, (When, Until, Let, Expect)):
        return actions(r.body, lib, _seen)
    if isinstance(r, Choose):
        # BOTH ARMS. Which one runs is not known until the guard is read, so a routine whose
        # else-arm names an unadvertised action must fail this check before it is ever chosen.
        return actions(r.body, lib, _seen) + actions(r.otherwise, lib, _seen)
    if isinstance(r, Try):
        return actions(r.body, lib, _seen) + actions(r.otherwise, lib, _seen)
    if isinstance(r, Call):
        if lib is None or r.name not in lib:
            return (f"?{r.name}",)                 # LOUD, never empty
        if r.name in _seen:
            return ()                              # recursion: its actions are already counted
        return actions(lib[r.name], lib, _seen | {r.name})
    raise TypeError(f"not a routine: {r!r}")


def render(r: Any) -> str:
    """One line, readable in a ledger row. The legibility rule applies to the ACT space too."""
    if isinstance(r, Act):
        return r.action
    if isinstance(r, Seq):
        return f"{render(r.first)} ; {render(r.then)}"
    if isinstance(r, When):
        return f"when({r.guard}) {{{render(r.body)}}}"
    if isinstance(r, Choose):
        return f"choose({r.guard}) {{{render(r.body)}}} else {{{render(r.otherwise)}}}"
    if isinstance(r, Try):
        return f"try {{{render(r.body)}}} else {{{render(r.otherwise)}}}"
    if isinstance(r, Until):
        return f"until({r.guard}/{r.budget}) {{{render(r.body)}}}"
    if isinstance(r, Call):
        return f"{r.name}()"
    if isinstance(r, Let):
        return f"let {r.var}={r.value} in {{{render(r.body)}}}"
    if isinstance(r, Expect):
        return f"expect({r.slot}) {{{render(r.body)}}}"
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
    # THE BRANCH, AND IT IS APPENDED AFTER rather than interleaved. `cap` takes the shortest
    # `cap` shapes and `sort` is stable, so insertion order decides ties -- putting `Choose`
    # last means nothing that was reachable before this line stops being reachable. The
    # ordering is therefore REVERSIBLE and not a judgement about which shape is better.
    #
    # **BOTH ARMS DIFFERENT, AND IT IS `_branches`' `idn` FILTER AGAIN.** `Choose(g, b, b)`
    # does `b` whichever way the guard reads -- a distinct NAME for an identical computation,
    # which is the one thing that grows a closure without reaching anything.
    #
    # **SO THE BRANCH IS UNREACHABLE UNTIL THE SHELF HOLDS SOMETHING, AND THAT IS CORRECT
    # RATHER THAN A GAP.** `tether` hands this ONE action, so `base` is that action plus the
    # settled routines, and with an empty shelf there are no two different arms to choose
    # between. **An agent with one thing it can do has no choice to make**, and §14.4's
    # chunking rule is what supplies the second: a settled routine becomes a callable step.
    for b in base:
        for c in base:
            if render(b) == render(c):
                continue
            for g in guards:
                out.append(Choose(g, b, c))
    # THE FALLBACK, AND IT NEEDS NO GUARD -- it branches on an OUTCOME, which is the whole
    # difference from `Choose`. Appended last for the same reason `Choose` was: nothing
    # reachable before this line stops being reachable.
    for b in base:
        for c in base:
            if render(b) != render(c):
                out.append(Try(b, c))
    seen, uniq = set(), []
    for r in out:
        k = render(r)
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    # **ROUND-ROBIN WITHIN A LENGTH, BECAUSE THE CAP WAS DECIDING WHICH SHAPES EXIST.** `sort`
    # is stable, so ties broke on INSERTION ORDER -- and that is the defect `tether` already
    # names at its own bargain: *the dict remembering who arrived, not the bargain preferring
    # anyone.* Here it decided something larger than a winner: with one kind exhausted before
    # the next begins, a `cap` reached mid-kind means the later kinds are NEVER ENUMERATED.
    #
    # **IT WAS LATENT UNTIL TONIGHT AND THEN I MADE IT LIVE.** Compound and comparison guards
    # take the guard count from `n` to `4n - 2`, and `When`/`Until` are `base x guards x 2` at
    # length 2 -- so past a handful of objectives the length-2 band alone exceeds `cap` and
    # `Seq`, `Choose` and `Try` vanish entirely. **It activates exactly when the agent starts
    # having objectives, which is exactly when the ACT space starts to matter.**
    #
    # SHORTEST STILL FIRST -- the bargain prices length and that ordering is the whole reason
    # for it. What changes is only the tie: one of each kind, then two of each, so a cap that
    # cuts mid-band cuts EVERY kind evenly instead of erasing the last ones. **No new constant,
    # and `cap` stays exactly what it was: a compute bound, ours.**
    rank: dict[str, int] = {}
    keyed = []
    for r in uniq:
        kind = type(r).__name__
        rank[kind] = rank.get(kind, -1) + 1
        keyed.append((length(r), rank[kind], kind, r))
    keyed.sort(key=lambda t: t[:3])
    return [r for *_, r in keyed[:cap]]


def reach(r: Any, lib: dict | None = None, _seen: frozenset = frozenset()) -> int:
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
        return reach(r.first, lib, _seen) + reach(r.then, lib, _seen)
    if isinstance(r, When):
        return reach(r.body, lib, _seen)
    if isinstance(r, Choose):
        # **`min`, AND IT IS THIS DOCSTRING RATHER THAN A PREFERENCE.** Exactly one arm runs and
        # which one is unknown until the guard is read at execution, so the reach the routine can
        # be HELD to is the smaller. `max` would let a branch be priced on its better arm and
        # then take the other -- over-stating reach is the precise defect this function was
        # written for, and a branch is the first shape that can do it while looking honest.
        return min(reach(r.body, lib, _seen), reach(r.otherwise, lib, _seen))
    if isinstance(r, Try):
        # `min`, FOR `Choose`'s REASON. Exactly one arm's work lands, and which is unknown
        # until the body has already failed -- so the reach it can be HELD to is the smaller.
        return min(reach(r.body, lib, _seen), reach(r.otherwise, lib, _seen))
    if isinstance(r, Until):
        return max(r.budget, 0) * reach(r.body, lib, _seen)
    if isinstance(r, (Let, Expect)):
        return reach(r.body, lib, _seen)
    if isinstance(r, Call):
        # **ZERO WHEN UNRESOLVED, AND THAT IS THE SAFE DIRECTION HERE RATHER THAN THE LOUD ONE.**
        # `actions` reports `?name` because a missing action must not pass an environment check.
        # This feeds `left = unsat - reach`, so OVER-stating reach is what lets a candidate claim
        # to close a residual it cannot -- the exact defect this function was written for. An
        # unresolved call therefore reaches NOTHING and the candidate is priced as closing
        # nothing, which refuses it rather than admitting it on a guess.
        if lib is None or r.name not in lib or r.name in _seen:
            return 0
        return reach(lib[r.name], lib, _seen | {r.name})
    raise TypeError(f"not a routine: {r!r}")
