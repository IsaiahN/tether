"""Undo the hold wrongly put on _hold_invention's accept span; put it on _mint's (the one ruled)."""
import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
L = open(p, encoding="utf-8").read().split("\n")
TAG = "        with cap.hold():   # C1 (A): the accepted term and what is written with it cross whole (15:34 (b))"
w = [i for i, x in enumerate(L) if x == TAG]
assert len(w) == 1, w
i0 = w[0]
fn = max(i for i in range(i0) if L[i].startswith("    def "))
assert "_hold_invention" in L[fn], L[fn]
end = next(i for i in range(i0 + 1, len(L)) if L[i] == "            self.chain.note_mint()")
for i in range(i0 + 1, end + 1):
    if L[i].strip():
        assert L[i].startswith("            "), (i + 1, L[i][:50])
        L[i] = L[i][4:]
del L[i0]
a = next(i for i, x in enumerate(L) if x.startswith("        self.gamma.accept(term, seq=len(self.led), residual=")
         and "_mint" in L[max(j for j in range(i) if L[j].startswith("    def "))])
b = next(i for i in range(a, len(L)) if L[i] == "        self.chain.note_mint()")
for i in range(a, b + 1):
    if L[i].strip():
        assert L[i].startswith("        "), (i + 1, L[i][:50])
        L[i] = "    " + L[i]
L.insert(a, "        with cap.hold():   # C1 (A): the accepted term and what is written with it")
L.insert(a + 1, "            # cross whole (the reviewer 2026-10-22 15:34 (b))")
open(p, "w", encoding="utf-8", newline="\n").write("\n".join(L))
print("undone at", i0 + 1, "| mint hold at", a + 1, "through", b + 2)
