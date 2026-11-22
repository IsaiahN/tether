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