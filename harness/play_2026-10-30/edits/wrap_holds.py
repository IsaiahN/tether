"""Wrap the two held spans of C1 (A) in `with cap.hold():` (the reviewer 2026-10-22 15:34 (b), 15:40): _mint from
gamma.accept through chain.note_mint(); sweep's pays branch body. Located by exact text; idempotent."""
import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
L = open(p, encoding="utf-8").read().split("\n")
assert not any("with cap.hold():" in x for x in L), "already wrapped"


def wrap(a, b, indent, comment):
    """Lines a..b (0-based, inclusive) are statements at `indent`: put them under a with-block."""
    for i in range(a, b + 1):
        if L[i].strip():
            assert L[i].startswith(" " * indent), (i + 1, L[i][:60])
            L[i] = "    " + L[i]
    L.insert(a, " " * indent + "with cap.hold():   " + comment)


s = next(i for i, x in enumerate(L) if x.startswith("            if pays(ref_ if cred else cost, left, base)"))
e = next(i for i in range(s + 1, len(L)) if L[i].strip() and not L[i].startswith("             "))
wrap(s + 1, e - 1 if L[e - 1].strip() else e - 2, 16,
     "# C1 (A): the re-bind (pull row, install, bind) is one unit (15:34 2)")
a = next(i for i, x in enumerate(L) if x.startswith("        self.gamma.accept(term, seq=len(self.led), residual="))
b = next(i for i in range(a, len(L)) if L[i] == "        self.chain.note_mint()")
wrap(a, b, 8, "# C1 (A): the accepted term and what is written with it cross whole (15:34 (b))")
open(p, "w", encoding="utf-8", newline="\n").write("\n".join(L))
print("wrapped sweep", s + 2, "and mint", a + 1)
