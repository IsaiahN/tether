# The Perception Pipeline, against what is built

**A build plan in `PERCEPTION_PIPELINE_general.md`'s form, stated against this instantiation.** Each
layer carries: **what exists today · what would change · what it depends on · what the corpus says.**

**Validated against Figures 1–13, the Operators and Symbols tables, and `THE_FORMULA`.**

> **REVISION 3, 2026-09-04 — THIS SUPERSEDES REVISIONS 1 AND 2 AND THE AMENDMENT TRAIL.** Ten seams
> and three open items are settled and folded into the layers they touch; **one item remains and it is
> a P5 gate.** *The reasoning for every settlement is in `docs/INDEX.md`; this document carries the
> decisions.*

> **WHAT DONE MEANS FOR THE WHOLE PIPELINE, BEFORE ANY PHASE IS READ.** *The build is finished when it
> **represents everything `ARC GAMEPLAY - WHAT THE AGENT SEES.md` lays out and demonstrates what it left
> out**, per game.* **The phase gates are not that test and cannot be summed into it** — *every phase
> can pass its own gate and the pipeline still not meet the story*, the same way contact does not
> aggregate over a week. **Eight greens is not done; the story is the bar.** See THE ACCEPTANCE TEST.

---

# THE STANDING CHECKS

**Seven, produced by this deliberation, each having caught something. They govern how the rest of this
document is read and how the build is written.**

**1 · SEAT-ACCESS IS NOT AGENT-EXPERIENCE.** *Before writing "the agent knows X", name the code path
the agent reads X through.* **The ledger is the worst trap because it is full of true numbers.** Caught
three times: `_last_mass`, the death-point ceiling, and the contact claim below.

**2 · A VALUE PUBLISHED AS A PER-EPISODE LABEL IS A PLACEMENT, NOT AN IDENTITY.** *Check for the
pointer/value split before publishing any new sensor.* **Proven at two sites** — the colour ID and
sensor 5's shape ID — **so it is a check, not a lesson to re-learn at a third.**

