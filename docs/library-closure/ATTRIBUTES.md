# The attribute list — parsed, refactored, and the index it supports

**2,700 atoms across 61 domains carry an attribute list. 5,076 distinct attribute names across
them.**

**After the reachability refactor: every one of the 2,700 is reachable.** The path is four tiers
and the first carries two thirds of the list.

---

# What the list is, and it is more than attributes

**Every row carries three things:** the atom, **the attributes to check**, and **a boolean
condition that confirms or denies it.**

That third column is the part the framing missed. **`Solidity` is confirmed when `overlapArea ==
0` for any two objects.** **`Support` is confirmed when `contactPoints` is empty and vertical
acceleration is downward.** **`Movement` is `position(t2) != position(t1)`.**

**So the list is not a taxonomy — it is a set of detectors.** An atom with attributes and a
condition is **something an agent can check against a board**, not something it has to be told.

**And that answers *how does an attribute get added*:** an attribute is added when a sensor
computes it, **and a sensor is worth computing when an atom's condition names it.**

---

# The reachability refactor

## The claim that was wrong

**I ruled that most atoms could never be reached because they name things a grid does not
supply** — `temperature`, `mass`, `voltage`, `ATP`.

***Temperature is not probable but it is possible — turn an object from grey to red.***

**A scalar is a scalar.** Every one of those is **an ordinal magnitude an object carries**, and an
ordinal magnitude shows as a palette band or an extent — **the same shape as `colour`, which the
loop already has.**

**The line is not physical-versus-abstract. It is *measurable from outside* versus *reportable
only from inside*.**

## What was genuinely unrepresentable — one family, 75 mentions

**`selfReport` and its variants.** 48 as `selfReport`, 13 as `report`, and a dozen one-off forms:
`agentReport`, `curiosityReport`, `heavinessReport`, `dizzinessReport`, `dreamReport`.

**74 atoms named one. Not one is orphaned by dropping it:**

| atom | drops | keeps |
|---|---|---|
| `Valence` | `selfReport` | `physiologicalSignals` |
| `Flow State` | `selfReport` | `timeDistortion`, `taskPerformance` |
| `Mindfulness` | `selfReport` | `attentionFocus`, `ruminationLevel` |
| `Insight` | `selfReport` | `problemSolving`, `reactionTime` |
| `Awe` | `selfReport` | `physiologicalResponse`, `scale` |
| `Reputation` | `peerReports` | `observations` |

**The list's authors reached for *ask it* when *watch it* was already in the same row.**

## The encodings, after the refactor

| encoding | mentions | what it is |
|---|---|---|
| **SCALAR** | 4,983 | an ordinal magnitude the object carries — a palette band or an extent |
| **TEMPORAL** | 741 | a difference across frames; `history()` already carries them |
| **EVENT** | 529 | what happened between two frames; sensor 9 computes it |
| **BEHAVIOURAL** | 473 | inferred from an observed action sequence, never read directly |
| **RELATION** | 455 | holds between two objects |
| **SHAPE** | 183 | the object's cell set — comparable, not orderable |
| **EXTENT · POSITION · COUNT · COLOUR** | 285 | the five the loop already has |
| **STATE** | 131 | a discrete condition; an integer with no order |
| **RULE** | 77 | a regularity over frames, not a property of an object |

**`SCALAR` at 63% is the point.** Most of the list is magnitudes, **and a magnitude is one integer
per object.**

---

# What each atom needs — the tiers, and the build order

| tier | atoms | share | cumulative | what it needs |
|---|---|---|---|---|
| **0** | 11 | 0% | 0% | **reachable today** |
| **1** | 1,749 | **65%** | **65%** | a sensor that emits an integer per object |
| **2** | 122 | 5% | 70% | the `ATTR` split — comparable versus orderable |
| **3** | 749 | 28% | 97% | objects in the loop, and the predicate residual |
| **4** | 69 | 3% | 100% | a frame-level regularity |

## Tier 1 is the cheapest thing on the board

