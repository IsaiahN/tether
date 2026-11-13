# WATSON + CODE AUDIT 2026-10-31 night — Does the agent remember what worked, and are library search, retrieval and saving accurate?

Reviewer seat. Asked by Isaiah:
- 21:30: "i also suspect that the agent doesnt recall the games its playing from before or cannot retrieve the rules or remember what worked and what didnt i.e what caused what effect and what didnt in particular games. i bet its just starting over from scratch again and again, thats the only way it couldnt have learned to pass level 1s. even random agents pass level"
- 21:31: "when you are done with the changes, just run a watson on what i mentioned above + a code audit and see what needs to be fixed to prove that library search, retrieval, and saving is working accurately."

The figure lines are verbatim from docs/FIGURES_TEXT.md at general-agent 1e9d4d5. Every world source below was opened and read. The code audit read general-agent 1e9d4d5 (read-only).

## QUESTION
Does what the agent learns, about which action causes which effect on which kind of thing, survive (a) from step to step within a game, (b) from game to game within a life, and (c) from life to life through the lineage? Is it then found again and used when it applies? And what would PROVE that search, retrieval and saving are accurate?

## THE FACTS THAT FRAME IT (seat, 2026-10-31)
- Rounds 3 and 4: 361 and 418 terms entered the in-memory library on the bargain; 269 and 286 settle rows. But round 4's end write carried 10 terms, and library_n went 225 -> 229 across round 3.
- 0 levels in 75 + 25 + 25 games. 2-50 presses a game. Every slice ended by time, with no death.
- The described tiers (T1a-T2, "offered before" / "carried landings") were EMPTY on a cold life (seat probe, 14:33).
- The goal lines: held a median of 3 steps, mostly "stalled", and no reach ever became a level (seat, 20:28).

## DOMAIN CENSUS
- **R:** arity 3 (an action, an effect, the kind of thing it lands on); symmetry: two boards with the same kinds are interchangeable for a rule, while their object ids are not; scale: step, game, life (lineage).
- **The game (within).** Actors: presses and their observed effects. Currency: effects known per press. Anchor: the interface's effect record and the frame.
- **The record (the library within a life).** Actors: terms, bindings, settles. Currency: terms that hold on frames they were not fitted to. Anchor: the settle rows.
- **The lineage (across lives).** Actors: the written generation and the load. Currency: terms carried and found again. Anchor: the write report and the next load's library_n.
- **Retrieval (the bridge).** Actors: a residual's description and the lit / tiered entries. Currency: carried entries that are lit, offered and bound at their first chance. Anchor: the lookup rows.
- **Union:** record ∩ lineage = what is CARRIED; lineage ∩ retrieval = what is FOUND AGAIN. Each has its own loop and its own test.
- **Order (Fig 3):** game -> record -> lineage -> retrieval.

## TETHER (primary, verbatim)
- Fig 4 :23-25: "upward: a method that can be reapplied. Never the recording of a particular success. / downward: something that makes the next search cheaper. Never a replay of what worked once. / A recording carried upward looks like knowledge and is a description of one occasion."
- Fig 10 :68: "a generator crosses, an instance does not".
- Fig 12 :107-110: "where the arrangement is recorded, re-deriving it is a lookup and the actions were spent once. Where it is not, the result carries forward and the deriving does not, so every lineage pays again. Which boundary matters is the one the record does not cross. Inside a run the arrangement persists and nothing is re-earned; across a boundary that drops it, everything is."
- Fig 6 :42: "What is recorded only grows. What is reachable is derived, and it can fall."
- Fig 5 :55: "Nothing leaves the library. What falls is the reach."

READING, per domain:
- **Within a game**, nothing should be re-earned (Fig 12 :109). What a press did on this board is recorded, and the next choice should read it.
- **Across games and lives**, the instance (this board's object ids, this game's exact press sequence) must NOT cross (Fig 10 :68, Fig 4 :25). What must cross is the METHOD: "ACTION_k moves an object of kind K by +1 along x", or "a click on kind K recolours it". It is carried as a kind, and it is what makes "the next search cheaper" (Fig 4 :24).
- So Isaiah's suspicion has a precise Tether form. **If the lineage carries almost no methods, every life pays again (Fig 12 :108-109), which is "starting over from scratch".** And if a carried method is never FOUND at a new board's first steps, it is recorded but not reachable (Fig 6 :42). That is starting over in effect, even with a full library.
- **Triangulated:** Figs 4, 10, 12, 6 and 5, with low overlap.

