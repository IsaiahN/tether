# The demand-ranked perception log

Spec: `TRAINING_PLAN.md` §"the demand-ranked list" (2026-09-14). This is the accumulator that
decides — later, never now — what perception is worth building. It is **seat-side evidence**, not
an input to the agent: nothing here is fed to the loop.

## The rules this file obeys

- **Rank on the GAP, never on the fix.** The gap is the evidence (`gap:`); the fix is a per-instance
  hypothesis (`fix?:`) in its own field, and the list never sorts on it. When the threshold fires,
  the fix is **re-derived from all accumulated instances**, not taken from the first.
- **Count GAMES, not chunks.** Eleven chunks in one game is *one game* demanding a cue. The chunk
  count sizes the demand; the game count is what crosses the threshold. Per-game-not-pooled, applied
  to demand.
- **A perception change is earned by cross-game demand only.** The same breadth counter as promotion
  and demotion, on a third axis (the tenth-sense licence — *repeated demand across different
  situations* — applied to perception). One game never earns a change.
- **The answer key stays inside today's perception.** A chunk that won't fit is logged here as a
  finding; reaching for a relation to make it fit is the key deciding what the agent gets, which is
  forbidden. Logging is the whole response.

Today's perception (what a gap is measured against): 8 extractors — `colour` (a within-game
distinctness id, never a literal), `row`, `col`, `h`, `w`, `drow`, `dcol`, `shape` — plus the one
relation `touching`. `VOCABULARY_FROZEN.md` is the dated frozen set.

## The threshold

Not yet set as a constant, and it must not be a tuned one — state-derived (how many independent
games demanded the same gap-shape), like promotion's and demotion's counters. Placeholder reading:
nothing is near earning a change; every gap below stands at **1 game**.

---

## Entries — ranked by game-count of the gap (highest first)

Two kinds of evidence, both perception-reach demand, kept labelled because they carry different
specificity. `binding-refused` is the agent's own play failing to compose a paying term (demand
without a named gap-shape). `chunk-inexpressible` is a human-replay chunk whose effect cannot be
stated in the frozen vocabulary (demand with a named gap-shape) — the §13 source, populated as the
reverse-engineering map is built.

### binding-refused (agent's own residuals, no frozen term pays)

- **[BR-1] ls20 — refused slots, CORRECTED: mostly a pricing artefact, not perception**
  `games:` ls20 (1) · `chunks/size:` did-not-pay 160, no-split 753 (250-cycle stream) ·
  `gap:` **PARTLY WITHDRAWN as perception demand (reviewer, 2026-09-14).** Measured the did-not-pay
  overage (cost+left − base) on disk: median 4.23 bits, **73% within one atom-cost (5.6 bits) of
  paying, 34% within F48's 2.77-bit median slack, and some NEGATIVE** (would pay under `pays()` but
  were refused/relabeled). So the majority of did-not-pay is the **strict all-or-nothing acceptance
  gate (`pays: cost+left < base`) refusing near-paying terms — a PRICING BUILD ITEM, not a
  perception gap** (F48: one atom = 5.6 bits vs 2.77 median slack). Only the far-over tail (~27%
  beyond one atom, up to 16.65 bits over) is a candidate perception-reach gap, and even that is not
  filed until the pricing fix is tried, because a corrected gate moves the denominator. · `fix?:`
  (hypothesis, not ranked) two separable: (a) BUILD — partial-credit / staged acceptance so a term
  that compresses most of a residual is not refused all-or-nothing; (b) PERCEPTION — only for the
  residual tail that stays refused after (a). · `status:` reclassified — the pricing half is a build
  item, not perception demand; the perception half is HELD pending the pricing fix. 1 game.

