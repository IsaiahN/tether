# WATSON 2026-10-30: fast and accurate reasoning that keeps its human origin

Reviewer, 09:18 CDT. Isaiah, 09:17:

> "lets do a watson on how a human would handle this. the agent has superior recall, and access to the tether itself, its reasoning capabilities can far than a human (you llms are proof of that), so we must find out how to make it reason accurately yet faster while still retaining its human prior origins and its human like reasoning"

"This" is PLAY21's measured slowdown (r423, r424):
- PERCEIVE per step grows along a round, in both PLAY20 and PLAY21. ls20 takes 1.1 s at 5th place but 21.9 s at 24th.
- The owed paths (CONTACT_FIRST, ROUTE_NAMED) save about 10-15 s on a named step, but only 7 of 109 steps are named.

## QUESTION

How should a mind with perfect recall keep each decision fast and still accurate, as what it holds keeps growing? What does each option lead to?

## DOMAIN CENSUS

- **R:**
  - **Arity:** three. The step's reading, the record it consults, and the ground that settles.
  - **Symmetry:** two objects of one kind are interchangeable; two games at the same position in a round are not.
  - **Scale:** step, then game, then round, then lineage.
- **Domains** (actors / currency / anchor):
  - **(a) Perception in the step.** The board's change against the expected board / what passes up / the per-slot residual (Fig 1).
  - **(b) Recall in the step.** The record and the index into it / time per lookup / the record's size against the step's cost.
  - **(c) Keeping across boundaries.** Game to game, and round to round / what crosses / the membrane (Fig 4).
  - **(d) Prior and history.** The inherited human prior and the agent's own record / w / the belief b (Symbols).
- **Order:** (a) feeds (b), and (b) is shaped by (c). (d) mixes into (b) at each step.

## TETHER (primary, verbatim, from docs/FIGURES_TEXT.md at e7a1c8e)

**(a) What passes up**
- Fig 4 :21-22: "Not a wall: a filter with a direction. Only methods cross up. Only head starts come down."
- Fig 4 :27: "The transform between scales loses information, and that is the point."
- Fig 1 :19, :22: "The residual is indexed by object slot, not aggregated." / "Aggregating across slots is how a live signal disappears into an average."
- So what reaches reasoning is the per-slot residual (what did not go as expected), not the whole board. That is Isaiah's "EM waves vs colour": colour is the compressed reading that crosses.

**(b) Looking up versus searching the record**
- Fig 12 :107-108: "where the arrangement is recorded, re-deriving it is a lookup and the actions were spent once."
- Fig 9 :29: "matching is a one-pass check, not a search".
- Fig 9 :45: "Describing the residual is the expensive part. Leaving, looking up and recognising are one step each, and cheap only in that order."
- Fig 6 :42: "What is recorded only grows. What is reachable is derived, and it can fall."
- Fig 12 :104: "A settled molecule becomes an atom for whatever composes over it."
- So recall should cost one step per lookup, whatever the record's size. A step whose cost grows with the record has turned a lookup into a search.
- Keeping everything is right; consulting everything is not.
- Settled arrangements should be held as single units (atoms), so the next composition has fewer, larger parts.
- **Triangulated:** Figs 12, 9 and 6.

**(c) Across boundaries**
- Fig 10 :68-69: "a generator crosses, an instance does not, and the level it lands on remakes it."
- Fig 4 :23-24: "upward: a method that can be reapplied. Never the recording of a particular success. downward: something that makes the next search cheaper."
- Fig 12 :109-110: "Inside a run the arrangement persists and nothing is re-earned; across a boundary that drops it, everything is."
- So at a game's end, the kinds and methods carry forward. The per-game instances (object ids, this board's pairs) should not be carried as working state into the next game's per-step work.
- **Triangulated:** Figs 10, 4 and 12.

