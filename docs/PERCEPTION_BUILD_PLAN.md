# The Perception Pipeline, against what is built

**A build plan in `PERCEPTION_PIPELINE_general.md`'s form, stated against this instantiation.** Each
layer carries: **what exists today · what would change · what it depends on · what the corpus says.**

**Validated against Figures 1–13, the Operators and Symbols tables, and `THE_FORMULA`.**

> **REVISION 2, 2026-09-04. THE NINE SEAMS ARE SETTLED.** Each settlement is stated at the layer it
> lands on, and the seam section now records **the resolution and what it changed** rather than
> options. **Three settlements were grounded in mechanisms that already exist** — `R_T` for the
> ablation round trip, `Standing.decay` for the confidence clock, §16.2 for the per-locus mode — and
> **two lookups inverted a proposed derivation.** *The phase order is unchanged; what moved is what
> each phase must contain.*

---

## Where the chain breaks today

**Measured 2026-09-03, per link, from this session's readings.** *A reading, not a property.*

    1 perception    REACHED     120 slots on g50t; identity by max overlap, shape_of fallback
    2 vocabulary    THIN        5 of 7 affordances written; ONE relation of ~70; COUNT and
                                AXIS have no producer
    3 objective     PRESENT,    the ticker runs every cycle -- R_goal = 1 - degree on the
                    BORROWED    REWARD channel -- and reads levels_completed/win_levels, 0.0
                                first cycle to last. Not "in its own terms"
    4 planning      SLOT HELD   no PLAN step in ledger.STEPS; the spread argmax and
                    BY OTHER    _learned_split choose the MOST DISTINCTIVE action
    5 learn/carry   UNASSESS-   advanced:false at every length, so nothing has crossed a level
                    ABLE

**The pipeline's seven layers map onto this chain, and the break sits at the pipeline's Layer 5** —
*a thin relation vocabulary caps everything the lookup can name*, which is the spec's own sentence
and this build's measured state. **The settlements did not move it.**

---

## Layer 1 — The frame as a change-tracked tree

**EXISTS.** `arc_percept.components` is a flood-fill partition into connected same-colour regions,
one dict per object with `cells · colour · row · col · h · w`. `Objects.__call__` tracks identity
across frames by **maximum overlap**, falling back to `shape_of` when overlap is zero — *an object
smaller than its own displacement has zero overlap with itself one frame later.* **Death only on
evidence.** Change detection exists in three places: `delta_of` per object, `_advertised` for the
action set, `_present` for the slot set.

**WHAT CHANGES.** Five now, and the first is a ruling not a build.

**(a) The tree is flattened at the boundary.** `observe()` returns `dict[str, int]`, so every object
becomes `name.attr -> int` and the tree structure is gone by the time the loop sees it. **This is the
`dict[str, int]` ruling, open.** *Four erasure sites depend on it: the frame stack, the component
list, the offset frozenset, and the extractor ceiling.* **SEAM 8 settled the direction** — the tree
enters by a side channel, Layers 4 and 5 read it directly, and **only their OUTPUTS need to become
bettable.** *That shrinks (a) from a widening to a wiring.*

**(b) `cascade` — the within-step chain — is discarded.** `board()` returns `frame[-1]`. **Measured:
`g50t` carries 7 or 9 frames on 39% of responses; `ls20` carries one, always.** *So a relation forming
and breaking mid-cascade is invisible — on one board and not the other.* **Per game, never pooled.**

**(c) The full pair matrices are computed and thrown away.** *The matcher computes overlap for every
(new × tracked) pair and keeps one name; `contacts()` computes every same-frame pair and drops it on
`step`.* **A store keyed by pair is a record written where a matrix already exists, not a
computation.**

**(d) NEW — the two change quantities are named apart, and `animation` is retired.** *One word over
two real quantities was filed prospectively as `A6i` and ruled before it cost anything.*

    cascade      WITHIN-STEP. the sub-frame chain one action spurred. carries the causal
                 ORDERING the endpoint erases. CONSUMER: the causality tracker -- the WHY
    transition   ACROSS-STEP. the change between two settled boards. CONSUMER: the attribute
                 tracker -- the WHAT

**`transition` is not a new word: `tether.py:101` already declares it as a residual channel and
`tether.py:535` files `SlotResidual(s, TRANSITION, pred[s], actual, bits)` on the per-slot across-step
change.** *Same quantity, already named.* **THE ACCEPTANCE CONDITION ON THE NAME IS ONE PRODUCER, ONE
CHANNEL** — if Layer 1 emits transitions that never reach a `SlotResidual`, two things called
transition never meet **and it becomes `A6i` after all.** `cascade` is unclaimed.

**(e) NEW — the per-locus mode, and its detectors are built while its consumer is not.**

**§16.2 already rules the design, quoting `THE_MISSION`:** *is there an **avatar** my directional
actions translate, or do I act through a **click actuator** — and even that **BLENDS mid-game**, so it
must be detected **contingently per step, never used to label the game**.* **Four readings:**

    one slot's delta correlates with my action  ->  avatar         (embodied)
    no slot correlates but the board changes    ->  actuator       (disembodied)
    several correlate                           ->  COUPLED BODIES
    and it may change mid-level                 ->  re-read every step

**BUILT:** all four §18.3 hypotheses — `arc_self.family()` returns `TranslationSelf`, `GrowthEdgeSelf`,
`ValueLatentSelf`, `RegionToggleSelf` in table order, fed at `arc_world:290`.

> **NOT BUILT, AND THE GAP IS PRECISE: THE LOOP READS THE FAMILY'S MEASUREMENTS AND NOT ITS VERDICT.**
> `_learned_split` consumes `contingency()` — `{member: {per_action, stable}}` — and **`tether.py`
> contains zero references to `selected()` or `has_self()`.** *Nobody reads which hypothesis won, or
> whether there is a self at all.* **And the family is ONE family over the WHOLE BOARD**, so a
> per-locus index does not exist either.

