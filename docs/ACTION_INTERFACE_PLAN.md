# The action interface — a plan, not a build

**Isaiah, 2026-09-28. Nothing here is built until he and the reviewer check the shape.**

**THE INSTRUCTION, IN HIS WORDS:** *"The agent shouldn't really care about what action they
choose. It shouldn't factor in their reasoning at all. They should reason first, consider all
systems, then come to a conclusion, and then depending on if it's a single or multistep plan,
they coordinate with the interface that translates that into actions. If it is done this way an
agent never need worry about wagering or balancing actions or worry about how ACTION6 'works'."*

---

## 0. THIS IS NOT A NEW RULING. IT IS AN OLD ONE APPLIED WHERE IT NEVER WAS

`TRAINING_PLAN:405`, Isaiah 2026-09-14, recorded as **two rulings, both binding**:

> *"RL trains on the REASONING/COMPOSITIONS ... **never on the actions** ... **ACTIONS MUST NOT
> BE BAKED IN** — action-mapping happens AFTER, is trivial, and must stay agnostic. The agent's
> brute-force enumeration **baked actions into the composition space (`slot × action → slot`)**,
> which is the trap to avoid ... the *which button achieves it* mapping is a trivial post-hoc
> lookup, kept out of the trained content entirely."*

**That ruling was written about TRAINING. The live decision path never obeyed it**, and
`slot × action → slot` — the exact trap it names — is `PREDICT`, which the running agent
enumerates over every cycle. **So this is a conformance job against a binding ruling, not a new
design.**

**AND F28 ALREADY DREW HALF THE SEAM.** `arc_world.actions()`: *"Only the DIRECTIONAL SEMANTICS
must never reach the agent — **availability is legitimate to read**."* Isaiah's instruction
extends that: availability should reach the agent **as reasoning**, never as a button name.

---

## 1. THE SEAM

    ABOVE      systems 0, 1, 2 reason over objects, attributes, relations and goals.
               They emit INTENT. They never name, count, enumerate, price or wager over
               an action, and no atom reads one.

    THE        translates intent -> the board's current action vocabulary, and translates
    INTERFACE  back what changed IN REASONING TERMS. Fallible, auditable, and the only
               thing in the system that knows a button exists.

    BELOW      the world's advertised actions.

**What crosses upward is never a button.** *"We can now move left or right"*, *"we can no longer
go that way"*, *"we can now click freely on any object"* — capability, in the same vocabulary the
agent reasons in.

---

## 2. WHAT THE AGENT EMITS

**Intent, in the grammar it already has.** `grammar.PRIMES` is already NSM and already typed:
`BE_AT(OBJECT, REGION)`, `TOUCH(OBJECT, OBJECT)`, `BECOME(OBJECT, ATTR)`, `CAN`, `NOT`, and the
four quantifiers. That is enough to say *put this block inside that one* or *rotate object 9*
without a new language, which is the cheapest reading of Isaiah's *"maybe they speak in NSM"* —
**flagged as the seat's reading, and he has confirmed it.**

Single-step and multi-step are the same emission at different lengths: *this*, or *this then
this*. The interface receives a plan, not a keypress.

---

## 3. SYSTEM 0 HAS TWO JOBS. SAME MODE, SEPARATE JOBS — Isaiah, 2026-09-28

**JOB A — THE CONTACT AND RELATIONS FINDER.** What does this board DO? Feeds systems 1 and 2.

  - does repeating this produce the same response, or does it CYCLE (like a rotate)?
  - how many times can it be taken — is it ONE-SHOT, like a switch?
  - is that a WALL? a CROSSING?
  - which interactions change which part of the delta?

**`RELATIONS.md` Part 1 is the substrate and it needs no avatar**: every pair of objects is
exactly one of *disjoint / touching / intersecting*, and contact subdivides into point, edge and
face — *"the subdivision carries information the boolean does not."* **Nothing there asks whether
anything is embodied.**

