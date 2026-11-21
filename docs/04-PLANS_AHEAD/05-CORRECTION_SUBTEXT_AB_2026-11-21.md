
## A/B result — correction-as-subtext on a real unseen game (2026-11-21)

Real game `cd82`, fresh processes, 120 cycles, `TETHER_AGENT_SEED=0`, every switch ON except
the A/B arm. ~42 min wall each.

| measure | ON | OFF |
|---|---|---|
| `correction_subtext` rows | **1** | 0 |
| `arrived_no_clear` | 1 | 1 |
| repair rows | 5 | 5 |
| `subgoal_adopted` | 2 | 2 |
| settles | 102 | 102 |
| minted | 17 | 17 |
| ledger rows | 83,568 | 83,566 |
| level verdict | unreached | unreached |

### Honest reading
1. **The mechanism fires**: the ON arm wrote one `correction_subtext` row, the OFF arm wrote none.
   The correction is now legible in the record — the article's "describe it before you go
   looking" is satisfied at the write site.
2. **It did not change a decision on this game**: all structural counts are identical. The
   reason is visible in `_ss_reads` (tether.py:25490-25499): a steer publishes a reading only
   when `1 + paid < against`, i.e. at least TWO stops at the same (goal-kind, slot-kind).
   One `arrived_no_clear` is one witness, deliberately not a basis (Fig 10). I did NOT lower
   that bar — doing so would make one correction decide, which is exactly the "one witness is
   a rule" failure the steer's own docstring refuse.
3. **More contact advanced the chain**: with 120 cycles the run reached `subgoal_adopted=2`
   and 5 repairs, whereas the earlier T0 runs (600 s, fewer actions) had subgoal 0/6. The
   chain moved one more link with more actions — Fig 11 contact, not a score. Still no clear.

### Verdict
Built-and-reached, with no decision change from a single correction. The hook is sound and
reversible; it will price a kind up when the SAME kind is refused twice, which this game did
not produce. Record, do not tune. This is the same honest "no occasion" class as the other
audits — but here the row proves the mechanism ran.

No ARC-game tuning, no answer encoded, no check weakened.
