p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in s else "\n"
s = s.replace(eol, "\n")
anchor = "- **(2a)(i) THE EXACT LEDGER"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **(2a) EXACT, GAIN UNSHOWN; THE PAIR PROTOCOL; THE CUTOFF DROPPED (the reviewer 2026-10-21 06:14, 06:24, 06:46).** "
       "S2Q (308f304): the sp80 CHECK game and the bench IDENTICAL on 4,572 rows, every seq compared (379,360 reuses "
       "agree, 0 disagree). S2R, the PAIR PROTOCOL (OFF, ON, OFF, ON alternating, alone, one restore point; CPU per "
       "step = process_time beside wall; a gain counts only outside both spreads): every ledger identical; CPU OFF "
       "108.1/116.8 s, ON 106.4/110.7 s -- (2a)'s gain NOT shown (refuter fired); wall - CPU 1.0-23.0 s per run (the "
       "wall spread is mostly off the CPU). (2a) STAYS ON for now, marked exact, gain unshown. FREEZE (L4), ruled: "
       "every speed arm whose gain was not shown on a pair goes OFF in the shipped default (today (2a) and S2a), "
       "re-read at freeze. METHOD (lesson): a profiled-twin projection built on calls under ~50 us is inflated by the "
       "instrument's per-call overhead -- S2L projected 7-12 s for (2a), the pair showed ~0; (B) and (C) were real "
       "because they removed expensive calls (1 ms units, 118 ms scans); the pair decides. THE WHAT-ELSE-RUNS READ: "
       "the idle machine is quiet (3,192 of 3,192 MHz, High performance, under 4% of a core); Defender real-time ON, "
       "exclusions unreadable without admin -- to Isaiah. THE CUTOFF (S2S, a box replicating _left's loop, its "
       "ledger identical to the bench): an exact cutoff would stop 113,877 of 118,646 first evaluations and skip "
       "347,705 of 458,216 history rows, saving ~4.4 s of a ~110 s game; it would not write 728 choice rows -- 695 "
       "repeats, 29 written again later, and 4 DISTINCT (objective_domain draws on o0.stability, cycles 4-5: frontier "
       "{5 or 11 at 0.0, 1 at ~6.41-6.43}, picks 5, 1, 5, 1). DROPPED from the exact queue (it changes the record), "
       "and its worth was inside the CPU spread anyway. The exact speed queue is empty; what remains is the pacing "
       "question (the mint work budget, which binds in 54 of 72 sp80 searches; the walk's STEP_BUDGET, which never "
       "binds there).\n")
assert "(2a) EXACT, GAIN UNSHOWN" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", eol))
print("ok")
