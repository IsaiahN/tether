# WATSON 2026-10-28 22:05 CDT — The growing queue of postponed questions: carry it, re-judge it, or release it?

## Isaiah, verbatim (22:00 CDT)
> "'Re-judge the growing queue of postponed questions.' Run a WATSON and then decide. This agent is running on human priors but machine substrate. It's technically a unique umwelt, but still has to follow the rules of systems, i.e. the Tether"

## QUESTION
B2 (merged 10-26) postpones each derived-want ask that cannot run this step and carries it "owed".
- PLAY16 r4: owed sets reached 74 (re86), 54 (ls20) and 43 (cn04) at game end, with derived_run 0 in those games. On every step that had derived asks, the ACCEPT loop had already used the step's one full search.
- What should happen to a postponed question: keep carrying it, re-judge it, or let it go?

## DOMAIN CENSUS
R: arity 2 (the owed ask, and the step's capacity to serve it); scale step → game → life.

| Domain | Actors | Currency | Anchor |
|---|---|---|---|
| RECORD | the deferral rows | rows | Fig 6's monotone record |
| LIVE QUEUE | owed asks | steps of capacity | whether the ask still has something to explain NOW |
| HABITAT | the board | frames | the ask's evidence is a past frame's transition |
| CAPACITY | the one full search a step may run (B1/B2) | | which question gets it |

Order (Fig 3): HABITAT → LIVE QUEUE → CAPACITY. The RECORD stands apart and only grows.

## TETHER (primary, verbatim)
- **RECORD.** Fig 6 :42-46: "What is recorded only grows. What is reachable is derived, and it can fall. … A store that deleted instead would have neither property, and could not tell never-held from held-and-given-up." → Releasing an ask from the live queue must ADD a record ("given up, why"), never delete one.
- **LIVE QUEUE / HABITAT.** Fig 10 :24-25: "the ground does not decay, the channel does / stale percepts, dropped transients". Fig 11 :51: "No standing list of good actors survives a change of residual." Fig 11 :73: the habitat "updates". → An owed ask carries a transition from a past frame, which is a channel reading and goes stale. A standing queue does not survive the residual changing. Each owed ask must be re-read against the current frame.
- **The re-judgment's test.** Fig 5 :19-25, :33, :41: "the three guards, all of which must pass / is there anything to explain? … can we even build this term? … is it actually new? … The three guards are a product, not a checklist. … Any one of them at zero stops the mint entirely." → A postponed ask gets no exemption. When it comes due it passes the same guards as a fresh ask, NOW, or it is released.
- **CAPACITY.** Fig 5 :18: the drive "seeks the gap that is large and compressible". Fig 9 :60: "Use filters for the budget and witnesses for the verdict." → The step's one full search goes to the highest-value question across ALL kinds (loop mint or derived ask), by the agent's existing measure (`_understanding` = outstanding × recurrence, tether.py :11765). Code order and age decide nothing. A release is a budget filter, never a verdict on the question.
- **Unreached is not refuted.** Fig 6 :49-51 and Fig 8 separate "underivable-in-principle from unreachable-at-this-budget". → A released ask was not answered "no". It stays askable: B2 already never marks an owed ask tried, so fresh evidence re-raises it.

Triangulated across Figs 5, 6, 10 and 11, which overlap little.

## THE CODE (d12c74e, B2 in `_derived_wants`)
- Owed asks go first (a stable sort) and are asked with their STORED transition. They skip the moved / new-evidence test and the echo test.
- They are dropped only if the slot stopped being declared derived or now wants something. Nothing checks whether the gap still has mass now, or whether a newer transition has superseded the stored one.
- When the ACCEPT loop exhausted earlier in the step, every owed ask is re-deferred. So in games where the loop exhausts every step, the queue is never served and only grows. That is the freeze.
- B1's owed map for loop mints already re-judges: an owed slot is minted again only if route bins it to a mint again that step (10-26 r251, "owed dropped"). B2 does not. The fix makes B2 behave as B1 already does.

## WORLD (secondary, each read)
- **Emergency medicine.** Murray, Bullard & Grafstein, "Revisions to the Canadian ED Triage and Acuity Scale Implementation Guidelines", *CJEM* 6(6), 2004:
  - "the focus should shift to the timely reassessment of patients waiting to be seen";
  - "Should acuity increase upon reassessment, the order of priority of the patients waiting in the ED may change".
  - The initial triage level is not changed; a separate reassessment level is recorded.
  - This predicts the same split as the figures: the record is fixed, the live priority is re-derived. Corroborates Fig 6 and Fig 5.
- **Behavioural ecology.** Charnov, "Optimal foraging: the marginal value theorem", *Theoretical Population Biology* 9:129-136, 1976: the forager "should leave the patch it is presently in when the marginal capture rate in the patch drops to the average capture rate for the habitat."
  - This predicts that an ask is released when its current value falls below what the step's capacity earns elsewhere: value against value, with no fixed age or size limit. Corroborates CAPACITY.
- **Human cognition (the priors).** Masicampo & Baumeister, "Consider it done! Plan making can eliminate the cognitive effects of unfulfilled goals", *JPSP*, 2011 (DOI 10.1037/a0024192), via Psychology Today: "committing to a specific plan for a goal frees up cognitive resources for our other pursuits."
  - This predicts that an open loop with a recorded plan (a re-judgment rule) need not be carried live. Corroborates RECORD versus LIVE QUEUE.
- **On the substrate.** A machine does not feel the open loop the way a person does. Its cost here is real but different: owed asks re-sorted and re-counted every step, fresh asks starved by owed-first ordering, and stale evidence asked over newer evidence. Isaiah's point holds: the umwelt is its own, and the rules are the Tether's. The figures decide; the human findings only corroborate.

## VERDICT AND DECISION
Re-judge the queue; do not carry it blindly, and do not cap it with a number. It becomes item **1d** of decision 1 (the twenty-questions build), because a postponed ask is an open gap whose question has not run yet.

1. **RECORD.** Every deferral already writes a row. Every release adds an `owed_released` row (slot, first-deferred cycle, the guard that failed or "outranked", the current values). Nothing is deleted (Fig 6 :42-46).
2. **RE-JUDGE WHEN DUE.** Each step, every owed derived ask is re-read against the CURRENT frame by the same guards as a fresh ask:
   - it is still declared derived and wants nothing (as now);
   - there is still something to explain now: the slot's outstanding surprise is above 0;
   - it is not already explained: no held term or want formed since predicts its transition.
   - Newer evidence supersedes older: if the slot moved again, the new transition replaces the stored one.
   - Failing any guard → released and recorded. A release is not "tried", so new evidence re-raises the ask.
3. **RANK, NOT AGE; ONE QUEUE FOR CAPACITY.** Surviving owed asks compete with fresh asks, and with the ACCEPT loop's mint candidates, for the step's one full search by `_understanding` (Fig 5 :18).
   - Ties go to A1's choice (less-seen first, which favours the long-waiting).
   - "Owed-first" by age, and "loop first" by code order, are both replaced by rank.
   - An ask that is outranked when its game ends is released and recorded "outranked" (Charnov: below what capacity earns elsewhere).
4. **No new constant anywhere.** The guards and the rank are quantities the agent already computes.
5. **Scope.** B2's derived queue, and the cross-kind ordering of the step's one full search. B1's owed map already re-judges by route and changes only through point 3's ordering. One arm, `TETHER_OWED_REJUDGE`, default ON, with its arms row.
6. **Tests:**
   - (a) a stale owed ask whose slot no longer has surprise is released and recorded;
   - (b) newer evidence replaces a stored transition;
   - (c) the step's one full search goes to the highest-ranked question across kinds;
   - (d) MUST-FAIL with OFF: the queue grows as in PLAY16 r4;
   - (e) MUST-HOLD: OFF is byte-equal to the base;
   - (f) a released ask is re-raised by fresh evidence.

## Cost, undo, reversal
- **Cost if wrong:** a postponed question that would have paid later is released early. It is recorded, and new evidence re-raises it.
- **Undoable:** yes; it is an arm.
- **Reversed by:** PLAY rounds where released asks come back and pay; or derived wants formed falling with no gain in steps or settles.

## CORRECTION 2026-10-29 07:40 CDT (r326)
Point 2's guard ("the slot's outstanding surprise is above 0") and point 3's rank (`_understanding` of the slot) read ZERO on every DERIVED slot by construction: derived slots are never bound, bet on or charged. The seat measured it: 162 derived slots, outstanding 0 at every step, while the owed queue reached 49. Built as written, every owed derived ask would have been released unasked.
- **Ruled (Option A):** the guard reads the ask's SOURCES (env.derived()). The ask stays owed while any source has outstanding > 0, and is released "sources explained" when none does. The rank stays the ask's own (0), so a derived ask takes the step's one full search only when no plain mint candidate is in the step: upstream first (Fig 3; Fig 13, "a derived bind restates its sources").
- An added must-fail reproduces this error: with the literal guard, every owed ask is released at its first re-judgment.