**What the mode owes:** per-locus indexing · a consumer for the verdict · composition to a board
reading · the trajectory record. **An embodied locus drops to PREDICTION-ONLY** — the agent knows it
moved left because it *chose* left, so what is tracked is the prediction and whether the locus *stops*
responding. **A disembodied locus maps available actions to surroundings** through relations and
attributes, because there is no self-object to reduce.

**THREE CONSTRAINTS, AND THEY ARE WHAT KEEP IT LEGAL:**

- **PER-LOCUS DRIVES, AND THAT IS LICENSED.** *Thin I/O, detected contingently per step* is the one
  legitimate distinction `CLAUDE.md` allows.
- **BOARD-LEVEL COMPOSES AS A READING, NEVER AN INPUT.** **The skill-map law:** *the moment it is
  available beforehand the mechanism has been handed its answer.* **A composed `HYBRID` that selects
  behaviour is a type branch; one read afterwards is a finding.**
- **A RECALLED TRAJECTORY PREDICTS AND NEVER GATES** — which proven/believed/open already enforces,
  since a recalled mode is **believed** and belief yields to first-hand.

**NO THRESHOLD IS INTRODUCED.** A locus is **proven-embodied the moment alignment holds first-hand**
and demotes when it stops. *The count was never the thing, and the demotion IS the switch detection —
no separate alarm.*

**AND `disembodied` IS NOT READ FROM AN ABSENCE.** *The whole-family-fails case already has a built
reading and it is not this one:* **`SelfModelFamily.unmodeled()` — *"the completeness critic. **The
whole family failing together is the signal**"* — true when `selected()` is `None` or when unexplained
exceeds explained.

> **`unmodeled` MAPS TO `unknown`, NEVER TO `disembodied`.** *`has_self() == False` across four members
> says the detectors found nothing, which is not the claim that there is nothing* — **and §18.3 is the
> case: `has_self: false` for 904 steps meant the detector was wrong, not that `ls20` had no self.**
> **`unknown` is `NOT_RESOLVED` at the mode level** — null-not-absent, one level up, and the same
> reason.

**SO THE DISEMBODIED VERDICT NEEDS A POSITIVE CONJUNCT, AND THE BUILD HAS IT:** §16.2's own wording is
***no slot correlates BUT THE BOARD CHANGES*** — *acting at a distance.* **The second half is the
transition residual over the slot set, and it is what makes the reading causal rather than absential.**

    unknown        the family found nothing, and nothing else is established
    disembodied    the family found nothing AND the board moved -- something changed and
                   nothing I track did it

*`CLAUDE.md`: **prefer positive causal evidence over absential; absence of evidence resting on
completeness never holds mid-episode.*** **A `disembodied` read off `all(not has_self())` alone is
exactly the inference §18.3 refuted.**

### THE FIVE VALUES, EACH WITH A POSITIVE CONDITION — AND THEY DO NOT ALL LIVE AT ONE LEVEL

**RULED 2026-09-04: the full set is a requirement, not a schedule.** *That `coupled_agency.py` is named
in §16.2 and absent from the repo is a name written before its code and says nothing about whether the
capability is needed.*

    PER-LOCUS      unknown        the family found nothing here, and nothing else is established
                   embodied       this locus's delta correlates with my action, holding FIRST-HAND
                   disembodied    no locus correlates AND the board moved

    BOARD-LEVEL    coupled        SEVERAL loci correlate TOGETHER -- not one avatar
                   hybrid         the loci DISAGREE -- at least one embodied, at least one not

> **THE SPLIT IS NOT COSMETIC: SEAM 8's CONSTRAINT REACHES `coupled` TOO.** *Board-level composes as a
> reading, never an input.* **`coupled` and `hybrid` are BOTH compositions over several loci, so
> NEITHER MAY GATE** — and the full-set ruling therefore extends the gating discipline rather than
> relaxing it. **Only the three per-locus values drive anything, and they drive tracking, not
> behaviour.**

### `coupled` IS THREE STATES, NOT A CHOSEN READING — RULED 2026-09-04

**The fork was real and NEITHER reading wins, because a public game mixes them.** *So the two readings
become the two DISCRIMINATORS, and the classification is PER RELATIONSHIP rather than per game:*

    independent      moved this action, DIFFERENT displacements    coincidence, not coupled
    coupled-rigid    moved this action, SAME displacement          one body
    coupled-loose    moved together consistently, not identically  correlated, not rigid

**Two comparisons, both over data already held:** *same action* is the per-locus contingency;
*same displacement* is `delta_of`'s `(drow, dcol)` compared over the pair. **Nothing new is gated, and
`coupled` stays in the ungated set.**

> **AND THE THREE DO NOT CLASSIFY AT THE SAME RATE, WHICH THE PER-STEP REQUIREMENT MAKES MATTER.**
> *`independent` and `coupled-rigid` are readable in ONE step; `coupled-loose` is **consistently, not
> identically**, which needs a HISTORY.* **So loose cannot be a per-step verdict** — and it needs no new
> machinery, because **rigid is `proven` per step and loose is `believed` from accumulation.** *The
> confidence rule already carries the difference.*

**AND THE LEVEL TABLE GAINS A THIRD ROW, BECAUSE A RELATIONSHIP IS NOT A LOCUS AND NOT THE BOARD:**

    PER-LOCUS           unknown · embodied · disembodied          drive TRACKING
    PER-RELATIONSHIP    independent · coupled-rigid · -loose      a READING over per-locus data
    BOARD-LEVEL         coupled · hybrid                          compositions; Seam 8: NEITHER GATES

### AND ONE MEMBER OF THE FAMILY HAS NO LOCUS TO INDEX, WHICH PER-LOCUS INDEXING ASSUMES AWAY

**`ValueLatentSelf`: *"a NON-SPATIAL self … **there is no self-cell to point at — the self IS the
value**."*** It tracks `_counts(board)` **keyed by colour, board-wide** — not per object.

