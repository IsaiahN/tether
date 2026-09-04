# The Perception Pipeline, against what is built

**A build plan in `PERCEPTION_PIPELINE_general.md`'s form, stated against this instantiation.** Each
layer carries: **what exists today · what would change · what it depends on · what the corpus says.**

**Validated against Figures 1–13, the Operators and Symbols tables, and `THE_FORMULA`.** Nine seams
are raised in the last section and **none is solved here** — options are offered, judgement is not.

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
and this build's measured state.

---

## Layer 1 — The frame as a change-tracked tree

**EXISTS.** `arc_percept.components` is a flood-fill partition into connected same-colour regions,
one dict per object with `cells · colour · row · col · h · w`. `Objects.__call__` tracks identity
across frames by **maximum overlap**, falling back to `shape_of` when overlap is zero — *an object
smaller than its own displacement has zero overlap with itself one frame later.* **Death only on
evidence.** Change detection exists in three places: `delta_of` per object, `_advertised` for the
action set, `_present` for the slot set.

**WHAT CHANGES.** Three things, and the first is a ruling not a build.

**(a) The tree is flattened at the boundary.** `observe()` returns `dict[str, int]`, so every object
becomes `name.attr -> int` and the tree structure is gone by the time the loop sees it. **This is the
`dict[str, int]` ruling, open.** *Four erasure sites depend on it: the frame stack, the component
list, the offset frozenset, and the extractor ceiling.*

**(b) Animation is discarded.** `board()` returns `frame[-1]`. **Measured: `g50t` carries 7 or 9
frames on 39% of responses; `ls20` carries one, always.** *So a relation forming and breaking
mid-animation is invisible — on one board and not the other.* **Per game, never pooled.**

**(c) The full pair matrices are computed and thrown away.** *The matcher computes overlap for every
(new × tracked) pair and keeps one name; `contacts()` computes every same-frame pair and drops it on
`step`.* **A store keyed by pair is a record written where a matrix already exists, not a
computation.**

**DEPENDS ON.** (a) is the gate. (b) and (c) are buildable under either ruling.

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

**SEAM 1 — see below. This layer's admission is the plan's largest open question and it is not a
build question.**

---

## Layer 3 — Colour as order-of-encounter

**DOES NOT EXIST.** `colour` is the raw palette integer, published as a durable slot value and used
directly in `correction_bits`. **There is no ID, no band, no cache/durable split for it.**

**WHAT WOULD CHANGE.** A colour-ID table per play: first encounter in a band gets `<band>1`, the raw
value stays cache-only, the ID goes durable. **On reset with a palette swap, new hues alias onto
existing IDs by band and role.**

**WHAT IS ALREADY THE RIGHT SHAPE.** `Affordances` already runs the cache/durable split with the
rule stated: *"Drop the bindings, keep the table. **Vocabulary permanent, instances transient.**"*
**The colour-ID split is that same rule at a different site**, which is a strong argument that the
shape is native rather than imported.

**SEAMS 2 AND 3 — see below.**

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

**SEAM 4 — the lookup trigger differs from ours. See below.**

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

**(b) The prediction-outcome gap already exists and the animation half does not.** *Predicted five
presses, one sufficed* requires reading the frames between — **which is Layer 1(b).**

**SEAM 5 — "a ceiling the agent learns from cache". See below.**

---

## Layer 7 — Persistence, recall, import

**PARTIAL.** `gamma.save(path)` / `load(path)` exist and are switchable, default cold. Terms carry
`origin` — `prior | minted | imported` — **so provenance is a field and not a convention.** `retarget`
parks unresolved residuals per level as `L{level}:{slot}`.

**ABSENT.** The structural hash, the `hash_episode_level` stack, palette-swap aliasing, cross-game
lookup.

**SEAMS 6 AND 7 — the ablation clause and the weighting. See below.**

---

# THE PHASE ORDER, AND WHY

