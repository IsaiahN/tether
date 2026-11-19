# The state of the agent (2026-11-16, refreshed 2026-11-19)

A handoff: what works, what doesn't, where the gap is, and what's designed next. Written so someone picking this up can start without the conversation history. Every claim points to a measurement or a commit.

**Refresh, 2026-11-19.** Everything below is shipped on development, arc-solver-agent and general-agent: the GA PR carrying the four in-flight helpers was merged as #18 (`90c02632`). Those helpers finished the fast AKAZE index and abstraction centres (`5afae479`), the agent's `TETHER_RECOGNISED` row (`00fac2c9`), the reading of ConceptNet and VerbNet by the affordance bet (`1cf6bd8e`), and the contact-verb rule that closed the last open call (`40228c63`). The full account, including two real defects found and fixed while finishing, is in `docs/04-PLANS_AHEAD/04-IN_FLIGHT_BRANCHES_2026-11-16.md`; the remaining work is in `docs/04-PLANS_AHEAD/03-NEXT_STEPS_AFTER_2026-11-16.md`. ImageNet finished downloading at 23:31 on 11-16 (all 294 train and 14 validation parquet files, 142.8 GB), but the class memory is deferred by Isaiah. Kaggle upload of `code_21ecd7b5` and revocation of the Hugging Face token are still owed by him.

## Since 2026-11-13: the build sequence is built, and the T0 gate is running

Every item of `docs/04-PLANS_AHEAD/02-BUILD_SEQUENCE_FUTURE_STATE.md` up to the T0 gate is now built, each behind its own switch (default ON, gridworld gw12 identical OFF):

| Item | Switch | Commit |
|---|---|---|
| 0 Goals wait until the buttons are known | TETHER_HYP_AFTER_WORDS | `eb1fed6` |
| 0b What the buttons did carries to the next board | TETHER_WORDS_CARRY | `dcac0e8` |
| 1a Walls readable from contact | TETHER_PASSABILITY | `36c727f` |
| 1b Names that hold | TETHER_NAMES_HOLD | `b10d2bb`, cost `87b8822` |
| 2a The agenda reader | TETHER_AGENDA | `be06f93` |
| 2b The symbol binding table | (record only, `symbols.py`) | `81dc628` |
| 3 Cards v4 and the tier-2 contrast | TETHER_TIER_CONTRAST | `9b9f7bf` |

And the fixes the T0 runs asked for, in the order they were found:

| Found by | Fix | Switch | Commit |
|---|---|---|---|
| T0: refused, never repaired | the refusal's missing condition becomes a subgoal | TETHER_REPAIR_AT_REFUSAL | `b4cb279` |
| T0b: one lp85 step took 53 min over 43,102 tied conditions | conditions that never varied are not priced; when none can pay, say so first | TETHER_GOAL_VARIES, TETHER_GOAL_FLOOR | `8df0d55`, `dd1b793` |
| T0b: count goals with no known first step | touch the goal's object and watch | TETHER_CONTACT_ROUTE | `1efbe45` |
| T0c: touching never moved the count | press what moved the same reading on another object | TETHER_KIND_LEVER | `d9ea763` |
| T0c: the subgoal ended without helping its parent | when the subgoal arrives, the refused parent is held again; refused again, that subgoal is dropped for it | TETHER_HTN_RETURN | `606f96a` |

**The T0 runs** (six games neither seat had studied, ar25 cd82 g50t ka59 lf52 lp85, 600 s each, fresh copy of central; pass = goal, refusal, repair row, subgoal, the goal again, a clear, in that order on one board):

