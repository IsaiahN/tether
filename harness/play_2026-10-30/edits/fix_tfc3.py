import sys
sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
R = [
    ("import arc_holdout, lineage, lineage_store as ls, tether\n",
     "import arc_holdout, compile_term, lineage, lineage_store as ls, tether\n"),
    ("        lib, rd = self._inv_library(), compile_term.readings()\n",
     "        lib, rd = self._inv_library(), compile_term.readings()\n"
     "        assert lib is not None, \"C3: precondition: the private library\"\n"),
    ("    assert r[\"lib_terms\"] == [pl[\"before\"]], (\"C3: a fresh load holds the earlier term only\", r)\n",
     "    assert r[\"lib_terms\"] == [pl[\"before\"]], (\"C3: a fresh load holds the earlier term only\", r)\n"
     "    ic = r[\"inv_carried\"]\n"
     "    assert len(ic) == 1 and ic[0][\"reinvented\"] == [\"planted_before\"] and not ic[0][\"refused\"], (\n"
     "        \"C3: the carried invention (a real template) must re-invent\", ic, r[\"plants\"])\n"),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
