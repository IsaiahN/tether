# Next steps after 2026-11-16

Written at 17:55 CST on 2026-11-16, the day's cutoff; refreshed 2026-11-19 after the four in-flight helpers were finished and the release was merged. The design is `docs/05-RESEARCH/42-WATSON_2026-11-16_RECURSIVE_DIFFUSION_LEARNING_THE_DESIGN.md` (its handoff has the same items with exact pointers). Every piece built on 2026-11-16 is behind its own switch, on by default, with no standing until the board pays; Isaiah's plan is to test everything together.

## The four helpers at the cutoff: all finished, merged and shipped

All four helpers stopped at the cutoff with uncommitted work in their worktrees; three were finished on 2026-11-16 evening (two real defects found and fixed on the way: a large circle named `dot` because Hu moments are scale-invariant, and a must-fail that passed for the wrong reason once ConceptNet could supply "moves"). The verb-senses call was made later, after Isaiah approved the principled rule. The full account, with the measurements and the known limit (a mathematically ideal circle abstains), is in [`04-IN_FLIGHT_BRANCHES_2026-11-16.md`](04-IN_FLIGHT_BRANCHES_2026-11-16.md).

| Branch | What | Outcome |
|---|---|---|
| `wip/rec-index` | multi-index-hash nearest-neighbour search for AKAZE descriptors and abstraction-level centres across WordNet hypernyms | built `1c5aa1f7`, merged `5afae479` |
| `wip/read-relations` | TETHER_RELATIONS_READ: ConceptNet verbs merged beside the word map's, a verb in both ranking first | built `e343542f`, merged `1cf6bd8e` |
| `wip/rec-agent` | TETHER_RECOGNISED: a picture's class written and read where a shape name is read; inert on grid boards | built `21d83753`, merged `00fac2c9` |
| `wip/fix-senses` | contact verbs predict motion by WordNet's hypernym chain (throw -> propel -> move), plus the corrected object senses | built `40228c63`; shipped on 2026-11-19 |

All four branches and their worktrees are gone; their commits are on development. The GA PR carrying them was merged by Isaiah as **PR #18, `90c02632`** on 2026-11-19.

## In order, after those

1. **The ImageNet class memory (deferred by Isaiah on 2026-11-19; do not start).** The precondition is now met: the download finished at 23:31 on 11-16, and all 294 train plus 14 validation parquet files are in `C:\TETHER_RUNS\DATA_2026-11-16\imagenet-1k\data\` (142.8 GB, zero incomplete). When asked, run `recognize.build_from_parquet` with `per_class=50` over the validation files into `C:\TETHER_RUNS\DATA_2026-11-16\recognition\` using `C:\TETHER_RUNS\venv313` (OpenCV 4.14 and pyarrow are installed there). Local only, never in the repo (ImageNet terms). Then the same over train for more pictures per class.
2. **Strengthen the shape library where it is weak**: cube 0/4, cone 1/4, cylinder 2/4, square 2/4 on held-out pictures. More view angles (not just more samples of the same range), and a solidity/edge feature for solids.
3. **More RDL ordering sites**: the library-first offer walk (`_library_chains`) and the atom-chain walk (`make_order_key` / `ordered_closure`), each a last tie-break like `_topk`'s, each with its OFF identity checked row for row.
4. **The parser rebuilt between generations** from the carried `rdl_n` counts (`rdl_parse.parse(stats=...)` already sheds what the board refused), written beside the generation and stamped.
5. **The rulings for Isaiah** in `docs/03-DESIGN/REVIEW_2026-11-16_INDEX_CALLS_AND_CATEGORIES.md`: whether a trigger or a capacity counts as a described effect (49 filings, 147 more follow), and which category source wins per pair (R1-R5).
6. **Without OpenCV, if wanted**: akaze-eigen with a small Python binding behind `recognize.describe`; numpy versions of the contour, Hu-moment and RANSAC steps.
7. **The proving runs** (testing, after the build): the together-test at 600 s a game on a quiet machine; the T0 gate (a level cleared through goal, refusal, repair and return); a live settle of an affordance prior and of RDL material; the keep rules of every switch; then step 9 (the noise floor and the four experiments) and RDL's T1-T4.

## Owed by Isaiah

- **Done:** the general-agent PR was merged as #18 (`90c02632`) on 2026-11-19. The `promote/c-general-agent-ship4b` branch it superseded is still on the remote and can be deleted with the other release branches.
- **Upload to Kaggle:** `C:\TETHER_RUNS\KAGGLE_2026-11-16\code_21ecd7b5` as a new version of the code dataset (925 files, manifest `3be248e93cf03c09`; the memory dataset is unchanged). This is the only bundle left in that folder and matches the released arc-solver-agent.
- **Revoke the Hugging Face token now:** the ImageNet download ended at 23:31 on 11-16, so the token is no longer needed. The retry commands are in write-up 42.
