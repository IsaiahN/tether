# The library — design record

**What this is:** the still-valid decisions and measurements from the 24 files in
`docs/library-closure/`, recombined into one document that lives beside the data. Each point names
its source and its status: **CURRENT**, **SUPERSEDED** (and by what), or **OPEN**. The data those
files held is now in `library/*.json`. LIBRARY_SPEC.md says how the library runs; this file says why
it is shaped the way it is.

Reviewer seat, 2026-10-08, at Isaiah's order to recombine, recontextualise and save in the library
folder so the old files can go.

---

## 1. What the library is

- **CURRENT.** It is the frontloaded human priors. Isaiah, 2026-09-22/23/27: "front load it with
  everything"; "why underprepare the rover"; molecules are preloaded examples of what could work.
  The bill is paid by inheritance, not re-evolved. *Supersedes* ATOMS.md's header line "the visible
  set, not the library; loading these as held terms would delete evidence the composition system
  works". (Sources: ATOMS.md header, LIBRARY_RETRIEVAL Part 12.)
- **CURRENT.** It has three layers. The seed is read-only; the runtime layer holds what the agent
  makes or carries; learnings are what the ground proved. Origins are PRIOR, MINTED, IMPORTED (across
  games, Isaiah 2026-10-07) and INVENTED. (LIBRARY_RETRIEVAL 2.4; rulings 2026-09-22.)
- **CURRENT.** It is one store, and every index is derived from it (Isaiah 2026-10-08; Figure 6).

## 2. The population, measured

- **CURRENT.** 2,694 entries in ATOMS.md across tiers 1–7 and 61 domains. 2,700 keys carry an
  attribute list. After the 2026-10-08 duplicate removal (139 removed, all logged), the library holds
  1,739 atoms and 2,164 molecules, plus 62 agent atoms and 66 relations. (ATOMS.md; ATTRIBUTES.md;
  DEDUP_LOG.json.)
- **CURRENT.** There is no irreducible core. Coverage grows about linearly, roughly 5 composites per
  atom added, because composition is local: 74% of ingredient references stay inside their own domain.
  The leverage is in the level-2 composites (about 200 used as ingredients), not in a small atom set.
  (COMPOSITE_REACH.md.)
- **CURRENT.** The atom list is mostly nouns. The verbs (Move, Grab, Release, Observe, Loop, Break,
  Cycle, Practice, Recovery) are tier-2 composites. With the role views (2026-10-08) every noun also
  reads as a verb, so this is no longer a gap in kind, only in what is named.
  (COMPOSITE_REACH.md; LIBRARY_SPEC 7.)

## 3. Attributes and reach

- **CURRENT.** Each atom row is a detector: attributes to check, plus a condition that confirms it
  (Solidity: `overlapArea == 0`). The conditions are effect shapes. (ATTRIBUTES.md.)
- **CURRENT.** Every atom is reachable. A scalar is a scalar: temperature, mass and health are
  magnitudes an object carries, shown as a palette band or an extent. The line is "measurable from
  outside" versus "reportable only from inside". The self-report family (75 mentions) was dropped
  without orphaning any atom. (ATTRIBUTE_REACH.md.)
- **CURRENT.** The reach tiers are kept per entry as `reach_tier`:
  - 0: today;
  - 1: a per-object integer;
  - 2: comparable vs orderable;
  - 3: objects and the predicate residual;
  - 4: a frame-level regularity.

  (ATTRIBUTE_REACH.json.)
- **CURRENT.** The attribute vocabulary clusters in three passes. The first two (form variants, head
  words) are mechanical; the third, 17 clusters, is ruled. Its rulings: `velocity` is SPEED;
  DIRECTION is split out; `delta` is CHANGE; `phase` is TIME. Now in `clusters.json` and on every
  entry's tags. (ATTRIBUTE_CLUSTERS.md/.json.)
- **OPEN.** Tags ending in `*` are 17 proposed clusters awaiting Isaiah's ruling. The README noted
  that `phase` in HEAT means matter-phase (a STATE), not TIME.
- **CURRENT.** Index lookups accumulate and never intersect. A delta decomposes (position change
  lights POSITION, MOTION, SPEED and DIRECTION); entries are ordered, never excluded. (inherited.py
  docstring; LIBRARY_SPEC 3.)

## 4. The grammar

- **CURRENT, now in `grammar.json`.** The operators come from the Operators table and Figure 12:
  - `+` conjunction;
  - `∥` disjunction;
  - `≡` identity;
  - `→` sequence;
  - `⇒` production;
  - `−` subtraction;
  - `⋛` comparison;
  - `¬` negation (unary).

  `+` was carrying seven meanings (2,111 of the recipes against 48 for every other operator), so it is
  read as `?` (UNKNOWN) until the ground settles it. The qualifiers `A(x)` and `A?` are not operators.
  (OPERATORS.md; Operators table.)
- **CURRENT.** NSM is the syntax:
  - substantives are the placeholder variables (existential SOMETHING, bound THIS, binding THE SAME,
    anti-binding OTHER);
  - frames carry arity, so a relation has a slot: `TOUCH(X, Y)`;
  - connectives are the operators.

  The full prime inventory and the 68 prepositions (as role markers) are now in `grammar.json`.
  (NSM_GRAMMAR.md; Isaiah 2026-10-08.)
