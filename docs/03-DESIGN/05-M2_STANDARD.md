# THE `M2` STANDARD — set by Isaiah 2026-09-05, before the build

**This file is the acceptance criteria. It is read at the start of every work session on `M2`,
BEFORE the code, because it is the definition the report must be written against and
`A6i`'s writing side says the summary otherwise gets written from the work just done.**

## THE ONE-LINE STANDARD

> **`M2` is done when the agent forms and pursues a BOUNDED MULTI-STEP BEHAVIOUR whose route
> comes from its OWN LEARNED TERMS, priced against the DENSE GOAL RESIDUAL, terminating
> safely — and NOT when it takes a good single step, runs a fixed script, or reads its route
> from anywhere the environment named.**

## THE RULING TAKEN BEFORE THE BUILD

**ROUTINES SURVIVE LEVEL BOUNDARIES — Isaiah, 2026-09-05.** Asked because a routine is neither
a binding nor a residual: `retarget` clears bindings because the SLOTS do not survive, and
`outstanding` is monotone because the RESIDUAL does. **A routine is a BEHAVIOUR, and it
carries across.** So `boundary()` must not clear routines, and a routine referring to slots
that did not survive must fail its guard rather than crash.

## THE SEVEN, EACH TIED TO HOW IT ALREADY WENT WRONG

1. **`CAN` BEFORE `Until`.** `Until(P, R)` with unsatisfiable `P` never terminates. `CAN(PRED)`
   is declared in `grammar.py` with NO PRODUCER, and `Until` needs it. **Termination is
   VERIFIED, never assumed.** *Check: does every `Until` have a `CAN(P)` confirming `P` is
   reachable before the loop commits?*
2. **MINT ON THE GOAL RESIDUAL, NOT THE REWARD.** `_route_reward` bins on `degree` — the sparse
   channel, absent most of a run. **That is the exact criterion error the selector had.** §14.4:
   a routine mints when *a goal residual no routine closes*. Dense channel for mechanism, sparse
   only to select among goals. *Check: read what the trigger bins on.*
3. **THE ROUTE IS LEARNED — Guard A, and it now COMPOUNDS.** A routine selects actions because
   the agent's own `_predict` over its own bound terms says so. **The tempting sentence when the
   algebra is half-built — *the routine just needs to pick the action that advances the goal* —
   is the fault if *advances* comes from anything but learned prediction.** Single-step
   contamination is one wrong move; **a routine built on it is a wrong PLAN.** *Check: trace the
   route to `_predict` at EVERY constructor, not just the first.*
4. **ONE BARGAIN, NO NEW CURRENCY.** §14.4: one `pays(cost, left, base)` across all three
   spaces — routine length as cost, goal residual as left. **No routine-specific cost, no magic
   number, no CE apparatus** — that thread collapsed four times. *Check: is any routine priced
   by anything but `pays`?*
5. **A FIXED SCRIPT IS NOT A ROUTINE.** §14.3 is blunt: *you cannot build it by chaining
   functions.* The temptation is a long pipeline called done. **`Until` must genuinely
   repeat-until-terminate, so *navigate* is ONE bounded chunk, not an N-step script.** *Check:
   is `Until` a real repeat-until, or a fixed-count loop wearing the name?*
6. **CHUNKING IS REUSED, NOT REINVENTED.** A settled routine becomes a callable step in a bigger
   routine — the same rule already running for terms. *Check whether term-chunking generalises
   before writing new chunking* — three of five times the mechanism was present and the
   capability was not.
7. **`M2 DONE` IS THE HEADLINE `A6i` MUST CATCH.** It was claimed twice this session on
   link-3-closed. **Report against the DEFINITION — forms and pursues a bounded multi-step
   behaviour — not against the work — a routine ran once.**

## THE VERIFICATION SPLIT, WHICH MAY NOT BE COLLAPSED

    MECHANISM   checkable on fixtures, REQUIRED before "built": each constructor does what it
                says -- `Seq` sequences, `When` guards, `Until` repeats AND terminates, `Act`
                wraps; `CAN` produces; the trigger bins on residual; chunking nests; `pays`
                prices routines
    CAPABILITY  OWED TO A REAL BOARD and not blockable-in: does the agent compose a routine
                that SOLVES. **The routine cannot be planted -- planting it is building toward
                the answer**

**Report mechanism-built when the synthetic checks pass, and capability-owed explicitly. Never
collapse the two.**

## TWO FIREWALL STANDARDS SPECIFIC TO `M2`

**A — THE ROUTE IS LEARNED, THE GOAL IS GROUNDED, NOTHING ELSE SUPPLIES EITHER.** `M2` makes
this worse because routines PERSIST: **a contaminated route becomes a durable plan.** The most
dangerous shortcut in the build is a routine that "knows" the action sequence from the env —
**it looks like planning and is lookup, across a sequence, passing the public board and failing
transfer.**

**B — NO REAL BOARD UNTIL FROZEN, NO FREEZE UNTIL `M2` IS GENUINELY THE ACT SPACE, AND THE
FREEZE IS ISAIAH'S.** The seat reports `M2` built against the definition; it does not freeze.

## THE STANDING CHECKS `M2` IS MOST LIKELY TO TRIP

- **Check 3, absence-as-fact** — a guard reading *I have no evidence* as *the guard is false*,
  which is `disembodied`-by-absence. **`CAN` and the guards ABSTAIN on no-evidence.**
- **Check 7 / `A6i`** — *M2 done* from *a routine ran*.
- **Law 6, go to the source** — every criterion, cost and trigger: check what channel it bins
  on at the source that defines it. **`_route_reward`-on-`degree` is this check waiting to fire.**
- **Guard B, the `_value_of` bypass** — `M2` puts `OBJ` terms in more places; **wherever a
  routine hits a direct `t.apply`, it is the pricing bypass again.**

## THE SINGLE MOST IMPORTANT THING

> **`M2` IS THE FIRST BUILD WHERE THE CONTAMINATION IS DURABLE.** Every prior one was a single
> wrong step, bet or claim — caught and fixed in one place. **A routine is a PERSISTED
> SEQUENCE, so a contaminated route, an unsafe `Until`, or a reward-keyed trigger does not fail
> once — it fails as a committed plan, repeatedly, and it LOOKS LIKE THE AGENT PLANNING while
> it is looping on a bad guard or executing a lookup.**

**At every constructor: the route is learned and the termination is guaranteed — because `M2`
is where a wrong answer stops being a move and becomes a behaviour.**
