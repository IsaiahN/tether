# Status of the four in-flight branches (2026-11-16, 18:15 CST)

## Outcome, 19:00 CST: all three merged, green

`wip/rec-index`, `wip/read-relations` and `wip/rec-agent` were finished, made ruff-clean, tested, and merged into development in that order (`5afae479`, `1cf6bd8e`, `00fac2c9`), with every check re-run on the merged tree: `test_recognize`, `test_shapes`, `test_recognised`, `test_affordance`, `test_relations_read`, `test_gate` (60/60), `test_arm_modules`, `test_root_logs`, `conform/arms.py`, ruff. What finishing them changed:

- **Two registry rows conflicted and both were kept**, and so were both module docstrings; the arms seat and its gate check confirm it (`1cf6bd8e`, `00fac2c9`).
- **`test_affordance`'s must-fail MF-A6 had to isolate its own arm.** ConceptNet's verbs predict `moves` on their own once `TETHER_RELATIONS_READ` is on, so the block that tests `TETHER_CONTACT_MOVES` now switches relations off as well; otherwise the must-fail would have passed for the wrong reason.
- **The "dot" defect was real and its cause is the interesting part.** Hu moments are scale-invariant, so a rendered `dot` and a rendered `circle` share a signature, and a large circle was named `dot`. Two declared rules fixed it: `DOT_MAX_SHARE` (a blob covering more than 2% of the picture is not a dot) and `DISC_ROUNDNESS` (a polygon class is penalised when the outline is at least `DISC_ROUNDNESS` round). Measured: hexagon 1/4 → 4/4.
- **A third rule came out of the same investigation**: a Hu moment saturated on either side (`HU_SATURATED`) is left out of the distance and the distance rescaled, because an invariant that has collapsed to zero carries no information. Held-out shape accuracy is **134/176**; square, cube, cylinder and cone remain weak.
- **A known limit, recorded rather than tuned away**: a *mathematically ideal* circle (every higher Hu moment exactly zero) abstains at distance 7.58, while a rendered circle is named at once. The test fixture is a rendered variant from `library/build_shapes.py`, and the ideal case stays a limit.

**Shipping (2026-11-19 refresh).** The release carrying all of this went out on 11-16: arc-solver-agent `21ecd7b5`. Isaiah merged the general-agent PR as **#18, `90c02632`** on 11-19 after the four helpers were finished. The verb-senses piece closed the one call the cutoff left open (`40228c63`): a contact verb predicts motion when WordNet's own hypernym chain reaches a motion verb (throw -> propel -> move), and ball's throw and kick senses were corrected. The Kaggle bundle at the released commit is `C:\TETHER_RUNS\KAGGLE_2026-11-16\code_21ecd7b5` (925 files, manifest `3be248e93cf03c09`), still to be uploaded.

## The m2 seat, 2026-11-19: one regression fixed, an older set still open

`conform/check.py` was run on the shipped tree. **m2 was FAIL**: the RDL wiring (`0b1245c`) stored the `rdl_store` and `rdl_release` MODULES in `ag._rdl`, and `tests/test_m2.py` deep-copies one warmed agent for every check — a module object cannot be deep-copied. Fixed at `66e57a3c`: `rd['fns']` now holds the six plain module-level functions the readers call, so deepcopy works and RDL behaviour is unchanged. The full re-run is **45/68 checks pass, 23 fail**; every `cannot pickle` failure is gone.

**Correction to commit `66e57a3c`'s message.** It says "44 of the 47 m2 checks died". The 47 was `conform/check.py`'s "3 of 47 finding *lines* shown" — a display limit, not the check population. The real denominator is **68 checks**; the number of pickling failures was not counted. This is the project's own "every count is restricted to the population it names" applied to a commit message: two different quantities under one number. The message stands (an error entry whose evidence is edited away stops being evidence); this note corrects it.

The 23 remaining failures are NOT from the deepcopy fix and were not addressed here. Grouped by their own assertions:
- **fixture trajectory** (`fixture: the routine did not exhaust`, `no bound want was bet on`, `library-first changed no winner`, `the slot's own guard must stay reachable`, `the dense channel must still owe`, `the M2 suite no longer reaches: exhausted`) — the file documents that these checks are pinned to one action policy, so a policy change reads as a fixture failure.
- **new attributes from 11-16** — `grew, kind, scale, shape_name, shrank, turned` are declared in `arc_world.ALPHABET` but the fixture's `check_an_attribute_atom_follows_its_arm` arm list and `_ranges()` table do not know them.
- **undeclared book keys** — 14 keys (`fade_ctx_hit`, `fold_total`, etc.) entered at commits on 11-10 and 11-02 without a `BOOKS` declaration; the seat's rule is that a zero must be visible, so each needs a reason, not a bulk addition.
- **narration and routine state** — `routine_bound`, `routine_formed`, `routine_hold`, `routine_not_formed`, `routine_rebid`, `routine_recheck` have ledger rows but no NSM sentence; plus `check_spent_plan_is_settled_in_its_deciding_cycle: held`, `check_one_bargain: wrong reason`, and two agent-rate refutation readings.

