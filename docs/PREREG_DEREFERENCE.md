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

## OUTCOME 2026-09-14: the typed stream was built and REFUTED at a THIRD layer — the novelty gate

Built the typed predictor stream `(stype, stype)` + the partner atoms + the group-coherence guard
(no group-reading atom in the typed stream). Result: partner is NOW enumerated as a value-predictor
(instrumented: 609 EXTENT + 135 SHAPE + 12 POSITION + 6 DELTA partner terms/6cyc in the typed
streams) — the wiring works — but STILL zero settle/reach events. Verified cause, layer by layer:

- **Bare `partner<operand>`** (len 1 — the primary "my attr = my partner's attr" predictor) is cut
  by `is_atom` as NOT-NOVEL. `is_atom = len(term)==1 and name in registry` — it IGNORES the operand
  binding, so `partner_extent<o1.w>` is treated as the un-novel bare atom. This hits same/other/above
  identically: a relation atom only ever settles when COMPOSED into an objective, never as a bare
  bound prediction.
- **Composed partner** (len 2-3) reaches `_cannot_pay` and is **100% bounded-out** (552 len-2, 8544
  len-3, all) — it does not fit enough of the residual.

So the typed relational vocabulary is walled off from PREDICTION by at least THREE independent
mechanisms: (1) no relation→value atom; (2) the untyped predictor stream; (3) the novelty gate cutting
the bare value-predictor, with composed forms failing to fit R. Reverted (inert-with-cost, pure
denominator growth). This is the reviewer's "circling one structural fact" hypothesis, seen from the
build side: RELATIONS → OBJECTIVES ONLY is enforced at multiple layers.

To make relation→value actually PREDICT would require changing `is_atom`'s novelty definition (a bound
operand-reading atom counts as novel) — CENTRAL, affecting every operand-reading atom's behaviour —
on the UNCONFIRMED premise that residuals are partner-equality-shaped, which the 100%-bounded-out
composed partners weakly argue against. Fork for alignment; not a unilateral change.

## THE FINDING (reviewer, 2026-09-15): RELATIONS → OBJECTIVES ONLY, enforced ~5 ways

Not one defect with one fix, and not unrelated failures: ~5 distinct MECHANISMS reading ONE STANCE
— prediction is val-only, relations exit through objectives, the objective outlet is starved. This
is why no single lever moves the ground (the three-layer build showed it prospectively: each fix
revealed the next). PROGRESS IS NOW "HOW MANY ENFORCERS REMAIN," NOT "WHICH LEVER." The ~5:
(1) no relation→value atom; (2) untyped predictor stream; (3) the novelty gate blind to binding
(is_atom ignores the operand — the sharpest); (4) OBJ-binding starved (F36); (5) objective gaps
degenerate 0/1 (arity-1 consumer) / unary operand socket (0a).

Premise (equality-shape) is CONFIRMED PER-GAME, not weak: ls20 27% real, vc33 0% does not dilute it
(averaging would be the pooling error). Real where the skill is present, absent where it isn't — the
genuine-capability-gap pattern.

## THE FORK RESOLVED (reviewer, 2026-09-15)

The deciding asymmetry: the EVIDENCE is per-game, the is_atom CHANGE is GLOBAL — it alters every
operand-reading atom on every board. On vc33 (premise 0%) it buys pure denominator (bound
same/other/above become novel, enumerate, fail to fit, cost cycles). So the question is whether a
global change pays where the premise holds by more than it costs where it does not — which needs
MORE BOARDS to BOUND THE HARM (not to strengthen ls20). Run over the public set the ablation needs
anyway = work taken earlier.

is_atom CHANGE ITSELF: PARKED FOR ISAIAH. It is a change in REACH (a term becoming mintable that
could not be before), which is his standing carve-out — what the agent is HANDED, not how it prices
what it holds. Everything before was the seat's; this one holds for him.

NEXT (seat, sanctioned): the equality-shape read across more boards (the public set), to bound the
harm. A read/measurement, not the central change.

## PRE-REG: ls20 payoff probe (reviewer 04:36) — success is the WALL MOVING, not settling

vc33 proved settles do NOT imply the wall moves (settle +10, reach-failure flat 208->208). So the
payoff must be measured directly, and the success condition is pre-registered BEFORE the numbers:

  SUCCESS  = reach-failure FALLS on ls20 while reach HOLDS (the standing guard) -- the only reading
             that distinguishes a capability from a bigger library.
  REFUTED  = partner fires and terms settle but reach-failure stays at baseline (ls20: reach 794,
             fail 786, ok 8) -- equality capability real and reachable but does NOT explain the
             residuals actually failing. A genuine, disappointing result; better found here.