## WORLD (secondary; each source read)
- **Harlow's learning sets (1949; via Thomas 2012, Encyclopedia of the History of Psychological Theories).** After a series of two-object problems, monkeys became "near-perfect on trial 2 and subsequent trials" of NEW problems: "learning to learn". What transferred was a strategy, "win-stay, lose-shift", not the objects. And the "error factor theory": the animal learns to drop response strategies that fail.
 - Predicts: across games the agent should carry a METHOD for finding out what a new game's actions do (press once, keep what changed, drop what did nothing). It should then reach the effects of a new game's actions in very few presses. Corroborates Fig 4 :23-24. And it predicts the measurable sign of learning across lives: presses-to-effect-known on a new game should FALL from life to life.
- **Complementary learning systems (McClelland, McNaughton & O'Reilly 1995, Psychological Review 102:419-457).** "The hippocampal system permits rapid learning of new items without disrupting this structure"; "the neocortex learns slowly to discover the structure in ensembles of experiences". Memories are reinstated and interleaved, so structured knowledge accumulates.
 - Predicts: two stores with two jobs. A fast per-game store (instances: this board's effects) and a slow cross-game store (structure: kinds, methods), fed by replaying many episodes. If the slow store keeps almost nothing (10 terms of 361), structure never accumulates. Corroborates the record ∩ lineage domain.
- **Schemas (Tse et al. 2007, Science; via Squire 2007, Science 316:57-58).** Rats with an established schema learned new flavour-place pairs in ONE trial, and the memory was neocortical within 48 h. In an arena whose pairings were rearranged ("inconsistent"), one-trial learning failed.
 - Predicts: once the right kinds are carried, a NEW game consistent with them is learned in very few presses. Where nothing carried applies, learning is slow. So a carried method has to be FOUND at a new board's first contact, or it is as if absent. Corroborates the lineage ∩ retrieval domain.

No conflict between the figures and the world.

## CODE AUDIT (read-only, general-agent 1e9d4d5; two audits, key lines re-read by the reviewer)

### A. Within a game: it keeps what worked, while the game lasts
- Seat R2 (21:40): after an action first changes the frame, the agent presses it again in 39-44% of the next 10 presses, against a 14-25% chance. Dead presses are 6% overall, but concentrated: ft09 round 4, 8 of 8; lp85, 0 of 10 changed in its first 10 presses, EVERY round.
- The interface's action-effect table is per board by design. interface.py:477-480: "This table starts empty on every board and is filled only by acting." aimed_effect "must not cross: never persisted" (536-543). Arm 17's tally is "per action on this board" (149-154).
- retarget empties the bindings at every level (tether.py:4045, `self.bound, self.trace = {}, []`), keeping them only across a death.

### B. Across games and lives: what the lineage carries
- **Saving and loading work as written.** In a synthetic check, 108 settled instance terms (`take<oN.row|col|colour>`, `inc . take<oN.attr>`, `neg . take<oN.attr>`) were written, then loaded into a fresh agent. All 108 settle rows were applied (not_held 0), and 5 KIND terms were installed.
- **But a kind of two or more atoms LOSES ITS ATTRIBUTE.** gamma.kind_of (gamma.py:1244-1254) keeps the operand (with ids blanked to "?") only when the bare composition would collide with a PRIOR atom. Otherwise the operand is dropped. So `inc . take<o1.row>` and `inc . take<o1.colour>` both come back as `inc . take`. In the check, `inc . take` came back holding 36 confirmations from three different attributes. The save key keeps the attribute (gamma.py:1626), so the save is finer than the load.
- **So evidence is pooled per bare kind** (lineage.py:514; gamma.py:1136-1155). One case that worked and eleven that failed net out to an unsettled kind. This is the most likely cause of "forgets which action did what": the "what" (the attribute) is erased at the boundary.
- **The cause object's kind is not carried either.** The operand becomes "?" (gamma.unbound_form, 1612-1618), and nothing records what kind of object the cause was.
- **Never written, so gone at a game's end:** paths, _refusals, _not (tether.py:3647-3654, 4103-4109), though the code's own comments say this evidence "does cross"; _dir, the action/sign movability store (3657); the move map (4127); candidates (3403); _contact_seen (on purpose, 12784-12786); the ruin vetoes (574-577).
- **Decay across lives is on the wrong clock.** gamma.py:915: `gap = max(0, tick - self.last_tick)`, where tick is the cycle number. last_tick is carried (lineage.py:198), but the cycle restarts at 0 in each new LIFE (tether.py:3687). It does not restart per game: inside a stream life there is "ONE CLOCK" (tether.py:10166). Corrected by the seat's P3, 21:53. A carried refutation stops decaying until the new life passes the old last cycle. The code says it "needs a games counter, which does not exist yet" (gamma.py:936-942).
- **The fault exclusion never matches.** lineage.py:493 tests `residual.endswith(f"@{fc}")`, but residuals are written as `reuse:…@c:stamp` (tether.py:18165) and `…@c:event:p` (4883). So terms from a faulted cycle can still be carried.
- Smaller: rows with a guard_ref skip dedup and are rewritten every game (lineage.py:497); the side-file writes swallow every exception (678-693); a store refusal falls back quietly to the slow re-fold (1203-1206).
- Why round 4 showed "361 entered -> 10 carried": "terms" counts each write's NEW rows (lineage.py:473-476, 644-648); many entries are carried kinds re-bound on a new board under a new name (tether.py:10284-10288); and instances whose blanked key is already held are de-duplicated with no alias (lineage.py:495-501). That much is design. Most of the loss of MEANING is item 2 (the attribute).

### C. Retrieval: is carried knowledge FOUND when it applies?
- **Nothing carried is used before the first miss.** Prediction is `bound.get(slot, IDN)` (tether.py:9652, 9858), and bindings are empty at every game and level start. So at step 1 every slot predicts "nothing changes", whatever the lineage holds. A slot with fewer than 2 trace rows is routed NOVEL with no fit (11318-11319). Nothing predicts what ACTION1 does before it is pressed.
- A probe, cold life vs a life loaded from it on the fake game: bound {} in both; _pred_by all None at step 1 in both; iface.table 0 in both. The loaded life carried `translate<?.drow>` and `translate<?.shape>`, and re-bound one of them a cycle EARLIER than the cold life (3 vs 4) and the other a cycle LATER (6 vs 5).
- **Carried kinds only reorder.** The tiers (T1a-c, T2) order candidates. Binding happens only in _library_fit -> retrieve -> _rebindings, after a miss (10659-10686, 10253-10282).
- **The kind key is the exact shape.** _kind (6309-6324) is the attribute types plus `form=<hash of the exact cells>` (arc_world.py:509-523). Every object has all 6 attribute types, so the shape hash is all that tells kinds apart. A rotated, recoloured or grown object of the same kind is a different "kind", and the hash is dropped when the object is untracked.
- **T1 locks itself.** T1a-c fill only from OFFERS (5437-5439). _lib_offer withholds anything "already held" (8065-8066). On the fake game: 5 offer rows against 4,494 landings.
- **T2 is empty by construction** under DELTA_KIND, which reads only landings with no delta kind (lineage.py:963-964; tether.py:5204-5207).
- **T1d holds every entry that ever compiled,** not ones that explained (6016-6059). The loaded life listed ~885 carried, unlit entries beside 1,086 lit. That is part of why lookups grow with the lineage.
- **The costly reach runs before the cheap recall.** Each fit first runs the full _lookup / _library_reach (10566), spending the step budget, and its offers feed only the mint (6616), never the rebind.
- retrieve() is called without in_type / out_type (10659), so it always ranks as "val". This affects ranking only.

- **In the round's own data (seat R3, 22:02, the frozen 29094f4c library):** 6,645 distinct terms. 380 are press terms (guard TOUCH 316, ACTED_SELF 64), and NO term names an action. In round 5, 22 press terms were pulled and rebound and 16 settles were accepted on them. Only ONE of those 16 came in a game's first 3 presses. The library holds "my press did X here" in kind form, but it almost never pays at first contact.
- **Within a game (seat R2, 21:40):** an action that changed the frame is re-pressed in 39-44% of the next 10 presses, against a 14-25% chance. lp85 opens with 0 of 10 presses changing anything, every round.

- **How much of the library loses its cause on load (seat, 22:17):** of the 380 press terms, 312 (82%) are multi-atom with an operand, and the load turns them into attribute-less chains. Of all 6,645 terms, 5,311 (80%) do. So for about four-fifths of what the agent has learned, the "because of what" is dropped at every boundary.

### D. Test coverage: what is and is not proven
- Tests exist for single-life retrieval (test_m4, test_reach, test_reuse_candidate, test_carry, test_library_explains), identity tests (test_tiers_index, test_tiers_draw, test_fit_tier0, test_fit_dedup), and the lineage (test_lineage_carry, test_kind_save, test_save_dedup, test_lineage_boundary, test_settled_core, test_used_carry, test_consolidate, test_lineage_merge, test_cold_start).
- **The one cross-life retrieval test is RED at HEAD.** tests/test_k1.py:277, K(b): `known_dk` is 0 against 4,494, because W-4 (tether.py:300) keeps those rows in the on-disk snapshot. Every later check (MF-K-CUT, MF-K, S, MF-S, P) is skipped.
- **Nothing asserts** any of these:
 - that the attribute of a multi-atom term survives a save;
 - that a carried term is lit, offered, bound and settled in a LATER life or game;
 - any first-step prediction from carried knowledge;
 - that lookups get no more expensive as the lineage grows;
 - that standing decays on a games clock;
 - a round trip on a real ARC game with hundreds of installs;
 - store-path vs re-fold-path counters equal.

## VERDICT (from the figures, per domain)
- **Within a game:** the record mostly works. What changed is re-pressed above chance. But a game opens blind (lp85: 10 dead presses, every round), because nothing carried predicts a press before it is made.
- **Record ∩ lineage (CARRIED):** Isaiah is right in effect. The lineage carries the kind of a rule but drops WHAT it acts on (the attribute) and WHAT caused it (the cause object's kind), and it pools their evidence. By Fig 4 :23-24 a method must be "reapplied" and must make "the next search cheaper". A kind with no attribute and no cause does neither. Fig 12 :108-109: "every lineage pays again".
- **Lineage ∩ retrieval (FOUND AGAIN):** what is carried is reachable only after a miss, keyed by an exact shape hash, through tiers that fill only from this life's offers. By Fig 6 :42 it is recorded but barely reachable. Schemas (Tse) and learning sets (Harlow) say the gain from carried structure comes at the FIRST contact with a new problem, and that is where the agent never consults it.
- **The instance rule stands.** Object ids and per-game press sequences must not cross (Fig 10 :68). The fix is to carry the method as a richer KIND (the attribute and the cause's kind are not instances), and to use it at first contact.
- **Triangulated:** Figs 4, 10, 12, 6 and 5. The world corroborates (Harlow; McClelland et al.; Tse / Squire).

## WHAT TO FIX (ruled by the reviewer, r603), and the TESTS THAT PROVE IT
Proof first: each fix ships with the test that fails today and passes after.

| # | Fix | Proof test (must fail today) |
| --- | --- | --- |
| F1 | A multi-atom kind keeps its attribute (blanked ids "?", attribute kept), so the load is as fine as the save | P1: settle `inc . take<o1.row>`, refute `inc . take<o1.colour>`, write, load fresh: two kinds come back with their own standing (FAILS today, seat 21:53) |
| F2 | The cause object's kind is carried with the term (kind, never id) | P2: a CAUSE term from game 1 loads with its cause kind; on a game-2 board with that kind it is offered with that partner first |
| F3 | Decay on a clock that continues across lives (games or lives, the counter the code already names) | P3: a refutation carried into a new life decays, not stalled by the cycle restarting at 0 (FAILS today, seat 21:53) |
| F4 | The fault exclusion matches the residual formats actually written | P4: a term from a faulted cycle is never carried (FAILS today, seat 21:53) |
| F5 | test_k1 K(b) repaired to read the on-disk snapshot, and extended | P5: life 2 OFFERS and BINDS the carried entry life 1 offered |
| F6 | First contact uses what is carried: at a game's first steps, settled carried kinds whose atoms apply to an object kind on the board predict that object's slot (bound with a fresh operand of the matching kind), and are checked by the ground like any other bet | P6: game 1 settles "ACTION_k moves kind K"; at step 1 of game 2, a slot of a kind-K object has a non-None _pred_by from the carried kind, and the first press either confirms it or refutes it |
| F7 | The kind key tolerates the same object moved, recoloured or rotated (a ladder: exact shape -> shape up to symmetry -> attribute types), and does not drop when untracked | P7: the same sprite moved or recoloured on a second board hits T1a or T1b |
| F8 | T1d holds only entries that EXPLAINED, not every entry that compiled | P8: over lives 1-3 on one seed, T1d <= lit and per-lookup _spent does not rise |
| F10 (= M1, morning design, from round 6's 22:45 rows) | The mint grows candidates outward from the contact: the objects and attributes that changed in this residual seed the chain, and the bound is spent on candidates that touch them. The mint budget is split across the slots owing by how much each is owed or by surprise (graded effort), not one slot a step, first-come | P10: on round 6's logged residuals, replayed offline, candidates_priced > 0 in most parks (today 46 of 66 price zero), and at least one owing slot other than the first is minted in a step. Then on a fake game with a planted new rule (no library term explains it), the rule is minted within N steps of its first residual |
| F9 | The cheap recall runs before the costly reach: a held, carried or offered explainer is tried by one-pass check first, and the reach runs only if it fails | P9: with a planted IMPORTED explainer, route and rebind rows are identical with the reach stubbed out, and _spent / reach_s fall |

**Overnight status (seat, 22:13; branch wip/memory-proof-2026-11-01 = d07d1c1):**
- The proof suite is committed (a4b0d8c). P1, P3 and P4 failed at 1e9d4d5, as predicted.
- F4 is committed (a7ff3a0): P4 passes ON and fails OFF.
- F3a is committed (d07d1c1): decay no longer stalls in a new life. P3 passes ON and fails OFF. A true games clock is still a design question.
- **P6 FAILS as predicted** (034c86a, tests only). Life 1 settled and carried 10 terms. At step 1 of life 2, 0 of 19 slots have a predictor. That is "carried knowledge predicts nothing at first contact", proven by test.
- **test_k1's K(b) fails before its repair** (known_dk 0), as the audit said.
- **Round 6 (per-game writes, 22:39):** 0 mint and 0 accept rows in all 6 games, so each write carries 0 new terms (not a dedup). Library terms ARE re-installed 8-43 times a game and settle 1-19 times. So retrieval works mid-game, but only after a miss (P6), and nothing new is minted (rounds 3-6: 4, 0, 0, 0). The step_mint rejection reasons are asked for (r615).
- **F5 DONE** (1c10e1b, tests only): test_k1 K(b) rc 0. Life 2 holds life 1's 4,494 index rows. So saving and loading are proven across lives. Use at first contact is not (P6 red).
- **Why nothing new is minted (round 6, 22:45):** starved, not refused. There is one mint a step, and 438 slots were deferred. That mint parks with its budget exhausted in 58 of 66 parks, and 46 of 66 priced ZERO candidates. About 976k chains were cut "bounded out on cost" before reaching the bargain. Library-term pricing: 78 did not pay, 1 paid.
- **M1 (morning design):** the mint enumerates blind and cuts on cost, the same fault as reading the whole library. It should grow candidates outward from the contact (what changed in this residual). Its budget should be split by how much each slot is owed or by surprise, not first-come.
- **P8 PASSED, against the audit's prediction** (f36f792, tests only). Over 3 lives of 30 steps, T1d stays at or below lit and spent per lookup does not rise. But mean T1d grows 606 -> 786 -> 872 against a flat ~1,095, with the margin -201 -> -96 -> -47. So the mechanism is visible, but the predicted FAIL is not shown. The prediction is withdrawn as stated, and F8 is now a design question. A longer P8 waits.
- **A RED must-hold (22:55):** test_lineage_carry --on at d07d1c1 fails on its fixture precondition ("no same-text handles arose"). F4 and F3a stay off every chain until the OFF refuter answers (r618: bisect, then show whether the fixture leaned on the faulted-cycle bug).
- **The red must-hold is not F3a's or F4's** (00:44): the OFF refuter fails identically and writes the same first generation. The base run decides tree vs box.
- **Round 6 complete:** 0 levels. 24/24 game writes verified. 6 term ROWS written in the round (tu93, cd82, sk48, cn04 x2, plus 1 in the end write). CORRECTION (Nov 1, 04:50, r662): these are not mints. A game write's "terms" counts rows new by (born, handle) identity (lineage.py:470-503), not mint events; round 8 wrote 13 term rows with only 1 mint and 1 accept in 25 games (wa30, press 8). The mint counts for rounds 6 and 7 are asked for from stream.jsonl.
- **B0 random complete:** 1 level (sp80) on 47,207 presses vs the agent's 0 on 257. That is volume, not skill: speed is a precondition for winning.
- **The red is the tree's** (base 1e9d4d5 fails the same way, same hashes). The _part_c fixture depends on two games' handle draw counts lining up by coincidence, so the fixture is the defect (r626). The repair is test only: make the precondition on purpose, with the assertion unchanged. Last green was 5caf2a3. The test is not in the landing six.
- **Correction (01:42):** both reds (lineage_carry part c and save_dedup D-4) were already measured and filed as after-deadline items by the reviewer on 10-29 (r299, r303). Tonight added part c's mechanism: game 2 re-mints the carried term before anything new. r299 already read D-4 as aliases losing nothing under KIND_SAVE.
- **Terms are not learnings; names are files (Nov 1, r662).** Round 8: 13 term rows in 10 game writes, spread over slices 1-22 of 25, but only 1 mint and 1 accept event (wa30, slice 11, press 8) and 4 invent events; 6 of the 10 term-bearing games had no mint, accept or invent row. WRITE_CHECK's names (+75) count FILES: each write adds gen_, idx_, ak_ (25 writes x 3). My r638 line "new terms ... come early in a life" read rows as learning; it is withdrawn. What holds: mints are near-absent, which fits M1's starvation.
- **F1 is HELD, with good reason.** On load, a kept "?" operand "reads its slot as absent" until re-bound (gamma.py:1708-1717). So keeping the attribute alone could make carried terms LESS usable. The operand is the SOURCE of the effect, its cause. So F1 and F2 are one design: carry the source as a kind-level reference (its reading, plus its relation to the target: self, touching, same kind, a known kind), and re-bind it at first contact (F6). That is a morning design.

Plus two whole-system proofs:
- **PX1, the round trip on a real game:** play one ARC game, write, load fresh. Rows summed over the game's generations equal its new distinct keys. The next load's replayed.settle equals the evidence written, not_held is 0, and every deduped_onto_composition is listed.
- **PX2, learning across lives (Harlow's sign):** the same 5 public games over 3 lives. Presses until each action's effect is known must FALL from life 1 to 3, and lp85's first-10 dead presses must fall below 10. If they do not, the carry still fails, whatever the unit tests say.

Order: P1-P9 as failing tests first (a must-fail suite), then F1, F4, F3, F5 (small and exact), then F2, F7, F8, F9, then F6 (the behaviour change). Each fix is its own arm, default ON, OFF byte-equal, and goes on the training branch, not B2.

## Sources
- [Harlow 1949 learning sets, via Thomas 2012, Encyclopedia of the History of Psychological Theories (PDF)](https://psyc.franklin.uga.edu/sites/default/files/inline-files/Harlow.pdf)
- [McClelland, McNaughton & O'Reilly 1995, Psychological Review (PDF)](https://stanford.edu/%7Ejlmcc/papers/McCMcNaughtonOReilly95.pdf)
- [Squire 2007, Rapid Consolidation, Science (on Tse et al. 2007), PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2271071)
- docs/FIGURES_TEXT.md at 1e9d4d5 (Figs 4, 5, 6, 10, 12); tether.py, gamma.py, lineage.py, interface.py, tests/test_k1.py at 1e9d4d5 (lines cited above)
- The two audit reports (scratchpad: audit_save_load.md, audit_search_retrieval.md) and their probes (syn.py, probe_first_step.py); seat R2 (21:40)