> **SO THE ONE MEMBER §18.3 ADDED BECAUSE A TRANSLATION-SHAPED FAMILY FAILED TOGETHER IS THE ONE THE
> PER-LOCUS INDEX CANNOT HOLD** — *and it is the member that answers `ls20`, the board the family was
> repaired for.* **Per-locus indexing assumes every self-hypothesis is about a locus, and one of four
> is not.**

**THE HOLE IS NOT A REASON TO DROP THE INDEX; IT IS AN ENTRY THE MODE NEEDS.** *A value-latent self is
a self with a board-wide extent*, so it composes to a board reading without passing through a locus —
**which the two board-level values already admit as a level.**

### THE WORKSHOP, AND TWO THINGS THE MEMBER'S CODE ALREADY SETTLES

**DRAFTED CONDITION — input→value alignment, where embodied has input→locus alignment:** *concludes
when an agent action produces a consistent, intended change in a board-wide value, and no single locus
accounts for the change.*

> **THE SECOND CONJUNCT IS ABSENTIAL AS WRITTEN, WHICH IS THE DEFECT JUST CORRECTED FOR
> `disembodied`.** *"No single locus accounts for it"* **is not an absence — it is a RESIDUAL, and the
> build computes residuals.** **State it positively: the value's change carries UNEXPLAINED MASS after
> every locus's contribution is priced** — which is `outstanding`, monotone and per-slot, already
> running. *An absence cannot be checked mid-episode; a residual can.*

**AND THE INPUT→VALUE HALF IS ALREADY IMPLEMENTED.** `_attribute(action, cts[colour] − was)` is the
per-action contingency on the value; `has_self()` is *"consistent AND meaningful: every nonzero step one
way, and net travel of at least one unit per nonzero step."* **The condition's positive half is built;
only the residual conjunct is missing.**

### AND THE P5 KEY QUESTION IS SMALLER THAN IT LOOKS, BECAUSE THE MEMBER ALREADY SEARCHES

**The member does NOT hold a stipulated value. It SELECTS one** — *the non-background series with the
highest monotonicity*, `mono = |Σ sign(Δ)| / |nonzero|`, `best` updated every observation.

> **SO THE WORKSHOP QUESTION IS NOT *WHICH VALUE PLAYS THE ROLE* — THE AGENT ALREADY ANSWERS THAT.**
> **What P5 changes is only the SPACE THE EXISTING SELECTOR RUNS OVER**: palette integers today,
> and after P5 whatever board-wide quantities are published. **The item is *widen the candidate set*,
> not *identify the value*.**

**AND THAT IS THE DOCTRINE LINE, NOT A CONVENIENCE.** *Naming the zoom-level for a given game would be
encoding the answer* — **the monotonicity search IS the agent doing the identification, and it is the
evidence the mechanism works.** *Hand it the value and there is nothing left to measure.*

**WHAT REMAINS TO THE WORKSHOP:** the residual conjunct's exact form, and **what board-wide quantities
P5 should publish into the candidate set** — *a perception question with an entry rule, which is the
legitimate way to widen Tier 1.* **It must resolve before P5, because P5 changes what the member
reads.**

**The trajectory is a record, not a state machine:** `EMBODIED@0 → +DISEMBODIED@k → HYBRID (current)`,
**transitions filed as causal events under the level** — *object_7 became controllable at step k*, *the
avatar went inert at step m* — **the same class of event as an object appearing or vanishing.**

**DEPENDS ON.** (a) is the gate for (c). **(d) and (e) are ungated** — (d) is a naming decision, and
(e)'s loci already have a key in `slot_owner()`.

**CORPUS.** Figure 13: *a state with no structure has no magnitude.* The slot dict holds states;
`slot_types` and `slot_owner` are the structural half and are domain-declared, which is correct.
**Figure 4's membrane licenses the flattening as a coarse-graining — provided the loss is measured,
and `R_T` is the instrument for that and is not pointed here.**

---

## Layer 2 — The reading pattern

**DOES NOT EXIST.** Nothing orders the slot set. `slots()` returns `sorted(self._decomposed())` —
**alphabetical by slot name**, which is stable, arbitrary, and not a perceptual order.

**WHAT WOULD CHANGE.** A per-frame ordering over slots, recomputed each frame, narrated in the
ledger, never settled as a term.

> **SEAM 1 SETTLED: §11 NEVER APPLIED.** `CLAUDE.md` 390–396 — ***entering means entering Γ**; the
> five non-Γ homes are **POPULATED, not entered**… §23.2's* what to look at vs what to do *governs
> loading the five; §11's two clauses govern entry into Γ.* **A reading order is *what to look at*, so
> §23.2 governs it and the entry rule was never the test.**

**AND THE FALLBACK IS ALREADY BUILT.** `_last_mass` picks the focal slot by **maximum unexplained
mass** — `outstanding` used as an ordering, running today, **licensed as ROUTING rather than
scoring.** *Not a new mechanism; the existing one given a second consumer.*

**The abstraction rule stands as the design obligation:** *the same layout under the same conditions
yields the same ordering every time.* **F by default, the others as conditioned fallbacks, the
fallback conditions themselves consistent.**

---

## Layer 3 — Colour as order-of-encounter

**DOES NOT EXIST.** `colour` is the raw palette integer, published as a durable slot value and used
directly in `correction_bits`. **There is no ID, no band, no cache/durable split for it.**

**WHAT WOULD CHANGE.** A colour-ID table per play: first encounter in a band gets `<band>1`, the raw
value stays cache-only, the ID goes durable. **On reset with a palette swap, new hues alias onto
existing IDs.**

### `GB1` IS `SPECTRUM × TIME`, AND THAT IS A CELL ALREADY IN FIGURE 13'S MATRIX

- **the band is `SPECTRUM`** — *where*, ordered, physically real. **A subset of a spectrum is still a
  spectrum**, so the visible band keeps the name.
- **the index is `TIME`** — ***the ordered succession of differences***, which is exactly what
  order-of-encounter is.

