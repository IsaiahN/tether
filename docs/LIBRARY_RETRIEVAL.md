# The library system — what retrieval, lookup and search DO today, and what the plan says they should

**Written 2026-09-22 at Isaiah's instruction, after `F271`–`F273`. Every claim in Part 1 is a read
of the code or a measurement with its source named. Part 2 is the specified pipeline. Part 3 is the
gap. Part 4 is what is NOT known, and it is short on purpose.**

---

# Part 1 — WHAT IT DOES TODAY

## 1.1 There are three call sites, and they are not the same mechanism

| | what it is | where |
|---|---|---|
| **`retrieve` / `_library_fit`** | the LOOKUP — one pass over the library, ordered by fit | `retrieval.py`, `tether.py:_library_fit` |
| **`enumerate_closure`** | the SEARCH — type-valid pipelines over units, shortest first, under a budget | `gamma.py:617` |
| **`_bindings`** | the OPERAND axis — which slot fills operand 0 | `tether.py:_bindings` |

**`mint` is reached only when `route` binned `MECHANISM`, i.e. after the lookup already missed
(`F234`).** So the search is the fallback, and the lookup is the thing that should prevent it.

## 1.2 THE LOOKUP NEVER CUTS — and that is by construction, not by defect

`retrieval.retrieve`'s own docstring: ***"ONE PASS over the library, ordered by fit. EVERY NAME
COMES BACK."***

