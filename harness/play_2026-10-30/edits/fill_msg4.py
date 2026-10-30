import sys
sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
assert s.count("RESULTLINES") == 1
open(p, "w", encoding="utf-8").write(s.replace("RESULTLINES", "35"))
print("ok")
