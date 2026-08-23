# Discovery

Working document. Nothing here is a decision until you mark it one.
Nothing gets built until you say so.

**Sources read.** The eleven figures (SVG, Desktop). `THE_FORMULA (4).md`. The
Substack post.

From **`Ouroboros-Redux` @ `v4-cold`**, shape only: `cognitive_loop.py` (stage
methods and the SPEED-2 seam), `grammar.py`, `gate.py`, `perception.py`,
`planner.py`, `scheduler.py`, `composer.py`, `mint.py`, `effects.py`, `fabric.py`,
`narration.py`, `decision_rung_system.py`, `rungs/`.

From **`Ouroboros-Redux` @ `new-horse`**, shape only: `src/newhorse/grammar.py`,
`agent_loop.py`, `goal.py`, `relations.py`, `logical_grid.py`, plus `residual.py`
and `marketplace.py` because the loop's own docstring names them as its MAP stage.

From **`Ouroboros-Redux` @ `Nexus`**, shape only: `THE_MISSION_north_star.md`,
`THE_ALIGNMENT.md`, `THE_TERMINAL_CONDITION.md` (now distilled into `CLAUDE.md` as the
proctor rules), `DESIGN_the_grammar_fluent_proposer.md`, `nexus/kernel.py`,
`nexus/reasoning.py`, and `redux_arch/{molecule,probe,planner}.py`.

Nothing else in any tree was opened.

**Companion.** `docs/PHILOSOPHY.md` carries the derivation behind the figures — the
load-bearing analogies, the grounded imports, the four-region map, and the list of what
`THE_FORMULA` does not cover. This file is the build questions; that one is the why.

**Still to gather.** See §7.

---

## 1. What we are building

An agent that solves problems. Verbal or physical; the machinery is the same. The
running example is a rover on unknown terrain, because it forces every part of the
loop to be real:

- **priors** are loaded at start — knowledge about what things afford
- **atoms** are the primitives the agent can execute or express
- both are composable, and composition is the only thing MINT can do
- the agent takes the **residual** between where it is and what it is for
- it spins a hypothesis, which demands some capability
- it either has that capability, composes it, or cannot get there and says so

That last clause is the product. An agent that reports *"I cannot reach this from
what I hold"* is worth more than one that produces a confident route into a crater.

### Why the rover and the word problem are the same shape

|          | word problem                                   | rover                                     |
| -------- | ---------------------------------------------- | ----------------------------------------- |
| slots    | the entities in the problem                    | objects segmented out of the scene        |
| priors   | what kinds of things do                        | what terrain and matter do                |
| atoms    | inference and arithmetic steps                 | motions, sensor operations, manipulations |
| residual | what the statement demands but the model lacks | distance between current state and goal   |
| ground   | the check that settles the answer              | the terrain, which does not negotiate     |

---

## 2. The three goals

**G1 — the agent speaks.** Not fluency. The agent states its reasoning in a fixed
grammar, and what it says is checkable line by line. No LLM in the core.

**G2 — perceive, think, map, act; then the Gate.** The four-phase loop proposes an
action. The action does not execute until the Gate has checked that the framework
was actually used, rather than bypassed by something that reasoned however it liked
and described itself nicely afterwards.

**G3 — the framework survives being lent to an LLM.** A demonstration, not the
product. The product is the version that does not need one, because nobody will
hand a black box the world-hunger class of problem.

> **And the acceptance criterion is inverted from the field's.** An agent running this
> framework should **fail** the Turing test — it will say *"I cannot close this from what I
> hold, and here is the budget I spent"*, which is more useful and less human-like in the
> precise dimension that test measures. See `PHILOSOPHY.md` §0.1. The structural reason:
> RLHF makes abstention a **behaviour** over outputs, promptable away and calibrated to
> raters; the framework makes it a **state** the mechanism reports on itself.
>
> **And the two fluencies must not be conflated** — the corpus's own distinction, from
> `DESIGN_the_grammar_fluent_proposer.md`:
>
> | | status |
> |---|---|
> | **Compositional fluency in Γ** — reliably emitting well-typed, well-shaped compositions | **the target.** 99.7% well-typed is a real number to beat |
> | **Readable rendering of the record** — prose derived from the ledger and traceable to it | **fine.** Q16's resolution: tokens are the record, prose renders it |
> | **Human-likeness as an optimisation target** | **the failure signature.** Never tune toward it |
>
> The agent should be **fluent in the framework** and indifferent to sounding human. Three
> axes, and only the third is the trap.

> On the black-box claim: frontier models are transformers, not CNNs. The objection
> survives the correction and gets stronger — the opacity is not the architecture
> family, it is that the learned representation and the decision procedure are the
> same object. This framework splits them: the library is external, so what decided
> is readable even when what proposed is not. Much harder to argue with.

---

## 3. What is already settled

From `docs/THE_FORMULA.md` — the corrected revision, which now carries the fixes this
document produced (the `R_T` composition order, step 5 renamed SETTLE, the `α → w` rename,
and twenty-seven other changes itemised in its CHANGES section). Not open for
rediscovery:

- Eight ordered steps, and the ordering is a dependency chain. Each step consumes
  the previous step's output. A diagnosis that cannot name its step is vocabulary,
  not derivation.
- `R` is indexed per slot and never aggregated.
- ROUTE sorts into four bins before any remedy is chosen.
- Acceptance is a bargain — `|φ| + |R|φ| < |R|` — not a threshold, and `left(R,φ)`
  may exceed zero. A term can pay and still not close `R`.
- Step 7 fires on failure to **close** `R`, a different predicate from failure to
  **pay**.
- The three guards are a product. Any one at zero forces inertness.
- **A gate is not the ground.** ACCEPTED means the ground settled it. Everything
  else is a CANDIDATE, whatever the numbers look like.
- Every run declares its mode: general, specified, or grounded.
- The loop does not maintain the ground. That is a seat's office.

---

## 4. Two axes, and the human on Mars

You said the second level for a human is society, friends, family — and asked how a
human on Mars would solve this. That question separates two things I had collapsed.

**They are different axes.**

**Axis 1 — scale.** Agent ↔ population. Society lives here. This is step 6, the
membrane, `T_A` and `T_E` and `R_T`. It is where import comes from, because another
frame is where an atom you cannot derive already exists.

**Axis 2 — kind of gap, inside one agent.** Prediction error versus goal distance.
Both are agent-scale. Both exist whether or not anyone else does.

**What Mars strips is axis 1 only.** A lone human on Mars has:

- a full Γ — school already happened, the library is loaded
- priors from DNA and senses
- a live ground: Mars, which does not negotiate and does not update
- **no import channel**, because there is no second frame

So step 7's OUTWARD branch is closed to them. They can only go INWARD: extend the
instrument, sharpen in their own terms, compose inside a closure that is large
because it was filled before they left. What they lose is exactly Figure 8's union
surplus — they cannot triangulate. What they keep is the ability to mint, because
the ground still settles.

**And they still solve problems.** That is the whole answer. Society is not a second
residual. It is a second *frame*, and it belongs to Figure 8 and step 7 OUTWARD, not
to a new `R`.

**The baby is the opposite configuration**: nearly empty Γ, ground present but barely
instrumented, and import-dominant — mirroring *is* import from a peer frame, which is
why a baby without one does not bootstrap.

### The design decision that follows

**Our agent is the adult on Mars, not the baby.** Rich priors loaded, live ground, no
import channel. Which means deferring step 6 and IMPORT is not a convenience — it is
the correct configuration for the target. The agent must be complete without them.

Corollary worth writing into the README: an agent that *cannot function* without a
population has not demonstrated the thing. The population makes it faster; the lone
agent is what makes it real.

---

## 5. The questions, and what is still yours to rule

Twenty-nine entries, numbered as permanent IDs — **Q-numbers never change**, so a
reference stays valid. Sorted numerically below; status is the thing to read.

**SETTLED** — the answer is known and recorded. No decision needed.
**DECIDE** — a recommendation is ready and I will not build on it until you rule.
**OPEN** — genuinely unresolved.

### If you read nothing else, these are the rulings that unblock a build

| | question | my recommendation |
|---|---|---|
| **Q12** | one track or two? | **one.** The derivation *is* the decision, with no fast path to fall back to. This is the whole rebuild |
| **Q11** | which three guards? | **SUPPORT × REACHABILITY × NOVELTY**, MDL as the bargain after. Two of three sources agree; the outlier is the one that stalled |
| **Q27** | which domain first? | **the one with the best ground.** May change the toy env from a gridworld to an expression evaluator |
| **Q1** | one residual or two? | **two, one router** — and Q21 supplies the measurement, so this is closer to settled than open |
| **Q15** | does the Gate block? | **yes, from step one.** A shadow mode is not a cautious rollout, it is the failure pre-installed |

