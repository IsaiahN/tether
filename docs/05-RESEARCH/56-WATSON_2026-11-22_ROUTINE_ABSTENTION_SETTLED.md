WATSON 56 -- the routine "does-not-pay" gap is CORRECT ABSTENTION, settled (2026-11-22)

RESIDUAL (effect terms): WATSON 54 held a possible routine-price defect (fractional `unsat`
for `base` vs integer gap for `reach`). The six 1800-cycle proving ledgers can settle it
without a new run.

MEASUREMENT (per game, never pooled; detail.reach from every `routine_cut` row):

| game | routine_cut (all does-not-pay) | adopted (`routine` verdict=pays) | cut reach max |
|---|---|---|---|
| ar25 | 5  | 0 | 1 |
| cd82 | 13 | 6 | 1 |
| g50t | 2  | 0 | 1 |
| ka59 | 5  | 0 | 1 |
| lf52 | 14 | 0 | 1 |
| lp85 | 8  | 0 | 1 |

(The earlier audit measured reach up to 31 on cd82's bought plans; every REFUSED candidate on
every board has reach 1.)

DERIVATION (figures decide):
- Fig 5 :16 "mint if the description length pays." A plan with reach 1 saves naming one
  action; `term_bits(L,n) >= (L+1)log2(n+1) > log2(n)` for any L>=1, so it CANNOT pay. The
  bargain refusing every reach-1 plan is the figure working, not a defect.
- Fig 12 :126 "Bits price the description. Actions price finding out whether it holds." The
  two currencies are held apart; a plan that compresses one action is dearer than the action.
- Fig 9 :60 "filters for the budget and witnesses for the verdict. Never let a filter hand you
  a verdict." The cut is a budget filter; it never says the goal is false.
- Fig 11 :39-40 capability is agent-and-habitat. cd82 (large integer gap) buys 6 plans —
  the SAME kernel, a different habitat. That is contact deciding, exactly as the figure says.

VERDICT: the held "currency mismatch" is NOT a live defect. Plans are bought where a
multi-step gap exists (cd82) and refused where reach is 1 (every other board) — correct
abstention. No kernel price change is warranted; none was made. WATSON 54's price-side
"Fix 2" stays retracted (editing the rule for naming what worked would be a species change,
Fig 4 :19-20). This closes the routine half of the capability question as: built, reached,
behaving as the figure requires.

CORRECTION to WATSON 54/55: those records called the price issue "held pending a ground run."
This is that ground run, read from ledgers already produced; the result is "no defect,"
so the held item is now CLOSED, not pending. Kept as a record, not silently rewritten.

OUTSTANDING (unchanged): the nested-method CAPABILITY (Fix 1's payoff — can the composer
build a term that USES a settled method as a nested operand and pay) is still not shown;
representation confirmed, closure composes by atoms (gamma.py:2545). That is the one open
capability item, and it stays HELD (no kernel edit).

FIGURE CENSUS: Fig 1 mint-if-pays · Fig 4 kernel invariant · Fig 5 when a composition pays ·
Fig 9 filters-not-verdicts · Fig 11 contact/capability=agent-and-habitat · Fig 12 two currencies.
Strained: none.
