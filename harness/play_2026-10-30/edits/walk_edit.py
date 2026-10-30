p = "tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
assert nl == "\r\n"


def rep(old, new):
    global s
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    assert s.count(old) == 1, (old[:80], s.count(old))
    s = s.replace(old, new)


# 1. arms
rep('''_FIT_TIER0_CHECK = armflag.arm("TETHER_FIT_TIER0_CHECK")
''', '''_FIT_TIER0_CHECK = armflag.arm("TETHER_FIT_TIER0_CHECK")
# (A), THE WALK MEMO (the reviewer 2026-10-20 21:18, 21:28): _index_reach keeps each lit entry's
# walk by what it reads -- the library, the atoms (token, signature: the held index is a pure
# function of (signature, entry, role) within a process), the entry, slot, mine, partner, others,
# targets -- and a hit merges it as a walk would, charging _spent the same count and replaying the
# landings (this step's dk) and the asked tally. _index_for's whole-walk store retires under it.
# OFF: walked every time, the whole-walk store as before (6fbdd5f)
_WALK_MEMO = armflag.arm("TETHER_WALK_MEMO", default=True)
# (A)'s check run: each hit is also walked fresh and compared (contributions, refusals, charges,
# landings, asks); the fresh walk is used. OFF: no check
_WALK_MEMO_CHECK = armflag.arm("TETHER_WALK_MEMO_CHECK")
''')
# 2. state
rep('''        self._seen_keys: dict = {m: set() for m in ("reach_index", "compile", "fold", "verdicts",
                                                    "units_for")}''',
    '''        self._seen_keys: dict = {m: set() for m in ("reach_index", "compile", "fold", "verdicts",
                                                    "units_for", "walk")}''')
rep('''        self._reach_index: dict = {}       # M4: distinct compiled terms per description
''', '''        self._reach_index: dict = {}       # M4: distinct compiled terms per description
        self._walk_memo: dict = {}         # (A): one lit entry's walk, by what it reads
        self._ak_rec: Counter | None = None   # (A)'s check: the asks a fresh walk made
''')
# 3. retarget clear
rep('''            for m in (self._reach_index, self._reach_verdicts, self._reach_fold,
                      self._compile_cache, self._units_for_memo, self._frontiers):
                m.clear()''', '''            for m in (self._reach_index, self._reach_verdicts, self._reach_fold,
                      self._compile_cache, self._units_for_memo, self._frontiers,
                      self._walk_memo):
                m.clear()''')
# 4. memo sizes (only under the arm, so OFF's row is unchanged)
rep('''                 "units_for": len(self._units_for_memo), "frontiers": len(self._frontiers)}''',
    '''                 "units_for": len(self._units_for_memo), "frontiers": len(self._frontiers),
                 **({"walk": len(self._walk_memo)} if _WALK_MEMO else {})}''')
# 5. _compiled's two asked-tally sites -> one writer
rep('''                if lineage._MEMORY_STORE and lineage._COMPRESS:
                    # L6a (the reviewer 11:13, fold at ask): an ask is recorded by what was true
                    # when it was asked -- a pair held whole counts on its whole row, any other
                    # slot ask on its (key, role, slot class) alone, so the counter grows by class,
                    # not by instance. Only write_ak reads it; ak_whole's whole rows are unchanged
                    self._ak_asked[(*mkey, None) if mkey in memo else
                                   (self._atoms_token, sig, key, role, None, None,
                                    "#" + lineage._ak_class(slot))] += 1
                elif lineage._MEMORY_STORE:
                    self._ak_asked[skey] += 1     # S4: times asked; only write_ak reads it
''', '''                self._ak_note(key, role, o, x, slot, sig)   # S4: times asked (write_ak reads it)
''')
rep('''            if lineage._MEMORY_STORE:
                self._ak_asked[(*mkey, None)] += 1     # S4: a whole ask, times asked
''', '''            self._ak_note(key, role, o, x, slot, sig)       # S4: a whole ask, times asked
''')
# 6. _index_for retires its whole-walk store under the arm
rep('''            self._k1_trunc = False
            if _REACH_RANK:
                # REACH-LIT-KEY:''',
    '''            self._k1_trunc = False
            if _WALK_MEMO:          # (A): the walk keeps its own per-entry memo
                if _REACH_RANK:
                    return self._index_reach(lib, lit_, slot, mine, cands,
                                             partner=others[0] if others else mine,
                                             late=late, probe=probe, targets=tg)
                return self._index_reach(lib, lit_, slot, mine, others, late=late, probe=probe,
                                         targets=tg)
            if _REACH_RANK:
                # REACH-LIT-KEY:''')
# 7. the per-entry hook in _index_reach (after the late-tier truncation check)
rep('''                self._late = (a_ + 1, na_)
            for role in reach.SINGLE:
                if _pno:''', '''                self._late = (a_ + 1, na_)
            if _WALK_MEMO:
                self._walk_memo_entry(lib, key, slot, mine, partner, others, targets, comp, atoms,
                                      sig, tally is not None, _pno, views, causes, refused)
                continue
            for role in reach.SINGLE:
                if _pno:''')