**JOB B — THE INTERFACE AUDIT.** Do the actions still do what the interface's table says? Is the
mapping conditional? **And reverse-translate what changed, in reasoning terms** — *the board has
enabled us to move left after XYZ* — so 0, 1 and 2 learn that a capability opened **without being
told which action it is.**

**AND SYSTEM 0 NEVER HOLDS THE WHEEL.** `TRAINING_PLAN` §14.12 already says it *"runs in PARALLEL
with systems 1 and 2 rather than instead of them"* and exists against **analysis paralysis**. The
correct relation is that **1 and 2 defer to it while they lack solid reasoning**, and stop
deferring at *enough confidence about how the board behaves* — Isaiah: >50%, or coverage of most
of the board, or salient tips about which sequences move the delta. **Not "every action tried
twice"**, which is what the code checks today.

---

## 4. WHAT THIS COLLAPSES — FOUR DEFECTS INTO ONE

Every action-path defect found 2026-09-28 is the same violation:

    `discriminate` varies the ACTION and scores terms that cannot read it
    `_move_map` keys action -> avatar displacement
    `untried` means "no avatar moved when I pressed this"
    three notions of `tried`, none of them the one the spec wants

**All four are the agent reasoning about buttons.** Above the seam, none of them exists.

**AND THE FIX I CARRIED TO ISAIAH WAS THE ENCODED ANSWER, REJECTED THREE TIMES ALREADY.**
`tether.py:2876` is explicit:

> *"spread distinguishes the actions, WITH `act` 33/96 · WITHOUT `act` 0/96. `act` is
> `v + DELTA.get(c.action, 0)` with its effect table **closed over at construction** — so
> discriminate is a property of the atom set, not a model the agent built. **It has never had to
> learn what pressing something does, because the primitive it was given already knew. That is
> the thing the action world has to take away.** ... It was read as a defect three times — twice
> by me — and each time the proposed fix was an atom that reads `c.action`, **which is the
> encoded answer with a name and a measurement already against it.**"*

**The flat spread is the DESIGNED state.** The reviewer's lead — *bind the candidate's operand
from what the action is known to do* — is that rejected fix in a new costume, and I forwarded it.
**A fourth instance, caught by the record.**

**AND THE SAME DOCSTRING NAMES WHAT IS ACTUALLY MISSING:** *"What no branch reads is the BOUND
TERM or the OBJECTIVE: nothing selects an action because it ADVANCES A GOAL."* **That is exactly
what the seam supplies** — above it the agent emits a goal-derived intent; below it the interface
picks. The gap this architecture closes is the one the record already named.

---

## 5. THE `taken` RECORD, RESCOPED

Recording *which button was pressed* preserves nothing: the board can reshuffle what buttons mean
and the record goes stale. **Record the INTENT or the multi-step plan** — the meaning survives a
reshuffle, and it is the same substrate `TRAINING_PLAN:405` already says RL trains on.

---

## 6. BUILD ORDER — AND NOTHING BELOW STARTS BEFORE THE SEAM

    1  THE SEAM         the interface module; intent in, action out, capability-change back up
    2  STRIP ABOVE IT   remove action reasoning from 0, 1 and 2 -- 38 sites in `tether.py`
                        reference `self.actions`; each is either an EMISSION (moves to the
                        interface) or REASONING (deleted, not relocated)
    3  SYSTEM 0 JOB A   contact/relations probing on the RELATIONS.md partition, no avatar
    4  SYSTEM 0 JOB B   the interface audit and the reverse translation
    5  THE OLD FIXES    whatever still exists after 1-4. Expected: much less

**AND THE MEASUREMENT CANNOT BE TAKEN YET.** The board stop is live, and it is live for the right
reason — Isaiah, 2026-09-28: *"I stopped real games because you were trying to beat the games and
build towards the games instead of finishing the agent. The real test will feature none of these
games."* **Phase 2 (`PHASE2_GUIDE_CURRICULUM.md`) widens gridworld to the families the public set
does not cover.** So the seam is built and reasoned about; it is not tuned against these boards.

