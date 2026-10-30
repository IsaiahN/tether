"""1e NAMED_REMAINDER (r325, r364) on the (a2) tree. argv: repo root, (a2)'s short sha (the OFF base)."""
import sys

sys.dont_write_bytecode = True
R, A2 = sys.argv[1].rstrip("/"), sys.argv[2]


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
 ("_STOP_RULES = armflag.arm(\"TETHER_STOP_RULES\", default=True)\n",
  "_STOP_RULES = armflag.arm(\"TETHER_STOP_RULES\", default=True)\n"
  "# 1e NAMED_REMAINDER (the reviewer 2026-10-29 r325, r364; Fig 13 :134-139, Fig 9 :4-5, Fig 8 :39-42):\n"
  "# when 1c finds no survivor, a remainder row names what is left -- two of the last survivors whose\n"
  "# charged rows are disjoint (several questions), the gap's kind, and the reach the gap's last mint\n"
  "# proved, in the mint's own words. Record only: nothing reads it. Needs TETHER_STOP_RULES. ON;\n"
  "# conform/arms.py\n"
  "_NAMED_REMAINDER = armflag.arm(\"TETHER_NAMED_REMAINDER\", default=True)\n"),
 ("                                  \"(Fig 5 :13-14); nothing binds\")\n"
  "        if self._space:\n",
  "                                  \"(Fig 5 :13-14); nothing binds\")\n"
  "            if rule == \"none_survive\" and _NAMED_REMAINDER:\n"
  "                self._remainder(s, prev[0], extra[\"cause\"])\n"
  "        if self._space:\n"),
 ("    def _aims(self) -> set:\n",
  "    def _remainder(self, slot: str, last: dict, cause: str) -> None:\n"
  "        \"\"\"1e (r325, r364): what is left when the last survivors are gone. (a) several questions:\n"
  "        two of the LAST SURVIVORS whose charged-row sets over the gap's current residual rows are\n"
  "        disjoint (Fig 9 :4-5), each set read on read by the one row test, the pair whose larger\n"
  "        set is smallest (ties by name); none is a not-found, never a proof (Fig 8 :39). (b) the\n"
  "        gap's kind. (c) reach: the gap's last mint verdict with its own note and cycle.\"\"\"\n"
  "        t0 = time.perf_counter()\n"
  "        seen = self._tally.get(slot)\n"
  "        held = self.gamma.library[self.bound.get(slot, IDN)]\n"
  "        robs = self._residual_obs(slot, held, self.history(slot))\n"
  "        terms = ({t.name: t for cells in (seen[1], seen[2]) for t in cells}\n"
  "                 if seen is not None else {})\n"
  "        sets: dict = {}\n"
  "        for n in sorted(last):\n"
  "            if n in terms:\n"
  "                k = frozenset(i for i, row in enumerate(robs)\n"
  "                              if self._row_wrong(terms[n], slot, row))\n"
  "                sets.setdefault(k, []).append(n)\n"
  "        reps = sorted((names[0], k) for k, names in sets.items())   # one term per charged set\n"
  "        best = None\n"
  "        for i, (na, sa) in enumerate(reps):\n"
  "            for nb, sb in reps[i + 1:]:\n"
  "                if self._split_disjoint(sa, sb):\n"
  "                    rank = (max(len(sa), len(sb)), na, nb)\n"
  "                    if best is None or rank < best[0]:\n"
  "                        best = (rank, na, sa, nb, sb)\n"
  "        if best is None:\n"
  "            several = \"no split found among the last survivors\"\n"
  "        else:\n"
  "            _r, na, sa, nb, sb = best\n"
  "            several = {\"pair\": [na, nb], \"explained_by_a_only\": sorted(sb - sa),\n"
  "                       \"explained_by_b_only\": sorted(sa - sb),\n"
  "                       \"explained_by_both\": len(robs) - len(sa | sb),\n"
  "                       \"shared_charged\": len(sa & sb)}\n"
  "        sp = self._space.get(slot, {})\n"
  "        v = sp.get(\"verdict\")\n"
  "        reach = (None if v is None else \"unreached at this budget\" if v[0] == \"budget_spent\"\n"
  "                 else v[1])\n"
  "        self.led.record(self.cycle, \"MINT\", slot, \"remainder\", cause=cause,\n"
  "                        population=\"last_survivors\", last_survivors=len(last),\n"
  "                        unpriced=sum(1 for n in last if n not in terms), charged_sets=len(sets),\n"
  "                        several=several, kind=list(sp.get(\"kind\") or ()), residual_rows=len(robs),\n"
  "                        verdict=v[0] if v else None, verdict_cycle=v[2] if v else None,\n"
  "                        opened=sp.get(\"opened\"), reach=reach,\n"
  "                        wall_s=round(time.perf_counter() - t0, 4),\n"
  "                        reads=\"1e: what remains when the last survivors are gone -- record only \"\n"
  "                              \"(Fig 13 :134-139)\")\n\n"
  "    @staticmethod\n"
  "    def _split_disjoint(a: frozenset, b: frozenset) -> bool:\n"
  "        \"\"\"1e (a): no residual row is charged to both, so each is explained by one of the two.\"\"\"\n"
  "        return not (a & b)\n\n"
  "    def _aims(self) -> set:\n"),
 ("            detail[\"base_bits\"] = round(base, 3)\n"
  "            if detail[\"verdict\"] == \"no_support\":\n",
  "            detail[\"base_bits\"] = round(base, 3)\n"
  "            if _NAMED_REMAINDER and slot in self._space:\n"
  "                # 1e (r364): the gap's last verdict, in the mint's own words, with its cycle\n"
  "                self._space[slot][\"verdict\"] = (detail[\"verdict\"], detail.get(\"note\"), self.cycle)\n"
  "            if detail[\"verdict\"] == \"no_support\":\n"),
])

