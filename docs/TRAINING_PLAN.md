# Training the agent — the aligned plan (curriculum, not answers)

**Seat + reviewer + Isaiah, aligned 2026-09-13. This is the working roadmap. It supersedes
scattered notes; where it conflicts with an older doc, this is the current intent.**

The one-sentence law that governs everything below:

> **A solution may be used to test our instruments and to measure how far the agent got. It
> may never be used to decide what the agent is given.**

---

## 1. The goal and the bar

Build a **white-box** agent that beats ARC-AGI-3 by **reasoning**, not by being told answers —
one that, handed a fresh game, forms plans and clears levels using all its reasoning systems,
and can say *how* and *why* in a readable string of atoms and operators. The metric is the
ground: **levels completed per game (RLVR)**, per game, never pooled. Enough level completions
is a win. Traction is the mechanism; level completion is the readout.

**The ablation gate (terminal condition, clause 3), refined 2026-09-13:** back up Γ, wipe, and
re-run — if the win survives, the agent composed it; if it disappears, the library was carrying
the answer. **Ablation is not all-or-nothing at 25/25: it is interpretable per game the moment
that game is won** (wipe, re-run *that* game, see if the win holds). **25/25 — all twenty-five
public games each carried to a `WIN` game status** — is the *full* ablation across the set, not
the threshold for any ablation at all. The *recording* of what admitted each term must still
happen as entries occur (proctor-side; see §11), because it cannot be reconstructed later.

---

## 2. The problem this plan solves

Ouroboros v1–v4 paid in **generations across a network of agents** sharing wins, losses and
learnings (Figure 4: the population, the membrane). **A single agent in a nine-hour window
cannot pay that bill** — it might stumble onto 1–2 of ~120 games by brute force, and random
alone clears some level-1s, which the agent has not yet done at all. So the agent needs
**pretraining**, and pretraining is the legitimate substitute for the generations: **pay in
bodies across thousands of generated tasks, buying with habitat what earlier generations bought
with agents.**

Brute force will not turn into strategy on its own. Something has to shape the contingency
evidence into reflexes. In a symbolic system that shaping force is **RLVR over a curriculum**
plus the symbolic credit-assignment the framework already half-owns (negation, the fifth ROUTE
bin, the failed-path catalogue) — the symbolic analog of backprop, not backprop itself.

---

## 3. The bright line — what MAY and MAY NOT be done with the public answers

We have the **public set and its publicly available answers/replays**. We do **not** have the
private set — only ARC does, playable solely through an offline Kaggle notebook. The score
comes from that private set, which we never see. Therefore anything overfit to the *public*
games is undetectable to us and fails silently on the private set. This is exactly why the
answers must be an **exam and a diagnostic**, never a **training source**.

**MAY — the positive control.** Execute a known solution by hand, read `levels_completed`, read
the frame beside it. Nothing reaches the agent. One outcome (the harness not reporting
completions) would invalidate every capability reading in the record. This is Isaiah's live-watch
side; it needs online/Kaggle access. **On the live watch: symptoms may come down, solutions may
not** — "it isn't acting / actions aren't landing / it repeats one button" may cross to the seat;
"the door is at Y / do A before B" may not.

**MAY — a distance metric for us.** *Reached step 3 of 7* instead of *lost*, for reading traces,
never as a signal to the agent.

**MAY, CAREFULLY — an expressibility check.** Can the vocabulary *state* a solution? It may tell
us **whether**. The moment it tells us **what** to add, it is contaminated, because then we add
exactly that and the architecture did not reach it.

**MAY NOT — derive the compositions, paths, atoms or recipes a game needs and build toward
them, or train the agent toward reverse-engineered paths, in any form, for any game, however
general the resulting change looks.** The white-box argument is decisive here: if we train the
agent toward paths we derived, the atom-strings we read afterward are *ours*, not its reasoning —
the white-box becomes a mirror, and the ablation can no longer separate composed-from-reasoning
from given-as-head-start. Convergent derivation and adopted import look identical in the
contents (Figure 8); only provenance separates them, and training on imports destroys the
provenance the whole claim rests on.

---

## 4. The white-box RL, stated so it cannot drift

The deciding variable for every training decision is one question:

> **Does the agent see the SITUATION, or the SOLUTION?**

- **Present the situation** — the frames, the state, chunked into short windows so multi-step
  structure is visible — and let the agent reason, act, and be corrected by the ground. That is
  **practice**. The atom-strings it produces are its own, so the white-box stays real, and only
  cross-situation **method** promotes (which is what transfers).
- **Show the winning actions to imitate** — that is a **demonstration** it will replay and
  cannot generalize; it overfits the public set, forfeits the private set, and turns the
  white-box into a mirror.

Isaiah's intent is the first: *present the situation frame by frame, or in chunks of frames, so
it understands relationships and multi-step planning.* Understand, not copy. The guardrail while
building: the presentation carries the **situation and the ground's verdict, never the winning
action**, and at ablation we confirm what *promoted* is cross-situation method, not
public-game-specific recipe.

---

## 5. Current state of the agent (code-grounded)

- **The root is binding.** ~97.5% of residuals sit on a slot with no binding at all; of the
  bound, most hold a bare atom that cannot settle by construction; a few settle. **Settling is
  starved, not blocked** (F118). Every barrier named before this — selector, shelf, acceptance
  gate, promotion — is downstream of the binding gate.

