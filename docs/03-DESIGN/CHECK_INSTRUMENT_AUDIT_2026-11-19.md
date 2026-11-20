# Check-instrument audit, 2026-11-19

Read-only audit of `conform/check.py`'s 25 seats at HEAD `31718e75`: **17 clean, 6 found something, 2 DID-NOT-RUN**. This page records which findings are real, which are stale instruments, and which need a ruling. It does not weaken any check.

## Real findings (already or being addressed)

| seat | finding | status |
|---|---|---|
| `shipped` | `test_the_residual_bound_loses_nothing`: with `_cannot_pay` live, seed 0 bound 2 terms / library 10 / 655 rows; exhaustive arm bound 0 / library 8 / 564 rows. | **OPEN — derive before ruling.** The A/B was repeated in four SEPARATE processes: same-arm structural state is stable (seed 1: bound `s0:take`, library 8, ledger 590/600 in one pair — note the row-count variance), so this is not warm-state contamination of the compared tuple. A NECESSARY filter that removes candidates can change WHICH candidates win a bargain in a finite run; the invariant's claim "neutering it changes nothing at all" may be the stale premise, not the filter. **Measured 2026-11-19: the bound loses ZERO of the exhaustive arm's terms and gains two (`take . dec<s0~1>`, `take . inc<s1>`); the ledger differs because the freed budget buys different work (exhaustive-only: 13 purse_cut, 10 split_refused; real-only: 36 stream, 12 divide, 2 mint). So the run changes while no term is lost.** **DO NOT 'fix' by relaxing the assertion to a term subset:** measured, the planted unsound narrowing (`operand is not None`) also loses zero terms on that seed, so the check would go permanently green — a guard that cannot go red. The check needs a contract that both (a) accepts a freed-budget trajectory change and (b) still fails on the unsound narrowing. That is a derivation from the figures, not a patch. |
| `m2` | 45/68 checks pass. | Grouped work in `04-IN_FLIGHT_BRANCHES_2026-11-16.md`: book declarations, narration, fixture attributes, trajectory re-pins. |
| `panel` | ledgers MISSING/STALE. | **Instrument needs a detached job**: `conform/panel.py --produce` runs real board panels and was killed by a 120 s shell cap (the "cap below estimate is a kill by setup" rule). Relaunched fully detached 2026-11-19 17:47; do not read its result until that job reports. |

## Stale instruments — the check no longer measures what its docstring says

| seat | finding | evidence at the write site | action |
|---|---|---|---|
| `layers` | flags `arc_percept`, `compile_term`, `composer`, `gamma`, `inherited`, `ledger` for importing `cap`, `store`, `narrate` as "worlds" | `conform/layers.py` REASONING is an enumerated set; BRIDGE = {world, interface}; anything not enumerated is treated as environment-side. `cap.py` imports only contextlib/functools/time/armflag — it is the agent's own overrun net, not a world. The docstring itself warns "a rule that ENUMERATES WORLDS protects only the worlds someone remembered"; the enumeration has drifted as new agent infrastructure was added. | **Record, do not mass-edit.** Re-derive the agent/world line from the figures; the fix is a derived set, not adding 23 names one by one. |
| `recshape` | 26 findings, e.g. `for s, *_r in hist` "hides a widening" | `tether.py:27627` uses only the before-state of each history row (`_jc_value(k, s)`); the trailing fields are deliberately ignored by the O2 junction-scoring code. The seat's message `_invent did this and raised on its first call` is a fixed string, not derived from each site — and `_invent` is RETIRED. The check's SOURCES = {hist, robs, obs, trace} also matches unrelated 5-tuples named `obs`. | **Record, do not mass-edit.** Several unpacks are correct by construction. A leading-star check has merit; a blanket trailing-star refusal is wrong. Re-derive from the actual consumers. |
| `wiring` | 68 status transitions the manifest does not record; 25+ NEW-in-declared-set entries | `conform/wiring.json` binds status to artifact stamps; the tree gained a large amount of new machinery after the newest recorded board artifact (2026-09-21). Some of these are genuinely new capabilities whose status never occurred on a recorded run. | **Needs a ruling** on whether a never-occurred capability is a defect or an unexercised arm. Do not bulk-update the manifest. |
| `library` | 14 findings on the real library; all 5 planted must-fails CAUGHT | The must-fail paths work — this is not a dead check. The 14 real findings need reading one by one before any edit. | **Open — read each finding**, then fix library data through its generator, never by hand. |
| `lint` | DID-NOT-RUN, timed out after 180 s | `STAGE_TIMEOUT = 180` is explicitly Isaiah's calibration constant (`conform/check.py:182-205`), ~50% headroom over a 2m01s measurement from 2026-09-28. Today's suite is longer; the cap is a measurement, not a verdict. | **Isaiah's constant to move.** Record the new measurement; do not silently raise it. |

