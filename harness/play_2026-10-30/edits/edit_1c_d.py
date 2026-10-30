import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
# state: risky keyed, spent refusals, probed aims
("        self._risky: set = set()        # 1c: (slot, term name) with a risky settle (code space)\n"
 "        self._split_aim: dict = {}      # 1c (iii): refused gap -> its owner's readings then\n",
 "        self._risky: dict = {}          # 1c: (slot, term) -> the space key of its latest risky settle\n"
 "        self._split_aim: dict = {}      # 1c (iii): refused gap -> (owner readings, refusal key)\n"
 "        self._split_spent: dict = {}    # 1c (iii): gap -> the refusal key its aim was spent on\n"
 "        self._split_probed: dict = {}   # 1c (iii): gap -> the owner's readings when the probe pressed\n"),
# settle record keyed by the space's key
("            if _STOP_RULES and self._settle_pred(slot, r)[\"risky\"]:\n"
 "                self._risky.add((slot, name))     # 1c (i): a survival persistence would miss\n",
 "            if _STOP_RULES and self._settle_pred(slot, r)[\"risky\"]:\n"
 "                # 1c (i): a survival persistence would miss, under the space's key of now (r338)\n"
 "                self._risky[(slot, name)] = self._tally.get(slot, (None,))[0]\n"),
# retarget
("            self._stop, self._had_surv, self._risky, self._split_aim = {}, set(), set(), {}\n",
 "            self._stop, self._had_surv, self._risky = {}, set(), {}\n"
 "            self._split_aim, self._split_spent, self._split_probed = {}, {}, {}\n"),
# held judged on the current key + rename (ii)
("                if len(sv) == 1 and (s, sv[0].name) in self._risky:\n"
 "                    rule = \"held\"\n"
 "            elif s in self._had_surv:\n"
 "                rule = \"mechanism_broken\"\n",
 "                if len(sv) == 1 and self._risky.get((s, sv[0].name), self) == self._tally[s][0]:\n"
 "                    rule = \"held\"                 # a risky settle under the current key\n"
 "            elif s in self._had_surv:\n"
 "                rule = \"none_survive\"             # owes; the import route sorts the kind\n"),
("            if rule == \"mechanism_broken\":\n"
 "                self.owed_import.add(s)\n",
 "            if rule == \"none_survive\":\n"
 "                self.owed_import.add(s)\n"),
("                            reads=\"1c: held (one survivor, a risky settle) stops asking; no \"\n"
 "                                  \"survivor left owes a term (Fig 5 :10-14); nothing binds\")\n",
 "                            reads=\"1c: held (one survivor, a risky settle) stops asking; none \"\n"
 "                                  \"surviving owes -- the import route refits before a mint \"\n"
 "                                  \"(Fig 5 :13-14); nothing binds\")\n"),
# leaves: probed first
("        for s, reads in sorted(self._split_aim.items()):\n"
 "            owner = s.rsplit(\".\", 1)[0]\n"
 "            why = (\"space closed\" if s not in self._space\n"
 "                   else \"owner read anew\" if self._owner_reads(owner, now) != reads else None)\n"
 "            if why is not None:\n"
 "                del self._split_aim[s]\n"
 "                self.led.record(self.cycle, \"MINT\", s, \"split_aim_left\", why=why, owner=owner,\n"
 "                                aims=len(self._split_aim),\n"
 "                                reads=\"1c (iii): the owner's readings moved, or the gap closed\")\n",
 "        for s, (reads, rkey) in sorted(self._split_aim.items()):\n"
 "            owner = s.rsplit(\".\", 1)[0]\n"
 "            after = self._owner_reads(owner, now)\n"
 "            probed = self._split_probed.pop(s, None)\n"
 "            why = (\"probed\" if probed is not None else \"space closed\" if s not in self._space\n"
 "                   else \"owner read anew\" if after != reads else None)\n"
 "            if why is None:\n"
 "                continue\n"
 "            del self._split_aim[s]\n"
 "            if why == \"probed\":\n"
 "                self._split_spent[s] = rkey      # once per refusal (r338): a new one re-enters\n"
 "            self.led.record(self.cycle, \"MINT\", s, \"split_aim_left\", why=why, owner=owner,\n"
 "                            aims=len(self._split_aim),\n"
 "                            **({\"before\": probed, \"after\": after} if probed is not None else {}),\n"
 "                            reads=\"1c (iii): the probe pressed at the owner, its readings moved, \"\n"
 "                                  \"or the gap closed\")\n"),
# split refused: refusal key, spent check
("        if r is None and _STOP_RULES:\n"
 "            owner = slot.rsplit(\".\", 1)[0]\n"
 "            self._split_aim[slot] = self._owner_reads(owner, before)\n"
 "            self.led.record(self.cycle, \"PLAN\", slot, \"split_refused\", survivors=len(sv),\n"
 "                            vectors=len(set(vec.values())), owner=owner,\n"
 "                            aims=sorted(self._split_aim),\n",
 "        if r is None and _STOP_RULES:\n"
 "            owner = slot.rsplit(\".\", 1)[0]\n"
 "            rkey = (self._tally[slot][0], frozenset(t.name for t in sv))\n"
 "            spent = self._split_spent.get(slot) == rkey\n"
 "            if not spent:\n"
 "                self._split_aim[slot] = (self._owner_reads(owner, before), rkey)\n"
 "            self.led.record(self.cycle, \"PLAN\", slot, \"split_refused\", survivors=len(sv),\n"
 "                            vectors=len(set(vec.values())), owner=owner, spent=spent,\n"
 "                            aims=sorted(self._split_aim),\n"),
# choose: mark probed
("            self._probe_n[pick] += 1\n"
 "            self._count_kind(\"starved\", pick)\n",
 "            self._probe_n[pick] += 1\n"
 "            self._count_kind(\"starved\", pick)\n"
 "            if _STOP_RULES and pick in self._split_aim:     # 1c (iii): this aim is spent\n"
 "                self._split_probed[pick] = self._owner_reads(pick.rsplit(\".\", 1)[0], before)\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