| Run | Code | Result |
|---|---|---|
| T0 (3 games) | `acd2ca3` | refused, not repaired |
| T0b | `b4cb279` | no refusal rows; every goal a count goal with no known first step |
| T0c | `dd1b793`, KIND_LEVER off | not a pass, the best yet: refusals in 4 games, subgoals in 3, ka59 returned to a parent once; no clear through the chain. lp85 cleared level 1 without the chain |
| T0d | `16a4b3b` (= `dd1b793` agent), KIND_LEVER on | not a pass. KIND_LEVER fired 114 times and replaced touching (21 -> 2), so goals mostly ended untested and nothing was refused or repaired (repairs 4 -> 0). Its pre-registered refuter fired; the switch stays ON until the whole build is tested together (Isaiah 2026-11-16). The run shared the machine with a download and builds, so its step counts do not compare with T0c. lp85 cleared level 1 again, without the chain. HTN_RETURN (606f96a) was not in this run |
| T0e (together-test) | `0b1245c`, every switch ON, 300 s a game, quiet machine | not a pass. **lp85 cleared level 1** (without the chain). About twice the steps per second of T0d (lf52 15 in 341 s against 14 in 742 s; ka59 16 in 305 s against 19 in 662 s) and one step over 60 s (65 s) against T0d's 483 + 501 s; the bank share and the quiet machine together, not separated. The new pieces fire on real games: `words_carry` 24, `produce_key` 86, `rdl_release` 8, `rdl_offer` 2, kind lever 23 and touches 24. No goal was refused at contact, so the repair and the return had no occasion; no RDL material settled or was refused yet |

**Also added:** `library/lexicon_imagenet_wordnet.json` (the 1000 ImageNet-1k classes, each with its WordNet 3.0 synset, lemmas, gloss and hypernym chain, provenanced and licensed in its header). It is a data source read by the builders (`build_word_map`, `rdl_parse`, `recognize.build_from_parquet`), not by an agent decision; the derived `word_map.json` and `rdl_preload.json` are what the agent reads. 306 older tests were retired (108 kept), because the full suite took hours.

**The operators:** O1, ⇒ usable in an idea's guard, ordered, read as (not A) or B (TETHER_IMPLIES_BOND, `bc49790`). O2, a guard may join two conditions, not only two readings, to a declared depth of 2, offered only where it sorts the history strictly better than each part and priced as its parts plus one bond (TETHER_GUARD_NEST, `580f9ab`). O3, bond pricing: `BONDS = 1` is correct where it is used (the predict signature, r1953); the price that was missing was the joined guard's, and it landed with O2. Not yet: offering the production ledger's learned A ⇒ B pairs as guard keys (they are press and kind pairs, not two readings), and joining conditions across slots.

**Recursive Diffusion Learning has started** (2026-11-16 afternoon; design `docs/05-RESEARCH/40`, interfaces `docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md`):
- `rdl_store.py` (C1 no recordings, C2 usable needs bonds and an attach, C3 no standing field anywhere, C6 every preload stamped with stage and source) and `rdl_parse.py`, which writes `library/rdl_preload.json`: 1,494 preloads over tiers 1-4 (1000 / 36 / 445 / 13), 191 usable. They attach to library entries by cluster, never by raw name. `fa208f3`.
- `rdl_release.py` (`cd557b0`):
  - C4: tier k opens when tier k-1 has 2 settled, which is MIN_REPEAT reused. The inherited library counts as settled for tier 1.
  - Codified reach: an ordered validity table from the rdl rows. No weights.
- The agent (TETHER_RDL, `0b1245c`):
  - Released preloads break ties in the described lookup's ranking. That is search priority only: nothing becomes reachable and nothing gains standing.
  - `rdl_offer`, `rdl_settle` and `rdl_refuse` rows carry the stamp.
  - Counts carry in the lineage as `rdl_n`.
  - OFF is identical to the tree before it (gridworld 12 steps, 2,427 rows).
- Not yet: other ordering sites (the library-first offer walk, the atom-chain walk), clusters on the feedback rows, and a live settle or refuse of RDL material. Tiers above 1 open only when the board settles tier-1 material.

**And the meaning chain** (Isaiah: "it's a ball, shaped like a ball, acts like a ball; balls can roll, does this roll?"), in `docs/05-RESEARCH/42`: shape names in perception (TETHER_SHAPE_NAMES), a flat-to-solid shape bridge (disc -> sphere -> ball), a word map with categories and a synonym index, concept -> actions from WordNet both ways and ConceptNet, VerbNet classes, a vocabulary of WordNet minus NSM, and the affordance bet with its sentences (TETHER_AFFORDANCE). All preloaded with no standing; the board decides.