### The full index

| ID | question | status | the answer, or the ruling I need |
|---|---|---|---|
| **Q1** | one residual or two | **DECIDE** | two, one four-bin router. Q21 measures the second; `scheduler.py` rebuilt the same split independently |
| **Q2** | what may the Gate see | **SETTLED** | three currencies — ledger, executable, completeness — over a reification, domain-blind. One rider open: is completeness the primary perception metric? |
| **Q3** | what is a prior | **SETTLED** | a molecule: a named type-valid composite with holes, stamped `prior`. One closure, not two |
| **Q4** | how does the agent speak | **SETTLED** | a typed utterance; terminals produce RECORDs so precedence type-checks; the typed hole is the probe |
| **Q4b** | and the LLM tension | **SETTLED** | a tiny DSL-native proposer trained on the enumerator's own output. Proposes, never scores, never promotes |
| **Q5** | what is MAP | **SETTLED** | the priced market. External currency, Goodhart-guarded |
| **Q6** | the visual interpreter | **SETTLED** | classical segmentation, no downsampling, permanence by overlap, death only on evidence. Input format still to gather |
| **Q7** | what settles a mint | **SETTLED** | the ground, by held-out payment. Candidate until then, and **held but not cited** |
| **Q8** | `cost(R)` per-step or accumulated | **SETTLED** | **accumulated per slot** — and that makes an evidence-count gate unnecessary |
| **Q9** | guards boolean or scalar | **SETTLED** | booleans are the zero-checks on the three scalars. Implement booleans |
| **Q10** | one vocabulary or two | **DECIDE** | two, bridged by RECORD — but the bridge must be the only path. Every hypothesis reaches the market as a Term or not at all |
| **Q11** | which three guards | **DECIDE** | SUPPORT × REACHABILITY × NOVELTY, MDL after |
| **Q12** | what makes the framework load-bearing | **DECIDE** | one track. No fast path. Expect the agent to be worse at first |
| **Q13** | memory ranges | **DECIDE** | carry `[EP]`, `[OWN]`, `[REPLAY]` now; defer `[COL]` with step 6 |
| **Q14** | the magic numbers | **SETTLED** | one constants block, every entry carrying mode and provenance. No bare numbers |
| **Q15** | does the Gate block | **DECIDE** | yes, from step one |
| **Q16** | prose or fixed tokens | **SETTLED** | tokens are the record; prose renders it. Three fluencies, only human-likeness is the trap |
| **Q17** | the brake invariant | **DECIDE** | carry it, and carry that it is structural. No `suppress()`, no reset, no decay |
| **Q18** | learn own effects first | **DECIDE** | a phase, not a flag. Goal pursuit gated on a complete action map |
| **Q19** | when may it change its representation | **SETTLED** | only when the round trip is near-lossless. `R_T` gates the abstraction; keep the original either way |
| **Q20** | SUPPORT at zero | **SETTLED** | probe — uninformed, triggered by own prediction error, outcome back through the same residual |
| **Q21** | is `R_goal` measurable | **SETTLED** | yes: `1 − degree(molecule)`, priced by the same MDL one level up |
| **Q21b** | self-application | **SETTLED** | every mechanism legal under the framework's own rules. Applies to itself, does not certify itself |
| **Q21c** | the harness | **SETTLED** | a substituted habitat. Every run report says a synthetic solve proves wiring, never capability |
| **Q22** | the seat stack | **DECIDE** | lazy instantiation, a meta-continuation. Depth set by escalation, not by hierarchy |
| **Q23** | the ledger | **SETTLED** | a reification, which is *why* a domain-blind checker is sound |
| **Q24** | requisite variety | **SETTLED** | `H(outcome) ≥ H(disturbance) − H(regulator)`. Not falling → mint or probe, and they are not interchangeable |
| **Q25** | the branching test | **SETTLED** | no divergence means no transform. Checkable from outside |
| **Q26** | instantiating in a domain | **DECIDE** | the eight-slot binding table as the literal `Env` protocol. Cannot fill all eight → fails at construction |
| **Q27** | build order | **DECIDE** | by the quality of the ground. Crisp ground tests the machinery; poor ground tests the alignment claim |

**Still genuinely OPEN, and small:** Q2's completeness rider, and what the rover's input
actually is (Q6, §8).

> ### ⚠ Read §11 before acting on this table.
> **§11 audits every entry above against the eleven figures**, and four statuses change:
> **Q1 is SETTLED by Figure 1** (three residual channels — `transition · reward · bracket`
> — not one or two); **Q5 reopens** (Figure 1's phases are *perceive · plan · act ·
> predict*, so my answer came from a branch rather than the spec); **Q20 widens** to two
> triggers on two channels; **Q27 is reframed** (Figure 2's axis is constitutive-versus-
> instrumental, not good-versus-poor ground). §11 also lists **ten things the figures carry
> that this document does not**, most of them build rules.

---

### Q1 — One residual or two?  ·  DECIDE

`THE_FORMULA` defines `R = |Γ(b,a) − o′|`: prediction error. Your rover description
defines a gap against the **goals**. §4 rules out "society" as the answer, so the
question stands on axis 2 alone.

**Recommendation.** Two residuals, one router.

- `R_pred`, per slot, drives MINT of predicates — the formula's `R`
- `R_goal`, per objective, drives composition of actions

**And Q21 supplies the measurement**, which moves this from a proposal to a design with
a number behind it: `R_goal = 1 − degree(molecule)`, priced by the same two-part MDL one
level up. What remains is your ruling, not a missing mechanism.

**Second witness.** `scheduler.py` independently built the same
discrimination for the goal side. Its abort router splits a failed plan into
**WORLD-MOVED** (state changed under the plan — re-plan, atoms not penalised) versus
**PLAN-WRONG** (state exactly as predicted and the step still failed — recorded
against the plan). That is `BROKEN·rebinding` versus `BROKEN·mechanism`, arrived at
separately, for goals rather than predictions. Two residuals sharing one four-bin
router now looks less like a proposal and more like a rediscovery.

### Q2 — What does the Gate check, and what may it see?

**Largely answered by `gate.py`, and its answer is better than mine was.** Three
check currencies, one riding each head:

| currency         | what pays it                                                     |
| ---------------- | ---------------------------------------------------------------- |
| **LEDGER**       | looked up in the agent's own earned records                      |
| **EXECUTABLE**   | run through the world's own mechanics                            |
| **COMPLETENESS** | a set checked *as a set* against what actually differed          |

Plus PARSE, which precedes all three: an ill-typed utterance is refused at the head
before any currency is charged. Every refusal names the failing head and a **fixed
token**, never prose.

**The builder/gate split, which is the load-bearing part.** The builder translates
decision state into an utterance and reads **only the agent's own state**. The Gate
reads the world and the ledger. Neither reads the other's sources. And it is
enforced by an import-time AST wall: a builder that so much as *names* an after-state
variable fails at import.

That is Figure 10 implemented in the file system rather than promised in a comment,
and it is a stronger version of what I proposed. Carry it.

**Still open:** the completeness check is the one that measures map fidelity
(differing vs reported). Nothing currently reads it as one. Should it be the primary
perception metric?

**Warning to write into the code.** A passing Gate means well-formed. It never means
right.

### Q3 — What is a prior, mechanically?

Unchanged from last round, and the reference tree does not settle it. `fabric.py`
has a `priors()` read — all visible ideas for a game across collective, personal and
kin — but those are *learned* ideas pooled from other agents, which is import, not
the DNA-and-senses priors of §4.

**Recommendation.** Priors are terms in Γ with a different origin stamp — `prior`
rather than `minted` or `imported`. One composition space, one closure, provenance
distinguishes them. `effects.py` already stamps an origin marker at write time, so
the mechanism exists.

**Partly answered by `new-horse`.** `grammar.py` has MOLECULES — named typed
composites, each type-checking by construction:

```
MATCH  =  SOME( SAME(ATTR, ATTR) )
REACH  =  SOME( BE_AT(OBJECT, REGION) )
CLEAR  =  NONE( EXIST(OBJECT) )
```

**That is what a prior is, mechanically: a named, type-valid composite carrying
typed holes, loaded at start, composable like anything else.** It is not a separate
population and it needs no separate composition space — which settles the literal
reading of "combine priors together, and primitives with each other" in favour of
one closure. A prior is a molecule; an atom is a prime; both are terms.

**Still needs answering:** what molecules does the rover start with, concretely?

**The objection to pre-empt.** A hand-authored library of composable knowledge
predicates is Cyc. The answer is that Cyc's ontology was graded by its authors and
these are graded by a ground that does not update — but say it in the README before
a reader thinks it.