**Not a new mechanism.** `colour` is already *one integer per object*, and a scalar is the same
shape with a different source. **The sensor emits it; `_extract` takes it; nothing else changes.**

**And it repairs a stated accident rather than installing a capability:** *the composable set was
decided by which sensors happened to return integers.* `_extract` takes the five dict keys that
are ints — **not a rule, not a decision.**

**The compliance test:** a scalar sensor is **computed from the board**, not **composed from other
sensors.** The first is perception; the second is the agent's job — **and §12.3 forbids installing
symmetry, containment, holes, counting-by-colour and alignment for exactly that reason.**

## Tier 3 has a contract change behind it

**The loop sees `slots()` and `observe()` — names and name→int.** `touching(a, b)` needs two
object dicts with cells.

**So every two-object property is blocked before the predicate residual is even askable** — and
**the constraint is the firewall: what crosses must not be the board.**

---

# The index, and where it does not yet work

## Built, and the fanout is legible

**Attribute → the atoms that name it.** A change in an attribute lights up its candidates.

| a change here | lights up |
|---|---|
| `action` | 59 atoms |
| `selfReport` | 48 — **now dropped** |
| `persistence` | 28 |
| `time` | 24 |
| `outcome` · `temperature` · `coherence` | 21 each |
| `speed` | 20 |

**205 attributes name five or more atoms.** Those are the ones a signal can usefully trigger on.

## And the problem, measured

**3,963 of 5,076 attributes name exactly one atom.** **78% of the vocabulary is per-atom prose
rather than a shared index.**

**Which breaks the intersection, which is the whole mechanism.** *Colour changed and position
changed, so these ten atoms are candidates* — **measured on the raw vocabulary, `colour` ∩
`position` returns zero.** Not because no atom involves both, **because the two were spelled
differently in every row that has both.**

## The seventeen clusters are the fix, and they are ruled

**See `ATTRIBUTE_CLUSTERS.md` and `.json`.** Three passes — form variants and head words are
mechanical; **only the semantic clustering needed a ruling.**

**ACTION · SPEED · SIGNAL · TIME · FORCE · CHANGE · EXTENT · STRUCTURE · STATE · CONTACT ·
DIRECTION · COUNT · POSITION · SHAPE · MOTION · IDENTITY · COLOUR** — **1,736 mentions, 22%.**

**With `SPEED` absorbing velocity, `DIRECTION` split out as its own, and `delta` ruled into
`CHANGE`** — a position delta is motion and a temperature delta is not, **and the head word cannot
tell them apart.**

**686 head words remain unassigned, carrying most of the rest.** The next sixty clusters reach
roughly 78%, **which is the ceiling of what head-word grouping can do** — stated as a limit rather
than a target.

---

# Two things the list establishes beyond the attributes

## The conditions are §15.3's missing fourth key

**Effect shape — *what changed, not what caused it*** — is unbuilt and has four consumers.

**Every row of this list supplies one.** *`overlapArea == 0`* is an effect shape. *`position(t2)
!= position(t1)`* is an effect shape. **They are written as prose and they are the quantity.**

**Which reframes the missing key from a design problem to a parse.**

## The polling question answers itself

**A sensor is priced.** §12.3 gives each a cost; §12.1 runs them per slot per frame; **a sensor
that costs more than the residual it explains is refused.**

**So the polling interval is the bargain applied to observation** — a reading, not a constant, and
**there is no number to pick.**

---

# The open question the list does not answer

**Nothing here says how an attribute comes to exist for an agent that has not been told.**

**The list says which attributes each atom depends on.** It does not say **how a board becomes
`position` and `colour` and `extent`** — that is perception, and it produces five.

**§12.4's trigger is the specified answer and it is not built:** *when two objects have the same
attribute vector and different residuals, compose a new attribute from existing sensors to tell
them apart.* **Its own example is `holes(shape)`.**

**So the mechanism exists as a spec, and it is gated on tiers 1 through 3.** A trigger that
composes from sensors needs the sensors reachable first.
