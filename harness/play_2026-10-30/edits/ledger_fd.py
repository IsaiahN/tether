p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
assert "\r\n" not in s
anchor = "- **THE _tiers NAME TIE -> THE RECORDED DRAW"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **(2a) ONE DEFINITION ONCE PER FIT (the S2L twin; the reviewer 2026-10-21 04:40): TETHER_FIT_DEDUP "
       "(default ON; check switch TETHER_FIT_DEDUP_CHECK).** Names holding one definition walked the same "
       "candidates and priced each again (78% of a fit's candidate walks repeat a definition on sp80). In "
       "_library_fit a library Term's candidates (_rebindings) are kept per fit, and each candidate's bindability "
       "(_may_bind, _head_accepts), leftover (_left) and cost (_bits with the fit's units) per fit; everything read "
       "by NAME -- exclusion, refusal, carry credit and price, the first payer, the paying order, the pull -- stays "
       "per name, in the same order. OFF: per name (920dfc7). test_fit_dedup: CHECK on gridworld 380 reuses equal "
       "fresh, 0 disagree, ON's 2,714 rows CHECK's and OFF's; THE CARRY PLANT -- two names of one definition, the "
       "carry crediting one: ON picks the credited name with OFF's carry, crediting either; a carry cached per "
       "definition (the defect) does not pick it. OFF identity vs 920dfc7.\n")
assert "(2a) ONE DEFINITION ONCE PER FIT" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