**A STRUCTURE AGAINST A STATE — a legal cell in `EVERY PAIRING AVAILABLE`, with no within-kind
composition anywhere in it.** *The network is not involved and must not be:*
`RECURSIVE_TRANSFORMATION` Part 4 — ***not from `NETWORK`, though it is often claimed***, the
construction *presupposes what it derives*; a network **exhibits** discreteness rather than
**producing** it; ***`SPECTRUM` supplies distinguishability, and distinguishability is all counting
requires.***

**THERE IS NO CUT, BECAUSE THE BAND WAS NEVER CONTINUOUS IN THE AGENT'S HANDS.** A continuum is *a
spectrum with **no gaps required*** — **the requirement is ADDED, so the gaps were never removed.**
The agent only ever holds **encountered colours, a countable set.**

### FROZEN AT PLACEMENT, FOR TWO REASONS

**Figure 13:** *a settled composition enters the library as a term, and is then **an operand like any
other**.* **A composition becomes an operand only once SETTLED**, so a derivative recomputed on every
palette swap was never an operand and could never have joined. **And a coarse-graining that recomputed
would be re-deriving the level from a substrate it discarded.**

### THE CACHE/DURABLE SPLIT IS THE COARSE-GRAINING, SO THE LOSS IS THE MECHANISM RATHER THAN THE COST

*"**Physical continua are not found. They are what remains after detail is discarded** … water
modelled as a field keeps density and discards ten to the twenty-three molecules."* **The raw RGB is
the molecules; the band is the density.** **So *raw value cache-only, band ID durable* IS the lossy
upward transform — and a new hue aliases onto `GB1` PRECISELY BECAUSE the transform already discarded
what would have told them apart.** *Derived, not stipulated.*

**AND IT IS `R_T` A THIRD TIME:** `T_A` is colour → band, `T_E` is band → a colour, **the gap is the
raw value that cannot come back.**

### WHAT THIS DOES NOT DO

**`above(GB1, GB2)` never forms.** The band is genuinely ordered; **the index is order-of-encounter
and arbitrary**, so it is not a magnitude. **`COLOUR` stays `COMPARABLE` and not `ORDERED`**, and the
erasure work is untouched.

**WHAT IS ALREADY THE RIGHT SHAPE.** `Affordances` already runs the cache/durable split with the rule
stated: *"Drop the bindings, keep the table. **Vocabulary permanent, instances transient.**"* **The
colour-ID split is that same rule at a different site.**

**SEAM 3 SETTLED: `GB1` is `Item1` until filled** — the band carries no significance, and **the fill
is what carries strategy.** *Aliasing on position alone inherits nothing.*

### THE MID-GAME COLOUR CHANGE — SPECIFIED 2026-09-04, AND IT SEPARATES THREE THINGS THE PLAN HAD AS ONE

**RESOLVED AS POINTER-VERSUS-VALUE, WHICH IS A CHANGE FROM THE FIRST STATEMENT OF THE RULING.**
*The identity was first given as `IV3` — a colour label made permanent. It is not a colour label at
all.*

    IDENTITY     A POINTER. a stable handle, assigned once, NEVER REUSED, and never a colour.
                 `obj_7` is `obj_7` whatever happens to its colour
    PLACEMENT    A VALUE. a band plus that band's RUNNING MAXIMUM -- a position ANOTHER object
                 can hold at another time. `GB4` highest means the next arrival is PLACED AT
                 `GB5`, and the one after is `GB6`. Shared and monotonic per band
    CHANGE-LIST  append-only, a standard attribute on every object. the placements it has held
                 over time, plus whatever rode with each change -- which step, what else moved

> **AND THE POINTER ALREADY EXISTS: `slot_owner()` ASSIGNS IT.** *`{s: s.rsplit(".", 1)[0]}` is the
> object handle, domain-declared, running today.* **So the split does not add a mechanism — it REMOVES
> a responsibility from Layer 3**, which never needed to carry identity and only ever needed to produce
> placements.

**THE SHARED MONOTONIC COUNTER CONFIRMS THE `SPECTRUM × TIME` DERIVATION RATHER THAN COMPLICATING IT.**
*`TIME` is **the ordered succession of differences***, and **a shared per-band sequence IS a succession;
a per-object index would have been a tally.** *The ruling picked the one that types.*

**AND THE CHANGE-LIST IS THE MONOTONE-BY-ADDITION SHAPE, FOR THE THIRD TIME.** *`outstanding` is the
dilution rule as a data structure — nothing leaves the confines*; `origin` is append-only provenance;
**the change-list is the same shape at a third site.** *Native, not imported.*

**THE `A6i` IS CLOSED BY THE SPLIT** — *one label carrying two quantities, cured by one name per
quantity, which is the same cure `ATTR` and `OBJ × OBJ` took.*

> **BUT IT LEAVES A HOLE THE FIRST STATEMENT WAS FILLING, AND THE HOLE IS CROSS-PLAY.** *If the colour
> ID is a placement and not an identity, **what carries an object's strategy from one play to the
> next?*** **`slot_owner()`'s handle is a WITHIN-play tracker name** — `Objects.__call__` re-derives it
> by max overlap each episode — **and Layer 7's hash identifies the GAME, not an object in it.**
> *The original spec had the colour ID doing this job — "**strategies filed under `GB1` are still
> reachable**" — and the split takes the job away without reassigning it.*

**AND THE CORPUS ALREADY SPECIFIES THE ANSWER, ONE SCALE DOWN.** Layer 7: *a hash from **the game's own
structure, the distinctive groupings and attributes, the shape of the game and not its colours**.*
**Distinctive groupings and attributes are OBJECT-level content, so the same construction applies to an
object: a cross-play object identity is a hash of ITS structure, not its colour.**

> **Which is why the colour ID could never have carried it: filing by hue is the contamination the
> hash rule exists to forbid, and it does not stop being contamination one level down.** *The game hash
> and the object hash are one law at two scales, and only the first is written down.*

### RGB IS THE LIVE GROUPING KEY, WHICH CORRECTS ONE OF THE TWO FREEZE REASONS