- **OPEN.**
  - `∥` has no NSM prime (MAYBE is a different claim).
  - `∥` and `≡` carry second senses the corpus and the code disagree on (Operators table, open item).
  - The primes TRUE, CAN and KIND had no atom filling them.
- **CURRENT.** The chemistry mapping is Isaiah's nomenclature: element = atom, valence bond =
  operator, molecule = recipe. Isomers share ingredients and differ in bond and orientation;
  catalysts survive their own use; there is exactly one mutual cycle (Runaway ↔ Positive feedback);
  functional groups (`Momentum`, `Res`, `Damp`) fix a family and the qualifier picks the member.
  Isomers, cycles and orientation are in `index.json` and `orientation_draft.json`. (CHEMISTRY.md /
  _INSTANCES.json.)

## 5. Relations

- **CURRENT, now in `relations.json`.** The relation vocabulary between two objects (Parts 1–5):
  static, relative motion, constraint, force, interaction, non-rigid. Each is perceived, composable or
  blocked. Relations computed from the board are instruments, and they are perceived. (RELATIONS.md;
  VOCABULARY_FROZEN header.)
- **CURRENT.** Isaiah's observer schema (2026-09-15): every object carries the full attribute and
  relation set, NULL at frame 0, updated per frame; the delta is the cue. The specification is
  LIBRARY_SPEC 3; the readings are in `readings.json`. (RELATIONS.md, schema section.)

## 6. Structure across the library

- **CURRENT.** The domain graph is sparse (8%), connected and small-world (clustering 1.7× random;
  mean path 2.11). Hubs are Human, Phenomenological and Connection; the physics domains are leaves.
  Now derived as `index.domain_adjacency` (791 pairs under the library's full ingredient
  resolution, against 285 under ADJACENCY.md's strict rule). (ADJACENCY.md.)
- **CURRENT.** There are three edge types: ingredient, identity (≡, costs zero) and default (fires on
  absence: Commitment ⊣ Latency). The library records ingredient edges and ≡ candidates. Default
  edges are not yet recorded (**OPEN**). (ADJACENCY.md.)
- **CURRENT.** The six super-categories are a reading aid, not a search structure: 24% of edges are
  internal, against 17% at random. Traversal follows ingredients, not subject matter. (ADJACENCY.md;
  CATEGORIES.md.)
- **CURRENT.** Traversal belongs at entry level, not domain level. A refined path is a control loop
  with terminals. (TRAVERSAL.md.)
- **CURRENT.** The entry kinds (PROPERTY, OPERATION, RELATION, STATE, MECHANISM, MEASURE, BIAS,
  FAILURE MODE, DEFAULT) and the axes are a scheme. The 2026-10-08 role views cover what KIND was
  for, derived rather than hand-tagged. Arity is derivable. Bodily/Textual is not derivable and is
  **OPEN**. (ENTRY_CATEGORIES.md.)

## 7. Perception and the corpus narrative

- **CURRENT, corpus (Isaiah's).** The seven-layer pipeline:
  - the frame as a change-tracked tree (a MutationObserver);
  - reading order as a prior;
  - colour as order of encounter within a spectrum band (GB1, GB2), never a stored value;
  - objects, groups and subgroups;
  - attributes, relations and causality tracked in real time;
  - budget-sized bets;
  - persistence and cross-game import.

  (PERCEPTION_PIPELINE_general.md; "ARC GAMEPLAY — WHAT THE AGENT SEES.md", whose build-specific
  rewrite is docs/WHAT_THE_AGENT_SEES.md.)
- **OPEN, a conflict to rule.** The corpus models colour as a band plus encounter order, a
  disposable label with an order on the spectrum (ROYGBIV). Today's code and readings.json treat
  colour as the environment's palette index, with arithmetic allowed (reviewer ruling 2026-10-08).
  The corpus is Isaiah's, so the readings and the type should follow it once he confirms.
- **CURRENT, proposed principle, not a law.** Recursive transformation: time is known through change;
  space supplies relations; energy is conserved and directionless; gradients drive directed change;
  states and structures are different kinds of term that swap. It matches Figure 13's six.
  (RECURSIVE_TRANSFORMATION.md.)

## 8. Withdrawn, kept for provenance

- **SUPERSEDED 2026-09-22.** The 2026-09-14 vocabulary freeze. Isaiah: "get rid of the freeze.
  SENSORS ARE INSTRUMENTS." What still stands: a solution may test our instruments, and may never
  decide what the agent is given. (VOCABULARY_FROZEN.md, recorded in ISAIAH_RULINGS.)

## Figure census
Figure 6 (*"What is recorded only grows. What is reachable is derived"*: one store, derived
indexes); Figure 12 (the bond; *"which one holds is not recoverable from the operands"*); Figure 13
(*"The set is closed. The arrangements are not."*; the six). Strained: the colour conflict in §7 is
named, not resolved.