**(d) The human prior**
- Symbols :20-21, :24-26: b is "Formed from its own history and from what it inherited, mixed by w." w "is learnable from the outcomes of past weightings. Two frames with identical architecture diverge because their histories and their w diverge."
- Fig 9 :32, :42: "you get a kind of thing, never the answer itself" / "narrowing gets you close, the ground decides".
- So speed comes from recognition (the lookup), and accuracy comes from the ground (contact).
- The human prior is the inherited half of b. Speed must not be bought by dropping it; it is a weighting, and w is learned.
- **Triangulated:** the Symbols table and Fig 9.

**Strain test:** each line governs the quantity in question: per-step cost against what is held, and what crosses a boundary. No re-census was needed.

## WORLD (secondary; each source was read)

- **Human memory: the fan effect.**
  - Source: Anderson 1974, Cognitive Psychology 6:451-474 (via the Wikipedia summary and its citations).
  - What it found: "recognition times or error rate for a particular concept increases as more information about the concept is acquired."
  - The remedy it reports: "The fan effect can be reduced if random sentences are exposed frequently and unified into one concept" (Moeser 1979).
  - **Prediction:** a human also slows as facts pile onto one thing, and recovers by integrating them into one unit. That is the agent's PERCEIVE climb, and its remedy is Fig 12 :104.
  - **Corroborates (b).**
- **Skill acquisition: automaticity as retrieval.**
  - Source: Logan 1988, Psychological Review 95:492-527.
  - "Automaticity is memory retrieval: Performance is automatic when it is based on single-step direct-access"
  - "a race between memory and the algorithm—whichever finishes first controls the response."
  - The speed-up with practice "follows a power function".
  - **Prediction:**
    - More experience should make a step faster, because retrieval wins the race more often.
    - The agent shows the opposite, slower with more held. So its retrieval is not single-step direct access; it scans.
    - The human design runs both, the lookup and the derivation, and the first to finish answers. That is CONTACT_FIRST / ROUTE_NAMED's shape, but here they fire on only 7 of 109 steps.
  - **Corroborates (b) and (d).**
- **Rational memory: availability tracks need.**
  - Source: Anderson & Schooler 1991, Psychological Science 2.
  - "Availability of human memories for specific items shows reliable relationships to frequency, recency, and pattern of prior exposures to the item … the environmental relationships are the same as the memory relationships."
  - **Prediction:** human "forgetting" is not loss. It is ranking by expected need, so the likely item is reached first.
  - For a perfect-recall agent, the analogue is to keep the record whole (Fig 6 :42) but order what a step consults by recency and frequency of use. The reach can fall; the record cannot.
  - **Corroborates (b) and (c).**
- **Expertise: chunks.**
  - Source: Simon & Chase 1973, "Skill in Chess", American Scientist 61:394-403.
  - "The acquisition of chess skill depends, in large part, on building up recognition memory for many familiar chess patterns."
  - On random positions "all players, from master to novice, recalled only about three or four pieces on the average".
  - "a chess master can recognize at least 50,000 different configurations of pieces on sight".
  - **Prediction:** experts are fast because they look up larger units by pattern, not because they search faster.
  - **Corroborates (b),** Fig 12 :104.
- **Vision: predictive coding.**
  - Source: Rao & Ballard 1999, Nature Neuroscience 2:79-87.
  - "feedback connections … carry predictions of lower-level neural activities, whereas the feedforward connections carry the residual errors".
  - "This reduces redundancy by removing the predictable, and hence redundant, components of the input signal."
  - **Prediction:** perception's cost should scale with what is surprising, not with what is held or what is on the board.
  - **Corroborates (a),** Fig 1 :19 / Fig 4 :21.
- **Sleep: downscaling.**
  - Source: Tononi & Cirelli 2006, Sleep Medicine Reviews 10:49-62.
  - "plastic processes occurring during wakefulness result in a net increase in synaptic strength".
  - "The role of sleep is to downscale synaptic strength to a baseline level that is energetically sustainable".
  - Downscaling "could benefit learning … by increasing signal-to-noise ratios."
  - **Prediction:** a brain that only accumulates during waking gets costlier and noisier. The boundary (sleep) is where working state is renormalised, while what matters is kept.
  - **Corroborates (c),** Fig 12 :109 and the project's own DERIVATION 10-18 (consolidation at boundaries).

