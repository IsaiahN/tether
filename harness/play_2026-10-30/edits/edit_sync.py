import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
("    def _divide_open(self, slot: str, tri: tuple, kind: tuple, base: float, units: tuple):\n",
 "    def _divide_open(self, slot: str, tri: tuple, kind: tuple, base: float, units: tuple,\n"
 "                     hist_n: int | None = None):\n"),
("        self._dv = {\"mint\": sp[\"mints\"], \"base_prev\": sp[\"base\"], \"krec\": krec, \"now\": set(),\n",
 "        self._dv = {\"mint\": sp[\"mints\"], \"base_prev\": sp[\"base\"], \"krec\": krec, \"now\": set(),\n"
 "                    \"hist_n\": hist_n,\n"),
("                rkey = self._divide_open(slot, _tri, _divide_kind(gap), base, _units)\n",
 "                rkey = self._divide_open(slot, _tri, _divide_kind(gap), base, _units, len(hist))\n"),
("        or before -- a stale stamp never reaches here, `_cannot_pay` recomputes it), else None;\n"
 "        the seventh the cost it was priced at, so S1 reads its stored bound (r327).\"\"\"\n",
 "        or before -- a stale stamp never reaches here, `_cannot_pay` recomputes it), else None;\n"
 "        the seventh the cost it was priced at, so S1 reads its stored bound (r327); the eighth the\n"
 "        history length it was priced over, so 1c compares it with the bar's own (r342 5).\"\"\"\n"),
("                dv[\"mint\"] if dv is not None else 0, self._decoder_size() if read else None,\n"
 "                cost)\n",
 "                dv[\"mint\"] if dv is not None else 0, self._decoder_size() if read else None,\n"
 "                cost, dv.get(\"hist_n\") if dv is not None else None)\n"),
# _space_bounds: return the stamps
("                out.append((t, c[6] + unit * c[1]))\n"
 "        return out, self._bar(slot, held)\n",
 "                out.append((t, c[6] + unit * c[1]))\n"
 "                if len(c) > 7:\n"
 "                    rows[t.name] = c[7]\n"
 "        return out, self._bar(slot, held), rows\n"),
("        unit, size, out = math.log2(self.alphabet[slot]), None, []\n"
 "        for cells in (seen[1], seen[2]):\n",
 "        unit, size, out, rows = math.log2(self.alphabet[slot]), None, [], {}\n"
 "        for cells in (seen[1], seen[2]):\n"),
("        got = self._space_bounds(slot)\n"
 "        return None if got is None else self._s1_of(*got)\n",
 "        got = self._space_bounds(slot)\n"
 "        return None if got is None else self._s1_of(got[0], got[1])\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
