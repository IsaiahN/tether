import sys
sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
a = 'r["event"] == "mint" and r["detail"].get("verdict")'
assert s.count(a) == 2, s.count(a)
open(p, "w", encoding="utf-8", newline="").write(s.replace(a, 'r["event"] == "park" and r["detail"].get("verdict")'))
print("ok")
