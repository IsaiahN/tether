# Changelog

Tether is a recursively self-improving agent that runs on a CPU. No neural network, no training run. It composes ideas from NSM primes, plans with hierarchical task networks, and writes, prices and keeps its own programs. Everything it learns stays readable.

Each release below is an operating-system update: it changes what grows on the kernel (ideas, search, reflexes, what the agent knows about kinds of objects), never the kernel itself, which stays fixed on the [`core`](https://github.com/IsaiahN/tether/tree/core) branch. For what that means and why, see [What recursive self-improvement means here](README.md#what-recursive-self-improvement-means-here).

Releases are listed newest first.

## 2026-11-12: Ordered search

### New
- Search for explanations runs in a planned order: skips what already failed, rescans only what changed, and tries the cheapest fitting ideas first with an exact stopping point.
- Knows where a change came from: the agent itself, a neighbor, its own clock, or something hidden.
- Keeps word senses apart by context.
- Reuse book: remembers which settled ideas paid off and where.
- Nested ideas (one idea's output feeding another) are in place but not yet used.

### Improved
- Narration weighs what it reports.
- More moves come from the agent's own reasoning rather than the fallback chooser.

### Fixed
- demo.py no longer crashes on a fresh clone.
- A finished idea is no longer marked as unfinished when the thinking budget runs out after it.
- demo.py's record check passes: board reads made while forming an idea are recorded under the right step. The previous release failed this check about 3 runs in 5.

### Known issues
- Steps run slower on tn36 and bp35. Profiling is next.
- The demo's answers vary slightly from run to run (1 wrong "can't explain" in 25 runs).

### Repository
- docs/ sorted into numbered folders, each with a README.
- Logs written to logs/.
- About 35 obsolete files removed (all kept in git history).
- Attribute index moved to library/.
- README: a section on what recursive self-improvement means here.
- CHANGELOG.md added.

## 2026-11-11: Measurement and memory fold

### New
- Records of why no idea was made, which search each candidate came from, and which reached ideas were later confirmed.
- A test showing the right entry for a one-step move ranked about 1,440th of 2,750.

### Performance
- 3.1 million one-off sightings folded into 18,071 patterns, with no counts lost.
- Pattern lookups about 50x faster.
- Recount after a save: 42 minutes down to 7 seconds.

## 2026-11-10: Memory that ages by use

### New
- Memory ages by how much has been written since, not by wall time.
- One-off sightings fold into general patterns at each game's end.
- Ties ranked by confidence, decayed by disuse, with a bonus for new ideas.

### Fixed
- A thinking-budget leak (worst overrun cut from 7.2 million to 142 thousand units).
- All 15 move choosers now respect the block on a move that lost the game.

## 2026-11-08: Lessons across lives and levels

### New
- Unfinished lookups are recorded at a life loss or level edge.
- Object kinds carried from earlier games map to new objects by shape.
- Random tie-breaks only among equally unknown options, logged as exploration.
- New names in the code are checked against existing ones.

## 2026-11-07: Thinking budget

### New
- A thinking budget for every step.
- Contact has levels: touching, adjacent, near.
- Every change to a learned weight is logged.

## 2026-11-06: Seven builds

### New
- Objects known by kind: attribute types and canonical shape.
- Bonds: how strongly two objects move together.
- Hidden causes: "something unseen did this."
- Goal types: groups, counts, "none left", "connected".
- Reflexes carry across lives; danger is read ahead; musing between games.
- One chooser decides between thinking and acting.
- Leaves a stuck plan; quits an unwinnable game.
- NSM grammar primes in the library.

## 2026-11-02: Indexed search

### New
- First level cleared by the agent's own reasoning (lp85).
- Indexed lookup with caching and pages of 32.
- Kaggle bundles.

## 2026-10-30: First public release

### New
- Splits a question in half to find a cause.
- Detects a new game on its own and puts stale ideas away.
- Breaks goals into steps it can take.
- Records exactly what is left unexplained.
- Released as two branches: general-agent and arc-solver-agent.

## 2026-10-25: Freeze and one store

### New
- Notices a game switch by itself.
- First overnight learning run (25 games, 5 rounds).

### Performance
- Library data merged from 15 files into 3.
- Saved learning in one SQLite store (3.7 million rows).
- Memory ceiling and time limits on every game.

## 2026-10-21: The 14-step list

### New
- Reused ideas are put on trial before they are trusted.
- Fatal moves are recorded and never repeated.
- An unexplained change is split into parts and each part is searched.
- One library of role-tagged entries.
- Lineage: one save history across games, in the order things happened.
- Canonical shapes; endings recorded by name.

## 2026-10-08: The figures as law

### New
- The Tether figures govern every decision, checked by a test.
- Typed placeholders; guards that refer to other objects.

## 2026-09: First real game boards

### New
- Combines simple operations into new ones on real boards.
- Contact-seeking: aims actions at what it has not yet touched.
- Failed ideas are reconsidered on the agent's own clock.
- A numbered research log of findings.

## 2026-08-22: Tether v7

### New
- The core loop: perceive, route, settle.
- The gate, and abstention when nothing explains a change.
- Generated test worlds and a self-checking test suite.
