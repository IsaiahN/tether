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
