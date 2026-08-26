# ARC-AGI-3 agent — design

Branch `arc-agent`. Nothing is built yet.

Sources: `docs.arcprize.org` (llms.txt index and eleven pages), the three Kaggle sample
notebooks in `docs/sample-notebooks/`, and — most usefully — **the installed `arcengine`
and `arc_agi` packages** in `Ouroboros-Redux/.venv`, which are ground truth where the docs
are vague.

> `docs/` is gitignored on this branch, so this file is local unless you want it tracked.

---

## 1. What the platform actually is

**There are two different APIs and the docs interleave them.** This mattered enough to get
wrong, so it goes first.

| | `arc_agi` **toolkit** | `ARC-AGI-3-Agents` **harness** |
|---|---|---|
| entry | `Arcade(operation_mode=...)`, `arc.make(game_id)` → `EnvironmentWrapper` | subclass `agents.agent.Agent`, run `main.py --agent x` |
| loop | you drive: `env.reset()`, `env.step(...)` | harness drives: it calls your `choose_action()` |
| reasoning | `env.step(action, data=..., reasoning={...})` | `action.reasoning = ...` on the returned action |
| swarm | you orchestrate | `agents.swarm.Swarm`, one agent per game, threaded |
| **Kaggle uses** | no | **yes** |

**All three sample notebooks use the harness.** So the agent is a `MyAgent(Agent)` subclass
implementing two methods, and the reasoning goes on the action object rather than into a
step call. Building against the toolkit's `step(reasoning=…)` signature would not run on
Kaggle.

### Operation modes

`OperationMode` = `NORMAL` · `ONLINE` · `OFFLINE` · `COMPETITION`.

- **OFFLINE / local** — ~2,000 FPS, no rate limit, no credentials, runs many instances.
  No scorecards, no replays. **This is the development mode.**
- **ONLINE** — 600 RPM cap, needs a key, gives scorecards and shareable replays.
- **COMPETITION** — API-only; scored against *all* environments whether you play them or
  not; game resets silently become level resets; **`make` may be called exactly once per
  environment**; one scorecard only, and no reading it while in progress.

**Kaggle forces COMPETITION and you cannot opt out.** Two consequences for us: nothing may
depend on re-making an environment, and **the mid-run reward signal cannot come from the
scorecard** — it has to come from the frame, which is fine because `levels_completed` is in
the frame.

---

## 2. The observation, exactly

From `arcengine/enums.py`, not from prose:

```python
class FrameData(BaseModel):
    game_id: str
    frame: list[list[list[int]]]      # 3-D: a STACK of 2-D grids, not one grid
    state: GameState                  # NOT_PLAYED | NOT_FINISHED | WIN | GAME_OVER
    levels_completed: int             # 0..254   <- the ground
    win_levels: int                   # 0..254   <- the target
    action_input: ActionInput
    guid: str | None
    full_reset: bool
    available_actions: list[int]      # raw ints, not GameAction
```

**Three things to hold on to:**

- **There is no `score` field.** The StochasticGoose notebook records having to replace
  `latest_frame.score` with `levels_completed`. The ground is `levels_completed`, and
  `levels_completed == win_levels` is a game win — which is the terminal condition's first
  clause, already stated in `CLAUDE.md`.
- **`frame` is a stack.** The animation plays oldest → newest, so the settled board is
  `frame[-1]`. `new-horse`'s `unwrap_frame` already worked this out the hard way and wrote
  down why: acting on `frame[0]` means betting on a board the world has already left.
- **`available_actions` are ints**, and they change per frame. `GameAction.from_id(n)`
  converts.

### Actions

`RESET=0`, `ACTION1–4` directional, `ACTION5` context (select/rotate/fire), **`ACTION6`
complex — requires `x, y` in 0–63**, `ACTION7` undo. `is_simple()` / `is_complex()`,
`set_data({"x":…, "y":…})`.

Only `RESET` is accepted in `GAME_OVER`; anything else returns 400.

---

## 3. The reasoning channel — and it is better than the docs suggest

```python
class ActionInput(BaseModel):
    id: GameAction
    data: dict[str, Any] = {}
    reasoning: Optional[Any] = Field(
        default=None,
        description="Opaque client-supplied blob; stored & echoed back verbatim.")
```

with a validator that enforces **`MAX_REASONING_BYTES = 16 * 1024`** — 16 KB, JSON-
serialisable, and it *raises* rather than truncating. The docs do not state this limit
anywhere; it is in the package.

**Three facts that shape the design:**

1. **It is an opaque blob, any JSON.** Not a string field. So the whole per-cycle
   derivation record can go in it, structured, and come back structured.
2. **It is echoed back verbatim.** `frames[i].action_input.reasoning` returns what was
   attached to the action that produced frame `i`. **The agent can read why it did each
   past thing, from the environment's own record of it.**
3. **On the wire the remote wrapper does `json.dumps(reasoning)`** — so it is a JSON string
   at the transport layer and a dict at both ends.

### What this means for Tether

The ledger already *is* the thing this field wants. Every cycle Tether emits entries naming
their loop step, the bin and why-not-the-neighbour, the three guards including the ones
that passed, the code, the budget, and the verdict. That is the reasoning payload.

**But 16 KB is a real budget and a full cycle's ledger will exceed it.** So:

| | where it lives |
|---|---|
| **the full ledger** | local JSONL, gate-checked, never sent |
| **the per-action digest** | `action.reasoning`, ≤16 KB, derived from that cycle's entries |

The digest is a *rendering of the record*, which is exactly `speak.py`'s job — the same
rule as prose: fixed tokens, traceable, and it must cite the ledger sequence numbers so a
reader can join the two.

**An honest note on the echo.** It is tempting to treat the echoed reasoning as external
corroboration. It is not — it is the agent's own words handed back by a server that stored
them. No independence is gained. What *is* gained is a tamper-evident, timestamped copy
outside the agent's own process, which is worth having for a different reason: it survives
the agent crashing, and it is what appears in replays.

### And the per-action *why*, which is ask #4

`Nexus`'s `reasoning.py` already has the shape, and it is worth carrying almost verbatim:

```
regime · action · frame_read · rule_hypothesis · expect · disproof · status · step
        + a proposer block: candidates, current pick, abduced objectives
```

The two fields that make it more than a log are **`expect`** and **`disproof`** — what
should happen if the read is right, and what would show it wrong. Stated *before* the
action, which is what makes the next frame a test rather than a story.

That maps onto Tether cleanly: `expect` is the bet, `disproof` is the residual that would
refute it, `status` is candidate-until-the-ground-settles.

---

## 4. Mapping ARC onto the eight-slot contract

`world.py` already demands eight members. Here is the ARC adapter:

| slot | ARC |
|---|---|
| **substrate** | 64×64 grids, cell values 0–15 |
| **environment** | the game's hidden mechanics; the shaping medium |
| **actors** | `available_actions` this frame — and they change |
| **currency** | prediction error in bits, per object slot |
| **ground** | `levels_completed`. RLVR, and the only metric |
| **slots** | **segmented objects** — and this is the gap, see §5 |
| **atoms** | grid transforms: translate, recolour, reflect, rotate, appear, vanish |
| **transform** | full-resolution ↔ the logical-grid lens, gated on the round trip |

**Three channels of R, per the figure audit:**

- `transition` — predicted next frame vs actual, **per object slot**
- `reward` — `levels_completed`, and it is sparse. Almost always zero
- `bracket` — `1 − fidelity` of the logical-grid lens; **this env actually feeds it**,
  unlike the toy world where it was inert

---

## 5. The gap: perception is now required

Stage 2 deliberately gave slots by name, so that a failure was unambiguously a loop
failure — a gridworld tests perception and the loop at once. **ARC removes that choice.**
Slots have to be found.

Two files from `new-horse` do this and are worth carrying by shape:

- **`perception.py`** (219 lines) — connected same-colour components as objects; never
  downsample; segmentation as a *revisable belief*; permanence by IoU overlap so identity
  survives recolour and reshape; death only on evidence; every birth/keep/occlude/retire
  recorded.
- **`logical_grid.py`** (150 lines) — the lens. Detect a rendered N×N board, commit **only
  if the round trip is near-lossless**, and return `None` otherwise. `1 − fidelity` is
  `R_T`, and the calibration story (ls20's true 5-px grid scores 0.818 while a spurious
  2-px tiling scores 0.946) is why the gate is 0.98 and why the stride comes from motion
  instead.

**Neither is a rewrite.** Both are small, both already carry their own receipts, and both
were built against this exact API.

---

## 6. Getting it onto Kaggle

### What the notebooks actually do

Four cells, and all three samples share the shape:

1. `pip install --no-index --find-links /kaggle/input/competitions/arc-prize-2026-arc-agi-3/arc_agi_3_wheels arc-agi python-dotenv`
2. `%%writefile /kaggle/working/my_agent.py` — **the entire agent, inlined, one file**
3. gated on `KAGGLE_IS_COMPETITION_RERUN`: wait for the gateway, copy the harness out of
   the read-only competition input, drop `my_agent.py` into `agents/templates/`, rewrite
   `agents/__init__.py`, write `.env`, run `main.py --agent myagent`
4. if *not* a rerun: write a dummy `submission.parquet`

Two details worth copying exactly rather than rediscovering:

- **`agents/__init__.py` must be rewritten**, because the shipped one eagerly imports
  `langgraph`, `smolagents` and friends that are not installed. Every sample does this.
- **the gateway readiness loop** — `curl --retry 999 --retry-all-errors --retry-delay 5
  --retry-max-time 600 http://gateway:8001/api/games` before anything else.

`.env` for the rerun:

```
SCHEME=http
HOST=gateway
PORT=8001
ARC_API_KEY=test-key-123
ARC_BASE_URL=http://gateway:8001/
OPERATION_MODE=online
ENVIRONMENTS_DIR=
RECORDINGS_DIR=/kaggle/working/server_recording
```

Submission schema, from the two newer samples: `row_id, game_id, end_of_game, score`.
*(The `just-explore` sample writes `task_id, output` instead — that looks stale. Confirm
against the competition page before relying on either.)*

### The inliner — ask #2

The core is eight modules and about 1,481 lines. Kaggle wants one file. StochasticGoose's
agent cell is 17,040 characters, so size is not the problem — module imports are.

**`build_notebook.py`:** read the core modules in dependency order, strip the imports they
make *of each other*, keep third-party imports, concatenate, and emit both
`build/my_agent.py` and the `.ipynb` with that file written into cell 2.

Three rules it has to honour:

- **`gate.py` imports nothing, and must still import nothing after inlining.** Easiest is
  to inline it as its own section with no cross-references, and run it *after* the play
  loop over the local ledger, printing the verdict. Its non-access is the whole reason it
  is sound; an inliner that quietly wires it to the loop destroys that.
- **`speak.py` reads the ledger only**, `world.py`-equivalent reads the frame. The
  builder/gate split has to survive the flattening or it was never structural.
- **The output must be diffable and re-runnable.** Generated, never hand-edited, and
  regenerated by `make notebook` — because a notebook edited in place is a notebook whose
  source of truth has moved.

**And the local loop stays primary.** The ARC Prize starter kit's own advice is that
editing in an IDE and running locally gives a real-engine feedback loop in seconds, versus
notebook iteration. `OperationMode.OFFLINE` at 2,000 FPS is the development target; the
notebook is a packaging step, not a workflow.

---

## 7. Swarms — later, and they are step 6

`Swarm` instantiates one agent per game, runs them concurrently on threads, manages the
scorecard lifecycle, and produces replay links. `main.py --agent x --game ls20 --tags "…"`.

That is the population scale, which the build deliberately deferred: **generators cross up,
playback never does.** When it comes in, the membrane rule is the design constraint — what
crosses between agents is a *method*, never a recording of one game's success. A shared
library that accumulates replays is the failure mode with a nice name.

**Deferred, and noted so the deferral is not silent.**

---

## 8. Risks, in the order they will bite

**1 · `GameAction` members are process-wide singletons, and the samples mutate them.**

```python
action.reasoning = "..."        # sets an attribute on the shared enum member
action.set_data({"x":…, "y":…}) # writes action_data on the shared enum member
```

`GameAction.ACTION6` is one object for the whole process. In a **threaded swarm**, two
agents setting coordinates or reasoning concurrently will clobber each other, and the
symptom is an agent acting on another agent's coordinates — which will read as a reasoning
bug, not a race. Copy the member or carry `(action, data, reasoning)` as a tuple and only
touch the enum at the submission boundary. **This is the one I would guard first.**

**2 · The reward channel is nearly always zero.** `levels_completed` moves rarely. That is
`density(R) ≈ 0` on the reward channel by construction, so the curiosity drive fires almost
always and its trigger has to be the *transition* channel or it is useless. `probe.py`
already triggers on the agent's own prediction error, which is the right one.

**3 · Competition mode's `make`-once rule** conflicts with anything that wants to
re-instantiate an environment to retry. Level resets only.

**4 · 16 KB is easy to exceed** with a full cycle's derivation. The validator raises. Budget
the digest and test the boundary rather than discovering it in a scored run.

**5 · The lens will fire on the wrong grid** if the fidelity gate is loosened. The 0.98
constant carries its provenance for a reason; a wrong grid makes located clicks miss and
abort, which is the designed-for failure, but only at a strict gate.

**6 · The submission schema is ambiguous across samples.** Verify before submitting.

---

## 9. The plan

Local first, always. Each stage keeps the gate passing.

| | stage | what |
|---|---|---|
| **A** | the adapter | `arc_world.py` — the eight members over `arc_agi` OFFLINE. `levels_completed` as ground, `frame[-1]` as the board, ints → `GameAction` |
| **B** | perception | carry `perception.py`'s shape: components as slots, permanence by overlap, death on evidence. **Slots at last.** |
| **C** | the lens | `logical_grid.py`'s rule: commit only on a near-lossless round trip, else `None`. This feeds the bracket channel for real |
| **D** | atoms | grid transforms as the atom set. `λ` reported — and here the type graph is genuinely sparse, so unlike the toy world the number should mean something |
| **E** | the reasoning digest | ledger → ≤16 KB payload on `action.reasoning`, with `expect` and `disproof` stated before the action |
| **F** | the harness bridge | `MyAgent(Agent)` wrapping the Tether loop; `choose_action` returns the action the utterance proposed, or no action |
| **G** | the inliner | `build_notebook.py` → one `my_agent.py` + the `.ipynb`, generated and never hand-edited |
| **H** | swarm | step 6. Membrane rule first, code second |

**Done for A–F is the same as it was:** the gate passes on the run's ledger, and the agent
abstains correctly when the atom it needs is not in the closure — which on ARC is not
planted but real, and therefore no longer measurable against a known answer. **That is a
loss of measurement we should feel.** The toy world could score abstention because the
harness knew the truth; ARC cannot. Keeping a planted-unreachable toy slot in the local
suite is how the false-abstention number stays alive.

---

## 10. To gather

- [ ] **The `ARC-AGI-3-Agents` repo itself.** Not checked out anywhere locally, and the
      `Agent` base class's exact contract — constructor args, `MAX_ACTIONS`, what it does
      with the returned action, how `Swarm` threads — is the one thing here I am reading
      second-hand from notebooks rather than from source.
- [ ] The competition page's authoritative submission schema.
- [ ] Whether the Kaggle gateway exposes local/OFFLINE mode at all, or only the online path
      through `gateway:8001` (the samples all set `OPERATION_MODE=online` even though
      Kaggle enforces COMPETITION — worth understanding why).
- [ ] Accelerator choice. T4 default; irrelevant until something needs a GPU, and nothing
      in Tether does.

---

## 11. Composition, and the minimum viable prior set

`[I]` *"If your friend's keys happen to be something non-standard or non-metallic, your
assumed priors would fail and so would your detector. No amount of searching or filtering
with either would help you without more hints. Solvable by humans just means human priors
are required."*

### 11.1 The three priors in the analogy are three different kinds of thing

