# tether

Agent-level implementation of the Tether decision architecture. Version 7.
Domain-agnostic. `core` is the general proof of concept; competition work goes on
its own branch.

---

## THE PROCTOR RULES

Carried from `Ouroboros-Redux`: `THE_MISSION_north_star.md`, `THE_ALIGNMENT.md`,
`THE_TERMINAL_CONDITION.md`. These are Isaiah's values externalised and durable — they
outrank momentary preference, mine and his. When a design fork appears, **derive the
answer from the doctrine**; ask only where the doctrine is genuinely silent or in real
conflict.

### The job

**The agent is the prize. Winning is not.** A black box that wins teaches nothing.
The deliverable is an agent that reasons its way through problems it was never told
about, and can say how and why.

**I am the proctor, not the player.** Remove impediments; make the challenge clear; do
not do the work. When the agent cannot do something:

> debug the detectors · debug the reasoning · debug the logic · debug the perception

If it still cannot, it is a bug or a blockage. Finding that is the whole job.

**Never encode the answer.** The one unforgivable failure. An encoded answer is the one
thing guaranteed not to transfer. Knowing the mechanics is fine; spending that knowledge
on anything but *judging* is not.

**Agency is the goal, not a means.** If I find myself picking A vs B on a question the
agent could reason, I am taking the test. Stop. The fix is never "encode the answer" —
it is "repair the pipeline so the agent can form the hypothesis, test it, and read the
result itself."

**A hardcoded procedure that pre-answers a question the agent should ask is a FAULT,
even when it is correct.** Scaffolding that removes a choice removes agency.

**Residue is the agent's to close.** When something is unexplained by any existing
primitive, the agent builds the primitive. Making the library more complete steals a
discovery. Prefer the agent deriving it crudely to me installing it cleanly — the
refined version can be installed next turn, *because it earned it*.

### Legibility is the instrument

The architecture is whitebox **so that triangulation is possible at all.** Because Γ
predicts explicitly, its model is readable. Because R is an explicit object, the
cause-and-effect it perceived is readable. Because minting is an inspectable event, the
moment of discovery — or its absence — is a diagnosis rather than a mystery.

**A change that makes the agent better but makes its reasoning unreadable has destroyed
the instrument. It is a loss, not a win.** Every change preserves the legibility of
predict → residual → mint → Γ.

No scar tissue that routes around the loop. No machinery I cannot read. No opaque
shortcut replacing an explicit φ / residual / Γ object.

### One loop

One uniform per-step loop for every problem. **No type branching.** Grouping by problem
type is the opposite of generalising — anything branched on type is dead weight that
cannot transfer. The only legitimate distinction is thin I/O, detected contingently per
step, never used as a label.

### Why the constraints are the constraints

**Each is the answer to *what would make this claim falsifiable*, and not one of them is a design
preference.**

| the constraint | the claim it makes falsifiable |
|---|---|
| **the ground is the only metric** | a frame cannot score itself with a quantity it produces |
| **the bargain prices terms** | a term that explains everything by saying nothing must fail |
| **reach must be total** | a partial closure makes every null unreadable — *only a sealed room can be searched to the end*, so an abstention counts only when it names the closure it searched |
| **import must be provenanced** | convergent derivation and adopted import are **indistinguishable in the contents**; only the record of where each came from separates them |
| **the knowledge must be domain-agnostic** | the membrane lets only METHODS cross — a binding is a recording, a composition is a method |

**REMOVING ANY ONE LEAVES A SYSTEM THAT CAN LOOK LIKE IT WORKS AND CANNOT BE SHOWN TO.** That is
the test to apply when a constraint feels expensive: not *is this slowing us down* but **which
claim stops being checkable without it.**

### Metrics

**Only the ground counts.** A proxy metric is an anchor that updates, and an updating
anchor collapses triangulation into a mirror.

I have a documented weakness for **invented metrics and magic numbers**. Coverage, terms
minted, compression achieved, and anything else the frame produces are frame-internal
and are not evidence.

**CONTACT IS WHAT SEPARATES CAPABILITY FROM INSTRUMENTATION, AND IT IS FIGURE 11's.**
*Capability is a property of agent-and-habitat, never of the agent alone. An improvement that
does not change contact changes nothing, however much it improves.* Asked of one day's work:
`outstanding`, the branching test, both audit passes, the `idn` cut — **instruments, no contact
change**. `delta` published and the import made pullable — **contact**. That is the whole of *a
third of it moved the goal*, and it is **not a discipline failure**: most work does not touch
contact, and only contact moves capability. **The question to ask of a change is whether the
agent can now reach something it could not**, not whether a number improved.

