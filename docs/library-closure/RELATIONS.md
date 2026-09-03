# The relation vocabulary

**What two objects can be to each other, what one can do to another, and which of it a bounded
agent can currently read.**

Every row is marked. **`P`** the agent perceives it today. **`C`** it is composable from what the
agent has. **`—`** neither: no sensor produces it and nothing composes to it.

**Counts and markings were revised twice.** After `_overlap` was read, six relations moved from
composable to blocked. **After the type audit, the third blocker stopped being a ruling** — `shape`
publishes a lossy stand-in for a structural quantity it already computes.

**The three blockers named in Part 6 are different kinds of thing:** a missing sensor, a missing
consumer, and an erasure. **None is a decision to revisit**, which is a change from what this
document said.

---

# Part 1 — Static relations: where two things are

## 1.1 Contact and its absence

The base partition. Every pair of objects is in exactly one of these at any instant.

| relation | condition | status |
|---|---|---|
| **disjoint** | no points in common | **C** — the negation of contact |
| **touching** | boundaries meet, interiors do not | **P** — `touching(a,b)`, the one published relation |
| **intersecting** | interiors cross | **C** — needs overlap |
| **overlapping** | share a region of nonzero area | **—** and not for the reason first recorded, see below |
| **coincident** | occupy exactly the same region | **—** same blocker as overlapping |

**Contact subdivides by dimension**, and the subdivision carries information the boolean does not:

| kind | on a grid | what it affords |
|---|---|---|
| **point contact** | corner to corner | pivoting; minimal constraint |
| **edge contact** | one cell face shared | sliding along; one axis constrained |
| **face contact** | a run of shared faces | pushing; two axes constrained |

**A grid makes these countable** — the number of shared cell-faces is an integer, **and the agent
has no atom that returns it.**

### What `overlap` actually computes, and why it is not the route to containment

**It was recorded here as *computed inside perception, never crosses*, implying a one-line publish.
That was wrong on both counts.**

**`_overlap` is intersection-over-union across two objects' *normalised* shapes.** It measures
**congruence — whether two things are the same shape — and carries no spatial information at all.**
Publishing it would say nothing about where anything is.

**And the version that would help does not exist.** Cell-level overlap between two distinct tracked
objects is **identically zero under solidity** — two objects cannot occupy the same cell — so a
cell-IoU is a constant and publishing it yields another silent instrument.

**What containment needs is bounding-box overlap, and nothing computes it.** A different sensor, not
a missing line.

**And `overlap` is an `A6i`:** the tracker's `overlap` is board cells across frames; the sensor's is
normalised shapes in one frame. **Same word, two subjects, and the sensor is never called.**

## 1.2 Containment

| relation | condition | status |
|---|---|---|
| **contained** | one interior lies wholly inside another | **—** needs bounding boxes, which nothing computes |
| **strictly contained** | inside, not touching the boundary | **—** downstream of contained |
| **internally tangent** | inside and touching the boundary | **—** downstream of contained |
| **contains** | the inverse | **—** the same test, arguments swapped |
| **nested** | containment in layers | **—** containment, transitively |

**Containment is `§12.3`'s named Tier 2 example, forbidden to install.** *The agent should have to
reach for it, because reaching is the only evidence the composition system works.*

**And the library agrees:** `Contain = To + So` — topology plus solidity, **both of which the agent
holds.** So the route is composition.

**But the composition needs an input nothing produces.** The recorded route was
`overlap(A,B) == area(B)`; **that route is closed**, for the reason set out in 1.1. **Containment
and everything under it move from composable to blocked**, and the blocker is a missing
bounding-box sensor rather than an unpublished one.

## 1.3 Alignment and orientation

| relation | condition | status |
|---|---|---|
| **collinear** | centres or edges on one line | **C** — from position |
| **aligned** | reference features share a direction or coordinate | **C** — equality on one axis |
| **parallel** | matching directions, need not meet | **C** on a grid: same row-extent or column-extent |
| **perpendicular** | directions meet at a right angle | **C** — one extends in row, the other in column |
| **concentric** | shared centre, different size | **C** — equal centroid, unequal extent |
| **offset** | a fixed separation maintained | **C** — constant delta between positions |
| **symmetric** | one is the other under reflection, rotation or translation | **—** needs the offset frozenset, which is computed and unpublished |
| **congruent** | same shape and size, after moving | **C** — equal shape ids, the one relation the label can carry |
| **similar** | same shape, different size | **—** the same erasure, under scaling |

**Alignment is `§12.3`'s other named Tier 2 example.** Same ruling, same route.

