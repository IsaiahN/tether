# ARC agent — build plan

Branch `arc-agent`. **Nothing is built until Isaiah says so.**

Companion to `ARC_AGENT.md` (§1–22, the design and the salvage), `THE_FORMULA.md`, and
`BUILD_PLAN.md` (the core build, already done).

---

## 0. Two questions answered first, because they change the plan

### 0.1 Is "humans beat a level in 50–70 moves" useful *to the agent*?

**Yes — as a rank signal, never as a filter.** And the distinction is Figure 9's: *use filters
for the budget and witnesses for the verdict; never let a filter hand you a verdict.*

**Why it is legitimate at all.** It is not a fact about any game — it is a fact about **the
benchmark's design**: these are built to be solvable by a human in tens of moves. The private
set is designed the same way, so it transfers by construction. That makes it a prior in the
exact sense §12 defines: knowledge available before evidence, and not an encoded answer.

**Two uses, one safe and one not:**

| use | verdict |
|---|---|
| **prior on plan length** — shorter routines rank first | ✓ safe. A soft, reversible ranking, and it is precisely what §19.7's missing rank function needs |
| **hard cap on routine length** | ✗ **a wrong cut removes the answer and speeds up.** A level needing 60 becomes unreachable and reports as unreached |

**And a second use worth having: the agent's own alarm.** At 300 moves on a level a human
clears in 50, the agent can *know* it is off track — which is uncertainty monitoring (Tier-1
prior 8) firing on an external reference rather than on its own confidence. The response is
generic and encodes nothing: **re-segment, escalate the ladder, or abandon the live hypothesis.**

### 0.2 Should the agent simulate?

**Yes, and exactly as far as its model has earned — which is a reading, not a setting.**

The trade is obvious: actions are the scarce resource, compute is not.

**And Γ does not start empty** (§23) — it ships loaded with the six loadable prior shapes. So
simulation is useful from step one, not as a *predictor* of this game (general priors do not
know what `ACTION5` does here) but as a **hypothesis generator with a better-than-random
prior**, which is exactly what ranking needs. What stays unearned is accuracy about *this*
game, and that is what the fidelity gate below measures.

**The gate is measurable and self-calibrating.** The divergence between a simulated outcome and
the actual one **is a residual** on a channel we do not currently read. So:

```
sim_fidelity  =  1 − (simulated vs actual residual, EMA)
lookahead depth grows as fidelity rises;  starts at 0
```

No magic number, and it fails safe: a bad model simulates one step and is immediately
corrected.

**And it lines up with the human phase structure (§22.2):** humans imagine more in later phases
because their model is better. Lookahead ≈ 0 in the random phase, 1–2 in directed, deeper in
strategy. **The same curve, from the same cause.**

**One discipline, and it is the third time this rule has appeared:**

> **Simulate to *rank* candidate routines. Never to *settle* one.**

Proposer: proposes, never scores. Retrieval: retrieves, never settles. Simulation: ranks, never
settles. **Only the ground settles** — and a plan that looks good because your own model says
so is the horse describing itself.

---

## 1. What this is built toward — and it is not a win

`abort_code.py` already states the right bar, and it is far short of winning:

> **ONE firing of the whole loop: a task fails → an operator is minted from the residual → that
> operator is **reused on a task it was not minted for** → the reuse clears a break.**

Two readings are available even before that, and both are readable without any win:

| | reading |
|---|---|
| **the stage code** | how far down the chain the stall got — and *only* `MINTED_UNUSED` indicts the architecture |
| **the phase histogram** | random → directed → strategy, and whether phase 1 shrinks across levels (§22.2) |

**Target for the whole plan: a run that produces both readings honestly, on a real game.**
Winning is downstream of that and is not the deliverable.

### And what an ARC result can and cannot test — stated before the run, not after

`DISCOVERY` Q27 tiers domains by the quality of their anchor, and the tier decides what a
result means:

| domain | anchor | quality |
|---|---|---|
| an interpreter, a proof checker | does it evaluate correctly | **near-perfect** — mechanical, instant, unarguable |
| **a rover, a game, a puzzle — ARC** | did it reach the goal | **good** — sparse, slow, does not negotiate |
| "is this a good answer for a person" | human judgment | **poor** — it updates, which is Figure 2 collapse 1 |

> **A crisp-ground domain tests the MACHINERY. A poor-ground domain tests the ALIGNMENT
> CLAIM. Doing both at once teaches nothing about either.**

**`snaps` is the top tier** — exact match on the next state, mechanical, instant,
constitutive. **ARC is the middle.** So the ARC run is a step DOWN in ground quality and it
**tests machinery**, which is the correct order Q27 prescribes: prove the loop where the
anchor cannot be talked to, then move outward.

**The consequence to state now:** a strong ARC score is evidence about the machinery and
**is not evidence for the alignment claim, which is the project's stated goal.** That
misreading is available to any reader and to us, and it is cheaper to head off here than to
correct in a write-up.

**But the alignment claim does NOT need a poorer ground, and a first draft of this section
said it did.** Alignment here is triangulation: **the system shows its reasoning, the human
shows theirs, neither is the anchor, and the ground settles it.** A disagreement then has
exactly two causes -- **the human holds context the library does not** (an import: name what
is missing and supply it) or **something else is weighting the decision**, risk or reward or
the cost of being wrong, which is **not a disagreement about the world** and was never
derivable by the system. **Both are locatable only if the reasoning is legible**, which is
why a black box leaves only override or defer, and neither is alignment.

**So what the alignment claim needs is not a POOR ground. It is a ground THE AGENT CANNOT
SEE**, scored over **the agent's report rather than over its answers** — and that is a
weaker requirement, already implemented:

    unreachable in fact  : ['opaque']   (harness knows; the agent is not told)
    agent abstained on   : ['opaque']
    correct abstentions  : 1/1        FALSE abstentions : 0/6

**`demo.py` runs it today** on a top-tier ground. **The missing domain is that arrangement
at scale — withheld ground, report-scored — which is buildable and much smaller than a test
of values.**

### And the second thing the ARC move gives up, which is not the tier

`ARC_AGENT` §5: **Stage 2 gave slots BY NAME on purpose** — *a gridworld tests perception
and the loop at once, which is two experiments in a trench coat* — **so that a failure was
unambiguously a LOOP failure.** That was a designed property, bought by refusing a
perception layer.

> **ARC removes that choice. Slots have to be found.**

**So the move does two things at once, and they are independent:** a tier down in ground
quality, **and the perception confound reintroduced.** An ARC failure will not be
unambiguously a loop failure — it may be a segmentation failure wearing one.

**This is a designed property being given up, not a limitation being accepted**, and the
difference matters for how a null reads. **State it before the run**, for the reason the
tiering is stated before the run: **a caveat that arrives after a result reads as
excuse-making, and the identical sentence written beforehand reads as design.**

**And one mechanism changes disposition on the way in.** `R_T` has produced **zero readings
in this repo, ever** — `world` supplies no `transform()`, and `snaps`'s domain sweep needs
16,807 against a 4,000 budget, so every reading is the capped case. **In ARC it is
`logical_grid`'s admission criterion**: commit to a detected board only if the round trip is
near-lossless, `None` otherwise, with `1 − fidelity` as `R_T`. **That is a fidelity number
over a detected grid, so the reason it is unmeasured here does not apply there.** It moves
from *a mechanism that has never measured anything* to **a mechanism whose first real
reading is in this build**, and those have different dispositions.

### How the test works, and what it establishes  ·  `[I]`, 2026-08-27

**THE TEST IS NOT THE SCORE.** A zero can mean the theory is wrong, **or four wiring
defects in sequence.** §22.6 says it plainly — *a wiring gap gets written up as a theory
failure* — and that is what happened to `g7` for a month.

> **So the deliverable is the score PLUS a chain that says where it stopped.**
> `RESIDUAL_EMPTY` indicts perception. `MINTED_UNUSED` indicts the architecture.
> **Same zero, different verdicts, and only the instruments separate them.**

**And the narration is what makes a loss legible.** A failure that names the step — *ROUTE
sorted this into mechanism when it was rebinding*; *the mint offered nothing and SUPPORT was
the zero* — is a finding. A failure that says *it did not work* is not. **That is why the
whitebox requirement was never a constraint on winning: it is what makes the result mean
something either way.**

#### The ablation, and what it isolates

**Wipe the learned library. Keep the ability to describe.** §23.4's stratified clause
sharpened by §15.2 — the agent forgets these games and retains its priors, its primitives,
and its capacity to characterise a residual and search.

> **Which separates two claims that keep getting conflated: does this agent know these 25
> games, versus DOES THIS LOOP LEARN GAMES.** The first is worthless for the private set.
> The second is the thesis.

**Anything less than clean is diagnostic rather than a failure**, because the stage code
says where each one stopped.

#### The limit of that test, and how to answer it

**The agent forgets. THE ARCHITECTURE DOES NOT.** Every design decision that survived is one
that helped on these 25, so ablation shows the loop can **rediscover**, not that it
**generalises**.

**But if the theory is sound there should be very few decisions of that kind, and that is
COUNTABLE rather than a matter of confidence.** The distinction that decides each one:

| | |
|---|---|
| **a game showing you something is broken** | **legitimate** — that is the residual doing its job |
| **a game telling you what to build** | **the leak** |

**And the test is whether the fix generalises:** *bindings come from contact* is general;
*this game needs a wall detector* is not.

> **So the count worth running is: HOW MANY MECHANISMS WOULD HAVE BEEN BUILT THE SAME WAY
> WITH NO GAMES AT ALL?** If it is most of them, the architecture is derived and the
> ablation result means what we want it to mean.

**§13.4 already identifies the honest exceptions** — three archetype-derived files against
six domain-general, with the corpus flagging those three as the seductive ones. **Quarantined
rather than invisible, which is the right state for them to be in.**

#### The arbitration, and why the position is legitimate

**A human arbiter rules on gaps and exceptions**, because the corpus is a theory under test
and nuances may be needed.

**The corpus's own rule is that a maker checking their own work is the soundness condition
failing, so the position needs its warrant stated or the seat will notice the tension:** the
arbiter is **outside the slice being graded**, and the ground is **`levels_completed`, which
the arbiter cannot move.** That is what makes it sound rather than special pleading.

**Each exception is a ROW, not a judgement** — granted at the step that failed, with the
evidence that prompted it and **what would have shown it wrong.** A ruling carries provenance
so a later reader can locate the error rather than only feel it.

> **The failure mode to guard is the anchor updating on what the frame produced** — an
> exception granted because a mechanism failed and the theory feels right. **The narration is
> what makes that auditable afterward by someone who did not write the corpus.**

---

### Reconciled against `ARC-AGI-3-Agents` source, 2026-08-26

The repo is checked out now. It had been read second-hand from notebooks, and **two things
the plan relies on were wrong.**

**1 · `MAX_ACTIONS` is 80 in the base class, and this project defended 1000.**
`Agent.MAX_ACTIONS: int = 80`, commented *to avoid looping forever if agent doesnt exit*,
and `main()` enforces it as a hard loop bound. §22.1 defended **1000** on the basis
*humans complete a level in under 500 actions, so this is the 2× honest ceiling* — **a
legitimate anchor, external to the frame, for a number 12.5× the default.** A subclass
override is the mechanism (one in-repo agent sets `MAX_ACTIONS = 1000000`).

> **So the project must SET it deliberately and record the basis on the line.**
> Inheriting 80 silently is the failure; overriding to 1000 without recording why is the
> same failure wearing a decision's clothes.

**2 · The reasoning echo does not reach the live agent, and §3 assumed it does.**
§3 builds on *`frames[i].action_input.reasoning` returns what was attached to the action
that produced frame `i` — the agent can read why it did each past thing from the
environment's own record of it.* **`_convert_raw_frame_data` constructs `FrameData` from
eight fields and `action_input` is not one of them.** In the live loop `self.frames` are
those converted objects. `action_input` is read in exactly one place: the **`Playback`**
class, from a recording file.

> **The reasoning survives into the RECORDING and not back to the playing agent.**
> §3's *what appears in replays* holds. *The agent can read its own past reasoning* does
> not, through this harness — **and anything specified downstream of that channel needs
> re-reading against what exists.**

**And one that was right for a better reason than stated:** `agents/__init__.py` must be
rewritten not merely because it eagerly imports langgraph and smolagents, but because
**`AVAILABLE_AGENTS` is built from `Agent.__subclasses__()`** — a subclass must be
*imported* to register at all.

**Also corrected:** §1 says building against the toolkit's `step(reasoning=…)` signature
would not run on Kaggle. **The harness calls that signature itself** —
`self.arc_env.step(action, data=data, reasoning=reasoning)`. It wraps the toolkit rather
than replacing it. The instruction (attach to the action object) stands; the reason does
not.