---

## 7. THE RISK THIS PLAN CARRIES

**An interface that silently decides things is the encoded answer relocated, not removed.** If it
ever chooses BETWEEN goals, ranks intents, or withholds a capability the board advertises, the
agency has moved into a layer nobody is auditing. **Its only permitted job is translation and
report.** Any decision it appears to make is a defect, and the audit in Job B is what makes that
checkable rather than promised.


---

# Reviewer's four, 2026-09-28 — all taken, two checked against the code

## 8. THE BOOTSTRAP — who presses the first button

**The gap is real.** On a new board the interface's table is empty, so *rotate object 9* cannot
be translated, and learning the translation means pressing things nobody has mapped. Section 7
says the interface only translates — **so an interface that invented those presses would be the
section 7 failure on turn one.**

**TAKEN, in the reviewer's shape: the decision stays ABOVE the seam.** System 0 emits an explicit
exploratory intent — *elicit a response from object X*, *vary* — and the interface realises it by
trying unmapped actions. **Declared, recorded, and audited by Job B.**

**AND THAT IS NOT A CARVE-OUT, IT IS §14.12's TIER 1 SAID IN INTENT.** *Contact-seeking is the
DEFAULT mode ... act to make one object touch or interact with another.* The exploratory intent
IS contact-seeking; the interface's unmapped-action trial is how it gets realised on a board
whose buttons are unknown. **The one non-translating behaviour the interface has is therefore
requested from above, per-call, and visible in the record.**

## 9. WHAT `PREDICT` BECOMES — and it must be stated before step 2, not discovered in it

The loop's bet is `(before, action, after)` and `PREDICT` is `slot x action -> slot`. Section 6
says what is removed and not what replaces it.

    the bet becomes      (before, INTENT, after)
    the realisation      recorded BESIDE it, never inside it

**This changes the bet rows the ledger and the kernel checks read**, which is why it is stated
here. The agent is wrong about *what it meant to achieve*, not about *which button it pressed* —
and that is the only form under which being wrong teaches it anything transferable.

## 10. RECORD BOTH — Isaiah said "instead OR WITH the action set"

Section 5 kept only the intent and that is short of the ruling.

    INTENT        above the seam. Survives the board reshuffling its buttons
    REALISATION   below it -- which actions, in which board state. What Job B audits, and
                  what the interface's table is BUILT from

Intent alone leaves Job B nothing to check the table against.

## 11. JOB B NEEDS A WORLD WHERE IT CAN FAIL — and gridworld is not one. CHECKED

**Verified rather than accepted:** `gridworld.actions()` returns the module constant `ACTIONS`,
and `step` resolves through a fixed `_DELTA[action]` table. **The action set never changes and
the effects never change.** Job B's whole reason to exist is that they do — unlocked, made
conditional, withdrawn — so on gridworld today **it would pass vacuously**, which is *a guard
whose failure path is never exercised is indistinguishable from one that cannot fail.*

**Two fixtures, and they are Phase-2 shaped rather than invented for the test:**

    A   an action whose effect CHANGES after a trigger        -- the "unlocked / conditional" case
    B   NO AVATAR, where only acting on objects does anything -- the "click freely" case

**Those are exactly the two capabilities Isaiah's ruling names**, and B is also what retires the
no-avatar collapse properly: the contact/relations partition never needed a body, and a world
without one is where that gets demonstrated instead of argued.

## 12. "FIVE TIMES" — the primes cannot count, and they do not need to

**Checked.** No prime carries a repetition count: `ALL/SOME/ONE/NONE` quantify over a SCOPE of
objects, not over repetitions, and nothing else takes a number.

**But `routine.py` already has repetition, and in the better form** — `Routine ::= Act(a) |
Seq(R1, R2) | When(P, R) | Until(P, R)`. `Until(P, R)` is repetition terminated by a PREDICATE,
and a predicate is exactly what the primes can say.

