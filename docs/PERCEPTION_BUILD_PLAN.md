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

**(b) The prediction-outcome gap already exists and the cascade half does not.** *Predicted five
presses, one sufficed* requires reading the frames between — **which is Layer 1(b), and it is now the
same case as an embodied locus behaving differently than commanded.** *Self-tracking-as-prediction,
seen from the action side.*

> **SEAM 5 SETTLED: DISCOVERING A BOUND THROUGH PLAY IS EXPERIENCE; READING A GIVEN PARAMETER IS A
> SEAT-READ.** *The same line as the hash — computed versus handed.* **`PER_LEVEL` and `MAX_ACTIONS`
> stay seat-side and unread by the agent.**

**AND THE LEARNED CEILING IS ALREADY IN THE LEDGER.** *The death point is `by` summing to the act
count* — **~131 acts on `g50t`, ~152 on `ls20`, measured.** *A reading over data already recorded
rather than a new instrument.*

---

## Layer 7 — Persistence, recall, import

**PARTIAL.** `gamma.save(path)` / `load(path)` exist and are switchable, default cold. Terms carry
`origin` — `prior | minted | imported` — **so provenance is a field and not a convention.** `retarget`
parks unresolved residuals per level as `L{level}:{slot}`.

**ABSENT.** The structural hash, the `hash_episode_level` stack, palette-swap aliasing, cross-game
lookup.

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
> it owes is a consumer for a verdict nothing reads.* **So it can be taken at any point in the order,
> and it is the cheapest contact-changing item in the set** — because it is the difference between the
> agent measuring contingency and the agent concluding from it.

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

# STILL OPEN

- **The mid-game colour-change attribute.** *Two hooks exist before anything is designed:*
  **`Affordances.bindings` is the detector in embryo** — *"a key with two colours in it is a row
  carrying two things"* — and **`COLOUR` is `COMPARABLE` not `ORDERED`, so the record can be
  *changed / to which ID*, never *by how much*.**
- **Whether the learned-ceiling abstention persists a summary to the library.**
- **`coupled bodies` is NAMED AND UNBUILT.** §16.2 names the value and `coupled_agency.py` does not
  exist in this repo. **An item, not a question.**

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
