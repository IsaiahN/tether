Reviewer → Seat — 13:05 CST — r810 — ISAIAH 12:53: "WATSON how SERPs do it." Verdict: search engines do NOT make an any-match list fast by adding tags. They BOUND the work at K: rank by how many asked attributes an entry carries, score only the top K, fall back to the next tier only when fewer than K fit. That is buildable today, and with it the attribute backfill can only help.

QUESTION: the library lookup lights every entry that reads ANY asked reading (an OR). Adding attributes to 1,123 bare atoms lights more entries, so the backfill alone can slow a step. How do search engines keep many tags fast?

TETHER (primary, verbatim, docs/FIGURES_TEXT.md):
- Fig 9 :40-41 "a wrong cut removes the answer and speeds up / so keep every cut ranked and reversible"
- Fig 9 :60 "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict."
- Fig 9 :44 "searching and finding nothing proves nothing."
- -> A cut sized by the budget is lawful if it is RANKED (best first) and REVERSIBLE (what was cut is reached later). The cut must never record a verdict. Single figure, three lines; plain on its face.

WORLD (secondary, each source read):
- Manning, Raghavan & Schütze, Introduction to Information Retrieval (Cambridge UP, 2008):
  - tiered indexes: "If we fail to get K results from tier 1, query processing 'falls back' to tier 2, and so on."
  - index elimination: "We only consider documents that contain many (and as a special case, all) of the query terms." Its stated danger: "we may end up with fewer than K candidate documents."
  - inexact top K: the aim is to avoid "computing scores for most of the N documents".
  - Boolean AND: process "in order of increasing document frequency", so intermediate results are "no bigger than the smallest postings list".
- Elastic (Lucene) block-max WAND blog: documents whose maximum possible score cannot reach the top K are skipped ("skipping blocks whose sum of maximum scores is not competitive"); disjunctions up to "15x faster".
- -> Every one predicts the same shape: the work is bounded by K, not by the list's length. Ranking uses the matched-term count (more tags = better ranking, not more work). Falling to the next tier happens only on fewer than K. CORROBORATES Fig 9 :40-41 and :60.

RULING: TOP-K WITH FALL-BACK ("TK") on the described lit list, before the attribute backfill.
0. MEASURE FIRST (minutes, the guard slice): entries KEPT per lookup after _described_lit (self._dl_n "kept" / lookups), max and p90. If the p90 kept is already <= 32, TK changes nothing: skip it and say so.
1. ORDER the kept list by (its tier as listed, then the count of the asked readings the entry reads, high first). Stable within ties.
2. EVALUATE ONLY THE FIRST K = 32 per lookup.
3. FALL BACK: if those K offer no fit, the next lookup with the SAME description key continues from K (a per-key offset, reset when the description changes or a term is adopted). Nothing is dropped; it is reached on later steps.
4. NO VERDICT FROM A CUT: _dl_miss ("no_entry") may fire ONLY when the offset has passed the end of the list. A cut list that offered nothing is "not yet", never "nothing here" (Fig 9 :44, :60).
5. Behind an arm (TETHER_TOPK, default ON); OFF = today's list.
MUST-FAILS:
- MF-TK1: 200 kept entries, K=32 -> at most 32 evaluated in one lookup.
- MF-TK2: the only fitting entry is at rank 70 -> not found on lookup 1 or 2, found on lookup 3 of the same key. Under OFF it is found on lookup 1, so the cut is reversible, not lossy.
- MF-TK3: no "no_entry" verdict is recorded while the offset is short of the end.
- MF-TK4: an entry reading 3 of the asked readings ranks above one reading 1, within the same tier.
MEASURE: step time and levels on the guard slice, OFF vs ON.

THEN THE BACKFILL (r809 §3): under TK the work per lookup is bounded at K, so the backfill can no longer slow a step. It only makes the ranking better. Ship it if the reads diff is additions only and the guard is green.

ORDER, FREEZE UNCHANGED (15:00):
- If hot/cold is green by 13:45, commit it; otherwise park it.
- TK (measure first): by 14:30.
- Backfill: by 14:50.
- Guard slice; FREEZE 15:00; bundle + smoke; READY by 15:35.
- Priority if time runs short: TK > backfill > hot/cold.

WATSON verdict: from Fig 9; corroborated by three independent IR sources. Cost if wrong: an answer found a few steps later than today, not lost. Undoable: the arm. Reversed by: the guard slice showing fewer levels with TK ON.
