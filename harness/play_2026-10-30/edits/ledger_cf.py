p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
assert "\r\n" not in s
anchor = "- **(B) BUILT: THE UNITS ONCE PER FIT"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **_tiers' LATENT CRASH FIXED (found reading _tiers for (C); the reviewer 2026-10-21 03:05):** under "
       "CONSOLIDATE the T2 loop re-bound the name 'last' -- the per-entry recency DICT T1d's sort reads after it -- to a "
       "number, so _tiers raised AttributeError whenever T2 and T1d both held an entry (a carried landing with no delta "
       "kind beside a landed-only one). Latent on the agent's lineage only because its T2 store is empty (0 rows). Fix: "
       "the T2 number has its own name. Planted case (test_k1's OLD setup plus a landed-only entry, the fake world): "
       "raises at 78520a8, passes after; test_k1's OLD case now holds T2 and a non-empty T1d together, with two "
       "landed-only entries whose recency is opposite to their names, so T1d is checked to order by the recency dict. "
       "Gridworld (15 steps, seeds 0/0) identical to 78520a8. THE READ for the same class (ruff PLW2901 and the "
       "redefinition rules over tether.py): two hits, tether.py:1399 (c = dict(c)) and :4267 (prov = {**prov, ...}), "
       "both copy-or-widen, nothing after either loop reads the old value; and the read's limit: these rules do not "
       "see THIS class (a non-loop name re-bound to another type), so the absence of more hits is not a proof. K1 on "
       "the export list (one uncaught step exception ends the game and a worker) stays the guard behind it.\n"
       "- **ALIASES (Isaiah 2026-10-21 02:30, 02:35; the reviewer 02:32, 02:37, replacing 02:33):** a definition held "
       "under several library names is ONE member wearing names (Fig 8 :48-49, Fig 13 :36-39). For the alias design "
       "after the speed step: one canonical definition with an alias list (at the 10-18 consolidation boundary; a new "
       "mint of an existing definition becomes an alias at mint time); EVERY record of origin kept (name, game, slot, "
       "cycle, event); the tally (n_landed, offers, the carry credit's counts) derived per DEFINITION over the DISTINCT "
       "origin events across its aliases (Fig 2 :18-21: one event landed by two names counts once); per-slot and "
       "per-game provenance unpooled wherever a ranking reads context (10-19 governs slots and games, not names). "
       "Must-fails: two aliases on ONE event count 1; on two events, 2; every origin record retrievable after "
       "consolidation. In the speed queue meanwhile: (2a) per-fit dedup by definition -- the work once per "
       "definition, carry still priced per name, the pick unmoved. And a relevance / recency stack ('slide rule') for "
       "the life-scale stores, a design under W after speed: the record kept whole, the hot set ranked by recurrence, "
       "misses read through.\n")
assert "_tiers' LATENT CRASH FIXED" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