> **SO THE AGENT SAYS *rotate until it is upright*, NOT *rotate five times*** — and that is
> **more** robust, not a workaround. A count breaks the moment the board rotates by 120 degrees
> instead of 90; a termination condition does not. **It is Isaiah's own meaning-preservation
> argument** — store the intent, not the button — applied one level in, to the loop count.

**And it adds a line to step 2:** `routine.Act(a)` holds an ACTION today. It becomes
`Act(intent)`, which makes `routine.py` part of the strip rather than downstream of it.


---

## 13. SAYING BOTH — the count is a BET, not a bound. Isaiah, 2026-09-28

**HIS CORRECTION, AND IT RETIRES §12's CONCLUSION:** *"upright is subjective and transitory but
rotate five times is specific."* **I had ranked the predicate above the count. That is wrong —
they fail in opposite directions:**

    a PREDICATE   adapts to a board whose step size is not what you assumed, and needs a
                  definition the agent may not have, of a state the board may not keep
    a COUNT       is exact, checkable and reproducible, and cannot adapt to anything

**`routine.Until` ALREADY CARRIES BOTH, and the count is the wrong KIND of thing.** `guard` is
the condition; `budget` is a number — but its own docstring says it is *"derived at
construction, never picked ... the difference between a bound and a magic number"*, existing so
that *"a satisfiable-but-unreachable guard"* cannot loop forever. **It is a safety cap. It is not
something the agent MEANS.**

### the invention: `expect`, and it makes repetition a bet

    guard    WHAT to achieve      -- adaptive, may be subjective, may be transitory
    expect   HOW MANY the agent PREDICTS it will take -- specific, and it can be WRONG
    budget   the safety bound     -- unchanged, still derived, still never picked

**EITHER HALF MAY STAND ALONE, which is what Isaiah's case needs:**

    expect only    "rotate five times"          -- pure count, terminates at five
    guard only     "rotate until it is upright" -- pure condition
    both           the bet

**AND THE DISAGREEMENT BETWEEN THEM IS A RESIDUAL — which is the whole point.** Say *rotate until
upright, expecting five*, and:

    it took five        the agent's model of the action's effect was right
    it took three       the step is LARGER than modelled -- a residual, and a specific one
    it took seven       the step is SMALLER than modelled
    it never held       a different residual, and the budget catches it

> **A BARE COUNT CANNOT BE SURPRISED. A BARE CONDITION CANNOT BE WRONG ABOUT MAGNITUDE. Together
> they predict, and being wrong is what teaches.** That is the same loop the architecture runs on
> everything else -- perceive, bet, be wrong, mint -- applied to repetition, which had been the
> one place the agent issued an instruction instead of a prediction.

**AND IT IS EXACTLY WHAT JOB A IS FOR.** *Does repeating this cycle? How many times can it be
taken? Is it one-shot?* **`expect` is where that knowledge gets spent, and the miss is where it
gets corrected.** With no model yet, the agent emits no `expect` — which is honest rather than
missing: System 0 has not learned the cycle length.

### and it answers "subjective" too

**A guard the agent cannot define, it cannot say.** *Upright* has to be built from its own
attributes — `same(orientation, X)` — so the grammar refuses a goal the agent cannot check,
which is a feature. **And TRANSITORY is a reading, not a problem**: a guard that holds and then
stops holding is the difference between a one-shot and a stable state, and that is Job A's
question asked by the routine itself.

**`expect` is NOT a magic number under `F341`'s rule.** It is not tuned, not a threshold, and not
picked by the seat: **it is emitted by the agent from its own model and is falsified by the
world.** A constant nobody can be wrong about is a magic number; a prediction is the opposite of
one.


---

## 14. RELOCATING `_learned_split` — the 71-85% mode, and two cautions that change the plan

**`_learned_split`/`_fine_vote` vote over actions** -- `max(self.actions, key=votes)` -- fed by
`contingency()`, `{member: {action: measured signal}}`. That is `discriminate:learned`: **93 of
131 acts on `g50t`, 128 of 150 on `ls20`.** The largest action-reasoning violation in the file
and the thing that works.