**3 · PREFER A RESIDUAL TO AN ABSENCE.** *"Nothing accounts for it" is not checkable mid-episode;
"unexplained mass remains after every contribution is priced" is.* **Caught twice in two rounds** —
`disembodied` and `ValueLatentSelf`'s second conjunct — **and §18.3 is the standing case: `has_self:
false` for 904 steps meant the detector was wrong, not that there was no self.**

**4 · A CONTACT CLAIM MUST BE READABLE, NOT ARGUED.** *An improvement that does not change contact
changes nothing* — so a claim that something changes contact names the reading that would show it.

**5 · ONE FORMAT OVER TWO LIFETIMES IS `A6i`'s INVERSE.** *A single namespace asserted where two
exist.* **It is the tidy-looking change a later reader makes**, and Seam 10 is where it would land.

**6 · A COMMENT'S CLAIM ABOUT SCOPE OR LIFETIME IS NOT THE CODE — VERIFY IT BEFORE DESIGN RESTS ON IT.**
*One verified site: `arc_percept`'s shape id, documented as episode-scoped and reset nowhere, which
three rounds of design planned around.* **Recorded at one site rather than the two the others carry,
because the colliding item is nameable — the frozenset publish is the next thing whose justification
rests on that comment.**

> **AND IT COMPLETES THE SIXTH LAW RATHER THAN ADDING TO IT.** *Assume it is already specified, and go
> look* says **read the comment**; this says **then check it.** **The two pull opposite ways and the
> pair is the instruction** — *reading sensor 6's comment would have prevented the Tier-2 error; reading
> the shape id's comment is what CAUSED the scope error.* **Neither half is safe alone.**

**7 · A SUMMARY RIDING ON VERIFIED FINDINGS INHERITS THEIR CREDIBILITY, NOT THEIR VERIFICATION.**
*A milestone is a COMPOSITION of findings, and the composition can be false while every part is true* —
so **check the sentence that assembles them, separately from the findings it assembles.**

    "the ruling got smaller"                    the channel existed; the ruling had not shrunk
    "it repairs `touching` on the way through"   it would have ACTIVATED the defect, not repaired it
    "every link is live except a payable board"  the atoms are runnable and NOT coherently reachable

**Three sites, and the remedy is none of the others** — *not the estimate bias, not check 3's
absence-as-fact, not law 6's unread comment.* **A true set of parts, a false summary, and the summary
borrowing the parts' credibility.** *The third instance was caught inside the message that produced it,
which is the test of a check worth having: it fires on itself.*

---

# Where the chain breaks today

**Measured 2026-09-03, per link.** *A reading, not a property.*

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

**The break sits at the pipeline's Layer 5** — *a thin relation vocabulary caps everything the lookup
can name*, which is the spec's own sentence and this build's measured state. **Nothing settled here
moved it.**

---

## Layer 1 — The frame as a change-tracked tree

**EXISTS.** `arc_percept.components` is a flood-fill partition into connected same-colour regions, one
dict per object with `cells · colour · row · col · h · w`. `Objects.__call__` tracks identity across
frames by **maximum overlap**, falling back to `shape_of` when overlap is zero — *an object smaller
than its own displacement has zero overlap with itself one frame later.* **Death only on evidence.**
Change detection exists in three places: `delta_of` per object, `_advertised` for the action set,
`_present` for the slot set.

### (a) The tree is flattened at the boundary — a side channel, not a widening

`observe()` returns `dict[str, int]`, so every object becomes `name.attr -> int` and the tree is gone
by the time the loop sees it. **Four erasure sites depend on the ruling: the frame stack, the component
list, the offset frozenset, and the extractor ceiling.**

**THE DIRECTION IS SETTLED: the tree enters by a SIDE CHANNEL, Layers 4 and 5 read it directly, and
only their OUTPUTS need to become bettable.** *That makes P0 a wiring decision rather than a widening
of the betting surface.*

### (b) The cascade is DROPPED, not debounced

`board()` returns `self._frame.frame[-1]` — *"the settled board is `frame[-1]`"* — **so the loop never
receives the intermediate frames at all.** *A debounce coalesces a signal it receives; a drop never
receives one.* **Same observable behaviour today, decisive difference at P4.**

**Measured: `g50t` carries 7 or 9 frames on 39% of responses; `ls20` carries one, always.** *So a
relation forming and breaking mid-cascade is invisible on one board and not the other.* **Per game,
never pooled.**

> **AND DEBOUNCE IS THE WRONG TOOL AT P4, NOT THE RIGHT ONE.** §16.3: *"A moved, **then** B reacted.
> Within-step causal order, **which the endpoint erases**."* **A debounce firing once at settle
> discards ordering — which is what `frame[-1]` already does, so debouncing the cascade would reproduce
> the drop and make P4 pointless.** *The answer is TWO CONSUMERS, which is (d).*

### (c) The full pair matrices are computed and thrown away

*The matcher computes overlap for every (new × tracked) pair and keeps one name; `contacts()` computes
every same-frame pair and drops it on `step`.* **A store keyed by pair is a record written where a
matrix already exists, not a computation.**

### (d) Two change quantities, two names, two consumers — `animation` is retired

    cascade      WITHIN-STEP. the sub-frame chain one action spurred. carries the causal
                 ORDERING the endpoint erases. CONSUMER: the causality tracker -- the WHY
    transition   ACROSS-STEP. the change between two settled boards. CONSUMER: the attribute
                 tracker -- the WHAT

**`transition` is not a new word.** `tether.py:101` declares it as a residual channel and `tether.py:535`
files `SlotResidual(s, TRANSITION, pred[s], actual, bits)` on the per-slot across-step change — *the
same quantity, already named.*

**ACCEPTANCE CONDITION ON THE NAME: ONE PRODUCER, ONE CHANNEL.** *If Layer 1 emits transitions that
never reach a `SlotResidual`, two things called transition never meet and it becomes `A6i` after all.*
**`cascade` is unclaimed.**

### (e) The per-locus mode — detectors built, verdict unread

**§16.2 rules the design, quoting `THE_MISSION`:** *is there an **avatar** my directional actions
translate, or do I act through a **click actuator** — and even that **BLENDS mid-game**, so it must be
detected **contingently per step, never used to label the game***.

**BUILT:** all four §18.3 hypotheses — `arc_self.family()` returns `TranslationSelf`, `GrowthEdgeSelf`,
`ValueLatentSelf`, `RegionToggleSelf` in table order, fed at `arc_world:290`.

> **THE GAP: THE LOOP READS THE FAMILY'S MEASUREMENTS AND NOT ITS VERDICT.** `_learned_split` consumes
> `contingency()` — `{member: {per_action, stable}}` — and **`tether.py` contains zero references to
> `selected()` or `has_self()`.** *Nobody reads which hypothesis won, or whether there is a self at
> all.* **And the family is ONE family over the WHOLE BOARD**, so no per-locus index exists.

**WHAT IT OWES:** per-locus indexing · a consumer for the verdict · composition to a board reading ·
the trajectory record.

#### The values, and the three levels they live at

    PER-LOCUS           unknown          the family found nothing here, nothing else established
                        embodied         this locus's delta correlates with my action, FIRST-HAND
                        disembodied      the family found nothing AND the board moved
                                                                            these DRIVE TRACKING

    PER-RELATIONSHIP    independent      moved this action, DIFFERENT displacements
                        coupled-rigid    moved this action, SAME displacement
                        coupled-loose    moved together consistently, not identically
                                                        a READING over per-locus data

    BOARD-LEVEL         coupled          several loci correlate together
                        hybrid           the loci DISAGREE
                                                        compositions -- NEITHER MAY GATE

**`unknown` IS `unmodeled`, AND IT IS `NOT_RESOLVED` ONE LEVEL UP.** `SelfModelFamily.unmodeled()` is
*"the completeness critic — **the whole family failing together is the signal**"*. **It never means
`disembodied`**: check 3, and §18.3 is the case.

**`disembodied` TAKES §16.2's OWN POSITIVE CONJUNCT** — *no slot correlates **but the board changes***,
acting at a distance — **and the second half is the transition residual over the slot set.**

**`coupled-loose` IS ORDINAL, AND A TRAILING WINDOW IS WHAT THIS SITE ALREADY REFUSED.**
`SelfHypothesis.stable()`: *"**ORDINAL, BECAUSE A THRESHOLD HERE WOULD MEASURE THE SAMPLE COUNT.** A
running mean changes by `(x − mean)/n`, which shrinks as `1/n` **whatever the data does** … it is a
RANKING rather than a magnitude … `MIN_REPEAT` is reused rather than a second constant invented."*
**So loose is *has the pair's co-movement ranking stopped reordering* — no new constant.** *And
`Standing.decay`'s half-life is the other of the build's two accumulation shapes: it prices a TERM
across generations, where this is a per-relationship reading inside an episode.* **Not
interchangeable.**

#### The constraints that keep it legal

- **PER-LOCUS DRIVES, AND THAT IS LICENSED.** *Thin I/O, detected contingently per step* is the one
  legitimate distinction `CLAUDE.md` allows.
- **BOARD-LEVEL COMPOSES AS A READING, NEVER AN INPUT.** *The moment it is available beforehand the
  mechanism has been handed its answer.* **`coupled` and `hybrid` are both compositions, so neither
  gates.**
- **A RECALLED TRAJECTORY PREDICTS AND NEVER GATES** — a recalled mode is `believed`, and belief yields
  to first-hand.
- **NO THRESHOLD.** *Proven-embodied the moment alignment holds first-hand; demotes when it stops* —
  **and the demotion IS the switch detection.**

**The trajectory is a record:** `EMBODIED@0 → +DISEMBODIED@k → HYBRID (current)`, transitions filed as
causal events under the level — *the same class of event as an object appearing or vanishing.*

#### One member has no locus, and it is the one that answers `ls20`

**`ValueLatentSelf`: *"a NON-SPATIAL self … **there is no self-cell to point at — the self IS the
value**."*** It tracks `_counts(board)` **keyed by colour, board-wide.**

> **So the member §18.3 added *because a translation-shaped family failed together* is the one a
> per-locus index cannot hold — on the board the family was repaired for.** *A value-latent self is a
> self with board-wide extent, so it composes to a board reading without passing through a locus.*
> **Its establishing condition and its candidate set are the one open item — a P5 gate, below.**

**DEPENDS ON.** (a) gates (c). **(d) and (e) are ungated** — (d) is a naming decision; (e)'s loci
already have a key in `slot_owner()`.

**CORPUS.** Figure 13: *a state with no structure has no magnitude.* The slot dict holds states;
`slot_types` and `slot_owner` are the structural half, domain-declared. **Figure 4 licenses the
flattening as a coarse-graining provided the loss is measured, and `R_T` is that instrument and is not
pointed here.**

---

## Layer 2 — The reading pattern

**BUILT 2026-09-04 (M1).** `ArcWorld.read_order()` returns `(order, pattern)` sorted by
`(row, col)` off the tracked objects, recomputed per frame; `slots()` returns it; `Agent._narrate_order`
files one `read_order` row per step. **It produces no atom, enters no closure, and leaves nothing
behind.**

**AND THE OLD ORDER WAS WORSE THAN "ARBITRARY", WHICH THIS PLAN SAID AND HAD BACKWARDS.**
`components()` scans the grid in raster order and `Objects` names arrivals `o0, o1, …`, **so name order
is a raster order that was correct AT BIRTH.** *It diverges two ways:* **after objects move past each
other, and — with no motion at all — the moment there are ten objects**, because `o10` sorts between
`o1` and `o2`. **Measured: 17 objects give `o0 · o1 · o10 · o11 … o2`, and `g50t` publishes 120 slots.**

**ONLY THE RASTER PATTERN IS BUILT, AND THE OTHERS ARE REFUSED WITH A REASON.** *Layer-cake, spotted
and marking need firing conditions nobody has measured* — **picking one is the invented number.** Name
order remains the fallback where geometry is unreadable.

> **§11 NEVER APPLIED.** `CLAUDE.md` 390–396: ***entering means entering Γ**; the five non-Γ homes are
> **POPULATED, not entered** … §23.2's* what to look at vs what to do *governs loading the five; §11's
> two clauses govern entry into Γ.* **A reading order is *what to look at*.**

**THE FALLBACK IS BUILT.** `_last_mass` picks the focal slot by **maximum unexplained mass** —
`outstanding` used as an ordering, **licensed as ROUTING rather than scoring.** *The existing mechanism
given a second consumer.*

**The abstraction rule is the design obligation:** *the same layout under the same conditions yields
the same ordering every time.* **F by default, the others as conditioned fallbacks, the fallback
conditions themselves consistent.**

---

## Layer 3 — Colour, identity, and placement

**DOES NOT EXIST.** `colour` is the raw palette integer, published as a durable slot value and used in
`correction_bits`. **No ID, no band, no cache/durable split.**

### `GB1` is `SPECTRUM × TIME` — a cell already in Figure 13's matrix

- **the band is `SPECTRUM`** — *where*, ordered, physically real. **A subset of a spectrum is still a
  spectrum.**
- **the index is `TIME`** — ***the ordered succession of differences***, which is what order-of-encounter
  is. **The counter is SHARED and MONOTONIC per band, which is what makes it a succession rather than a
  tally.**

**A STRUCTURE AGAINST A STATE, with no within-kind composition.** *The network supplies nothing and must
not:* `RECURSIVE_TRANSFORMATION` Part 4 — ***not from `NETWORK`, though it is often claimed***, the
construction *presupposes what it derives*; a network **exhibits** discreteness rather than **producing**
it; ***`SPECTRUM` supplies distinguishability, and distinguishability is all counting requires.***

**THERE IS NO CUT: the band was never continuous in the agent's hands.** A continuum is *a spectrum with
**no gaps required*** — **the requirement is ADDED, so the gaps were never removed.** *The agent holds
encountered colours, a countable set.*

**`above(GB1, GB2)` NEVER FORMS.** The band is ordered; **the index is arbitrary order-of-encounter, so
it is not a magnitude.** *`COLOUR` stays `COMPARABLE` and not `ORDERED`.*

### Identity is a pointer; placement is a value

    IDENTITY     A POINTER. a stable handle, assigned once, NEVER REUSED, and never a colour
    PLACEMENT    A VALUE. `<band><n>` from the band's running maximum -- a position ANOTHER
                 object can hold at another time. `GB4` highest means the next arrival is
                 placed at `GB5`, and the one after is `GB6`
    CHANGE-LIST  append-only, a standard attribute on every object: the placements it has held,
                 plus whatever rode with each change -- which step, what else moved

**The within-play pointer already exists:** `slot_owner()`'s `{s: s.rsplit(".", 1)[0]}`, domain-declared,
running today. **So the split REMOVES a responsibility from Layer 3**, which never needed to carry
identity.

**THE CHANGE-LIST IS THE MONOTONE-BY-ADDITION SHAPE FOR THE THIRD TIME** — after `outstanding` (*the
dilution rule as a data structure*) and `origin`. **Native, not imported.** *And `COLOUR` being
comparable-not-ordered is what makes it the right shape: **changed / to which placement** is recordable,
**by how much** is not.*

### Cross-play identity: two keys, different stability, and they must not merge

    obj: INTRINSIC        hash(obj["shape"])  -- the frozenset of NORMALISED offsets
                          position-free, colour-free, STABLE. BUILT, and being erased
    obj: DISAMBIGUATION   attribute profile + relations, for two objects of identical shape
                          BOARD-DEPENDENT, so it is stable only while the board is

> **CHECK 5 APPLIES: one key over two stability classes is a single namespace asserted where two
> exist.** *State them as two keys or the disambiguation half silently destabilises the intrinsic one.*

**THE INTRINSIC HALF IS BUILT AND DOCUMENTED AS IDENTITY.** `shape_of` returns `obj["shape"]` —
*"normalized means relative to the object's own top-left, so it is **POSITION-INDEPENDENT** — which is
what makes it **identity under translation as well as under recolour**."*

**WHAT DESTROYS IT IS THE PUBLICATION, and `arc_percept` writes its own diagnosis:** *"SENSOR 5,
PUBLISHED AS A **PER-EPISODE ID** … **the id is a LABEL, exactly like `colour`**: arbitrary, comparable,
never orderable, and **valid only for the episode it was assigned in**."*

> **`sid = self._shapes.setdefault(shape, len(self._shapes))` IS AN ENCOUNTER INDEX — A PLACEMENT.**
> *Check 2 at its second proven site, with the same cure.* **So `obj:` is `hash(obj["shape"])` and what
> it needs is P1's *publish shape's frozenset*, already in the order** — *cross-play identity was never
> new P7 scope; it is the shape-erasure fix seen from the identity side.*

**And filing by hue could never have carried it:** *the contamination the hash rule forbids does not
stop being contamination one level down.* **The game hash and the object hash are one law at two
scales.**

### RGB is the live grouping key, and the freeze is protected by the boundary drop

*When an object changes colour or a new one appears, placing it and deciding whether it joins an
existing group is done by comparing its actual RGB against the values already recorded.*

    cache, this play   raw RGB, keyed to the placement. THE SUBSTRATE THE PLACEMENT RUNS OVER
    durable            the identity, the change-list, and the groupings keyed to them

**SO `T_A` RUNS REPEATEDLY WITHIN A PLAY.** *What is frozen is the IDENTITY, never the placement
OPERATION* — **and the freeze is protected by the cache being dropped at `boundary`, which is also why
aliasing works next play: by then the substrate really is gone.**

**THE SPLIT IS THE COARSE-GRAINING, SO THE LOSS IS THE MECHANISM RATHER THAN THE COST.** *"Physical
continua are not found. They are what remains after detail is discarded"* — **the raw RGB is the
molecules, the band is the density**, and **a new hue aliases onto a placement precisely because the
transform already discarded what would have told them apart.** *`R_T` a third time: `T_A` is colour →
band, `T_E` is band → a colour, the gap is the raw value that cannot come back.*

**WHAT IS ALREADY THE RIGHT SHAPE.** `Affordances`: *"drop the bindings, keep the table. **Vocabulary
permanent, instances transient**"* — **the same split at a different site**, and now known to be a
coarse-graining rather than housekeeping. *`Affordances.bindings` is also the conflation witness — a key
with two colours in it is a row carrying two things — which is the same object as a two-entry
change-list.*

---

## Layer 4 — Objects, groups, subgroups

**PARTIAL.** `slot_owner()` groups slots into objects, domain-declared — *"a loop that split on `.`
would be reading domain structure."* **One level only: no grouping of objects into classes, no
subgroup.**

**WHAT WOULD CHANGE.** Classes keyed by placement; subgroups by shape and orientation within a class;
**class behaviour as data — do the members move together or individually.**

**DEPENDS ON.** Layer 3 for the class key. **And §12.4's trigger already computes something adjacent** —
*two slots with the same attribute vector and different residuals*, grouped by `(type, value)`. **Built;
it groups by attribute vector rather than by class, and the machinery is the same.**

**IT SHARES A COMPUTATION WITH LAYER 1(e).** *Do the members move together or individually* and *several
loci correlate together* **are one measurement read for two purposes** — a class, and `coupled-rigid`.

**CORPUS.** Figure 13: *network — that entities relate, and influence travels.*

---

## Layer 5 — Attributes, relations, causality

**PARTIAL, AND THIS IS THE BREAK.**

    BUILT     eight extractors (colour · row · col · h · w · drow · dcol · shape)
              NOT_RESOLVED as null-not-absent, at the sensor AND in `Term.apply`'s
              propagation -- THIS IS LAYER 5's OWN REQUIREMENT, ALREADY MET
              retrieval keyed by the characterised residual (`retrieval.py`, 3c)
    THIN      ONE relation published: `touching`, via `contacts()`
              `triggers_remote` and `terminates` declared and never written
              COUNT and AXIS declared with no producer; BOOL, RATIO, REGION produced and
              unconsumable
    ABSENT    a causality tracker distinct from the attribute tracker

**WHAT WOULD CHANGE.** The relation vocabulary is the item. `RELATIONS.md` marks **~30 relations as
composable from what the agent already holds**, blocked by **`slot_types` having no entry for a
relation, so the retrieval key can never name one.**

> **AND THE BOUNDING-BOX ROUTE IS A TIER-2 INSTALL, WHICH THIS PLAN CALLED TIER 1 — CORRECTED
> 2026-09-04.** *The claim rested on sensor 6 `overlap` being a same-frame `OBJ × OBJ` sensor computing
> the wrong quantity.* **It is not same-frame.** `sensors.py` types it `(OBJECT_BEFORE, OBJECT)` and says
> why: *"6 AND 7 ARE CROSS-FRAME BY §12.3's OWN PROSE… the repair is deferred deliberately: cross-frame
> cell IoU is what the tracker already computes, so it agrees with an existing quantity and **unlocks
> nothing**."*
>
> **The only same-frame `OBJECT × OBJECT` sensor in the nine is `touching`, and it is a BOOL.** *So a
> same-frame bounding-box relation is a TENTH SENSOR* — **forbidden, because §12.3 says containment must
> be REACHED and reaching is the only evidence the composition system works.** **P1 is the frozenset
> publish alone.**

**THE TRIGGER: ONE EVENT, TWO THRESHOLDS.** **Settled change is the TRIGGER; residual size is the
SALIENCE FILTER.** *One named the firing, the other named the ranking.* **The consequence is call
volume, priced rather than objected to:** §15.3 claims matching is *a one-pass check, not a search*, and
`R > 0` holds retrieval to one pass **per residual**.

**THE CAUSALITY TRACKER'S INPUT IS NAMED.** *`cascade` is what it consumes* — the within-step ordering —
**which is why it is a tracker distinct from the attribute tracker rather than a second reading of one
stream.** *Layer 1(e)'s mode transitions file to it, being causal events of the same class.*

**CORPUS.** §12.3's nine and the Tier-2 rule: *if it composes from the nine it should be minted, not
installed.* **Containment and alignment both compose, so both are forbidden as installs.** *What breaks
the circle legitimately is a richer Tier 1 — and `overlap` is Tier 1 and computes the wrong quantity.*

---

## Layer 6 — The action loop

**LARGELY BUILT.** Bets are per slot per action; `R = |Γ(b,a) − o′|` is the transition residual; the MDL
bargain prices candidates; `Budget` counts actions and `spend()` is wired.

**(a) The budget is not read by anything.** `exhausted()` and `Termination`'s `cap` are unwired.
**Figure 13 settles what it is: a GRADIENT — *a difference that can be spent* — not energy, which is
*directionless alone*.** `THE_FORMULA`: *the action budget prices finding out whether it holds*, **in a
currency that does not add to the description length.**

**(b) The action-scale case has TWO gates, different in kind.**

    THE GAP          predicted action count against actual. NEEDS A MULTI-STEP PLAN, and there
                     is no PLAN step in `ledger.STEPS`. Gated on LINK 4, not on P4
    THE MECHANISM    slid or teleported -- what property was missed. NEEDS THE CASCADE, so
                     gated on P4. `ls20` carries one frame always, so there the mechanism half
                     is UNAVAILABLE PERMANENTLY rather than pending

*It is the same case as an embodied locus behaving differently than commanded —
self-tracking-as-prediction, seen from the action side.*

### The ceiling abstention — an instrument rather than a loss

    KEPT, DURABLE   step counts, action counts, what-cost-what PER GAME. First-hand experience,
                    how bets are sized, and the recall behind `strategy X took 40 steps there`
    ABSTAINED       the single `MAX_ACTIONS` ceiling per level. NEVER SAVED AS A NUMBER

**Discovering a bound through play is experience; reading a given parameter is a seat-read** — *computed
versus handed, the same line as the hash.* **`PER_LEVEL` and `MAX_ACTIONS` stay seat-side and unread.**

**THE REASON IS NOT BOARD-SPECIFICITY.** *Keeping every count and never the ceiling leaves the agent
knowing only the **RELATIVE** action cost of games and never the absolute budget of a level* — **which
is the proof-of-learning property**, and **earning the number is categorically different from being
handed it.**

> **SAME SHAPE AS CLAUSE 3 AND SEAM 6's BACKUP: WITHHOLDING IS WHAT CREATES THE MEASUREMENT**, and it
> carries a falsifier — **if an absolute budget ever appears, provenance says whether it was derived or
> read.**

**AND *RELATIVE COST ACROSS GAMES* IS NOT POOLING**, which the next reader will assume it is. *Pooling
averages a metric across games and destroys the per-game reading; comparing two games' costs keeps both
intact.*

**THE DEATH POINT — `by` summing to the act count, ~131 on `g50t`, ~152 on `ls20` — IS A SEAT READING**,
per check 1. *Not the agent's memory.*

---

## Layer 7 — Persistence, recall, import

**PARTIAL.** `gamma.save(path)` / `load(path)` exist, switchable, default cold. Terms carry `origin` —
`prior | minted | imported` — **so provenance is a field, not a convention.** `retarget` parks unresolved
residuals per level as `L{level}:{slot}`.

**ABSENT.** The structural hash, the `hash_episode_level` stack, palette-swap aliasing, cross-game
lookup.

### The ablation backup is an instrument, and the round trip is literal

**`DECOMPOSITION.md:164` already defines the computation:**

    R_T  =  gap( x , (T_E . T_A)(x) )        x concrete

**Wipe is `T_A`, rebuild is `T_E`, the gap is what did not come back** — *the same form one scale up, and
`R_T` is settled as **a reading, never a gate**, which is what turning a verdict into a measurement
restates.*

> **THE THING THAT MADE `R_T` TOY-SHAPED IS ABSENT AT THIS SCALE.** `_round_trip` finds the pre-image
> **by sweeping the domain** — `3.32e+13` on a 4×4, **the span overflows a float on 64×64.** **At
> ablation scale the pre-image is STORED, not searched: the backup IS the pre-image.**

**WHAT IT BUYS, AND NONE OF IT IS PROTECTION:** *reproduction* — where and when a failure happened rather
than only that the win did not survive; *same-shape-different-data, shown* — a cold start collects in a
different order and the backup lets that be demonstrated; *network effects, traceable* — how cold starts,
presentation order and cross-game recall interact.

**TWO CONSTRAINTS:**

- **HARNESS-SIDE, AND THE AGENT NEVER READS IT.** *A frame that could read its own recall gap is scoring
  itself with a quantity it produced.*
- **KEYED BY TERM CONTENT AND LINEAGE, NEVER BY ORDER.** *A cold start collects in a different order*, so
  an order-keyed comparison reads **recovered differently** as **not recovered**. **The denominator is
  fixed by the backup being taken BEFORE the wipe** — clause 3's *back up first; refuse to wipe if
  verification failed.*

**ONE TEXT REPAIR OWED IN A WORKING DOCUMENT:** **clause 3 says *wipe Γ* and the store is outside Γ.**
*The next reader wipes what the text names.*

### Cross-game scenario lookup is a separate build from term import

**The hash IDENTIFIES a game; the scenario lookup MATCHES A SITUATION ACROSS games.**

**THE MATCHING MECHANISM EXISTS AT THE WRONG SCOPE.** `retrieval.retrieve(library, gap)` is *one pass
over the store ordered by fit — "not a search: no composition, no enumeration, no closure walked"* —
**which is precisely *this obstacle is familiar, where have I seen this shape*.** *What it lacks is what
it is handed: one library, one game.*

- **a scenario store to search.** `fits(t, gap, in_type, out_type)` is typed over TERMS. **A stored play
  is not a term, so a scenario must present a gap-shaped face before it is searchable at all.**
- **an ordering across stores** — *current game weighted highest; a wider search only when own strategies
  are exhausted and confidence is low.* **The mode supplies it with no bare number.**
- **import at low priority with provenance** — `origin: imported` is a field. **The only part built.**

### The mode is derived, and its clock is built

**Provenance seeds the mode; performance updates it** — *derived rather than assigned, the same move as
the structure hash*, making **proven / believed / open computed corpus-wide.**

**`Standing.decay` runs on a LOGICAL clock — `rejections *= 0.5 ** (gap / REJECTION_HALFLIFE)`, attempts
and generations, no wall clock** — and `settled_at` is the promotion side. **Wiring, not invention.**

**One rule everywhere:** *proven* when it holds first-hand now, *believed* when carried from a prior level
or play, *open* when carried from a different game. **A composition takes the weakest of its parts.**

---

# SEAM 10 — The band counter's reset semantics

**The counter advances within a play. Nothing said what it did across plays, and the change-list is
durable, so a placement written this play is read next play.**

**SETTLED: PER-PLAY COUNTER, STAMPED WITH THE FULL `hash_episode_level`.**

    identity      a pointer. permanent, structural, never a colour
    placement     `<band><n>` @ `hash_episode_level`. the counter is PER PLAY, and the stamp is
                  what makes an entry readable after the counter that minted it has reset

**THE STAMP IS THE DILUTION RULE MADE ADDRESSABLE.** Layer 7: *a later level uses an earlier one, but
LOSSILY — the earlier plays are residual the new level composes against, the way solute already in a
container is not removed when more solvent is added.* **The level component is what lets prior plays
remain available AT REDUCED STRENGTH rather than being either overwritten or confused.** *Nothing leaves;
the stamp is how what stayed is still reachable.*

> **DO NOT HARMONISE THE TWO STAMP FORMATS — CHECK 5.** `retarget` parks residuals as **`L{level}:{slot}`**,
> level only; placements carry **hash, episode AND level.** *A residual's lifetime ends at a LEVEL
> boundary; a placement's ends at an EPISODE boundary, because the palette swaps on reset.* **One format
> over two lifetimes is a single namespace asserted where two exist, and it is the tidy-looking change a
> later reader makes.**

**AND THE NAMESPACES SEPARATE FIRST.** *Under a per-play counter a fresh placement `GB1` would collide
with an existing object's identity `GB1`* — **which the pointer/value split has already closed.**

---

# THE PHASE ORDER

**Dependency, not cost.** *Read the SPEC of each item before ordering a phase, not the row that
summarises it.* **The order is unchanged across all three revisions.**

    P0  RULE `dict[str, int]`            gates L1(a), L4, L5. Nothing below moves first.
                                         NARROWED: side channel, not widening
    P1  PUBLISH shape's frozenset        closes the erasure; the six orientation relations
                                         follow -- AND IT IS `obj:` INTRINSIC IDENTITY, which
                                         is why cross-play identity is not new P7 scope.
                                         BBOX OVERLAP REMOVED: it is a TENTH SENSOR, not a
                                         Tier-1 repair -- sensor 6 is CROSS-frame
    P2  a pair store                     write where the matrices already exist. Gives
                                         relational HISTORY and MATCH CONFIDENCE
    P3  a relational key                 `slot_types` cannot name a pair. THE build of the
                                         three -- L5's cap and Figure 3's link 2
    P4  cascade: the frame stack         L1(b)+(d). TWO CONSUMERS, never a debounce. g50t only
    P5  placements + classes             L3 and L4. `SPECTRUM x TIME`, identity/placement split,
                                         `hash_episode_level` stamp.
                                         GATED ON THE `ValueLatentSelf` WORKSHOP -- below
    P6  the budget as a gradient channel L6(a). Wiring; the REWARD/TRANSITION pattern exists
    P7  hash, stack, and the backup      L7. The backup is the ablation's instrument.
                                         `obj:` DISAMBIGUATION lands here, not the intrinsic half

**P1 through P4 are Layer 1 and Layer 5 work: the break is there, and everything below it is a reading
of nothing until it moves.**

## STATUS, 2026-09-05 — WHAT IS BUILT AND WHAT THE ROW STILL OWES

    P0  side channel      BUILT.  `Ctx.obj` reassembled from the flattened state -- nothing
                          stored, because `_decomposed` publishes exactly the keys `_extract`
                          reads. The extract atoms no longer abstain
    P1  frozenset publish BUILT.  `structure` beside `shape`, resolved through the RUN-STABLE
                          shape table, verified to round-trip on replay. Unblocks congruence
                          via `overlap`; symmetry / rotation / similarity still need a REFLECT
                          or ROTATE that is not in the nine -- a Tier-2 question, unripe
    P2  pair store        NOT BUILT. No consumer: nothing reads relational history
    P3  relational key    NOT BUILT. `slot_types` publishes ZERO relation types. LINK 2 IS
                          UNMOVED, and `touching` is `OBJECT -> BOOL` reachable but the
                          `OBJECT -> OBJ` query that would enumerate it was WITHDRAWN as
                          type-incoherent (`Ctx.group` follows the SLOT, not the chain)
    P4  cascade           NOT BUILT. `board()` still returns `frame[-1]`; the causality tracker
                          that would consume `cascade` does not exist
    P5  placements        NOT BUILT, and M4 stands: the frame publishes colour INDICES, so the
                          BAND has no producer and `SPECTRUM x TIME` survives as `TIME` alone
    P6  budget gradient   AT ITS RULING. `Termination`: *the agent does not read the cap* --
                          Seam 5 -- so what remains is seat-side and is not agent capability
    P7  hash and store    BUILT to the fixture's limit. The signature is the transformation
                          trace with every environment label stripped -- action anonymous,
                          name-free, colour-free -- measured ACTION-INVARIANT across three
                          different action sequences, and plays stack `_1_1 _2_1 _3_1`.
                          The BACKUP is Seam 6's and is owed at 25/25, not now

**ALSO BUILT, OUTSIDE THE PHASE ORDER:** *M1's read order · M5's per-locus mode with per-member streak
invariants · the input adapter with its render round-trip · `operand_type` on the three relate atoms ·
`Ctx.group` and the three quantifiers · the EDGE (`objective_step`) · the POSITION/EXTENT modulus fix ·
the panel-debt gate at `summary.report`.*

**AND THE PANEL IS STALE TWICE** — the atom count moved 18 to 21, and POSITION/EXTENT re-priced from the
palette to the board. **`summary.report`'s docstring gates it.**

## The ungated item, and the contact claim stated so it can be read

> **LAYER 1(e), THE PER-LOCUS MODE, IS UNGATED.** Its detectors are built and fed; its loci already have
> a key in `slot_owner()`; **it needs neither P0's ruling nor P4's stack.** *What it owes is a consumer
> for a verdict nothing reads.*

**(e) CHANGES CONTACT BY REDUCING WHAT IS TRACKED for a confirmed locus, never by selecting behaviour
from the board-level composition.** *The per-locus drive is licensed as thin I/O; the board composition
remains a finding.* **What changes is what is MEASURED, not what is CHOSEN.**

**THE READING THAT WOULD SHOW IT — check 4:** *mass stops piling on the locus the agent is driving, so
`_last_mass`'s focal ordering points at what the agent did NOT cause.* **Checkable against the focal
ordering before and after, and it is to be measured rather than argued.**

## The `ValueLatentSelf` workshop — a P5 gate

**IT BITES EXACTLY ONE PLACE.** *The member keys its history on the raw palette integer that P5 replaces,
so if P5 lands without this settled, **the one detector that answers `ls20` breaks silently**.*

**NEARLY SETTLED — THE RESIDUAL CONJUNCT.** The condition is *input→value alignment*, where embodied has
*input→locus alignment*. **Its positive half is built:** `_attribute(action, cts[colour] − was)` is the
per-action contingency, and `has_self()` is *"consistent AND meaningful: every nonzero step one way, and
net travel of at least one unit per nonzero step."* **The second conjunct states positively as *the
value's change carries unexplained mass after every locus's contribution is priced*** — `outstanding`,
running. *Check 3.*

**THE REAL PIECE — WHICH BOARD-WIDE QUANTITIES P5 PUBLISHES INTO THE CANDIDATE SET.** *A perception
question with an entry rule, which is the legitimate way to widen Tier 1.*

> **AND THE CONSTRAINT ON P5, STATED SO NOBODY WALKS INTO IT: WIDEN THE CANDIDATE SET, NEVER NAME THE
> VALUE.** **The member SELECTS its value** — the non-background series with the highest monotonicity,
> `mono = |Σ sign(Δ)| / |nonzero|`, updated every observation — **so the agent already answers *which
> value*, and the monotonicity search IS the evidence the mechanism works.**
>
> **Naming the value for a game encodes the answer and destroys what the member exists to demonstrate.**
> *The correct fix and the fatal fix produce the same behaviour on the target game and diverge only on
> transfer* — **which is the firewall's own failure mode, one level down.**

#### THE VERIFICATION, AND IT IS NOT "DOES THE MEMBER STILL WORK"

**`ValueLatentSelf` worked BEFORE P5. It will work after P5 either way** — *naming the value also makes
it work on `ls20`* — **so a builder checking the outcome gets a green light down both roads.** *That is
`conform/lint.py`'s named silence: **witness the boundary, not the decision.*** **The decision is
whether the member fires; the boundary is the candidate set and the selection trace.**

**THREE READINGS, ALL CHEAP, AND THE GATE PASSES ONLY ON ALL THREE:**

    1  the candidate set has MORE THAN ONE member at selection time
       -- a selector over a set of one is supplying the answer with extra steps
    2  the selected value DIFFERS ACROSS GAMES
       -- per game, never pooled. one quantity winning everywhere is either a uniform
          world or a set narrowed to the answer, and the second is the likely one
    3  the selection is REVISABLE -- `best` can still move after it is first set
       -- a `best` that never moves after step 1 had one candidate

> **AND A CONTROL THAT EXAMINES NOTHING CANNOT DEMONSTRATE A CLEAN STATE.** *"Does it still work on
> `ls20`" examines nothing about HOW it works*, which is the whole of what P5 can break.

---

# THE ACCEPTANCE TEST

**The finished build must represent everything `ARC GAMEPLAY - WHAT THE AGENT SEES.md` lays out, and
DEMONSTRATE what it left out.** *The story is the specification and the test.*

**ONE CONDITION, AND IT IS LOAD-BEARING: the story includes animation and `ls20` has none, so the test
is PER GAME.** *A build that satisfies the story on `g50t` and shows nothing on `ls20` has **PASSED**,
not failed* — **firing only where the capability is present is the stronger verdict, because it
discriminates.**

**AND ONE STEP THE SHRINK DOES NOT REACH:** *a pair has no slot, so its output has no bettable name.*
**That is P3, and it is the load-bearing one.**

---

# WHAT WAS SETTLED

**Ten seams and three items, 2026-09-04. The reasoning is in `docs/INDEX.md`; the decisions are in the
layers above.**

| | resolution |
|---|---|
| **1** reading pattern vs §11 | §11 never applied; §23.2 governs. `_last_mass` is the built fallback |
| **2** `ROYGBIV` vs Figure 13 | `GB1` = `SPECTRUM × TIME`; the network supplies nothing |
| **3** aliasing by position | `GB1` is `Item1` until filled — the fill carries the strategy |
| **4** the lookup trigger | one event, two thresholds: change triggers, residual filters salience |
| **5** the learned ceiling | discovered through play is experience; a given parameter is a seat-read |
| **6** the store vs clause 3 | the store is wiped, and the backup makes the wipe MEASURABLE |
| **7** cross-game weighting | provenance seeds the mode, performance updates it |
| **8** the tree the loop can't hold | side channel, outputs bettable; plus (d) and (e) |
| **9** unflagged rulings | `animation` is per-game — `ls20` has none |
| **10** the band counter | per-play, stamped `hash_episode_level`; do not harmonise the stamps |
| **i** mid-game colour change | identity permanent, placement re-numbered, change-list append-only |
| **ii** the learned ceiling | counts durable per game; the ceiling abstained and never saved |
| **iii** the mode values | all five built, at three levels; only per-locus drives |

---

# STILL OPEN

**THREE THINGS NEED REAL BOARDS AND CANNOT BE READ ON THE FIXTURE — 2026-09-05.** *The synthetic
fixture authored both sides, so it pays nothing and it is one game:*

    the contest        does an objective ever out-predict a value bet. The mechanism records
                       the winner and the margin; 143 of 143 mint rows read `depth_exhausted`
                       and NO candidate paid, in either stream
    convergence        how fast the signature settles on a board richer than four patterns
    collision rate     how often two real games share a signature. FIVE attribute types give
                       32 patterns and one game used four, so sharing is EXPECTED rather than
                       unlikely -- the report emits the digest beside the game name so that
                       this is readable across runs

**AND ONE DESIGN QUESTION IS FILED, NOT RULED:** *`Ctx.group` follows the SLOT's attribute, so a chain
that extracts a different one compares apples to oranges.* **The second site where `Ctx` is built before
the chain runs and cannot know its runtime state** — the edge's consumed slot value was the first.
**Two is a pair; a third would make it one ruling rather than three patches.**

**AND ONE ITEM: the `ValueLatentSelf` workshop — the residual conjunct's exact form, and which board-wide
quantities P5 publishes into the candidate set the member already searches.** *It does not touch P0–P3
and does not delay the start; it must resolve before P5.*

---

# WHAT IS ALREADY COMPLIANT

**Null-not-absent** — `NOT_RESOLVED` at the sensor, propagating through `Term.apply`. **Layer 5's own
requirement, built and measured.**

**Provenance on import** — `origin: prior | minted | imported`. **Figure 8's requirement, structural.**

**Cache versus durable** — `Affordances`: *vocabulary permanent, instances transient*. **Layer 3's split
at a different site, and the lossy coarse-graining rather than housekeeping.**

**Described, never composed** — the seat/agent line, and `slot_owner`'s *the loop may not derive this*.
**Layer 2's discipline, already the house rule.**

**The budget as a gradient** — Figure 13's *a difference that can be spent*. **Layer 6's framing,
corpus-confirmed.**

**The self-model family** — four hypotheses with independent failure modes, fed every step. **Layer 1(e)'s
detectors, built. Only the verdict goes unread.**

**The accumulation shapes** — `stable()` ordinal on `MIN_REPEAT`, `Standing.decay` on a logical clock.
**Two shapes, both built, not interchangeable.**

**The intrinsic object key** — `shape_of`'s normalised frozenset, position-free and colour-free.
**Computed every frame; erased only at publication.**

**The round trip** — `round_trip_gap` / `_round_trip`, `R_T` as a reading. **Built at slot scale and free
at ablation scale.**
