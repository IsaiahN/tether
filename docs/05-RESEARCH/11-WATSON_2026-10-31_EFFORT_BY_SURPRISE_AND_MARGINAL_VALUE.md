# WATSON 2026-10-31 19:10 CDT — Should the agent justify the time it spends, step by step?

Reviewer seat. Asked by Isaiah:
- 18:48: "Can the agent justify the time it spends based on the new data how drastic the change or effect from a previous change is and if they need to come up with strategy? As an llm you deal with this yourself you guage request by challenge lvevel etc and guage what level of reasoning is required system 0,1,2 etc. run a watson to get the answers we need"
- 18:49: "I believe that in somw scenarios it moght really need the time just like llms do, in other cases without proper justification theres no reason. Think predator pret innature or hunter gatherer in your watson as well or in a separate watson"

The figure lines are verbatim from docs/FIGURES_TEXT.md at general-agent 1e9d4d5. Every world source below was opened and read.

## QUESTION
Can each step decide for itself how much thinking it is worth, by how big and how unexpected the new evidence is, and by whether more thinking is still paying off? And can it tell when a whole line of work should be dropped for a new strategy? Three outcomes are possible:
- (a) every step thinks the same (today);
- (b) a fixed cap (a clock or a count);
- (c) effort is graded by the step's own reading, with no cap and no clock.

## THE FACTS THAT FRAME IT (seat, 2026-10-31)
- Rehearsal 1, 329 steps: median 38.6 s, p90 132 s, max 1,767 s. 307 of 329 steps had at least one failed prediction (a median of 8 failed slots). The 22 steps with no failure already cost 5.8 s, with lookup and invention near zero.
- Round 3, 25 games: 267 presses in 9,252 s, about 35 s a press, and 0 levels.
- The wa30 profile: ROUTE is 80% of the step, most of it re-judging terms against each failed slot's history. With arm 22 + lazy Ctx: median step 103.7 -> 75.8 s, and ROUTE -33%, exactly (ON = OFF).
- So today a small, expected deviation and a big, unexplained one get the same work. The graded gate proposed on 10-21 ("in the slot's own range = refit or hold, no lookup or mint") was never built.

