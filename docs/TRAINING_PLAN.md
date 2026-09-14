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

Build a task generator over the **same substrate the agent already perceives**: objects,
attributes (position, colour, extent, shape), relations (same, other, above), the seven actions,
the same partial observability. Thousands of tasks; none an ARC game fed as an answer.

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
- **The public set** (source of record: https://arcprize.org/tasks?v=3): 21 slugs extracted —
  `ar25 bp35 cd82 cn04 dc22 ft09 ka59 lf52 lp85 ls20 re86 sb26 sc25 sk48 sp80 su15 tn36 tr87 tu93
  vc33 wa30` — with ~101 human-panel replays at `arcprize.org/replay/<uuid>`. The 25/25 ablation
  gate is these public games each carried to WIN.
- **Why one-at-a-time with carry-forward:** it is the single-agent substitute for generations. The
  library accretes across games (settled / unsettled / cache), so the Nth game is approached with
  everything the first N−1 left behind — transfer *within* the public set, and the rehearsal for
  transfer to the private set.