### Q4 — How does the agent speak? (answered; my template idea was wrong)

**`grammar.py` is the best thing in that tree and it should survive nearly intact in
shape.** Speech is not templates. Speech is a **typed composition**, and the type
system enforces the loop's own dependency chain.

Five world types — OBJECT, ATTR, REGION, PRED, OBJ — plus two speech types, RECORD
(a citable id) and PRICE (a cost claim with its evidence count, or an explicit null).

Thirteen primes, grouped by Kant category, building PRED and closing into OBJ:

```
Relation  BE_AT  TOUCH  BECOME  BECAUSE
Quality   SAME   OTHER  NOT
Modality  EXIST  CAN
Quantity  ALL    SOME   ONE     NONE
```

Nine speech heads under three terminals:

```
PERCEIVE  <-  SEE, CHANGED, SETTLE, STAND
BET       <-  WANT, GROUND, DERIVE, PAY
ACT       <-  NEED
```

**And here is the move that matters.** Each terminal *produces* a RECORD. So BET's
GROUND consumes the PERCEIVE record, and ACT's NEED consumes the BET record — which
makes **precedence type-checkable**. A later step can only consume what an earlier
step produced. That is `THE_FORMULA`'s "each step consumes what the one before
produces", implemented as a type system rather than as a convention. It is the single
best idea in the reference tree.

Two more properties to keep:

- `compose()` **raises with its reason, never silently.** An ill-typed utterance is a
  refusal with a named head, not a shrug.
- The **typed hole** — a bare type as a leaf — is a template without content, and it
  is how the agent asks a question. A DERIVE with a hole in the bet position *is* the
  probe. That is the grammatical form of "I do not know", and it typechecks.

**What this gives us for free.** The abstention sentence I wanted becomes a
well-formed utterance rather than a special case: a WANT with a holed objective, a
GROUND citing what was actually perceived, a DERIVE that is a probe, and a PAY of
explicit null with its reason. The agent says *I cannot close this* in the same
grammar it uses to say anything else, and the Gate checks that claim the same way.

**Open sub-question.** Nine heads was a hypothesis, and the basis rule in that file
says heads grow or merge only on a composition failure surfaced as a named refusal.
Do we inherit the same discipline, and do we inherit nine?

#### Q4b — And the "no LLM" tension is already resolved, on `Nexus`

`DESIGN_the_grammar_fluent_proposer.md` settles what I had been treating as a hard
constraint. It is not "no model". It is **no model in the decision path**, and there is
a specific, built, measured design for the part a model may legitimately occupy.

**A tiny model trained on Γ itself.** TinyStories recipe — narrow clean domain gives
fluency at tiny scale. The corpus is the interesting part:

> **The type-directed enumerator, run generatively instead of as a filter, IS the corpus
> generator.** The same type discipline the mint search already uses, pointed the other
> way. Unlimited well-formed examples, free, available now, no bootstrap.

Built and measured 2026-08-02: 3,246 well-typed terms at depth ≤3 became the corpus, a
19-token DSL-native alphabet, and the resulting proposer emits **99.7% well-typed** terms
against **0%** for random tokens. Conditioning on a seed term holds at 99.6–100%.

**The one hard rule, and it is exactly the asymmetry this project is about:**

> *"Fluent = plausible = a proxy. The proposer **proposes, never scores**."* Extended one
> level up for forward-projection: **never promotes**. Even its own perplexity is a
> training signal, not an acceptance metric. Kept strictly upstream of the gate it is
> pure upside — *it cannot corrupt the metric because it never touches the metric.*

**Why this satisfies the trust argument rather than compromising it.** The proposer is
~millions of parameters, local, in-process, with a vocabulary that is your own DSL, and
its every output is type-checked, MDL-priced and ground-settled before it can matter. It
lowers the branching prior of the mint search and does nothing else. Nobody has to trust
it, which is the entire point — the thing that must be trusted is the checker, and the
checker is small enough to read.

**And the honest limit is Figure 6, stated independently:**

> *"Front-loads recombination WITHIN Γ's expressive envelope; does NOT solve true
> transfer. You can only project worst cases you can express."*

That is *MINT composes inside the closure and can never add an atom*. The proposer makes
composition cheaper; **only IMPORT moves the wall.** The doc says so in its own words and
warns it must not become a reason to skip extending the vocabulary.

**Recommendation.** Adopt it, adopt the rule verbatim, and put the rule in the code:
the proposer's output type is *candidate*, and there is no method by which it can
produce anything else.

### Q5 — What is MAP? (answered by `new-horse`)

`v4-cold` had no answer: `cognitive_loop.cycle()` is documented as a
"Perceive-Think-Map-Act cycle" but the stage methods are `_perceive`, `_think`,
`_act`. There is no `_map`. The phase existed in a docstring and not in the code.

**`new-horse` has it, and it is not what I guessed.** From `agent_loop.py`'s own
wiring block:

```
PERCEIVE  perception.segment + ObjectTracker  -> the controllable object, held steady
THINK     generic transforms as hypotheses    -> filtered by the falsified ledger
MAP       marketplace.informative_salience    -> score each hypothesis by the
                                                 residual it leaves
ACT       commit the best-believed action     -> take it, observe the real frame
```

**MAP is the market.** Propose → vote → resolve, where the currency is prediction
error and the price is what selects. My recommendation (hypothesis → required
capability) was wrong; that work lives in `v4-cold`'s planner and composer, which
is a different thing.

Two properties of that market matter more than the phase name:

- **The currency is measured externally.** *"A hypothesis cannot self-report its own
  salience."* That is Figure 1's "a frame cannot score itself with a quantity it also
  produces", arrived at independently and implemented.
- **The currency is Goodhart-guarded by construction.** Credit is for predicting the
  cells that *actually changed*, minus hallucinated change. A hypothesis that
  predicts "nothing changes" scores **zero** on a frame that changed, so it can never
  win by saying nothing — and over-claiming is penalised too. That is Figure 5's "a
  term that explains everything by saying nothing" closed off in the scoring function
  rather than warned about in prose.

**Recommendation: adopt MAP-as-market, with both properties, verbatim in shape.**

### Q6 — The visual interpreter (answered)

`perception.py` is 219 lines and the shape is right. Carry it:

- **Never downsample.** A symbolic glyph is exact; averaging destroys it. Enforced by
  a raise, not a convention.
- **Segmentation = connected same-symbol components** — near-decomposable clusters,
  after Simon. The boundary is where cohesion drops.
- **Segmentation is a revisable belief, not a fact.** Objects carry `belief=True`. If
  a boundary moves, re-segment.
- **Object permanence by overlap, not by paint.** Identity is founded at first sight
  and carried by IoU, so it survives recolour and reshape. It persists through
  non-observation (occlusion) and **dies only on evidence** — when its cells are
  taken over by other live objects.
- **Nothing silent.** Every id records why it was born, kept, occluded, or retired.

Objects are slots. That is the whole bridge to the rest of the loop.

**Still needs answering:** what is the actual input for the rover — real images, a
renderer, or synthetic terrain arrays?

### Q7 — What settles a mint at agent scale?

Still open. Best reading remains **held-out payment**: a candidate becomes ACCEPTED
once it predicts transitions it was never fitted to. The ground settles a term by
continuing to behave as the term says.

Support from the tree: `narration.py`'s ECHO point emits "what settled, or *candidate*
stated as such", so the distinction was already being tracked. And `composer.py` has
a **citability rule** — a composite is not citable until settled, and `live_settle`
is the one writer of that flag. That is the same idea with teeth: an unsettled term
cannot be used as evidence in a later bet.

**Recommendation.** Adopt citability. A candidate may be *held*, but may not be
*cited*. That single rule stops unsettled terms from compounding.

### Q8 — `cost(R)`: per-step or accumulated?  ·  SETTLED

**Where the ambiguity lives:** not inside one figure, but in the **join between Figure 1
and Figure 5**, which neither states. Figure 1 defines `R` per-step, per-slot — *one bet
per object slot, every action*. Figure 5 then prices a term against `|R|` without saying
whether that is this step's residual or the slot's accumulated history.

**Accumulated, and the argument is what makes two-part MDL discriminate at all.**

`L(model) + L(data | model)`: the model cost is paid **once**, and the savings scale with
the number of observations it explains. A term capturing a real regularity saves on every
future observation; a term memorising one occasion saves once and costs its own length.
**That discrimination requires n > 1 to operate** — at n = 1 there is nothing to amortise
and the test degenerates into constants.

**And accumulation makes an evidence gate unnecessary — which removes machinery.**

