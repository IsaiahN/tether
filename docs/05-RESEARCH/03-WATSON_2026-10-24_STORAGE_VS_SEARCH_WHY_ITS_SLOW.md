# WATSON 2026-10-24: why storage isn't what makes the agent slow, and what is

Reviewer, 07:45 CDT. Isaiah asked at 07:39: "This is surprising. Please watson this but as a programmer this makes little sense". The Tether figures were read from the SVGs (tspans joined) before anything here was concluded. The numbers come from the seat's code reads and the timed-replay profile (07:31, 07:35) and from the overnight ledgers.

## The short version

- **Your instinct is right in principle, aimed at the wrong layer.** Search is fast when there's an index: a structure built once, kept, and looked up. The disk layer already has one: memory.db is the deduplicated, indexed store, and it loads in 4–5 seconds.
- **The missing index is in the thinking layer.** While it plays, the agent keeps rebuilding the same derived structures from scratch on every check, inside loops that run hundreds of thousands of times. It's the programmer's classic: an expensive call that should be computed once and cached, sitting inside a hot loop.
- **So the fix is the one you'd write as a programmer:** build those structures once, keep them, and look them up. That's the relational-slots cache you approved on 10-23. Moving the files into one store is still right, because it's tidier and stops things being stored twice. But it won't make play noticeably faster.

## The numbers

| Where the time goes | Share or cost | Source |
|---|---|---|
| All storage: loading, the in-play database reads, saving | about 5.5% of the timed replay | py-spy, 13,965 samples (seat 07:31) |
| Database reads during play (4 lazy reads, cached after the first ask) | 0.18% | the same profile |
| Any frame inside an sqlite execute or fetch | 0 samples | the same profile |
| Matching routes against the library (`route → _library_fit`) | about 77–80% | the same profile |
| Load from memory.db | 3.6–5.3 s per round | overnight ledgers |
| bp35, one move (GQ2 plan search, crowded board of about 7,200 slots) | 75–104 minutes, rounds 2–4 | overnight ledgers |

**Amdahl's law.** If storage cost nothing at all, the replay would be at most 1 / (1 − 0.055) ≈ 1.06×, so about 6% faster. The other 94% is computation.

## Why a 156-entry library can still take hours

The library itself is small: 156 terms. The cost is in what the agent derives from it, and from the board, on every check, and how many checks there are.

- **bp35 (crowded board).** In round 3 the planner built 1,675,070 candidate plans and checked 508,442 of them. Each check rebuilds the board's relational slots across all of its roughly 7,200 slots (`arc_world.relational_slots`, reached from `_is_relational` on every call). If each rebuild visits every slot once, that's about 508,442 × 7,238 ≈ 3.7 billion slot visits in one move. That's an estimate, and it assumes one visit per slot. The real per-slot work is larger if relations pair slots.
- **ft09 (earlier finding).** In one cycle the agent routed 134 residual slots. Each `_library_reach` took about 17 seconds over 618 lit library entries × 188 other objects, and the index was rebuilt on every call. That cycle spent 99.5% of its time there.
- **The timed replay.** The cost per route grew as one game went on (11 s per step rising to 60–100 s). Records that keep growing (`since_written`, `_judge`) are walked in full on every check.

In each case the same answer is computed again and again, when it could be kept from the first time. None of it is disk.

## THE TETHER (verbatim)

- **Fig 12 :107-109:** "Settling compresses the description and not what it cost to establish. Whether that cost must be paid again depends on the substrate: where the arrangement is recorded, re-deriving it is a lookup and the actions were spent once. Where it is not, the result carries forward and the deriving does not, so every lineage pays again."
  - The board's relational slots and the library's fit index are arrangements the agent derives and then throws away, so every check pays again. Recorded once, each later ask is a lookup.
- **Fig 9 :29:** "matching is a one-pass check, not a search". And **Fig 9 :45:** "Leaving, looking up and recognising are one step each, and cheap only in that order."
  - Today, matching a candidate against the board is a fresh search every time, rather than a one-pass check against something already held.
