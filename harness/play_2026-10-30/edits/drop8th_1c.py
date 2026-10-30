"""1c's rebase: drop the 8th cell field (hist_n) and the 'unsynced' cause -- 1c reads the re-priced, current
record (r346, r349: staleness is each cell's own c[0]). argv: repo root."""
import sys

sys.dont_write_bytecode = True
p = sys.argv[1].rstrip("/") + "/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n"
pairs = [
 ("    def _divide_open(self, slot: str, tri: tuple, kind: tuple, base: float, units: tuple,\n"
  "                     hist_n: int | None = None):\n",
  "    def _divide_open(self, slot: str, tri: tuple, kind: tuple, base: float, units: tuple):\n"),
 ("        self._dv = {\"mint\": sp[\"mints\"], \"base_prev\": sp[\"base\"], \"krec\": krec, \"now\": set(),\n"
  "                    \"hist_n\": hist_n,\n",
  "        self._dv = {\"mint\": sp[\"mints\"], \"base_prev\": sp[\"base\"], \"krec\": krec, \"now\": set(),\n"),
 ("            got = self._space_bounds(s)\n"
  "            if got is None:\n"
  "                continue                          # the record cannot judge this frame\n"
  "            bounds, bar = got[0], got[1]\n"
  "            stamps = got[2] if len(got) > 2 else {}\n",
  "            got = self._space_bounds(s, \"reprice\")   # r346: 1c reads a CURRENT record only\n"
  "            if got is None:\n"
  "                continue                          # the record cannot judge this frame\n"
  "            bounds, bar = got\n"),
 ("                bar_rows = len(self.history(s))\n"
  "                cell_rows = sorted({stamps[n] for n in prev[0] if n in stamps})\n"
  "                # r342 5 (Fig 10 :13): the bounds and the bar compared only over the same rows\n"
  "                cause = (self._none_cause(prev[0], low, prev[1])\n"
  "                         if self._rows_synced(cell_rows, bar_rows) else \"unsynced\")\n",
  "                # r342 5 (Fig 10 :13): the bounds and the bar over the same rows -- the bounds are\n"
  "                # re-priced to the gap's current residual rows (r349: each cell's own c[0])\n"
  "                cause = self._none_cause(prev[0], low, prev[1])\n"),
 ("                         \"cell_rows\": cell_rows, \"bar_rows\": bar_rows,\n", ""),
 ("        the seventh the cost it was priced at, so S1 reads its stored bound (r327); the eighth the\n"
  "        history length it was priced over, so 1c compares it with the bar's own (r342 5).\"\"\"\n",
  "        the seventh the cost it was priced at, so S1 reads its stored bound (r327).\"\"\"\n"),
 ("                cost, dv.get(\"hist_n\") if dv is not None else None)\n",
  "                cost)\n"),
 ("                rkey = self._divide_open(slot, _tri, _divide_kind(gap), base, _units, len(hist))\n",
  "                rkey = self._divide_open(slot, _tri, _divide_kind(gap), base, _units)\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
