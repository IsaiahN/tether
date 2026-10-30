import sys
sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
for a, b in [('    """Two eligible gaps on the stored record; the top-ranked one holds one survivor once re-priced."""',
              '    """Two eligible gaps on the stored record; the top-ranked one keeps one survivor re-priced."""'),
             ("  check_s1_mustfail_lazy  MUST-FAIL: re-pricing spied off: the top gap is asked among stale survivors",
              "  check_s1_mustfail_lazy  MUST-FAIL: re-pricing spied off: the top gap is asked among stale\n                          survivors")]:
    if a in s:
        s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