**The raw value is not kept merely to tell two blues apart at first encounter.** *When an object changes
colour or a new one appears, placing it in the right band and deciding whether it joins an existing
group is done by comparing its actual RGB against the values already recorded.* **RGB is the GROUPING
key during play; the ID is the IDENTITY key across play.**

    cache, this play      raw RGB, keyed to the colour ID. THE SUBSTRATE THE PLACEMENT RUNS OVER
    durable              the identity, the change-list, and the groupings keyed to them

> **SO `T_A` RUNS REPEATEDLY WITHIN A PLAY, AND MY SECOND FREEZE REASON WAS SCOPED WRONG.** *A
> coarse-graining that recomputed would be re-deriving the level from a substrate it discarded* is
> **true ACROSS plays and false WITHIN one** — the substrate is live in cache all play. **The
> conclusion is unchanged and the mechanism is corrected: what is frozen is the IDENTITY, never the
> placement OPERATION**, and the freeze is protected by the cache being dropped at `boundary` rather
> than by the substrate being unavailable. *Which is also why aliasing works next play: by then the
> substrate really is gone.*

---

## Layer 4 — Objects, groups, subgroups

**PARTIAL.** `slot_owner()` groups slots by object — `{s: s.rsplit(".", 1)[0]}`, domain-declared,
*"a loop that split on `.` would be reading domain structure."* **That is grouping at one level only:
slots into objects. There is no grouping of objects into classes, and no subgroup.**

**WHAT WOULD CHANGE.** Classes keyed by colour ID; subgroups by shape and orientation within a
class; **and class behaviour as data — do the members move together or individually.**

**DEPENDS ON.** Layer 3 for the class key. **And on §12.4's trigger, which already computes something
adjacent**: *two slots with the same attribute vector and different residuals*, grouped by
`(type, value)`. **That is a same-attribute grouping and it is built** — it groups by attribute
vector rather than by colour class, and the machinery is the same.

**AND IT NOW SHARES A CONSUMER WITH LAYER 1(e).** *Do the members move together or individually* and
*several loci correlate with my action* **are the same measurement read for two purposes** — the first
names a class, the second names `coupled bodies`. **One computation, two readings.**

**CORPUS.** Figure 13: *network — that entities relate, and influence travels.* A class whose members
move together is a network reading. **The corpus has the term; the build has one grouping level.**

---

## Layer 5 — Attributes, relations, causality

**PARTIAL, AND THIS IS THE BREAK.**

    BUILT     eight extractors (colour · row · col · h · w · drow · dcol · shape)
              NOT_RESOLVED as null-not-absent, at the sensor AND in `Term.apply`'s
              propagation -- "the instrument could not see it" travels rather than
              becoming a wrong attribute. THIS IS LAYER 5's OWN REQUIREMENT, ALREADY MET
              retrieval keyed by the characterised residual (`retrieval.py`, 3c)
    THIN      ONE relation published: `touching`, via `contacts()`
              `triggers_remote` and `terminates` declared and never written -- `note` is
              contact-local and a remote trigger has no touching partner at the far end
              COUNT and AXIS declared with no producer; BOOL, RATIO, REGION produced and
              unconsumable
    ABSENT    a causality tracker distinct from the attribute tracker

**WHAT WOULD CHANGE.** The relation vocabulary is the item. `RELATIONS.md` marks **~30 relations as
composable from what the agent already holds**, blocked by two things: **`overlap` computes shape
congruence rather than spatial overlap** (and cell-IoU between distinct objects is identically zero
under solidity, so bounding boxes are needed and are a Tier-1 addition), **and `slot_types` has no
entry for a relation, so the retrieval key can never name one.**

> **SEAM 4 SETTLED: ONE EVENT, TWO THRESHOLDS.** **Settled change is the TRIGGER; residual size is
> the SALIENCE FILTER.** *The pipeline and the build were never describing different events — one
> named the firing, the other named the ranking.*

**THE CONSEQUENCE IS CALL VOLUME, AND IT IS PRICED RATHER THAN OBJECTED TO.** §15.3 claims matching is
**a one-pass check, not a search**, and `R > 0` is what holds retrieval to one pass **per residual**.
**Firing on every settled change retrieves for events the model already predicts.**

**AND THE CAUSALITY TRACKER NOW HAS ITS INPUT NAMED.** *Absent* above is answered by Layer 1(d):
**`cascade` is what it consumes** — the within-step ordering — **which is why it is a tracker distinct
from the attribute tracker rather than a second reading of the same stream.** *And Layer 1(e)'s mode
transitions are filed to it, being causal events of the same class.*

**CORPUS.** §12.3's nine, and the Tier-2 rule: *if it composes from the nine it should be minted, not
installed.* **Containment and alignment both compose, so both are forbidden as installs.** *What
breaks the circle legitimately is a richer Tier 1 — and `overlap` is Tier 1 and computes the wrong
quantity.*

---

## Layer 6 — The action loop

**LARGELY BUILT.** Bets are per slot per action; `R = |Γ(b,a) − o′|` is the transition residual;
the MDL bargain prices candidates; `Budget` counts actions and `spend()` is wired.

**WHAT CHANGES.** Two, and both are small.

**(a) The budget is not read by anything.** `exhausted()` and `Termination`'s `cap` are unwired.
**Figure 13 settles what it is: a GRADIENT — *a difference that can be spent* — not energy, which is
*directionless alone*.** `THE_FORMULA` licenses it by name: *the action budget prices finding out
whether it holds*, **in a currency that does not add to the description length.**

**(b) The action-scale case has TWO gates, not one, and they are different in kind.** *Predicted
five presses, one sufficed* is the same case as an embodied locus behaving differently than commanded —
*self-tracking-as-prediction, seen from the action side.* **But it splits:**

    THE GAP          predicted action count against actual. NEEDS A MULTI-STEP PLAN, and there
                     is no PLAN step in `ledger.STEPS`. Gated on LINK 4, not on P4
    THE MECHANISM    slid or teleported -- what property was missed. NEEDS THE CASCADE, so
                     gated on P4. And `ls20` carries one frame always, so on ls20 the
                     mechanism half is UNAVAILABLE PERMANENTLY rather than pending