**Dependency, not cost.** *Read the SPEC of each item before ordering a phase, not the row that
summarises it.*

    P0  RULE `dict[str, int]`            gates L1(a), L4, L5. Nothing below moves first
    P1  bounding-box overlap (Tier 1)    unblocks ~6 containment relations by COMPOSITION
        + publish shape's frozenset      closes the erasure; the six orientation relations follow
    P2  a pair store                     write where the matrices already exist. Gives
                                         relational HISTORY and MATCH CONFIDENCE, which
                                         nothing holds today
    P3  a relational key                 `slot_types` cannot name a pair. THE build of the
                                         three -- L5's cap and Figure 3's link 2
    P4  the frame stack                  L1(b). Same tracker, finer sampling. g50t only
    P5  colour IDs + classes             L3 and L4. Depends on P0 for the class structure
    P6  the budget as a gradient channel L6(a). Wiring; the REWARD/TRANSITION pattern exists
    P7  hash and stack                   L7. Blocked on SEAM 6 (the ablation clause)

**P1 through P4 are all Layer 1 and Layer 5 work: the break is there and everything below it is a
reading of nothing until it moves.**

---

# THE SEAMS

**Nine. None is solved here.**

## SEAM 1 · The reading pattern fails §11's entry rule

**The rule:** *a prior enters only if the loop cannot run without it, or the agent minted a crude
version first and we are promoting it. **Never because it would help on a game.***

**The F-pattern fails both clauses.** The loop runs today with an alphabetical order. Nothing has
minted a crude read-order. **And the justification offered is that ordering is load-bearing under a
budget — which is the third clause, the forbidden one.**

**It is also a human cultural prior** — *absent in pre-literate children, emerging through
adolescence* — where §12.3's nine are admitted on *the loop cannot run without it*. **The two
justifications are different in kind.**

**Options, unjudged.** (i) Admit it as a **seat-side description** rather than an agent prior — the
seat narrates the order, the agent does not carry it, which matches *described, never composed* and
keeps §11 intact. (ii) Derive an ordering from something the loop already has — **`outstanding` per
slot is a live ordering and is already used for routing**, which would make the order earned rather
than carried. (iii) Admit it and record the entry-rule exception explicitly, so the ablation clause
knows what it cannot see.

## SEAM 2 · `ROYGBIV` under Figure 13's definition of a spectrum

**Figure 13: *spectrum — ordering, so more and less can be said*.** **The pipeline says the colour ID
is *not a rank*.**

**So the scheme uses a spectrum's POSITIONS while denying its ORDER.** Under Figure 13 that is either
a spectrum — in which case *more and less* must be sayable of two colours, and the build's
`ORDERED = (POSITION, EXTENT, DELTA)` deliberately excludes `COLOUR` — **or it is a NETWORK: a naming
scheme over adjacency, which is a different member of the six.**

**This matters beyond naming**: the erasure work established that `COLOUR` and `SHAPE` are
`COMPARABLE` and not `ORDERED`, **correctly, because a hue has no more-and-less.** *A band position
that is explicitly not a rank is consistent with that and inconsistent with calling it a spectrum.*

**Options.** (i) Call it a network placement — adjacency between named anchors — which is what it
behaves as. (ii) Keep *spectrum* and accept that the band index IS an ordering, and move `COLOUR`
into `ORDERED`. (iii) Leave both and record the divergence.

## SEAM 3 · Aliasing a new hue onto `GB1` inherits strategy by position

**The skill-map rule:** *the moment either is available beforehand the mechanism has been handed its
answer.* **Aliasing means a hue never seen inherits everything filed under a band position.**

**The pipeline's defence is that structure, not hue, is the key** — and that is a real defence.
**The question is whether *lands in the same band* is enough structure to carry a strategy**, or
whether the alias should require the groupings to match too. **The doc says *band and role*; `role`
is undefined.**

## SEAM 4 · The lookup trigger differs from §15.3's

**The pipeline:** *settled attribute change fires retrieval; the changed attributes become the key.*

**This build:** `retrieval.retrieve(gamma.library, gap)` where `gap = characterise(robs, slot, ...)`
— **keyed on the RESIDUAL, which is a prediction MISS, not any settled change.**

> **A settled change with no prediction miss produces no residual and would fire the pipeline's
> lookup and not ours.** *Those are different triggers, and the difference is whether retrieval is
> driven by surprise or by change.*

