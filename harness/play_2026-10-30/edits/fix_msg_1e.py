import sys
sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
for a, b in (("- tests/test_remainder.py (12):", "- tests/test_remainder.py (11):"),
             ("55 result lines rc 0 (test_remainder 12, test_stop_rules 20,",
              "55 result lines rc 0 (test_remainder 11, test_stop_rules 20,")):
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("ok")
