import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
# state
("        self._ask_abstained: tuple | None = None   # 1b: (slot, survivors) when no press split\n",
 "        self._ask_abstained: tuple | None = None   # 1b: (slot, survivors) when no press split\n"
 "        self._stop: dict = {}           # 1c: slot -> the stop rule it is in (held / broken)\n"
 "        self._had_surv: set = set()     # 1c: slots whose current space has had a survivor\n"
 "        self._risky: set = set()        # 1c: (slot, term name) with a risky settle (code space)\n"
 "        self._split_aim: dict = {}      # 1c (iii): refused gap -> its owner's readings then\n"),
# risky settle record
("            self._carry_note(name, slot, \"settled\")\n"
 "            self._settled_lvl.add(name)\n"
 "            self.led.record(self.cycle, \"SETTLE\", slot, \"settle\", term=name,\n",
 "            self._carry_note(name, slot, \"settled\")\n"
 "            self._settled_lvl.add(name)\n"
 "            if _STOP_RULES and self._settle_pred(slot, r)[\"risky\"]:\n"
 "                self._risky.add((slot, name))     # 1c (i): a survival persistence would miss\n"
 "            self.led.record(self.cycle, \"SETTLE\", slot, \"settle\", term=name,\n"),
# call site
("        if _DERIVED_WANT and self.trace:\n"
 "            with self._step_scope(\"MINT\"):\n"
 "                self._derived_wants()\n"
 "        if by == \"probe\":\n",
 "        if _DERIVED_WANT and self.trace:\n"
 "            with self._step_scope(\"MINT\"):\n"
 "                self._derived_wants()\n"
 "        if _STOP_RULES and _ASK and _DIVIDE:\n"
 "            self._stop_rules()\n"
 "        if by == \"probe\":\n"),
# retarget
("            self._dw_seen, self._mint_seen = Counter(), Counter()   # slot names do not cross\n",
 "            self._dw_seen, self._mint_seen = Counter(), Counter()   # slot names do not cross\n"
 "        if _STOP_RULES:\n"
 "            self._stop, self._had_surv, self._risky, self._split_aim = {}, set(), set(), {}\n"),
# the pass
("    def _owner_reads(self, owner: str, state: dict) -> dict:\n",
 "    @_in_step(\"MINT\")\n"
 "    def _stop_rules(self) -> None:\n"
 "        \"\"\"1c, read from each open space after the step (r325, r327): (i) HELD -- one survivor with\n"
 "        a risky settle on this slot: the gap leaves 1b; (ii) MECHANISM BROKEN -- the space had\n"
 "        survivors and has none, judged only where the record is current: the slot owes. And (iii)'s\n"
 "        aims leave when their owner's readings change or their space closes. A stop_rule row on\n"
 "        each change of rule; nothing binds.\"\"\"\n"
 "        now = self.trace[-1][2] if self.trace else {}\n"
 "        for s in list(self._stop):\n"
 "            if s not in self._space:\n"
 "                self._stop.pop(s)\n"
 "        self._had_surv &= set(self._space)\n"
 "        for s in sorted(self._space):\n"
 "            sv = self._space_survivors(s)\n"
 "            if sv is None:\n"
 "                continue                          # the record cannot judge this frame\n"
 "            was = self._stop.get(s)\n"
 "            rule = None\n"
 "            if sv:\n"
 "                self._had_surv.add(s)\n"
 "                if len(sv) == 1 and (s, sv[0].name) in self._risky:\n"
 "                    rule = \"held\"\n"
 "            elif s in self._had_surv:\n"
 "                rule = \"mechanism_broken\"\n"
 "            if rule == was:\n"
 "                continue\n"
 "            if rule is None:\n"
 "                self._stop.pop(s, None)\n"
 "                rule_row = \"resumed\"\n"
 "            else:\n"
 "                self._stop[s] = rule_row = rule\n"
 "            if rule == \"mechanism_broken\":\n"
 "                self.owed_import.add(s)\n"
 "            self.led.record(self.cycle, \"MINT\", s, \"stop_rule\", rule=rule_row, was=was,\n"
 "                            survivors=len(sv), term=sv[0].name if len(sv) == 1 else None,\n"
 "                            reads=\"1c: held (one survivor, a risky settle) stops asking; no \"\n"
 "                                  \"survivor left owes a term (Fig 5 :10-14); nothing binds\")\n"
 "        for s, reads in sorted(self._split_aim.items()):\n"
 "            owner = s.rsplit(\".\", 1)[0]\n"
 "            why = (\"space closed\" if s not in self._space\n"
 "                   else \"owner read anew\" if self._owner_reads(owner, now) != reads else None)\n"
 "            if why is not None:\n"
 "                del self._split_aim[s]\n"
 "                self.led.record(self.cycle, \"MINT\", s, \"split_aim_left\", why=why, owner=owner,\n"
 "                                aims=len(self._split_aim),\n"
 "                                reads=\"1c (iii): the owner's readings moved, or the gap closed\")\n\n"
 "    def _owner_reads(self, owner: str, state: dict) -> dict:\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