## The lesson to carry

A seat that finds nothing can be a seat that no longer looks at the thing it names: `layers` and `recshape` are green-until-irrelevant in exactly the way `conform/focus.py`'s own docstring describes for guards whose failure path is never exercised. Their fixes are derivations, not edits to the code they police. `shipped` is the opposite: a red check whose premise may be older than the mechanism it pins. Both need the figures at the write site before either the code or the check moves.

## RDL feedback gap (verified 2026-11-19, not a wiring bug)

RDL's store, parser, release, tie-ordering, lineage carry and deepcopy all verify (5 test files green, 1494 preloads / 191 usable, a controlled rank flip with a real released pid, `rdl_n` present in `memory.db`). On a real 12-step gridworld run only `rdl_release`×1 and `rdl_offer`×4 appear; `rdl_settle`/`rdl_refuse` never fire because `term_entry` stays empty — its only writer (`tether.py:30014-30019`) needs library-first provenance whose `library` key is an RDL-attached entry. 419 of 420 attach names ARE real library entries, but they are overwhelmingly ARC-domain (`ACOUSTIC|…`) that gridworld never reaches. **This is a test-world limitation, not a defect.** Fabricating a gridworld path would be a synthetic solve; the ground for RDL is the ARC board, where those entries live. Record it as a known limit and do not "fix" it with a fake match.

## Two more instrument findings, 2026-11-19 (prepared, landed with the m2 merge)

### `m2` is hash-seed nondeterministic — a green count is not reproducible

Measured by the m2-fixture agent at `63fe70f9`: the full suite gives **45/68**, but four checks flip with `PYTHONHASHSEED` — `check_a_blocked_routine_ends_at_planning_with_no_verdict`, `check_a_zero_act_routine_still_ends_at_planning`, `check_an_unreadable_guard_blocks_at_execution`, `check_only_a_trial_refutes`. With seed 0 all four fail; with seeds 1 and 2 all four pass. None is reachable from the fixture edits (they sort before the changed checks). The shared 25-step warm-up in `tests/test_m2.py::_agent()` (lines 117-170) is built once and handed out as `deepcopy`, so every check inherits whatever trajectory the warm-up took — and that warm-up calls `ag.drive.choose(ag.actions, ...)` with an action set whose iteration order can move with the hash seed. **The count is a reading from one seed, not a property of the agent.** Record it; do not pin `PYTHONHASHSEED` to make the suite green (that would hide the non-reproducibility rather than remove it), and do not weaken the four assertions.

### `wiring` and `libagree` are stale instruments, not 82 defects

`conform/wiring.py` reports 68 transitions: terms whose occurrence set in four recent artifacts (`demo.jsonl` and bodies) no longer matches the manifest, plus newly-declared terms that have not occurred. The manifest records a long-lived history; the artifacts are a short recent sample. This is a sampling-window mismatch, not a capability regression. Bulk-updating the manifest would rubber-stamp it.

`conform/libagree.py` reported 14. **Six were an instrument bug, now repaired** (measured: 14 → 8 findings). Two separate defects, both at the instrument's own write site:
  1. `env_of()` required `armflag.arm("TETHER_...")` to end at the closing quote, but all 13 `arc_percept` arms declare `default=True`, so it returned `None` for every one and never forced the named arm on. The regex now reads only the name.
  2. The six cell-change atoms are declared `arc_percept._CELL_CHANGE (import-time)`, but `build(off=...)` only did `setattr` **after** import — too late for an arm baked into the atom list at import. It now sets the env var to `0` for the off arm as well.

