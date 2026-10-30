p = "C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/c_edit.py"
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)


rep("""            if e not in self._dk_this:
                self._dk_this.add(e)
                if self._kix is not None:          # (C): the index follows its writer
                    self._kix_add(e, 1)
                self._kind_landed_dk[e] += 1
                if _CONSOLIDATE:
                    if _CYCLE_SEQ:
                        self._next_seq(per_landing=False)
                    self._kdk_last[e] = (self.gamma.game, self.level, self.cycle, self._kind_seq)
                    if self._kix is not None:
                        lk = self._kix["last_k"]
                        lk[e[1]] = max(lk.get(e[1], 0), self._kind_seq)
""", """            if e not in self._dk_this:
                self._dk_this.add(e)
                # (C): the index follows its writer while it is current; a stale one rebuilds
                ix_ok = self._kix is not None and self._kix["sig"] == self._kix_sig()
                if ix_ok:
                    self._kix_add(e, 1)
                self._kind_landed_dk[e] += 1
                if _CONSOLIDATE:
                    if _CYCLE_SEQ:
                        self._next_seq(per_landing=False)
                    self._kdk_last[e] = (self.gamma.game, self.level, self.cycle, self._kind_seq)
                    if ix_ok:
                        lk = self._kix["last_k"]
                        lk[e[1]] = max(lk.get(e[1], 0), self._kind_seq)
                if ix_ok:
                    self._kix["sig"] = self._kix_sig()
""")
rep('''        return {"ver": self._kix_ver, "rows_d": rows_d, "tot_d": tot_d, "tot_t": tot_t,
                "at": {}, "last_k": last_k}
''', '''        return {"sig": self._kix_sig(), "rows_d": rows_d, "tot_d": tot_d, "tot_t": tot_t,
                "at": {}, "last_k": last_k}

    def _kix_sig(self) -> tuple:
        """(C): what the index was built from -- the lineage loads' version and each store's
        identity and size. A write past the writers that adds a key or replaces a store moves it,
        and the index rebuilds; one that only changes an existing count does not (the CHECK)."""
        return (self._kix_ver, id(self._kind_known_dk), len(self._kind_known_dk),
                id(self._kind_landed_dk), len(self._kind_landed_dk), id(self._kdk_last),
                len(self._kdk_last))
''')
rep('''        if ix is None or ix["ver"] != self._kix_ver:
''', '''        if ix is None or ix["sig"] != self._kix_sig():
''')
rep('''                    land_ix_used = False
                else:
                    land_ix_used = False
            else:
                land_ix_used = True
''', '''                land_ix_used = False
            else:
                land_ix_used = True
''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
