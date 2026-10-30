import sys
sys.dont_write_bytecode = True
p = sys.argv[1]
b = open(p, "rb").read()
n = b.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
open(p, "wb").write(n)
print("lf-only now", n.count(b"\n") - n.count(b"\r\n"))
