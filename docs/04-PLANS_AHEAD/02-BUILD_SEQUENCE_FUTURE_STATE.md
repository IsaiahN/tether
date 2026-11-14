# The build sequence: future state (designed, not built)

As of 2026-11-13. This is the next stretch of work after the 2026-11-13 release. Each item is designed here in enough detail to build from. Each one also carries the check that decides whether to build it, so nobody has to guess where it stopped.

The order is set by Fig 3 :20, "Each link consumes what the one above produces", and Fig 3 :22, "A step whose input never arrives cannot be diagnosed, only its predecessor can." Each step feeds the next, so they run in this order:

```
0. finish the goal fix (HYP_AFTER_WORDS)     goals stop being adopted while the agent is still learning its buttons
0b. what the buttons do carries across boards  built only if the agent reaches board 2 often enough to measure it
1. perception                                  walls readable; names that hold
2. the agenda reader + the symbol binding table  the agent runs the Tether cards itself
3. cards v4                                    four corrections the hand test found
4. the T0 gate                                 the agent, alone, forms a goal, repairs it, clears an unseen level
5. housekeeping + SHIP 4                       index audit, old tests, the operators, release
6. step 9                                      the noise floor and the experiments; then Recursive Diffusion Learning (T1-T4)
```

## The rules every item follows

- **Its own switch, default ON.** Switched OFF, the agent behaves byte for byte as before; gridworld gw12 proves it.
- **Must-fails.** Each item ships with a test that passes with the item and fails with it removed.
- **Count before you build (the standing rule from r1923).** No trigger is built until its exit has been counted on recorded ledgers. Two planner parts were built on exits that never occurred on real boards (route_exhausted: 0 in 1,206; split_refused: 0 in five games). That cost a day, and the rule exists so it doesn't happen again.
- **A DECIDES line.** Each item is pre-registered: what reading keeps it, what reading reverts it. Where a threshold is a convention, it is named as one.
- **Design first, ruled, then built.** The designs below are the starting point. The builder reads the code site first and proposes exact fields; the reviewer checks them before the build.

---

## 0. Finish the goal fix (TETHER_HYP_AFTER_WORDS)

