p = "docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
a = "- **SIX PRE-EXISTING REDS DEFERRED TO AFTER STEP 13"
assert s.count(a) == 1
i = s.index(a)
j = s.index(nl, i)
s = s[:j + len(nl)] + ("- **A SEVENTH DEFERRED RED (the reviewer 2026-10-20 19:54):** test_goal_link fails about 2 of 3 runs with the birth seed unpinned, at 89c1ee9 as at 1df6cf7 (3 runs each tree), and passes pinned (TETHER_AGENT_SEED=0); a seed dependence in the test, not read." + nl) + s[j + len(nl):]
anchor = "- **E4a DECISIONS ON A POSSIBLY DEGENERATE GROUP RESIDUAL"
assert s.count(anchor) == 1 and "THE CLOCK BY WHERE THE PRESS LANDS" not in s
new = ("- **THE CLOCK BY WHERE THE PRESS LANDS (2026-10-20; the reviewer 19:54, ruled (c) by data): TETHER_GOAL_HYPOTHESES.** "
       "THE FINDING (the S0 replay box, vc33): the per-candidate draw picked o11.age == o7.age at c2, a frame counter, because _self_moving read the delta table, which is blind to where a click lands, and required every surfaced action -- RESET included, never pressed until c4 -- so on a one-action click game it could never read. "
       "THE READ (10 min, the GQ2C and S0 vc33 ledgers): by c2 two clicks, landing at (46,44) on o9 and (63,0) on o11; o7.age, o0.age and o7.stability moved +1 at both (the rule refuses them at c2), o8.col did not move (accepted); o11.age and o11.col had no reading at the first click (o11 not on the board), so only one landing covers them and the rule leaves them open at c2 -- it refuses o11.age from the second landing on. library/readings.json declares no counters: age and stability carry substrate 'time', as do 25 change readings (drow, dcol, came, add_n, ...), so the substrate is not a counter declaration and (a) had nothing to read. "
       "THE BUILD: _self_moving reads the agent's own transitions (the trace), keyed (action, the object the press landed on) for a positioned action and (action) for a discrete one; the platform's actions (provenance platform-universal) are left out; a slot is self-moving when every press made while it was present moved it by the same nonzero delta, every discrete steering action was pressed, a positioned one landed in two places or more, and at least two keys exist. One source (the trace) replaces the delta table here. "
       "test_hyp_trend T4 replanted on the trace (a -2-every-action slot refused ON, accepted OFF; a slot moved only by one action accepted); T5 a one-action click board with RESET never pressed: a +1-every-click slot is self-moving after landings in two places and not after one; a slot moved only where the click lands on one object is not." + nl)
s = s.replace(anchor, new + anchor)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
