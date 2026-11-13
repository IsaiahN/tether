# WATSON 2026-10-26 08:29 CDT: the switched-off limbs, and a look-back that knows when to stop

## Isaiah, verbatim (08:24 CDT)

> "Turning off a feature is like cutting off a limb. It should be done with extreme scrutiny after perusing any other options. You may need to revamp the history window to work better with the new system and not overpower. It's in a similar position to overthinking versus when action is better, and some sort of reasoning in that vein should hamper it. You can run a WATSON on these if you prefer, to see what's useful or needed from the other 6 versus what's not, and if any others are needed, how they should adapt to the current umwelt."

## QUESTION

There are 22 OFF switches at 2e77f16 (arms.py: 236 switches, 214 ON).

- Which are limbs (behaviour) and which are instruments?
- For each limb:
  - keep it off;
  - turn it on as is;
  - or adapt it to the Umwelt build and turn it on.
- How should the history window be governed so that looking back never overpowers acting?

## RECORD (read at 2e77f16, conform/arms.py rows and code sites)

**Instruments: 15.** Off in play by design. These are not limbs.

- **14 \*_CHECK switches and W_EVICT_EVERY_STEP.** Each recomputes a shortcut the slow way and asserts that the two answers are equal. Each row says "a measurement switch for check runs, never a play setting."
- **HOLD.** It withholds an offer on a seeded half of occasions. The row says: "OFF in the shipping agent: a control that changes what the agent is OFFERED is an instrument."

**Behaviours: 7.**

| Switch | What it does | Why it is off (recorded) |
|---|---|---|
| WINDOW (tether.py:537; offer :15024-15043; rounds :15357-15376) | offers slot~j (j frames back) as an operand | MEASURED (7 members, 60 cycles): 5 slots that paid OFF never pay ON. Crowding: 5 of 6 lost slots never reached their OFF winner. The two-pass fix (2b) brought chains back, but the no-evidence lags went unreached (3,306-16,452 beyond-bound per member). The 2c trade is parked. |
| DELTA_OPERANDS (:500; _delta_narrowed; sites :9703, :14957) | bounds the operand set by what moved in the wrong frames | "IT EXCLUDES ... a cut, not an ordering"; "the version that DROPPED operand-reading terms ... LOST A CLOSING TERM" |
| TYPED_BIND (:144; site :10043) | refuses a binding whose head does not accept the slot's type | "tn36 loses its objective" (flip list 10-15); "those slots may simply lose their objective" |
| STREAM_WIDEN (:1974; site :15405) | adds mint streams for each type the delta lights | "refuted, INDEX 46590" (flip list 10-15). That refutation was on 09-23, before D2 STREAM_SHARE (10-12, ON). The H-budget finding (10-12) shows one shared budget starving the later streams. |
| MEMO_ADMIT | memo stores on the second ask | measured: saved 17 entries (fake) / 6 (gridworld) and cost 364 late recomputes |
| NOT_ATOM | prices not-t as one atom slot | a VARIANT: the figures leave the price open; the default is the other branch |
| WANT_TARGET_SUBJECT | narrow fallback | "With TETHER_WANT_TARGET also ON, the full unmask subsumes it" (WANT_TARGET is ON) |

## DOMAIN CENSUS

**R.** Arity 3: the residual, the search that would explain it, and the action that would test it. The search and the action are not interchangeable: they are priced in different currencies. Scales: the step, the mint call, the level.

| Domain | Actors | Currency | Anchor |
|---|---|---|---|
| SEARCH | mint streams, bindings, lags | work budget (rank), i.e. bits and compute | a closer: cost + left < base |
| ACTION | choose / act / probe | steps, and the risk of a death | the ground's answer (o′, progress) |
| PERCEPTION (the Umwelt) | trace, reafference (2a), surprise (5a), contact (2b) | what is offered for search | the observation |

- **Union SEARCH ∩ ACTION** is the seam where overthinking lives: Fig 12's two currencies.
- **Order (Fig 3):** perception (what is offered) → search (how far) → action.

## TETHER (primary, verbatim)

**SEARCH: cuts must be ranked and reversible.**

