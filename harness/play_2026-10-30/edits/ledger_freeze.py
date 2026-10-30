p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in s else "\n"
s = s.replace(eol, "\n")
old = ("(2a) STAYS ON for now, marked exact, gain unshown. FREEZE (L4), ruled: "
       "every speed arm whose gain was not shown on a pair goes OFF in the shipped default (today (2a) and S2a), "
       "re-read at freeze.")
new = ("(2a) STAYS ON, marked exact, gain unshown. [The 06:46 freeze rule -- unshown-gain speed arms OFF at freeze -- "
       "is WITHDRAWN: ISAIAH 2026-10-21 15:15, \"lets not switch those off\" (via the reviewer 15:16). (2a) "
       "TETHER_FIT_DEDUP and S2a TETHER_FIT_TIER0 stay ON in the shipped default, both exact, gain unshown.]")
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", eol))
print("ok")
