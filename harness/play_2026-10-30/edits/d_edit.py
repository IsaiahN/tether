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
    ('''_WALK_MEMO_CHECK = armflag.arm("TETHER_WALK_MEMO_CHECK")
''', '''_WALK_MEMO_CHECK = armflag.arm("TETHER_WALK_MEMO_CHECK")
# (D), THE KIND HOIST (the S2E box, 2026-10-20 23:08): inside one _index_reach call the slots never
# change (only __init__, retarget and _present replace them), so an owner's _kind is constant there;
# the walk memo's landings read it once per owner per call. OFF: _kind per landing (a88909d)
_KIND_HOIST = armflag.arm("TETHER_KIND_HOIST", default=True)
'''),
    ('''                         tallied: bool, pno: bool, views: dict, causes: dict,
                         refused: Counter) -> None:
''', '''                         tallied: bool, pno: bool, views: dict, causes: dict,
                         refused: Counter, kinds: dict | None = None) -> None:
'''),
    ('''            self._walk_apply(rec, key, sig, views, causes, refused, replay=True)
            return
''', '''            self._walk_apply(rec, key, sig, views, causes, refused, replay=True, kinds=kinds)
            return
'''),
    ('''        self._walk_apply(fresh, key, sig, views, causes, refused, replay=False)
''', '''        self._walk_apply(fresh, key, sig, views, causes, refused, replay=False, kinds=kinds)
'''),
    ('''    def _walk_apply(self, rec: dict, key: str, sig: Any, views: dict, causes: dict,
                    refused: Counter, replay: bool) -> None:
''', '''    def _walk_apply(self, rec: dict, key: str, sig: Any, views: dict, causes: dict,
                    refused: Counter, replay: bool, kinds: dict | None = None) -> None:
'''),
    ('''        if _7L_KIND:
            for role, a, b, t_ in rec["landed"]:
                self._land_kind((key, role, self._kind(a), self._kind(b)),
                                dk=self._dk_of.get(t_), slot=t_)
''', '''        if _7L_KIND:
            for role, a, b, t_ in rec["landed"]:
                if kinds is None:
                    ka, kb = self._kind(a), self._kind(b)
                else:          # (D): one _kind per owner per _index_reach call
                    ka = kinds[a] if a in kinds else kinds.setdefault(a, self._kind(a))
                    kb = kinds[b] if b in kinds else kinds.setdefault(b, self._kind(b))
                self._land_kind((key, role, ka, kb), dk=self._dk_of.get(t_), slot=t_)
'''),
    ('''        _pno = _PAIR_NOT_OBJECT and ("~" in mine or "~" in partner)
        for i_, (key, _w) in enumerate(lit):
''', '''        _pno = _PAIR_NOT_OBJECT and ("~" in mine or "~" in partner)
        kinds: dict | None = {} if _KIND_HOIST else None
        for i_, (key, _w) in enumerate(lit):
'''),
    ('''                self._walk_memo_entry(lib, key, slot, mine, partner, others, targets, comp, atoms,
                                      sig, tally is not None, _pno, views, causes, refused)
''', '''                self._walk_memo_entry(lib, key, slot, mine, partner, others, targets, comp, atoms,
                                      sig, tally is not None, _pno, views, causes, refused, kinds)
'''),
])
edit("conform/arms.py", [
    ('''    "TETHER_G1_SUFFIX": "G1-S (the reviewer 2026-10-18 11:19): G1 asks on a pair reading's base "
''', '''    "TETHER_KIND_HOIST": "(D) (the S2E box, 2026-10-20 23:08): inside one _index_reach call the "
                         "slots never change, so the walk memo's landings read each owner's _kind "
                         "once per call. OFF: _kind per landing (a88909d). default ON",
    "TETHER_G1_SUFFIX": "G1-S (the reviewer 2026-10-18 11:19): G1 asks on a pair reading's base "
'''),
])
print("ok")