My spike had `min_support: int = 2`: a magic number with no provenance (Q14), and also
**redundant**. Early on a slot's accumulated `|R|` is small and almost nothing pays. As
evidence accumulates the *same* term — same fixed `|φ|` — starts paying, because it now
explains five transitions instead of one.

> **The bargain is its own support gate. The evidence requirement is emergent from the
> arithmetic, not imposed as a threshold.**

Which means Figure 5's SUPPORT says exactly what it should: *"the gap has real mass
somewhere."* Is there anything to explain — **not** is there *enough*. The figure was
right; I added "enough" and it was never there.

**And this reconciles the third option rather than choosing against it.** `v4-cold`'s
`mint.py` mints from one contact event and then *intersects* the context with each later
matching observation, so varying cells become `DONT_CARE`. That looked like a third
theory. It is not: it is mint-as-candidate, and each later mismatch routes through step 2
as **`BROKEN · rebinding`** — *the model is right and attached to the wrong thing; re-fit,
do not mint*. **Narrowing is the refit.** The loop already handles it with no new rule, and
it keeps the agent acting on a hypothesis instead of sitting inert while it collects.

### Q9 — Guards: booleans or scalars?

**Recommendation unchanged** (booleans are zero-checks on the three scalars), but the
reference tree raises a sharper problem — see Q11.

### Q10 — Two vocabularies or one?

`grammar.py` has 13 primes for *stating*. `effects.py` has atoms for *doing*, learned
from contact events. They are different type systems, bridged only by RECORD: DERIVE
cites `RECORD[atom]`.

**The question.** Is Γ one library the agent both reasons in and acts through, or two
libraries with a citation bridge?

**`new-horse` makes the problem worse and diagnoses it at the same time.** There,
`grammar.py` holds the typed primes, `compose()`, and MOLECULES — and **nothing in
`src/` imports it.** Its only consumer is its own test. The live agent reasons through
`relations.py`, which emits `BE_AT` / `TOUCH` / `COVER` as bare `(name, cell)` string
tuples into `goal.py`'s price market. Same vocabulary, two parallel implementations,
no call between them.

So `grammar.compose()` never runs in play. The typed grammar is a basis and a
search-space counter, not a decision procedure.

**Recommendation: keep the bridge, do not unify — but the bridge must be the only
path.** What the agent can *say* and what it can *do* are genuinely different
closures, and collapsing them would make every utterance an action proposal. But if
a relation can be proposed as a string tuple that never passes through `compose()`,
the type system is decoration. Every hypothesis reaches the market **as a Term or not
at all.**

### Q11 — Which three guards?

**A real divergence, and it needs your ruling.**

`THE_FORMULA` step 3: **SUPPORT × REACHABILITY × NOVELTY**, with MDL as the *bargain*
that runs after the guards pass.

`mint.py` in the tree: **SUPPORT × NOVELTY × MDL**, as the product. REACHABILITY is
absent, and the bargain has been promoted into a guard slot.

These are not the same architecture. Dropping REACHABILITY is what removes the ability
to say *"nothing I hold can build this"* — which is step 7's trigger and the abstention
behaviour that makes the whole thing worth building. My read is that the tree lost the
most important guard, and that this is one of the reasons the framework track ended up
in shadow.

**Settled by `Nexus`.** `probe.py` states the product with the scalar names, and it
matches `THE_FORMULA` exactly:

```
novelty capacity = density(R) × orthogonality(R, Γ) × reachability(φ, Γ)
                   └ SUPPORT      └ NOVELTY            └ REACHABILITY
```

with MDL as the bargain that runs after, not as a factor. Two of three sources agree;
`v4-cold`'s `mint.py` is the outlier, and it is the one that stalled.

**Ruling: SUPPORT × REACHABILITY × NOVELTY, MDL as the bargain afterwards.** Q9's scalar
reading is confirmed at the same time — the booleans are zero-checks on these three.

### Q12 — What forces the framework to be load-bearing? (the biggest one)

See §6. `gate.py`'s own first line is *"REASONING GATE STAGE 1: SHADOW MODE"*, and
`refuse` is zero by construction — no code path returns a blocking verdict. The agent
utters, the gate checks, the result is logged, **and the action proceeds regardless.**

So the reference system has two tracks. Track A picks actions through a 77-rung ladder
(~9,700 lines across `rungs/`, of which `exploitation.py` alone is 4,570). Track B
states reasoning and is watched. 266,570 decisions went through Track A while the
framework named none of them.

**This is the thing not to carry, and it is the whole point of the rebuild.**

**Recommendation: one track. The derivation *is* the decision.** Not "the loop decides
and the gate audits" but "the utterance is how an action is proposed, and an utterance
that does not typecheck and pass is not an action." There is no fast path to fall back
to, because a fast path is what made the framework optional.

**The uncomfortable consequence, stated up front:** the agent will be much worse at
first. The rung ladder exists because it worked. Deleting it means the framework has
to carry the performance itself, and early on it will not. That is the correct trade
and it should be a stated expectation rather than a surprise in week three.

### Q13 — Memory ranges

`narration.py` tags every record with one of `[EP]` this episode, `[OWN]` this agent's
history, `[COL]` the collective with contact-class provenance, `[REPLAY]` playback
narrated as playback.

`[REPLAY]` is Figure 4's membrane rule enforced in the record: playback is never
narrated as a fresh decision.

**Recommendation.** Carry `[EP]` and `[OWN]` now; they are agent-scale. Carry
`[REPLAY]` now — it costs nothing and prevents a real error. Defer `[COL]` with step 6.

### Q14 — The magic numbers

The tree is full of tuned constants: MDL margin `0.9`, compressibility wall `0.5` of
board area, cheap-route confidence bar `0.5`, birth IoU `0.30`, death occupancy
`0.50`, settle epsilon.

Under the Mode rules these are **specified**, not grounded — named targets for
measurement. Several are annotated in the tree as `provenance GUESSED`, which is
honest and should be preserved.

**Recommendation.** One constants block, every entry carrying its mode and provenance.
A number without a provenance tag does not go in.

### Q15 — Does the Gate block?

The tree has a rollout ladder — `off` / `observe` / `active` — defaulting to `observe`,
with `active` explicitly not built. Stage 2 was meant to be a flip.

**Recommendation.** Skip the ladder. Build it blocking from step one. Given Q12, a
shadow mode is not a cautious rollout — it is the failure mode, pre-installed.

### Q16 — Fluent prose or fixed tokens?

You said `new-horse`'s reasoning log felt more fluid for NSM composition, and that
you were not sure. I think you are picking up something real, and the cause is the
opposite of an improvement.

`new-horse` logs read well because they are **prose**:

```
GOAL     pursue ('BE_AT', (12, 7)) (price 1.00)
COMMIT(nav)  RIGHT dir=(0,1) from=(11,7) goal=BE_AT((12,7))
REPROBE  UP from=(4,9) (tries=1/3) -- completing the action map before nav
```

`v4-cold` deliberately refused prose: *"Every refusal names the failing head and a
FIXED token, never prose."* Its output is worse to read and it is the only one of the
two a Gate can check, because a fixed token is a value and a sentence is not.

**So the fluency is real and it is a symptom.** `new-horse` reads better precisely
because nothing is checking it. The fluent line is a narration *of* a decision;
`v4-cold`'s token is a claim *in* one.

**Recommendation.** Fixed tokens are the record; prose is a rendering *of* the record,
generated afterwards and never the thing checked. Then you get both — `speak.py`
renders the readable sentence, `gate.py` checks the tokens, and the sentence is
verifiable because it was derived from something that was.

### Q17 — Does the brake invariant come with us? (I think yes, and it is important)

`new-horse`'s `residual.py` holds something neither `THE_FORMULA` nor the figures
state explicitly:

> **NO DRIVE MAY EVER SUPPRESS THE TIME-INTEGRAL OF PREDICTION ERROR.**

Two quantities, not one:

- `pe_integral()` — every surprise ever, **monotone non-decreasing**. There is no
  `suppress()`. A drive may read it, never zero it.
- `outstanding()` — surprise not yet explained. This is the aim and the currency.
- `explain(bits)` reduces **outstanding only**. The integral is untouched, because
  understanding a surprise afterwards does not unmake having been surprised.

**Why this is load-bearing.** `THE_FORMULA` step 8 says the loop stops in two ways
that look alike from inside — a perfect prediction, or a closed channel — and that
detecting the second is *not something the loop can do*, because a loop with no error
signal has nothing to detect with.

The monotone integral is a partial structural defence against exactly that. A system
that could zero its own surprise record could look calm by forgetting it had ever been
wrong, and the two cases would become indistinguishable from outside as well as
inside. Keeping the integral un-suppressible means a seat can read the divergence
between "integral flat because nothing surprising happened" and "integral flat because
nothing is arriving" against the record rather than against the moment.

