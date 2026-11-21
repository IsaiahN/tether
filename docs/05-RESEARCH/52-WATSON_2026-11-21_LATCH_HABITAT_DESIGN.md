WATSON — why a two-step latch habitat, derived from the gap audit (2026-11-21)

PROMPT: Isaiah — "make more gridworlds, more test etc to help the agent. IT already has
metaprogram capability that is what the composition was for. you need to audit what it already
has." Plus: "retain the architecture, transparent, whitebox, 100% interpretable; whatever we
put in place needs to be accessible by the agent via the library as one of those composition
metaprograms it can access."

This WATSON is the derivation for the code in `latchworld.py` and `tests/test_latchworld.py`.
It is a HABITAT addition, not a kernel change, not a prior, not a new sense.

===============================================================================
1. RESIDUAL (effect terms, Fig 9 :30-31) — describe before looking
===============================================================================
"the agent has a full metaprogram algebra (Act/Seq/When/Until/Call/Let/Expect) and an
inferred-cause mechanism (count of presses / latch), both default-ON, and neither has ever
bought a multi-step plan: routines adopted 0, chunk_reuse 0 across 14 readings; the inferred
cause has never had a world that requires two steps."

Not "the agent is slow" or "composition is weak" — those are causes. The EFFECT is: **a
built-and-starved capability with no habitat that pays it.** Fig 11 :39-40: capability is
agent-and-habitat; an agent-only improvement that doesn't change contact changes nothing.

===============================================================================
2. THE FIGURES DECIDE — why habitat, not kernel or dictionary
===============================================================================
- Fig 11 :40 "an improvement that does not change contact changes nothing" → more gridworlds
  are the legitimate move: introduce an actor into the habitat (Fig 11 :31 "introduce, never
  subtract") so a built mechanism gets a contact surface.
- Fig 11 :48 "what you cannot perceive or measure yet is the residual" → the latch state is
  PUBLISHED (`latch.armed`), so the two-step causal chain is perceivable, not a hidden null.
- Fig 11 :70 "a test harness is a substituted habitat. Which is why a synthetic solve proves
  wiring and never capability." → the world's own tests assert it can EXHIBIT the capability;
  they never claim the agent clears it. No encoded answer.
- Fig 12 :5,14,94 "the arrangement is the substance" → the new thing is the ARRANGEMENT
  (press arm THEN press fire), not new atoms. The atom set is `world2d._atoms()` verbatim.
- Fig 13 :114 "the set is closed. The arrangements are not." → no new atom, no new sense; a
  new composition of existing actions.
- Fig 9 :60 "filters for the budget and witnesses for the verdict" → the world publishes
  the goal and the latch; it never tells the agent which press is arm. The board judges.
- Fig 6 :26 "The world does not gain primitives; a frame gains access." → `wired=False` is the
  control arm: same atoms, same actions, goal directly reachable. The differential is contact.

===============================================================================
3. THE DESIGN (world2d contract, one vocabulary, single BECOME objective)
===============================================================================
- Three objects; three `press_i` actions; a seed-drawn permutation of arm / fire / goal.
- press(arm) sets the published `latch.armed=1` and nothing else; press(fire) while armed
  advances the goal colour and clears armed; every other press moves a distractor (the ARM
  object — distinct from the goal) and never the goal.
- Therefore the ONLY way to move the goal is the sequence [arm, fire]. Single-press policies,
  repeated, cannot clear it — a structural refuter, not a threshold.
- One `BECOME(oG.colour, target)` objective and one `@goal.completed` slot, so the A6i pairing
  (objective degree == goal slot) and the WANT construction in tether.py are untouched.
- Standalone module (the world2d pattern) so `gridworld.py` and its four families stay
  byte-identical — no fork of `step` or `_assert_reachable`.
- The two-step structure is exactly what `Until`/`Seq` (routine.py) and `TETHER_INFERRED_CAUSE`
  (count/latch) are built for; the world gives them an occasion without changing either.

===============================================================================
4. MUST-FAIL CHECKS (tests/test_latchworld.py) — refuters, not existence
===============================================================================
1 contract binds (all eight methods) · 2 reachability by construction (arm+fire clears on 12
seeds) · 3 REFUTER: no single action repeated 8× moves the goal · 4 latch perceivable (published
and consumed) · 5 fire-alone/distractors move something but not the goal · 6 control arm
directly reachable · 7 determinism + goal slot not writable · 8 one vocabulary with world2d.
The tests caught two real defects while being written: a fixed-count reachability check that
overshot a mod-4 colour target (fixed: drive until cleared), and a distractor `(i+1)%N` that
could BE the goal (fixed: distractor is the arm object). Both are recorded in the code.

===============================================================================
5. WHAT THIS DOES NOT CLAIM
===============================================================================
It does NOT claim the agent now reasons better. It is a MEANS: a habitat where a two-step
composition can pay and be measured. Whether it does is a run on the ground, per game, never
pooled. No kernel switch changed, no max_depth raised, no prior given standing, no text channel
added, no ARC game touched. Every addition is a readable world object + a must-fail test.

FIGURE CENSUS: Fig 1 claim/mode · Fig 3 dependency order · Fig 4 methods-only membrane · Fig 5
when a composition pays · Fig 6 primitives vs arrangements · Fig 9 describe-effect /
filters-not-verdicts · Fig 11 capability=agent-and-habitat / introduce / enumerate / contact /
substituted-habitat · Fig 12 bond-is-the-substance / one vocabulary · Fig 13 closed set open
arrangements. Strained: none.

Status: built, ruff-clean, 8/8 must-fail tests pass; smoke run on the direct agent driver in
progress. No capability conclusion until the ground run is read.

## Latch habitat — first ground read (2026-11-21, development d9b28beb)

Smoke: `ag.step()` directly on `LatchWorld(seed=0)`, 150 cycles, `TETHER_AGENT_SEED=0`,
every arm default. Purpose was write-site execution + a first contact reading, NOT a
capability claim. Agent completed cleanly: 149 actions, 13,673 ledger rows, 0 crashes.
Both harnesses: the 8 unit tests are the tape/write half; this is the live direct-driver half.

### What exhibited on the habitat (verbatim ledger)
- `goal_hypotheses`: 48 candidates formed, **0 checked**, on cycles 3/4/5/7/11 — the goal
  machinery ran and had candidates but admitted none.
- `route @objective`: 2,400 rows, `why_not` = "not mechanism: too little history on the
  objective" / "nothing in the library advances the degree"; `remedy` = "deferred:
  **composition of actions is not built at agent scale**" (tether.py:18281-18297 states the
  remedy is not built). This is GAP 2 exhibited at the write site, not a stale record.