**§15.3 is explicit that its key is the characterised residual and that *matching is a one-pass
check, not a search*.** **The pipeline's trigger would fire more often and on unsurprising events.**
**Which is right is a ruling.**

## SEAM 5 · "A ceiling the agent learns from cache"

**Layer 6 says the budget's ceiling is a placeholder the agent lowers from experience.** **`PER_LEVEL`
and `MAX_ACTIONS` are seat-set, with provenance — §22.1's *humans complete a level in under 500
actions, so 1000 is the 2× honest ceiling*.**

**An agent that infers the seat's parameter from its own history is reading a seat quantity.**
*Spending the gradient is licensed; inferring its ceiling may not be.* **And `Budget.left` is already
published, so the agent could simply be told — which is a different design from learning it.**

## SEAM 6 · The hash store versus the ablation clause — the sharpest one

**Terminal condition, clause 3:** *back up Γ, verify the backup, **wipe Γ**, re-run. If the win
survives, the agent composed it.*

> **A `hash_episode_level` store is a second library that lives OUTSIDE Γ. The ablation wipes Γ. So
> the wipe would leave the store intact and the clause could not tell a composer from a lookup
> table** — which is the exact thing it exists to detect.

**Options.** (i) The store is part of Γ and is wiped with it. (ii) The store is outside Γ and the
ablation is extended to wipe both, which changes the clause. (iii) The store holds only what would
survive a wipe anyway — provenance and residual records rather than strategies — **in which case it
is a ledger and not a library, and should be named as one.**

**This one is not a preference. Clause 3 is one of five terminal conditions and this touches it
directly.**

## SEAM 7 · Cross-game weighting is an untethered number

**"The current game's own data weighs highest"** and **"low on confidence"** are both thresholds.
**Q14: one constants block, every entry carrying mode and provenance, no bare numbers.**

**And CLAUDE.md's no-pooling rule is adjacent but not the same**: pooling a *metric* across games is
forbidden; importing a *term* with provenance is Figure 8's licensed move. **The import is fine; the
weighting needs a mode.**

## SEAM 8 · The pipeline assumes a tree the loop cannot hold

**Layers 1, 4 and 5 all assume rich nodes with attribute sets, groups and relations. `observe()`
returns `dict[str, int]`.** **Every layer below Layer 1 inherits that flattening**, and P0 is the
ruling that decides whether the pipeline is implemented over a widened slot or over a side channel.

**`[I]` has already ruled the direction — structure enters by a side channel, not the betting
surface** — **and the pipeline as written does not distinguish the two.** *If the tree is a side
channel, Layers 4 and 5 read it directly and only their OUTPUTS need to become bettable.* **That
reading should be confirmed or corrected before P1.**

## SEAM 9 · Two claims the spec marks as rulings, and a third it does not

**The spec names three: the reading pattern as prior, colour's position as filing rather than
magnitude, the hash as recall.** **Correctly flagged.**

**A fourth is unflagged: *animation is first-class*.** **On `ls20` there is no animation — one frame
per response, always.** *So Layer 1(b) is a per-game capability, and a spec that states it flatly
would have a reader build it and see nothing on half the panel.* **Not a defect in the claim; a
missing condition on it.**

---

# WHAT IS ALREADY COMPLIANT, AND WORTH SAYING

**Null-not-absent** — `NOT_RESOLVED` at the sensor, propagating through `Term.apply`. **Layer 5's own
requirement, built and measured.**

**Provenance on import** — `origin: prior | minted | imported` is a field. **Figure 8's requirement,
structural.**

**Cache versus durable** — `Affordances`: *vocabulary permanent, instances transient*, dropped at
`boundary`. **Layer 3's split, already running at a different site.**

**Described, never composed** — the seat/agent line, and `slot_owner`'s *the loop may not derive
this*. **Layer 2's discipline, already the house rule.**

**The budget as a gradient** — Figure 13's *a difference that can be spent*, and `THE_FORMULA`'s two
currencies that do not add. **Layer 6's framing, corpus-confirmed.**
