# Recursive Diffusion Learning: the build spec (2026-11-16)

Isaiah 2026-11-16: "RDL matters most to me, start working on it." Design: `docs/05-RESEARCH/40-WATSON_2026-11-13_RECURSIVE_DIFFUSION_LEARNING.md` (constraints C1-C6, the tier ladder, the bridle, codified reach) and `41` (strata, islands, gap widths). This page fixes the interfaces so the pieces can be built in parallel. Every name below is binding for all builders.

## The three quantities, never blurred (40, "Three quantities")
- **reachable**: yes/no, by derivation (the agent's closure; RDL never sets it);
- **search priority**: where to look first (the ONLY thing tier, release and the reach policy set);
- **standing**: only a term's own record with the board (RDL never writes it).

## Piece 1: `rdl_store.py` (C1, C2, C3, C6) and `rdl_parse.py` (the parser)

`rdl_store.py`, no import of tether:
- `STAGES = ("instance", "regularity", "abstraction", "core_rule")`; tier = index + 1 (1..4).
- `@dataclass(frozen=True) class Preload`: `pid: str` (sha256[:16] of the canonical JSON of every other field), `tier: int`, `stage: str`, `source: dict` (`corpus`, `corpus_sha`, `parser`, `parser_version`), `kind: str` (a kind-level key, e.g. `"wn:n02776205"`, `"card:<id>"`; never an object name, never a coordinate), `text: str` (the head start in the agent's grammar: NSM primes / operators where the source gives them, else the gloss), `bonds: tuple` of `(bond, a, b)` with bond from library/grammar.json's bond set, `refusal: tuple` of refusal forms (strings, e.g. `"NOT <kind> WHEN <condition>"`), `attaches: tuple` of library entry names reached BY CLUSTER (ATTRIBUTE_INDEX `by_cluster`, never raw-name intersection), `parents: tuple` of pids of the lower-tier preloads this one abstracts.
- `head_start(p) -> tuple[bool, str]`: C1. False with the reason for a recording (a move list, an action sequence, an object name like `o12`, a coordinate, a solution).
- `usable(p) -> bool`: C2. True only with at least one bond AND at least one attach; otherwise the preload is recorded, never offered.
- `load(path) -> list[Preload]`, `dump(preloads, path, header)`: deterministic JSON (sorted keys, stable order), a header with sources (file, bytes, sha256), licences carried from the inputs, `"standing": "none (C3): preloaded material has no standing until the board pays"`, `"readers"`.
- No field anywhere means standing. Nothing in this module settles anything (C3).

`rdl_parse.py`, the forward shed (40 "The loop" 1), no import of tether:
- `parse(lexicon_path, attribute_index_path, rules_path, stats=None) -> list[Preload]`:
  - tier 1 instance: one per lexicon class (lemmas + gloss, kind `wn:<wnid>`), attached by cluster;
  - tier 2 regularity: synonym sets / shared-lemma groups and same-cluster groups (kind `wn-group:<key>`), parents = their tier-1 pids;
  - tier 3 abstraction: hypernym strata (each hypernym that 2+ classes share; kind `wn:<hypernym wnid>`), parents = tier-1/2 pids under it;
  - tier 4 core rule: each card of library/tether_rules.json (kind `card:<id>`), its rule in operators and NSM primes, its `refuted_by` as the refusal form;
  - each tier is LOSSIER than the one below (tier 1 keeps gloss and lemmas, tier 2 only the set, tier 3 only the stratum, tier 4 only the rule) (Fig 4 :27-28).
  - `stats` (C5): `{(corpus, tier): {"settled": n, "refused": m}}` from the agent; a (corpus, tier) the ground refused more than it settled is shed one tier coarser in the next build (record the decision in the header). Never the parser's own taste.
- `build(out_path)` writes `library/rdl_preload.json`; `--check` rebuilds in memory and compares byte for byte.

## Piece 2: `rdl_release.py` (C4, the release base layer, codified reach), no import of tether

- `MIN_SETTLED = 2`: the project's MIN_REPEAT ("one observation is a coincidence"), reused, not a new constant.
- `released(preloads, stats, inherited_settled=True) -> set[str]` (pids): tier 1 is released at once (the base layer: inherited priors count as settled for the fringe: priority, not standing); tier k > 1 is released when the settled count at tier k - 1 (summed over sources) is at least MIN_SETTLED. Only `usable` preloads are released. Age is never a release trigger; it is only a tiebreak.
- `stats_from_rows(rows) -> dict`: `{(corpus, tier): {"offered": n, "settled": n, "refused": n}}` from ledger rows `rdl_settle` / `rdl_refuse` / `rdl_offer` (detail fields `pid`, `tier`, `corpus`).
- `reach_policy(rows) -> list[tuple]`: codified reach (40 "Codify reach"): cues `(corpus, tier, cluster)` with `[tried, paid]` from those rows, validity `(paid + 1) / (tried + 2)` (the same form as the agent's `_b2_cues`), ordered by validity descending, then tried descending, then the cue's text: an ordered symbolic table (Take The Best), never weights.
- `priority(preload, policy, age) -> tuple`: the sort key for search priority: (policy rank of its cue, tier, -age, pid). Lower sorts first.
- `merge_stats(a, b) -> dict`: summed increments (the lineage carry adds a generation's increments to its ancestors').

## Piece 3: the agent (TETHER_RDL, default ON)

- At birth: load `library/rdl_preload.json` if present (absent: inert) and the carried stats (`rdl_n` in the lineage counts blob, the `obg_n` pattern: increments since the last save, summed at load).
- Search priority only: where the agent orders library entries for a lookup or mint walk, entries attached to RELEASED preloads come first among otherwise-equal candidates, ordered by `rdl_release.priority`. Nothing is added to the library, nothing is made reachable, no standing is written.
- Feedback (C5, the reverse step): when an entry attached to a released preload settles (the ground paid), write `rdl_settle` with the preload's pid, tier, corpus; when it is refused, `rdl_refuse`; the first time it is offered by priority, `rdl_offer`. These rows are the stats the release, the reach policy and the parser read.
- Every row carries the stamp (C6): pid, stage, tier, corpus, parser.
- OFF: nothing loaded, no order change, no rows.

## Built 2026-11-16 (the door)
Piece 1 `fa208f3` (store and parser, `library/rdl_preload.json`: 1,494 preloads, 191 usable), Piece 2 `cd557b0` (release and codified reach), Piece 3 `0b1245c` (TETHER_RDL: tie-break in `Agent._topk`, stamped rdl_offer / rdl_settle / rdl_refuse rows, `rdl_n` carried in the lineage; OFF identical, 2,427 gridworld rows). Hops 1-2 of write-up 40's chain for the 1000 ImageNet classes: `library/lexicon_imagenet_wordnet.json`.

## The plan ahead: "it's a ball (shaped like a ball, acts like a ball); balls can roll; does this roll?"

Isaiah 2026-11-16 16:12-16:20: *"I want the agent to be like 'its a ball (shaped like a ball, acts like a ball)' and lets see, balls can roll, does this roll? that type of fluency"*; *"we have primitives and atoms in the library, but if we can connect them to other words, that might if in tandem with a dictionary ... let us derive word or concept -> action"*; *"does the agent know how to identify a ball versus rectangle? (We need to give it all the basic shapes in its visualizer - these are likely atoms, but they need to connect those atoms to those visual things)"*; *"go into the library and define if something is a thing, a shape, an action etc. categorize so that helps make search faster"*; *"opponent -> deception, trick, adversary"*.

This is write-up 40's affordance chain, *shape -> concept -> properties -> predictions*, with the visual-lexicon gambit on top. The found gap (2026-11-16, read in code): perception gives each object `shape` (the exact cell pattern), `h`, `w`, holes, corners, solidity, but **no shape name**, and the library's shape atoms (`TOPOLOGICAL|Circle`, `TOPOLOGICAL|Sphere`, ...) are connected to nothing on the board. The library is already filed by kind (PERCEPT 1,739, COMPOSITE 2,164, PRIMITIVE 79, RELATION 66), default role (STATE 2,049, PROCESS 1,781, ...), 128 domains and 17 clusters; what it lacks is a plain category (object, shape, action, relation, property) and a bridge from words to entries.

**The loop, link by link** (each link consumes what the one above produces, Fig 3 :20):

| # | The thought | Piece | Switch | Status |
|---|---|---|---|---|
| L1 | "shaped like a ball" | **shape names in perception**: a `shape_name` reading per object from its own cells only (dot, line, square, rectangle, ring, cross, disc, ...), each a declared predicate (Fig 10), attached to the library's shape atoms (`SHAPE_ATOMS`) | TETHER_SHAPE_NAMES | building 2026-11-16 |
| L1b | "a circle stands for a ball" (2D -> 3D, Isaiah 16:20) | **the shape bridge**: a declared table, shape_name (2D) -> 3D form -> object concepts (disc -> sphere -> ball, globe, marble; square -> cube -> block, box; rectangle -> rectangular solid -> brick; ring -> torus/hoop -> hoop, tire; line -> rod/cylinder -> stick, pole; triangle -> cone/pyramid), each resolved to WordNet 3.0 synsets, stamped `abstraction`, no standing. Write-up 40 "Reversed development": the agent learns "this flat pattern means depth". On flat boards the depth meaning is held and cannot settle; what settles is **behaviour** -- a disc earns "ball" by acting like one (L4), and drops back to "disc" with the refusal recorded when it does not | data, `shape_bridge` in `library/word_map.json` | building 2026-11-16 |
| L2 | "it's a ball" | **the word map**: every library entry's words -> WordNet senses (chosen by its domain and clusters, never by spelling alone; ties recorded, never resolved silently), a category per entry (object, shape, action, relation, property, measure, rule) cross-checked with the library's own kind and role, and a synonym index (`opponent` -> `TRANSFORMATION|Adversary` through a shared synset) | data, `library/word_map.json` | building 2026-11-16 |
| L3 | "balls can roll" | **affordance priors**, the dictionary half: the actions a concept's WordNet definition names ("ball: a round object that is hit or thrown or kicked") and its derivationally related verbs; each a stamped prior (C6), no standing (C3) | data, in the word map | building 2026-11-16 |
| L4 | "does this roll?" | **the affordance bet**: at a new kind's first sighting, the prior's prediction is written; the first press on that kind tests it; the board settles it or refuses it, and a refusal splits the rule by the condition read ("round things roll, except when blocked"); nothing deleted | TETHER_AFFORDANCE | building 2026-11-16 |
| L5 | saying it | NSM lines over those rows: "THIS IS LIKE `ball`. `ball` CAN MOVE. I DO SOMETHING TO THIS. THIS MOVES." Only listed primes; the word is a filler that unpacks to its primes | (in L4) | building 2026-11-16 |
| L6 | "adversary -> deception, trick, decoy" | **the relation layer** (write-up 40 hop 3): roles and bonds between different things (UsedFor, CapableOf, Causes). Needs a corpus choice (ConceptNet or FrameNet): Isaiah's call | -- | next |
| L7 | categories make search faster | the L2 categories as a **search-priority filter** (Fig 9 :60: a filter for the budget, never a verdict), beside RDL's tie-break | -- | next |
| L8 | recognition from pictures | the ImageNet images through a swappable recognition front end at the edge (write-up 40 hop 1 with pictures); photos are not grids, structure transfers through the shared clusters | -- | later (the images are downloading) |
| L9 | fluency measured | primes per explanation fall as words ground, at the same meaning; presses to settle a domain's first terms fall with each domain already learned | -- | later |
| L10 | dictionary and voice | cmudict pronunciations (hop 5), a rule-based synthesizer (hop 6); talking needs an ear and a listener as the board | -- | later |

**The rules every link keeps** (write-up 40): preloaded with no standing; attached by cluster and sense, never raw spelling; the board alone settles; a refusal splits by condition and is kept (Fig 6); every row stamped (C6); search priority only, never reach or standing; each piece behind its own switch, ON by default (Isaiah 2026-11-16: everything is tested together once the build is done).

## Checks every piece ships with
Its switch (default ON, gw12 identical OFF where it touches the agent), one must-fail, tests under 5 minutes (Isaiah 2026-11-16), ruff clean from the root, `python -B conform/arms.py` exit 0.
