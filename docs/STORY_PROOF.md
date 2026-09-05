# Does the build plan produce the story?

**Beat by beat against `library-closure/ARC GAMEPLAY - WHAT THE AGENT SEES.md` (79 lines, the restored
original), section-checked against the code as it stands 2026-09-04.**

    PRODUCED/B   a BUILT mechanism produces this beat -- named
    PRODUCED/P   a PLANNED mechanism produces it -- named, with its phase
    CHANGED      produced differently than the story tells it -- how
    MISSING      no mechanism produces it

**`PRODUCED/B` and `PRODUCED/P` are split on purpose.** *A beat marked produced by a mechanism that
turns out unbuilt is a `MISSING` wearing a `PRODUCED` label* — **so "planned" carries its phase, and a
plan with no phase is `MISSING`, not `PRODUCED`.** That distinction is what found four of the five gaps
below.

---

## VERDICT

**FIVE `MISSING`. The plan does not yet produce the story, and 8/8 phases would not change that.**

| | beat | why |
|---|---|---|
| **M1** | **the reading pattern** (¶7–11) | Layer 2 is settled as admissible and **appears in no phase, P0–P7** |
| **M2** | **"predicts five presses"** (¶45) | needs multi-step planning. `ledger.STEPS` has **no PLAN step** and **no phase creates one** |
| **M3** | **cross-game scenario search** (¶69) | described at Layer 7, **absent from P7's row**, and `grep` finds no scenario store |
| **M4** | **the band** (¶17, ¶21) | the frame publishes **colour INDICES**; nothing produces a spectral position |
| **M5** | **the per-locus mode** (¶27, ¶45–47) | settled and **ungated — and ungated is not the same as scheduled.** No phase number |

**M1, M3 and M5 are the same defect: a mechanism described at its layer and never carried into the
phase order.** *The phase table lists what the build does; three settled mechanisms are not in it.*
**M2 and M4 are different — those are mechanisms nothing anywhere produces.**

---

# BEFORE THE FIRST MOVE

**¶5 · "A frame arrives. Not a picture, a tree… a structure of objects, each a node."**
**`PRODUCED/B`** — `arc_percept.components`, flood-fill into connected same-symbol regions, one dict per
object with `cells · colour · row · col · h · w`. **And `arc_percept:20` refuses the obvious shortcut:**
*"NO BACKGROUND COLOUR. Every same-symbol region is a component, INCLUDING colour 0… it costs slots and
refuses an assumption."*

**¶5 · "Something watches the tree the way a `MutationObserver` watches a page… noticing what changed."**
**`PRODUCED/B`, in three places** — `delta_of` per object, `_advertised` for the action set, `_present`
for the slot set. **`CHANGED` in one respect:** *it re-reads the whole frame and computes the diff*
rather than being notified. **Same output, and the story's "not re-reading the whole thing" is not what
happens.**

**¶5 · "a node moved, a shape changed, a node vanished."**
**`PRODUCED/B` for moved and vanished** — `Objects.__call__` tracks by maximum overlap with a `shape_of`
fallback, and **death only on evidence**. **`CHANGED` for *a shape changed*:** shape is published as a
per-episode ID, so a change is visible as *a different label*, **never as what changed** — until P1.

**¶7–9 · The F-pattern, recomputed every frame, described and never composed.**

> **`MISSING` — M1.** `slots()` returns `sorted(self._decomposed())`: **alphabetical, stable, arbitrary,
> not perceptual.** *Seam 1 settled that it is admissible — §23.2 governs it, §11 never applied — and
> then no phase took it.* **P0–P7 contains no Layer 2 work.**

**The fallback exists and the pattern does not.** `_last_mass` orders by **maximum unexplained mass**,
running today, licensed as routing. *So the agent has an order that is earned and no order that is
perceptual.*

**¶11 · "under a budget the first bet is the one that gets made."**
**`CHANGED`** — **the loop bets on every slot each step, not on the first.** *Ordering is load-bearing
for the story's reason only once the budget gates action, which is P6.* **Today the claim's premise is
absent, not its mechanism.**

---

# NAMING THE COLORS

**¶15 · "the color itself is disposable… what matters is that cyan is different from the others."**
**`PRODUCED/P`, P5** — the cache/durable split. **And the shape is already running at another site:**
`Affordances` — *"drop the bindings, keep the table. **Vocabulary permanent, instances transient.**"*

