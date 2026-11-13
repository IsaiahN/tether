# WATSON 2026-10-24 18:15 CDT: compaction and decay keep the learned store bounded over months and years

Isaiah, 18:09, verbatim: "That's why compaction and decay were always important. You can see how I handled this in Ouroboros v1-v4, but you should also do a WATSON and Tether analysis to come up with"
(It came after his 18:00 message: "Please always think of scale. If the agent ran nonstop for months or years, imagine how big the DB would be".)

## QUESTION (effect terms)
- The learned store grows with play. Which parts may be compacted, and which may decay, so that the agent's memory stays flat and its disk grows only with real novelty?
- What must never be lost?

## MEASURED (three points on the one lifetime, rows per section; seat readings)
| section | save 12 | save 18 | save 33 | per save, 12→18 | per save, 18→33 |
|---|---|---|---|---|---|
| kind | 600,428 | 914,404 | 2,223,541 | +52.3k | +87.3k |
| kind_dk | 301,091 | 431,276 | 1,208,291 | +21.7k | +51.8k |
| asked_tally | 141,277 | 242,389 | 246,965 | +16.9k | +0.3k |
| held (library) | 12,640 | 12,923 | 13,034 | +47 | +7 |
| pair | 399 | 666 | 1,766 | +44 | +73 |
| evidence | 284 | 480 | 2,830 | +33 | +157 |
| sym | 3,408 | 3,533 | 3,835 | +21 | +20 |

Sources: seat 14:41 and 14:44 (saves 12 and 18), seat 07:35 and 16:06 today (save 33).
- kind and kind_dk are 93% of the 3.70 M rows. Both grow FASTER per save over time. They are the growth.
- The library and the asked tally have nearly stopped growing.
- The readable db is 1,714,429,952 B for 3.70 M rows, about 463 B per row with indexes.
- At the latest rate (about 139k rows per save), that is about 64 MB of readable db per save. This is a straight-line guess; G1 measures the real curve.
- Caveat: a save is not a fixed amount of play. G1 normalizes by games and actions.

## DOMAIN CENSUS (written before the figure lines were chosen)
- R:
  - arity 3: the play that writes, the store that holds, the working set that reads;
  - symmetry: two sightings of one kind are one fact plus a count, but a row seen once and a row that recurs differ in KIND (a recording vs a method);
  - scale: step (RAM), level/game (the boundary), save, lifetime (months).
- D-library: actors = held terms, symbols, aliases. Currency = reach. Anchor: held 13,034; Isaiah 10-14 "the library should never be compacted/compressed".
- D-fold: actors = perception tallies (kind, kind_dk, pair, kind_off, asked_tally). Currency = rows, bytes, lookup time. Anchor: the table above.
- D-record: actors = save files, origin records. Currency = compressed bytes. Anchor: the archive is about 116 MB for 33 saves (seat 07:35).
- D-working set: actors = what is in RAM. Currency = RSS. Anchor: B1 (1.692 GiB whole), G2 (flat).
- D-clock: actors = boundaries (level, game, save). Currency = which verdicts go stale. Anchor: Isaiah 10-09 "Staleness stays boundary-only".
- UNION D-fold ∩ D-clock = DECAY of a row's standing in the hot fold.
- UNION D-fold ∩ D-record = COMPACTION, the move from hot to compressed.
- Order (Fig 3): library (keys) → record → fold → working set; the clock paces the fold.

## TETHER (primary, verbatim from docs/FIGURES_TEXT.md)
D-fold: what crosses a boundary, and what a row must earn.
- Fig 4 :23 "upward: a method that can be reapplied. Never the recording of a particular success."
- Fig 4 :25 "A recording carried upward looks like knowledge and is a description of one occasion."
- Fig 5 :43-44 "A new term is worth having when stating it, plus what remains unexplained after it, costs less than what was unexplained before. A term that explains everything by saying nothing fails this, and so does a term that explains one occasion perfectly."
- Fig 10 :24-26 "the ground does not decay, the channel does / stale percepts, dropped transients, / saturated metrics, pooled readings"
- → A tally row seen on one occasion is a recording. A row that recurs is a method. The hot fold keeps what recurs; one-occasion rows are the channel's transients and may decay out of it. TRIANGULATED (Figs 4, 5, 10, low overlap).

