# WATSON 2026-11-08 -- Tie-breaks without luck: the 2nd and 3rd readings at every draw site

Asked by Isaiah, 10:02 CST: "If by draw you mean random draws for these those are like last resort and should only happen when agent attempts something or encounters unknowns. Humans and animals never work this way. Try to do a watson to fill in the gaps on the second and third test metrics for each".

## QUESTION

Eleven sites in the agent end in the seeded hash draw (r1476). For each one: what should the agent read SECOND and THIRD, before any draw? And when, if ever, is a draw legitimate?

## DOMAIN CENSUS

- **R:** relates options x readings x outcome. Its arity is one choice among k options. It is not symmetric: the options differ, but the readings tie. Its scale is per decision, credited per game.
- **The agent's record:**
  - actors: options and their kinds;
  - currency: endings (paid / parked / refuted);
  - anchor: the ledger.
- **The board:**
  - actors: objects and values;
  - currency: what is present and in contact now;
  - anchor: the frame.
- **Cost:**
  - actors: options;
  - currency: bits (to state) and actions (to settle);
  - anchor: compile size and expected test length.
- **Order (Fig 3):** the board and the cost are read before choosing; the record is written by the ending and read at the next choice.

## TETHER (primary, verbatim)

1. **Fig 12 :125-130.** "A composition costs in two currencies, and they do not add. Bits price the description. Actions price finding out whether it holds ... Neither figure predicts the other, so both are read or the choice is made blind ... A price in bits and a price in actions are two readings, held apart."
   - So: COST is a reading, in two currencies, held apart as a frontier and never summed. frontier_pick already does this at the _choice sites. It must be added wherever only one currency, or neither, is read.
2. **Fig 7 :35.** "Selection between rooms is where the ground votes."
   **Symbols :20-26.** The belief comes "from its own history and from what it inherited, mixed by w".
   - So: the RECORD of how this option, or this kind of option, ENDED is a reading. Own history and inherited history are mixed by w (Isaiah 09:57: the agent uses its past history).
3. **Fig 9 :43-45.** "The verdict tells you to leave. The lookup tells you where to go ... Leaving, looking up and recognising are one step each, and cheap only in that order."
   - So: before searching blind, LOOK UP what is already on the board or in the store. A value, press or chain that is present or in contact now is read before one that is not.
4. **Fig 6 :39, :42, :49-50.** "a search that finds nothing is never a proof of absence"; "the remedy is more search"; search "fails by spending budget on a region already swept. Distribute the search."
   - So: what was just tried and not settled goes after the untried (inhibition of return), and search spreads across regions.
5. **Fig 2 (triangulation).** Two low-overlap witnesses outrank one.
   - So: where an option has several independent readings in its favour, that counts for more than a single reading.
6. **Fig 5 :68.** "rank by persistent-and-flat residual".
   - So: a mint or ask that would close a residual that has persisted and not moved comes first.
7. **Fig 4 :24.** "Never a replay of what worked once."
   - This is a CAUTION on 2: the record weighs a KIND of option in a context. It never replays one past success verbatim.

Triangulated: the cost reading (Fig 12, Fig 9), the record reading (Fig 7, Symbols), and spread after failure (Fig 6, Fig 9 :44). Each pair has low overlap.

**When the draw is legitimate.** No figure orders by chance. Fig 6 calls for MORE search, not random search. So the draw is legitimate ONLY when every reading above ties AND the tied options are equally UNKNOWN (no record, no cost difference, no board contact). Even then, the least-tried option goes first, and the draw breaks ties only among options equally untried. The draw is recorded as an exploration act ("attempts something or encounters unknowns", Isaiah 10:02).

## WORLD (secondary, each read)

- **Human decision heuristics.** Gigerenzer & Goldstein, *Psychological Review* 103(4), 1996, "Reasoning the fast and frugal way". Take The Best walks cues in order of validity and stops at the first that discriminates. "If no cue discriminates, then choose randomly", and if neither option is recognized, "choose randomly between them".
  - Predicts: an ordered list of readings, with chance only when every reading ties or the options are unknown.
  - CORROBORATES the verdict, including Isaiah's "last resort ... unknowns".
- **Human exploration.** Wilson, Geana, White, Ludvig & Cohen, *J. Exp. Psych.: General* 143(6), 2014. People use "directed" exploration (an information bonus toward less-known options) and "random" exploration (decision noise), and both rise with the horizon. The operational definitions are from Krueger, Wilson & Cohen, *Judgment and Decision Making* 12(2), 2017.
  - Predicts: under uncertainty, prefer the least-known option.
  - PARTLY CONFLICTS: humans do show some random choice noise. The figures stand (no figure orders by chance). The world reading narrows the claim to "random only among the equally unknown, and less of it than directed choice". Reported, not averaged.
- **Attention and foraging.** Klein, 2000, as summarised on Wikipedia "Inhibition of return": IOR "promotes exploration of new, previously unattended objects" (the "foraging facilitator" proposal; Pratt & Abrams 1995 dissent).
  - Predicts: just-searched options are tagged and visited last.
  - CORROBORATES parked-last (r1473) and distribution (r1474).