**And it is why widening PERCEPTION is legitimate where installing TIER 2 is not.** *Introduce,
never subtract*: one changes contact, the other **substitutes the habitat** — and *a synthetic
solve proves wiring and never capability.*

**A flat metric is not a dead direction.** A level bump is 30–40 things going right at
once; solving 20 of 30 shows nothing. Judge by whether the reasoning is sound and the
code is actually running, not by the number.

### Nothing silent

No isolated code. No silent code. No code without reason. Legible beats silent,
demonstrated.

**A checker goes silent in seven places, and they are named in `conform/lint.py`'s
docstring.** Read them before widening an exemption, changing a denominator, or writing a
witness — each was found by a checker going quiet once, and none by reasoning about what a
good checker should do:

- **fixtures before changes** — the only order with an observable half-state
- **witness the boundary, not the decision** — exemptions and denominators, never the rule
- **exemptions as data, not logic** — a table can be pinned; logic widens quietly. **And it
  reaches a MEASUREMENT'S POPULATION, not only a rule's scope**: the detector-family
  independence test must exclude the six games where **the adapter surfaces no action** —
  they advertise a positioned click and the adapter drops it, because the loop cannot supply
  a position. **Every detector fails there because nothing acts, not because the detectors
  are correlated: a shared failure mode from the HARNESS rather than from the family**, and
  four independent ones would read as correlated. **Excluded on a checkable fact — no
  SURFACED action — never on judgement, and never on *no action*: what those games contain
  is unestablished, and the exclusion expires the moment positioned actions are supplied.**
  First instance outside a rule's scope
- **reintroduce the defect, never disable the check** — tests reach, not existence
- **a repair can break the layer above** — and that is where causes get asserted
- **a metric whose denominator the mechanism changes cannot falsify that mechanism** —
  before pinning a falsifier, ask whether the mechanism moves the quantity the metric is
  computed over. If it does, the metric is measuring itself. `false_mint_rate` is over
  CLAIMS, and STAGE 1's whole effect was on what counts as a claim; it moved numerator and
  denominator together, read null, and a correct mechanism was withdrawn on it
- **assume it is already specified, and go look** — not *check afterwards*. An improvised
  metric is fitted to the case that prompted it, which is a repair validated on its own
  case, one level up. **Nine times the corpus had already named the instrument, and nine
  times the specified one was the better one**: `λ` as the spectral radius · `UNREACHED`
  as the post-escalation claim · the escalation ladder · chunk reuse count · retrieval
  keyed by residual shape · `R_T` as a gate rather than a reading · binding by contact
  rather than by enumeration · `λ^d` as the coverage denominator · reset-vs-advance before
  demoting at a boundary. **The design step is a search of the corpus, not a design.**

Five corollaries with the same standing: *a control that examines nothing cannot
demonstrate a clean state*; *an exit code is a declaration where a pattern match over
stdout is a guess*; *a panel property must be measured before it is used as a premise,
never asserted from the shape of the generator* — the DS ladder was called easing on ten
seeds, is flat on forty, and a panel repair was designed on top of it; and *before a null
is read as a finding about a mechanism, state what property of the panel the mechanism
would need in order to show, and confirm the panel has it* — `M = 7` is prime so no
coarsening can preserve arithmetic, the ladder is flat so the carried-cold gap has nowhere
to open, and four independent slots make echo nearly accidental. **Three nulls, three
worlds structurally unable to reward the thing tested, and none of it visible in the
result.** **AND THE SAMPLE-SIZE HALF RUNS IN BOTH DIRECTIONS, WHICH IT WAS NOT WRITTEN TO
SAY.** *Ten seeds versus forty* is filed against over-claiming a POSITIVE. §12.4's trigger
fired **0 of 25 steps on `ls20`, 25 of 25 on `sk48`, 7 of 25 on `g50t`** — one panel, and
*the trigger cannot fire* was drafted as a fact about the mechanism. **Over-claiming a null
is the worse case, because a null presents as caution and needs no defence.** And the tell
is the explanation: *objects that look alike behave alike* was true of `ls20` and general in
its wording. **A null carrying a satisfying causal story is harder to doubt than a bare
one**, so the story is the thing to distrust, not the number. And *read the things that produce conditions before the things that produce
results* — a generator, a config, a plan, a fixture. **They do not announce themselves,
and a condition is invisible in the results it conditions.** `SNAPS_PLAN` was the shortest
document in the set, was never opened, and four of its ten sections overturned a published
conclusion. The laws apply to the panel, not only to the code.