NARROW version tested (answers the reviewer's packet question): the novelty relaxation is gated on
the atom's OUT_TYPE being a VALUE type (COLOUR/POSITION/EXTENT/DELTA/SHAPE), so bound partner_* become
novel but bound same/other/above (PRED out) do NOT. Cleanly separable at the site. This is the version
Isaiah should rule on IF it buys the payoff -- it gets the equality capability without unlocking the
predicate vocabulary that cost +22% and moved nothing on vc33.

Persistence condition: cold (no library/store), revert, md5-confirm library byte-identical.

## REPRODUCIBILITY: the exact probe diff (reviewer note 2026-09-15)

The is_atom cost/payoff probes (vc33 wide, ls20/sk48 narrow) were run build-measure-revert, so
the code is NOT in HEAD. The exact diff that ran is recorded here so a later reader finds code
behind the results. WIDE version: the gamma is_atom relaxation drops the `out_type in VALUE`
clause (bound same/other/above also become novel). NARROW version is exactly the diff below.

```diff
diff --git a/arc_atoms.py b/arc_atoms.py
index 506d8cc..b7d0fe5 100644
--- a/arc_atoms.py
+++ b/arc_atoms.py
@@ -468,6 +468,16 @@ def _relate() -> list[Atom]:
                  reads_ctx=("operands",))]
 
 
+
+def _dereference() -> list[Atom]:
+    """PROBE (2026-09-15, reverted): relation->value dereference operators."""
+    def deref(v: Any, c: Ctx) -> Any:
+        return c.operands[0] if c.operands else v
+    return [Atom(f"partner_{t.lower()}", deref, t, t, reads_operand=True,
+                 operand_type=SAME_AS_TARGET, reads_ctx=("operands",))
+            for t in (COLOUR, POSITION, EXTENT, DELTA, SHAPE)]
+
+
 def _count(v: Any, c: Ctx) -> Any:
     """How many peers share this value. **A cardinality, not a truth.**
 
@@ -645,5 +655,5 @@ def three_spaces(predict: list[Atom]) -> list[Atom]:
     3d -- and inventing one here would be this file choosing what the agent may bet on.
     """
     return (list(predict) + _extract() + _transform() + _shape_facts() + _shape_more()
-            + _contact() + _relate() + _over_group() + _group_more() + _connect()
-            + _quantify())
+            + _contact() + _relate() + _dereference() + _over_group() + _group_more()
+            + _connect() + _quantify())
diff --git a/gamma.py b/gamma.py
index 1338611..8dbc349 100644
--- a/gamma.py
+++ b/gamma.py
@@ -461,8 +461,11 @@ class Gamma:
         return len(self.atoms)
 
     def is_atom(self, term: Term) -> bool:
-        """NOVEL is relative to atoms, not to the world."""
-        return len(term) == 1 and term.atoms[0].name in self._by_name
+        """PROBE 2026-09-15 (reverted): NARROW relaxation, value-out bound operand atoms novel."""
+        a = term.atoms[0]
+        if len(term) == 1 and getattr(a, "reads_operand", False) and            getattr(term, "operand", None) is not None and            a.out_type in ("COLOUR", "POSITION", "EXTENT", "DELTA", "SHAPE"):
+            return False
+        return len(term) == 1 and a.name in self._by_name
 
     # -- persistence: Â§17.8's decision, made rather than defaulted -------------------------
 
diff --git a/tether.py b/tether.py
index 5366a44..153cb15 100644
--- a/tether.py
+++ b/tether.py
@@ -2565,6 +2565,7 @@ class Agent:
             stype = self.slot_types.get(slot)
             if stype:
                 streams.append((stype, OBJ_TYPE))
+                streams.append((stype, stype))  # PROBE 2026-09-15
             # THE THIRD STREAM IS WITHDRAWN, AND THE REASON IS A DEFECT IT INTRODUCED.
             # `OBJECT -> OBJ` was legitimate once `Ctx.obj` stopped the extract atoms
             # abstaining -- and it is NOT type-coherent, which the reachability check missed.
@@ -2586,12 +2587,16 @@ class Agent:
             by_kind: dict[str, tuple] = {}
 
             for in_t, out_t in streams:
-                kind = "predictor" if out_t == "val" else "objective"
+                kind = "objective" if out_t == OBJ_TYPE else "predictor"
+                typed_pred = out_t not in ("val", OBJ_TYPE)
                 by_fit = partial(retrieval.fits, gap=gap, in_type=in_t, out_type=out_t)
                 st: dict = {"seen": 0, "budget_spent": False, "depth_exhausted": True,
                             "units": self.gamma.alphabet, "estimate": 0}
                 for cand in self.gamma.enumerate_closure(in_t, out_t, self.cfg.max_depth,
                                                          self.cfg.budget, st, order=by_fit):
+                    if typed_pred and any("group" in (getattr(a, "reads_ctx", ()) or ())
+                                          for a in cand.atoms):
+                        continue
                     binds = operand_binds if cand.reads_operand else [None]
                     binds = [x for x in binds if self._operand_fits(cand, slot, x)]
                     for bind, g in ((b, g) for b in binds for g in self._guards(robs)):
```