**Recommendation: carry it, and carry the fact that it is structural.** No suppress
method, no reset, no decay. If a later design wants forgetting, it argues for it
explicitly rather than getting it by omission.

### Q18 — Learn your own effects before pursuing goals?

`agent_loop.choose()` has an ordering worth noticing. Before it will navigate anywhere
it runs **coverage-first**: try every action until the action-map is known, then
**re-probe** any action still unmapped from a *different cell* each time — because an
action can look inert merely from having been tried twice against a wall. Inert is a
verdict earned by trials, never assumed early. Only once the map is complete does goal
pursuit begin.

That is the `self_as_slot` flag from my earlier spike, but as a **phase** rather than a
toggle: the agent models its own effects first, and its goal-seeking is gated on having
done so.

**Recommendation.** Make it a phase, not a flag. An agent that pursues a goal before
knowing what its own actions do is betting with an unmodelled slot, and the slot is
itself.

### Q19 — When may an agent change its own representation? (`logical_grid.py` answers it, and computes `R_T` to do it)

Neither `THE_FORMULA` nor the figures say when an agent is allowed to adopt a coarser
vocabulary for its own thinking. `logical_grid.py` answers it, and the answer is the
round trip.

**What the file does.** Many boards are a small logical N×N grid rendered up into a
64×64 frame, so a click must land on a cell centre and a "move" is one logical cell,
not one pixel. `detect_grid` finds that hidden lattice — or returns `None`.

**Three properties, each of which is a figure implemented.**

**1. The lens is added, never substituted.** It supplies a pitch, a cell↔pixel mapping,
and non-destructive per-cell reads. `logical_read()` is explicitly *"a DERIVED reasoning
VIEW ... for THINK-stage coordinate reasoning ONLY — it is NOT the working frame and
must NEVER be fed to perception."* Raw full-resolution perception is untouched.

That is Figure 4's membrane, applied *inside one agent* between resolutions rather than
between scales: a coarse view may inform thinking and may never become what perception
reports. Generators cross up, playback never does — in miniature.

**2. `fidelity()` is `R_T`, and it gates the transform instead of merely reporting it.**

`fidelity` is the fraction of pixels equal to their own cell's modal colour. Abstract
(modal colour per cell) then concretise (paint the cell), and the pixels that come back
wrong are exactly the non-modal ones. So:

```
R_T  =  1 − fidelity(frame, pitch, pad, N)
```

This is the **only place in either branch where `R_T` is actually computed.** And it is
not used as a report — it is the admission criterion for the abstraction itself. Figure
4 says take the round trip and measure the gap; this takes the round trip and *refuses
the coarser vocabulary when the gap is not near zero.*

**Recommendation: this is the general rule.** An agent may adopt a derived
representation only if the round trip through it is near-lossless, and it must keep the
original either way. That answers a question the formula leaves open, and it is
implementable in any domain.

**3. The arbiter is a measurement, not a vote.** The file's own note: Arrow's
impossibility says no rank-order vote among competing axis/pitch candidates cleanly
picks the true grid — so the arbiter *is not a vote*. Candidate grids do not rank each
other; each is measured against the pixels, which can refuse.

That is Figure 2, arrived at from Arrow rather than from the figure: alignment is
triangulation, not negotiation, and a room's agreement is variation rather than a
verdict.

**And then the calibration story, which is the best single receipt in either tree.**

- ls20's *true* grid is 5px — the piece moves exactly 5px per action
- whole-frame fidelity at 5px is only **0.818**
- the only tiling that passes a 0.93 gate is a **spurious** 2px/24×24 one at **0.946**
- so a plausibly-tuned gate commits, confidently, to the **wrong** grid
- the gate was therefore set near-lossless (0.98), ls20 is correctly rejected as native,
  and the stride is recovered from **motion** instead

A measure tuned to a reasonable-looking threshold picks the confident wrong answer over
the honest refusal. The fix was to make the gate strict enough to abstain, and then get
the answer from a *different instrument*.

That is Figure 6's inward/outward split executed: the tiling instrument cannot carry
ls20's stride at any honest threshold, so stop refining on an axis that cannot hold it
and go to another instrument. *"Fails by refining forever on an axis that cannot carry
it."*

**Two more things to carry from it.**

- **Fail toward refusal.** *"A wrong grid makes located clicks MISS (abort), never a
  false win."* The failure mode was designed to be visible rather than rewarded. Figure
  10's arrange-for-refusal, as a design habit rather than a seat.
- **`None` is a real answer.** `detect_grid` does not return a best-effort grid for a
  board that has none. This is the abstention behaviour, already implemented, in a
  perception primitive — the small version of *"I cannot close this."*

**For the rover.** There is no logical lattice, but the shape generalises: a lens is a
derived coordinate system committed only when the round trip is near-lossless, and
refused otherwise. Traversability lattice, terrain patch decomposition, the scale at
which ground is locally planar — same test, same refusal, same fallback to another
instrument.

**And it is the one constant in either tree with exemplary provenance.** `0.98` is not
`GUESSED`; the docstring records the measurement that forced it, including the value
that would have been wrong. That is Q14's standard, met once. It is the template.

### Q20 — What happens when SUPPORT is zero? (`probe.py` answers a gap in the formula)

`THE_FORMULA` says SUPPORT is checkable before the search and that a guard at zero forces
inertness. It does not say what to *do* about it. `probe.py` does, and the diagnosis
behind it is the sharpest self-criticism in any of the three branches:

> *"Eight builds attacked the third factor for eight +0s while the FIRST factor was never
> touched. If `|R| ≈ 0` then `|φ| + |R|φ| < |R|` is unsatisfiable and NO φ can mint,
> whatever atoms exist."*

With the receipts: uniform noise visits 884 distinct frames on one game while the agent
orbits 51 distinct frames in 2,050 steps on another. *You cannot compress what you never
observed.*

**The remedy: random perturbation as an experiment.** And the line it must not cross is
drawn mechanically rather than rhetorically:

> ✗ random action selection **to score** is Goodhart — buys wins, proves nothing
> ✓ random perturbation as an **experiment whose outcome is consumed by the residual**

The separator is that the probe's outcome enters as an ordinary observation, is scanned
by the same residual, and is scored under the unchanged MDL guard. *"Nothing here scores,
mints, promotes, or exempts."*

**Three properties worth carrying whole:**

- **The trigger is the agent's own prediction error and may be nothing else.** Never a
  score, never a step count. The forward model is deliberately the weakest one that still
  has a residual — the modal magnitude bucket per action. It fires when the error EMA has
  fallen to ~0 *with enough observations behind it to be a model at all*: the agent
  explains everything it sees, therefore it is learning nothing, therefore it must
  perturb.
- **It is a closed loop.** A probe that shakes something loose raises the error and
  *suppresses further probing* until the agent has explained what it found. The probe
  rate self-regulates to the rate at which the world still surprises.
- **It is uninformed by construction, and that is the safety property.** The draw sees
  the advertised action set and the board's shape. Not the score, not the goal, not the
  effect model, not a colour. *"A probe chosen by the current model can only confirm the
  current model; a probe aimed at reward is the Goodhart failure wearing a probe's coat."*

**Recommendation.** Adopt it. My spike's `NO_SUPPORT` verdict just returned, which is
inert exactly where the loop most needs to move. The correct branch is: **no support →
probe, uninformed, and feed the outcome back through the same residual.**

### Q21 — Is `R_goal` measurable? (`molecule.py` says yes, and prices it the same way)

Q1 proposed a goal residual without saying how to measure one. `redux_arch/molecule.py`
has it.

A **molecule** is a quantified typed objective — `quantifier(ALL/SOME/ONE/NONE)` over an
inner relation, evaluated across a *scope* of objects under a pairing mode
(`consecutive` / `all_pairs` / `unary`). It returns a verdict **and a continuous degree**:

```
ALL   -> fraction satisfied            NONE -> 1 − fraction satisfied
SOME  -> fraction satisfied            ONE  -> peaks at exactly one
```

**So `R_goal = 1 − degree(molecule)`,** and it is graded rather than binary, which is what
makes progress measurable at all.

**And it is priced by the same bargain, one level up.** `score_molecule` asks whether the
molecule's per-step degree partitions the progress stream, thresholded at *its own median*
so the split is data-driven — *"no free parameter"* — and charges two bits for the
molecule's description. Same two-part MDL, applied to objectives instead of transitions.

**Recommendation.** One bargain, two levels: atoms priced against transitions, molecules
priced against progress. That closes Q1 — the two residuals genuinely do share machinery,
which is the strongest argument yet that they are two readings of one mechanism rather
than two mechanisms.

