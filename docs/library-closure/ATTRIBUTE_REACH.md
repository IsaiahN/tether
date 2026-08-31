# Every atom is reachable — the refactor, and what it costs

**You were right and my *not achievable* was wrong.** It was a claim about the attribute list's
wording, stated as a claim about what a grid can represent.

**After the refactor: 2,700 of 2,700 atoms are reachable.** Zero exceptions.

---

# The argument that fixed it

***Temperature is not probable but it is possible — turn an object from grey to red.***

**A scalar is a scalar.** Temperature, mass, health, voltage, energy, ATP, pressure — **every one
is an ordinal magnitude an object carries**, and an ordinal magnitude shows as a palette band or
an extent. **The same shape as colour, which the loop already has.**

**What cannot be shown is a state only the entity can report.** *Faith* and *belief-as-felt* have
no pixel.

**So the line is not *physical versus abstract*. It is *measurable from outside versus reportable
only from inside*.**

---

# What was actually unrepresentable — 75 mentions of one family

**`selfReport` and its variants.** 48 as `selfReport`, 13 as `report`, and a dozen one-off forms:
`agentReport`, `curiosityReport`, `heavinessReport`, `dizzinessReport`, `dreamReport`.

**74 atoms named one. Every one of them keeps its other attributes:**

| atom | drops | keeps |
|---|---|---|
| `Valence` | `selfReport` | `physiologicalSignals` |
| `Flow State` | `selfReport` | `timeDistortion`, `taskPerformance` |
| `Mindfulness` | `selfReport` | `attentionFocus`, `ruminationLevel` |
| `Insight` | `selfReport` | `problemSolving`, `reactionTime` |
| `Awe` | `selfReport` | `physiologicalResponse`, `scale` |
| `Reputation` | `peerReports` | `observations` |

**Zero atoms are orphaned by the drop.** Every one already carried an observable alternative —
**the self-report was a convenience, not the only route.**

**Which is the finding: the list's authors reached for *ask it* when *watch it* was already in
the same row.**

---

# The refactored classification

**Every attribute now carries how it is expressed and what that requires.**

| encoding | mentions | what it is |
|---|---|---|
| **SCALAR** | 4,983 | an ordinal magnitude the object carries — a palette band or an extent |
| **TEMPORAL** | 741 | a difference across frames; `history()` already carries them |
| **EVENT** | 529 | what happened between two frames; sensor 9 computes it |
| **BEHAVIOURAL** | 473 | inferred from an observed action sequence, never read directly |
| **RELATION** | 455 | holds between two objects |
| **SHAPE** | 183 | the object's cell set — comparable, not orderable |
| **EXTENT** · **POSITION** · **COUNT** · **COLOUR** | 285 | the five the loop already has |
| **STATE** | 131 | a discrete condition; an integer with no order |
| **RULE** | 77 | a regularity over frames, not a property of an object |

**`SCALAR` at 63% is the point.** Most of the list is magnitudes, **and a magnitude is one integer
per object — the same shape as `colour`.**

---

# What each atom needs, and the tiers are the build order

| tier | atoms | share | what it needs |
|---|---|---|---|
| **0** | 11 | 0% | **reachable today** |
| **1** | 1,749 | **65%** | a sensor that emits an integer per object |
| **2** | 122 | 5% | the `ATTR` split — comparable versus orderable |
| **3** | 749 | 28% | objects in the loop, and the predicate residual |
| **4** | 69 | 3% | a frame-level regularity |

**Cumulative: 65% at tier 1, 70% at tier 2, 97% at tier 3, 100% at tier 4.**

## Which reorders the buckets

**Tier 1 is two thirds of the list and it is the cheapest thing on the board.**

**It is not a new mechanism.** `colour` is already *one integer per object*, and a scalar is the
same shape with a different source. **The sensor emits it; `_extract` takes it; nothing else
changes.**

**And that was the ceiling's actual cause, in your proctor's own words:** *the composable set was
decided by which sensors happened to return integers.* **An encoding accident, not a rule** — so
adding an integer-emitting sensor is repairing an accident rather than installing a capability.

## What tier 1 must not become

**§12.3 forbids installing symmetry, containment, holes, counting-by-colour and alignment** —
*they compose from the nine, and the agent should have to reach for them, because reaching is the
only evidence the composition system works.*

**A scalar sensor is not one of those.** It is a Tier-1 observation, not a Tier-2 composition —
**and the test is whether the thing being added is computed from the board or composed from other
sensors.** The first is perception; the second is the agent's job.

---

# What I got wrong, stated

**I said *all atoms reachable is not achievable and should not be*.**

**Both halves were wrong.** It is achievable — 100% after dropping one attribute family. And it
should be, **because an atom whose attributes cannot be expressed is not a conservative exclusion,
it is dead weight in a library the agent is meant to search.**

**And the reason I got it wrong is worth recording:** I read *the attribute list says
`temperature`* as *this needs a thermometer*, **when it needs a palette band.** A claim about the
list's wording, delivered as a claim about physics.
