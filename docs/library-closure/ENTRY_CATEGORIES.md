# Entry categories — refined

**Yes, it helps, and the useful part is at the bottom rather than the top.**

## The problem with sections 1–15

**They are a second domain taxonomy over the same population.** *Perception · Physical Systems ·
Biological Systems · Cognitive Systems · Logical and Mathematical · Information · Social ·
Temporal · Philosophical · Aesthetics · Pathological · Cross-domain · Skills · Technical Arts*

**That is roughly the six super-categories again, cut slightly differently.** Fluids under
Physical Systems, memory under Core Cognitive Foundations, criticality under Cross-Domain
Dynamics — **every one of those already has a domain.**

**Two taxonomies over one population is the collision this list has been catching all along**,
and it produces the same failure: an entry filed under `2.2 Fluids` and under `Aquatic` looks
like two facts and is one.

**Plus three specific defects.** Membership is illustrative — two to five atoms named per
subcategory out of 2,694. **Sections 14 and 15 introduce entries that are not in the list at
all** — welding, soldering, debugging, choreography, group theory. And several subcategories
have no members that exist, which is a category with an empty subject.

## The part that is genuinely new

**The tags reference and the cross-category index.** Those are **orthogonal to domain**, which
is what an entry-level scheme has to be, and they are the only part of the file that adds a
dimension rather than re-cutting one.

**So: invert it.** The bottom is the taxonomy and the top is a second domain map.

---

# KIND — what sort of thing an entry is

**Eight, refined from the original ten.**

**Five of the original ten collapse.** `Process`, `Behavior`, `Function`, `Mechanism` and
`Operation` are near-synonyms — *any ongoing activity*, *any observable activity*, *any purpose
or role*, *any causal process*, *any action*. **Three survive with clear boundaries; two do not
earn a place.**

**And two are added that the original lacks, and they are the two this project uses most.**

| kind | what it is | examples |
|---|---|---|
| **PROPERTY** | a fact about how something is, that does not change under use | Cohesion · Solidity · Viscosity · Traction · Chirality |
| **OPERATION** | something done to a thing; it has a before and an after | Translate · Recolour · Merge · Compress · Encode |
| **RELATION** | how two or more things stand to each other | Contact · Containment · Support · Coupling · Adjacency |
| **STATE** | how a system currently is; it can change without anything acting | Rest · Chaos · Saturation · Equilibrium · Fatigue |
| **MECHANISM** | a thing that produces an effect, and persists across uses | Lever · Catalyst · Buffer · Ratchet · Transistor |
| **MEASURE** | a quantity or ordering read off something else | Entropy · Fluency · Elegance · λ · Coverage |
| **BIAS** | a systematic way of being wrong that feels like being right | Anchoring · Confirmation bias · Sunk cost · Similarity heuristic |
| **FAILURE MODE** | a way a system stops working, named | Learned helplessness · Overload · Rumination · Death spiral |
| **DEFAULT** | what takes the outcome when nothing else is chosen | Latency · Hesitation · Stagnation · Inertia · Drift |

## Why `DEFAULT` is a kind, and it is the one a traversal exposed

**Latency is not an operation, a state, or a failure mode.** It is **what takes the outcome when
nothing else does** — and *lost to latency* is a different event from *chose to wait.*

**The list already models it.** `Hesitation = Latency + equal alternatives + weak basis` —
*equal options, weak grounds, and time passing.*

**And it matters beyond the entry.** **An abstention that costs nothing and an abstention that
loses to the clock are different**, and the abstention discipline currently prices neither.

## Why `BIAS` and `FAILURE MODE` are separate kinds

**Neither is in the original and both are load-bearing here.**

**A bias is not a failure** — it is a heuristic with a domain where it works and a domain where
it does not. `Similarity heuristic` is how analogy works *and* how voodoo works. **Filing it as
an operation loses the fact that it can be right.**

**A failure mode is not a state** — `Fatigue` is a state a system passes through and recovers
from; `Learned helplessness` is a state it does not leave without intervention. **The
difference is whether it is self-limiting**, and that is worth a field.

## Why the five collapse

| original | goes to | why |
|---|---|---|
| `Process` | OPERATION or STATE | an ongoing activity is either something being done or a condition holding |
| `Behavior` | OPERATION | *observable activity* is an operation seen from outside |
| `Function` | MECHANISM | a purpose is what a mechanism is for |
| `Structure` | PROPERTY or RELATION | an arrangement is either a fact about one thing or a fact about several |
| `System` | — | *any system, dynamic or static* has no complement; **a tag that fits everything sorts nothing** |

**`System` is the one to name explicitly.** It was listed first in the original as the most
frequent tag — **and a tag applying to every entry partitions nothing**, which is the vacuity
problem in a taxonomy.

---

# AXES — the binary properties

**Six of the original twelve survive, and three are added.**

## Kept

| axis | what it distinguishes | why it earns a field |
|---|---|---|
| **Physical / Abstract** | does it need a substrate | decides whether a domain change breaks it |
| **Reversible / Irreversible** | can the before-state be recovered | **`Merge` is irreversible, `Abut` is not, and that is the whole distinction between them** |
| **Local / Global** | does it read one place or many | decides whether it can be computed per slot |
| **Discrete / Continuous** | can it take intermediate values | decides whether a threshold is even meaningful |
| **Deterministic / Probabilistic** | does the same input give the same output | decides whether repetition is evidence |
| **Individual / Collective** | does it need more than one agent | decides whether it is available to a solitary agent at all |

## Cut, with reasons