**No conflict.** Every world source predicts what the figures already say.

## VERDICT (from the figures)

**One rule: a step's cost must scale with its residual (what changed or surprised), never with the size of the record.**
- Perfect recall is an advantage only while recall is a lookup (Fig 12 :107-108, Fig 9 :45).
- PLAY21's climb (the same game 1 s at 5th, 22 s at 24th) is the measured sign that some per-step work is scanning what the agent has accumulated. That is the fan effect, built into code.

What this means, stated as readings and candidates, not orders. Each waits on B2 to name what grows.

1. **(a) Perception passes up the residual only.**
   - Compare the board against what was expected, per slot (Fig 1). Only changed or surprising slots go up for reasoning.
   - Unchanged slots reuse last step's reading, held by kind (Rao & Ballard; Fig 4 :21).
2. **(b) Recall is a lookup keyed by kind, ordered by need.**
   - Keep the whole record (Fig 6 :42; the agent's superior recall is kept).
   - Each step's lookup is keyed by the live residual's kind (Isaiah's "kind, never id tag"), so its cost is one step (Fig 9 :29).
   - Where several entries answer, they are ordered by recency and frequency of use (Anderson & Schooler). That is the human "forgetting", done as ranking, not deletion.
3. **(b) Chunk what has settled.**
   - A settled arrangement becomes one atom for what composes over it (Fig 12 :104; Simon & Chase; Moeser on the fan effect).
   - Fewer, larger units are faster to recognise and keep accuracy, because a chunk is only kept once it has settled against the ground.
4. **(c) Renormalise at the game boundary.**
   - Kinds and methods cross. Per-game instances (ids, this board's pairs, per-object histories) are dropped from the working set at the game's end (Fig 10 :68; Tononi & Cirelli).
   - The lineage record is untouched. Only the per-step working set is reset.
5. **(d) Keep the human shape: recognise first, derive when recognition fails, let the ground decide.**
   - Lookup and derivation race (Logan), and the first to finish answers.
   - Contact settles it (Fig 9 :42), so speed never costs accuracy. A wrong recognition is refuted by the next board and costs one act, not a wrong belief.
   - The inherited prior stays in b, weighted by a learned w (Symbols). CARRY_W is this.
   - What makes it more than human is that its recall is complete and its w is measured, not guessed.

**Cost if wrong:** effort aimed at the store when the climb comes from something else (e.g. game order). B2 tests that first.

**Undoable:** every candidate above would be an arm with OFF identity.

**Reversed by:** B2 showing PERCEIVE flat when one agent is carried through 4 games. Then the climb is the game order, not accumulation, and (b)/(c) are not the lever.

## Sources

- [Anderson 1974, fan effect (Wikipedia summary with citations)](https://en.wikipedia.org/wiki/Fan_effect)
- [Logan 1988, Toward an instance theory of automatization, Psychological Review 95:492-527](https://pcl.sitehost.iu.edu/rgoldsto/courses/cogscilearning/loganautomaticity.pdf)
- [Anderson & Schooler 1991, Reflections of the environment in memory, Psychological Science](https://www.psychologicalscience.org/journals/psychological-science/j.1467-9280.1991.tb00174.x/)
- [Simon & Chase 1973, Skill in Chess, American Scientist 61:394-403](https://www.Gwern.net/doc/psychology/chess/1973-simon.pdf)
- [Rao & Ballard 1999, Predictive coding in the visual cortex, Nature Neuroscience](https://www.cs.utexas.edu/~dana/nn.pdf)
- [Tononi & Cirelli 2006, Sleep function and synaptic homeostasis, Sleep Medicine Reviews](https://www.psychiatry.wisc.edu/courses/Nitschke/seminar/tononi%20&%20cirelli%202006%20sleep%20medicine%20reviews.pdf)
- docs/FIGURES_TEXT.md at e7a1c8e: Fig 1 :19-22; Fig 4 :21-27; Fig 6 :42; Fig 9 :29, :32, :42, :45; Fig 10 :68-69; Fig 12 :104, :107-110; Symbols :20-26
