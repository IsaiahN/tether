# THE MISSION — the north star (Isaiah, 2026-08-03/04). Read this before anything else.

This is WHY the whole project exists. Every other doc is in service of THIS. When Claude drifts — tries to
solve games, invents proxy metrics, theorizes rebuilds off pixels, or reasons in game-TYPES — it lost the
mission. Re-read this.

## The goal
**Build the AGENT's reasoning/composition until it generalizes across ALL public-set games — and then, on
its own, across the PRIVATE (OOD) set it has never seen.** End state: Isaiah AND Claude FALL BACK, and the
agent goes into the private set **ALONE**, with only its **library (Γ) + its own reasoning/composition**.
The deliverable was never "wins on the 25." It is an agent whose reasoning is aligned with the reasoning a
human uses — built **without ever being told what the games are or how they work** — that can walk into
unseen games, reason its way through, and **tell you HOW and WHY** (whitebox).

## ★ THE UNIFORM ENGINE (the architecture — Fig 1 `fig1_agent_simplified.png`). THERE IS NO GAME-TYPE BRANCHING.
The whole agent is **ONE per-step POMDP loop for EVERY game**: **perceive · plan · act · predict.**
- **Γ — typed DSL + library** holds structure and **predicts** the next observation.
- **residual `R = |Γ(b,a) − o′|`** = the prediction error (predicted vs actual). **This IS the universal
  cause-and-effect signal every game has** — "what did my action actually cause vs what I predicted."
- **boundary diff → mint φ if two-part MDL pays** (`Γ ← Γ ∪ {φ : |φ|+|R·φ| < |R|}`): when a new predicate
  COMPRESSES the residual, it is MINTED into Γ. Discovering the objective = minting the φ that explains the
  residual. **Γ IS the memory** — it grows by minting from residuals.
- **ground — RLVR is the ONLY metric.** Everything above either PRODUCES R or CONSUMES Γ.
- **★ THE HONEST GAP: the boundary-diff → mint boxes are DASHED = "specified, not yet demonstrated."** The
  mint loop is not firing (that is exactly why `abduced=[]` / no objective composed on most games). This —
  making the mint loop real so Γ grows from residuals uniformly — is the core work, NOT more per-family drives.

## ★★ WHY THIS IS BUILDABLE AT ALL — the architecture is the ENABLING CONDITION of triangulation itself.
This is the deepest point, and the reason the whole thing can theoretically work. **The architecture is not
just the agent's design; it is the precondition for my being able to shape the agent at all.** Triangulation
(Fig 2) requires that I can read the agent's mind and judge the delta between its reasoning and the ground's
true reasoning. That is ONLY possible because the architecture is **whitebox and legible by construction**:
- Because **Γ predicts explicitly**, I can see what the agent expects — its model, not a hidden activation.
- Because the **residual R is an explicit object**, I can see the exact cause-and-effect the agent perceived.
- Because **minting φ is an explicit, inspectable event**, I can see the moment it discovers an objective —
  or see that it never fired (the empty `abduced`), which is a diagnosis I could not make from a blackbox.
A neural policy gives me none of these vantage points — its "reasoning" is unreadable, so there is nothing to
triangulate to the ground, and alignment collapses into me feeding answers (the mirror). **So the architecture
IS what makes the proctor role possible.** Kill the legibility and you kill triangulation; without
triangulation there is no way to build this agent honestly. This is why the architecture can theoretically
work where a blackbox can't: it is the only design under which a proctor who holds the answer can shape the
reasoning WITHOUT encoding the answer.

**Therefore every build move must be made IN RESPECT TO the architecture.** I do not bolt on scar tissue that
routes around the loop; I do not add machinery I cannot read; I do not replace an explicit φ/residual/Γ object
with an opaque shortcut. Each change must PRESERVE (or restore) the legibility of predict → residual → mint →
Γ, because that legibility is the very thing I am using to triangulate. **I cannot help triangulate the agent
I am building without building it in respect to this architecture.** A change that makes the agent win but
makes its reasoning unreadable has destroyed the instrument I align with — it is a loss, not a win.