The notes below are the survey taken before that work; they are kept as the record of what the helpers left behind.

Written after the four helpers started at 17:53 were stopped by the day's cutoff. None of them committed; all their work survives, uncommitted, in four worktrees. Each branch was cut from development `dc7314ff`; development itself is now at `9a9d034f`, and the difference between the two is the `03-NEXT_STEPS_AFTER_2026-11-16.md` page.

Everything below was measured just now, not taken from a helper's claim.

## The four branches

| Worktree | Branch | Uncommitted | Tests run here | Verdict |
|---|---|---|---|---|
| `C:\TETHER_RUNS\WT_RI` | `wip/rec-index` | `recognize.py` +133/−7 | `test_recognize.py` **rc 0** | **Near-mergeable**: one ruff error to clear |
| `C:\TETHER_RUNS\WT_RR` | `wip/read-relations` | `affordance.py`, `conform/arms.py`, `tests/test_relations_read.py` (+118) | `test_relations_read.py` **rc 0**; `test_affordance.py` **rc 0** | **Near-mergeable**: one ruff fix |
| `C:\TETHER_RUNS\WT_SN` | `wip/fix-senses` | `affordance.py`, `conform/arms.py`, `library/build_word_map.py`, `library/word_map.json` (regenerated), `tests/test_affordance.py`, `tests/test_word_map.py` (+44k/−38k, almost all the regenerated word map) | `test_word_map.py` **rc 0**; `test_affordance.py` **rc 0** | **Mergeable as it stands**: ruff clean, arms rc 0, both tests green — this is the item Isaiah asked for ("contact verbs predict moves") and A6 passes again |
| `C:\TETHER_RUNS\WT_RA` | `wip/rec-agent` | `affordance.py`, `conform/arms.py`, `tether.py`, `tests/test_recognised.py` (+211) | `test_gate.py` **rc 0**; `test_recognised.py` **rc 1** | **Not mergeable**: a drawn circle is recognised as `dot` (the contour route is right for its own fixtures but the test's picture is too small), four ruff fixes pending |

Static checks, all four: `conform/arms.py` exits 0 everywhere. Ruff: clean in WT_SN; 1 error in WT_RI and WT_RR; 4 fixable in WT_RA.

## What each one is

- **`wip/rec-index`** (handoff item 2 and 3): a `HammingIndex` (multi-index hash in numpy) over AKAZE descriptors — substring keys, bucket candidates, exact Hamming on candidates — plus `build_abstractions`/abstraction-level fallback so a picture matching no single class can still match "a ball". New constants `INDEX_RADIUS`, `INDEX_PAIR_BUDGET`.
- **`wip/read-relations`** (item 5): `TETHER_RELATIONS_READ`. `affordance` now merges `library/relations.json`'s ConceptNet verbs beside the word map's, with `CN_READING` (the declared verb → reading table: roll, bounce, move, slide, push, kick, throw, fall → "moves"), a merge that ranks a verb found in both sources higher, and `cn_sources`/`merge` helpers that load `relations.json` and `vocabulary.json`.
- **`wip/fix-senses`** (item 9, the call I left open): the word map's contact-first senses for objects (ball: throw `v01508368`, kick `v01371756`), implausible example hits dropped, plus `TETHER_CONTACT_MOVES`: a prior predicts "moves" when its verb's WordNet `@` hypernym chain reaches `verb.motion`, recorded as `moves_object`/`moves_via`. That is the principled rule rather than a hand list, and it makes `test_affordance.py` A6 green again.
- **`wip/rec-agent`** (item 4): `TETHER_RECOGNISED`, picture detection on an observation (`is_picture`, `pictures`, `picture_sha`), a `recognise_rows` writer and a `recognised` row; `affordance` reads a recognised class where it reads a shape name. Inert on grid boards.

## The one real defect

`wip/rec-agent`'s test draws a circle that the contour route calls `dot` (`{'class': 'dot', 'grid_shape_name': 'dot', 'route': 'contour', ...}`). Either the fixture is too small (a `dot` is one cell) or `recognise_shape` should prefer `circle` for a closed round contour at any scale. The fix belongs in the test's picture size first; only if that fails does the recogniser need a change.

## Recommended order

1. Merge `wip/fix-senses` (green now) after a diff review — it closes the item left open at the cutoff.
2. Clear the one-ruff-error branches (`rec-index`, `read-relations`), re-run their tests, merge.
3. Fix `rec-agent`'s fixture, re-run `test_recognised` and `test_gate`, merge.
4. Then the two still blocked on the pictures: the ImageNet class memory (needs the 14 validation parquet files) and anything downstream of it.