### Q21b — Self-application is a build requirement, not a stylistic one

From `PHILOSOPHY.md` §0.2. Every law in the figures applies to the framework itself, and two
figures say so in those words. It is forced — a theory about frames that exempts itself is
special pleading — and it survives Gödel only in the precise form:

> **The framework applies every law TO itself. It does not CERTIFY itself.**

**Recommendation, as checkable properties of the build.** Every mechanism must be legal
under the framework's own rules; where one is not, that is a defect in the mechanism or in
the rule, never an exemption. The ones with teeth here:

- nothing the system produces may be used to score it (Figure 1)
- the Gate is subject to the seat's own prohibitions, including being unable to reconstruct
  what it checks
- a mode is declared on the run's output, **including on the run's own diagnostics**
- **the observer's defect** — a new instrument's first output is a claim about the
  instrument, not about the system

**And the reason it had to be recursive:** the anchor was natural selection, so anything put
in its place must preserve the same six-part order — variation before selection, selection
external to the variant, generators up and never recordings, environment shapes / actors
select, the ground does not negotiate, the lineage carries what no individual does.

**Which reframes the proctor rules in `CLAUDE.md`.** They are not a working style. Each is a
clause of that substitution, and relaxing one does not make the build faster — it makes the
result stop being selection and start being authorship, and an authored result does not
transfer because nothing external ever tested it.

### Q21c — The harness is a substituted habitat

`PHILOSOPHY.md` §0.3. The cat in the box and the agent in the test harness are the same
object: substituted habitat, stale model of the real one, and no way to tell from inside.

**Recommendation.** Whatever env we build, the run report states plainly that a synthetic
solve proves **wiring** and never **capability**, and it names what the harness failed to
reproduce as far as that is knowable. Figure 11's two silent failure modes — what you did
not reproduce, and what you brought with you — are properties of *every* env we will write,
including the good one.

### Q22 — The seat stack is a meta-continuation (lazy instantiation)

From `PHILOSOPHY.md` §11. Smith's 3-LISP result: an infinite tower of interpreters is
finitely runnable because a meta-level is instantiated **only when a reflective procedure
actually fires**. Wand & Friedman (1988) give the non-reflective proof — one interpreter
plus a **meta-continuation**, a stack of pending levels.

**Recommendation.** Seats are not a standing hierarchy. A seat at level n+1 is instantiated
when, and only when, a residual crosses the seam that level n cannot settle — and the stack
is popped when it can. Cost is proportional to actual escalation, not to nominal depth.

**Which makes Figure 10's "no top rung" a data structure rather than an argument**, and it
means the oversight machinery costs nothing while nothing is escalating.

**And the transform sits at the seam, not between dormant levels.** Reflection reifies:
the level below's running process becomes the level above's data. Dormant levels are
identical and collapse for free; every actual crossing pays.

### Q23 — The ledger is a reification, and that is why the Gate can be domain-blind

**Reification** = making the interpreter's implicit state available as data. **Reflection**
= making that data the machine's state again (Friedman & Wand, LFP 1984).

The ledger is a reification mechanism. So Figure 10's soundness condition stops needing a
hand-argument: **the Gate receives a reification, not the running machine.** Reified state
is data, and a checker over data is domain-blind by construction.

**Recommendation.** This settles §7's layout on principle rather than taste — `gate.py`
imports nothing and reads the ledger, because that *is* the meta-level relationship, not a
tidiness convention.

### Q24 — Requisite variety gives the mint-vs-probe fork a number

Ashby 1956: `H(outcome) ≥ H(disturbance) − H(regulator)`. Γ sets the regulator's variety;
the environment sets the disturbance's.

> If `R` is not falling: either Γ's variety is below the environment's — **mint** — or the
> disturbance variety was never observed — **probe**.

**Recommendation.** Record both. It is the same fork as `density(R)` versus
`reachability(φ,Γ)` (Q11, Q20) reached from control theory, and it confirms the two are not
interchangeable remedies. It also reframes MINT as **variety acquisition**, which gives
`closure(Γ)` a lower bound the environment imposes rather than one the designer picks.

### Q25 — The branching test: a diagnostic that works from outside

An invertible transform, iterated, is a **permutation** — orbits, not a tree. Branching
requires one-to-many forward and non-invertible backward.

You cannot inspect a transform for non-invertibility from inside the system running it
(§8.4, dead reckoning). **But you can look for branches.** A tower of seats, agents, or
generations that has produced no divergence has no transform and is a copy loop however
deep it goes — and that is visible without access to the transform itself.

**Recommendation.** Ship it as a check on any multi-level structure the build grows. Cheap,
external, and it fails loudly.

### Q26 — Instantiating the framework in a domain: the eight-slot binding table

From `PHILOSOPHY.md` §14. `main` is domain-agnostic, so this is the contract an adapter
must satisfy — the generalisation of the `Marketplace` protocol's actor / currency / arena
bindings.

**substrate · environment · actors · currency · ground · slot · atom · transform**

> **If a domain cannot fill all eight, the framework has not been instantiated there. It
> has been mentioned there.**

**Recommendation.** Make it the literal `Env` protocol — eight members, and an adapter that
cannot supply one fails at construction rather than at run time. That turns the
philosophical claim into an import error, which is the only form of it that can be
enforced.

**With the shadow test applied to the port itself:** was there a residual in this domain
already unexplained that the framework predicts, or did we go looking for somewhere to put
it? Echo without shadow is apophenia, including when the thing being ported is this
framework.

### Q27 — Build order is set by the quality of the ground

Domains differ in how good an anchor they have, and the framework is only ever as sound as
the anchor available.

| domain | anchor | quality |
|---|---|---|
| an interpreter / a proof checker | does it evaluate correctly | **near-perfect** — mechanical, instant, unarguable |
| a rover, a game, a puzzle | did it reach the goal | **good** — sparse, slow, does not negotiate |
| "is this a good answer for a person" | human judgment | **poor** — it updates, which is Figure 2 collapse 1 |

**Recommendation, and it may change what the toy env should be.** A crisp-ground domain
tests the **machinery**; a poor-ground domain tests the **alignment claim**. Doing both at
once teaches nothing about either. Prove the loop where the anchor cannot be talked to,
then move outward.

Which is also what the alignment argument needs: the framework buys auditability and
correctability *given* a legitimate anchor. Demonstrate that where one exists before
arguing about the domains where one does not.

**Open for you:** the current toy env is a gridworld. A tiny expression evaluator would
have a strictly better ground — every prediction is checkable mechanically and instantly,
and `R` per slot is per subexpression. Worth considering before the adapter is written.

---

## 6. What the reference tree teaches

Shape only, per your instruction. Two lists.

### Carry the shape

| from                | what                                                                       |
| ------------------- | -------------------------------------------------------------------------- |
| `grammar.py`        | typed utterance; terminals produce RECORDs so precedence typechecks; compose raises with a reason; the typed hole as probe |
| `gate.py`           | three check currencies; builder/gate split; the import-time wall; fixed refusal tokens, never prose |
| `perception.py`     | no downsampling; components as objects; segmentation as revisable belief; permanence by overlap; death only on evidence |
| `narration.py`      | narration *is* the decision — the bet-side record is emitted before the action, and ACT refuses to emit without a BET this step |
| `narration.py`      | ROUTE records **why not the neighbour bin**; MINT records **which guard was the zero** |
| `planner.py`        | bidirectional search, backward steps verified by forward replay; exhaustion returns None — "a too-big search is a shadow, never a stall" |
| `scheduler.py`      | the abort router (WORLD-MOVED vs PLAN-WRONG); the starvation guard — deferral within a cycle may never become denial across cycles |
| `composer.py`       | citability — an unsettled composite cannot be cited as evidence                |
| `effects.py`        | one contact event teaches one atom; the key drops bbox position, so the same mechanism at two positions is one atom |
| `fabric.py`         | append-only JSONL, monotonic seq, corrupt line skipped never fatal; falsify down-ranks and never deletes |

From `new-horse` (`Ouroboros-Redux` @ `new-horse`):