**And the honest note: nine of these are one comparison over attributes the agent already
publishes.** Position, extent, shape id. **What is missing is not the data but any term that
compares two objects' attributes** — which is `RELATE`, built, typed, and reaching nothing.

## 1.4 Visibility

| relation | condition | status |
|---|---|---|
| **occluding** | one blocks part of another from a viewpoint | **—** |
| **adjacent** | next to, possibly sharing a boundary | **C** — contact or distance one |
| **interlocked** | cannot separate without passing through | **—** needs a motion test, not a static one |

**Occlusion is the one static relation a grid genuinely cannot express** — there is no viewpoint and
no depth. **On a layered board it becomes *drawn over*, which is `Layer = Abut + Contr partial`,
and that is composable.**

---

# Part 2 — Relative motion: how one moves with respect to another

**Every row here needs two frames.** The agent has `delta` per object, published this week, **so the
inputs exist and the comparisons do not.**

| motion | condition | status |
|---|---|---|
| **no relative motion** | deltas equal | **C** |
| **translation** | relative position changes, orientation does not | **C** — delta differs, shape id constant |
| **rotation** | relative orientation changes | **—** the same erasure, under rotation |
| **rolling** | contact maintained, no relative slip at the contact | **—** needs the rolling constraint, `v = Rω` |
| **sliding** | contact maintained, tangential relative motion | **C** — touching persists and deltas differ |
| **spinning** | rotation at the contact region | **—** |
| **orbiting** | one circles the other | **C** — distance constant, direction cycling |
| **oscillating** | relative motion reverses periodically | **C** — delta sign alternates |

**Four of eight are composable from delta and contact.** **The four that are not all need
orientation** — which is the same gap as symmetry and similarity, **and it is an erasure rather than
a limit.**

**Two quantities are computed under the name `shape` and the poorer one is published.**
`shape_of(obj)` returns the normalised offset frozenset — **structural, and comparable under a
transform.** The published slot carries an episode-local integer, **arbitrary and orderable by
nothing.**

**§12.3's sensor 5 specifies the frozenset.** So the four are blocked by a lossy stand-in **standing
where the specified sensor should be**, and publishing the specified quantity is not a new sensor.

---

# Part 3 — Constraint: what one body prevents another from doing

**This is the layer that turns geometry into gameplay.** A constraint is not a fact about a moment;
**it is a fact about which moments are reachable.**

| constraint | what it removes | on a grid |
|---|---|---|
| **fixed** | all relative motion | two cells that always move together |
| **contact** | interpenetration | solidity — a prior, already loaded |
| **distance** | separation beyond a bound | a tether or rod |
| **cable** | separation only; compression free | pull but do not push |
| **revolute** | all but one rotation | a pivot |
| **prismatic** | all but one translation | a slot or rail |
| **planar** | motion off a plane | a floor |
| **rolling** | translation and rotation independently | wheel on ground |

**None is perceivable and all are inferable**, and the inference is the same in every case: **an
action that should have changed a slot did not, repeatedly, and only in the presence of a
particular other object.**

**Which is a residual with a condition attached, and it is exactly what the guard was built for** —
`When(P, R)`, where `P` names the other object's presence.

**So constraints are the first row of this document that the loop is already shaped to learn**, and
the thing it lacks is `P`: a predicate over two objects.

---

# Part 4 — Interaction: what one does to another

## 4.1 Contact forces

| force | direction | detectable as |
|---|---|---|
| **normal** | perpendicular to the contact | a blocked move |
| **friction, static** | tangential, prevents slip | a move that fails while touching |
| **friction, kinetic** | tangential, during slip | motion slower than the action commands |
| **rolling resistance** | opposes rolling | — |
| **tension** | pull along a connector | two objects moving together at a distance |
| **compression** | push along a support | one object moving because another did |
| **spring** | proportional to displacement | delta proportional to separation |
| **damping** | opposes relative velocity | delta decaying over frames |
| **impact** | large, brief | a single-frame delta far above the usual |

**Every right-hand column is a pattern over `delta` and `touching` across frames.** **None needs a
force model.** *A struck thing moves; an unstruck one does not* is already the library's definition
of `Collide = So + Ca`.

**Which is the general shape: a force is not observed, it is the name for a regularity in
deltas.**

## 4.2 Field interactions, and why they matter here

| interaction | contact required | on a grid |
|---|---|---|
| **gravity** | no | a persistent delta in one direction absent support |
| **electric, magnetic** | no | attraction or repulsion by distance |
| **buoyancy** | no, mediated | a delta against the gravitational one under a condition |
| **radiation, thermal** | no | a value changing with proximity |

