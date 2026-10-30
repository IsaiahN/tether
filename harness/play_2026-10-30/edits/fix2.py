import sys
p = sys.argv[1]
s = open(p, encoding='utf-8', newline='').read()
nl = '\r\n'
def rep(a, b):
    global s
    a = a.replace('\n', nl); b = b.replace('\n', nl)
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
rep('''def _held_in_store(folder: str, key: str, role: str, snap: Any, con: Any = None) -> tuple | None:
    """One held row (gen, items) by key: through the load-time snapshot while it is open (the same
    rows as at load), else a read-only connection (the rows now: at load, plus this life's own merged
    entries, which the asker already holds locally)."""''',
'''def _held_in_store(folder: str, key: str, role: str, snap: Any,
                   con: Any = None) -> tuple | None:
    """One held row (gen, items) by key: through the load-time snapshot while it is open (the same
    rows as at load), else a read-only connection (the rows now: at load, plus this life's own
    merged entries, which the asker already holds locally)."""''')
rep('''    set's answers, which were the held rows at load plus the additions minus the discards. Holds only
    this life's additions (the set) and discards (gone)."""''',
'''    set's answers, which were the held rows at load plus the additions minus the discards. Holds
    only this life's additions (the set) and discards (gone)."""''')
rep('''    def discard(self, k) -> None:
        set.discard(self, k)
        self.gone.add(k)''',
'''    def discard(self, k) -> None:
        set.discard(self, k)
        self.gone.add(k)
        b = _LAZY_BASE      # a lazy key's load-time gen, kept for _cap_copy if its row is rewritten
        if b and b["folder"] == self.folder and k[0] == self.sig_repr:
            lk = (b["sig"], k[1], k[2])
            if lk not in b["skip"] and lk not in b["taken"] and lk not in b["kept"]:
                row = _held_in_store(self.folder, k[1], k[2], getattr(self.ag, "_dk_snap", None))
                if row is not None:
                    b["kept"][lk] = row[0]''')
rep('''            rows = con.execute("SELECT s1.s, s2.s, held.gen FROM held JOIN sym s1 ON s1.id = held.key"
                               " JOIN sym s2 ON s2.id = held.role").fetchall()''',
'''            rows = con.execute("SELECT s1.s, s2.s, held.gen FROM held JOIN sym s1 ON "
                               "s1.id = held.key JOIN sym s2 ON s2.id = held.role").fetchall()''')
rep('''            for key, role, gh in rows:
                k = (b["sig"], key, role)
                if (k not in b["skip"] and k not in b["taken"]
                        and not set.__contains__(kn, (kn.sig_repr, key, role))):
                    _LAZY[k] = {"gen": gh, "folder": folder}''',
'''            for key, role, gh in rows:   # a row rewritten this life has a gen not in the load's
                k = (b["sig"], key, role)
                g = b["kept"].get(k, gh if gh in b["gens"] else None)
                if g is not None and k not in b["skip"] and k not in b["taken"]:
                    _LAZY[k] = {"gen": g, "folder": folder}''')
rep('''    """A second store load in one process: the first load's answers are copied into the old sets
    (rows never leave held, and a row is rewritten only for a key this life added or took, so the
    rows now give the first load's answers), and every later load copies, as before."""''',
'''    """A second store load in one process: the first load's answers are copied into the old sets
    (rows never leave held; a row this life rewrote has a gen not in the load's, and a lazy key's
    load gen was kept at its discard), and every later load copies, as before."""''')
rep('''        skip = set()
        for key, role, _gh, _it in v["held"]:
            k = (v["sig"], key, role)
            if k in tether._INDEX_STORE:
                skip.add(k)
            else:
                _PENDING.pop(k, None)
        _LAZY_BASE.update(sig=v["sig"], folder=v["folder"], skip=skip, taken=set())''',
'''        skip, gens = set(), set()
        for key, role, gh, _it in v["held"]:
            k = (v["sig"], key, role)
            gens.add(gh)
            if k in tether._INDEX_STORE:
                skip.add(k)
            else:
                _PENDING.pop(k, None)
        _LAZY_BASE.update(sig=v["sig"], folder=v["folder"], skip=skip, taken=set(), gens=gens,
                          kept={})''')
open(p, 'w', encoding='utf-8', newline='').write(s); print('ok')
