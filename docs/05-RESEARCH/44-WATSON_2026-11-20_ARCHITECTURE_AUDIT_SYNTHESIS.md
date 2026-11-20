WATSON — architecture audit synthesis and what to build next (2026-11-20 night)

QUESTION (effect terms, unbundled): Isaiah asked three things. (1) Is the architecture solid —
every faculty working, no blockages — so the agent can eventually win through correct function
rather than encoded answers? (2) How does it compare to an LLM, given preload-without-pretraining?
(3) How can we measure, across epochs of game playing, whether it is getting better at forming
words and sentences in its grammar — and how are WordNet/VerbNet/ConceptNet meant to work in tandem?

DOMAIN CENSUS (before figure lines):
- R1 architecture: arity = one faculty × its occasion; symmetry = a faculty can be built yet
  starved; scale = one run / one generation.
- R2 epoch improvement: arity = (generation N, ground-settled grammar artifact); symmetry =
  a count can rise while capability does not (frame-internal); scale = a game series.
- R3 knowledge sources: arity = (concept → verb → class), currency = candidate actions,
  anchor = the board; union of WordNet+ConceptNet+VerbNet priors is one compound, each NO
  STANDING until the ground settles.
- domains (actors / currency / anchor):
  - agent kernel: loop/gate/mint / description bits + actions / the figures
  - habitat: boards/objects / residual + ground verdict / the platform (Fig 11)
  - lineage: generations / methods, never recordings / the chain (Fig 4)
  - knowledge layer: three corpora / candidate priors / the board (42:117)
- order (Fig 3): kernel → perception → goal → search → grammar → knowledge enrichment.

TETHER (primary, verbatim from docs/01-FOUNDATIONS/03-FIGURES_TEXT.md):
- Fig 11 :39-40 "capability is a property of agent-and-habitat ... An improvement that does
  not change contact changes nothing." → the faculty audit's three top blockages are all
  missing CONTACT (no adoptable goal, no settled term), not broken mechanisms.
- Fig 9 :27-28 "describe it before you go looking, or any frame you pick will seem to fit"
  and :30-31 "describe the effect rather than the cause" → the epoch instrument must describe
  the effect (did the ground settle more of the grammar), not a frame-internal count.
- Fig 10 "A verifier that can reconstruct the claim cannot verify it" → the epoch measure
  must be ground-only and never read by the agent's decisions.
- Fig 4 :22 "Only methods cross up. Only head starts come down." → "getting better at grammar"
  = more methods that crossed and paid, not more recordings/replays.
- Fig 12 :46 "A bond is the typed relation between two operands ... not recoverable from the
  operands" → VerbNet classes are bonds between verbs, recorded not inferred; :41 "the bond
  is charged for what it could have been" → class expansion is priced.
- THE FORMULA (figures/THE_FORMULA.md:75-81) "a system measuring progress by terms minted is
  counting the denominator" → terms minted is explicitly REFUSED as a progress measure.
- Fig 6 :49-50 "more search at the same reach: is it in here and unfound? ... Fails by spending
  budget on a region already swept." → speed mechanisms matter only if they change reach.

WORLD (secondary, corroboration only):
- Epoch/learning-curve measurement is standard practice; but the figure rule decides WHAT is
  admissible evidence (ground-settled, not frame-internal). Pezzulo/Cisek affordance landscape
  (used in the goal-direction WATSON) corroborates that grounding grows from contact.

AUDIT FINDINGS (anchors, file:line):
- Faculty audit (25-step live gridworld, seed 0, 5,153 rows): 16 faculties inventoried.
  WORKING: perceive/bet/residual/route/mint-bargain/narrate/books/budget/relations.
  STARVED with named preconditions: recognition (no picture field), promote/import (no sweep
  close), HTN/lookahead/plan (no settled bound term: 1 of 196 slots bound), goal formation
  (12/12 goal_hypotheses pick=None, 150 candidates refused by type/route mismatch), repair
  (no OPEN enabler — `_htn_push` 16799-16804), affordance (no shape_name), word carry (no
  settled productions). Top 3 blockages: (1) no adoptable goal here / insufficient goal on T0,
  (2) `arrived_no_clear` is terminal not a residual, (3) no settled bound term starves planners.
- Speed audit (7 notes): nearly all "not built" notes are stale. Built-and-reached default-ON:
  caching/hoisting `_W_CACHES`, `_MINT_HOIST` (measured 14.9M calls fixed per mint), TOP-K as
  `TETHER_SERP` K=32 with must-fails, reflex tier with `_urgent` fed, System 0/1/2 graded
  effort, tiebreaks (draw last), RDL codified search order. Remaining planned-but-unbuilt:
  per-line marginal-gain leave rule (level-rate×wall exists), full general habit tier.
