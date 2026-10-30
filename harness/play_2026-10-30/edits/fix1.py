import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
old = '(grep "reproduc|same seed|generation hash" over docs/LEDGER.md: no such line)'
new = '(grep -niE "reproduc|same seed|hash.*not reproducible|generation hash" over docs/LEDGER.md printed 5 lines, none about the generation hash)'
assert s.count(old) == 1
open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
print("ok")
