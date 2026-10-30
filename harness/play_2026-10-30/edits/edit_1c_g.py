import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
("    def _space_survivors(self, slot: str) -> list | None:\n"
 "        \"\"\"S1 where the record can judge, else None (no space, or its tally's key is stale) -- so\n"
 "        1c (ii) tells 'none survive' from 'the record cannot say'.\"\"\"\n"
 "        if not _DIVIDE or slot not in self._space:\n"
 "            return None\n"
 "        seen = self._tally.get(slot)\n"
 "        held = self.gamma.library[self.bound.get(slot, IDN)]\n"
 "        if seen is None or seen[0] != self._divide_key(slot, held):\n"
 "            return None\n"
 "        bar = self._bar(slot, held)\n"
 "        unit, size, out = math.log2(self.alphabet[slot]), None, {}\n"
 "        for cells in (seen[1], seen[2]):\n"
 "            for t, c in cells.items():\n"
 "                if len(c) < 7 or (c[3] is not None and c[3] != self.cycle):\n"
 "                    continue\n"
 "                if c[5] is not None:\n"
 "                    size = self._decoder_size() if size is None else size\n"
 "                    if c[5] != size:\n"
 "                        continue\n"
 "                bound = c[6] + unit * c[1]\n"
 "                if bound < bar:\n"
 "                    out[t] = bound - bar\n"
 "        return sorted(out, key=lambda t: (out[t], t.name))\n",
 "    def _space_survivors(self, slot: str) -> list | None:\n"
 "        \"\"\"S1 where the record can judge, else None (no space, or its tally's key is stale) -- so\n"
 "        1c (ii) tells 'none survive' from 'the record cannot say'.\"\"\"\n"
 "        got = self._space_bounds(slot)\n"
 "        if got is None:\n"
 "            return None\n"
 "        bounds, bar = got\n"
 "        out = {}\n"
 "        for t, bound in bounds:\n"
 "            if bound < bar:\n"
 "                out[t] = bound - bar\n"
 "        return sorted(out, key=lambda t: (out[t], t.name))\n\n"
 "    def _space_bounds(self, slot: str) -> tuple | None:\n"
 "        \"\"\"([(term, stored bound)] over the valid cells in the record's order, the bar), or None\n"
 "        where the record cannot judge. 1c reads a survivor's bound rising apart from the bar.\"\"\"\n"
 "        if not _DIVIDE or slot not in self._space:\n"
 "            return None\n"
 "        seen = self._tally.get(slot)\n"
 "        held = self.gamma.library[self.bound.get(slot, IDN)]\n"
 "        if seen is None or seen[0] != self._divide_key(slot, held):\n"
 "            return None\n"
 "        unit, size, out = math.log2(self.alphabet[slot]), None, []\n"
 "        for cells in (seen[1], seen[2]):\n"
 "            for t, c in cells.items():\n"
 "                if len(c) < 7 or (c[3] is not None and c[3] != self.cycle):\n"
 "                    continue\n"
 "                if c[5] is not None:\n"
 "                    size = self._decoder_size() if size is None else size\n"
 "                    if c[5] != size:\n"
 "                        continue\n"
 "                out.append((t, c[6] + unit * c[1]))\n"
 "        return out, self._bar(slot, held)\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