**Status:** built and merged with its switch ON (2026-11-13, r1945). The 3-game panel confirmed the mechanism (goals adopted inside the hold: 3 OFF, 0 ON) but was too small to show capability (1 to 6 goals per game). **What remains:** read its keep rule again, unchanged, at the next retest with more goals (per-goal own-press share up in at least 2 of 3 games, none down by more than 10 points); the refuter (ON's goals park by no_route at the same or a higher per-goal rate in 2 of 3 games) turns it OFF. The 57 parks outside the hold, found in the recorded ledgers, are the next read either way. Results: docs/STATE_OF_THE_AGENT.md.

**The defect it fixes.** In 87% of 976 parked goals, a goal was adopted while TRY_FIRST was still holding the goal path (the agent hadn't yet pressed every action once). The hold then parked the goal, and a parked goal reads as a verdict ("parked", `_parked_n`, `_door_set_aside`). Fig 9 :60: "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict." The hold is an order, so it must not decide the goal.

**The change.** One holder in `_goal_hypothesis_run`, after "routine" and before goal_choice: while TRY_FIRST's hold is on, the goal path waits; no goal is adopted, so none is parked. No new row type, state or threshold.

---

## 0b. What the buttons do carries to the next board (TETHER_WORDS_CARRY)

**Status:** designed (r1942), queued. Full design: `claude/DESIGN_2026-11-13_words_carry_across_boards.md` in the project; the essentials:

- **The idea.** A new board has some familiar kinds and some unfamiliar ones. Within one game, what each action did carries to the next board as an expectation, not a fact.
- **Record.** Per game, per action name: the effect's shape at the level of kinds (which kind moved or changed, its direction, how many objects), and its cost kept separately (for example, bar cells spent).
- **On a new board, the hold counts only** actions never pressed in this game, and actions whose carried effect has been contradicted on this board.
- **The first ordinary press is the check.** The same shape confirms it. A different shape marks it contradicted and puts it back in the hold. The same shape at a new cost (the hand test's level 2: 1 bar cell became 2) stays met, and the cost change is recorded as a changed condition.
- **No blanket "touch every kind first".** That was the retired kinds clause, which made holds run about 20 cycles.
- **Precondition, read first:** the share of game-runs that reach board 2 or later. If the median is 0, the build waits until the agent clears levels.
- **Keep:** fewer presses to the first goal on later boards in 2 of 3 games, none worse by more than one press, wrong presses no higher. **Revert:** contradicted share above one half in 2 of 3 games, or more wasted presses.

---

## 1. Perception: walls readable, names that hold

**Why first.** The hand test (ls20, the proctor playing from the agent's view with only the cards) cleared level 1 and lost level 2's first 21 presses to things the agent's view does not show. Level 2's OUTSIDE share was perception, not game knowledge. Fig 3 :22: when a step never gets its input, fix the predecessor. The method (the cards) can't work on what the agent can't see.

**The code site.** `arc_percept.py`: `components()` (4-connected, no background colour), `identity_of()` (how a name is re-found: overlap, unique-shape, look-alike), and `class Objects`. Read `docs/03-DESIGN/01-WHAT_THE_AGENT_SEES.md` first: it is the contract this item restores.

### 1a. Walls readable (hand-test finding f)

**The residual (effect terms).** The background is one object spanning the board. No reading says which cells next to a body are free and which are blocked. So the agent learned the walls only by pressing into them: 21 presses, with corrections falling 13 -> 1 -> 0 as a wall map entered the proctor's record. That map is exactly what the agent's view lacks.

**The design: a passability reading, earned, never assumed.**
- **Keep the rule that nothing is scenery.** No colour is declared background or wall. The reading is learned per game from contact.
- **Per body (an embodied object), per action axis, record two kinds of contact:**
  - **entered:** the body's cells came to overlap cells of colour c (it moved onto or through them);
  - **blocked:** a press of a moving action produced no move, and the cell the body would have entered has colour c.
- **From those, per colour class, a passability verdict:** `passable` (entered at least once, never blocked), `blocking` (blocked, never entered), `mixed` (both: the colour isn't what decides, so look for another condition), `unknown` (no contact yet). `unknown` is a value, not a failure (the same discipline as a null attribute).
- **The new reading, per body, each frame:** for each of the four neighbouring positions the body could move to, `free` / `blocked` / `unknown`, from the colour classes of the cells it would occupy. It is a reading like any other: it can be wrong, and a contradicting press refutes it.
- **Where it plugs in.** Routes read it before pressing: a route through `blocked` cells is not offered; `unknown` cells are where press-and-watch goes. This is the reach check counting contact (cards v4 c).
- **Arm:** TETHER_PASSABILITY, default ON.
- **Must-fails:** a gridworld board with walls of one colour: ON, after one blocked press into the wall colour, the next route avoids that colour; with the reading removed, the agent presses into the wall again. A second case: a colour first blocked and then entered (a door that opened) becomes `mixed`, not `blocking`.
- **Count first (read-only):** on today's ledgers, blocked presses per game-run (a moving action, no move). If the median is near 0, walls aren't what's costing presses on the competition games and this waits behind 1b.
- **DECIDES:** on a hand-test-style replay of ls20 level 2, or the first 5 games that have a body, blocked presses before the first goal adoption fall ON vs OFF in at least 2 of 3 games, with no rise in route length. If they don't fall, the reading isn't reaching routes: check the plug-in before anything else.

### 1b. Names that hold (hand-test finding d)

**The residual.** Names don't hold. About 10 instances in the hand test: an old name reused for a different object (#8, #12, #17), an unchanged part renamed (#18), and new names for everything after every reset. That breaks the contract: "a pointer, assigned once and never reused". A plan built on o3 breaks when o3 is suddenly something else.

**The design: three rules, in this order of precedence.**
1. **Unchanged means same.** An object whose cells are identical to the previous frame keeps its name, checked before any other matching. This alone fixes #18.
2. **A shared shape is not an identity.** When a candidate match is "look-alike" (its shape is shared with another object) and it has zero overlap with the named object's last cells, it gets a fresh name plus a "maybe the same as oN" link, never the old name. The existing refusal machinery (`refused`, NOT-IDENTITY) records any identity later shown wrong. This fixes #8, #12 and #17.
3. **A reset is not a new world.** On a level reset (the RESET action, or a level start that repeats an earlier start), match the new frame to the snapshot of that level's first frame, by shape and position, before minting names. Objects at their start positions get their start names back. This fixes the every-reset renaming.
- **Names are still never reused.** The counter only goes up; a retired name is never issued again.
- **Arm:** TETHER_NAMES_HOLD, default ON.
- **Must-fails:** (i) two same-shaped objects, one moves far: the mover keeps its name, the other keeps its own, no swap; with rule 2 removed, the names swap or merge. (ii) press RESET: every object at its start position gets its start name; with rule 3 removed, all get new names. (iii) an untouched object across 50 frames keeps one name.
- **Count first (read-only):** on today's ledgers, renames per game-run (a name retired and a same-shaped object named in the same frame, and resets followed by all-new names). This sizes the problem on real games, not only on ls20.
- **DECIDES:** name changes on unchanged objects go to 0 in the replay, and goals whose target name vanished mid-pursuit fall ON vs OFF in at least 2 of 3 games. If target loss doesn't fall, names weren't what broke the goals: say so and move on.

---

## 2. The agenda reader and the symbol binding table

**Why.** The Tether's rules are in the library now (`library/tether_rules.json`, 12 cards from Figs 3, 9 and 13, kept apart from the lookups so nothing reads them yet). The hand test was the pre-registered check: the proctor played ls20 using only the cards. 96 of 121 presses and 33 of 58 decision points came from the cards, so the pre-registered branch is "build the reader". The caveat travels with it: in level 1, the two decisions that found the answer were game knowledge. Only the agent itself, which has none, can settle whether the cards carry the method. That is the T0 gate (item 4).

### 2a. The agenda reader

**What it does.** It runs a card the way the hand test did, as the agent's own thinking step.
1. **Describe the residual** in effect terms (the card "Describe before you look" runs first, order 0): what changed, how many things, what is interchangeable, at what scale.
2. **Look the card up by the residual's shape**, matching the card's `when`. A card is never lit by a word in a reading. It is chosen by the shape of what is unexplained. Ties are broken by the card's `order` field (Fig 3: upstream first).
3. **Run its `asks` in order, as child questions.** Each child is answered from one of three places, tried in this order: the board's current readings, the agent's record, a press-and-watch. A child answered moves to the next. A child that can't be answered is the agenda's next residual (recursion: it gets its own card).
4. **Check `refuted_by`** after each answer. If it fires, the card's pairing didn't bear on this residual; drop to the next card by order, and record that it fired.
5. **Write one decision row per step,** in the same shape as the hand test's records: residual | card | question | answer (and from where) | press | why. This is what makes the agent auditable the way the hand test was.

**Budget.** Depth is capped by the same budget as other thinking (no new clock), and a question asked twice on one board without a new reading is not asked a third time.

**Where it sits.** Beside the goal path, not replacing it. Its first job is the WORDS -> GOAL -> ROUTE chain of "Which link first": it decides which link is unmet and asks that link's question. The goal path still forms and pursues goals; the reader supplies the questions that lead to them.

**Arm:** TETHER_AGENDA, default ON. OFF: the cards stay unread, as today.

**Must-fails.** On a fixture board with no progress, the reader picks "Which link first", asks SEE before WORDS, and writes the rows; with the reader removed, no rows. A card whose `refuted_by` fires is dropped and the next card by order is used.

### 2b. The symbol binding table

**Why.** `grammar.json` holds the formula's symbols (Γ, R, closure(Γ), φ, |φ|, |R|φ|, a, o′, Γ(b,a)) as text only. Nothing binds them to anything the agent can read at run time. Fig 9 :30: "your words are borrowed too". A symbol the agent can't evaluate is a name with nothing behind it. The cards' `do_sym` fields can't run until this table exists.

**What it is.** A table: symbol -> the agent reading that evaluates it, with the unit and where it is read. The meanings are the Symbols table's own words (docs/01-FOUNDATIONS/03-FIGURES_TEXT.md, "Symbols table"). The bindings are proposed, to be confirmed against the code by the builder:

| Symbol | Meaning (Symbols table) | Bound to (proposed) |
|---|---|---|
| Γ | the library: everything the system can currently express | the library as loaded (inherited plus learned terms, with standing) |
| atoms(Γ) | the primitives | the library's atoms (terms not built from others) |
| closure(Γ) | the reach: everything expressible by combining the primitives | the reach check's answer: can a term of this shape be composed from Γ |
| b | the belief, before it acts | the agent's expectation per slot before the press (history and inherited prior) |
| w | the weighting between private history and inherited prior | the lineage weighting already applied when a learned term and an inherited one disagree |
| a | the action | an action name, with its recorded effect (shared with item 0b) |
| o′ | the observation: what actually happened | the frame after the press |
| Γ(b,a) | the prediction | what the library predicts for each slot given b and a |
| R | the residual: the gap between prediction and observation, per slot | per slot, the observed change the prediction missed |
| s | the slot | one tracked object (a pointer name, item 1b) |
| R⁺_s | the live mass on slot s | the per-slot unexplained mass the reading order already uses |
| φ | a candidate term | a term being considered for minting |
| \|φ\| | its cost, under a declared code | the term's description length (the bits the pricing already computes) |
| \|R\|φ\| | the leftover once φ explains what it can | the residual after applying φ's prediction |

**Its first job: state vs structure** (cards v4 a). "Where the body is" is a STATE (space). "A corridor" is a STRUCTURE (a network of free cells). The hand test miscited exactly this (#9: a containment question asked as a structure question). The table tags each reading as state (space, time, energy) or structure (spectrum, gradient, network), so the reader can pick "A state asks for its structure" or "A structure asks for its states" correctly.

**Must-fails.** Each binding has a test that evaluates the symbol on a fixture and checks the value; an unbound symbol in a card's `do_sym` makes the reader skip that card's symbolic form and write "unbound", never invent a value.

**DECIDES (2a + 2b together):** on the 5 retest games, the reader writes decision rows in every game, and the share of goal adoptions preceded by a reader question is above one half (a convention). If the reader runs but goals don't follow its questions, the plug-in point is wrong: the reader is talking to nobody.

---

## 3. Cards v4

Four corrections from the hand test. The cards are library data, so v4 is a new version of `library/tether_rules.json` with its sha held by `build_library.py --check`, byte for byte, and each change is a corpus edit approved as one.

**(a) State vs structure.** Each of "A state asks for its structure" and "A structure asks for its states" gets a worked example in its own text: a body's position is a state; a corridor, a path or a group is a structure. The binding table (2b) supplies the tag at run time.

**(b) Refutation becomes a subgoal.** "Three texts before acting" fired its `refuted_by` at hand-test #11 (all three texts present, and the press still didn't do what it was for). The block showed a condition the context reading missed, and that condition became level 1's second goal. v4 says so: when this card's refutation fires, ask which text was thin; if it was CONTEXT, the missing condition is a new subgoal ("enter o3" needs "the carried pattern matches" first). This is the decomposition the planner needs, at the place the board actually refuses a goal.

**(c) + (g) The reach check counts contact and budget.** "Could it be reached at all" was never used in level 1, and came late in level 2 (#41 missed, first used #46). Its `when` ("before searching any question") assumes a library question. On a fresh board, a press-and-watch reaches by contact. v4: contact is a route in the reach check, and the check also weighs the budget (moves left, bar cells left) before a route is chosen. At #86 the pair ran exactly as written and paid: reach -> no, on this bar -> narrow what is missing by its effect ("more bar") -> the refill found at #88.

**(e) A new card: "Could it have come out the other way?"** At #46, "kept" and "restored" read the same, so 21 presses (#100-#120) were built on a reading that couldn't have come out otherwise, and they fell together at #121. The same shape is in the tier-2 rules: a J that changes on every step agrees with every opening and carries nothing (Fig 2 :29-30: "If it moves when you push on it, it is not an anchor"). One card for both:
- **when:** before a reading carries a plan or a rule;
- **asks:** "Could this reading have come out the other way? Which press or board would have shown the opposite?";
- **do:** count K-after-J only where J changed on some steps and not others, and score it by contrast, P(K opens | J changed) minus P(K opens | J did not), not by count alone;
- **refuted_by:** a plan built on a reading that later proves uninformative, or a tier-2 rule whose contrast is 0.
- It ships with the tier-2 contrast check as one test.

**DECIDES:** cards v4 are kept if, on the next hand-test-style audit or the reader's own rows, the miscitation of state vs structure goes to 0 and no plan rests on a reading the new card flags. Otherwise the card text is the problem, and it is revised before T0.

---

## 4. The T0 gate

**What it is.** The single check that decides whether the agent can run the Tether's method on its own. It is the prerequisite for everything in Recursive Diffusion Learning (docs/05-RESEARCH/40).

**The test.** The agent itself (no seat at the controls, no game knowledge), with the agenda reader and cards v4, on a game it has never seen:
1. forms a first goal (G1) from a reader question;
2. is refused by the board (G1's own test fails at contact: arrived, no clear, or blocked);
3. repairs it: the missing condition becomes a subgoal, and the repaired goal (G2) is formed;
4. clears a level.

**The games.** Neither the five retest games (vc33, tn36, ft09, dc22, bp35) nor ls20 (both seats know it). Chosen before the run, from the remaining games, three of them, named in the pre-registration.

**What counts.** The ledger rows: reader decision rows, the G1 adoption with its source question, the refusal row, the subgoal row, the G2 adoption, and the level clear, in that order on one board. A clear without the chain doesn't count (a lucky press is not the method).

**DECIDES:**
- **Pass:** the full chain on at least one of the three games. Recursive Diffusion Learning's T1-T4 open.
- **Chain without the clear** (G1 -> refusal -> G2 rowed, no clear): the method runs; the gap is downstream (routes or budget). Read the G2 pursuit before anything else.
- **No refusal rows** (goals never reach their own test): the gap is still upstream, as the 2026-11-13 reads found. Return to goal formation and routes.
- **No reader rows:** the reader isn't wired. Fix that first.

---

## 5. Housekeeping, then SHIP 4

**Step 5: the index audit.** The SQL parity half is done (the join and the store-mode load on 2026-11-13: all 14 data tables equal to the backup). What remains: audit the index, every entry against its source, and fix filings that point at the wrong described effect.

**Step 6: old tests.** Fix, re-pin or retire, named per test. Pinned-by-cycle tests break when an earlier change moves the path; re-pin them by occasion kind, not cycle number.

**The operators (added after step 7).** O1: ⇒ wired (implication usable in terms). O2: nesting with a budget and a guard on nesting depth. O3: bond pricing (today BONDS = 1).

**SHIP 4.** development -> arc-solver-agent (the release merge), one scrubbed general-agent pull request, and a CHANGELOG entry.

## 6. Step 9, then Recursive Diffusion Learning

**Step 9.** The noise floor (the first run on the new version, done twice), cycles by the stopping rule, and the four experiments, each on its own data branch. It stays last so its baseline is the version everything above produced.

**Recursive Diffusion Learning.** After T0 passes: T1 (format: raw preload vs parsed with bonds), T2 (schedule: all at once vs bridled release), T3 (reach policy vs uniform search), T4 (drift guard). The design and its constraints C1-C6 are in docs/05-RESEARCH/40-WATSON_2026-11-13_RECURSIVE_DIFFUSION_LEARNING.md, and the companion on strata and islands in 41.

## Sources inside this repo

- The hand test and its audit: the reviewer's rulings r1912, r1922, r1923, r1925 (in the project's ruling record).
- The goal-path reads: r1926 (i)(ii), r1937-r1939 (iii)-(vii).
- The cards: `library/tether_rules.json`.
- The figures: `docs/01-FOUNDATIONS/03-FIGURES_TEXT.md`.
- What the agent sees: `docs/03-DESIGN/01-WHAT_THE_AGENT_SEES.md`.
