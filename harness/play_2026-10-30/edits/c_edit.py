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
    # the flags
    ('''_FIT_UNITS_CHECK = armflag.arm("TETHER_FIT_UNITS_CHECK")
''', '''_FIT_UNITS_CHECK = armflag.arm("TETHER_FIT_UNITS_CHECK")
# (C), THE TIERS INDEX (the reviewer 2026-10-21 03:05): _tiers ranked by walking every carried and
# landed (delta kind, entry, target) row and every recency row on each call -- a cost that grew
# with the agent's life. rung() only reads the asked kinds and their types, so the per-entry sums
# it needs are kept indexed by kind and by type, and kept exact at the stores' writers (a landing,
# a recency write; a lineage load bumps a version and the index is rebuilt). OFF: the scan (78520a8)
_TIERS_INDEX = armflag.arm("TETHER_TIERS_INDEX", default=True)
# (C)'s check run: every call also scans and compares the rung sums and the recency map; the scan's
# are used. A measurement switch, never a play setting. OFF: no check
_TIERS_INDEX_CHECK = armflag.arm("TETHER_TIERS_INDEX_CHECK")
'''),
    # the book keys
    ('''    "fit_units_disagree",               # (B) check run: the reused units did NOT match
''', '''    "fit_units_disagree",               # (B) check run: the reused units did NOT match
    "tiers_index_agree",                # (C) check run: the index's rung sums matched the scan
    "tiers_index_disagree",             # (C) check run: they did NOT match
    "tiers_index_fallback",             # (C): a count <= 0 met; that call scanned
'''),
    # the state
    ('''        self._kind_known_dk: Counter = Counter()
''', '''        self._kind_known_dk: Counter = Counter()
        self._kix: dict | None = None   # (C): the tiers index, rebuilt when _kix_ver moves
        self._kix_ver = 0               # bumped by each lineage load of the dk stores
'''),
    # the writer: a landing and its recency
    ('''            if e not in self._dk_this:
                self._dk_this.add(e)
                self._kind_landed_dk[e] += 1
                if _CONSOLIDATE:
                    if _CYCLE_SEQ:
                        self._next_seq(per_landing=False)
                    self._kdk_last[e] = (self.gamma.game, self.level, self.cycle, self._kind_seq)
''', '''            if e not in self._dk_this:
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
'''),
    # the read in _tiers
    ('''            land = {r_: Counter() for r_ in "abc"}
            off = {r_: Counter() for r_ in "abc"}
            for (d, k, tgt), m in itertools.chain(self._kind_landed_dk.items(),
                                                  self._kind_known_dk.items()):
                g_ = rung(d, tgt)
                if g_:
                    land[g_][k] += m
''', '''            land = None
            if _TIERS_INDEX:
                land, last_ix = self._kix_land(kinds, ko)
            if land is None or _TIERS_INDEX_CHECK:
                ix_land = land
                land = {r_: Counter() for r_ in "abc"}
                for (d, k, tgt), m in itertools.chain(self._kind_landed_dk.items(),
                                                      self._kind_known_dk.items()):
                    g_ = rung(d, tgt)
                    if g_:
                        land[g_][k] += m
                if ix_land is not None:            # the check: the scan's sums are used
                    last_scan = {}
                    for (_d, k, _t), v in self._kdk_last.items():
                        last_scan[k] = max(last_scan.get(k, 0), v[3])
                    same = (all(+land[g] == +ix_land[g] for g in "abc")
                            and (not _CONSOLIDATE or last_scan == last_ix))
                    _book_add(self.gamma.book, "tiers_index_agree" if same else
                              "tiers_index_disagree")
                    if not same:
                        self.led.record(self.cycle, "ROUTE", mine, "tiers_index_check",
                                        agree=False, dk=list(dk),
                                        reads="the index's rung sums differed from the scan (C)")
                land_ix_used = False
            else:
                land_ix_used = True
            off = {r_: Counter() for r_ in "abc"}
'''),
    ('''            last: dict = {}
            if _CONSOLIDATE:
                # CONSOLIDATION's recency (the reviewer 04:43 2d, 04:55 3): an entry's latest
                # landing over its K1 keys; it breaks ties only, so the 20:43 order stands
                for (_d, k, _t), v in self._kdk_last.items():
                    last[k] = max(last.get(k, 0), v[3])
''', '''            last: dict = {}
            if _CONSOLIDATE and land_ix_used:
                last = last_ix                     # (C): the per-entry max, kept at its writers
            elif _CONSOLIDATE:
                # CONSOLIDATION's recency (the reviewer 04:43 2d, 04:55 3): an entry's latest
                # landing over its K1 keys; it breaks ties only, so the 20:43 order stands
                for (_d, k, _t), v in self._kdk_last.items():
                    last[k] = max(last.get(k, 0), v[3])
'''),
    # the methods
    ('''    def _pair_counts(self) -> dict:
''', '''    def _kix_build(self) -> dict | None:
        """(C): the tiers index from the stores -- per kind and per type, each entry's summed count
        over the landed and carried rows (one combined count per (kind, entry, target), as the old
        chained scan sums them); each kind's rows by reference; each entry's latest recency. None
        if a count <= 0 is met (the scan keeps such a key with 0; the index cannot), counted."""
        rows_d: dict = {}
        tot_d: dict = {}
        tot_t: dict = {}
        for store in (self._kind_known_dk, self._kind_landed_dk):
            for key, m in store.items():
                if m <= 0:
                    return None
                d, k, _t = key
                if store is self._kind_known_dk or key not in self._kind_known_dk:
                    rows_d.setdefault(d, []).append(key)
                tot_d.setdefault(d, Counter())[k] += m
                tot_t.setdefault(d[0], Counter())[k] += m
        last_k: dict = {}
        for (_d, k, _t), v in self._kdk_last.items():
            last_k[k] = max(last_k.get(k, 0), v[3])
        return {"sig": self._kix_sig(), "rows_d": rows_d, "tot_d": tot_d, "tot_t": tot_t,
                "at": {}, "last_k": last_k}

    def _kix_sig(self) -> tuple:
        """(C): what the index was built from -- the lineage loads' version and each store's
        identity and size. A write past the writers that adds a key or replaces a store moves it,
        and the index rebuilds; one that only changes an existing count does not (the CHECK)."""
        return (self._kix_ver, id(self._kind_known_dk), len(self._kind_known_dk),
                id(self._kind_landed_dk), len(self._kind_landed_dk), id(self._kdk_last),
                len(self._kdk_last))

    def _kix_add(self, e: tuple, m: int) -> None:
        """(C): one landing added to the index exactly as the scan would count it."""
        ix = self._kix
        d, k, tgt = e
        if e not in self._kind_landed_dk and e not in self._kind_known_dk:
            ix["rows_d"].setdefault(d, []).append(e)
        ix["tot_d"].setdefault(d, Counter())[k] += m
        ix["tot_t"].setdefault(d[0], Counter())[k] += m
        at = ix["at"].get((d, tgt))
        if at is not None:
            at[k] += m

    def _kix_land(self, kinds: tuple, ko: tuple) -> tuple:
        """(C): _tiers' rung sums from the index. a = an asked kind's rows whose target is ko; b =
        the asked kinds' other rows; c = the asked TYPES' rows of kinds not asked (rung()'s three
        cases). (land, last) or (None, None) when the index cannot serve (a count <= 0)."""
        ix = self._kix
        if ix is None or ix["sig"] != self._kix_sig():
            ix = self._kix = self._kix_build()
            if ix is None:
                _book_add(self.gamma.book, "tiers_index_fallback")
                return None, None
        qs = set(kinds)
        land = {r_: Counter() for r_ in "abc"}
        for q in qs:
            tot = ix["tot_d"].get(q)
            if not tot:
                continue
            at = ix["at"].get((q, ko))
            if at is None:
                at = Counter()
                for key in ix["rows_d"].get(q, ()):
                    if key[2] == ko:
                        at[key[1]] += self._kind_landed_dk.get(key, 0) + \\
                            self._kind_known_dk.get(key, 0)
                ix["at"][(q, ko)] = at
            land["a"].update(at)
            for k, m in tot.items():
                b = m - at.get(k, 0)
                if b > 0:
                    land["b"][k] += b
        for t in {q[0] for q in qs}:
            tot_t = ix["tot_t"].get(t)
            if not tot_t:
                continue
            asked = [ix["tot_d"].get(q) or {} for q in qs if q[0] == t]
            for k, m in tot_t.items():
                c = m - sum(a.get(k, 0) for a in asked)
                if c > 0:
                    land["c"][k] += c
        return land, ix["last_k"]

    def _pair_counts(self) -> dict:
'''),
])
edit("lineage.py", [
    ('''        for k, n in v["koff"]:
            ag._kind_known_off[k] += n
        rep["kinds_known_dk"] = len(ag._kind_known_dk)
''', '''        for k, n in v["koff"]:
            ag._kind_known_off[k] += n
        ag._kix_ver = getattr(ag, "_kix_ver", 0) + 1    # (C): the tiers index rebuilds
        rep["kinds_known_dk"] = len(ag._kind_known_dk)
'''),
    ('''            for dk_, k, ko, n in g.get("kinds_offered_dk", ()):
                ag._kind_known_off[(tuple(dk_), k, tuple(ko))] += n
        rep["kinds_known_dk"] = len(ag._kind_known_dk)
''', '''            for dk_, k, ko, n in g.get("kinds_offered_dk", ()):
                ag._kind_known_off[(tuple(dk_), k, tuple(ko))] += n
        ag._kix_ver = getattr(ag, "_kix_ver", 0) + 1    # (C): the tiers index rebuilds
        rep["kinds_known_dk"] = len(ag._kind_known_dk)
'''),
])
edit("conform/arms.py", [
    ('''    "TETHER_FIT_UNITS": "(B), THE UNITS ONCE PER FIT (the S2I box; the reviewer 2026-10-21 02:02): "
''', '''    "TETHER_TIERS_INDEX": "(C), THE TIERS INDEX (the reviewer 2026-10-21 03:05): _tiers reads its "
                          "rung sums from per-kind and per-type entry counts kept at the stores' "
                          "writers (a landing, a recency write; a lineage load rebuilds), not by "
                          "scanning every carried row per call. OFF: the scan (78520a8). "
                          "default ON",
    "TETHER_TIERS_INDEX_CHECK": "(C)'s check run: every call also scans and compares the rung sums "
                                "and the recency map; the scan's are used. A measurement switch "
                                "for check runs, never a play setting. default OFF",
    "TETHER_FIT_UNITS": "(B), THE UNITS ONCE PER FIT (the S2I box; the reviewer 2026-10-21 02:02): "
'''),
])
print("ok")
