WATSON — make the `arrived_no_clear` correction readable as subtext (goal-direction, 2026-11-21)

QUESTION (effect terms): on an unseen game the agent adopts a goal, meets its own condition,
and the board does not clear. The chain stops: repair fires with pushed=False and no subgoal,
so no second, different goal is tried. What minimal change lets the correction direct the NEXT
goal toward a different kind of condition, without encoding any game's answer?

RESIDUAL described in effect terms (Fig 9 :30-31 "describe the effect rather than the cause"):
"my own condition was met; the ground did not pay; I re-proposed the same kind and stopped again."
This is Isaiah's correction-as-subtext ("Decoding Tacit Knowledge", 2026-11-10): the meaning is
in the unstated gap between what the agent did and what the board showed. It is NOT a new
fact about the world — it is a claim about the agent's own line, so it belongs in the steer.

DOMAIN CENSUS:
- R: one (goal-template-kind, slot-kind) pair; arity 2; symmetry = a stop is evidence against
  that kind, not proof; scale = one board's proposal comparisons.
- domains: (a) the correction (actors: the board's no-clear, the agent's ended goal; currency:
  a witness against a kind; anchor: the ledger row); (b) the proposer (actors: candidate goals;
  currency: bits/rank; anchor: the comparison); (c) the steer store (actors: stopped/paid lines;
  currency: a reversible p; anchor: the row). Order: correction → steer → proposer.
- union: "my kind stopped" ∩ "another kind could win" is one compound (Fig 9 :55-58).

TETHER (primary, verbatim):
- Fig 9 :53 "Nobody chooses. The gap does, and the gap is only as good as its description."
  → the correction must be DESCRIBED into a readable signal, not just rowed.
- Fig 9 :27-28 "describe it before you go looking, or any frame you pick will seem to fit"
  → describe the kind that stopped BEFORE picking the next one.
- Fig 4 :30-32 "the gap is not an error to eliminate. It is the measurement of what the
  coarser description cannot hold" → the correction size is evidence, kept and priced.
- Fig 13 "a wrong cut removes the answer and speeds up / keep every cut ranked and reversible"
  → the preference must be reversible (paid can undo a stop), never a deletion.
- Fig 11 :39-40 "capability is a property of agent-and-habitat" → this changes what the agent
  can REACH (a different condition kind), not a game score.
- Fig 1 :22 "Aggregating across slots is how a live signal disappears" → key by kind, never pool.
- Fig 10 "A verifier that can reconstruct the claim cannot verify it" → the signal must be an
  agent-written row, not a seat-injected value.

WORLD (secondary, corroboration only): the article's eight-combination table — context-only
→ Noise; pretext-only → Projection (Fig 9 :27-28) — predicts that a correction with no read-back
is noise. The agent's existing `_SELF_STEER` is exactly a "correction read back as a price".

CODE ANCHOR (write sites, measured):
- `tether.py:11399-11400` produces `arrived_no_clear`, loss=True.
- `tether.py:11493-11501` already publishes a reversible stop for the ended goal's kind:
  `sk = (self._ss_form(h["tkey"][0]), self._kind_key(h["slots"][0]))`,
  `link = {"stalled": "plan", "arrived_no_clear": "objective"}.get(why)`,
  `self._ss_stop(link, "hyp", sk)`.
- `tether.py:25501-25508` reads it back in `_ss_hyp_price` over lines ("plan", "objective")
  and prices the candidate up by -log2(p): the failed kind loses rank, another kind can win.
- So the CORRECTION already changes rank and eligibility (`_hyp_tried`, `_goal_refuted` at
  :12145-12147, `_hyp_pair` at :12542-12555) — but the "subtext" meaning (my KIND is what
  stopped) is published only as a generic stop, not named as the correction's reading.

DECISION: add a distinct, named subtext line to the SAME existing steer (no new state field,
no new reset, no new rank tuple element):
- At `_hyp_end` on `arrived_no_clear`, additionally `self._ss_stop("objective", "subtext", sk)`
  with a row that NAMES the gap in effect terms (met condition, no clear, kind) — the
  described correction Isaiah asks for.
- Extend `_ss_hyp_price` to read ("objective", "subtext", kind) as a third line, so the
  kind that just arrived-without-clear is priced up and a different kind can win. It is the
  SAME reversible store: `_ss_pay` on a later success undoes it.
