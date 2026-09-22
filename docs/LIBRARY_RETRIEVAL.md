# The library system — what retrieval, lookup and search DO today, and what the plan says they should

**Written 2026-09-22 at Isaiah's instruction, after `F271`–`F273`. Every claim in Part 1 is a read
of the code or a measurement with its source named.**

---

# THE RULINGS INDEX — 2026-09-22, and where each one lives

**Consolidated at the reviewer's request so the document can be checked against one list. Every row
is a ruling by Isaiah or the reviewer on 2026-09-22.**

| # | the ruling | where |
|---|---|---|
| 1 | vocabulary freeze withdrawn; instruments built per board; CUE_BOUNDARY retired, re-scoped by input provenance, `mapping` blocked, KEY_BOUNDARY unchanged; learning persists across games | 5.0, 5.10.1 |
| 2 | the observer is the TRACKER: instrumented attributes NULL at frame 0; delta WITH ITS ORDER; `came`/`gone`; relations per pair; route (a)→(b)→(c); delta bounds operands at BOTH sites; null-not-absent | 5.1, 5.2, 5.4, 5.5 |
| 3 | build on `composer.py`; port the abstention receipt, coverage, ranking, `Term`, laziness, the `idn` principle; drop the walk and the toy constants; delete only after 6.5's five checks | Part 6 |
| 4 | `+` is a placeholder, every junction UNKNOWN; the ground settles the bond via the six tests; tagged on use; bond as a PARAMETER; real trees; schema factory; lazy; reach never enumerated | 5.3, 5.4, 5.6, 5.8, 5.9 |
| 5 | the seed stays read-only; a condition is the AGENT's hypothesis in its runtime layer, approved BY THE GROUND — **no human gate** | 5.9.5 |
| 6 | MINTED / IMPORTED / INVENTED, three distinct things; invention's trigger exists as `owed_import`; `≡` rather than deletion | 5.9.6 |
| 7 | BIRTH fixed forever; STATUS per context; **IMPORTED is a status, not an origin**; the agent NEVER has the game's name — contexts key on its own STRUCTURE HASH | 5.10.9, CONFLICTS |
| 8 | record successes; confidence and relevance separate; youth bonus; decay by games/cycles never clock; orders never excludes; learnings → runtime → seed | 5.10.4, 5.10.8 |
| 9 | procedurally generated games: layout hash vs mechanics signature; NEAREST match; transfer counts only when MECHANICS differ | **Part 7** |
| 10 | the measurements | 5.10.6, 5.10.7, Part 6.5 |

---

# CHANGE LOG — 2026-09-22

    Part 4    by_cluster / by_encoding resolved; the observer contradiction reconciled as an
              A6i name collision; F165 re-labelled EXPECTED-INERT, then UNTESTED once
              CUE_BOUNDARY was found to have walled the recipe composer off
    Part 5.0  the vocabulary freeze withdrawn; VOCABULARY_FROZEN.md marked WITHDRAWN, kept
    5.3-5.6   the bond ruling: `+` is a placeholder; exists-vs-needed grepped; 76.5% of
              recipes need real trees; `came`/`gone` make `⇒` and `−` observable
    5.8       reach vs work held apart; where the claim can fail (`r`)
    5.9       the generator design; 5.9.5's human gate SUPERSEDED by ruling 5
    5.9.6     IMPORT rewritten as INVENTION; the word collision recorded
    5.10      cross-game persistence, track record, youth bonus, relevance decay
    5.10.9    NEW -- the `g.game` leak check, run and reported
    Part 6    the `enumerate_closure` inventory; two drops that would have broken the gate
    Part 7    NEW -- procedurally generated games
    BUILT     `cbd400a` order/duplicate-preserving parse · `be936c2` delta bounds operands at
              both sites · `d29c4f4` relations as per-pair slots, arm `TETHER_OBSERVER`

---

# CONFLICTS — flagged rather than smoothed, as instructed

**Four places the code or the corpus does not match a ruling. None is smoothed over below.**

**(a) `IMPORTED` IS AN ORIGIN IN THE CODE AND RULING 7 MAKES IT A STATUS.** `gamma.py:32` declares
`PRIOR, MINTED, IMPORTED` as one triple and `Term.origin` defaults to `MINTED`; `gamma.py:531`
assigns `origin=IMPORTED` on load. **Ruling 6 says keep the meaning and do not rename; ruling 7 says
move it from origin to status.** Both are satisfiable together — the meaning is unchanged, the FIELD
changes — but it is a real refactor touching `Term`, `save`, `load` and `summary`, and it is not
done. **Flagged, not started.**

**(b) NO STRUCTURE HASH EXISTS.** Grepped: `structure_hash`, `situation_key`, `_struct_key` — zero
hits anywhere. Ruling 7 keys birth, status, transfer, table stakes and the youth bonus on it, and
ruling 9 splits it into two. **So rulings 7, 8 and 9 all rest on a mechanism that is not built, and
5.10 cannot be built before it.** This is the single largest unbuilt prerequisite in the document.

**(c) MY 5.10.4 WOULD HAVE CREATED THE LEAK RULING 7 FORBIDS.** I wrote `settled_in:
frozenset[str]` as *the distinct GAMES a composition settled in*, feeding `fits()`. **Game names
reaching the ranking is precisely the contamination Layer 7 names.** Corrected to structure hashes
below. **The ruling arrived before the build, which is the only reason this is a correction and not
a defect.**

**(d) RELATIONS: RULED *PER-PAIR DIRECTED*, BUILT UNDIRECTED.** `d29c4f4` writes one
`a~b.contact` slot per unordered pair because the shared-face count is SYMMETRIC — `b~a` would store
the same integer, doubling the slot set for no information. Measured +23% slots on m0r0 rather than
the +47% a directed reading costs. **Direction WILL be needed for the asymmetric relations (`above`,
`inside`, `contains`) and they cannot reuse this shape.** Standing disagreement, awaiting a ruling.

---

**Part 1 is what the code does. Part 2 is the specified pipeline. Part 3 is the gap. Part 4 is what
is not known. Part 5 is the design. Part 6 is the composer inventory. Part 7 is procedural
generation.**

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

# Part 4 — RESOLVED, and what remains unknown

**The reviewer read this document against the closure files and resolved the two open items from
the data. Their counts, my verification where I could run it.**

## 4.1 RESOLVED — what the index is keyed by

- **`by_cluster` values are ATOMS** (`ACTION|Counter`, `ADHERENCE|Allegiance`, …): ACTION 202 …
  COLOUR 8.
- **`by_encoding` values are `{tier, why, atoms}`** — the "3 entries each" I counted were **the
  dict keys, not the population**. Real atom counts:

      SCALAR_DEFAULT 2,179 · SCALAR 699 · TEMPORAL 628 · EVENT 448 · BEHAVIOURAL 415
      RELATION 384 · SHAPE 167 · EXTENT 121 · STATE 115 · POSITION 80 · RULE 69
      COUNT 52 · COLOUR 11

**That is the census-of-the-wrong-population error, caught one step before it was published.** I
flagged the shape as unverified and stopped; the reviewer read the values.

## 4.2 ANSWERED — what today's 8 attributes actually light

    clusters overlapping the 8 perceived kinds       500 of 2,700
    gated by ATTRIBUTE_REACH to tier 0                11
      HUMAN|Number · HUMAN|Movement · RAW DATA|Adjacency · HEAT|Volume · AESTHETIC|Balance
      AESTHETIC|Scale · MATERIAL|Strain · ALEATORY|Probability · ACTION|Scope
      NETWORK|Degree · ATMOSPHERIC|Global circulation

**Several have no grid referent at all. And ENCODING DOES NOT NARROW: `SCALAR_DEFAULT` alone is
81% of the closure.**

> **SO ON TODAY'S PERCEPTION THE CUE LIGHTS ALMOST NOTHING USABLE — ELEVEN ATOMS, SEVERAL
> MEANINGLESS ON A GRID.** This *strengthens* Part 3's order rather than weakening it: **the lookup
> only narrows usefully after perception widens, and widening is only affordable after the operand
> axis is cut.** It also retires my own hope that `by_encoding` was the route around `F164` — the
> overlap with Γ's types is real and the narrowing is not.

## 4.3 THE OBSERVER CONTRADICTION — reconciled, and it is a NAME COLLISION

