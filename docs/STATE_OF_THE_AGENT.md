# The state of the agent (2026-11-13)

A handoff: what works, what doesn't, where the gap is, and what's designed next. Written so someone picking this up can start without the conversation history. Every claim points to a measurement or a commit.

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