- Behind arm `TETHER_CORRECTION_SUBTEXT` default ON; OFF = byte-identical ledger and choices.
- Must-fail control: with the new line removed, the same (kind) candidate still wins; with it
  present, a different-kind candidate of equal bits wins — and the planted-defect test shows
  the check can fail. No game identity read, no answer encoded, no threshold tuned.

cost if wrong: a kind is priced up after one no-clear that was actually a budget artifact —
mitigated by the steer's p (one witness is weak; 1+paid >= against means no reading) and by
reversibility (a paid success restores it). undoable: yes, arm OFF identity row. reversed by:
a game where re-proposing the same kind after a no-clear clears (then the stop is not evidence),
or Isaiah ruling that the correction should name a different key.

HOLD: this is a SEAT-side design derived from the figures and the article. No ARC-game tuning.

WATSON — should the arbitrary per-game time cap be raised or removed to get more contact?

QUESTION (effect terms): the T0 chain stops at subgoal/clear after 600 s/game. Some games have
built-in limits, others could run indefinitely. We set 600 s while building; it could be raised
or removed. Does more time change what the agent can REACH, or only how long we wait?

RESIDUAL described in effect terms (Fig 9 :30-31): "the agent reached its own goal, the board
did not clear, and no second goal was tried before the budget ended." Is the stop a capability
limit or a budget artifact? The two are distinguishable only by a longer run.

TETHER (primary, verbatim):
- Fig 9 :44 "Only a sealed room can be searched to the end, and no frame is a sealed room.
  So searching and finding nothing proves nothing." → a null at 600 s is not evidence the
  mechanism cannot; the room was not sealed.
- Fig 6 :49-50 "more search at the same reach: is it in here and unfound? The closure does
  not change ... Fails by spending budget on a region already swept." → more time at the SAME
  reach is not the fix; but the correction-subtext change ALTERS reach (a different kind can
  win), so more time AFTER it can find something new. The two work together.
- Fig 12 (two currencies): actions/wall is a real cost, read beside description bits, never
  netted. So time is a genuine currency, not free — raising it must be measured and named.
- Fig 11 :39-40 "capability is a property of agent-and-habitat" → more contact (more actions
  on a real board) is the only thing that moves capability, so a budget that ends contact early
  is a habitat restriction.
- Fig 5 : budget exhaustion is "unreached at this budget", NOT a verdict — so the 600 s stop
  must be read as unreached, never as "the agent cannot."

CODE ANCHOR (measured 2026-11-21):
- No per-game wall is imposed by the platform. `tether_agent.py:28` `deadline=None` default,
  `:48-50` deadline is optional; `arc_holdout.play()` has NO deadline parameter at all.
- The 600 s is OUR harness flag: `harness/mem_store/e4_stream.py:32 --slice-s default=600.0`.
  T0e actually ran 300 s (STATE_OF_THE_AGENT:43); the written protocol says 600 s (:35).
- Removing the wall is NOT safe: a single step took 53 min (STATE:30); a documented runaway
  hit 18-54.5 GB (INDEX:257). The only stop inside a step is `CapReached` (cap.py:43-53),
  driven by the deadline. The supervisor (harness/supervise.py:146-159 memory ceiling) is the
  runaway guard and must stay.
- Platform walls that CANNOT move: Kaggle 9 h notebook (`make_notebook.py:19`), 600 s gateway
  wait (`:210,215`). A 6-game × 1800 s run = 3 h, inside 9 h.

DECISION: RAISE, do not remove. Keep the deadline (the only in-step stop and the agent's clock)
and the supervisor; raise the per-game slice from 600 to 1800 s for a proving run, run under
the supervisor, with the new correction-subtext mechanism ON. Read the result as contact, not
as a score: did the chain reach subgoal/clear with more actions, and does the epoch correction-
size trend fall across generations? Never pool games; report per game.
- cost if wrong: 3 h of wall and a larger memory footprint, bounded by the supervisor; and
  the clock the agent reads changes, so 1800 s runs are NOT A/B-comparable with 600 s runs.
- undoable: yes, the slice is a flag, no code change.
- reversed by: the chain reaching the same stop at 1800 s (then time was not the limit); or
  Isaiah ruling the 600 s protocol is the competition condition and must not change.

NOT done: no ARC-game tuning, no answer encoded, no cap removed from code. The proving run is
an instrument reading, run detached under the supervisor.
