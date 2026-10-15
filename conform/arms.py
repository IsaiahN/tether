"""arms: eighteen capability switches, all default OFF, and nothing computed the sum.

**ENVIRONMENT SWITCHES ONLY, AND THE COUNT ABOVE IS THEREFORE NOT THE AGENT'S TOTAL --
ANNOTATED 2026-09-28.** The detector is `os.environ.get("TETHER_X")`, so a capability switch
that is a `Config` FIELD is invisible here. There is exactly ONE: `Config.accumulate`.

**IT WAS TWO UNTIL 2026-09-29, AND THE SECOND WAS REMOVED RATHER THAN COUNTED -- ISAIAH:
*remove the "System 0 off" override. System 0 is always on.*** `Config.system0` is gone from
the dataclass, so the blind spot this paragraph describes no longer has it to hide. **That is
the stronger fix: a field-arm the census cannot see is dangerous because it can be OFF, and an
arm that does not exist cannot be.**

**AND THAT IS CHECKED RATHER THAN HEDGED, because a corrected count that is itself uncounted is
how the first one got here.** Every class in the repository was scanned for `bool`-annotated
fields: FOUR have them, and only `Config`'s are configuration -- `gamma.Atom`'s
`reads_operand`/`polymorphic` are per-atom DECLARATIONS, and `instruments.Segment` and
`instruments.Termination` hold recorded READINGS. Of everything `arc_holdout.play` constructs
(`ArcWorld`, `Ledger`, `Config`, `Gamma`, `Agent`, `Budget`) only `Config` carries a bool.

**AND `system0` WAS THE ONE THAT MATTERED** -- it was found OFF on the
ARC path against a standing ruling of Isaiah's, and it is exactly the class this file's
`UNDECLARED` check exists to prevent entering silently. *A new arm cannot enter silently* is
true of env arms and false of field arms.

**KEPT IN THE PAST TENSE RATHER THAN DELETED, because an error entry whose evidence is edited
away stops being evidence.** The instance is closed by removal; **the CLASS is not** -- a future
`Config` bool would be just as invisible to this census, and `accumulate` is one today.

Widening the census to cover them is FILED, NOT DONE, deliberately: an instrument is installed
once you know what it must measure, and the System 0 rulings are open. **But the count is a
statement about the agent, a reader meets it first, and it is wrong -- so it is annotated now
rather than left standing until the census is built.**

Every arm in this codebase is `bool(os.environ.get("TETHER_X"))` -- no default value, so OFF
unless the environment says otherwise -- and **the repository sets one only by a RULING, in
code, which the census below now detects rather than narrates**. The agent
that actually runs is therefore the most starved variant of itself, in eighteen independent
respects, and that was true without anyone deciding it.

**THE FINDING IS NOT THAT THEY ARE WRONGLY OFF.** Each site carries a real reason and several
are costed: `TETHER_INSTRUMENTS` is off because a new published attribute widens the slot set
and §12.12 prices that in EPISODES FORGONE; `TETHER_SHAPE_DELTA` says *both arms belong on
together; that is a measurement, not a default*. Turning any of them on is a measurement and
a ruling, and this seat does neither.

**THE FINDING IS THAT THE REASONS LIVE AT NINETEEN SCATTERED SITES AND NO PLACE HELD THE SUM.**
That is verbatim the ground-focus seat's own origin -- *each looked reasonable alone; the drift
was visible only in the sum, and nothing computed the sum* -- one level up, about configuration
instead of commits. **Eighteen individually-justified OFFs compose into an agent nobody chose.**

    python arms.py        the census, and it FAILS on the three things below

WHAT MAKES IT FAIL, and each is a fact rather than a judgement:

    UNDECLARED   an arm is read in code and absent from the table below. **A new arm cannot
                 enter silently**, which is how eighteen accumulated
    STALE        the table names an arm no code reads any more
    HALF A PAIR  an arm is ON and a partner its own site declares is OFF. `arc_percept` says
                 of the shape deltas: *the `holes` and `perimeter` ATOMS only resolve when
                 `TETHER_SHAPE_DECODE` is on, so with arm I off the agent reads a delta of a
                 quantity it cannot itself measure.* **That coupling was written in a comment
                 and nothing enforced it**

IT DECIDES NOTHING AND FLIPS NOTHING. The table is DATA -- `conform/lint.py`'s rule, *exemptions
as data, not logic* -- so it can be read, pinned and moved by the reviewer without touching code.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).parent.parent
# the repo root, for `armflag` -- the one parser the arms read through
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# THE TABLE. One line per arm, taken from the arm's OWN SITE rather than summarised from what
# it looked like it did -- `A6i`'s writing side, which fires exactly where a row is authored.
# A pair means the two are declared at their site to belong on together.
ARMS: dict[str, str] = {
    "TETHER_ACTED_GUARD": "a term may be guarded on `ACTED_SELF` -- true when the press "
                          "LANDED ON this slot's object, resolved per slot by the caller so "
                          "no object NAME ever crosses into a term. **DEFAULT OFF, AND THE "
                          "DEFAULT IS A REFUTER THAT FIRED.** The semantics are confirmed "
                          "(60/60 against the world, `conform/landed.py`) and the "
                          "pre-registered test failed: payments up and TOTAL refusals down "
                          "on 6 of 6, refusal rate 19.67% -> 0.40% on three. Kept because "
                          "`buttons` seed 1 settled two guarded terms under a PRICED guard. "
                          "Returns ON only under Isaiah's settled/unsettled rule. **ANNOTATED "
                          "2026-10-12: the default is ON (tether.py 180, default=True) under "
                          "Isaiah 2026-10-05 (?ACTED ON by default, superseding the zero-failure "
                          "bar; CLAUDE.md standing rulings). DEFAULT OFF above is the earlier "
                          "state, kept as written.**",
    "TETHER_AIMED_CURIOSITY": "the CURIOSITY exit names a subject -- the slot with the "
                              "most unexplained surprise that it has also watched move "
                              "(Figure 5's *large and compressible*) -- instead of "
                              "exploring with none. **ON BY DEFAULT, and the flag exists "
                              "so the before/after is ONE SCRIPT WITH ONE FLAG rather "
                              "than two code states.** The `bored()` exit is NOT behind "
                              "it and never becomes aimed: that draw's uninformedness is "
                              "a safety property, not an arm. `F401`: 3 of 3 seeds on "
                              "`buttons` bind a slot where none ever bound. Spelled "
                              "`get(..., \"1\") != \"0\"`, read here as default-on",
    "TETHER_BARGAIN_FIT": "library fit priced by the bargain rather than by fit alone. "
                          "**ON BY DEFAULT SINCE 2026-09-30 -- Isaiah's ruling, and the "
                          "flip LANDED** once the four M2 failures holding it were "
                          "diagnosed. None was a capability the flip removed: one check "
                          "was vacuous, two were green only on a phantom scope and are "
                          "owed under ruling 6, and one was not isolated from the want "
                          "state. Spelled `get(..., \"1\") != \"0\"`, which this census "
                          "reads as default-on",
    "TETHER_LIBRARY_FIRST": "the library's offered chains (M4, the Figure 9 lookup) yielded before "
                            "the closure stream and priced by the one body (the reviewer 08:30Z). "
                            "ON by the registered rule (no closer lost, demo green, time "
                            "x0.93-1.06). On the panel it executed only on fake (328 yielded, 0 "
                            "won). In M2's fixture world it decides one equal-cost tie (17.184 "
                            "bits: same . all<o0.dcol>, ACOUSTIC|Brain, replaces above . "
                            "none<o0.col>). On demo and gridworld nothing reaches the mint, so the "
                            "pass there is vacuous. In M2's world slots are not independent: "
                            "o2.dcol's chain_only win depends on o1.dcol's. Spelled "
                            "`default=True`, default-on",
    "TETHER_NO_CARRY_CANDIDATE": "**INVERTED POLARITY -- the SECOND row here that is, so "
                                 "the first is no longer the only one and both say so.** A "
                                 "DEFAULT-ON write: a term the agent BINDS becomes a candidate "
                                 "awaiting the ground, so an IMPORTED term can reach `settle`. "
                                 "`candidates` had one writer (mint), so a carried term could "
                                 "never settle on any board and `gamma.refute`'s promise that a "
                                 "demoted term *can settle again if it starts paying* was "
                                 "unmeetable for imports. IMPORTED ONLY: unscoped it also moved "
                                 "local terms' birth cycles and took M2 to 27/30. Spelled `NO_` "
                                 "so the inversion is in the NAME. The OFF arm is the non-zero "
                                 "control the null needs",
    "TETHER_CELL_CHANGE": "WHERE a matched object's cells changed -- added/removed counts and "
                          "centroids, read only where identity is sure. OFF until measured: it "
                          "adds six slots per object and six atoms, so it prices every term "
                          "(F492)",
    "TETHER_DELTA_KEY": "route (b) re-keyed on this frame's delta",
    "TETHER_LOOKUP_ORDER": "the residual's library look-up orders the mint's operand candidates "
                           "(after contact, before variance; never excludes). ON: the reviewer "
                           "2026-10-08 00:54Z; 0 is the one-flag A/B control",
    "TETHER_OBJECTIVE_DOMAIN": "an objective is searched over the values the record has shown "
                               "and its operands' boundaries, not the declared alphabet, which "
                               "only prices. ON: the reviewer 2026-10-08 09:55Z (cd82, 2,112 s "
                               "in one cycle); 0 is the one-flag control",
    "TETHER_NOT_ATOM": "not-t priced as one atom slot instead of the bits to name which "
                       "predicting term is wrong (the default, reviewer 2026-10-07). The figures "
                       "leave the price OPEN; this arm keeps the alternative readable (F496)",
    "TETHER_DELTA_OPERANDS": "deltas offered as operands",
    "TETHER_GUARD_AXIS": "the guard axis in the reject key",
    "TETHER_INSTRUMENTS": "the embedded instrument set -- Part 12 item 3, PAID BILLS from "
                          "frame 0. Off at a COSTED price: a new attribute widens the slot "
                          "set and §12.12 prices that in EPISODES FORGONE",
    "TETHER_HOLD": "THE RANDOMISED HOLD -- MEASUREMENT ONLY, the reviewer 2026-10-03 "
                   "ruling 3. Withholds the ACTED_SELF offer on a seeded ~half of "
                   "ELIGIBLE (cycle, slot) occasions so a measurement run carries its "
                   "own within-run control. OFF in the shipping agent: a control that "
                   "changes what the agent is OFFERED is an instrument, and leaving it "
                   "on would make every later reading a reading of the instrument",
    "TETHER_HOLD_SEED": "the hold's seed, so the withheld pattern is REPRODUCIBLE and "
                        "a row can be replayed. An unseeded flip makes the treatment "
                        "unrecoverable, and a row whose treatment cannot be "
                        "reconstructed cannot be checked",
    "TETHER_ITERATE": "the fold constructs -- `cells`/`cell_row`/`cell_col`/`count_true`. "
                      "§12.0 rules the MEANS to iterate is INHERITANCE where a solved case "
                      "would be an answer, and the agent could hold a cell set and not walk it. "
                      "**RULED ON by Isaiah 2026-09-24 and set in `arc_holdout.play` for the "
                      "ARC path, so the env census below reads OFF while the capability is "
                      "LIVE.** A ruling turned it on, not a measurement -- the house rule is "
                      "his to override. The toy world is untouched: it has its own atoms",
    "TETHER_NO_RESUME": "**INVERTED POLARITY, the THIRD such row.** A DEFAULT-ON frontier in "
                        "`_mint`: under an unchanged scope key a chain already priced is not "
                        "priced again, and a search that stopped at the budget resumes past "
                        "what it refused (plan item 7, F485). A BEHAVIOUR change, not only an "
                        "optimisation: on gridworld it adds binds. The variable turns it OFF, "
                        "so the A/B is one script with one flag. Inert on the ARC path while "
                        "the shape-decode arm puts the cycle in the key",
    "TETHER_NO_TALLY": "**INVERTED POLARITY. THIS SAID *THE ONLY ROW HERE THAT IS* AND IT "
                       "STOPPED BEING TRUE ON 2026-09-30**, when `TETHER_NO_CARRY_CANDIDATE` "
                       "was added -- correct when written and falsified by a later build, "
                       "which is the class this table cannot catch by passing. Every OTHER arm "
                       "is OFF and its variable turns it ON; this names a DEFAULT-ON incremental "
                       "tally in `_cannot_pay` and the variable turns it OFF. Spelled `NO_` so the "
                       "inversion is in the NAME and not only in this row. It exists for the "
                       "identity A/B -- one script, one flag -- because an exact optimisation has "
                       "to be provable against its own absence, and a default-off one is an "
                       "optimisation nobody runs",
    "TETHER_OBSERVER": "the corpus's cheap mutation set carried PER OBJECT, not counted",
    "TETHER_PREV_OFFER": "a term reading a slot's value one frame earlier (slot~1) offered "
                         "into a mint, at three sites: _bindings' slot~1 offer, compiled ~1 "
                         "views, and CAUSE then-sides (the reviewer 07:14Z, 07:23Z). OFF: under "
                         "A3 a ~1 term cannot close, and its binding seals the slot against later "
                         "closers (demo swing: dec . neg never reached after c3; trace "
                         "2026-10-09). 16 of 18 ~1 terms settled held-out on the panel when ON. "
                         "Re-ON pending the ruling on pricing a law that needs an earlier frame",
    "TETHER_UNSEAL_START": "the seal repair (R3 item 1; Isaiah's H1 and H3(i)): when the HELD "
                           "term reads an earlier frame, a challenger is priced against the held "
                           "rule's whole two-part length (its cost plus its leftover, whose unseen "
                           "starts are its own price), not its leftover alone, which can sit under "
                           "the floor and seal the slot; a challenger leaving more than the held "
                           "rule is refused (unseal_leaves_more). Opens the seal; does not by "
                           "itself rebind on one record (swing: ~1 rule 10.422 vs any 2-atom "
                           "closer >= 11.422); the rebind is item 3's (the reviewer 16:46Z). Inert "
                           "while TETHER_PREV_OFFER is OFF unless the window binds a lagged term. "
                           "ON BY DEFAULT since the 7.5 switch-on (the reviewer 2026-10-11 "
                           "02:19Z), a SUBSET OF THE MEASURED ON CONFIGURATION (the ON panel ran "
                           "16 arms together; this subset was not measured alone); 0 is the "
                           "one-flag control. Spelled `default=True`, default-on",
    "TETHER_CARRY_PRICE": "carry credit (R3 item 3; DISCOVERY 503; H3(ii); R-D4; the reviewer "
                          "16:31Z, 21:18Z, 21:37Z): a MINTED term paid its cost at its own entry, "
                          "so where it RE-GROUNDS (pays on a slot's own record alone, left < base, "
                          "and bears on its open residual) its DEFINITION is not charged again but "
                          "NAMING it is: price log2(H+1) + left, H the held terms (21:55Z, the "
                          "corpus's +log2(k+1)). Any reuse, within a level or across one (Fig 12: "
                          "nothing re-earned inside a run); any slot name (Q2 (ii)), never pooled. "
                          "_library_fit takes the lowest WHOLE price "
                          "among payers, ties in fit order (Q1 (a): library first); sweep credits "
                          "the swept term and opens under_floor records to a credited term only; a "
                          "pre-boundary close is marked STALE (MF-D3; its promotion is held by "
                          "P2 in every arm). 3(b) as counts: each credited binding's settles and "
                          "demotes. GATE (the reviewer 22:54Z, 03:03Z): may not go ON until 3(b) "
                          "resolves -- "
                          "every credited binding refuted or settled more than once, on ONE "
                          "longer run shared with 2c; the one-settle bar is the same question at "
                          "P2's _promote and gamma.units() :1379. CONTROL (batch 1, 60 cycles): "
                          "(1) held on one settle and outnumbered by misses is in EVERY binding "
                          "kind in both arms (batches 1 and 2), so not carry's; (2) credit raises "
                          "the demote rate over the uncredited pull it replaces on 5 of 6 "
                          "gridworld members (s0 81% vs 31%; arc_s1 25 vs 29 the exception), and "
                          "on 4 of 6 with PREV_OFFER+UNSEAL (batch 2: s0 76 vs 33; s1 and arc_s1 "
                          "the exceptions, their credited bindings held on one settle outnumbered "
                          "by misses): recorded as 3(b) evidence that log2(H+1) is too cheap, "
                          "not ruled",
    "TETHER_TWO_READINGS": "7a(7)+(9) plan readings (R3(a); the reviewer 2026-10-10 22:30Z, "
                           "22:33Z, 22:47Z): ON, at plan adoption a plan reads bits and "
                           "confirm-actions, never their sum; MC4's reader drops a plan that "
                           "cannot finish inside a reserve learned by running out; the dominated "
                           "are dropped and the existing order picks on the frontier; factor 8 "
                           "(waiting) is read from Agency.order. On the test worlds paying plans "
                           "mostly tie in both readings (a correctness rule: never a sum). "
                           "ON BY DEFAULT since the 7.5 switch-on (the reviewer 2026-10-11 "
                           "02:19Z), a SUBSET OF THE MEASURED ON CONFIGURATION (the ON panel ran "
                           "16 arms together; this subset was not measured alone); 0 is the "
                           "one-flag control. Spelled `default=True`, default-on",
    "TETHER_D13": "7a(10) D1-D3, the same loop one level up (R3 part 2; the reviewer "
                  "2026-10-10 23:50Z): ON, the agent's process states bet on GROUND outcomes "
                  "and each settles only at a level or game ending, from the ending word or "
                  "the world's grade of the slot's last CHANGE after the park, never from the "
                  "agent's own diagnosis. ON BY DEFAULT with objective build step 1 (the "
                  "reviewer 2026-10-11 02:19Z), its consumer; record only. Spelled "
                  "`default=True`, default-on",
    "TETHER_REALISE_CELL": "the cell tier (the reviewer 2026-10-11 09:53Z): ON, a direction intent "
                           "reads each action's effect from the CELL the slot is in -- the sign of "
                           "after - before in its singleton `lands` entry keyed (ctx, slot, "
                           "before), this ctx then any ctx (non-relational) -- before today's "
                           "mean-delta tiers, so a wrap seen at an edge cannot set the direction "
                           "from column 2 "
                           "(run C, c98). expected_move keeps today's reading (cell=False). OFF: a "
                           "default-path reader, it needs its own panel reading",
    "TETHER_RELATION_SET": "the comparison set (the reviewer 2026-10-11 14:19Z-14:28Z, plan "
                           "accepted 14:33Z; Isaiah 09:15-09:26 CDT): ON, B1 -- arc_atoms "
                           "builds `below`, the own-slot converse of `above`, and "
                           "compile_term's '<' against a slot keeps the left party the "
                           "subject. B2 -- gridworld publishes every ordered pair's relations as "
                           "slots `{a}.{rel}_{b}` (dist, drow, dcol, inside, touches; "
                           "relations.pair_slots). B2b -- a pair slot is a derived reading: "
                           "not bet on, predicted from the predicted sources, searched only on "
                           "a relational surprise; mint walks derived binds in a last round "
                           "(round 3). ARC B2 -- arc_world publishes the same slots over the "
                           "contact pairs plus the pairs of the agent's actor set "
                           "(relate(), its Agency.contingent owners, one step behind). "
                           "Later items join this arm. OFF until "
                           "ALL-ON; build "
                           "checks only (Isaiah 09:15)",
    "TETHER_ROUTINE_SUBJECT_BUDGET": "R-dir (c) (the reviewer 2026-10-11 10:39Z, 10:53Z): ON, a "
                                     "routine whose body is one BECOME intent takes its budget "
                                     "AND the count it claims (_expected) from that subject's "
                                     "own gap -- |target - now| signed, 1 on a value want -- "
                                     "not the group unsat; unreadable target keeps the group "
                                     "count. OFF: a default-path reader, joins the objective "
                                     "arms for a switch-on reading",
    "TETHER_ROUTINE_STALE": "R-dir (ii) (the reviewer 2026-10-11 10:39Z): ON, a held routine "
                            "whose step is a signed BECOME ends `stale` before pressing when the "
                            "live _goal_target reads the OPPOSITE sign to the minted one; an "
                            "unreadable or held comparison keeps today's path (A1). A non-trial: "
                            "no verdict, no refusal, not shelved. OFF: a default-path reader, "
                            "joins the objective arms for a switch-on reading",
    "TETHER_WANT_TARGET_SUBJECT": "F2's fallback (the reviewer 2026-10-11 07:20Z, option (i)): ON, "
                                  "_goal_target and _term_of read a retained want ONLY where "
                                  "_want_scope names it (a goal-condition want); every own want "
                                  "keeps the masked lookup. With TETHER_WANT_TARGET also ON, the "
                                  "full unmask subsumes it. 7.5: OFF PENDING READING (B); "
                                  "habitat arc_s1 at 120; reader the goal exit; gate (B)",
    "TETHER_WANT_TARGET": "F2, one lookup for a slot's objective (the reviewer 2026-10-11 "
                          "05:38Z): ON, _goal_target and _term_of read _objective_of -- the bound "
                          "term if it is an objective, else the retained want -- the order "
                          "goal_residual already used, so a want masked by a bound predictor "
                          "yields its target. OFF until the live arc_s1 reading (step 8) "
                          "'step 8' above was a slip, corrected 06:01Z. A DEFAULT-"
                          "PATH change: the 42 masked refusals were the agent's own wants. 7.5: "
                          "OFF PENDING READING (A); habitat: the 7-member panel at 60; reader: "
                          "_goal_target and the goal exit; gate: (A) read and ruled",
    "TETHER_GOAL_PAIR": "objective build 2a, the goal pair (the reviewer 2026-10-11 05:14Z): ON, "
                        "a held goal condition may be the AND of two different conditions, "
                        "priced once as one term (both parts plus the `both` joiner); a pair is "
                        "formed only from conditions true on every step the objective held (a "
                        "search bound, recorded as one); L1's recheck and E1's close apply "
                        "unchanged; a held pair is not linked (item (b)). Needs "
                        "TETHER_GOAL_CONDITION ON. OFF until (b) and its reading "
                        "(b) LANDED at 11adca0: a held pair links as one subject-scoped want per "
                        "conjunct, so the 'not linked' above is superseded. 7.5: OFF PENDING "
                        "READING (B); habitat: arc_s1 at 120; reader: TETHER_GOAL_LINK; gate: (B)"
                        " read and ruled",
    "TETHER_GOAL_LINK": "objective build 3, the link to composition (the reviewer 2026-10-11 "
                        "02:19Z, 03:14Z): ON, a held goal condition is closed into the "
                        "objective stream with `all` and becomes its slot's want, so "
                        "_goal_choice and _mint_routine can pick it; linked only where the slot "
                        "holds no want (one want per slot; replacing one is not this item's). "
                        "Needs TETHER_GOAL_CONDITION ON. OFF until the objective panel "
                        "7.5: OFF PENDING READING (B); habitat: arc_s1 at 120; reader: "
                        "_goal_choice and _goal_target (steers only with TETHER_WANT_TARGET); "
                        "gate: (B) read and ruled",
    "TETHER_GOAL_CONDITION": "objective build 2, the goal condition (the reviewer 2026-10-11 "
                             "02:19Z): ON, at each completion the library's condition templates "
                             "over the readings are priced against WHEN the world's objective "
                             "held (positions named at log2 N bits: no term names each reached "
                             "step, Q names each step it gets wrong), and the cheapest that pays "
                             "is held in-episode in the private library copy; the flag is the "
                             "then-side, never the subject; nothing about the target is "
                             "published. Needs TETHER_COMPLETION_SWEEP ON. OFF until the "
                             "objective build's panel "
                             "7.5: OFF PENDING READING (B); habitat: arc_s1 at 120 (a pair pays "
                             "at c89, no single condition does); reader: TETHER_GOAL_LINK; gate: "
                             "(B) read and ruled",
    "TETHER_COMPLETION_SWEEP": "objective build 1, the completion sweep (ARC_AGENT 21.3; the "
                               "reviewer 2026-10-11 02:19Z): ON, when the WORLD's objective "
                               "degree reaches 1.0 ('reached', not 'banked'), the segment since "
                               "the last completion is re-examined and recorded: what was "
                               "live, which terms settled, which owed slots closed. Record "
                               "only; nothing retargeted, dropped or cleared. OFF until the "
                               "objective build's panel "
                               "7.5: OFF PENDING READING (B); habitat: a world whose objective "
                               "completes (arc_s1, 6 in 120); reader: TETHER_GOAL_CONDITION; "
                               "gate: (B) read and ruled",
    "TETHER_MC6": "7a(10) MC6 muse (R3 part 2; the reviewer 2026-10-10 23:50Z): ON, on a step "
                  "that owes nothing (owed_import empty, under_floor included, and this "
                  "step's bets paying), the settled methods are re-tested as chains on an "
                  "earlier level's parked residuals, priced as the sweep prices them, and a "
                  "MUSE row records what would pay and the compute spent; nothing is "
                  "installed and no action is taken. OFF until 7-and-a-half: a reading with "
                  "no consumer yet (D1-D3 are named to read it)",
    "TETHER_M6_INVENT": "7c M6 invent (ISAIAH_RULINGS 'Mint, invent, import'; the reviewer "
                        "2026-10-10 23:14Z): ON, at a budget_spent or priced_out_at_depth park "
                        "where the change recurred and nothing lit, the agent names a condition "
                        "over the readings that held where the slot changed (f when Q, identity "
                        "otherwise), prices it at its whole length by the one bargain, and holds "
                        "it in a private in-memory library copy only if it pays; carry is M7 and "
                        "gated. ON BY DEFAULT (the reviewer 2026-10-11 02:55Z), a SUBSET OF THE "
                        "MEASURED ON CONFIGURATION; its 0.113-bit margins are the uniform "
                        "code's quantum (5 x log2 11 - term_bits 2), verified; wall cost bounded "
                        "(+56 of +225 s on arc_s1, noise on arc_s0); 0 is the one-flag control. "
                        "Spelled `default=True`, default-on",
    "TETHER_MC34": "7a(8) MC3/MC4 (R3 part 2; the reviewer 2026-10-10 22:33Z): ON, every ending "
                   "is appended to the ground's record (word, kind, cleared, actions this "
                   "level and run, attempts, and the scope it ran out: level if a new level "
                   "followed, run if the run ended), and a plan's adoption row reads its need "
                   "against reserve_level_seen and reserve_run_seen (the agent's own cap "
                   "endings at that scope, minus this level's or this run's actions; the "
                   "reviewer 23:18Z) and level_cost_seen (what cleared levels cost), kept "
                   "apart; a world's cap is "
                   "never read. OFF because it is a reading with no decision consumer yet: "
                   "item 9's per-plan factors are named to read it",
    "TETHER_CASCADE_AGENCY": "7a(6) H2, the in-between frames (R3 part 2; the reviewer "
                             "2026-10-10 22:14Z): ON, the order objects change in inside one "
                             "action gives each non-controlled object a mode (self-moved, "
                             "moving with the controlled one, reacting) in Agency. OFF and "
                             "HELD because no test world has a cascade: only arc_world "
                             "publishes one, and ARC is closed until step 13; proven on a "
                             "hand-built cascade fixture",
    "TETHER_GUARD_PRICE": "F408, every named guard priced (Fig 12 :99-102; the reviewer "
                          "2026-10-10 21:31Z): ON, an intent guard and 'no intent' cost "
                          "log2(G+1) over the G on offer, like ACTED_* (whose referent term "
                          "stays); no guard is the free +1 slot. A correctness rule: it reprices "
                          "the mint's bargain so every named guard pays for the choice. "
                          "ON BY DEFAULT since the 7.5 switch-on (the reviewer 2026-10-11 "
                          "02:19Z), a SUBSET OF THE MEASURED ON CONFIGURATION (the ON panel ran "
                          "16 arms together; this subset was not measured alone); 0 is the "
                          "one-flag control. Spelled `default=True`, default-on",
    "TETHER_D5": "7a D5, split a slot's residual on strain (Fig 9 :4-5; the reviewer 2026-10-10 "
                 "15:58Z, 16:24Z): ON, when a held predicate (an intent kind, or ACTED_SELF) "
                 "cleanly separates the rows a term got right from the rows it got wrong, among "
                 "every row it predicted the slot in this level (2 a side, and it pays), the "
                 "slot gets two parts: the incumbent guarded by P, and the not-P rows searched "
                 "by the same mint on their own rows; credit per (term, part); the incumbent is "
                 "shadow-graded on not-P steps and a broken partition reverts. OFF because it "
                 "is new and changes binding; on fake it does not fire (no held predicate "
                 "separates o2.drow: the true cut is the button). A found cut is a CANDIDATE "
                 "until a witness row confirms or refutes it, on either side of P. "
                 "HELD until the candidate-cut "
                 "amendment (one witness before acting) lands and is read (the reviewer 18:46Z; "
                 "F408 cannot bind at a 2-a-side cut, so it was the wrong unblocker)",
    "TETHER_CONTACT": "7a(5b), the contact instrument (Isaiah 2026-10-10 06:46 CDT; the reviewer "
                      "11:46Z, 12:27Z): ON, the REPEAT row's gamma_read gains fed, one entry per "
                      "library term read by the exit whose action is RETURNED, {kind, name, slot, "
                      "seq, role: goal|route|body}, and MC2's resolution fed becomes [REPEAT seq, "
                      "role] after the bet. Record only; read by conform/contact.py per member, by "
                      "exit and role, never pooled. OFF because it is new and nothing reads the "
                      "field yet; the per-step gamma_read reset beside it is NOT under this arm",
    "TETHER_RUIN": "7a(5) C, ruin ordered first (R3 Part 1; the reviewer 2026-10-10 10:41Z, "
                   "11:53Z): ON, a pair the veto floor holds for THIS board is withheld from "
                   "the one choose() call at the sites below the seam (offered, TOUCH route 1, "
                   "_made's spots, the bare routine step), unless every option is vetoed; one "
                   "PLAN '@ruin' 'withheld' row per step. REQUIRES TETHER_RUIN_RECORD (import "
                   "refuses without it). OFF because it is behaviour and new: the panel never "
                   "dies, so its only evidence is the dying-world fixture until step 13",
    "TETHER_RUIN_RECORD": "7a(5) A + B (ARC_AGENT 19.3-19.4; the reviewer 2026-10-10 10:41Z): "
                          "ON, every ending reaches instruments.Termination exactly once "
                          "(retarget, or end_run unless retarget counted the same word; "
                          "cap/time/run_end map to cap) with an IMPORT 'termination' row "
                          "when its class "
                          "changes, and a death adds (fingerprint, action, realised coordinate) "
                          "to a veto set that only grows, one IMPORT 'veto' row each; the "
                          "fingerprint is the world's board() where it gives one, else "
                          "observe(). OFF because it is record only and new: nothing reads the "
                          "vetoes until C (TETHER_RUIN, its own arm, which will require this "
                          "one), and the panel has no deaths",
    "TETHER_MC_SIGNAL": "MC1 + MC2 (R3 item 4, 7a(4); the reviewer 2026-10-10 07:57Z): the signal "
                        "is the TRANSITION bet row the ground answered (ledger.signal_sign: paid "
                        "iff not vanished and mass 0); ON, each gets exactly one SETTLE "
                        "'resolution' row (signal_seq, kind level|game, how, fed) when its level "
                        "ends at retarget or the run ends with it open (end_run). fed is None: no "
                        "row names the term an action was chosen through. OFF because it is "
                        "record only and new: nothing reads the rows, and its level half has never "
                        "fired on a real level end (first real reading at step 13)",
    "TETHER_WINDOW": "the history window (R3 item 2; Isaiah's H1; the reviewer 14:52Z, 15:26Z, "
                     "18:10Z, 18:15Z): every lag slot~j the trace can reach is offered AFTER "
                     "every other binding (their order and position unchanged), evidence lags "
                     "first, nearest first, then the rest nearest first; the per-mint work "
                     "budget is also checked inside a chain, so the cut falls between lags and "
                     "unreached ones are counted by kind (window_beyond_bound). Evidence: on the "
                     "residual frames the outcome is a function of the value j frames back AND "
                     "some earlier value recurs. Price untouched (R-D1). Note: ~j reads j "
                     "frames before the BEFORE-state, so j+1 before the outcome. DEPENDENCY: a "
                     "lag-j law leaves j unseen starts; measure and run with TETHER_UNSEAL_START "
                     "ON, or the seal returns on every lag (the reviewer 18:25Z). MEASURED, 7 "
                     "members, 60 cycles: chains seen fall -1% to -30% (fake -67%); 5 slots that "
                     "paid OFF never pay ON (6 with TETHER_UNSEAL_START), slots paid rise on 5 of "
                     "7 members; seal count 0 (no lag law bound here is otherwise exact); 0 "
                     "closers and 0 level ends in any arm, so no capability claim. Crowding "
                     "traced (19:34Z): 5 of 6 lost slots never reached their OFF winner; item 2b "
                     "orders the search in two passes (evidence lags first), and when "
                     "TETHER_RUIN lands, stakes-tagged lags join pass 1 by the same R-D3 rule "
                     "(the reviewer 19:45Z; nothing built for it yet). Item 2b: two ROUNDS over "
                     "every stream, round 2 walking the chains round 1 recorded with only their "
                     "no-evidence lags. _TWO_PASS: test-only, restores item 2's one-pass order "
                     "for the tie guard; defaults to two-pass, read from no environment or CLI "
                     "(the reviewer 20:25Z). 2b's REACH TRADE: chains back at the OFF level (at "
                     "worst -4%) and the 3 clean crowding slots return, but no-evidence lags go "
                     "mostly unreached (beyond-bound no-evidence 3306-16452 per member, from "
                     "0-7497 one-pass) and slots paid fall on 5 of 7 members; trade "
                     "PARKED as item 2c (reviewer 21:18Z). GATE: may not go ON, "
                     "and item 5's stakes may not depend on the window's "
                     "order, until 2c is measured and ruled. OFF until "
                     "measured; under it ~1 is one lag of the block, not TETHER_PREV_OFFER's offer",
    "TETHER_REBIND_HELD": "rebinding a slot whose term is already held",
    "TETHER_RECIPE_DEDUP": "one candidate per recipe rather than per instance",
    "TETHER_DIRECTION_MOVABLE": "B (the reviewer 2026-10-12 05:43, 05:47 CDT): a slot is movable "
                                "when, in one context (its object's signed offset from the "
                                "controlled owners, from the agent's own pair slots), two "
                                "actions change it with different PURE signs; mixed cells "
                                "abstain. Adds movables only. Needs TETHER_RELATION_SET for "
                                "the pair slots. OFF until its s0 probe and OFF identity are "
                                "accepted",
    "TETHER_STREAM_SHARE": "D2 (the reviewer 2026-10-12 05:43, 06:19 CDT): within a round of "
                           "mint's search the stream that has spent the least rank takes the next "
                           "candidate (ties to list order), and a stream stops at its OWN kind's "
                           "floor. No share or quota; the shared cap is unchanged. Records "
                           "stream_share on the MINT row. OFF until R1 and OFF identity are "
                           "accepted",
    "TETHER_PARK_WANT": "The park return (the reviewer 2026-10-12 08:43, 08:52 CDT): when nothing"
                        " in a mint paid, the mint returned before its tail and the unpaid "
                        "objective want it ranked by recurrence (Isaiah 2026-09-25) was never "
                        "written. Under the arm the park branch writes it through the tail's own "
                        "writer, for budget_spent, not_novel and priced_out_at_depth, before the "
                        "park row, which also carries bound_at_park. Chains only. OFF until "
                        "R-exec, R-lever and OFF identity are accepted",
    "TETHER_DEST_GAP": "Stage 1a (the reviewer 2026-10-12 12:41, 13:04 CDT): nothing recorded "
                       "where a press LEADS, so the chooser's own Fig 5 line ('a gap "
                       "elsewhere') could not be read and least-seen alternated between "
                       "mapped contexts. Under the arm "
                       "audit keeps the post-press context beside the pre-press key, and among "
                       "equal-price reaching options ELICIT prefers one seen to lead where an "
                       "offered action's effect is unknown (one step). OFF until fixture, OFF "
                       "identity and R-exec are accepted; ground on the 25 in step 13",
    "TETHER_AIM_GAP": "Stage 1b (the reviewer 2026-10-12 15:26 CDT): an explore press at a click "
                      "site went to a coordinate already known to move its subject (_aim_for) "
                      "ahead of an object never pressed. Under the arm audit keeps each press's "
                      "effect per (coordinate, pre-press context), and ELICIT aims first at an "
                      "object not yet pressed in this context; BECOME keeps the known knob. OFF "
                      "until fixture, OFF identity and R-exec are accepted; ground on the 25 in "
                      "step 13",
    "TETHER_NO_REFUTED_BIN": "**INVERTED POLARITY.** The fifth bin (Fig 5's amendment), DEFAULT ON "
                             "since F497: a refuted slot is offered a same-type competitor and "
                             "not-t is priced there (F496). The variable turns it OFF, so the A/B "
                             "is one script with one flag. Off on the shipped path it was the "
                             "switch-never-set genus (the reviewer, 2026-10-07)",
    "TETHER_REL_GAP": "the relational gap reading",
    "TETHER_SHAPE_DECODE": "arm I -- `_as_shape`, the decoder eight SHAPE atoms need",
    "TETHER_SHAPE_DELTA": "`dholes`/`dperimeter` across frames. PERCEPTION: no atom accepts "
                          "OBJECT_BEFORE, so the agent cannot compose a cross-frame delta",
    "TETHER_STARVED_CONTACT": "the starved-contact reading",
    "TETHER_STREAM_WIDEN": "the widened candidate streams",
    "TETHER_TYPED_BIND": "binding filtered by type",
    "TETHER_VIEW_HOLD": "7e the view hold (Fig 12 :107-108; the reviewer 2026-10-14 00:49, "
                        "00:57): ON, an entry's STATE/TEST/PROCESS/CAUSE view is derived once "
                        "per run under the library's placeholders and the names are put back "
                        "as text, a lookup in place of a re-derivation (R-c 0.839 on su15 and "
                        "sp80, CAUSE control 0); RELATION/MEASURE, o == x and braced names take "
                        "the named call. A cost change only. OFF: R7e-0/1/2/3 not refuted "
                        "(the record identical OFF and ON on gridworld s0/s1@20, su15 and sp80 "
                        "a1-3; su15 a2 333.5 -> 109.6 s, sp80 a3 100.5 -> 37.7 s); R7e-4 refuted "
                        "as registered (the peak rise exceeded the hold's deep size by 0.3-2.3%). "
                        "ON BY DEFAULT, Isaiah 2026-10-14 06:07 (via the reviewer 06:08): 'the "
                        "library never resets. its always storing'; the memory cost is accepted "
                        "(measured 9-35 MiB, bound about 112 MiB); 0 is the one-flag control. "
                        "Spelled `default=True`, default-on",
    "TETHER_INDEX_HOLD": "(b'-q) the index hold (Fig 12 :107-108; the reviewer 2026-10-14 12:19, "
                         "12:23): ON, a held role's view (STATE/TEST/PROCESS/CAUSE) is compiled "
                         "ONCE per process under the placeholders PHo/PHx and kept, keyed by "
                         "compile_term.signature (the template atoms and their types, and the "
                         "arm); a question binds its names to it, re-sorts a bbox pair and "
                         "rebuilds each Term from its own Gamma's atoms. Non-held roles, o == x "
                         "and names that are not plain ids compile the named text as before. A "
                         "cost change only. OFF until its panel (R'-0, R'-1, R'-2 registered "
                         "2026-10-14 11:46 and 12:17)",
    "TETHER_LINEAGE_HOLD": "(b'-l) phase 1, the lineage hold (Fig 6, Fig 12, Fig 4; the reviewer "
                           "2026-10-14 16:29, 16:34, 16:38, 17:02): ON, every store retarget "
                           "clears, the trace included, is kept dormant in instance form with a "
                           "count row per store, and one attempt row per attempt (the ending's "
                           "sign, the actions and gap kinds THIS attempt tried; never a verdict); "
                           "a same-level restart carries reach_tested, wants, undone and "
                           "Drive.tried back per object where identity is sure, restarted's "
                           "refutation carry names both objects of a pair owner (o12~o3), and "
                           "play() calls restarted() as tether_agent.run does. Nothing dormant "
                           "is consulted by slot name. OFF until its panel (RL-0..RL-6, RL-2b, "
                           "registered 2026-10-14 16:29; RL-5 restated 17:02)",
    "TETHER_LINEAGE_CARRY": "(b'-g) the lineage carry (Fig 12, Fig 10, Fig 4, Fig 6; the reviewer "
                            "2026-10-14 20:18, 20:22): ON, with a lineage folder given, every game "
                            "and run boundary writes a generation holding only what changed since "
                            "its parent (term rows, status, settle/refute evidence, the dormant "
                            "record), and the next instance loads the chain folded; no deletion, "
                            "never overwritten, one tip or it raises. Evidence and the dormant "
                            "record are the record only, never read back. OFF until Isaiah's word "
                            "after R-g1..R-g3 (registered 2026-10-14 20:18) and the OFF identity",
}

# DECLARED AT THE SITE, NOT INVENTED HERE. `arc_percept`'s shape-delta comment: *pairs with arm
# I rather than standing alone ... both arms belong on together; that is a measurement, not a
# default.* The comment could not fire; this can.
PAIRS: tuple[tuple[str, str], ...] = (
    ("TETHER_SHAPE_DELTA", "TETHER_SHAPE_DECODE"),
)

# BOTH QUOTE STYLES, AND THE SEAT IS WHY. This matched double quotes only, so an arm written
# with single quotes would enter SILENTLY -- past the one check whose entire purpose is that a
# new arm cannot. The codebase is double-quoted throughout and `ruff format` keeps it that way,
# **which is exactly the reasoning that makes a detector brittle**: it is true of the code today
# and is not a property anything enforces. A guard resting on a convention it does not check is
# the arms' own shape one level up -- reasonable, and nothing computes it.
# AND THE ONE PARSER (2026-10-08): every arm now reads through `armflag.arm`, so the census
# reads that form as well as the raw one -- a raw read is still found, and still refused below.
_READ = re.compile(
    r'''(?:os\.environ\.get|armflag\.arm)\(\s*["'](TETHER_[A-Z0-9_]+)["']''')

# A RULING TURNS AN ARM ON BY ASSIGNING ITS MODULE FLAG, AND NOTHING SAW THAT. `_ITERATE` was
# set in `arc_holdout.play` on 2026-09-24 and this seat kept reporting `0 ON`, with the fact
# carried in a PRINTED SENTENCE naming that one arm -- so the second ruling (2026-09-27, the
# shape pair) made the sentence false the moment it landed. **Detected now instead of narrated,
# because a hardcoded name is stale by success the next time someone rules.**
#
# AND IT IS THE `HALF A PAIR` RULE THAT ACTUALLY NEEDED IT: that check reads `on`, `on` read the
# ENVIRONMENT, and the pair it exists for is set IN CODE -- so it could not fire on the one case
# it was written for, and setting just one of the two would have left the seat GREEN.
_RULED = re.compile(r'''^\s*[A-Za-z_][\w.]*\._([A-Z0-9_]+)\s*=\s*True\s*(?:#.*)?$''', re.M)


# **THE CENSUS WAS BLIND TO A DEFAULT-ON ARM AND THAT IS WHY THE NAMES HAD TO CARRY IT.**
# `on` is built from the ENVIRONMENT plus `_RULED`, so an arm whose DECLARATION defaults to
# true is reported OFF while the agent runs with it ON -- the one state a census must never
# get wrong. The project's answer had been spelling: `TETHER_NO_TALLY` and
# `TETHER_NO_CARRY_CANDIDATE` put the inversion in the NAME so a READER could see what the
# SEAT could not. **That is a convention holding up a blind spot**, and when Isaiah ruled
# `TETHER_BARGAIN_FIT` on by default there was no honest way to spell it -- the ruling names
# that arm, not its negation. So the seat learns to see the form instead.
#
# Two spellings, both already in the tree: `not os.environ.get("X")` and
# `os.environ.get("X", "1") != "0"`.
_DEFAULT_ON = re.compile(
    r'^\s*_[A-Z0-9_]+\s*=\s*(?:not\s+os\.environ\.get\(|os\.environ\.get\()')
_FALSY_DEFAULT = re.compile(r'''os\.environ\.get\(\s*["']TETHER_[A-Z0-9_]+["']\s*\)\s*$''')


def defaults_on() -> dict[str, str]:
    """`{arm: "file:line"}` for arms whose DECLARATION is true with nothing exported.

    Keyed on the ARM NAME IN THE LINE, not on the module variable, because the inverted
    spellings deliberately differ (`_TALLY` <- `TETHER_NO_TALLY`). Read from the code like
    every other census here: the table is the CLAIM and this is the WORLD.

    **DECIDED BY EVALUATING THE LINE, NOT BY PATTERN-MATCHING ITS SHAPE.** A regex over
    spellings would go stale the next time someone writes a third one, and the question --
    *is this true with an empty environment* -- has an exact answer.
    """
    out: dict[str, str] = {}
    for path in _tracked():
        if path.name == "arms.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for i, line in enumerate(text.split("\n"), 1):
            arms = _READ.findall(line)
            if not arms or "=" not in line:
                continue
            expr = line.split("=", 1)[1].strip()
            try:
                # NO ENVIRONMENT AT ALL, so the reading is of the DECLARATION and not of the
                # shell this seat happens to run in.
                val = eval(expr, {"os": type("o", (), {"environ": {}})(),  # noqa: S307
                                  "armflag": _NO_ENV})
            except Exception:
                continue
            if val:
                for arm in arms:
                    out[arm] = f"{path.relative_to(ROOT).as_posix()}:{i}"
    return out


_NO_ENV = type("armflag", (), {"arm": staticmethod(lambda _name, default=False: default)})

# VALUES, NOT SWITCHES: read raw because they are not on/off. Data, so a new one is a visible
# edit here rather than a quiet exemption in logic.
VALUES = {"TETHER_HOLD_SEED": "the hold-out seed, an integer"}
_RAW = re.compile(r'''os\.environ(?:\.get\(\s*|\[\s*)["'](TETHER_[A-Z0-9_]+)["']''')


def bypasses(texts: dict[str, str]) -> list[str]:
    """An arm read that does not go through the one parser -- the way the "0"-is-ON defect
    would return through a nineteenth arm (the reviewer 2026-10-08 18:39Z). Assignments to
    os.environ are writes and are not reads."""
    bad = []
    for name, text in texts.items():
        for i, line in enumerate(text.split("\n"), 1):
            for m in _RAW.finditer(line):
                if m.group(1) in VALUES:
                    continue
                if re.match(r"\s*\]\s*=(?!=)", line[m.end():]):
                    continue
                bad.append(f"BYPASS      {m.group(1)} read raw at {name}:{i}, not through "
                           f"armflag.arm")
    return bad


# EVERY ARM SET TO "0" READS OFF -- Isaiah's ruling, 2026-10-08. Eighteen arms read the raw
# string's truthiness, so "0" turned them ON and a run record saying "=0" could describe an
# agent running with the arm on. Checked in a fresh process, because the flags resolve at import.
_SITE = re.compile(r'^(_[A-Z0-9_]+) = (not )?armflag\.arm\("(TETHER_[A-Z0-9_]+)"', re.M)
_PROBE = """
import importlib, json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import armflag
if LEGACY:
    armflag.arm = lambda n, default=False: (os.environ.get(n, "1") != "0" if default
                                            else bool(os.environ.get(n)))
