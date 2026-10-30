p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
assert "\r\n" not in s
anchor = "- **THE ARMS SEAT GREEN AGAIN; RED SINCE 10-18"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **ONE SEQ PER CYCLE BUILT: TETHER_CYCLE_SEQ (default ON; the reviewer 2026-10-20 23:33, 23:55, 2026-10-21 "
       "00:05).** Landings within one cycle were numbered in set-iteration (hash) order, an invented recency read by "
       "the recency tie-breaks (_tiers' T1 / T1d / T2 sorts, 7m's pair order). Now _kind_seq moves once per (game, "
       "level, cycle), at that cycle's first landing, and every landing in it carries that seq in _kind_last and "
       "_kdk_last; a recency tie falls to whatever the reader breaks ties with. _pair_counts' cache key gains a "
       "landing counter (_kind_events), since the seq no longer moves at every landing; under OFF it moves exactly "
       "when the seq does. OFF: one seq per landing (582a223). test_cycle_seq: (1) ON under hash seeds 1 and 2 "
       "gives identical _kdk_last (5,339) and _kind_last (5,168) and 2,714 identical rows (masked: the arms row's "
       "pythonhashseed and goal_hypotheses' wall_s); CONTROL: OFF under the same two seeds differs; (3) a planted "
       "two-landing cycle: ON seqs (1, 1), OFF (2, 3). (2) OFF identity vs 582a223: 2,714 rows identical; ON's "
       "gridworld rows also equal OFF's. Built as a patch set aside for the arms-seat fix and re-applied on fec66fd: "
       "the diff equals the saved patch in every line but the blob-id index line (content sha bebdfce76f3fa8cf both). "
       "NAMED, not built: _tiers' final tie is the entry NAME (kv[0]), a standing breach of A1 that equal recency now "
       "reaches more often -- replaced by the recorded draw as its own item right after (C).\n")
assert "ONE SEQ PER CYCLE BUILT" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