**¶15, ¶21 · "it does not write down `RGB(0,255,255)`" / "it checks the RGB against everything named."**

> **`CHANGED`, AND IT IS NOT A SMALL ONE: THERE IS NO RGB.** `arc_world:74` describes the frame as ***"a
> stack of 2-D grids of **colour indices** mod {palette}."*** **The agent sees an integer, not a hue.**

**¶17, ¶21 · "cyan lands between green and blue… its name is `GB1`" / "it too falls between green and
blue."**

> **`MISSING` — M4, AND IT IS THE ONE THAT COSTS A DERIVATION.** **Placing an index on `ROYGBIV` needs
> an index→hue mapping, and that mapping is in the renderer, not in the frame.** *Reading it would be a
> seat-read; deriving it from an index is not possible, because an index carries no spectral content.*
>
> **`SPECTRUM × TIME` survives only in its `TIME` half.** *The encounter counter is real and shared and
> monotone; **the band has no producer.*** **Two rounds of derivation rest on the half that does not
> resolve.**

**AND THE MECHANISM SURVIVES ANYWAY, WHICH IS WHY THIS IS A GAP AND NOT A COLLAPSE.** *The band's job was
to decide where a new colour lands so a strategy could be inherited. **The pointer/value split already
took that job away** — a strategy is reachable by `obj:` structure, not by band.* **So what M4 costs is
the placement's spectral meaning, not the aliasing.**

**¶19 · "`GB1` is not a rank… the anchor I file this object's strategy under."**
**`CHANGED`, twice.** *It is a **placement**, not an identity* — a value another object can hold later —
**and nothing is filed under it.** *Strategy files under `obj:` = the shape frozenset.* **The story's
`GB1` is doing two jobs the deliberation split apart.**

**¶19 · "a brand-new hue landing in the same spot can alias into `GB1`."**
**`CHANGED`** — **aliasing is by structure, not by spot.** *Filing by hue is the contamination the hash
rule forbids, and it does not stop being contamination one level down.*

---

# GROUPING WHAT IT NAMED

**¶25 · "Everything `GB1` is one group."**
**`PRODUCED/P`, P5.** *Today `slot_owner()` groups slots into objects and nothing groups objects into
classes.*

**¶25 · "some square, some L-shaped, some turned different ways… shape and orientation subdivide."**
**`PRODUCED/P`, P1 — and the corpus confirms the mechanism rather than the plan asserting it.**
`RELATIONS.md:335`: *"blocked by an erasure | spin · interlock · **symmetry · similarity · rotation** ·
rolling | **previously recorded here as a ruling with a price, and it is not one.** Ninety-degree
rotation survives the compression fine… **the published stand-in is what removed these**."* **So
publishing the frozenset unblocks orientation.** *`RELATIONS.md:356` bounds it: ninety degrees, not an
arbitrary angle.*

**¶27 · "Do the `GB1` squares all move together, or does each respond on its own?"**

> **`MISSING` — M5.** **This is `coupled-rigid` versus `independent`, settled at Layer 1(e) with both
> discriminators available** — *same action* from the per-locus contingency, *same displacement* from
> `delta_of`'s `(drow, dcol)`. **And Layer 1(e) has no phase.** *It is recorded as ungated, which says it
> needs nothing — not that anything will do it.*

**¶29 · "the full attribute set, null where it can't be read — null, not absent."**
**`PRODUCED/B`** — `NOT_RESOLVED` at the sensor **and** propagating through `Term.apply`. **Layer 5's own
requirement, met before it was asked for.**

---

# WHAT IT HOLDS, SPLIT TWO WAYS

**¶33–35 · cache versus durable.**
**`PRODUCED/B` in shape, `PRODUCED/P` in content, P5.** `Affordances.boundary()` drops per-episode
bindings today. **`CHANGED`: the raw value is not merely kept to tell two blues apart — it is the
grouping key the placement runs over all play**, which is why it cannot be dropped at naming.

---

# THE FIRST DECISION

**¶39 · "which atoms are candidates, which recipes apply."**
**`PRODUCED/B`** — `retrieval.retrieve(self.gamma.library, gap)` at `tether.py:676`, *"one pass over the
library, ordered by fit… not a search: no composition, no enumeration, no closure walked."*

