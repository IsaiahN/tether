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

---

## What earns nothing yet, and why that is the correct state

Two games, two different gaps, each at 1 game. Nothing is near the cross-game threshold. No
perception is added. This is the log doing its job: accumulating evidence with the question left
open, so that when a gap-shape does repeat across games, the fix is derived from the full evidence
rather than rubber-stamped from the first instance.