| from             | what                                                                              |
| ---------------- | --------------------------------------------------------------------------------- |
| `residual.py`    | the brake invariant — monotone `pe_integral`, no `suppress()`; `outstanding` as a separate, reducible quantity (Q17) |
| `residual.py`    | the **tautology guard** — a φ that reads the after-state compresses perfectly and predicts nothing, so minting with `reads_after=True` **raises**. `v4-cold` guards the same thing with an import-time AST wall. Two branches, two mechanisms, one law: it is load-bearing |
| `marketplace.py` | MAP as a priced market; currency measured **externally** (a hypothesis cannot self-report its salience); the Goodhart guard built into the currency (Q5) |
| `grammar.py`     | MOLECULES — priors as named typed composites with holes (Q3)                        |
| `grammar.py`     | `count_typed_objectives` vs `count_flat_bag` — "typing beats size" as a *measured* claim rather than an asserted one |
| `agent_loop.py`  | coverage-first then re-probe: learn your own effects before pursuing goals; *inert is a verdict earned by trials* (Q18) |
| `relations.py`   | salience ranked by (static, rarity, size), with the reasoning for each recorded against the run that forced it |
| `falsified_ledger.py` | refuted hypotheses skipped rather than re-derived, and defeasibly (there is a clock) |
| `probe.py` (Nexus) | the SUPPORT-is-zero branch: perturb, uninformed, trigger on own prediction error, closed loop, outcome back through the same residual (Q20) |
| `molecule.py` (Nexus) | quantified objectives with a graded **degree**, priced by the same two-part MDL one level up; median split so there is no free parameter (Q21) |
| the fluent proposer (Nexus) | the enumerator run generatively as a corpus generator; proposes, never scores, never promotes (Q4b) |
| `nexus/kernel.py` | one Γ, one registry, plain imports — never a second loaded copy of the type system |
| `logical_grid.py` | the lens rule — a derived view for THINK only, never fed to perception; `R_T` computed and used to *gate* the abstraction; a fidelity measurement instead of a vote; `None` when no lattice exists (Q19) |

### Do not carry

| what                                | why                                                                 |
| ----------------------------------- | ------------------------------------------------------------------- |
| **shadow mode**                     | Q12. It is the failure, not a rollout stage.                        |
| **the 77-rung ladder**              | ~9,700 lines of heuristics that decided everything while the framework watched. Its competence is precisely what let the framework stay optional. |
| **two tracks**                      | one loop, one decision path.                                        |
| **`mint.py`'s guard set**           | Q11. REACHABILITY is missing and the bargain was promoted into its slot. |
| **the scope/kin machinery**         | population scale; defer with step 6.                                |
| **`fabric.py`'s reputation-by-echo** | reputation summed over echoes is agreement, and agreement among frames is Figure 2 collapse 1. If it comes back later, it must be ground-weighted. |
| **the caching layers**              | seq high-water marks, parsed-stream LRU, anchor bytes, memoisation. All real optimisations for a system under time pressure, all noise at this stage. |
| **`cognitive_loop.py` at 5,472 lines** | the shape is one cycle with four phases. It should be readable in one screen. |

### Do not carry, from `new-horse`

| what                                  | why                                                              |
| ------------------------------------- | ---------------------------------------------------------------- |
| **an unimported grammar**             | Q10. `grammar.py` is imported by its test and by nothing else.   |
| **string-tuple relations**            | `("BE_AT", (12, 7))` bypasses `compose()` entirely, so the type system never runs in play. |
| **prose logs as the record**          | Q16. Readable, and unverifiable.                                 |
| **hand-tuned salience constants**     | `max_objs=5`, `min_members=2`, `demote_factor=0.4`, `stall_steps=50`. Same treatment as Q14 — mode and provenance or out. |

### The one-line diagnosis, now from two branches

`v4-cold`: the framework **speaks but does not decide.** The gate is in shadow mode,
`refuse` is zero by construction, and a 77-rung ladder picked 266,570 actions.

`new-horse`: the framework is **typed but does not run.** `grammar.py` is not imported
by anything in `src/`; the live agent reasons through parallel string keys.

`Nexus`: the framework is **imported twice.** `nexus/kernel.py` records it — two
`spec_from_file_location` loads of the same source produced two module objects, so
`dsl.Predicate is kernel.Predicate` was **False**, `isinstance` failed across the seam,
and the two halves could not hand each other a predicate at all. The docstring's claim
that the population never gets its own private notion of a predicate *"was true of the
SOURCE and false of the RUNTIME."*

> **"A double-loaded module is a reinvention that no grep can see."**

Three independent attempts, three different mechanisms, **the same failure**: the
framework ends up *beside* the agent rather than *inside* it.

That is not bad luck twice. In both cases something else was already competent enough
to pick actions — the rung ladder in one, the priced relation market in the other — and
once something else can decide, the framework is never forced to be sufficient. It gets
to be a description, and a description is not load-bearing.

**Which makes Q12 the whole rebuild.** Not "add a gate to a working agent" but "the
derivation is the only way an action gets proposed." Everything else in this document
is detail by comparison. If the new build ends up with any path from perception to
action that does not pass through a composed, type-checked, ground-settled utterance,
it will become v8 for the same reason v4-cold and new-horse became v5 and v6.

---

## 7. Proposed shape

Flat, per your constraint, and the Gate gives an independent reason to want it.

```
grammar.py   types, primes, heads, terminals, compose          ·  Q4, Q10
gamma.py     atoms, molecules (= priors), closure, the λ report ·  Q3, Q26
tether.py    the loop: belief, residual, route, mint, ledger    ·  the eight steps
probe.py     the SUPPORT-at-zero branch. Uninformed by construction · Q20
speak.py     decision state -> utterance. THE BUILDER: reads agent state only · Q16
gate.py      the checker. IMPORTS NOTHING. Reads the ledger.    ·  Q2, Q23
world.py     perception + the eight-slot Env protocol            ·  Q6, Q26
demo.py      one runnable problem, start to finish
```

Eight files, one direction of dependency, no package tree.

**Three of those lines are load-bearing rather than tidy:**

- **`gate.py` imports nothing.** Not a convention — Q23's finding is that the ledger is a
  **reification**, so a checker over it is domain-blind *by construction*. The file
  boundary is Figure 10 enforced by the file system: a Gate that cannot import the solver
  cannot reconstruct the claim. The reference tree went further and had an import-time AST
  wall that failed the build if a builder so much as *named* an after-state variable —
  worth copying once the split exists.
- **`probe.py` is separate and blind.** It sees the advertised action set and the board's
  shape, and nothing else. Keeping it in its own file with no imports from the composer is
  how "uninformed by construction" stays true under later edits.
- **`speak.py` is the builder and reads only agent state.** The builder/gate split is the
  one thing `v4-cold` got most right, and it only holds if neither can reach the other's
  sources.

**Not in the layout, deliberately:** the tiny proposer (Q4b) is a training artefact plus a
loader, not a module of the loop, and it must be possible to run the whole thing with the
proposer absent. If removing it breaks the loop, it stopped being a proposer.

**Tooling.** ruff kept. vulture and pydeps removed — vulture flags every public
function in a small library as dead, and pydeps exists to untangle an import graph
this layout is designed not to have.

---

## 8. To gather

- [ ] What the rover's actual input is (Q6)
- [ ] The prior set — what does it start knowing? (Q3)
- [ ] The atom set for the domain
- [ ] Whether a reference problem exists that we agree counts as solved
- [ ] Any further files worth the same shape-read

---

## 9. Deliberately deferred

- **Step 6 and PROMOTE.** Population scale. §4 makes this the *correct* omission, not
  merely a convenience: the adult on Mars is complete without it.
- **`R_T` is NOT deferred.** Q19 shows the round trip has an agent-scale job —
  full-resolution ↔ derived view, inside one agent — separate from its population-scale
  job. `logical_grid.fidelity` is the working example. The round trip comes in now; only
  the agent↔population transform waits.
- **Step 7 OUTWARD, IMPORT.** Needs a second frame. Until then the loop records the
  debt, which is the honest state.
- **Competition specifics.** Own branch, per your call.

---

## 10. The disposable spike

~700 lines under `tether/`, written before I had the formula. A spike, not a
foundation.

Survived: the four-bin router; *pays* and *closes* as different predicates; per-slot
residual with no aggregation; the closure enumerator treating a yielded term as a
witness and an exhausted budget as UNREACHED rather than unreachable; the ledger.

Wrong: it labels things ACCEPTED that no ground settled; there is no belief `b`;
its NOVEL bin is an evidence counter rather than a diagnosis; no speech, no Gate,
no priors, no goal residual.

Say the word and I delete it.

**And one open item on it that Q27 may settle first:** its toy env is a gridworld. A tiny
expression evaluator would have a strictly better ground — every prediction checkable
mechanically and instantly, `R` indexed per subexpression, and no perception layer in the
way of testing the loop. The gridworld tests perception *and* the loop at once, which is
two experiments in a trench coat. Worth deciding before any adapter is written.

---

## 11. Audit: this document against the figures

Every question and recommendation in §5, checked against the eleven SVGs rather than
against `THE_FORMULA` or the reference branches. **The figures win** — they are the
specification, the branches are attempts at it, and where I leaned on a branch instead of
the spec that is a defect in this document.

