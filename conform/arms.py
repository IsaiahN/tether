"""arms: every capability switch the agent reads, each with its default and its row below; the
seat prints the count and how many are ON (this line said "eighteen, all default OFF" long after
that stopped being true -- the reviewer 2026-10-30 r452 C), and nothing computed the sum.

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
                          "(F492)"
                          ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                          "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_DELTA_KEY": "route (b) re-keyed on this frame's delta"
                        ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                        "the record; the switch is kept for the checklist's culprit isolation",
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
    "TETHER_DELTA_OPERANDS": "L2, ON AS AN ORDERING (Isaiah 2026-10-26 08:24; the reviewer "
                             "08:30; Fig 9 :60 'Use filters for the budget and witnesses for "
                             "the verdict'). WHAT CHANGED: Agent._delta_narrowed no longer drops "
                             "slots; Agent._delta_tier ranks ALL candidates -- world-moved on "
                             "the residual frames (0), self-moved by 2a (1), contact partners "
                             "of a moved slot (2), the rest (3) -- the first key at both sites "
                             "(_rebindings' lookup walk; _bindings' final order, a stable sort "
                             "over today's order). WHY ON: the named defect, the lost closing "
                             "term, was the CUT; an order cannot lose one. WAS (OFF): deltas "
                             "offered as operands. HELD OFF on its named defect, the "
                             "lost closing term (the reviewer 2026-10-15 17:32; 3e census "
                             "2026-10-16)",
    "TETHER_GUARD_AXIS": "the guard axis in the reject key"
                         ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                         "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_INSTRUMENTS": "the embedded instrument set -- Part 12 item 3, PAID BILLS from "
                          "frame 0. Off at a COSTED price: a new attribute widens the slot "
                          "set and §12.12 prices that in EPISODES FORGONE"
                          ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                          "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_AGENT_SEED": "HOLD_SEED (the reviewer 2026-10-15 14:56, 15:04): the agent draws its "
                         "own seed at birth from the OS, records it (run header, lineage), "
                         "carries it through its lineage with the generation index, and every "
                         "draw (mind, interface, minted handles) uses it. default ON (Isaiah "
                         "2026-10-15 07:53); OFF is the old constant 0",
    "TETHER_HOLD": "THE RANDOMISED HOLD -- MEASUREMENT ONLY, the reviewer 2026-10-03 "
                   "ruling 3. Withholds the ACTED_SELF offer on a seeded ~half of "
                   "ELIGIBLE (cycle, slot) occasions so a measurement run carries its "
                   "own within-run control. OFF in the shipping agent: a control that "
                   "changes what the agent is OFFERED is an instrument, and leaving it "
                   "on would make every later reading a reading of the instrument",
    "TETHER_ITERATE": "the fold constructs -- `cells`/`cell_row`/`cell_col`/`count_true`. "
                      "§12.0 rules the MEANS to iterate is INHERITANCE where a solved case "
                      "would be an answer, and the agent could hold a cell set and not walk it. "
                      "**RULED ON by Isaiah 2026-09-24 and set in `arc_holdout.play` for the "
                      "ARC path, so the env census below reads OFF while the capability is "
                      "LIVE.** A ruling turned it on, not a measurement -- the house rule is "
                      "his to override. The toy world is untouched: it has its own atoms"
                      ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is the "
                      "record; the switch is kept for the checklist's culprit isolation",
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
    "TETHER_OBSERVER": "the corpus's cheap mutation set carried PER OBJECT, not counted"
                       ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is the"
                       " record; the switch is kept for the checklist's culprit isolation",
    "TETHER_PREV_OFFER": "a term reading a slot's value one frame earlier (slot~1) offered "
                         "into a mint, at three sites: _bindings' slot~1 offer, compiled ~1 "
                         "views, and CAUSE then-sides (the reviewer 07:14Z, 07:23Z). OFF: under "
                         "A3 a ~1 term cannot close, and its binding seals the slot against later "
                         "closers (demo swing: dec . neg never reached after c3; trace "
                         "2026-10-09). 16 of 18 ~1 terms settled held-out on the panel when ON. "
                         "C-HELD-5, the reviewer 2026-10-26 05:13: default ON. The seal is "
                         "repaired by TETHER_UNSEAL_START; a ~1 term pays its own statement like "
                         "any term (Fig 5 :231), and it unblocks closer (Q25)",
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
                          "not ruled. C-HELD-5, the reviewer 2026-10-26 05:13: default ON; the "
                          "gate's measurement is replaced by the 25-game rounds (Isaiah 04:51), "
                          "promotion stays held by _PROMOTE_AFTER_SETTLE, Fig 12 :807; reverses "
                          "on settles per round falling or demotes rising against r1-r9",
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
                           "default-path reader, it needs its own panel reading"
                           ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is"
                           " the record; the switch is kept for the checklist's culprit isolation",
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
                           "checks only (Isaiah 09:15)"
                           ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is"
                           " the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_ROUTINE_SUBJECT_BUDGET": "R-dir (c) (the reviewer 2026-10-11 10:39Z, 10:53Z): ON, a "
                                     "routine whose body is one BECOME intent takes its budget "
                                     "AND the count it claims (_expected) from that subject's "
                                     "own gap -- |target - now| signed, 1 on a value want -- "
                                     "not the group unsat; unreadable target keeps the group "
                                     "count. OFF: a default-path reader, joins the objective "
                                     "arms for a switch-on reading"
                                     ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF "
                                     "wording above is the record; the switch is kept for the "
                                     "checklist's culprit isolation",
    "TETHER_ROUTINE_STALE": "R-dir (ii) (the reviewer 2026-10-11 10:39Z): ON, a held routine "
                            "whose step is a signed BECOME ends `stale` before pressing when the "
                            "live _goal_target reads the OPPOSITE sign to the minted one; an "
                            "unreadable or held comparison keeps today's path (A1). A non-trial: "
                            "no verdict, no refusal, not shelved. OFF: a default-path reader, "
                            "joins the objective arms for a switch-on reading"
                            ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above "
                            "is the record; the switch is kept for the checklist's culprit "
                            "isolation",
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
                          "_goal_target and the goal exit; gate: (A) read and ruled"
                          ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                          "the record; the switch is kept for the checklist's culprit isolation",
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
                        " read and ruled"
                        ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                        "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_GOAL_LINK": "objective build 3, the link to composition (the reviewer 2026-10-11 "
                        "02:19Z, 03:14Z): ON, a held goal condition is closed into the "
                        "objective stream with `all` and becomes its slot's want, so "
                        "_goal_choice and _mint_routine can pick it; linked only where the slot "
                        "holds no want (one want per slot; replacing one is not this item's). "
                        "Needs TETHER_GOAL_CONDITION ON. OFF until the objective panel "
                        "7.5: OFF PENDING READING (B); habitat: arc_s1 at 120; reader: "
                        "_goal_choice and _goal_target (steers only with TETHER_WANT_TARGET); "
                        "gate: (B) read and ruled"
                        ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                        "the record; the switch is kept for the checklist's culprit isolation",
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
                             "(B) read and ruled"
                             ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above "
                             "is the record; the switch is kept for the checklist's culprit "
                             "isolation",
    "TETHER_COMPLETION_SWEEP": "objective build 1, the completion sweep (ARC_AGENT 21.3; the "
                               "reviewer 2026-10-11 02:19Z): ON, when the WORLD's objective "
                               "degree reaches 1.0 ('reached', not 'banked'), the segment since "
                               "the last completion is re-examined and recorded: what was "
                               "live, which terms settled, which owed slots closed. Record "
                               "only; nothing retargeted, dropped or cleared. OFF until the "
                               "objective build's panel "
                               "7.5: OFF PENDING READING (B); habitat: a world whose objective "
                               "completes (arc_s1, 6 in 120); reader: TETHER_GOAL_CONDITION; "
                               "gate: (B) read and ruled"
                               ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording "
                               "above is the record; the switch is kept for the checklist's "
                               "culprit isolation",
    "TETHER_MC6": "7a(10) MC6 muse (R3 part 2; the reviewer 2026-10-10 23:50Z): ON, on a step "
                  "that owes nothing (owed_import empty, under_floor included, and this "
                  "step's bets paying), the settled methods are re-tested as chains on an "
                  "earlier level's parked residuals, priced as the sweep prices them, and a "
                  "MUSE row records what would pay and the compute spent; nothing is "
                  "installed and no action is taken. OFF until 7-and-a-half: a reading with "
                  "no consumer yet (D1-D3 are named to read it)"
                  ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is the "
                  "record; the switch is kept for the checklist's culprit isolation",
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
                   "item 9's per-plan factors are named to read it"
                   ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is the "
                   "record; the switch is kept for the checklist's culprit isolation",
    "TETHER_CASCADE_AGENCY": "7a(6) H2, the in-between frames (R3 part 2; the reviewer "
                             "2026-10-10 22:14Z): ON, the order objects change in inside one "
                             "action gives each non-controlled object a mode (self-moved, "
                             "moving with the controlled one, reacting) in Agency. OFF and "
                             "HELD because no test world has a cascade: only arc_world "
                             "publishes one, and ARC is closed until step 13; proven on a "
                             "hand-built cascade fixture"
                             ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above "
                             "is the record; the switch is kept for the checklist's culprit "
                             "isolation",
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
                 "F408 cannot bind at a 2-a-side cut, so it was the wrong unblocker)"
                 ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is the "
                 "record; the switch is kept for the checklist's culprit isolation",
    "TETHER_CONTACT": "7a(5b), the contact instrument (Isaiah 2026-10-10 06:46 CDT; the reviewer "
                      "11:46Z, 12:27Z): ON, the REPEAT row's gamma_read gains fed, one entry per "
                      "library term read by the exit whose action is RETURNED, {kind, name, slot, "
                      "seq, role: goal|route|body}, and MC2's resolution fed becomes [REPEAT seq, "
                      "role] after the bet. Record only; read by conform/contact.py per member, by "
                      "exit and role, never pooled. OFF because it is new and nothing reads the "
                      "field yet; the per-step gamma_read reset beside it is NOT under this arm"
                      ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is the "
                      "record; the switch is kept for the checklist's culprit isolation",
    "TETHER_RUIN": "7a(5) C, ruin ordered first (R3 Part 1; the reviewer 2026-10-10 10:41Z, "
                   "11:53Z): ON, a pair the veto floor holds for THIS board is withheld from "
                   "the one choose() call at the sites below the seam (offered, TOUCH route 1, "
                   "_made's spots, the bare routine step), unless every option is vetoed; one "
                   "PLAN '@ruin' 'withheld' row per step. REQUIRES TETHER_RUIN_RECORD (import "
                   "refuses without it). OFF because it is behaviour and new: the panel never "
                   "dies, so its only evidence is the dying-world fixture until step 13"
                   ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is the "
                   "record; the switch is kept for the checklist's culprit isolation",
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
                          "one), and the panel has no deaths"
                          ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                          "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_MC_SIGNAL": "MC1 + MC2 (R3 item 4, 7a(4); the reviewer 2026-10-10 07:57Z): the signal "
                        "is the TRANSITION bet row the ground answered (ledger.signal_sign: paid "
                        "iff not vanished and mass 0); ON, each gets exactly one SETTLE "
                        "'resolution' row (signal_seq, kind level|game, how, fed) when its level "
                        "ends at retarget or the run ends with it open (end_run). fed is None: no "
                        "row names the term an action was chosen through. OFF because it is "
                        "record only and new: nothing reads the rows, and its level half has never "
                        "fired on a real level end (first real reading at step 13)"
                        ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                        "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_WINDOW": "L1 THE LOOK-BACK, ON (Isaiah 2026-10-26 08:24 'turning off a feature is "
                     "like cutting off a limb ... revamp the history window to work better with "
                     "the new system and not overpower'; the reviewer 08:30). WHAT CHANGED: "
                     "only EVIDENCE lags are offered (no-evidence lags counted, never walked), "
                     "depth at most the deepest evidence lag and at most 4f's effect window; "
                     "order (fixed 2026-10-26, the reviewer 08:47): frames the agent's own "
                     "press moved the slot (it changed, and is not in that step's 2a "
                     "reafferent set, kept per trace index) first, then frames it changed "
                     "anyway, then nearest; lag j from the live frame reads trace[-j]'s "
                     "before-state, so step -j ranks it; ~1 belongs to TETHER_PREV_OFFER, "
                     "offered in its own place in round 1 window or not, and the look-back "
                     "offers j >= 2 (fixed 2026-10-26, the reviewer 09:43: the window had cut "
                     "~1 when it had no evidence); "
                     "every lag walked in a round of its own AFTER the present frame's, so it "
                     "never takes rank from a present binding; that round runs only when the "
                     "governor (TETHER_THINK_OR_ACT) says think, and the mint row's window "
                     "record carries gate / beyond_depth / no_evidence_not_walked. WHY ON: the "
                     "measured harm below was crowding by no-evidence lags inside round 1; "
                     "this removes both. WAS (OFF): "
                     "the history window (R3 item 2; Isaiah's H1; the reviewer 14:52Z, 15:26Z, "
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
    "TETHER_REBIND_HELD": "rebinding a slot whose term is already held"
                          ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                          "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_RECIPE_DEDUP": "one candidate per recipe rather than per instance"
                           ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is"
                           " the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_DIRECTION_MOVABLE": "B (the reviewer 2026-10-12 05:43, 05:47 CDT): a slot is movable "
                                "when, in one context (its object's signed offset from the "
                                "controlled owners, from the agent's own pair slots), two "
                                "actions change it with different PURE signs; mixed cells "
                                "abstain. Adds movables only. Needs TETHER_RELATION_SET for "
                                "the pair slots. OFF until its s0 probe and OFF identity are "
                                "accepted"
                                ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording "
                                "above is the record; the switch is kept for the checklist's "
                                "culprit isolation",
    "TETHER_STREAM_SHARE": "D2 (the reviewer 2026-10-12 05:43, 06:19 CDT): within a round of "
                           "mint's search the stream that has spent the least rank takes the next "
                           "candidate (ties to list order), and a stream stops at its OWN kind's "
                           "floor. No share or quota; the shared cap is unchanged. Records "
                           "stream_share on the MINT row. OFF until R1 and OFF identity are "
                           "accepted"
                           ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is"
                           " the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_PARK_WANT": "The park return (the reviewer 2026-10-12 08:43, 08:52 CDT): when nothing"
                        " in a mint paid, the mint returned before its tail and the unpaid "
                        "objective want it ranked by recurrence (Isaiah 2026-09-25) was never "
                        "written. Under the arm the park branch writes it through the tail's own "
                        "writer, for budget_spent, not_novel and priced_out_at_depth, before the "
                        "park row, which also carries bound_at_park. Chains only. OFF until "
                        "R-exec, R-lever and OFF identity are accepted"
                        ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                        "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_DEST_GAP": "Stage 1a (the reviewer 2026-10-12 12:41, 13:04 CDT): nothing recorded "
                       "where a press LEADS, so the chooser's own Fig 5 line ('a gap "
                       "elsewhere') could not be read and least-seen alternated between "
                       "mapped contexts. Under the arm "
                       "audit keeps the post-press context beside the pre-press key, and among "
                       "equal-price reaching options ELICIT prefers one seen to lead where an "
                       "offered action's effect is unknown (one step). OFF until fixture, OFF "
                       "identity and R-exec are accepted; ground on the 25 in step 13"
                       ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is the"
                       " record; the switch is kept for the checklist's culprit isolation",
    "TETHER_AIM_GAP": "Stage 1b (the reviewer 2026-10-12 15:26 CDT): an explore press at a click "
                      "site went to a coordinate already known to move its subject (_aim_for) "
                      "ahead of an object never pressed. Under the arm audit keeps each press's "
                      "effect per (coordinate, pre-press context), and ELICIT aims first at an "
                      "object not yet pressed in this context; BECOME keeps the known knob. OFF "
                      "until fixture, OFF identity and R-exec are accepted; ground on the 25 in "
                      "step 13"
                      ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is the "
                      "record; the switch is kept for the checklist's culprit isolation",
    "TETHER_AIM_ROUTED": "THE AIMED ROUTE (the reviewer 2026-10-25 12:02, 12:17): a positioned "
                         "action realised by a route (BECOME's lands / delta / cell tier, TOUCH's "
                         "route 2) carries a coordinate from the agent's own record -- where its "
                         "presses moved this slot, this situation, since its last frame break -- "
                         "else the slot's own object (never a pair or relation slot); with "
                         "neither it is not a candidate (chosen among, never picked then "
                         "dropped); a routine's bare-string positioned step is refused. A bare "
                         "click is a scored action that lands nowhere (bare_click.out). OFF: "
                         "today's routes, no coordinate. default ON",
    "TETHER_OWN_CLOCK_SUBJECT": "THE OWN CLOCK DECIDES WHAT MOVES ON ITS OWN (Isaiah 2026-10-09; "
                                "the reviewer 2026-10-25 12:17, 12:35, 12:48): a slot the agent's "
                                "own clock writes (env.own_expected) changes with time, so a goal "
                                "hypothesis naming ANY such slot is not proposed (the proposer "
                                "also reads env.own_counted, so a track's first step is covered, "
                                "one newborn or a whole board after a game switch; the reviewer "
                                "2026-10-25 16:23, 16:37), a test on one is "
                                "graded \"own clock\" (no credit, no route reading), and a press "
                                "is not credited with one in the aim record. The instrument's keys "
                                "decide, never a slot name; an empty own clock refuses nothing "
                                "only when own_counted is ALSO empty (counted). OFF: today's "
                                "proposer, grading and record. default ON",
    "TETHER_NO_REFUTED_BIN": "**INVERTED POLARITY.** The fifth bin (Fig 5's amendment), DEFAULT ON "
                             "since F497: a refuted slot is offered a same-type competitor and "
                             "not-t is priced there (F496). The variable turns it OFF, so the A/B "
                             "is one script with one flag. Off on the shipped path it was the "
                             "switch-never-set genus (the reviewer, 2026-10-07)",
    "TETHER_REL_GAP": "the relational gap reading"
                      ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is the "
                      "record; the switch is kept for the checklist's culprit isolation",
    "TETHER_SHAPE_DECODE": "arm I -- `_as_shape`, the decoder eight SHAPE atoms need"
                           ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is"
                           " the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_SHAPE_DELTA": "`dholes`/`dperimeter` across frames. PERCEPTION: no atom accepts "
                          "OBJECT_BEFORE, so the agent cannot compose a cross-frame delta"
                          ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                          "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_STARVED_CONTACT": "the starved-contact reading"
                              ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above"
                              " is the record; the switch is kept for the checklist's culprit "
                              "isolation",
    "TETHER_STREAM_WIDEN": "L4, ON UNDER THE SHARE (Isaiah 2026-10-26 08:24; the reviewer 08:30; "
                           "Fig 6 :49-50 'Distribute the search, and keep the searchers "
                           "independent'). WHAT CHANGED: in Agent.mint's stream rounds the "
                           "widened streams (slot type -> each type the delta lights) are HELD "
                           "until every base stream (val, objective) has stopped in that round "
                           "(its own floor, exhausted, or the work budget); then "
                           "Agent._think_or_act decides whether they draw, sharing least-spent "
                           "among themselves. The mint row's widen record: the widened kinds "
                           "and the gate per round; their turns, rank and pays are in "
                           "stream_share. WHY ON: the 09-23 refutation was under ONE shared "
                           "budget, before D2's share; held back, a widened stream cannot take "
                           "rank from a base one. Its pre-registered abort criteria are read per "
                           "round. WAS (OFF): the widened candidate streams",
    "TETHER_TYPED_BIND": "L3, ON AS AN ORDERING (Isaiah 2026-10-26 08:24; the reviewer 08:30; "
                         "Fig 9 :60 'Use filters for the budget and witnesses for the "
                         "verdict'). WHAT CHANGED: in Agent._library_fit a candidate whose head "
                         "does not accept the slot type is DEFERRED by _judge, never refused, "
                         "and walked once in a late round after every typed candidate, gated "
                         "by Agent._think_or_act; the ROUTE row typed_late records deferred, "
                         "walked, the gate and closed. WHY ON: the named defect, the tn36 "
                         "loss, was the REFUSAL; a late round cannot lose a term. WAS (OFF): "
                         "binding filtered by type. HELD OFF on its named defect, the tn36 "
                         "loss (the reviewer 2026-10-15 17:32; 3e census 2026-10-16)",
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
                         "2026-10-14 11:46 and 12:17). The bound answer is kept per Agent, keyed "
                         "(signature, entry, role, o, x), so a repeated question is a lookup, "
                         "as OFF's text-keyed compile cache is (the reviewer 2026-10-15 04:57: "
                         "unmemoised, each new key re-bound every candidate, 12.6 M rebinds on "
                         "the fake)"
                         ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                         "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_ATOMS_ONCE": "the code primitives built once per process (the reviewer 2026-10-15 "
                         "06:10, 06:13, 06:56, 07:00, 07:13, 07:18; Isaiah 06:01, 06:13): ON, "
                         "each builder's set is kept under a content token (every Atom field "
                         "through repr, the CR-normalised source digest, never ids) and every "
                         "later build of that content gets the same objects in its own list; an "
                         "Agent over the shared objects keeps the index hold's bound answers in "
                         "one memo per process, and under the lineage carry they are written by "
                         "atom name beside each generation and resolved, checked whole, at first "
                         "ask. A set with no source is refused a token and counted. OFF until the "
                         "end-of-step-7 checklist (Isaiah 2026-10-15 05:25: each feature behind "
                         "its own arm), not by doubt"
                         ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is "
                         "the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_HYP_MOVABLE_ONCE": "(C), THE EXACT SPEED BUILD (the reviewer 2026-10-23 05:00, "
                               "05:25; Isaiah 'i like c and then a'): one _goal_hypothesis call "
                               "reads agency.contingent() and env.derived() once for every "
                               "_movable_by inside it, scoped to that call; neither can change "
                               "there (they move only in perceive). OFF: per-call reads, as "
                               "before. default ON",
    "TETHER_HYP_MOVABLE_CHECK": "(C)'s CHECK: inside the scope, every _movable_by also reads "
                                "both per call and raises if either differs from the scoped "
                                "read (a verification switch, never a play setting). default OFF",
    "TETHER_DORMANT_TERM_FORM": "(c) THE DORMANT ITEM WRITTEN WHOLE (the reviewer 2026-10-22 "
                                "20:57): a boundary item's live Terms (its want_terms copy) are "
                                "written by lineage.write in their term-row form "
                                "(lineage.term_form), a record nothing rebuilds a Term from; the "
                                "live and in-memory record untouched. OFF: one Term refuses the "
                                "whole boundary item, named in dormant_refused. default ON",
    "TETHER_LINEAGE_BOUNDARY": "the boundary write (the reviewer 2026-10-15 06:46, 07:30, "
                               "07:32; Isaiah 06:20): ON with the carry and a lineage folder, "
                               "both runners write a generation after a terminal edge's "
                               "retarget and at a level clear (levels()[0] rising), through "
                               "one helper, lineage.boundary; each write moves the parent so "
                               "the chain stays one line, and carries only the terms, evidence "
                               "and dormant items new since the last. Loss window: the current "
                               "level. A write point only: nothing reaches the agent. OFF until "
                               "the end-of-step-7 checklist (Isaiah 2026-10-15 05:25: each "
                               "feature behind its own arm), not by doubt"
                               ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording "
                               "above is the record; the switch is kept for the checklist's "
                               "culprit isolation",
    "TETHER_LEVEL_EDGE": "F1, the agent perceives a level clear (the reviewer 2026-10-15 07:32, "
                         "07:42, 07:55): ON, both runners deliver a levels_completed rise with no "
                         "terminal edge as retarget(how=ADVANCE), so the level's segment is "
                         "credited, its signals resolve as a level, its owed slots park and "
                         "Agent.level counts clears; with TETHER_LINEAGE_BOUNDARY one generation "
                         "follows the retarget. Default ON (Isaiah 2026-10-15 07:53); the switch "
                         "is kept for the checklist's culprit isolation",
    "TETHER_A1_CHOOSE": "A1-CONVERT site 2 (the reviewer 2026-10-15 09:33, 09:38): the known-"
                        "effect pick through frontier_pick: residual = REACH (0 for a known "
                        "no-change; else the interface's count of unknowns reached), actions = "
                        "acts in the world (a restart throws away this attempt's; None for a "
                        "known no-change); then least-seen, then the draw. "
                        "default ON (Isaiah 2026-10-15 07:53); the switch is kept for the "
                        "checklist's culprit isolation",
    "TETHER_A1_STARVED": "A1-CONVERT site 3: which starved slot to probe, through "
                         "frontier_pick: residual = outstanding(slot), learning = how often "
                         "probed (_probe_n), then the draw; never sorted()[0]. "
                         "default ON (Isaiah 2026-10-15 07:53); the switch is kept for the "
                         "checklist's culprit isolation",
    "TETHER_A1_OBJECTIVE": "A1-CONVERT site 5: a bound objective and a retained want weighed "
                           "(settled here gates; bits = term_bits; grade events), one pick "
                           "per (cycle, slot); never bound-first. "
                           "default ON (Isaiah 2026-10-15 07:53); the switch is kept for the "
                           "checklist's culprit isolation",
    "TETHER_A1_STREAM": "A1-CONVERT group 2 site 4 (the reviewer 2026-10-15 14:23): an exact tie "
                        "in a stream's spent rank goes to the recorded draw, never the list order; "
                        "and the stream_share row. default ON (Isaiah 2026-10-15 07:53); the "
                        "switch is kept for the checklist's culprit isolation",
    "TETHER_A1_LIBRARY": "A1-CONVERT group 2 site 6 (the reviewer 2026-10-15 09:05 U3, 14:23): the "
                         "library chains enter the closure's walk at their own depth, evidence "
                         "ordering them within it, never all first. default ON (Isaiah "
                         "2026-10-15 07:53); the switch is kept for the checklist's culprit "
                         "isolation",
    "TETHER_A1_LOOKUP": "A1-CONVERT group 2 sites 7-8 (the reviewer 2026-10-15 14:27): the bind "
                        "key in the shape's order (contact gate, derived, evidence, distinct "
                        "values, draw); and the lookup_order row. default ON (Isaiah "
                        "2026-10-15 07:53); the switch is kept for the checklist's culprit "
                        "isolation",
    "TETHER_A1_DOMAIN": "A1-CONVERT group 2 site 9 (the reviewer 2026-10-15 09:05 U2, 14:23): an "
                        "objective's unseen values stay reachable, priced by novelty beside "
                        "distance, never removed. default ON (Isaiah 2026-10-15 07:53); the "
                        "switch is kept for the checklist's culprit isolation",
    "TETHER_A1_TIES": "A1-CONVERT exact ties (sites 10, 11, 12, goal_condition, and in the "
                      "interface the aim among the unpressed and the band pick): the least-"
                      "known, then the recorded draw; never a name, a text or a position. "
                      "default ON (Isaiah 2026-10-15 07:53); the switch is kept for the "
                      "checklist's culprit isolation",
    "TETHER_SLOT_FILTER": "SPEED-1 S1 (the reviewer 2026-10-15 11:05): under the hold, "
                          "_index_reach binds only the held rows that land on the asked slot "
                          "(a CAUSE's then-slot); refusals and quantified rows counted as "
                          "before; its own memo, keyed with the slot, never written to the "
                          "lineage as a whole view. OFF binds every held row, as before. "
                          "S1c (12:02): a pair asked for a second slot is promoted, its whole "
                          "bound once and held as a whole; a held whole is read through a slot "
                          "map built once, never scanned per slot. "
                          "default ON (Isaiah 2026-10-15 07:53); the switch is kept for the "
                          "checklist's culprit isolation",
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
                           "registered 2026-10-14 16:29; RL-5 restated 17:02)"
                           ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above is"
                           " the record; the switch is kept for the checklist's culprit isolation",
    "TETHER_SPEED2_COUNT": "SPEED-2 item 1 (Isaiah 2026-10-15 17:24; the reviewer 17:31, 17:32): "
                           "a pair's refusals are counted ONCE into the Counter _index_reach "
                           "adds, never re-iterated per slot, bound, or stored in a slot's memo; "
                           "the named compile (compound partners) is split once per pair. The "
                           "same views, causes and counts. OFF is the line before it exactly. "
                           "default ON (Isaiah 2026-10-15 07:53, 17:26); the switch is kept for "
                           "the checklist's culprit isolation",
    "TETHER_DEAD_PRICE": "Decay class S1 (Isaiah 2026-10-15 15:54; the reviewer 16:18, 18:13): "
                         "on a dead board a press adds nothing to the restart's price, the "
                         "restart reads the interface's reach (the leads-back zero skipped) and "
                         "every other press reads reach 0. OFF is the line before it exactly. "
                         "default ON (Isaiah 2026-10-15 07:53, 17:26); the switch is kept for "
                         "the checklist's culprit isolation",
    "TETHER_SITUATED_EFFECT": "Decay class S2: an effect is stamped with its situation's epoch; "
                              "within the epoch the latest decides, an earlier change carries, "
                              "an earlier no-effect and destination lapse (read-side; the "
                              "record only grows). OFF is the line before it exactly. "
                              "default ON (Isaiah 2026-10-15 07:53, 17:26); the switch is kept for "
                              "the checklist's culprit isolation",
    "TETHER_SITUATED_REACH": "Decay class S5: a reach verdict is filed with whether it was watched "
                             "alive. OFF is the line before it exactly. "
                             "default ON (Isaiah 2026-10-15 07:53, 17:26); the switch is kept for "
                             "the checklist's culprit isolation",
    "TETHER_SITUATED_CLICK": "Decay class S11: a click from an earlier epoch excludes nothing; "
                             "within the epoch recency orders (unclicked first). OFF is the line "
                             "before it exactly. "
                             "default ON (Isaiah 2026-10-15 07:53, 17:26); the switch is kept for "
                             "the checklist's culprit isolation",
    "TETHER_RESET_ADJACENT": "RESET ADJACENCY (Isaiah 2026-09-29 'no consecutive resets'; "
                             "the reviewer 2026-10-25 22:21, 22:46; PLAY11 round 2's c12-c13 "
                             "RESET,RESET chosen by Interface.undirected): the flag is set where "
                             "the press is SENT (Interface.note_sent after env.step), not in "
                             "audit; one helper (Interface.adjacent) drops RESET from the offer "
                             "right after a RESET in realise, undirected and a bare routine "
                             "step; an agent-side backstop refuses a RESET,RESET at the send "
                             "(row reset_adjacent_refused); a RESET-only offer after a RESET "
                             "proposes nothing (row no_action). OFF: the flag from audit and "
                             "realise's re-choose only, as before. default ON",
    "TETHER_AIM_INSIDE": "(2c) AIM INSIDE THE OBJECT (Isaiah 2026-10-26 04:51 build order, the "
                         "reviewer 04:53; UMW A7): Interface._at / _acted take the world's "
                         "cell_of (ArcWorld.aim_cell: the shape key placed at row/col, the "
                         "occupied cell nearest the box centre), set by the agent at construction "
                         "and retarget, so a positioned press lands on a cell the object occupies, "
                         "not its bounding-box corner. A world with no aim_cell, or an undecodable "
                         "shape: the corner. OFF: the corner always, as before. default ON",
    "TETHER_AFF_MOVER": "(3a) THE AFFORDANCE RECORDER FED ITS MOVER (Isaiah 2026-10-26 04:51 build "
                        "order, the reviewer 04:53; UMW A3): ArcWorld.step passes "
                        "Affordances.note the one locus the control mode holds embodied "
                        "(ArcWorld._mover, read off the current mode streaks through _held_by, "
                        "the rule mode() uses, never advancing them), so blocks / passes are "
                        "written on contact with the self. No held locus, or more than one: "
                        "mover None, those readings unread. OFF: mover=None, as before. "
                        "default ON",
    "TETHER_UNREALISED_WHY": "(4b) A FAILED REALISE RETURNS A REASON (Isaiah 2026-10-26 04:51 "
                             "build order, the reviewer 04:53; UMW A6): every None "
                             "Interface.realise returns goes through _none(kind, why, asker): "
                             "blocked / no way known / tried and failed (_tried: an offered "
                             "action's table holds a cell on the subject), kept in "
                             "iface.unrealised and a bounded log the agent's REPEAT row drains "
                             "each step (unrealised). The None itself is unchanged. OFF: a bare "
                             "None, nothing recorded, as before. default ON",
    "TETHER_URGENCY_PROGRESS": "(6d) COMMIT URGENCY FROM STEPS SINCE PROGRESS (Q24; Isaiah "
                               "2026-10-26 04:51 build order, the reviewer 04:53): the commit "
                               "bar's clock (idle in the accumulator's threshold) counts cycles "
                               "since any objective gap last shrank (_last_progress, stamped in "
                               "_note_progress where g < prev), not since the last commitment. "
                               "OFF: since the last commitment, as before. default ON",
    "TETHER_DEATH_KEEPS": "(6b) A DEATH KEEPS THE LEVEL'S BINDINGS AND REFUSALS (Q12, Q18, R-D "
                          "carry; Isaiah 2026-10-26 04:51 build order, the reviewer 04:53; AUD "
                          "link 5): at a death retarget holds self.bound and _route_refused "
                          "(_held_level), and restarted() carries back (_restore_level) each "
                          "entry whose objects (_objs_named plus every o<n> in the key's text) "
                          "were re-found as overlap or unique-shape, the held refutations' rule; "
                          "row death_kept with kept / dropped per store. OFF: both cleared at "
                          "every boundary, as before. default ON",
    "TETHER_UNDO_WEIGHED": "(4h) A MET GOAL UNDONE IS WEIGHED (09-29; Isaiah 2026-10-26 04:51 "
                           "build order, the reviewer 04:53; AUD link 4; WATSON case 7): in "
                           "_note_decision, when the intent has undone an objective that holds "
                           "now MIN_REPEAT times or more, the route the press took "
                           "(_route_key: intent, action, coord, context) is refused through R-B's "
                           "_route_refused (why undoes_met_goal, row route_refused), which the "
                           "choosing path reads; the decision row reads 'weighed'. Below the bar, "
                           "or OFF: the conflict row only, 'not yet weighed', as before. "
                           "default ON",
    "TETHER_REAFFERENCE": "(2a) I-B REAFFERENCE (the 10-23 design; UMW A1; Isaiah 2026-10-26 "
                          "04:51 build order, the reviewer 04:53): Agent._reafferent(after) "
                          "names the slots that changed anyway -- an own-clock slot on its own "
                          "rule's value (env.own_expected) and every slot of an object the last "
                          "cascade read SELF_MOVED (_self_moved_now, set in _cascade_agency) -- "
                          "and Interface.audit(reaff=) drops them before crediting the press "
                          "(changed, delta, lands, signs), keeping them as last_reaff; the R4 "
                          "audit row adds reafferent. OFF: every changed slot credited, as "
                          "before. default ON",
    "TETHER_TOUCH_FELT": "(2b) TOUCH IS FELT (UMW A2; Isaiah 2026-10-26 04:51 build order, the "
                         "reviewer 04:53): System 0's contact pick is held as _contact_pending "
                         "(with its pair) instead of being marked explored before the press; "
                         "after the audit, _contact_felt reads contact made (the press landed on "
                         "the pair, or a slot of either changed in the credited set) in a "
                         "contact row, and marks the key explored when made or after MIN_REPEAT "
                         "tries without contact. OFF: marked before the press, as before. "
                         "default ON",
    "TETHER_STEER": "(4c) R-F STEERING (Isaiah 2026-10-23 19:19; the 10-23 design; A11; the "
                    "reviewer 2026-10-26 04:53, 05:27): Agent._steer reads each graded goal-exit "
                    "press on course (closer / reached) / nothing happened / wrong way (farther, "
                    "not reached) / wrong thing (no change on the subject, another credited slot "
                    "changed), row steer; off course, the route is set aside once for the next "
                    "realisation of that intent in that context (_route_offer, only while "
                    "another offer exists); a wrong thing re-states the intent with its target "
                    "named (_rf_restate -> R-C's Specific form in _goal_split). 4b's reader: "
                    "route_exhausted carries the interface's reason (iface.unrealised) and its "
                    "next move, 'no way known' -> re-state the intent, else another subject. "
                    "OFF: R-B alone, as before. default ON",
    "TETHER_IA_SERVED": "(4a) I-A, THE LIMB LEARNS FROM THE PROGRESS VERDICT (the 10-23 design; "
                        "UMW A5; Isaiah 2026-10-26 04:51 build order, the reviewer 04:53): "
                        "Agent._steer sends each R-F reading down as Interface.verdict(intent, "
                        "context, action, coord, on course), kept in iface.served; "
                        "Interface._served offers FIRST, in both BECOME branches of _choose, the "
                        "realisation that served this intent in this context more often than "
                        "not (not withheld); and the audit receives what the press meant "
                        "(Agent._meant: intent, why, mode; iface.last_meant; the R4 audit row's "
                        "meant). OFF: none of it, as before. default ON",
    "TETHER_CAN_PROBE": "(3d) Q23, A CAN-UNKNOWN AFFORDANCE GETS A CHEAP PROBE (AUD link 2; "
                        "Isaiah 2026-10-26 04:51 build order, the reviewer 04:53): where the "
                        "routine mint refuses because CAN is unknown (never no), the slot's "
                        "object is held as one probe (row can_probe); _contact_target offers it "
                        "first to System 0's TOUCH while the object exists, and it is spent when "
                        "TOUCH reaches it, pressed or abstained. OFF: the refusal alone, as "
                        "before. default ON",
    "TETHER_BODY_APPEND": "THE BODY RECORD STARTS WITH ITS LEDGER (the reviewer 2026-10-26 06:02; "
                          "PLAY11 r9's c0-c96 @body rows lost): Agent._consolidate opens "
                          "{ledger}.body.jsonl 'w' once per ledger object (led._body_opened), "
                          "'a' after, so (B)'s fresh agent on the same ledger appends instead of "
                          "truncating the faulted agent's rows. No ledger row changes. OFF: 'w' "
                          "at each agent's first fold, as before. default ON",
    "TETHER_ACTION_KINDS": "(3b) SYSTEM 0's ACTION KINDS (Isaiah 09-28; AUD link 2, Fig 3 :7; the "
                           "04:51 build order): Interface.action_kinds reads, per action per "
                           "contact context (MIN_REPEAT presses or unread), repeatable / cyclic "
                           "(a value chain back to its start, Interface._cycles) / count-limited / "
                           "one-time switch / inert / varies off the table's ep and lands; a "
                           "do-nothing that acts elsewhere is a WALL only where the world's "
                           "affordance recorder read something to block (3a), else 'no effect "
                           "here'; an effect here that is nothing elsewhere is a CROSSING only "
                           "where it read something to pass. OFF: not computed. default ON",
    "TETHER_CAP_READ": "(3c) 'YOU CAN NOW ...' REACHES THE MODES (Isaiah 09-28; AUD link 2; Fig 11 "
                       ":40, Fig 10 :24-25; the 04:51 build order): Agent._cap_read rows each "
                       "change of the kinds (action_kinds); when a way to act opened or a switch "
                       "is newly read as used, the route refusals earned before (but "
                       "undoes_met_goal) are set aside into _route_stale, kept, and the routes "
                       "re-engaged (capability_read). OFF: the report is recorded and read by "
                       "nothing, as before. default ON",
    "TETHER_SITUATED_REFUSAL": "(4d) S4, A REFUSAL IS SITUATED (Q16; UMW A9; the 04:51 build "
                               "order): Agent._situation keys R-B's route refusal (and 4h's) by "
                               "the subject slot's own objects' contact kinds "
                               "(Interface.context's actor filter, merged over a compound owner) "
                               "plus ('@alive', 0|1); the table and realise keep the whole-board "
                               "key for pooled presses; no epoch, since R-D carries refusals "
                               "across a death; a slot with no object keeps the board key. OFF: "
                               "the whole-board key, as before. default ON",
    "TETHER_PRED_FIRST": "(4e) I-C, THE CURRENT PREDICTION BEFORE THE POOLED TABLE (the 10-23 "
                         "design, approved; WATSON P5; the 04:51 build order): the goal exit "
                         "asks Agent._predicted_serves which offered actions the SETTLED term "
                         "bound on the subject slot predicts move it nearer the stated target, "
                         "else in the intent's sign, from this state; realise is asked over "
                         "those first (row predicted_route), and the table's pick when it names "
                         "none or cannot realise them. A term on trial, an unreadable or "
                         "no-change prediction names nothing; _pred_raw restored. OFF: the "
                         "table alone, as before. default ON",
    "TETHER_DELAY_WINDOW": "(4f) R-E, A DELAYED EFFECT IS REFUSED ONLY AFTER ITS PREDICTED WINDOW "
                           "(the 10-23 design, approved; WATSON case 6; the 04:51 build order): "
                           "Agent._effect_window is the largest lag j the slot's bound term "
                           "reads (operand x~j, through operand_term); R-B's no-change count "
                           "refuses at MIN_REPEAT + window, a refusal held back by the window "
                           "rowed route_waiting; 'farther' still refuses at once; no lag, window "
                           "0, unchanged. OFF: MIN_REPEAT, as before. default ON",
    "TETHER_SURPRISE_NOMINATES": "(5a) A4, SURPRISE SAYS WHERE TO LOOK (Isaiah 2026-10-25 20:21 "
                                 "'do what the tether says'; Fig 1 :28, Fig 9 :53): in "
                                 "_goal_choice the objects carrying unexplained surprise "
                                 "(outstanding > 0) nominate; among wants that pass the "
                                 "shrinking bar, a nominated one ranks first (a lexicographic "
                                 "prefix, never a filter, so an un-nominated want still "
                                 "qualifies); surprise is never scored or maximised (Fig 1 "
                                 ":23-27); row nominated (gate 1 only) when it changed the "
                                 "pick. OFF: as before. default ON",
    "TETHER_S0_CONTEST": "(5b) SYSTEM 0 NEVER HOLDS THE WHEEL (Isaiah 09-28; AUD link 3, PLAY11 "
                         "r1: 44 of 72 presses System 0's; the 04:51 build order): while System "
                         "0 is active, distinguish and goal still enter Agent._exit_choice's "
                         "contest beside it, weighed by A1's readings (outstanding where each "
                         "aims, turns taken this level, the draw); the exit row carries "
                         "s0_contest. OFF: the goal-directed exits defer to it, as before. "
                         "default ON",
    "TETHER_DEATH_VOTE": "(5c) A12, A DEATH VOTES ON THE ROUTE TOWARD THE GOAL (Isaiah 2026-10-25 "
                         "20:21; Fig 11 :49, :51; Fig 7 :35): every audited press is counted "
                         "under Agent._press_kind (the held goal's slot kind, the action, the "
                         "situation's contact kinds; never names, never alive); a death adds a "
                         "vote to the last press's kind (retarget, row death_vote); the reading "
                         "is deaths / presses, so it decays as such presses survive; the goal "
                         "exit realises over the never-voted offers first (row danger_order, "
                         "also within I-C's predicted set) and _goal_choice ranks a want whose "
                         "kind carries deaths after, below A4's nomination. No action is "
                         "removed, RESET included. OFF: deaths are not read. default ON",
    "TETHER_SUBGOAL": "(4g) R-C, SUBGOALS ARE ROUTES (the 10-23 design; the reviewer 2026-10-26 "
                      "06:19: only on an enabling reading the code already holds): "
                      "Agent._enablers reads the SETTLED term bound on a slot for an operand "
                      "(Term.operand, lag stripped, through operand_term) on ANOTHER object; at "
                      "route_exhausted ('another subject', not a re-statement) the first such "
                      "slot with an open want is held as the subgoal (row subgoal_adopted, "
                      "naming the operand read) and _goal_choice selects it while open, so R-B "
                      "reads routes on its gap and the parent's growth refuses nothing; ends on "
                      "arrival, its own exhausted routes, or the level (row subgoal_end). OFF: "
                      "as before. default ON",
    "TETHER_REENGAGE": "(6a) R-D, UNREACHABLE AT BUDGET, THEN RE-ENGAGE (the 10-23 design; A11; "
                       "Fig 8 :40-41): route_exhausted carries verdict 'unreachable at budget' "
                       "and the intent is kept in Agent._unreachable with the situation it was "
                       "read in; when a route is offered for it again (its situation moved, 4d, "
                       "or its refusals were set aside, 3c), row re_engaged (since, "
                       "situation_changed, action). Refusals untouched; cleared at the level. "
                       "OFF: as before. default ON",
    "TETHER_ROUTINE_CARRY": "(6c) ROUTINES CARRIED BY KIND (the reviewer 2026-10-26 06:32, ruled; "
                            "Fig 4 :22-24): Agent._routine_form writes each settled routine with "
                            "every slot as its kind key and a TOUCH object as its kind (a Call, "
                            "Let, repeat, or a name that is no slot/object is not carried); "
                            "lineage._write adds the optional generation field routines_by_kind "
                            "(absent when nothing new, so such a generation is as before); "
                            "lineage_store._counts_apply folds it ONE ROW PER KIND FORM (load "
                            "grows with distinct kinds, never lifetime); both load paths hand it "
                            "to Agent._carry_routines_in; per level Agent._carried_cands binds "
                            "each form where every kind has exactly one slot here (row "
                            "routine_bound: carried, bound, unbound) and the routine mint offers "
                            "the bound ones as CANDIDATES (on trial, never settled). An older "
                            "store without the field loads as none. OFF: none of it. default ON",
    "TETHER_THINK_OR_ACT": "THE GOVERNOR, THINK OR ACT (Isaiah 2026-10-26 08:24 'similar position "
                           "to overthinking versus when action is better'; the reviewer 08:30; "
                           "Fig 12 :125-130, two currencies read apart): Agent._think_or_act "
                           "(slot, closer) -> (walk, why), read by the look-back (L1), the "
                           "typed-late round (L3) and the widened streams (L4) before each walks: "
                           "closer_found (a present-frame binding closed in this mint) / urgent "
                           "(steps since progress, 6d, have lowered the commit bar to its floor: "
                           "idle / relief rate >= _QUORUM_HALF) / urgent_declined (urgent, but "
                           "the slot was deferred urgent at an earlier cycle: it walks this "
                           "cycle and may be deferred again at the next, so under urgency the "
                           "library is consulted every other step, never zero; the reviewer "
                           "2026-10-26 11:52 item 3) / probe_first (3d's probe names "
                           "the slot's object, or an advertised action was never tried) / "
                           "probe_declined (the same probes were open at an earlier cycle's ask "
                           "for this slot and none was taken since: the agent chose not to act, "
                           "so it may think; the reviewer 08:47, no constant) / ok. "
                           "Agent units only, no wall clock. OFF: the three walk ungated. "
                           "default ON",
    "TETHER_STEP_ACT": "A1, THE GOVERNOR AT THE STEP (Isaiah 2026-10-26 11:25 'still sounds like "
                       "that think act fix isnt in place yet'; the reviewer 11:33; Fig 12 "
                       ":125-129, two currencies, act when an action is cheaper; Fig 5 :12, aim "
                       "the probe): Agent.route asks Agent._think_or_act(slot, closer=False) "
                       "before a slot's library lookup (the mass-0 owed lookup and the residual "
                       "lookup). urgent / probe_first -> Agent._defer_lookup: the lookup is not "
                       "run this step, the slot is OWED through C1's queue (asked first next "
                       "step), the ROUTE row lookup_deferred names the why, and the bin falls "
                       "through as a lookup that found nothing does (MECHANISM) -- recorded as "
                       "deferred, never as not found (Fig 9 :60). ok / probe_declined / "
                       "urgent_declined -> the "
                       "lookup runs as today. The refuted-bin lookup is NOT gated: it answers a "
                       "refutation in hand. Per step the ROUTE row step_act: lookups_walked and "
                       "lookups_deferred by why. OFF: every lookup runs as before. default ON",
    "TETHER_STEP_CLOCK": "THE STEP CLOCK, A LEDGER INSTRUMENT (the reviewer 2026-10-26 r263 (b); "
                         "Fig 1, every claim names its instrument): never read by the agent. "
                         "Agent.step opens a clock; Agent._step_scope times each step scope "
                         "EXCLUSIVELY (a nested scope's time is its own, never its parent's). Each "
                         "REPEAT row carries wall_s per scope that ran (PERCEIVE, ROUTE, ACCEPT, "
                         "MINT, PLAN, SETTLE, ...), other and total, plus trace_len, wants_n, "
                         "owed_import_n, gamma_reuse_live (live Gamma terms whose stamp residual "
                         "starts reuse:) and gamma_reuse_on_board (of those, the ones whose "
                         "object ids are all on the current slots; r264); the ACCEPT row "
                         "step_mint and each MINT park row carry "
                         "wall_s. Nothing the agent decides reads them (tests/test_step_clock.py "
                         "guards it). OFF: none of these keys is written. default ON",
    "TETHER_STEP_DERIVED": "B2, ONE STOP PER STEP FOR EVERY MINT KIND (the reviewer 2026-10-26 "
                           "r270; the think-or-act rule; Fig 9 :60 owed, never a verdict): the "
                           "derived-want mints after the ACCEPT loop (Agent._derived_wants) share "
                           "B1's stop. If an ACCEPT-loop mint this step parked at a bound "
                           "(budget_exhausted), every derived ask that would mint is OWED; else "
                           "they run and the first that exhausts sets the stop and the rest are "
                           "owed. An owed ask is a MINT row derived_deferred (owes, after, its "
                           "transition), is NOT marked tried (so it stays askable), and is asked "
                           "first next step while still declared derived and wanting nothing; "
                           "one no longer due is dropped and counted. Per step the MINT row "
                           "step_derived: derived_run, derived_deferred, owed_dropped, "
                           "derived_stop, stop_from_accept. Echo asks (no mint) and the D5 and "
                           "G1 paths are not touched. OFF: every derived mint runs, as before. "
                           "default ON",
    "TETHER_ARRIVAL_GAP": "5, THE ARRIVAL GAP (the reviewer 2026-10-28 r280, r283; Isaiah 10-28 "
                          "'same seed, new soil'; Fig 5 :4-5, Fig 11 :73; not TETHER_ARRIVAL, "
                          "GQ3's goal predicate). arc_world.arrive defers the tracker's appearance "
                          "call on the new frame's first board-changed decomposition (claims kept, "
                          "state from before kept); at the next step head Agent._arrival_gap "
                          "scores the frame the agent held (perceive's after) against the arrived "
                          "one, per slot, held or failed (gone counts failed). Break iff the share "
                          "is above every ORDINARY no-press reading this life (every other step "
                          "head is one; no constant); before the first, the appearance call "
                          "decides alone, as OFF. A break restores the tracker and re-reads the "
                          "frame with that call's break forced; what a break does is unchanged. "
                          "Rows arrival_gap (held, failed, share, carried, changed, bar, bar_n, "
                          "decided_by, broke, applied, appearance) and appearance_disagrees. OFF: "
                          "the appearance AND-gate decides at arrive, as before. default ON",
    "TETHER_INSTANCE_RETIRE": "2, INSTANCE TERMS LEAVE THE LIVE SET AT THE AGENT'S OWN BREAK (the "
                              "reviewer 2026-10-29 r292, r294; Fig 6 :42, Fig 10 :68). At the "
                              "turnover after any applied frame_break (arrival or seam), a gamma "
                              "term stamped 'reuse:' naming an object the break did not re-find "
                              "(env.identity not overlap / unique-shape) goes to Gamma.retired, "
                              "the record (blob still writes it; never read back); one a live "
                              "binding still names stays until the binding drops. Its kind (the "
                              "term with no operand, origin the instance's, residual "
                              "kind:<instance>@cycle) is installed if not held, and takes the "
                              "instance's evidence by replay, its own per-slot standing kept. "
                              "Row instance_retired per break (count 0 included). OFF: no term "
                              "leaves the live set, as before. default ON",
    "TETHER_KIND_SAVE": "3, THE SAVE CARRIES THE KIND, NEVER THE INSTANCE (the reviewer 2026-10-29 "
                        "r292, r294; Fig 4 :22, Fig 10 :68). lineage.write: an instance row (one "
                        "with an operand) writes no alias and its 'was' is its kind's name "
                        "(gamma.Gamma.kind_of, the rule load_blob installs by); an evidence row "
                        "naming an instance is written under that kind name, so the load-time "
                        "replay lands on the same term as through today's alias. Rows otherwise "
                        "unchanged. OFF: instance aliases and instance-named evidence, as before. "
                        "default ON",
    "TETHER_SETTLE_PRED": "THE SETTLE ROW CARRIES ITS OWN PREDICTION, RECORD ONLY (the reviewer "
                          "2026-10-29 r288, r294; harvest item 6). Agent._settle_pred adds to each "
                          "settle row: predicted_code (the residual's own, the maker's), "
                          "actual_code, from_value (this step's trace row) and from_code in the "
                          "code space the ground judged in (the slot's alphabet), and risky = "
                          "predicted_code != from_code (persistence would have been wrong). No "
                          "decision reads it. OFF: the row as before. default ON",
    "TETHER_PLAN_NARROW": "4 PLAN_NARROW (the reviewer 2026-10-29 r325 ASK 3, r365; Fig 12 :127). "
                          "_hyp_propose_body admits candidates in two phases when the goal shelf "
                          "holds a won record: the shelf-won texts first (known before "
                          "compiling), the rest only if the won groups yield no pick. Every won "
                          "group ranks above every other and the walk stops at the first group "
                          "with a route, so the pick is today's. The goal_hypotheses row carries "
                          "compile_reads (compile-cache reads in the phases run), not_admitted "
                          "(texts in a phase never run: no route-first, compile or filter), "
                          "phases and wall_s; open, ranked and refused cover "
                          "the phases run; the cap record carries phases. The kind-scoped cut is a "
                          "later item. OFF, or nothing won: one phase, as before. default ON",
    "TETHER_CONTACT_FIRST": "1 CONTACT_FIRST (Isaiah 2026-10-30 06:19-06:21; the reviewer r392, "
                            "r393; Fig 12 :126-127, Fig 9 :53). In the step's mint, read from the "
                            "step's own record: (a) the act was already named (a settled "
                            "prediction served the intent -- predicted_route taken -- or a held "
                            "routine emitted it), or (b) the gap holds the same rows under the "
                            "same 1a key and library size as at its last walk, so nothing the "
                            "mint could form is told apart until a new row arrives. Then the "
                            "mint is not walked: the slot is owed (owed_import) with a "
                            "contact_first row (why named / same_rows); (a) walks at the next "
                            "step, (b) when the rows change. No number. OFF: the mint walks "
                            "every step, as before. default ON",
    "TETHER_ROUTE_NAMED": "2 ROUTE_NAMED (the reviewer r392, r393). In ROUTE's _defer_lookup, "
                          "before A1's reading: when this cycle's act was already named "
                          "(CONTACT_FIRST's (a), set when either arm is on) and the slot's lookup "
                          "was not already owed for it, the library lookup is not walked -- the "
                          "slot is owed through C1's queue (_owed_q, owed_import) with a "
                          "route_named row, and asked at the next step. No number. OFF: the "
                          "lookup as before. default ON",
    "TETHER_PROGRESS_SHELF": "3 PROGRESS_SHELF (the reviewer r392). At _note_progress's progress "
                             "row, each held goal condition whose slots (its _goal_links and the "
                             "slots its own text names) meet closer counts one progress. At "
                             "_close_goals with how not WIN or ADVANCE (no clear, so not already "
                             "shelved won), a condition with progress >= 1 is SHELVED through "
                             "GQ1's own shelving (_shelve_one, the M7 template carry) with record "
                             "{won 0, lost 0, progress n}; its goal_shelved row carries the "
                             "record. The proposal ranks won, then progress, then the rest "
                             "(ordinal classes; bits second, as before) and PLAN_NARROW's first "
                             "phase takes progress entries with the won. No number. OFF: close "
                             "drops them, as before. default ON",
    "TETHER_UNTESTED_KEEP": "4 UNTESTED_KEEP (the reviewer r392, r397). In _hyp_end, a goal "
                            "hypothesis that ends with steps == 0 and touches == 0 and no loss or "
                            "win (the board could not host its test) ends why 'untested' with "
                            "ended_by = the check's own why, and is kept in _untested, NOT "
                            "_hyp_tried. The proposal forms candidates only over objects present "
                            "now and its tried key carries the slot, so it comes back only when "
                            "its slot is on the board again; then a goal_hypothesis_reopened row "
                            "(ended_by, since). Reset with _hyp_tried at a level. No number. OFF: "
                            "it enters _hyp_tried, as before. default ON",
    "TETHER_CARRY_W": "5 CARRY_W (the reviewer r392, r395, r397; Symbols :20-26). In gamma: an "
                      "outcome of a carried, non-innate term in this life (settle = held; a "
                      "refute that is a refusal by Standing.refute's own held reading = failed; "
                      "replay's carried evidence excluded) counts for its kind "
                      "(gamma.kind_of(term).name); w = held / (held + failed). track_of for such "
                      "a term is w * Laplace(its standing as loaded) + (1 - w) * Laplace(this "
                      "life's own counts) once its kind has an outcome; with none, today's "
                      "track_of exactly. Orders retrieval only; settled and is_settled are "
                      "untouched; the innate core is untouched. tether writes a carry_w row "
                      "(kind, held, failed, w) per change. No number. OFF: carried standing "
                      "taken whole, as before. default ON",
    "TETHER_INDIST_ON_CHANGE": "6 INDIST_ON_CHANGE (the reviewer r400; the r396 profile: 21% of "
                               "ft09's and 32% of lp85's step time, cold). indistinguishable() "
                               "still builds the grouping every step (which owners share a "
                               "featural vector); when the set of groups with two or more "
                               "members (vector, members) equals the last one computed it "
                               "returns None: no _left walk over the slots' histories and no "
                               "indistinct row. On a change it computes as before and the row "
                               "carries since (the last row's cycle). The row has no reader; "
                               "3a's contradiction_routed is untouched. No number. OFF: every "
                               "step, as before. default ON",
    "TETHER_VIEW_HOLD_SAME": "7 VIEW_HOLD_SAME (the reviewer r414, r415; the r396 profile: on sp80 "
                             "nearly every _lib_view call bypassed the hold since G1 asks "
                             "mine == partner). In _lib_view, a STATE / TEST / PROCESS view with "
                             "o == x and no brace in o is held once per (entry, role, 'same') as "
                             "lib.view(key, role, '{o}', '{o}'), served by _restore(held, o, o). "
                             "Exact: one placeholder keeps text equality, so PROCESS's dedup by "
                             "condition keeps the same rows in order. MEASURE / RELATION stay "
                             "bypassed (partner_named reads the name). _view_hold_n counts "
                             "held_same / served_same; the memo_sizes row carries view_hold. No "
                             "number. OFF: the o == x view computed fresh, as before. default ON",
    "TETHER_VIEW_HOLD_SAME_ROLE": "8 VIEW_HOLD_SAME_ROLE (the reviewer r417). The same "
                                  "one-placeholder hold for MEASURE / RELATION views with o == x "
                                  "(they reach _lib_view as the 'role' bypass, so the branch reads "
                                  "o == x directly): (key, role, 'same'), lib.view(key, role, "
                                  "'{o}', '{o}'), _restore(held, o, o); counts held_same_role / "
                                  "served_same_role. Exact because partner_named is library "
                                  "_names, a whole-id regex whose edge class excludes braces; one "
                                  "collision is named, not proved absent (a reading name equal to "
                                  "an id), and TETHER_VIEW_HOLD_SAME_CHECK counts it. No number. "
                                  "OFF: computed fresh, as before. default ON",
    "TETHER_CONTINGENT_ONE_PASS": "9 CONTINGENT_ONE_PASS (B3, the reviewer r427): "
                                  "instruments.Agency.contingent groups tried by slot in ONE pass "
                                  "and applies the same always / never tests per slot, returning "
                                  "the same sorted list; OFF scans the whole of tried once per "
                                  "distinct slot (quadratic in what was ever noted; 49 s of own "
                                  "time at cycle 85 in B3). Exact: the same keys are read, and a "
                                  "Counter's missing key reads 0 without inserting. Cost-only. "
                                  "default ON",
    "TETHER_ARRIVAL_ALIAS": "10 ARRIVAL_ALIAS (the reviewer r428, r431, r432; Fig 10 :68 'a "
                            "generator crosses, an instance does not'). At the turnover after the "
                            "agent's own frame break, Agency's (slot, action) counts on objects no "
                            "longer on the board move to Agency.dormant_tried / dormant_moved "
                            "(kept, never read per step), so contingent() and mode() read this "
                            "board; an object that left whose form (the break row's old_form) is "
                            "unique among those that left and equal to the form of exactly one "
                            "board object (ArcWorld.forms()) has its counts MOVED to that object, "
                            "renamed, unless the board already wrote the key (alias_collision: "
                            "left dormant). One arrival_alias row per turnover (aliases_by_form, "
                            "aliases_by_successor, kept / aliased / dormant / alias_collision). "
                            "A world without forms() (gridworld, the fake) retires only and "
                            "aliases nothing; OFF never calls forms(). No number. OFF: the counts "
                            "of every object ever seen stay in the per-step Agency, as before. "
                            "default ON",
    "TETHER_STOP_READ_STEP": "12 STOP_READ_STEP (the reviewer r462, r463; Fig 3 :20). 1c's pass "
                             "(_stop_rules) runs after the ACCEPT loop and before the step's "
                             "SETTLE; ON its scope and its four rows (stop_rule, stop_read, "
                             "split_aim_left, remainder) say ACCEPT, where it sits. Label only: "
                             "no decision moves, no row is added or dropped. OFF: they say MINT, "
                             "so a slot that ACCEPTed this cycle reads MINT after ACCEPT and the "
                             "gate refuses the ledger (demo.py on draws c2377d1e, 838dce71). "
                             "default ON",
    "TETHER_REMAINDER_VERDICT_KEY": "14 REMAINDER_VERDICT_KEY (the reviewer r466 1(b)). The "
                                    "remainder row (1e) carries the gap's last mint verdict as "
                                    "mint_verdict and mint_verdict_cycle. Key names only: no "
                                    "decision moves, no row is added or dropped. OFF: the keys are "
                                    "the mint's own, verdict and verdict_cycle, so gate.py's "
                                    "unreached check reads the row as a park with no coverage and "
                                    "refuses the ledger (demo.py on draws c36f0f02, 838dce71, "
                                    "c2377d1e). default ON",
    "TETHER_CHANGE_TALLY": "17 CHANGE_TALLY (the reviewer r481; Isaiah 2026-10-31 02:15; Fig 11 "
                           ":40). Below the seam: interface.audit counts per action the presses "
                           "after which something credited to the press changed (changed_n beside "
                           "n), and per positioned action by the kind it landed on. Read only "
                           "inside the variety rule's tiers: an action or landing kind pressed in "
                           ">= 2 contexts that never changed anything goes last, and ties of the "
                           "tier's first reading go to the higher changed-per-press ratio; one "
                           "@tally tally_order row when it decided. OFF: no count, no row, the "
                           "tiers' order as before. default ON",
    "TETHER_CONTACT_LIGHT": "16 CONTACT_LIGHT (the reviewer r481, r483, r490, r491). The library "
                            "lookup scores a row once per (slot, val-typed candidate), not every "
                            "step (r491): _library_fit's two full-history _left calls resume a "
                            "stored prefix while the slot's _divide_key holds and the shape table "
                            "has not grown under a row that read its extent, and score only the "
                            "new rows. An OBJ-typed candidate walks its whole history (its domain "
                            "draws per cycle and writes choice rows). Needs TETHER_DIVIDE. The "
                            "repeat-mint wait was stopped, the existing deferrals already take it "
                            "(r490). Saves, on six identical movers over 20 steps: 35.5% of the "
                            "rows re-scored and 23% of the scoring time, which is 9% of the "
                            "lookup; the lookup's time is in _library_reach (r498). OFF: every "
                            "candidate is scored over its whole history at every lookup. "
                            "default ON",
    "TETHER_HARNESS_LEVEL_RESET": "13 HARNESS_LEVEL_RESET (the reviewer r464 2; Isaiah 2026-10-30 "
                                  "20:11). HARNESS, never the agent: arc_holdout._mode, the one "
                                  "call before every Arcade, sets ONLY_RESET_LEVELS=true, so "
                                  "arcengine's handle_reset makes every RESET a level reset. OFF: "
                                  "the variable is left as the environment has it, and a RESET on "
                                  "a level with no action yet (just reached, or right after "
                                  "another RESET) is a FULL reset to level 1, score 0, which "
                                  "competition play never does. default ON",
    "TETHER_RETIRE_HOLDER": "15 RETIRE_HOLDER (the reviewer r466 1(c), r470). At the break, "
                            "_repoint_retired re-points D5's three holders -- a cut candidate's "
                            "and a pending split's incumbent, a split's parts A and B -- to the "
                            "retired instance's kind when it is live, else drops that cut or "
                            "split beside the instance; _held_dangling lists them. OFF: a pending "
                            "split carries the retired name past the break, _d5_split writes it "
                            "back into bound, and _present's orphan scan raises KeyError (PLAY24 "
                            "round 8, cycles 21 and 106). default ON",
    "TETHER_ASK_ON_BOARD": "11 ASK_ON_BOARD (the reviewer r452 A). In 1b's eligibility loop a "
                           "gap whose slot is not in this step's `before` is not eligible this "
                           "step; it stays in the space and is not released, so it can be asked "
                           "on a later board that holds it. The ask and ask_none rows count them "
                           "(gaps_off_board). The test is the slot's presence on this board, never "
                           "an object id. OFF: such a gap can be chosen, and its prediction reads "
                           "state[slot] in _value_of and raises KeyError (contained in play by "
                           "fault recovery, at the cost of the life's state). default ON",
    "TETHER_VIEW_HOLD_SAME_CHECK": "7's check (the reviewer r415): each view served from the "
                                   "'same' hold is also computed fresh with lib.view(key, role, "
                                   "o, x) and compared; same_checked / same_mismatch in "
                                   "_view_hold_n. A test instrument for the must-hold. default "
                                   "OFF",
    "TETHER_NAMED_REMAINDER": "1e NAMED_REMAINDER (the reviewer 2026-10-29 r325, r364; Fig 13 "
                              ":134-139, Fig 9 :4-5, Fig 8 :39-42). When 1c's none_survive fires "
                              "(any cause), a MINT 'remainder' row on the slot: (a) among the LAST "
                              "SURVIVORS, each one's charged rows over the gap's current residual "
                              "rows by the one row test, grouped by set; two with DISJOINT sets "
                              "are several questions (the pair whose larger set is smallest, ties "
                              "by name), else 'no split found among the last survivors' -- never "
                              "'one question'; (b) the gap's kind and residual row count; (c) the "
                              "gap's last mint verdict (stored on its space with its cycle): "
                              "budget_spent is 'unreached at this budget', every other verdict "
                              "carries the mint's own note verbatim. Its wall_s is in TIMINGS. "
                              "Record only: nothing reads it. Needs TETHER_STOP_RULES. OFF: no "
                              "row, no stored verdict. default ON",
    "TETHER_STOP_RULES": "1c STOP_RULES (the reviewer 2026-10-29 r325, r327, r337; Fig 5 :10-14, "
                         "Fig 9 :42). Read from 1a's space after each step (_stop_rules, MINT): "
                         "HELD -- one S1 survivor and a risky settle of it on this slot under "
                         "the space's current key (_settle_pred's code space) -- takes the gap "
                         "out of 1b's eligible gaps; NONE SURVIVE -- the space had survivors and "
                         "has none, judged only where the record is current -- puts the slot in "
                         "owed_import, whose route refits before a mint (r338); each "
                         "change is a stop_rule row. SPLIT REFUSED -- 1b abstained -- writes "
                         "ask_unsplit (never the goal split's split_refused) and adds the gap "
                         "to the probe's aim set beside _starved "
                         "(_aims), spent once the probe presses at the owner, or left when the "
                         "owner reads anew or the space closes (split_aim_left); a spent gap "
                         "re-enters only on a new refusal key. Nothing binds. Needs TETHER_ASK. "
                         "OFF: as before. "
                         "default ON",
    "TETHER_OWED_REJUDGE": "1d OWED_REJUDGE (the reviewer 2026-10-28 r281, 2026-10-29 r326 "
                           "Option A; Fig 11 :51, Fig 3). Each owed derived ask is re-read "
                           "against the current frame and released (owed_released, with why) "
                           "when no longer derived, when it wants, or when none of its sources "
                           "(env.derived()) has outstanding > 0 ('sources explained'); never "
                           "marked tried, so new evidence re-raises it. Newer evidence replaces "
                           "its stored transition (owed_superseded). The step's mint candidates "
                           "take their turns by _understanding, ties by A1 (mint_rank row); "
                           "derived asks rank 0 and run after them, ordered by A1. Releases "
                           "'level end' at retarget and 'outranked' at end_run. OFF: B1/B2's "
                           "owed-first order as before. default ON",
    "TETHER_ASK": "1b ASK (the reviewer 2026-10-29 r279, r322, r325; Fig 9 :38, Fig 5 :12). Under "
                  "TETHER_DIVIDE, choose's DISTINGUISH is aimed at ONE gap: among the open spaces "
                  "with two or more survivors (S1, bargain-shaped, r327: terms in valid cells "
                  "whose stored bound, cost + unit x rows charged, is still below the current bar, "
                  "ranked by deficit), the one _understanding ranks first (ties: A1). Each "
                  "survivor's prediction of the slot under each offered action gives the split as "
                  "block sizes; interface._choose takes the press whose largest block is smallest "
                  "(then more blocks, then A1; a live board's RESET splits nothing, D-WIN-RESET) "
                  "or abstains when no press splits, and then the board-level DISTINGUISH runs as "
                  "before. An aimed DISTINGUISH competes in "
                  "_exit_choice with its gap's outstanding. Row: PLAN 'ask'. OFF: DISTINGUISH as "
                  "before. default ON",
    "TETHER_S1_REPRICE": "1b's S1 re-priced on read (the reviewer 2026-10-29 r346, r347, r349, "
                         "r350). Under TETHER_ASK, a cell under the current bar charged on fewer "
                         "residual rows than its gap now holds (its own c[0] against the list, "
                         "which only extends under the tally key) is charged on exactly the rows "
                         "it missed, by the bound's one row test (_row_wrong, which _cannot_pay "
                         "calls), before it counts as a survivor; a moved key or a shrunk list "
                         "cannot judge (no ask). Eligibility is read on the stored S1 (an upper "
                         "set) and re-priced lazily in rank order; a gap under two is skipped "
                         "with its count, and none left writes PLAN 'ask_none' on '@ask'. The "
                         "charges are kept per cell across cycles (same cell, list length, key, "
                         "decoder size). The reason: r346 found 8 of 13 asks reading a stale "
                         "record, and re-pricing cuts gridworld's stored survivors 45,384 -> "
                         "0/38 and 70,620 -> 37 at 5.17 s max, 0.51 s median per ask (24 steps). "
                         "OFF restores the stale-S1 asks, byte-equal to 20cc52a: a measuring "
                         "setting, not a safe one. default ON",
    "TETHER_DIVIDE_CREDIT": "1a CREDIT (the reviewer 2026-10-29 r312 ask 3; Fig 12 :108, Fig 6 "
                            ":50). Under TETHER_DIVIDE, a closure chain the gap's kind had met "
                            "before, re-met with no row evaluated and no term reaching the "
                            "bargain, is a lookup: its yield is credited back (st['credit'], which "
                            "gamma.enumerate_closure subtracts from what it has emitted), so the "
                            "same cfg.budget reaches chains never met. The divide row carries "
                            "'credited'. Its cost is wall time, read apart from DIVIDE's. OFF: no "
                            "credit is written and the closure counts as before. default OFF since "
                            "(a2): the credit refunds the yield count but not the work, so a "
                            "credited walk runs the whole space (r344's ledger read: credited = "
                            "candidates_seen = 62,585 on a PLAY19 round-1 walk); Isaiah 2026-10-29 "
                            "15:50 'you can switch off credit' (r355). ON is a measuring setting",
    "TETHER_DIVIDE": "1a DIVIDE, A CARRIED SPACE PER OPEN GAP (the reviewer 2026-10-29 r279, r308, "
                     "r311, r312; Fig 9 :38-41, Fig 6 :50, Fig 12 :108). The mint's row tally "
                     "(_cannot_pay) is keyed by Agent._divide_key -- held, alphabet, epoch, the "
                     "break window, the D5 row filter, len(_invented), the slot's peers, its "
                     "owner's attribute map -- in place of the cycle, so it lives for the gap's "
                     "life; an OBJ term's cell keeps its cycle (the objective domain draws per "
                     "cycle). 1b (r313-r315): the shape table reaches evaluation as a counting "
                     "Mapping (_DecoderView), and a cell whose rows read its EXTENT (a miss, a "
                     "reverse search, len) carries the table's size and is recomputed once the "
                     "table grows; every other cell survives growth. A term the record still "
                     "refuses takes no rank. "
                     "Chain costs are kept per gap kind (retrieval's described gap) under "
                     "(code_ver, units). Rows: MINT 'divide' per searching mint (m1 = carried / "
                     "priced_now) and 'space_closed' (cause by key part, kind, epoch, end). "
                     "In-run only, never saved. OFF: the cycle key and every row as before. "
                     "default ON",
    "TETHER_STEP_MINT": "B1, WHOLE MINTS PER STEP (the reviewer 2026-10-26 14:20, (b'); Fig 12 "
                        ":127 'the budget is what decides how much of the space is reached', "
                        "read as the mint's own stop; Fig 6 :49-50 distribute the search across "
                        "steps; Fig 9 :60 owed, never a verdict): a mint runs as before, with all "
                        "its bounds. Once one mint this step parks with its search stopped at a "
                        "bound (budget_exhausted), the step's remaining MECHANISM / REFUTED mints "
                        "are OWED: an ACCEPT row mint_deferred (owed_import), minted first next "
                        "step. A mint ending under its bounds does not end the step's minting. "
                        "Per step the ACCEPT row step_mint: mints_run, mints_deferred, stop. No "
                        "constant: the unit is the mint's own stop. The derived-want and D5 mints "
                        "are not touched. OFF: every mint runs in its step, as before. default ON",
    "TETHER_WALK_BUDGET": "A2, THE STEP BUDGET INSIDE THE WALK (Isaiah 2026-10-26 11:25 'still "
                          "sounds like that think act fix isnt in place yet'; the reviewer 11:33; "
                          "Fig 9 :40-41 'keep every cut ranked and reversible'): "
                          "Agent._index_reach applies K1's guard to EVERY key -- once the step's "
                          "evaluations reach "
                          "STEP_BUDGET (its value unchanged, the declared convention) the walk "
                          "stops at an entry boundary, never inside an entry, after a memo-walked "
                          "entry's charge has landed. The lit list is ranked, so the strongest "
                          "entries are walked first; the truncated index is not memoised; "
                          "Agent._library_fit owes the slot (C1's queue, asked first next step) "
                          "and writes the ROUTE row walk_cut with the entries unreached -- "
                          "'unreached at this budget', never absent. OFF: only K1's late entries "
                          "are cut, "
                          "and one lookup's walk runs to its end. default ON",
    "TETHER_BLOB_STAMP": "(i-e) EOL-independent stamps (the reviewer 2026-10-14 10:19, 2026-10-15 "
                         "18:45): the run header adds files_blob (the .py files on disk minus "
                         "an exclusion table of directory names) and library_blob, each over "
                         "git blob ids with CRLF read as LF; new names, so never compared with "
                         "files_sha/library_sha, which are kept. Nothing reads them to decide. "
                         "OFF writes the header as before. default ON (Isaiah 2026-10-15 07:53, "
                         "17:26); the switch is kept for the checklist's culprit isolation",
    "TETHER_SETTLED_CORE": "7i, the settled core (Isaiah 2026-10-14 07:08, 07:14; the reviewer "
                           "2026-10-15 19:04): INNATE -- every PRIOR one-atom term and a mint "
                           "that is the library's one-atom description -- is never demoted, a "
                           "contradiction recorded; LEARNED -- a library recipe taken whole -- "
                           "starts settled and is revisable; a carried term keeps its standing "
                           "(lineage replays the evidence). OFF is the line before it exactly. "
                           "default ON (Isaiah 2026-10-15 07:53, 17:26); the switch is kept for "
                           "the checklist's culprit isolation",
    "TETHER_7H_TRIED": "7h (the reviewer 2026-10-15 17:32, 19:59): site 8's least-known reads the "
                       "tries per (level, slot, operand) this level, fewer first, before the draw. "
                       "OFF is the line before it exactly. "
                       "default ON (Isaiah 2026-10-15 07:53, 17:26); "
                        "the switch is kept for the checklist's culprit isolation",
    "TETHER_7H_SHOWN": "7h: site 9's least-known reads how often each value was shown before "
                       "this frame (at least 1 for a value shown). "
                       "OFF is the line before it exactly. "
                       "default ON (Isaiah 2026-10-15 07:53, 17:26); "
                        "the switch is kept for the checklist's culprit isolation",
    "TETHER_7H_ROOT": "7h: one intent_root row per live situation (what is shown, what is "
                      "expected, what is open and owed; no button, coordinate or game name), "
                      "every choice row carrying its id, an intent_verdict row at the next "
                      "boundary with the ground's ending; a record read by no chooser. "
                      "OFF is the line before it exactly. "
                      "default ON (Isaiah 2026-10-15 07:53, 17:26); "
                        "the switch is kept for the checklist's culprit isolation",
    "TETHER_7J_TEST": "7j (the reviewer 2026-10-15 17:32, 20:27): the goal exit's choice gets "
                      "one hypothesis_test row pairing the objective term's prediction with "
                      "what the ground showed (ordered or categorical by the slot's type), "
                      "linked to the 7h root; read by no chooser. "
                      "OFF is the line before it exactly. "
                      "default ON (Isaiah 2026-10-15 07:53, 17:26); "
                      "the switch is kept for the checklist's culprit isolation",
    "TETHER_7K_LEARN": "7k: ELICIT's fresh pick reads the unknowns each action reaches "
                       "(more first) and its presses everywhere (fewer first) before the "
                       "draw. "
                       "OFF is the line before it exactly. "
                       "default ON (Isaiah 2026-10-15 07:53, 17:26); "
                       "the switch is kept for the checklist's culprit isolation",
    "TETHER_7L_KIND": "7l (the reviewer 2026-10-15 17:32, 20:41): the library questions asked "
                      "by kind (the sorted attribute types of an owner's slots) and one "
                      "episode per ask (outcome, salience = outstanding surprise), written "
                      "through the lineage; read by no chooser. "
                      "OFF is the line before it exactly. "
                      "default ON (Isaiah 2026-10-15 07:53, 17:26); "
                      "the switch is kept for the checklist's culprit isolation",
    "TETHER_3C_CANON": "3c-CANON (the reviewer 2026-10-16 14:49; Isaiah 16:21, 16:41): the ARC "
                       "world publishes shape_code(owner), a stable hash of the object's "
                       "normalised cells (the same form, the same code, on any board), and "
                       "_kind adds it, so 7l, 7m, 7h (h) and (a)/(b) read form, not an "
                       "encounter index. Worlds without it (gridworld, the toy) keep the type "
                       "kind. OFF: the type kind everywhere. default ON",
    "TETHER_RESET_KNOWN": "D-WIN-RESET (the reviewer 2026-10-16 19:01 Q4): on a live board RESET "
                          "is a known effect (it restarts the level), never an unknown to "
                          "elicit: it leaves the never-taken and effect-unknown bands of "
                          "ELICIT/DISTINGUISH and stays among the priced known effects; a dead "
                          "board keeps it everywhere. OFF: RESET elicited as never taken. "
                          "default ON",
    "TETHER_7H_LEARNED_ORDER": "U1 (the reviewer 2026-10-16 19:01 Q2): A1's learning reading "
                               "gains a third key, left minus paid over the slot kind's "
                               "lines (lineage and own), lower first, after the slot count "
                               "and the carried kind count; never in the bits. OFF: two "
                               "keys, as before. default ON",
    "TETHER_7H_RECURSE": "7h RECURSE-PARTS (Isaiah 2026-10-14 06:23; Fig 9 :54): at 7f's leave, "
                         "a union where "
                         "a held predicate splits into lawful parts is searched part by part by "
                         "the same mint and the terms held as D5 parts; the line is not left. "
                         "OFF: the leave records the union and leaves, as before. default ON",
    "TETHER_7H_ROUTE_GRADE": "7h (d) by route: a line that paid also counts paid_by_<route> "
                             "(invention, carried, library, mint, fell) under its kind, carried "
                             "with the grades. OFF: paid/left only. default ON",
    "TETHER_SPEED2_BOUND": "SPEED-2 (3d census; the reviewer 2026-10-16 19:01 Q10): the mint "
                           "prefix tally is generational per slot -- this walk's entries and "
                           "the previous walk's are kept, older ones dropped; a cache that "
                           "stays, bounded by the mint's own walk, every price unchanged. OFF: "
                           "the tally grows until the slot's triple moves. default ON",
    "TETHER_REACH_EXACT": "E1 X1 (the 10-17 crash audit; the reviewer 2026-10-17 06:38): the "
                          "library route's CAUSE verdict is a fold over the frames, so a step "
                          "reads only the frames not yet read, one entry per pair; restarted "
                          "from frame 0 whenever the frames' inputs change. Every verdict "
                          "unchanged. OFF: every cause re-tested from frame 0 each step, one "
                          "entry kept per trace length. default ON",
    "TETHER_BIND_ONCE": "E1 BIND ONCE (the reviewer 2026-10-17 08:57: exact, the seat's): a "
                        "held compile's Term is rebuilt under the question's names once per "
                        "(held Term, o, x) and shared by every row holding it, kept with the "
                        "bound memos. Every row equal to the rebuild. OFF: rebuilt per row "
                        "(5987421). default ON",
    "TETHER_OWN_CLOCK": "E1 OWN CLOCK (the reviewer 2026-10-17 10:05; Fig 5 :12; the "
                        "reafference principle): age and stability, which the agent's own "
                        "perception writes by its own rule, are predicted by that rule when "
                        "the frames arrive (env.own_expected: age prev + F, stability prev + F "
                        "if the settled cells and colour are unchanged else 0, F the tracker "
                        "advances read); maker none, so no term is credited or blamed; bet "
                        "rows say own_clock. OFF: bet on as no_change (6f37e8e). default ON",
    "TETHER_CLOCK_DESC": "E1 1 (the reviewer 2026-10-17 10:47; Fig 9 :29-30): an own-clock "
                         "slot whose own residual is 0 this step is left out of the "
                         "residual's description (what varied with it); a nonzero own "
                         "residual stays in. NOT exact: it changes what the library "
                         "lights. OFF: every varied slot described (5217b8d). default ON",
    "TETHER_ENTRY_USE": "E1 1b (the reviewer 2026-10-17 10:47): per library entry, times "
                        "lit, offered, refused and explained, and the last (generation, "
                        "cycle) it explained a residual; carried by the lineage per "
                        "generation. Record only, no consumer. OFF: not kept. default ON",
    "TETHER_CAP_MIDSTEP": "THE CAP ENDS A STEP BETWEEN LOOKUPS (the reviewer 2026-10-17 "
                          "10:47, 11:35): the runner sets Agent.deadline (its wall "
                          "allowance, never a prior); before each library lookup a passed "
                          "deadline stops the step there with one @cap cap_mid_step row, so "
                          "the runner's own end path flushes the record and the lineage. "
                          "OFF: the step runs to its end whatever the clock (e77a982). "
                          "default ON",
    "TETHER_STEP_BUDGET": "C1 (the reviewer 2026-10-17 14:12, 15:36): each step spends at most "
                          "STEP_BUDGET evaluations (50,000 since Isaiah 10-21 18:58; "
                          "TETHER_STEP_BUDGET_N; an entry x role x pairing call or "
                          "a row it yields), checked between lookups as the cap is; a lookup "
                          "not run is recorded (budget_owed) under its question's id and its "
                          "slot owes, asked first next step; one @budget row per step with the "
                          "owed queue. OFF: no bound (3a8238c). default ON",
    "TETHER_MEMO_CLEAR": "R4 (the reviewer 2026-10-17 17:35 C, split 2026-10-18 00:10): the "
                         "agent-level instance memos (_reach_index, _reach_verdicts, _reach_fold, "
                         "_compile_cache, _units_for_memo, _frontiers) are cleared at every "
                         "boundary, after one @memo row of sizes and the bound memos' hit "
                         "counter; their keys hold this board's names; Isaiah's carried bound "
                         "memos are exempt (10-15 06:01). OFF: never cleared (e945a7f). "
                         "default ON",
    "TETHER_MEMO_AT_BREAK": "P3 (the reviewer 2026-10-25 13:11): the same seven instance memos "
                            "(with _walk_memo) are also cleared at the agent's own frame break, "
                            "after a memo_sizes row (at frame_break, step PERCEIVE), since a break "
                            "re-issues the names their keys hold; nothing else of the sweep. The "
                            "walk memo grew 1.18M -> 1.73M entries over rounds 2-4 in 0-level "
                            "streams. A miss recomputes. OFF: cleared at retarget only. default ON",
    "TETHER_MEMO_ADMIT": "R4 (the reviewer 2026-10-17 23:52 (A), split 2026-10-18 00:10): the "
                         "agent-level memos store an answer only on its key's SECOND ask; the "
                         "asked keys are kept. OFF because RK-3 fired: it saved 17 entries on "
                         "the fake (640 vs 657) and 6 on gridworld, and cost recomputation the "
                         "budget pays for (late_asked 364 vs 0); revisit only if lf52's byte "
                         "attribution shows these memos large. OFF: stored on the first ask "
                         "(e945a7f). default OFF",
    "TETHER_CONSOLIDATE": "CONSOLIDATION (Isaiah 2026-10-18 04:10, 04:20, 04:26; the reviewer "
                          "04:21, 04:43, 04:55): at a level end, the agent's restart, a game's "
                          "start, and when commit reaches half the supervisor's ceiling "
                          "(hysteresis: not again until commit exceeds its value then), the six "
                          "instance-keyed bound stores and the agent's twins are counted and "
                          "cleared, one @consolidate row each; nothing is re-added (7l and K1 "
                          "learn at landing), ak_ and the episodes untouched. The 7l kind store "
                          "counts its landings (n_landed, summed at load; a set-form generation "
                          "counts 1) and keeps last_seen on 7l and K1 keys; T1 / T1d / T2 and "
                          "7m order by n_landed then last_seen (orders, never excludes). OFF: "
                          "the bound stores outlive every boundary, the 7l store is a set "
                          "(e79ac10). default ON",
    "TETHER_G1_WANT": "G1 (the reviewer 2026-10-17 15:30, 23:04, 23:17): per event, one "
                      "objective-only question over the derived slots it changed; the want is "
                      "the library condition the change made true, closed with all; bare "
                      "quantifiers refused; one want per event, never bound or bet; origin and "
                      "outcome recorded to the boundary. OFF: no such want (f631977). default ON",
    "TETHER_DERIVED_WANT": "E0-W (the reviewer 2026-10-18 11:03): a declared-derived slot that "
                           "moved and wants nothing is minted for the objective only; the want "
                           "is written, the slot never bound, bet or charged (E0 stands for "
                           "pricing). OFF: no such want (433e689). default ON. (DS 2026-10-20: "
                           "'never bound' held only under TETHER_DERIVED_SUBJECT -- before it a "
                           "want-only park invented and bound)",
    "TETHER_DERIVED_SUBJECT": "DS (the reviewer 2026-10-20 08:36, 09:02, 09:06 alpha): a declared-"
                              "derived slot is no subject -- no term bound to it at any bind site, "
                              "an echo (a source missed) not searched (its want by G1's no-search "
                              "rule), a new relational gap recorded as derived_new and never "
                              "binned, a want-only park neither owes nor invents. OFF: as at "
                              "59cd5b9. default ON",
    "TETHER_COMPRESS": "COMPRESSION L1 + L6a + L2 (the reviewer 2026-10-20 11:06, 11:13): "
                       "save files written zlib-6 under the hash of their uncompressed bytes (one "
                       "reader, lineage_store.file_bytes, reads both); the asked record in form 3 "
                       "(a tally per (key, role, slot class) + the whole pairs, all its readers "
                       "read); the in-game asked counter folded at ask. OFF: raw files, form 2. "
                       "default ON",
    "TETHER_CUE_NORM": "DS (5) (the reviewer 2026-10-20 08:36): the library lookup reads a pair "
                       "reading (dcol_o1) as its base when the base is a known reading, by the "
                       "one cue_attr G1-S uses. OFF: the attribute as named (59cd5b9). default ON",
    "TETHER_ALPHA_LAST": "ALPHA-LAST (the reviewer 2026-10-18 19:47): a slot that left the slot "
                         "set keeps the alphabet it last had, so sweep can price a departed parked "
                         "slot; a present slot reads as before. OFF: the departed read raises "
                         "KeyError (38b2daa). default ON",
    "TETHER_ALPHA_PRICE": "ALPHA-PRICE, F2 (the reviewer 2026-10-20 13:38): a bet's prediction "
                          "is coded under the alphabet pricing uses (re-read after the "
                          "observation), so a correct prediction of a never-seen value costs 0 "
                          "bits. OFF: coded under the bet-time alphabet; it wraps and is charged "
                          "a full miss (d5c1b12). default ON",
    "TETHER_ARRIVAL": "GQ3, ONE ARRIVAL PREDICATE (the reviewer 2026-10-20 14:27; Isaiah 14:11): "
                      "every reader of a goal series asks arrival() -- one zero is TOUCHED "
                      "(held, re-read; a routine guard HOLDs one step), MIN_REPEAT zeros "
                      "CONFIRMED; can() loses 'any zero ever'. OFF: each reader's own rule (the "
                      "selector two zeros, the gate / guard / rows one; 181ddd2). default ON",
    "TETHER_LEVEL_GOAL": "GQ1, A LEVEL CLEAR COUNTS (the reviewer 2026-10-20 14:27; Isaiah "
                         "14:11): the completion sweep fires on the step that RAISED the world's "
                         "degree (any level clear; on ARC degree = levels / win, so 1.0 was the "
                         "whole game), candidates from the clearing step's after AND before "
                         "states, held conditions SHELVED at ADVANCE / WIN with (game, level) and "
                         "carried as a template through M7-INV, goal atoms numbered for the life. "
                         "OFF: degree >= 1.0 > prev, closed with the level (7091be4). default ON",
    "TETHER_GOAL_HYPOTHESES": "GQ2, GOAL HYPOTHESES (the reviewer 2026-10-20 14:27; Isaiah "
                              "14:11): with no objective held, the library's own condition "
                              "grammar over THIS board and the shelf's templates propose goals, "
                              "each a subject-scoped want on a movable slot with a route in the "
                              "agent's delta table (CAN), ranked (shelf win, term_bits; A1 ties), "
                              "pursued through the selector -> routine path, ended on arrival "
                              "without a clear or a stall; the next differs; then a pair; then "
                              "System 0. OFF: no proposal (86c7998). default ON",
    "TETHER_GROUP_MEMBER": "GQ2b, F-a + F-b (the reviewer 2026-10-20 14:27 (b)): a group-scoped "
                           "objective is judged member by member, each in its own context (its "
                           "peers, its record), the subject included, so the residual is a real "
                           "fraction that moves when one member moves; the goal sites read "
                           "shapes (cached per cycle). OFF: each peer judged with the subject's "
                           "context (aligned / any_same / none_same constant), shapes off "
                           "(8ef01f2). default ON",
    "TETHER_HYP_DRAW": "S0 (the reviewer 2026-10-20 18:18): at the goal-hypothesis site only, "
                       "an exact tie's draw is one hash per candidate (frontier.draw_order) "
                       "and routes are checked in that order, stopping at the first "
                       "routable -- the same pick as checking all under that draw; the "
                       "proposal row carries its wall time and its checks. OFF: every tied "
                       "member route-checked, the draw a hash of the routable pool "
                       "(6fe24e2). default ON",
    "TETHER_FIT_TIER0": "S2a (the reviewer 2026-10-20 19:54): route's Tier 0 -- an owed slot whose "
                        "bet held is not re-fitted while the key of its last full _library_fit "
                        "that found none stands (bound term, exclude, alphabet, type, library and "
                        "units, refusals, carry, level, epoch, row filter); a budget-capped fit is "
                        "never stored; a missed bet reopens it. OFF: re-fitted every step "
                        "(e8a5454). default ON",
    "TETHER_FIT_TIER0_CHECK": "S2a's check run (must-fail (b)): each Tier-0 skip also runs the "
                              "full fit, records whether it agreed (None, the library unmoved) "
                              "and uses the full fit. A measurement switch for check runs, never "
                              "a play setting. default OFF",
    "TETHER_WALK_MEMO": "(A) (the reviewer 2026-10-20 21:18, 21:28): _index_reach keeps each lit "
                        "entry's walk keyed by what it reads (library, atoms token, compile "
                        "signature -- the held index is a pure function of it --, entry, slot, "
                        "mine, partner, others, targets); a hit merges the record as the walk "
                        "would, charges _spent the same count, lands its kinds under this step's "
                        "dk and replays its asks; _index_for's whole-walk store retires. OFF: "
                        "walked every time (6fbdd5f). default ON",
    "TETHER_WALK_MEMO_CHECK": "(A)'s check run: each hit is also walked fresh and compared "
                              "(views, causes, refusals, charges, landings, asks); the fresh "
                              "walk is used. A measurement switch for check runs, never a play "
                              "setting. default OFF",
    "TETHER_TIERS_DRAW": "THE _tiers NAME TIE (the reviewer 2026-10-20 23:55 (ii), 2026-10-21 "
                         "03:05; "
                         "Isaiah's 10-15 A1 rule): a tie on _tiers' numbers falls to the recorded "
                         "draw (frontier.draw_key, keyed per lookup), never the entry's name, at "
                         "T1a-c, T2, T1d and T5. OFF: the name (03b793e). default ON",
    "TETHER_TIERS_INDEX": "(C), THE TIERS INDEX (the reviewer 2026-10-21 03:05): _tiers reads its "
                          "rung sums from per-kind and per-type entry counts kept at the stores' "
                          "writers (a landing, a recency write; a lineage load rebuilds), not by "
                          "scanning every carried row per call. OFF: the scan (78520a8). "
                          "default ON",
    "TETHER_TIERS_INDEX_CHECK": "(C)'s check run: every call also scans and compares the rung sums "
                                "and the recency map; the scan's are used. A measurement switch "
                                "for check runs, never a play setting. default OFF",
    "TETHER_FIT_UNITS": "(B), THE UNITS ONCE PER FIT (the S2I box; the reviewer 2026-10-21 02:02): "
                        "_library_fit takes the slot's units at the first candidate that needs "
                        "them and reuses them for the fit (nothing in the loop writes their "
                        "inputs). OFF: _units_for per candidate (35c283a). default ON",
    "TETHER_FIT_UNITS_CHECK": "(B)'s check run: every reuse also takes _units_for fresh and "
                              "compares; the fresh units are used. A measurement switch for "
                              "check runs, never a play setting. default OFF",
    "TETHER_STORE_KEY_MEMO": "W1 (S2V; the reviewer 2026-10-21 15:38): lineage_store._merge_kinds "
                             "keeps each kind value's JSON string for one merge, keyed on its "
                             "repr (1, True and 1.0 encode apart); other types encoded fresh. "
                             "OFF: json.dumps per row (23a9077). default ON",
    "TETHER_STORE_KEY_MEMO_CHECK": "W1's check run: every reuse also encodes fresh and "
                                   "compares; the fresh string is used. A measurement "
                                   "switch. default OFF",
    "TETHER_LOAD_KEY_MEMO": "W2 (S2V; the reviewer 2026-10-21 15:38): the store load decodes each "
                            "kind sym id once per load, reusing the tuple when hashable. OFF: "
                            "json.loads per row (23a9077). default ON",
    "TETHER_LOAD_KEY_MEMO_CHECK": "W2's check run: every reuse also decodes fresh and "
                                  "compares; the fresh tuple is used. A measurement "
                                  "switch. default OFF",
    "TETHER_BUDGET_GENERATED": "Q3, THE WORK BUDGET CHARGES WORK DONE (Isaiah 2026-10-21 "
                               "18:58; the reviewer 19:02 (B)): a chain bounded out on cost "
                               "generates no instance and is not charged to work_budget. A "
                               "reach change; the default is set by the measurement. OFF: "
                               "charged, as before (7d5fcf9). C-HELD-5, the reviewer 2026-10-26 "
                               "05:13: default ON (Isaiah agreed 10-21; his 04:51 order makes the "
                               "25-game rounds the measurement; back OFF if wall rises with no "
                               "reach gain)",
    "TETHER_LIBRARY_EXPLAINS": "(iv), RECOGNITION EXPLAINS (the reviewer 2026-10-21 21:52, "
                               "2026-10-22 01:55): a library-served term (route REBIND or "
                               "compete) that makes the slot's bet and settles credits "
                               "explain() as a mint's winner does. OFF: a served slot keeps its "
                               "whole past surprise as outstanding (116481a). ON by Isaiah "
                               "2026-10-22 03:50 / 04:01. default ON",
    "TETHER_OWN_COUNTERS_DERIVED": "STABILITY / AGE, THE NARROW ARM (B) (the reviewer "
                                   "2026-10-21 21:52, 2026-10-22 02:13): the slots the world's own "
                                   "clock writes (env.own_counted()) are never minted for or "
                                   "bound and their misses are not charged; still bet by the own "
                                   "clock and recorded. OFF: as at 116481a. ON by Isaiah "
                                   "2026-10-22 03:50 / 04:01. default ON",
    "TETHER_W_BUDGET": "W-1, THE BUDGET (Isaiah 2026-10-19 03:38 / 03:47; the reviewer "
                       "2026-10-22 05:14): B = min(8 GiB, half the RAM or the container's "
                       "limit), in the @run header; a fold at 0.75 B (a step's start) and "
                       "0.90 B (a between-lookup point) when commit is above its last fold's. "
                       "OFF: the size trigger at half SUP_CEILING, as before. default ON",
    "TETHER_W_CACHES": "W-2, THE CACHES (E) (the reviewer 2026-10-22 05:14): six memos whose "
                       "miss writes no ledger row and moves no decision state are evicted at a "
                       "W-1 fold (soft: the entries not read since the last fold; hard: all) "
                       "and recomputed at their next miss; the counts go to @body. OFF: they "
                       "grow for the life of the agent or the process. default ON",
    "TETHER_W_SOFT_READS": "M2 (the reviewer 2026-10-23 09:18, 09:25): a write to a W-2 cache no "
                           "longer marks the entry seen, so a SOFT fold drops the entries not READ "
                           "since the last fold (used once); the first SOFT fold was inert by "
                           "construction (E4b: three SOFT folds, 0 evicted). W-2-exact: a dropped "
                           "entry is recomputed at its next miss. OFF: a write marks seen, as "
                           "before. default ON",
    "TETHER_CHOICE_TALLY": "THE CHOICE TALLY (Isaiah 2026-10-23 09:12 \"these should be deduped "
                           "and tallied\"; the reviewer 10:40, 10:52, 11:06): an objective_domain "
                           "choice row whose every decision field repeats an earlier row is not "
                           "appended; at the step's end (and at end_run) one choice_tally row per "
                           "repeated key carries ref, n, first and last cycle (E4b: 636,386 rows, "
                           "3,001 keys). `written` counts every record() call and since_written "
                           "returns both in call order, so the fit's dedup capture and replay are "
                           "unchanged. OFF: every row appended, as before. default ON",
    "TETHER_CHOICE_TALLY_CHECK": "the tally's check: every row's FULL detail is kept per key, and "
                                 "the flush asserts one full key per tally key with an equal "
                                 "count (two rows that differ in any field were never merged). "
                                 "Costs a set per key; for tests. default OFF",
    "TETHER_CHOICE_TALLY_ORDER": "the tally's order guard (the reviewer 2026-10-23 11:21, 11:25, "
                                 "11:32): a repeat is tallied only if the latest row appended in "
                                 "its (cycle, slot) carries the same step, its detail has no field "
                                 "outside the key, and its mode equals its first row's; otherwise "
                                 "it is appended in full, so no check gate.py makes on the file "
                                 "can change (gate._steps compares each row with the previous row "
                                 "of its (cycle, slot)). OFF: the tally ignores order (c2ddc5a), "
                                 "for MF-ORDER. default ON",
    "TETHER_FRAME_BREAK": "B, THE FRAME BREAK (the reviewer 2026-10-23 12:35, 13:04; design posted "
                          "13:00): on a decomposition whose board differs from the previous "
                          "call's (arc_world.py:279 or :198), the tracker reads its claims with "
                          "two instruments and calls a break iff the median claim score < 0.71 "
                          "AND the colour-changed share > 0.42 (arc_percept.BREAK_MEDIAN / "
                          "BREAK_COLOUR, DECLARED CONVENTIONS at the midpoint of the measured "
                          "gap: switches median <= 0.4844, colour >= 0.70; insides median >= "
                          "0.9273, colour <= 0.143; panel 7 switches, 5 games' insides, no level "
                          "boundary seen, one toggle game; moved only by ruling). 0 claims: no "
                          "test, recorded. On a break every non-exact claim (exact = score 1.0, "
                          "same colour, same cells) is issued as a birth; a frame_break row is "
                          "recorded; and the step whose outcome broke is a SEAM: every bet "
                          "suspended (seam), no audit, surprise, reward route, contingency, "
                          "progress or goal-choice note, no step-local mint, and no trace row "
                          "appended (the reviewer 13:12). The matches row reports every "
                          "board-changed call. OFF: today's tracker and record. default ON",
    "TETHER_BREAK_WINDOW": "C, THE BREAK WINDOW (the reviewer 2026-10-23 13:04, 13:12, 13:43): "
                           "after a frame break (TETHER_FRAME_BREAK), history(slot) -- what the "
                           "fits read -- starts at the trace row after the break "
                           "(Agent._window_at, set in perceive; reset to 0 with the trace at a "
                           "level boundary), so no slot's fit reads across a world swap (Fig 12 "
                           ":109). The library, standings and atoms are untouched (Fig 4 "
                           ":22-23). Other whole-trace readers are listed in C's build post with "
                           "a decision each. OFF: history to the level's start. default ON",
    "TETHER_R4_RECORD": "THE R4 RECORD (the reviewer 2026-10-23 18:19, 18:28, 18:37, 18:43, "
                        "19:39): record-only rows and fields making F1-F5 readable -- the "
                        "per-press audit row (credited count, own_clock slots credited), REPEAT's "
                        "offered / withheld / realised (the pick's table evidence), the clock "
                        "verdict per subject on goal_hypotheses, [gap, span] beside goal_series, "
                        "a hypothesis's test outcomes on its end row. Read by nothing that "
                        "decides; the ON/OFF must-fail shows identical decisions. OFF: today's "
                        "ledger. default ON",
    "TETHER_ROUTE_REFUSE": "R-A + R-B, PROGRESS AND THE ROUTE (WATSON, Isaiah 2026-10-23 19:21 "
                           "\"Approved\"; the build design accepted by the reviewer 22:12). R-A: "
                           "the trend readers (shrinking via trend_of, the selector and its rank, "
                           "goal_series qualifies, _hyp_check's stuck) read the raw gap where the "
                           "window carries one; R_goal's value unchanged. The selector ranks by "
                           "the share of the window's opening reading closed, today's shrink the "
                           "tie-break. R-B: a route (intent, action, coord, contact context) at "
                           "the goal exit is refused after MIN_REPEAT non-closing outcomes or one "
                           "farther (route_refused row), kept for the level (retarget clears it, "
                           "on a level edge and on a death), withheld from that intent in that "
                           "context; none left: route_exhausted, a held hypothesis ends "
                           "by=routes. Known limits: delayed effects (R-E) can be refused early; "
                           "no carry across a death (R-D, open). R-C (the reviewer 2026-10-24 "
                           "09:30, 09:37): a general intent's right-way move is reached; a "
                           "specific one's (interface.Specific) overshoot is corrected toward "
                           "its target (route_corrected / route_uncorrected), never refused, "
                           "and refused after MIN_REPEAT non-shrinking overshoots. OFF: today's "
                           "trend and goal exit. default ON (Isaiah 2026-10-24 14:16: 'just "
                           "keep the switch on period')",
    "TETHER_W_DK_KEYED": "W-4, THE DK KIND STORE KEYED (the reviewer 2026-10-22 05:14 (c), "
                         "05:52): the life's kind_dk stays on disk, read through a snapshot "
                         "held from load (one read transaction, lineage.DkSnapshot) -- each "
                         "asked kind's rows at its first ask, the per-type sums and latest "
                         "seqs from its aggregates; closed before the game's checkpoint. OFF: "
                         "every carried dk key and its last seq in RAM from load. default ON",
    "TETHER_CAP_INNER": "C1 (A), THE OVERRUN SAFETY NET (Isaiah 2026-10-22 12:36-12:37; the "
                        "reviewer 15:17, 15:34, 15:40): cap.head() at every growing loop on the "
                        "step path (278, tether.py and 12 modules), raising cap.CapReached (a "
                        "BaseException) once the thinking deadline passes; one catch in step; "
                        "no step after a cut; the end-path-read units held whole. OFF: the "
                        "heads inert, only _cap_due's four points cut. default ON",
    "TETHER_ERROR_CARRY": "ITEM 4, THE LEARNING WRITTEN ON AN AGENT FAULT (the design post "
                          "2026-10-22 15:14; the reviewer 15:17 (C3)): play's catch of an "
                          "Exception from ag.step() (a frame in arc_agi/arcengine: re-raised at "
                          "once): an agent_fault row and the traceback file, the end path guarded "
                          "part by part, ending agent_fault, the library replaced only by a save "
                          "that loads back, the generation without the faulted cycle's stamped "
                          "entries and written only if it reads back; then re-raised. OFF: the "
                          "fault leaves play at once and nothing is written. default ON",
    "TETHER_FAULT_RECOVER": "(B), IN-GAME RECOVERY AFTER AN AGENT FAULT (the design post "
                            "2026-10-22 15:13; the reviewer 15:17 (C3), (C4)): "
                            "arc_holdout.step_or_recover, at play's and e4_stream's step: "
                            "after an agent fault (item 4's row and checked save) a fresh "
                            "world on the same wrapper (no RESET) and a fresh agent on the "
                            "same ledger load the checked "
                            "save; only the cycle and the deadline cross; the same fault "
                            "again (type + innermost repo frame; a MemoryError by type) ends "
                            "the game. OFF: the first fault ends the game, as item 4 alone. "
                            "default ON",
    "TETHER_END_RESERVE": "C1 (A)'s END-PATH RESERVE (the reviewer 2026-10-22 14:27, 15:34): "
                          "thinking stops at the deadline less the agent's own latest measured "
                          "end-path wall (stored in the memory store's meta after the game's "
                          "sleep, read at load; a boundary write never lowers it). OFF: no "
                          "reserve, no end_path row or store write. default ON",
    "TETHER_W_HELD_LAZY": "W-3, THE HELD INDEX LAZY (the reviewer 2026-10-22 05:14 a, b, 06:37): "
                          "the store load reads the held keys only; each entry's items from the "
                          "load-time snapshot at its first ask; _INDEX_STORE evictable by W-2 for "
                          "entries with resolve's verdict (re-read without hashing), never this "
                          "life's own compiles. OFF: every held entry decoded at load and kept "
                          "for the process. default ON",
    "TETHER_CAP_HELD": "THE 20 MB CAP, part (ii) (Isaiah 2026-10-25 05:31; the reviewer 05:49, "
                       "06:06): under the store load with W-3, lineage's _CARRIED and _LAZY are "
                       "answered from the held table (the load-time snapshot, else a read-only "
                       "connection) plus this life's own adds, discards and first resolves, "
                       "instead of copied at load (16.4 MB at 33 saves); the same answers. A "
                       "second store load in one process copies the first load's answers back "
                       "into the old sets. OFF: both copied at load. default ON",
    "TETHER_REL_SLOTS_CACHE": "bp35's crowded-board search (Isaiah 2026-10-23; the reviewer "
                              "2026-10-25 06:25, 06:31): ArcWorld.relational_slots keeps its tuple "
                              "while the frame's read and pair read are the same objects (its only "
                              "inputs, never written in place once built); 3 of 3 py-spy dumps of "
                              "bp35's slow (second) step sat in its rebuild. OFF: rebuilt on every "
                              "ask. default ON",
    "TETHER_REL_SLOTS_CHECK": "TETHER_REL_SLOTS_CACHE's CHECK, a measurement switch: rebuilds on "
                              "every ask and asserts the kept tuple equal (REL_SLOTS_N counts). "
                              "default OFF",
    "TETHER_HYP_SLOTSET": "bp35's next hot line (the reviewer 2026-10-25 08:05; 30.9% of the "
                          "record's samples at _hyp_propose_body's slot test): the slot test "
                          "asks one set built at the top of the call instead of scanning the "
                          "slot LIST per candidate; nothing in the call writes self.slots. OFF: "
                          "the list. default ON",
    "TETHER_HYP_SLOTSET_CHECK": "TETHER_HYP_SLOTSET's CHECK, a measurement switch: also asks the "
                                "list on every candidate and asserts equal (HYP_SLOTSET_N counts). "
                                "default OFF",
    "TETHER_HYP_ROUTE_FIRST": "ROUTE FIRST (Isaiah 2026-10-25 09:48 \"audit why its taking so "
                              "long to decide\"; the reviewer 09:54, final plan 10:29 P1; Fig 9 "
                              ":60): a goal-hypothesis text is dropped before it is compiled when "
                              "it has no call, every slot it names is live and no change reading, "
                              "and none has a route source (an action-table entry of its own, or "
                              "K3's kind entry); a hold needs a route on a slot the text names. "
                              "Exact: the pick is unchanged. OFF: every text. default ON",
    "TETHER_HYP_ROUTE_FIRST_CHECK": "TETHER_HYP_ROUTE_FIRST's CHECK, a measurement switch: keeps "
                                    "every text and asserts no text the filter would drop ever "
                                    "holds (HYP_ROUTE_FIRST_N counts). default OFF",
    "TETHER_KIND_CARRY": "LEARNING FILED BY KIND, NOT BY NAME TAG (Isaiah 2026-10-25 08:02, 08:19 "
                         "\"thats dementia\", 08:40 \"fix\"; the reviewer 08:43). K1 arc_percept: "
                         "at a frame break each retired name's refused claim is published as its "
                         "successor, one-to-one, with both form codes. K2 tether: at the next "
                         "turnover what was held on it (bindings without a gone operand, wants, "
                         "held goals and the open hypothesis, settled slots) moves to a same-kind "
                         "successor (_kind; colour not in it); none: the drop, and the hypothesis "
                         "ends as an absence; a carried row. K3 interface: effects also filed "
                         "under the kind, read only for a slot with no entry of its own, never "
                         "blended. OFF: today's filing. default ON",
    "TETHER_KIND_EFFECTS": "TETHER_KIND_CARRY's K3 alone, a measurement switch: OFF keeps K1 and "
                           "K2 and files no effect by kind, so the aimed check can carry the very "
                           "hypothesis the arm-OFF run picks. default ON",
    "TETHER_KIND_TEST": "(ii) A CARRIED KIND ENTRY IS A TEST, NOT A ROUTE (the reviewer "
                        "2026-10-25 17:26, 17:55, 18:11; Fig 9 :60 \"Never let a filter hand you a "
                        "verdict\"): on a BECOME whose slot has no entry of its own, a kind cell "
                        "(action, kind key) not borne out in this (epoch, breaks) era -- no "
                        "press of THAT action has moved the kind's slot the way the cell's "
                        "prior said, here -- does not route; the best such cell is offered as a "
                        "TEST (Realisation mode kind_test), only when no borne-out cell routes, "
                        "and never RESET (its delta is state-relative, Fig 4 :25). The test is "
                        "graded \"kind test: borne out / not borne out\", not into the "
                        "hypothesis's progress tally; R-B reads the base outcome unchanged. "
                        "Order: cell tier > own delta > a borne-out kind cell > a carried cell, "
                        "as a test only. OFF: today's realise. default ON",
    "TETHER_W_EVICT_EVERY_STEP": "W-2's CHECK, a measurement switch: a hard eviction at every "
                                 "step's start, for MF-W2 (decisions equal to a run that never "
                                 "evicts). default OFF",
    "TETHER_LIBRARY_REQUIRED": "COLD START (ii), SHAPE A (the reviewer 2026-10-21 23:27): "
                               "wire() fails at startup naming each missing library file, or "
                               "the absent library/ folder. OFF only for the ablation clause: "
                               "run without the inheritance (an absent library/ runs with no "
                               "vocabulary and the @run header says absent (ablation)). "
                               "default ON",
    "TETHER_INTERVAL_BOUND": "THE INTERVAL BOUND (S3C; the reviewer 2026-10-21 17:46): an "
                             "objective whose atoms are all declared in gamma.VALUE_TURNS "
                             "(arc_atoms.VALUE_TURNS, one row per atom) is constant between "
                             "its breakpoints, so _priced_hit's unseen walk is answered from "
                             "one evaluation per piece, the nearest ring evaluated as the walk "
                             "does. Undeclared: the walk. OFF: the walk (c0d00a0). default ON",
    "TETHER_INTERVAL_BOUND_CHECK": "the interval bound's check run: the walk beside the bound "
                                   "on every call, the walk's answer used. A measurement "
                                   "switch for check runs, never a play setting. default OFF",
    "TETHER_FIT_DEDUP": "(2a), ONE DEFINITION ONCE PER FIT (the S2L twin; the reviewer "
                        "2026-10-21 04:40): a library Term's candidates and each "
                        "candidate's bindability, leftover and cost are computed once "
                        "per fit; everything read by NAME (exclusion, refusal, carry, "
                        "the first payer, the paying order, the pull) stays per name. "
                        "OFF: per name (920dfc7). default ON",
    "TETHER_FIT_DEDUP_CHECK": "(2a)'s check run: every reuse also computes fresh and "
                              "compares; the fresh values are used. A measurement "
                              "switch for check runs, never a play setting. default OFF",
    "TETHER_CYCLE_SEQ": "ONE SEQ PER CYCLE (the reviewer 2026-10-20 23:33): every landing in a "
                        "(game, level, cycle) carries that cycle's _kind_seq -- equally recent, "
                        "the ground gave them no order -- and _pair_counts' key gains a landing "
                        "counter. OFF: one seq per landing, in set-iteration order (582a223). "
                        "default ON",
    "TETHER_KIND_HOIST": "(D) (the S2E box, 2026-10-20 23:08): inside one _index_reach call the "
                         "slots never change, so the walk memo's landings read each owner's _kind "
                         "once per call. OFF: _kind per landing (a88909d). default ON",
    "TETHER_G1_SUFFIX": "G1-S (the reviewer 2026-10-18 11:19): G1 asks on a pair reading's base "
                        "(dcol for dcol_o1) when the base is a known reading; nothing else is "
                        "equated. OFF: the suffixed name, never known (1e8ccbe). default ON",
    "TETHER_OBJ_EVENT": "E1-E3 (the reviewer 2026-10-17 12:53, 21:48, 21:53): an owner with two "
                        "or more live residual slots in a step is one question -- one lookup over "
                        "its members' united description, each member answered from its own "
                        "bucket and bet / settled on its own -- priced as the joint code over its "
                        "non-derived members (the cell-change group as its largest). OFF: per "
                        "slot (089789e). default ON",
    "TETHER_EVENT_SHARED": "E3 (the reviewer 2026-10-17 21:53), under TETHER_OBJ_EVENT: a chain "
                           "already offered to two or more of an event's unexplained members is "
                           "stated once -- its cost plus each member's binding and leftover -- "
                           "and admitted below the covered members' joint price; guarded chains "
                           "are not priced shared yet. OFF: gate-only. default ON",
    "TETHER_LOOKUP_STREAM": "L (the reviewer 2026-10-19 20:34-20:40; P3: o6.add_n's lookup held "
                            "1,315,061 pairs as lists, +2.1 GB for 50 s): _lookup's pairs in one "
                            "pass in the lists' order (composer.lookup_iter), each READING PAIR's "
                            "bond reading computed once (composer.read_iter's cache, keyed by the "
                            "two readings, the only per-pair inputs read_pairs reads); the record "
                            "and every decision are the same. The dedupe set still grows with the "
                            "pairs, a named limit. OFF: the lists, as before. default ON",
    "TETHER_DELTA_KIND": "K1 (the reviewer 2026-10-17 20:25, 20:28, 20:43): the residual's delta "
                         "kind (cluster, sign, size class) is stored with every landing and every "
                         "offer; the lit list leads with T1a-c (offered before: this kind, any "
                         "object kind, this cluster) and T2 (carried, no delta kind), and T1d "
                         "(landed only) follows T3 under the budget guard; a T1a-c offer defers "
                         "the rest for that ask, a re-ask of the same "
                         "(slot, kind) walks all. An order, never a cut. OFF: 83d67f7. default ON",
    "TETHER_MOLECULES": "K1 (the reviewer 2026-10-17 17:47, 20:25): T4, the molecules "
                        "Library.molecules_lit offers over the entries already listed (its first "
                        "caller), walked only while the step's budget remains; priced by their "
                        "atom expansion (the alphabet does not grow). OFF: 83d67f7. default ON",
    "TETHER_ATTR_INDEX": "K1 (the reviewer 2026-10-17 17:35 A, 17:37): T5, ATTRIBUTE_INDEX's "
                         "by_cluster entries for the described readings' clusters (the declared "
                         "reading -> cluster table), atoms before molecules, walked only while the "
                         "step's budget remains; the corpus file hash-checked, T5 empty and why "
                         "when it is absent or changed. OFF: 83d67f7. default ON",
    "TETHER_REPLAY_UNIT": "R7i (the reviewer 2026-10-17 19:50): 7i's replay applies a carried "
                          "settle / refute row to the term load installed from that row (the "
                          "generation row keeps its old name as was; load records renamed), so "
                          "bound and guarded terms, which reload under another name, are no "
                          "longer not_held; the method crosses, the binding does not. OFF: by "
                          "name (ffb365c). default ON",
    "TETHER_USED_CARRY": "L1b (the reviewer 2026-10-17 19:06, 19:33): Rank.used per unit (by "
                         "atom sequence, never by binding) is written on each generation and "
                         "summed root to tip at load; it lived on the Agent, so it never "
                         "crossed. Paid is not carried here: 7i's replay is its one carrier. "
                         "OFF: nothing written or read (a102c5a). default ON",
    "TETHER_PRIOR_CODE": "L1 (the reviewer 2026-10-17 18:13 (a), 18:40, 18:48): a transition "
                         "term's stating cost is its length under a NORMALIZED code over "
                         "{units, END}, p(s) = (w(s) + 1) / Z, w = Rank.used + Standing.paid of "
                         "the library terms a unit states, END = |atoms| / the library's mean "
                         "recipe length (3.026) + settlements; Kraft sums to 1; no library and "
                         "nothing learned is today's uniform code exactly. The condition code is "
                         "unchanged (no recipe prior: its count read back compile_term's table). "
                         "OFF: term_bits (9f26ee9). default ON",
    "TETHER_LEDGER_HANDLE": "R2 (the reviewer 2026-10-17 17:58, 18:04): the ledger's path is "
                            "opened once, at the first row, and flushed after every row (the "
                            "loss window stays one row); closed at end_run and at exit; a row "
                            "after a close reopens it. OFF: opened and closed per row "
                            "(011c8c8). default ON",
    "TETHER_UNITS_MEMO": "R1 (the reviewer 2026-10-17 17:43, 17:47): gamma.units() is held "
                         "under a key of everything it reads -- the atoms, the settled names "
                         "(scanned from standing), the rank's version (bumped in Rank.note, its "
                         "only writer) -- and _units_for under the units, the slot's refusal key "
                         "and the grow-only refusal scope's lengths; exact by construction. "
                         "OFF: rebuilt each call (ffbdf14). default ON",
    "TETHER_UNITS_VER": "S6 (iv) (the reviewer 2026-10-19 14:56, 15:05): R1's key scanned all of "
                        "standing on every units_held call; now one count is bumped by every "
                        "mutation of the library and standing dicts and by a Standing's settled_at "
                        "flipping None <-> a tick (watched at the containers, so no writer can be "
                        "missed), and the scan runs only after such a write, the held tuple kept "
                        "when the key reads the same; a rebound plain dict falls back to the scan. "
                        "Identical decisions by construction. OFF: the scan every call (753339c). "
                        "default ON",
    "TETHER_INV_FACTOR": "S6 (v) (the reviewer 2026-10-19 15:35, 15:56): an invention's "
                         "(condition, then-term) pairs are priced from each part walked once and "
                         "folded in Code.bits' order, bit-equal to _inv_cost, with left cached per "
                         "(then-term, the condition's truth vector), its whole input; the pick "
                         "(first, A1's ties, the cheapest five) is kept streaming, never the list "
                         "of every pair. Identical decisions and ledger rows; under "
                         "TETHER_PRIOR_CODE only. OFF: priced pair by pair (753339c). default ON",
    "TETHER_INV_CHOICE_PAYS": "(ii-a1) (the reviewer 2026-10-20 03:14, 04:47, 07:46; "
                              "Isaiah 07:45): an invention's A1 tie is chosen only when "
                              "the tied total pays; every tie member shares cost + left, "
                              "so an unpaid tie's pick was discarded and its choice row "
                              "recorded a decision that decided nothing (Fig 13 :126). "
                              "The failed tie is kept as n_tied on the 'none paid' row, "
                              "an aggregate no decision reads (Fig 6 :46). OFF: the "
                              "choice at every tie (5872919). default ON",
    "TETHER_STEP_RANK": "C1b (the reviewer 2026-10-17 17:07, 17:29, 17:30): the step's lookups "
                        "are spent in class order -- owed and changed, changed, our own act's, "
                        "owed and still, the rest -- stable within a class; route hands the "
                        "mints today's order (a mint changes later mints, a lookup no other "
                        "lookup). @budget counts asked / not asked per class. OFF: b7c7a0b's "
                        "order (owed first, then today's). default ON",
    "TETHER_PAIR_NOT_OBJECT": "C1a (the reviewer 2026-10-17 14:24): a library pairing whose "
                              "object name is a pair owner (o0~o1) is refused once, counted "
                              "('a pair owner is not an object name') and never compiled -- "
                              "the grammar has no '~' identifier, so every candidate refused "
                              "at parse (88% of lf52 cycle 2's evaluations; 5.69 M pairings, "
                              "0 rows landed). Pair owners stay cause candidates in the "
                              "ranking. OFF: compiled and refused per candidate (d777217). "
                              "default ON",
    "TETHER_DERIVED_PERCEPT": "E0 (the reviewer 2026-10-17 12:53, 12:59): the percept declares "
                              "what it derives -- h / w / the frame deltas from shape, motion "
                              "from row / col, colour_changed from colour, gridworld proximity "
                              "and distance from positions; pair sources resolved through to "
                              "shape; E0b (14:12) the observer pairs a~b.contact / bbox / "
                              "inside from both parties' row, col, shape -- so they are "
                              "predicted from their sources and carry a "
                              "residual only as B2b relational surprise. OFF: only the pair "
                              "slots are declared (610654c). default ON",
    "TETHER_3A_DIAGNOSE": "E2, 3a DIAGNOSE (Isaiah 2026-10-17 03:37, 04:59; the reviewer PART "
                          "2c, 05:00, 05:01): a contradiction is diagnosed per slot before "
                          "anything is blamed -- noise, recall, own slip, world change or moved, "
                          "the own acts' order, scope or model too small, reading, else "
                          "undiagnosed -- one contradiction_diagnosed row with its next probe; "
                          "the hazard per spot, kind and actor (kind/actor carried by the "
                          "lineage); part 2's 'no visible cause' credited as an unseen actor. "
                          "Acting on the probe is 3a-PROBE. OFF: routed to the reading only "
                          "(7i). default ON",
    "TETHER_REACH_SHARE": "E1 C4 (the reviewer 2026-10-17 08:04): a (pair, slot) of the "
                          "library route reads its held rows from the entry's landing groups "
                          "(grouped once by slot template under the placeholders) and binds "
                          "only those; no pair is promoted to a whole bound for every slot. "
                          "The same rows in the same order. OFF: promote on reuse and scan every "
                          "held row per (pair, slot). default ON",
    "TETHER_REACH_RANK": "E1 part 2 (Isaiah 2026-10-17 06:42; the reviewer 06:49): the route's "
                         "CAUSE candidates ranked and budgeted, never excluded -- the agent's "
                         "own act's target, then the objects that changed (most recent first), "
                         "then the contact cascade ring by ring, then every object no ring "
                         "reached; a kind that already caused this kind of effect first in its "
                         "tier (the record carried by the lineage); one ring per step while "
                         "unexplained, 'no visible cause' when every tier is reached. OFF: every "
                         "other object every step (part 1). default ON",
    "TETHER_M7_INV": "M7-INV (Isaiah 2026-10-15 06:01; the reviewer 2026-10-16 19:01 Q3): an "
                     "invention is carried as its method (template with {o}/{x}, reading, "
                     "affects, then-chain, standing then), named with a content hash; the "
                     "lineage carries the records and the load re-invents them on trial in "
                     "the private library, which the route then reads. OFF: inventions "
                     "private to the game, the route on the shared library. default ON",
    "TETHER_7H_REHEARSE": "7h (e), mental rehearsal (Isaiah 2026-10-14 06:23; the reviewer "
                          "2026-10-16 19:01 Q1): a settled term's prediction is chained one "
                          "more step in thought under the same action; the next step, if it "
                          "repeats the action, grades it on its own channel (rehearsal rows: "
                          "held, links_held, differed = the read slots predicted wrong), never "
                          "summed into the transition residual. Reader: _expected attaches a "
                          "routine's multi-step expect only where the subject's last rehearsal "
                          "this level held (rehearsal_read row). OFF: no rehearsal, _expected "
                          "as before. default ON",
    "TETHER_7H_TRACE": "7h (d), the recallable graded trace, smallest form (Isaiah 2026-10-16 "
                       "16:21): each line (a slot's search) is graded by the slot's kind "
                       "(7h (h)'s key) when it ends -- paid (bound, or its outstanding fell) "
                       "or left (7f) -- written per generation, summed at load; read at the "
                       "leave: a kind whose lines paid more than they were left is searched "
                       "a second full pass before leaving. The leave row carries "
                       "kind_record. OFF: no grades, the leave as before. default ON",
    "TETHER_7H_UNBUNDLE": "7h (c), recursion's smallest form at 7f's leave (Isaiah 2026-10-16 "
                          "16:21): a slot D5 is splitting (parts, pending, candidate) is never "
                          "left, and the leave row carries unbundled -- whether a held "
                          "predicate splits the slot's rows into parts each lawful (after a "
                          "function of before) while the whole is not. A read; searching "
                          "the parts alone is RECURSE-PARTS on the after-list. OFF: the leave "
                          "as before. default ON (Isaiah 2026-10-15 07:53, 17:26)",
    "TETHER_INDEX_AFFECTS": "step 5, the search index (Isaiah, RULINGS_CHECK item 8; the reviewer "
                            "2026-10-16 15:06, 15:10): the two atoms the agent makes are tagged "
                            "with the bare reading they affect -- an invention with its slot's "
                            "attribute, a goal condition with completed -- when the library knows "
                            "it as a reading, so the abductive lookup (by_affects) can reach "
                            "them. The tag is within the game: inventions are this agent's "
                            "private library (M7 carry off). OFF: no affects, as before. "
                            "default ON (Isaiah 2026-10-15 07:53, 17:26)",
    "TETHER_HOLES_REPOINT": "step 6, the sensors_heavy repoint (Isaiah 2026-10-12 via the reviewer "
                            "10:16; REPO_AUDIT sensors_heavy KEEP): sensors_heavy._holes returns "
                            "arc_percept.holes_of, the one implementation (enclosed regions); OFF "
                            "is the old border flood (cells, wrong on 56 of 263 wa30 objects). "
                            "default ON (Isaiah 2026-10-15 07:53, 17:26)",
    "TETHER_7I_ROUTE": "3a, 7i ROUTED (the seat 2026-10-16 14:14): an innate term refuted on a "
                       "slot (at the refute site) and a settled term refused (refuse_term) are "
                       "queued per step; beside the indistinct row one PERCEIVE row "
                       "contradiction_routed names them and carries resolve()'s remedy. "
                       "Nothing is demoted or removed. OFF: no queue, no row. default ON "
                       "(Isaiah 2026-10-15 07:53, 17:26)",
    "TETHER_7H_RESCOPE": "7h (b), B1 (the reviewer 2026-10-16 13:54, 13:57): in _goal_choice a "
                         "qualifying slot whose held goal shape (7h (a)) reads refuted by level "
                         "outcomes ranks after every other qualifying slot; still chosen when "
                         "nothing else qualifies, never removed. One rescope row (running step) "
                         "when the rank changes the pick. unsupported and mixed do not re-rank. "
                         "The 7f lines and tried counts re-scope by construction (keyed by "
                         "root). OFF: today's selection. default ON (Isaiah 2026-10-15 07:53, "
                         "17:26)",
    "TETHER_7H_ROOT_GRADE": "7h (a), A1 (the reviewer 2026-10-16 13:46, 13:47): the root's held "
                            "goal hypotheses as shapes by kind (slot kind, term), graded by the "
                            "ground's level endings (win, clear, death; a cap grades nothing), "
                            "written per generation and summed at load; intent_root carries "
                            "each shape's counts and the label read from them (refuted needs "
                            "two losses and no win). A graded record, never a minted term; "
                            "(b) is its consumer. OFF: no shapes, no grades. default ON "
                            "(Isaiah 2026-10-15 07:53, 17:26)",
    "TETHER_7H_EXIT_CHOICE": "7h (f), choose()'s exit order (the reviewer 2026-10-16 13:24, "
                             "13:29): the held routine first, bored a gate, mint-a-routine a "
                             "planner, draw the fallback; the live middle exits are chosen by "
                             "A1's readings (residual = outstanding of the aimed slots, actions "
                             "1, seen = turns at this level). While System 0 is active the "
                             "goal-directed exits (distinguish, goal) defer: the contest is "
                             "starved probe vs system0. One exit row with s0_defer and "
                             "fixed_would. OFF: today's fixed order. default ON (Isaiah "
                             "2026-10-15 07:53, 17:26)",
    "TETHER_7F_LEAVE": "7h (i), 7f LEAVE (the reviewer 2026-10-16 13:02, 13:05): after a mint, "
                       "a slot whose lookup closure was tried to its end at this level with "
                       "nothing bound and its outstanding not fallen since the line's first "
                       "mint is LEFT: one leave row (verdict unreachable at this budget, its "
                       "scope and attempt record); mint() on it returns at once until the "
                       "level or the root changes, the slot shows a (before, action, after) "
                       "transition not held at the leave (13:14), or a new operand appears; "
                       "then one reopen row "
                       "(reopen_by, skipped). Outstanding untouched; attention unchanged. "
                       "OFF: no rows, no skip. default ON (Isaiah 2026-10-15 07:53, 17:26)",
    "TETHER_7H_KIND_CARRY": "7h (h), H3 (the reviewer 2026-10-16 12:33): A1's starved and "
                            "curiosity counts are also kept by kind (owner kind, attribute "
                            "type), written per generation and summed at load; the carried-in "
                            "count is A1's second tie-break key after the slot count, and the "
                            "choice row says tie_by. OFF: no tally, no carry, no second key. "
                            "default ON (Isaiah 2026-10-15 07:53, 17:26)",
    "TETHER_LIBRARY_ABDUCE": "7d, the reverse lookup (the reviewer 2026-10-16 11:56, 12:00): "
                             "Library.light abduce=\"after\" at M4's lookup, one abduce row per "
                             "lookup (lit / extra / new / routed / refused); frame.came compiles "
                             "to {subject}.age == 0 marked via=event:came. OFF: no reverse "
                             "lookup and no came route; refusal wording stays named (the "
                             "reviewer 12:19). default ON (Isaiah 2026-10-15 07:53, 17:26); "
                             "the switch is kept for the checklist's culprit isolation",
    "TETHER_7M_ANALOGY": "7m: at site 8 a pair whose kinds were asked before goes first, "
                         "before the 7h tried count and the draw; an order, never a cut. "
                         "OFF is the line before it exactly. "
                         "default ON (Isaiah 2026-10-15 07:53, 17:26); "
                         "the switch is kept for the checklist's culprit isolation",
    "TETHER_SAVE_DEDUP": "(d), DEDUP AT SAVE (Isaiah 2026-10-25 05:33; the reviewer 19:57, the "
                         "alias form): a term row whose load key (gamma.row_key: atoms, guard, "
                         "operand tree, operand with ids blanked) the parent fold or this save "
                         "already holds as a row is written as an alias {was, key}; load_blob "
                         "resolves each alias to what that row installed (renamed / onto an atom "
                         "/ refused), so the replay maps the evidence as before. An alias naming "
                         "no row raises. OFF: every row written, as before. default ON",
    "TETHER_STORE_HEAL": "S6 H (the reviewer 2026-10-19; the K crash runs): under "
                         "TETHER_MEMORY_STORE, a store failing its cheap check at load WITH a WAL "
                         "is checkpointed "
                         "(TRUNCATE) and checked again, size and quick_check "
                         "(committed WAL pages made a correct store "
                         "read as short); one still failing is set aside (renamed .dead-<UTC>, "
                         "never deleted) and rebuilt from the saves by catch_up, where the load "
                         "fell back to the saves' fold. The load report carries store_healed. "
                         "OFF: as 753339c. default ON",
    "TETHER_MEMORY_STORE": "the consolidated memory (the reviewer 2026-10-19 06:13-07:35; Isaiah "
                           "06:12): lineage.load reads the memory folder's store "
                           "(lineage_store.py: one indexed SQLite file, integer keys, derived from "
                           "and rebuildable from the saves) after merging any save it lacks, "
                           "instead of re-reading every save; a folder the store cannot answer "
                           "exactly (a merge generation, another signature, bm_/bs_ files, a "
                           "failed check at open) loads from the saves as before, with a "
                           "store_refused row. default ON (Isaiah 2026-10-19 17:03 'turn it "
                           "on'; OFF every load is the saves' fold, 14.35 GiB on the E4 life). "
                           "OFF (=0): the saves' fold, as before",
    "TETHER_ONE_PASS": "the one-pass load (the reviewer 2026-10-19 06:09 d, 06:13): lineage.load "
                       "reads and folds the memory saves' chain once; head()'s pass was the same "
                       "chain and the same fold, read twice (a 4.95 GiB transient measured at 1 s, "
                       "06:04). The values are the same; OFF reads twice as before. default ON "
                       "(the reviewer 2026-10-19 06:35: 896/897 rows, 0 decision differences, a "
                       "byte-identical save, the load 23 s shorter); the switch is kept as a "
                       "stop-gap until the consolidated store replaces the load path",
    "TETHER_CARRY_RECORD": "S1g, the asked record (Isaiah 2026-10-15 13:26, option B; the "
                           "reviewer 13:27): under the slot filter a generation carries which "
                           "questions were asked (ak_), never the bound answers; a pair recorded "
                           "as a whole is rebuilt whole at its first ask from the carried, live-"
                           "checked index; bm_/bs_ stop for new generations, old files still "
                           "load. OFF writes bm_/bs_ as before. default ON (Isaiah 2026-10-15 "
                           "07:53); the switch is kept for the checklist's culprit isolation",
    "TETHER_LINEAGE_CARRY": "(b'-g) the lineage carry (Fig 12, Fig 10, Fig 4, Fig 6; the reviewer "
                            "2026-10-14 20:18, 20:22): ON, with a lineage folder given, every game "
                            "and run boundary writes a generation holding only what changed since "
                            "its parent (term rows, status, settle/refute evidence, the dormant "
                            "record), and the next instance loads the chain folded; no deletion, "
                            "never overwritten, one tip or it raises. Evidence and the dormant "
                            "record are the record only, never read back. OFF until Isaiah's word "
                            "after R-g1..R-g3 (registered 2026-10-14 20:18) and the OFF identity"
                            ". DEFAULT ON since 2026-10-15 (Isaiah 07:53): any OFF wording above "
                            "is the record; the switch is kept for the checklist's culprit "
                            "isolation",
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


def defaults_on(texts: dict[str, str] | None = None) -> dict[str, str]:
    """`{arm: "file:line"}` for arms whose DECLARATION is true with nothing exported.
    `texts` ({path: text}) stands in for the tracked files, for the selftest.

    **A VALUE IS NOT A SWITCH** (the reviewer 2026-10-14 06:49, 2026-10-15 14:56): a name in
    `VALUES` is skipped, because its default is data -- `TETHER_HOLD_SEED`'s "0" (retired since
    HOLD_SEED) was a seed, and a non-empty string evaluates true, so it was counted ON.

    Keyed on the ARM NAME IN THE LINE, not on the module variable, because the inverted
    spellings deliberately differ (`_TALLY` <- `TETHER_NO_TALLY`). Read from the code like
    every other census here: the table is the CLAIM and this is the WORLD.

    **DECIDED BY EVALUATING THE LINE, NOT BY PATTERN-MATCHING ITS SHAPE.** A regex over
    spellings would go stale the next time someone writes a third one, and the question --
    *is this true with an empty environment* -- has an exact answer.
    """
    if texts is None:
        texts = {}
        for path in _tracked():
            if path.name == "arms.py":
                continue
            try:
                texts[path.relative_to(ROOT).as_posix()] = path.read_text(encoding="utf-8")
            except OSError:
                continue
    out: dict[str, str] = {}
    for name, text in texts.items():
        for i, line in enumerate(text.split("\n"), 1):
            arms = [a for a in _READ.findall(line) if a not in VALUES]
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
                    out[arm] = f"{name}:{i}"
    return out


_NO_ENV = type("armflag", (), {"arm": staticmethod(lambda _name, default=False: default)})

# VALUES, NOT SWITCHES: read raw because they are not on/off. Data, so a new one is a visible
# edit here rather than a quiet exemption in logic.
VALUES = {"TETHER_SEED_FROM": "a REPLAY: the path of a record (a ledger or a lineage generation) "
                              "whose recorded seed and generation the agent reads; never a seed "
                              "value (HOLD_SEED, the reviewer 2026-10-15 15:04)",
          "TETHER_RUNS_DIR": "a PATH: the runs folder (the run index, its pins and removals, the "
                             "box folders, E4's folder for the mem_store runners); never on/off "
                             "(Isaiah 2026-10-30 16:33, the reviewer r454)",
          "TETHER_HOLDING_DIR": "a PATH: the holding folder beside the runs folder, scanned for "
                                "box folders; never on/off (Isaiah 2026-10-30 16:33, the reviewer "
                                "r454)",
          "TETHER_DECAY_RECORD": "a PATH: test_decay's captured birth record; never on/off (Isaiah "
                                 "2026-10-30 16:33, the reviewer r454)",
          "TETHER_STEP_BUDGET_N": "a COUNT, MAGIC (an interim constant authored by the seats, Fig "
                                  "10 :48; B1-B5 replaces it after the competition entry): "
                                  "K-W, the per-step lookup budget tether.STEP_BUDGET "
                                  "(default 50,000, Isaiah 2026-10-21 18:58; 1000000 restores "
                                  "the old pacing); never on/off",
          "TETHER_WORK_BUDGET_N": "a COUNT, MAGIC (an interim constant authored by the seats, Fig "
                                  "10 :48; B1-B5 replaces it after the competition entry): "
                                  "K-M, the ARC path's mint work budget "
                                  "(arc_holdout.ARC_WORK_BUDGET, default 5,000, Isaiah "
                                  "2026-10-21 18:58; 15000 restores the old pacing; the toy "
                                  "world's Config() keeps 15,000); never on/off",
          "TETHER_W_RAM_BYTES": "a BYTE COUNT: a planted RAM figure for W-1's budget "
                                "(tether._ram_bytes, test_w MF-W5); never on/off (2026-10-22)",
          "TETHER_CONSOLIDATE_CEILING": "a BYTE COUNT: a fixture's lowered per-process ceiling "
                                        "for CONSOLIDATION's size trigger (tether._fold_ceiling, "
                                        "test_consolidate CON-5); never on/off (the reviewer "
                                        "2026-10-20 23:55, 2026-10-21 00:05)"}
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
                           '_S = os.environ.get("TETHER_SEED_FROM", "0")\n'}
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


def sites(texts: dict[str, str] | None = None) -> dict[str, list[str]]:
    """`{arm: ["file:line", ...]}` -- READ FROM THE CODE, never from the table.

    A census built from the table would agree with the table by construction, which is the
    measurement that cannot fail. The table is the CLAIM and this is the WORLD.
    `texts` ({path: text}) stands in for the tracked files, for the selftest. A name in
    `VALUES` is not a switch, so it is not counted (the reviewer 2026-10-15 15:04)."""
    if texts is None:
        texts = {}
        for path in _tracked():
            if path.name == "arms.py":
                continue
            try:
                texts[path.relative_to(ROOT).as_posix()] = path.read_text(encoding="utf-8")
            except OSError:
                continue
    found: dict[str, list[str]] = {}
    for name, text in texts.items():
        for i, line in enumerate(text.split("\n"), 1):
            for arm in _READ.findall(line):
                if arm not in VALUES:
                    found.setdefault(arm, []).append(f"{name}:{i}")
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

    # G -- A VALUE IS NOT A SWITCH: a VALUES name whose default is a truthy string ("0") must
    # not count as ON; and the control, a switch spelled the same way, must.
    got = defaults_on({"x.py": '_HS = os.environ.get("TETHER_SEED_FROM", "0")\n'
                               '_X = os.environ.get("TETHER_X", "1") != "0"\n'})
    out["G value"] = ("ok" if "TETHER_SEED_FROM" not in got
                      else "UNWITNESSED (a value's truthy default counted as ON)")
    out["G control"] = ("ok" if got.get("TETHER_X") == "x.py:2"
                        else f"UNWITNESSED (a default-ON switch was not seen: {got})")
    sw = sites({"x.py": '_HS = os.environ.get("TETHER_SEED_FROM", "0")\n'
                        '_X = os.environ.get("TETHER_X", "1") != "0"\n'})
    out["G switches"] = ("ok" if "TETHER_SEED_FROM" not in sw
                         and sw.get("TETHER_X") == ["x.py:2"]
                         else f"UNWITNESSED (a value counted as a switch, or the switch "
                              f"missed: {sw})")
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
    "TETHER_HOLD_SEED": "the reviewer 2026-10-15 15:04 (HOLD_SEED Q2): a seed-valued input is "
                        "a route to forcing the seed; the seed is the agent's, drawn at birth "
                        "and recorded, and a replay names a record (TETHER_SEED_FROM). Setting "
                        "it is refused by name at the agent's birth.",
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
