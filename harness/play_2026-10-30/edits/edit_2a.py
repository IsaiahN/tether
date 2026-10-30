import sys

T = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/tether.py"
A = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/conform/arms.py"
s = open(T, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in s else "\n"
s = s.replace(eol, "\n")
assert "_FIT_DEDUP" not in s


def once(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)


# 1. the arm
once('_FIT_UNITS_CHECK = armflag.arm("TETHER_FIT_UNITS_CHECK")\n',
     '_FIT_UNITS_CHECK = armflag.arm("TETHER_FIT_UNITS_CHECK")\n'
     "# (2a), ONE DEFINITION ONCE PER FIT (the S2L twin; the reviewer 2026-10-21 04:40): names that hold\n"
     "# one definition walked the same candidates and priced each again. The work that reads only the\n"
     "# definition -- a library Term's candidates, and each candidate's bindability, leftover and cost --\n"
     "# is done once per fit; everything that reads the NAME (exclusion, refusal, carry credit and price,\n"
     "# the first payer, the paying order, the pull) stays per name, in the same order. OFF: per name\n"
     "# (920dfc7)\n"
     '_FIT_DEDUP = armflag.arm("TETHER_FIT_DEDUP", default=True)\n'
     "# (2a)'s check run: every reuse also computes fresh and compares; the fresh values are used. A\n"
     "# measurement switch, never a play setting. OFF: no check\n"
     '_FIT_DEDUP_CHECK = armflag.arm("TETHER_FIT_DEDUP_CHECK")\n')

# 2. the book keys
once('    "fit_units_disagree",               # (B) check run: the reused units did NOT match\n',
     '    "fit_units_disagree",               # (B) check run: the reused units did NOT match\n'
     '    "fit_dedup_agree",                  # (2a) check run: a reused definition matched fresh\n'
     '    "fit_dedup_disagree",               # (2a) check run: a reused definition did NOT match\n')

# 3. the loop
a = s.index("        for n in retrieval.retrieve(self.gamma.library, gap, track=self.gamma.track_of,\n")
b = s.index("                return self._take_pull(n, cand, slot)\n", a)
b += len("                return self._take_pull(n, cand, slot)\n")
old = s[a:b]
p1 = old.index("            # RE-BIND WHAT ARRIVED WITHOUT A BINDING.")
p2 = old.index("            for cand in self._rebindings(")
rebind_comment = old[p1:p2]
q1 = old.index("                # BEFORE `_explains`, and separately from it")
q2 = old.index("                if not _may_bind(cand, self.slot_types.get(slot)):")
before_comment = old[q1:q2]
r1 = old.index("                # F127 EXPERIMENT")
r2 = old.index("                if _TYPED_BIND and not _head_accepts(")
f127_comment = old[r1:r2]
u1 = old.index("                # F32 ARM D")
u2 = old.index("                if _BARGAIN_FIT:\n                    _left = self._left(")
f32_comment = old[u1:u2]
c1 = old.index("                    if _CARRY_PRICE:\n")
c2 = old.index("                elif not self._explains(cand, slot, hist):")
carry_part = old[c1:c2]


def dedent4(t):
    return "".join(x[4:] if x.startswith("    ") else x for x in t.splitlines(True))


new = (
    "        # (2a): the definition's own work, once per fit -- nothing in this loop writes its inputs\n"
    "        _dd_reb: dict = {}\n"
    "        _dd_cand: dict = {}\n"
    "        _st = self.slot_types.get(slot)\n"
    "\n"
    "        def _judge(cand, price, n):\n"
    "            nonlocal _uf\n"
    + dedent4(before_comment)
    + "            if not _may_bind(cand, _st):\n"
    "                return False, None, None\n"
    + dedent4(f127_comment)
    + "            if _TYPED_BIND and not _head_accepts(cand, _st):\n"
    "                return False, None, None\n"
    "            if not price:\n"
    "                return True, None, None\n"
    "            _left = self._left(cand, slot, hist)\n"
    "            if not _FIT_UNITS:\n"
    "                _units = self._units_for(slot)\n"
    "            elif _uf is None:\n"
    "                _uf = _units = self._units_for(slot)\n"
    "            elif _FIT_UNITS_CHECK:\n"
    "                _units = self._units_for(slot)\n"
    "                _same = _units == _uf\n"
    "                _book_add(self.gamma.book,\n"
    "                          \"fit_units_agree\" if _same else \"fit_units_disagree\")\n"
    "                if not _same:\n"
    "                    self.led.record(self.cycle, \"ROUTE\", slot, \"fit_units_check\",\n"
    "                                    term=n, agree=False,\n"
    "                                    reads=\"the fit's reused units differed from fresh (B)\")\n"
    "            else:\n"
    "                _units = _uf\n"
    "            return True, _left, self._bits((cand, _units))\n"
    "\n"
    "        for n in retrieval.retrieve(self.gamma.library, gap, track=self.gamma.track_of,\n"
    "                                    youth=self.gamma.youth_of):\n"
    "            if n == exclude or (self._not and self._term_refused(n, _gk)):\n"
    "                continue\n"
    + rebind_comment
    + "            _lt = self.gamma.library[n]\n"
    "            if _FIT_DEDUP:\n"
    "                _cands = _dd_reb.get(_lt)\n"
    "                if _cands is None or _FIT_DEDUP_CHECK:\n"
    "                    _fresh = list(self._rebindings(_lt, slot, _guard_pool, _robs))\n"
    "                    if _cands is not None:\n"
    "                        self._dedup_check(slot, n, \"rebindings\", _fresh == _cands)\n"
    "                    _cands = _dd_reb[_lt] = _fresh\n"
    "            else:\n"
    "                _cands = self._rebindings(_lt, slot, _guard_pool, _robs)\n"
    "            for _i, cand in enumerate(_cands):\n"
    "                if _i == 0:\n"
    "                    cand = _lt          # the name's own object, as _rebindings yields it first\n"
    "                if _FIT_DEDUP and _BARGAIN_FIT:\n"
    "                    _v = _dd_cand.get(cand)\n"
    "                    if _v is None or _FIT_DEDUP_CHECK:\n"
    "                        _fresh = _judge(cand, True, n)\n"
    "                        if _v is not None:\n"
    "                            self._dedup_check(slot, n, \"candidate\", _fresh == _v)\n"
    "                        _v = _dd_cand[cand] = _fresh\n"
    "                    _ok, _left, _cost = _v\n"
    "                else:\n"
    "                    _ok, _left, _cost = _judge(cand, _BARGAIN_FIT, n)\n"
    "                if not _ok:\n"
    "                    continue\n"
    + f32_comment
    + "                if _BARGAIN_FIT:\n"
    + carry_part
    + "                elif not self._explains(cand, slot, hist):\n"
    "                    continue\n"
    "                return self._take_pull(n, cand, slot)\n"
)
s = s[:a] + new + s[b:]

# 4. the check helper, beside _carry_ref
once("    def _carry_ref(self) -> tuple[int, float]:\n",
     "    def _dedup_check(self, slot: str, n: str, what: str, same: bool) -> None:\n"
     "        \"\"\"(2a)'s check run: a reused definition against fresh; booked, and a row when they differ.\"\"\"\n"
     "        _book_add(self.gamma.book, \"fit_dedup_agree\" if same else \"fit_dedup_disagree\")\n"
     "        if not same:\n"
     "            self.led.record(self.cycle, \"ROUTE\", slot, \"fit_dedup_check\", term=n, what=what,\n"
     "                            agree=False,\n"
     "                            reads=\"the fit's reused definition differed from fresh (2a)\")\n"
     "\n"
     "    def _carry_ref(self) -> tuple[int, float]:\n")
open(T, "w", encoding="utf-8", newline="").write(s.replace("\n", eol))

a_ = open(A, encoding="utf-8", newline="").read()
aeol = "\r\n" if "\r\n" in a_ else "\n"
a_ = a_.replace(aeol, "\n")
assert "TETHER_FIT_DEDUP" not in a_
old = '    "TETHER_CYCLE_SEQ": "ONE SEQ PER CYCLE'
assert a_.count(old) == 1
a_ = a_.replace(old,
                '    "TETHER_FIT_DEDUP": "(2a), ONE DEFINITION ONCE PER FIT (the S2L twin; the reviewer "\n'
                '                        "2026-10-21 04:40): a library Term\'s candidates and each "\n'
                '                        "candidate\'s bindability, leftover and cost are computed once "\n'
                '                        "per fit; everything read by NAME (exclusion, refusal, carry, "\n'
                '                        "the first payer, the paying order, the pull) stays per name. "\n'
                '                        "OFF: per name (920dfc7). default ON",\n'
                '    "TETHER_FIT_DEDUP_CHECK": "(2a)\'s check run: every reuse also computes fresh and "\n'
                '                              "compares; the fresh values are used. A measurement "\n'
                '                              "switch for check runs, never a play setting. default OFF",\n'
                + old)
open(A, "w", encoding="utf-8", newline="").write(a_.replace("\n", aeol))
print("ok", repr(eol), repr(aeol))
