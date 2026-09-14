# Pre-registration: the dereference operator (relation → value)

**Written BEFORE wiring, on the reviewer's insisted-on condition (Doc 22:32, 2026-09-14).** The fix
expands the closure, and the closure IS the cost curve. Routing `relation → value` multiplies the
reachable set by ~(relations in scope × objects in scope), so it can make the search materially
worse at the same time as it opens real ground — and BOTH effects land in the reach-failure number.
A flat reach-failure could mean the fix did nothing OR that it opened ground while the denominator
grew underneath it. Those are opposite readings of one number, so the denominator is registered here
first.

## The fix (one line, so the pre-registration is honest about what is measured)

A dereference operator: apply an extractor to the object at the far end of a relation, returning its
VALUE (not a truth about it). Shaping-safe because it names no relation, no object, no value — it
says the path exists and contains no answer. Stamped `ADMITTED` at entry.

## BASELINE, measured before the build (40 cycles, system0, per board — never pooled)

| board | bets/cyc | routes/cyc (closure size proxy) | reach succeed/total | reach-rate |
|-------|---------:|--------------------------------:|--------------------:|-----------:|
| vc33  |     97.2 |                            96.2 | 3 / 211             |      1.4%  |
| sp80  |     56.5 |                            55.7 | 9 / 304             |      3.0%  |
| ls20  |    174.3 |                           173.3 | 8 / 794             |      1.0%  |

Reach-failures that are arity-2 value-target: 100% on all three. Conservative unproducible cut
(SHAPE/POSITION/DELTA/COLOUR — no existing atom makes these from a relation): 62% / 82% / 77%.

## What counts as the fix WORKING (registered before the numbers)

Three quantities, read per board, never pooled:

1. **reach-failure falls** — necessary, not sufficient (it can fall because fewer bets are made).
2. **reach HOLDS or rises** — the standing guard. A fix that raises expressiveness and drowns the
   search would drop successful reaches while reach-failure also drops; that reads as progress and
   is not. Reach (succeeding retrievals) must not fall.
3. **bets/cyc and routes/cyc are read alongside** — so an expansion of the denominator is VISIBLE
   rather than inferred. If reach-failure is flat while routes/cyc jumps, the fix opened ground the
   growing denominator hid; if reach-failure falls while routes/cyc is controlled, the wall moved.

**And the discipline half already registered:** the number falls only if arity-2 VALUE terms SETTLE
and get REACHED. A library-count change is NOT the wall moving. `by=composed`/dereference terms must
appear in settle+reach events, not merely in the library.

## What would REFUTE the fix

- reach-failure flat AND routes/cyc up → denominator grew, no real ground opened (or opened-and-hidden; disambiguate by whether arity-2 value terms settle+reach).
- reach DROPS while reach-failure drops → the search drowned; expressiveness up, capability down. Reject.
- arity-2 value terms mint but never settle/reach → the operator types but pays nothing; not the wall.