**AND THE DILUTION RULE, WHICH STATES CONTAINMENT BETTER THAN THE ABOVE DO.** *You can dilute a
residual of apple juice in a cup with water, but unless it leaves the confines it cannot be
removed.* **Dilution is not removal**: the concentration changed and the quantity did not, and
nothing inside the cup can reduce it. Figure 11's *introduce, never subtract* is the same law —
adding water is the only move available from inside.

**THE TEST, AND IT IS ONE QUESTION:** *does anything leave the confines?* **If not, it is a
dilution and the quantity is unchanged.** It would have retired the segment-scoping proposal
before it was measured — the regime change is INSIDE the cup, `Segment`'s boundaries are level
changes, and a slot going from oscillating to running is not one. **That is a better account than
*there was no break event near step 8*: the break was real and internal, and internal changes
dilute.**

**AND `outstanding` IS THIS RULE AS A DATA STRUCTURE.** `pe_integral` is monotone against the
actual and never reduced; `explain` moves surprise out of `outstanding` and cannot unspend it.
**A system that could zero its own surprise record would look calm by having forgotten it was ever
wrong.**

**THE ONE PLACE SOMETHING DOES LEAVE IS `retarget`** — and that is not dilution, it is **the cup
being emptied because the room changed.** Figure 11's isolation law: *isolation is not removal of
the habitat, it is substitution of one habitat for another.* **You do not get an empty cup. You
get a different one** — with whatever it already had, and whatever you failed to bring across.
**Two failure modes, and the second is the one that keeps arriving: what you failed to reproduce
is invisible until the goal fails; what you unintentionally introduced is invisible until it
acts.**

**And FOUR STEPS, which are a different kind of thing and are filed apart on purpose.**
Every law above installs something that fires — a rule, a fixture, a witness, a denominator
that can be checked. **These cannot. They happen before the work or they do not happen, and
after the fact there is nothing to catch, because after the fact the reading is clean.**

- **Check what a name means in both places you are using it, before pinning a shape to it.**
  Two legitimate quantities under one word is well-formed code, well-formed docs and a
  well-formed measurement. `conform/lint.py` declares this unlintable as `A6i`, and it has
  **three instances, of two kinds.** **RETROSPECTIVE, caught at the point of damage:**
  **`molecule`** is a prior term in `gamma` and a quantified objective in `DISCOVERY` Q21;
  **`DIRECTED`** is `by == "discriminate"` in the loop and *bets with bound terms* in
  `ARC_AGENT` §22.2 — **9% and 37% on the same runs.** **PROSPECTIVE, and the only one whose
  value came from being recorded while nothing was wrong:** **`BUDGET`** is a loadable prior
  shape of cognitive bounds in `ARC_AGENT` §12.1 and the harness cap in §22.1 — filed as
  *checked and clear*, and it made the Phase 3a ablation split takeable instead of a guess
  one ruling later.

  **A FOURTH, and it is the one that made a ruling unimplementable:** **`PRIOR`** is an
  **origin stamp** in `gamma` — every atom gets it at construction, so it means *no mint
  record* — and in `ARC_AGENT` §11 it is **a category admitted under an entry rule**. §12.1's
  own title says *a prior is not one kind of thing, so it cannot have one code shape.* **The
  stamp is therefore not evidence the rule was applied**, which is exactly what `3a`'s *all
  stamped `prior`* invites a reader to believe.

  **So the trigger is *where a headline OR A RULING is about to be made*.** And the
  prospective half needs its own condition, because it is the harder case to justify at the
  time: **a cleared hazard is worth recording when the ITEM THAT WOULD COLLIDE WITH IT IS
  NAMEABLE.** `3a` was identifiable in advance as the only item loading one of `BUDGET`'s two
  senses, which is why it was written down. **That condition is checkable, and it is what
  stops this becoming *record every near-miss* — which is how a register fills with noise
  until nobody reads it.**
- **Read the things that produce conditions before the things that produce results** — a
  generator, a config, a plan, a fixture.