The six `(c)` findings (`add_col`/`add_n`/`add_row`/`rem_col`/`rem_n`/`rem_row`) were artifacts of those two lines and are gone. The remaining eight `(a)` findings (`below`/`grew`/`kind`/`scale`/`shape_name`/`shrank`/`subtract`/`turned` built but not in `agent_atoms.json`) are genuine divergence from the GIVEN corpus, which is Isaiah's and may not be edited — a fact to record, not a library defect to repair. The planted must-fails (a)-(e) all still fire.

## ERRATUM, 2026-11-19 — the "hash-seed nondeterminism" finding above is WITHDRAWN

The section above claimed the agent and the m2 suite were hash-seed nondeterministic. **That was wrong.** It was a satisfying causal story attached to a number, which is the exact failure this file warns about. The original text is kept so the error stays evidence; the correction follows.

What actually varies is the **agent's own draw seed**, and that is by design:

- `_AGENT_SEED = armflag.arm("TETHER_AGENT_SEED", default=True)` (`tether.py:3862`). `_seed_at_start()` (`tether.py:3888-3898`) therefore draws `secrets.token_hex(8)` for each fresh process. Two runs at the *same* `PYTHONHASHSEED=0` gave different `draw_seed`s and different tallies (`bargain_bounded_out` 15542 vs 15526). Hash seed is not the variable.
- The four "flipping" checks were each run in isolation under `PYTHONHASHSEED` 0, 1 and 2: **all four passed under all three**. The earlier attribution was one sample per seed, not a controlled comparison — and the agent's seed was redrawn each time.
- The first bound-call divergence (call 8228) is `inc . take<s1>` vs `inc . take<s2>` at identical cost and base. `FR.draw_key` is `blake2b` (`frontier.py:34-40`, deterministic) and `_lookup_order` passes `self.draw_seed` (`tether.py:3114-3115`), so the tie is broken by the recorded draw, not by Python hashing.
- Across all the variation the agent's **decisions were identical**: the same 10 library terms, the same bound, the same `bargain_paid` (5). Only the effort tallies (`bargain_bounded_out`, `bargain_does_not_pay`) and the ledger row count moved — which is the draw choosing which candidate is examined first under a finite budget, exactly what `_bindings` says order does.

**The README standard does hold.** A fresh run draws its own seed and records it in a `@run` row; replay names that record with `TETHER_SEED_FROM` (`tether.py:3866-3885`). Measured here: a record written from one run was replayed twice, and both replays reproduced the same `draw_seed 3377de0c2a477759:0`, the same tallies `14884 / 258 / 5`, the same **1255** ledger rows and the same library. *Results reproduce* means a recorded run replays — not that two fresh runs with independent draws are byte-identical.

**What remains true and what to do.** The m2 count is a reading from one particular agent draw and can move between fresh runs because its warm-up fixture (`tests/test_m2.py::_agent()`) builds a fresh agent; that is a fixture-reproducibility observation, not an agent defect and not a hash-seed one. If a stable count is needed, pin the *replay* seed in the fixture, not `PYTHONHASHSEED`. The four checks were not shown to be flaky by controlled measurement; no assertion was weakened and no seed was pinned.

**Correction to the `shipped` row too.** Its note about "row-count variance" between same-arm repeats is also explained by the fresh draw per process, not by warm memo contamination. The bound-loses-zero-terms measurement stands; the must-fail trap stands; no code was changed.

## The `shipped` seat's masked chain, 2026-11-19

`conform/stateful.py --fast --tether` stops at its first failing invariant, so fixing the bound check uncovered three older failures that had been masked behind it. `gamma.py` and `interface.py` are byte-identical to parent `31718e75`, so none is a regression from this session's work.

