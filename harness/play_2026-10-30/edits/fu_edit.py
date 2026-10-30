import os

T = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv"


def edit(p, pairs):
    p = os.path.join(T, p)
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for old, new in pairs:
        old, new = old.replace("\n", nl), new.replace("\n", nl)
        assert s.count(old) == 1, (p, old[:80], s.count(old))
        assert new not in s, (p, "already applied", new[:80])
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("tether.py", [
    ('''_CYCLE_SEQ = armflag.arm("TETHER_CYCLE_SEQ", default=True)
''', '''_CYCLE_SEQ = armflag.arm("TETHER_CYCLE_SEQ", default=True)
# (B), THE UNITS ONCE PER FIT (the S2I box; the reviewer 2026-10-21 02:02): the fit priced every
# candidate with _units_for(slot), whose refusal path rebuilds its memo key per call (~1 ms);
# nothing in the candidate loop writes gamma's units, the slot's gkey, _not, the library or the
# routines, so the units are taken at the first candidate that needs them and reused for the fit.
# OFF: _units_for per candidate (35c283a)
_FIT_UNITS = armflag.arm("TETHER_FIT_UNITS", default=True)
# (B)'s check run: every reuse also takes _units_for fresh and compares; the fresh units are used.
# A measurement switch, never a play setting. OFF: no check
_FIT_UNITS_CHECK = armflag.arm("TETHER_FIT_UNITS_CHECK")
'''),
    ('''    "walk_memo_disagree",               # (A) check run: the kept walk did NOT match
''', '''    "walk_memo_disagree",               # (A) check run: the kept walk did NOT match
    "fit_units_agree",                  # (B) check run: the fit's reused units matched fresh
    "fit_units_disagree",               # (B) check run: the reused units did NOT match
'''),
    ('''        _paying: list = []
        _today = None
''', '''        _paying: list = []
        _today = None
        _uf = None          # (B): the slot's units, taken at the first candidate that needs them
'''),
    ('''                    _cost = self._bits((cand, self._units_for(slot)))
''', '''                    if not _FIT_UNITS:
                        _units = self._units_for(slot)
                    elif _uf is None:
                        _uf = _units = self._units_for(slot)
                    elif _FIT_UNITS_CHECK:
                        _units = self._units_for(slot)
                        _same = _units == _uf
                        _book_add(self.gamma.book,
                                  "fit_units_agree" if _same else "fit_units_disagree")
                        if not _same:
                            self.led.record(self.cycle, "ROUTE", slot, "fit_units_check",
                                            term=n, agree=False,
                                            reads="the fit's reused units differed from fresh (B)")
                    else:
                        _units = _uf
                    _cost = self._bits((cand, _units))
'''),
])
edit("conform/arms.py", [
    ('''    "TETHER_CYCLE_SEQ": "ONE SEQ PER CYCLE (the reviewer 2026-10-20 23:33): every landing in a "
''', '''    "TETHER_FIT_UNITS": "(B), THE UNITS ONCE PER FIT (the S2I box; the reviewer 2026-10-21 02:02): "
                        "_library_fit takes the slot's units at the first candidate that needs "
                        "them and reuses them for the fit (nothing in the loop writes their "
                        "inputs). OFF: _units_for per candidate (35c283a). default ON",
    "TETHER_FIT_UNITS_CHECK": "(B)'s check run: every reuse also takes _units_for fresh and "
                              "compares; the fresh units are used. A measurement switch for "
                              "check runs, never a play setting. default OFF",
    "TETHER_CYCLE_SEQ": "ONE SEQ PER CYCLE (the reviewer 2026-10-20 23:33): every landing in a "
'''),
])
print("ok")
