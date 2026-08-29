# The adjacency graph — measured

**Derived from the recipes, no judgement anywhere.** An edge exists when one domain's recipe
names an ingredient that unambiguously belongs to another domain.

**Strict rule:** the ingredient name must exist in exactly one domain across all 2,666 entries.
Ambiguous names — `flow`, `signal`, `node`, `pressure` — **produce no edge**, because they
cannot say which domain they came from.

---

# The result

| | |
|---|---|
| nodes | **61 domains** |
| edges | **285 undirected** |
| density | **8.1%** of possible pairs |
| components | **one** — everything is reachable from everything |
| mean hop distance | **2.11** |
| longest path | **4** |

**It is sparse, it is connected, and the paths are short.** Which is the answer to the question
that was asked: **a mesh would carry no information and this is not one.**

## And it is a small-world graph, measured

| | value | random baseline | ratio |
|---|---|---|---|
| clustering coefficient | **0.271** | 0.156 | **1.7×** |
| mean path length | **2.11** | 1.84 | 1.15× |

**Clustered well above chance, with path lengths barely above chance.** That is the small-world
signature — **local neighbourhoods that hold together, and shortcuts that cross the whole graph
in two or three hops.**

**Which is exactly the structure a hop-and-traverse strategy needs.** Dense local
neighbourhoods make *what is one hop away* meaningful; short global paths make *reach into a
distant tree* cheap.

---

# Your path, checked

**`Game → Desire → Win`, expanded into the full sequence, against the measured graph:**

| hop | direct edge | shortest path |
|---|---|---|
| Ludological → Desire | no | **2** |
| Desire → Learning | no | **2** |
| Learning → Choice | no | **2** |
| Choice → Action | **yes** | 1 |
| Action → Information | no | 3 |
| Information → Dynamic | no | **2** |
| Dynamic → Social | no | **2** |
| Social → Adversarial | no | 3 |
| Adversarial → Exchange | no | **2** |
| Exchange → Curiosity | no | **2** |
| Curiosity → Connection | no | **2** |
| Connection → Skill | **yes** | 1 |
| Skill → Habit | **yes** | 1 |

**Every hop lands within one to three steps, and ten of thirteen are one or two.** The
traversal is real structure rather than free association.

**And the intermediate nodes are legible:**

```
Ludological → Exchange → Desire
Desire → Connection → Learning
Curiosity → Phenomenological → Connection
Habit → Transformation → Dynamic
Raw data → Fluid → Network → Social
Thaumaturgical → Ludological → Human
```

**`Desire → Connection → Learning`** is *wanting reaches learning through relation*, which is
not an arbitrary route. **`Habit → Transformation → Dynamic`** is *a groove reaches a system
state through what breaks it.*

---

# Hubs and leaves

## Hubs — the domains most things route through

| degree | domain |
|---|---|
| 21 | **Human** |
| 20 | **Phenomenological** |
| 20 | **Connection** |
| 19 | **Bio** |
| 17 | **Transformation** |
| 17 | **Ontological** |
| 16 | Skill |
| 15 | Habit · Automaton · Social |

**Human is the top hub and it should be** — it holds the priors everything composes from.

**Phenomenological and Connection at second is the finding.** *Intentionality, horizon, lived
body, the felt world* and *bond, relation, the interdependent web* — **two domains that a first
pass would have called soft turn out to be the connective tissue.**

**And `Phenomenological` was one hair from being cut.** Its `Qualia` entry was removed for being
the hard problem; **the rest of it is load-bearing infrastructure.**

## Leaves — the terminal domains

| degree | domain | connects only to |
|---|---|---|
| 2 | **Tabula Rasa** | Embodiment · Aquatic |
| 2 | **Electro** | Embodiment · Habit |
| 2 | **Thaumaturgical** | Ludological · Phenomenological |
| 3 | **Mechanical** | Automaton · Thermo · Human |
| 3 | **Thermo** | Adversarial · Human · Mechanical |
| 3 | **Atmospheric** | Dynamic · Human · Phenomenological |

**The physics domains are terminal.** Things bottom out in them and do not route through them —
**which is what you would expect if they are the substrate rather than the machinery.**

**And `Tabula Rasa` being a leaf is worth noticing.** It is the smallest domain, everything is
measured over it, **and almost nothing composes from it** — because raw values are what other
things are made of rather than what they are built from.

---