**These are the relations a contact-gated sensorium cannot see at all** — and they are the ones the
board most plausibly uses. **A button that opens a door across the room is a field interaction in
this sense: an effect at a distance with no contact between cause and effect.**

**Which is `triggers_remote`, declared in the seven affordances and never written, for exactly this
reason.** `Affordances.note` iterates touching partners and continues when there are none — **and a
remote trigger has no touching partner at the remote end.** `terminates` fails identically.

**So the affordance alphabet is five of seven, and the two missing are structural rather than
contingent.** `profile()` returns unknown for both, forever, **and nothing distinguishes that from
*not yet observed*** — which is `unreached` against `unreachable`, one layer below where the corpus
invented the pair.

## 4.3 Collision, as a sequence

**A collision is not a state, it is an ordered five-step process**, and each step is separately
observable:

| step | observable |
|---|---|
| **approach** | distance decreasing |
| **contact** | touching becomes true |
| **compression** | shapes deform, or deltas go to zero |
| **exchange** | momentum transfers: one delta drops, another rises |
| **separate or stick** | touching becomes false, or both deltas match thereafter |

**And the outcome types are distinguishable by one number** — the ratio of separation speed to
approach speed:

| collision | ratio | after |
|---|---|---|
| **elastic** | 1 | both move, energy preserved |
| **inelastic** | between 0 and 1 | both move, some lost |
| **perfectly inelastic** | 0 | they move as one |

**All three are readable from deltas before and after contact.** **None needs mass or energy.**

---

# Part 5 — Non-rigid interaction

**The rigid-body idealisation fails in exactly the cases a puzzle board finds interesting.**

| behaviour | what breaks | on a grid |
|---|---|---|
| **deformation** | shape is not invariant under motion | shape id changes while the object persists |
| **fragmentation** | one object becomes several | one component becomes two — `Separate = Decompose + Co` |
| **merging** | several become one | two components become one — `Merge`, and the seam is gone |
| **accretion** | one grows by absorbing another | extent increases as another's disappears |
| **erosion** | one shrinks without an absorber | extent decreases, nothing gains |
| **flow** | no fixed shape at all | a region that changes shape and conserves area |
| **phase change** | the kind changes at a threshold | `Melt`, `Freeze`, `Boil` — one formula, three substances |

**And this is where the identity question bites.** *Is this the same object, changed, or a different
object?* **Rigid bodies never raise it. Deforming ones raise it constantly**, and the tracker's
`shape_of` is what answers it — **which is why shape is used for tracking and cannot be bet on.**

**`Merge` and `Abut` differ only by whether the originals persist**, and that distinction took a
ruling to establish. **It is the same distinction as elastic versus perfectly inelastic**, one
layer up.

---

# Part 6 — What this measures

## The count, corrected

| | count |
|---|---|
| **perceived today** | **1** — `touching`, published as a binding-list ordering |
| **composable from what the agent holds** | ~24 |
| **blocked, and each blocker named below** | ~21 |
| **constraints and forces**, inferable as delta patterns | ~24 |

**One relation published, out of roughly seventy.**

**The composable figure fell from about thirty when `overlap` was checked.** Containment,
intersection, coincidence, nesting and internal tangency were counted as composable on a route that
turned out to be closed. **That is six moved from one column to another by reading one function.**

## Three blockers, and they are different kinds of thing

**One is a missing sensor.** Bounding-box overlap is not computed anywhere. **Containment and its
five dependents wait on it**, and it is a build rather than a publish.

**One is a missing consumer.** Nothing compares two objects' attributes. `RELATE` is built and typed
— `same`, `other`, `above` — **and its output is a truth the transition bargain cannot price.** So
alignment, concentricity, congruence, collinearity and every ordering relation are **one consumer
away and unreachable.** Measured: 476 candidates offered, none beat the incumbent, the closest 25.9
bits worse — **because they are not bets.**

**And one is an erasure, which this document previously recorded as a ruling.** Two quantities are
computed under the name `shape`. **`shape_of(obj)` returns the normalised offset frozenset — §12.3's
sensor 5 as specified.** The published slot carries an episode-local integer instead.

**So *shape is a label, arbitrary and never orderable* is true of what is published and false of
what is available.** Rotation, symmetry, similarity, rolling, spinning and interlocking **were never
blocked by an accounting decision** — they are blocked by the richer quantity being computed every
frame and discarded.

**Which makes it a build and not a decision to revisit**, and the smallest of the three: **no new
sensor, no entry rule, no exemption.**

### And it is one of three erasures with the same shape