D-fold ∩ D-record: compaction is lossy, and the loss is measured.
- Fig 4 :9 "verified, and compressed to its essentials"
- Fig 4 :27-28 "The transform between scales loses information, and that is the point. Going up throws away detail; that is what makes the result reapplicable."
- Fig 4 :30-31 "So take the round trip and measure the gap. ... The gap is not an error to eliminate. It is the measurement of what the coarser description cannot hold"
- → Compaction is required, and its acceptance is a round trip: how often a compacted row is asked for again. TRIANGULATED with Fig 12 :107 below.

D-record and D-library: what never leaves.
- Fig 6 :42 "What is recorded only grows. What is reachable is derived, and it can fall."
- Fig 6 :46 "A store that deleted instead would have neither property, and could not tell never-held from held-and-given-up."
- Fig 12 :107-109 "Settling compresses the description and not what it cost to establish. ... where the arrangement is recorded, re-deriving it is a lookup and the actions were spent once. ... Which boundary matters is the one the record does not cross."
- → The library and the record are never deleted. Tallies are derived ("can fall"), so they may move tiers. They are never destroyed while Isaiah's 10-21 "fetched on a miss, never deleted" stands.
- STRAIN TEST: Fig 6 :42 governs the CLOSURE (terms and refusals), not perception tallies, as already ruled 10-20. For tallies the governing lines are Fig 4, 5 and 10. No strain.

D-clock: decay acts on standing, at boundaries.
- Fig 6 :42 with the 10-15 ruling: "Decay acts on the verdict's hold on the choice ... It never acts on the record."
- Fig 9 :60 "Never let a filter hand you a verdict." A row moved to cold is unranked, not refuted. It is fetched on a miss.

## WORLD (secondary; each source read)
- Ouroboros v3/v4, `safe_cleanup.py` (IsaiahN/Ouroboros, branch Ouroboros-v4, read today):
  - "RAW OBSERVATIONS (Per-Game Ephemeral) ... Once patterns extracted to aggregated tables, raw data is redundant";
  - "AGGREGATED KNOWLEDGE ... CLEANUP: NEVER delete (only deprecate if stale)";
  - "Uses generations as computational clock, not wall time ... System paused for a month? Nothing deleted until new gens run";
  - `_compress_knowledge`: "Orchestrate all compression steps BEFORE deletion ... merge overlapping learned rules";
  - adaptive thresholds by "knowledge density" (useful rows / total) and DB size;
  - `_deprecate_stale_patterns`: "Mark stale patterns as inactive (don't delete - game might return)".
  - Predicts: the same three tiers (raw windowed, aggregated kept, stale deprecated, not deleted) and a boundary clock. CORROBORATES.
  - It DIFFERS on one point: the thresholds were set constants (30 generations, 50 generations, 5,000 logs). Isaiah's 10-21 rule "50k and 5k are magic numbers" retires that. The window here comes from the agent's own recurrence rates.
- Computer science: Ungar 1984, "Generation Scavenging" (ACM SIGSOFT/SIGPLAN): "young objects die young and old objects continue to live"; "new objects that have survived several scavenges are awarded old status ... This promotion to old status is called tenuring."
  - Predicts: new rows on probation, promoted by surviving, i.e. by recurring. CORROBORATES the shape.
  - Garbage collection DELETES what is unreachable. Here a cold row stays reachable (the kind may recur), so it MOVES tier and is not deleted. The figures stand on that point (Fig 6 :46).
- Linguistics: Kornai 2008, Mathematical Linguistics (via Wikipedia, "Hapax legomenon"): "For large corpora, about 40% to 60% of the words are hapax legomena." Malmkjær 2002: in the Brown Corpus "about half of the 50,000 distinct words are hapax legomena."
  - Predicts: a large share of distinct kind rows occur once, and that share keeps the store growing (Heaps). This is a measurable PREDICTION for G1.
