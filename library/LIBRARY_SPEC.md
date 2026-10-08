# The one library — what it holds, how every entry runs, how the search narrows, how the agent adds to it

Reviewer seat, 2026-10-08, at Isaiah's order. Line of record: `seat-act` e50406d.
Files in this folder go into the repo's `library/`. The seat owns the build; the reviewer rules on
figure conformance. **No game testing until this is in and working** (Isaiah, 2026-10-08).

---

## 1. One store

**Everything the agent is preloaded with, atoms or recipes, is in `library/`.** Every index is
derived from it by `build_library.py` and regenerated, never edited by hand (Figure 6: *"What is
recorded only grows. What is reachable is derived"*).

| file | holds | kind |
|---|---|---|
| `readings.json` | **the floor**: 36 quantities perceived or told, per object, pair, event, board, with type and live status | authored, from `arc_atoms.ATTRIBUTE_TYPE` and the arms |
| `grammar.json` | the eight operators, `?` (unknown bond), the two qualifiers, the NSM frames, the loop's symbols, the six substrate terms | authored, verbatim from the Operators and Symbols tables and Figures 12–13 |
| `atoms.json` | 1,748 GIVEN atoms (586 defined, 42 attribute-only, 1,120 implicit) | seed |
| `molecules.json` | 2,294 GIVEN molecules | seed |
| `agent_atoms.json` | 62 BUILT executable atoms (kept apart for the ablation) | seed |
| `relations.json` | 66 relations (RELATIONS.md Parts 1–5) | seed |
| `grid_groundings.json` | what each atom is in a 2D grid world | seed (reviewer, 2026-10-08) |
| `index.json` | by_reading (weighted), by_tag, by_grid_term, by_substrate, by_kind, by_domain, by_attribute, ingredient_of, isomers, identity_candidates, same_name_across_domains | **derived** |
| `runtime.json` | what the agent made or carried this run | runtime layer |
| `learnings.json` | promoted when proven by the ground | learnings layer |
| `BUILD_REPORT.md` | counts and every unresolved item, named | derived |

**What this replaces.** The code reads the library from two places today: `composer.py`,
`condition.py`, `mapping.py`, `self_graded.py` read `docs/library-closure/` (ATOMS.md,
ATTRIBUTES.md, ATTRIBUTE_INDEX.json, WORKING_SET.json); `inherited.py` and `kaggle_bundle.py` read
`library/*.json`. Same population, two stores — the duplicate Isaiah named. After this, all of them
read `library/`; `docs/library-closure/` keeps the source texts as provenance only.
`tag_index.json` is superseded by `index.json` (its `by_tag` and `by_attribute` are in it).

---

## 2. Every entry, and its one way to run

Every entry carries: `kind`, `grid` (what it is in a 2D grid world), `reads` (readings whose change
lights it — it is *affected by* them; weighted 1.0 from its grid meaning, 0.5 from its tags and
encodings), `affects` (readings it changes when it holds — operations only), `substrate` (Figure
13's six, through its readings), and `run`:

| route | kinds | how it runs | no hand-written function because |
|---|---|---|---|
| **PRIMITIVE** | the 62 agent atoms | `arc_atoms` builds the callable | they are the floor's operations |
| **GROUNDED** | 1,748 PERCEPT atoms, 66 RELATIONS | ONE generator, `candidates()`, turns `reads` into candidate conditions from a template family per reading TYPE; the agent's bargain picks which (if any) holds on this board | the family is the grammar applied to the type, the same few templates for every entry |
| **COMPOSED** | 2,294 molecules | operands in written order; junctions carry their bond, `?` where the source wrote `+`; ONE `bind(bond, l, r)` (composer.py) | the bond is a parameter, not a function |

**The template family** (`library_runtime.TEMPLATES`), written in `condition.py`'s grammar — all
23,029 candidates generated over the seed parse with the repo's parser:

| type | candidates |
|---|---|
| DELTA | moves `o.r != 0`, up `> 0`, down `< 0` |
| EXTENT | more / less / same against another object, present `> 0` |
| POSITION | before / after / level against another object |
| COLOUR | same / other |
| SHAPE | same / other — **nominal: no order, no arithmetic** (ruling 2026-10-08) |
| BOOL | holds / fails |
| PRED (pair) | `touching(o, x) == 1` / `== 0` |
| pair EXTENT | `contact(o, x) > 0` / `== 0` |
| board | `board.completed > 0` |
| event | `frame.came > 0`, `frame.gone > 0` |
| context (`action`, `press`) | none — these are GUARDS, `When(P, R)` |
| operand (`prev`) | none — offered to the binder as an operand |

**The term is the pair** (entry, candidate) — Figure 13: *"That record is not documentation of the
term. It is the term."* A candidate is the agent's hypothesis, priced, kept only if it pays
(ruling 5, 2026-09-22; Figure 5: *"does the new term cost less to state than the confusion it
removes?"*). Nothing in the library asserts a candidate true.

**Isomers.** 170 families share an ingredient set; the bond tells them apart (Figure 12, CHEMISTRY.md).
**Identity.** 256 `≡` candidates (truncated forms in one domain) and 222 names shared across domains
are listed for the retrieval layer; nothing is deleted (Isaiah 2026-09-22: `≡` rather than deletion).

---

## 3. The search index and the mutation observer (item 6)

**The mapping, not a search** (RELATIONS.md schema, Isaiah 2026-09-15; LIBRARY_RETRIEVAL 5.2,
2026-09-22). Per frame:

1. **The observer is the tracker.** Every tracked object carries its full reading vector from
   `readings.json`, **NULL at frame 0**, updated from frame 1; *null, not absent*.
2. **The change is the cue.** The frame's delta is the set of readings that moved, per slot.
3. **Light.** `Library.light(changed)` reads `index.by_reading_reads[r]` for each changed reading and
   ranks entries by the weighted share of the change they read. Molecules are never lit directly.
4. **Confirm.** Each lit entry's candidates are evaluated three-valued (`condition.evaluate`:
   True / False / None) on the frame — the reader maps `touching(a, b)` to `a~b.touching`,
   `board.completed` to `@goal.completed`, `frame.came` to the frame's events.
5. **Compose.** `Library.molecules_lit(confirmed)` walks `ingredient_of` up to the molecules whose
   operands are all lit; their junctions settle by Figure 12's tests over the residual's frames
   (`composer.settle_tree`).
6. **Offer, never exclude.** The ranked entries and molecules go to the mint as ORDERED operand and
   term candidates — the F510 ordering's place (contact first, then the library's partner, then
   variance). Figure 9: *"keep every cut ranked and reversible"*.

**Updated on every addition**: `invent_atom` and `mint_recipe` index the new entry at once.

---

## 4. The agent adds to the library (item 7)

| origin | what | trigger | lands in |
|---|---|---|---|
| **PRIOR** | the seed | — | read-only forever |
| **MINTED** | a new arrangement of existing entries, in the agent's grammar (operands + bonds) | a residual a composition pays for | runtime |
| **INVENTED** | a new primitive the agent NAMES (the name is arbitrary; its identity is the observed pattern), grounded in readings | an abstention receipt — `owed_import`: *I observed this and could not compose it* (LIBRARY_RETRIEVAL 5.9.6) | runtime |
| **IMPORTED** | an entry carried into the next game (Isaiah 2026-10-07: import = across games) | the run moving on | runtime, status marked |

Both new kinds use the seed's schema, are indexed at once, and run through the same path as
preloaded entries (Figure 12: *"A settled molecule becomes an atom for whatever composes over it"*).
Standing is earned from the ground like everything else — no head start for being the agent's own.
If a later growth makes an invention composable, record `≡` and **keep** the invention (its date
is evidence). Ablation: wipe `learnings.json`, keep the seed, re-run.

---

## 5. What the code must change (item 5), in order, each its own commit with fixtures

| # | change | where | why |
|---|---|---|---|
| 1 | read the library from `library/` only; `docs/library-closure/` becomes provenance text | composer.py `_ATOMS_MD`/`_INDEX_JSON`, condition.py `corpus_glosses`, mapping.py, self_graded.py, detectors.py | one store (Figure 6) |
| 2 | `inherited.py` reads `index.json` | inherited.py | tag_index superseded |
| 3 | **REVISED 2026-10-08, see METAPROGRAMMING_DESIGN §0: no `Gamma.register`; a COMPILER turns candidates into Terms over Γ's existing atoms, and adoption goes through the mint.** (Original:) **`Gamma.register(entry)`** — the atom registry grows at run time; the callable is GENERATED from the entry (`condition.evaluate` over its candidate for GROUNDED, `bind` over its operands for COMPOSED) | gamma.py (`self.atoms`/`_by_name` are fixed at construction today: "the agent cannot create an atom", LIBRARY_RETRIEVAL 5.9.6) | Isaiah's "fire as a new function in the metafunction list, just like the preloaded ones" |
| 4 | the reach site lights from the frame's change via `Library.light` and offers candidates and `molecules_lit` to the mint, ordered | tether.py (`composer.lookup` call at the reach) | section 3 |
| 5 | the observer publishes the full vector of `readings.json`, NULL at frame 0, and emits the changed-reading dict | arc_percept / arc_world (the tracker) | section 3 step 1 |
| 6 | runtime and learnings layers persisted; promotion reuses `gamma.Standing` | gamma.py save/load, library_runtime | section 4 |
| 7 | the Kaggle bundle ships `library/` whole | kaggle_bundle.py | the agent travels with its library |
| 8 | a seat check: `build_library.py --check` reproduces `index.json`; every entry has a route; every candidate parses; every `reads` is a reading | conform/ | derived means checkable (Figure 10: *"a convention nothing can check is a constant the seat authored"*) |

**Acceptance (fixtures only, no game runs):** `library_runtime._selftest` (11 checks, all pass);
the parse census (23,029 of 23,029); a fixture that a planted mutation lights the expected entry
and offers the expected molecule; a fixture that an invented atom and a minted recipe register in
Gamma and produce a value through the generated callable; a must-fail for each.

---

## 6. Open items, named

- **181 atoms name no reading** — reachable by name and recipe only. The first to sharpen.
- **22 recipes** carry operators the parser could not place; their junctions are all `?`.
- **`∥` and `≡` second senses** — the Operators table's own open item.
- **`count` has no type** in the importable set (EXTENT stands in, recorded at `arc_atoms`).
- **`level`** is planned, not published.

## Figure census
Figure 6 (*"What is recorded only grows. What is reachable is derived"*; *"already returning
something"*); Figure 5 (the bargain); Figure 9 (*"keep every cut ranked and reversible"*); Figure 12
(the bond; *"which one holds is not recoverable from the operands"*; *"A settled molecule becomes an
atom"*); Figure 13 (*"It is the term"*; the six substrate terms); Figure 10 (checkable
conventions). Strained: none.

---

## 7. Roles, prepositions and orientation (added 2026-10-08, at Isaiah's direction)

**One atom, several views.** Isaiah's point was effect and affect: the noun and the verb are one
concept. `Library.view(key, role)` gives any entry's candidates in a role, from the same `reads` and
the same template family, so nothing is authored per entry:

| role | the view | example (Contagion) |
|---|---|---|
| STATE, TEST, RULE | its value this frame (TEST is the verdict; RULE holds on every frame) | `touching(o1, o2) == 1` |
| PROCESS | its change across frames: what it changes first, then the deltas of what it reads ("contagion *of* x") | `o1.colour_changed == 1` |
| RELATION, MEASURE | measured against a second object ("from a to b"; "how far") | `contact(o1, o2) > 0` |
| CAUSE, AGENT | a state of o followed by a change of x (production ⇒) | `touching(o1, o2) == 1 ⇒ o2.colour_changed == 1` |
| RESULT | a change of o following a state of x | — |
| INSTRUMENT | the change happens to o only while x takes part ("done *with*") | — |

All 311,572 role-view conditions over the seed parse with the repo's `condition.py`.

**The held pairs are now base plus role.** Of the 151 pairs still held after the duplicate passes,
71 are one concept in two roles. The longer entry keeps its place and gains `role_of`
{base, role, marker}, for example Contagion spread = Contagion in its PROCESS role, Damping material =
Damping, INSTRUMENT, Fidelity test = Fidelity, TEST, and Exploration drive = Exploration, CAUSE.
**80 remain distinct concepts** (Tissue engineering, Simulation argument, Courage under fire),
listed in `ROLES_LOG.json` and not guessed at. Every role assignment is a draft.

**Prepositions.** `grammar.json` gains all 68 prepositions Isaiah listed, each a ROLE MARKER on a
frame slot, with:
- the NSM prime or primes it decomposes into;
- the operator it realises;
- the readings it reads;
- its meaning in the grid.

For example, *into* = MOVE + INSIDE (→), *toward* = MOVE + NEAR (more) (⋛), *without* (−),
*than*/*versus* (⋛), *despite* (¬ of what was expected), *of* (patient). `grammar.json` also holds
the full NSM prime inventory. NSM_GRAMMAR.md used about 24 primes; the missing time, space, quantity
and mental primes are the ones the prepositions decompose into.

**Orientation.** The look-alike families are now counted with qualifiers and written order included.
Of the 68 first reported:
- 31 were already told apart by their qualifiers;
- 24 were misspelled or retitled twins, now removed (pass 4);
- 2 are role pairs (Mastery / The mastery path; Craft / The craftsman);
- 11 needed orientation.

`orientation_draft.json` supplies it for those 11 from a closed set: rising/falling, from X to Y,
before/after, oldest-first/newest-first, plus the bond. For example Melt = Temperature(rising,
crosses melting point) ⇒ Phase(from solid to liquid), and Traverse = Node(from) → Edge(along) →
Node(to). Each is marked as a DRAFT for Isaiah, and the ground still settles each junction.

**Every entry now carries its role table** (Isaiah, 2026-10-08: "make sure all the other atoms get
those distinctions"). The build writes `roles` on every atom, molecule, relation and agent atom:
`default` (derived, never authored), `available` (the number of candidates in each of the ten roles),
and `example` (the first candidate for STATE, PROCESS, RELATION, MEASURE and CAUSE).
`index.by_default_role` groups all entries by their default role.

To make that complete:
- **The 180 atoms that named no reading were rewritten in perceivable terms**
  (`sharpened_2026_10_08.txt`, with explicit readings in `reads_explicit.json`). For example,
  Authority = "an object whose state controls others: when it changes, others change on the same
  turn".
- **The floor gained the agent's own record** (residual, prediction, standing, library size), so
  atoms about rules, beliefs and learning read something real.
- **It also gained the observer's per-attribute changes** (progress, contact, containment, residual,
  standing, library size), each marked *planned*, per Isaiah's rule that every attribute's change is
  the cue.

Over all 3,969 grounded and composed entries, every role view is non-empty except RELATION (154
entries) and MEASURE (109), which are board-level or self-level entries with no second object.
Every condition sampled (1.45 million) parses with `condition.py`.

**New entries get all of this automatically.** `Library.role_table(key)` is ONE function, used by
the build for the 4,000 preloaded entries and by `invent_atom` / `mint_recipe` for every new one. A
new entry needs nothing per role:
- an atom the agent invents needs only the condition it was formed from (its `reads` are parsed out
  of it) and, if it changes something, `affects`;
- a recipe it mints inherits its operands' readings.

The roles, the template family and the default role all follow from those. A human-added atom
needs a grid meaning; the build's tagger and `reads_explicit.json` give its readings.


## 8. What crosses an episode (Isaiah, 2026-10-08)

*"the colors are changing everytime the game loads so anyting that stores that would be problematic.
you might even assume objects are randomly arranged on the private OOD board or the entire rotated or
shrank for instance all in service of showing that your generalizing"*

- **Colour is an episode-local label.** It is named by order of encounter within its spectrum band
  (the corpus, PERCEPTION_PIPELINE Layer 3), compared same/other only, with no arithmetic, and never
  stored across episodes.
- **No raw value crosses.** `carry_check` refuses to carry any condition that compares a reading with
  a literal other than 0, or 1 on a boolean: that is a recording of one occasion (Figure 4: *"A
  recording carried upward looks like knowledge and is a description of one occasion"*). It stays in
  its episode, with its reason recorded.
- **Every generated candidate is value-free by construction.** All 125,655 of them compare objects
  with each other, never with a constant, so every one can cross.
- **Turned, mirrored and shrunk boards.** `axis_forms` offers a carried rule in its turned and
  mirrored forms (axes swapped, orderings reversed, alone and together), and the ground at the
  destination decides which holds. Scale needs nothing, because nothing compares against a size. This
  is the Symbols table's T_A (*"Detail is thrown away, which is what makes the result reusable"*)
  and F (the frame transform).
- **For the code:**
  - perception relabels colour per episode by encounter order within its band;
  - the colour type moves into the nominal set;
  - `gamma.save/load` carry applies `carry_check` and offers `axis_forms` at load;
  - the colour alphabet prices the episode's labels, not the palette.