- Knowledge audit: WordNet genuinely read; ConceptNet read via an 8-pair motion table only
  (UsedFor/IsA/HasProperty unused); **VerbNet written at affordance.py:219, read by nothing** —
  "throw brings toss and hurl" (42:116) has no implementation.

VERDICT (from the figures, triangulated Fig 11 + Fig 9 + Fig 4 + Fig 10 + THE FORMULA):
1. The architecture is NOT hindered by broken faculties. The three top blockages are missing
   contact (no settled term, no adoptable goal), exactly Fig 11's capability-as-contact. No
   switch flip or game tuning is the fix; the goal-direction WATSON (research 43) already
   derives the right direction (describe arrived_no_clear → look up a frame predicting the win
   condition's shape → narrow ranked candidates) and is the design for that blockage.
2. Speed is not a current blocker: the mechanisms exist and are reached. Do not add more.
3. The two genuine "built but not reached" faculties are VerbNet (data inert) and the epoch
   measure (never built). These are the legitimate changes for this autonomous session.

BUILDS DECIDED (in order, each behind a switch, with must-fails, on development only):
A. **Epoch progress instrument** (answers the user's explicit ask). A read-only, ground-only
   per-generation record: words grounded (distinct atoms with a ground settle), sentences
   formed (distinct composed terms that settled AND were used as a method/route), presses-to-
   first-settle, and ground outcomes (levels). Explicitly NOT terms minted or frames (THE
   FORMULA). Written at the generation boundary, never read by agent decisions (Fig 10).
   Must-fail: a frame-internal proxy cannot make the trend move; a replay cannot count as a
   new method (Fig 4). This makes "getting better at grammar" checkable across epochs.
B. **VerbNet class expansion** (wires a built faculty). One-pass: a found verb with a declared
   class brings its sisters as NO-STANDING prior candidates, same source/stamp, ranked by
   agreement, priced (Fig 12 :41), behind an arm default ON with an OFF identity row. Must-fail:
   with the expansion removed, the sister verbs are absent from the prior list. Cost if wrong:
   more candidate verbs to test, bounded because ground alone gives standing; undoable: arm OFF;
   reversed by: held-out measurement showing no improvement, or Isaiah ruling the class data
   too noisy (docs already flag rough verb picking).

HOLD / NOT BUILD: goal-direction change (research 43) is a design for Isaiah — no code this
session. Reflex/habit generalization and per-line marginal leave rule are proposed-not-built
but not blockages. No ARC-game tuning, no answers encoded, no check weakened.

CENSUS: Fig 1 per-slot residual · Fig 2 ground-only evidence · Fig 3 dependency order ·
Fig 4 methods cross up · Fig 5 bargain prices · Fig 6 reach vs budget · Fig 7 handoffs ·
Fig 8 residual-first lookup · Fig 9 describe-then-look-up-then-narrow · Fig 10 verifier's
non-access · Fig 11 capability is agent-and-habitat · Fig 12 bonds charged · Fig 13 minimum
set. Strained: none after unbundling.


## 2026-11-20 — ImageNet to AKAZE, demonstrated end to end (opt-in, offline)

The optional ImageNet class memory was previously only verified structurally (detector,
header, inert rows). It is now DEMONSTRATED: ImageNet images built into an AKAZE memory and
named back to the correct WordNet synset.

- **Build**: one validation shard, six classes (`labels=[575,761,159,700,209,116]`),
  `per_class=8`, offline into `C:\TETHER_RUNS\CLEANUP_2026-11-16\imagenet_val_small`.
  Completed in **93 s**. Memory: 6 classes, 38,172 AKAZE centres, 2.2 MB npz, 6 WordNet synsets.
- **Activation**: with `RDL_RECOGNITION_DIR` pointed at the built memory and
  `IMAGENET_PARQUET_DIR` at the local data, `class_memory_status` returns
  `active=True, classes=6, event=class_memory_active`.
- **Recognition**: 6 source images from the same shard were named with the correct synset
  (e.g. `n03445924`, `n01955084`, `n04074963`), RANSAC inliers 314–1,573, zero abstentions.
  This is the same AKAZE index and vote/geometry path used by the shipped shape memory; only
  the source images differ.

Two builder defects were found and fixed while doing this, both measured:
1. `build_from_parquet` materialized all image bytes of a shard into Python objects BEFORE
   the `per_class` filter (`read_table(["image","label"]).to_pylist()`). A 458 MB validation
   shard reached 2.96 GB RAM and 8+ min, while reading the label column alone took 0.1 s.
   Fixed by choosing row indices from labels first and decoding only selected rows.
2. Even fixed, an unfiltered full-shard proof (~974 classes, ~2,900 images) is a large
   clustering job (~9 min CPU, 3.2 GB) — the centroid pass, not AKAZE. Added an optional
   `labels` filter so a proof build can select a handful of classes; the six-class build took
   93 s.

Scope: this is a demonstration of capability for people who have ImageNet locally. Nothing
was committed to the repo (the memory lives in a temp dir), the builder is offline-only and
never on the agent path, the data was never uploaded, and real boards still carry no picture
field so the route remains inert in the live task. No ARC-game tuning, no neural network.

The 142.8 GB for the full 1,000-class train set is data, not training: the cost is reading
and indexing example images once offline. The proof shows a subset takes seconds per class.

WATSON — VerbNet: data carried but never used for inference (DRAFT, awaiting faculty audit)

QUESTION (effect terms): the design says "one found verb brings its class: throw brings toss,
hurl, fling" (42:116), widening the testable action list. In the run, a found verb does NOT
bring its sisters — the affordance prior list stays narrow. What should be done?

DOMAIN CENSUS:
- R: one verb-prior expansion (arity: verb → class → sister verbs; scale: one concept's
  prior list; symmetry: a sister is a candidate, not a verdict).
- domains: (a) the library layer — actors: verbs/classes, currency: candidate actions,
  anchor: word_map/relations data. (b) the affordance bet — actors: priors, currency:
  settled/refused, anchor: the board. (c) grammar — actors: bonded terms, currency:
  compositions, anchor: the ledger.
- union: found-verb and class-sister share a prior row; both are NO-STANDING candidates
  settled only by the ground (42:117 "the board is the only one with standing").
- order (Fig 3): library → prior → bet → ground.

TETHER (primary, verbatim from docs/01-FOUNDATIONS/03-FIGURES_TEXT.md):
- Fig 12 :46 "A bond is the typed relation between two operands. There are seven, they are
  not interchangeable, and which one holds is not recoverable from the operands." → a verb
  class is a bond between verbs, not a synonym; the relation must be RECORDED, not inferred
  from names.
- Fig 12 :41 "and the bond is charged for what it could have been" → class expansion is not
  free; a wrong sister costs description bits, so it must be priced like any other candidate.
- Fig 9 :29 "matching is a one-pass check, not a search" / :42 "narrowing gets you close, the
  ground decides" → expansion is a one-pass lookup from the found verb's declared class,
  then the board settles. No search over all verbs.
- Fig 4 :22 "Only methods cross up. Only head starts come down." → VerbNet classes are a
  head start (inherited data), not a claim; they carry no standing.
- Fig 11 :39-40 "capability is a property of agent-and-habitat" → the widening matters only
  if it changes contact (more testable verbs on a real board), not a count of data rows.

WITNESS (world): lexical class expansion is standard in distributional semantics (a found
verb's class members are candidates); but the witness is secondary and cannot overrule the
figure requirement that each candidate is charged and ground-settled.

CODE ANCHOR:
- affordance.py:219 writes `"verbnet": list(a.get("vn") or ())` into each ConceptNet prior.
- A repo-wide search finds NO reader of that key. build_relations.py:484 builds `e["vn"]`
  from VerbNet 3.4 data (609 classes); the design's "throw brings toss and hurl" (42:116,
  CHANGELOG:63) has no implementation.
- So the faculty is BUILT AS DATA but NOT REACHED — the project's named "built and never
  wired" defect class.

DECISION (provisional, pending faculty audit): wire a one-pass class expansion in
affordance.merge — when a verb with a declared class is found, add its class sisters as
NO-STANDING prior candidates with the same source/stamp/found_in, behind an arm default ON
with an OFF identity row. Each sister is a candidate the board settles, not a belief.
- cost if wrong: more candidate verbs to test (wall time + a wrong prior, priced by the
  bargain); bounded because ground has no standing change.
- undoable: yes, arm OFF restores the exact prior list.
- reversed by: a measurement showing class expansion does not improve held-out affordance
  prediction or grammar composition across games; or Isaiah ruling that the class data is
  too noisy (the docs already flag rough verb picking).

HOLD: do not implement until the faculty inventory and speed audits report — a more
fundamental blocker may take priority, and the epoch-measurement design may need the same
prior-grounding signal. Record this decision then, not before.