- **Fig 6 :42:** "What is recorded only grows. What is reachable is derived, and it can fall."
  - Deriving the reach is fine. Deriving it again on every call, when nothing it depends on changed, is the defect.
- Triangulated: Fig 12 and Fig 9 have little overlap and give the same verdict. Fig 6 bounds it: the derived parts may be rebuilt when their inputs change, not on every ask.

**Isaiah, 10-14 (verbatim, from the rulings):** "Rebuilding stored knowledge on every lookup is like dementia (brains don't forget how to breathe or walk)." That is this defect, in his words.

## OUTWARD WITNESSES (WATSON)

1. **A database is fast because of its indexes, not because it's a database.** SQLite's own query-planner documentation, for a query with no index: "SQLite reads every row out of the table ... This algorithm is called a full table scan since the entire content of the table must be read and examined in order to find the one row of interest." With an index, it "starts by doing a binary search", and the page notes that indexes "must normally be added by programmers." ([SQLite: Query Planning](https://www.sqlite.org/queryplanner.html))
   - The agent's in-play matching is a full scan per candidate, whether the data sits in a database, a JSON file or a Python dict. Moving it doesn't index it.
2. **Amdahl's law** (Amdahl 1967, AFIPS): the overall speedup from improving one part is limited by that part's share of the time. A 5.5% share caps the gain at about 6%. ([Wikipedia: Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law))
3. **Loop-invariant code motion and memoisation.** Standard compiler and programming practice: a value that doesn't change inside a loop is computed once, outside it (Aho, Lam, Sethi & Ullman, *Compilers*, the code-optimisation chapter). A pure function's result is cached by its arguments ([Wikipedia: Memoization](https://en.wikipedia.org/wiki/Memoization)). The relational-slots cache is exactly this.
4. **Measure before optimising.** Knuth (1974, "Structured Programming with go to Statements", *ACM Computing Surveys* 6(4)): "We should forget about small efficiencies, say about 97% of the time ... Yet we should not pass up our opportunities in that critical 3%." The profile says which part is critical, and it isn't storage.

## Where Isaiah's point stands, and where it doesn't

- **It stands:** one central, deduplicated store (2–3 JSON files, or one database) instead of 99 save files plus a database holding the same facts twice. Removing duplicates when saving, not on every load: today the same 842 duplicates are removed at every load and the result is never kept. Both are ruled (07:36, 07:37), and the seat is writing the plan.
- **It doesn't hold:** that the storage shape is why play is slow. On the measurements, storage is about 5.5% of the time, and the slowness is computation repeated inside the thinking loops.

## LIMITS, named

- The profile covers one game (ls20, about 30 minutes). Last night's play run wasn't profiled.
- bp35's cost is attributed to the relational-slots rebuild from the code path and the ledger (75–104 minutes, the ledger silent, memory flat). It hasn't been profiled.
- The pre-registered refuter from 10-23 stands: profile bp35 first. **If the rebuild is under about 20% of the samples, it isn't the main cost**, and this reading is wrong for crowded boards.

## WHAT THIS CHANGES

- **The order, for Isaiah to set:** (1) profile bp35, then build the relational-slots cache (approved 10-23), measured against the refuter; (2) the other per-check rebuilds (the library-fit index, the growing-record walks), found the same way; (3) the central store as ruled, with dedup when saving.
- Nothing is built, moved or deleted until Isaiah orders it.

## Sources

- [SQLite: Query Planning](https://www.sqlite.org/queryplanner.html)
- [Wikipedia: Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law)
- [Wikipedia: Memoization](https://en.wikipedia.org/wiki/Memoization)
- Knuth, D. E. (1974). Structured Programming with go to Statements. *ACM Computing Surveys* 6(4), 261–301.
- Aho, Lam, Sethi & Ullman, *Compilers: Principles, Techniques, and Tools* (2nd ed.), the code-optimisation chapter.
