"""4e: K11 at the end of the LEDGER's Kaggle export list line (the reviewer 2026-10-22 23:00)."""
import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
anchor = "- **KAGGLE EXPORT LIST, step 14"
i = s.index(anchor)
j = s.index("\n", i)
line = s[i:j].rstrip("\r")
end_old = "the cold-start fixes already make an empty dir work."
assert line.endswith(end_old), line[-120:]
assert "(K11," not in line
K11 = (" (K11, the reviewer 2026-10-22 15:17, 23:00) the HELD RUNNER ITEMS are in git: "
       "docs/kaggle_export/E9_RUNNER_HELD.txt (item 2, the runner backstop at the ceiling; item 3, the "
       "per-worker memory share min(8 GiB, RAM/(2K)); item 4b, the worker goes on after an agent fault; and "
       "tether_agent.run's step_or_recover call, (B)'s Kaggle entry, held), to be reconciled with K1 against "
       "the 10-14 05:55 design. With it two notes: the shipped lineage snapshot must carry a measured "
       "end_path_s (C1 (A)'s reserve; a snapshot that never ran under 1 + (A), as the S3O point, has none, so "
       "every worker's first game runs with no reserve), and the bundle's library_sha changes "
       "(library/library_runtime.py edited in 1d4c4c8).")
s = s[:i] + line + K11 + s[i + len(line):]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