**Found by three unrelated routes, and stated together they say where to look for a fourth.**

| computed | published | found by |
|---|---|---|
| the frame stack, up to nine per response | one frame, `frame[-1]` | reading the ARC schema |
| the component list, `FRAME → [OBJ]` | one object, typed `OBJECT` | asking why nothing can count |
| the offset frozenset, `shape_of(obj)` | an episode-local integer | the deliberate type audit |

**The richer quantity is produced, the poorer one is published, and one type name covers both.**

**Which is why each looked like a limit rather than a loss.** A single frame, a single object and a
label **are each a coherent thing to have** — nothing downstream fails, and the absence of the richer
quantity is invisible from the name.

## The absent library terms split three ways, not two

**This document previously listed eighteen geometric terms as absent from the library and read the
whole list as a gap. It is three categories, and only one of them is.**

| category | terms | status |
|---|---|---|
| **dropped by the medium** | `occlude` | correct. A 2D grid has no viewpoint and no depth, so there is no referent |
| **blocked by an erasure** | `spin` · `interlock` · `symmetry` · `similarity` · `rotation` · `rolling` | **previously recorded here as a ruling with a price, and it is not one.** Ninety-degree rotation survives the compression fine, and the structural quantity is computed every frame — **the published stand-in is what removed these** |
| **absent from the library** | `disjoint` · `intersect` · `adjacent` · `align` · `nest` · `concentric` · `collinear` · `perpendicular` · `congruent` · `offset` · `tangent` | the actual gap. All survive compression cleanly |

**The middle category is the finding, and it is smaller than recorded.** It was filed as *a decision
with a price* — **the only one of the three anyone could act on by revisiting a choice.** There is no
choice: the specified sensor is computed and a lossy stand-in is published in its place.

**So it is the only one of the three that is a build**, and the same erasure blocks the orientation
relations in Part 2 — **one cause, two sites, and neither is an accounting cost.**

**And `perpendicular` sits across the line:** dropped in its three-dimensional sense, composable on
a grid. **One word, two relations, and the compression took only one of them.**

## Why the medium decides the vocabulary

**The list is not arbitrary and its gaps are not all oversights.** A gridworld is three-dimensional
physics rendered to cells, and **what survives is what remains legible from the compressed form
alone.**

| survives | dies |
|---|---|
| rotation at ninety degrees | rotation at an arbitrary angle |
| discrete delta | continuous velocity |
| layering — *what is drawn over what* | occlusion — there is no viewpoint |
| *heavier resists more*, as a delta pattern | mass as a quantity |
| contact, containment, adjacency | depth, coplanarity, skewness |

**Which is why `Layer` is in the library and `occlude` is not.** The grid kept the relation that
compresses and dropped the one that needs a camera. **That is the medium deciding, not an
omission.**

**And it gives the minimum viable set a derivation rather than a measurement.** *Which relations
does a 2D grid admit* is a property of the medium, **answerable now, and it bounds the vocabulary
from above.** Measure what the agent reached against that ceiling; **the gap between them is the
finding, and neither number alone is one.**

**This extends Figure 11 rather than restating it.** *Capability is a property of agent-and-habitat,
never of the agent alone* is stated about capability. **The same holds of vocabulary: the right atom
set is a fact about what the habitat can present.**

## What a thin reading costs, measured

**The agent's search is undirected. That is the correct policy when the target configuration is
invisible** — you cannot aim at what you cannot perceive, so sampling is the best available move,
and it stops being best the moment the relation becomes readable.

**But sampling requires a reading, and the reading is one relation of about seventy.** The agent
arrives in configurations and **notices almost nothing about them.**

**And it is not currently sampling either.** Measured over 998 steps: **one action taken 954 times
on one board and 881 of 998 on another.** The policy locks onto a single action rather than
exploring — a greedy selection with no tie-break — **so the configurations are not being visited in
the first place.**

**Two failures stacked, and they are separable.** Widening the reading does nothing while the search
visits one configuration repeatedly; **fixing the search does nothing while the reading is a
thirtieth built.**

## What the relation graph would add, and does not exist

**This document lists relations. It does not say which composes from which.**

**`Contain = To + So`. `Abut = Contact + So`. `Layer = Abut + Contr partial`.** Those are edges, and
the library's recipes already carry some of them.

**A graph over them would give the dependency depth** — how many composition steps from `touching`
to each unreached relation. **Which is a number nobody has**, and it would rank the composable set
by distance rather than listing it flat.

**It reads over recipes already on disk**, and is the same shape as the adjacency graph already
built for the atom library.