# 8. the methods, before _index_reach
rep('''    def _index_reach(self, lib: Any, lit: list, slot: str, mine: str, others: tuple,''',
    '''    def _ak_note(self, key: str, role: str, o: str, x: str, slot: str | None, sig: Any,
                 dry: Counter | None = None) -> None:
        """S4's asked tally for one held-role ask (only lineage's write_ak reads it). L6a (the
        reviewer 11:13, fold at ask): an ask is recorded by what was true when it was asked -- a
        pair held whole counts on its whole row, any other slot ask on its (key, role, slot class)
        alone (the compressed store), else on the slot key; a whole ask counts its key. ONE
        writer -- _compiled and the walk memo's replay (A) both call it, so they cannot drift.
        `dry` collects instead of counting."""
        if not lineage._MEMORY_STORE:
            return
        mkey = (self._atoms_token, sig, key, role, o, x)
        if slot is not None and _SLOT_FILTER:
            if lineage._COMPRESS:
                memo = _BOUND_MEMO if self._atoms_token else self._bound_cache
                k = ((*mkey, None) if mkey in memo else
                     (self._atoms_token, sig, key, role, None, None, "#" + lineage._ak_class(slot)))
            else:
                k = (*mkey, slot)
        else:
            k = (*mkey, None)
        if dry is not None:
            dry[k] += 1
            return
        self._ak_asked[k] += 1
        if self._ak_rec is not None:
            self._ak_rec[k] += 1

    def _walk_memo_entry(self, lib: Any, key: str, slot: str, mine: str, partner: str,
                         others: tuple, targets: tuple, comp: Any, atoms: dict, sig: Any,
                         tallied: bool, pno: bool, views: dict, causes: dict,
                         refused: Counter) -> None:
        """(A): one lit entry of _index_reach. Its key is everything the entry's walk reads; a hit
        merges the kept record as the walk would (_walk_apply), a miss walks it fresh
        (_walk_one) and keeps it. Under the check arm a hit is also walked fresh and compared."""
        ek = (id(lib), self._atoms_token, sig, key, slot, mine, partner, tuple(others),
              tuple(targets))
        rec = self._walk_memo.get(ek)
        if rec is not None and not _WALK_MEMO_CHECK:
            _book_add(self.gamma.book, "walk_memo_hit")
            self._walk_apply(rec, key, sig, views, causes, refused, replay=True)
            return
        dry = None
        if rec is not None:                    # the check: what the replay would have asked
            dry = Counter()
            for call in rec["calls"]:
                self._ak_note(*call, sig, dry=dry)
            self._ak_rec = Counter()
        try:
            fresh = self._walk_one(lib, key, slot, mine, partner, others, targets, comp, atoms,
                                   sig, tallied, pno)
        finally:
            asked, self._ak_rec = self._ak_rec, None
        if rec is not None:
            agree = (self._walk_view(rec) == self._walk_view(fresh)
                     and (dry or None) == (asked or None))
            _book_add(self.gamma.book, "walk_memo_agree" if agree else "walk_memo_disagree")
            if not agree:
                self.led.record(self.cycle, self._running_step, slot, "walk_memo_check",
                                entry=key, agree=False,
                                reads="a kept entry walk differed from the fresh walk (A)")
        else:
            _book_add(self.gamma.book, "walk_memo_miss")
            if self._admit("walk", ek):
                self._walk_memo[ek] = fresh
        self._walk_apply(fresh, key, sig, views, causes, refused, replay=False)

    def _walk_one(self, lib: Any, key: str, slot: str, mine: str, partner: str, others: tuple,
                  targets: tuple, comp: Any, atoms: dict, sig: Any, tallied: bool,
                  pno: bool) -> dict:
        """(A): _index_reach's body for ONE lit entry, into the entry's own record: its views and
        causes in walk order with their first entry and their counts, its refusals, its _spent
        charges, its landings (role, the two kinds' names, target), and its held-role asks."""
        views: dict = {}
        causes: dict = {}
        rd: Counter = Counter()
        tally = rd if tallied else None
        spent = 0
        landed: list = []
        calls: list = []
        held = sig is not None

        def ask(role_: str, o_: str, x_: str, t_: str) -> None:
            if (held and role_ in _HELD_ROLES and o_ != x_
                    and all(_PLAIN.fullmatch(n) and "PH" not in n for n in (o_, x_))):
                calls.append((key, role_, o_, x_, t_))
        for role in reach.SINGLE:
            if pno:
                rd[PAIR_NOT_OBJECT] += 1
                continue
            _landed: set = set()
            spent += 1
            for t_ in (targets or (slot,)):
                ask(role, mine, partner, t_)
                for cand, c, _ in self._compiled(lib, key, role, mine, partner, comp, atoms,
                                                 sig, slot=t_, tally=tally):
                    spent += 1
                    if c is None:
                        rd[compile_term.QUANTIFIED] += 1
                        continue
                    if isinstance(c, compile_term.Refusal):
                        rd[c.reason] += 1
                    elif c.slot == t_:
                        vk = (t_, c.term.name) if targets else c.term.name
                        hit = views.get(vk)
                        if hit is None:
                            views[vk] = [c, {"library": key, "role": role,
                                             "template": cand.get("template"), "entries": 1,
                                             **({"via": c.via} if c.via else {})}, 1]
                        else:
                            hit[2] += 1
                        _landed.add(t_)
            for t_ in sorted(_landed):
                landed.append((role, mine, partner, t_))
        for o_ in others:
            if _PAIR_NOT_OBJECT and ("~" in o_ or "~" in mine):
                rd[PAIR_NOT_OBJECT] += 1
                continue
            _landed = set()
            spent += 1
            for t_ in (targets or (slot,)):
                ask("CAUSE", o_, mine, t_)
                for cand, if_c, then_c in self._compiled(lib, key, "CAUSE", o_, mine, comp,
                                                         atoms, sig, slot=t_, tally=tally):
                    spent += 1
                    if isinstance(if_c, compile_term.Refusal):
                        rd["if: " + if_c.reason] += 1
                        continue
                    if isinstance(then_c, compile_term.Refusal):
                        rd["then: " + then_c.reason] += 1
                        continue
                    if then_c.slot != t_:
                        continue
                    pk = ((if_c.term.name, if_c.slot, then_c.term.name, t_) if targets
                          else (if_c.term.name, if_c.slot, then_c.term.name))
                    hit = causes.get(pk)
                    if hit is None:
                        _via = if_c.via or then_c.via
                        causes[pk] = [if_c, then_c, {"library": key, "role": "CAUSE",
                                                     "bond": cand.get("bond"), "entries": 1,
                                                     **({"via": _via} if _via else {})}, 1]
                    else:
                        hit[3] += 1
                    _landed.add(t_)
            for t_ in sorted(_landed):
                landed.append(("CAUSE", o_, mine, t_))
        return {"views": views, "causes": causes, "refused": rd, "spent": spent,
                "landed": landed, "calls": calls}

    def _walk_apply(self, rec: dict, key: str, sig: Any, views: dict, causes: dict,
                    refused: Counter, replay: bool) -> None:
        """(A): merge one entry's record into the walk's views, causes and refusals exactly as
        the walk would have; charge its _spent; land its kinds under THIS step's dk; on a hit,
        replay its asked tally. One merge for a fresh entry and a kept one."""
        for vk, (c, meta, n) in rec["views"].items():
            hit = views.get(vk)
            if hit is None:
                m = dict(meta)
                m["entries"] = n
                views[vk] = (c, m)
            else:
                hit[1]["entries"] += n
        for pk, (if_c, then_c, meta, n) in rec["causes"].items():
            hit = causes.get(pk)
            if hit is None:
                m = dict(meta)
                m["entries"] = n
                causes[pk] = (if_c, then_c, m)
            else:
                hit[2]["entries"] += n
        refused.update(rec["refused"])
        self._spent += rec["spent"]
        if _7L_KIND:
            for role, a, b, t_ in rec["landed"]:
                self._land_kind((key, role, self._kind(a), self._kind(b)),
                                dk=self._dk_of.get(t_), slot=t_)
        if replay:
            for call in rec["calls"]:
                self._ak_note(*call, sig)

    @staticmethod
    def _walk_view(rec: dict) -> tuple:
        """(A)'s check: a record as comparable values (terms by name and slot)."""
        def term(c: Any) -> Any:
            return None if c is None else (c.term.name, c.slot, c.via)
        return (tuple((vk, term(c), tuple(sorted(m.items(), key=str)), n)
                      for vk, (c, m, n) in rec["views"].items()),
                tuple((pk, term(a), term(b), tuple(sorted(m.items(), key=str)), n)
                      for pk, (a, b, m, n) in rec["causes"].items()),
                tuple(sorted(rec["refused"].items(), key=str)), rec["spent"],
                tuple(rec["landed"]), tuple(rec["calls"]))

    def _index_reach(self, lib: Any, lit: list, slot: str, mine: str, others: tuple,''')
# 9. books
rep('''    "fit_tier0_disagree",               # S2a check run: the skipped fit, run, did NOT agree
''', '''    "fit_tier0_disagree",               # S2a check run: the skipped fit, run, did NOT agree
    "walk_memo_hit",                    # (A): a lit entry's walk merged from its record
    "walk_memo_miss",                   # (A): a lit entry walked fresh and kept
    "walk_memo_agree",                  # (A) check run: the kept walk matched the fresh one
    "walk_memo_disagree",               # (A) check run: the kept walk did NOT match
''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
