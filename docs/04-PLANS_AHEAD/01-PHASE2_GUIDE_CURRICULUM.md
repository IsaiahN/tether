# Phase 2 — the guide-harvest curriculum (Isaiah, 2026-09-19)

**A PLAN, not a build.** This is PART 2, and it runs **after Phase 1** — the agent training on the
25 games (`TRAINING_PLAN.md` §13–§14). It is written down now so the design is legible; nothing
here is built until Phase 1 is done and Isaiah/the reviewer sign off on the shape.

---

## The idea

Retro-game **walkthroughs are (state, human-trace) pairs at scale.** A walkthrough step carries an
**image** (a game state the agent can perceive) and **text** (what the human did, why, and what it
depended on). GameFAQs alone has in-depth guides — text walkthroughs, maps, boss/item guides — for
**essentially every retro game**, so this is a near-unlimited, diverse source of human-traced
chunks covering the whole mechanic space, not the 25 games' slice.

**Why it is the right Phase 2:** the 25 public games are mostly single-mechanic; the private set is
diverse 8-bit games. The corpus (`DISTRIBUTION_COVERAGE_ANALYSIS`) put ~45% of the private set on
families current approaches lack — constraint/prerequisite ordering (F1), causal chains (F5),
multi-step coordination (F10). A walkthrough is a **deep dependency graph** exactly of that kind:
"get item X before dungeon Y", nested sub-goals, item-as-tool. It is the "trace of thought" the
pretraining thesis wants — chunkify it, let the agent learn the prerequisite reasoning without
being told.

---

## Variance across walkthroughs → the essence (Isaiah, 2026-09-19)

GameFAQs has **several walkthroughs for the same game**, written independently. Their **intersection
is the essence**: the dependency structure *every* author agrees on is the game's true necessary
order — the sub-goals that MUST happen and the prerequisites that MUST hold. The **variance** — one
author's particular route, order-of-optional-detours, style — is incidental.

- **This is the membrane test made mechanical.** The invariant across independent traces is the
  METHOD (what transfers); the per-author variance is the recording (what does not). Extract the
  invariant, and you have grabbed exactly the domain-agnostic structure and discarded the bindings.
- **It is offset-augmentation one level up** (`TRAINING_PLAN.md` §14.4 varies the CUT to average the
  chunking arbitrariness; this varies the AUTHOR to average the route arbitrariness).
- **It is also a derivational-independence check.** Multiple independent human derivations agreeing
  is stronger evidence a structure is real than any single trace — the same reason the corpus is a
  trustworthy frame (written independently, earlier, by a different hand).
- **The variance is not waste — it is the noise floor.** Out-of-consensus real routes are exactly
  §14.5's "noise = out-of-context real chunks, never garbage": they stop the agent overfitting one
  author's exact sequence.

---

## The chunk structure

- **Image = a state.** Consecutive step-images = a before→after transition — the same shape the
  observer already eats from the human-panel replays.
- **Text = the human trace, and it stays OFF-LINE.** It is the answer-key that shapes the learner,
  never fed at runtime — the **F134 firewall**: the agent perceives the image and must *derive* the
  action; the text only grades whether it inferred what the human did.
- **The membrane:** the trace's METHODS cross (prerequisite ordering, sub-goal nesting,
  item-as-tool); the game-specific bindings ("this key, this door") are **recordings, provenanced
  as import**, never treated as the agent's own derivation.

---

## The perception finding (measured 2026-09-19, one screenshot)

A NES Zelda walkthrough screenshot has **~7 unique colours** — it quantizes to essentially an
ARC-style label grid, so `arc_percept.components` can eat it after a colour-quantize step. The
perception path is **favorable**, not the blocker feared. What remains, and is the real
preprocessing work before any harvest:

- **A sprite is several colour regions, not one object** (Link = skin + tunic). Objecthood needs a
  sprite-grouping step, or a tile-grid downsample (NES is 8×8 tiles, a screen 32×30).
- **HUD vs playfield** — the status bar (hearts/rupees/items) is a region, not the world; must be
  cropped/separated (the presentation gap already flagged in `CLAUDE.md`).
- **Scroll** — the frame is a window on a larger world; camera motion must not read as
  everything-moving.
- **Text↔image alignment** — a guide's prose must be aligned to the step it annotates.

---

## Doctrine guardrails (each is why a claim stays checkable)

- **Contamination-clean.** These games are NOT the ARC private set — a different distribution
  entirely, so no test answer can leak. Curriculum, out of the test's reach, like the human panel.
- **Provenance required.** Every harvested trace enters as **import**, stamped with its source, so
  convergent derivation and adopted import stay distinguishable (they are identical in content).
- **Domain-agnostic.** What must transfer is the compositional STRUCTURE (dependency ordering,
  sub-goal nesting, item-as-tool), never game facts. Grade on the structure, not the bindings.
- **Off-line only.** The text trace shapes the learner off-line; the run path reads no guide.

---

## Open — Isaiah's / the reviewer's, not decided here

- **Source & scale:** which games, how many, weighted how (by mechanic coverage? by the corpus's
  family gaps?). GameFAQs breadth vs curated depth.
- **Harvest mechanics:** copy the text trace, the imagemap, or both; how to align them; how to
  segment/crop the images (sprite-grouping vs tile-downsample; HUD crop; scroll handling).
- **Placement in the schedule:** Phase 2 strictly after the 25-game run; whether it interleaves
  with the synthetic-generation path (`TRAINING_PLAN.md` §14.10) or precedes it.
- **Grading:** the self-graded / F134 reward applied to guide-derived chunks — does the agent
  re-derive the human's next step from the image alone.

---

## Prerequisites (ordering)

1. **Phase 1 complete** — the agent converges on the 25 games (the ablation/terminal-condition
   subject exists) before broadening.
2. **Perception-presentation layer** — sprite-grouping / HUD-crop / scroll handling, so a real
   screenshot becomes the object representation the agent perceives. This is the first buildable
   piece and the one the 25-game (cleaner) frames never force.
3. **Provenance plumbing** — the import stamp on harvested traces, so the ablation stays honest.

**The synthesizer (`synth.py`) and the guide-harvest are complementary:** the synthesizer makes
scenes from library compositions (controlled, unlimited, self-graded); the guide-harvest imports
real human traces (rich, diverse, provenanced). Phase 2 likely uses both — generated breadth plus
harvested depth — but that interleave is an open schedule question above.