1. **`test_a_per_slot_refusal_decays_like_the_term` — repaired.** It passed `halflife=None` as the "use the seed" case, but under `TETHER_FADE_BY_STORE` (default ON) the live caller passes `SeedCycles` or an explicit store halflife (`gamma.py:1996-2003`), and `_store_fade` reads `None` as "no step yet → no fade" (`gamma.py:531-536`). It now passes `gamma.REJECTION_HALFLIFE`; the `inf` control still unsettles. Measured: `None` gave `refusals_on=2.0` (cliff), the seed gives `1.9259` (survives).
2. **`test_the_admitting_clause_crosses_into_gamma` — repaired.** It compared Γ's stamps against `arc_atoms.ADMITTED` alone (31 built atoms), but the code admits from `{**ADMITTED, **_fold_admissions()}` (`arc_atoms.py:1295,1335`), which adds nine built atoms (`all_of`, `cell_col`, `cell_row`, `cells`, `count_true`, `none_of`, `one_of`, `size`, `some_of`). Γ stamped 40 and the test called that a defect. It now reads the clause from each atom's own `admitted` field — the value Γ actually installs so a stamp overwritten downstream is still caught.
3. **`test_the_seam_varies_what_it_explores_with` — LEFT RED, deliberately.** It builds a bare `Interface()` (constant draw seed `FR.SEED="0"`) and asserts that six `ELICIT` realisations never repeat an action more than twice. Measured: `['C','A','B','A','A','A']` — the first-three-distinct assertion passes, the variety ceiling fails. This is a statistical assertion over six seeded draws, the same class as the m2 count: a fixed draw can violate it without any mechanism failing. The live agent sets `iface.draw_seed` per run, so the bare-interface fixture is not the live condition. Repairing it means asserting the *mechanism* (frontier/tally path taken, forbidden action not repeated by a degenerate realiser) rather than a count over one draw — a derivation, not a threshold tweak. Do NOT raise the cap or pin a lucky seed. The check stays red and readable.

## Final consolidation, 2026-11-19

### The reproducible m2 count is 48/68, not 45/68