**Also this afternoon:**
- TETHER_BANK_SHARE (`68628e2`): one hard question no longer drains the level's whole thinking bank (T0d g50t: 52 M of allowance in one step).
- TETHER_PRODUCE_KEYS (`519ad1b`): settled productions become ⇒ guard keys by kind.
- 18 of 22 symbols bound (`5667f1a`).
- The step-5 index audit (`2ed264a`): 142 filings fixed through the builder, 253 judgement calls listed in `docs/03-DESIGN/INDEX_AUDIT_2026-11-16.md`.

**Still open:**
- The T0 gate itself: a clear through the chain.
- Four symbols unbound, each with its reason in `symbols.py`.
- The keep rules of every item above, read at the next retest that reaches enough goals and boards.

The sections below are as of 2026-11-13 and are kept as the record of how the order above was decided.

## What it is

A recursively self-improving agent that runs on a CPU, with no neural network and no training run. It perceives a board as objects, composes terms from a library of human primitives (NSM primes and the Tether's operators), plans with hierarchical task networks, and writes, prices and keeps its own programs. Everything it learns is readable. ARC-AGI-3 is the current test bed. The theory it is built from is the Tether: `figures/` and `docs/01-FOUNDATIONS/03-FIGURES_TEXT.md`.

## What works

- **It runs end to end on Kaggle.** The commit run on 2026-11-13 passed every check and played. Code at `5f811fa` (tag `kaggle-2026-11-13`), memory head `edfe475c7e5ff724`. How: `docs/kaggle/RUNNING_ON_KAGGLE.md` (arc-solver-agent and development).
- **One memory, carried across runs.** Every run's learning is saved as an archive (compressed JSON, named by hash, never overwritten) and merged into a SQL store. On 2026-11-13 the eight branch ends of central memory were joined into one (join `edfe475c`): 333 saves, all 14 data tables equal to the backup after one store-mode load.
- **Perception as objects.** Every same-colour region is an object, with kinds, contact, and who-moves-with-whom (`arc_percept.py`; the contract is `docs/03-DESIGN/01-WHAT_THE_AGENT_SEES.md`). Two known gaps, below.
- **The Tether's method as library data.** 12 rule cards from Figs 3, 9 and 13 (`library/tether_rules.json`), each with when it applies, the questions it asks, the rule in operators and NSM primes, the figure lines verbatim, and what would refute it. Kept apart from the lookups: nothing reads them yet.
- **The cards carry the method when a player runs them.** In the hand test (ls20; the proctor played from the agent's view using only the cards), 96 of 121 presses and 33 of 58 decision points came from the cards, and level 1 cleared. Caveat: in level 1, the two decisions that found the answer came from knowing the game. Only the agent itself can settle whether the cards are enough (the T0 gate).
- **Every new piece has its own switch** (default ON) and is byte-identical when OFF, proven on gridworld gw12.

## What doesn't work yet

- **It rarely clears levels.** In the 2026-11-13 runs (the Kaggle smoke on wa30, the 3-game panel on dc22, re86 and wa30 at 600 s each), no levels cleared. This is the gap everything below is aimed at.
- **The planner parts are built but silent.** HTN parts 1 and 2 (plans that start at the pick; tiers learned bottom-up) are merged and switched on, but their triggers almost never fire on real boards: route_exhausted 0 in 1,206 recorded games; split_refused 0 in five 10-minute games. Hence the standing rule: count a trigger's exit on recorded ledgers before building it.

## Where the gap is: upstream of planning

A chain of read-only counts on 2026-11-13 traced it, each one pre-registered:

1. **(i)(ii) Goals almost never reach their own test.** Across 4,547 game-runs in 23 games, a goal tested at contact happens 0 times at the median, in every game. So the gap is not in the planner. It is upstream: goal formation or routes.
2. **(iii) Most goals were parked before a single press.** In today's code, 87% of 976 parked goals were adopted while the TRY_FIRST hold was still on (the agent hadn't yet pressed every action once). The hold parked them, and a parked goal reads as a verdict. Fig 9 :60: "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict." That is a fourth class of failure: the order gate.
3. **(v)-(vii) The hold itself works as designed.** It counts action names (1 to 7 per board), every held press is an unpressed action, and it ends by pressing the last one (median 4 presses, the same as the hand test). The long holds in older records were a clause retired on 2026-11-11.
4. **The fix: TETHER_HYP_AFTER_WORDS.** While the hold is on, no goal is adopted, so none is parked. See the result below.

**Also measured:** the affordance baseline. Of the first presses on an object kind the agent had not met before in that game-run, the share that changed the pressed object itself is 0.417 at the median (board 1, 18 games; 0.500 over all boards, 19 games). That is the number a future affordance reading (shape -> concept -> properties -> predictions) would have to beat. Three games' values (ls20, wa30, re86) were flagged for a recheck when it was accepted.

## The goal fix: result

A 3-game panel (dc22, re86, wa30; 600 s each; fix ON vs OFF; one game-run per game per arm, the same starting memory) was pre-registered with a refuter and a keep rule, and read as written:

| Per game, ON / OFF | wa30 | re86 | dc22 |
|---|---|---|---|
| goals adopted | 1 / 6 | 1 / 4 | 4 / 3 |
| goals parked inside the hold | 0 / 1 | 0 / 1 | 0 / 1 |
| parked with no route, per adopted goal | 0 / 0.17 | 0 / 0.25 | 0.25 / 0.33 |
| ended goals with at least one press of their own | 1/1 / 2/5 | 0/1 / 1/4 | 3/3 / 1/3 |
| cycles from a board's start to its first goal (median) | 5 / 1 | 7 / 1 | 5 / 0 |
| levels | 0 / 0 | 0 / 0 | 0 / 0 |

- **The refuter did not fire.** ON's goals parked less, in all three games. The gate didn't just move the parks later.
- **The keep rule was not met.** The share of goals pursued with their own presses rose by 60 and 67 points in wa30 and dc22, and fell by 25 in re86, where ON had a single goal.
- **The cost, reported beside the gain and never netted against it:** the first goal on each board comes 4 to 6 cycles later.
- **Ruling (r1945): the mechanism is confirmed and the capability is not shown.** Goals adopted during the hold went from 3 to 0, as designed. With 1 to 6 goals per game, the pursuit numbers move 25 to 100 points on a single goal, so they can't show capability either way. The fix enforces the card's own order (WORDS before GOAL, Fig 3) and removes a filter that was handing out verdicts (Fig 9 :60), so it is merged with its switch ON. The keep rule is read again, unchanged, at the next retest with more goals; if the refuter fires there, the switch goes OFF.

## The two perception gaps (from the hand test)

- **Walls are unseen.** The background is one object spanning the board, so no reading says which neighbouring cells are free. Level 2's first 21 presses went to learning walls by bumping into them.
- **Names don't hold.** About 10 instances: an old name reused for a different object, an unchanged part renamed, everything renamed after a reset. A plan built on o3 breaks when o3 becomes something else.

## What's designed next

In order, each with its own switch, must-fails and DECIDES line: `docs/04-PLANS_AHEAD/02-BUILD_SEQUENCE_FUTURE_STATE.md`.

1. Finish the goal fix; then what the buttons do carries to the next board (built only once the agent reaches board 2 often enough to measure it).
2. Perception: walls readable (a passability reading earned from contact), names that hold.
3. The agenda reader and the symbol binding table: the agent runs the Tether cards itself.
4. Cards v4: four corrections from the hand test.
5. The T0 gate: the agent alone forms a goal, repairs it when the board refuses, and clears a level on a game it has never seen.
6. Housekeeping (index audit, old tests, the operators), SHIP 4, then step 9 and Recursive Diffusion Learning.

Further out, as a blueprint: the README's "Future state" (Recursive Diffusion Learning, a visual lexicon, flat boards to depth, a voice by mapping) and `docs/05-RESEARCH/40` and `41`.

## How the work is checked

Two Claude seats work on this: the proctor builds and the reviewer verifies each commit with its own checks, and Isaiah decides. Because both seats are one model, their agreement is not evidence (Fig 2 :40). So every claim rests on a ledger, a test with a must-fail, or the board itself, and each test is pre-registered before it runs. Negative results are kept: three of today's readings came back "no", and they decided the order above.
