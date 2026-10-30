import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
("            bounds, bar = got\n"
 "            low: dict = {}\n",
 "            bounds, bar = got[0], got[1]\n"
 "            stamps = got[2] if len(got) > 2 else {}\n"
 "            low: dict = {}\n"),
("                cause = self._none_cause(prev[0], low, prev[1])\n",
 "                bar_rows = len(self.history(s))\n"
 "                cell_rows = sorted({stamps[n] for n in prev[0] if n in stamps})\n"
 "                # r342 5 (Fig 10 :13): the bounds and the bar compared only over the same rows\n"
 "                cause = (self._none_cause(prev[0], low, prev[1])\n"
 "                         if self._rows_synced(cell_rows, bar_rows) else \"unsynced\")\n"),
("                extra = {\"cause\": cause, \"owes\": cause == \"bound\", \"last_survivors\": len(prev[0]),\n",
 "                extra = {\"cause\": cause, \"owes\": cause == \"bound\", \"last_survivors\": len(prev[0]),\n"
 "                         \"cell_rows\": cell_rows, \"bar_rows\": bar_rows,\n"),
("    @staticmethod\n"
 "    def _none_cause(prev: dict, low: dict, bar_before: float) -> str:\n",
 "    @staticmethod\n"
 "    def _rows_synced(cell_rows: list, bar_rows: int) -> bool:\n"
 "        \"\"\"1c (ii), r342 5: the survivors' cells were priced over the same history the bar reads\n"
 "        now (each cell's stamp equals the bar's row count). Cells with no stamp say nothing.\"\"\"\n"
 "        return all(r == bar_rows for r in cell_rows)\n\n"
 "    @staticmethod\n"
 "    def _none_cause(prev: dict, low: dict, bar_before: float) -> str:\n"),
("        \"\"\"([(term, stored bound)] over the valid cells in the record's order, the bar), or None\n"
 "        where the record cannot judge. 1c reads a survivor's bound rising apart from the bar.\"\"\"\n",
 "        \"\"\"([(term, stored bound)] over the valid cells in the record's order, the bar, {term name:\n"
 "        the history length its cell was priced over}), or None where the record cannot judge. 1c\n"
 "        reads a survivor's bound rising apart from the bar, and only over the same rows.\"\"\"\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
