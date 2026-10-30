p = "test_hyp_draw.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
i, j = s.index('"""S0'), s.index("    python test_hyp_draw.py")
new = nl.join([
    '"""S0, THE PER-CANDIDATE DRAW (TETHER_HYP_DRAW; the reviewer 2026-10-20 18:18 CDT).',
    "gridworld_arc_s1, the agent seed pinned, one process, the arm toggled at the call.",
    "",
    "  (1a) LAZY == EAGER UNDER THE NEW DRAW, on test_goal_hyp's world (25 steps): before every",
    "       proposal an oracle copy of the agent runs the EAGER path (every tied member route-checked)",
    "       and records which were routable; the real proposal, lazy, must pick the lowest-hash",
    "       routable of them (frontier.draw_order), with checks lazy <= eager on each, < in total.",
    "  (1b) A PLANTED TIE GROUP of 50 (the board's own conditions, one rank group), the routable",
    "       members known (every tenth): the lazy pick is the lowest-hash routable, found at its",
    "       place in the hash order (checks < 50); OFF checks all 50.",
    "  The OFF arm's bit-for-bit identity (2) and the other A1 sites (3) are ledger runs, not here.",
    "", ""])
open(p, "w", encoding="utf-8", newline="").write(s[:i] + new + s[j:])