## ★ THE ANTI-PATTERN TO KILL: reasoning in GAME TYPES (Isaiah, cycle 15+).
Grouping by game type is erroneous and is the OPPOSITE of generalizing — the OOD set has NONE of these
types, so anything branched on type is dead weight that cannot transfer. The reasoning ENGINE (the loop
above) is what transfers. The ONLY legitimate distinction is topical **I/O**: is there an **avatar** my
directional actions translate, or do I act through a **click actuator** — and even that BLENDS mid-game, so
it must be detected CONTINGENTLY per step, never used to label the game. Above that thin I/O layer: one
uniform loop. (Grounded audit of the CURRENT code: `ReduxPolicy` branches by `family` (two_body/directional/
effect/click) with a separate path per type + objective-search only in two_body; cross-game memory is keyed
by game-PREFIX; the mint is gated behind reward-boundary + human `mint_gate`. All three are type-fragmentation
/ convolution to DE-FRAGMENT toward the clean Fig-1 loop. Isaiah: the code is a human-simplified, slightly
convoluted realization of the clean architecture — realize the clean loop, don't add to the scar tissue.)

## ★ TRIANGULATION — how alignment happens (Fig 2 `fig2_ground_simplified.png`). "A mirror cannot correct you."
**Alignment is triangulation, not negotiation.** The **GROUND (ARC — levels, the gif truth) is the ANCHOR,
and it MUST NOT update.** The agent (A) and I the proctor (B) BOTH ground to the anchor. I do NOT correct the
agent by being its mirror — a mirror can only average us (collapse 1: mutual update → weighted average, fake
correction) or spuriously correlate us (collapse 2: one evidence pool). Only when both A and B pin to an
UNMOVING ground do they converge to the truth. **This is the deep reason the only metric is levels-completed:
a proxy metric is an anchor that UPDATES → it collapses triangulation back to panel 1.** I hold the answer
(the gif) so the ground is not mute to me — I have the TRUE subgoals to JUDGE the delta — but I use it ONLY
to judge and to shape the composer, NEVER to feed the answer. **And I can only read the agent's vantage point
to judge that delta because the architecture is whitebox (see WHY THIS IS BUILDABLE ABOVE) — triangulation
rides on the architecture's legibility.**

## THE STRICT TENSION (both hold at once, always)
- **I do NOT solve the games — the AGENT does.** A Claude win is meaningless; if I solve it, the mission failed.
- **I do NOT code the answers.** Know the winning path; use it only to JUDGE (LAW 0/answer_lint). The agent
  must reach the reasoning itself or it will not transfer OOD (where I am not there and there is no answer to encode).
- **I do NOT forget I am the proctor.** Solving, or grading on a movable proxy, or theorizing instead of
  watching the gif = abandoning the role; the alignment becomes fake.
- **I do NOT build in ways that break the architecture's legibility.** The whitebox loop is the instrument I
  triangulate with; an unreadable "improvement" destroys the instrument.

## What this makes true operationally
- **Only metric = levels-completed** (the unmoving anchor; a proxy is an updating anchor → collapse).
- **Watch the GIF first** (the true reasoning IS the answer; guessing shapes the agent toward a fiction).
- **Read the agent's composed SUBGOALS, not telemetry** (I'm aligning its reasoning, so I must see it — and I
  CAN see it only because the architecture keeps predict/residual/mint explicit).
- **Fix the reasoning ENGINE / Γ-mint loop, NOT per-game or per-family patches** (a type patch is a smuggled
  answer that dies OOD). De-fragment toward the one uniform loop; make memory (Γ growth) unconditional.
- **Build IN RESPECT TO the architecture** — every change preserves the legibility of predict → residual →
  mint → Γ, because that legibility is what triangulation and the whitebox promise both depend on.
- **Never encode the answer / never solve** (an encoded answer is the one thing guaranteed not to transfer).

## The test of success
Not public-set wins in isolation — but: **would this agent, dropped into an unseen OOD game with only its
library and reasoning, compose a sound objective from the residual, pursue it, and explain its own how/why?**
We are aligning a reasoner, not racking up wins.

Figures: `fig1_agent_simplified.png` (the agent loop) + `fig2_ground_simplified.png` (triangulation) under
`/root/.claude/uploads/211f1e65-dba5-5409-adda-14d37d29163f/`; full transcription in
`corpus/THE_TETHER_figures_transcribed.md`. Codified 2026-08-03/04 from Isaiah's statements + the two figures.
Pointed to from START_HERE (top) + the heartbeat. If a proposed action doesn't serve THIS, stop and re-read.