`fits()` is a score out of 5:

    2 * (type in == gap in AND type out == gap out)
      + (arity == gap arity)
      + aimed          (the gap's target type is among the types that varied)
      + relational     (the term reads `touching` AND the gap saw a relation change)

**A relation is worth ONE POINT of five, and no term is ever removed from the list.** The lookup
reorders; it does not select.

## 1.3 THE SEARCH IS BOUNDED BY TWO CONSTANTS, BOTH ANCHORED ON THE TOY WORLD

    Config.budget       = 4000     bounds YIELDS from enumerate_closure
    Config.work_budget  = 15000    bounds RANKED work = yields x operand-binds x guards

`Config`'s own comment: *"`budget` bounds YIELDS and the work is yields × operand-binds, so on a
dense board the runaway `budget` cannot [bound it]"*, and `budget = 4000` is grounded in *"the
toy's depth-3 search over its few operands prices ~13,298 candidates."*

**Measured (`F258`, `ls20`, 20 cycles, 1,283 mint rows):**

    units (the library the closure walks)      48
    candidates SEEN   (closure yields)         135,257 total   ~105 per mint call
    candidates TRIED  (ranked)                 13,564,135      ~10,572 per mint call
    ratio                                      ~100x
    budget_exhausted                           67% of mint calls
    coverage (seen / space_estimate)           median 0.0

**Per board the ratio is 32× (`vc33`) to 106× (`tn36`). Per game, never pooled.**

> **THE YIELDS ARE ALREADY SMALL — ~105 PER CALL. THE ~100× IS THE OPERAND × GUARD CROSS-PRODUCT.**
> Any cut aimed at the candidate list attacks the cheap factor.

## 1.4 THE OPERAND AXIS IS THE MULTIPLIER, AND NOTHING CUTS IT

`_bindings` returns **`[None]` + EVERY OTHER SLOT**, ordered contact-first then by variance. Its
docstring is explicit: ***"ORDERING, NEVER EXCLUSION"*** — and records why: *"the version that
DROPPED operand-reading terms when R showed no dependence on another slot LOST A CLOSING TERM."*

**So binds ≈ slot count.** More attributes per object ⇒ more slots ⇒ a bigger multiplier.

**Arm L** (`TETHER_DELTA_OPERANDS`, default OFF) bounds operands to the residual's delta plus
contact partners. Measured (`F261`): the falsifier held — **no composition lost on four boards** —
but the bound **decays with the trace**, 11× at 4 cycles to 1.5× at 20, because over twenty frames
nearly everything has moved at some point.

## 1.5 WHAT THE AGENT PERCEIVES

    arc_atoms.ATTRIBUTE_TYPE      EXACTLY 8
    colour, row, col, h, w, drow, dcol, shape

    atoms declaring a relation    2 of 21   (`touching`, `touching_n`)
    relation kinds readable       1         (`touching`)

`RELATIONS.md` Part 6 counted the same from the other side: **1 perceived · ~24 composable from
what the agent holds · ~21 blocked with named blockers · ~24 constraints and forces inferable as
delta patterns**, of roughly seventy.

## 1.6 THE RELATION CHANNEL IS WIRED AT TWO SITES AND NOT AT THE THIRD

Three sites call `retrieval.characterise(..., relations=...)`:

    the failed-path catalogue      supplies relations unconditionally
    `mint`'s gap characterisation  supplies relations unconditionally
    `_library_fit` -- THE LOOKUP THAT BINDS -- gated behind arm C (`_REL_GAP`), RETIRED, default OFF

**So `rel_types` is always empty exactly where the binding is decided**, and `fits()`'s
`relational` term is always 0 there. The site's own comment says so.

## 1.7 THERE IS NO MUTATION OBSERVER IN THE LOOP

    grep -rn "import observer" --include=*.py .
    ./test_perception.py:9:import observer

**`observer.py` defines `observe`, `_mutations`, `summarise` and NOTHING IN THE AGENT PATH CALLS
ANY OF THEM.** What exists live is `arc_world.contact_changes()` — *which relation TYPES changed
this frame*, with a confidence derived from the tracker's match quality.

## 1.8 WHAT THE CLOSURE SHIPS THAT IS NOT USED

| artefact | what it holds | used by the agent |
|---|---|---|
| `ATTRIBUTE_INDEX.json` (849 KB) | attribute → candidate atoms; 5,040 distinct attributes, 3,941 naming one atom, 201 naming five or more; three indexes: **raw name, semantic cluster (17), encoding (13)** | **no** |
| `ATTRIBUTE_REACH.json` | every atom's attributes rewritten grid-expressible, with what each requires to be reachable; 2,700 atoms | **no** |
| `ADJACENCY` | 61 domains, **285 undirected edges**, ONE component, mean hop 2.11, longest path 4 — derived from recipes, no judgement | **no** |
| `COMPOSITE_REACH.md` | 585 tier-1 atoms → 2,205 composites, as a greedy set-cover curve (300 atoms → 64%) | **no** |
| `WORKING_SET.json` | roots, Set-A atoms, Set-B level-2 composites; 74% within-domain ingredients | **no** |
| `ATOM_RANKING.json` | 477 ranked atoms | **no** |
| `OPERATORS.md` | seven bonds + negation | **no** |

**Reach is PRECOMPUTED in three of these. The agent computes reach at runtime by enumerating under
a budget and estimating the space with `space_exact`.**

---

# Part 2 — HOW THE PIPELINE SHOULD WORK

## 2.1 The plan's own statement

`TRAINING_PLAN` §*The chunk → library mapping pipeline*:

    perceive a change
      -> normalize its attribute            (17 clusters, ATTRIBUTE_CLUSTERS)
      -> ATTRIBUTE_INDEX lights candidate DOMAIN|Atoms
      -> ATTRIBUTE_REACH gates on whether the sensor stack can perceive it
      -> WORKING_SET gives the entry points (61 roots, ~200 Set-A, ~200 Set-B)
      -> a recipe in ATOMS.md is the aim point, tagged with an operator (OPERATORS.md)

    composition is 61 shallow domain-local trees (74% within-domain),
    bridged by the 285-edge domain adjacency graph

## 2.2 Isaiah's cascade, and where it maps

> *attributes trigger these atoms to highlight → adjacency says all these atoms are reachable or
> likely, so they become lower-level candidates to check for or consider*

**That is the pipeline, with one refinement about which file does which narrowing:**

| step | what narrows | which artefact |
|---|---|---|
| **1 — HIGHLIGHT** | a changed attribute lights the atoms that depend on it | `ATTRIBUTE_INDEX` |
| **2 — GATE ON PERCEIVABILITY** | can this sensor stack see it at all | `ATTRIBUTE_REACH` |
| **3 — ENTRY POINTS** | where a composition starts | `WORKING_SET` |
| **4 — BRIDGE** | which domains connect, for composing ACROSS one | `ADJACENCY` (285 edges) |

**`ADJACENCY` is step 4, not step 2.** It is a DOMAIN graph — it says which of 61 domains touch,
which matters when a composition has to leave its own domain (26% of ingredients). The
*perceivability* gate is `ATTRIBUTE_REACH`, and the *likelihood* ordering is `ATOM_RANKING`.

## 2.3 The four corollaries that bind

From `TRAINING_PLAN` §*IT IS A MAPPING JOB, NOT A SEARCH* (Isaiah, 2026-09-15):

1. **Map only into the closure.** Whatever a delta maps to must be reachable in
   `docs/library-closure` and composable with `OPERATORS.md`. **Do NOT map to the agent's ~45
   gamma atoms** — those are concrete instantiations, not the map.
2. **Deltas are ATTRIBUTE CHANGES, not atoms.** The change is what lights candidate atoms.
3. **The full-attribute MutationObserver.** Every object carries the FULL attribute+relation set
   (~100, from `RELATIONS.md`/`ATTRIBUTES.md`), **initialised NULL at frame 0**, updated in real
   time from frame 1. Every frame compounds the cue + relational vector — ***"the opposite of the
   agent's current 8-attribute reading, WHICH IS WHY ITS SEARCH IS UNDIRECTED."***
4. **Attributes are DETECTORS, not a taxonomy.** Each atom carries attributes-to-check plus a
   boolean CONDITION that confirms it (`Solidity` ⟺ `overlapArea == 0`; `Movement` ⟺
   `position(t2) != position(t1)`). **An attribute CHANGE re-fires the conditions that reference
   it** — and *"an attribute is added when a sensor computes it, and a sensor is worth computing
   when an atom's condition names it."*

**Corollary 4 is the CUT.** A condition that re-fires selects; a fit score orders.

## 2.4 The runtime architecture (Isaiah, this session)

    SEED / KERNEL      the closure-derived index, frozen, never written to
    RUNTIME OVERLAY    additions and updates during play, for this agent runtime, across all games
    LEARNINGS          promoted when proven true, saved SEPARATELY

**Lookup order: `learnings → runtime → seed`, first hit wins. The seed is read-only forever.**

**Why the three layers are required and not merely tidy:** *import must be provenanced* —
convergent derivation and adopted import are **indistinguishable in the contents**, and only the
record of where each came from separates them. Three files ARE that record. It also makes the
ablation clause runnable: **wipe `learnings`, keep the seed, re-run.**

**Promotion should reuse `Standing`, not invent a confidence.** Γ already has settle/demote with
decaying `rejections`, and Isaiah's hit-rate ruling fixes what earns standing: **expressed and
failed**, never *not retrieved*. A second confidence number would be a magic number, and two that
disagree is worse than one.

---

# Part 3 — THE GAP, IN ONE TABLE

| the plan says | the code does |
|---|---|
| a change lights candidates | the closure is enumerated by type, shortest first |
| conditions re-fire and SELECT | `fits()` scores 0–5 and `retrieve` returns every name |
| ~100 attributes + relations per object | **8 attributes**, `touching` as the only relation |
| a mutation observer updates them per frame | no observer in the loop |
| reach is precomputed and looked up | reach is enumerated under a toy-world budget |
| operands come from the delta | `[None]` + **every other slot** |
| relations reach the lookup | relations reach the lookup only behind a RETIRED arm |

**And the two facts that make the ORDER matter:**

- The lookup cut attacks the candidate axis, which is **~105 per call**.
- The attribute expansion multiplies the operand axis, which is **~100×**.

> **So widening attributes BEFORE the operand axis is cut spends the index's win paying for the
> new slots.** 105 → 10 candidates is a 10× saving; 8 → ~100 attributes is ~12× more slots. Net:
> a wash. **Cut the operand axis, or replace enumeration with lookup entirely, before widening.**

---

# Part 4 — WHAT IS NOT KNOWN

**These are unmeasured. Nothing above depends on them, and nothing should be built on a guess
about them.**

1. **What `by_cluster` and `by_encoding` actually map to.** The counts read
   `ACTION=202 … COLOUR=8` (17 clusters) and 13 encodings with 3 entries each — **I have not
   verified whether those values are ATOMS, ATTRIBUTE NAMES, or metadata.** A census of the wrong
   population is the error that cost the most tonight; this one is unresolved on purpose.
2. **Whether an encoding-keyed lookup narrows on a real board.** Take one frame's actual deltas,
   map them to encodings, count how many closure atoms light up against 2,700.
3. **What a ~100-attribute observer costs.** More attributes is more slots and `F258`'s
   cross-product multiplies slots. Unmeasured, and not obviously affordable.
4. **Whether any closure atom lit this way is COMPOSABLE in Γ.** `F164` measured Γ's 45 grid atoms
   and the closure's 61-domain atoms disjoint **by name**. The encoding route may survive that —
   `by_encoding`'s keys include `EXTENT` and `SHAPE`, which are also Γ slot types — **but that is a
   hypothesis, not a result.**
5. **Whether the NAME-keyed join stays forbidden.** It does. `F164` stands, and nothing here
   revisits it. What is reopened is that the specified operation is **change → attribute →
   candidates**, which is a different key from the atom → atom join that was correctly refused.