- **[BR-2] sp80 — 64 slots, zero binding, agent goes inert**
  `games:` sp80 (1) · `chunks/size:` 64 slots, 0 bound all 4 plays · `gap:` distinct from BR-1 —
  after play 1 the funnel empties to `no-eligible-target:none-stale`: no slot ever goes stale, so no
  candidate is even proposed. The agent's actions produce no change its vocabulary registers, so
  binding is never re-attempted. · `fix?:` (hypothesis, not ranked) perception that registers
  whatever sp80's actions do to the board — untested which attribute. · `status:` 1 game, held.

  Note: BR-1 and BR-2 are NOT the same gap and must not be pooled into "2 games demand perception."
  BR-1 is *refusal* (bargain loses); BR-2 is *inertia* (nothing goes stale). They may resolve to the
  same or different fixes; that is decided when each gap-shape independently reaches threshold.

### chunk-inexpressible (human-replay chunks that won't fit the frozen vocabulary)

From the ls20 answer key (`reverse_engineer.answer_key`, 72 chunks, 49 inexpressible). Two
gap-shapes, aggregated — ls20 is **1 game** regardless of chunk count; the chunk count sizes the
demand, the game count crosses the threshold.

- **[CI-1] recolour referent is a relation not in the frozen set**
  `games:` ls20 (1) · `size:` 124 chunks · `gap:` a recolour whose new colour matches no
  `touching` or `above` object — the rule that sets the colour references a relation the frozen set
  (touching, above) does not contain, so the transformation cannot be written in current
  perception. · `fix?:` (hypothesis, not ranked) a colour-source relation — nearest-same, contains,
  or a global palette map; re-derived from all instances at threshold, not taken here. · `status:`
  1 game, held.

- **[CI-2] systematic spawn/death trigger is arity ≥ 2**
  `games:` ls20 (1) · `size:` 31 chunks · `gap:` ≥3 objects appear/vanish within a chunk on a
  trigger (a conditional/event) the one-slot-in-one-slot-out atom signature cannot bet on —
  population count is frozen but the trigger is not. · `fix?:` (hypothesis, not ranked) an arity-≥2
  event relation (NSM frame holds the arity); re-derived at threshold. · `status:` 1 game, held.

  Note: CI-1/CI-2 and BR-1's perception tail are DIFFERENT gap-shapes and not pooled. All at 1
  game — nothing near the cross-game threshold, so no perception is added. Correct state.

### positioned-action-coordinate (a positioned action needs a PRODUCTIVE coordinate)

- **[PC-1] the productive coordinate is not perceivable — the focal-object heuristic misses it**
  `games:` ft09, su15 (**2**) · `size:` measured after F28/F144 (the positioned action now lands its
  coordinate): on games where ACTION6 is the arm, the agent chooses the coordinate = the focal
  object's position, which works where objects overlap interactive cells (vc33 full loop, tn36 alive)
  but is INERT where the interactive region is sparse — ft09 (board responds 1/20, bound 0, reach 0)
  and su15 (loop never engages, bound 0). · `gap:` the agent perceives object positions but NOT which
  board regions are INTERACTIVE (respond to a positioned action), so it cannot choose a productive
  coordinate where interactive cells are not at objects — the action fires and nothing happens. ·
  `fix?:` (hypothesis, not ranked) a perception of interactive/affordance regions — where a positioned
  action would have an effect — re-derived from all instances at threshold. · `status:` **2 games**,
  held. First cross-game gap in the log; still below whatever the state-derived threshold is, so no
  perception is added — but it is the first to accumulate past one game, and it came from a contact
  change (F28) making a previously-unmeasurable gap measurable.

  Note: PC-1 is a gap about POSITIONED-ACTION productivity, distinct from BR (binding refusal) and CI
  (chunk inexpressibility) — not pooled. Its two games agree on the gap-shape (productive coordinate
  not perceivable); the fix is one hypothesis, re-derived from both at threshold.

---

## What earns nothing yet, and why that is the correct state