- **Animal foraging.** Charnov, *Theoretical Population Biology* 9, 1976 (marginal value theorem): leave a patch "when the marginal capture rate in the patch drops" to the habitat's average.
  - Predicts: a search stream is left when its yield per step falls below the average, not after a fixed count and not by chance.
  - CORROBORATES a yield-rate reading for streams and budgets.
- **Learning from outcomes.** Win-stay, lose-shift (Nowak & Sigmund, *Nature* 364, 1993, as cited on Wikipedia).
  - Predicts: repeat what paid in this context, and shift away from what failed.
  - CORROBORATES the record reading (Fig 7), with Fig 4's caution: it applies per kind and context, never as a verbatim replay.

## VERDICT -- the 2nd and 3rd readings, site by site

| Site (line at 8cd9a0d) | What it orders | 1st today | 2nd (add) | 3rd (add) | Draw only when |
|---|---|---|---|---|---|
| (a) goal pick :9910 | goal hypotheses in a key group | S-class (ruled) | RECORD: learned score, own+inherited (r1475/1476) | CONTACT STRENGTH (Fig 2), then parked-last, contingent, distribute | never; least-tried kind first among equals |
| (b) derived asks :6154 | which derived question to ask | fewer asks | RECORD: share of this ask-kind that settled before (Fig 7) | COST: actions to settle, cheapest first (Fig 12) | equally unknown; least-asked first |
| (c) mints :23374 | which new term to mint | understanding, times seen | RESIDUAL: closes a persistent-and-flat residual (Fig 5 :68) | COST: fewer bits first, MDL (Fig 12) | identical on all; least-seen first |
| (d) search streams :2490 | which stream gets the next candidate | least rank spent | YIELD RATE: hits per step so far; leave a stream below the average (Charnov; Fig 6 :50) | LOOKUP: library evidence offered for the stream (Fig 9 :45) | equal yield and evidence; least-spent first |
| (e) library chains :2501 | which chain to walk | depth, evidence | COST: actions to test, held apart from depth's bits (Fig 12) | RECORD: this chain's past endings in this context (Fig 7) | untried chains only |
| (f) tied values :2554 | order of numerically tied values | value | LOOKUP: present on the board or in contact objects now (Fig 9, Fig 11) | RECORD: how often this value was the answer before (Symbols) | never by NAME; unknown values least-tried first |
| (g) _lookup_order :2571 | operand slots for a shape | gate, actions, bits, magnitude | already has least-known (7h) | already has analogy (7m) | already last; measure its share only |
| (h) parameter search :2585 | which value to try | distance (ordered); NOTHING (unordered) | LOOKUP: values present on the board / held by contact objects (Fig 9 :45) | RECORD: values this slot-kind took before, own+inherited (Symbols) | unordered and all unknown; least-tried first |
| (i) shown vs unseen :2620 | a shown value vs the unseen region | frontier bits/actions | already (Fig 12) | least-seen | already last |
| (j) _choice sites :20107 (goal_condition, invent, two_readings, starved, curiosity, exit, choose_known, objective, ...) | generic choices | residual gate, then the bits/actions frontier | RECORD: how this option ended at this site, own+inherited (Fig 7) | least-seen (exists) | only among equally unknown |
| (k) interface presses :1047/:1117/:1158 | which button to press | separability or residual, least-seen | RECORD: this press's observed effect reliability in this context (Fig 7; win-stay lose-shift) | COST: cheap or reversible presses before costly ones (Fig 12 actions) | an untried press in this context, recorded as exploration |

**The general rule, for every site.** A draw that decides anything other than a tie among equally unknown options marks a missing reading. Under that rule, the census (r1476) is the test. For each site, it counts how often the draw decided and how large the tie was. Every non-trivial share is a gap to fill from this table.

- **Cost if wrong:** low. Each reading goes in under its site's arm and ships beyond its spread (r1426).
- **Undoable:** yes.
- **Reversed by:** a site where the added reading does not move outcomes beyond the spread. That reading then stays off at that site.

## Sources

- [Gigerenzer & Goldstein 1996, Psychological Review (PDF)](https://www.dangoldstein.com/papers/FastFrugalPsychReview.pdf)
- [Wilson, Geana, White, Ludvig & Cohen 2014, J Exp Psych: General](https://experts.arizona.edu/en/publications/humans-use-directed-and-random-exploration-to-solve-the-explore-e/)
- [Krueger, Wilson & Cohen 2017, Judgment and Decision Making](https://www.cambridge.org/core/product/15AA852DC35A7D6E30014D3063249CF8/core-reader)
- [Inhibition of return (Klein 2000, foraging facilitator)](https://en.wikipedia.org/wiki/Inhibition_of_return)
- [Marginal value theorem (Charnov 1976)](https://en.wikipedia.org/wiki/Marginal_value_theorem)
- [Win-stay, lose-switch (Nowak & Sigmund 1993)](https://en.wikipedia.org/wiki/Win%E2%80%93stay,_lose%E2%80%93switch)