edit("conform/arms.py", [
 ("    \"TETHER_STOP_RULES\": \"1c STOP_RULES (the reviewer 2026-10-29 r325, r327, r337; Fig 5 :10-14, \"\n",
  "    \"TETHER_NAMED_REMAINDER\": \"1e NAMED_REMAINDER (the reviewer 2026-10-29 r325, r364; Fig 13 \"\n"
  "                              \":134-139, Fig 9 :4-5, Fig 8 :39-42). When 1c's none_survive fires \"\n"
  "                              \"(any cause), a MINT 'remainder' row on the slot: (a) among the LAST \"\n"
  "                              \"SURVIVORS, each one's charged rows over the gap's current residual \"\n"
  "                              \"rows by the one row test, grouped by set; two with DISJOINT sets \"\n"
  "                              \"are several questions (the pair whose larger set is smallest, ties \"\n"
  "                              \"by name), else 'no split found among the last survivors' -- never \"\n"
  "                              \"'one question'; (b) the gap's kind and residual row count; (c) the \"\n"
  "                              \"gap's last mint verdict (stored on its space with its cycle): \"\n"
  "                              \"budget_spent is 'unreached at this budget', every other verdict \"\n"
  "                              \"carries the mint's own note verbatim. Its wall_s is in TIMINGS. \"\n"
  "                              \"Record only: nothing reads it. Needs TETHER_STOP_RULES. OFF: no \"\n"
  "                              \"row, no stored verdict. default ON\",\n"
  "    \"TETHER_STOP_RULES\": \"1c STOP_RULES (the reviewer 2026-10-29 r325, r327, r337; Fig 5 :10-14, \"\n"),
])

edit("conform/identity_mod_rows.py", [
 ("           (\"stop_read\", \"reprice_s\"))        # 1c's per-step re-price of every open space (r361)\n",
  "           (\"stop_read\", \"reprice_s\"),         # 1c's per-step re-price of every open space (r361)\n"
  "           (\"remainder\", \"wall_s\"))           # 1e's remainder row (r364)\n"),
])

edit("tests/_batch.py", [
 ("    (\"TETHER_STOP_RULES\", \"d148097\"),        # 1c\n"
  ")\n",
  "    (\"TETHER_STOP_RULES\", \"d148097\"),        # 1c\n"
  "    (\"TETHER_NAMED_REMAINDER\", None),        # 1e; its sha comes with the next arm\n"
  ")\n"),
 ("    (\"TETHER_DIVIDE_CREDIT\", \"TETHER_STOP_RULES\", \"1\", None),   # (a2), Isaiah 2026-10-29 15:50\n",
  f"    (\"TETHER_DIVIDE_CREDIT\", \"TETHER_STOP_RULES\", \"1\", \"{A2}\"),   # (a2), Isaiah 2026-10-29 15:50\n"),
])
print("ok")