- **Persistence is built and verified, and was switched OFF.** `gamma.save`/`load` round-trips
  correctly (verified 2026-09-13, three arms: same-game carries as `minted`, cross-game enters as
  `imported` and is counted apart so the ablation stays clean, incompatible registry refuses
  loudly). Isaiah ruled the library persists, because transfer is the claim. The switch is
  `arc_holdout.play(..., library=<path>)`, default cold — and every "reach 48 baseline, levels 0"
  reading was taken cold, which is a real confound. **Persistence is ON from here.** (This proves
  the wiring; capability — that carrying the library across plays helps — needs a real run with
  the switch on.)

- **Promotion is wired and starved, coupled to persistence.** The chain
  `retro → _promotions → _promote → gamma.promote` fires only when a term minted for one slot
  retroactively closes a *parked residual on a different slot* (or across a level):
  `if slot != origin_slot or cross`. On real boards that cross-slot event never happens — plausibly
  because binding is starved, so there is almost no occasion for one slot's term to resolve
  another's residual. A cold run also evaporates any promotion, so this only reads true with the
  switch on. **Trace pending, after persistence is on.**

- **System 0 is an ordering, plus one small state-derived build.** `choose()` priority is:
  held routine → plan formation → probe (if bored) → discriminate → learned arm → fall-through
  formation → goal split → **uniform draw, dead last.** The uniform-random mechanism System 0
  wants already exists (the "draw"), but it is the blind fallthrough, reached only when every
  strategic arm is silent. Isaiah's System 0 — *start random, then jump to strategy; a System 0
  beneath System 1 and 2* — is the opposite ordering: act variously **first**, before the learned
  arm collapses to one button (F26: ACTION1 on ~79% of cycles, 100% where the learned arm has an
  opinion), so binding gets the varied (before, action, after) evidence it needs. A one-button
  policy produces one column of the contingency table over and over — same zero as random,
  entirely different evidential yield. **The switch must be state-derived** (binding density, or
  coverage of the action-by-slot space, read from the agent's own state) — **never a fixed cycle
  count**, which is a tuned constant under the shaping ruling.

---

## 6. The stages

### Stage 0 — the preconditions (cheap, gate everything)

1. **Persistence round-trips** — DONE, verified. Now run with it ON.
2. **Does promotion complete anywhere** — trace after persistence is on. If it never fires even
   then, that is the finding and it outranks the curriculum: training without promotion fills a
   library that never becomes a capability.
3. **Does the harness report completions** — the positive control (Isaiah's side). If it does
   not, every capability reading (including "levels 0") is suspect.

### Stage 1 — a generated / situational curriculum, NOT the 25 games as answers

**THERE MAY BE NO GENERATOR TO BUILD — THE CURRICULUM ALREADY EXISTS (reviewer + Isaiah,
2026-09-14). See `SELF_GRADED_CURRICULUM.md`.** The library-closure is itself a curriculum: hold
out a random subset of its 2,205 composites ACROSS TIERS and have the composer re-derive them from
the remainder, grading by the recipe (the recipe is the receipt — *did it rebuild this composite* is
mechanically checkable). No board, no generator, no answer key in the contaminating sense — **the
library is the ground.** The contamination defence is Isaiah's: randomise the split and let fitness
select, so no one chose what to withhold and nothing about the boards can leak; fitness is
re-derivation inside the held-out library, NEVER performance on the target games. It runs over the
library-closure's OWN domain-general vocabulary (the composer core is generic — `Gamma` takes any
typed atom list), disjoint from ARC, so it cannot contaminate the claim. It is FAST (no board/API),
so the accumulation the flywheel needs is affordable here, and it is the only direct measure of the
parts-bin thesis: does re-derivation cost per composite FALL as the bin grows. This is the
preferred Stage 1 — the generator below is the fallback if the three code-checks in
`SELF_GRADED_CURRICULUM.md` fail.

The generator fallback: build a task generator over the **same substrate the agent already
perceives**: objects, attributes (position, colour, extent, shape), relations (same, other, above),
the seven actions, the same partial observability. Thousands of tasks; none an ARC game fed as an
answer.

- **Legitimate because no board knowledge enters** — the generator is built from the agent's own
  type system (the code's stated intent), not from watching what these boards need. **Every
  generator parameter carries the same provenance check**, not just the atom set — board
  structure can enter through a design choice as easily as through an atom.
- **The one permitted board-adjacent use:** the *published* ARC-AGI-3 taxonomy of task kinds is
  external and public. Use it to check the curriculum **covers the same kinds of structure**
  (containment, ordering, conditional triggers). Deriving that taxonomy ourselves by playing the
  games is not permitted — the distinction is provenance, which is the shaping test.
- **Real public frames may be used as situations** (they are public), presented for the agent to
  **solve itself** under the ground's reward — never with the winning actions shown.

### Stage 2 — curriculum by horizon (the chunk idea, kept intact)

Grade by plan length / frame-chunk length, because that is the stage the agent has not cleared:

1. **One action / one frame** — does acting change anything? Contingency detection (passed).
2. **Two–three actions / a short chunk** — the first kept routine. **The means-end gate, the
   first thing that has never happened** (`routine_cut` 0, 38 planning attempts, 38 refusals).
3. **Five actions** — composition over a kept routine.
4. **Ten and beyond** — plans that survive an interruption.

**Advance on a measured criterion, never a fixed schedule** — `routine_cut` non-zero and holding,
not *after N episodes*. A schedule is a tuned constant under the same ruling as every other one.

### Stage 3 — what "training" is here (not backprop)

The learning mechanism already exists and is the whole architecture: **mint, pay the bargain, let
the ground settle it, promote what survives.** Training is that loop run over a large habitat with
**the library carried forward** (persistence) and **promotion completing** — no new mechanism.
The one borrowing worth making is not gradients but **conflict-driven clause learning**: when a
search fails, derive *which* commitment caused it and learn a term that forbids it — the fifth
ROUTE bin, negation, and the failed-path catalogue, three pieces of one mechanism the framework
specifies and has never run.

**THE ASYMMETRY, AND IT REPRIORITISES THIS WHOLE PLAN (Isaiah, 2026-09-14).** Pretraining is mainly
there to negate the combinatorial explosion of ways things go **wrong**, more than to name the
right answers — and the two are not the same size. **The right answers are a thin set; the wrong
ones are almost everything.** A prior that says where *not* to look prunes vastly more than one
that says where to look, *and it cannot carry the answer* — it only shrinks the space. That is the
**safe** form of a prior (which is exactly why F133's positive what-to-do channel was over the line
and a negative prior is not): the aisles aren't removed, they're marked dead. **So the what-not-to-
do half is not the second blade of the scissors — it is the load-bearing one.** The qualification:
*not here* narrows, it never proposes, so a generator is still needed — but generation already
exists and is cheap (minting + the closure walk). **What is missing is the thing that stops the
generator producing the same dead candidates forever: 174 bets a cycle, 99% failing, and nothing
remembering they failed.** That makes the **refutation cache the highest-value unbuilt mechanism in
the project**, and it is the direct attack on the reach-failure metric — the composer becoming a
librarian by marking aisles dead. Build it before the accumulation runs, not after: it is also what
makes them affordable. See `LIBRARY_VS_COMPOSER.md`.

**THE ONE PROPERTY THAT DECIDES PRUNE-OR-BLOAT (reviewer, 2026-09-14).** The refutation must be
keyed on something that **generalises**, not on the candidate that failed. *This exact term failed
here* prunes one candidate — a lookup table that grows as fast as the search does, which against
174 bets a cycle is the explosion wearing a cache's clothes. *This shape of composition fails under
these conditions* prunes an aisle — and **that** is what makes it a negative prior. The design is
already half-answered: the failed-path catalogue (`_gap_key`) keys on the **characterised residual
— types, not instances** (arity, `varies_types`, `target_type`, `rel_types`), and `rel_types`
crosses on type rather than pair. **The refutation cache must obey the same rule**, or the two
mechanisms disagree about what a failure is. Not a check to add and not a thing to measure — the one
property that decides whether it prunes or bloats.

**AND THE FAILURE MODE, WRITTEN DOWN BEFORE THE NUMBERS ARRIVE (reviewer, 2026-09-14).** A key
coarse enough to prune an aisle can prune an aisle that **had a door in it**. `_gap_key` was
designed for *retrieval*, where too-wide is survivable — a slightly-too-wide retrieval still cuts
the problem down. As a *refusal* key, too-wide **silently removes reachable terms**, and nothing
downstream reports a term that was never generated. This is not a reason to narrow the key; it is
the one way the mechanism goes wrong *quietly*. The symptom reads as success: **reach-failure
falls, and reach falls with it.** So the guard — the paired-run guard the plan already requires for
speedups, applied here — is: **reach-failure down is only good if reach HOLDS.** Measure successful
reach (reach − reach_failed), not reach-failure alone; a pruned door shows up as successful reach
falling while a working cache shows reach-failure falling with successful reach held. Record a
distinct `reach_pruned` event where the cache skips, so the believed-dead are never confused with
the genuinely-searched.

### Stage 4 — test on a fresh public board, cold

After the curriculum, run a public board the agent has not trained on. **Success is not that it
wins — success is that it forms a plan (`routine_cut` non-zero)**, because that is the thing that
has never happened and everything downstream waits on it.

---

## 7. The diagnostician role (the seat, with the public answers)

Given a replay, play it against the library **step by step, as a diagnostician, not a player**,
and produce a white-box map of two things:

1. **Expressibility** — can the existing atoms and bonds even *state* this solution's path?
2. **Reach gap** — where does the agent's own attempt diverge from an expressible path?

That map has exactly two legitimate uses: it tells us what **kinds** of structure the curriculum
must cover (validated against the published taxonomy), and it **diagnoses** where the pipeline
breaks. Its one forbidden use is becoming the target the agent is trained toward. Same artifact,
two uses; the line is whether it decides what the agent is given.

---

## 8. Closed levers / constraints (do not re-propose)

- **Do not seed the shelf** (permanent) — hands a routine never earned; ablation could not then
  separate composed-a-plan from given-a-head-start.
- **Directional semantics must never reach the agent** — availability of actions is legitimate to
  read; what they *mean* is not.
- **No tenth sensor unless earned** — repeated cross-situation demand that composition cannot
  meet; never handed. Ladder: composition → atom → sensor, each licensed by the level below
  having tried and failed.
- **`both`/`either` are inert by design**, not omission — do not file their zero as a gap.
- **Every speedup needs a paired run** proving reach did not fall; a cut justified by *what we saw
  ls20 need* is shaping.
- **The switch/threshold of any mechanism must be state-derived or corpus-derived**, never a
  constant tuned so a mechanism fires on the boards being tested.
- **Corpus files: annotate, never edit** (authorship by originator defines corpus).
- **Permission sits with the seat** — test both arms, A/B, git is the safety net; escalate only
  when an A/B cannot separate the arms, or a change alters what the agent is *handed*.

---

## 9. Resources

- **Public game set, replays, GIFs, and JSONLs:** https://arcprize.org/tasks?v=3 — the exam and
  the diagnostic source. Replays/answers are used to test instruments, measure how far the agent
  got, and set curriculum coverage. **Never as a training target.**
- **Published ARC-AGI-3 task-kind taxonomy** (external, public) — for coverage checking only.

---

## 10. Order of work

1. Run with **persistence on**; confirm capability (does carrying the library help across plays).
2. **Promotion trace** — does any cross-slot resolution occur; if not, is it starved by binding.
3. **System 0** — reorder the uniform draw ahead of the learned arm early, gated by a
   state-derived switch (binding density / action-slot coverage), A/B against baseline.
4. **The generator** (Stage 1) — the first real L1 contact build, once persistence + a binding
   fix let promotion complete, else it fills a leaky bucket.
5. **The diagnostician map** from the public replays, to set curriculum coverage and diagnose.

The break is at binding; System 0 is the lever most likely to unblock both binding and the
promotion that persistence then carries. The generator rests on that, not the other way round.

---

## 11. Refinements — the library model (reviewer + Isaiah, 2026-09-13)

**Ablation is per-game, not only 25/25.** Interpretable the moment the agent wins a game: wipe,
re-run *that* game, see if the win survives. 25/25 is the full ablation across the set. (Corrects
the earlier "no interpretable subject below 25/25", which was too strict.)

**Provenance is split — the agent operates provenance-free; the proctor keeps the mint record.**
The agent's operational library carries the composition (the atom string) but **not** where it
came from, so selection is driven by perceiving the situation, never by knowing an origin.
Separately, and **out of the agent's reach**, the proctor keeps a mint-provenance log
(`game_etc_mint`) for reading RL/training results and running the ablation. This satisfies the
doctrine's *import must be provenanced* (the record exists, proctor-side) and its *record the
admitting clause as entries happen* (the proctor log is that record), while denying the agent
provenance as a crutch. Figure 8's *convergent and import look identical in the contents* is
handled exactly here: identical in the AGENT's contents, separated in the PROCTOR's record.

**Selection among many is the proof.** With a large, game-agnostic settled/unsettled library, the
agent *choosing* the right composition from many — driven by perception of a novel situation — is
itself evidence of understanding rather than lookup, **provided it generalizes (transfer)**. The
proctor-side provenance is what confirms the pick was not a stored answer for that game.

**The library is symmetric: one breadth counter, two directions.** A population prunes by killing;
one agent cannot kill, so refutation-in-cache is the single-agent substitute for a body dying. It
is the same counter as promotion, run with the opposite sign:

- **Promotion** — a term paid across many *unrelated* situations → becomes primitive.
- **Demotion** — a term failed across many *unrelated* situations → loses standing.

Neither fires on a single occasion, which is exactly the rule that stops one board shaping
anything. **Refutations live in a cache and consolidate only on repeated cross-situation demand.**
The agent does not refute or permanently attribute/add to the shared library on a game-to-game
basis. **This is a BUILD ITEM: the framework specifies refutation but says nothing about how a
refusal accumulates** — and the demotion threshold, like promotion's and like the System-0 switch,
must be **state-derived (how many independent situations demanded it), never a tuned constant.**

**Transfer learning IS the goal, not a hazard.** Figure 8's indistinguishability is what transfer
looks like — methods learned in training generalizing to the private set. The ambition is to prove
it in a **white-box, CPU-only** architecture, with every decision a readable string of atoms and
operators and the proctor's provenance record keeping it honest.

**Implementation implications (to build, not yet built):**
- Persistence `save` splits into an agent-facing library (composition, provenance-light) and a
  proctor-side mint log (game + origin + handle), the latter out of the agent's reach.
- Refutation consolidates **across** games through a cache with a **state-derived** demotion
  threshold — the symmetric twin of promotion's breadth counter — rather than within one run.

---

## 12. The training loop — one game at a time (Isaiah, 2026-09-13)

Run RL + training on a **single game** until the agent has produced its **settled list, unsettled
list, and refutation cache** for that game. **Persistence carries those forward.** Advance to the
next game **only on a FULL WIN** of the current one.

- **Answer set per game = the human-panel replay** — `arcprize.org/replay/<uuid>`, plus its jsonl
  and gif. Used strictly per §3's bright line: exam and diagnostic (expressibility, distance,
  positive control), **never a training target; present the situation, never the winning actions.**
- **The replay jsonl/gif are NOT committed to git** (gitignored under `replays/`) and are kept
  **out of the agent's reach** — the seat reads the answer set, the agent reads only the frame.
  Same firewall as `environment_files/`.
- **The public set — 25 games** (source: the "ARC 3 public set replay -list" sheet, and
  https://arcprize.org/tasks?v=3): `ar25 bp35 cd82 cn04 dc22 ft09 g50t ka59 lf52 lp85 ls20 m0r0
  r11l re86 s5i5 sb26 sc25 sk48 sp80 su15 tn36 tr87 tu93 vc33 wa30`, all cached in
  `environment_files/`, human panel 100% on every one, ~101 replays at `arcprize.org/replay/<uuid>`.
  The 25/25 ablation gate is these games each carried to WIN.
- **Why one-at-a-time with carry-forward:** it is the single-agent substitute for generations. The
  library accretes across games (settled / unsettled / cache), so the Nth game is approached with
  everything the first N−1 left behind — transfer *within* the public set, and the rehearsal for
  transfer to the private set.

---

## 13. The per-game reverse-engineering loop (Isaiah, 2026-09-14; reward boundary confirmed)

**WHAT THE REVERSE-ENGINEERING IS FOR (Isaiah, 2026-09-14): NOT how to win the game — how to
EXPLAIN the derivation, the arrival process, the composition.** The answer key is an account of
*how a solution's steps map onto library derivations* (which atoms/bonds compose the observed
transformation), so the agent's own compositions can be verified by effect against it. It is never
a winning strategy to feed. The answer set is the **Human Panel Replays** (the panel solved 100% of
all 25 public games): the index is the "ARC 3 public set replay -list" sheet, the per-game replays
are `arcprize.org/replay/<uuid>` (jsonl + gif), gitignored under `replays/` and out of the agent's
reach.

**CONFIRMED (Isaiah): the RL reward VERIFIES each chunk's effect — ground-checkable against the
frames — and never scores reproduction of the human's action string.** The reverse-engineered
answers are exam, dense verifiable reward, and diagnostic; the agent discovers its own
compositions. This is the one seam the architecture forbids crossing, and the confirmation is
explicit.

**ACTION-AGNOSTIC — the training substrate is the COMPOSITION, never the action (Isaiah,
2026-09-14, two rulings, both binding):**

- **RL trains on the REASONING/COMPOSITIONS — the atoms / molecules / attributes / relations that
  make each move (or multi-move) possible — never on the actions.** Actions are doubly irrelevant:
  not the reward target (that is the effect) AND not the training substrate (that is the
  composition). The answer key describes the before→after TRANSFORMATION as a composition of frozen
  attributes/relations + operator; the human's button presses are chunk-window markers only, never
  mapped, rewarded, or learned.
- **ACTIONS MUST NOT BE BAKED IN — action-mapping happens AFTER RL, is trivial, and must stay
  agnostic.** The agent's brute-force enumeration baked actions into the composition space (PREDICT:
  `slot × action → slot`), which is the trap to avoid: the reach failure and bets/cycle explosion
  are partly that the closure enumerates over actions. RL trains the RELATE space (composing the
  goal-transformation from attributes/relations — *what* to achieve), and the `which button
  achieves it` mapping (PREDICT) is a trivial post-RL lookup, kept out of the trained content
  entirely. Nothing in the answer key, the reward, or the curriculum may reference an action.

**Pre-RL baseline preserved (reviewer, 2026-09-14):** the cold-loop numbers are the cleanest
baseline the project has, and guided RL must MOVE them: `runs/PRE_RL_BASELINE_ls20.json` —
reach-failure **98.7%** (2,789/2,825), **174 bets/cycle**, 1 routine committed (cycle 65). If
training teaches retrieval, reach-failure and bets/cycle FALL; if they don't move, the RL didn't
teach it, measured against a number taken before anything was trained.

**Acceptance gate is partly a pricing artefact, not perception (reviewer, 2026-09-14):** before
filing did-not-pay as perception demand, measured the did-not-pay overage (`cost+left − base`) on
disk — median 4.23 bits, **73% within one atom-cost (5.6) of paying**, some negative (would pay but
refused/relabeled). The strict all-or-nothing gate (`pays: cost+left < base`) refuses near-paying
terms, so the majority of did-not-pay is a **pricing BUILD ITEM** (partial-credit / staged
acceptance), not a perception gap (F48: one atom = 5.6 bits vs 2.77 median slack). `DEMAND_LOG.md`
BR-1 corrected accordingly; the perception tail is held until the pricing fix is tried, because a
corrected gate moves the denominator.

**The loop, per game, as the diagnostician:**

1. **Ingest the human-panel replay** (gif / jsonl / frames / actions), proctor-side, out of the
   agent's reach.
2. **Chunk the actions** into ~5–10-action segments (adjustable), each a candidate multi-step
   routine large enough to house planning.
3. **Reverse-engineer each chunk, "pretending to be the agent" — using the agent's own perception
   and vocabulary, not mine:** (a) the perceptual cues — objects/groups, attributes, relations —
   the agent's pipeline would read from the before/after frames; (b) the library derivation path —
   the atoms/recipes/chains/molecules **and the operator/bond**, because isomers prove an
   ingredient set alone does not fix the molecule (`Melt`/`Freeze`/`Boil` are all `Tmp + Ph`).
4. **Run the real agent across all levels of that one game. Rigorous RLVR:** the agent's
   settled / refuted / unsettled library is verified against the reverse-engineered answers —
   reward = **did it achieve each chunk's effect** (ground-checkable), never *did it reproduce the
   actions.*
5. **Provenance split:** the library entry records the granular scenario — relations, attributes,
   cues (from `RELATIONS.md` etc.) — and the **game of origin goes proctor-only, out of the
   library.** The library stays game-agnostic.
6. **Refutation cache:** failures accumulate; permanent demotion only on repeated cross-situation
   demand (the symmetric counter, §11).
7. **Milestones, not solve-or-nothing (reviewer, 2026-09-14):** the agent has never once formed a
   plan, so gating on a win means stalling on game one with no signal. The ladder: **`routine_cut`
   non-zero (a plan committed) — the FIRST real milestone and the near-term target** → plan
   completes → level cleared → full-game win (the per-game ablation proof). Reward and track every
   rung; the early target is the first plan, not the win. On graduation (the agent solves the game
   on its own library) → archive that game's reverse-engineered answers → keep the library → next
   game. *Open for Isaiah: whether advancement to the next game triggers at an early rung or at
   full-win — §12 said full-win; the reviewer's point is that early progress must be
   milestone-driven.*

### The chunk → library mapping pipeline (from the library-closure indexes)

Perceive a change → normalize its attribute (17 clusters, `ATTRIBUTE_CLUSTERS`) →
`ATTRIBUTE_INDEX` lights up candidate `DOMAIN|Atom`s → `ATTRIBUTE_REACH` gates on whether the
sensor stack can perceive it → `WORKING_SET` gives the entry points (61 domain roots, ~200 Set-A
atoms, ~200 Set-B level-2 composites) → a recipe in `ATOMS.md` is the aim point, tagged with the
operator (`OPERATORS.md`: seven bonds + negation). Composition is **61 shallow domain-local trees**
(74% within-domain), bridged by the 285-edge domain adjacency graph (`ADJACENCY_EDGES`).

### IT IS A MAPPING JOB, NOT A SEARCH — and the cue system that makes it one (Isaiah, 2026-09-15)

**This whole thing is a MAPPING job: map the human-panel INTENT to a library composition per game.
Every other route is a combinatorial explosion — a fool's errand at best, a Sisyphus problem at
worst. The seat/agent does NOT "figure out" anything except HOW TO MATCH a library composition to
the panel's intent (never the action).** Corollaries, all binding:

- **Map only into the closure.** Whatever a delta maps to must be REACHABLE/FINDABLE in
  `docs/library-closure` — nothing invented — and COMPOSABLE with `OPERATORS.md`'s operators. Do NOT
  map to the agent's ~45 gamma atoms; those are its concrete instantiations, not the map.
- **Deltas are ATTRIBUTE CHANGES, not atoms.** There are ~2,000 closure atoms/derivatives; the delta
  is a change in an object's attribute, and the change is what lights candidate atoms.
- **The full-attribute MutationObserver.** Each object/slot carries the FULL attribute+relation set
  (~100, from `RELATIONS.md`/`ATTRIBUTES.md`), initialised NULL at frame 0, and is updated in real
  time from frame 1 by a mutation-observer. This yields dense data from the start, and EVERY FRAME
  COMPOUNDS the cue + relational vector — the opposite of the agent's current 8-attribute reading,
  which is why its search is undirected (`RELATIONS.md` Part 6).
- **Attributes are DETECTORS, not a taxonomy (`ATTRIBUTES.md`).** Each atom carries attributes-to-
  check plus a boolean CONDITION that confirms it (`Solidity` ⟺ `overlapArea==0`; `Movement` ⟺
  `position(t2)!=position(t1)`). An attribute CHANGE re-fires the conditions that reference it; the
  atoms whose condition CONFIRMS are the ones that light up. That is "what atoms to search for or
  mint" — a check against the board, not a lookup handed to the agent.
- **Lit atoms → molecules via the RECIPES, not `ADJACENCY_EDGES`** (measured 2026-09-17, F162).
  `ADJACENCY_EDGES.json` is a 61-node DOMAIN graph (Acoustic, Aesthetic, Economic…) and its own
  header (`ADJACENCY.md`) says it is *derived from* the recipes — an edge is one domain's recipe
  naming another domain's ingredient. None of the ARC atoms (Translate, Deform, Construct…) are
  nodes, so it cannot compose them. The atom→molecule composition IS the RECIPE structure
  (`ATOMS.md`; machine-readable in `WORKING_SET.json` `set_b_level2`, e.g. `Orbit = Rotate +
  Translate`): a molecule is CANDIDATE when the lit atoms cover its recipe's ingredients. The
  domain graph is a coarse example of the SHAPE of composition, not the source for it.
- **MEASURED (F165, 2026-09-17): the emergent-molecule layer is INERT on ARC — 0 molecules fire
  across all 25 games.** The only per-object multi-atom co-occurrences that occur anywhere are
  `Recolour+Translate` (15165), `Recolour+Scale` (4907), `Deform+Recolour` (1248): a geometric
  change WITH a recolour, which is a CONJUNCTION the atom list already states, not a named molecule.
  No object ever does two composable GEOMETRIC things (`Rotate+Translate` = `Orbit` never occurs;
  `Deform` pairs only with `Recolour`). So the atom-conjunction `closure_derivation` (F160–F162) is
  the COMPLETE answer for ARC, and resolving `Deform → Rotate/Reflect` would NOT unlock molecules —
  there is no geometric co-occurrence to compose, so that perception question is not the blocker it
  looked like. The composer (F163/F164) is structurally correct and correctly stays silent; the
  molecule layer is proven-out infrastructure that this corpus does not exercise.

### EXPRESSIBILITY IS CLOSED, AND PROVENANCE IS WHY THIS IS THE ONLY METHOD (Isaiah, 2026-09-15)

**FOUNDATIONAL, and it corrects how expressibility has been treated here.** The primitives were
derived from the ARC human PRIOR SET, which is **exhaustive by construction**. The priors are
complete and the primitives derive from them, so **anything a human solver does is expressible in
principle.** Isaiah deliberately included substrate a machine would not need — human-only redundancy
— because that is what gets LOST in the abstraction/transformation of concepts.

**So an "inexpressible chunk" is NOT a finding for anything a human DID.** The `expressible`/`gaps`
verdicts (`reverse_engineer.py`), the `chunk-inexpressible` entries (`DEMAND_LOG.md`), and the
blocked markings (`RELATIONS.md`) read expressibility as open — and for a human-panel chunk it is
CLOSED. If a human solved it on the grid it is expressible on the grid; a chunk the pipeline cannot
express is a **MAPPING GAP (the mapping is incomplete), not a vocabulary gap.** Repair the mapping;
do not conclude a gap. (The whole is_atom / composition-wall line treated expressibility as the open
question — it never was; the open question is the MAPPING and its provenance.)

**PROVENANCE IS UNRECOVERABLE FROM PROJECTIONS, which is why you cannot build cold.** You cannot tell
how "green" was composed — RGB, CMYK, or otherwise — from the output; no one can. The projection is
lossy about how it was made, so the AUDIT TRAIL / PROVENANCE is REQUIRED to carry the composition
path (Figure 8: convergent derivation and adopted import are identical in the contents; only
provenance separates them). Evolution recovers provenance by paying in BODIES and CENTURIES — the
winners literally being the encoded answers — which we cannot afford with one agent and no time.
**So there is exactly ONE way to derive the provenance path and teach the agent the pattern:
reverse-engineer it from the human panel and MAP it.** This is why persistence is ON, the library is
not wiped, and cold/from-scratch is a fool's errand.

### CHUNKING IS THE RL TRAINING METHOD, WITH OFFSET AUGMENTATION (Isaiah, 2026-09-15)

**Chunking is not just windowing for the answer key — it is how the created agent is RL-trained.**
The agent RLs against the generated relations/compositions derived from the human panel, so it
learns to make similar decisions IN GENERAL after enough epochs (not memorising steps). Chunking
cuts the winning path into multi-step PIECES **so multi-step planning and causality are observable
within a piece** — learning step-by-step includes no causality or planning.

**OFFSET, to overcome chunking in the wrong place:** create an offset for the same game so the chunk
boundaries differ — the self-supervised move of removing a word from a sentence (masked-LM). A cut
that splits a plan in one pass is intact in an offset pass. (`protocol_b2_*` / `protocol_d25_*` jsonl
are chunk/offset protocols.)

**WHAT THIS IS FOR, MEASURED AT THE GROUND (F172, 2026-09-17): the flywheel FIRES but does not
COMPOUND, and that is what the chunking curriculum must fix.** A current-code run — `arc_holdout ls20`,
OFFLINE, the real game, 40 cycles — shows `promote: 10`, `settle: 24`, `mint: 24`, `reuse_install: 12`,
`pull: 21`, 13 reuse closures, `none-stale` only 1. **So the standing "flywheel never turns / echo
never fires / 0 promotions / REUSE_UNWIRED / units sit at the atom floor" claims (INDEX and elsewhere)
are FALSE on current code** — they were diagnosed from reading and stale/board-specific funnels, and
the run refutes them. **But it does not compound:** `chunk_reuse: 2` (the reach read's own "failure
signature" is chunk reuse of zero), `unreached_rate` flat at ~0.67 across the run (it "should FALL"),
effective depth flat, `advanced: False`. So the accurate problem is **"turns but does not compound,"**
which is a TRAINING problem this chunking curriculum is the lever for — not a dormant mechanism to
wake. **AND THE REUSE AFFORDANCE CANNOT BE MEASURED FROM THE ANSWER KEYS** (F172): their composition is
coarse closure-atom conjunctions (9 atoms), so full-chunk recurrence reads 14% (too strict) and
atom-pair recurrence reads 100% (base-rate confounded — 9 atoms make every pair recur); the agent's
reuse is over BOUND TERMS with operands, a granularity the answer keys do not carry. The compounding
question lives at the agent-run level, not the mapping level.

**AND THE CHUNK-COMPOUNDING BLOCKER, NAMED AT THE AGENT-RUN LEVEL (F173, 2026-09-17): objective
SELECTION, not routine mechanics.** A run (ledger monkeypatched for the refusal reason, ls20 offline)
shows chunks do not compound because ROUTINES are proposed and refused every time — 13 refusals, and
of the 10 that are not the loop correctly declining (3 are "objective already holds"), **8 are one
gate: "no objective is confidently shrinking" — `_goal_choice()` returns None.** So routines are not
broken; they are starved of a goal to plan toward. This is F36's OBJ-binding starvation and the M2
WIRE (composed-OBJ→WANT firing 3/17 on ka59), now measured as the DIRECT cause of flat chunk reuse.
**The mapping lands here squarely: the answer keys ARE the objective compositions (the WANT)**, so
teaching the agent to form confident objectives from the human panel is what would make `_goal_choice`
return a slot, let a routine form, and let chunks compound. The lever is objective FORMATION (the
pretraining), one level up from routine mechanics. Diagnosis only; the fix is training plus possibly
the M2/OBJ-binding path in the betting loop, which is a scope call not yet ruled.

**CORRECTED ONE LEVEL DEEPER (F174, 2026-09-17): NOT binding starvation — objectives bound but not
SHRINKING.** F173 read the refusal as OBJ-binding starvation (F36); the reviewer flagged that the
string `no objective is confidently shrinking` does not distinguish *zero objectives bound* from
*objectives bound and none shrinking*, and a run splits them. Measured (`_goal_choice` instrumented,
ls20 offline, 51 None-returns): **28 are bound-LONG-but-FLAT (55%)** — objectives ARE bound, tracked
with a long-enough series, residual flat; only **7 are zero-bound starvation (14%)**; 8 diverging, 8
warmup; and `_goal_choice` DID return a slot 12 times. So the agent forms objectives and cannot make
them shrink — it cannot find actions that reduce a goal it holds. **By the criterion, that means the
curriculum is aimed correctly:** chunking-as-RL trains exactly the pattern "form an objective, act so
it shrinks." **F134 FIREWALL (binding, per the reviewer):** the answer keys shape the LEARNER only —
the trained pattern, off-line; at runtime the agent forms its own objectives from what it perceives
(`_goal_choice` reads `self._res`, never a key), and no answer-key artifact is ever loaded into the
run path (CUE_BOUNDARY plus that rule is the firewall). The key that touches a live `_goal_choice` is
F134 and forbidden.

**AND WHY REDUCIBILITY IS A RUN QUESTION, NOT A MAPPING ONE (F176, 2026-09-17).** The reviewer's next
read — are the 28 flat objectives REDUCIBLE (some composition would shrink them) — was run as
"does the answer key change the attribute each flat objective targets," and it came back CONFOUNDED:
the human panel changes all 8 object attributes on 23 of 25 games (7 on the other 2), so every
objective attribute is trivially in the set and the measure reads ~100% by base rate. That is the
THIRD instance of one ceiling — CI-2's adjacency, chunk-recurrence, now this: **the answer key is
coarse (9 atoms, 8 attributes) and the agent's objectives are fine-grained (a specific object, a
specific value in a direction).** But the deeper reason the key cannot answer it: **the agent forms
its OWN objectives at runtime (the F134 firewall), so their reducibility is not a fact about the
HUMAN's solution** — the human solved via their goals, the agent holds its own. Reducibility is
therefore a RUN question, and the run already partly answers it: of the `_goal_choice` outcomes, 12
returned-slot (reducible AND found), 8 diverging (residual worsening under action — mis-formed
objective or wrong action-model, unconfounded), and 28 flat (ambiguous: reducible-but-unfound vs no
observed action moves it). Disambiguating the flat needs a run-based coverage test (does any observed
action move the slot), or the training itself. **So the scope question — curriculum lever vs
refinement of the wrong thing — is settled by the RUN, not the mapping; the mapping side has reached
its measurement ceiling here.**

### The hard perceptual-reach gate

`ATTRIBUTE_REACH` grounds **only 11 atoms today**; ~1,749 unlock with a single scalar-emitting
sensor. **THE KEY IS WRITTEN ONLY IN WHAT THE AGENT PERCEIVES TODAY (reviewer, 2026-09-14):** the
five attributes and one relation, full stop. A reward that references a cue the agent cannot
perceive is constant no matter what the agent does — no gradient, teaches nothing. **And a chunk
that cannot be written in current perception is THE FINDING, recorded as inexpressible — never a
reason to add perception.** The moment the key reaches for a relation to make a chunk work, the key
is deciding what the agent gets, which is the thing the plan forbids.

**But the gap is logged, not discarded (Isaiah, 2026-09-14).** When a chunk won't fit current
perception, record it as inexpressible **with what it would need** (which attribute, relation, or
sensor). Those gaps accumulate across games into a **demand-ranked list**, and a perception change
is earned by **cross-game demand** — the same breadth counter as promotion and demotion, now on a
third axis. One game never decides a perception change; repeated demand across many games earns it,
which is the tenth-sense licence (*repeated demand across different situations*) applied to
perception. So the answer key stays inside today's perception, and the accumulated demand list is
how we later know what perception is worth building — never one game reaching for it.

**Two nuances that make the tally earn something rather than just accumulate (Isaiah, 2026-09-14):**

- **Count games, not chunks.** Eleven chunks in one game is *one game* demanding a cue; six games
  demanding the same cue is what crosses the threshold. The chunk count is useful for *sizing* the
  demand; the **game count** is the unit that earns a change — the per-game-not-pooled rule applied
  to demand.
- **Gap and fix are SEPARATE FIELDS: the gap is evidence, the fix is a hypothesis.** *"This chunk
  needs a relation between two objects"* is the gap — the evidence that accumulates, and the thing
  the list **ranks on**. *"This needs `touching()`"* is a per-instance fix hypothesis, logged in
  its own field and **never ranked on**. Separate fields keep the question open: the gap
  accumulates across games, and when the game-count threshold fires, the fix is **re-derived from
  all the accumulated instances, not taken from the first one.** So the ranked list is a build
  queue, but its specification is derived from the full evidence at the moment it is earned —
  never rubber-stamped from game one's guess.

### Relations and arity (`NSM_GRAMMAR.md`)

Chunks will involve two-object relations (`contains`, `blocks`, `touches`) that the current atom
signature — one slot in, one out — cannot bet on. NSM grammar is the spec'd route: a **frame holds
the arity, the atom fills a slot**, and the seven operators are NSM's connective family. Relevant,
but a **spec, not built**; it flags `TRUE`, `CAN`, `KIND` as zero-atom gaps — `TRUE` the sharpest,
since the whole loop turns on *the ground settled it* and no atom names it.

### Reference

`docs/library-closure/` is the ~2,700-atom visible set the agent reaches for (not loaded):
`ATOMS.md` (master list), `WORKING_SET.json` (the composer's working vocabulary), plus
`OPERATORS` / `RELATIONS` / `CHEMISTRY` / `ADJACENCY` / `ATTRIBUTES` / `ATTRIBUTE_REACH` /
`ATTRIBUTE_CLUSTERS` / `CATEGORIES` / `ENTRY_CATEGORIES` / `COMPOSITE_REACH` / `TRAVERSAL` /
`NSM_GRAMMAR`, and the `ATTRIBUTE_*` / `ADJACENCY_EDGES` / `CHEMISTRY_INSTANCES` / `ATOM_RANKING`
JSON indexes. `PERCEPTION_PIPELINE_general.md` and `ARC GAMEPLAY - WHAT THE AGENT SEES.md` specify
the seven-layer perception the "pretend to be the agent" step must use.
