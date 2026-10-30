p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
assert "\r\n" not in s
anchor = "- **CON-6 READS WHERE THE RANKING READS"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **(B) BUILT: THE UNITS ONCE PER FIT (the S2G/S2H/S2I boxes; the reviewer 2026-10-21 01:08, 01:30, 02:02): "
       "TETHER_FIT_UNITS (default ON), check switch TETHER_FIT_UNITS_CHECK.** The benchmark (sp80, seeds 0/0, no wrapper, "
       "3fbb2b3) is 35.72 s/step mean, 20.78 median, 172.09 max; step 6 is _library_fit's own loop (151.9 of 172.5 s). "
       "S2H refuted (B)'s first premise -- _left is 5.5 of the fit's 159.6 s, so running sums and the cutoff save ~5 s "
       "there -- and S2I named it: _units_for, called once per CANDIDATE, 144.0 s over 143,640 calls; from the first "
       "refusal on (step 6) its refusal path rebuilds its memo key per call (O(_not) plus routine_lib, derived on every "
       "read). Nothing in the candidate loop writes gamma's units, the slot's gkey, _not (one writer, a plan refusal), "
       "the library or routine_lib, and _take_pull ends the loop, so the units are taken at the first candidate that "
       "needs them (lazily: the same memo admission) and reused for the fit. OFF: _units_for per candidate (35c283a). "
       "test_fit_units (gridworld_arc_s1, 15 steps, seeds 0/0): CHECK 1,801 reuses equal fresh, 0 disagree, ON's 2,714 "
       "rows = CHECK's; PLANT (one settled two-atom term held before the game, since a cold gridworld settles no "
       "composite, then refused INSIDE the loop under the slot's key) 74 disagree; OFF moves no counter. OFF identity "
       "vs 35c283a: 2,714 rows identical (the new book keys masked). Projected ~286 -> ~142 s on the benchmark; the sp80 "
       "CHECK game and the measured benchmark follow. (A) answered on the way: no slot is fitted twice in any step "
       "(in-step fit memo DROPPED); a within-fit dedup by definition is not exact (_carry_credit reads the name; "
       "DROPPED).\n"
       "- **NAMED, W (memory ceiling), LIFE-SCALE (the reviewer 2026-10-21 02:02):** _units_for's memo key is O(_not) "
       "plus a derived routine_lib on EVERY call for every other caller; _not grows as refusals accumulate, so if it "
       "carries across levels or games this is the tiers scan's class, a cost that grows with the agent's LIFE. The "
       "exact remedy when the numbers ask: version counters bumped at _not's one writer and at routine_lib's inputs' "
       "writers, the key built on them. One 10-min read after the benchmark: _not's size over a life, and whether it "
       "carries. (C), the tiers index, sits beside it under W.\n"
       "- **NAMED, COMPRESSION (not tonight; for refine / E5.2; the reviewer 2026-10-21 02:02):** in one step-6 fit "
       "112,562 of 143,640 candidates (78%) are the SAME definition under DIFFERENT library names (about 4-5 names per "
       "definition among a fit's candidates). Not exact to merge today, since carry credit reads the name; whether "
       "names that share a definition should share one carry record is a design question for after the speed step, "
       "Isaiah's, with the numbers (Fig 13 :39, compression at every level).\n")
assert "(B) BUILT: THE UNITS ONCE PER FIT" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
