p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in s else "\n"
s = s.replace(eol, "\n")
anchor = "- **(2a) ONE DEFINITION ONCE PER FIT"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **(2a)(i) THE EXACT LEDGER (the reviewer 2026-10-21 05:43).** S2O (sp80, 033760f): the CHECK game 379,360 "
       "reuses agree, 0 disagree, every decision identical, its ledger S2K's; but the ON bench dropped 8 duplicate "
       "objective_domain choice rows -- _domain's _PricedDomain writes a choice row per pick (note=_domain_row), inside "
       "_left, two calls below the side-effect scan's reach; gridworld searches no objective domain. Ruled (i): the "
       "fit's cache keeps the rows its first evaluation wrote (the once-per-fit units call's span left out) and a reuse "
       "records them again (same cycle, step, slot, event, of, detail; new seq); the CHECK compares them. "
       "test_fit_dedup (3): rows planted in every _left and _units_for call -- ON's rows are OFF's; without the "
       "replay ON writes 1,540 of 1,920. S2P (four sp80 runs alternating, 033760f): OFF 119.1/106.3 s, ON 100.9/124.0 s "
       "-- one run's spread exceeds (2a)'s projected gain, so (2a) neither costs nor shows time on one run. (ii), "
       "exact-repeat rows never written (Isaiah's 10-19 encode rule), is its own item, TETHER_NO_REPEAT_ROWS, after the "
       "cutoff.\n")
assert "(2a)(i) THE EXACT LEDGER" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", eol))
print("ok", repr(eol))
