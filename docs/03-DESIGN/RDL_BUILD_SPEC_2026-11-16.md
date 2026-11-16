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

## Checks every piece ships with
Its switch (default ON, gw12 identical OFF where it touches the agent), one must-fail, tests under 5 minutes (Isaiah 2026-11-16), ruff clean from the root, `python -B conform/arms.py` exit 0.
