p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
assert "\r\n" not in s
anchor = "- **(C) BUILT: THE TIERS INDEX"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **(C) MEASURED + THE TWIN AT (C) (the reviewer 2026-10-21 03:46):** the benchmark (sp80, seeds 0/0, no wrapper) "
       "16.52 -> 13.22 s/step (132.2 -> 105.7 s; median 19.63 -> 13.51); the sp80 CHECK game 122 calls agree, 0 disagree, "
       "0 fallback, rows identical; the index ~7.8 MB of containers (477,253 row references, 75,074 per-kind and 11,569 "
       "per-type entries, 85 (kind, target-kind) pairs). Since the baseline 285.8 -> 105.7 s, every step exact. THE TWIN "
       "(same game, its ledger identical to the bench's): steps 4-5 are the walk's misses (_compiled); EVERY miss in "
       "every step is first-ever (its stable key -- entry, slot, mine, partner, others, targets -- never walked before), "
       "so no memo can serve them; (2a) per-fit dedup ~7-12 s (78% of a fit's candidate walks repeat a definition); "
       "the mint cursor's re-yields are ~44% of steps 3-6's yields but skipping them is NOT exact (an earlier call "
       "priced the chain on an older history) -- a behaviour change, for the pacing question.\n"
       "- **THE _tiers NAME TIE -> THE RECORDED DRAW (the reviewer 2026-10-20 23:55 (ii), 2026-10-21 03:05; Isaiah's "
       "10-15 A1 rule: never a name): TETHER_TIERS_DRAW (default ON).** Every _tiers order whose numbers tie fell to "
       "the entry's NAME; it falls to the recorded draw (frontier.draw_key, keyed per lookup: cycle, owner, delta "
       "kind), at T1a-c, T2 (both forms), T1d (both forms) and T5 (molecule, score -- the same class). Only a tied run "
       "is hashed (_draw_ties). OFF: the name (03b793e); the OFF path sorts by (numbers, name), the old keys' order. "
       "test_tiers_draw: a tied pair whose names sort opposite to their draw -- ON in draw order, OFF in name order; ON "
       "under hash seeds 1 and 2, 2,714 gridworld rows identical. OFF identity vs 03b793e; ON's gridworld rows also equal "
       "OFF's (no tie decided anything there). Built before the reviewer's 03:46 (twin first), so set aside as a patch "
       "while the twin ran on a clean 03b793e, re-applied byte-identically (sha db24bbf3df276d62).\n")
assert "THE _tiers NAME TIE -> THE RECORDED DRAW" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
