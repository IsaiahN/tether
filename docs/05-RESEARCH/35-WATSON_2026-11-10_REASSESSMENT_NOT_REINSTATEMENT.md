# WATSON — a new failure: reassessment, not reinstatement (2026-11-10 20:40 CST)

QUESTION: Under the store clock (Piece 1), when a habit fails again, what happens to its older, faded failures?
- (a) Each keeps fading from its own time (per-event stamps, r1711).
- (b) All come back to full weight (one stamp per item, "reinstatement").
- (c) Isaiah 20:37: a REASSESSMENT, as a venture investor re-values a company.

DOMAIN CENSUS:
- R: arity 2 (one item; its failure events) · symmetry: failures with the same cause are interchangeable reports of one defect · scale: a step's events against a lifetime's record.
- Domains (actors / currency / anchor):
  - The agent's record: terms / refusal counts / the ground's verdicts.
  - The derived reading: presented weight / the share age / recomputed at read, never written.
- Order: the record first (upstream), then the reading derived from it.

TETHER (primary, verbatim):
- Fig 6 :42-43 "What is recorded only grows. What is reachable is derived, and it can fall." ... "So the closure and the reach are two quantities: one monotone, one not."
  - A reassessment is a re-derivation under everything now held. The record is untouched, and only the reading is recomputed.
- Fig 2 :31 "Independence, between two frames, is how little they draw on the same evidence. Two people reading the same report are not two frames"
  - Failures with the same cause draw on one defect: they are one pool. A new failure of that cause is evidence the defect is still there, so the old failures of that cause were not stale. Failures of another cause are separate evidence, and this one says nothing about them.
- Triangulated: Fig 6 and Fig 2, low overlap.

WORLD (secondary, each read):
- Venture capital. VC portfolio valuation (Bloomstine, beehiiv, read 2026-11-10):
  - "Calibration involves using the original transaction price to establish baseline valuation inputs", updated at each measurement date.
  - A markdown trigger: "Failure to meet key milestones that underpinned the prior valuation".
  - Predicts: a new miss re-prices what the value rested on, not everything ever recorded. Corroborates (c).
  - Also: a round over a year old no longer satisfies fair value on its own, so old valuations lose weight with time. Corroborates the fade itself.
- Credit scoring. myFICO, "Are all negative items equally bad?":
  - "The presence of recent delinquency is heavily weighted"; "A credit report reflecting multiple negative items is generally more risky."
  - Predicts: recency and the pattern both count, so a new miss makes the earlier ones read as a pattern. Corroborates (c) over (a). Says nothing on cause.
- Carta, down rounds 2023: "If the context for fundraising has changed, valuations can be expected to shift accordingly." A whole-context change re-prices all at once. That is the rarer case, and it maps to a new board or level, not a single failure.

VERDICT (from the figures): (c) REASSESSMENT BY CAUSE.
- A new failure re-derives the item's weight. Old failures of the SAME cause fade again from now, because the pattern is confirmed. Failures of OTHER causes keep fading from their own times.
- The record never changes.
- In the code the cause key already exists: Standing.refusals_on is keyed by slot. One stamp per (item, cause): presented = sum over causes of n_cause x 0.5^(age(W_last_cause)/h).
- This also bounds storage by the number of causes per item, not by events. That closes r1711's LIMIT.
- Cost if wrong: small. It sits behind TETHER_FADE_BY_STORE and can be undone.
- Reversed by: an e2e reading where reassessed failures keep a habit suppressed after its cause was fixed (a rise in refusals-then-vindications on the same slot).
- Status: proposed to Isaiah 20:40; not built until he says yes.

