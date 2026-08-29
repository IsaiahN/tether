# The refined path — what it adds, measured

**It improves the analysis in four ways, and one of them says my graph is built at the wrong
level.**

---

# 1 · It is measurably tighter than the first path

**Same graph, same method, both paths checked:**

| | mean hops | max |
|---|---|---|
| the first path | **2.11** | 4 |
| **the refined path** | **1.79** | **3** |
| graph average | 2.11 | 4 |

**The first path was exactly average. The refined one is better than average.**

**Which is a real result rather than a compliment.** A path articulated more carefully is
*shorter through the graph*, and that is checkable without anyone agreeing it reads better.

**The hops:**

```
Ludological → Exchange → Desire          Desire → Exchange → Dynamic → Choice
Choice → Action                          Action → Habit
Habit → Emotion → Dynamic                Dynamic → Kinetic → Learning
Learning → Skill                         Skill → Action → Choice
Curiosity → Skill → Connection           Connection → Learning
Cybernetic → Dynamic
```

**Four of fourteen are direct edges.** `Choice → Action`, `Action → Habit`, `Learning → Skill`,
`Connection → Learning` — **the spine of the loop is single hops, and the branches are two.**

---

# 2 · The nodes are entries, not domains — and my graph is one layer too coarse

**Fifteen of thirty-five nodes are not domains at all.**

Environment · Observation · Novelty · Setpoint · Frustration · Urgency · Latency · Commitment ·
Inertia · Momentum · Cascade · Feedback · Ascent · Descent · Stagnation · Reset · Witness ·
Dither · Break Habit

**Some are entries that exist:** `Novelty` [Habit] · `Latency` [Choice] · `Stalemate` [Dynamic] ·
`Cascade` [Human] · `Feedback` [Habit, Learning] · `Negative feedback` [Dynamic] · `Witness`
[Pathological] · `Dither` [Dynamic].

**So the traversal runs at entry level and the domain graph is a projection of it.**

**And the entry-level graph is buildable** — the same method finds **1,714 directed
entry-to-entry edges** with no judgement. **But only 20% of entries are ever an ingredient of
something**, which means four fifths of the list are leaves at entry level.

**That is the real limit and it is now measured:** the domain graph is dense enough to traverse;
**the entry graph is a thin spine with a very large fringe.**

**The most-used ingredients are the spine:**

| used as an ingredient | entry |
|---|---|
| 28 | `Randomness` [Aleatory] |
| 26 | `Meaning` [Phenomenological] |
| 23 | `Rule` [Automaton] |
| 19 | `Group` [Social] |
| 17 | `Trust` [Social] |
| 14 | `Resource` · `Self` · `Intent` · `Identity` · `Dream` |
| 13 | `Goal` [Desire] |

**`Meaning` at second is the same finding as Phenomenological being the second hub** — arriving
at entry level from a different direction.

---

# 3 · It is a control loop with three terminals, not a path

**And the discriminator is the sign of the feedback:**

| feedback | trajectory | terminal |
|---|---|---|
| **negative** | ascent | **WIN** |
| **positive, unchecked** | descent | **LOSE** |
| **zero, balanced** | stagnation | **STALEMATE** |

**Every component already exists, and all in one domain:**

`Negative feedback` · `Positive feedback` · `Runaway` · `Stalemate` · `Equilibrium` — **all
Dynamic, all tier 3–4.**

**So the outcome discriminator is not something to build. It is `Dynamic` read as a decision
rather than as a set of states**, and nothing in the list said so.

**And it is checkable at every step rather than only at the end.** *Which sign is the feedback
carrying right now* is a per-step reading, **which is exactly what a per-step terminal predicate
would need.**

## Why this is the most valuable thing in the refined path

**The corpus has `levels_completed` as the ground and no intermediate reading of trajectory.**
An agent knows it won when it wins.

**Three terminals discriminated by feedback sign give it a reading before the terminal
arrives** — *am I ascending, descending, or stuck* — **and all three are already named.**

---

# 4 · Two reset paths, and they are not the same reset

```
Cascade/Outcome → Learning → Skill/Novelty      → Reset
Cascade/Outcome → Learning → Witness/Dither → Break Habit → Reset to Choice/Observation
```

**The first is *I learned something, go again*.** The second is ***I did not, break the groove,
and go back further.***

**And `Dither` being the discriminator is exactly right.** *Small deliberate noise to stop the
system sticking to a false equilibrium* — **which is what you do when the loop is running and
producing nothing**, and it is the entry I flagged in Part Two as one the loop lacks.

**`Witness` beside it is the other half:** observe the loop without being in it, **which is the
only way to notice that it is looping.**

**This is the staleness question drawn as a branch.** A library is commentary on past rooms —
`Habit` is what it becomes unchecked, **and `Break Habit` is the explicit move nobody had named
until this path.**

---

# 5 · `Frustration → Urgency → Choice` is the three-channel argument as a mechanism

**Not an affect decorating a decision. Affect *driving* it.**

**Internal feedback → appraisal → urgency → the choice is made sooner and with less search.**
Which is the Embodiment/Emotion/Noetic loop producing a change in behaviour rather than a
report about a state.

**And it names a real control:** urgency is what converts an unbounded search into a bounded
one. **The loop has a budget and no urgency**, so it searches the same amount whether or not
anything is at stake.

---

# What is missing from the list, named by the path

**Fifteen nodes have no entry. Nine of those are gaps rather than synonyms.**

| missing | nearest existing | verdict |
|---|---|---|
| **Setpoint** | `Adaptive homeostasis`, `Governor` | **gap** — the reference a controller compares against has no entry |
| **Urgency** | pressure entries, all physical | **gap** — no entry for time pressure changing how much is searched |
| **Momentum** | `Inertia cont` [Habit], `The conservation` [Action] | **gap** — inertia is there, momentum as a quantity is not |
| **Ascent / Descent / Stagnation** | `Level ascend`, `Level descend`, `Stalemate` | **gap as a triple** — the pieces exist and the trajectory reading does not |
| **Reset** | `Resilience with reset`, `Reboot` [Automaton] | **partial** — reset as a state exists, reset as a move does not |
| **Break habit** | — | **gap** — and it is the second reset path's whole content |
| **Observation** | `Witness stance`, sense entries | **partial** — observing exists per modality, not as an act |
| **Environment** | `Niche`, `The lifeworld`, `Terrain` | **covered** — three good synonyms, no gap |
| **Commitment** | `Commitment act`, `Pre commitment` [Choice] | **covered** |
| **Inertia** | `Inertia cont` [Habit] | **covered** |
| **Game** | `The game itself` [Ludological] | **covered** |
| **Frustration** | `Frustration resp`, `Frustration loop` [Desire] | **covered** |
| **Info** | Info is a domain | **covered** |

**Six genuine gaps: `Setpoint`, `Urgency`, `Momentum`, the ascent/descent/stagnation triple,
`Reset` as a move, and `Break habit`.**

**Every one is on the control-loop spine**, which is the part of the path the list is thinnest
about — **and Cybernetic is degree 6, one of the smaller hubs, despite being the domain the
whole structure runs on.**

---

# What I would change in the analysis

**Build the entry graph as well as the domain graph.** The domain graph answers *which
neighbourhood*; **the entry graph answers *which ingredient*, and that is the one a composer
uses.** 1,714 edges exist and are derivable.

**Report the fringe.** 80% of entries are never an ingredient. **An agent traversing from one of
those has nowhere to go**, and that is a fact about the list rather than about the agent.

**And add the six.** They are named by a path that was not built to find gaps, **which is a
better source than a review looking for them.**