The 2026-09-20 record reported a heavy temporal sensor **called at `observer.py:89` on every
persisting object, every frame.** Part 1.7 says nothing in the agent path calls `observer`. **Both
are true.**

    observer.py:89          calls `sensors_heavy.temporal(...)`   -- the line is real
    observer._mutations     0 callers outside observer.py
    observer.observe(       EXACTLY 1 caller -- test_perception.py
    env.observe(            21 callers -- A DIFFERENT FUNCTION

**`observe` names two things.** The heavy sensor does fire every frame **whenever
`observer.observe` runs, and that is only ever in a test.** That is `A6i` — two legitimate
quantities under one word — and it is why the record could hold both claims without either being
wrong.

**And `F165` settles what the module does even when it runs:** *"it already computes EIGHT
non-positional cross-frame deltas, AND AGGREGATES THEM AWAY BEFORE ANYTHING COULD CARRY THEM"* —
summed to a count. So wiring the observer in without changing that would carry nothing.

## 4.4 F165 AND THE MOLECULE LAYER — expected-inert, and it must be said

`TRAINING_PLAN`: ***"MEASURED (`F165`, 2026-09-17): the emergent-molecule layer is INERT on ARC —
0 molecules fire"*** across all 25. **Lit atoms composed via recipes produced nothing.**

**That ran on the 8-attribute reading.** With 11 tier-0 atoms lit, of which several have no grid
referent, **a zero there is EXPECTED and says nothing about the widened pipeline.** It is not
evidence against the cue design — **but it must be stated, because a reader meeting `0 molecules`
without this line will read the pipeline as already refuted.**

## 4.5 THE CUT NEEDS A PARSE — a build dependency nobody had listed

`ATTRIBUTES.md`'s confirm-conditions (`Solidity` ⟺ `overlapArea == 0`) are **PROSE**, and the file
says so: *"reframes the missing key from a design problem to a parse."*

> **Corollary 4 IS the cut, and the cut is not executable today.** Parsing conditions into checks
> is a **build dependency** and it was missing from this document.

## 4.6 STEP 3.5 — the ENTRY-level graph, which is the one Isaiah meant

Part 2.2 assigns `ADJACENCY` to domain bridging, correct for the 285-edge file. **But
`TRAVERSAL.md` specifies an ENTRY-LEVEL ingredient graph** — *"the traversal runs at entry level
and the domain graph is a PROJECTION of it"* — **1,714 directed entry-to-entry edges, derivable
from the recipes with no judgement.**

**That is the graph matching *"adjacency says these atoms are reachable or likely"*.** It is
**derivable, not shipped**, and it goes in as **step 3.5**, between entry points and the recipe.

**With one measured qualifier: only 20% of entries are ever an ingredient of anything, so
`TRAVERSAL` calls it *"a thin spine with a very large fringe."*** Four fifths of the list are
leaves at entry level, and the graph narrows only within the spine.

## 4.7 WHAT REMAINS UNKNOWN

1. **What a ~100-attribute observer COSTS.** More attributes is more slots and `F258`'s
   cross-product multiplies slots. Unmeasured, and the reason the per-observation operand bound
   (`F262`: flat on three of four boards, no composition lost) is paired with it.
2. **Whether any closure atom lit this way is COMPOSABLE in Γ.** `F164` measured Γ's 45 grid atoms
   and the closure's 61-domain atoms disjoint **by name**. 4.2 removes the encoding escape.
3. **HOW A LIT AIM BECOMES AN ACTION — reviewer, 12:46, and it is the gap between lookup and
   PLAY.** A lit atom whose condition holds says **what is TRUE, not what to DO to make it
   true.** Route (b) returns an AIM; nothing in this document says how the agent gets from
   *`Contain` would explain this* to *press ACTION3*. Two candidates, both in the record and
   neither assessed: **route (a)'s recorded action->delta mapping** (`_note_move` already
   learns action->displacement), and **the BODY shelf** of the 2026-08-21 composer design
   (per-action deltas, chained to an anchor). **Unresolved, and it is load-bearing: a route
   chart can show (b) growing while the agent plays no better, if aims never reach actions.**
4. **Candidates from cue vs from closure enumeration, per action.** That is the 11:02 trace and it
   is the baseline the build is judged against.

---

# Part 5 — THE VOCABULARY FREEZE IS REMOVED (Isaiah, 2026-09-22)

> ***get rid of the freeze. SENSORS ARE INSTRUMENTS. No instruments = no perception = brute
> force.***

**`VOCABULARY_FROZEN.md` is WITHDRAWN and kept** — marked at its head, not deleted, because what
governed the build before today is part of the provenance.

**Its premise was already gone.** The freeze rested on *an expressibility failure is a finding*,
and Isaiah's 2026-09-15 ruling removed that: **expressibility is closed; a gap is a MAPPING gap.**
It outlived its justification by a week, **froze perception at 8 attributes + `touching`, and was
never narrowed.**

**What still stands, and is not a freeze:** *a solution may test our instruments and measure how
far the agent got; it may never decide what the agent is given.* Instruments are built from
`RELATIONS.md` / `ATTRIBUTES.md` **for every board** — never from one game's answer.

**And it settles the §12.3 tension:** containment and alignment are **computed from the board**, so
they are instruments and they are perceived. `RELATIONS.md`'s own line — *computed from the board
is perception; composed from other sensors is the agent's job.*

## 5.1 The build, in the order the evidence fixes

    1  arm M's A/B -- KILLED 12:10 on the reviewer's ruling, no output in 3h10m. Its
       question is re-asked after the observer, where binding density means something.
    2  the 11:02 trace -- per action: attributes changed, relations published, lookup key,
       candidates by SOURCE (cue vs closure), bindings tried, time split      THE BASELINE
    3  the full-attribute observer + the PER-OBSERVATION operand bound, together

**Together, not in sequence, and that is Part 3's arithmetic:** the observer widens slots and the
per-observation bound is the only measured thing that holds flat as the trace grows (`F262`:
m0r0 6.9→8.9%, ls20 21.3→20.1%, sk48 27.0→27.3%).

**Start with what `RELATIONS.md` names as cheap:** the three erasures (shape frozenset not the
integer, the frame stack, the component list) · contact types (point/edge/face, **already computed
for System 0 and currently trapped in its bookkeeping**) · the ~24 composable relations · the
bounding-box sensor (containment and its five dependents) · **the eight per-object deltas CARRIED,
not counted** (`F165`) · and **relations reaching `_library_fit`**, arm C's gate retired.

**Pre-registered, 3 seeds, spread beside every effect:** attributes and relations published per
object · **candidates lit by the cue — the 11 should grow** · candidates from cue vs closure
enumeration · s/action late in the run · distinct compositions · binding density · atoms-only
control. **No ground prediction.**

## 5.2 WHAT THE OBSERVER ACTUALLY IS — Isaiah, 2026-09-22, and it is smaller than "wire in `observer.py`"

> ***the delta is only in the DETECTED OBJECTS and their attributes (currently 8 but will expand)***
> ***— the mutation observer was meant to observe that change of those objects, which I believe you
> both call slots.***

**This narrows the build and corrects how Part 1.7 and Part 4.3 read.** The observer is **not** a
pass over the closure's 2,700 atoms or its 5,040 attribute names. It is:

    for each DETECTED OBJECT the tracker holds
      carry the FULL attribute + relation vector   (8 today, ~100 specified)
      NULL at frame 0, updated every frame from frame 1
      EMIT THE CHANGE -- which attributes of which objects moved

**`slot` is exactly that pair.** `o5.colour` is object `o5`'s `colour` attribute, and the delta is
the set of slots whose value moved between two frames. **So the observer is the TRACKER carrying
more per-object attributes and publishing the change — not a separate subsystem being wired in.**

> **WHICH MEANS `observer.py` IS NOT THE THING TO WIRE.** Part 4.3 reconciled why the record held
> two contradictory claims about it, and `F165` showed it aggregates its eight deltas away. **But
> the specified observer lives where the objects live — `arc_percept.Objects` and what
> `_decomposed` publishes** — and `observer.py` is an offline analysis module that happens to share
> the name. **A third instance of `A6i` on the same word.**

**And one clause of it went in tonight, for an unrelated reason.** Ruling (b) made a covered
object's attributes publish `NOT_RESOLVED` rather than vanish — ***null, not absent***, which is
the observer spec's *"initialised NULL at frame 0"* applied to one case. **The pattern is already
in the code; what is missing is the width and the emission.**

**The cost question is unchanged and is now precisely statable:** slots = objects × attributes, so
8 → ~100 attributes on a board holding ~70 objects takes ~560 slots to ~7,000, and `_bindings`
returns one bind per slot. **That is the multiplier Part 3 says to cut first, and the
per-observation bound is the only measured candidate that holds flat as the trace grows.**

### 5.2.1 WHAT `came`/`gone` COST IF A DEPARTED OBJECT PERSISTS AS NULL — counted first

**Two clauses of ruling 2 meet here.** *Publish `came`/`gone`* and *null-not-absent: unreadable =
present with no value.* Together they mean a DEPARTED object should leave a NULL rather than
vanishing — which is what makes `−` (absence is the point) and `⇒` (it did not exist before)
readable as deltas at all.

**Today `_present` DELETES a departed slot** and pops its binding, its residual and its trend
(`tether.py:3094`). If objects persist instead, the slot set becomes every object EVER SEEN rather
than every object PRESENT — and `_bindings` is linear in the slot set. So the cost had to be counted
before the clause was built.

    board   frames   live (mean)   came/frame   gone/frame   EVER SEEN   peak live
    sk48      14         723         20.0         40.0          926         912
    dc22      14         724         19.2          4.9          802        ~738
    m0r0      14         168          4.6          1.2          192         176

#### THE FIRST READING WAS A DENOMINATOR ERROR, AND IT IS THE SAME ONE AGAIN

I first compared EVER SEEN against the LAST live count and read **sk48 at 2.28x** — a number that
would have made this clause look unaffordable on the board that matters most.

**It is wrong because sk48's last frame is POST-SHEDDING.** Per frame: slots only GROW for frames
0-8 (666 → 912, ZERO departures), then **376 depart at once at frame 9**, and erosion continues —
48, 32, 40, 24. `blind` is `False` on every frame, so this is a real structural event and not the
blind-frame artefact `_present`'s own docstring warns about.

> **AGAINST PEAK LIVE — THE RIGHT DENOMINATOR — PERSISTING COSTS +1.5% ON sk48 (926 vs 912), +9% ON
> dc22 AND +9% ON m0r0.** Cheap on all three.
>
> **AND THE REASON IS STRUCTURAL RATHER THAN LUCKY: OBJECTS DO NOT COME BACK.** `EVER SEEN` climbs
> 920 → 926 across frames 9-13 while **520 slots depart** over the same span. So the cumulative set
> is bounded by the PEAK object count, not by cumulative churn — which is what makes
> persist-as-null affordable in general rather than on these three boards.

**That is the third denominator error of this session** (`F262`'s four-call baseline, the
contaminated thirds, this) and the same shape each time: a ratio taken against whatever count was
nearest rather than against the one the decision turns on.

#### What it means for the build

    persist departed objects as NULL     affordable -- bounded by peak, not by churn
    `came` / `gone` carried per cycle    they are computed at `tether.py:3086` and DISCARDED
    the consumer                         the bond tests (`⇒`, `−`), which are held for greenlight

**So item 3 splits: the CARRY is cheap and unblocked; the null-persistence is affordable but
changes object lifetime, and its only consumer is held.** Publishing a quantity nothing reads would
be the silent code the checker forbids, so the carry lands first and the lifetime change lands with
the bond tests.

## 5.3 THE BOND IS A HYPOTHESIS THE GROUND SETTLES — Isaiah, 2026-09-22, RULED

> ***OPERATORS.md shows that any operator can be used. The recipes list mostly uses `+` only as an
> example, but I expect the programming or metaprogramming to handle this too.*** — and, asked
> whether the bond is therefore a hypothesis rather than data: ***"Correct."***

**`+` IN A RECIPE IS A PLACEHOLDER, NOT A CLAIM.** A lit recipe written `A + B + C` is a **FAMILY of
candidates, one per bond reading**. OPERATORS.md's own worked example is the proof: `Bal + Prop +
Cnt` is **Walk**; `Bal → Prop → Cnt` is *falling forward and catching yourself*; `Prop ⇒ Cnt` is a
collision. Same three ingredients, four different things.

**THE GROUND SETTLES WHICH READING HELD** — this frame's delta and the atoms' conditions confirm or
refute each, exactly as route (a) does for any live theory. **Tagged ON USE, never in advance**, so
the 2,600-judgement wall never has to be paid: an entry becomes worth tagging the moment something
composes from it.

## 5.4 EFFICIENCY — WHY BLIND GENERATION IS NOT AN OPTION, WITH THE NUMBER

**Blind generation is the combinatorial walk one axis over, and it is worse than it sounds.** For a
recipe of `n` ingredients there are `7^(n-1)` bond assignments times the binary groupings:

    2 ingredients      7 readings
    3 ingredients     98 readings        <-- THE MEDIAN RECIPE
    4 ingredients  1,715 readings

**Measured over ATOMS.md's 2,120 `+` recipes: 23.5% are binary, 50.7% have three ingredients, 25.7%
have four. 76.5% HAVE THREE OR MORE.** So the median lit recipe would expand to ~98 candidates.
Against a candidate axis already running ~105 per lookup call, that is a **~100x multiplication of
exactly the axis Part 3 exists to cut.**

**SO THE SIX TESTS ARE NOT AN OPTIMISATION. THEY ARE THE ONLY VIABLE ROUTE**, and they work because
each one is a **yes/no question about a quantity the delta already carries** — the reading is
SELECTED, not searched:

| bond | OPERATORS' test | the delta quantity that answers it | today |
|---|---|---|---|
| `+` vs `→` | swap the operands — does the meaning change? | **the ORDER of the changes** | **NO — see below** |
| `∥` | remove one — does it still work? | a frame where one ingredient's condition failed and the result still occurred | across frames |
| `−` | is the ingredient's **absence** the point? | a **value → null** transition | computed, unpublished |
| `⇒` | does B exist **before** A fires? | a **null → value** transition | computed, unpublished |
| `⋛` | is it about **which is larger**? | a magnitude comparison between two changed slots | `above` / `is_max` / `rank_in` |
| `≡` | substitute one for the other — anything lost? | two names whose slots co-vary perfectly | derivable, no atom |

> **AND THE ONE TEST THAT CANNOT BE ANSWERED TODAY IS THE MOST IMPORTANT ONE.** `+` versus `→` is
> the distinction the whole corpus turns on, and it needs **the ORDER of the changes within and
> across a frame**. Today's delta is a SET of changed slots with no ordering — the trace measures
> `delta_slots` as a count and `delta_attrs` as a Counter. **So the observer must carry the SEQUENCE
> of changes, not only the set.** That is `WHAT_THE_AGENT_SEES`' transition/cascade distinction, and
> it is now a **hard requirement of the observer build** rather than a nicety.
>
> **AND IT IS THE SAME ITEM AS ONE OF 5.1's THREE ERASURES — the reviewer's 12:46, and I had
> them filed as separate work.** The FRAME STACK is where order lives: a single response
> returns up to nine frames (`PERCEPTION_PIPELINE` Layer 1), and the agent currently reads
> only the last. **The cascade within a response IS the sequence of changes.** So
> un-erasing the frame stack is not one cheap item among three — **it is the PREREQUISITE
> for `+` versus `→`, and therefore for the commonest bond distinction in the corpus.**

## 5.5 EXISTS VERSUS NEEDED — GREPPED, NOT RECALLED

| bond | what is in the code | verdict |
|---|---|---|
| `→` sequence | `Term.atoms` applies left to right | **EXISTS — a `Term` IS a `→` chain** |
| `+` conjunction | `Atom("both", PRED→PRED, reads_operand=True)` — `arc_atoms.py:645` | **EXISTS, arity 2**, via the operand join |
| `∥` disjunction | `Atom("either", ...)` — `arc_atoms.py:647` | **EXISTS, arity 2** |
| NOT | `Atom("negate", PRED→PRED)` — `arc_atoms.py:644` | **EXISTS** |
| `⋛` comparison | `above`, `is_max`, `is_min`, `rank_in` | exists **as predicates**, not as a bond **between two composed terms** |
| `⇒` production | `_present`'s `came` — `tether.py:3039` | **raw material exists, UNPUBLISHED** |
| `−` subtraction | `_present`'s `gone` — `tether.py:3038` | **raw material exists, UNPUBLISHED** |
| `≡` identity | nothing | **MISSING — and it does not belong here** (below) |

**THE FINDING WORTH MORE THAN THE TABLE: `⇒` AND `−` ARE EXACTLY THE TWO BONDS THAT RULING (b)'s
*NULL, NOT ABSENT* MAKES OBSERVABLE.** Production is a `null → value` transition; subtraction is
`value → null`. `_present` ALREADY computes both, as `came` and `gone`, and files them as *"a plain
event"* — recorded and never published as a delta anything downstream can read. **So two of the
three missing bonds fall out of observer work that is already ordered, at no extra cost.** They were
never a bond problem; they were the publication gap.

**AND `≡` SHOULD BE SAID PLAINLY RATHER THAN LISTED AS A GAP: it is a statement about the LIBRARY,
not about the board.** *Two names, one referent* is what `_library_fit` needs in order to know two
candidates are the same term. It has no delta test of its own beyond perfect co-variation, and
generating an `≡` reading at runtime would be asking the board a question the board cannot answer.
**It belongs in the retrieval layer, not in the bond generator.**

## 5.6 WHICH BONDS FIT A CHAIN AND WHICH NEED A TREE — the reviewer's direct question

- **`→` fits a chain.** That is precisely what `Term` is, and nothing is owed.
- **A BINARY `+`, `∥`, `⋛` fits the ONE operand join.** `both` / `either` are `reads_operand=True`,
  so the second predicate arrives through the operand slot — and §4's computed operand (`f<g(s)>`)
  lets that second argument itself be composed. **One level of nesting, and one only.**
- **A REAL TREE IS NEEDED THE MOMENT A RECIPE HAS THREE INGREDIENTS UNDER MIXED BONDS.** `A + B → C`
  cannot be a chain: `+` groups A with B, and `→` sequences that GROUP against C. `Term` carries one
  operand and one guard, so it can express `(A + B)` or `(X → Y)` and cannot express the nesting.

> **AND THAT IS THE MAJORITY CASE, NOT AN EDGE CASE: 76.5% of the recipes have three or more
> ingredients.** Only 23.5% are binary and fit what exists today. **So "a real tree" is not a
> refinement to defer — it is the representation 3 in 4 recipes require**, and any claim that the
> bond machinery is built must state which quarter it was built for.

## 5.7 WHERE THE SETTLED BOND LIVES, AND THE DEPENDENCY ORDER

**THE MECHANISM EXISTS AND IS NOT NEW — `gamma.Standing`** (`settled_at`, `rejections`, `refute`,
`decay`): *"a term's record against the ground. Weighted, clocked, and never a hard ban."* **A bond
reading is a hypothesis with a `Standing` like any other term** — it settles when the ground
confirms it and decays when refuted. Nothing has to be invented for item 3.

    runtime overlay   the settled bond, provenance DERIVED-BY-GROUND, this agent, this run
    learnings         promoted via `Standing` once expressed AND confirmed
    the seed          READ-ONLY. Never written. The closure files are the inherited frontload.

**DEPENDENCY ORDER, and it is strict:**

    1  the CONDITION COMPILER          a bond reading is only checkable if the atoms' conditions
                                       are. Today FOUR lines of ATTRIBUTES.md carry a comparison
                                       operator at all, all inside prose (4.5). THE PARSE IS FIRST.
    2  the OBSERVER carrying ORDER     `+` vs `→` is unanswerable without the sequence of changes,
                                       and it is the commonest distinction in the corpus (5.4).
                                       `came` / `gone` published turns on the same work (5.5).
    3  the SIX TESTS as a selector     only now do they have inputs to read.
    4  TREES                           needed by 76.5% of recipes; binary works without them.

**So the bond programme does not begin with bonds.** Steps 1 and 2 are the observer and the parse
already ordered in 5.1 — **the bond work is what those two unlock**, which is why it costs less than
it looks and why it cannot be started first.

**DESIGN ONLY. Nothing in Part 5 is built.**

## 5.8 SIZING — REACH IS ~10k–20k AND MUST NEVER BE ENUMERATED (Isaiah, 2026-09-22)

> ***In theory the 1,266 recipes should work with just the `+`, but depending on how sophisticated
> the agent is in composing, there could be 10k–20k.***

**REACH AND WORK ARE TWO NUMBERS AND THE DESIGN MUST HOLD THEM APART.** ~1,266 recipes used as
ingredients times up to 8 bond readings is ~10k; `→` also varies by ingredient ORDER (three
ingredients have six) pushing toward ~20k; the full list is ~2,650 and the agent's own settled terms
raise the ceiling again. **NOTHING MAY ENUMERATE THAT SET.** No precompiled bond readings, no table
of 20k functions, no walk.

### 5.8.1 The real reference point — CORRECTED, because the trace has since landed

The addendum cites *~1,283 candidates x ~130 bindings per action*. **That was the 4-cycle m0r0 smoke
test. The completed 30-cycle baseline is far worse**, and the design has to beat the real number:

    sk48  cycle 27   32,562 closure candidates   x  646 binds/cand  =  21,047,303 binds  (129.7 s)
    dc22  cycle 29   24,398 closure candidates   x  330 binds/cand  =   8,058,186 binds  ( 65.0 s)

### 5.8.2 The per-action cost bound, in terms of the DELTA rather than the library

**TODAY** an action costs `C x S` — `C` closure candidates (grows with library size AND depth) times
`S` operand binds, where `S ~= the slot count` because `_bindings` returns every other slot.
**NEITHER TERM IS BOUNDED BY WHAT HAPPENED.**

**UNDER THIS DESIGN** an action costs `d x r x 6(n-1)` -- **corrected by the reviewer
(12:46): a recipe of `n` ingredients has `n-1` JUNCTIONS, each settled separately.** With
`n = 3` the median (5.6), that is ~12 checks per lit recipe rather than 6. **The claim is
untouched -- `n` is a property of the recipe, not of the library size:**

    d   slots that CHANGED this frame        measured: sk48 median ~74, dc22 median ~10
    r   recipes the changed attributes LIGHT via ATTRIBUTE_INDEX
    6   OPERATORS' yes/no tests per lit recipe -- NOT 7^(n-1) readings (5.4)

Operands come from the delta too, so `S` becomes `d` rather than the slot count — **that is conflict
4, and it is the term that carries most of the reduction.**

**AND THE STRUCTURAL CLAIM IS THAT NONE OF `d`, `r`, `6` IS THE LIBRARY SIZE.** `d` is how much the
world changed; `6` is a constant from the corpus; `r` is what the delta lit. **So the library can go
2,650 -> 20,000 and a later action costs the same — which is the claim the route chart tests.**

### 5.8.3 WHERE THAT CLAIM CAN FAIL, AND IT IS `r`

**`d` and `6` are genuinely library-independent. `r` IS NOT, and saying otherwise would be the
design marking its own homework.** The index is keyed by attribute; if the library grows, MORE
recipes contain any given attribute, so `r` grows with library size unless something bounds it.

**So "bigger library, less work per action" holds for two of three terms automatically and requires
a DELIBERATE BOUND on the third.** That bound is a decision rather than a derivation, and it
collides with the standing behaviour that `retrieve` **never cuts** — *"ONE PASS over the library,
ordered by fit. EVERY NAME COMES BACK."*

**The honest statement of the open question: either `r` is bounded by ranking and taking a head — a
CUT, which changes retrieval's contract and needs a ruling — or `r` is bounded by the CONDITIONS,
where a lit recipe survives only if its atoms' conditions actually hold on this frame.** The second
is the corpus's own answer (4.5's parse) and costs nothing extra, because the conditions must be
evaluated anyway to settle the bond. **It is also unmeasurable until the parse exists**, which is
why the parse is dependency 1 in 5.7 and not an afterthought.

### 5.8.4 Precomputed versus generated on demand

    PRECOMPUTED, small, loaded once     ATTRIBUTE_INDEX (attribute -> atoms) · the instrument list
                                        (RELATIONS + ATTRIBUTES) · the ~8 bond combinators · the
                                        recipe table as DATA (ingredients, no bonds fixed)
    GENERATED ON DEMAND, never stored   every composition. A recipe exists as `(ingredients,
                                        candidate bonds)` until a delta lights it; it becomes
                                        executable only when lit; its bond is fixed only when the
                                        ground settles it.
    CACHED AFTER THE FACT               settled compositions only -- looked up FIRST next time

**THE GENERATORS ARE THEREFORE LAZY BY CONSTRUCTION, AND THAT IS WHAT MAKES 20k REACH COST NOTHING
TO HOLD:** an unlit composition is a row of data, not a function, not a closure walk, not a term in
Γ.

### 5.8.5 The three store layers, and the direction of travel

    seed        READ-ONLY, inherited frontload -- the closure files. NEVER written at runtime.
    runtime     this agent, this run: settled bonds, lit compositions, provenance DERIVED-BY-GROUND
    learnings   promoted from runtime via `Standing` once EXPRESSED and CONFIRMED

**Lookup order is the reverse: learnings -> runtime -> seed.** A composition the agent has already
settled is found before anything is generated, so repeated structure gets cheaper with experience —
**which is the mechanism behind "progress arrives effortlessly", stated as a cache rather than as a
metaphor.**

### 5.8.6 What the route chart will actually show if this is right

    (c) mint          shrinks -- lookup misses fall as settled compositions accumulate
    (b) lookup        grows, then FLATTENS as the cache absorbs the repeats
    (a) theory        grows -- more live theories, each confirmed or refuted by the delta
    binds/action      falls and stays flat as the library grows      <-- THE LOAD-BEARING ONE
    s/action          stops rising within a run

**The baseline for every one of those is now measured on two boards (sk48, dc22, 30 cycles), and all
four currently run the wrong way.**

---

# Part 5.9 — THE GENERATORS: how 2,700 atoms become executable without 2,700 functions

**Isaiah asked for MY design rather than a restatement of his. This is it. Design only.**

## 5.9.0 A MEASUREMENT THAT CORRECTS BOTH OF US FIRST

**The recipe column contains almost nothing but `+`.** Character census over ATOMS.md's 3,495 table
rows:

    `+`  4,294        `(` / `)`  713 each (the `A(x)` qualifier)
    `>`      5        `=`  1              <-- the ONLY ordered/comparison bonds present, in ASCII
    the seven unicode bonds: effectively absent

**SO "AN ORDER-PRESERVING PARSE" HAS NO ORDER IN THE FILE TO PRESERVE**, and my own 5.4 implied the
ordered bonds were merely rare rather than absent. **This does not weaken Isaiah's ruling — it is
the strongest possible form of it.** `+` is not mostly-a-placeholder; it is the ONLY thing ever
written, so **every junction is UNKNOWN by default** and there is nothing to re-tag, only something
to settle.

**What IS recoverable and is currently destroyed: the ORDER OF THE INGREDIENTS AS WRITTEN.**
`Translate = Ct + Co` names `Ct` first. `composer.py` parses to a `frozenset` and loses it. That is
the real content of step 2's fix.

**And one count to correct: 2,061 recipes carry 2,669 DISTINCT INGREDIENT NAMES**, not the ~1,266
used for scoping the parse. The parse population is twice what was assumed.

## 5.9.1 The object class — A SCHEMA FACTORY, NOT A METACLASS, and the reason

**Chosen: a schema-driven factory.** The schema is a list of `Instrument` records (name, type,
detector, condition); an object is a mapping from instrument name to reading, every entry NULL at
frame 0.

**Why not a metaclass.** A metaclass fixes the attribute set **when the class is created**, and the
instrument list **grows at runtime** — that is the whole of the freeze withdrawal. Adding a sensor
would mean re-creating the class, and every object already alive would be an instance of the old
one. **The schema factory grows by appending to a list that instances share by reference.**

**And the deciding argument is that the syntax a metaclass buys is syntax this codebase does not
use.** Slots are addressed as STRINGS end to end — `o3.colour` is a dict key, not attribute access,
in `_decomposed`, `observe`, `slots`, `_bindings` and the lookup key. A metaclass would make
`obj.colour` work in Python while every consumer kept using `state["o3.colour"]`. **Zero call sites
would benefit.**

## 5.9.2 The combinators — ONE function, the bond as a PARAMETER

Isaiah's item 6 is that the generators take the bond as a parameter, so this is **not eight
functions**:

    Bond = "+" | "→" | "⇒" | "∥" | "−" | "≡" | "⋛"        NOT is unary

    bind(bond: Bond, left: Node, right: Node) -> Node     # one constructor
    negate(node: Node) -> Node

    settle(bond: Bond, left: Node, right: Node, delta: Delta) -> bool | None
        # True confirmed, False refuted, None not-yet-decidable on this delta

**`settle` is the six tests, one per bond, each reading a quantity the delta already carries (5.4).
`None` is the third answer and it matters** — a bond that is not yet decidable must not be counted
as refuted, or a reading gets eliminated by a quiet frame.

## 5.9.3 The tree — `Term` is kept as the CHAIN case and wrapped, not replaced

    Node = Term | Bonded
    Bonded = (bond, left: Node, right: Node, standing: Standing, origin: str)

**`Term` already IS the `→` chain (5.5) and ~24% of recipes need nothing more**, so replacing it
would be a rewrite in exchange for nothing. `Bonded` nests, carries its own `Standing` so each
junction settles independently, and leaves every existing `Term` consumer untouched.

## 5.9.4 The recipe compiler — what a lazy row looks like

    BEFORE LIGHTING (data, never executed -- this is what makes 20k reach free to hold):
        Recipe(name, ingredients: tuple[str, ...]  # ORDERED, as written
                     junctions: tuple[Bond|UNKNOWN, ...]   # length n-1, all UNKNOWN from the file
                     provenance: "seed:ATOMS.md:<line>")

    AFTER LIGHTING (this frame's delta lit its ingredients and their conditions hold):
        a `Node` tree, junctions still UNKNOWN, each with a fresh `Standing`
    AFTER SETTLING:
        junctions fixed, provenance DERIVED-BY-GROUND, cached in the runtime layer

## 5.9.5 The condition compiler — THE METHOD

**Target grammar** — deliberately tiny, so the parse is checkable and a failure is a parse error
rather than a wrong reading:

    cond := cmp | cond ('and'|'or') cond | 'not' cond
    cmp  := expr OP expr          OP in { == != < <= > >= }
    expr := INSTRUMENT '(' args ')' | SLOT | NUMBER

**How the prose is converted: OFFLINE, and NOT by the agent.** A batch pass over ATOMS.md /
ATTRIBUTES.md emits candidate conditions into a `condition` field beside ATTRIBUTE_REACH. **It never
runs in the loop**, so a bad parse cannot become a live reading.

**Every output is stamped and INERT until reviewed:**

    provenance: DERIVED · source: <file>:<line> · method: <parser version> · status: PROPOSED

**THE HUMAN GATE IS SUPERSEDED — RULING 5, 2026-09-22.** This section required a human review to
flip `status` from PROPOSED to ACTIVE before the agent could read a condition. **The ruling removes
it: the seed stays read-only, a checkable condition is the AGENT'S HYPOTHESIS in its runtime layer,
and THE GROUND approves it — used and held raises standing, used and failed fades. No human gate.**

**AND THE RULING DISSOLVES THE PROBLEM THE GATE WAS SOLVING RATHER THAN OVERRIDING IT.** My reason
for the gate was that writing a machine-checkable condition for a prose atom is CORPUS AUTHORING,
which `CLAUDE.md` forbids this seat. **That holds only if the condition is written INTO THE CORPUS.
It is not — it lives in the agent's runtime layer as a hypothesis, and the seed is never touched.**
So the constraint is satisfied by where the condition lives, not by who approves it, and a human
approving it would have been the proctor deciding what the agent may believe — which is the larger
error of the two.

**The provenance stamp stays** (`DERIVED`, source, parser version): it is what keeps the ablation
partition reconstructible, and that was never the gate's job.

**PROPOSED FIRST SCOPE, for Isaiah to rule** — I agree with the reviewer's suggestion and would add
a stop condition: **the atoms today's perception can light, and only those whose instruments already
exist.** It is the smallest set that can be checked END TO END on a live board, and it grows by
exactly the event that grows perception, so the parse never runs ahead of the instruments that would
make it checkable. **Against 2,669 ingredient names (5.9.0), an unscoped parse is the 2,600-judgement
wall Isaiah's tag-on-use ruling exists to avoid.**

### 5.9.6 IMPORT IS INVENTION — Isaiah, 2026-09-22, AND THE WORD ALREADY MEANS SOMETHING ELSE

> ***Import comes from OUTSIDE the library — only when you observe a behaviour on the board, or want
> to do an action you cannot compose from the available atoms. It is the creation of a BRAND-NEW
> ATOM described from what the agent has observed, not available in the library even with
> composition — YET.***

**THIS SUPERSEDES WHAT THIS SECTION SAID.** It read *mint and import are one operation … `MINTED`
from a residual, `IMPORTED:<source>` from a game* — import as ADOPTION, a term arriving from
elsewhere. **That is not what Isaiah means, and the two are different operations: mint makes a TERM
out of existing atoms; invention makes a NEW ATOM.**

#### The collision, and it is `A6i` with the item that collides already nameable

**`import` NAMES TWO LEGITIMATE THINGS IN THIS PROJECT AND ONLY ONE OF THEM IS ISAIAH'S:**

    gamma.py:32          `PRIOR, MINTED, IMPORTED = "prior", "minted", "imported"` -- an ORIGIN,
                         meaning ADOPTED FROM ELSEWHERE
    tether.py:1448       *"an IMPORTED operand-reading term is `idn` here … binding is re-decided
                         at the destination; the import path never did it"* -- adoption again
    CLAUDE.md            *"import must be provenanced -- convergent derivation and ADOPTED import
                         are indistinguishable in the contents"* -- the corpus uses adoption too

**So writing "import = invent a new atom" into this document would put two quantities under one word
at the site that defines both** — the exact failure `A6i` records, and the writing-side version of
it, which fires where step three cannot because there is no separate spec to consult.

> **RESOLUTION: THE OPERATION IS `INVENTED`, A FOURTH ORIGIN BESIDE `PRIOR` / `MINTED` / `IMPORTED`.**
> The reviewer's own note already wrote *provenance INVENTED*; making it THE WORD rather than a
> description is what keeps the collision out of the code. `IMPORTED` keeps its meaning, unchanged.

#### What EXISTS: the trigger, with its receipt, already recorded

**`owed_import` IS THE GAP LIST AND IT IS ALREADY POPULATED BY EXACTLY ISAIAH'S CONDITION.**
`tether.py:3480` adds a slot when mint ABSTAINS — verdict `budget_spent`, `depth_exhausted` or
`under_floor` — and `abstained[slot]` carries `depth`, `candidates`, `coverage`, `verdict`,
`units_then`.

**That is *I observed this and could not compose it*, recorded, with the closure it searched attached
to it.** So trigger (a) is built and the agent already holds a ready-made candidate list for
invention. **Nothing needs to be detected that is not already being detected.**

#### What DOES NOT EXIST: the agent cannot create an atom

`Gamma.__init__` sets `self.atoms = list(atoms)` and `self._by_name`, and **nothing appends to
either.** `compose` resolves names only through `self._by_name[n]`. **The atom registry is fixed at
construction**, so the whole of invention — the part that makes a new primitive rather than a new
arrangement of old ones — is unbuilt.

**AND ITS NEAREST EXISTING RELATIVE IS MEASURED DEAD.** `retro → _promotions → promote` writes
`primitive=True` on *a residual recorded before it existed, on a slot it was not minted for* — the
enshrinement chain — and `F56` measured it **never once completing on a real board.** So the
machinery for earning a promotion exists, has never crossed anything, and invention must not be
built on the assumption that it will.

#### The licensing is already written, and Isaiah's trigger IS the clause

`CLAUDE.md`'s ladder: ***`composition → atom → sensor`, and every step is licensed by the same
thing: THE LEVEL BELOW TRIED AND COULD NOT. Never by usefulness.*** And the atoms' entry clause
admits one *when the agent's own machinery PERCEIVED AND NAMED THE GAP*.

> **`owed_import` IS THAT MACHINERY, AND THE ABSTENTION RECEIPT IS THE NAMING.** So invention is not
> a new permission being requested — it is the second rung of a ladder the corpus already built,
> with the gate condition already computed every cycle.

#### What an invented atom carries

    name          ARBITRARY and meaningless -- the identity is the OBSERVED PATTERN it was made
                  from: colour-agnostic, game-agnostic, structure-keyed
    origin        INVENTED, with the game and cycle where it was first formed
    index         entered, so a later delta can light it
    Standing      earned like anything else -- no head start for being the agent's own
    the key       NEVER. KEY_BOUNDARY is untouched by any of this.

**"YET" IS LOAD-BEARING.** If later growth makes an invented atom composable, **record the identity
(`≡`, in the retrieval layer per 5.5) and DO NOT DELETE THE INVENTION** — *when* it was invented is
part of the evidence, and deleting it would erase the only record that the agent once could not get
there.

**DESIGN ONLY. Nothing in Part 5 is built.**

## 5.10 COMPOSITIONS PERSIST ACROSS GAMES, AND TRACK RECORD WEIGHTS THE RANKING

> ***The agent should STILL be able to save compositions and retrievals across games — that is
> proof of learning, and work that doesn't have to be reworked for every game. The more a recipe is
> called upon and works, the higher its confidence and weight in ranking … most games require
> certain recipes or a mix of certain things that are like table stakes.*** — Isaiah, 2026-09-22

### 5.10.1 It does not conflict with 5.0's rule, and the code already says so

*A solution may never decide what the agent is GIVEN* forbids the ANSWER KEY choosing. **It says
nothing about the agent keeping what IT settled against the ground** — those carry provenance
DERIVED-BY-GROUND, and carrying them across games IS the transfer claim the ablation tests.

**`Gamma.save`'s own docstring already carries the ruling**: *"§17.8 … recorded its own inclination
as start cold across games. **Isaiah ruled the opposite: the library persists, because transfer is
the claim.** The switch is that nothing calls save/load unless the seat does, so the ablation stays
runnable by simply not loading."* **So this is not a new permission — it is a 2026 ruling being
honoured, and the ablation switch is the absence of a call rather than a flag.**

### 5.10.2 WHAT IS ALREADY TRUE, and one boundary on my own baseline

**Cross-game persistence is REAL TODAY on the pooled path.** `feeder.py`'s multi-game loop builds
ONE `Gamma`, switches `g.game` per cycle, and never resets — so the library accumulates across
games within the process. Separate-process carry is opt-in via a `library=` path (`feeder.py:319`
loads, `:329` saves).

> **AND THE BOUNDARY THAT MATTERS FOR EVERYTHING ELSE IN THIS DOCUMENT: THE sk48/dc22 BASELINE WAS
> COLD-START, SINGLE-GAME.** The trace harness builds `Gamma(env.atoms(), game=GAME)` and never
> loads. **So 5.10's entire subject — carried compositions — was absent from the before-picture BY
> CONSTRUCTION**, and the route chart's learnings share is 0 there for that reason rather than as a
> finding. Any post-build comparison must either hold this constant or say which side carried a
> library.

### 5.10.3 WHAT IS MISSING: `Standing` IMPLEMENTS THE FADE AND NOT THE RISE

Isaiah's rule is three-way. Grepped against `gamma.Standing`:

| his rule | the code | verdict |
|---|---|---|
| used and **FAILED** → fades gradually | `refute()` → `rejections += 1.0`, halved on a `REJECTION_HALFLIFE` clock | **BUILT** |
| **retrieved but NOT tested** → no change | `refute` fires only at `tether.py:3778`, whose comment is *"express-before-judge: this term actually predicted, and was wrong"* | **BUILT, by construction** |
| used and **WORKED** → weight rises | `settle()` sets `settled_at = self.tick` — **a TIMESTAMP THAT OVERWRITES** | **NOT BUILT** |

**SETTLING TEN TIMES LEAVES EXACTLY WHAT SETTLING ONCE LEAVES.** There is no success counter and no
distinct-games field; `self.game` records where a term was **minted** and, by its own comment,
*"does not change when the term is later pulled elsewhere."*

**So the asymmetry is real: failure accumulates and success does not.** It is narrower than it first
looks — clause 3 holds, so a recipe is NOT punished merely for being retrieved where it does not
apply. But among terms actually expressed, **a recipe that is right in nine games and wrong in one
carries a rejection and no credit**, which is precisely backwards for the table-stakes set Isaiah is
describing.

### 5.10.4 The design

**EXTEND `Standing`; do NOT invent a second confidence number** (Part 2.4's own rule):

    settled_in: frozenset[str]     the DISTINCT STRUCTURE HASHES this composition settled under
    confirmations: float           successes, on the same decay clock as `rejections`

**STRUCTURE HASHES, NOT GAME NAMES — RULING 7, and my first draft had it wrong.** I wrote *distinct
GAMES*, which would have fed the environment's identifier into `fits()`. **`WHAT_THE_AGENT_SEES`
Layer 7: a persistent key the agent READS from the environment is contamination; one it COMPUTES
from structure is recall.** An agent keyed on a given ID looks like it is learning, is doing lookup,
and scores zero the moment identities are hidden — which is the private set. **No structure hash
exists in the code today (CONFLICTS b), so this is a prerequisite rather than a field.**

**`fits()` gains a track-record term that ORDERS AND NEVER EXCLUDES.** Today it scores type
signature 2, arity 1, aimed 1, relational 1 — and reads `Standing` nowhere. The new term sits
alongside those, and `retrieve`'s contract is untouched: **every name still comes back; a
low-weight recipe still wins when the board calls for it.** Not a cut — which also keeps it clear of
5.8.3's open question, where a head-cut was explicitly NOT ruled.

**BREADTH OUTRANKS REPETITION, and it is `len(settled_in)` that carries it, not `confirmations`.** A
composition that settled in six games is table stakes; one that settled fifty times in a single game
is that game's trick. **The two are indistinguishable under a plain counter, which is why the
distinct-game set is the field that matters.**

**Where it lives:** the learnings layer, persisted across games and runs; lookup order is
**learnings → runtime → seed**, so a proven composition is found before anything is generated. That
is also the cache in 5.8.5 — the same mechanism, now with a reason to rank what it holds.

### 5.10.5 WHERE THIS DESIGN CAN FAIL — two, in 5.8.3's spirit

**(a) IT IS A FEEDBACK LOOP.** Rising weight means being tried earlier, which means more chances to
settle, which raises the weight. **Early winners can lock in**, and the boards that came first would
shape the ranking more than the boards that came later. *Orders-never-excludes* bounds the damage —
nothing becomes unreachable — but it does not remove the loop. **The check is cheap and must be
pre-registered: report the table-stakes set's composition against GAME ORDER, and if it correlates
with which games ran first rather than with what the games need, the loop is what we are measuring.**

**(b) THE RANKING STOPS BEING REPRODUCIBLE FROM THE BOARD ALONE.** Two agents with different
histories rank the same gap differently. **That is the intended behaviour — it IS the learning — but
it means every A/B on retrieval from here on must state the library state on both arms**, and a
result compared against a cold baseline is comparing two things at once.

### 5.10.6 Measurement, pre-registered

    share of deltas answered from LEARNINGS      should RISE game over game, in sequence
    compositions reused in >= 3 distinct games   the table-stakes set -- report it, with game order
    the ablation                                 wipe learnings, re-run the same games; the gap is
                                                 what the carried library was worth

### 5.10.7 THE INVENTED-ATOM MEASUREMENT — the cleanest transfer evidence available

**Corpus atoms were FRONTLOADED, so using one proves LOOKUP, not learning.** An invented atom did
not exist until the agent made it, so its reuse cannot be explained by the frontload, by the corpus,
or by the key — **none of them contained it.**

    invented in game A, reused in game A        LEARNING
    invented in game A, used in game B          TRANSFER -- provably not corpus and not key
    remove invented atoms, re-run game B        the drop is what the agent taught itself

**Per run, into the ledger and the route chart:** atoms invented (count, per game) · each invented
atom's uses per game · **cross-game uses of invented atoms — the transfer count** · the
invented-atom ablation gap.

> **AND IT IS RUNNABLE NOW, WHICH THE Γ-WIPE ABLATION IS NOT.** `CLAUDE.md` defers clause 3 to 25/25
> because *wipe the library of an agent at 3/25 and it goes to 3/25 or lower, and neither number is
> interpretable — there was nothing worth wiping.* **The invented-atom ablation has a subject the
> moment ONE atom is invented**, because its question is not *did the library carry the win* but
> *did the agent's own additions do anything*. That question is interpretable at any level.
> **It is a smaller claim than clause 3 and it does not defer.**

### 5.10.8 CONFIDENCE AND RELEVANCE ARE TWO QUANTITIES — youth bonus, decay over games

**Isaiah, 2026-09-22: fix success tracking; balance rich-get-richer with a YOUTH BONUS and a DECAY
OF RELEVANCE over epochs or usage — never wall-clock. And an UNTESTED recipe must not be
downgraded, so decay may never touch belief.**

| | moves when | never moves when |
|---|---|---|
| **CONFIDENCE — does it work?** | expressed and confirmed; expressed and refuted | **not used. Disuse is not evidence.** |
| **RELEVANCE — how high does it rank now?** | cross-game success raises; games since last use lowers; youth bonus while barely tried | — |

#### The clocks, checked rather than assumed

**`gamma.tick` IS ALREADY CYCLES AND NOT WALL-CLOCK** — `tether.py:1304` sets
`self.gamma.tick = len(self.trace)`, so the existing `REJECTION_HALFLIFE = 8.0` decay is already
counted in steps taken. **Isaiah's never-wall-clock rule is honoured today; nothing has to change to
satisfy it.**

**What does NOT exist is a GAMES counter.** `tick` resets per run, so *games played since last use*
has nothing to read. That is the one new piece of state: an epoch counter on the learnings layer,
incremented per game, never per second.

#### CONFIDENCE — the Laplace posterior mean, and it has no free constant

    confidence = (confirmations + 1) / (confirmations + rejections + 2)

**Zero trials reads 0.5 — neither favoured nor penalised, which is Isaiah's clause 3 as arithmetic
rather than as a special case.** The `+1 / +2` is a uniform prior, not a tuning knob: there is no
value to fit and no number to defend.

#### YOUTH — `1 / (1 + trials)`, and WHY NOT the two better-known forms

    youth = 1 / (1 + confirmations + rejections)

1.0 untried, 0.5 after one trial, → 0. **No constant.** Large at zero and shrinking as evidence
accumulates, which is exactly what was asked for.

**NOT UCB1 (`sqrt(2 ln N / n)`), and the reason is not style.** It carries a constant, it is infinite
at `n = 0` and needs a special case — and its regret guarantee is for a bandit that makes ONE PULL
PER ROUND. **`retrieve` returns EVERY name, ordered. That is not the setting**, so importing the
form would import credibility the setting does not support. This file's own warning: a satisfying
borrowed story is harder to doubt than a bare number.

**NOT THOMPSON SAMPLING — `Beta(confirmations+1, rejections+1)`, ranked by a SAMPLE — even though it
is the most principled option available and has ZERO constants**, with the youth bonus falling out
as posterior variance rather than being added. **Its cost is that the ranking becomes STOCHASTIC,
and every A/B this seat runs depends on a deterministic ranking.** Recorded as the reviewer's call
rather than silently dropped: it is the better mechanism and the worse instrument.

#### RELEVANCE DECAY — a half-life in GAMES, one named constant

    relevance = confidence x 0.5 ** (games_since_last_use / RELEVANCE_HALFLIFE_GAMES) + youth

**Structurally identical to `REJECTION_HALFLIFE`, deliberately** — the codebase already has this
shape and a second clock idiom would be a second thing to reason about. **ONE constant, named and
PRE-REGISTERED rather than tuned**, per the instruction.

**It enters `fits()` as one more term beside type / arity / aimed / relational. It ORDERS AND NEVER
EXCLUDES** — `retrieve`'s every-name-comes-back contract stands, and decay never becomes refutation.

#### AND "NEVER EXCLUDES" ALREADY HAS ONE LIVE EXCEPTION, WHICH MUST BE NAMED RATHER THAN OVERLOOKED

`tether.py:2743` filters routine candidates by `self._rejection(...) < 1.0` — **an EXCLUSION, not an
ordering**, and its own comment says so: *"a refutation excludes only while its decaying strength
stands, so a failed shape leaves the running and returns."*

> **SO `Standing.decay()` IS THE REVERSIBILITY OF A REAL EXCLUSION, AND THAT CONSTRAINS THIS DESIGN.**
> The clean reading of the two-quantity split would move forgiveness out of confidence and into
> relevance — but doing that wholesale **turns the routine filter into a permanent ban**, which
> §18.2's *never a hard ban* forbids. **Either the decay stays where it is, or the routine filter
> moves to relevance in the same change. It cannot be half-done**, and I am flagging it rather than
> picking, because it is a behaviour change to a mechanism with a standing rationale.

#### Added to the pre-registration

    table-stakes set vs GAME ORDER          the feedback-loop check (5.10.5a), unchanged
    FIRST-TRIAL LATENCY                     cycles from a composition being minted or invented
                                            until it is first EXPRESSED -- with youth on and off.
                                            This is the quantity the youth bonus exists to move,
                                            and invented atoms are the population that needs it.

**Build order: AFTER the observer lands** — there is nothing to rank until settled compositions
exist. **Design only.**

---

### 5.10.9 THE `g.game` LEAK CHECK — RUN, and the answer is *latent, not absent*

**Ruling 7 asked whether the agent already holds the environment's game ID. Grepped, every consumer:**

| site | what it does with `self.game` | behaviour? |
|---|---|---|
| `gamma.py:333` | `self.game = str(game)` | — |
| `gamma.py:371` | `handles.setdefault(name, term.handle(self.game))` | **provenance label only** |
| `gamma.py:498` | writes `"game": self.game` into `save()` | persistence |
| `gamma.py:531` | `origin=IMPORTED if r.get("game") != self.game else r["origin"]` | **a STAMP on load** |
| `summary.py:156` | a `foreign` flag for reporting | measurement side |
| `feeder.py:250` | rotates `g.game` per cycle on the pooled tape | provenance rotation |

**AND NOTHING ELSE READS THEM.** `term.origin` is consumed at `gamma.py:361` (whether to assign a
handle at all), `:494` (skip priors when saving) and `:536` (a stamp); `tether.py` reads
`stamps[name]["seq"]` once and reads `handles` NEVER.

> **SO: `g.game` REACHES PROVENANCE LABELS, SAVE/LOAD STAMPING AND REPORTING. IT DOES NOT REACH
> RANKING, RETRIEVAL, BINDING, MINTING OR ACTION CHOICE. No contamination today.**

**BUT IT IS LATENT RATHER THAN ABSENT, AND THAT IS THE PART WORTH REPORTING.** `gamma.py:531` lets
the game NAME decide a term's origin stamp. **The moment origin or `settled_in` feeds the ranking —
which is exactly what 5.10 proposes — that stamp becomes a behaviour input and the leak is real.**

**The ruling therefore arrived one build early rather than one late.** 5.10 as I first drafted it
would have created the contamination it forbids (CONFLICTS c). The fix is structure hashes from the
start, not a later cleanup — a leak of this shape is invisible in results, because an agent doing
lookup on a given ID looks exactly like an agent that learned.

---

# Part 6 — THE `enumerate_closure` INVENTORY (step 1), and TWO DROPS THAT WOULD HAVE BROKEN THE GATE

**Isaiah, 2026-09-22: build on `composer.py`, port what is usable from `gamma.enumerate_closure`,
then delete it.** This is step 1 — what it does that the recipe composer does not, marked *port* or
*drop*. **Every row was settled by asking WHICH FUNCTION CONSUMES THIS QUANTITY AND WHAT IT READS**,
not by reading `enumerate_closure` and judging the feature.

## 6.1 THE TABLE

| what it does | consumer, grepped | verdict |
|---|---|---|
| **type validity** — `in_type in u.accepts`, `chain[-1].out_type in u.accepts` | the walk itself | **NOT A PORT — see 6.3** |
| **the abstention receipt** — `seen` · `budget_spent` · `depth_exhausted` | **`gate.py:203`**, `conform/kernel.py:541`, `ledger.py`'s park split | **PORT — load-bearing** |
| **`space_exact`** → `stats["estimate"]` → `coverage` | **`gate.py`'s `_unreached`** | **PORT — was on the drop list** |
| **ranking by fit** (`order=`) + the degenerate-ranking refusal | orders which candidates are reached inside budget | **PORT** |
| **the `idn` cut** — no identity inside a chain, 5.57x inflation | the coverage denominator | **PORT THE PRINCIPLE** |
| **`Term(chain)` construction** | everything downstream that executes a term | **PORT — composer returns dicts** |
| **laziness** (a generator; a yield is a reachability witness) | 5.8's whole lazy-generator requirement | **PORT — composer returns a list** |
| shortest-first BFS frontier | the walk | **DROP** — the recipe composer does not walk |
| `Config.budget` 4000 / `work_budget` 15000 | toy-world constants (1.4) | **DROP** |
| **operand / guard binding** | — | **NOT ITS TO PORT — see 6.2** |

## 6.2 A CORRECTION TO THE EXPECTED LIST: OPERAND/GUARD BINDING IS NOT IN `enumerate_closure`

The reviewer's 12:24 expected *operand/guard binding* among the port candidates. **It is not there.**
`gamma.units()` says so at its own site: *"`t.name` carries the operand binding and the emitted unit
does not … `enumerate_closure` composes over `.atoms` alone, so the chunk IS the atom sequence and
the operand has no business in the key."*

**Binding is re-decided per slot at MINT** (`tether.py:3280`), not during enumeration. So it is
untouched by the deletion and stays exactly where it is — which also means **conflict 4's
delta-bound applies to the mint loop and `_library_fit`, and NOT to the composer.**

## 6.3 THE TWO DROPS THAT WOULD HAVE BROKEN SOMETHING

**(a) `space_exact` WAS ON THE DROP LIST AND IT IS THE GATE'S DENOMINATOR.** `coverage = seen /
estimate`, and `estimate` is `space_exact`'s only product. `gate.py`'s `_unreached` REFUSES a run
whose park carries verdict `budget_spent` or `depth_exhausted` without a `coverage` in `[0,1]` plus
`units` and `depth`. Its docstring is the doctrine verbatim:

> *"A park that does not carry the fraction of the space actually seen is the stronger claim
> smuggled in wearing the weaker one's word, so the coverage number is required AT THE POINT OF
> REFUSAL, not in a later report."*

**That is `CLAUDE.md`'s *reach must be total* clause with a check behind it — *only a sealed room can
be searched to the end, so an abstention counts only when it names the closure it searched*.**
Dropping `space_exact` makes every abstention unreadable and fails the gate. **It must be ported in
a recipe-shaped form before anything is deleted.**

**(b) THE ABSTENTION RECEIPT HAS THREE CONSUMERS, NOT ZERO.** `budget_spent` / `depth_exhausted`
are read by `gate.py:203`, by a `conform/kernel.py` seat, and by `ledger.py`'s park-verdict split.
They are two DIFFERENT claims — *we stopped early* versus *we saw the whole space and it was not
there* — and only the second is an honest null.

> **THE RECIPE COMPOSER HAS NO EQUIVALENT OF EITHER, AND ITS DENOMINATOR IS EASIER, NOT HARDER:**
> the population is `len(recipe_rows())` = **2,061**, and *seen* is how many the delta lit. The
> `depth_exhausted` analogue is *every recipe whose ingredients the delta touched was considered*;
> `budget_spent` is *we stopped*. **Both remain checkable, and the numbers are smaller and more
> honest than a `λ^d` over a closure walk.**

## 6.4 TYPE VALIDITY IS NOT A PORT — IT IS THE BRIDGE, AND IT IS THE REAL WORK

`enumerate_closure` composes by TYPE: a chain extends only where `chain[-1].out_type` is accepted by
the next unit. **`composer.py` has no types at all** — its ingredients are STRINGS parsed out of a
markdown table (`Ct`, `Co`, `Ge`).

**AND THE TWO VOCABULARIES ARE DISJOINT BY NAME (`F164`).** Γ's atoms are `rotate`, `above`, `holes`,
`touching`; the closure's ingredient names are `Action`, `Node`, `Time`, `Flow`, `Edge`. **2,669
distinct ingredient names, and the overlap with Γ's typed atoms is the thing `F164` measured as
empty.**

> **SO THIS IS NOT CODE TO MOVE. A closure ingredient has no type because it has no BODY — it is a
> name, a condition and a recipe (the reviewer's 12:07 caveat).** Type-checking becomes portable
> only once a lit ingredient resolves to something executable, which is the CONDITION COMPILER
> (5.9.5) and dependency 1. **Until then the recipe composer is type-free by necessity rather than
> by omission, and saying "port the type checking" would schedule work that cannot be done.**

## 6.5 THE DELETION PRECONDITION — what must be true before `enumerate_closure` goes

Isaiah's step 5 is *then delete it*, and step 4 gates it on the route chart. **These are the checks
that say the port actually happened, each one a thing that breaks loudly if it did not:**

    1  `gate.py` passes with parks carrying `coverage` / `units` / `depth` from the recipe path
    2  the `conform/kernel.py` verdict seat passes on recipe-shaped parks
    3  `budget_spent` and `depth_exhausted` remain DISTINGUISHABLE and are both reachable
    4  the composer yields lazily and produces executable `Term`/`Node`, not dicts
    5  the route chart holds on three seeds: (c) shrinks, (a)/(b) grow, compositions do not fall

**Not before step 4 — deleting first leaves mint with nothing.** One commit, recoverable from
history, recorded in the ledger.

---

# Part 7 — PROCEDURALLY GENERATED GAMES (Isaiah, 2026-09-22)

**A game whose boards regenerate gives a NEW STRUCTURE HASH EVERY EPISODE.** Ruling 9.

## 7.1 The core loop is unaffected, and that is a property of the design rather than luck

**The delta keys recipes; it does not key game identity.** Nothing in route (a) → (b) → (c) consults
what world this is: the observer publishes what changed, the changed attributes light candidates,
the conditions confirm. **A regenerated board produces a different delta and the same machinery
reads it.** So procedural generation costs the loop nothing.

**AND EXACT-HASH RECALL FAILS — CORRECTLY.** A memorised route is useless on a regenerated board,
so a design that leaned on exact recall would be discovering that its recall was memorisation.
**The failure is the right one to have.**

## 7.2 Two levels of identity, because one hash answers two different questions

    LAYOUT HASH          the exact arrangement. Within-level recall: "I have seen THIS board."
                         Regenerates every episode on a procedural game, and should.
    MECHANICS SIGNATURE  object kinds, what each action does, what happens on contact --
                         LEARNED BY PLAYING, not read. "This is the same KIND of world."

**The mechanics signature is the one that carries transfer**, and it is the harder of the two
because it is not a function of the frame: it accumulates over a run as the agent discovers what its
actions do. **That makes it a product of route (a) — the action→delta record — rather than of
perception.**

## 7.3 RECOGNITION IS NEAREST MATCH, NOT EXACT MATCH

An exact-match key over a mechanics signature would fail on the first unobserved action, because the
signature is partial until the agent has tried everything. **Nearest match over a partial signature
is what makes it usable mid-episode**, and it is also what makes "the same kind of world" a
judgement the agent can be WRONG about — which is the legible failure mode, and the right one.

## 7.4 TRANSFER COUNTS ONLY WHEN MECHANICS DIFFER, AND THIS BITES NOW

**A composition reused on a regenerated layout of the same game is not transfer.** Counting it would
inflate the transfer number by exactly the regeneration rate, which is a number about the generator
rather than about the agent.

> **AND IT IS NOT A FUTURE PROBLEM: ARC LEVELS ALREADY VARY LAYOUT WITHIN A GAME.** So 5.10.7's
> transfer count must be keyed on the MECHANICS signature from the first measurement, or the first
> number it reports is already inflated. **This is the same error as pooling across games, one level
> in: a rate computed over a population the mechanism itself generates.**

## 7.5 What this adds to the build

    layout hash            a function of the frame -- cheap, and the observer already has the input
    mechanics signature    accumulated from route (a)'s action->delta record -- NOT built
    nearest match          over partial signatures -- NOT built, and it needs a distance

**The distance is the open question**: nearest-match needs a metric over partial mechanics
signatures, and choosing one is exactly the kind of invented number this project refuses. **The
corpus should be searched for it before one is designed** — the rule that has paid nine times.

---

# OPEN QUESTIONS — what is genuinely unresolved

1. **The nearest-match distance over mechanics signatures** (7.5). Search the corpus first.
2. **`r`'s bound** (5.8.3) — conditions are ruled as the bound; whether they bound it ENOUGH is
   unmeasurable until the condition compiler exists.
3. **Directed vs undirected relation slots** (CONFLICTS d) — symmetric relations do not need
   direction; asymmetric ones do, and they cannot reuse the built shape.
4. **Thompson vs deterministic ranking** (5.10.8) — the better mechanism against the better
   instrument, put to the reviewer and not yet ruled.
5. **How a lit aim becomes an ACTION** (4.7) — still the gap between lookup and play, and a route
   chart can show (b) growing while the agent plays no better.

**Everything else on the rulings list is either built, designed here, or named as a prerequisite.**

