# Changelog

Tether is a recursively self-improving agent that runs on a CPU. No neural network, no training run. It composes ideas from NSM primes, plans with hierarchical task networks, and writes, prices and keeps its own programs. Everything it learns stays readable.

Each release below is an operating-system update: it changes what grows on the kernel (ideas, search, reflexes, what the agent knows about kinds of objects), never the kernel itself, which stays fixed on the [`core`](https://github.com/IsaiahN/tether/tree/core) branch. For what that means and why, see [What recursive self-improvement means here](README.md#what-recursive-self-improvement-means-here).

Releases are listed newest first.

## 2026-11-20: Semantic reading, optional recognition, and a measured kernel (v1.0.5)

Since v1.0.4 (2026-11-13) the operating system gained a semantic layer and a way to grow it without training. The kernel is unchanged. This entry summarises 8 release PRs merged to general-agent (#14-#21) and the stability work on development.

### New
- **Recursive Diffusion Learning (RDL) grew up.** Two more strict-last ordering sites (library-first offers, ordered closure) behind TETHER_RDL; a generation-stamped parser rebuild from carried `rdl_n` counts, written beside the generation, never over the read-only Kaggle `library/`. OFF is byte-identical. The two new tie-breaks fired zero times on the panel because there were no ties — no synthetic match was manufactured.
- **Recognition without a neural network.** AKAZE keypoints, bitwise-majority centroid memory, Lowe-ratio voting, RANSAC geometry and abstention; a 44-class preloaded shape library (352 generated images) shipped in the repo; a fast Hamming index and abstraction-level centres; corner counting separates hexagons to decagons. Held-out accuracy 134 of 176 (the earlier record of 136 was corrected). A measured closed-outline guard (SHAPE_MAX_SHARE 0.75, set between held-out max 0.4803 and noise ~0.98) stops frame-filling noise being named `sphere`.
- **An optional, data-detected ImageNet class memory.** The class memory activates only when parquet data is detected AND a built memory loads, emitting one legible `class_memory_active` or `recognised_inert` row naming the exact reason. It is never committed, never on the agent path, and inert when absent. Detection uses `rglob` so the real 308-shard download under `data/` is seen. A small offline builder maps ImageNet labels to WordNet ids, the same AKAZE index used for shapes. A picture on a board observation is named once per holder and picture through `TETHER_RECOGNISED`.
- **Words, relations and affordances.** Shape names on every object; a word map linking library entries to WordNet meanings; 3,577 action priors from WordNet definitions; reverse dictionary from example sentences; the affordance bet ("this is like a ball; a ball can move") checked against the board; motion words when a concept predicts movement; ConceptNet/VerbNet relations feeding the bet.
- **Operators and symbols.** O1 (⇒ as a guard junction) and O2 (nested junction guards with a depth budget); CAN_PRODUCE's settled productions offered as kind-keyed guards; five more formula symbols bound to readings that now exist.
- **A NEEDED admission clause** (Isaiah, 2026-11-20): the third category, for atoms acquired during the build and later load-bearing (`kind`, `grew`, `shrank`, `turned`, `scale`, `shape_name`), each with a recorded reason. Admissions read `necessary: 38, handed: 40, needed: 6`. The ablation can now tell birth-given, handed and acquired-and-required apart.
- **A 2-D domain-agnostic test world** where derived relations and deltas are load-bearing: 12 distinct minted atom names with hooks on, 0 with them off, each episode in a fresh process.
- **A structure-hash primitive:** a stable SHA-256 of term form (atom order, operand tree, guard structure, types), never slots or ids; unwired, with a must-fail control.
- **A new README** (figure-by-figure index, DOI badges, FAQ, prior art, quickstart), with the capability list marked as design commitments, not results.

### Improved
- **Per-stage timeouts from measurement**, approved by Isaiah: lint 1900 s from a measured 1261.6 s, m2 1500 s from ~960 s, the 180 s default kept. A single global value large enough for m2 would hide every other hung stage.
- **m2 stability:** 44 to 66 of 68 checks with the agent draw pinned, zero new failures. The accounting closed exactly (44 parent + 1 book declarations + 3 attribute flags = 48, plus 18 re-pins). The apparent hash-seed nondeterminism was withdrawn: it was the agent's own recorded draw (`TETHER_AGENT_SEED` defaults ON); replay from a named record reproduces exactly.
- **Instrument fidelity:** recshape detects records by producer data-flow; wiring abstains (rc 2) across a changed artifact set instead of inventing transitions; lint triaged with reason-bearing DATA exemptions (REACH/SINGLETON fixed, findings that have no documented source left standing honestly); the shipped seat green at 36 of 36 invariants; the book registry declares every key with its zero-meaning; narration faults are recorded instead of silent.

### Fixed
- Shape-noise false positive, RDL module objects in agent state breaking `copy.deepcopy`, an undocumented hardcoded recognition path, six silent narration rows, the ImageNet parquet detector's top-level-only glob (the real shards live under `data/`), and the class-memory detector reading a fully populated directory as "no data."

### Measured, not claimed
- **T0 gate on six unseen games, 600 s each, every switch on: 0 of 6 pass.** Goal and goal-again on 6 of 6, refusal on 5 of 6, repair on 3 of 6, subgoal and clear on 0 of 6. The chain stops because the goal was already satisfied at its own test (`arrived_no_clear`), so no open condition exists to decompose. Diagnosed at the write site; no game was tuned to. A WATSON (research note 43) directs goal formation to describe that residual, look up a frame predicting the win condition's shape, then narrow ranked candidates.
- **RDL ground feedback has never fired on gridworld** (its attach names are ARC-domain entries that world never reaches) and **recognition is inert on real boards** (no picture field). Both recorded as test-world limits; no synthetic path fabricated.

### Known issues
- Two m2 checks left red as NEEDS-DESIGN (no moved winner in this world; the library-winner route). No assertion was weakened.
- 61 ANCHOR and 15 ISOLATED lint findings left standing: no documented source for those constants, and no safe mass-deletion; no anchors were invented.
- The full conform check is 21 of 25 seats clean. The two FAILs are stale local panel artifacts and the remaining m2 fixture debt. One stage reports INCOMPLETE and one DID-NOT-RUN, neither folded into a pass.

## 2026-11-16: Recursive Diffusion Learning begins

### New
- Recursive Diffusion Learning starts (TETHER_RDL, on by default). Material is preloaded, never pretrained:
  - The WordNet lexicon, the attribute index and the Tether cards are parsed into four tiers: instances, regularities, abstractions and core rules. Each tier loses more detail than the one below. Every entry is stamped with its stage and its source, and none has standing.
  - Only entries that carry bonds and reach something the agent can compose over, by cluster and never by raw name, are offered: 191 of 1,494. The rest are recorded.
  - A tier is released only after the board has settled enough of the tier below. The inherited library counts as settled for the first tier.
  - What settles and what is refused is counted by tier and source, carried across generations, and turned into an ordered search policy.
  - Released material changes only where the agent looks first among equally good candidates. Only the board gives standing.
- Objects have shape names. Each object's own cells are read as a dot, line, square, rectangle, ring, plus, L, T, diamond, disc or irregular shape. Each name is a stated geometric rule, and colour and position play no part. The disc, line and square are tied to the library's shape concepts (TETHER_SHAPE_NAMES, on by default).
- A word map links the library's entries to WordNet meanings. A meaning is chosen by the entry's domain and clusters, never by spelling alone, and ties are kept. Each entry gets a category (object, shape, action, relation, property, measure or rule) for faster search later. A synonym index takes a new word to an entry the agent already holds: "opponent" leads to the adversary. Nothing reads the map yet.
- The dictionary half of word to action: 3,577 action priors read from WordNet definitions ("a ball is hit, thrown or kicked"). Each is stamped and has no standing until the board tests it.
- A shape bridge from flat to solid: a disc stands for a sphere, which a ball, globe or marble has; a square for a cube; a ring for a torus or hoop. On a flat board this meaning is held, and an object earns "ball" only by acting like one.
- Concepts have action lists. Verbs are also read backwards from WordNet's example sentences ("Catch the ball!", "bounce a ball"), so a ball gets catch, bounce, dribble, hit and kick beside the verbs in its own definition, for 1,439 concepts. Each has its sources and no standing.
- The affordance bet. The first time the agent meets a new kind of object with a shape name, it says what the shape suggests ("this is like a ball; a ball can move") and checks it on its first press. If the board disagrees, the rule is kept with an exception for the condition it saw, and nothing is deleted. The narrator says both (TETHER_AFFORDANCE, on by default).
- Recognising pictures without a neural network: AKAZE key points from each picture are compared with a memory of each class's key points, kept small by replacing groups of similar points with their centre. A match must agree on one geometry, and the agent says it cannot tell rather than guess when the evidence is thin. Plain objects with no key points are read by their outline into the same shape names the grid uses. The memory is built from the ImageNet pictures once they are downloaded and stays on the local machine, as ImageNet's terms require. Nothing in the agent calls it yet.
- A preloaded shape library: 44 standard flat and solid shapes generated as pictures (352 in all, kept in the repository), each tied to its WordNet word and to the grid's shape names, with a memory the recogniser loads at once. Most shapes are recognised from new pictures; squares, hexagons, many-sided polygons, cubes, cylinders and cones are still weak.
- Motion words: when an object moves as its concept predicted, the agent says which way (right, left, up, down) and how ("rolls" when it keeps moving and its concept rolls, "glides" otherwise), e.g. "the ball rolls to the right" (TETHER_MOTION_WORDS, on by default).
- Recognition reads pictures without a neural network and can now name a class memory (`TETHER_RECOGNISED`): a picture on an observation is named once, the row carries the class, its WordNet synset, the route, votes or distance, the margin and whether it abstained, and an attended class is read where a shape name is read. A faster Hamming index replaces brute-force matching, and a picture that matches no single class can match a broader term ("a ball"). A blob filling more than 2% of a picture is no longer called a dot, a round outline is no longer called a polygon, and a shape invariant that has collapsed to zero is no longer charged against a picture. `TETHER_RELATIONS_READ` lets the affordance bet read ConceptNet's verbs beside the WordNet ones, a verb found in both ranking first.
- The shape recogniser counts corners, so polygons are told apart: hexagons to decagons now mostly recognised (136 of 176 held-out pictures, from 123). Squares, cubes, cylinders and cones remain weak.
- Recursive Diffusion Learning's feedback rows record the cluster through which their material reached the library, so its search order can learn by cluster.
- The library's categories guide where the agent looks first. When what changed is a movement, actions are tried first among equally good candidates; a change of shape, shapes first; a count or size, measures first (TETHER_CATEGORY_ORDER, on by default).
- A vocabulary and a relation layer. The vocabulary is WordNet's nouns and verbs less the NSM words the agent already speaks with, so what is left is what needs grounding. Verbs carry their VerbNet class, so throw brings toss and hurl. ConceptNet's English relations say what things can do, what is done to them and what they are for: a ball rolls and bounces, is kicked and hit, and is for throwing and catching. Nothing reads these yet; the ConceptNet file is CC BY-SA 4.0.
- A settled "pressing A makes kind B appear" is now offered as a guard condition, keyed by kind, never by object (TETHER_PRODUCE_KEYS, on by default).
- Five more symbols of the formula are read from the agent: the leftover once an idea explains what it can, the bond held between two readings, an idea's bonded arrangement, the round-trip gap, and the coarse view. Four stay unbound, each with its reason.

### Improved
- One hard question no longer spends a level's whole saved thinking time. The time saved is shared among the hard questions waiting, and a question waiting alone still gets all of it (TETHER_BANK_SHARE, on by default).

### Fixed
- The library index listed 142 effects that their own entries deny ("never moves", "cannot pass"), and 38 entries defaulted to a process because of them. Both are corrected through the library builder; 253 cases that need a ruling on what counts as an effect are listed for review in docs/03-DESIGN/INDEX_AUDIT_2026-11-16.md.

### Known issues
- On six games at 5 minutes each with everything on, lp85 clears its first level and the others reach their goals' objects without meeting them. No goal was refused at contact, so repairing and returning had no occasion yet. Thinking ran about twice as fast per step as the day before.
- Recursive Diffusion Learning orders one lookup site so far. In these short runs its material was offered twice and has not yet been settled or refused, so its ladder has not moved past the first tier.
- The word map's verb picking from definitions is rough, and its categories disagree with the library's own roles in 2,148 places. Both are flagged in the map, not hidden.

## 2026-11-16: The agent repairs a refused goal and returns to it

### New
- Walls become readable from contact. Each colour the agent's body bumps into or passes through is recorded as passable, blocking or mixed, and routes no longer plan through cells known to block (TETHER_PASSABILITY, on by default).
- Object names hold. An unchanged object keeps its name, a shared shape alone is no longer an identity, and an object back where a name was first seen gets that name back (TETHER_NAMES_HOLD, on by default).
- The agent runs the Tether cards itself. Each planning step it describes what is unexplained, picks a card by the shape of that residual, asks the card's first unmet question and writes a decision row (TETHER_AGENDA, on by default).
- A symbol table ties each symbol of the formula to the reading that evaluates it, or marks it unbound with the reason. It never invents a value.
- Cards v4: state versus structure, a refused goal's missing condition becomes a subgoal, the reach check counts contact and budget, and a new card asks whether a reading could have come out the other way. Tier 2 rules are scored by contrast, not by count (TETHER_TIER_CONTRAST, on by default).
- A goal refused at its own test is repaired there: its missing condition is pursued as a subgoal (TETHER_REPAIR_AT_REFUSAL, on by default).
- When that subgoal is reached, the refused goal is taken up again on the changed board. If it is refused again, that subgoal is marked as not its missing condition and a different one is tried (TETHER_HTN_RETURN, on by default).
- When no known action moves a goal's reading, the first step is to touch the goal's object and watch (TETHER_CONTACT_ROUTE, on by default). Before touching, the agent presses an action that moved the same kind of reading on another object the wanted way (TETHER_KIND_LEVER, on by default).
- What each action did carries to the next board of the same game as an expectation. The first press on the new board checks it; only actions never pressed in this game, or contradicted on this board, are held for trying first (TETHER_WORDS_CARRY, on by default).
- The production bond ⇒ can be used in an idea's guard: A ⇒ B holds unless A holds and B does not, and it is ordered (TETHER_IMPLIES_BOND, on by default).
- A guard can join two conditions, not only two readings, up to a declared depth of two. A joined guard is offered only where it sorts the history better than each part, and it costs its parts plus one bond (TETHER_GUARD_NEST, on by default).
- A lexicon joins the 1000 ImageNet classes to their WordNet 3.0 meanings (words, definition, broader terms), from the label list alone, with its sources and licences in its header. Nothing reads it yet.

### Fixed
- One step on lp85 spent 53 minutes weighing 43,102 tied goal conditions. Conditions whose readings never varied are now skipped before pricing (TETHER_GOAL_VARIES), and when no condition can pay at all the agent says so before pricing any (TETHER_GOAL_FLOOR). Both on by default.
- A refused goal's subtask method was credited as paid at the goal's earlier arrival. It is now credited when the goal taken up again ends, and only if it won.
- The commit check that counts off-agent commits crashed on Windows when reading commit messages with non-ASCII characters.

### Known issues
- On the T0 gate runs (six games the seats had not studied, 10 minutes each) no level has yet been cleared through the chain of refusal, subgoal and return. In the latest run the lever by kind replaced touching, so goals rarely reached their own test; it stays on until the full build is tested together. lp85 clears its first level in each run, without the chain.
- Carrying what the buttons do across boards only acts once a second board is reached, which few runs do today.
- Nine of the formula's symbols are still unbound; each has its reason in the table.

### Repository
- 306 older tests retired; 108 kept (everything since 2026-11-10, everything the checks or the agent name, and the gate checks). Git history keeps them all.

## 2026-11-13: Goals wait until the buttons are known

### New
- While the agent is still pressing each action once to learn what it does, it no longer adopts goals. Before, a goal adopted during that hold was parked by the hold and treated as given up (TETHER_HYP_AFTER_WORDS, on by default).

### Known issues
- Measured on three games at 10 minutes each: goals parked during the hold fell from 3 to 0, and goals given up with no route fell in all three games. The first goal on each board now comes 4 to 6 cycles later. With 1 to 6 goals per game, whether goals are pursued better is not shown yet; the next larger retest reads it again, and the switch goes off if goals park more.

### Repository
- New pages: the state of the agent (what works, what doesn't, where the gap is), and the build sequence ahead, each step with its switch, tests and deciding check.

## 2026-11-13: Plans that start at the pick

### New
- A goal picked with no known route is broken into subtasks when it is picked, not only after its routes run out (TETHER_HTN_AT_ADOPT, on by default).
- What has to hold first is learned from the bottom up: each opening is recorded whole, "K opens after J changes" is counted across openings, and the strongest are offered as subtasks (TETHER_HTN_TIERS, on by default).

### Known issues
- On the five-game retest at 10 minutes a game, neither the earlier planner nor these two parts broke down a goal: the exits they wait for almost never occur on these boards. With them off nothing changes, and with them on nothing measurable changed. Finding where goals actually stall comes next.
- The "K opens after J changes" counts include readings that change on every step, which agree with everything. A contrast check that fixes this is planned.

## 2026-11-13: Plans with subtasks

### New
- Hierarchical task planning: when a goal runs out of routes, the agent breaks it into the subtasks it needs first, and breaks those down in turn. A finished subtask hands control back to the task above it.
- Before a subtask is taken on, a quick check asks whether it can be reached at all. Unreachable subtasks are dropped before any effort is spent on them.
- Subtask methods are kept by kind, not by object. The methods that paid off are tried first, and the record carries across generations.
- The "is this possible?" check now runs before idea-making starts, so an impossible job costs nothing.
- Board reads made while forming an idea are charged to idea-making. Each read records whether this kind of object was seen before, to measure how experience makes looking cheaper.
- Blocked items can now open: an item counted as blocked because every action was tried can be read as opened when the board changes.

### Improved
- Memory reuse from an earlier level is filed under that level's key.
- The memory lookup's bucket walk is charged per read.
- Each new idea's record notes how much past evidence backed it.
- Clearer names in the records.

### Known issues
- Not yet measured on full games; the five-game retest follows this release. Each new piece has its own switch.

## 2026-11-13: Search that learns its order

### New
- Search order learned from results: when the cheaper idea and the right type of object point different ways, the agent tracks which one paid and puts it first. The record carries across generations.
- Goals with several parts try the part with the fewest routes first; a stall on the first part parks the goal.
- Like kinds first: when a shelved goal's template comes up again, objects of the kinds that won before are tried first.
- Idea trees grow one level at a time, each level priced by its own cost, with an exact stopping point.
- "A then B": an action that opened one item is offered for a closed item of the same kind.
- "A => B": each reading predicts what the last action will produce, then checks the prediction.
- Every step records what can be done, what is blocked, what was not found and what was given up.

### Improved
- Faster kind lookups in the search pass, and a faster budget check, with identical results.
- Reuse credit is keyed by the ideas a chain starts with.

### Known issues
- Not yet measured on full games; the five-game retest follows this release. Each new piece has its own switch.

### Repository
- docs/05-RESEARCH: 39 design write-ups, each settled from the Tether figures and checked against outside research.

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