The earlier 45/68 and the debt agent's 44/68 and 46/68 were readings taken with a fresh agent draw each process. With the agent's own draw pinned (`TETHER_AGENT_SEED=0`, i.e. the constant draw seed the arm's OFF value selects), the full suite gives **48/68** for twenty failures, reproducibly. This is the count to quote going forward with its arm state named. The eight fixture-class failures the m2-fixture agent identified are among the twenty; the rest are pre-existing narration, rate and `Want.atoms` failures documented in `04-IN_FLIGHT_BRANCHES_2026-11-16.md`. **No check was weakened and no seed was pinned in the repository** — this is a measurement arm state, not a code change.

The controlled head-to-head closes the accounting exactly. With both arms pinned, the debt commit `b9020827` scores **45/68** and its parent `31718e75` scores **44/68**; the mechanical failure-set diff is one baseline-only failure (`check_every_book_key_is_declared`) and **zero** new ones. The m2-fixture commit `63fe70f9` fixes three more attribute checks (measured `ATTR OK` and three names gone from its failure list). `44 + 1 + 3 = 48`, which is the development count. There is no regression and no unexplained spread left.

### `recshape` is a name collision, left red with proof

All 26 findings come from `SOURCES = {"hist","robs","obs","trace"}` (`conform/recshape.py:44`) and `add()`'s test `names(itr) & SOURCES` (line 83): *any* variable named `obs` anywhere in an iterable expression is treated as a history record. Measured at the reported sites:

- `tether.py:3679` is `(t for _a, t in obs)` where `obs` is the fifth field of a six-field `contact` tuple (`a, typ, before, after, obs, code = contact` at 3678), not a history row.
- `tether.py:8029` is `frames = [b for b, *_r in hist]` — a deliberate trailing-star discard of fields the reader does not use.
- The fixed message *"`_invent` did this and raised on its first call"* is printed at every short-unpack site even though `_invent` was retired 2026-10-05.

A correct fix needs to tie the iterable to an actual `history()`/`self.trace` producer by data flow, not by variable name — a derivation, not a list of exemptions. The check stays red and readable; do not mass-edit the 26 call sites.

### Panel: a duplicate production, both jobs left to finish

The first `conform/panel.py --produce` call was moved to background by a shell cap rather than killed; a second was then launched detached. Both (pids 9328 and 3720) are running the same members against the same `runs/panel/` artifacts. The output is deterministic for a given tree, so the result should be identical; the standing rule is that a running job always finishes, so neither was killed. Verify the `panel` seat after both report and regenerate once cleanly only if a stamp is corrupt.

### Measured flake rate of the four m2 checks, 2026-11-19

`flake_count.py` rebuilt the fixture eight times in one process (clearing `_BUILT` each time, so the agent drew a fresh `secrets.token_hex(8)` seed) for each of PYTHONHASHSEED 0 and 1:

| check | hash 0 | hash 1 |
|---|---|---|
| `check_only_a_trial_refutes` | 6/8 | 4/8 |
| `check_a_blocked_routine_ends_at_planning_with_no_verdict` | 6/8 | 3/8 |
| `check_an_unreadable_guard_blocks_at_execution` | 7/8 | 4/8 |
| `check_a_zero_act_routine_still_ends_at_planning` | 4/8 | 6/8 |

Both columns vary in the same range, so the draw is the variable and Python hashing is not. This is the measured basis for the erratum above: an m2 count taken with a fresh draw is a reading from one draw, not a property of the agent; pinning `TETHER_AGENT_SEED=0` makes it 48/68 reproducibly. No repository code or test was pinned as a result — only the measurement's arm state is named.

## The atom registry gap (Isaiah's question, 2026-11-20)

Measured, not asserted. `library/given.json` (the immutable GIVEN corpus) reconstructs `agent_atoms.json` with **79 declared atoms**. `arc_atoms.three_spaces(arc_predict.predict())` builds **84 atoms** under all arms. Eight built atoms are absent from the corpus registry:

    below    subtract   -- already carry a `handed` reason in arc_atoms.ADMITTED
    grew     kind  scale  shape_name  shrank  turned
             -- no admission clause; Gamma therefore stamps them NECESSARY

This is **not** game learning and **not** RDL. Playing a game and RDL preloads add TERMS to Γ's library; ATOMS are the irreducible vocabulary installed at construction. These eight are code-side atoms added after the corpus was written, with no entry record.

Why it matters: the terminal condition's ablation partitions entries by *which clause admitted them*. NECESSARY is the category the ablation stays BLIND to. If an atom we handed the agent is silently stamped NECESSARY, the wipe cannot remove it and the agent appears to have composed what it was given. The project's own rule requires the admitting clause to be written **as entries happen**, because it cannot be reconstructed later from a `PRIOR` stamp.

Rectification (proposed, needs Isaiah's ruling on the six):
1. Add a WORKING registry `library/atom_births.json` recording name, admitting clause, date/commit, in/out type, form, reading and tags for every post-GIVEN atom.
2. Have `libagree.load()` compare code-built atoms against GIVEN **∪** births, so `(a)` stops reporting eight false absences while real drift still fires.
3. Port the two existing `handed` reasons verbatim — no new judgement there.
4. Rule on the six clause-less attributes: if the loop cannot run without them, stamp NECESSARY **with a recorded reason**; if a measurement named them, stamp ON DEPTH / HANDED with that reason. Either way the clause must be recorded now, or the WIPE half of the ablation stays unrunnable for them.

The GIVEN corpus is NOT to be edited — its derivational independence is the property the whole check runs on.

## Lint after the timeout was lifted

`conform/lint.py` measured **1261.6 s** (21m01s) over 323 files, rc=1: ANCHOR, ISOLATED, REACH and SINGLETON fail with accumulated findings that the old 180 s cap had hidden as DID-NOT-RUN. One "file could not be parsed" (`library/build_lexicon.py`) was an instrument bug: the file has a UTF-8 BOM, imports fine under Python's tokenizer, but lint read it as plain utf-8 and `ast.parse` saw U+FEFF. Fixed by reading `utf-8-sig`. The four rule failures are real accumulated debt and are NOT classified or repaired here — a rule that was never able to run has no clean baseline, so its findings need reading one by one before any mass edit.

## 2026-11-20 — the two remaining investigations, resolved

### T0 gate: 0 of 6 games pass (the full 600 s run)

Six unseen games, every switch ON, 600 s each, fresh copy, `TETHER_AGENT_SEED=0`, offline.
Pass = goal → refusal → repair row → subgoal → goal again → clear, in ledger order on one board.

| game | goal | refuse | repair | subgoal | goal-again | clear | actions |
|---|---|---|---|---|---|---|---|
| ar25 | ✓ | — | — | — | ✓ | — | 28 |
| cd82 | ✓ | ✓ | ✓ | — | ✓ | — | 19 |
| g50t | ✓ | ✓ | — | — | ✓ | — | 20 |
| ka59 | ✓ | ✓ | ✓ | — | ✓ | — | 34 |
| lf52 | ✓ | — | ✓ | — | ✓ | — | 22 |
| lp85 | ✓ | ✓ | — | — | ✓ | — | 55 (reached level 1, not through the chain) |

**Verdict:** the chain gets partway every time — goal and goal-again on 6/6, refusal on 5/6, repair on 3/6 — but **no game ever files a subgoal or clears a level**. This is the honest ground reading on unseen games; the T0 gate has not passed. It is a capability gap, not a test failure. The together-test duration contradiction is resolved by parameterizing the harness: the written protocol is 600 s/game (the run above), while the earlier T0e executed at 300 s. Do not tune to clear a level; diagnose where the chain stops (repair → subgoal never fires).

### The remaining red m2 checks — full triage (seed 0)

- **`check_the_accumulation_commits_where_the_bargain_refused`** — STALE, FIXED (`ffd7ba27`). It set `_last_commit`, but `TETHER_URGENCY_PROGRESS` (default ON) reads idle from `_last_progress` (tether.py:25038). Both cold and warm idle were already past the quorum floor (bar 2.0 → floor 1.5 at idle 4), so relief never moved. Pinning the live field gives cold threshold 2.0, warm 1.5; control intact.
- **`check_the_suite_reaches_the_hard_cases`** — REAL, LEFT RED. It correctly reports `unadvertised` not reached. Cause is a *different quiet check*, `check_only_a_trial_refutes` (test_m2.py:828), which plants on the derived slot o1.dcol (guard unreadable → ends `blocked`) and never asserts the outcome, so it stays green. Fix the companion, not the tripwire (being done on wip/m2-redfix).
- **Seven stale instruments** — measured re-pins with controls intact: claim/spent sample a slot absent from observe(); two DONE-shelving checks assume one zero ends a guard (GQ3 needs two consecutive); one-bargain and shelf-runnable stall at `discrepancy NOT_RESOLVED` on o1.dcol; library-winner has no moved winner in this world. Being applied on wip/m2-redfix.
- **`check_can_gates_until`** — NEEDS-DESIGN, LEFT RED honestly. Measured at seed 0: `o0.add_n`/`o0.rem_n` have `can=yes` but `disc=0`; `o1.col` has `disc=1` but `can=unknown`; `o1.dcol` has `can=unknown`/`disc=NOT_RESOLVED`. **No slot has can=YES ∧ positive gap ∧ goal target simultaneously.** I probed installing a goal hypothesis on o1.col (the agent's own record): that makes `can=yes` honestly, but only by driving disc to 0 — the tension is structural, not a field swap. `can=YES` requires the slot to hold its goal now (disc=0), have a route from the delta table, or a bound term with observed motion toward the target; none co-occurs with a positive gap in this fixture. Resolving it needs a NEW OCCASION (a world where the objective is reachable-but-not-yet-held with a known route) or a ruling to re-scope — not a weakened assertion. The guard mechanism itself is intact at tether.py:26018-26027, with an exercised control: deleting the `all(can(g)==YES ...)` clause makes a guarded candidate commit. No ARC-game tuning.
