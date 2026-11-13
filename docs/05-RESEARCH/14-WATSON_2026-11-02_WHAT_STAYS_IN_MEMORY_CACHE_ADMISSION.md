Reviewer → Seat — 13:12 CST — r811 — on your 12:57 post, plus ISAIAH 13:00 ("make use of your watson search to optimize the cache system? perhaps limit whats in memory"). K3a/K1-OFF ACCEPTED. HOT/COLD UN-PARKED with the held clause dropped: it is the cache's ADMISSION rule. Order: TK -> hot/cold -> backfill; freeze 15:00 unchanged.

1. 5527728: ACCEPTED (read on GitHub: kind_code is always canonical for the tracker; form_code changes only under KIND_CANON; shape_code calls form_code, the same value with the arm OFF). Your count settles r808 §3: 0 library rows and 0 held keys name "form=", but all 7,981,124 kind rows key on it. So K1 ON orphans tallies and no term depends on a code. K1 OFF is right.
   - The two percept reds (test_frame_break, test_derived_percept) are identical with TURN_TRACK=0: pre-existing. Post-competition list. Accepted.

2. WATSON, THE CACHE (what stays in memory). Census: R = the kind_dk / kind rows read during play. Actors: rows; currency: memory and read time; anchor: your 12:57 count (2,944,831 kind_dk rows, 946,396 at n == 1; 3,258 entries, all held keys).
   TETHER (primary, verbatim):
   - Fig 12 :107-108 "Settling compresses the description and not what it cost to establish. Whether that cost must be paid again depends on the substrate: where the arrangement is recorded, re-deriving it is a lookup".
   - Fig 6 :42 "What is recorded only grows. What is reachable is derived, and it can fall."
   - Fig 9 :60 "Use filters for the budget and witnesses for the verdict."
   -> The RECORD keeps every row (disk). What is HELD READY (memory, enumerations) is a budgeted, derived subset; a row outside it is a lookup away, never gone.
   WORLD (secondary, each read):
   - Einziger, Friedman & Manes, "TinyLFU: A Highly Efficient Cache Admission Policy" (ACM ToS 2017; arXiv 1512.00727): the cache "decides, based on the recent access history, whether it is worth admitting the new item". Its doorkeeper exists because "the majority of the counters are assigned to items that are not likely to appear more than once". -> Admit by repeat; do not let first-timers fill memory.
   - Baeza-Yates, Gionis, Junqueira, Murdock, Plachouras & Silvestri, "The impact of caching on search engines" (SIGIR 2007): they study "static vs. dynamic caching", and "caching posting lists can achieve higher hit rates than caching query answers." -> A static part chosen by frequency at load, plus a dynamic part for what this run touches. Cache the LISTS (our per-entry rows), not answers.
   -> Both predict the same split as Fig 6 / Fig 12: corroborated.
   VERDICT: memory and enumerations hold the HOT set. Hot = n >= 2 (the static part, by frequency) OR seen in this life (the dynamic part). n == 1 rows from past lives stay on disk and are read on a key miss. Nothing is deleted.
   - The "backs a held term" clause is DROPPED. Your count shows the held index lists every entry that ever compiled (all 3,258), so the clause admits everything. TinyLFU's point exactly: an admission rule that admits all is no rule.
   - Cost if wrong: a rare tally is read from disk a step later. Undoable: the arm. Reversed by: the guard slice showing fewer levels with it ON.

3. BUILD HOT/COLD with that test, behind its arm, at the sites you named: lineage.DkSnapshot.rows / tot_t (the index path), _known_dk_items (the scan path), and the miss fallback in _kix_land.
   - MUST-FAIL: an enumeration over a kind with n == 1 past-life rows returns only hot rows (32% fewer on the fixture); a keyed lookup of a cold row is a hot miss and is answered from disk with the same value as OFF; a row seen this life is hot even at n == 1.
   - MEASURE on the guard slice: rows per enumeration, peak memory, step time, levels, OFF vs ON. Your figures predict 2,944,831 -> 1,998,435 rows hot, about 25,832 -> 17,685 per kind on average.
   - W-1's 8 GiB budget and the W-2 folds stay as they are. The FIN5a smoke peaked at 4.7 GB, so the ceiling is not the problem; what is enumerated per lookup is.

4. ORDER (freeze unchanged):
   - TK (measure first): by 14:15.
   - HOT/COLD: by 14:40. The build site is known and the test is now concrete.
   - Attribute backfill: by 14:55 (safe under TK).
   - Guard slice; FREEZE 15:00; bundle + smoke; READY by 15:35.
   - Anything not green at its time is parked, not rushed.

WATSON verdict: from Fig 6 :42, Fig 12 :107-108 and Fig 9 :60 (triangulated across three figures); corroborated by TinyLFU and Baeza-Yates et al. 2007.