Several gaps, mostly at 1 game; PC-1 is the first at **2 games** (ft09 + su15). Nothing is confirmed
past the state-derived cross-game threshold, so no perception is added. This is the log doing its
job: accumulating evidence with the question left open, so that when a gap-shape does repeat across
enough games, the fix is derived from the full evidence rather than rubber-stamped from the first
instance. PC-1 crossing from 1 to 2 games is the mechanism working as designed — a contact change
(F28) turned a previously-invisible gap into counted, cross-game evidence.

### relation-to-value operator gap (a two-place relation has no way to hand you its far end's VALUE)

**This is an OPERATOR/composition-path gap, not a perception gap (reviewer, 2026-09-14, Doc 21:47).**
Filed here because the reviewer ruled it earns the log's first real-weight, cross-game entry — but
it is governed by composition-vs-import (Isaiah's call), NOT the tenth-sense licence: nothing is
unrepresented (both objects and both values are already slots; the operand mechanism already carries
the related object into Ctx). What is missing is a PATH — a dereference operator that returns the
far end's value — not a reading. Figure 6's line: composition explores what OPERATORS reach;
instruments extend what can be REPRESENTED.

- **[OP-1] `relation → value` is structurally absent AND cross-game demanded — the reviewer's outcome 1, measured on THREE boards**
  `games:` vc33, sp80, ls20 (**3**) · `structural (game-independent, from the atom registry):` of 45
  non-PREDICT atoms, every value-typed OUT reads the focal object's own attribute (ctx-self), a unary
  transform, or a whole-population fold (→EXTENT only: count/rank_in/sum_group/distinct). ZERO atoms
  dereference a SPECIFIC related object to yield its value. The 5 operand-reading (arity-2) atoms —
  same/other/above/both/either — all output PRED; touching outputs BOOL. So `relation → value` is
  absent on EVERY board identically (the atom set is shared) — reachability does not vary per game. ·
  `demand (per-board, 40 cycles each):` **100% of reach-failures on all three boards are arity-2 with
  a value target** — vc33 207/208, sp80 294/295, ls20 786/786. The conservative cut that excludes
  EXTENT (where the group-folds could already pay) — targets NO existing atom can produce from a
  relation (SHAPE/POSITION/DELTA/COLOUR) — is still **62% (vc33), 82% (sp80), 77% (ls20)**. And the
  demand is real, not a firing artefact: arity-1 reaches SUCCEED (3, 3, 8 across boards) while arity-2
  value reaches succeed at ~0–2% (0/207, 6/300, 0/786). · `fix?:` (hypothesis, not ranked) a
  dereference OPERATOR — apply an extractor to the object at the far end of a relation, returning its
  value; shaping-safe because it names no relation, no object, no value (it says the path exists,
  contains no answer). Re-derived at ruling, not taken here. · `status:` **3 games, cross-game demand
  MEASURED rather than argued — outcome 1.** Structurally absent and load-bearing (not "not ripe").
  HELD for Isaiah's composition-vs-import ruling; reviewer holding with the seat, not ruling.

  **CORRECTION (reviewer, 2026-09-14 Doc 22:32): cross-game demand is NOT the gate for this, and OP-1
  should not be read as "outcome 1 licenses the build."** Cross-game demand via the demand log gates
  PERCEPTION changes. This resolved to COMPOSITION (Figure 6), so the demand log does not apply — the
  gate is **legitimacy (the figures) + effect (it moves reach while reach-failure falls)**, which the
  reviewer ruled GO. The three-board walk keeps its value for a DIFFERENT question — **generality: is
  this THE wall or a wall on vc33** — and that check runs AFTER the build, not as its licence. OP-1 is
  retained as generality evidence and as the structural proof; it is not the licensing gate.

  Note: OP-1 is distinct from BR (binding refusal), CI (chunk inexpressibility), and PC (positioned-
  action productivity) — not pooled. It is the first entry to cross with three games AND a structural
  proof under it, which is why the reviewer weighted it above the 1-game and 2-game entries above.
