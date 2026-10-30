# Item 5 — the codebase against the one library

Reviewer seat, 2026-10-08. Read at `seat-act` e50406d: docstrings, imports, call sites and data
paths of every library-adjacent module. **The finding in one line:** almost every piece of Isaiah's
design exists somewhere in the code, in two or three partial copies, and the pieces do not reach one
another. The work is joining and deduplicating, not inventing.

## Component by component

| what the library needs (LIBRARY_SPEC) | what the code has | status | action |
|---|---|---|---|
| **One store** | `composer.py`, `condition.py`, `mapping.py`, `self_graded.py`, `detectors.py` read `docs/library-closure/` (ATOMS.md, ATTRIBUTES.md, ATTRIBUTE_INDEX.json, WORKING_SET.json); `inherited.py`, `kaggle_bundle.py` read `library/*.json` | **duplicate** | all read `library/` (spec §5 #1) |
| **The readings floor** | **three partial copies**: `arc_atoms.ATTRIBUTE_TYPE` + `ATTRIBUTE_ARM` (live); `observer.py`'s "frozen 8" (the freeze was withdrawn 2026-09-22); `sensors_heavy.py` (reviewer 2026-09-23: "SUPERSEDED, AND PENDING DELETION", still in the tree) | **duplicate + stale** | `readings.json` is the one table; `ATTRIBUTE_TYPE` is derived from it; observer reads it; delete `sensors_heavy.py` |
| **The observer** (full vector, NULL at frame 0, change = cue) | `observer.py` + `observer.Live` in `arc_world` (live since 2026-09-26); the cue is stored as `Agent.cue`; `tether._came/_gone` | **partial** | the vector is the frozen 8 plus relations. Widen it to `readings.json` and emit the changed-reading dict |
| **Lighting** (the cue lights tagged entries; never exclude) | **four overlapping mechanisms**: `inherited.reach/tags_of` (by tag; its ONLY consumer is the curiosity aim, tether.py:3524); `composer.lookup` (F508, per-residual, via ATTRIBUTE_INDEX encodings); `detectors.light_*` (hand-written predicates per target atom); `mapping.map_answer_key` (lint-fenced as a cue module) | **duplicate; the main path never reaches the library** | ONE: `Library.light(changed)` over `index.by_reading_reads`, queried with the residual's scoped description (`retrieval.characterise`), feeding the reach site (spec §5 #4). Retire `detectors.light_*` (hand predicates) and `inherited.reach` |
| **Candidate conditions, no hand functions** | `detectors.py` encodes conditions BY HAND per atom ("a new atom is admitted by naming its condition"); `condition.py` parses the grammar (keep) | **violates the generator rule** | the template family generates them (`Library.candidates` / `view`); `condition.py` stays the parser and evaluator |
| **Composition** | `composer.Bonded`, `bind(bond, l, r)`, `settle`, `holds` (the 7 bond tests), `settle_tree` | **exists, correct** | keep as the ONE bind. Switch `recipe_rows/light/candidates` from parsing ATOMS.md to `molecules.json` `run.operands`/`junctions` (orientation included) |
| **Registry growth** (new atoms fire like preloaded ones) | `gamma.Gamma`: `self.atoms`/`_by_name` fixed at construction; `build()` makes Terms from existing atom names only | **missing** | `Gamma.register(entry)`: the callable is GENERATED (`condition.evaluate` over the entry's candidate; `bind` over operands) (spec §5 #3) |
| **MINTED** | `gamma.library` Terms, minted and settled; `Standing` | **exists** | minted terms also land in the library runtime layer (same schema), so they light and compose like seed entries |
| **INVENTED** | none: "the agent cannot create an atom" (LIBRARY_RETRIEVAL 5.9.6); the trigger `owed_import` is named, not built | **missing** | `Library.invent_atom` + `Gamma.register`; the trigger is an abstention receipt |
| **IMPORTED** (across games) | `gamma.save/load`, carry-fidelity work, provenance kept | **exists** | carried entries keep `origin` and `born`; binding re-decided at the destination |
| **Roles** (state, process, cause …) | none | **missing** | `Library.view` / `role_table` (built, reference) |
| **Frames and prepositions** (NSM) | `grammar.py` is the UTTERANCE grammar (PERCEIVE / BET / ACT records), a different thing; no NSM frame layer | **missing** | `grammar.json` frames, primes and prepositions; a frame type in the composition layer is the open question NSM_GRAMMAR raised (Gamma's or grammar.py's) — for the seat to propose |
| **Agent's own retrieval** | `retrieval.characterise/fits/retrieve` over `gamma.library` | **exists** | keep. It supplies the residual's description that `light` is queried with |
| **Priors** | `priors.py` loads shapes from ARC_HUMAN_PRIORS.md | **exists** | keep; the source moves to `library/sources/` |
| **Curriculum** | `self_graded.py` reads WORKING_SET.json | **exists** | read the `working_set` flags in the library |
| **Kaggle bundle** | ships `library/{molecules,tag_index,domains,agent_atoms}.json` | **partial** | ship `library/` whole (readings, grammar, relations, clusters, index) |
| **Gate** | 23 seats; none checks the library | **missing** | the seat check in spec §5 #8, plus `fast_check.py` (item 10) |

## The three things that matter most

1. **The cue never reaches the library on the main path.** The observer is live and the agent
   stores `self.cue`, but the only consumer is the curiosity aim. The reach site uses
   `composer.lookup` over a different index. The mapping Isaiah designed on 2026-09-15 has been
   half-built since 2026-09-26, and the code says so itself ("NO CONSUMER YET, AND SAYING SO IS THE
   POINT"). Joining `self.cue` → `Library.light` → the reach is the change that makes the 4,000
   entries matter.
2. **Atoms cannot be added at run time.** Gamma's registry is fixed at construction, so nothing the
   agent invents can ever fire as a function. `Gamma.register` is the smallest change with the
   largest consequence for Isaiah's "the agent builds new atoms that fire like the preloaded ones".
3. **Conditions are hand-written where they exist** (`detectors.py`). That is the 2,700-functions
   path in miniature. The template family replaces it.

## Figure census
Figure 11 (*"An improvement that does not change contact changes nothing"*: a cue with no consumer
is that case); Figure 6 (one store); Figure 12 (*"A settled molecule becomes an atom for whatever
composes over it"*: needs a registry that can grow). Strained: none.
