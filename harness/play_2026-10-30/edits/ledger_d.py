p = "docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
assert "\r\n" not in s
# (1) the export list gains the hash seed (the reviewer 2026-10-20 23:33 item 2)
tail = " Known: RAM 16 GB CPU / ~13 GB GPU (Isaiah 10-19); one submission a day, a scalar back (CLAUDE.md)."
assert s.count(tail) == 1
add = (" (K6, the reviewer 2026-10-20 23:33) the submission runner pins PYTHONHASHSEED as the local wrappers do, "
       "belt and braces even after TETHER_CYCLE_SEQ: any other set-order dependence would otherwise differ between "
       "Kaggle and here; a one-time grep for set-iteration-ordered numbering that feeds a decision is NAMED, a 10-min "
       "read after the speed builds.")
assert add not in s
s = s.replace(tail, tail + add)
# (2) the (D) line and the two rulings, after the K line
anchor = "- **K REWRITTEN ON A PLANTED MEETING; test_k1 GREEN"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **(D) BUILT: THE KIND HOIST (the S2E box 2026-10-20 23:08; the reviewer 23:24, 23:33): TETHER_KIND_HOIST "
       "(default ON).** S2E found the walk's overhead beyond _compiled was _kind (6.1 s of 8 sp80 steps, 315,864 calls, "
       "two per landing in _walk_apply), not the ask replay (0.08 s; the reviewer's expectation refuted). Inside one "
       "_index_reach call the slots never change (only __init__, retarget and _present replace them), so an owner's "
       "_kind is constant there: _index_reach makes one kinds dict per call and _walk_apply reads each owner once. "
       "OFF: _kind per landing (a88909d). test_kind_hoist (gridworld_arc_s1, 15 steps, agent and hash seeds pinned): "
       "ON's 2,714 rows = OFF's and the five kind stores the landings write (_kind_landed 5,168, _kind_pairs, "
       "_kind_landed_dk, _kdk_last, _kind_last) equal; _kind calls 2,196 ON vs 94,328 OFF; MF a planted kind moves all "
       "five. OFF identity vs a88909d: 2,714 rows identical. The sp80 ON/OFF pair is S2F. FOUND ON THE WAY: with the "
       "hash seed unpinned two ON runs differ in _kdk_last / _kind_last (same entries and cycles, different "
       "_kind_seq): landings within a cycle are numbered in set-iteration order, an invented recency. RULED (23:33): "
       "one seq per cycle, equal recency falls to the A1 tie rule (TETHER_CYCLE_SEQ, its own commit after S2F, before "
       "(C)).\n"
       "- **NEVER OPEN THE LINEAGE'S memory.db IN PLACE, EVEN READ-ONLY (the reviewer 2026-10-20 23:24):** a mode=ro "
       "open of the WAL database created memory.db-shm and -wal in the lineage at 23:07 (memory.db untouched; "
       "restored through ds_point, RESTORE_LOG). Read the restore point's copy, with immutable=1.\n")
assert "(D) BUILT: THE KIND HOIST" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
