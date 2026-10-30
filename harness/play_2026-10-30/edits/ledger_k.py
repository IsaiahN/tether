p = "docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
assert "\r\n" not in s
anchor = "- **test_k1 READ FIXED; K NAMED RED (the reviewer 2026-10-20 21:58, 22:20):**"
i = s.index(anchor)
j = s.index("\n", i) + 1
new = ("- **K REWRITTEN ON A PLANTED MEETING; test_k1 GREEN (the reviewer 2026-10-20 22:20, 22:52):** "
       "the old K asked whether process 2's own trajectory happened to meet a delta kind process 1 landed. "
       "Now (a) process 1 reports the delta kind it OFFERED most, and process 2 loads its lineage with this "
       "run's own offered and landed stores emptied (so only the carry can feed T1) and is asked under that "
       "kind: T1a-b list exactly the carried entries under it, first, and today's lit entry after them "
       "(on the fake: (POSITION, -, 2), T1a 1, the lit entry at 1). (b) process 2 holds every carried row "
       "(known_dk 7,533 = written, known_off 7 = written) and some lookup of its own run lists a T1 (4 of 4). "
       "MF-K-CUT: the same ask on an empty lineage lists no T1; MF-K (TETHER_DELTA_KIND=0) stays. The stray CR "
       "df76d13 left in one line is gone (the file is LF). test_k1 joins the per-commit set (176 s).\n")
assert "K REWRITTEN ON A PLANTED MEETING" not in s
s = s[:j] + new + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
