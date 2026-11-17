# Status of the four in-flight branches (2026-11-16, 18:15 CST)

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
