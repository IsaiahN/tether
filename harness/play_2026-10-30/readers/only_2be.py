import sys

p, head = sys.argv[1], sys.argv[2]
full = open(p, "rb").read().decode("utf-8")
base = open(head, "rb").read().decode("utf-8").replace("\r\n", "\n").replace("\n", "\r\n")


def block(t, name):
    i = t.index("def " + name)
    j = t.index("\r\n\r\n\r\ndef ", i)
    return t[i:j]


# the 2b_a check and the imports from HEAD; everything else (the 2b_e change) from the working file
n = "check_2b_a_pass_1_is_the_off_walk_when_no_lag_has_evidence"
out = full.replace(block(full, n), block(base, n))
out = out.replace("import collections\r\nimport contextlib", "import contextlib")
assert out != full
open(p, "wb").write(out.encode("utf-8"))
print("2b_e only")
