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
    ('''_KIND_HOIST = armflag.arm("TETHER_KIND_HOIST", default=True)
''', '''_KIND_HOIST = armflag.arm("TETHER_KIND_HOIST", default=True)
# ONE SEQ PER CYCLE (the reviewer 2026-10-20 23:33): landings within one cycle are equally recent
# -- the ground gave them no order -- so every landing in a (game, level, cycle) carries that
# cycle's _kind_seq, and a recency tie falls to whatever the reader breaks ties with. OFF: one seq
# per landing, numbered in set-iteration (hash) order (582a223)
_CYCLE_SEQ = armflag.arm("TETHER_CYCLE_SEQ", default=True)
'''),
    ('''        self._kind_seq = 0
        self._kind_cls: Counter = Counter()
''', '''        self._kind_seq = 0
        self._kind_seq_at: tuple | None = None     # the (game, level, cycle) the seq was taken in
        self._kind_events = 0                      # 7l landings: _pair_counts' change signal
        self._kind_cls: Counter = Counter()
'''),
    ('''            self._dk_this.add(("7l", entry, slot))
            self._kind_seq += 1
            self._kind_landed_n[entry] += 1
''', '''            self._dk_this.add(("7l", entry, slot))
            self._kind_events += 1
            self._next_seq()
            self._kind_landed_n[entry] += 1
'''),
    ('''                self._kind_landed_dk[e] += 1
                if _CONSOLIDATE:
                    self._kdk_last[e] = (self.gamma.game, self.level, self.cycle, self._kind_seq)
''', '''                self._kind_landed_dk[e] += 1
                if _CONSOLIDATE:
                    if _CYCLE_SEQ:
                        self._next_seq(per_landing=False)
                    self._kdk_last[e] = (self.gamma.game, self.level, self.cycle, self._kind_seq)
'''),
    ('''    def _pair_counts(self) -> dict:
''', '''    def _next_seq(self, per_landing: bool = True) -> None:
        """The landing's _kind_seq: under TETHER_CYCLE_SEQ it moves once per (game, level, cycle),
        so a cycle's landings are equally recent; OFF it moves once per 7l landing (per_landing)."""
        if not _CYCLE_SEQ:
            if per_landing:
                self._kind_seq += 1
            return
        at = (self.gamma.game, self.level, self.cycle)
        if self._kind_seq_at != at:
            self._kind_seq += 1
            self._kind_seq_at = at

    def _pair_counts(self) -> dict:
'''),
    ('''        sig = (self._kind_seq, len(self._kind_known), len(self._kind_landed), self._kind_store_ver)
''', '''        sig = (self._kind_seq, self._kind_events, len(self._kind_known), len(self._kind_landed),
               self._kind_store_ver)
'''),
])
edit("conform/arms.py", [
    ('''    "TETHER_KIND_HOIST": "(D) (the S2E box, 2026-10-20 23:08): inside one _index_reach call the "
''', '''    "TETHER_CYCLE_SEQ": "ONE SEQ PER CYCLE (the reviewer 2026-10-20 23:33): every landing in a "
                        "(game, level, cycle) carries that cycle's _kind_seq -- equally recent, "
                        "the ground gave them no order -- and _pair_counts' key gains a landing "
                        "counter. OFF: one seq per landing, in set-iteration order (582a223). "
                        "default ON",
    "TETHER_KIND_HOIST": "(D) (the S2E box, 2026-10-20 23:08): inside one _index_reach call the "
'''),
])
print("ok")