| cut | why |
|---|---|
| `Simple / Complex` | no stated threshold and none available; it is a judgement wearing an axis |
| `Stable / Dynamic` | this is `PROPERTY` versus `STATE`, which the kind field already draws |
| `Mental / Material` | duplicates Physical / Abstract |
| `Closed / Open` | undefined for most entries; means three different things across the sections that use it |
| `Linear / Nonlinear` | applies to a small subset and is a special case of Deterministic |
| `Normal / Pathological` | this is the `FAILURE MODE` kind, which is a better place for it |

## Added — the three this list needs and the original lacks

| axis | what it distinguishes | why |
|---|---|---|
| **Bodily / Textual** | could a body have found this, or only a document | **This is the criterion that removed 267 entries and it is not a field.** Buoyancy is bodily; entanglement is textual. Both are kept, and knowing which is which is what makes the keep defensible |
| **Arity** | one thing, two things, or many | **A relation has no slot**, so arity decides expressibility rather than difficulty — and it is the parked arity question's own subject |
| **Lifetime** | permanent vocabulary, or bound per episode | **The colour ruling in one field.** *The colour nothing else sits on* is permanent; *which colour that is* dies at the boundary |
| **Ordered / Simultaneous** | do the recipe's parts happen in sequence or together | **`+` currently means both.** `Walk = Prop + Bal + Cnt` is simultaneous; `Ascent = Negative feedback + Momentum` is sequential — **same notation, different logic, and a composer reading a recipe as a plan needs to know which** |

**`Ordered / Simultaneous` is one of seven distinctions `+` is currently carrying alone.** See
`OPERATORS.md`: **`+` appears in 2,111 recipes and every other operator combined appears in 48**,
so the notation has one symbol and seven meanings.

**It does not corrupt the adjacency graph** — *ingredient-of* holds under every operator — **but
it corrupts anything that reads a recipe as a procedure**, and `Merge` and `Abut` collapse to the
same recipe under `+`.

**`Arity` is the one that pays first.** Every entry with arity 2 or more is currently
inexpressible against the loop's signature, **and nobody can say how many that is without the
field.**

---

# The universals — corrected

**The cross-category index is right in shape and needs its members checked.**

| appears in every domain | entries |
|---|---|
| **Mathematical** | Number · Geometry · Statistics · Correlation · Variance · Distribution · Probability |
| **Physical** | Solidity · Support · Continuity · Topology · Space-time |
| **Cognitive** | Attention · Memory · Belief · Inference · Prediction |
| **Social** | Group · Trust · Reputation · Exchange · Power |
| **Temporal** | Time · Duration · Rhythm · Cycle · Becoming |

**And a sixth the original does not have**, which the three-part list surfaced:

| **Recurrent shapes** | Positive feedback · Criticality · Pattern-in-noise · Least-means-greatest-effect · Bounded region · Cause-effect delay |

**These are the six shapes already marked `[dup]` at every site.** They are not universals in the
sense the others are — **they are one shape reached independently from several directions**,
which is why they are marked rather than merged.

---

# What a fully tagged entry looks like

**Applied to four real entries, to show the scheme does work:**

| entry | domain | tier | kind | axes |
|---|---|---|---|---|
| **Cohesion** | Human | 1 | PROPERTY | Physical · Local · Deterministic · Individual · Bodily · arity 1 · permanent |
| **Merge** | Human | 3 | OPERATION | Physical · **Irreversible** · Local · Deterministic · Individual · Bodily · **arity 2** · permanent |
| **Sunk cost** | Economic | 6 | BIAS | Abstract · Local · Deterministic · Individual · Bodily · arity 1 · permanent |
| **Learned helplessness** | Psychological | 5 | FAILURE MODE | Abstract · **Irreversible without intervention** · Global · Deterministic · Individual · Bodily · arity 1 · permanent |

**Eight fields, two of which are already recorded** (domain, tier), **six of which are new.**

## A third `[dup]` kind, and it is the one that hides

**Two kinds were marked:** same quantity in two domains (`Pressure`), and **same word for two
quantities** (`Conductivity`).

**There is a third: same referent, different word, different domain.**

**`Setpoint` [Dynamic] and `Goal` [Desire] are the same object.** Cybernetic says so itself —
`Goal seeking = Setpoint + Error + Action + Feedback` — **the setpoint is the reference the
error is measured from, which is what a goal is.**

**And no grep finds it.** The other two kinds share a string. **This one shares nothing but
meaning**, which makes it the case that survives every mechanical check.

**It was found by accident**, by a traversal that was not looking for it. **How many more exist
is unknown and probably not small.**

**And the tagging is what makes the `[dup]` entries separable**, which was the reason for
restoring them: `Pressure` in Aquatic and `Pressure` in Thermo have identical kind and identical
axes and different domains — **so they are one quantity used twice.** `Conductivity` in Thermo
and in Electro differ on nothing recorded — **which is the signal that the word is doing two
jobs and the entries need renaming rather than merging.**

---

# What this still does not solve

**Nothing is tagged.** This is a scheme over 2,694 entries and **not one of them carries a kind
or an axis today.**

**And tagging by hand is the failure the list itself warns about.** 2,694 judgements made in one
sitting replaces something checkable with something tired — **the same argument that turned the
provenance field from a hand stamp into a watermark commit.**

**So the question before tagging is whether any of the six axes is derivable rather than
judged.** `Arity` is — it can be read off a recipe's operand count. **`Reversible` may be** —
an operation whose recipe includes a loss is irreversible. **`Bodily / Textual` is not**, and
that is the axis carrying the most weight, which is worth knowing before anyone starts.

**One field derivable, one probably, one certainly not.** That ratio decides whether this is a
build or a very long afternoon.