Read the beach case precisely and it does not contain three instances of one thing:

| | the prior | what kind |
|---|---|---|
| 1 | keys are metallic | **an attribution** — a class has an attribute |
| 2 | a metal detector detects metal | **an instrument** — a sensor that makes an attribute readable |
| 3 | what a standard key looks like | **a recognizer** — a verification predicate |
| — | *"is this your key?"* | **the ground**, supplied by the friend |

**And they do not compose as functions. They join on a shared term.** "Metallic" appears in
1 and in 2, and that shared attribute is the whole hinge — it is what lets a fact about keys
reach an instrument that knows nothing about keys.

> **Composition here is a join on a shared attribute, not `f ∘ g`.**

Which the salvaged grammar already supports and the executable library does not:
`SAME(ATTR, ATTR)` **is** the join, and `CAN(PRED)` is the affordance. The type system is
the joining machinery.

### 11.2 There are three composition spaces. We have one and a half.

| space | signature | what composing in it buys | status |
|---|---|---|---|
| **PREDICT** | `slot × action → slot` | what can be *bet on* | built — this is `gamma.py`'s atoms |
| **RELATE / QUANTIFY** | `ATTR × ATTR → PRED → OBJ` | what can be *stated and wanted* | `grammar.py` exists, unwired |
| **EXTRACT** | `grid × object → ATTR` | **what can be represented at all** | **missing** |

**EXTRACT is the metal detector, and the analogy says it is the decisive one.** Figure 6
says the same thing in its own words: *"Composition explores what the operators reach;
instruments extend what can be represented at all."*

Without extractors there are no attributes; without attributes no predicates can be stated;
without predicates no objective can be posed. **That is Figure 3's chain — perception,
vocabulary, objective — and the break is at link 2, exactly where the figure says chains
usually break, "because it attracts the least attention and the fewest instruments."**

### 11.3 And extractors are what make `λ` mean something

The Stage 1 falsifier fired in the toy world: `λ = V = 7`, because every atom was
`val → val` and the type graph was a single node.

With three spaces the graph is genuinely sparse — `grid → ATTR`, `ATTR × ATTR → PRED`,
`PRED → OBJ`, `slot × action → slot` — and most primitives do not compose with most others.
**`λ < V` for real, and the number starts reporting something.** The instrument was working
in the toy world; it just had nothing to measure.

### 11.4 How to choose from 130 priors without buying the shopping list

`ARC_HUMAN_PRIORS.md` catalogues about 130 with citations. **The danger is not that it is
wrong. It is that it is a shopping list, and shopping lists get bought.** 130 priors times
"it would help on game X" is Cyc, and Cyc is the thing the framework has to answer for
already.

**Two selection criteria, and only one of them survives the OOD objection.**

- ✗ **by performance** — "this prior wins games 7 and 12." This is selection against the
  public set, which is the overfit trap the whole OOD argument names. It also has a second
  failure that is worse: **it makes the experiment unmeasurable.** An agent handed every
  prior never mints, and you cannot tell a composer from a lookup table. The terminal
  condition's ablation clause is exactly this test — wipe Γ, re-run, and see whether the
  win survives.
- ✓ **by structural necessity** — "remove this prior and the *loop cannot run*." Not "wins
  less". Cannot execute: no slots to index `R` by, no way to compute `R` at all, no way to
  tell self-caused from world-caused.

**The second criterion never mentions the game set**, which is why it transfers and why it
is the one to use.

And it is the doctrine restated: *residue is the agent's to close; prefer the agent
deriving it crudely to installing it cleanly; the refined version can be installed next
turn, because it earned it.*

### 11.5 Tier 1 — the loop cannot run without these

Eight, and **four already exist in some form** across the branches.

| | prior | why the loop dies without it | have |
|---|---|---|---|
| 1 | **forward model / efference copy** | this *is* `R = \|Γ(b,a) − o′\|`. No prediction, no residual, no loop | yes |
| 2 | **cohesion → connected components** | without it there are no slots, so `R` cannot be indexed per slot | `perception.py` |
| 3 | **persistence / tracking by overlap** | without it a slot is not the *same* slot next frame, so no history, so no induction | `perception.py` |
| 4 | **self as object; contingency detection** | without it the agent cannot tell its own effects from the world's — every residual is unattributable | `agency.py`, `self_locus.py` |
| 5 | **contact** | the default causal hypothesis. Without it, everything is a candidate cause of everything | no |
| 6 | **change detection** | where to look. Figure 1: the per-object gap is "the only signal that says where to look" | partial |
| 7 | **near-decomposability** | the licence for per-slot at all. Simon 1962, and it is already the ground under `perception.py` | implicit |
| 8 | **uncertainty monitoring** | *know that you do not know.* This is abstention, and it is the product | **built** |

> **Prior 1 deserves its own line.** *"Predict the sensory consequence of one's own action
> and subtract it; the remainder is world-caused"* — von Holst & Mittelstaedt, **1950**.
> **The formula's step 1 is a documented human prior with a seventy-five-year-old
> citation.** That belongs in the paper.

Everything else in the catalogue is **Tier 2**: expressivity, not viability. Tier 2 is what
the agent should have to reach for — and reaching for it is the only evidence that the
composition system works.

### 11.6 The analogy has one bad implication, and correcting it changes the plan

In the beach case the friend is a **cheap verifier**: you can ask *"is this it?"* as often
as you like. The cost is your patience.

**ARC gives no such verifier.** `levels_completed` might not move for five hundred actions.
The reward channel is not merely sparse — it is *absent* for most of a run. So "throw
everything at the validator" is not slow here; it is unavailable.

**Which forces the composition strategy:**

> **Learn the mechanics from the dense channel; use the sparse channel only to select among
> goals.**

Every action yields a transition residual. That is the only dense signal in ARC. So the
priors that matter most are the ones that make **prediction** possible — objects, motion,
contact, persistence — and *not* the ones that make goals expressible. Goal vocabulary is
useless while nothing can be predicted, which is Figure 3's ordering again.

This also settles a question the three-channel design left open: **the curiosity trigger
must be on the transition channel**, because `density(R) ≈ 0` on the reward channel is the
normal state and would fire the drive permanently.

### 11.7 "The agent doesn't know to look in the sand" — and it does not need to

Two answers, and both are already in the framework.

**Where to look is what the residual is for.** Figure 1: *"the gap is measured per object,
not per step. A system that averages across objects has thrown away the only signal that
says where to look."* The changed cells are the sand. No prior required — a per-slot
residual and a probe for when nothing is changing.

**And the concrete case is ACTION6.** It takes `x, y` in 0–63: **4,096 coordinates**, which
is the beach, and an action budget that cannot cover it. Uninformed search there is the
"very long day at the beach", exactly.

> **Extractors collapse it.** Candidate coordinates come from *objects* — centroids, edges,
> interiors, holes, contact points — not from the raw grid. Twenty candidates instead of
> four thousand.

**That is the metal detector, literally**: a prior about where a property lives, turned into
an instrument that narrows the search. And it is the single highest-leverage extractor in
the whole set.

### 11.8 What this means for the plan

Two changes to §9's stages, and one addition.

- **Stage D becomes the important one.** Atoms are not just grid transforms: they are three
  typed families — EXTRACT, RELATE/QUANTIFY, PREDICT — and the type graph is what joins
  them. Report `λ` there and it will finally say something.
- **Stage B carries Tier-1 priors 2, 3, 4, 6**, which mostly exist already.
- **New stage, between D and E: the ACTION6 candidate generator**, sourced from extractors.
  It is small, it is the difference between a tractable and an intractable search, and it is
  measurable on its own — count candidates before and after.

**And a discipline to write into `CLAUDE.md` before any of it:**

> **A prior enters the library only if the loop cannot run without it, or the agent minted a
> crude version first and we are promoting it. Never because it would help on a game.**

Because the moment a prior enters for the second reason, we have encoded an answer, and the
ablation clause will not be able to tell us we did.

---

## 12. How a prior is expressed

`[I]` *"The primitives and priors aren't the problem — we have the text stuff. The problem
is how to express priors. We have the terms. What does that look like coding-wise?"*

Right, and no more catalogues. This section is about **form**.

### 12.1 A prior is not one kind of thing, so it cannot have one code shape

Sorting the catalogue by *what it would have to become in code* gives seven shapes. This is
the load-bearing distinction, because each shape lives somewhere different and obeys
different rules.

| shape | signature | lives in | example priors |
|---|---|---|---|
| **SENSOR** | `frame × obj… → ATTR` | a typed registry | cohesion, containment, symmetry, amodal completion, count |
| **TERM** | `slot × action → slot` | Γ, stamped `prior` | continuity, gravity, momentum, collision, launching |
| **CONSTRAINT** | `prediction → bool` | a filter **before** the bargain | solidity, conservation, identity |
| **TRACKER** | `objs × objs → ids` | perception's identity rule | persistence, occlusion, numerical-vs-featural identity |
| **BIAS** | `candidates → ordering` | search order, **reversible** | simplicity, essentialism, contact-first, take-the-best |
| **BUDGET** | a number with provenance | the constants block | subitizing ≤4, relational complexity ~4, working-memory span |
| **ALREADY THE LOOP** | — | nothing to add | forward model, prediction-error learning, uncertainty monitoring |

**Three consequences that change the build:**

**Most of the catalogue is not sensors.** Perhaps a quarter. Treating all 130 as "things to
implement as detectors" would produce a pile of code that mostly is not detectors at all.

**Biases must be reversible cuts.** Figure 9: *a wrong cut removes the answer and speeds up,
so keep every cut ranked and reversible.* A prior that reorders search is a cut. The gate
already refuses an irreversible one — so biases enter as ranked, reversible cuts or they do
not enter.

**The last row is a trap worth naming.** Several catalogued priors *are already the
architecture*: the forward model is step 1, prediction-error learning is the residual,
uncertainty monitoring is abstention, near-decomposability is the licence for per-slot.
**Adding them as library entries would duplicate the loop inside the loop.** They should be
documented as priors the design already discharges — which is also the strongest thing to
say about the design.

### 12.2 What a sensor is, precisely

```python
@dataclass(frozen=True)
class Sensor:
    name: str
    fn: Callable[..., Any]     # frame, obj, [obj] -> value, or NOT_RESOLVED
    in_types: tuple[str, ...]  # ("FRAME","OBJ") | ("OBJ","OBJ") | ("ATTR","ATTR")
    out_type: str              # COLOUR | COUNT | POSITION | EXTENT | SHAPE | BOOL | ...
    origin: str                # prior | minted | imported
    cost: int                  # called per slot per frame; this is a real budget
```

**Four properties it must have, and each is a rule from a figure:**

- **Typed output.** `ATTR` alone is not enough — `SAME(ATTR, ATTR)` would happily compare a
  colour to a cell count. **The attribute types are what make the join sound**, and the join
  is the whole composition mechanism (§11.1).
- **Total, with an explicit non-reading.** A sensor returns a value or `NOT_RESOLVED`. Never
  a guess, never a default. That is abstention at the sensor level, and it is what lets
  "this instrument cannot see it" propagate up instead of becoming a wrong attribute.
- **Composable.** A sensor's output can feed another's input, which is what makes the
  registry a closure rather than a list.
- **Priced.** It runs per slot per frame; a sensor that costs more than the residual it
  resolves is not worth having, which is the same bargain one level down.

**The attribute type set** — small on purpose, because it is the join vocabulary:

```
COLOUR   COUNT   POSITION   EXTENT   SHAPE   BOOL   DELTA   AXIS   RATIO
```

### 12.3 The minimum initial sensor set

Criterion unchanged: **the loop cannot run without it.** Working from what step 1 actually
needs — slots that exist, persist, carry a state you can predict, and a way to tell your own
effects from the world's:

| | sensor | type | why the loop dies without it |
|---|---|---|---|
| 1 | `components(frame)` | `FRAME → [OBJ]` | no slots, so `R` cannot be indexed per slot |
| 2 | `colour(obj)` | `OBJ → COLOUR` | part of the slot's predictable state |
| 3 | `position(obj)` | `OBJ → POSITION` | part of the slot's predictable state |
| 4 | `extent(obj)` | `OBJ → EXTENT` | part of the slot's predictable state |
| 5 | `shape(obj)` | `OBJ → SHAPE` | identity under recolour; normalized offsets |
| 6 | `overlap(a, b)` | `OBJ × OBJ → RATIO` | tracking — the slot is the *same* slot next frame |
| 7 | `delta(a, b)` | `OBJ × OBJ → DELTA` | motion, and the contingency test for self |
| 8 | `touching(a, b)` | `OBJ × OBJ → BOOL` | contact, the default causal hypothesis |
| 9 | `changed(f1, f2)` | `FRAME × FRAME → REGION` | where to look |

**Nine.** Everything else in the catalogue should be reachable by composing these, or it is
genuinely out of reach and the agent should say so.

Note what is *not* here: symmetry, containment, holes, counting-by-colour, alignment. All of
them compose from the nine — `inside` from position and extent, `count` from components plus
a colour filter, `symmetry` from shape plus a reflection. **They are Tier 2 and the agent
should have to reach for them**, because reaching is the only evidence the composition
system works.

### 12.4 How the agent invents a sensor

This is where Figure 6 stops being a slogan:

> *An instrument is not built from a description. It is improved from a worse instrument
> already returning something. The question is not whether a sensor could exist, but whether
> anything, at any resolution, is already returning something that fails to resolve.*

**Which gives an exact, implementable trigger:**

> **Two slots with the same attribute vector and different residuals.**

The current sensor set says those slots are identical; the world says they are not. The
vocabulary *fails to resolve* them. That is a reading that already exists and does not
resolve — precisely the condition the figure names — and it is `orthogonality(R, Γ) > 0` in
the sensor space rather than the term space.

Two remedies, and they are the two branches of step 7:

- **INWARD, and mintable:** compose a new sensor from existing ones that *does* split them.
  `parity(position)`, `ratio(count(colour=a), count(colour=b))`, `holes(shape)`. Inside the
  closure, priced by the same bargain.
- **OUTWARD, and not available here:** a primitive reading of the raw grid that no
  composition of the nine yields. That needs IMPORT, there is no second frame, and the
  honest output is **unreached**.

**Which makes the initial nine a ceiling, and a measurable one.** Whatever is not reachable
by composing them is genuinely unreachable, and the agent should abstain on it — correctly.
That restores the abstention measurement ARC otherwise takes away (§9): we cannot know the
game's true rule, but **we can know the closure of our own sensor set**, and therefore we
can still score whether abstention was correct.

**And it gives the selection criterion for the nine**: not "which priors are true" but
**which small set has the largest closure**. Which is the `λ` argument, one level down.

### 12.5 Sketch — what it looks like in the code that exists

```python
# sensors.py -- the registry. A prior in SENSOR shape.
COMPONENTS = Sensor("components", _components, ("FRAME",), "OBJS", PRIOR, cost=8)
TOUCHING   = Sensor("touching",   _touching,   ("OBJ","OBJ"), "BOOL", PRIOR, cost=2)

# gamma.py -- unchanged. A prior in TERM shape is a molecule, already supported:
MOLECULES = [("continuity", ("delta", "add", "wrap")), ...]   # origin=prior

# the mint, unchanged in shape -- it now searches the sensor closure too, and the
# guards read the same: support (two slots differ and we cannot tell them apart),
# reachability (a composition of sensors splits them), novelty (not already a sensor).

# constraints run BEFORE the bargain, not inside it
def solidity(pred: dict[str, Any]) -> bool:
    return len({p for p in pred.values()}) == len(pred)     # no two slots in one cell
```

**The shape of the existing build does not have to change.** `Sensor` is `Atom` with real
types instead of `val → val`; the sensor closure is the same enumerator; the bargain, the
guards, the ledger and the gate are untouched. What changes is that the type graph becomes
sparse — which is the thing that was making `λ` uninformative.

### 12.6 The salvage hunt, scoped