- **Read the SPEC of each item before ordering a phase, not the row that summarises it.**
  Build tables group by cost; the dependency order falls out of neither the table nor the
  cost. **Four for four**: `2c` grouped a lens with sensors that needed `2b`; sensor 4 needed
  sensor 8 from a different list and sensor 3's read; `2d`'s `bounded` is *defined* by a cap
  nobody had set; `2e` turned out to be the consumer for two mechanisms built without
  triggers. **None of them would have FAILED** — the work would have been done against
  something that was not there yet. **And the reason it keeps paying is that the tables list
  CAPABILITIES while the code files MECHANISMS**: three of five times the mechanism was
  present and the capability was not — a type-directed closure with no varied types, seven
  sensors under the items that needed them, a sweep with no trigger. **So *is it built* is the
  wrong question to ask a row; *what does it still owe* is the right one, and the two differ
  most where the mechanism is finished.**
- **Assume it is already specified, and go look.** This is the sixth law and it is ALSO a
  step, which is why it appears twice — the other six install something that fires, and
  this one cannot. **And familiarity actively suppresses it**: citing a file feels like
  evidence of having read it, so each successful lookup accumulates evidence in the wrong
  direction, and the entry you never needed stays unread precisely because you kept finding
  what you did. `A6i` was declared in a table quoted from for six batches and read on the
  last edit of the session. **There is no state recording how completely a file was read,
  so *I have read this* is a memory of an act rather than a claim that can be checked.**

**And the reason they are steps and not laws eight and nine: `B17`.** *Pre-registration does
not protect a reading if the instrument measures something else.* The phase sweep pinned its
expected shape in advance, correctly, derived from an independent measurement — **and pinned
it to a label whose meaning had never been checked.** Discipline correctly applied, producing
a false finding with a clean provenance trail. **It cost nothing only because 9-versus-37 is
impossible to miss; 15-versus-18 passes straight through.** A step filed among mechanisms
reads as something that will be enforced, and it will not be.

### How I work here

- **Do not over-test, do not over-probe.** Self-generated tests are mostly not helpful.
- **Long comments are waste.** Isaiah does not read the code. Comment only to remind a
  future refactor of something. Everything else is me performing rigour. *(My v7 spike
  violated this heavily. Do not repeat it.)*
- **Never ship half a mechanism.** Half-cooked data is worth nothing.
- **Fix forward.** Progressive means "part of the goal", not "the number went up".
- **When stuck, abstract, then niche back down.** Lift the problem until its structure
  is visible — name the two or three things in contention and the two or three signals
  that could decide between them — let the answer shake out at that altitude, then drop
  back to specifics. A first-class move, not a fallback. Both I and the agent run it.
