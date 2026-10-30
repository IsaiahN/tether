p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
assert "\r\n" not in s
anchor = "- **ONE SEQ PER CYCLE BUILT: TETHER_CYCLE_SEQ"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **CON-6 READS WHERE THE RANKING READS (the reviewer 2026-10-21 00:27; the read 00:58):** test_consolidate "
       "CON-6 asserted the two-game SUM on _kind_known_n, which the memory store leaves EMPTY by design ('the trio "
       "stays EMPTY'), so it was red. The read (CON-6's own scenario, a temp lineage): the agent HOLDS the sum where "
       "_tiers and _pair_counts read it -- 2,687 of 2,687 (dk, entry, target) rows landed in both games load "
       "_kind_known_dk n = the sum, the store pairs 9 of 9; none of the 2,705 both-game 7l keys is in t2 (each has a "
       "dk landing), so t2's own count was not exercised there. Answer (i): a test-side fix. CON-6 now asserts the "
       "sum on the dk rows always, and under the memory store on the store's t2 and pairs (else _kind_known_n); MF: "
       "an overwrite instead of an add differs on 2,687 rows. test_consolidate joins the per-commit set; the "
       "deferred reds are 7.\n")
assert "CON-6 READS WHERE THE RANKING READS" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
