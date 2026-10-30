T = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/tether.py"
s = open(T, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in s else "\n"
s = s.replace(eol, "\n")
assert "_replay_rows" not in s


def once(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)


once("import collections\n", "import collections\nimport copy\n")

once("        # (2a): the definition's own work, once per fit -- nothing in this loop writes its inputs\n"
     "        _dd_reb: dict = {}\n",
     "        # (2a): the definition's own work, once per fit -- nothing in this loop writes its inputs.\n"
     "        # (i): with the ledger rows that work wrote, replayed on a reuse, so the record is OFF's\n"
     "        _dd_reb: dict = {}\n")

once("        def _judge(cand, price, n):\n"
     "            nonlocal _uf\n",
     "        def _since(n0, n1=None, n2=None):\n"
     "            if len(self.led) == n0:\n"
     "                return ()\n"
     "            rs = self.led.rows(n0)\n"
     "            if n1 is not None:\n"
     "                rs = rs[:n1 - n0] + rs[n2 - n0:]      # the once-per-fit units call's rows stay out\n"
     "            for r in rs:\n"
     "                r.pop(\"seq\", None)\n"
     "                r.pop(\"mode\", None)\n"
     "            return tuple(rs)\n"
     "\n"
     "        def _judge(cand, price, n):\n"
     "            nonlocal _uf\n"
     "            _n0 = len(self.led)\n")

once("            if not _may_bind(cand, _st):\n"
     "                return False, None, None\n",
     "            if not _may_bind(cand, _st):\n"
     "                return False, None, None, _since(_n0)\n")
once("            if _TYPED_BIND and not _head_accepts(cand, _st):\n"
     "                return False, None, None\n"
     "            if not price:\n"
     "                return True, None, None\n"
     "            _left = self._left(cand, slot, hist)\n",
     "            if _TYPED_BIND and not _head_accepts(cand, _st):\n"
     "                return False, None, None, _since(_n0)\n"
     "            if not price:\n"
     "                return True, None, None, _since(_n0)\n"
     "            _left = self._left(cand, slot, hist)\n"
     "            _n1 = len(self.led)\n")
once("            else:\n"
     "                _units = _uf\n"
     "            return True, _left, self._bits((cand, _units))\n",
     "            else:\n"
     "                _units = _uf\n"
     "            _n2 = len(self.led)\n"
     "            _cost = self._bits((cand, _units))\n"
     "            return True, _left, _cost, _since(_n0, _n1, _n2)\n")
once("                        _v = _dd_cand[cand] = _fresh\n"
     "                    _ok, _left, _cost = _v\n"
     "                else:\n"
     "                    _ok, _left, _cost = _judge(cand, _BARGAIN_FIT, n)\n",
     "                        _v = _dd_cand[cand] = _fresh\n"
     "                    else:\n"
     "                        self._replay_rows(_v[3])\n"
     "                    _ok, _left, _cost, _ = _v\n"
     "                else:\n"
     "                    _ok, _left, _cost, _ = _judge(cand, _BARGAIN_FIT, n)\n")
once("    def _dedup_check(self, slot: str, n: str, what: str, same: bool) -> None:\n",
     "    def _replay_rows(self, rows: tuple) -> None:\n"
     "        \"\"\"(2a)(i): a reused evaluation records the rows its first evaluation wrote, as OFF does.\"\"\"\n"
     "        for r in rows:\n"
     "            self.led.record(r[\"cycle\"], r[\"step\"], r[\"slot\"], r[\"event\"],\n"
     "                            of=tuple(r[\"of\"]) if r.get(\"of\") is not None else None,\n"
     "                            **copy.deepcopy(r[\"detail\"]))\n"
     "\n"
     "    def _dedup_check(self, slot: str, n: str, what: str, same: bool) -> None:\n")
open(T, "w", encoding="utf-8", newline="").write(s.replace("\n", eol))
print("ok")
