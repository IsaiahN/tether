import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
# the arm
("_ASK = armflag.arm(\"TETHER_ASK\", default=True)\n",
 "_ASK = armflag.arm(\"TETHER_ASK\", default=True)\n"
 "# 1c STOP_RULES (the reviewer 2026-10-29 r325, r327, r337; Fig 5 :10-14, Fig 9 :42): read from 1a's\n"
 "# space after each step -- HELD (one survivor with a risky settle: the gap leaves 1b), MECHANISM\n"
 "# BROKEN (the survivors ran out: the slot owes), SPLIT REFUSED (1b abstained: the gap's owner joins\n"
 "# the probe's aim). They stop asking and never bind. Needs TETHER_ASK. ON; conform/arms.py\n"
 "_STOP_RULES = armflag.arm(\"TETHER_STOP_RULES\", default=True)\n"),
# _survivors -> _space_survivors
("        on a row may still be the best there is (Fig 9 :40). Ranked by deficit, lowest first.\"\"\"\n"
 "        if not _DIVIDE or slot not in self._space:\n"
 "            return []\n"
 "        seen = self._tally.get(slot)\n"
 "        held = self.gamma.library[self.bound.get(slot, IDN)]\n"
 "        if seen is None or seen[0] != self._divide_key(slot, held):\n"
 "            return []\n",
 "        on a row may still be the best there is (Fig 9 :40). Ranked by deficit, lowest first.\"\"\"\n"
 "        return self._space_survivors(slot) or []\n\n"
 "    def _space_survivors(self, slot: str) -> list | None:\n"
 "        \"\"\"S1 where the record can judge, else None (no space, or its tally's key is stale) -- so\n"
 "        1c (ii) tells 'none survive' from 'the record cannot say'.\"\"\"\n"
 "        if not _DIVIDE or slot not in self._space:\n"
 "            return None\n"
 "        seen = self._tally.get(slot)\n"
 "        held = self.gamma.library[self.bound.get(slot, IDN)]\n"
 "        if seen is None or seen[0] != self._divide_key(slot, held):\n"
 "            return None\n"),
# _ask: held gaps are not eligible
("        for s in sorted(self._space):\n"
 "            sv = self._survivors(s)\n"
 "            if len(sv) >= 2:\n"
 "                elig[s] = sv\n",
 "        for s in sorted(self._space):\n"
 "            if _STOP_RULES and self._stop.get(s) == \"held\":\n"
 "                continue                         # 1c (i): asking has stopped on this gap\n"
 "            sv = self._survivors(s)\n"
 "            if len(sv) >= 2:\n"
 "                elig[s] = sv\n"),
# _ask: split refused
("                        reads=\"1b: the press that splits this gap's surviving hypotheses most \"\n"
 "                              \"evenly, or none\")\n"
 "        return r, (slot if r is not None else None)\n",
 "                        reads=\"1b: the press that splits this gap's surviving hypotheses most \"\n"
 "                              \"evenly, or none\")\n"
 "        if r is None and _STOP_RULES:\n"
 "            owner = slot.rsplit(\".\", 1)[0]\n"
 "            self._split_aim[slot] = self._owner_reads(owner, before)\n"
 "            self.led.record(self.cycle, \"PLAN\", slot, \"split_refused\", survivors=len(sv),\n"
 "                            vectors=len(set(vec.values())), owner=owner,\n"
 "                            aims=sorted(self._split_aim),\n"
 "                            reads=\"1c (iii): no press splits the survivors -- new: extend \"\n"
 "                                  \"perception, aim the probe at the gap's owner (Fig 5 :12)\")\n"
 "        return r, (slot if r is not None else None)\n\n"
 "    def _owner_reads(self, owner: str, state: dict) -> dict:\n"
 "        \"\"\"1c (iii): every reading of the gap's owner in this frame; any change lets it go.\"\"\"\n"
 "        return {k: v for k, v in state.items() if k.split(\".\", 1)[0] == owner}\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
