# Item 3 — the docs folder, every file

Reviewer seat, 2026-10-08. The status facts come from the seat's inventory (Drive, 08:27, 67
files, each backed by a grep or header), checked against the code at `seat-act` e50406d. The
verdicts are mine, by the figures and Isaiah's rulings.

**Rules for the verdicts:**
- **Corpus is Isaiah's.** It is never deleted for age. At most it moves.
- **Deleting is safe only when two things hold:** the content lives somewhere stated, and nothing
  loads the file. Git history keeps every deleted file at the commit named in the deletion message.
- Figure 6: *"What is recorded only grows. What is reachable is derived."* The record is git and
  the library; a stale doc in the working tree is a second, contradicting store.

Verdicts: **KEEP** · **KEEP, UPDATE** · **MOVE** (to `library/` or `docs/corpus/`) · **DELETE**
(content captured; safe) · **DELETE AFTER** (after a named code change lands).

---

## A. `docs/library-closure/` — 24 files: the library's sources. Data → `library/`; design → `library/LIBRARY_DESIGN.md`

| file | verdict | where its content lives now |
|---|---|---|
| ATOMS.md | **MOVE** → `library/sources/ATOMS.md` | every entry is in atoms.json / molecules.json with `sources` pointing at its line; kept as the seed's source text. Loaded by composer.py, condition.py, kaggle_bundle.py until code change #1 |
| ATTRIBUTES.md | **DELETE AFTER** code change #1 | attributes and conditions are on every entry (`attributes`, `condition`); the argument is LIBRARY_DESIGN §3. Loaded by condition.py today |
| ATTRIBUTE_INDEX.json | **DELETE AFTER** #1 | `index.by_attribute`, `by_tag`, entry `encodings`. Read by composer.py today |
| ATTRIBUTE_REACH.json, .md | **DELETE** | `reach_tier`/`encodings` on entries; argument in LIBRARY_DESIGN §3 |
| ATTRIBUTE_CLUSTERS.json, .md | **DELETE** | `library/clusters.json` (whole vocabulary), entry tags; rulings in LIBRARY_DESIGN §3 |
| ATOM_RANKING.json | **DELETE** | `index.use_ranking` (derived) |
| ADJACENCY.md, ADJACENCY_EDGES.json | **DELETE** | `index.domain_adjacency` (derived); findings in LIBRARY_DESIGN §6 |
| CATEGORIES.md | **DELETE** | `domains.json` (super-category per domain); findings in LIBRARY_DESIGN §6 |
| ENTRY_CATEGORIES.md | **DELETE** | role views replace KIND, derived (LIBRARY_SPEC §7); open axes in LIBRARY_DESIGN §6 |
| CHEMISTRY.md, CHEMISTRY_INSTANCES.json | **DELETE** | `index.isomers`, `index.mutual_cycles`, entry `chemistry` fields, orientation_draft.json; nomenclature in LIBRARY_DESIGN §4 |
| COMPOSITE_REACH.md | **DELETE** | LIBRARY_DESIGN §2 |
| WORKING_SET.json | **DELETE AFTER** #1 | entry `working_set` flags (390), roots in domains.json. Loaded by self_graded.py today |
| NSM_GRAMMAR.md | **DELETE** | `grammar.json` (frames, full primes, prepositions, roles); open items in LIBRARY_DESIGN §4 |
| OPERATORS.md | **DELETE** | `grammar.json` operators (verbatim from the Operators table, which governs); LIBRARY_DESIGN §4 |
| RELATIONS.md | **DELETE AFTER** comments updated | `relations.json`, `readings.json`; schema in LIBRARY_SPEC §3. Cited in comments of 7 .py files; repoint them to LIBRARY_SPEC |
| TRAVERSAL.md | **DELETE** | LIBRARY_DESIGN §6 |
| VOCABULARY_FROZEN.md | **DELETE** | withdrawn 2026-09-22; recorded in ISAIAH_RULINGS and LIBRARY_DESIGN §8 |
| PERCEPTION_PIPELINE_general.md | **MOVE** → `docs/corpus/` | Isaiah's corpus spec; summarised in LIBRARY_DESIGN §7 |
| ARC GAMEPLAY - WHAT THE AGENT SEES.md | **MOVE** → `docs/corpus/` | Isaiah's corpus narrative |
| RECURSIVE_TRANSFORMATION.md | **MOVE** → `docs/corpus/` | proposed principle; LIBRARY_DESIGN §7 |

## B. `docs/` top level — 40 files

