import sys
sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
a = "(lines 58-62: a no-op"
assert s.count(a) == 1
s = s.replace(a, "(lines 59-63: a no-op")
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