- Human and animal cognition:
  - Anderson & Schooler 1991, Psychological Science 2:396-408, as described by Stevens, Marewski, Schooler & Gilby 2016, R Soc Open Sci 3:160293: need probability rises with "the recency and frequency" of past encounters, as a power function of time since the last encounter;
  - in chimpanzees "the power function fits ... better than the exponential function."
  - Predicts: rank by recency and frequency of recurrence (Isaiah's 10-21 "slide rule"), not by a fixed age cutoff. CORROBORATES.
- Immunology: Kurtulus, Tripathi & Hildeman 2013, Frontiers in Immunology 3:404: "80–90% of the responding T cells undergo apoptosis"; the cells that persist become "long-lived memory T cells".
  - Predicts: most one-occasion responses leave, and the pattern that recurs is kept. CORROBORATES.
- Earlier, witnessed 10-18:
  - LSM trees (O'Neil et al. 1996): merges remove "redundant or obsolete entries", and flushes are triggered by size;
  - Tononi & Cirelli 2014: sleep "weakens the connections ... to save energy";
  - Berry et al. 2012: "forgetting is an active process".
  - These corroborate boundary consolidation plus a size-pressure wall.

## VERDICT (from the figures)
Three tiers, one rule, one clock.
1. LIBRARY (held terms, symbols, alias list): never compacted, never decays from disuse (Isaiah 10-14, 09-29). It already grows by 7 per save and is bounded by the world's structure, not by play. Its only consolidation is the alias dedup (10-21 b).
2. FOLD (the perception tallies, 93% of rows): two tiers.
   - HOT: indexed, read on demand.
   - COLD: compressed and exact, fetched on a miss, never deleted (10-21 c).
   - A row stays hot while it is DUE: the boundaries since its last sighting are no more than twice its own longest gap between sightings.
   - A one-occasion row has no gap of its own, so it uses its section's median first-recurrence lag, which G1 measures.
   - The factor 2 is the doubling schedule (Luby; already derived 10-21), not a tuned number.
   - A row that is seen again returns to hot with its counts summed (recurrence bumps it up, 10-21).
   - The rule runs at the consolidation boundary already built (game end, 10-18), inside the save. Size pressure is an outer wall only.
3. RECORD (save files, origin records): only grows, compressed (Fig 6 :42, Fig 4 :9). Nothing in it is deleted under this design.
- WORKING SET: reads on demand (step 5). The hot cache is SQLite's page cache with a fixed wall set by the machine. G2 proves memory is flat.
- CLOCK: boundaries (game ends and saves), never wall time. Within a level, age only orders (10-09, 10-15).
- DECAY: acts on standing only. Situated verdicts go stale at boundaries (10-15, built); fold rows move hot to cold; library terms only on use failure.

- Cost if wrong: a row demoted too early costs one cold fetch, measured in ms (B1-db), and it returns hot on the next sighting.
- Undoable: yes. Cold is exact, so hot ∪ cold = today's fold, row for row.
- Reversed by:
  - G1 showing most rows recur. Then compaction buys little: the growth is real structure, and disk grows with real novelty (G3 reports it).
  - Or the round trip showing cold fetches erase the gain.

## ACCEPTANCE (measured on the thing once built)
- A1, hot flat with play: on the save-10/20/33 replays with compaction ON, the slope of hot rows per game is near 0, or falling.
- A2, nothing lost: at every save, hot ∪ cold = the OFF fold (digest).
- A3, the round trip (Fig 4 :30): cold fetches per game are reported, and play is identical to OFF on a fixed seed (a cache's exactness, a CHECK run).
- Must-fails, red stated before each runs:
  - MF-C1: plant a demoted row that play needs, with the fetch disabled. Decisions must differ.
  - MF-C2: re-see a demoted row. It must return with n_before + n_after; red if its counts reset.
  - MF-C3: a library term unused for many boundaries stays. Red if it is demoted.
- A meter at each consolidation: per section, the share of rows seen once, the recurrence curve, and hot/cold bytes. These are the agent's own numbers and G3's inputs.

## WHERE IT GOES
- Step 4 lands as planned.
- G1 adds two outputs from the replay it already does: each section's distribution of n (the share seen once), and its first-recurrence lag curve. It also normalizes per game and per action.
- The compaction design is posted inside step 5 (the save switch is where it runs), then built.
- No deletion anywhere in this design.
- Open for Isaiah, with G3's numbers: whether the cold tier stays exact forever (the 10-21 "never deleted"). It is about 48 B per row compressed (the json form), so at the latest rate roughly 6-7 MB per save, a straight-line guess.

Sources:
- [Ungar 1984, Generation Scavenging](https://people.cs.umass.edu/%7Eemery/classes/cmpsci691s-fall2004/papers/p157-ungar.pdf)
- [Hapax legomenon (Kornai 2008; Malmkjær 2002)](https://en.wikipedia.org/wiki/Hapax_legomenon)
- [Stevens et al. 2016, chimpanzee memory, citing Anderson & Schooler 1991](https://decisionslab.unl.edu/pubs/stevens_etal_2016_RSOS.pdf)
- [Kurtulus, Tripathi & Hildeman 2013, Frontiers in Immunology](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2012.00404/pdf)
- [Anderson & Schooler 1991, Psychological Science](https://www.psychologicalscience.org/journals/psychological-science/j.1467-9280.1991.tb00174.x/)
- IsaiahN/Ouroboros, branch Ouroboros-v4, `safe_cleanup.py`