`[I]` *"I have a lot of trepidation about bringing in any code because it's likely the wrong
build."*

**Agreed, and the rule should be explicit: salvage the shape, never the code.** Every prior
attempt encoded assumptions about a build that is not this one, and importing a working file
imports its assumptions invisibly. Three branches have already shown that a component can be
present, correct, and load-bearing for the wrong architecture.

**What a salvage hunt should return** — a list, not a patch:

| for each candidate sensor | |
|---|---|
| what it reads | in a sentence |
| its type signature | `in_types → out_type` in the vocabulary above |
| which of the seven shapes it is | it may not be a sensor at all |
| whether it composes from the nine | if yes it is Tier 2 and should be minted, not installed |
| the receipt | any measured claim the original made, with where |
| the trap | what it assumed about its own build |

**Where to look**, in rough order of expected yield: `redux_arch/dsl.py` (1,093 lines — the
typed predicate DSL and its extractor basis, the closest thing to a sensor registry already
written), `effects.py` (the atom constructor and its classifiers), `relation.py`,
`referent.py`, `loci.py`, `transform.py`, `boundary.py`, `affordance.py`, and `perception.py`
plus `logical_grid.py` on `new-horse`.

**Beware:** the tree contains orphaned and broken code, and `policy.py` alone is 3,274 lines
of the thing we are deliberately not rebuilding. A file being large is not evidence it is
load-bearing; on that tree it has usually been the opposite.

---

## 13. The salvage hunt — findings

Read on `Ouroboros-Redux @ Nexus`: `redux_arch/{dsl, relation, referent, loci, boundary,
affordance, transform, progress, operator_effect}.py`, plus `new-horse`'s `perception.py`
and `logical_grid.py` from earlier. **Shape only. No code carried.**

### 13.0 The headline: the sensor registry already exists, and it is better than §12's sketch

`dsl.py` is not a predicate list. It is **extractors + comparison primes + type-gated
composition**, which is exactly the mechanism §12 proposed, built, with a design note saying
why:

> *"Relational atoms are not a hand-list; they are COMPOSITIONS of typed before-state
> EXTRACTORS under comparison PRIMES. `{SAME_ROW, SAME_COL, SAME_COLOUR}` = EQ over
> extractor pairs — **re-derived, not hand-written**; LT over a position axis **invents** an
> ORDER relation with no ORDER atom ever written."*

Three properties to carry whole:

- **The type gate is the join.** Only same-type extractor pairs compose, so `row` compares
  to `row` and never to `colour`. That is §11.1's join discipline, enforced.
- **Abstention propagates by mechanism, not by convention.** An unresolved slot reads
  `None`, and `_compose_atom` makes any comparison over a `None` evaluate **False** — so an
  unresolved socket switches off every relation built on it. *"No special case, no second
  convention."*
- **The tautology guard is a TYPE property.** `Context` carries only before-state, and
  there is no accessor to the outcome, so *"a φ that predicts by peeking is not
  constructible."* **This is stronger than both other branches' versions** — `v4-cold` used
  an import-time AST wall, `new-horse` a runtime raise; this one makes the bad φ
  unrepresentable.

### 13.1 The table

`SHAPE` uses §12.1's seven. **`from 9?`** = reachable by composing the minimum set, so
Tier 2 and *mintable* rather than installable.

| # | source | what it reads | signature | shape | from 9? | note |
|---|---|---|---|---|---|---|
| 1 | `dsl` | slot colour / row / col | `SLOT → COLOUR\|ROW\|COL` | SENSOR | **yes** | positional readers, `None` = abstain |
| 2 | `dsl` | **`size`** — 0th moment, pixel count | `SLOT → M2_SIZE` | SENSOR | yes | = `extent` |
| 3 | `dsl` | **`ext_row` / `ext_col`** — 2nd central moments as lengths, `2·√μ₂₀` | `SLOT → M2_EXT` | SENSOR | **no** | genuine new reading |
| 4 | `dsl` | **`orient`** — principal-axis angle, integer degrees `(-90,90]` | `SLOT → M2_ORIENT` | SENSOR | **no** | **import-class** |
| 5 | `dsl` | **`ecc`** — eccentricity of the moment ellipse, integer percent | `SLOT → M2_ECC` | SENSOR | **no** | **import-class** |
| 6 | `dsl` | EQ / LT comparison primes | `ATTR × ATTR → BOOL` | SENSOR | — | the composer; EQ re-derives, LT invents |
| 7 | `relation` | `_bfs_dist` — 4-connected distance over *passable* cells | `POS × POS × FRAME → COUNT` | SENSOR | **no** | **the highest-value import.** Reachability as a reading |
| 8 | `relation` | `_line_bg_gap` — background cells on the straight segment `a→b` | `POS × POS → COUNT` | SENSOR | borderline | needs a rasteriser primitive |
| 9 | `relation` | `_levenshtein` over token sequences | `SEQ × SEQ → COUNT` | SENSOR | **no** | ORDER-native discrepancy |
| 10 | `relation` | `_contains`, `_overlap`, `_bbox_*` | `OBJ × OBJ → BOOL` | SENSOR | **yes** | composes from position + extent |
| 11 | `progress` | `ProgressProbe` — the colour whose count rises most **monotonically** | `FRAME* → COLOUR` | SENSOR | yes | see 13.3 — **do not let this become the ground** |
| 12 | `transform` | `detect_global_transform`, `_colour_perm`, `_detect_translation` | `FRAME × FRAME → T` | SENSOR | **no** | whole-frame T; a few bits where per-object costs everything |
| 13 | `affordance` | `EffectAffordance` — which actions are effective / no-ops / **undo** | `(before,action,after)* → ACTION→CLASS` | SENSOR | yes | read straight off the transition residual |
| 14 | `referent` | panels, ring panels, legends, endpoints, node pairs, sequences | `FRAME → [REGION]` | SENSOR | mostly | **archetype-derived — see 13.4** |
| 15 | `referent` | `_context_of`, `_same_context` — which named region a locus sits in | `POS × [REGION] → IDX` | SENSOR | yes | topology, from `contains` |
| 16 | `loci` | `LociTracker` — stable ids across translate / recolour / reshape | `OBJ* × OBJ* → IDS` | **TRACKER** | — | colourless shape signature; identity ≠ colour |
| 17 | `boundary` | `BoundaryDiff` — TRANSFERRED / NOVEL / GONE by tracked id | `IDS × IDS → BINS` | **already the loop** | — | this **is** ROUTE. See 13.2 |
| 18 | `boundary` | `Quarantine` — park unresolved under a **decay bound** | — | already the loop | — | the park branch, with a wake budget |
| 19 | `relation` | `RelationBank` — hold five relation hypotheses, select the one whose discrepancy is confidently shrinking | — | **BIAS** | — | archetype-derived; the *selection rule* is general, the five are not |
| 20 | `operator_effect` | site → effect-on-workspace, learned by intervention | — | TERM | — | archetype-derived framing, general idea |

### 13.2 `BoundaryDiff` is ROUTE, and it carries a discriminator we do not have

`loci.py`'s own statement of why it exists is the framework's, in the framework's words:

> *"Without retained identity there is no diff, only two unrelated piles of residual."*

And `boundary.py` partitions by tracked identity into TRANSFERRED / NOVEL / GONE — three of
the four bins — with one concrete rule we lack:

> **A grown action set (2 → 4 → 8) is the canonical broken-by-REBINDING case** — re-fit the
> bindings, do not mint — *distinguishable from broken-by-MECHANISM, which owes a mint.*

That is a real why-not-the-neighbour discriminator for ARC, where `available_actions`
changes per frame. Take it.

Note also `GONE` is a **fourth** outcome the four bins do not name. A slot that vanishes is
neither held, novel, rebinding, nor mechanism. Worth deciding where it routes.

### 13.3 `ProgressProbe` is the answer to sparse reward — and the fastest way to wreck the ground

§11.6 said ARC's reward channel is absent for most of a run, so the loop must live on the
transition channel. `progress.py` offers a third option:

> *the progress signal is the COLOUR whose cell-count rises most MONOTONICALLY across the
> stream* — bars filling, grids filling with correct tiles, corridors filling with a path,
> all of which are "a colour's count only goes up". With a confidence gate against noise.

**This is genuinely clever and it is exactly the shape of a Goodhart disaster.** A dense
signal that correlates with winning, computed by the agent, from the frame.

> **Figure 2: a proxy metric is an anchor that updates, and an updating anchor collapses
> triangulation into a mirror.**

So the placement has to be explicit and it is not the obvious one:

- ✓ **as a SENSOR** whose reading feeds a hypothesis — "this colour's count rising is what
  progress looks like here" — a candidate, **settled by `levels_completed` and nothing
  else**
- ✗ **as the ground, or as anything the mint bargain is priced against.** The moment the
  agent optimises the probe, the probe stops measuring and the run becomes unreadable

Worth a gate check of its own: **no entry may cite a sensor reading as a settle event.**

### 13.4 The split that matters most: domain-general vs archetype-derived

The files divide cleanly, and several **say which they are in their own docstrings**.

| domain-general — safe to take shape from | archetype-derived — flag hard |
|---|---|
| `dsl.py` — "names no game"; the extractor basis is structural | `relation.py` — the five relations {MATCH, CONNECT, ORDER, ARRANGE, REACH} come from a **GIF-archetype audit of the 23 games** |
| `loci.py` — identity by shape, colourless | `referent.py` — panels / legends / endpoints are the shapes *those* games use |
| `boundary.py` — partition by identity | `operator_effect.py` — "the shared driver for **~18 of the 23** zero-win games" |
| `affordance.py` — "effective is just *this changed the board*" | |
| `transform.py` — "privileges no colour or position" | |
| `progress.py` — one structural feature, no game id | |

**The right-hand column is selection against the public set, stated in its own comments.**
That is the OOD trap and the "a fix that helps one case is an answer wearing a fix's
clothes" clause, and it is the single most useful thing this hunt found — because those
three files are also the most *seductive*, being the ones that name the actual solving
concepts.

**But the right-hand column is not worthless — its second-order content is general.** Strip
the five relations from `RelationBank` and what remains is a real mechanism:

> **hold several goal hypotheses at once, express each as a scalar discrepancy that is zero
> exactly when satisfied, and select the one whose discrepancy is confidently shrinking
> under play.**

That is the marketplace with a currency, and it names no game. **Take the selector, leave
the five.** Same for `referent.py`: the *idea* that a goal is often specified by a region of
the board rather than by the reward is general; the panel/legend/endpoint detectors are not.

### 13.5 What I would actually take, in order

**Tier 1 — the shape, more or less as-is:**

1. **`dsl.py`'s extractor/prime/type-gate architecture.** The single best thing in the tree
   for this build. It *is* §12, already thought through, with the abstention rule and the
   tautology-as-type-property attached.
2. **`loci.py`'s identity rule** — colourless shape signature, survives recolour and reshape.
   Slots are not slots without it.
3. **`boundary.py`'s partition** as ROUTE's ARC implementation, with the action-set-growth
   discriminator.
4. **`affordance.py`'s effective / no-op / undo classification** — three bits per action,
   read off the residual we already compute, and it directly narrows the action set.

**Tier 2 — four genuine imports, because they do not compose from the nine:**

5. `bfs_dist` — passability-aware distance. **The highest-value single reading in the list**,
   because "can I get there" is the question a navigation game turns on and no composition
   of the nine answers it.
6. Second moments — `orient`, `ecc`. New readings of shape, cheap, and they discriminate
   where colour and bbox cannot.
7. `detect_global_transform` — where a per-object model has enormous residual and a
   whole-frame `T` has almost none.
8. `levenshtein` — only if a sequence type enters the vocabulary at all.

**Deliberately not taking:** the five relations, the referent detectors, the operator-effect
framing, and anything in `policy.py` (3,274 lines of the thing we are not rebuilding).

### 13.6 Two warnings from the source

- **The extractor registry is POSITIONAL and append-only.** `dsl.py` notes that inserting a
  name rather than appending renumbers the universe, making it *"a DIFFERENT SEARCH at the
  same size"* — so stored terms and determinism receipts silently stop meaning what they
  said. If we adopt a registry, adopt the append-only rule with it.
- **The cost is quartic in the operand count, and they capped it at 4.** `enumerate_predicates`
  is `combinations(universe, 2)` and the universe is quadratic in N, so N=4 is roughly 10× the
  search of N=2. Their own note: *"a vocabulary bought with 10× the agent's lifetime is a net
  loss even if it is the right vocabulary."* That is the REACHABILITY cost model, measured,
  and it should set our depth budget rather than a guess.

---

## 14. Composition — the part that is sketchy, and why

`[I]` *"When the agents are taking the test they won't have you or me, and will need to
compose these into actual functionality or fresh shortcuts to stack these into routines. That
composition part seems sketch to me."*

It is sketchy, and the instinct is right for two reasons. One is a defect in the code I
already wrote; the other is a whole missing algebra.

### 14.1 The defect: minted terms never re-enter the search

`gamma.py`, both at the seed and at every extension:

```python
frontier = [(a,) for a in self.atoms if a.in_type == in_type]
...
nxt += [chain + (a,) for a in self.atoms if a.in_type == chain[-1].out_type]
```

**`self.atoms`. Never `self.library`.** A minted term is stored, bound to a slot, and used
for prediction — and it is **never available as a building block for a deeper term.**

> **The library grows. The reach does not.**

Which makes composition exactly as flat on cycle 500 as on cycle 1: always depth ≤ 3 over
the same primitives. There is no stacking, no shortcut, no routine. **That is the thing the
question is pointing at, and it is a real bug rather than a design gap.**

### 14.2 Chunking — and it is the exponent, not the coefficient

The fix is one line in principle and it is the whole mechanism:

> **An accepted, settled term re-enters the search as a single unit.**

The closure does not change — Figure 6 is safe, **MINT still cannot add an atom**. What
changes is what is *reachable at a given budget*:

| | search depth 3 over… | effective atom depth |
|---|---|---|
| atoms only | 3 primitives | **3** |
| after minting `A∘B∘C` | 3 units, one of which is 3 long | **up to 9** |
| after a few generations | 3 units of chunks of chunks | **grows multiplicatively** |

**That is the difference between lowering the coefficient and lowering the exponent**, which
the bill ledger names as the frontier. Depth stays 3; reach compounds.

And it is a documented human prior sitting in the catalogue already — *"Chunking: recognize
larger units with expertise, Chase & Simon 1973."* It is also Soar's chunking and
DreamCoder's library learning, so it is the well-trodden part of this design rather than the
speculative part.

**The gate on promotion is already written and it is `citability`.** Q7's rule — *a candidate
may be held but not cited* — does real work here:

- **unsettled** term → usable as a slot's binding, **not** as a building block
- **settled by the ground** → promoted into the search vocabulary

So junk cannot expand the search. Only what the ground has paid for becomes a shortcut, and
the ablation clause stays meaningful because the chunk library is exactly what gets wiped.

### 14.3 The missing algebra: a predicate is not a routine

The deeper problem. Everything built so far composes objects of one shape:

```
sensor    state → attr
predicate state → bool
term      slot × action → slot
```

All three are **pipelines**, and pipelines compose by chaining. But *"go to the door, press
the button, come back"* is none of those. It is a **routine**: `state → action`, with
sequence, conditions and repetition. **You cannot build it by chaining functions**, which is
why the composition story feels thin — half the objects the agent needs are not in the
algebra.

The minimal algebra that fixes it is four constructors:

```
Routine ::= Act(a)              a primitive action
          | Seq(R₁, R₂)         do, then do
          | When(P, R)          guarded by a predicate
          | Until(P, R)         repeat until the predicate holds
```

**`Until` is the one that matters.** It turns a one-step action into a *behaviour with a
termination condition*, which is what "navigate to X" actually is. Without it every routine
is a fixed-length script and depth explodes on the first navigation problem. With it,
"navigate" is one chunk of depth 2.