**So *action-scale learning waits on P4* would be wrong in both directions**: the gap waits on
something P4 does not supply, and the diagnosis never arrives on half the panel. **Seam 9's condition,
reaching a second item.**

> **SEAM 5 SETTLED: DISCOVERING A BOUND THROUGH PLAY IS EXPERIENCE; READING A GIVEN PARAMETER IS A
> SEAT-READ.** *The same line as the hash — computed versus handed.* **`PER_LEVEL` and `MAX_ACTIONS`
> stay seat-side and unread by the agent.**

**AND THE DEATH POINT IS ALREADY IN THE LEDGER — AS A SEAT READING, WHICH REVISION 2 DID NOT SAY.**
*`by` summing to the act count* — **~131 on `g50t`, ~152 on `ls20`.** **That is MY reading of the
ledger, not the agent's memory**, and revision 2's phrasing invited the opposite.

### THE CEILING ABSTENTION — RULED 2026-09-04, AND IT IS AN INSTRUMENT RATHER THAN A LOSS

    KEPT, DURABLE   step counts, action counts, what-cost-what PER GAME. First-hand experience,
                    how bets are sized, and the recall behind `strategy X took 40 steps there`
    ABSTAINED       the single `MAX_ACTIONS` ceiling per level. NEVER SAVED AS A NUMBER

**THE REASON IS NOT BOARD-SPECIFICITY.** *Keeping every count and never the ceiling leaves the agent
knowing only the **RELATIVE** action cost of games and never the absolute budget of a level* — **which
is itself the proof-of-learning property**, since it demonstrates the shape of effort was learned
without the answer key. **And if it ever reconstructs the ceiling from relative data, EARNING the
number is categorically different from being handed it.**

> **SAME SHAPE AS CLAUSE 3 AND AS SEAM 6's BACKUP: WITHHOLDING IS WHAT CREATES THE MEASUREMENT.**
> *Wipe Γ and see whether the win survives; withhold the absolute and see whether it is derived.*
> **An abstention that makes a later claim checkable is an instrument, and this one has a falsifier:
> if an absolute budget ever appears, provenance says whether it was derived or read.**

**AND *RELATIVE COST ACROSS GAMES* IS NOT POOLING, WHICH THE NEXT READER WILL ASSUME IT IS.** *Pooling
averages a metric across games and destroys the per-game reading.* **Comparing two games' costs keeps
both intact and reads the relation between them** — the thing the no-pooling rule exists to protect,
not the thing it forbids.

---

## Layer 7 — Persistence, recall, import

**PARTIAL.** `gamma.save(path)` / `load(path)` exist and are switchable, default cold. Terms carry
`origin` — `prior | minted | imported` — **so provenance is a field and not a convention.** `retarget`
parks unresolved residuals per level as `L{level}:{slot}`.

**ABSENT.** The structural hash, the `hash_episode_level` stack, palette-swap aliasing, cross-game
lookup.

### CROSS-GAME SCENARIO LOOKUP IS A SEPARATE BUILD FROM TERM IMPORT, AND IS NOT ABSORBED BY THE HASH

**The hash IDENTIFIES a game; the scenario lookup MATCHES A SITUATION ACROSS games.** *Different
operations, and only the first is what P7's hash machinery does.*

**THE MATCHING MECHANISM EXISTS AND IS AT THE WRONG SCOPE.** `retrieval.retrieve(library, gap)` is
**one pass over the store ordered by fit** — *"not a search: no composition, no enumeration, no closure
walked"* — **which is precisely *this obstacle is familiar, where have I seen this shape*.** What it
lacks is **what it is handed**: one `library`, one game.

**WHAT IT OWES, AND `retrieve` SUPPLIES NONE OF IT:**

- **a scenario store to search.** `fits(t, gap, in_type, out_type)` is typed over TERMS. **A stored
  play is not a term, so a scenario must present a gap-shaped face before it is searchable at all** —
  that is the build, and it is not the hash's.
- **an ordering across stores.** *Current game weighted highest; a wider search only when own
  strategies are exhausted and confidence is low.* **SEAM 7 supplies the weighting with no bare
  number** — provenance seeds the mode, performance updates it, and *open* is what a match from
  another game starts as.
- **import at low priority with provenance.** `origin: imported` is already a field. **Structural,
  and the only part already built.**

### SEAM 6 SETTLED — THE BACKUP IS AN INSTRUMENT, AND THE ROUND TRIP IS LITERAL

**`DECOMPOSITION.md:164` already defines the computation:**

    R_T  =  gap( x , (T_E . T_A)(x) )        x concrete

**Wipe is `T_A`, rebuild is `T_E`, the gap is what did not come back.** *The same form, one scale up —
and `R_T` is settled as **a reading, never a gate**, which is what turning a verdict into a
measurement restates.*

> **AND THE THING THAT MADE `R_T` TOY-SHAPED IS ABSENT AT THIS SCALE.** `_round_trip` finds the
> pre-image **by sweeping the domain** — `3.32e+13` on a 4×4, **the span overflows a float on 64×64**.
> **At ablation scale the pre-image is STORED, not searched: the backup IS the pre-image.**

**WHAT THE BACKUP BUYS, AND NONE OF IT IS PROTECTION:** *reproduction* — where and when a failure
happened, rather than only that the win did not survive; *same-shape-different-data, shown* — a cold
start collects in a different order and the backup lets that be demonstrated rather than assumed; and
*network effects, traceable* — how cold starts, presentation order and cross-game recall interact.

**TWO CONSTRAINTS ON THE INSTRUMENT:**

- **THE BACKUP IS HARNESS-SIDE AND THE AGENT NEVER READS IT.** *The seat may read the harness; the
  agent may read only the frame.* **A frame that could read its own recall gap is scoring itself with
  a quantity it produced.**