**IT RELOCATES BELOW THE SEAM RATHER THAN BEING DELETED**, and the argument is its own
docstring: *"Learned, never handed ... a member reports what moved when it acted."* **Taking a
MEASURED per-action fact and picking an action IS translation** -- the interface's whole job.
And it gains the reason `tether.py:2876` says it has never had: *"nothing selects an action
because it ADVANCES A GOAL."* Below the seam it is the informed realisation of `ELICIT`.

### 14a. "SAME BEHAVIOUR, CORRECT LOCATION" IS WRONG — the reviewer, and I wrote it

I claimed the relocation preserves the 71-85%. **It does not, and it should not.** Today
`learned` acts with no request from anyone. After the move it runs **only when a mode emits
`ELICIT`** -- and Isaiah's rule is that 1 and 2 defer to exploration *only until they understand
the board well enough*.

> **SO IF THE DESIGN WORKS, `ELICIT` IS EMITTED LESS AS A RUN GOES ON AND `learned`'s SHARE
> FALLS. THE BEHAVIOUR SHOULD CHANGE -- BY DESIGN, NOT AS A REGRESSION.**

**PRE-REGISTERED HERE, BEFORE THE A/B EXISTS**, because a falling share read against the wrong
expectation is a regression report about a working mechanism: **expect the share to fall, and
expect it to fall MORE in later cycles than early ones.** A flat share would be the surprising
result -- it would mean 1 and 2 never stop deferring, which is the handover question in another
costume.

### 14b. AND IT MUST NOT CARRY THE ONE-BUTTON COLLAPSE BELOW THE SEAM

**`learned` is the mode that pressed `ACTION2` 105 of 150 times on `ls20`** -- the collapse
System 0 exists to prevent. **If `ELICIT` is realised by "the most informative action by
contingency", the same scoring can keep choosing one button, and exploration that presses one
button is not exploration.** Job A needs VARIED responses from the board.

