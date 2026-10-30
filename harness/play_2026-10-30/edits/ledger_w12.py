p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in s else "\n"
s = s.replace(eol, "\n")
anchor = "- **(2a) EXACT, GAIN UNSHOWN; THE PAIR PROTOCOL; THE CUTOFF DROPPED"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **W1 / W2, THE STORE'S KEY MEMOS (S2U, S2V; the reviewer 2026-10-21 15:16, 15:38): "
       "TETHER_STORE_KEY_MEMO and TETHER_LOAD_KEY_MEMO (default ON; check switches *_CHECK).** S2U: outside the moves "
       "an sp80 game spends ~38 s CPU -- lineage.load ~10 s per game (in wire) and lineage.boundary, the lineage "
       "write at the death boundary, 26.9 s wall / 21.8 s CPU per boundary (it runs between steps, so step_s missed "
       "it); imports ~1 s once per process. S2V (cProfile, shares read): the boundary write is CPU in the store's "
       "statements (22.9 s profiled against fsync 0.2, commit 0.24), mostly lineage_store._merge_kinds re-encoding the "
       "same few kind values with json.dumps per row (607,920 key builds; it scales with the game's NEW landings); the "
       "load decodes them back per row (885,038 json.loads; it grows with the whole life -- the W class, later). W1: "
       "one merge keeps each value's string keyed on repr(value) (1, True and 1.0 hash alike and encode apart; their "
       "reprs differ); W2: one load decodes each kind sym id once, reusing the tuple when hashable. test_store_key_memo: "
       "the type plant (a value-keyed memo gives [1] for [True], shown to fail; the memo gives each its fresh string); "
       "two fake games written ON and OFF byte-identical (6 files, memory.db by iterdump; Python's random seeded per "
       "game since a handle's suffix draws from it, an OFF-OFF control identical first; 283,434 encodings reused); "
       "loads ON / OFF / CHECK give equal carried stores (16,535 decodes reused, 0 disagree); a second load in one "
       "process equals a fresh one. Named, not built: the 3.1 s of time.sleep on the boundary path (unattributed), "
       "the (C) index rebuild at load, the compiled-candidate decode, the sqlite close.\n")
assert "W1 / W2, THE STORE'S KEY MEMOS" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", eol))
print("ok")
