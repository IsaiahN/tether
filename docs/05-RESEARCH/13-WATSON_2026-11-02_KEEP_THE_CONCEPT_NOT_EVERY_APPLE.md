# WATSON 2026-11-02 10:05 CST: keep the concept, not every apple. The perception tallies, recall and search speed

Isaiah, 09:59: "Is this not the least useful data? ... Animals don't save a copy of every apple or pair they encounter and every angle, just the general concept"
Isaiah, 09:59: "Perform a WATSON. No wonder our recall is so slow, and search"
Isaiah, 10:00: "Today this changes, because search speed depends on it"

## QUESTION (effect terms)
What should the agent keep about the objects and changes it has perceived, across games? What should search read? And what must change TODAY so that search reads less?

## FACTS (measured)
- The perception tallies are 93% of the store's rows (WATSON 10-24, save 33):
  - kind: 2.22 M rows;
  - kind_dk: 1.21 M rows;
  - the library of held terms: 13 k.
- Both tallies grew FASTER per save over time.
- W-4 (tether.py:297): 434,602 kind_dk keys, 127 MB at load, ~10% read in a game.
- Each tally row is a count keyed by (entry, role, kind_o, kind_x) or (dk, entry, tgt). It holds n and the LAST game/level/cycle (lineage_store.py schema). n == 1 marks a one-occasion row.
- P8 (11-02): the T1d tier "keeps every entry that ever compiled". In test_k1 it lists 1,872 entries against 1 in T1a, and it outgrows what the residual lit.
- Every save rewrites the whole fold blob (lineage_store.py:564-571).

## DOMAIN CENSUS (written before the figure lines were chosen)
- R:
  - arity 3: the occasion perceived, the concept it supports, the search that reads one or the other;
  - symmetry: two sightings of one kind are one fact plus a count; a row seen once and a row that recurs differ in KIND;
  - scale: step, game (the boundary), lifetime.
- D-perception (within a game): actors = tally rows; currency = rows read per lookup; anchor = the game's own detail.
- D-concept (across games): actors = settled terms, their standing, the recurring tallies; currency = reach; anchor = Fig 4's membrane.
- D-search: actors = tiers T1a-T5, keyed reads; currency = lookups and seconds per lookup; anchor = A4(c)'s baseline.
- UNION D-perception ∩ D-concept = CONSOLIDATION at the game boundary, with its own loop.
- Order (Fig 3): perception -> consolidation -> concept -> search.

## TETHER (primary, verbatim, docs/FIGURES_TEXT.md)
D-concept: what crosses the boundary.
- Fig 4 :8-9 "a method that can be reapplied / verified, and compressed to its essentials"
- Fig 4 :23 "upward: a method that can be reapplied. Never the recording of a particular success."
- Fig 4 :25 "A recording carried upward looks like knowledge and is a description of one occasion."
- Fig 4 :27-28 "The transform between scales loses information, and that is the point. Going up throws away detail; that is what makes the result reapplicable."
- Fig 5 :43-44 a term "fails this, and so does a term that explains one occasion perfectly."
- Fig 12 :107 "Settling compresses the description and not what it cost to establish."
- -> A one-occasion tally carried across games is a recording. What crosses is the concept (settled term + standing) and what recurs. TRIANGULATED (Figs 4, 5, 12).

D-search: what search may cut.
- Fig 9 :60 "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict."
- Fig 9 :40-41 "a wrong cut removes the answer and speeds up, so keep every cut ranked and reversible"
- -> Search may skip one-occasion rows (a budget filter). A skipped row is never "absent". It is fetched on a miss, so the cut is reversible.

STRAIN TESTS:
- Fig 1 :22 "Aggregating across slots is how a live signal disappears into an average." This governs slots WITHIN a step, a different quantity. So within a game the per-object detail stays whole. Consolidation acts only across occasions at the game boundary. No strain once the scale is kept.
- Fig 6 :42 "What is recorded only grows." This governs the closure (terms and refusals), not tallies (ruled 10-20). Tallies are derived, so they may move tier; nothing is deleted. No strain.

