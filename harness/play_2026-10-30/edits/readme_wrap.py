import sys, hashlib, textwrap
S = sys.argv[1]
p = S + "/README_general_final.md"
t = open(p, encoding="utf-8", newline="").read()
before_words = t.split()
a0 = t.index("These two layers are the swappable parts.")
a1 = t.index("\n\n", a0)
para = " ".join(t[a0:a1].split())
t = t[:a0] + "\n".join(textwrap.wrap(para, 99)) + t[a1:]
b0 = t.index("- **Does not ship:**")
b1 = t.index("\n\n", b0)
item = " ".join(t[b0:b1].split())
t = t[:b0] + "\n".join(textwrap.wrap(item, 99, subsequent_indent="  ")) + t[b1:]
assert t.split() == before_words, "words changed"
assert max(len(l) for l in t.split("\n") if not l.startswith("    ")) <= 100
open(p, "w", encoding="utf-8", newline="\n").write(t)
for n in ("README_general_final.md", "README_arc_final.md"):
    b = open(S + "/" + n, "rb").read()
    print(n, len(b), hashlib.sha256(b).hexdigest())