Four corrections, five confirmations, ten omissions.

---

### A · Corrections — where this document is wrong or leans on the wrong source

#### A1 · Q1 is not open. **Figure 1 answers it, and Figure 5 corroborates.**

Figure 1, immediately under *"residual R indexed by object slot"*:

> **`transition · reward · bracket`**

Figure 5's three inputs to the sort:

> **the prediction gap** — fires on every action
> **the score** — only when something scores
> **the round trip** — the loss across scales

**Those are the same three, named twice.** Not one residual, and not two — **three
channels into one router:**

| channel | Figure 1 | Figure 5 | fires |
|---|---|---|---|
| prediction error | `transition` | the prediction gap | every action |
| **goal / reward** | **`reward`** | **the score** | only when something scores |
| round trip | `bracket` | the round trip | across scales |

**So Q1's framing was wrong in both directions.** My "two residuals, one router" undercounts
— and the second one is not something I proposed, it is on the figure. `R_goal` is
`reward`, and `R_T` is `bracket`, which the formula already has but never lists as a
*residual channel* alongside the other two.

**Q1 → SETTLED, by Figure 1.** What Q21 added is the *measurement* for the reward channel
(`1 − degree(molecule)`), not the channel itself.

**And it exposes a gap in `THE_FORMULA`:** step 1 defines `R` on the transition channel
only. The reward channel is in two figures and in neither the symbol table nor step 1.

#### A2 · Q5 answers a question the figures do not ask. **Figure 1's four phases are different.**

Figure 1: *"per-step loop (POMDP) — **perceive · plan · act · predict**"*.

There is no **think** and no **map**. Q5 took "perceive → think → map → act" from
`cognitive_loop.py` and from your message, then answered *"MAP is the market"* from
`new-horse`'s docstring. **Both sources are branches, not the spec**, and the spec uses a
different decomposition entirely.

Three namings are now in play and they should be reconciled once:

| source | phases |
|---|---|
| **Figure 1 (the spec)** | perceive · plan · act · predict |
| `cognitive_loop.py`, and your framing | perceive · think · map · act |
| `THE_FORMULA` | eight steps |

**Q5 → reopened, as a naming question rather than a mechanism question.** The market is
real and does real work; whether it is called MAP, and whether the loop has four phases or
eight steps, is unresolved and only the figures can settle it.

#### A3 · Q27's axis is wrong. **Figure 2 gives the right one.**

Q27 ranks domains by "quality of the ground" and calls human judgment **poor**. Figure 2
says something different and sharper:

> *An anchor is legitimate when the question is **constitutively about it**. Human judgment
> is the right anchor for* is this a good answer for a person, *because the question is
> about people. It is only an **instrument** for* is this code correct, *and instruments can
> be wrong on axes they do not measure.*

**Human judgment is not a poor anchor. It is a legitimate anchor for one class of question
and a fallible instrument for another.** The axis is **constitutive versus instrumental**,
not good versus poor.

**Q27 corrected:**

| domain | the anchor | why |
|---|---|---|
| an interpreter | does it evaluate correctly | **constitutive** — the question *is* about evaluation |
| a rover, a puzzle | did it reach the goal | **constitutive** — the question *is* about arrival |
| "is this a good answer for a person" | human judgment | **constitutive**, and legitimately so |
| "is this code correct" | human judgment | **instrumental** — and wrong on axes it does not measure |

The build-order recommendation survives, for a different reason: a **mechanical**
constitutive anchor is instant and unarguable, so it tests the machinery fastest. That is
about latency and cost, not legitimacy.

#### A4 · Q20 adopts a trigger the figures put on a different channel.

Figure 5: *"the curiosity drive — **fires when nothing is scoring**, aimed at the new bin,
seeks the gap that is large and compressible."*

`probe.py`'s trigger is the agent's own **prediction-error** EMA falling to zero. Q20 took
that one. **They are different channels** — score versus transition — and under A1 that is
now a coherent distinction rather than a conflict:

- **nothing is scoring** → the curiosity drive (Figure 5), aimed at the NOVEL bin
- **nothing is surprising** → the probe (`probe.py`), perturb and read the outcome

Both are `density(R) = 0`, on different channels. **Q20 should carry both, not one.**

---

### B · Confirmations — where a figure backs this document explicitly

| | claim | the figure's own words |
|---|---|---|
| **Q8** | accumulated, not per-step | Figure 5: *"a term that explains one occasion perfectly"* **fails the bargain** — the figure rules out the single-occasion term directly |
| **Q11** | SUPPORT × REACHABILITY × NOVELTY | Figure 1: *"guards: support · reach · novel"* |
| **R is a slice** | never complete | Figure 7: *"every room closes some of the gap; **no finite number of them ever arrives**"* |
| **Q19** | the round trip gates the abstraction | Figure 4: *"take the round trip and measure the gap… the only honest report of how much was given up"* |
| **Q2** | the verifier cannot reconstruct | Figure 10: *"a verifier that can reconstruct the claim cannot verify it"* |

---

### C · Omissions — figure content this document does not carry

Each of these is on a figure and absent from §5. Several are build rules.

**C1 · Filters do not issue verdicts.** Figure 9: *"Use filters for the budget and witnesses
for the verdict. **Never let a filter hand you a verdict.**"* This is a direct constraint on
the Gate and on every search cutoff in the build, and it is nowhere in Q2.

**C2 · Every cut stays ranked and reversible.** Figure 9: *"a wrong cut removes the answer
and speeds up, so keep every cut ranked and reversible."* The failure mode is that pruning
looks like progress. A build requirement, unrecorded.

**C3 · The seat *may* author conventions — it is the one thing it can author.** Figure 10:
*"It does author conventions, because nothing else can see across a seam. A convention makes
no claim about the world; a verdict and an atom both do. The seat may author what has no
truth value and nothing that does."* Q2 describes the Gate as purely a checker. That
understates it, and the two guards that come with the power are also missing: *a convention
that decides an outcome has stopped being one*, and *a convention nothing can check is a
constant the seat authored*.

**C4 · Stakes are structural and must be declared.** Figure 10: *"A seat with no stake at all
does not exist… an interest in the outcome is unavoidable, an interest in the reading is
disqualifying. Where a stake cannot be removed, declare it. An undeclared interest is
modelled anyway and an unnamed model runs unchallenged."* Nothing in §5 has the Gate
declaring anything about itself.

**C5 · Standing.** Figure 10: *"standing is a stake that survives the outcome it was earned
on."* Absent.

**C6 · Divergence regenerates unevenly.** Figure 10: *"Frames whose independence is renewed
by separate experience can be maintained; frames whose correlation is fixed at origin can
only be **rotated**, because no amount of use makes them less alike and replacement is the
only refresh."* This is a hard constraint on any ensemble or multi-agent design and it is
not in the document.

**C7 · Capability is a property of agent-and-habitat.** Figure 11: *"An improvement that does
not change contact changes nothing, however much it improves."* **That is an acceptance
criterion for every change the build proposes**, and it is not being applied.

**C8 · A wrong atom is worse than no atom.** Figure 6: *"Import from a live peer is debited
against that frame's independence. **A wrong atom costs more than starting from
primitives.**"* The import path's risk is unstated in Q10 and Q26.

**C9 · Progress per handoff has two factors.** Figure 7: `R = h² × S` — bracket fidelity and
ground pressure, *"zero either and the chain runs in place."* Population-scale, so deferred
— but the deferral should be recorded rather than silent, and the change spec already says
to label it illustrative unless computed.

**C10 · Figure 3's diagnostic is not operationalised.** *"Before asking whether a system is
good, ask which link it currently stops at, and whether the answer was measured or
assumed."* Five links: perception, vocabulary, objective, planning, learn-and-carry. **This
is the single cheapest instrument in the whole set** and the build has no place to report
it. Every run should say which link it stopped at and whether that was measured.

---

### D · What this audit changes

| item | was | now |
|---|---|---|
| **Q1** | DECIDE — one residual or two | **SETTLED** — three channels, from Figure 1 |
| **Q5** | SETTLED — MAP is the market | **OPEN** — the figures use different phase names; a naming question |
| **Q20** | SETTLED — probe on prediction error | **SETTLED, widened** — two triggers on two channels |
| **Q27** | DECIDE — ground quality | **DECIDE, reframed** — constitutive vs instrumental |
| **C1–C10** | absent | **ten new items**, mostly build rules, several with teeth |

**And one for `THE_FORMULA`:** the reward channel is on two figures and in neither the
symbol table nor step 1. That is the largest single omission this audit found, and it is in
the normative document rather than in this one.