## WORLD (secondary; each source read)
- Neuroscience, forgetting. Richards & Frankland 2017, Neuron, "The Persistence and Transience of Memory": transience "prevents overfitting to specific past events, thereby promoting generalization"; "the goal of memory is to optimize decision-making." CORROBORATES.
- Neuroscience, two systems. McClelland, McNaughton & O'Reilly 1995, Psychological Review 102(3):419-457: "the neocortex learns slowly to discover the structure in ensembles of experiences"; "The hippocampal system permits rapid learning of new items without disrupting this structure." Predicts a fast detailed store within a game plus slow structure across games, which is this design. CORROBORATES.
- Cognition, prototypes. Posner & Keele 1968, as described by Huber, Avian Visual Cognition: "humans readily identify a prototype dot figure"; "the more similar a novel pattern was to a category prototype, the easier it was to classify." CORROBORATES the concept tier.
- Animal cognition, partial CONFLICT. Huber on pigeons: "evidence in support of the prototype theory is rather poor and contradictory in pigeons"; "Pigeons appear unable to abstract prototypes in this manner."
  - Re-census: storing exemplars without abstracting is a LIMIT on transfer to new categories, not a model for an agent that must transfer across games.
  - The figures stand (Fig 4 :23). The pigeon case is the cost of not consolidating.
- Language statistics (read 10-24). Kornai 2008: "For large corpora, about 40% to 60% of the words are hapax legomena." Predicts that a large share of tally rows have n == 1. To be MEASURED.

## VERDICT (from the figures)
- Keep the occasion detail inside the game.
- Carry across games only the concept and what recurs.
- Search reads the recurring and the current. A one-occasion row from a past game is cold: never deleted, read only on a key miss, and back to hot the moment it recurs.
- Cost if wrong: a cold row needed by an enumeration is missed until it recurs. Undoable: yes (n and l_game are kept, so the filter is a query). Reversed by: the measurement showing few n == 1 rows, or the 1-board slice reaching fewer levels.

## TODAY'S BUILD (A4.7; Isaiah 10:00 "Today this changes")
1. MEASURE (read-only, on the merged tip): per tally table, rows, the share with n == 1, the share with n == 1 and l_game not the latest, and bytes.
2. HOT/COLD BY RECURRENCE, one switch, default ON:
   - search's enumerations (the T1a-T1d tiers, kind_dk keyed lists, the held index lists) read only rows with n >= 2, OR l_game == this game, OR an entry that backs a held or settled term;
   - keyed lookups that miss hot read cold (exact);
   - nothing is deleted;
   - a row seen again is hot by its own n.
3. P8 PULLED FORWARD from A5: T1d becomes an order over the lit set (T1d <= lit).
4. MUST-FAILS:
   - a cold row read by key still answers;
   - a row seen a second time becomes hot;
   - T1d <= lit;
   - an OFF run reads every row as before.
5. PASS: lit entries per lookup, rows read per lookup and seconds per lookup fall against A4(c)'s baseline; the 1-board slice reaches no fewer levels; the six + guard green.
6. NOT TODAY: folding tallies into per-kind concepts (prototypes), and the fold blob as a table. Both are first on the post-deadline list.

Sources:
- [Richards & Frankland 2017, Neuron (via Neuroscience News)](https://neurosciencenews.com/forgetting-smarter-6947/)
- [McClelland, McNaughton & O'Reilly 1995, Psychological Review](https://stanford.edu/%7Ejlmcc/papers/McCMcNaughtonOReilly95.pdf)
- [Huber, A Prototypical Point of View, Avian Visual Cognition](https://pigeon.psy.tufts.edu/avc/huber/prototype.htm)
- Kornai 2008 / Malmkjær 2002 via Wikipedia "Hapax legomenon" (read 10-24)
- docs/FIGURES_TEXT.md at general-agent 3bfda18; lineage_store.py schema; tether.py:297