Sources:
- [Valuing early-stage startups in a VC portfolio](https://dannybloomstine.beehiiv.com/p/valuing-early-stage-startups-in-a-vc-portfolio-when-there-s-no-revenue-no-comps-and-the-last-round-w)
- [myFICO: are all negative items equally bad?](https://www.myfico.com/credit-education/blog/negative-items-equally-bad)
- [Carta: down rounds 2023](https://www3.carta.com/blog/down-rounds-2023)

---

## Part 2 (2026-11-10 20:45 CST): why reassess — different river, different man; who does the categorizing

Isaiah, 20:43, verbatim: "The reason why we re-assess is because the contact is different and the agent is different (you never step in the same river twice - different river, different man). By different, also think in terms of how we broke down contact into context earlier today. Also, that compression came from another past self of the agent. Its present self cannot guarantee that it would categorize something the same way as it would when it was less experienced. A fun house might scare a kid, but amuse an adult - WATSON this too"

QUESTION: When a new failure arrives, WHO decides which old failures share its cause: the label the past self stored, or the present self re-reading the raw contact?

DOMAIN CENSUS:
- R: arity 3 (the new failure's contact, an old failure's contact, the self reading both) · symmetry: none across selves (a past self's reading is not interchangeable with the present one's) · scale: lifetime.
- Domains (actors / currency / anchor):
  - The record: failure events / raw contact (slot, transition, cues) / the ground's verdict at the time.
  - The present reading: today's categorizer (kinds, delta kinds, later the catalog's clusters) / cluster membership / the next verdict.
  - The self over time: past and present selves / W (writes since) / the store clock.
- Order: the record (upstream) -> the present reading -> the derived weight.

TETHER (primary, verbatim):
- Fig 11 :49-50 "An actor's valence is relative to the residual, not a property it carries. The same actor is a benefactor to one residual and a malfactor to another"
  - The fun house: the same stimulus is a threat to one self and a game to another. A failure's weight is read against the present residual, not carried as a fixed property.
- Fig 4 :22-26 "Only methods cross up. Only head starts come down." ... "A recording carried upward looks like knowledge and is a description of one occasion."
  - A cause label written by a past self is a recording of one occasion. What crosses time is the METHOD (the present categorizer), applied to the raw contact.
- Fig 6 :42-43 "What is recorded only grows. What is reachable is derived, and it can fall."
  - Keep the raw contact (it only grows); derive the grouping and the weight fresh.
- Triangulated: Fig 11, Fig 4, Fig 6, low overlap.

WORLD (secondary, each read):
- Emotion. Appraisal theory (Lazarus; Wikipedia, "Appraisal theory"): "emotions are extracted from our evaluations (appraisals or estimates) of events"; it "accounts for individual variability in emotional reactions to the same event"; reappraisal is "appraising the emotional situation in a new way".
  - Predicts: the same contact carries a different weight for a different self. Corroborates.
- Development. Gullone, "Developmental Psychopathology and Normal Fear", Behaviour Change 13(3), 1996: "major changes in the content of normal fear over the course of development". Early fears are "largely noncognitive", to "immediate, concrete, and prepotent stimuli"; later ones respond to "anticipatory, abstract, and more global stimuli and events".
  - Predicts: what counts as the same kind of threat changes as the categorizer matures. The kid and the adult sort the fun house differently. Corroborates.
- Memory. Alberini, "The Role of Reconsolidation and the Dynamic Process of Long-Term Memory Formation and Storage", Front. Behav. Neurosci. 5, 2011: "Retrieval or reactivation of an apparently consolidated memory can render the memory labile again".
  - Its own conclusion is that reconsolidation mainly STRENGTHENS rather than rewrites: "the reconsolidation of the reactivated trace does not mediate this updating".
  - Predicts: re-reading changes the memory's present strength, not its stored content. Corroborates Fig 6's split (record kept, reading derived). Rewriting the record would conflict.

VERDICT (from the figures), REFINING Part 1:
- Each failure keeps its RAW contact with its W stamp: the slot, the transition, the contact cues. A reference to the record row is enough, since the ledger already holds it. The cause is not stored as a label.
- On a new failure, the PRESENT self re-reads the item's old failures through its CURRENT categorizer:
  - tonight, the kind and delta kind computed now from the raw transition;
  - later, the catalog's clusters.
- Old failures it now puts in the same context as the new one are reassessed: their fade restarts from now.
- The others keep fading from their own times.
- Nothing is written back. The grouping and the weight are derived at read time (Fig 6).
- "Different man" is already measured: the share age (writes since / memory now) is how much the agent has changed since that failure. The more it has grown, the less an old failure counts.
- Cost: reassessment runs only on a new failure, only over that item's failures, and under the purse (owed if unaffordable). Storage grows with events, which Fig 6 permits. Books report the largest list.
- Cost if wrong: small (arm). Undoable: yes.
- Reversed by: an e2e where the present categorizer groups failures that the ground later shows were unrelated (reassessed failures followed by vindications on the same item).
- Status: proposed to Isaiah 20:45; the seat holds this piece.

Sources:
- [Appraisal theory (Wikipedia)](https://en.wikipedia.org/wiki/Appraisal_theory)
- [Gullone 1996, Developmental Psychopathology and Normal Fear](https://www.cambridge.org/core/journals/behaviour-change/article/abs/developmental-psychopathology-and-normal-fear/F6A1B96612FF8586BE05EF6E58493566)
- [Alberini 2011, Reconsolidation](https://frontiersin.org/articles/10.3389/fnbeh.2011.00012/full)