- **Falsify a signal before trusting it.** Prefer positive causal evidence ("I tried and
  a bound stopped me") over absential ("I have never been there"). Absence of evidence
  resting on completeness never holds mid-episode.
- **Wait for permission before building.** Isaiah says when.

### My known failure modes

1. Tries to solve the problem instead of the pipeline. Gets in the weeds.
2. Jumps to conclusions.
3. Compacts and forgets the rules.
4. Invents metrics and magic numbers.
5. Over-tests and over-probes.
6. Writes long comments performing rigour into a codebase nobody reads.
7. Encodes the answer. The unforgivable one.

### The instantiation check — which comes first, and is not a score

**The only goal right now is a WORKING INSTANTIATION OF THE FRAMEWORK.** Not winning, not a
count, not a rate. **The test is not of the agent — it is of the framework running as an
instance in the agent.**

**And it is checkable without any score:** does the loop run end to end — perceive · bet · be
wrong · mint · settle · promote · import — **with every step producing a receipt that could have
been refuted and was not.** ARC is a proving surface with the right properties, and
`levels_completed` is what the surface reports, never what the framework claims.

> **A RUN IS NOT AN INSTANTIATION AND NOT A CONTACT CHANGE.** Figure 11: *an improvement that does
> not change contact changes nothing.* A measurement introduces nothing. **The answer to too many
> instruments is never one more instrument** — it is the next mechanism the framework names and
> the code does not have.

**AND A GROUND READING TAKEN BELOW THE BREAK IS A READING OF NOTHING.** `levels_completed` is
link 4. With link 2 measured-and-failing and link 3 never reached, zero levels cannot separate
*the machinery is broken* from *the agent cannot express the objective*. **Run for it when link 3
exists** — when there is something to diagnose rather than a number with no subject.

**The map, and every entry is a mechanism the framework names rather than a proxy:**

    INSTANTIATED       perceive · the bet · the bargain · minting · promotion · transfer
    NOT INSTANTIATED   the objective layer · the second consumer for EXTRACT/RELATE/QUANTIFY
                       · the description vocabulary · everything gated behind those

### The terminal condition

Not "it improved". Five clauses, each checkable:

1. **It wins** — the whole task, not the first step.
2. **Whitebox** — its own record names the reason, and the stated reason matches the
   ground's reason.
3. **Ablation — A POST-MASTERY TEST, and the corpus says so in the clause's own grammar.**
   *If **the win** survives* takes THE WIN as its subject, so below mastery it has no
   referent: wipe the library of an agent at 3/25 and it goes to 3/25 or lower, and **neither
   number is interpretable, because there was nothing worth wiping.** "It wins" is clause 1
   and this is clause 3. §11 agrees from the other side — *an agent handed every prior never
   mints, and you cannot tell a composer from a lookup table* — and a composer/lookup
   distinction needs something composed. **Run it at 25/25, not before.**

   Back up Γ, verify the backup, wipe Γ, re-run. *If the win survives,
   the agent composed it. If the win disappears, the library was carrying the answer and
   the agent was retrieving, not reasoning.* The sharpest clause and a runnable
   falsifier. **Back up first; refuse to wipe if verification failed.**

   **AND THE ENTRY RULE THAT PROTECTS IT, WHICH `ARC_AGENT` §11 SAID TO WRITE HERE AND WHICH
   WAS NEVER WRITTEN:** *a prior enters **only** if the loop cannot run without it, or the
   agent minted a crude version first and we are promoting it. **Never because it would help
   on a game** — the moment one enters for that reason we have encoded an answer, and the
   ablation clause cannot tell us we did.*

   **THE RULE SPLITS IN TWO, AND ONLY ONE HALF IS LIVE.** The **LOAD side binds today**:
   *SENSORs beyond the nine are forbidden, because §12.3 says the agent must reach for them
   and reaching is the only evidence the composition system works* — a constraint on `3a`
   regardless of when any wipe happens.

   **AND THE CIRCLE THIS CREATES IS THE DESIGN, RULED 2026-08-31 AND NOT TO BE RELAXED.**
   §12.4's remedy is built and its verdict is a permanent `UNREACHED`: the nine all terminate
   at an attribute type — `accepting(COLOUR|POSITION|EXTENT|SHAPE|RATIO|DELTA|BOOL|REGION)` is
   empty on every one — so a chain from an OBJECT is one step and novelty refuses a bare
   sensor. **What would extend it is `parity(POSITION)` or `holes(SHAPE)`, which are §12.4's
   own examples of what the agent must compose, and this rule forbids installing them.** So
   the reach mechanism cannot reach.

   > **THAT IS NOT A BUG TO EXEMPT.** *Reaching is the only evidence the composition system
   > works* is precisely the sentence that makes the circle correct: **admit Tier 2 to make
   > reaching possible and the thing it enables IS the evidence, so there is nothing left to
   > measure.** **What breaks the circle legitimately is a RICHER TIER 1** — a perception
   > question with its own entry rule — **never a Tier 2 exemption.**

   **AND THE ABSTENTION IS THE DELIVERABLE, NOT THE BLOCKAGE.** *I cannot tell these apart, I
   cannot build an instrument that would from what I hold, and here is the closure I searched*
   — **the alignment claim at the perception level, carrying a denominator rather than
   asserting a property.** The **WIPE side — which shapes survive — is owed at
   25/25**, not now. **But its PRECONDITION does not defer**: the partition is by *which
   clause admitted a thing*, and that cannot be reconstructed later from a `prior` stamp, so
   **the admitting clause must be recorded AS ENTRIES HAPPEN or the deferred half becomes
   unrunnable.** Same shape as the watermark: the decision defers, the recording cannot.

   **§11'S LIBRARY SCOPE IS CORRECT — the 2026-08-27 re-scoping was the error, and this is
   the corrected text.** I read *four of five shapes escape a rule whose purpose is the thing
   they escape* and widened §11 to all six homes. **The conflict came from the word, not the
   rule.** Entering means **entering Γ**; the five non-Γ homes are **POPULATED, not entered**.
   So the two tests divide without overlapping and neither needs widening: **§23.2's *what to
   look at vs what to do* governs loading the five; §11's two clauses govern entry into Γ.**
   And *TERM wiped* is now **vacuous** — a TERM is VISIBLE, never held unearned, so nothing
   unearned is in Γ to wipe. **What
   entered under *cannot run without it* is what the ablation stays blind to; what entered
   under *promoted from crude* is what it wipes.** Ruled 2026-08-27: TRACKER blind (identity
   across frames is perception, not knowledge — wiping it makes the agent blind rather than
   untaught); BUDGET's cognitive bounds wiped, its termination caps never being priors at all;
   and **SENSORs beyond the nine are not wiped but FORBIDDEN**, because §12.3 says they must be
   reached and *reaching is the only evidence the composition system works.*
4. **Not fed** — no answer encoded anywhere. Every correction must generalise; a fix
   that helps one case is an answer wearing a fix's clothes.
5. **Time to learn** — and the budget is not the excuse.

---

## Which documents I may repair, and which I may only annotate

**The corpus is the one derivationally independent frame available, and editing it spends the
property the whole check runs on.** §8.4: *death → explanation requires an interpreter
**derivationally independent of the thing being explained**. Otherwise it is two mirrors.* The
corpus qualifies because it was written **earlier, by Isaiah, in a different context** — which
is why the section check has paid on every item it touched. **Repair a defect in it and the
next check against it is that much closer to dead reckoning.**

| | files | treatment |
|---|---|---|
| **WORKING — inside the seat** | `CLAUDE.md` · `ARC_BUILD_PLAN.md` · `docs/INDEX.md` · all code | **repair at source.** A finding left as a note makes the next reader re-derive it |
| **CORPUS — annotated from outside** | `ARC_AGENT.md` · `PHILOSOPHY.md` · `DISCOVERY.md` · `SNAPS_PLAN.md` · `FALSE_MINT.md` · `BUILD_PLAN.md` · `DOCTRINE_AUDIT.md` | **record the defect in `INDEX.md`; do not fix it.** Isaiah's to repair or leave — **if he repairs it the provenance stays clean, because he wrote both halves** |

**A DEFECT ANNOTATED EXTERNALLY IS STILL CHECKABLE. A CORPUS I HAVE EDITED IS NOT.** Live
instance: `ARC_AGENT` §23.2 opens *"the seven shapes from §12.1"* and they are **not the same
seven** — it drops `ALREADY THE LOOP` and adds `ROUTINE`, so **eight shapes appear as two
tables of seven and each section carries one prohibition the other lacks.** Recorded, left
unfixed, and the `INDEX` cross-reference is the mitigation.

**THE BOUNDARY IS WHAT GETS FUZZY, NOT THE PRINCIPLE** — a document appearing later needs a
side, and *is this a working document* is answerable only against a written split. **The rule
places itself**: `CLAUDE.md` is working by its own terms, which is why this entry could be
written at all.

## Hard rules for the code

- **No bytecode.** `sys.dont_write_bytecode` in the package root;
  `PYTHONDONTWRITEBYTECODE=1` in the harness; a Stop hook sweeps strays.
- **No foundation model in the decision path.** A tiny, local, DSL-native *proposer* is
  permitted — it proposes, never scores, never promotes. See `docs/DISCOVERY.md` Q4.
- **No aggregation across slots.** R is indexed per object slot. Averaging is how a live
  signal disappears.
- **No pooling across games — the same law, one level up.** Every game tests a different
  skill, so a rate across games averages a board that tests the thing with a board that does
  not. **A mechanism firing on one board and not another is not a mechanism reading**: §12.4's
  trigger fires 25/25 on `sk48`, 7/25 on `g50t` and 0/25 on `ls20`, and *`ls20` does not test
  discrimination* is the finding. **Firing nowhere across many games is broken; firing only
  where the skill is present is CORRECT, and it is the stronger verdict because it
  discriminates.** Per game, never pooled.
- **The skill map is a reading, never an input.** *Which games need which skill* and *what
  overlapped across games* are taken from the ledger AFTERWARDS. **The moment either is
  available beforehand the mechanism has been handed its answer** — `act` arrived knowing what
  each action does; a skill map would arrive knowing what each game requires. **Same failure,
  one level up.** And the firing pattern is not evidence FOR an independent fact about which
  games test what: **the trigger finding work IS the evidence, and the pattern IS the map.**
- **Nothing scores itself.** A frame cannot score itself with a quantity it produces.
- **One Γ, one registry.** Never two loaded copies of the type system — a double-loaded
  module is a reinvention no grep can see.
- Keep it small. v1–v6 drowned in code before the core was right.

## Commands

    .venv/Scripts/python.exe demo.py              # the whole thing, end to end
    .venv/Scripts/python.exe gate.py runs/demo.jsonl
    .venv/Scripts/python.exe test_gate.py         # the gate's 8 checks, one defect each
    .venv/Scripts/python.exe -m ruff check .
