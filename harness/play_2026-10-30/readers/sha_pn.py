import sys
sys.dont_write_bytecode = True
p = sys.argv[1] + "/tests/_batch.py"
s = open(p, encoding="utf-8", newline="").read()
a = '    ("TETHER_PLAN_NARROW", None),            # 4; its sha comes with the next arm'
assert s.count(a) == 1
s = s.replace(a, '    ("TETHER_PLAN_NARROW", "e4c3be3"),       # 4')
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
