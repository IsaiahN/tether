import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
("                self.drive.bored() and not (_STARVED_CONTACT and self._starved)):\n",
 "                self.drive.bored() and not (_STARVED_CONTACT and self._aims())):\n"),
("        if _STARVED_CONTACT and self._starved and take in (None, \"probe\"):\n"
 "            pick = sorted(self._starved)[0]\n"
 "            if _A1_STARVED and len(self._starved) > 1:\n",
 "        aims = self._aims()\n"
 "        if _STARVED_CONTACT and aims and take in (None, \"probe\"):\n"
 "            pick = sorted(aims)[0]\n"
 "            if _A1_STARVED and len(aims) > 1:\n"),
("                pick = self._choice(\"starved\", None, [(s, None, None) for s in self._starved],\n"
 "                                    {s: self.outstanding(s) for s in self._starved},\n"
 "                                    self._seen_n(\"starved\", self._probe_n, self._starved))\n",
 "                pick = self._choice(\"starved\", None, [(s, None, None) for s in aims],\n"
 "                                    {s: self.outstanding(s) for s in aims},\n"
 "                                    self._seen_n(\"starved\", self._probe_n, aims))\n"),
("        starved = _STARVED_CONTACT and bool(self._starved)\n",
 "        starved = _STARVED_CONTACT and bool(self._aims())\n"),
("            res[\"probe\"] = max(self.outstanding(s) for s in self._starved)\n",
 "            res[\"probe\"] = max(self.outstanding(s) for s in self._aims())\n"),
("    def _owner_reads(self, owner: str, state: dict) -> dict:\n",
 "    def _aims(self) -> set:\n"
 "        \"\"\"The probe's aim set: the starved slots, and under 1c (iii) the gaps whose survivors no\n"
 "        press splits (r325 (3)), each until its owner reads anew or its space closes.\"\"\"\n"
 "        return self._starved | set(self._split_aim) if _STOP_RULES else self._starved\n\n"
 "    def _owner_reads(self, owner: str, state: dict) -> dict:\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