## DOMAIN CENSUS
- **R:** arity 3 (the new evidence's surprise; the thinking it would cost; what that thinking could change in the next press); symmetry: misses differ in size and in kind, so they are not interchangeable; scale: step, line of work (one gap, one goal), game.
- **The gap (perception).** Actors: failed slots. Currency: the size of the miss against the slot's OWN recorded variability. Anchor: the frame.
- **The deliberation (search).** Actors: lookup, mint, plan. Currency: evaluations. Anchor: the step clock.
- **The board (contact).** Actors: presses. Currency: actions. Anchor: new contact and progress rows.
- **The strategy (a line of work).** Actors: a gap's version space, a goal hypothesis, a game. Currency: gap closed per evaluation spent. Anchor: the progress rows.
- **Union:** gap ∩ deliberation = the value of a computation: is this thinking worth more than the press it delays? That compound has its own loop.
- **Order (Fig 3):** gap -> deliberation -> contact -> strategy.

## TETHER (primary, verbatim)

**The gap: surprise is graded, and its size decides the work.**
- Fig 5 :10-14: "sort the gap into four kinds / held: the model was right, nothing owed / new: extend perception, aim the probe here / mis-attached: refit what you have, do not invent / mechanism broken: a new term is owed".
- Fig 4 :36: "What is not borrowed is using the size of the gap to decide" when a new term is worth minting.
- Fig 9 :53: "Nobody chooses. The gap does, and the gap is only as good as its description."
- So the gap's own description sets the level of work. No controller sits above the step (Isaiah 10-30: "humans dont have governor in their brains").

**The deliberation: thinking is a cost that must buy a press.**
- Fig 12 :126-127: "Actions price finding out whether it holds ... It proposes arrangements it cannot afford to test, and the budget is what decides how much of the space is reached at all."
- Fig 5 :43: "A new term is worth having when stating it, plus what remains unexplained after it, costs less than what was unexplained before."
- Fig 9 :43: "The verdict tells you to leave. The lookup tells you where to go. Elimination is what you do after you arrive."
- So a computation is worth running only if it can change what the agent does or knows by more than it costs. When only the board can decide, the right move is to press.

**The strategy: when effort stops shrinking the gap, change the question.**
- Fig 9 :4-5: "Disagreements that do not shrink with effort, where each rule keeps working well on a different subset, are not one hard question but several well-formed ones. Split it rather than search."
- Fig 5 :46, :48: "When nothing is scoring, the drive manufactures a gradient." / "A system can be enthusiastically curious and produce nothing."
- Fig 3 :10: "it can say what would count as progress here, in its own terms".
- So "change strategy" has a reading: effort is being spent and the gap is not shrinking. The answer is to split the question or leave it, not to search harder.

**Triangulated:** Figs 5, 4, 9, 12 and 3, with low overlap. The verdict is (c).

## WORLD (secondary; each source read)

**Animals, predator and prey.**
- **Chittka, Skorupski & Raine 2009, Trends in Ecology and Evolution 24(7):400-407.** "Obtaining high-quality information often increases sampling time, especially under noisy conditions." When errors cost little, "an adaptive foraging strategy could be one that is fast and error prone". When accuracy matters, "substantial time might need to be invested". "Errors can be substantially more costly when prey is potentially hazardous". Guppies from high-predation streams decided more slowly. House-hunting ants lower their quorum, deciding faster and less accurately, when the nest is destroyed.
 - Predicts: time per decision should scale with the cost of an error and the noise in the evidence, not be fixed. Most ARC presses are cheap errors (a level reset is allowed). Presses near a known death are not (the ruin record). Corroborates the gap and deliberation domains.
- **Charnov 1976, Theoretical Population Biology 9:129-136 (the marginal value theorem; via its Wikipedia summary).** A predator should leave a patch "when the marginal capture rate in the patch drops to the average capture rate for the habitat."
 - Predicts: a line of work (a gap, a goal, a game) is worth staying on while its gain per unit effort beats the agent's own running average across its other lines. When it falls below, leave. No constant: the threshold is the agent's own average. Corroborates the strategy domain, and gives Fig 9 :4-5's "do not shrink with effort" a measure.

**Hunter-gatherers.**
- **Liebenberg 2006, Current Anthropology 47(6):1017-1025 (persistence hunting).** "Systematic tracking involves following footprints where they are reasonably easy to see." "Speculative tracking involves the interpretation of signs" and "creating a hypothesis to explain what the animal is doing"; "the speculative tracker predicts where tracks will be found and then looks for them where they are expected." "Losing the tracks was the main reason the hunters gave up in unsuccessful attempts."
 - Predicts: two modes, switched by the evidence. When the trail is clear (predictions hold), move fast and do not theorise (System 0/1). When the trail is lost (prediction fails badly), stop and build a hypothesis, then look only where it says (System 2, then a keyed check). And giving up comes when the hypothesis stops finding tracks. Corroborates all four domains, and matches Fig 9's describe -> look up -> leave.

**Brains.**
- **Dayan & Yu 2002, NeurIPS 15 ("Expected and Unexpected Uncertainty: ACh and NE in the Neocortex").** Acetylcholine signals expected uncertainty; "norepinephrine reports the radical divergence of bottom-up inputs from prevailing top-down interpretations."
 - Predicts: noise the model already expects should not trigger revision. Only a radical divergence should. That is Fig 5's held / mis-attached vs mechanism broken. Corroborates the gap domain.

**Machines (Isaiah's LLM point).**
- **Russell 1997, MIT Encyclopedia of the Cognitive Sciences, "Metareasoning".** A computation is an action: its benefit is better external decisions, its cost the delay. The metalevel decides "which computations to do and when computation should give way to action."
 - Predicts: think only while the expected improvement in the next press exceeds the delay. Corroborates the deliberation domain.
- **Snell, Lee, Xu & Kumar 2024, arXiv:2408.03314.** Test-time compute "acts to most effectively allocate test-time compute adaptively per prompt". Compute-optimal allocation is ">4x" more efficient than best-of-N, and can beat a 14x larger model on problems of middling difficulty.
 - Predicts: Isaiah's point. Some problems truly need much more thinking, and giving it to them pays. Spreading it evenly wastes most of it. Corroborates (c) over (b).
- **De Sabbata, Sumers, AlKhamissi, Bosselut & Griffiths 2024, arXiv:2410.05563 ("Rational Metareasoning for LLMs").** It trains models "to use intermediate reasoning steps selectively when they are likely to be beneficial", with a reward that "penalizes unnecessary reasoning". The result: "23-45% fewer tokens", with performance kept or raised.
 - Predicts: graded effort costs nothing in quality when the grading reads the problem. Corroborates (c).

**No conflict between the figures and the world.**

## VERDICT (from the figures)
**(c): each step's effort is graded by its own reading. There is no clock and no fixed cap, and a step may take long when its reading justifies it.**

Three levels, chosen by the gap, never by a governor:
1. **System 0: held or in range.** The miss is within the slot's own recorded variability (expected uncertainty, Fig 5 :11/:13). Record it, refit only by the cheap check, press. No lookup, no mint. This is the tracker on clear spoor.
2. **System 1: out of range but recognised.** The miss is outside the slot's range, and its description keys to the library. Make one keyed lookup and a one-pass check, bind, press (Fig 9 :29, :43).
3. **System 2: unexplained, large and compressible.** Nothing keys to it (mechanism broken, Fig 5 :14), and the gap is large and compressible (Fig 5 :18, :43). Here the agent IS justified in taking real time: the mint, a plan, a hypothesis to test. This is the tracker who has lost the trail, and the LLM on a hard prompt. It is the case Isaiah says may truly need the time.

**One rule for staying or leaving (strategy):** every line of work keeps its own gain per evaluation (bits explained, or gap closed, per evaluation spent). It continues while that rate beats the agent's running average over its lines. Below the average, it leaves with a verdict row: split the question (Fig 9 :4-5), press to get new evidence, or move to another gap or goal. The same rule decides when to leave a game (Isaiah's "replay until it wins", bounded by Charnov). The threshold is the agent's own average, never a chosen number.

**Cost if wrong:**
- in-range misses that hid a real change get no lookup. The first out-of-range miss on the same slot routes it, so the cost is a step's delay;
- a line of work left too early. It stays recorded and is reachable again when its gain rate rises (Fig 9 :41, "ranked and reversible").

**Undoable:** yes, one arm per level and one for the leave rule, default ON, OFF byte-equal.

**Reversed by:** the measurement below showing that in-range misses DO produce binds and accepts as often as out-of-range ones (then the range is not the line), or levels falling when the leave rule is ON.

## ADDENDUM 19:03: ISAIAH'S SYSTEM 0 GAUGE
Isaiah, 19:00: "I feel like system 0 takes like <5 seconds not to put magic numbers on things but as a guage its a gut instinct almost subconscious or automated patter n matching novelty seeking like explorer am i wrong let me know if we need to watson that too".
- **Not wrong; it is already this WATSON's System 0.** The tracker on clear spoor (Liebenberg), and expected uncertainty that triggers no revision (Dayan & Yu). Novelty seeking is Fig 5 :12 and :15-17: "new: extend perception, aim the probe here" and "the curiosity drive / fires when nothing is scoring / aimed at the new bin". It is a press, not a deliberation.
- **The data sit near his gauge where System 0 already happens.** Rehearsal 1's 22 steps with no failed prediction had a median of 5.8 s.
- **The mismatch is in the label.** Steps whose exit is "system0" (explore unexplored contact) had a median of 36.3 s. The exit is the explorer, but each step still pays the full lookup and mint for every miss the last press left. System 0 as he means it is the exploring press PLUS in-range misses only noted.
- **The gauge stays a gauge.** Under 5 s is reported as a share of steps, never a cut in code (no clock in reasoning).
- **No separate WATSON is needed.** The question is the same quantity: effort graded by the gap. The seat's read m4 (r576) measures it.

## ADDENDUM 20:30: THE FIRST MEASURES (seat 20:17 and 20:20), AND A CORRECTION
- **m1 fired this WATSON's own reversal condition.** With "in range" read as either a value the slot has already shown (SEEN) or a value within the slot's earlier min-max (SPAN):
 - in-range misses are 30-39% of misses and take 39-45% of the lookup and invention seconds;
 - but they bind about as often as out-of-range ones (0.07-0.22 binds per miss, against 0.10-0.22).
 - So that range is NOT the line between System 0 and System 1, and arm 24 is not built on it. The verdict (graded effort) stands. Its first proposed measure of the grade does not.
- **The bigger finding:** across all of that search, settles were 0-8 per worker and accepts 1 in total. Lookup and invention are 94-98% of every step over 60 s. Nearly all the time buys temporary binds that rarely become settled knowledge.
- **m3 could not be answered from the ledger.** Did the thinking change the press? The ledger records only the press taken. The seat did not guess.
- **Next measure, the one that decides it (r582):** a record-only probe (arm 27) of the press the step would make BEFORE lookup and invention, against the press it made after. Where thinking rarely changes the press, it is not worth its seconds. That is Russell's value of computation, read from data. The System 0 / 1 / 2 line will be drawn from it, not from a chosen range.
- **m2 (slots):** 13-26% of a slot's evaluations come after its last gain, and 8-18% go to lines that never gain. Lines that gain are mostly left once they hold. The marginal-value leave rule has that much to act on, at most. Goal-hypothesis lines are still to be read.
- **m4 (Isaiah's gauge):** in steps labelled system0, the agent's own thinking (perceive and plan) is 1-3 s, already under 5 s. The other 23-58 s is lookup and invention on misses. Only 0-17 of 19-57 such steps had all their misses in range. Share of all steps under 5 s: 3-11% in rehearsal 1, 30 of 267 (11%) in round 3.

## MEASURE BEFORE BUILDING (read-only, on rehearsal 1 and round 3's ledgers)
- m1. For every failed slot: its miss against the slot's own recorded variability (in range vs out, from the slot's history; no constant). Count each class, the ROUTE and MINT seconds spent on each, and the binds, settles and accepts each produced.
- m2. Per line of work (a slot's version space, a goal hypothesis): evaluations spent vs bits explained or gap closed, step by step, to see whether the gain rate falls and when.
- m3. Steps where the agent spent over 60 s: what level the gap was, and whether the press that followed differed from the press the step would have made without the thinking.
If m1 shows in-range misses rarely bind but cost a large share of the time, System 0 is the lever (arm 24). If m2 shows long tails of low-gain effort, the leave rule is (arm 25).

## Sources
- [Chittka, Skorupski & Raine 2009, Speed-accuracy tradeoffs in animal decision making, TREE (PDF)](https://repository.royalholloway.ac.uk/items/badd34de-b90a-c5fd-88ea-9d57609ef565/7/Chittka_etal_2009_TREE.pdf)
- [Marginal value theorem (Charnov 1976), Wikipedia](https://en.wikipedia.org/wiki/Marginal_value_theorem)
- [Liebenberg 2006, Persistence Hunting by Modern Hunter-Gatherers, Current Anthropology (PDF)](https://originalwisdom.com/wp-content/uploads/bsk-pdf-manager/2019/05/Liebenberg_2006_PersistenceHuntingByModernHunterGatherers.pdf)
- [Dayan & Yu 2002, Expected and Unexpected Uncertainty: ACh and NE in the Neocortex, NeurIPS](https://proceedings.neurips.cc/paper/2002/hash/758a06618c69880a6cee5314ee42d52f-Abstract.html)
- [Russell, Metareasoning, MIT Encyclopedia of the Cognitive Sciences (PDF)](https://aima.eecs.berkeley.edu/~russell/papers/mitecs-metareasoning.pdf)
- [Snell et al. 2024, Scaling LLM Test-Time Compute Optimally, arXiv:2408.03314](https://arxiv.org/abs/2408.03314)
- [De Sabbata et al. 2024, Rational Metareasoning for Large Language Models, arXiv:2410.05563](https://arxiv.org/pdf/2410.05563)
- docs/FIGURES_TEXT.md at 1e9d4d5 (Figs 3, 4, 5, 9, 12); claude/DERIVATION_2026-10-21_WATS_graded_surprise_lookup_invent_memory.md (the 10-21 gate, never built)