# The taxonomy result, and it is uncomfortable

**The six super-categories barely predict the edges.**

| | |
|---|---|
| edges within a super-category | **67** |
| edges across | **218** |
| internal share | **24%** |
| random baseline | **17%** |

**Twenty-four percent against a seventeen percent baseline.** The grouping is doing something and
**it is close to nothing** — a seven-point lift over shuffling the domains at random.

## What that means

**The super-categories group by subject matter. The recipes connect by ingredient.** Those are
different relations, and **the taxonomy is organised by the first while the composition runs on
the second.**

**Which is not a defect in either.** A reader needs subject-matter grouping to find things; **an
agent traversing to compose needs the ingredient graph**, and they are not the same structure.

**But it does mean the six super-categories are a reading aid rather than a search structure**,
and using them to guide traversal would send an agent to the wrong neighbours.

---

# What this settles about the axes

**The adjacency graph is derivable with no judgement.** No hand-tagging, no threshold, no
per-entry call — **it falls out of what the recipes already say.**

**And it answers the question the axes could not.** `Bodily / Textual` says *may this be here.*
`Arity` says *can this be expressed.* **Neither says *from here, what next* — and that is the
question a composing agent asks at every step.**

---

# CORRECTION — the fringe is mostly notation

**I reported that 80% of entries are never an ingredient and read it as a fringe.** That was the
strict rule: an ingredient counts only if it names an entry exactly and unambiguously.

**Re-measured with a defensible middle rule** — exact entry name *or* exact first word, no
truncation, tokens longer than three characters:

| | strict | middle |
|---|---|---|
| entries whose recipe names another entry | — | **78%** |
| entries used as an ingredient | **20%** | **48%** |
| directed entry edges | 1,714 | **7,375** |

**The entries were there. The recipes just did not name them in full.** A recipe writes
`Frust + Blockage` where the entry is `Frustration resp`, and `Set + Err + Action + Fdbk` where
the entries are `Setpoint`, `Error`, `Action` and `Feedback`.

**So the entry graph is four times denser than the strict count suggested**, and the fringe is
**roughly half an artifact of abbreviation.**

**Stated with its own caution:** the middle rule has false positives — `edge` matches `Edge of
chaos`, `bound` matches four different entries. **The true density is between 20% and 48% and
neither bound is the answer.** A canonical ingredient name per entry would settle it, and
nothing has one.

---

# Three edge types, not one

**The graph currently has one relation: *A is an ingredient of B*.** A traversal exposed two
more.

| edge | meaning | example |
|---|---|---|
| **ingredient** | A is a part of B | `Setpoint` → `Goal seeking` |
| **identity** | A and B are the same thing under two names | `Setpoint` ≡ `Goal` — **a hop that should cost zero** |
| **default** | B takes the outcome if A does not happen | `Commitment` ⊣ `Latency` — **an edge that fires on absence** |

**A composer traversing on ingredient edges alone misses both.** It would treat `Setpoint → Goal`
as a two-hop journey between domains when it is one object, **and it would never find `Latency`
at all**, because nothing produces it — it is what happens when nothing does.

## What it needs to be usable

**The 561 recipes with no unambiguous ingredient.** Twenty-one percent of the list contributes
no edges, either because its ingredients are ambiguous names or because the recipe is prose.
**Those are the entries an agent cannot traverse from**, and they are unevenly distributed.

**And the edge weights are counts, not distances.** `Mechanical → Human` fires ten times and
`Optical → Acoustic` fires four. **Whether a heavier edge is a shorter hop or merely a more
common one is not established** — and treating count as proximity would be a metric nobody
checked.

**Neither blocks the traversal.** Both should be stated before anything routes on it.

---

# For the NSM combination

**The primes will need to attach somewhere, and the graph says where.**

**`DO`, `MOVE` and `HAPPEN` are Action and Kinetic** — degree 10 and 11, mid-graph, well
connected to Skill, Habit and Transformation.

**`IF` is Ludological and Choice.** **`BEFORE/AFTER` and `FOR SOME TIME` are Temporal**, which
sits next to Somnial, Dynamic and Mnemonic.

**None of the six attaches to a leaf.** Every one lands in the connected middle of the graph —
**which means a routine composed from them can reach the physics domains in two or three hops
and cannot get stranded.**

**That is checkable and it just checked out**, which is a better position than the primes having
been chosen for their names.