- **THE COMPARISON KEYS BY TERM CONTENT AND LINEAGE, NEVER BY ORDER.** *A cold start collects in a
  different order*, so an order-keyed comparison reads **recovered differently** as **not recovered**.
  **And the denominator is fixed by the backup being taken BEFORE the wipe** — clause 3's *back up
  first; refuse to wipe if verification failed.*

**ONE TEXT REPAIR OWED, IN A WORKING DOCUMENT.** **Clause 3 says *wipe Γ* and the store is outside Γ.**
*The substance is settled and the text is not, and the next reader wipes what the text names.*

### SEAM 7 SETTLED — THE MODE IS DERIVED, AND ITS CLOCK IS BUILT

**Provenance seeds the mode; performance updates it.** *Derived rather than assigned — the same move
as the structure hash*, and it makes **proven / believed / open computed corpus-wide**, which was the
hole the weighting sat in.

**`Standing.decay` runs on a LOGICAL clock — `rejections *= 0.5 ** (gap / REJECTION_HALFLIFE)`,
attempts and generations, no wall clock — so demotion already has a clock and a half-life**, and
`settled_at` is the promotion side. **Wiring, not invention.**

**And the confidence rule is one rule everywhere:** *proven* when it holds first-hand now, *believed*
when carried from a prior level or play, *open* when carried from a different game. **A composition
takes the weakest of its parts**, so parts can be proven while the whole is believed — **which is what
a per-locus mode composing to a board reading needs, and it needs nothing else.**

---

# THE PHASE ORDER, AND WHY

**Dependency, not cost.** *Read the SPEC of each item before ordering a phase, not the row that
summarises it.* **The order is unchanged from revision 1; the contents are not.**

    P0  RULE `dict[str, int]`            gates L1(a), L4, L5. Nothing below moves first.
                                         NARROWED by SEAM 8: side channel, not widening
    P1  bounding-box overlap (Tier 1)    unblocks ~6 containment relations by COMPOSITION
        + publish shape's frozenset      closes the erasure; the six orientation relations follow
    P2  a pair store                     write where the matrices already exist. Gives
                                         relational HISTORY and MATCH CONFIDENCE, which
                                         nothing holds today
    P3  a relational key                 `slot_types` cannot name a pair. THE build of the
                                         three -- L5's cap and Figure 3's link 2
    P4  cascade: the frame stack         L1(b)+(d). Same tracker, finer sampling. g50t only.
                                         The naming split lands HERE, before the collision bites
    P5  colour IDs + classes             L3 and L4. GB1 = SPECTRUM x TIME, frozen at placement
    P6  the budget as a gradient channel L6(a). Wiring; the REWARD/TRANSITION pattern exists
    P7  hash, stack, and the backup      L7. UNBLOCKED -- SEAM 6 settled, and the backup is
                                         now part of the deliverable rather than a hazard

**P1 through P4 are all Layer 1 and Layer 5 work: the break is there and everything below it is a
reading of nothing until it moves.**

## Where the settlements land, and the one item that is ungated

- **P0 narrowed.** The tree is a side channel; Layers 4 and 5 read it directly and **only their
  outputs become bettable.** *A smaller ruling than revision 1 posed.*
- **P4 gained the naming split** — `cascade` to the causality tracker, `transition` to the attribute
  tracker, **with `animation` retired.** *This is where the collision would have bitten.*
- **P5 gained a derivation** rather than a stipulation, and **`role` is no longer undefined**, because
  the fill carries the strategy and the band carries nothing.
- **P7 is unblocked and gained the backup as its instrument.**

> **AND ONE NEW ITEM IS UNGATED: LAYER 1(e), THE PER-LOCUS MODE.** Its detectors are built and fed;
> **its loci already have a key in `slot_owner()`; it needs neither P0's ruling nor P4's stack.** *What
> it owes is a consumer for a verdict nothing reads.* **So it can be taken at any point in the order.**

**AND THE CONTACT CLAIM IS QUALIFIED, BECAUSE UNQUALIFIED IT CONTRADICTS SEAM 8.** **(e) changes
contact by REDUCING WHAT IS TRACKED for a confirmed locus, never by selecting behaviour from the
board-level composition** — *the per-locus drive is licensed as thin I/O; the board composition remains
a finding.* **What gets changed is what is MEASURED, not what is CHOSEN.**

> **AND THE REACH CLAIM IS STATED SO IT CAN BE READ, NOT ASSERTED.** *An improvement that does not
> change contact changes nothing.* **The claim is that mass stops piling on the locus the agent is
> driving, so `_last_mass`'s focal ordering points at what the agent did NOT cause.** **That is
> checkable against the focal ordering before and after, and it should be measured** — *a contact claim
> defended by argument is the failure mode the rule was written against.*

---

# THE NINE SEAMS, SETTLED

**All nine resolved 2026-09-04. Recorded here as resolutions; the reasoning is in `INDEX.md`.**

| | seam | resolution | what it changed |
|---|---|---|---|
| **1** | the reading pattern vs §11 | **§11 never applied** — a reading order is *what to look at*, so §23.2 governs; the five non-Γ homes are populated, not entered | Layer 2 admissible; `_last_mass` is the built fallback |
| **2** | `ROYGBIV` vs Figure 13 | **`GB1` = `SPECTRUM × TIME`** — band is where, index is the ordered succession of differences. A legal matrix cell; the network supplies nothing | Layer 3 derived; `COLOUR` stays comparable-not-ordered |
| **3** | aliasing inherits by position | **`GB1` is `Item1` until filled** — the band carries no significance, the fill carries the strategy | aliasing inherits nothing on position alone |
| **4** | the lookup trigger | **one event, two thresholds** — settled change triggers, residual size filters salience | Layer 5's trigger reconciled; call volume priced |
| **5** | the learned ceiling | **discovered through play is experience; a given parameter is a seat-read** | seat constants stay unread; the ceiling is already measurable |
| **6** | the store vs clause 3 | **the store is wiped, and the backup makes the wipe MEASURABLE** — `R_T` at ablation scale | P7 unblocked; clause 3's text owes a repair |
| **7** | cross-game weighting | **provenance seeds the mode, performance updates it** | no bare number; `Standing.decay` is the clock |
| **8** | the tree the loop cannot hold | **side channel, outputs bettable** — plus the `cascade`/`transition` split and the per-locus mode | Layer 1 gained (d) and (e) |
| **9** | unflagged rulings | **`animation` is per-game** — `ls20` has none | conditions the claim, and the acceptance test |

