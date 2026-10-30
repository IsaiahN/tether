p = "docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
anchor = "- **E4a DECISIONS ON A POSSIBLY DEGENERATE GROUP RESIDUAL"
assert s.count(anchor) == 1 and "S2a BUILT, ROUTE TIER 0" not in s
new = ("- **S2a BUILT, ROUTE TIER 0 (2026-10-20; the reviewer 19:54, 20:15): TETHER_FIT_TIER0 (default ON), TETHER_FIT_TIER0_CHECK (default OFF, a check-run switch).** "
       "THE SITE: route called _library_fit on every OWED slot whose bet held (mass 0), every step, and _library_fit keeps no verdict (S1: 30-34% of search work at 14-20 steps). "
       "THE ARGUMENT (read at the write sites): _left is a per-row sum of non-negative costs (log2 alphabet or correction_bits) and pays is strict (cost + left < base); a row the bound term predicted adds 0 to base and >= 0 to every candidate's left, so a full fit that found none finds none again while what it reads otherwise stands. "
       "THE KEY (_fit_key): the trace epoch, the slot's row filter, the bound term, exclude, the slot's alphabet and type, the library's names and gamma's _units_key, the level, the carry log's size, and (when any refusal exists) the gap key with the refusal count. A no-fit is STORED only from a call where _lookup was asked and _spent stayed under STEP_BUDGET after it -- the step budget and _lookup's walk budget are one counter (_index_reach stops on _spent >= STEP_BUDGET; _spent resets only at route's start), so a walk cut by the budget is never stored; _CapReached raises and stores nothing. Route drops the stored verdict at every other fit site (a missed or refuted bet). "
       "test_fit_tier0 (gridworld_arc_s1, 25 steps, ON / OFF / CHECK): ON 1 skip, 37 fits vs OFF 38 (the precondition holds, thinly: gridworld has few owed slots); (b) the CHECK run's skipped fit, run anyway, returned None with the library unmoved, and its rows are OFF's (tier0 / tier0_check rows dropped; the arms row's lists, the proposal's wall_s and the check's book counters masked); (a) route with the bet held skips the fit, with it missed runs it and drops the verdict; (d) a planted term moves every stored key, and removing it restores them; (e) a call at a spent budget and one whose walk ran to the budget store nothing, a full call stores. The ARC proof is the sp80 light test (ON, and a CHECK run on the same lineage)." + nl)
s = s.replace(anchor, new + anchor)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