**¶39 · "given these attributes and changes."**
**`CHANGED`** — **the key is the characterised RESIDUAL, not the changes.** *Settled: change is the
trigger, residual size is the salience filter — one event, two thresholds.* **The story names the
trigger and not the filter.**

**¶41 · "sizes the bet against a budget it doesn't fully know… the real one it learns from cache."**
**`CHANGED`, and the change is deliberate.** **The ceiling is ABSTAINED — never saved as a number.**
*Counts are durable per game; the absolute is withheld, because knowing only relative cost is what makes
the learning provable.* **`PRODUCED/P`, P6 for the gradient wiring** — `spend()` is wired at
`arc_holdout:120`; **`exhausted()` appears only in `arc_check`, not in the agent's loop.**

---

# MOVING, AND BEING SURPRISED

**¶45 · "It predicts five presses left to reach `x1,y1`."**

> **`MISSING` — M2, AND IT IS THE LARGEST.** **`ledger.STEPS = ("PERCEIVE", "ROUTE", "MINT", "ACCEPT",
> "SETTLE", "PROMOTE", "IMPORT", "REPEAT")` — there is no PLAN step, and no phase P0–P7 creates one.**
> *A five-press prediction is a multi-step plan, and the loop bets one step ahead.*
>
> **This is Figure 3's link 4, and the chain is measured broken at link 2.** *So M2 is not a scheduling
> oversight the way M1, M3 and M5 are — it is downstream of the break, and it cannot be scheduled ahead
> of the relational key.* **But the story requires it, so the plan does not yet produce the story.**

**¶45 · "it inspects the animation between the before-frame and the after."**
**`PRODUCED/P`, P4** — **and this is the `cascade`, one of two names that replaced *animation*.**
*Today `board()` returns `self._frame.frame[-1]`: the loop never receives the intermediate frames.*
**Measured: `g50t` carries 7 or 9 frames on 39% of responses; `ls20` carries one, always** — so this
beat is **per-game, and on `ls20` it is unavailable permanently rather than pending.**

**¶45 · "The board is ice. It updates: on this surface one press means slide-until-stop."**
**`PRODUCED/P`, P4 then minting.** *Minting from a residual is built; the evidence it would mint from is
the cascade.* **`CHANGED`: the gap that triggers it is not the five-versus-one count (M2) but the
transition residual.**

**¶47 · "something blocks the path… it names the blocker and the condition."**
**`PRODUCED/P`, P1 + P3.** *`RELATIONS.md` marks ~30 relations composable from what the agent holds,
blocked by two things: `overlap` computes shape congruence rather than spatial overlap, and `slot_types`
has no entry for a relation.* **Naming a blocker needs a relation with a bettable name, which is P3 —
the load-bearing phase.**

**¶47 · "turn from pass-through to solid mid-move."**
**`PRODUCED/P`, P4 + Layer 1(e).** *A mid-play property change is exactly a mode transition, filed as a
causal event.* **Inherits M5.**

---

# THE GAME IS LOST

**¶51 · "Game over. Everything stays in cache."**
**`PRODUCED/B`** — `boundary()` drops per-episode bindings; `retarget` parks unresolved residuals per
level as `L{level}:{slot}`.

**¶53 · "the colors have swapped… aliases them onto the old IDs in place."**
**`PRODUCED/P`, P5 — `CHANGED` in what carries it.** *The object is recognised by `shape_of`'s
normalised frozenset — **"position-independent… identity under translation as well as under
recolour"** — and the new placement is appended to its change-list.* **The old ID is not what makes it
reachable; the structure is.**

**¶53 · "filing under structure rather than under hue."**
**`PRODUCED/P`, P1.** **The story already had this right, and the build has the key computed every frame
and erased at publication** — *`sid = self._shapes.setdefault(shape, len(self._shapes))`, "**a LABEL,
exactly like `colour`**… valid only for the episode it was assigned in."*

---

# WHERE THIS PLAY GOES WHEN IT ENDS

**¶57 · "computes a hash from the game's own structure… the opposite of reading an ID."**
**`PRODUCED/P`, P7.** **The story's reason is the corpus's reason and both are right**, and the plan
carries it: *filing by hue is the contamination the hash rule forbids.*

**¶59 · "checks the hash prefix against the library, then the cache."**
**`PRODUCED/P`, P7** — including the prefix-collision check, which the `obj:` key reuses one scale down.

