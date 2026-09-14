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

- **[BR-1] ls20 — 164 slots the bargain refuses**
  `games:` ls20 (1) · `chunks/size:` 164 refused slots (persistence run, 4 plays, fixed point at
  12/176 bound) · `gap:` the frozen 8-attribute vocabulary composes no term that compresses these
  residuals — did-not-pay/no-split persist across plays; the agent finds candidates and the MDL
  bargain says no. Perception is too coarse to make these residuals payable. · `fix?:` (hypothesis,
  not ranked) unknown attribute/relation; the residual shapes on these slots would name it if
  clustered — deferred to when the threshold fires. · `status:` 1 game, held.

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

- *(empty — populated by the ls20 reverse-engineering map once the milestone precondition is read:
  a 400-cycle ls20 probe is running to confirm whether a routine ever commits under budget, i.e.
  whether the answer-key / goal-selection line has a subject before the map is built.)*

---

## What earns nothing yet, and why that is the correct state

Two games, two different gaps, each at 1 game. Nothing is near the cross-game threshold. No
perception is added. This is the log doing its job: accumulating evidence with the question left
open, so that when a gap-shape does repeat across games, the fix is derived from the full evidence
rather than rubber-stamped from the first instance.