And the pieces are already in the vocabulary: `P` is a predicate from the sensor basis, `a`
is an available action, `CAN(PRED)` is the affordance that says the guard is satisfiable.

### 14.4 Three spaces, three triggers, one bargain

The whole composition story, stated once:

| space | object | composes by | minted when | priced against |
|---|---|---|---|---|
| **SENSE** | sensor | `prime(extractor, extractor)`, type-gated | two slots share an attribute vector and differ in residual | discriminability |
| **PREDICT** | term | chaining + **chunking** | ROUTE says `BROKEN · mechanism` | transition residual |
| **ACT** | routine | `Seq / When / Until` | a goal residual no routine closes | goal residual |

**One bargain across all three** — `|φ| + |R|φ| < |R|` — which is what `molecule.py` already
demonstrated by pricing a quantified objective with the same two-part MDL one level up. Three
spaces, one acceptance test, one ledger, one gate.

And **chunking applies in all three.** A settled sensor composition becomes a readable
attribute. A settled term becomes a building block. A settled routine becomes a callable
step inside a bigger routine. *That* is stacking, and it is the same rule three times.

### 14.5 What gets gated, and how an import actually enters  ·  ⚠ SUPERSEDED BY §15.2

The four genuine imports from §13.5 — `bfs_dist`, second moments, global transform,
Levenshtein — **should not be installed at build time.** Installing them is deciding in
advance what the agent will need, which is the encode-the-answer failure with better
manners.

**Proposal: the bench.**

> A curated set of primitives that are **not in Γ**, that the agent cannot reach, and that
> can only enter by an IMPORT ceremony that cites the residual it closes.

| | |
|---|---|
| **the gate** | the shadow test: an import enters only against a residual **recorded before the import was chosen**. The ledger's sequence numbers prove the ordering, so it is checkable rather than promised |
| **the debit** | Figure 6 — an import is debited against the source frame's independence, and the bench is authored by us, so the debit is heavy and should be recorded as such |
| **why it is honest** | the agent did not have it, the run says so, and every pull is counted |
| **what it buys** | a real answer to the ablation clause. Wipe Γ and the bench remains, so *composed it* and *was handed it* stay distinguishable |

And it makes the bench the stand-in for the peer frame that a single agent does not have —
Figure 6's *"external source: nature · corpus · peer frame."* A curated corpus is the honest
version of that, provided the ceremony is recorded.

**A gate check to add:** an import entry must cite a prior residual by sequence number, or it
is refused. That closes the door on quietly widening Γ between runs.

### 14.6 On flags — the old build's discipline, and the trap in it

Every vocabulary addition in `redux_arch` is behind an environment variable — `OURO_COMPOSE`,
`OURO_VOCAB_MATCH`, `OURO_OPERANDS`, `OURO_PROBE` — with a stated reason that is genuinely
good: *"default OFF keeps every existing MDL decision and the suite byte-for-byte unchanged;
ON is A/B-able."*

**And that is also how `v4-cold` ended up with its gate in shadow mode.** A default-off flag
is a decision deferred, and deferred decisions accumulate into a build where the interesting
half never runs.

So: **no flags on the core path.** A flag is permitted only for something being A/B'd against
a measured baseline, and it carries an expiry — a date or a run count after which it is
removed or promoted. A flag with no expiry is shadow mode with a nicer name.

### 14.7 What to measure, so "composition is working" is not a feeling

Four numbers, all cheap, none of them frame-internal in the forbidden sense — they describe
*reach*, not success, and the ground still settles everything:

| number | says |
|---|---|
| **effective atom depth** = Σ chunk lengths at search depth 3 | whether chunking is compounding. Flat = the library is not being reused |
| **chunk reuse count** | how often a settled term appears inside a later mint. **Zero is the failure signature**, and it is the one that would otherwise look like progress |
| **bench pulls, per primitive** | which imports the agent actually needed. A never-pulled bench item was a guess |
| **unreached rate over time** | should fall as chunks accumulate — and if it does not, reach is not growing whatever the library size says |

**Chunk reuse is the one I would put on the wall.** A library that grows and is never reused
is a catalogue, and a catalogue is what "the agent is composing" looks like when it is not.

### 14.8 What this changes in the plan

- **Fix `enumerate_closure` first.** It is the smallest change with the largest effect, and
  everything else in this section depends on it. Settled terms seed the frontier and extend
  it; unsettled ones do not.
- **Add the routine algebra** — four constructors — as its own composition space with the
  goal residual as its trigger. This is new build, not salvage.
- **Ship the nine, bench the four.** Import by ceremony, recorded.
- **Report the four numbers every run**, next to the abstention rate.

---

## 15. Corrections: the game as a source, no gating, and where the routine algebra already lives

Four of these came from you and three of them correct me.

### 15.1 The game *is* an import source. I had this wrong.

I have been writing that a lone agent has no IMPORT channel — Mars, no peer frame, step 7
OUTWARD closed. **Figure 6 does not say that.** It names three external sources:

> **external source: nature · corpus · peer frame**

**Nature is on the list, and the game is nature.** So IMPORT was never closed; I collapsed
"no peer frame" into "no import" and it does not follow.

**And there is a concrete, enumerable channel — the action set.** `available_actions` changes
per frame. When a game goes 2 → 4 → 8, **the agent has just been handed four new operators**,
and `atoms(Γ)` grew by contact with something outside it. That is an import, by the
definition, from nature.

Three channels the environment actually imports through:

| channel | what arrives | is it an import? |
|---|---|---|
| **action-set growth** | new operators | **yes** — atoms, straightforwardly. The closure expands |
| **value-domain growth** | a colour never seen before | **yes** — it extends every parameterised atom family (`HAS_COLOUR(c)`) |
| **instrument extension** | a sharper reading of something already registering | **inward**, not import — but available, and available to a lone agent |

**One thing that stays closed, and the distinction is worth keeping.** The game is not a
*peer frame* in Figure 8's sense: you cannot read its closure, only its outputs, so there is
no union surplus to search and no triangulation. That channel is what a **swarm** would open,
and it is the honest reason swarms are on the roadmap rather than a nicety.

**On the game being both source and ground.** It is, and that is not a collapse. Figure 2's
failure is an anchor that *updates in response to a frame*. The game's mechanism does not
move because the agent believes something, and *"did I win"* is constitutively about the
game — which is the legitimacy test from the audit. Sound anchor, and a source of atoms, at
the same time.

`boundary.py` already half-saw this: it files a grown action set under REBINDING. **Both are
true at once** — the atoms were imported, *and* existing terms need re-fitting to the wider
set. Worth recording as two events rather than one.

### 15.2 No gating. The bench was wrong, and the reason is decisive.

> *"At the private set you or I are unable to ungate its functions. The agent shouldn't have
> to earn logic — it should be able to get it as soon as the understanding of what to look
> for is reachable."*

**This kills the bench, and it kills it on a fact rather than a preference.** The bench
required an import ceremony. Who performs it at test time? Me. I am not there. So the bench
is either never pulled — dead weight — or auto-pulled, in which case the ceremony was theatre
and I have built a gate that only gates during development. **That is shadow mode again, in a
third costume.**

Withdrawn.

**And the reframing is better than the thing it replaces.** The gate was never supposed to be
permission; it was supposed to be *provenance*. The condition that does that work is not
"has it earned this" but:

> **Can it characterise the gap? Then it can have the tool.**

Which is Figure 6's own test, and I had it quoted two sections earlier: *the question is not
whether a sensor could exist, but whether anything, at any resolution, is already returning
something that fails to resolve.* **The residual is the request.** Nothing is withheld;
retrieval simply requires you to say what you are missing.

### 15.3 What replaces it: retrieval keyed by the characterised residual

The whole library is present and reachable. **What you cannot do is ask for a primitive by
name** — you get it by describing the gap it fits, and Figure 9 already specifies the
procedure:

> *R, described: **arity · symmetry · scale** → the frame whose closure predicts it → one
> lookup. R's own predicates name the habitat that holds φ*. **Matching is a one-pass check,
> not a search.***

So the corpus is **indexed by residual shape**, not by name:

| index key | from |
|---|---|
| type signature | `in_types → out_type` in the sensor vocabulary |
| arity | how many slots the gap involves |
| what varies / what is invariant | the residual's own structure |
| effect shape | what changed, not what caused it — *describe in effect terms* |

`[I]` *"I've talked about how to search the library or corpus in v4-cold, but I don't know if
it was properly executed in code."* **It was designed and not wired.** `fabric.py` has
`priors()` — visible ideas for a game across collective, personal and kin — but keyed by
*game*, not by residual shape. And `Ariadnes-Mirror-MCP` has the real thing: **six `F*`
coordinates** (resource pressure, actor complexity, information asymmetry, coupling
tightness, time pressure, boundary permeability) for locating a problem and finding
structurally similar solutions **by structural distance, not surface similarity.**

That is the retrieval mechanism, built, for a different corpus. Pointing it at a primitive
library is the missing wire — and the coordinates for *this* corpus are the sensor-type ones
above rather than the coordination-theory ones.

**And this keeps everything the bench was protecting.** A retrieval requires a characterised
residual, so it is a *derivation step*: it cites the gap, it lands in the ledger, and the gate
can check that the citation preceded the pull. **A lookup that had to describe the gap first
is not a lookup, it is a diagnosis with an answer attached** — and the ablation clause still
reads clean, because what gets wiped is the library and what remains is the ability to
describe.

### 15.4 Soar and DreamCoder — what specifically

**From Soar:**

- **impasse → subgoal → chunk.** When the current operator cannot proceed, open a subgoal; on
  resolution, compile the result into a new production. That is `BROKEN · mechanism` → mint,
  and it is the same mechanism arrived at in 1987.
- **Its documented failure is our delta.** Soar's chunks go overgeneral and expensive. The MDL
  bargain is exactly the missing filter — *a term that explains one occasion perfectly fails
  the bargain*. Worth saying in the paper: we are Soar's chunking with an acceptance test.

**From DreamCoder, and this closes an open gap:**

- **The abstraction sleep phase refactors the library** — it finds subexpressions common
  across many solutions and names them as new primitives, scored by compression over the
  whole corpus of solutions. **That is §8.8's "nothing refactors Γ", answered.**
- And it is *the same bargain at a different scope*: per-mint chunking (§14.2) is local and
  greedy; DreamCoder-style refactoring is periodic and global, and it finds chunks no single
  mint could see because the evidence is spread across episodes.
- **Its recognition model is the fluent proposer** (Q4b), trained wake/sleep on the library's
  own output. Already designed; DreamCoder is the citation for why it works.

So: **local chunking on accept, global refactor on a schedule.** Two operations, one
objective, and the second one is the voluntary payment the ledger says nobody schedules.

### 15.5 The routine constructors are already NSM primes — the grammar is just missing its verbs

> *"Would NSM grammar help for the state-action sequence and the four constructors?"*

**Yes, and it is better than a separate combinator language.** Look at what the current basis
actually contains:

```
Relation  BE_AT  TOUCH  BECOME  BECAUSE
Quality   SAME   OTHER  NOT
Modality  EXIST  CAN
Quantity  ALL    SOME   ONE     NONE
```

Kant categories, thirteen primes — **and every one of them describes a STATE.** There is not
a single action or time prime in the basis. **The grammar has no verbs**, which is precisely
why routines would not fit in it and why I reached for a separate algebra.

NSM proper has them, and has had them all along:

| constructor | NSM prime(s) | in the basis today |
|---|---|---|
| `Act(a)` | **DO**, MOVE, HAPPEN | **no** |
| `Seq(R₁, R₂)` | **BEFORE**, **AFTER** | **no** |
| `When(P, R)` | **IF** | **no** *(`BECAUSE` is causal, not conditional — different prime)* |
| `Until(P, R)` | **FOR SOME TIME** + NOT | **no** |
| the guard's satisfiability | CAN | yes |

> **The routine algebra is not a new language. It is the missing third of the one already
> chosen** — the action and time primes that a Kant-category read of NSM drops.

Six primes — `DO`, `MOVE`, `HAPPEN`, `IF`, `BEFORE`/`AFTER`, `FOR SOME TIME` — and routines
compose in the same type system, type-check through the same `compose()`, get priced by the
same bargain, and chunk by the same rule. **One grammar, three spaces**, instead of a
grammar plus a bolted-on combinator language.

This also explains a symptom in the salvage: `relation.py` had to hand-write five *relations*
because the basis could express what a state looks like and not what a sequence of doings
looks like.

### 15.6 The proposer, conditioned on the residual

> *"Are TinyStories able to accept problems and imagine conclusions? It might help bridge the
> gap so agents don't have to randomly guess, or do classification lookup, or gradient
> descent."*

**Those three are exactly the alternatives it displaces**, and the ledger already names the
move: *aiming the variation with a spec lowers the exponent.* Not guessing (blind), not
lookup (retrieval only reaches what is indexed), not gradient descent (needs a differentiable
objective this has not got).

**And conditioning is the part already measured.** The design doc reports 99.7% well-typed
against 0% for random tokens, and — the relevant number here — **seeding a forced prefix and
measuring valid completion: `ALL`→99.8%, `SOME`→100%, `BECAUSE`→99.8%, and awkward seeds like
`NOT NOT`→99.8%.** Conditioning does not wash out, for a structural reason: generations are
one short term against a 32-token window, so the seed never scrolls off.

**What changes for ARC is only what you condition on.** Not a verified term — **the
characterised residual** from §15.3. Seed with the gap's signature, sample candidates,
type-check them free, and price them with the unchanged bargain.

**And the training pairs are already being written.** Every `accept` entry in the ledger is a
`(residual → term that closed it)` pair. That is DreamCoder's dream phase with the corpus
generated by play rather than by fantasy, and it is stage 2 of the proposer's own two-stage
plan.

**Two limits to keep attached, both from the design doc itself:**

- **Proposes, never scores, never promotes.** Its perplexity is a training signal, not an
  acceptance metric. It cannot corrupt the ground because it never touches it.
- **It front-loads recombination inside Γ's envelope and does not solve true transfer.** *"You
  can only project worst cases you can express."* It makes composition cheaper; **only import
  moves the wall** — and per §15.1, the game is doing that anyway.

### 15.7 What changed in the plan

| | was | now |
|---|---|---|
| IMPORT | closed for a lone agent | **open via nature.** Action-set growth and value-domain growth are import events, and should be recorded as such |
| the bench | curated, gated, ceremony | **withdrawn.** Full library, retrieval keyed by characterised residual |
| the gate on retrieval | permission | **provenance** — the citation must precede the pull, and the ledger proves it |
| routine algebra | four new constructors | **six NSM primes** added to the existing basis. One grammar |
| library refactor | unbuilt (§8.8) | DreamCoder abstraction phase, same bargain, global scope |
| proposer conditioning | seed with a verified term | seed with the **characterised residual** |
| swarms | "later" | **the only channel that opens the peer frame.** Now has a stated reason, not just a roadmap slot |

---

## 16. The level is a habitat, and enumerating it is the job

`[I]` *"The agent is trying to sniff out what habitat or ecosystem or system is this world
or level made of, and how does it work. What are the keys to mastering the environment's
levers."*

That is Figure 11 pointed at a game level, and it converts several loose intentions into
things that can actually be built. Five of them, plus one place the metaphor should stop.

### 16.1 `available_actions` is three sensors in one, and it is the cheapest data in the game

I had it as an import channel. It is also two other things, and all three are read from a set
of at most seven booleans — **no pixels involved**.

| read | what it tells you |
|---|---|
| **the set** | which operators exist right now → the import channel (§15.1) |
| **the delta** | *the previous action changed the world's gating.* A causal readout with no perception at all |
| **the pattern over time** | which conditions gate which — a **precondition structure** |

The third is the one worth building. If `ACTION5` only ever becomes available after some
`ACTION6` at some place, that is a **precondition edge**, learned from a sequence of tiny
sets rather than from 64×64 grids.