---

# THE ACCEPTANCE TEST

**The finished build must represent everything `ARC GAMEPLAY - WHAT THE AGENT SEES.md` lays out, and
DEMONSTRATE what it left out.** *The story is the specification, and it is also the test.*

**ONE CONDITION INHERITED FROM SEAM 9, AND IT IS LOAD-BEARING.** **The story includes animation and
`ls20` has none, so the acceptance test is PER GAME.** *A build that satisfies the story on `g50t` and
shows nothing on `ls20` has **PASSED**, not failed* — **firing only where the capability is present is
the stronger verdict, because it discriminates.**

**AND ONE STEP THE SHRINK DOES NOT REACH:** *a pair has no slot, so its output has no bettable name.*
**That is P3, and it is the load-bearing one.**

---

# THE THREE OPEN ITEMS, SETTLED 2026-09-04

| item | ruling | lands |
|---|---|---|
| **mid-game colour change** | **identity permanent, placement re-numbered from the band's running maximum, change-list append-only** — and RGB stays cache-live as the grouping key | **P5**, Layer 3 |
| **the learned ceiling** | **counts durable per game; the `MAX_ACTIONS` ceiling abstained and never saved as a number** — relative-only is the proof-of-learning property | **P6/P7**, Layer 6 |
| **the mode values** | **all five built** — the absent `coupled_agency.py` is a name written before its code | **Layer 1(e)**, ungated |

**And the two prior hooks are absorbed rather than dropped:** `Affordances.bindings` remains the
conflation witness — *a key with two colours in it is a row carrying two things* — **and it is now the
same object as a two-entry change-list**; and **`COLOUR` being `COMPARABLE` not `ORDERED` is what makes
the change-list the right shape**, since *changed / to which placement* is recordable and *by how much*
is not.

---

# SEAM 10 -- SETTLED: PER-PLAY COUNTER, STAMPED WITH THE FULL `hash_episode_level`

**Option (ii), with a richer stamp than the precedent.** *The counter resets each play; every placement
carries the full `hash_episode_level` triple, both namespaces are separated, and the level component is
what preserves the dilution.*

    identity      a pointer. permanent, structural, never a colour
    placement     `<band><n>` @ `hash_episode_level`. the counter is PER PLAY, and the stamp is
                  what makes an entry readable after the counter that minted it has reset

**THE STAMP IS THE DILUTION RULE MADE ADDRESSABLE.** Layer 7: *a later level uses an earlier one, but
LOSSILY -- the earlier plays are residual the new level composes against, the way solute already in a
container is not removed when more solvent is added.* **A level component in the key is what lets prior
plays remain available AT REDUCED STRENGTH rather than being either overwritten or confused.** *Nothing
leaves; the stamp is how what stayed is still reachable.*

> **AND THE TWO STAMP FORMATS DIFFER ON PURPOSE -- DO NOT HARMONISE THEM.** `retarget` parks residuals
> as **`L{level}:{slot}`**, level only; placements carry **hash, episode AND level.** *A residual's
> lifetime ends at a LEVEL boundary; a placement's ends at an EPISODE boundary, because the palette
> swaps on reset.* **One format over two lifetimes would be `A6i`'s inverse -- a single namespace
> asserted where two exist** -- and it is the tidy-looking change a later reader is most likely to
> make.

---

# STILL OPEN

**ONE ITEM, AND IT IS A WORKSHOP RATHER THAN A RULING: `ValueLatentSelf`'s residual conjunct, and which
board-wide quantities P5 publishes into the candidate set it already searches.** *Downstream of P0-P3
and runs in parallel; it must resolve before P5, because P5 changes what the member reads.*

**CLOSED:** the three original items - the identity/placement `A6i`, by the pointer/value split -
`coupled`, as three states classified per relationship - **SEAM 10**.

**AND ONE CONSEQUENCE OF A CLOSURE IS ITSELF OPEN, RAISED AT LAYER 3:** **the pointer/value split takes
cross-play object identity away from the colour ID and nothing has been assigned it.** *The corpus
specifies the construction -- a hash of structure, not colour -- one scale up, and applying it one
scale down is a reading rather than a ruling.* **It is not a new question; it is an unassigned job.**

---

# WHAT IS ALREADY COMPLIANT, AND WORTH SAYING

**Null-not-absent** — `NOT_RESOLVED` at the sensor, propagating through `Term.apply`. **Layer 5's own
requirement, built and measured.**

**Provenance on import** — `origin: prior | minted | imported` is a field. **Figure 8's requirement,
structural.**

**Cache versus durable** — `Affordances`: *vocabulary permanent, instances transient*, dropped at
`boundary`. **Layer 3's split, already running at a different site — and now known to be the lossy
coarse-graining rather than a housekeeping convention.**

**Described, never composed** — the seat/agent line, and `slot_owner`'s *the loop may not derive
this*. **Layer 2's discipline, already the house rule.**

**The budget as a gradient** — Figure 13's *a difference that can be spent*, and `THE_FORMULA`'s two
currencies that do not add. **Layer 6's framing, corpus-confirmed.**

**The self-model family** — four hypotheses with independent failure modes, fed every step. **Layer
1(e)'s detectors, built. Only the verdict goes unread.**

**The confidence clock** — `Standing.decay` on a logical clock. **Layer 7's promotion and demotion,
built.**

**The round trip** — `round_trip_gap` / `_round_trip`, `R_T` as a reading. **Layer 7's ablation
instrument, built at slot scale and free at ablation scale.**