> **SO THE REALISATION OF `ELICIT` NEEDS A VARIETY CONDITION AND NOT ONLY AN INFORMATIVENESS
> ONE** -- at minimum: do not repeat an action already known to do the same thing in the same
> context. **That needs the context key** (the same one §11's audit is missing), which makes the
> key a PREREQUISITE of the relocation rather than a later refinement.

**Otherwise the collapse moves below the seam intact and becomes harder to see**, because it
would then be wearing the word *exploration*.

### 14c. the `gone`/`came` duplicate

`tether.py:4783-4800` already computes the advertised-set delta, and `Interface.capability`
now duplicates it. **One goes.** The reviewer's rule is *keep whichever is built from acting,
not handed* -- and **checked, neither is**: both read `env.actions()`, which F28 explicitly
permits (*availability is legitimate to read*). So the rule does not discriminate here and the
choice is made on the other ground: **keep the one below the seam**, because that is where
knowing about the action set is allowed to live.

---

## 15. THE VALUE TABLE — the unordered half of `BECOME`, and it is a COLUMN rather than a mechanism

**Found while deleting the goal exit's voting fallback (`4c233db`), and the reviewer corrected
my estimate of it the same hour.** The ballot had two arms because `objective_step`'s type
split has two:

    ORDERED     *did this action move it the wanted WAY*        -- a sign
    COMPARABLE  *did this action ever PRODUCE that value*       -- no sign exists to want

`Interface.audit` records a SIGNED DELTA per `(context, slot)` and no record of a value
REACHED. **So the interface can serve the first arm and structurally cannot serve the second**,
and `Intent(BECOME, slot, "+")` has nowhere to put *make it 3*. The unordered case therefore
abstains under its own name, `unordered_no_value_table`, which is what makes the gap countable.

### 15a. MY ESTIMATE OF THE COST WAS WRONG AND IS WITHDRAWN

I wrote that the loss would be SMALL, reasoning that the old arm needed the exact target value
to appear in history, *which on a slot with a wide alphabet is nearly never*. **I never counted
which slots are actually unordered.** `ORDERED_TYPES` is exactly `("POSITION", "EXTENT",
"DELTA")` — so unordered is **COLOUR, SHAPE, BOOL and REGION**, and colour's alphabet is TEN.
Recolouring is among the commonest ARC transformations, so the population I dismissed as rare
is the one most likely to carry the goal. **The reviewer's flag, 2026-09-28, and the story was
general in its wording while the set it ranged over was never counted** — which is this
project's own *a null carrying a satisfying causal story* at the level of an estimate.

**AND THE HONEST STATEMENT IS SHARPER THAN EITHER ESTIMATE: UNDER THE BOARD STOP THE COST IS
UNMEASURABLE.** The one world that may run is gridworld, whose goal slots are POSITION — the
ORDERED side — so **gridworld cannot show this cost at all**, and a green reading there would
be a panel structurally unable to reward the thing tested. **Recorded as a known gap with no
available measurement**, neither small nor large.

### 15b. THE BUILD, AND IT IS THE COLUMN THE DELTA TABLE IS ALREADY STANDING NEXT TO

`audit` already receives `before` and `after` on every step. Recording **which VALUES each
action has been observed to produce on each slot** is the same rows, the same provenance, below
the seam. It is not a second mechanism.

    what is recorded    per (context, slot): the set of values this action was observed to
                        LEAVE the slot at -- `after[slot]`, never `before`
    what it serves      `BECOME(slot, =v)` -> the action observed to leave it at `v` here,
                        else across contexts, else ABSTAIN
    what it is not      a predictor. It says *this has happened*, never *this will*

**TWO THINGS THAT ARE NOT OBVIOUS FROM THE SKETCH, and both are decided here rather than in
the build:**

- **AND THE KEY CARRIES THE VALUE BEFORE THE PRESS — the reviewer, 2026-09-28, caught BEFORE
  the first multiplicity count was read.** Keyed `(context, slot)` alone, a **CYCLING** action —
  colour 3 → 4 → 5, or a rotation — leaves a different value every press, so its cell fills with
  values and the singleton rule refuses it. **But a cycle is perfectly reproducible, and
  recognising one is among the things Isaiah named System 0 for** (*is it cycled (rotate)*).
  With `before` in the key, `(context, slot, before) → after`, **a cycle and a fixed recolour
  are BOTH singletons** and only a genuinely unreliable action shows multiplicity. **Without
  this the refuter in 15c would have counted every cycle as a superstition** — a high number,
  correctly computed, measuring the wrong thing. It also changes what `realise` needs: the cell
  is asked FROM WHERE THE SLOT IS, so the current reading is passed down beside the context.
- **THE KEY IS THE SAME CONTEXT KEY, NOT A LOOSER ONE.** The context is what separates *conditional*
  from *the mapping changed*, and **a recolour that only works while touching something is
  exactly the case that needs it.** The realiser may fall back to the across-context prior —
  as `BECOME`'s signed half already does, and for the same reason — but the AUDIT's key does
  not widen.
- **THE SIGN AND THE VALUE MUST NOT SHARE A FIELD.** `Intent(BECOME, slot, "+")` puts the sign
  in `object`. A value intent wants that field to hold `3`. **One name carrying two quantities
  is `A6i`, and this one is avoidable before it exists** — a distinct spelling, so a reader can
  never mistake a sign for a value or a value for a sign.

### 15c. WHAT WOULD FALSIFY THE WHOLE IDEA

**That values are not reproducible from an action alone** — that `ACTION3` leaves a slot at 3
once and at 7 the next time in the same context, so the set is a history and not a capability.
That is visible in the table itself without a board: **a `(context, slot, action)` cell holding
more than one value is the refutation**, and the build must publish that count rather than
collapse the set to its most recent member. **If it is common, the right object is not a value
table but a residual, and the intent was unrealisable all along.**

---

## 16. `Act(a)` → `Act(intent)` — the last place above the seam that names a button, and the sites it actually touches

**Mapped by reading the call sites rather than by reasoning about the shape, 2026-09-28.**
`routine.Act` holds `action: str`, *"named as the environment advertises it"*. It is the last
structure above the seam that does.

### 16a. WHERE THE ROUTINE ALREADY SITS BELOW A DECISION THE INTERFACE MADE

`_mint_routine` builds its candidates as `Rt.enumerate_routines((act,), …)` where `act` is the
single action `_goal_split` returned — **which is now the interface's realisation of an
intent.** So the routine is not enumerating over the action space at all; it is wrapping ONE
already-realised button in a loop shape. **That makes the change smaller than it looks**: the
body does not need a new enumeration, it needs the thing it wraps to be the INTENT that
produced the button rather than the button.

    _goal_choice  ->  the slot            already above the seam
    _goal_target  ->  the target value    already above the seam
    the INTENT    ->  BECOME(slot, ±) or BECOME(slot, =v)    formed, then discarded
    realise       ->  one action          ** the routine is built from HERE **

**So the seam runs straight through `_goal_split`'s return type**, and the repair is to keep
the intent instead of throwing it away: the body holds the intent, and the interface realises
it AT EVERY STEP rather than once at construction. **That is not a refactor — it is a
behaviour change, and the right one**: a routine that re-realises can follow a board that
re-maps its buttons mid-loop, which is the case Isaiah described as *"we are now no longer able
to go (direction)"*.

### 16b. THE FIVE SITES, COUNTED

    routine.Act.action        the field. `advance` returns it; `render` prints it
    routine.actions(r)        every primitive the routine can emit -- 7 call sites
    tether.py:4403            the LEVEL-BOUNDARY CHECK:
                              `set(Rt.actions(r, lib)) <= set(self.actions)`
    tether.py:4111 / 4160 / 4459   `_reject_key` and the `paths` key -- a routine's
                              IDENTITY is `(slot, its action names, its guards)`
    tether.py:4377-4381       the price: `n = len(self.actions)`, `base = unsat * log2(n)`

### 16c. THE IDENTITY SITES ARE ISAIAH'S ITEM 3, AND I HAD NOT CONNECTED THEM

> *"only minor as I framed it; save the intent / action set / multistep instead, so meaning is
> preserved when the board shifts."*

**`_reject_key` and `paths` key a routine by ITS ACTION NAMES.** So a shape refuted as
`(o0.row, ("ACTION2",), ("g",))` loses its whole refutation history the moment the board
renames or re-maps that button — and worse, it KEEPS the history when the button name survives
but its meaning changes. **Keyed on the intent, the record says *I tried raising o0.row in a
loop and it failed*, which stays true across both.** That is the `taken` ruling arriving at a
site I was not looking at when he made it.

### 16d. THE LEVEL-BOUNDARY CHECK GETS BETTER, NOT WORSE

Today: *does this routine name an action the new level does not offer?* — a string comparison
against `env.actions()`. With intents there is no string to compare, and the honest replacement
is **can the interface still realise this intent here** — which is a question about the WORLD
rather than about a name, and it is the reverse-translation Isaiah asked System 0 for.

**AND IT IS STRICTLY MORE SENSITIVE**: a level that keeps every button name and changes what
two of them do passes the string check and fails this one. `audit`'s `changed` set is already
the detector.

### 16e. WHAT IS NOT DECIDED HERE, AND MUST BE BEFORE THE BUILD

- **THE PRICE.** `base = unsat * log2(len(actions))` prices *naming `g` actions myself*. If the
  agent names INTENTS, the alphabet is the intent space and not the button space, and **those
  are different sizes.** No number is invented here: the alphabet must be COUNTED at the site,
  and the count stated, or the bargain is being fed a constant nobody derived.
- **WHETHER A REALISATION FAILURE MID-LOOP IS `BLOCKED` OR `EXHAUSTED`.** Both already exist and
  they mean different things — *the guard says no* against *the budget ran out*. An
  unrealisable intent is neither, and reusing one of them would collapse two endings into one,
  which is the defect `F207` was diagnosed at. **It needs its own ending**, and `advance`'s
  contract says terminations are the only ways out that are not an action.

---

## 17. `_learned_split` BELOW THE SEAM — 71–85% of decisions, and the collapse must not travel with it

**The largest single move in this plan, and the one with a pre-registered expectation attached.
Measured: `discriminate:learned` 93 of 131 acts on `g50t`, 128 of 150 on `ls20`.**

### 17a. WHAT IT ACTUALLY READS, AND WHY THAT SETTLES WHERE IT BELONGS

`_learned_split` calls `env.contingency()` — `{member: {per_action: {action: scalar}, stable}}` —
and returns `max(self.actions, key=lambda a: sep[a])`, where `sep[a]` counts the self-members
that find action `a` distinguishable from every alternative.

**That data is an ACTION-EFFECT RECORD, which is the interface's subject and nothing else's.**
`arc_world.contingency`'s own docstring says so: *"THIS IS THE HALF `act` WOULD HAVE HANDED …
the difference is provenance."* It is the same kind of thing `audit` builds, arriving from a
different producer. **So this is not a judgement call about where the line falls** — the read
is below the seam and the argmax over `self.actions` is above it, and the argmax is the half
that moves.

### 17b. WHAT THE AGENT SAYS INSTEAD

`ELICIT`. The agent wants a distinguishable response and does not care which button gives one —
which is precisely what `sep` was computing, expressed without naming a button. **The intent is
already in the vocabulary**, so nothing new is invented above the seam.

### 17c. THE COLLAPSE, AND THE RULE THAT STOPS IT TRAVELLING — WRITTEN BEFORE THE BUILD

**`learned` IS the one-button collapse: `ACTION2`, 105 of 150 on `ls20`.** 14b already warned
that realising `ELICIT` by "the most informative action" lets the same scoring keep choosing the
same button, **below the seam, wearing the word exploration, where it is harder to see.** A
relocation done carelessly moves a known defect somewhere darker.

> **SO CONTINGENCY ORDERS, IT NEVER ADMITS. The variety rule is a CONSTRAINT and separability is
> a RANKING INSIDE IT, never a score that can override it.** Unmapped first, then
> effect-here-unknown, then least-seen — and `sep` breaks ties *within* whichever band the
> variety rule has already selected.

**That is the difference that makes it safe rather than a hope: a score can always be maximised
by one button; a constraint on repetition cannot be.** `test_the_seam_varies_what_it_explores_with`
already asserts the first three explorations differ and that no action exceeds 2 of 6, and it is
the certifying check for this move as well — **so the relocation must not require relaxing it.
If it does, that is the finding.**

### 17d. THE PRE-REGISTRATION, AND THE REFUTER, BOTH BEFORE THE RUN

**EXPECT THE `learned` SHARE TO FALL**, and to fall further in later cycles than early ones,
because systems 1 and 2 are supposed to take the turn once they have reasoning. Already written
at 14a.

> **AND THE REFUTER IS NOT *the share stayed flat*, WHICH IS TOO WEAK.** A flat share is
> consistent with the relocation working and 1/2 simply having nothing to say on this board.
> **The refuter is: the share stays flat AND the variety check's distribution is unchanged** —
> that is the collapse having travelled intact, and it is the one outcome that looks like
> success from the share alone.

### 17e. WHAT IS NOT DECIDED HERE

- **WHETHER `sep` AND THE DELTA TABLE SHOULD MERGE.** Both are action-effect records built from
  acting, from two producers. Merging them is attractive and is exactly the kind of tidy that
  loses a distinction: `contingency` is per SELF-MEMBER and the delta table is per SLOT. **Count
  what each holds before assuming they are the same thing.**
- **THE `by` LABEL.** `discriminate:learned` names a mechanism that will no longer be above the
  seam. A label that survives its mechanism is how a census keeps reporting a thing that has
  moved — so it is renamed in the same commit or the phase counts become unreadable.
