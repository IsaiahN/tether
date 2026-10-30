import sys
sys.dont_write_bytecode = True
src, dst, sha = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding="utf-8", newline="").read()
assert s.count("A2SHA") == 2, s.count("A2SHA")
s = s.replace("A2SHA", sha).replace("\r\n", "\n").replace("\n", "\r\n")
open(dst, "w", encoding="utf-8", newline="").write(s)
print("ok")
