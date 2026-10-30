"""r370: 1e's pair needs two NON-EMPTY disjoint charged sets (_splits), and the row counts the uncharged
last survivors; the must-fail drops non-emptiness. argv: repo root."""
import sys

sys.dont_write_bytecode = True
R = sys.argv[1].rstrip("/")


def edit(rel, pairs):
    p = f"{R}/{rel}"
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (rel, a[:80], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("tether.py", [
 ("                if self._split_disjoint(sa, sb):\n",
  "                if self._splits(sa, sb):\n"),
 ("                        population=\"last_survivors\", last_survivors=len(last),\n",
  "                        population=\"last_survivors\", last_survivors=len(last),\n"
  "                        uncharged=len(sets.get(frozenset(), ())),\n"),
 ("    @staticmethod\n"
  "    def _split_disjoint(a: frozenset, b: frozenset) -> bool:\n"
  "        \"\"\"1e (a): no residual row is charged to both, so each is explained by one of the two.\"\"\"\n"
  "        return not (a & b)\n",
  "    @staticmethod\n"
  "    def _splits(a: frozenset, b: frozenset) -> bool:\n"
  "        \"\"\"1e (a), r370: each of the two explains a row the other does not -- both charged\n"
  "        somewhere, on no row in common. A term charged nowhere explains every row alone.\"\"\"\n"
  "        return bool(a) and bool(b) and not (a & b)\n"),
])

edit("tests/test_remainder.py", [
 ("  check_a_mustfail_overlap  MUST-FAIL: the pair test with disjointness dropped names a pair whose\n"
  "                            charged sets intersect; the real test names none\n",
  "  check_a_mustfail_overlap  MUST-FAIL: the pair test with disjointness dropped names a pair whose\n"
  "                            charged sets intersect; the real test names none\n"
  "  check_a_mustfail_empty    MUST-FAIL (r370): with non-emptiness dropped, a survivor charged on no\n"
  "                            row pairs with another; the real test names none, uncharged 1\n"),
 ("def _remainder(charged: dict, verdict=None, disjoint=None) -> dict:\n",
  "def _remainder(charged: dict, verdict=None, splits=None) -> dict:\n"),
 ("    if disjoint is not None:\n"
  "        ag._split_disjoint = disjoint\n",
  "    if splits is not None:\n"
  "        ag._splits = splits\n"),
 ("    broke = _remainder(charged, disjoint=lambda a, b: a != b)[\"detail\"][\"several\"]\n",
  "    broke = _remainder(charged, splits=lambda a, b: a != b)[\"detail\"][\"several\"]\n"),
 ("def check_c_budget() -> None:\n",
  "def check_a_mustfail_empty() -> None:\n"
  "    charged = {\"rem_a\": set(), \"rem_b\": {0, 1}}\n"
  "    real = _remainder(charged)[\"detail\"]\n"
  "    assert real[\"several\"] == \"no split found among the last survivors\", real[\"several\"]\n"
  "    assert real[\"uncharged\"] == 1, real\n"
  "    broke = _remainder(charged, splits=lambda a, b: not (a & b))[\"detail\"][\"several\"]\n"
  "    assert isinstance(broke, dict) and broke[\"explained_by_b_only\"] == [], (\n"
  "        \"MUST-FAIL: without non-emptiness an uncharged survivor pairs with another\", broke)\n"
  "    print(f\"  MUST-FAIL: non-emptiness dropped names {broke['pair']} though rem_a explains every \"\n"
  "          \"row; the real test names none and reports uncharged 1\")\n\n\n"
  "def check_c_budget() -> None:\n"),
])
print("ok")
