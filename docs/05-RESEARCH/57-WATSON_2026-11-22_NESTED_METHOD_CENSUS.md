WATSON 57 -- nested-method census: no settled method is composed over (2026-11-22)

RESIDUAL (effect terms): Fix 1 made a settled method representable as a unit (WATSON 55).
Does that method ever get composed over in practice? Fig 12 :103 "a settled molecule becomes
an atom for whatever composes over it."

MEASUREMENT (read-only census of the six 1800-cycle proving ledgers, per game never pooled;
all from BEFORE Fix 1, so this is the baseline population, not the fix's effect):

| game | method terms (computed operand `<...(...)>`) | terms composing a method | terms with >=2 `<` |
|---|---|---|---|
| ar25 | 15 | 0 | 0 |
| cd82 | 0  | 0 | 0 |
| g50t | 0  | 0 | 0 |
| ka59 | 62 | 0 | 1 (a provenance stamp `?INVENTED<...>`, not a method) |
| lf52 | 58 | 0 | 0 |
| lp85 | 1  | 0 | 0 |

Detector validated: a bound operand is `<o0.col>`; a method is `<translate(o5.add_n)>`. The
single double-`<` case is `?INVENTED<AGENT-INVENTED|...>` — a stamp, not a composed method.

DERIVATION:
- Fig 12 :103 is a REQUIREMENT the code should meet, not a report that it does. The census
  says it is not met on these boards: methods settle but are never operands of later terms.
- Fig 5 :69 "settling is necessary for a term to be composed over, and it is not sufficient."
  These terms are settled; their being uncomposed is exactly the insufficiency the figure
  names. So this is not evidence of a representation defect — it is the state Fig 5 predicts
  when the *composition* (not the settlement) is missing.
- gamma.py:2545 `_iter_step` folds over `unit.atoms`, so the closure composes chains by atom
  names; a method's structure is carried in its `name`, not in the atoms the walk extends.
  Fix 1 makes the name distinct (representation) but does not change the walk (composition).

VERDICT: the nested-method capability is NOT demonstrated on the baseline population, and the
reason is structural (the walk extends atoms), not a price verdict and not a stale record.
Fix 1 is still the correct conformance repair — it stops a settled method from being *lost* —
but the next capability step would have to change how the composer extends a unit (Fig 12's
"arrangement"), which is kernel work and is HELD per the Fig 4 ruling. No kernel edit made.

WHAT WOULD CHANGE THIS: a per-seed A/B run of Fix 1 with the expensive cycles budgeted as a
detached job, showing a schema-named unit becoming an operand of a later PAYING term. The
earlier perf probe (~35 s/cycle) was inconclusive and had a detector bug; neither it nor this
census is a capability claim. Both are recorded so the open item is not forgotten.

FIGURE CENSUS: Fig 1 mint-if-pays · Fig 4 kernel invariant · Fig 5 settled-not-sufficient ·
Fig 9 describe-effect-before-looking · Fig 11 contact · Fig 12 settled-molecule-becomes-atom /
arrangement-is-the-substance · Fig 13 closed-set-open-arrangements. Strained: none.