> **A precondition lattice over ≤7 operators is the cheapest structural model in the whole
> problem, and it answers exactly the question — "what conditions are gated, and do they
> build on each other?"**

**Budget it.** The lattice is over subsets, so it is exponential in principle; the useful
version is pairwise edges — *"a became available after b"* — with counts, not the full
subset order. Pairwise is 49 cells and it is enough to see a chain.

### 16.2 Avatar or actuator is a per-step read, never a label  ·  ⚠ AMENDED BY §18.3

`[I]` *"an avatar, or a non-avatar GUI button system."*

`THE_MISSION` already rules on this and the ruling is strict:

> *The ONLY legitimate distinction is topical I/O: is there an **avatar** my directional
> actions translate, or do I act through a **click actuator** — and even that **BLENDS
> mid-game**, so it must be detected **contingently per step, never used to label the
> game**.*

So it is a sensor, not a config flag:

- one slot's delta correlates with my action → **avatar**
- no slot correlates but the board changes → **actuator**, acting at a distance
- several correlate → **coupled bodies** (`coupled_agency.py`'s case)
- and it may change **mid-level**, so it is re-read every step

That is contingency detection — Tier-1 prior 4 — and `self_locus.py` / `agency.py` already
implement the shape.

### 16.3 The animation stack is a mechanism sensor, and everyone throws it away

`frame: list[list[list[int]]]` is a **stack**, and `new-horse`'s `unwrap_frame` reduces it to
`frame[-1]` with a good reason: the settled board is the state the next observation will
corroborate, so betting on `frame[0]` is betting on a board the world has already left.

**Correct for the prediction target. Wrong as a general policy** — because the intermediate
frames are free evidence about *mechanism*, and nothing in the tree reads them.

Within one step the stack shows:

| | |
|---|---|
| **path** | a block that ends three cells left either slid or teleported — the stack says which |
| **ordering** | A moved, *then* B reacted. Within-step causal order, which the endpoint erases |
| **appearance vs motion** | did that object move here, or appear here? Identity depends on the answer |
| **speed / duration** | how many sub-frames the change took |

> **Two uses of one field: `frame[-1]` is what you bet against; the whole stack is what you
> learn the mechanism from.** Discarding the stack throws away within-step causal ordering,
> which is precisely the thing a per-step residual cannot recover afterwards.

Cheap, unused, and it directly serves *"animation changes are major data."*

### 16.4 Read affordances, not substances — otherwise nothing transfers

`[I]* "Is this abstract blob a wall denoting a solid, or fluid, is it the sky?"*

**Do not classify the substance.** A taxonomy of blob-kinds is learned from the public set and
will not survive contact with a private one — it is the archetype trap from §13.4 wearing a
perception costume.

**Classify by behaviour under contact**, which is Gibson's answer and is already half-built as
`INTENDED_FREE`:

| affordance | the reading |
|---|---|
| blocks | movement into it fails |
| passes | movement into it succeeds and nothing changes |
| moves-when-touched | it displaces on contact |
| changes-on-touch | it recolours or transforms |
| triggers-remote | contacting it changes something elsewhere |
| terminates | contact ends the episode |
| consumed | it disappears on contact |

Seven booleans per object *kind*, learned by interaction. **"Wall" is not a category, it is a
profile** — and the profile is what transfers, because a private-set game with a wall it has
never seen still has a thing that blocks.

This is what *"after interacting with other objects is major data"* means, made into a
schema: **the affordance profile is the interaction record, indexed by kind.**

And Figure 11's clause applies directly: **an actor's valence is relative to the residual.**
A blocker is a malfactor when you want through and a benefactor when something is chasing
you. So the profile records *what it does*, never *whether it is good*. No standing list of
good objects survives a change of objective.

### 16.5 Habitat enumeration as an operation the agent runs

Figure 11 gives the procedure and it is not a metaphor here:

> *List everything in contact with the residual, then what is in contact with those, and
> outward until the cascade stops mattering. **You do not invent the list. You read it off the
> world**, and what you cannot perceive or measure yet is the residual.*

For a level:

| Figure 11 | the level |
|---|---|
| **actors** | objects, with affordance profiles (§16.4) |
| **conditions** | what is gated: the action set, plus whatever the precondition lattice has found (§16.1) |
| **relations** | contact, containment, precondition, and the correlate-with-my-action relation |

**Enumerated, never composed** — which means the agent reads the object list off the frame
rather than deciding in advance what kinds of things exist. And **contact cascades**: the
thing that matters may be three steps out, which is why the enumeration goes outward rather
than stopping at what the avatar touches.

### 16.6 Death is the second ground reading, and early on it is the denser one

`[I]* "else it dies, unable to continue."*

Worth stating precisely, because there is a real signal here that most designs waste.
The ground has **two** readings, not one:

| | |
|---|---|
| `levels_completed` rises | a **positive** settlement. Rare, sometimes absent for a whole run |
| `GAME_OVER` | a **negative** settlement — it refutes whatever bet was live |

**Early in play, deaths are far more common than wins.** So the denser ground signal is the
negative one, and it is free.

Which is the bill's own line arriving in the domain: *evolution reads one bit per death.*
Here you get the deaths first. And **death → explanation** says read *why*, not just *that* —
which needs the frames leading up to it, and therefore §16.3's animation stack again. The two
findings meet.

`new-horse`'s `ResetGate` has the matching discipline: RESET is banned in active play unless
a credit was earned, because *a forbidden capability is earned, not granted*. A death that is
immediately reset away teaches nothing.

### 16.7 Where the metaphor should stop, and one real trap  ·  ⚠ HALF-CORRECTED BY §18.5

**No lineage at agent scale.** *"Continue its lineage or species to the next rung"* is
evocative and there is no lineage here: one agent, one run, no population, no inheritance.
That is step 6 and it is deferred. **Levels are not generations** — a level transition is the
same agent with a changed board, not a descendant. Letting the metaphor in would smuggle
population machinery into a single-agent build, and the membrane rule exists precisely to
stop that crossing.

**And the trap, which is where every prior attempt died.** *"Building a case for what it
believes to be true about... its purpose in the game"* is objective abduction, and the
measured history is `abduced=[]` on most games. `THE_MISSION` names the fix:

> *Discovering the objective = **minting the φ that explains the residual**.*

So the objective is **not** produced by a separate objective-guessing module reasoning about
purpose. It falls out of the mint: predict the mechanism from the dense channel, and an
objective is what you can now state *because* you can predict and control the pieces. Figure
3's ordering — perception, then vocabulary, then objective — and a module that jumps to the
third is a reading taken below the break.

### 16.8 What this adds to the build

Four new sensors, all cheap, none needing pixels beyond what perception already produces:

| | sensor | cost |
|---|---|---|
| 1 | **action-set delta** — the previous action changed the gating | trivial |
| 2 | **precondition edges** — pairwise "a became available after b", with counts | 49 cells |
| 3 | **control mode** — avatar / actuator / coupled, re-read each step | one correlation |
| 4 | **affordance profile** — seven booleans per object kind, learned by contact | one row per kind |

And two changes to how existing data is used:

- **read the animation stack for mechanism**, while still betting against `frame[-1]`
- **treat `GAME_OVER` as a negative settle event**, recorded as a settlement rather than as a
  failure — it refutes a live bet, which is exactly what a settlement does

---

## 17. What is still under-planned

Walked step by step through the loop looking for holes rather than for confirmations.
Eight, ordered by how much they hurt. The first two are structural.

### 17.1 ⚠ Terms are single-slot, so the agent cannot express an interaction

**The worst one, and it is in code I already wrote.**

```python
Atom.fn(value, ctx)          # one slot's value
term.apply(before, Ctx(action))
```

A term is `slot × action → slot`. **It cannot read a second slot.** So the agent cannot
state:

> *B moves because A touched it.*

And that is most of what an ARC game is — collision, contact, triggers, keys and locks,
pushing. A per-slot predictor can learn "B sometimes moves" and will never learn *why*,
because the cause is not in its argument list. Every such mechanism lands in
`BROKEN · mechanism` forever, mints nothing that closes, and reports unreached — **correctly,
and for the wrong reason.** The atom is not missing; the *arity* is.

`dsl.py` solved this and the solution is the one to copy: `Context` carries N operand slots,
`focus` and `target` and more. With its warning attached — **the cost is quartic in N and they
capped it at 4**, because *"a vocabulary bought with 10× the agent's lifetime is a net loss
even if it is the right vocabulary."*

**Fix:** terms take an operand tuple, not a scalar. Which slots fill the operands is a
binding decision, and the natural default is *the slot that owes* plus *whatever is in
contact with it* — Figure 11's enumeration supplying the argument list.

### 17.2 ⚠ Nothing demotes a settled term, and level transitions are where that kills you

`self.settled` is a set that only grows. **A term the ground later refutes stays settled and
stays citable — and once chunking lands, stays a building block.** The library poisons
itself and the poison compounds.

**And this is not hypothetical: it is the measured failure.** `THE_MAP`'s live reading —
*"ls20 level-2 stall: the agent hardens instead of recalibrating at the curriculum break."*
ARC-AGI-3 is **built** to change mechanics between levels; a term true in level 1 is often
false in level 2, and the whole benchmark is designed around forcing that refactor.

The machinery exists across the branches and was never joined up:

- `falsified_ledger.py` — `is_refuted(sig, clock)`, **with a clock**, so refutation *expires*
  rather than being permanent
- `fabric.py` — *"falsify pariah-marks defeasibly: down-ranked, never deleted"*
- `boundary.py` — the level-boundary partition, plus `Quarantine` with a decay bound

**Fix, and it is three rules:**

1. a settled term that fails on fresh evidence is **demoted to candidate**, not deleted
2. demotion is **defeasible and clocked** — it can re-settle if it starts paying again
3. **a level transition is a boundary event**: re-run the partition, expect rebinding, and
   do not treat a level-2 residual as evidence against a level-1 term until it has been
   re-tested there

Without this the agent hardens exactly where the benchmark is designed to make it recalibrate.

### 17.3 Delayed effects are misattributed to the wrong step

ROUTE attributes this step's residual to this step's action. **If pressing a button changes
something three steps later, the residual lands on a step whose action did not cause it** —
and the mint then searches for a term relating an unrelated action to the change.

`effects.py` handled *remote* (spatially distant) with `EFFECT_IF` and a remote predicate.
**Temporal delay is a different axis and nothing handles it.**

**Fix, cheap version:** keep a short window of recent (action, state) pairs, and when a
residual appears with no same-step explanation, let the mint search over the window rather
than only the current step. Bound the window hard — it multiplies the search — and record the
lag in the ledger, because "this effect had lag 3" is itself a finding worth keeping.

### 17.4 There is no belief state — `b` is the observation

The formula is explicit that the bet is on `b`, and `b` is *not* `o′`. In my build
`perceive()` reads `env.observe()` and predicts from that. **Under partial observability
those differ, and ARC is partially observable** — occlusion, off-screen regions, and hidden
state like *what does this button do before I press it*.

**Currently the agent has no place to hold a belief that is not directly visible**, so it
cannot represent "the door is unlocked" or "that region is a wall" as anything other than a
re-derivation from pixels every frame.

**Fix:** the belief is the tracked object set **plus** the affordance profiles (§16.4) **plus**
the precondition lattice (§16.1) — all of which are already proposed and none of which is
currently written down as *the belief*. Naming them collectively as `b`, and predicting from
`b`, is mostly bookkeeping over things already planned. It is the framing that is missing,
not the content.

### 17.5 Γ is a simulator and nothing uses it as one

Every settled term is a forward model: `slot × action → slot`. **A library of them is a
simulator of the whole board**, and nothing in the design ever runs it forward more than one
step.

Which means the agent cannot answer *"what happens if I do A then B?"* without doing A then B
— and in a game with an action budget and a death state, trying is expensive and imagining is
free.

The corpus already argued this: *"a human simulates a tiny, well-chosen handful, and the
choosing is the whole trick. Imagination is cheap many-worlds."*

**Fix:** roll Γ forward over a candidate routine before committing to it. It is nearly free
given terms exist, it is what makes the routine algebra (§15.5) usable rather than decorative,
and — the part that matters — **the divergence between the simulated and actual outcome is
itself a residual**, on a channel we do not currently read.

### 17.6 Nothing diagnoses which link is broken  ·  ANSWERED, see §18.1

Figure 3's whole point is that *a reading taken below the break is a reading of nothing*, and
`tether.py`'s `_link()` is a hand-written heuristic that reports a guess.

**If segmentation splits one object into two, everything downstream is noise** — the residual
is high, no term pays, the mint reports unreached, and the agent concludes it needs a new
primitive when it actually needs a different segmentation.

**Fix, and there is a real discriminator available:** *high residual on **every** slot with no
term paying anywhere* is far more likely to be one perception failure than five simultaneous
mechanism failures. Simplicity says suspect link 1. Concretely — if `unreached` fires on
most slots at once, re-segment (different connectivity, different background) before minting
anything, and record that the re-segmentation happened. Perception is *a revisable belief*
(`perception.py` says so); this is what would actually revise it.

### 17.7 Search order is unplanned, and the gate already demands it be ranked

`enumerate_closure` walks the frontier in registry order, breadth-first. With chunking (§14.2)
the library gets large and **order becomes the difference between finding a term and
exhausting the budget** — which the agent then reports as `unreached`, which is honest and
wrong.

The gate already requires **every cut ranked and reversible**, so a rank function is
mandatory, not optional — and there isn't one.

**Fix, interim, before the proposer exists:** rank by `(cost, reuse count, recency of the
residual it last closed)`. Cheap, non-arbitrary, and it makes chunk reuse pay for itself.
The trained proposer (§15.6) replaces this later; it should not be waited for.

### 17.8 Library persistence across levels and games is undecided, and the ablation clause depends on it

Does Γ carry from level 1 to level 2? From game to game? Nothing says. And competition mode
constrains it — `make` once per environment, one scorecard.

It is not a detail: **it is exactly what the ablation clause tests.** *Back up Γ, wipe it,
re-run: if the win survives, the agent composed it; if it disappears, the library was carrying
the answer.* That test only means something once persistence is a stated policy rather than an
accident of process lifetime.

**Fix:** state it, and make it switchable so the ablation is runnable. My inclination — carry
within a game across levels (the mechanics are related by construction), and start cold across
games (that is the thing being claimed). But it is a decision, not a default.

---

### 17.9 The four that are flagged but genuinely fine to defer

Distinguishing *noted* from *planned* honestly:

| | why it can wait |
|---|---|
| **action budget / discounting** | measured on the old build: 24 of 25 runs ended on `unearned_reset`, at ~11× the actions a level needs. **Budget was not the constraint.** Revisit only if that changes |
| **event segmentation** | needs the routine algebra first; without `Until` there are no episodes to segment |
| **exploration vs exploitation arbitration** | the priced market (§13.4's selector) covers it once discrepancies exist. The probe covers the degenerate case |
| **the 16 KB digest's exact schema** | a packaging decision, and it follows from the ledger's shape rather than driving it |

---

### 17.10 The revised order of work

§17.1 and §17.2 move ahead of everything, because they are structural and because the second
one is the benchmark's designed failure mode.

| | |
|---|---|
| **1** | **operand arity** — terms read N slots (§17.1). Everything about interaction depends on it |
| **2** | **demotion + level boundaries** (§17.2). The library must be able to be wrong |
| **3** | fix `enumerate_closure` to chunk (§14.1) — then rank the search (§17.7) |
| **4** | the four cheap sensors (§16.8) and the affordance profile |
| **5** | Γ-as-simulator (§17.5), which unlocks the routine algebra |
| **6** | belief state named (§17.4), delayed effects windowed (§17.3) |
| **7** | link diagnosis (§17.6), persistence policy (§17.8) |

**And one honest note about the shape of this list.** Six of the eight are things the old
branches had in some form and never joined up — demotion, defeasance clocks, operand arity,
boundary partitions. **The failure was never that the parts did not exist.** That is the same
finding as the three-branch diagnosis, arriving one level down, and it argues for joining
before building.

---

## 18. Hunting the gaps through the corpus and the repos

Searched: the figures and `THE_FORMULA`, then `Ouroboros` (v3 / v4 / v4-economies-of-thought,
~1,900 files), `Ouroboros-Redux` (`v4-cold`, `new-horse`, `Nexus`, `redux-arch`,
`redux-triality`), and `tabula-rasa`.

**Six of eight have answers already written. Two do not. And two findings correct things I
proposed.**

| gap | status | where |
|---|---|---|
| 17.1 operand arity | **answered** | `redux_arch/dsl.py` — N operand slots, cap 4, quartic cost stated |
| 17.2 demotion / defeasance | **answered, and better than my sketch** | `falsified_ledger.py` + `nexus/population/credibility.py` + `regime.py` |
| 17.3 delayed effects | **nothing found** | still open |
| 17.4 belief state | **partial** | `WorldState` (Ouroboros), `SensedState` (nexus), `forward.py` |
| 17.5 Γ as simulator | **answered twice** | Ouroboros MCTS; `tabula-rasa/predictive_core.simulate_rollout` |
| 17.6 which link is broken | **answered, much better than my sketch** | `redux_arch/abort_code.py` |
| 17.7 search order / rank | **nothing principled** | still open |
| 17.8 persistence | **answered** | `nexus/generational.py` |

---

### 18.1 ⭐ `abort_code.py` — the best single thing found, and it outclasses my §17.6

It makes *"how far down the chain a stall got"* a **measured code** rather than a narrative,
and the seven stages subsume each other so a later one cannot be reached without every
earlier signal:

```
diff never ran                        -> DIED_PRE_DIFF    implementation
diff ran, residual empty/degenerate   -> RESIDUAL_EMPTY   library -- wrong grain
residual there, no mint               -> MINT_UNFIRED     gate calibration
minted, reuse never ATTEMPTED         -> REUSE_UNWIRED    implementation -- loop not connected
minted, reuse tried, not explained    -> MINTED_UNUSED    ARCHITECTURE -- the only code that indicts
reused, no break cleared              -> USED_NOCLEAR     drive layer, not the tether
reused AND a break cleared            -> CLEARED          the tether fired once
```

**And the rule attached to it is the important half:**

> *A stage-one or stage-three stall must **NEVER** be written up as a verdict on the
> architecture. Only the reuse stage indicts it — and only when reuse was genuinely
> attempted.*

That is Figure 3's *"a reading taken below the break is a reading of nothing"*, turned into an
instrument that refuses to let a wiring gap be reported as a theory failure. **It is the
honesty mechanism the whole project needs and it already exists.**

Three further properties worth taking whole:

- **The bar is stated, and it is not winning.** *"Winning was never the bar. The bar is ONE
  firing of the whole loop: a task fails → an operator is minted from the residual → that
  operator is reused on a task it was not minted for → the reuse clears a break."* **That is
  §14.7's chunk-reuse metric, formalised** — and it is a far better first target than a win.
- **Per-segment, never cumulative.** *"A mint in segment 3 must not credit the stall in
  segment 7. Cumulative signals would silently ratchet the reported stage upward and make a
  wiring gap look like progress."*
- **A clear by search or the drive layer can never set CLEARED.** The membrane rule, enforced
  in the instrument: a level advancing is not the framework firing.

And the reuse funnel charges every attempt to a **string literal written at the branch that
resolved it**, publishing the identity `sum(reuse_branch) == reuse_attempts` — so an attempt
with no branch is a defect the counter can state. That is the gate's discipline, one level in.

### 18.2 ⭐ Gap 17.2 is answered three times over, and one of them names the level-2 stall

**`falsified_ledger.py`** — a first-class reject memory, with four properties I did not have:

- **express-before-judge** — a refutation is recorded *only after the hypothesis actually ran
  a trial and the operator registered*. **"I failed to do X" must never be coded as "X is
  inert."** A blocked or never-reached attempt is a non-trial. I would have got this wrong.
- **weighted, never binary** — strength-of-rejection, so the consumer de-prioritises; never a
  hard ban
- **defeasible two ways** — decay over a **logical** clock (attempts/generations, no wall
  clock), *and* a fitness-conditional gate-drop where **decisive new surprise reopens a
  refuted hypothesis**
- **an immune-system failure audit** as the design checklist: autoimmunity (rejecting
  something needed), **pathogen mimicry** (a dead idea re-tried under a slightly different key
  — *the signature-granularity problem*, named and left to the caller rather than baked in),
  and cytokine storm (over-rejection freezing the agent)

**`credibility.py`** names the failure I flagged, in its own words:

> *Credibility must decay **on the clock**, not only when re-voted. The plain vote-EMA froze a
> stale incumbent's standing — a role right on an early regime stayed trusted through a regime
> change it no longer fit — **the "incumbency" pathology.***

**That is the ls20 level-2 stall, diagnosed and fixed, one layer up.** `tick()` decays every
credibility by a half-life each round, so standing is earned by recent prediction and
forgotten otherwise.

**`regime.py`** supplies the detector: a **two-sided CUSUM** change-point test over the success
stream that *"fires only when deviations pile up past a threshold, so one spike never trips it
but a sustained drop does."* That is the level-boundary signal — and it does not need to be
told a level changed.

**Together these are §17.2's three rules, already built and never joined to a loop.**

### 18.3 ⚠ `self_family.py` refutes what I proposed in §16.2

I wrote: *one slot's delta correlates with my action → avatar.* **That is one detector, and it
was measured to fail.**

> *The first live ls20 test refuted the keystone's single instantiation: `has_self: false` for
> **904 steps**, because the forward model looked for ONE thing — a rigid object that
> translates — and ls20's self does not translate. It is a growing/advancing trail; a colour
> depletes monotonically.*

And the fix carries a principle that generalises well beyond this case:

> *A family of four **translation-flavoured** detectors would not have helped: **their failure
> modes are correlated, so they fail together on the same games.***

So they built a **non-simulable family** — four self-hypotheses whose failure modes are
*independent*, each priced by its own ground-facing residual and selected by EWMA:

| hypothesis | what "self" means |
|---|---|
| `TranslationSelf` | a rigid object that moves |
| `GrowthEdgeSelf` | a growing / advancing trail |
| `ValueLatentSelf` | **non-spatial** — a scalar, a colour's total count |
| `RegionToggleSelf` | a bounded region that genuinely alternates |

> **"Non-simulable" means the members do not share a failure mode.** That is Figure 2's
> independence requirement applied to *detectors* — four correlated detectors are one
> detector wearing four names, which is collapse 2 inside the perception layer.

**Correction to §16.2:** control-mode detection is a *family* with an independence
requirement, not a single correlation test. And the same rule should govern every sensor
family we add.

### 18.4 `objective.py` — a measured failure worth not repeating

> *The live ls20 test proved the sensorium had become **diagnostic-only**: it found the right
> self and changed nothing, because the only consumer of perception was the post-hoc veto,
> which has no legal move at an all-directions-fatal board. **Perception has to enter the
> PROPOSER**, not just what it forbids.*

A perception layer that can only veto is inert at exactly the moment it matters. **Sensors
must feed proposal, not only filtering** — worth writing into the build as a rule rather than
rediscovering.

### 18.5 Gaps 17.4, 17.5, 17.8 — found, with caveats

**Belief state (17.4), partial.** `WorldState` (Ouroboros) is `objects · grid · step · score`
plus `get_agent()` — an object-level state rather than pixels, which is the right shape.
`nexus`'s `SensedState` is *"the before-state the sensors see: the grid, the available actions,
and the self-model"* — closer, and it already includes `available_actions`, which §16.1 argues
for. **Neither carries inferred hidden state** (what a button does before pressing), so the
gap narrows rather than closes.

**Γ as simulator (17.5), found twice.** Ouroboros has a full MCTS — `WorldState.clone()`,
`WorldModel.apply_action`, UCB1 selection, expansion, random rollout to depth 20 against a
`goal_evaluator`. `tabula-rasa`'s `simulate_rollout` is explicitly *"the core of the
imagination — think ahead by simulating multiple action sequences"*, with a timeout.

**Caveat, and it matters:** MCTS needs a value estimate, which needs a goal, which is the thing
we do not have early. And a random rollout to depth 20 in ARC is expensive and near-useless.
**Take the structure — clone, apply, evaluate, timeout — and use it for short routine
validation, not for full tree search.** The honest early use is "does this routine do what I
think it does" rather than "which of these 10,000 futures is best."

**Persistence (17.8), answered.** `generational.py`: *"one agent, many lifetimes, over a
run-local ledger. On GAME_OVER the run resets into a new generation, but the **same policy
instance persists** — its falsified ledger and hypotheses carry over — and the RunLedger
records what was refuted, so generation N+1 never re-spends what N proved dead. **Compounding,
not thrash.**"* Plus `apply_fatal_veto`, a learned-fatal veto that survives resets.

**Correction to §16.7.** I said there is no lineage at agent scale and levels are not
generations. **Half wrong.** Generations here are *deaths within a run*, and the inheritance is
the refutation memory — which is a real, single-agent, non-metaphorical lineage. What stays
true is the narrower claim: **a level transition is not a generation** (same agent, changed
board), and cross-*game* inheritance is still the thing the ablation clause tests.

### 18.6 What the hunt did not find  ·  BOTH ADDRESSED IN §19

**Delayed effects (17.3).** Nothing anywhere handles temporal lag between an action and its
consequence. `effects.py`'s `EFFECT_IF` handles *spatially remote* conditions; `abort_code`'s
segments are about accounting, not attribution. **Genuinely open, and worth flagging because
"press a button, something changes three steps later" is common in these games.**

**Search order (17.7).** No principled rank function anywhere — enumeration is registry-order
everywhere it appears. The reuse funnel does supply the beginnings of one (a φ that has been
reused should rank above one that has not), but nobody wired it. **Open.**

### 18.7 The pattern, again, one level down

Six of eight gaps had answers already written — several of them careful, receipted, and
better than what I proposed. **`abort_code.py` alone is a more honest instrument than anything
in the current build.** And they were never joined to a running loop: the falsified ledger is
in `new-horse`, credibility and CUSUM in `Nexus`, operand arity in `redux_arch`, MCTS in
`Ouroboros`, and the loop they would serve is in none of them.

> **This is the three-branch diagnosis for the third time: the parts existed, correct and
> load-bearing, for architectures that could not use them.**

Which sharpens the build order. §17.10 assumed most of these were design work. They are not —
they are **integration** work, with the design already done and the receipts already written.
The two that are genuinely new build are the two the hunt came back empty on: **delayed
effects, and a rank function.**

---

## 19. "I ran out" is not "I was wrong" — the same bug in two places

`[I]` *"Unreached is a bug and we need to fix it to know if it's an action-budget problem or
a real loss."*

**It is one bug appearing twice**, and naming it that way makes both fixes the same shape:

| where | the conflation |
|---|---|
| **the mint** | `UNREACHED` means both *"the search budget ran out"* and *"no such term exists at this depth"* |
| **the episode** | a run ending means both *"I hit the action cap"* and *"the world killed me"* |

**In both cases a resource exhaustion is being reported as a verdict about the world.** Which
is Figure 9's rule violated in the loop's own reporting: *never let a filter hand you a
verdict.*

### 19.1 Decomposing the mint verdict, with a denominator

Five outcomes where there is currently one word:

| verdict | means | strength |
|---|---|---|
| `NO_SUPPORT` | nothing to explain — `\|R\| ≈ 0` | already separate |
| `NOT_NOVEL` | everything that fits is already held | already separate |
| **`BUDGET_SPENT`** | stopped enumerating early | **weak** — says almost nothing |
| **`DEPTH_EXHAUSTED`** | saw the *whole* space at depth *d*, nothing paid | **strong** — not at this depth |
| **`UNREACHED`** | reserved for after escalation (§19.2) | the honest claim |

**And the number that turns the word into a measurement is coverage** — which `λ` was already
computed for:

```
estimated space at depth d  ≈  λ^d            (the spectral radius, §11.3)
coverage                     =  candidates_seen / estimate
```

> *"Unreached, having examined 4,000 of an estimated 8,000,000 candidates — coverage 0.0005"*
> is a completely different claim from *"unreached, having examined 4,000 of 4,000"*, and at
> present they print identically.

Coverage near 1.0 licenses *"not at this depth."* Coverage near zero licenses nothing at all,
and should read as *"I have barely looked."*

### 19.2 Escalate cheapest-first, and record each rung

A weak `BUDGET_SPENT` is not a conclusion, it is a **prompt to try harder in a specific
direction**. The axes have very different prices, so the order is not arbitrary:

| rung | cost multiplier | what it buys |
|---|---|---|
| 1 · **re-rank** | free | a different thousandth of the same space |
| 2 · **more budget** | linear | more of the same space |
| 3 · **more lag** (§19.4) | `×k` | causes displaced in time |
| 4 · **more depth** | `×λ` per level | deeper compositions |
| 5 · **more arity** | quartic (`dsl.py`'s measured cap of 4) | causes in another slot |

**Each rung tried is a ledger entry**, so a final `UNREACHED` after all five is a genuinely
strong claim — *"I looked wider, later, deeper and across more slots, and still nothing"* —
while the same word before any escalation is nearly empty. **That is the difference between
an abstention worth trusting and one that is just a budget report.**

### 19.3 The same decomposition for episode endings — and it is already measured  ·  ⚠ REFINED BY §20

`[I]* "What consistently produces losses, and what actions don't? Or is it action-count
based?"*

**Measured, and the answer is no.** `survival.py`, from the win-ceiling probe:

> **13 of 25 dev games are lost to DEATH (`GAME_OVER`), several long before the action cap.**

And `THE_TERMINAL_CONDITION` measured the other side: *24 of 25 runs ended on `unearned_reset`,
exactly one on the action cap*, with a median of ~11× the actions a level needs. **Budget is
not the constraint. Deaths are.** Both numbers already exist and neither is currently read by
anything in the new build.

So endings decompose the same way, and the three carry completely different lessons:

| ending | what it says | what to learn from it |
|---|---|---|
| **WIN** | `levels_completed` rose | the positive settle. Rare |
| **DEATH** | the world refused a specific state | **a fatal condition — mintable** |
| **CAP** | I ran out of actions | a budget fact. **Says nothing about the world** |

Reporting DEATH and CAP under one "loss" is the same error as reporting `BUDGET_SPENT` as
`UNREACHED`.

### 19.4 Death is dense supervision for a mintable predicate

The framework-native reading of *"what consistently produces losses"* is not a probability. It
is a predicate:

> **Mint φ over the before-state such that φ holds exactly on the states that preceded a
> death.** Priced by the same bargain: does stating φ cost less than enumerating the deaths it
> covers?

That reuses everything — same guards, same code, same ledger. And **death is denser than
victory early on** (§16.6), so this channel has evidence when nothing else does.

`survival.py` gives the floor of that spectrum, and it is the right floor:

| | generalisation | false vetoes |
|---|---|---|
| **exact board fingerprint** → the action that killed you | none | **zero, by construction** |
| **avatar-centric hazard** | some | few |
| **minted predicate** | full, MDL-priced | possible, and the ground corrects them |

That is *an instrument improved from a worse instrument already returning something* —
Figure 6's rule, running on the survival channel. **Start with the fingerprint, which cannot
be wrong, and mint outward from what it records.**

And the enabling fact, stated in `survival.py` and load-bearing for the next section:

> **The games are deterministic.** The retry re-encounters the same boards, so a death is
> reproducible, and the safe path is threaded one veto at a time.

### 19.5 ⭐ The sweep — retrospective re-attribution

`[I]* "Humans retrace their steps from the beginning up to the current state and
back-propagate the hypothesis, update recursively, so each new action stacks and alters or
adds confidence to their overall model."*

**This is the strongest idea in the message and it is nearly free, because the history is
already in memory and the games are deterministic.**

What the build does today: `_accumulated()` scores a *candidate* against a slot's whole
history — so retrospective evaluation exists **for scoring**. What does not exist is
retrospective **routing**:

> When Γ changes, every past residual becomes re-examinable — and **nothing revisits them.**
> A slot marked `UNREACHED` at cycle 10 may be fully explained by a term minted at cycle 40,
> and the debt is never cleared.

**The sweep:** on every accept — and on every lag discovery — re-run the new term against all
outstanding parked and unreached residuals. If it closes one, that is a **retroactive
resolution**, recorded, with the gap between the residual and its explanation stamped on it.
That gap is itself data: *"this took thirty cycles of other evidence before it became
explicable."*

**Three properties make this worth building early:**

- **It is free of the environment.** No actions spent, no budget consumed. Pure re-reading of
  what was already paid for — which is the cheapest possible move under a body-count bill.
- **A retroactive resolution IS reuse**, in `abort_code.py`'s exact sense: a term minted for
  slot A that later explains slot B's old residual is *an operator reused on a task it was not
  minted for*. **Which is the stated bar for the whole architecture firing once.** The sweep
  is not just a fix; it is the most likely place the bar gets cleared first.
- **It does not corrupt settlement.** A term that explains old data is not *settled* by old
  data — that is its fit set. Settlement still requires fresh, held-out evidence. So the sweep
  clears debts and lowers residuals without ever manufacturing a settle.

**And it changes what `UNREACHED` means one more time.** With a sweep, unreached becomes
provisional by construction: *not explained yet, by a library that is still growing*. The
import debt stays open rather than closing the question — which is exactly the epistemic
status Chaitin's rule says it always had.

### 19.6 What to build, in order

| | |
|---|---|
| **1** | split the verdicts and print **coverage** — `λ^d` is already computed, this is arithmetic |
| **2** | split episode endings into WIN / DEATH / CAP and record which |
| **3** | the **sweep** on every accept — free, and it is where the reuse bar most likely clears |
| **4** | death-fingerprint memory as the survival floor, then mint outward from it |
| **5** | the escalation ladder, one rung per ledger entry |
| **6** | lag as a priced parameter (`+log₂(k+1)` bits), tested by the same sweep machinery |

**And one gate check to add:** an `UNREACHED` entry that carries no coverage figure is
refused. The word is not allowed to appear without its denominator — which is the same rule
as *"a bin without its discriminator is a label, not a diagnosis"*, applied to the one verdict
the whole product rests on.

---

## 20. Three termination classes, and the cap is an instrument

`[I]` *"Some games have a built-in action count, others have a death or loss condition. Some
run infinitely and you set your own cap to derive meaning and epochs."*

This corrects §19.3, which treated CAP as one thing that *"says nothing about the world."*
**In the third class the cap is the only ending there is** — so it is not noise, it is the
measurement interval, and choosing it is choosing what can be measured.

| class | ends by | what an ending tells you |
|---|---|---|
| **bounded** | the game's own action count | the world stopped you. A fact about the game |
| **mortal** | `GAME_OVER` | **a condition was violated** — the densest early signal (§19.4) |
| **open** | nothing | **only your own cap.** The ending is an artefact of your instrument |

### 20.1 The class is not given, so detecting it is a sensor — and the evidence is asymmetric

Nothing in `FrameData` announces the class. It has to be read, and it can only be read from
**positive** evidence:

| read | from | direction |
|---|---|---|
| **a win is possible** | `win_levels > 0` | given up front |
| **death is possible** | `state == GAME_OVER`, once | **proven on the first death, never disproven** |
| **bounded** | the run ends without a death and without your cap firing | proven by observation |
| **open** | none of the above, so far | **never proven** — only defaulted to |

**Not having died is not evidence that you cannot die**, which is the corpus's own rule:
*prefer positive causal evidence over absential; absence of evidence resting on completeness
never holds mid-episode.* So `DEATH_POSSIBLE` latches true and never latches back, and
`OPEN` is a standing assumption rather than a finding — and should be reported as one.

### 20.2 `win_levels` is a bounded progress read, and nothing uses it

`levels_completed` is a counter with no ceiling in the agent's view. But `win_levels` is in
every frame, so:

```
progress = levels_completed / win_levels     bounded, in [0, 1]
done     = levels_completed == win_levels    the terminal condition's clause 1
```

That is a **real** progress signal — from the ground, not derived, not a proxy — and it is
free. It does not have `ProgressProbe`'s Goodhart hazard (§13.3) because the agent cannot
move it except by actually winning. **It should be the reward channel's degree**, and
`ProgressProbe` should sit strictly below it as a *sensor* that proposes.

### 20.3 The open class needs a third stopping case that the formula does not have

`THE_FORMULA` step 8 gives two ways the loop stops, and says they are indistinguishable from
inside:

> *R stops arriving because the prediction is perfect · R stops arriving because the channel
> closed.*

**The open class supplies a third: the ground channel was never open at all.** Not decayed —
*absent*. And unlike the other two, **the agent can tell**, because `win_levels` is in the
frame. If `win_levels` is unreachable in the actions available, the objective channel is silent
by construction and no amount of play will settle anything on it.

**The honest report for such a game is a real result, not a failure:**

> *I modelled the mechanics. Nothing settled an objective, because nothing on this channel
> ever spoke.*

That is Figure 3's link 3 unreachable, correctly reported — and it is exactly the kind of
statement the whitebox claim is *for*. A black box in the same position produces a confident
action and no way to know it meant nothing.

### 20.4 The cap should be derived from the agent's own learning, not picked  ·  ⚠ CORRECTED BY §22.1

The old builds picked. `tabula-rasa` carries four caps at four scopes —
`MAX_ACTIONS_PER_{GAME,SESSION,SCORECARD,EPISODE}` — with comments that are the whole story:

> *"Increased for better pattern exploration **(was 1000)**"* · *"Higher max for complex games
> **(was 1000)**"*

Four numbers, tuned by hand, no provenance, and a whole script whose job is to rewrite them.
**That is the magic-number failure mode, at scale**, and Q14 already forbids it.

**There is a principled boundary available and it is already built.** `probe.py`'s `bored()`
fires when the agent's own prediction-error EMA has fallen to ~zero with enough observations
behind it — *"the agent's model explains everything it is seeing, so it is learning nothing."*

> **End the epoch when the agent stops learning, not at a fixed count.**

Which makes the epoch a *reading* rather than a setting, and gives it the right property in
both directions: a game that keeps surprising you gets more actions **because it is still
paying**, and a game that has gone quiet gets cut short **because it is not.**

Two bounds still needed, and they are different in kind and should be labelled so:

| | kind | provenance |
|---|---|---|
| **boredom threshold** | a reading | already has one: `EPS`, `WARM`, with the reasoning stated in `probe.py` |
| **hard ceiling** | a **safety bound**, not a tuning knob | so the run terminates at all. Constitutional, like `bounds.py`'s |
| **platform limit** | **read, never assumed** | competition mode imposes its own; ours must be ≤ theirs |

The harness's own knob is `MAX_ACTIONS` on the `Agent` subclass — the sample sets
`float('inf')` — so the ceiling belongs there, stated once, as a bound rather than a dial.

### 20.5 The cap defines the logical clock, so it reaches further than stopping

This is the part that makes the cap load-bearing beyond "when to stop."

`falsified_ledger.py` decays refutations over a **logical clock** — *attempts, generations —
no wall clock is read.* `credibility.py` decays standing per **round**. `generational.py`
counts a **generation** per `GAME_OVER`.

**In the open class there are no deaths, so there are no generations** — and every one of
those clocks stops ticking. Refutations never decay, standing never ages, the incumbency
pathology (§18.2) returns with nothing to correct it.

> **So in an open game the self-imposed epoch *is* the generation.** The cap is not a
> stopping rule; it is the unit that makes demotion, decay and the sweep meaningful at all.

Which raises its status: it is not a convenience parameter, it is **the clock**, and it should
be recorded in the ledger with every entry that depends on it.

### 20.6 What this adds

| | |
|---|---|
| 1 | **termination-class sensor**, latching, positive evidence only, reported as an assumption while it is one |
| 2 | **`win_levels` as the reward channel's degree** — bounded, from the ground, Goodhart-free |
| 3 | **a third stopping case**: the ground channel was never open — and the agent *can* tell |
| 4 | **epoch ends on boredom**, with a hard ceiling labelled a bound and the platform limit read rather than assumed |
| 5 | **the epoch is the logical clock** in open games — recorded, not implicit |

---

## 21. Level events — and the level-resetting loss is a controlled experiment

`[I]` *"Each level completed means you stumbled on the conditions, or the agent's hypothesis
or instrument got the crux of the level. Sometimes there is also a loss signal that will reset
the level — that's also juicy and useful data."*

The second half is the most valuable thing in the design and nothing so far uses it.

### 21.1 A level-resetting loss is the intervention operator

Everywhere else in this design the agent gets **observational** data: it acts, the world moves,
it reads the gap. Correlation is cheap; causation is not, because you can never re-run the same
moment.

**A loss that resets the level breaks that**, because `survival.py` establishes the enabling
fact: **the games are deterministic.** So:

> same starting board · vary exactly one action · observe the difference

**That is a controlled experiment**, and it is the only place in the whole loop where one is
available. It is what the prior catalogue calls *disambiguating intervention* — *"after
confounded evidence, act to separate hypotheses"* (Schulz & Bonawitz) — and *causal structure
learning from intervention* (Gopnik), which is precisely the machinery that separates `A→B`
from `A and B co-occur`.

**Cost:** actions, not the run. Which makes it cheap in the only currency that is scarce
according to the measurements — and §19.3 says the budget was never the binding constraint.

### 21.2 Deliberate death as an experiment — legitimate, with one discriminator

If a death costs actions and returns you to a known board, then **choosing to die is a way of
buying an experiment.** That is *aiming the variation*, which the bill ledger names as the
frontier move.

**But it is one step from farming**, and the project has already been burned there — `bounds.py`
exists because *"the Redux harness once violated this by force-RESETting on GAME_OVER to farm
~18 unearned attempts."*

Two things keep them apart, and both are checkable:

| | |
|---|---|
| **the mechanism differs** | `ResetGate` bans the *agent calling RESET*. A **game-inflicted** level restart is the world's own rule, not a bypass of it |
| **the intent is recorded** | an experiment states its **hypothesis and its disproof before the action**; farming states nothing and just wants the board back |

> **The discriminator is a gate check, and the fields already exist**: `nexus/reasoning.py`'s
> `expect` and `disproof`, stated *before* the action. A death preceded by a stated expectation
> and disproof is an experiment. A death preceded by nothing is a stall.

And the honest number to publish beside it: **what fraction of the action budget went to
deliberate deaths.** If that is 40%, someone should see it rather than infer it.

### 21.3 A level completion is a settle, and the sweep is how you find out what caused it

Seven levels means **seven separate positive settlements**, not one — so the reward channel is
sparse but not the single bit a game win would be.

But the same misattribution problem as §17.3 applies, and worse: **a level completes at step
500, and the last action did not cause it — the trajectory did.** Crediting the final action is
the delayed-effects bug at the scale of a whole segment.

**The sweep (§19.5) is the mechanism.** On a level completion, re-examine the segment: which
hypotheses were live, which terms had settled, which residuals were closed along the way. That
is retrospective credit assignment over a *recorded* history, costing no actions — and it is the
same operation already proposed for retroactive resolution.

### 21.4 A completion is simultaneously a settle and a regime-change warning

The two readings pull in opposite directions and both are correct:

| reading | says |
|---|---|
| **settle** | the hypotheses live at completion got the crux. **Credit them** |
| **regime warning** | ARC-AGI-3 changes mechanics between levels. **Do not trust them in the next level until re-tested** |

That is exactly §18.2's pairing: credit *and* clock-decay, with `regime.py`'s CUSUM watching for
the shift. **Crediting without the decay is the incumbency pathology; decaying without the credit
throws away the only positive evidence there is.**

### 21.5 ⭐ Reset and advance produce the same residual spike and mean opposite things

Both change the board, so both produce a large residual. **And the meaning inverts:**

| event | next board | a big residual means |
|---|---|---|
| **level RESET** after a loss | **known** — you have seen this exact board | **your model is wrong.** Real evidence, demote accordingly |
| **level ADVANCE** | **unknown** — new mechanics by design | **normal.** Evidence about nothing yet |

> **Same number, opposite verdict, disambiguated for free by which event fired.**

This matters more than it looks, because without the distinction **the demotion logic poisons
itself at exactly the wrong moment**: every level advance would demote the good terms that
carried the last level, because they mispredict an unfamiliar board. The agent would punish its
best work for the crime of a scene change.

And the reset case is the strongest evidence in the game for the opposite reason: on a board you
have already modelled, a residual has no excuse.

**This belongs in `boundary.py`'s partition** — it already distinguishes TRANSFERRED / NOVEL /
GONE across a redraw, and it needs one more bit: *was this redraw a reset or an advance?*

### 21.6 What this adds

| | |
|---|---|
| 1 | **level-reset loss = controlled experiment.** The only intervention operator in the loop. Build for it deliberately |
| 2 | **deliberate death is legitimate** when `expect` and `disproof` are stated first — a gate check, not a judgement call. Publish the fraction of budget spent on it |
| 3 | **a completion is a per-level settle**, credited by the sweep over the segment, not by the last action |
| 4 | **a completion is also a regime warning** — credit and decay together |
| 5 | **reset vs advance inverts the meaning of a residual spike.** Without it, demotion punishes the terms that just worked |

---

## 22. The cap is also a yardstick, and the phase mix is the real instrument

`[I]* "My magic numbers were somewhat empirical but good meters."*

### 22.1 Correcting §20.4 — the distinction is anchoring, not hard-coding

I lumped your caps in with `tabula-rasa`'s. **They are not the same kind of number**, and the
difference is exactly the one Figure 2 draws:

| | | verdict |
|---|---|---|
| *"Increased for better pattern exploration (was 1000)"* | **tuned toward a desired behaviour** by the frame that benefits from it | frame-internal. The failure mode |
| *"Humans need under 500 per level, so 1000 is 2× the honest ceiling"* | **anchored to a measurement of the world** that the agent cannot move | **specified mode, with provenance** |

A human's move count is not a quantity the agent produces, so using it as a reference is not
self-scoring. **What was missing was never the basis — it was that the basis was in your head
and not in the constants block.** Q14 asks for mode and provenance, and this has both.

So: `MAX_ACTIONS` keeps its number, and gains a line — *empirical: human play across the dev
set completes a level in <500 actions, typically ~100; this is the 2× ceiling.*

### 22.2 The valuable part is the decomposition, not the total

> *~30 random → ~10 directed → ~5 strategy → level win. Then each next level is pure strategy
> plus informed directed steps and new theories.*

That is not a count, it is a **phase structure**, and every phase maps onto a mechanism the
loop already has:

| phase | ≈ | what it is doing | the loop |
|---|---|---|---|
| **random** | 30 | acquiring density. *You cannot compress what you never observed* | the **probe** — `density(R)` at zero |
| **directed** | 10 | testing hypotheses against specific slots | **MINT**, bets with bound terms |
| **strategy** | 5 | executing a multi-step plan with a predicted outcome | **routines** (§15.5) |
| **next level** | — | random collapses; the library carries | **chunk reuse** — the transfer claim |

**And the shape is the composition test.** The claim "the agent is composing" has been hard to
falsify without a win. This makes it a curve:

- **random stays dominant at step 400** → it never left phase 1. Nothing is being modelled
- **directed grows and random shrinks** → the mint is firing on real structure
- **phase 1 shrinks on level 2** → **the library transferred**, which is the whole thesis

> **That is the chunk-reuse metric with a human reference overlaid, and it needs no win to
> read.**

### 22.3 The action-mix histogram is free

The loop already knows which branch produced each action — the probe fired, a bound term drove
a bet, or a routine executed. **Labelling each action with its phase costs one field**, and
the histogram over time is the diagnostic above.

It is also honest in the way the metrics rules demand: it describes *what the agent did*, not
whether it succeeded. The ground still settles everything.

### 22.4 One caution — compare the shape, not the counts

The 30/10/5 numbers are **a human's, with a human's priors.** The agent starts with nine
sensors and no affordance profiles, so expecting 40 moves is not a fair target and would be a
selection pressure toward encoding priors to hit it.

**What transfers is the shape:** random → directed → strategy, with phase 1 shrinking across
levels. **The ratio between phases, and its movement, is comparable. The absolute count is not
— yet.** When it becomes comparable, that is itself the result.

### 22.5 Two clocks, not one — understanding is not winning

`[I]* "under 500 moves per level to **understand**."*

Understanding and winning are different events and they fail differently. Both are already
derivable from what the loop logs:

| | measured by | a long value means |
|---|---|---|
| **steps-to-model** | the transition-residual EMA falling and staying low | perception or minting is the problem. **Links 1–2** |
| **steps-to-win** | `levels_completed` rising | you modelled it and could not act on it. **Links 3–5** |

**The gap between them is the cost of execution as distinct from the cost of learning**, and
splitting them turns one alarm into a located one. A short steps-to-model with a long
steps-to-win is a planning failure and should never be reported as a learning failure.

### 22.6 The ratio is the alarm; the stage code is the diagnosis

> *"When I see an agent taking 1000 moves for a level a human beats in 40, that's a signal."*

Agreed — and it is a signal that something is wrong, not *what*. **`abort_code.py` supplies the
what**, and the two compose cleanly:

```
ratio  =  agent_steps_to_model / human_reference     the ALARM  -- something is wrong
stage  =  DIED_PRE_DIFF | RESIDUAL_EMPTY | MINT_UNFIRED
          | REUSE_UNWIRED | MINTED_UNUSED | ...      the DIAGNOSIS -- where
```

A ratio of 25× with `RESIDUAL_EMPTY` is a perception grain problem. The same 25× with
`MINTED_UNUSED` is the only reading that indicts the architecture. **Same alarm, different
repair, and without the stage code they are indistinguishable** — which is how a wiring gap
gets written up as a theory failure.

### 22.7 What this adds

| | |
|---|---|
| 1 | `MAX_ACTIONS` keeps its value and gains its provenance line. **Anchored, not tuned** |
| 2 | **phase-label every action** — probe / directed / strategy. One field |
| 3 | **the phase histogram over time** is the composition test that needs no win |
| 4 | **steps-to-model and steps-to-win as separate clocks** — learning cost vs execution cost |
| 5 | **ratio-to-human as the alarm, stage code as the diagnosis.** Neither alone is enough |
| 6 | compare **shape** across levels; treat absolute parity with human counts as a *result*, never a target |

---

## 23. Γ does not start empty — and what may be loaded into it

`[I]* "Humans don't come in empty. They come with those priors and fully loaded with the
primitives they've minted from years of doing this."*

**Correct, and my "simulating is generating fiction" was wrong as stated.** It is right about
an *empty* Γ and Γ does not have to be empty. But the correction changes the simulation
argument less than it changes the loading rule, so both are below.

### 23.1 What a loaded Γ actually buys simulation

A loaded Γ does **not** make step-one simulation accurate — general priors do not know that
`ACTION5` teleports the avatar *in this game*. What they give is a **prior over which
mechanisms are plausible**: things move continuously, contact precedes effect, unsupported
things fall.

So the honest statement:

> **Simulation from a loaded Γ is not a predictor. It is a hypothesis generator with a
> better-than-random prior — which is exactly what ranking needs.**

Which does not weaken the discipline, it makes it useful sooner: *simulate to rank, never to
settle* was already the rule, and a loaded Γ makes the ranking good from step one instead of
useless until Γ fills. It is the corpus's own line — *"a human simulates a tiny, well-chosen
handful, and the choosing is the whole trick"* — and the priors are what does the choosing.

**The fidelity gate still stands unchanged**, because it measures *this game's* accuracy, which
is what lookahead depth should track regardless of how much was loaded.

### 23.2 The line: load what to *look at*, never what to *do*

The seven shapes from §12.1 sort cleanly, and the sorting is the rule:

| shape | loadable? | why |
|---|---|---|
| **SENSOR** | ✓ generously | what can be read. Domain-general |
| **TERM** | ✓ generously | *"unsupported things fall"* — a prior on mechanism, not a solution |
| **CONSTRAINT** | ✓ | *"two things cannot occupy one cell"* — plausibility, not answer |
| **TRACKER** | ✓ | identity rules |
| **BIAS** | ✓ | search order. Reversible by construction |
| **BUDGET** | ✓ with provenance | §22.1's rule |
| **ROUTINE** | ✗ **never** | **a routine is a solution**, and solutions are the thing that must not transfer in |

> **Load all six of the first shapes generously. Never load the seventh.**

The test is one question: **does it name what to look at, or what to do?**

- *"objects are connected components"* → what to look at. **Load.**
- *"contact precedes effect"* → constrains which mechanisms are plausible. **Load.**
- *"count the things of a colour"* → an instrument. **Load.**
- *"go to the nearest distinct object"* → **what to do. Do not load.**
- *"acquire the key, then use it on the lock"* → what to do, **and derived from the public
  set.** This is `relation.py`'s five relations and `referent.py`'s detectors — §13.4's
  archetype trap, arriving under a friendlier name.

**That is also the beach analogy's own line.** The human brings *metallic · a detector exists ·
keys look like this*. They do **not** bring *your keys are under the third umbrella* — and a
loaded strategy is the third umbrella.

### 23.3 Loading does not kill the mint signal, provided the stamps are read

§11.4's worry — *an agent handed every prior never mints, and you cannot tell a composer from
a lookup table* — holds only if the loaded priors cover **this game's** mechanics. General ones
do not, so the mint still has to fire for anything game-specific.

**And it is measurable, because the origin stamps already exist** (`prior | minted | imported`):

> **the fraction of a solution's terms that were minted rather than loaded**

A level solved entirely from priors is retrieval. A level needing minted terms is composition.
That number is readable per solution and needs no ablation run to produce.

### 23.4 The ablation clause must be stratified, and the machinery is already there

If Γ is preloaded, wiping all of it tests *"can it work with no priors at all"* — a question no
human passes either, and not the one the clause is asking.

**So ablation becomes two experiments, and the origin stamps make both cheap:**

| wipe | tests | the honest claim |
|---|---|---|
| **minted only, priors kept** | did it compose *this game's* solution, or retrieve it? | **this is the terminal condition's clause 3** |
| **everything** | bootstrap from nothing | interesting, and not the claim being made |

That sharpens the clause rather than weakening it: *"back up Γ, wipe the minted layer, re-run —
if the win survives, the priors were carrying it."*

### 23.5 The cost, and the dependency it creates

Loading is not free. More atoms means a larger `λ`, so `λ^d` grows and a fixed budget covers a
**smaller fraction** of the space — which shows up as coverage falling (§19.1) and, if nothing
is done, as more false `UNREACHED`.

> **Loading generously therefore *requires* retrieval-by-characterised-residual (§15.3), not
> enumeration.** A big library is an asset when you look things up by the shape of your gap and
> a liability when you walk it in registry order.

**Plan consequence: Phase 3c stops being optional.** If the library is loaded heavily, retrieval
and the rank function are prerequisites rather than improvements — otherwise loading makes the
agent *worse* by drowning every search.

### 23.6 What changes in the plan

| | |
|---|---|
| 1 | **Γ ships loaded** — the six loadable shapes, generously, all stamped `prior` |
| 2 | **no routines are loaded.** They are the one thing that must be minted |
| 3 | **simulation starts useful**, because ranking has a real prior from step one; the fidelity gate on depth is unchanged |
| 4 | **report minted-fraction per solution** — the composer-vs-lookup number, free from the stamps |
| 5 | **ablation is stratified** — wipe minted, keep priors. The sharper test |
| 6 | **Phase 3c (retrieval + rank) is promoted to a prerequisite** of loading, not a follow-on |

---

# Carried from the kernel: the decomposition question was already inside the frame

Measured on the kernel, where a defect costs a day. One board, three descriptions, and
the contract binds all three unmodified -- so the interface is a genuinely separate layer.
Two things the loop assumes anyway, neither of them written down:

- **the slot set is fixed for a level.** A second object appearing mid-episode produces no
  bet, no residual and no row. It is invisible rather than an error. Cells never do this
  and objects always will.
- **one alphabet covers every slot.** A boolean relation is charged 4.91 bits per miss
  instead of 1.00, so `base` is inflated on exactly the slots carrying least information
  and the mint gate is loosest where least is at stake. **A relations interface failing
  would look like the interface and would be the gate.**

## Loud and silent, and only one is survivable

    a loss is LOUD    the residual stays live and the agent abstains -- it can see
                      something it cannot explain, which is the honest state

    a loss is SILENT  the residual reads ZERO, so the agent believes it explained a world
                      still moving underneath it

An object-level view of a sub-object rule ran twenty steps without one live reading.
**This is worse than a narrowing that drops a candidate: that excludes a term which would
have been tested, this excludes the observation, so nothing downstream can report it.
There is no residual to be wrong about.**

The grading rule transfers exactly: a decomposition derived as a NECESSARY CONSEQUENCE of
the residual costs nothing; one chosen because objects are usually what matters is the
same shape as an applicability index built from observed deltas, and its exclusions are
silent.

## The part worth carrying

**`CHANNEL_CLOSED` is already the name for this. Its remedy is already step 7 INWARD. And
step 7 is the step that is not built.**

So the decomposition question was never outside the architecture -- it was filed as one of
the three causes of a low reading, with a remedy attached, waiting on a step nobody had
written. The agent has the same unbuilt step and had no name for the same problem.

The trigger is cheap and needs no threshold: **every advertised action drawn, and no slot
ever live.** Positive evidence, not absence of evidence. Built in the kernel; the row says
`built: False` for the remedy, which is the honest half.

---

# Motor skills — the read before the build

Measured on the kernel. Three questions, and the layering question underneath them.

## 0 · The agent imports the kernel. It does not edit it.

That is the right shape and it is already half true. **What an add-on can supply from
outside, with no kernel change** -- demonstrated, not assumed:

    a world          three decompositions of one board bound unmodified
    atoms            env.atoms() is asked for, never imported
    resolutions      env.transform() is asked for
    alphabets        one number or one per slot, the domain's to declare

**What it cannot supply from outside, and this is the finding:**

    a positioned action    `drive.choose` does sorted(actions) and dies on a mixed
                           action set: TypeError, tuple < str
    a recorded action      no tether row carries WHICH action was taken

So **motor work is kernel work.** The ARC agent imports a kernel that can already express
positioned actions and intentions; it does not add them on top, because the sites are
inside the loop. Getting that backwards means editing the kernel from the agent, which is
the layer violation this project exists to avoid.

## 1 · Can the loop express a positioned action?

Partly, and the part that fails is the part that matters.

**It can CARRY one.** `Ctx.action` is typed `Any`, so a compound action passes through the
atoms untouched. A world advertising five bare actions and one carrying (x, y) binds and
runs -- once every action is the same SHAPE, because `drive.choose` sorts them.

    5 bare + 9 positioned on a 3x3 board: binds, three steps run

**It cannot ENUMERATE one.** `choose` iterates the whole action set every step and
computes a spread over all of it. A coordinate multiplies the set by the board:

    3x3    14 actions
    30x30  905 actions, and the spread is computed over every one

**That is `_bindings` again** -- the O(slots) factor that produced the 13-hour figure,
arriving on the action axis. Same shape, and the residual bound does not touch it.

**And the action is on no row.** `kernel.Frame` records `action=` on both its bet and its
repeat rows. `tether` records it on neither:

    bet     ['actual', 'bound', 'cause', 'channel', 'from_value', 'mass', 'predicted']
    repeat  ['by', 'gamma_size', 'integral', 'owed', 'phase', 'stage']

**A record that does not say which action was taken cannot answer what an action does.**
No check reads the field, so eight seats stay green over it -- A9's shape for the third
time, and this one is load-bearing for everything below.

## 2 · Can the loop express a multi-step bet?

**It needs no new row type and no contract member, and I want to be precise about why.**

`perceive(action)` calls `env.step(action)` once and compares the reading before against
the reading after. **It never assumes the env took one step.** If an action is a sequence
and `env.step` executes it, the bet is already over the whole attempt and the residual is
already about the whole attempt -- because the loop only ever sees before and after.

So the intention half is free. **The composition half is not.** Building `northwest` out
of what the actions turn out to do is composing over a second type -- actions rather than
values -- and `Gamma` is typed `val -> val`. That is a real extension and it is where I
would expect a contract question rather than a field.

**And the architecture already names it.** `instruments.py`:

    PROBE, DIRECTED, STRATEGY
    "STRATEGY arrives with routines and is 0 until then -- an honest zero, not a gap."

The third phase exists, is tied to routines, and is unbuilt. **Fifth time in this project
the thing being designed already had a name and a socket waiting.**

## 3 · What does the agent already learn about actions?

**Nothing. Every bit of action-discrimination it has was handed to it.**

`act` is the only atom that reads `c.action`, and its effect table is closed over at
construction: `v + DELTA.get(c.action, 0)` with `DELTA = {A: 1, B: 2, C: 4}`.

    spread distinguishes the actions, with `act`    33/96   (34%)
    spread distinguishes the actions, without `act`  0/96   ( 0%)

**`choose`'s discriminate branch is a property of the atom set, not a model the agent
built.** Remove that one atom and the agent cannot tell its actions apart at all. It has
never had to learn what pressing something does, because the primitive it was given
already knew.

**That is the thing the action world has to take away**, and taking it away is what makes
motor learning a question rather than a lookup.

## 4 · Constants, and what each was chosen for

`M = 7` was anchored *prime, and small enough that the harness can sweep the whole domain
exhaustively* -- and it foreclosed the coarsening question, which nobody noticed until it
blocked a build. So every constant in the action world states its purpose up front.

**Already anchored:**

    M = 7                       prime; exhaustive sweep. FORECLOSES value-coarsening,
                                because Z_7 has no non-trivial quotient
    hold = 3                    the smallest hold one-step luck cannot satisfy
    LATE = 999                  past every switch the generator emits
    DISCRIMINATE_BUDGET = 200   depth 2 over the toy alphabet, exactly
    REJECTION_HALFLIFE = 8.0    specified, not grounded, and says so

**Unanchored today, and both are about actions:**

    ACTIONS = ("A", "B", "C")        why three? nothing says
    DELTA = {"A": 1, "B": 2, "C": 4} powers of two, so no two actions sum to a third
                                     mod 7 -- probably deliberate, nowhere stated

**The action world must declare, before it is built:** how many actuators and why that
many; how many of them do nothing; how large the field is and what the size is for; how
far one actuation carries; and what the coordinate's range is chosen against. **Any of
these can foreclose a later question and the point is to know which.**

## 5 · The vacuity check, stated in advance

If motor learning does not fire, that has two readings and they must be separable BEFORE
the run:

    the mechanism does not work          <- a result
    this world could not have shown it   <- vacuous

**This world can show it only if all three are present and reachable:**

    an actuator whose effect is discoverable from the record alone
    an actuator that does nothing, so `useless` is a finding the agent can reach
    two actuators that are indistinguishable, so `I cannot tell these apart` is reachable

**And the counterpart of the resolutions guarantee:** whatever constructs the action
effects must not be shown what the agent has to learn. `_views(names)` is handed the slot
names and never `spec.rules`, which is why the offered set cannot have been selected for
resolving anything -- at any rate, checkable by signature. **The action-effect constructor
gets the same treatment: give it the arity, never the meaning.**

**An unlabelled action set where every action does something distinct and useful is still
encoded.** Most should do nothing or nothing detectable. Finding that out is the work.
