WATSON 55 -- Fix 1 occasions, and what is next (2026-11-21)

The next step after Fix 1 was its CONTACT check (WATSON 54 falsifiers): representation is
proved, contact is not. This record anchors the first falsifier with a measurement and states
what remains.

## Falsifier (i): do settled trees exist? -- REFUTED (occasions exist)
Read from the six 1800-cycle proving ledgers (before Fix 1), per game never pooled:

| game | schema-named terms | schema settle rows | computed-operand examples |
|---|---|---|---|
| ar25 | 97 | 44 | translate<o12.drow_o13> |
| cd82 | 60 | 52 | translate<o14.dcells>, ...?BECOME OTHER |
| g50t | 7 | 7 | none?BECOME OTHER, count?no intent |
| ka59 | 174 | 34 | above . none<translate(o5.add_n)>?ACTED_SELF |
| lf52 | 95 | 25 | recolour . subtract . recolour<subtract(o41.colour)> |
| lp85 | 12 | 3 | translate . recolour<recolour(o1.add_n)>?BECOME OTHER |

Several carry a COMPUTED operand (translate(o5.add_n), subtract(o41.colour)) -- trees with a
real inner branch, exactly the method gamma.py:2478 used to strip on promotion. So Fix 1 has
occasions; the wall, if any, is price (falsifier ii), not representation. These ledgers were
produced BEFORE Fix 1, so they establish the population, not the fix's effect.

## What is next, in order (each a check, not a new capability)
1. EFFECT A/B (running): fix1_contact_probe.py, ON vs OFF, gridworld default seeds 0/1/11,
   90 cycles, per seed. Reports: settled trees, promoted schema units, paid schema terms.
   Falsifier (ii): if a schema unit is promoted but every depth-2 candidate still fails pays,
   that is correct abstention, not a representation defect. Falsifier (iii): if OFF differs
   from the pre-fix trace in any decision/binding/bargain count, reject the fix.
2. If effect is real: ship Fix 1 to the release branches (arc/general/GA PR were never given
   it) and update CHANGELOG.
3. If effect is inert but occasions exist: the wall is the PRICE, not representation -- report
   "unreachable at this rule" (Fig 8) to Isaiah. Do NOT edit the kernel price (Fig 4 :19-20,
   WATSON 54 correction): that is a species change. Evolution supplies the habitat/ground,
   never a hand-authored discount.

## Standing constraints (unchanged)
Kernel invariant preserved; Fix 1 is conformance to Fig 12 :103, not an amendment (see
docs/03-DESIGN/CONFORMANCE_2026-11-21_GAMMA_PROMOTION.md). Full lineage: units are plain
ledger-visible Terms; arm declared; OFF byte-identical; no output routes around the loop.

FIGURE CENSUS: Fig 1 mint-if-pays · Fig 4 kernel/only-methods-cross · Fig 8 unreachable-at-
budget · Fig 11 contact · Fig 12 settled-molecule-becomes-atom · Fig 13 closed-set-open-
arrangements. Strained: none.

## CONTACT CHECK RESULT (2026-11-21, appended) -- representation confirmed, payoff NOT shown
Three checks, all honest:
1. OCCASIONS (from proving ledgers, corrected detector): method-bearing trees DO settle
   (ar25 15, ka59 62, lf52 58, lp85 1, cd82 0, g50t 0), e.g.
   \ecolour . subtract . recolour<subtract(o41.colour)>\. Falsifier (i) REFUTED -- the fix is
   not inert on those boards.
2. A/B perf probe (fix1_contact_probe.py): inconclusive by instrument cost. 26 cycles of the
   ON arm consumed the 900 s budget (~35 s/cycle, the 122-bets/action bottleneck again), and
   seeds 1/11 never ran. Its \paid_schema\ detector also counted a BOUND operand
   (\<o0.dcol_o3>\) as a schema, which is a binding, not a method -- a second instrument bug.
   No OFF arm was run. NOT a valid A/B; do not read a result from it.
3. DETERMINISTIC structural test (fix1_structural.py): a settled tree \<g(:ANY)>\ promotes
   to a schema-named unit that keeps operand_term=True (OFF gives bare \\), and the schema
   unit passes the closure's start set. But enumerate_closure composes chains by \unit.atoms\
   (gamma.py:2545), so no COMPOSED term carries the method in its name, and \must_contain\
   counts are identical ON/OFF (45/45). So Fix 1 makes the method REPRESENTABLE and DISTINCT
   in the unit set -- its actual contract (Fig 12 :103, Fig 5 'settled not sufficient') -- but
   it does NOT by itself produce a deeper composed term the closure will pay.

VERDICT: Fix 1 is a correct CONFORMANCE fix (representation), fully documented and tested.
Its capability payoff is NOT demonstrated and is NOT claimed. The deeper question -- can the
composer build a term that USES a settled method as a nested operand and pay for it -- is the
GAP 1 price problem, which stays HELD (never a kernel edit, per Fig 4). Next real step, if
pursued: a large-gap, properly-supervised per-seed A/B with the expensive cycles budgeted as a
detached job; do not treat this inconclusive probe as evidence either way.

ANCHOR: gamma.py:2545 (closure walks atoms); fix1_structural.py output; fix1_contact_probe.py
output; ledger method-bearing counts above. Full lineage preserved; no code changed here.


## CORRECTION (2026-11-22): composition DOES stack and pay — the "can't stack" premise was a detector bug

Before building operand-composition (task 2) I checked the real ledgers. The premise is FALSE:
- `proving_1800` ledgers (created 2026-11-21 03:55, BEFORE Fix 1 at 14:24) already show nested
  method terms settling: ar25 `subtract . recolour . translate<subtract(o1.age)>?TOUCH` settled at
  c38; ka59 62 distinct nested terms; lf52 58; lp85 1.
- The lift machinery is BUILT and REACHED: `_DERIVED_LIFT` default ON, a molecule offer at a
  derived slot is re-filed at its source as an operand branch (`_lift_branches` at tether.py:15603),
  and `_trees` consumes it (15815). Lift counts: cd82 1009, lf52 1373; tree rows on all six boards.
- `_ops` already evaluates nested operand terms recursively under `_TIERED_TERMS` (14351-14355).

So Fig 12's "a settled molecule becomes an atom for whatever composes over it" is already
implemented in the operand arm. My earlier census (WATSON 55/57) that reported "0 nested operand
terms, must_contain 45/45 ON/OFF" used a detector counting `name.count('<')>=2`; the real nested
form is a SINGLE `<` with a computed term inside (`translate<subtract(o1.age)>`), so the detector
was blind to it. A6i-class error: a wrong detector read as a finding about the mechanism.

WHAT THIS MEANS:
- Task 2 (operand-composition) is NOT an open capability. It is built, reached, and paid. There is
  nothing to build; adding a "settled units as branches" change would duplicate `_lift_branches`.
- Fix 1's real effect is narrower than claimed: it preserves the method on PROMOTION (units()), so
  a settled nested term re-enters the closure with its schema. Whether that changes any decision
  is still unmeasured (the deterministic test showed must_contain 45/45 with the old detector, which
  was the wrong test) — but the underlying composition was never broken.
- Task 1 (goal-direction: no OPEN condition to decompose on arrived_no_clear, subgoal 0/6) is
  UNAFFECTED by this correction and remains the genuine measured break.

DECISION: do NOT build operand-composition. Report the correction. Build task 1 (goal-direction)
if proceeding, since that is the one real break the audits located. No code changed.

Anchor: proving_1800 ar25/k a59/lf52 ledgers; tether.py:14351/15603/15815; Fix 1 commit a75e543d.
