p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
assert "\r\n" not in s
anchor = "- **NEVER OPEN THE LINEAGE'S memory.db IN PLACE, EVEN READ-ONLY"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **THE ARMS SEAT GREEN AGAIN; RED SINCE 10-18 (the reviewer 2026-10-20 23:55, 2026-10-21 00:05):** "
       "conform/arms.py's self-test had failed since 5f40c7c (CONSOLIDATION): TETHER_CONSOLIDATE_CEILING, read raw at "
       "tether._fold_ceiling (and written / deleted by test_consolidate CON-5), was a BYPASS, so 'the seat's OWN guards "
       "are not firing' -- every 'arms row present' reading since then rested on a failing guard, and the seat's 22:14 "
       "green in this session's post was wrong. It is a byte count, not a switch, so it is declared as ONE VALUES row "
       "(the seat's own data table for values, as TETHER_SEED_FROM is), not a second reader in armflag. MF: a planted "
       "raw read under an undeclared name is caught, the declared one is not; the seat exits 0. The seat joins the "
       "per-commit set. ALSO FOUND, NOT FIXED: test_consolidate CON-6 (two games in one lineage: a 7l key landed in "
       "both loads n_landed = the sum) is RED at 582a223 and at its tree with TETHER_CYCLE_SEQ=0 -- an EIGHTH "
       "deferred red, the reviewer's to order.\n")
assert "THE ARMS SEAT GREEN AGAIN" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
