import sys
p = sys.argv[1]
b = open(p, "rb").read()
assert b"\r\n" not in b, "already CRLF"
open(p, "wb").write(b.replace(b"\n", b"\r\n"))
print("crlf", p)
