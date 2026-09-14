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

## UPDATE 2026-09-14 (post-refutation): the atom alone is inert; the fix is a TYPED PREDICTOR STREAM

The 5 partner atoms were built and REFUTED — inert on all three boards (zero partner events; vc33/sp80
byte-identical, ls20 perturbed +31% time / worse reach-failure for zero capability). Instrumented
cause: the mint emits 521 partner terms/8cyc but ALL into the objective (→OBJ) streams, NONE as a
value-predictor, because the predictor stream is hardcoded `("val","val")` and partner is typed. So
value-residual PREDICTION is untyped: only domain grid-transforms predict residuals; the entire typed
relational vocabulary lives in the objective stream. Atoms reverted. Reviewer elevated this — the
untyped predictor stream — as the headline over dereference (Doc 23:17).

### Pre-build TYPED-WALK test (the reviewer's gate, run offline, no wiring)

Enumerated the typed closure with a hypothetical `(stype, stype)` predictor stream, partner present:
relation→value chains reachable per type — COLOUR 3, POSITION 3, EXTENT **87**, DELTA 3, SHAPE **45**
(0 for every type WITHOUT partner). So the fix is BOTH the partner atoms AND the typed stream; neither
alone reaches. Named candidate chains (the success criterion): `partner_shape`, `rotate.partner_shape`,
`reflect.partner_shape`, `partner_extent`, `count.partner_extent`, `rank_in.partner_extent`,
`partner_colour`, `partner_position`, `partner_delta`. SUCCESS = THESE settle (a named prediction),
NOT merely reach-failure falling.

### ABORT CONDITION (registered before the numbers, per the reviewer)

The change adds one predictor stream of ~the objective stream's size, so the PHYSICAL prediction is
~2× enumeration per slot (measured proxy: the inert atoms cost +15% to +31% for ~500 candidates).

STOP even if relation→value chains settle when EITHER:
- **bets/cyc exceeds 2× the pre-registered baseline on any board** (vc33 >194, sp80 >113, ls20 >349).
  Beyond the physical ~2× prediction means the typed predictors are compounding into deeper chains
  (bloat), not just adding one stream — the parts-bin-strangulation curve.
- **zero named relation→value chains settle on any board** after wiring — then it is inert-that-costs,
  the refuted case wearing a stream's clothes; revert.
KEEP only if: named chains settle AND bets/cyc stays under 2× AND reach HOLDS while reach-failure falls.

### Provenance correction

"(or a typing)" was the SEAT's phrase (my boundary doc), NOT the reviewer's. The reviewer's GO covered
the boundary resolution (Figure 6), not an implementation scope; the scoping judgement is the seat's.
The typed predictor stream is a seat scoping decision inside the reviewer's boundary ruling.
