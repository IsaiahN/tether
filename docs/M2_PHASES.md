# `M2` — THE PHASE PLAN, ORDERED FROM EACH ITEM'S SPEC

**Written before the build, per the step: *read the SPEC of each item before ordering a phase, not
the row that summarises it.* That step is four-for-four, and it moved two items here.** Acceptance
criteria are `M2_STANDARD.md`; this is only the order and the checklist.

## WHAT THE SPEC READS CHANGED, BEFORE ANY CODE

**THE ALGEBRA SPLITS ON `CAN`, AND THE ROW DOES NOT SHOW IT.** `Act`, `Seq` and `When` need nothing
from `CAN`; **only `Until` does.** So *build the algebra* and *build `CAN` first* are not in tension —
`CAN` is a prerequisite of ONE constructor, and building the algebra without it would leave exactly
the unsafe one unbuilt.

**THE `PLAN` STEP IS LATE, NOT EARLY.** It reads as a trivial two-line item — add a string to two
copies of `STEPS`. **But `gate.py` ENFORCES step order**, so the edit cannot be made until it is known
WHERE planning happens in the cycle, and that is decided by the execution state in P3. **A row sorted
by cost puts it first; the spec puts it after P3.**

**AND ONE `A6i` FOUND IN `CAN`'s TWO SOURCES, BEFORE WRITING IT.** `grammar.py` glosses `CAN` as *"a
relation is **achievable**"*; `ARC_AGENT` §14.3 calls it *"the affordance that says the guard is
**satisfiable**"*. **Those are two quantities.** *Satisfiable* is logical — some value in the alphabet
makes `P` true, which `objective_gap` already computes as `hits`. *Achievable* is evidential — the
agent has grounds to believe it can GET there. **`Until` needs the second**: a guard that is
satisfiable but unreachable is exactly the non-terminating loop standard 1 names. Settled as
**achievable**, with satisfiability as one of its inputs.

## THE PHASES

    P1  CAN(PRED) producer                     depends on: nothing        [x]
    P2  the Routine algebra, all four          depends on: P1 (Until)     [x]
    P3  cross-step execution state             depends on: P2             [x]
    P4  PLAN step in ledger.STEPS + gate.py    depends on: P3             [x]
    P5  mint trigger on the goal residual      depends on: P2, P3         [x]
    P6  routine pricing via `pays`             depends on: P2, P5         [x]
    P7  ACT chunking                           depends on: P5, P6         [ ]

### P1 · `CAN(PRED)` — the producer that does not exist
Declared `CAN : (PRED,) -> PRED` in `grammar.py`, **composed nowhere.** Owes: a producer returning
**achievable / not-achievable / unknown**, three outcomes not two. **Check 3 governs the third**:
*I have no evidence* may not be recorded as *the guard is false* — the same error as
`disembodied`-by-absence. Evidence is the agent's own: `Affordances` (§16.4's seven, learned by
interaction, and it **already keeps unread apart from absent**) and the trace. `objective_gap`'s
satisfiability is a necessary input, never sufficient.

### P2 · the Routine algebra — a new object kind
`Act(a) | Seq(R1,R2) | When(P,R) | Until(P,R)`. §14.3: **you cannot build it by chaining functions.**
Owes all four. **`Until` must genuinely repeat-until-terminate** — a fixed-count loop wearing the name
is the thing `Until` exists to replace, and *navigate* must be ONE bounded chunk.

### CORRECTION — `P3`, `P5` AND `P6` ARE ONE MECHANISM, NOT THREE PHASES
**Found by `conform/lint.py`'s ISOLATED seat, which failed `P2` for `advance` having no caller.**
§14.4 mints a routine *when a goal residual no routine closes* — **so minting, pricing and
executing are the same loop and none of them works alone**: a routine never adopted cannot be
executed, an adoption with no executor does nothing, and an unpriced mint is not the one bargain.
*The step-3 law says the dependency order falls out of the spec rather than the table, and here
it says these three are one item.* Built and committed together.

### P3 · cross-step execution — the invasive one
**No cross-step action state exists**: `step()` opens by clearing every cache. Owes an execution
pointer that survives that, and — **per Isaiah's ruling 2026-09-05 — survives level boundaries**,
because a routine is a BEHAVIOUR, not a binding or a residual. A routine naming slots that did not
survive **fails its guard rather than crashing.**

### P4 · the `PLAN` step — two copies, order enforced
`STEPS` is duplicated in `ledger.py:18` and `gate.py:36`, and `gate.py` checks order via
`STEPS.index(step)`. Owes: the position, which P3 decides.

### P5 · the mint trigger — residual, never reward
§14.4: a routine is minted when **a goal residual no routine closes**. `_route_reward` bins on
`degree` — the SPARSE channel, absent most of a run, **which is the exact criterion error the selector
had.** Owes a ROUTE bin over `_discrepancy`.

### P6 · pricing — one bargain, no new currency
§14.4: **one `pays(cost, left, base)` across all three spaces.** Owes a routine length cost, derived
the way `term_bits` was, **never picked.** The CE thread collapsed four times on inventing a currency.

### P7 · ACT chunking — reuse, do not reinvent
`gamma.units()` is the precedent and its rule is the whole of it: *the atoms, plus every SETTLED term
as one unit — **only what the ground has paid for becomes a shortcut.*** Owes the same rule for
routines. **Check whether it generalises before writing new chunking** — three of five times the
mechanism was present and the capability was not.

## THE REPORT THIS PLAN IS WRITTEN AGAINST

**Each phase reports MECHANISM-BUILT when its synthetic checks pass. `M2` reports built only against
`M2_STANDARD.md`'s one-line definition — *forms and pursues a bounded multi-step behaviour whose route
comes from its own learned terms, priced against the dense goal residual, terminating safely* — and
never against the work just done.** Capability stays owed to a real board throughout.