**¶61 · "`eec40c6_2_1`, `eec40c6_3_1`… decisions, what worked, the transformations and deltas per object
and per action."**
**`PRODUCED/P`, P7 for the stack; `PRODUCED/B` for the contents** — `delta_of` per object and
`contingency()` per action are both computed today. *What is missing is the store, not the data.*

**¶63 · "level two uses level one, but lossily… the old plays are residual the new level composes
against."**
**`PRODUCED/B` in part** — `retarget` already parks per level and `outstanding` is monotone-by-addition,
which is the dilution rule as a data structure. **`PRODUCED/P`, P7 + Seam 10** for the stamped
placement that makes a prior level's entries readable rather than overwritten.

---

# COMING BACK, AND LOOKING ACROSS GAMES

**¶67 · "Leave, play other games, return, and it recognizes this one."**
**`PRODUCED/P`, P7.** *`gamma.save`/`load` exist and are switchable, default cold; the hash is what keys
them.*

**¶69 · "It searches every game's stored scenarios, its current game weighing highest."**

> **`MISSING` — M3.** **`retrieve` is called once, at `tether.py:676`, with `self.gamma.library`: one
> library, one game.** *And `grep` for a scenario store returns nothing.* **P7's row reads "hash, stack,
> and the backup" — the scenario store is described at Layer 7 and is in no phase.**
>
> **And it owes something a term store cannot give it:** `fits(t, gap, in_type, out_type)` is typed over
> **TERMS**. *A stored play is not a term, so **a scenario must present a gap-shaped face before it is
> searchable at all.***

**¶69 · "imports that as a low-priority test, marked with the game and hash it came from."**
**`PRODUCED/B` for the marking** — `origin: prior | minted | imported` is a field, not a convention.
**`PRODUCED/P` for the weighting** — provenance seeds the mode, performance updates it, and
`Standing.decay` is the clock. **The import is the only part of ¶69 that is not missing.**

---

# WHAT THE STORY LEFT OUT

**Isaiah's standing requirement, and the old story has none of these.** *They are the cases this
deliberation added, and each is a beat the rewrite must carry.*

- **a game that switches mode mid-level** — an avatar going inert, or a control surface becoming live.
  **The demotion IS the switch detection**, and the trajectory records it as a causal event.
- **a colour that changes mid-game and is logged in place** — the identity survives, the placement is
  re-numbered from the band's running maximum, the change-list appends.
- **two objects that move as one body versus two that merely move on the same action** —
  `coupled-rigid` against `independent`, and `coupled-loose` between them, ordinal on `MIN_REPEAT`.
- **a cross-game import of a familiar shape of situation** — at low priority, `open`, with provenance.

**And two the deliberation added that Isaiah did not list, which the rewrite also carries:**

- **an abstention** — *unreachable with the library as it stands*, which is the alignment claim and the
  thing the whole architecture exists to make sayable.
- **a null that is not an absence** — an attribute the instrument could not read, travelling as
  `NOT_RESOLVED` rather than becoming a wrong value.

---

# WHAT THIS COSTS THE PHASE ORDER

**Per the instruction — *if anything is `MISSING`, that is the next build item, ahead of the phase it
would have fallen in*:**

    M1  the reading pattern         Layer 2. UNGATED -- needs nothing from P0-P7. Takeable first
    M5  the per-locus mode          Layer 1(e). UNGATED -- detectors built, verdict unread
    M4  the band                    a QUESTION before it is an item: does the frame carry hue at
                                    all, or only an index? If only an index, the band has no
                                    producer and Layer 3 is `TIME` alone
    M3  the scenario store          belongs at P7. The gap-shaped face is the build, not the store
    M2  the multi-step plan         Figure 3's link 4. DOWNSTREAM OF THE BREAK -- cannot be
                                    scheduled ahead of P3, and the story needs it

> **M1 AND M5 ARE THE TWO THAT MOVE.** *Both are ungated, both have their inputs built, and both were
> lost the same way — settled at their layer, never carried into the table.* **That is the phase table
> failing as a checklist, not the plan failing as a design**, and it is `A6i`'s cousin: *a mechanism
> present and a capability absent, three times out of five.*

**M4 is not a build item until it is a question answered.** *The wrapper publishes indices. Whether the
environment exposes anything more is yours to say, and I have not looked* — **and if it does not, the
`SPECTRUM` half of `GB1` has no producer and the story's colour beats need rewriting rather than
building.**
