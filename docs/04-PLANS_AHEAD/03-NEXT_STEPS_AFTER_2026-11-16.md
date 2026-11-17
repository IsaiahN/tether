# Next steps after 2026-11-16

Written at 17:55 CST on 2026-11-16, the day's cutoff. The design is `docs/05-RESEARCH/42-WATSON_2026-11-16_RECURSIVE_DIFFUSION_LEARNING_THE_DESIGN.md` (its "handoff" section has the same items with exact pointers). Every piece built on 2026-11-16 is behind its own switch, on by default, with no standing until the board pays; Isaiah's plan is to test everything together.

## Work in flight at the cutoff (on `wip/` branches only, never merged)

Started at 17:53 and pushed, if finished, only to their own branches. Review each, run its tests, and merge into development only if green:

| Branch | What | Merge check |
|---|---|---|
| `wip/rec-index` | a multi-index-hash nearest-neighbour search for AKAZE descriptors (same answers as brute force) and abstraction-level centres across WordNet hypernyms ("a ball" when no single class passes) | `tests/test_recognize.py` |
| `wip/rec-agent` | TETHER_RECOGNISED: a `recognised` row when an observation carries a picture; the affordance bet reads a recognised class as it reads a shape name; inert on grid boards | `tests/test_gate.py`, `tests/test_arm_modules.py`, its own test, gridworld OFF identity |
| `wip/read-relations` | TETHER_RELATIONS_READ: the affordance bet merges ConceptNet's verbs (roll, bounce, push, kick, throw) beside the word map's | `tests/test_affordance.py`, its own test |
| `wip/fix-senses` | the verb senses for objects (ball: throw v01508368, kick v01371756; "have a ball" dropped) plus TETHER_CONTACT_MOVES: a contact verb predicts "moves" when its WordNet hypernym chain reaches a motion verb (throw -> propel -> move) | `tests/test_word_map.py`, `tests/test_affordance.py` A6 |

If a branch is absent, that helper did not finish; the item stays below.

## In order, after those

1. **The ImageNet class memory.** When the 14 `validation-*.parquet` files are in `C:\TETHER_RUNS\DATA_2026-11-16\imagenet-1k\data\`, run `recognize.build_from_parquet` with `per_class=50` into `C:\TETHER_RUNS\DATA_2026-11-16\recognition\` using `C:\TETHER_RUNS\venv313`. Local only (ImageNet terms). Then train for more pictures per class.
2. **Strengthen the shape library where it is weak**: cube 0/4, cone 1/4, cylinder 2/4, square 2/4 on held-out pictures. More view angles (not just more samples of the same range), and a solidity/edge feature for solids.
3. **More RDL ordering sites**: the library-first offer walk (`_library_chains`) and the atom-chain walk (`make_order_key` / `ordered_closure`), each a last tie-break like `_topk`'s, each with its OFF identity checked row for row.
4. **The parser rebuilt between generations** from the carried `rdl_n` counts (`rdl_parse.parse(stats=...)` already sheds what the board refused), written beside the generation and stamped.
5. **The rulings for Isaiah** in `docs/03-DESIGN/REVIEW_2026-11-16_INDEX_CALLS_AND_CATEGORIES.md`: whether a trigger or a capacity counts as a described effect (49 filings, 147 more follow), and which category source wins per pair (R1-R5).
6. **Without OpenCV, if wanted**: akaze-eigen with a small Python binding behind `recognize.describe`; numpy versions of the contour, Hu-moment and RANSAC steps.
7. **The proving runs** (testing, after the build): the together-test at 600 s a game on a quiet machine; the T0 gate (a level cleared through goal, refusal, repair and return); a live settle of an affordance prior and of RDL material; the keep rules of every switch; then step 9 (the noise floor and the four experiments) and RDL's T1-T4.

## Owed by Isaiah

- Merge the general-agent PR: https://github.com/IsaiahN/tether/compare/general-agent...promote/c-general-agent-ship4b
- Upload `C:\TETHER_RUNS\KAGGLE_2026-11-16\code_31f6da06` as a new version of the code dataset (the memory dataset is unchanged).
- Revoke the Hugging Face token once the ImageNet download ends; the retry commands are in the session record and in write-up 42.
