WATSON 64 — where this agent's intellect is actually starved, from two full audits (2026-11-22)

ISAIAH'S QUESTION: boost the agent's intellect and fluid reasoning from its own constitution and
umwelt — no LLM, no massive model, no massive dataset. WATSON 63 derived what "intellect" means
(levels of composition; the measured break; carry of methods). This WATSON reports WHERE, from two
read-only audits of the reasoning chain and the abstraction/self-reasoning machinery, every claim
verified at the write site.

QUESTION (effect terms): the agent reasons at goal 6/6 but clear 0/6. Which built mechanism is
starved of contact, and which is a correct abstention, so effort goes at the break and not above it?

## AUDIT 1 — the goal-to-clear chain (verified)
ONE ROOT CAUSE: the goal is satisfied at its own test, so refusal has no open condition to
decompose. `arrived_no_clear` is emitted only when the goal's own series is CONFIRMED
(tether.py:11408-11410). Repair is called, but `_htn_push` returns False because its candidate set
is empty — all candidates require `b in self._res and arrival(b)==OPEN` (16817-16823), and the
refused slot is CONFIRMED, not OPEN. `_enablers` further requires a settled bound term (16501-16503);
the refused goals were held/unsettled. Ledger: both observed `repair_at_refusal` rows read
`pushed:false, subgoal:null`; zero `subgoal_adopted`/`htn_push` rows in all six games.

Status table (per game, never pooled): goal/selection BUILT+REACHED (6/6); refusal BUILT+REACHED
(5/6); repair row BUILT+REACHED (3/6) but both proving rows pushed:false; subgoal push BUILT but
STARVED (0/6); `_htn_settle`/`_htn_close` BUILT but STARVED (no pending edges); HTN RETURN BUILT but
on the rare fire it re-adopts the SAME satisfiable-but-insufficient condition (16645-16647), so no
clear; the Fig 9 goal-direction loop (describe→unbundle→lookup→narrow on the no-clear residual)
is NOT BUILT (WATSON 43:88-115). Selector's refusal on a satisfied goal is CORRECT ABSTENTION —
there is no gap to pursue. A name mismatch makes it worse: the card's `do_sym` says `R_s`, agenda.py
looks for `R⁺_s` (verified: card contains R_s not R⁺_s; agenda tests R⁺_s; BOUND has only R⁺_s), so
every "Describe before you look" row has `sym:null`. The `sym` field is written but never read — a
legibility defect, not a decision input.

## AUDIT 2 — abstraction / self-reasoning machinery (verified)
The agent ALREADY reasons about itself and acts on it in two places:
- `_steer` (item 27, tether.py:16400-16431): a line stopping at the same link sets a route aside so
  the next realisation differs. BUILT+REACHED+CONTACT.
- `MUSING_CHOSEN` + `muse_test` (13608-13654, 13667-13721): the agent forms its OWN rival hypothesis
  from its own parked residuals/losses and runs its own discriminating press. BUILT+REACHED+CONTACT.
  This is curiosity from its own state — the closest thing to fluid self-directed reasoning it has.

What changes decisions across games (the real transfer): lineage library carry, `kind_of`
(drops object identity — gamma.py:1582-1593), `CARRY_W` kind-keyed counts feeding the bargain price
(gamma.py:1808-1815), `source_of` causal key (tether.py:3497-3554). All BUILT+REACHED+CONTACT.

The conspicuously RECORD-ONLY abstractions:
- `R_T`/`T_A` round trip: live worlds return `transform()=None` (verified tether.py:18217-18222),
  so the bracket channel is CLOSED and R_T is never computed; on snaps it is the identity view so 0.
  The only decision-changing use is in `arc_check.py`, a check script, not the live path. T_E is
  deliberately UNBOUND (symbols.py:230-233).
- M3 `_self_read`: reads where past games' chains stopped at game start — "a reading only, nothing
  steers by it" (tether.py:4231-4235). RECORD-ONLY, explicitly.
- process bets D1-D3: ground-graded records, no consumer feeds the verdict back.
- `self_family`/`arc_self`: built in the WORLD adapter, but tether.py never reads `env.selves`.

## THE FIGURES DECIDE WHERE TO SPEND (Fig 3: find the break first)
T0 stops at subgoal 0/6, and audit 1 locates exactly why: no open condition exists to decompose.
Fig 9 says the move on a satisfied-but-insufficient goal is describe-the-residual → unbundle →
look up a frame predicting the win condition → narrow — and that loop is NOT BUILT. That is the
break. Per Fig 3, improving perception (6/6) or goal selection (6/6) cannot rescue it.

VERDICT — the ranked, figure-faithful levers for "boost intellect from its own constitution":
1. **Build the Fig 9 goal-direction loop on `arrived_no_clear`** (NOT BUILT, WATSON 43). When the
   goal is met but the board is not cleared, describe that gap in effect terms and look up a
   condition-shape that predicts clearing, then bind it as an ordinary term and let it accrue a
   residual (Fig 5 :65-66). This creates the OPEN condition that `_htn_push` currently finds absent,
   so repair→subgoal can fire. This is the break; it is in the plan (WATSON 43/45); no external
   knowledge, no kernel change to the loop — a new step the loop already calls for.
2. **Give the record-only abstractions contact** — specifically `_self_read` (where past chains
   stopped) already exists and is legible; letting it steer the current game's route is a small,
   arm-guarded change using data the agent already has. This is Fig 4 "head start down" made real.
   The round trip is channel-closed on live worlds — a coarse-view instrument would be a new sense,
   which needs its own Fig 6 entry rule; NOT the first move.
3. **Strengthen what already has contact** — muse-chosen and `_steer` are the two places the agent
   self-corrects; they are the proof the architecture supports self-directed reasoning. Any change
   should extend these, not add a parallel self-reasoning module (Fig 12 "no free bond").

NOT levers, per these audits + WATSON 63: more corpus (perception/knowledge is cue-only, 6/6), a
bigger model (no model in decision path), the round trip on live boards (channel closed), ImageNet
data (recognition inert on grid boards), or an LLM in the loop (Fig 10 verifier rule).

COST IF WRONG: effort above the break cannot arrive (Fig 3). UNDOABLE: each lever behind an arm, OFF
byte-identical. REVERSED BY: a per-game run where the new open condition does not raise subgoal or
clear above 0/6.

BUILD ORDER: (1) symbol fix R_s→R⁺_s in the card/agenda — tiny, truthfulness only, no contact claim;
(2) Fig 9 goal-direction loop behind an arm with must-fail tests — the real L1 capability item;
(3) self_read steer, only if (2) still leaves the chain short. WATSON 63 and 64 commit with the
first L1 change (focus seat at stall 5). No code changed in this WATSON.

FIGURE CENSUS: Fig 1 · Fig 3 · Fig 4 · Fig 5 · Fig 6 · Fig 9 · Fig 10 · Fig 11 · Fig 12 (verbatim
from SVGs). Strained: none.

Sources: two read-only audits (2026-11-22), tether.py/agenda.py/symbols.py/gamma.py write sites,
six proving ledgers, WATSONs 43/45/63.
