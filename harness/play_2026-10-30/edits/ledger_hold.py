import sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
anchor = "- **E4a DECISIONS ON A POSSIBLY DEGENERATE GROUP RESIDUAL"
assert s.count(anchor) == 1 and "THE TOUCH HOLD FOR A HELD HYPOTHESIS" not in s
new = ("- **THE TOUCH HOLD FOR A HELD HYPOTHESIS (2026-10-20; the reviewer 18:40): TETHER_GOAL_HYPOTHESES.** "
       "THE FINDING (vc33, GQ2C ledger, read 18:48): at c4 the held hypothesis o11.col < o8.col read 0.0 (TOUCHED); the selector does not choose a touch, the exit choice held only system0 (s0_defer), and System 0's untried-first rule pressed RESET, the one action never taken; o11 went unreadable, then read 63 (the reset position): residual 0.0635. The agent reached its own goal and its next act undid it. c5's exit was 'not chosen' (the series popped), not 'no route'. "
       "THE BUILD: while a held hypothesis is TOUCHED, (1) the platform's actions (provenance platform-universal: RESET) are withheld on this board for every exit, through the one Withheld every realisation already honours (_withhold_platform); (2) choose returns a 'hold' (PHASE_OF: directed) with an action the agent's delta table never saw move the condition's parties -- both, whichever holds the want; taken at least once, not the platform's, not positioned (an aimed press is not known still); A1 (_choice 'hyp_still') among several -- and writes a hypothesis_hold row; (3) with no holding action known, System 0 acts with the platform actions withheld, and this is recorded. GQ3's routine HOLD is unchanged (a touched routine already makes no claim). (iii) the repeat row carries hyp_why while a hypothesis is held: acted / not chosen: <arrival> or no series / no route / touched: held with <a> / touched: no holding action known ... / a held routine acted first. "
       "test_hyp_hold: H1 a planted touch (residual 0 exactly while subject and other party keep their values): ON 'hold' with left on o0.row / o1.row, both kept, the next reading confirms (arrived_no_clear); OFF System 0 pressed up and the state moved. H2 no holding action known and one action planted as the platform's, untried: ON System 0 acts with up, the platform action withheld, the row says why; OFF System 0 takes the platform action (untried first). "
       "NOT IN THIS BUILD: the stall's low after a touch-loss (18:40 item 2) -- its condition failed for ordinary goals (the selector reads a sliding window over the whole series, no restart), posted 18:49 with the proposal to restart the stall's low for hypotheses only, where the selector reads no window; built on the reviewer's word." + nl)
s = s.replace(anchor, new + anchor)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