print(json.dumps({f"{m}.{v}": getattr(importlib.import_module(m), v) for m, v in SITES}))
"""


def _zero_reads(legacy: bool) -> list[str]:
    """Every arm exported as "0"; the flags whose value says the arm is ON."""
    sites, expect = [], {}
    for path in _tracked():
        if path.parent != ROOT:
            continue
        for m in _SITE.finditer(path.read_text(encoding="utf-8")):
            sites.append((path.stem, m.group(1)))
            expect[f"{path.stem}.{m.group(1)}"] = (m.group(3), bool(m.group(2)))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({arm: "0" for arm, _neg in expect.values()})
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    code = _PROBE.replace("LEGACY", str(legacy)).replace("SITES", repr(sites))
    p = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env,
                       capture_output=True, text=True)
    if p.returncode:
        return [f"ZERO-IS-OFF could not import the arm sites: {p.stderr.strip()[-200:]}"]
    got = __import__("json").loads(p.stdout.strip().splitlines()[-1])
    # a negated site (`not armflag.arm("TETHER_NO_X")`) is True when its arm is OFF
    return [f"ZERO-IS-ON {arm}=0 left {k} = {got[k]}" for k, (arm, neg) in sorted(expect.items())
            if got[k] != neg]


def zero_is_off() -> list[str]:
    """The fixture and its must-fail: the real parser reads every "0" as OFF, and the old
    truthy read, planted in its place, is caught. Empty when both hold."""
    import armflag
    bad = []
    if armflag.arm("TETHER_ARMFLAG_UNSET", default=True) is not True:
        bad.append("PARSER      an unset arm did not read its declared default (True)")
    if armflag.arm("TETHER_ARMFLAG_UNSET") is not False:
        bad.append("PARSER      an unset arm did not read its declared default (False)")
    for raw, want in (("1", True), ("true", True), (" TRUE ", True), ("True", True),
                      ("0", False), (" 0 ", False), ("false", False), ("FALSE", False),
                      ("", False)):
        os.environ["TETHER_ARMFLAG_PROBE"] = raw
        try:
            if armflag.arm("TETHER_ARMFLAG_PROBE", default=not want) is not want:
                bad.append(f"PARSER      {raw!r} did not read {want}")
        finally:
            del os.environ["TETHER_ARMFLAG_PROBE"]
    os.environ["TETHER_ARMFLAG_PROBE"] = "yes"
    try:
        armflag.arm("TETHER_ARMFLAG_PROBE")
        bad.append("PARSER      'yes' was accepted; anything but 1/true/0/false/empty is refused")
    except ValueError:
        pass
    finally:
        del os.environ["TETHER_ARMFLAG_PROBE"]
    plant = {"planted.py": '_X = bool(os.environ.get("TETHER_PLANTED"))\n'
                           'os.environ["TETHER_PLANTED"] = "1"\n'
                           '_S = os.environ.get("TETHER_HOLD_SEED", "0")\n'}
    hit = bypasses(plant)
    if len(hit) != 1 or "TETHER_PLANTED" not in hit[0]:
        bad.append(f"BYPASS      UNWITNESSED: planted raw read gave {hit} (want one finding; "
                   f"a write and a declared value are not findings)")
    bad += bypasses({p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8")
                     for p in _tracked() if p.name not in ("arms.py", "armflag.py")})
    bad += _zero_reads(legacy=False)
    if not _zero_reads(legacy=True):
        bad.append("ZERO-IS-OFF UNWITNESSED: the old truthy read, planted, was not caught")
    return bad


def _tracked() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "*.py"], cwd=ROOT,
                         capture_output=True, text=True, check=False).stdout
    return [ROOT / line for line in out.split("\n") if line.strip()]


def sites() -> dict[str, list[str]]:
    """`{arm: ["file:line", ...]}` -- READ FROM THE CODE, never from the table.

    A census built from the table would agree with the table by construction, which is the
    measurement that cannot fail. The table is the CLAIM and this is the WORLD."""
    found: dict[str, list[str]] = {}
    for path in _tracked():
        if path.name == "arms.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for i, line in enumerate(text.split("\n"), 1):
            for arm in _READ.findall(line):
                found.setdefault(arm, []).append(f"{path.relative_to(ROOT).as_posix()}:{i}")
    return found


def _ruling_source(name: str) -> bool:
    """A file whose `_FOO = True` is the AGENT's ruling. A test fixture sets a flag for its own
    check and rules nothing for the agent: counted, 18 of 21 hits were fixtures and the census
    read 34 ON where the run header read 23 (the reviewer 2026-10-14 06:42, A-1)."""
    return name != "arms.py" and not name.startswith("test_")


def ruled() -> dict[str, str]:
    """`{arm: "file:line"}` for arms a RULING turned on in code, rather than the environment.

    The convention it rests on is that the module flag is the arm name without `TETHER_`, and
    that convention is CHECKED rather than assumed: a `_FOO = True` whose `TETHER_FOO` is not a
    declared arm is simply not an arm and is ignored, so this cannot invent one."""
    out: dict[str, str] = {}
    for path in _tracked():
        if not _ruling_source(path.name):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in _RULED.finditer(text):
            arm = f"TETHER_{m.group(1)}"
            if arm in ARMS:
                line = text[:m.start()].count("\n") + 1
                out.setdefault(arm, f"{path.relative_to(ROOT).as_posix()}:{line}")
    return out


def selftest() -> dict[str, str]:
    """THE THREE REFUSALS, REINTRODUCED -- `wiring.py`'s form, and for its reason.

    **Every other seat in this folder carries one and this one did not.** Its three guards were
    proven by an ad-hoc script the night it was written, which is *a suite nothing runs is a
    suite that rots* with the suite left out entirely. **A guard whose failure path is never
    exercised is indistinguishable from a guard that cannot fail** -- which is this seat's own
    subject, one level up.

    NOT A TEST OF THE WORLD. Each case perturbs the TABLE or the ENVIRONMENT and asks whether
    the rule notices; none of them depends on which arms happen to exist today, so adding or
    retiring an arm cannot make a case pass or fail for the wrong reason.
    """
    out: dict[str, str] = {}
    found = {"TETHER_A": ["x.py:1"], "TETHER_B": ["y.py:2"]}
    table = {"TETHER_A": "a", "TETHER_B": "b"}

    bad = _judge(found, dict(table), on=set(), pairs=())
    out["clean"] = "ok" if not bad else f"UNWITNESSED (refused a clean table: {bad})"

    bad = _judge(found, {"TETHER_A": "a"}, on=set(), pairs=())
    out["A undeclared"] = ("ok" if any("UNDECLARED" in b for b in bad)
                           else f"UNWITNESSED ({bad})")

    bad = _judge(found, {**table, "TETHER_GHOST": "g"}, on=set(), pairs=())
    out["B stale"] = "ok" if any("STALE" in b for b in bad) else f"UNWITNESSED ({bad})"

    bad = _judge(found, dict(table), on={"TETHER_A"},
                 pairs=(("TETHER_A", "TETHER_B"),))
    out["C half a pair"] = ("ok" if any("HALF A PAIR" in b for b in bad)
                            else f"UNWITNESSED ({bad})")

    # AND THE CONTROL FOR C, without which "half a pair" would pass by always complaining.
    bad = _judge(found, dict(table), on={"TETHER_A", "TETHER_B"},
                 pairs=(("TETHER_A", "TETHER_B"),))
    out["C control"] = ("ok" if not any("HALF A PAIR" in b for b in bad)
                        else f"UNWITNESSED (a WHOLE pair was refused: {bad})")

    # E -- RETIRED: a retired flag read anywhere is refused; and the control, so the case
    # cannot pass by refusing everything.
    bad = _judge(found, dict(table), on=set(), pairs=(), retired={"TETHER_A": "gone"})
    out["E retired read"] = ("ok" if any("RETIRED" in b for b in bad)
                             else f"UNWITNESSED ({bad})")
    bad = _judge(found, dict(table), on=set(), pairs=(), retired={"TETHER_GONE": "gone"})
    out["E control"] = ("ok" if not any("RETIRED" in b for b in bad)
                        else f"UNWITNESSED (an absent retired arm was refused: {bad})")

    # D -- THE RULING DETECTOR, over literal text so it needs no fixture file. It exists
    # because `HALF A PAIR` read the environment while the pair it was written for is set in
    # code, so the guard could not fire on its own case.
    hits = {m.group(1) for m in _RULED.finditer(
        "    arc_atoms._ITERATE = True\n"
        "    tether._SHAPE_DECODE = True  # a trailing comment must not hide it\n"
        "        self._NOT_AN_ARM = True\n"
        "    x._SHAPE_DELTA = False\n")}
    out["D ruling seen"] = ("ok" if {"ITERATE", "SHAPE_DECODE"} <= hits
                            else f"UNWITNESSED (missed a ruling: {sorted(hits)})")
    # AND ITS CONTROL: `= False` is not a ruling, and the regex must not claim it.
    out["D control"] = ("ok" if "SHAPE_DELTA" not in hits
                        else "UNWITNESSED (read `= False` as ON)")

    # F -- A FIXTURE IS NOT A RULING (A-1): a test file's `= True` must not count as ON; and the
    # control, so the case cannot pass by refusing every file.
    out["F fixture"] = ("ok" if not _ruling_source("test_d5.py")
                        else "UNWITNESSED (a test fixture counted as a ruling)")
    out["F control"] = ("ok" if _ruling_source("arc_holdout.py")
                        else "UNWITNESSED (the agent's own ruling was refused)")
    return out


# RETIRED ARMS: the ruling that retired each, so the refusal carries its own reason.
RETIRED = {
    "TETHER_INVENT": "Isaiah 2026-10-04: inventing is just a bootleg composition -- fix "
                     "composition and imports and you will not need this crutch. Measured: "
                     "53 invented, 0 priced, 0 bound, 7 delta maps all fragments of `inc`.",
    "TETHER_DOWNRATE": "Isaiah 2026-10-11 17:09 CDT: delete it, evolution does not keep what is "
                       "not used. F386: met goals undone 4/6/10 ON vs 0/0/0 OFF; F425: its "
                       "one caller never ran on click worlds. Intent covered by _goal_choice, "
                       "both spellings and cascade agency.",
}


def _judge(found: dict, table: dict, on: set, pairs: tuple,
           retired: dict = RETIRED) -> list[str]:
    """The three rules, over data handed in. Split out so `main` and `selftest` share ONE
    implementation -- a fixture that re-states the rule tests the restatement."""
    bad: list[str] = []
    for arm in sorted(found):
        if arm not in table:
            bad.append(f"UNDECLARED  {arm} is read at {found[arm][0]} and is not in the table")
    for arm in sorted(table):
        if arm not in found:
            bad.append(f"STALE       {arm} is in the table and no code reads it")
    for a, b in pairs:
        if (a in on) != (b in on):
            bad.append(f"HALF A PAIR {a}={a in on} {b}={b in on} -- their own site declares "
                       "they belong on together")
    # **RETIRED MEANS GONE -- the reviewer, 2026-10-05.** The earlier guard only refused a
    # retired arm being ON while its code stayed in the tree. The code is now removed, so the
    # guard refuses the arm being READ ANYWHERE or DECLARED: a returning flag is a breach.
    for arm in sorted(retired):
        if arm in found:
            bad.append(f"RETIRED     {arm} is read at {found[arm][0]} and is retired. "
                       f"{retired[arm]}")
        if arm in table:
            bad.append(f"RETIRED     {arm} is retired and still has a registry row")
    return bad


def main() -> int:
    # **THE FIXTURES RUN ON EVERY INVOCATION, NOT BEHIND A FLAG.** `check.py` calls this seat
    # with no arguments, so a `--selftest` nobody passes is a suite nothing runs -- which is
    # the rot this folder's own docstrings name, and it would leave the guards unexercised
    # exactly as they were before the fixtures existed. They are pure data and cost nothing.
    worst = [c for c, v in selftest().items() if v != "ok"] + zero_is_off()
    if worst or "--selftest" in sys.argv:
        for case, verdict in sorted(selftest().items()):
            print(f"  {case:<16} {verdict}")
        for line in zero_is_off():
            print(f"  {line}")
        if worst:
            print("  the seat's OWN guards are not firing; its green means nothing")
            return 1
        return 0

    found = sites()
    rule = ruled()
    # ON IS WHAT THE AGENT RUNS WITH, not what the shell exported. Both routes, one set, so
    # `HALF A PAIR` finally reads the state it was written to judge.
    dflt = defaults_on()
    # A DEFAULT-ON ARM IS ON. Three routes now, not two -- and the third is the one the
    # census could not see, so every count it printed was understating what the agent
    # runs with. An explicit falsy override still wins: `X=0` means off.
    import armflag
    on = ({a for a in found if armflag.arm(a)}
          | set(rule)
          | {a for a in dflt if armflag.arm(a, default=True)})
    bad = _judge(found, ARMS, on, PAIRS)

    print(f"arms: {len(found)} switches at {sum(len(v) for v in found.values())} read sites; "
          f"{len(on)} ON -- environment, ruling and default together")
    if dflt:
        # **WORDED SO AN INVERTED NAME CANNOT BE READ BACKWARDS.** Saying
        # "TETHER_NO_TALLY is ON" invites exactly the wrong conclusion -- the BEHAVIOUR is
        # live and the variable turns it OFF. What is true of all three is that the
        # DECLARATION evaluates true with an empty environment, so that is what is printed.
        print(f"      {len(dflt)} LIVE WITH AN EMPTY ENVIRONMENT -- the declaration is true "
              f"and the variable turns the behaviour OFF:")
        for arm in sorted(dflt):
            print(f"        {arm:<26} {dflt[arm]}")
    if not on:
        # NOT A FAILURE, AND SAYING SO IS THE POINT. All-off is the honest default for an
        # unproven arm -- the house rule is that a measurement turns one on. **The line exists
        # so the sum is never invisible again**, which is the whole reason this file is a seat
        # rather than a note: eighteen reasonable OFFs were never once read as one number.
        print("      every arm is OFF by both routes -- environment and ruling")
    if rule:
        # A RULING CAN TURN AN ARM ON WHERE A MEASUREMENT DID NOT, and the arms it turned on
        # are READ FROM THE CODE rather than named here -- see `_RULED`.
        print(f"      {len(rule)} ON BY RULING, set in code rather than exported:")
        for arm in sorted(rule):
            print(f"        {arm:<24} {rule[arm]}")
    for line in bad:
        print("  " + line)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