- Fig 9 :40-41: "a wrong cut removes the answer and speeds up / so keep every cut ranked and reversible"
- Fig 9 :60: "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict."
- What this decides here: DELTA_OPERANDS and TYPED_BIND each lost an answer because each was a CUT. The same code's own comment (:14951-14955) says: "ORDERING, NEVER EXCLUSION ... order decides WHICH closer is found and never WHETHER one exists." So the repair is to rank, not to refuse.
- Triangulation:
  - Fig 6 :49-50 "more search at the same reach ... Fails by spending budget on a region already swept. Distribute the search, and keep the searchers independent" (that is STREAM_WIDEN and the window's crowding);
  - Fig 6 :53-54 "searchers drawing on the same evidence are one searcher wearing many names."
  - Verdict: TRIANGULATED (Fig 9, Fig 6).

**SEARCH ∩ ACTION: when to stop looking and act.**

- Fig 12 :125-130: "A composition costs in two currencies, and they do not add. Bits price the description. Actions price finding out whether it holds. ... It proposes arrangements it cannot afford to test, and the budget is what decides how much of the space is reached at all. ... A long chain of cheap parts is expensive to describe and may cost one action to refute. ... Neither figure predicts the other, so both are read or the choice is made blind. Summing them into one figure is the error this names, not the fix for it."
- What this decides here: the look-back is description-side work, priced in bits. Whether an earlier frame matters can sometimes be settled by one action. So the window must read BOTH prices and choose by which is cheaper, held apart (never one summed score). That is Isaiah's overthinking-versus-action, in the figure's own words.
- Fig 5 :12-13: "new: extend perception, aim the probe here / mis-attached: refit what you have, do not invent". A look-back extends perception backward. It is owed only for the "new" kind of gap (nothing in the present frame can explain it). It is not owed when a present binding fits.
- Fig 9 :27-28 "describe it before you go looking, or any frame you pick will seem to fit" and :53 "Nobody chooses. The gap does, and the gap is only as good as its description." A lag is offered because the residual's description calls for it (recurrence evidence), never wholesale.
- Verdict: TRIANGULATED (Fig 12, Fig 5, Fig 9).

**PERCEPTION.**

- Fig 5 :12 "aim the probe here".
- The Umwelt build already supplies three inputs:
  - what the agent itself moved (2a reafference);
  - where surprise points (5a);
  - which actions can touch which objects (3a/3b/3d).
- The look-back and the operand ranking should read these.
- Verdict: single-source on the figure line, anchored in the built code.

## WORLD (secondary; each source read)

- **AI / decision theory.** S. Russell, "Metareasoning" (MITECS entry, 1997): "A computation can be viewed as an action whose benefit is that it may result in better external decisions", and the metalevel decides "which computations to do and when computation should give way to action." This predicts that deliberation has a cost (the delay) and must stop when acting is better. It CORROBORATES Fig 12.
- **Neuroscience (human and primate decisions).** Ferrucci, Genovesio & Marcos, PLoS Comput Biol 2021, on the Urgency Gating Model (Cisek, Puskas & El-Murr 2009): "an urgency signal that increases over time, reflecting the increasing need to make a decision as time passes"; "less sensory or accumulated evidence ... is needed to make a decision as time passes." This predicts that the longer it goes without progress, the less look-back is warranted before acting. It CORROBORATES gating the window by 6d's urgency.
- **Animal learning.** "Taste, Sickness, and Learning", American Scientist 2015 (on Garcia's work): rats "acquired an aversion to the saccharin solution even when the injection was delayed by as long as 75 minutes", and "it also depended on which specific types of cues were paired with which specific types of consequences". This predicts that long look-backs are made selectively, for the kind of cue that has evidence of mattering, not uniformly. It CORROBORATES evidence-first lags, ordered by kind and by surprise.

No source conflicts with the figures.

## VERDICT (from the figures)

### Limbs to adapt and turn back ON

**L1. The history window, governed: "the look-back".** WINDOW, revamped. Default ON.

- **(a) Its own share.** Lag bindings draw from their own stream share under the D2 rule: the least-spent takes the next candidate, and each stops at its own floor. They never take rank from the present-frame bindings. The measured loss was crowding (5 of 6 lost slots never reached their OFF winner).
- **(b) Evidence lags only.** Only lags with recurrence evidence (_lag_evidence) are walked. No-evidence lags are counted (window_beyond_bound) and not walked. They are the overthinking tail.
- **(c) Order inside the evidence lags:**
  1. frames where the agent's OWN action moved the slot's object (2a's reafference record: what I did is the likeliest cause of a delayed effect);
  2. then slots that surprise nominated (5a);
  3. then nearest first.
- **(d) THE GATE: think or act.** Two currencies, held apart; no new constants. The look-back runs on a slot only when all of these hold:
  - (i) No present-frame binding closed in this mint (Fig 5: the gap is "new", not "mis-attached").
  - (ii) 6d's urgency (steps since progress) is below the commit bar it already uses. Once urgency crosses the bar, the agent acts instead of looking back.
  - (iii) No untried affordance can test the slot's object first. If 3d's cheap probe (or any untried action of a kind that reaches that object, 3b) is available, the probe goes first, because one action may refute what a long search would describe (Fig 12 :128). The look-back runs on the next mint if the probe left the gap open.
- **(e) Depth.** j is at most the largest lag with evidence, and at most 4f's effect window where a bound term reads a lag. There is no free constant.
- **(f) Rows.** window_gate gives the reason a look-back was skipped (closer_found / urgent / probe_first), plus window_reached and window_beyond_bound per mint. Under the window, ~1 stays one lag of the block (:14964).

**L2. DELTA_OPERANDS, as an ordering.** Default ON.

- `_delta_narrowed` returns an ORDER over all candidates, at both sites (_bindings :14957 and _rebindings :9703):
  1. world-moved slots (moved, minus 2a's reafferent set);
  2. then self-moved slots;
  3. then contact partners;
  4. then every other slot.
- The budget makes the cut (Fig 9 :60). A closer cannot be lost by construction. The cost goal (the 1.5M operand binds on sk48) is read per round as operand binds per cycle and wall time.

**L3. TYPED_BIND, as an ordering.** Default ON.

- A binding whose head does not accept the slot type is walked LAST (a late round, like the derived binds' round 3). It is never refused.
- tn36's objective stays reachable.
- Row typed_late: how many were walked late, and whether any of them closed. That second count names the type check's own error.

**L4. STREAM_WIDEN, under the share.** Default ON, with its own pre-registered abort criteria read per round.

- The 09-23 refutation was measured under one shared budget, before D2 STREAM_SHARE existed. The condition has changed.
- The widened streams draw only after both base streams reach their own floor, and are ranked after them.
- Abort criteria (unchanged, from :1971-1973): candidates tried rises while arrivals do not; calls per cycle steepen; binds per candidate rises. Any of these on the round lines switches it OFF, recorded as a result.

### Not limbs: leave OFF and say why

- **MEMO_ADMIT.** It is a caching policy, not a capability. OFF = store on the first ask, which is the working memo. It was measured to save almost nothing and to cost recomputation.
- **NOT_ATOM.** This is the other branch of an open price. The agent prices not-t by its default, so nothing is cut off.
- **WANT_TARGET_SUBJECT.** Subsumed by WANT_TARGET (ON).
- **The 15 instruments.** They must stay OFF in play, or every reading measures the instrument.

### Missing, and needed

**One governor for all deliberation extensions.** Gate (d) is the general rule, not a WINDOW detail. Every search extension uses the same gate:

- the look-back;
- the widened streams;
- the typed-late round (L3).

The existing derived-bind round (B2b round 3) is ON and measured, and it is left as it is: gating it would change a working limb, which this ruling does not do.

Each is walked only while the residual is unexplained and urgency is under the commit bar, with an available probe going first. This is "when computation should give way to action" (Russell), in the agent's own units. It uses no wall clock. It is ONE function returning (walk, why), why in closer_found / urgent / probe_first / ok, under one arm TETHER_THINK_OR_ACT (default ON; OFF = the extensions walk ungated).

Posted to the seat as r249 (Drive 1X7hhwl4, 13:30:22Z), built on wip/limbs from 8314ed6 beside PLAY12.

### Cost, undo, reversers

- **Cost if wrong:** wall time per cycle rises with no reach gain, or a slot that paid stops paying.
- **Undoable:** yes. Each piece has its own switch.
- **Reversed by**, on the round lines:
  - L1: slots paid fall against the rounds without the window, OR window_gate shows "urgent" skipping while levels stay 0 and wall rises;
  - L2 and L3: wall up with no closer gain;
  - L4: its own three abort criteria;
  - the governor: a level that was won without it is lost with it.

## Sources

- [Russell, Metareasoning (MITECS)](https://aima.eecs.berkeley.edu/~russell/papers/mitecs-metareasoning.pdf)
- [Ferrucci, Genovesio & Marcos 2021, The importance of urgency in decision making based on dynamic information](https://pmc.ncbi.nlm.nih.gov/articles/PMC8516247)
- [Taste, Sickness, and Learning, American Scientist 2015](https://www.americanscientist.org/node/3670)