### And one capability ARC GIVES, which must be labelled as borrowed

The move is not all cost. §21.1: everywhere else in this design the agent gets
**observational** data — it acts, the world moves, it reads the gap — and *correlation is
cheap; causation is not, **because you can never re-run the same moment.***

**A level-resetting loss breaks that, and it is the only place in the whole loop where a
controlled experiment is available:** same starting board, vary exactly one action, observe
the difference. That is *disambiguating intervention* (Schulz & Bonawitz) and causal
structure learning from intervention (Gopnik) — the machinery that separates `A→B` from
`A and B co-occur`.

> **But its precondition is that THE GAMES ARE DETERMINISTIC, which is a property of the
> domain and not of the design.**

**So label it borrowed.** The only controlled experiment the agent can run is a gift from
ARC, and **it evaporates in any domain that is not deterministic.** A capability that
depends on a domain property must be marked as such **before anything is built on it as if
it were structural** — otherwise the next port silently loses causal inference and nobody
knows which assumption went missing.

### And the shadow test, turned on this project's own choice of ARC

`DISCOVERY` Q26 closes the eight-slot contract by applying the framework to its own porting:

> **Was there a residual in this domain already unexplained that the framework predicts, or
> did we go looking for somewhere to put it? Echo without shadow is apophenia, INCLUDING
> when the thing being ported is this framework.**

**Answerable, and not answered in writing.** It is the first question a reviewer asks, and
having the corpus ask it is worth less than having it answered. **Answer it before the run,
for the same reason as the tiering above.**

**One negative result belongs with it**, per `PHILOSOPHY` §15's instruction that it travel
with the hypothesis rather than behind it: **ARC game-shapes do not predict solving
primitives, measured three ways.** That gate came back negative. §15.3's retrieval keys on
**residual shape** rather than on game, which is exactly what the negative implies — so the
design already complies, and **a design choice separated from the evidence that forced it
reads as a preference.**

---

## 2. The organizing principle, which already worked once

`BUILD_PLAN`'s stage 0 built the gate *before* the loop it gates, and it paid immediately —
the gate refused the loop three times, two were real defects, and one was a defect in the gate.

**Same principle, one level up: the instruments go in before the ARC adapter**, so the first
run against a real game is readable rather than a pile of logs someone has to interpret
afterwards. That means the stage code, the phase labels and the two clocks land in Phase 1,
before anything touches the API.

**And the corollary from the salvage hunt:** six of eight gaps were solved somewhere already.
Most of this plan is **integration, not invention** — the exceptions are called out.

---

## 3. Phases

### Phase 0 · Fix the core — domain-agnostic, testable on the toy world

Four defects in the existing build, all found in §14/§17, all fixable before ARC is involved.

| | fix | why now |
|---|---|---|
| **0a** | **operand arity** — terms read N slots, not one (§17.1) | without it no interaction is expressible, and interaction is most of ARC. Copy `dsl.py`'s N-slot Context, **cap 4, quartic cost stated** |
| **0b** | **chunking** — `enumerate_closure` seeds and extends from *settled* library terms, not just atoms (§14.1) | the library currently grows while the reach does not |
| **0c** | **demotion** — a settled term that fails on fresh evidence is demoted to candidate; defeasible, clocked (§17.2, §18.2) | copy `falsified_ledger`'s shape: weighted, decaying on a **logical** clock, **express-before-judge** |
| **0d** | **verdict decomposition** — `NO_SUPPORT / NOT_NOVEL / BUDGET_SPENT / DEPTH_EXHAUSTED / UNREACHED`, each with **coverage = seen / λ^d** (§19.1) | `unreached` currently conflates "I stopped" with "it is not there" |

**Done when:** the toy world still passes the gate, `test_gate.py` still passes, and a planted
two-slot interaction rule (new toy slot: *B follows A*) is minted — which 0a makes possible and
which is impossible today.

**Falsifier:** if the two-slot rule still cannot be minted, arity was not the blocker and the
diagnosis in §17.1 is wrong.

---

### Phase 1 · The instruments, before the adapter

| | build |
|---|---|
| **1a** | **the stage code** — the seven-stage chain, per segment, never cumulative (§18.1) |
| **1b** | **phase labels** — every action tagged probe / directed / strategy; the histogram over time (§22.3) |
| **1c** | **two clocks** — steps-to-model (transition-residual EMA) and steps-to-win, reported separately (§22.5) |
| **1d** | **the sweep** — on every accept, re-run the new term against outstanding parked residuals; a retroactive resolution is recorded, and **it is reuse** (§19.5) |
| **1e** | **gate checks added**: an `UNREACHED` with no coverage is refused; a sensor reading may never be cited as a settle event (§13.3) |

**Done when:** the toy world's run report prints a stage code, a phase histogram, both clocks,
and at least one retroactive resolution.

**Falsifier:** if the sweep never fires on the toy world, either nothing is being parked or
nothing minted later is general — both are findings, and both need to be looked at before ARC.

---

### Phase 2 · The ARC adapter and perception