| file | verdict | why / where |
|---|---|---|
| THE_MISSION_north_star.md, THE_TERMINAL_CONDITION.md, THE_ALIGNMENT.md | **KEEP** (corpus, required reading) | — |
| THE_SEAT_MAP_Field_Guide_amended.md | **KEEP** (corpus) | carry Isaiah's arc-agent wording (the seat edited one line; corpus is annotated, not edited) |
| THE_FORMULA.md | **KEEP** | in use; the figures govern it |
| ISAIAH_RULINGS.md | **KEEP, UPDATE** | item 9 |
| INDEX.md | **KEEP** | the finding log, required reading |
| SEAT_ORIENTATION.md | **KEEP, UPDATE** | point to `library/LIBRARY_SPEC.md` and `LIBRARY_DESIGN.md`; no game testing until the library is in (Isaiah 2026-10-08) |
| ARC_AGENT.md, DISCOVERY.md, DOCTRINE_AUDIT.md, FALSE_MINT.md, PHILOSOPHY.md, SNAPS_PLAN.md, BUILD_PLAN.md | **KEEP** (corpus) | — |
| ACTION_INTERFACE_PLAN.md | **KEEP** | the spec cited by the code |
| M2_STANDARD.md | **KEEP** | the standard the M2 suites cite |
| LIBRARY_VS_COMPOSER.md, `outputs are not generators.md` | **KEEP** | Isaiah's essays |
| CONFLATIONS.md | **KEEP** | an unbuilt linter spec cited by kernel.py |
| WHAT_THE_AGENT_SEES.md | **KEEP** | cited by code and docs |
| PHASE2_GUIDE_CURRICULUM.md | **KEEP** | future phase, paused |
| ARC_BUILD_PLAN.md | **KEEP, UPDATE** | mark its superseded parts in place |
| TRAINING_PLAN.md | **KEEP, UPDATE** | cited by 11 .py files; its library sections now point to LIBRARY_SPEC; its stages predate today's order |
| LIBRARY_RETRIEVAL.md | **DELETE AFTER** its rulings are confirmed in ISAIAH_RULINGS (item 9) | the 2026-09-22 rulings index → ISAIAH_RULINGS; the plan (generators, layers, observer) → LIBRARY_SPEC; the gap table is superseded by LIBRARY_SPEC §5 |
| ARC_HUMAN_PRIORS.md | **MOVE** → `library/sources/` | the citation source for the HUMAN tier-1 priors (priors.py line 1) |
| DECOMPOSITION.md | **KEEP** | still cited (2026-09-22); not superseded |
| REPAIRS.md, M2_PHASES.md | **KEEP** (historical record, cited by INDEX) | small; deleting gains little |
| LEDGER.md | **DELETE** | stale since 2026-09-22; open items live in INDEX and the channel |
| PERCEPTION_BUILD_PLAN.md | **DELETE** | its own header: "SUPERSEDED ... not to be worked from" (by LIBRARY_RETRIEVAL, now LIBRARY_SPEC) |
| DEMAND_LOG.md | **DELETE** | superseded by demand.py; its premise (the frozen vocabulary) was withdrawn |
| CODE_AUDIT.md, FREEZE_READ.md, POST_FREEZE_QUEUE.md, PREREG_DEREFERENCE.md, SELF_GRADED_CURRICULUM.md | **DELETE** | finished or self-marked closed; nothing loads them |
| STORY_PROOF.md, WINDOW_REPORT.md | **DELETE**, and repoint CLAUDE.md's "lesson" citations to the deleting commit | self-marked stale; kept only as lessons, and git keeps them |
| README.md | **DELETE**, replace with a 10-line `docs/README.md` listing the current reading order | lists 4 of 40 files |

## C. `docs/example/` — 3 notebooks

**KEEP.** kaggle_bundle.py loads the random-agent notebook; the other two are reference.

---

## The deletion list, in order

1. **Now, safe:** in `library-closure/`:
   - ATTRIBUTE_REACH.json and .md
   - ATTRIBUTE_CLUSTERS.json and .md
   - ATOM_RANKING.json
   - ADJACENCY.md and ADJACENCY_EDGES.json
   - CATEGORIES.md
   - ENTRY_CATEGORIES.md
   - CHEMISTRY.md and CHEMISTRY_INSTANCES.json
   - COMPOSITE_REACH.md
   - NSM_GRAMMAR.md
   - OPERATORS.md
   - TRAVERSAL.md
   - VOCABULARY_FROZEN.md

   In `docs/`:
   - LEDGER.md
   - PERCEPTION_BUILD_PLAN.md
   - DEMAND_LOG.md
   - CODE_AUDIT.md
   - FREEZE_READ.md
   - POST_FREEZE_QUEUE.md
   - PREREG_DEREFERENCE.md
   - SELF_GRADED_CURRICULUM.md
   - STORY_PROOF.md
   - WINDOW_REPORT.md
   - README.md

   That is **27 files**, deleted with the new `library/` files in place.
2. **After code change #1** (every module reads `library/`): ATTRIBUTES.md, ATTRIBUTE_INDEX.json,
   WORKING_SET.json. That is **3**.
3. **After the code comments are repointed:** RELATIONS.md. That is **1**.
4. **After item 9 confirms its rulings:** LIBRARY_RETRIEVAL.md. That is **1**.
5. **Moves:**
   - ATOMS.md and ARC_HUMAN_PRIORS.md → `library/sources/`;
   - the three corpus narratives → `docs/corpus/`.

The result: `docs/library-closure/` is gone, the library is one folder, and `docs/` holds corpus,
current plans and the record.

## Figure census
Figure 6 (*"What is recorded only grows. What is reachable is derived"*); Figure 10 (*"a convention
nothing can check is a constant the seat authored"*: a stale doc beside a live one is an unchecked
second claim). Strained: none.