- `invent` fired at cycles 12/21 on `latch.armed` and `o2.colour`: 3-5 cause candidates,
  but `park_verdict = "priced_out_at_depth"`, `pick = "none paid"`, `priced = 0`, with
  refusals like "above does not accept POSITION". This is GAP 1 (composition can't stack /
  type ceiling) exhibited: the BOOL latch could not bind into a cause over the COLOUR goal.
- `latch.armed` was heavily perceived (1,112 rows: 150 bet, 153 think_choice, 146
  design_read) — so this is NOT a "no occasion" null. The mechanism had occasion and did not
  fire. That distinction is the whole point of this habitat.
- End: `levels 0, won 0, minted 1, settled 1`. The two-step chain was never bought.

### Verdict
The habitat does its job: it is a MEANS that EXHIBITS the two audited gaps on a real run,
without any kernel/prior change. It produced a *sharper* null than a synthetic solve would —
`0 checked`, `priced_out_at_depth`, `none paid` — each a refuter that would flip if composition
or the type bridge existed. No capability improvement is claimed. The fix the agent names
("composition of actions is not built at agent scale"; BOOL→COLOUR cause refused by type) is
exactly the GAP 1/GAP 2 kernel work this project has NOT done — deliberately out of scope for
this habitat change, which preserves the architecture. Recorded, not patched.

Cost note: 150 direct cycles consumed ~370 s CPU — the 122-bets/action signal again. The
smoke had no deadline/supervisor; that is a lapse against the cap-long-runs rule and is
recorded, not repeated.

## CORRECTION, 2026-11-21 (WATSON 53) -- read this before the world-design claim above
Isaiah corrected the framing: the agent should NOT key a cause on colour ("games change their
colour -- a cheap temporary key, sticking something to the wall with gum"). The intent/interface
seam is Fig 4 ("only the actors, the currency and the anchor change") and is ALREADY BUILT:
the agent emits NSM intents (ELICIT/TOUCH/BE_AT/BECOME/DISTINGUISH) and \Interface.realise\
turns them into actions from an observed table (25 call sites, WATSON 53). So the fix I wrote
above ("BOOL latch -> COLOUR cause") is the wrong target. The real not-built part is narrower
and domain-general: interface-side outcome -> action-SEQUENCE search (interface.py:1410,
tether.py:18296). The latch habitat remains useful only as a SURFACE that made the agent say
"composition of actions is not built" -- not as a cause-keying proposal. Kernel untouched.