| | build |
|---|---|
| **2a** | `arc_world.py` — the eight members over `arc_agi` **OFFLINE**. Ground = `levels_completed`; degree = `levels_completed / win_levels` (§20.2); board = `frame[-1]` |
| **2b** | **perception** — connected components as slots, tracking by overlap, death only on evidence (`perception.py`'s shape) |
| **2c** | **the four cheap sensors** — action-set delta, precondition edges, control mode, affordance profile (§16.8) |
| **2d** | **termination class** — latching, positive-evidence-only; report `OPEN` as an assumption (§20.1) |
| **2e** | **event types** — WIN / DEATH / LEVEL-RESET / LEVEL-ADVANCE / CAP, distinguished. **Reset vs advance inverts the meaning of a residual spike** (§21.5) |

**Done when:** the loop runs a real game offline, the gate passes on its ledger, and the run
report names the termination class and the event that ended it.

**Falsifier:** if slots are unstable across frames — ids churning every step — tracking is
broken and everything above it is noise. Check this *first*, per §17.6.

**Note:** control mode is a **family** of self-hypotheses, not one correlation test. A single
translation detector was measured at `has_self: false` for 904 steps (§18.3).

---

### Phase 3 · Sensors and the three composition spaces

| | build |
|---|---|
| **3a** | the **nine minimum sensors**, typed, total with `NOT_RESOLVED`, priced (§12.3) — then **load generously** across the six loadable shapes, all stamped `prior`. **No routines** (§23.2) |
| **3b** | **EXTRACT / RELATE / PREDICT** as typed families; report `λ` — and here the type graph is genuinely sparse, so the number should finally mean something (§11.3) |
| **3c** | **retrieval by characterised residual** — indexed by type signature, arity, invariants, effect shape. Full library, no gating (§15.3). **PREREQUISITE, not a follow-on**: a loaded Γ raises `λ`, so enumeration order drowns the search and manufactures false `UNREACHED` (§23.5) |
| **3d** | the **rank function** — cost, reuse count, type-match to the residual, recency; **plus plan length prior** (§0.1). Ranked cuts, reversible, recorded |
| **3e** | **the four imports** available from the start — `bfs_dist`, second moments, global transform, Levenshtein. **Retrieval is by residual, not by name** |

**Done when:** `λ < V` is reported with a real ratio, and a sensor is minted by the
discriminability trigger — two slots with the same attribute vector and different residuals.

**Falsifier:** `λ ≈ V` again means the type families are not sparse and the design is wrong,
not the number.

---

### Phase 4 · Routines and simulation

| | build |
|---|---|
| **4a** | **six NSM primes** — `DO`, `MOVE`, `HAPPEN`, `IF`, `BEFORE/AFTER`, `FOR SOME TIME` — into the existing basis. **One grammar, not a bolted-on combinator language** (§15.5) |
| **4b** | routines priced by the **goal residual**, same bargain, one level up |
| **4c** | **Γ as simulator** — roll forward a candidate routine before committing; depth gated by measured `sim_fidelity` (§0.2) |
| **4d** | **lag as a priced parameter** — `+log₂(k+1)` bits, tested by the sweep machinery (§19.4) |
| **4e** | **level-reset as controlled experiment** — same board, vary one action. Deliberate death legal **only with `expect` and `disproof` stated first**; publish the budget fraction spent on it (§21.2) |

**Done when:** a routine is composed, simulated, executed, and settled — and the stage code
reaches at least `REUSE_UNWIRED`.

**Falsifier:** simulation fidelity that never rises means Γ is not a model, whatever the mint
log says.

---

### Phase 5 · Kaggle

| | build |
|---|---|
| **5a** | `build_notebook.py` — inline the core into one `my_agent.py`, emit the `.ipynb`. **Generated, never hand-edited** |
| **5b** | the harness bridge — `MyAgent(Agent)`, `choose_action` returns what the utterance proposed **or no action** |
| **5c** | the reasoning digest — ≤ **16 KB**, with `expect` and `disproof` stated *before* the action (§3) |
| **5d** | the rerun scaffold — gateway wait, `agents/__init__.py` rewrite, `.env`, submission parquet |

**Done when:** it runs end to end in a Kaggle rerun and the reasoning appears in the replay.

**Falsifier:** `gate.py` must still import nothing after inlining. If the inliner wires it to
the loop, the soundness argument is gone.

---

### Phase 6 · Swarm — deferred, with a stated reason

Not a roadmap slot: **it is the only channel that opens the peer frame** (§15.1). The game
gives imports from *nature*; only another agent gives a different closure to triangulate
against.

**Blocked on one thing first:** `GameAction` enum members are process-wide singletons and the
samples mutate them (`action.reasoning`, `set_data`). Threaded swarms will clobber each other,
and it will read as a reasoning bug rather than a race (§8).

---

## 4. Not built, deliberately

Step 6 PROMOTE · the tiny proposer (a training artefact plus a loader — **if removing it breaks
the loop it stopped being a proposer**) · a substance taxonomy of objects (affordance profiles
instead, §16.4) · `ProgressProbe` as anything but a sensor · any of `relation.py`'s five
relations, `referent.py`'s detectors, or `operator_effect.py`'s framing — **archetype-derived,
selection against the public set** (§13.4).

---

## 5. Rulings needed, and when

| stage | ruling |
|---|---|
| **0** | arity cap — take `dsl.py`'s measured 4, or lower for budget? |
| **0** | demotion clock unit — in an open game the epoch is the generation (§20.5). Confirm |
| **2** | library persistence: **carry across levels, cold across games?** This is what the ablation clause tests (§17.8) |
| **3** | how much to load, and from where — the 130-prior catalogue is the source, the six shapes are the filter (§23.2) |
| **4** | is deliberate death acceptable at all, given `bounds.py`'s history? My read is yes with the gate check; it is your call |
| **5** | Kaggle submission schema — the samples disagree; verify against the competition page |

---

## 6. How this fails

- **The instruments get skipped** to "get to the game faster", and the first ARC run produces
  logs nobody can interpret. This is the failure the whole plan is ordered to prevent.
- **A wiring gap gets written up as an architecture verdict** — which is exactly what the stage
  code exists to stop, so if the stage code is not in first, this happens by default.
- **Priors get installed because they would help**, and minting never fires. The ablation clause
  is then unable to tell us.
- **The rank function becomes a filter** and manufactures false abstentions, corrupting the one
  metric the product rests on.
- **Simulation gets trusted** and the agent settles plans against its own model.

---

## 7. Size

Core is 1,481 lines today. Phase 0–4 should land under **3,000 total**, and if a phase pushes
that the design is wrong rather than the estimate. `dsl.py` alone is 1,093 lines and is the
cautionary example: the mechanism in it is excellent and the file is three times the size the
mechanism needs.

---

# Reconciliation — where this plan is now wrong

Written after a long session on the kernel, and read against the plan afterwards rather
than during, which is its own finding: **`BUILD_PLAN.md` and this file were not consulted
while the work was done.** What follows is the diff.

## Phase 0 — three done, one HALF done and the half matters

| | state |
|---|---|
| **0a** operand arity | **HALF.** `Term.operand` is `str | None` and `_ops` returns `(state[term.operand],)` -- **arity ONE, not N with cap 4.** An interaction reading two other slots is still inexpressible, and the plan's reason for 0a is unchanged |
| **0b** chunking | done. And its dedup was WRONG: `units()` keyed on `t.name` (which carries the operand) while emitting `Term(t.atoms)` (which does not), so two settled terms differing only in binding became one unit counted twice -- inflating `space_estimate`, the denominator of `coverage` on every mint row. Fixed. Latent: it had never fired |
| **0c** demotion | done -- weighted, decaying, express-before-judge |
| **0d** verdict decomposition | done -- `no_support / not_novel / budget_spent / depth_exhausted`, each with coverage |

## Phase 1 — done, and 1c is superseded rather than complete

**1c says steps-to-model is a transition-residual EMA. The EMA is gone.** REPAIRS 1 deleted
`ALPHA`, `EPS` and `WARM` because SUPPORT is `|R+_s| > 0 for SOME slot s` -- a PREDICATE over
slots, not a magnitude averaged across them, and averaging is how a live signal disappears.
`steps_to_model` is now *no slot owes*.

**1b landed and was then repaired:** the phase is read off `by`, the site that chose the
action, rather than asserted alongside it. It used to be `DIRECTED if a term is bound`
attached to an action drawn by the identical mechanism either way -- a label the mechanism
could not make.

**1d landed** and now also licenses promotion.

## §0.2 · `sim_fidelity` would reintroduce exactly what REPAIRS 1 removed

    sim_fidelity = 1 - (simulated vs actual residual, EMA)
    lookahead depth grows as fidelity rises

**That is a threshold on an average across slots**, which is the construction deleted from
`probe.py` for the reason above. The section calls it *no magic number*, and the EMA weight
and the depth schedule are both magic numbers. **Needs restating as a predicate before it
is built.**

## §4 · "Not built, deliberately: Step 6 PROMOTE" — it was built

Shadow-then-echo, on this session's instruction. What happened, in full:

- it FIRES on a ladder -- 6 and 9 promotions over 12 seeds, mostly cross-level -- which
  overturned an earlier null measured on a single-level panel that had nothing to echo
- it **failed its own prereg**: `lib ok here / lib` did not move
- its unpredicted side effect **failed replication** on held-out seeds: claims 57→48 became
  54→53, and the rate difference pooled to 1.3 SE
- the boundary revert cost opportunity, uptake and carried in **both** panels, so it was
  removed; `promote` and the PROMOTE rows stay, because they record something real

**The plan should say `attempted, negative, mechanism retained` rather than `not built`.**

## §5 · The stage-2 ruling is answered by measurement

> library persistence: **carry across levels, cold across games?**

The boundary revert IS that question at the level boundary, and it was measured on two
independent panels: **reverting cost transfer in all three numbers with nothing measurable
bought. Carry.** The cold-across-games half is untouched.

## Phase 2 — its falsifier cannot fire as written

> if slots are unstable across frames — ids churning every step — tracking is broken

**Sharper, and worse:** `self.slots = env.slots()` is read at construction and at retarget,
nowhere else. A second object appearing mid-episode produces **no bet, no residual and no
row** -- invisible rather than an error, so there is nothing for the falsifier to see.
Cells never do this and objects always will.

**And 2b's `connected components as slots` inherits the loud/silent split.** An
object-level view of a sub-object rule read **zero residual for twenty steps** -- the agent
believing it had explained a world still moving underneath it. Worse than a narrowing that
drops a candidate: that excludes a term which would have been tested; this excludes the
observation. `never_live` is now built as the detector, and the utterance can say it.

## Phase 3c IS the effect-index, and A1 had to come first

Scoped: extension collapse 6.3x at depth 3, retrieval 4.7% of the closure -- **~19
candidates where the mint walks 1945.** A decomposition rather than a constant.

**It materialises the closure, which is A1** -- and A1 was STRUCTURAL and unchecked in both
seats. The check was therefore built FIRST, written to the property rather than the proxy:
*`accept()` is the library's only writer* and *`enumerate_closure` is the only producer of
reach*. It permits a memo of the generator and forbids a second producer, tested against
the real code. **Writing it after the index would have graded the index with a rule shaped
to fit it.**

## Phase 3d and §6 · "the rank function becomes a filter" now has a test

Measured on 407 mint calls:

    a narrowing derived as a NECESSARY CONDITION from the residual   0 terms lost
    a narrowing reasoning about what OUGHT to be relevant            lost a closing term

**That is the test.** Not the wording -- whether the exclusion can be stated as *this
provably cannot satisfy R* rather than *this probably is not needed*. The residual bound
built from the first form is 6.7x less work with nothing lost.

## §7 · Size

    core (loop and its parts)   2,181     plan baseline 1,481, Phase 0-4 target 3,000
    conform/ (the checking)     2,156     did not exist when this plan was written

Core has headroom. **The checking layer is not in the plan's budget and is now comparable
in size to the thing it checks** -- which is a decision to make explicitly rather than
discover.

## Not in the plan, and now needing slots

- **motor skills** -- positioned actions and intentions. The read is in `ARC_AGENT.md`, and
  the conclusion is that this is KERNEL work: `drive.choose` sorts the action set, so a
  positioned action cannot be added from outside, and no `tether` row records which action
  was taken
- **per-slot alphabets** -- built. A boolean was charged log2(7); it blocked measuring any
  view change in either direction
- **the interface question** -- regrouping, not resolution. `transform()`/`R_T` is the wrong
  socket for it, and snaps cannot answer it because M is prime

---

# Second pass — against `DISCOVERY.md` and `PHILOSOPHY.md`

**Read:** `DISCOVERY.md` §0–5 index and Q14, Q18, Q19, Q26 in full. `PHILOSOPHY.md`
headings, §8's audit table, §16.1 and §16.8. **Not read:** PHILOSOPHY §0–7, §9–13, §15,
§17+; DISCOVERY's remaining question bodies. The claims below are scoped to what was read.

**The vintage rule applies throughout:** both documents predate REPAIRS, per-slot
alphabets, the residual bound, the A1 check and the whole conform layer.

## Q19 is SETTLED and the session built against it twice

> **only when the round trip is near-lossless. `R_T` gates the abstraction; keep the
> original either way**

    ruling                                      what was built
    the lens is ADDED, never substituted        `self._view` SUBSTITUTES the reading
    keep the original either way                the full reading is not retained alongside
    R_T is the ADMISSION CRITERION              R_T is a row, and gates nothing

**Both are real and both are mine.** The bracket build reports `R_T` where the ruling says
it must refuse the coarser vocabulary when the gap is not near zero.

**The measure itself is NOT in conflict, and §16.1 is why.** `R_T = gap(x, (T_E∘T_A)(x))`
with the extensive law guaranteeing the sign, and: *the general statement should be the
order relation, because that is what guarantees the sign* -- with `logical_grid.fidelity`
named as the concrete-metric case. **The pre-image form is the general one the corpus
asks for.** Arrived at independently, which is the only good news in this section.

**And Q19 carries the calibration story that should govern the gate.** ls20's true grid is
5px at fidelity 0.818; the only tiling passing a 0.93 gate is a *spurious* one at 0.946.
**A plausibly-tuned gate commits confidently to the wrong grid.** The gate was set to 0.98
so it would abstain, and the stride was recovered from a different instrument. `0.98` is
called the one constant in the tree with exemplary provenance, and the template for Q14.

## Q18 is the motor question, already numbered, and it breaks `never_live`

> re-probe any action still unmapped **from a different cell** each time — because an
> action can look inert merely from having been tried twice against a wall. **Inert is a
> verdict earned by trials, never assumed early.**

`never_live` requires *every advertised action drawn*, and `Drive.tried` is a
`set[str]` -- **action labels, with no record of the state they were drawn from.** Drawing
`A` three times from one state counts as tried. **That is precisely the defect Q18 names**,
in the clause added specifically to make the evidence positive rather than absential.

The fix is stated in the ruling: `tried` keys on `(action, state)`, and inert is earned by
trials from different states.

**And Q18's larger half is unbuilt:** coverage-first as a PHASE, with goal pursuit gated on
a complete action map. The loop has no such ordering.

## §16.8's margin — measured, and it would make things worse

> a strict inequality with no margin accepts terms that clear by a fraction of a bit,
> which on finite evidence is overfitting

`pays` is `cost + left < base`, strict, and its docstring calls that a feature. So the gap
is real as stated. **But it is not the explanation for this project's false mints, and a
margin applied here would hurt:**

    correct  n=14   slack over the bargain: min 0.27  median 1.36  max 1.72 bits
    WRONG    n=13   slack over the bargain: min 1.36  median 1.72  max 3.80 bits

    mints clearing by under 1 bit:        3/27
    WRONG mints clearing by under 1 bit:  0/13

**Wrong mints clear by MORE than correct ones.** A one-bit margin removes three correct
mints and zero wrong ones. The reason is legible: a wrong term that closes a narrow slice
is usually SHORT, so it clears widely; a correct term is often longer and clears narrowly.
**A margin selects for short terms, and short terms are the coincidental fits.**

**The code half of §16.8 is done** -- `CODE` is declared in `tether.py` and carried on
every mint row.

## §16.9 · the shadow test as pre-registration — matches what was built

> compare the sequence number of the residual against the sequence number of the import

The PROMOTE rows carry `recorded_before` = the term's accept `seq`, against a target
residual already on the trace. **No new mechanism required, as §16.9 says.**

## Q14 · one constants block — deviated from, with a reason, unrecorded

> One constants block, every entry carrying its mode and provenance. A number without a
> provenance tag does not go in.

Implemented instead as **per-site `# anchor:` comments enforced by a checker** (lint's
ANCHOR rule, witnessed). Defensible -- a checker enforces what a block only encourages --
but it IS a deviation from a settled ruling and was never recorded as one. **And Q19's
`0.98` is the standard both forms are held to: the provenance names the measurement that
forced the number, including the value that would have been wrong.** No constant in this
tree meets that bar.

## Q26 · eight slots, and the contract is ten

Sourced to `PHILOSOPHY.md` §14. `actions` and `alphabet` were added during this project
with a stated reason -- *the two the loop used to reach past the contract for* -- and
**the ruling was never revisited.** Either the table is ten and §14 needs amending, or the
two additions belong somewhere other than the binding table.

## Confirmed rather than conflicted

    Q7   held but not cited              cite/hold rows, built this session
    Q8   accumulated per slot            `_accumulated`, and no evidence-count gate
    Q15  the gate blocks from step one   pre-commit hook blocks; no shadow mode
    Q20  probe uninformed, own error     boredom refuses the model the wheel

## Third batch — PHILOSOPHY §16.2–16.7 and BUILD_PLAN §8

**§16.5 is the largest unbuilt item in the corpus and it is a test of the central claim.**

> Selecting the best 1 of `N` variants supplies at most `log₂ N` bits about the target.
> **Death → explanation**: the claim is that reading *why* it failed extracts more than
> `log₂ N` from the same `N` trials. **That is now a measurable claim** — count the bits the
> diagnosis actually resolves against the bits ranking alone would have given. **If the
> answer is `log₂ N`, the diagnosis added nothing and it was prose.**

`mint` selects one of `N` enumerated candidates, so `N` is on every mint row as
`candidates_seen`. **The test is runnable on the existing panel and has never been run.**
It is the closest thing in the corpus to a falsifier for the whole thesis, and it sits
unbuilt while four narrower hypotheses were tested this session.

**§16.3 · NOVELTY is a syntactic proxy and the corpus says so.**

    orthogonality(R, Γ)  =  H(R | Γ)  =  |R| − min_{φ ∈ closure(Γ)} |R|φ|

> `φ ∉ atoms(Γ)` is only a proxy for it

Which is exactly what `mint` implements -- `is_atom(term) or term.name in library`. Named
as a proxy in the corpus, implemented as the proxy, never recorded as one.

**And `density(R)` in the same table confirms REPAIRS 1 rather than conflicting:** *live
mass, per slot -- **not an average, averaging is the thing Figure 1 forbids***.

**§16.6 · `λ` is built, computed from the wrong table.** `gamma.type_report` builds the
transfer matrix from the ATOM set; §16.6 says *computable directly from `grammar.py`'s own
production table*. Same quantity, different subject -- and `grammar.py` is where the type
graph is actually sparse, so the number that would mean something is not the one being
reported.

**§16.7 confirms the Galois choice** -- *a bijection has neither branching nor
irreversibility; that is why a lossy Galois connection is the right model.*

## BUILD_PLAN §8 · the retrospective

**Confirmed, not conflicted:** *a term known-partial from birth is not eligible to settle.*
`candidates[term.name]` is written only when `closes` is true, so a pays-not-closes term
has no birth record and `settle` skips it. The rule is enforced.

**And the bracket claim originated here:** *the bracket channel is inert because this world
defines no coarse view, and the entry says that rather than omitting the channel.* **The
entry said it and nothing checked it** -- `env.transform()` was never called until this
session. The retrospective recorded the intent; the code recorded the assertion.

**Size, against the record:** 1,481 core at the 2026-08-22 build, target 1,500. Core is now
2,181 -- **47% growth** -- plus 2,156 in `conform/`, which did not exist.

---

# §16.5 run — the thesis test, and it does not discriminate

> *reading why it failed extracts more than `log₂ N` from the same `N` trials ... if the
> answer is `log₂ N`, the diagnosis added nothing and it was prose*

**The corpus states the claim and not the arithmetic**, so two formalisations were built
and both are stated, because a wrong formalisation makes the number meaningless.

## Reading A · bits per TRIAL

Ranking identifies one of N and **costs N trials** -- one variant run against the ground
each, which is the evolutionary reading. The mint identifies one of N while spending no
trials on candidates: it reads them against observations already paid for, so the trials
it spent are the residual's `|R|` observations, each carrying at most `log2(alphabet)`.

    27 closing first-mints, 20 worlds

                    N     log2 N   trials |R|   bits supplied   sufficient   saved
    correct       344       7.59          4.1           11.43        14/14      79x
    WRONG         326       7.27          3.7           10.37        13/13      82x

**Indistinguishable, and the wrong mints save marginally more.** The observations supplied
enough bits in every single case, including all thirteen that identified the wrong term.

## Reading B · bits actually RESOLVED

`log2(N) - log2(k)`, where `k` is the candidates still consistent with R -- the faithful
reading of *bits the diagnosis actually resolves*.

    11 closing first-mints, residual captured at the mint

                    N        k     log2 N   resolved   trials
    correct      1579     10.6      10.62       8.83      5.2
    WRONG        1192      2.2      10.22       9.58      4.3

**The WRONG mints resolve MORE.** A wrong residual narrows to two survivors; a correct one
leaves eleven.

**And the mechanism is already measured.** Extensional collapse is 6.3x at depth 3 -- a
correct term lives in a family of equivalent forms, so many survive; a wrong term is a lone
coincidental fit on a narrow slice, so few do. **A residual that looks more decisive is
more likely to be wrong.**

## What this settles, and what it does not

**It is not the falsifier for the thesis.** On both formalisations the diagnosis extracts
far more per trial than ranking -- roughly 80x -- so the efficiency half of the claim is
confirmed and was never really in doubt. **What the arithmetic cannot do is tell a
diagnosis that works from one that does not**, and on Reading B it is anti-correlated with
correctness.

**So `log₂ N` is the wrong axis for the question this project actually has.** The claim
§16.5 tests is *diagnosis is cheaper than selection*. The claim that matters here is
*diagnosis is RIGHT*, and bits-per-trial is silent on it by construction: a wrong answer
reached in four observations is cheap and wrong.

**Caveats, stated:** Reading B is n=11 and the direction is consistent with the n=27 null
and with the independently measured collapse, but it is a small sample. And both
formalisations are mine.

---

# Fourth batch — `ARC_AGENT.md` §17 and §19

## §19.1 · five verdicts, four built — and the honest one is missing

    NO_SUPPORT       already separate      built
    NOT_NOVEL        already separate      built
    BUDGET_SPENT     weak                  built
    DEPTH_EXHAUSTED  strong                built
    UNREACHED        reserved for AFTER escalation -- the honest claim    NOT BUILT

**And §19.2's escalation ladder is not built either:** re-rank (free) -> more budget
(linear) -> more lag (xk) -> more depth (xλ) -> more arity (quartic), **each rung a ledger
entry**, so a final `UNREACHED` means *I looked wider, later, deeper and across more slots,
and still nothing*.

**The agent reports `depth_exhausted` 1094 times out of 1157 mint attempts and never
escalates.** That verdict is accurate -- it did see the whole space at depth 3 -- but it is
the strong claim made at rung zero, and the corpus reserves the honest claim for after the
ladder. **97.5% abstention accuracy is measured over slots declined at depth 3 with no
escalation attempted.**

## §19.1 · the coverage denominator is the wrong quantity

> `estimated space at depth d ≈ λ^d` (the spectral radius)

`Gamma.space_estimate` computes `sum(units^d)` -- **`V^d`, not `λ^d`.** And `λ` IS computed,
by `type_report`, and used in exactly one place: a print in `demo.py`.

**So `coverage` on every mint row is a ratio against a denominator the corpus says is
wrong, and the number that would fix it is already computed and thrown away.**

Numerically identical here, because this world's `λ = V = 8` -- one type node, so the type
graph is not sparse. **It diverges the moment it is**, which §16.6 says is exactly what
`grammar.py`'s production table provides. Combined with §16.6's finding that `λ` is built
from the atom set rather than the production table: **the number is computed from the wrong
subject AND fed to nothing.**

## §17.1 · arity, with the cap sourced — and the binding rule that answers the 13 hours

Confirms the half-done finding, and supplies what the plan's `cap 4` rests on: `dsl.py`
measured it, *the cost is quartic in N and they capped it at 4, because a vocabulary bought
with 10x the agent's lifetime is a net loss even if it is the right vocabulary.*

**And then the part I should have read before measuring anything:**

> Which slots fill the operands is a binding decision, and the natural default is **the slot
> that owes plus whatever is in contact with it** — Figure 11's enumeration supplying the
> argument list.

`_bindings` returns `[None] + every other slot`. **That is the O(slots) factor that produced
the 13-hour figure at 64x64, and the corpus already says the binding should come from
CONTACT rather than from enumeration.**

So the scaling problem I measured, scoped an effect-index for, and reported as needing a
different structure **has a stated answer in the design document**: bind by contact, and the
slot count stops driving the argument list. The effect-index may still be worth having; it
is not the fix for that number.

## Standing count

Four documents read for conflicts, in order: `ARC_BUILD_PLAN`, `DISCOVERY` (4 questions),
`PHILOSOPHY` (§8, §16), `ARC_AGENT` (§17, §19). **Every one contradicted something already
built.** The unread remainder is `DISCOVERY` Q1–13/15–17/20–25/27, `PHILOSOPHY` §0–7/9–15,
`ARC_AGENT` §1–16/18/20–23, `BUILD_PLAN` §1–7.

## Fifth batch — `ARC_AGENT.md` §14, §21, §23

### §21.5 predicted the step-6 failure in words, before it was measured

> without the distinction **the demotion logic poisons itself at exactly the wrong
> moment**: every level advance would demote the good terms that carried the last level,
> because they mispredict an unfamiliar board. **The agent would punish its best work for
> the crime of a scene change.**

**That is the boundary revert.** Built this session, measured on two independent panels,
cost opportunity/uptake/carried in both, removed. **The corpus named the failure mode and
the build walked into it.**

And it names the fix, which is not built:

    level RESET after a loss   the board is KNOWN     a residual means the model is wrong
    level ADVANCE             the board is UNKNOWN   a residual means nothing yet

`retarget` clears `bound`, so the worst case is softened -- nothing is demoted at the
instant of the boundary. But a term re-bound on the new level and mispredicting IS demoted,
and on an advance the corpus says that is evidence about nothing. **`snaps.ladder` has only
advances**, so every level change there is the kind where demotion is wrong.

### §14.7 names the metric this session approximated badly

> **chunk reuse count** — how often a settled term appears inside a later mint. **Zero is
> the failure signature, and it is the one that would otherwise look like progress.**
> ... A library that grows and is never reused is a catalogue.

**Not measured.** `Chain.reuse_attempts` counts the SWEEP's reuse -- a term closing another
slot's parked residual -- which is a different event from a settled term appearing as a
UNIT inside a later composition.

`lib ok here / lib` was invented this session for the same job, and it was worse: the
denominator can only grow under a never-delete library, which made it structurally
unrisable. **Chunk reuse has no such defect and was already specified.**

### §14.2 confirms `units()` exactly

    unsettled term      usable as a slot's binding, NOT as a building block
    settled by ground   promoted into the search vocabulary

Which is `units()` = atoms + settled terms. **Built, and built right.** *Only what the
ground has paid for becomes a shortcut.*

### §23.4 · the ablation clause must be stratified

    wipe minted only, priors kept   did it COMPOSE this game's solution, or retrieve it
                                    -- this is the terminal condition's clause 3
    wipe everything                 bootstrap from nothing -- not the claim being made

`CLAUDE.md`'s terminal condition says *back up Gamma, verify the backup, wipe Gamma,
re-run*. **Not yet a conflict, because nothing is preloaded** -- with atoms only, wiping
everything IS wiping the minted layer. **It becomes one the moment §23.2's loading
happens**, and the origin stamps that make it cheap are already written.

### §23.5 · loading requires retrieval, and it ties to the coverage defect

> more atoms means a larger `λ`, so `λ^d` grows and a fixed budget covers a smaller
> fraction -- which shows up as coverage falling and, if nothing is done, as more false
> `UNREACHED`. **Phase 3c stops being optional.**

So the effect-index is a **prerequisite of loading**, not an optimisation -- and the
mechanism runs through `λ^d`, which is the denominator `space_estimate` computes as `V^d`.
**Three findings meeting: the denominator is wrong, `λ` is measured from the wrong table,
and the consequence of both only appears once the library is loaded.**

## Sixth batch — `ARC_AGENT.md` §16, the habitat

### §16.5 is one mechanism answering three separate findings

> List everything in contact with the residual, then what is in contact with those, and
> outward until the cascade stops mattering. **You do not invent the list. You read it off
> the world**, and what you cannot perceive or measure yet is the residual.

**Three things this session treated as separate are this one procedure:**

    the operand binding      §17.1's `the slot that owes plus whatever is in contact
                             with it` -- and `_bindings` returns every other slot, which
                             is INVENTING the list
    B12, NO-BEHAVIOUR        `the habitat is enumerated` -- check text: the habitat type
                             is a sequence, not a library. Same mechanism, and it is why
                             the check has nothing to read
    the interface question   the decomposition read concluded `not a coarser alphabet,
                             a different slot set`. Figure 11 says which slots: the ones
                             in the contact cascade

**And the clause that settles the direction question outright:** *what you cannot perceive
or measure yet IS the residual.* The slot set is not chosen and not coarsened -- it is read
off contact, and what falls outside it is not a silent loss, it is R.

**`Enumerated, never composed`** is B12's own wording, so the check becomes runnable the
moment enumeration exists.

### §16.4 · affordances, and it is the action-learning schema already specified

> Do not classify the substance ... **Classify by behaviour under contact.**

    blocks · passes · moves-when-touched · changes-on-touch · triggers-remote ·
    terminates · consumed          seven booleans per object KIND, learned by interaction

> **"Wall" is not a category, it is a profile** — and the profile is what transfers.

This is the motor read's *what does an action do*, one level out: what does a THING do under
contact. **Learned by interaction, which is Q18's coverage-first**, and the two are the same
phase.

**And the valence clause matters for the objective work:** *an actor's valence is relative
to the residual. A blocker is a malfactor when you want through and a benefactor when
something is chasing you.* So the profile records what it does, never whether it is good --
**no standing list of good objects survives a change of objective.**

### §16.8 · `GAME_OVER` is a negative settle

> recorded as a settlement rather than as a failure — **it refutes a live bet, which is
> exactly what a settlement does**

Consistent with what is built: `demote` is a SETTLE-step event carrying `ground_said=False`.
The shape is right; the trigger does not exist because there is no death in this world.

---

# A standing rule, from four instances

    lambda                 specified as the spectral radius; built from the atom set and
                           fed to nothing
    UNREACHED              specified as the post-escalation claim; `depth_exhausted` is
                           reported at rung zero instead
    the escalation ladder  specified with five priced rungs; not built
    chunk reuse count      specified as the number to put on the wall; `lib ok here / lib`
                           invented in its place, and structurally unrisable

**When a metric is invented mid-session, check whether the corpus already named one.** In
all four cases the specified instrument had no defect and the improvised one did.

## Seventh batch — `ARC_AGENT.md` §18, the salvage hunt

### §18.2 restates Q18's rule, and `never_live` breaks it twice over

> **express-before-judge** — a refutation is recorded only after the hypothesis actually ran
> a trial and the operator registered. **"I failed to do X" must never be coded as "X is
> inert."** A blocked or never-reached attempt is a non-trial.

`settle`'s demote path has this and says so. **`never_live` does not:** `Drive.tried` is a
set of action labels, so an action drawn three times from one state is `tried`, and the
verdict *nothing I can see has ever moved* rests on it. **Two independent sources now name
the same defect** -- Q18's *re-probe from a different cell* and §18.2's *a never-reached
attempt is a non-trial*.

### Pathogen mimicry — named in the corpus, present in the code, measurable

> **pathogen mimicry** — a dead idea re-tried under a slightly different key — *the
> signature-granularity problem*, named and left to the caller rather than baked in

`Gamma.standing` keys on `term.name`, and a term's name carries its operand binding. **So a
refuted term has aliases**: same atoms, different binding, different name, no refutation.

**And the size of the hole is already measured.** Extensional collapse is 6.3x at depth 3 --
about six names per extension class -- so a refuted term has roughly six twins that escape
its refutation. **Directly checkable:** does an extensional twin of a refuted term get
minted afterwards? Not run.

### Two properties of defeasance, one built

    decay over a LOGICAL clock                      built -- `Standing.decay` on gamma.tick
    decisive new surprise REOPENS a refuted one     not built

The second is a fitness-conditional gate-drop, not a time decay. `Standing` only forgets;
it never reopens on evidence.

### `regime.py`'s CUSUM is the §21.5 detector

> a two-sided CUSUM change-point test over the success stream, fires only when deviations
> pile up past a threshold, so one spike never trips it but a sustained drop does -- **and
> it does not need to be told a level changed**

That is the reset/advance discriminator §21.5 requires, without a level flag. Not built, and
`snaps.ladder` currently announces its boundaries, so the detector would have nothing to do
there.

### §18.7 · the pattern, and it is this reading exercise one level down

> Six of eight gaps had answers already written -- several of them careful, receipted, and
> better than what I proposed ... **and they were never joined to a running loop.**
>
> **This is the three-branch diagnosis for the third time: the parts existed, correct and
> load-bearing, for architectures that could not use them.**

**Fourth time now**, and this session is the instance: the parts existed, in documents, for
a build that did not read them. §18.7 says the consequence is that the work is
**integration rather than design** -- which is also true of the six findings above.

## Eighth batch — `ARC_AGENT.md` §11–13

### A correction to my own §16.6 claim

I wrote that `λ` is *built from the wrong table*. **§11.3 says otherwise and it is right:**

> `λ = V = 7`, because every atom was `val → val` and the type graph was a single node ...
> With three spaces the graph is genuinely sparse ... **The instrument was working in the
> toy world; it just had nothing to measure.**

So `λ` computed over the atom set is CORRECT for the search it characterises -- the mint's
closure, which really is single-typed today. `grammar.py`'s productions are a different type
graph belonging to the utterance, not to the mint. **The instrument is waiting for
EXTRACT / RELATE / PREDICT, not misreading a table.**

**The `V^d` finding survives and is narrower than I stated.** `space_estimate(units: int, ...)`
takes a COUNT, so it cannot use `λ` even if handed it -- the signature forecloses the
substitution. Today `λ = V` so the number is right; the moment the type graph is sparse it
is wrong, and the fix is a signature change rather than an arithmetic one.

### §13.6 warning 1 · the atom registry's ORDER is load-bearing and nothing pins it

> inserting a name rather than appending renumbers the universe, making it **"a DIFFERENT
> SEARCH at the same size"** -- so stored terms and determinism receipts silently stop
> meaning what they said

Measured:

    same atoms, one moved to the front
    order A: ['idn', 'inc', 'dec', 'dbl', 'neg', 'act']
    order B: ['take', 'idn', 'inc', 'dec', 'dbl', 'neg']
    identical enumeration: False

**And `mint` breaks on the first closer**, so the emitted order decides which term is
minted. `take` was appended this project, which is the safe direction -- and nothing
enforces it. **This is checkable statically**, the way the append-only rule is.

### §13.6 warning 2 · the two numbers that set the whole search are unanchored

    class Config:
        max_depth: int = 3
        budget: int = 4000

**No anchors.** Q14: *a number without a provenance tag does not go in.* And §13.6 says the
measured quartic cost model *should set our depth budget rather than a guess* -- so the
provenance exists in the corpus and was never attached.

**And ANCHOR cannot see them.** Its docstring says *a module-level constant*, and these are
dataclass field defaults. **Same shape as ISOLATED reading only `tree.body`** -- a checker
scoped to one syntactic form, blind to the place the most load-bearing numbers actually
live. Sixth site.

### §13.4 · the archetype trap, and the part worth keeping

    domain-general, safe to take shape from   dsl · loci · boundary · affordance ·
                                              transform · progress
    archetype-derived, flag hard              relation (5 relations from a GIF-archetype
                                              audit of 23 games) · referent · operator_effect

> The right-hand column is **selection against the public set, stated in its own comments**
> ... and those three files are also the most *seductive*, being the ones that name the
> actual solving concepts.

**And the second-order content of the flagged column is general:** strip the five relations
and what remains is *hold several goal hypotheses at once, express each as a scalar
discrepancy that is zero exactly when satisfied, and select the one whose discrepancy is
confidently shrinking under play.* **Take the selector, leave the five.**

## ANCHOR widened — the sixth site closed, and eight numbers given a basis

**The subject was narrower than the property**, for the sixth time. `_anchor` read
`ast.parse(src).body` only, so the two numbers that set the entire search -- dataclass field
defaults -- were invisible to a rule whose stated property is *a number with no stated basis
is an invented metric*.

Widened to **class fields**. **Not to default arguments**: fifteen exist and most are
harness conveniences overridden at every call site, and a rule widened until it fires on
everything is what ISOLATED taught by inflicting it on itself. **The remaining form is named
in the docstring** so the gap is known rather than rediscovered.

## What it surfaced, and what each is

    Config.max_depth = 3    GROUNDED in the toy world's own falsifier. `world._ladder` is
                            four atoms deep and PAST this depth, so it is unreachable in
                            atoms and reachable in units once `swing` settles. Depth 3 is
                            what makes the chunking claim falsifiable; at 4 the falsifier
                            would be reachable without chunking.

    Config.budget = 4000    SPECIFIED, and it bounds the wrong quantity. It caps CLOSURE
                            YIELDS; the work is yields x operand bindings. Measured over 12
                            worlds: max yields 1884, max tried 4206, `budget_exhausted`
                            reported ZERO times. **The declared bound never binds, and the
                            work exceeded it.** Stated rather than fixed.

    SlotSpec.a / lag / switch / k2, WorldSpec.n     INERT -- `spec_for` draws every one of
                            them for every generated slot, so the defaults are reached only
                            by a hand-written spec. Placeholders carrying no claim.

    WorldSpec.hold = 3      ALREADY GROUNDED and unreadable. The basis was written when the
                            constant was: *the smallest hold that cannot be satisfied by
                            one-step luck*. It said "Anchored, not tuned" rather than the
                            marker, so the checker could not see it. **The format is the
                            contract, working as intended.**

**`Config.budget` is the find.** A declared search bound that caps the enumeration rather
than the search, never binds on this panel, and was exceeded by the actual work while
reporting no exhaustion. Every measurement this session ran under it.

    8/8 seats clean

## The atom order, pinned

    ['idn', 'inc', 'dec', 'dbl', 'neg', 'act', 'wrap', 'take']

A fixture rather than a rule: a static pass has no baseline to compare against, because the
correct order is a fact about **history**, not about shape.

**Why it is load-bearing.** The registry is positional, `mint` breaks on the first closer,
and moving one atom to the front changes the first six terms the closure emits. **So the
order decides which term gets minted.**

**And every number on this panel was measured under it** -- the false-mint rate, the
extensional collapse, both narrowing arms, the bit-rate readings -- **and not one of them
states it.** Now one thing does.

    passes as it stands
    fires on a reorder    ['take', 'idn', 'inc', ...] against the pin
    fires on an append    deliberately -- extending the pin is a decision, not a
                          side effect

**Append-only is the rule and the pin enforces the harder half:** an append leaves every
prefix intact so prior terms keep their identity, but extending the pin has to be a choice
someone makes rather than something that happens. `take` was appended, which was the safe
direction, and nothing enforced it until now.

    8/8 seats clean

---

# Two readings taken, both specified in the corpus, neither run before

## §22.2 · the transfer reading — NEGATIVE

> **phase 1 shrinks on level 2 → the library transferred, which is the whole thesis** ...
> random stays dominant → *it never left phase 1. Nothing is being modelled.*

    10 seeds x 4 levels x 40 steps, DS 0.4

     level   probe share   with my probe fix ABLATED
         0         92.2%                       90.0%
         1         92.2%                       89.5%
         2         96.2%                       91.5%
         3         93.8%                       90.5%

**Phase 1 does not shrink.** 2 of 10 seeds fell; the mean rose.

**And it is not my confound.** This session's probe fix routes bored steps to `by="probe"`
where they could previously reach `discriminate`, which moves the histogram toward phase 1
by construction. Ablated, the share is 2-4 points lower and **the shape is identical** --
90.0% -> 90.5%, flat.

Against the human reference of ~30 random / ~10 directed / ~5 strategy, ~67% at level 1.
**The agent sits at 90% and stays there.** Two-valued, because STRATEGY arrives with
routines and routines are not built -- so this reads probe-versus-directed, which is still
the shape that would show transfer if there were any.

## §14.7 · chunk reuse — POSITIVE, and it is the first time the number has been read

> **Zero is the failure signature, and it is the one that would otherwise look like
> progress.**

    mints                      158
    reuse by containment        37    23.4%   over-approximate: a short chunk can
                                              appear inside a longer term by chance
    PAST atom depth             22    13.9%   PROVABLE -- the closure is max_depth UNITS
                                              deep, so a term longer than max_depth atoms
                                              cannot be built from atoms alone
    deepest term                 6            against max_depth 3
    settled chunks at end       38
    library at end             163

**Not zero. The reach compounded to twice atom depth**, which is §14.2's claim measured:
*depth stays 3, reach compounds.* Predicted up to 9 atoms; observed 6.

## What the two together say

**The library compounds and the action mix does not change.** Those are different claims and
only one holds:

    chunking works                 13.9% of mints are past atom depth, deepest 6
    transfer does not show         phase 1 flat at ~90% across four levels

So the mechanism §14.2 specifies is running, and the reading §22.2 says would demonstrate
transfer is negative. **Both were specified, neither had been run, and they disagree** --
which is more informative than either alone, and is the reason §14.7 says to put chunk
reuse on the wall rather than a single summary number.

## The caveat, tested — transfer-as-better-probes does not show either

Four per-level readings the phase histogram cannot see:

     level  live fraction  steps to 1st close  mean mass/step  slots bound
         0          39.0%                18.6            0.50          2.3
         1          43.0%                12.3            0.57          2.9
         2          38.8%                15.3            0.49          3.1
         3          45.5%                15.3            0.60          3.3

**`slots bound` rises monotonically** -- 2.3 to 3.3 -- and I read that as transfer showing
in an instrument the histogram misses. **It is not. The control says so:**

     level   CARRIED    COLD   difference
         0      2.30    2.30         0.00
         1      2.90    2.90         0.00
         2      3.10    3.10         0.00
         3      3.30    3.30         0.00

A fresh agent with a fresh Gamma on the same worlds binds **exactly the same number at every
level**. **The rise is the generator: the ladder drifts toward easier worlds at DS 0.4.**

## But carrying is not inert — it changes what, not how much

    levels 1-3, 10 seeds, 30 comparisons
      identical bindings (same slots, same terms)     6
      DIFFERENT bindings                             24
    settled units available to carry   mean 1.9, max 6

**Carrying changes which terms are found in 24 of 30 cases and changes the count in none.**
The settled chunks enter `units()`, the enumeration differs, a different term is minted --
and the same number of slots ends up explained.

## Where that leaves the transfer reading

    phase histogram        flat at ~90% across four levels
    slots bound            rises, and rises identically without carrying
    steps to first close   falls, not monotone: 18.6, 12.3, 15.3, 15.3
    chunk reuse            13.9% provable, deepest term 6 against max_depth 3

**Chunking runs. Carrying alters the search. Neither shows up as the agent doing better.**

And the ladder drifting easier is a finding about the generator that nothing had checked:
**every level-over-level comparison on this panel needs the cold control**, because the
levels are not of equal difficulty and the drift is worth a full slot on its own.

## Is `different` better? No — and the direction is the alignment failure

Levels 1-3, 10 seeds, graded extensionally against the ground's rules:

    arm         claimed  correct   rate   atoms  mean len
    carried          40       25    62%       2      2.83
    cold             34       24    71%       1      2.71

**Carrying produces six more claims and one more correct term.** Five of the six extra
claims are wrong.

**And the mechanism is legible.** The number of slots BOUND is identical between arms -- the
cold control showed 0.00 at every level -- but `claimed` is *bound and not owed*. A larger
library gives `_library_fit` more to rebind from, more rebinds close, and more debts retire.
**So carrying converts abstentions into claims, and the converted ones are mostly false.**

**Stated with its uncertainty:** 62% against 71% on 40 and 34 claims is about 1.2 standard
errors. The rate difference is suggestive and not established. **What is established is that
correctness did not rise** -- 25 against 24 -- while claims rose by six.

## The transfer question, closed on the evidence available

    chunking runs                 13.9% of mints past atom depth, deepest 6 vs max_depth 3
    carrying alters the search    24 of 30 level-comparisons find different terms
    the count does not move       cold control identical at every level
    correctness does not move     25 correct carried vs 24 cold
    behaviour does not move       phase 1 flat at ~90% across four levels
    and the ladder drifts easier  which is why every level-over-level number needs the
                                  cold arm before it means anything

**The library is doing work and the work is lateral.** Not more explained, not better
explained -- differently explained, with a few more debts retired on terms that are wrong.

## Does the corpus say what a rebind may retire? — checked, and the answer redirects

**`THE_FORMULA` step 2:**

> `BROKEN · rebinding` — **the model is right and attached to the wrong thing. Re-fit the
> binding. Do not mint.**

**It does not say the debt persists.** And `_library_fit` requires `_explains`, which is
`left == 0`, so a rebind CLOSES R -- and by A3 (*step 7 fires on failure to CLOSE R*)
retiring the debt is correct. **The corpus does not forbid the retire.**

**What it forbids is one line further on, in the worked reading:**

> 4–5 · Where it came from, and what settled it. **If nothing settled it, the result is a
> candidate. Say so, and do not cite it.**

**And the code says so.** The rebind row carries `status="candidate"` in the same two lines
that clear `owed_import`. **The loop is honest; `owed_import` means R-not-closed, not
not-settled, and those are different states.**

**The collapse is in the grader.** `snaps.grade` reads `bound and not owed` as a CLAIM:

    R not closed          owes
    R closed, not settled CANDIDATE  <- the corpus's word, and grade calls this a claim
    settled               accepted

So the erosion measured above is real in the grader's terms and, in the corpus's terms,
**the carried arm produces more CANDIDATES rather than more claims.**

## Which redirects at STAGE 1, and says its falsifier was wrong

STAGE 1 was built this session to move the claim from MINT to SETTLE -- *a close makes a
candidate; the slot keeps owing until the ground has spoken.* **It measured null on
`false_mint_rate` (36% -> 38.5%) and was reverted.**

**Under STAGE 1 a rebind could not convert an abstention into a claim**, because the slot
would keep owing until settled. **So the carried-versus-cold reading is the falsifier STAGE
1 should have had, and `false_mint_rate` could not see its effect** -- the rate is over
claims, and STAGE 1's whole effect is on what counts as one.

**Testable and not tested:** re-run carried-versus-cold with STAGE 1's behaviour. If the six
extra claims stop appearing, the mechanism was right and the falsifier was wrong.

**Nine of nine holds.** The corpus said *candidate, and do not cite it*; the build enforced
it, then withdrew it against a number that could not measure it.

## STAGE 1 re-tested against the falsifier it should have had

    as built            claimed  correct   rate
      carried                40       25    62%
      cold                   34       24    71%
      carrying adds        +6 claims, +1 correct

    STAGE 1             claimed  correct   rate
      carried                29       19    66%
      cold                   32       23    72%
      carrying adds        -3 claims, -4 correct

**The hypothesis holds. The six extra claims stop appearing** -- carrying goes from
`+6 claims, +1 correct` to `-3 claims`. And the cold arm barely moves (34 -> 32), so the
effect lands almost entirely on the carried side, which is what the mechanism predicted:
STAGE 1 blocks rebind-driven debt retirement, and rebinds are what carrying enables.

**And the seventh law is demonstrated rather than argued.** `false_mint_rate` read
36% -> 38.5% and called STAGE 1 null. The carried-versus-cold reading detects it plainly,
because the quantity it compares is not the one STAGE 1 redefines.

## But it is not free, and the trade is the honest result

STAGE 1 costs the carried arm **11 claims, of which 6 were correct.** Those 11 become
abstentions. So it is a precision trade, not a repair:

    rate       62% -> 66%      claims 40 -> 29      correct 25 -> 19

**More right per claim, fewer right in total.** Whether that is an improvement depends on
what the product is -- and for a project whose product is *an agent that says when an
answer is unreachable*, giving up six correct claims to remove five wrong ones is a
question rather than an answer.

**Small panel:** 30 level-instances, ~120 slots. The direction is clear; the trade's size
is not.

## And one arm bug, caught before it was reported

The first STAGE 1 arm only ADDED to `owed_import` and never removed, so a slot that owed
once owed forever and both arms read near-zero -- carried 0, cold 2. **The rule is *owes IFF
not settled*, not *owes once unsettled*.** The tell was that 34% of bindings ARE settled at
level end, so ~39 claims were expected and 2 arrived. A result that disagrees with a
directly measurable quantity is a bug in the arm before it is a finding about the loop.

---

# RETRACTION — the ladder does not drift easier

**Claimed on 10 seeds. Does not survive 40.**

    COLD arm, 40 seeds x 4 slots, 40 steps
      level 0   2.92        level 2   2.95
      level 1   2.67        level 3   2.88

    level 0 -> 3:  -0.05,  SE 0.28  =  -0.2 SE

    in_closure share: 24%, 22%, 22%, 29%   +5% at 1.0 SE, non-monotone

**The ladder is flat in difficulty.** The 2.30 → 3.30 rise was ten-seed noise, and the
reason both arms showed it *identically* is that they are paired on the same worlds -- **the
control was working; there was nothing for it to detect.**

## What this costs and what it does not

**Costs:** the standing note in `INDEX.md`, now corrected. And the proposed panel repair's
premise -- *the toy ladder drifts easier, ARC-3 gets harder, those are opposed* -- **the
first half is false. The ladder is flat.**

**Does not cost:** the cold control itself, which remains required and is what caught this.
Nor the carried-versus-cold finding, which is paired within seed and stands: **a carried
agent binds exactly what a fresh one does, 0.00 at every level.**

**And it improves the transfer reading.** Flat behaviour on a *flat* ladder is honestly
flat. I had reported it as possibly stagnation masked by easing; it is not masked by
anything.

## The repair is still worth building, for a different reason

Not *because the ladder eases* -- it does not -- but because **a flat ladder gives the
carried-versus-cold gap nowhere to open.** On a rising curve, holding steady IS transfer and
the gap can widen. On a flat one, carrying and not-carrying look the same whether the
library works or not, which is what was measured.

**Same structural guarantee either way:** whatever sets the difficulty must not be shown
what the agent carries, and the cold arm must be measured to decline before the ladder is
used for anything.

## Ninth batch — `ARC_AGENT` §4 and §8

### §4 dissolves the eight-versus-ten conflict rather than confirming it

The adapter table gives **`actors` = `available_actions` this frame** and **`substrate` =
64x64 grids, cell values 0–15**. `actions()` and `alphabet()` are exactly those two made
**machine-readable** rather than prose. **Ten members over eight slots, and the ruling is
intact.** Recorded as `ok`, not `gap`.

### §4 also confirms the R_T split

> `bracket` — `1 − fidelity` of the logical-grid lens; **this env actually feeds it**,
> unlike the toy world where it was inert

Which is §16.1's concrete-metric case, and the pre-image form built here is the general
order relation for a domain with no metric. **Two forms, both sanctioned, and the ARC
adapter uses the one Q19 calibrated at 0.98.**

### §8 risk 2 · my audit was wrong about `starving()`

> The reward channel is nearly always zero ... `density(R) ≈ 0` on the reward channel **by
> construction**, so the curiosity drive fires almost always and **its trigger has to be the
> transition channel or it is useless.** `probe.py` already triggers on the agent's own
> prediction error, **which is the right one.**

The audit filed `starving()` as *computed, reported, and wired to nothing* -- an unwired
trigger, a defect. **It is not.** Branching on it is what would be the defect, and §20.3
gives the other half: computed and reported, it is the honest report that the objective
channel never spoke.

**Third finding this session that the audit called cosmetic or defective and the corpus
calls correct** -- after the one-alphabet number and `max_depth`.

### §8's other five, recorded

    1  GameAction members are process-wide singletons and the samples mutate them.
       Threaded swarms clobber each other and it reads as a reasoning bug, not a race.
    3  competition mode's make-once rule -- level resets only
    4  16 KB digest limit; test the boundary rather than discover it in a scored run
    5  the lens fires on the WRONG grid if the fidelity gate is loosened -- 0.98 again
    6  the submission schema is ambiguous across samples

## Tenth batch — `DISCOVERY` Q12 and Q17

### Q12 is built, and verified rather than assumed

> **one track. The derivation IS the decision.** Not *the loop decides and the gate audits*
> but *the utterance is how an action is proposed, and an utterance that does not typecheck
> and pass is not an action.* **There is no fast path to fall back to, because a fast path
> is what made the framework optional.**

In `step()`:

    except G.Ill as exc:
        self.refusals.append(str(exc))
        self.led.record(..., "refused", reason=str(exc))
        return False

**No action. Verified.** And the thing not to carry is named with its size: the reference
system ran **266,570 decisions through a 77-rung ladder while the framework named none of
them.**

### And Q12's stated expectation reframes every negative this session

> **The uncomfortable consequence, stated up front: the agent will be much worse at
> first.** The rung ladder exists because it worked. Deleting it means the framework has to
> carry the performance itself, and early on it will not. **That is the correct trade and
> it should be a stated expectation rather than a surprise in week three.**

Flat transfer, 90% probe share, a 42% false-mint rate, carrying that adds candidates rather
than correctness -- **these are the stated cost of one track, not evidence against the
design.** That does not make them good and it does change what they are evidence OF.

### Q17 · the integral is correct, and its partner is missing

> **NO DRIVE MAY EVER SUPPRESS THE TIME-INTEGRAL OF PREDICTION ERROR.** Two quantities, not
> one: `pe_integral()` monotone non-decreasing, and `outstanding()` -- surprise not yet
> explained -- **which is the aim and the currency.** `explain(bits)` reduces outstanding
> only.

**Built:** `_integral` is `+=` only across the whole file. No reset, no decay, no suppress,
and `retarget` leaves it alone -- which is right, because the integral spans the run rather
than the level.

**Not built:** `outstanding`. The loop has `owed_import` as a set of SLOTS and `base`
recomputed per slot on demand. **There is no bits quantity for unexplained surprise**, and
the corpus calls that one the aim.

### And Q17 names why the integral matters, which is `never_live`

> a seat can read the divergence between **integral flat because nothing surprising
> happened** and **integral flat because nothing is arriving** -- against the record rather
> than against the moment

**That is exactly what `never_live` distinguishes**, and the monotone integral is the
structural defence that makes it readable at all. Both were built this session, for
different reasons, without being connected. **Same instrument, twice.**

## Eleventh batch — `PHILOSOPHY` §5, and it re-opens the boundary revert

    SHADOW  does this predict something my frame does not?   local · online · in-episode
            -> decides whether to MINT
    ECHO    does this appear where I did not build it?       cross-domain · offline ·
            between episodes  -> decides whether it was a PRIMITIVE or a patch

    echo without shadow   apophenia
    shadow without echo   a working local hack. Legitimate, earns its keep, DOES NOT CROSS
    shadow then echo      a primitive

**`shadow without echo ... does not cross` is the boundary revert**, in the corpus, as a
rule. Built this session, measured as costing `opportunity`, `uptake` and `carried` on two
panels, and removed.

**The measurement was not wrong and the removal may have been.** The cost was real and
indirect -- reverting settled-ness shrinks `units()`, which changes what composes, which
changes what binds. **It is not a definitional reduction**, so the seventh law does not
apply here and the numbers were legitimate.

**But the correctness signal was inconclusive, not negative:** pooled 29.7% -> 21.8% at 1.3
SE. **The revert was removed on a transfer cost with an unresolved correctness benefit** --
and §5 says the rule it implements is a rule rather than a taste.

## The reconciliation, and it is about the panel

Promotions fire **6 and 9 times over 12 seeds x 4 levels**. So on this panel almost every
term is shadow-only, and *shadow-only does not cross* blocks almost all crossing. **The
rule costs what it costs here because there is barely any echo to spare.**

**That is a fact about the panel, not about the rule.** A domain where the same mechanism
recurs -- which is what ARC's private set is built to be -- has echo to spend, and the rule
is cheap there and expensive here.

**Which is the same shape as the coarsening null:** a mechanism measured in a world
structurally unable to reward it, and the null read as being about the mechanism.

## Status change

The index row for `promote` stays `ok`. **The boundary revert moves from `removed on
measurement` to `removed on a panel that cannot pay for it`** -- and re-testing it belongs
on a panel with recurring mechanisms rather than on `snaps`, where four independent slots
per world make echo nearly accidental.

---

# Conclusion — the panel is the binding constraint

Eleven batches of reading produced roughly a dozen actionable rows and four corollaries of
process. **None of that is the finding.**

**The kernel's defects were real and mostly fixable by reading.** Four `wrong` rows in
`INDEX.md`, several `gap`s closed, and three of this session's own audit findings reversed
because the corpus was right and the reader's rule was narrower than it looked.

**The panel's limits are what everything else is blocked on.** Three of the project's
central questions are unanswerable on `snaps` for stated structural reasons, and all three
need the same thing:

    does the library transfer?              needs difficulty that rises
    should shadow-only terms cross?         needs mechanisms that recur
    does coarsening make rules expressible? needs a value space with quotients

**Nobody was looking at the panel, because a panel does not produce findings.** It produces
the numbers everything else is judged by, and it was never itself judged. `M = 7` was
anchored for exhaustive sweeping and foreclosed coarsening. The ladder was called easing on
ten seeds and is flat on forty. Four independent slots per world make echo accidental. **All
three are properties of the generator that only appeared when a null needed explaining.**

## Why a new panel is the highest-value build left

**It unblocks three questions at once, and everything else on the board is a row.**

**And it is not a toy-world detour.** ARC-3's private set is built to be a domain where
mechanisms recur and difficulty rises -- which is exactly the two properties `snaps` lacks.
A panel with them is the closest available proxy for what the agent will actually face,
rather than a better version of a thing that is not the thing.

## The honest limit

**A better panel still is not ARC.** It would establish whether these mechanisms can show
AT ALL -- currently unknown for all three -- and not whether they work on a real game.

**But `currently unknown` is worse than `measured negative`**, and three central questions
are in that state for reasons that have nothing to do with the design.

## What it must satisfy, both stated before building

    STRUCTURAL   whatever sets the panel's property must not be shown what the agent
                 carries -- the way `_views(names)` is never shown `spec.rules`. A panel
                 tuned until the mechanism shows has encoded the result.

    MEASURED     state what makes the panel harder / recurring / quotient-bearing, and
                 CONFIRM IT before using the panel as a premise. The cold arm must be
                 measured to decline before the ladder is called harder.

---

# CORRECTION — transfer shows. I measured one point on a curve.

`SNAPS_PLAN` §1: *generate level n+1 at a **specified DS** and the question stops being
"does it transfer" and becomes **a curve**.* §7 falsifier 1: *if reuse rate is flat
**across DS 0.0→1.0**, DS is not controlling anything and the ladder is decoration.*

**Every transfer number this session was taken at DS 0.4.** The `ds` parameter has never
been swept. Swept:

       DS  claimed  carried   reuse  false   rate  x-retro
      0.0       18       13    0.72      5    28%        0
      0.2       31       11    0.35     16    52%        1
      0.4       29        6    0.21     11    38%        3
      0.6       25        5    0.20     13    52%        3
      0.8       25        1    0.04      2     8%        4

    (8 seeds x 4 levels x 40 steps per DS; the run reached DS 0.8 before the cap)

**Reuse: 0.72 → 0.35 → 0.21 → 0.20 → 0.04, monotone.** Falsifier 1 does not fire. **DS
controls transfer and the ladder is not decoration.**

## What this reverses

**The flat phase histogram and the identical cold control were read as `transfer does not
show`. They were one point on a curve** -- and DS 0.4 sits at reuse 0.21, in the middle of
a real decline.

**The two endpoints are exactly the degenerate cases §1 names:** *identical levels →
everything transfers, the metric reads one and means nothing* (DS 0.0 gives 0.72), and
*unrelated levels → nothing transfers, reads zero* (DS 0.8 gives 0.04). **The metric is
informative in between, which is what the ladder was built to produce.**

## And a finding inside the curve

**Reuse halves on a CONSTANT change alone.** DS 0.2 changes `k` and `a` and nothing else --
same families, same structure -- and reuse falls 0.72 → 0.35. **The library is tied to
specific constants, not to the mechanisms they parameterise.**

That is a sharper diagnosis than anything the level-wise readings produced, and it is
consistent with the false-mint read: terms that close a slice are fitted to the arithmetic
they saw.

## Twelfth instance, and the most expensive

The headline reading was specified, the machinery takes the parameter, and it had never
been swept. **`ARC_BUILD_PLAN`'s conclusion that the panel is the binding constraint was
written on a single-point measurement of a curve that was already available.**

**The panel is not the binding constraint for the transfer question.** It may still be for
the other two -- echo needs recurrence, coarsening needs a composite modulus -- and those
arguments stand on their own structural grounds.

## Twelfth batch — `SNAPS_PLAN` §0, §2, §3

### §3 closes the boundary revert, by ruling rather than by measurement

    | Γ library + standing | ✅ | this *is* the transfer claim |

**Standing persists across a level boundary. Explicitly, and the reason given is that the
persistence IS the claim being made.** The boundary revert un-settles unpromoted terms at
exactly that boundary.

**So it stays out**, and not because it cost transfer -- because the panel's own persistence
table says the thing it removes is the thing being measured. `PHILOSOPHY` §5's *shadow
without echo does not cross* is about crossing a SCALE or a domain; a level boundary in
this ladder spans DS 0.0 (a reskin) to DS 1.0 (nothing shared) and is not one boundary but
a dial.

**The re-opening I recorded last batch is withdrawn.** It rested on `promotions are rare on
this panel`, which is true and is not the reason.

### §2 reframes the 42%

> **`chain`, `lagged` and `hidden` are the direct attack on the 42% false-mint rate.** They
> are exactly the shapes that punish a term fitted to a narrow observed slice, **because the
> slice cannot contain the evidence that would refute it.**

**Three of the five added families are outside closure, `which roughly doubles the honest-
abstention test surface`.** So the false-mint rate is not purely an agent defect -- **it is
the panel's abstention test, and the families were chosen to make the agent fail it.**

The false-mint read found the wrong mints concentrated in exactly those families -- hidden
4, regime 2, lagged 2, quadratic 2, chain 2 -- and §7's falsifier 2 says that is the
diagnosis holding: *if chain/lagged/hidden do not move the false-mint rate, the 42% is not
about narrow slices and my diagnosis is wrong.* **They move it.**

### §3 also confirms the sweep

> parked residuals ✅ -- **the sweep's only real target.** A residual parked on level 2 is
> not re-searched by the mint while playing level 5 -- **which is precisely the condition
> the toy world could not create.**

Cross-level retro across the DS sweep: **0, 1, 3, 3, 4.** It rises with deviation, which is
the sweep doing work the mint could not.

### And no ruling on recurrence

§0 contributes families, weights and DS, and nothing about mechanisms recurring across
levels. **The echo question was closed by §3 instead, so recurrence is no longer load-
bearing** -- and the panel table is down to one open question: coarsening, which needs a
composite modulus and rests on `7 is prime`.

## `SNAPS_PLAN` finished — §4 and §9

**§4 is built.** Three terminations, all present: `terminal()` returns `death` when an
`AVOID` objective is violated, `advance` when the objective is held for `hold` steps, and
the ladder closes the segment as `run_end` otherwise. **And the AVOID subtlety is
implemented**: *AVOID can never advance -- surviving the budget is the win, so exhaustion
is scored as the advance for that family.*

**§9 is the firewall, and it holds.** Not coming in: the 30-expert taxonomy, the MoE
router, DCS, the coverage projection, and **any per-game mechanic -- absence lists only,
never content.** `snaps` carries families, weights and DS, and no game content.

## What the file was worth, in total

Ten sections, and **four of them overturned or reframed a conclusion this session had
already published:**

    §1  the transfer reading is a CURVE across DS      overturned the headline negative
    §2  chain/lagged/hidden ARE the 42% attack         reframed the session's central number
    §3  Γ library + standing persists                  closed the boundary revert by ruling
    §5  the curriculum is a monotone sweep over two    specifies the panel repair, and
        world properties; DCS rejected                 rates it S5, least certain to matter

**And the panel repair turns out to be specified and deprioritised by its own plan.** §5
gives the two orderings -- *fraction of slots outside closure* and *mean minimal term
length*, both computed from the key, both external, neither anything the agent produces --
and §8 puts the curriculum sweep last, *because it is the least certain to matter.*

**So `build a better panel` was never the missing piece.** It is S5 of a five-stage plan
whose S3 (DS-controlled generation) was built and never swept.

## The pattern this file demonstrates

**The panel's own document was the highest-yield reading of twelve batches, and it is the
one nobody opened, because a panel does not produce findings.** It produces the numbers
everything else is judged by, and it was never itself read.

## Thirteenth batch — `DISCOVERY` Q1, Q24, Q25

### Q1 confirms the A7 rename from the other side

> `R_pred`, **per slot**, drives MINT of predicates -- the formula's `R`
> `R_goal`, **per objective**, drives composition of actions

**`R_goal` is per OBJECTIVE, not per slot.** So the reward channel's quantity was never a
per-slot residual, and keying it `mass` -- which A7 caught by making `of` truthful -- was
the conflation. **Two routes to the same conclusion: A7 from the record, Q1 from the
design.**

And Q1's own remedy is the unbuilt half: *drives composition of actions* is routines, which
`demo.py` already reports as recorded-and-not-actioned.

### Q24 gives `closure(Γ)` a bound the designer does not pick

> If `R` is not falling: either Γ's variety is below the environment's -- **mint** -- or the
> disturbance variety was never observed -- **probe**. ... It reframes MINT as **variety
> acquisition**, which gives `closure(Γ)` **a lower bound the environment imposes rather
> than one the designer picks.**

**That is a basis for sizing the atom set and the depth, and it is not the basis in use.**
`Config.max_depth = 3` is grounded in the toy world's chunking falsifier -- a good anchor,
and a different quantity from the environment's disturbance variety. **Ashby's inequality
is the principled version and nothing computes it.**

### Q25's branching test is already passing, and nobody ran it as one

> An invertible transform, iterated, is a permutation -- orbits, not a tree. **A tower of
> seats, agents, or generations that has produced no divergence has no transform and is a
> copy loop however deep it goes** -- and that is visible without access to the transform
> itself. **Ship it as a check on any multi-level structure.**

**The carried-versus-cold measurement IS this test.** Same worlds, one agent carrying its
library and one fresh: **24 of 30 comparisons produce different terms.** That is divergence,
so the ladder is not a copy loop and the transform is real.

**It was run to ask whether carrying helps.** It also answers a question the corpus says to
ship as a standing check, and it passes -- which is the connection table's shape again: the
measurement existed and its second meaning did not.

---

# The figures are readable, and nobody had opened them

Eleven SVGs on the desktop, cited more often than any document in the set, and **not one
had been read this session.** They contain real text -- Figure 6 alone has forty-odd
statements.

## Figure 6 corrects the INWARD scoping

I concluded from Q19 that INWARD means **incremental** sharpening, coarse to fine. **The
figure explicitly rules that out as a requirement:**

> **What this rule does not say** ... theory routinely precedes its instrument, and is
> welcome to. **Neptune was calculated before it was seen** ... **instruments do not have
> to improve by small steps. A jump in resolution is fine.**
>
> **What is unavailable is a sensor for something that has never registered anywhere, at
> any resolution. That is the whole of it.**

**So the constraint is not gradualism. It is that SOMETHING must already be registering.**
*Where nothing is, there is no edge to extend from, and the search for a proto-instrument
is a search for one that is already there.*

**Which makes `never_live` the detector for exactly the one case the figure rules out.** It
fires when nothing has ever registered under any action -- *no edge to extend from* -- and
that is the state where INWARD has nothing to work with by the figure's own statement.

## And Figure 6 states three things the code already satisfies

    MINT composes inside the closure and can never add an atom     REACH checks it
    NOVEL means novel relative to ATOMS, not to the world          `is_atom`, and §16.3
                                                                   names it a proxy
    an import adds no atom to the WORLD; a frame gains access      step 7, unbuilt

## And it confirms §15.1 at the source

> **external source: nature · corpus · peer frame** ... IMPORT, **the only operator that
> moves the wall**, with a source gate on provenance and a shadow test on explaining a gap.

The channel was never closed. **`ARC_AGENT` §15.1 says the same thing and cites this
figure.**

## What this means for the reading

**Eleven figures, one read.** They are the primary source the documents cite, they contain
statements the documents paraphrase, and `PHILOSOPHY` §3 says at least one of them **still
carries a retired answer** -- so they are neither redundant nor uniformly current.

**Same shape as `SNAPS_PLAN`:** the thing everything else is written against, opened last.

## Figures 4 and 11

### Figure 4 disagrees with Q19 about `R_T`, and this is a routing finding

> take the round trip and measure the gap. Without it you are navigating by dead reckoning
> ... **The gap is not an error to eliminate. It is the measurement of what the coarser
> description cannot hold, and it is the ONLY HONEST REPORT of how much was given up.**

**The figure says measure and report. Q19 says gate.** And Q19 knows it is extending:
*Figure 4 says take the round trip and measure the gap; this takes the round trip and
**refuses** the coarser vocabulary when the gap is not near zero* -- offered as a
recommendation, not as the figure's content.

**So what is built matches the figure and not the recommendation.** The index row saying
`R_T reports where the ruling says it gates` is half right: it reports where the FIGURE says
report, and does not gate where Q19 recommends gating. **A figure and a document
disagreeing is a question to route, not a precedence to apply.**

### Figure 4 also states B9 in one line

> **Only methods cross up. Only head starts come down.** ... A recording carried upward
> looks like knowledge and is a description of one occasion. Replayed downward, it produces
> a system that repeats a past success and cannot produce a new one.

### Figure 11 · the third regime is the harness, and it has two silent failure modes

    1 unmaintained   survival of the fittest -- nothing chooses
    2 maintained     a seat acts: instrument, distil, introduce -- INTRODUCE, NEVER SUBTRACT
    3 isolated       the habitat SUBSTITUTED -- substituted, not removed

> **two silent failure modes: what you failed to reproduce, and what you brought with you**

**`snaps` is regime 3**, and `demo.py` already prints the first half -- *a synthetic solve
proves wiring and never capability; what it failed to reproduce is invisible until the goal
fails.*

**The second half is not printed anywhere.** *What you brought with you* -- and the clearest
instance is `snaps.key()`: **exhaustive extensional grading against the ground's own rules,
which ARC does not have.** Every correctness number this session rests on an instrument the
real domain cannot supply.

### And Figure 11 adds a clause §16.5 does not carry

> what the seat does: **enumerate the habitat, RANK BY CASCADE**, introduce actors, build
> instruments, read the ground

§16.5 gives the enumeration -- *list everything in contact with the residual, then what is
in contact with those, outward until the cascade stops mattering.* **The figure adds that
the result is RANKED by cascade**, which is the ordering `_bindings` would need and which no
document states.

## Figures 9 and 5

### Figure 9 · unreachability cannot be proved from inside

> φ found: one composition that pays, **proved inside**
> φ* out of reach: **nothing inside can prove that**
> **the witness is always imported** — *"it is not in here" cannot be proved from inside*
> **the edge can only be named from beyond it**

**This licenses the exact wording `depth_exhausted` already carries** -- *the whole space at
this depth was seen and none paid; not at this depth, NOT unreachable.* The verdict is
careful because the figure says the strong claim is unavailable.

**And it makes `UNREACHED` (§19.1, after escalation) still not a proof of absence.** Even
after five rungs, the honest claim is *I looked wider, later, deeper and across more slots*
-- **not that the term does not exist. That witness has to be imported.**

### Figure 9 · the retrieval keys, at source, and they differ from the document

    figure     R, described: arity · symmetry · scale  ->  the frame whose closure
               predicts it  ->  ONE LOOKUP
    §15.3      type signature · arity · what varies vs is invariant · effect shape

**Three against four, overlapping and not identical.** Route rather than resolve. Both agree
on the decisive part: **describe R before you go looking, or any frame you pick will seem to
fit.**

### Figure 9 · split before search, and it is unbuilt

> **First: is there a fact here?** Disagreements that do not shrink with effort, where each
> rule keeps working well on a different subset, are **not one hard question but several
> well-formed ones. Split it rather than search.**

Step 7's *is there even one fact here, or several* -- and nothing splits. The mint searches
harder where the figure says to split first.

### Figure 5 confirms the pipeline as built

Three channels (prediction gap, score, round trip), four bins (held / new / mis-attached /
mechanism broken), three guards, **and the bargain AFTER them**: *and then: does the new
term cost less to state than the confusion it removes?* **All built, in that order.**

**One clause is stated in `probe.py` and not done:** *the curiosity drive ... **aimed at the
new bin**, seeks the gap that is large and compressible.* `starving()` computes the trigger,
the docstring says it aims at NOVEL, and the draw is uninformed by construction. **Aiming is
specified and absent** -- which is a different thing from the transition-channel probe,
where uninformed IS the safety property.

## Figures 1 and 3

### Figure 1 · a routing case on `coverage`

> The ground enters as the only metric ... **These do not count: coverage, and compression
> achieved; predicates minted, and credibility accrued. They are frame-internal. A frame
> cannot score itself with a quantity it also produces.**

**`ARC_AGENT` §19.1 makes coverage the number that turns `unreached` from a word into a
measurement** -- *unreached, having examined 4,000 of an estimated 8,000,000 -- coverage
0.0005 is a completely different claim from 4,000 of 4,000.*

**Route.** Both hold if coverage is a QUALIFIER ON A VERDICT and never a SCORE OF THE AGENT.
It is on every mint row, and nothing scores with it -- which is the reading that satisfies
both. **Worth stating, because `coverage rose` would be an invented metric and `coverage
0.0005` is a caveat on a claim.**

### Figure 1 confirms the core, clause by clause

    residual R indexed by object slot -- transition · reward · bracket     built
    a global R near zero with ONE LIVE SLOT is a LEGAL STATE               REPAIRS 1
    aggregating across slots is how a live signal disappears               the `of` field
    support evaluated PER SLOT                                             the predicate

### Figure 3 · the agent stops at the link the figure says has no instruments

    1 perception   2 vocabulary   3 the objective   4 planning   5 learn and carry
                   ^ what the search can REACH      ^ what the search is FOR

`demo.py` reports **`stopped at link 2 - vocabulary (measured: 1 slot unreached at
budget)`**. And the figure:

> **Why the middle link is where chains usually break.** Perception has obvious failures and
> obvious tests. Planning has obvious failures and obvious tests. **The link between them --
> having terms for what a situation offers, and being able to say what would count as
> progress -- has neither, so it attracts the least attention and the fewest instruments.**
>
> **A link with no instrument is not a link that works. It is a link nobody has looked at.**

**The agent stops exactly there**, and the figure says that is where chains usually break
and why.

> **A step whose input never arrives cannot be diagnosed, only its predecessor can.** A
> reading taken below the break is not a weak reading. **It is a reading of nothing.**

**Which is the stage code's whole justification**, and it bears on this session: every
measurement of minting, transfer and carrying was taken at link 2 or below. **They are
readings of the link that is breaking, not of the ones underneath it.**

> Before asking whether a system is good, ask **which link it currently stops at, and
> whether the answer was measured or assumed.**

`demo.py` prints the link, and prints `measured`. **That clause is satisfied.**

## Figures 2 and 10

### Figure 2 names the paired-evidence error, and I made it before reading it

    collapse 1  mutual update -- no anchor; each updates on the others; they converge on
                whoever had the most influence, and THE DRIFT IS COHERENT, WHICH IS WHY
                NOBODY NOTICES
    collapse 2  common cause -- ONE EVIDENCE POOL. They never talk and still agree, so
                **the agreement is the pool talking, not two frames confirming each other**

> Independence, between two frames, is **how little they draw on the same evidence**. Two
> people reading the same report are not two frames; two instruments pointed at the same
> thing are.

**The carried-versus-cold arms run on the SAME WORLDS.** One evidence pool. **I read their
agreement -- 2.30, 2.90, 3.10, 3.30, identical -- as confirming a drift, and it was the pool
talking.** Diagnosed afterwards as *paired-noise agreement*; **Figure 2 is where that has a
name and a diagram.**

The pairing is still the right design -- it removes world variance -- **and what it cannot
do is corroborate.** Two arms on one pool agree by construction, so agreement carries no
information and only DISAGREEMENT does.

> **The anchor must not update.** If it does, panel 3 turns into panel 1 ... **If it moves
> when you push on it, it is not an anchor.**

### Figure 10 is the source of the checker laws

> **a declared meaning is not a grounded one → INSTALL WHAT CAN BE VIOLATED**
> the convention does not fix the bug, **it makes the bug statable**
> a disagreement nothing can state **is not yet a defect**

**That is `reintroduce the defect, never disable the check`, in the primary source** -- and
the whole witness discipline follows from it. The laws were written from defects; the figure
had the general form.

### Figure 10 · the channel decays, the ground does not

> **the ground does not decay, the channel does** -- stale percepts, dropped transients,
> saturated metrics, **pooled readings**
> **the output is not a verdict, it is `you have lost touch`** → keep the anchor reachable

**`never_live`'s utterance is this, in the agent's voice:** *either this world is still, or
what moves is not something I am built to see.* **`you have lost touch` is the figure's
phrasing of the same output**, and it is explicitly *not a verdict*.

**And `pooled readings` is listed as a CHANNEL FAILURE** -- the same collapse Figure 2
diagrams, arriving as a way the ground goes out of reach.

## Figures 7 and 8 — and the set is complete

### Figure 8 · the ceiling on `UNREACHED` is a theorem, not a design choice

> **Why A cannot derive the atom on its own**
> **Closure is idempotent.** Composing inside a closed set never leaves it, so no search,
> however long, adds an atom. **This one is definitional: it is what closure means.**
> **A frame cannot reach its own metaframe.** Godel's second theorem ... Tarski: truth for
> a language is not definable within that language.
> **A frame cannot certify its own limit.** Chaitin: beyond a fixed constant, no system
> proves that any object exceeds its own complexity.

**Figure 9 says the witness is always imported. Figure 8 says why, with citations.** So
`depth_exhausted`'s refusal to claim absence, and the ceiling on `UNREACHED` after the full
escalation ladder, are **Chaitin's result rather than a cautious wording choice.**

### Figure 7 · a formula no document carries

> **progress per handoff: R = h² × S**

The breeder's equation, applied to a chain of rooms: *low ρ between rooms; the next room is
picked against the residual the last one surfaced.* **`PHILOSOPHY` §16.5 gives selection's
bit-rate as `log₂ N`, which is a different quantity.** This one is not in any document read
so far.

**Third mechanism the figures name and no document carries**, after cascade ranking and
split-before-search.

### The five collapse modes, now complete across three figures

    1  mutual update        no anchor; each updates on the others; THE DRIFT IS COHERENT,
                            WHICH IS WHY NOBODY NOTICES                        Figure 2
    2  common cause         one evidence pool; the agreement is the pool talking  Figure 2
    3  the mirror chain     same closure handed along; agreement compounds, evidence does
                            not; ONE LONG ROOM: MOTION, NO PROGRESS             Figure 7
    4  the blend            same atoms, different names; their union adds nothing --
                            VOCABULARY, NEVER AN ATOM                           Figure 8
    5  the undirected union closures differ so a surplus exists, but NO RESIDUAL IS
                            DESCRIBED; nothing was aimed; the union is mute     Figure 8

**Collapse 5 is the one the build can walk into next.** It is importing without describing
R first -- and §15.3's *describe the gap before you go looking, or any frame you pick will
seem to fit* is the guard against it. **The retrieval mechanism is the guard, and it is
unbuilt.**

## The figures, read

**Eleven of eleven.** They produced: a scoping correction (Figure 6 -- INWARD is not
gradualism), a routing precedent used three times, a named error I had diagnosed the hard
way (Figure 2), the source of the checker laws (Figure 10), a formal basis for the
`UNREACHED` ceiling (Figure 8), and three mechanisms no document carries.

**They are the primary source every document cites, they are short, and they were opened
last.**

## `PHILOSOPHY` §7 and §11 — no actionable row, and that is the finding

**The character has shifted, as predicted.** Both sections are reasoning behind decisions
rather than specifications of mechanisms, and neither produced a row.

### §7 · the four regions — where the project's claim is located

    0 CONSERVATION  what is impossible          CLOSED -- theorems, not directions
    1 PERSISTENCE   given structure, how held   SOLVED repeatedly
    2 ACQUISITION   getting it from a source    PARTIALLY solved -- all the live engineering
    3 GENERATION    where it comes from when
                    nobody has it               NEARLY EMPTY. **THIS IS THE FINDING**

**MINT is the region-3 operator**, and the section's value is that it makes the emptiness
checkable rather than rhetorical -- the Price equation is *a mathematical identity ...
dynamically insufficient*, and origination *must be added by hand as an extra term*.

**Context for why the project exists. Not a row.**

### §11 · termination is free, productivity costs

> **A tower needs no transform in order to be RUNNABLE.** Lazy instantiation over identical
> dormant levels is enough ... **A tower needs a transform in order to DO ANY WORK.**
>
> **The transform is not what stops the regress. It is what makes the tower productive** --
> which is why it belongs on the bill and lazy instantiation does not.

**Two requirements the corpus had been asking one mechanism to serve.** It bears on Q22's
seat stack, which is unbuilt, and it settles what the transform is FOR when that is built.

And the branching argument in its substrate: *branching requires the map to be one-to-many
forward and non-invertible back. **Variation supplies the first; loss supplies the
second.*** Which is Figure 8 and §16.7 arriving a third time.

**Nothing to build, nothing to correct.** Recorded so the next reader knows these two were
read and produced framing rather than work.
