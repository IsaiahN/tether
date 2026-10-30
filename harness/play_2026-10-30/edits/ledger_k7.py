p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in s else "\n"
s = s.replace(eol, "\n")
assert "(K7," not in s
i = s.index("- **KAGGLE EXPORT LIST, step 14")
j = s.index("\n", i)
add = (" (K7, the reviewer 2026-10-21 06:24) library_sha moves with LINE ENDINGS: library/library_runtime.py is LF in "
       "the worktree and CRLF in a git-archive export of the same commit (1,094 CRLFs; the other eight library files "
       "byte-identical), so two copies of one library hash apart -- the arms row and any identity or carry check keyed "
       "on it would read the Kaggle export as a different library. At export: hash NORMALIZED content (CRLF -> LF) or "
       "pin library/'s line endings in .gitattributes; must-fail: an LF copy and a CRLF copy of one tree give one "
       "library_sha.")
s = s[:j] + add + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", eol))
print("ok", repr(eol))
