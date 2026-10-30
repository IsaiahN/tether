import sys

P = sys.argv[1]
src = open(P, encoding="utf-8", newline="").read()
L = src.split("\r\n")


def at(text, start=0):
    hits = [i for i, x in enumerate(L) if x == text and i >= start]
    assert len(hits) >= 1, text
    return hits[0]


# 1. the flag
i = at("_TYPED_BIND = armflag.arm(\"TETHER_TYPED_BIND\")")
assert L[i - 1].startswith("# F127's arm B.")
L[i - 1:i + 1] = [
    "# L3, ON AS AN ORDERING (Isaiah 2026-10-26 08:24; the reviewer 08:30): a binding whose head",
    "# does not accept the slot type is walked LAST, in its own late round -- never refused.",
    "_TYPED_BIND = armflag.arm(\"TETHER_TYPED_BIND\", default=True)",
]

# 2. _judge: the refusal becomes a deferral
j = at("        def _judge(cand, price, n):")
L[j] = "        def _judge(cand, price, n, late=False):"
k = at("            if _TYPED_BIND and not _head_accepts(cand, _st):", j)
assert L[k + 1] == "                return False, None, None, _since(_n0)"
c0 = at("            # F127 EXPERIMENT, SEAT-SIDE SWITCH, DEFAULT OFF. The line above filters the OUT", j)
L[c0:k + 2] = [
    "            # F127: the line above filters the OUT type and nothing filtered the IN type, so",
    "            # `none` bound an EXTENT slot and read `int(not width)`. L3: such a head is DEFERRED",
    "            # (None) to the late round, never refused; `late` is that round's own judging.",
    "            if _TYPED_BIND and not late and not _head_accepts(cand, _st):",
    "                return None, None, None, _since(_n0)",
]

# 3. the walk: candidates come from _pairs(), which ends with the late round
a = at("        for n in retrieval.retrieve(self.gamma.library, gap, track=self.gamma.track_of,")
s = at("                    cand = _lt          # the name's own object, as _rebindings yields it first", a)
assert L[s - 1] == "                if _i == 0:" and L[s - 2] == "                cap.head()"
assert L[s - 3] == "            for _i, cand in enumerate(_cands):"
e = at("                return self._take_pull(n, cand, slot)", s)
assert L[e + 1] == "        if _paying:"
head = L[a:s - 3]
body = L[s + 1:e]
gen = [
    "        # L3's late round: what `_judge` deferred is walked after every typed candidate, once",
    "        # per candidate, if the governor says think; `typed_late` records walked and closed.",
    "        _late: dict = {}",
    "        _late_keys: set = set()",
    "        _lw: dict = {}",
    "",
    "        def _late_row(took):",
    "            if _lw:",
    "                self.led.record(self.cycle, \"ROUTE\", slot, \"typed_late\",",
    "                                deferred=_lw[\"deferred\"], walked=_lw[\"walked\"],",
    "                                gate=_lw[\"gate\"], closed=int(took in _late_keys),",
    "                                reads=\"heads not accepting the slot type, walked last\")",
    "                _lw.clear()",
    "",
    "        def _pairs():",
] + ["    " + x if x else x for x in head] + [
    "                for _i, cand in enumerate(_cands):",
    "                    cap.head()",
    "                    if _i == 0:",
    "                        cand = _lt      # the name's own object, as _rebindings yields it first",
    "                    yield n, cand, False",
    "            if not _late:",
    "                return",
    "            _walk, _why = self._think_or_act(slot, closer=bool(_paying))",
    "            _lw.update(deferred=len(_late), gate=_why, walked=0)",
    "            if not _walk:",
    "                _late_row(None)",
    "                return",
    "            for cand, n in _late.items():",
    "                cap.head()",
    "                _lw[\"walked\"] += 1",
    "                _late_keys.add((n, cand.name))",
    "                yield n, cand, True",
    "",
    "        for n, cand, _is_late in _pairs():",
]
nb = []
for x in body:
    assert not x or x.startswith("    "), x
    nb.append(x[4:] if x else x)
# judging: the late round judges directly; a deferral is queued
i0 = nb.index("            if _FIT_DEDUP and _BARGAIN_FIT:")
nb[i0] = "            if _is_late:"
nb[i0:i0] = []
nb.insert(i0 + 1, "                _ok, _left, _cost, _ = _judge(cand, _BARGAIN_FIT, n, late=True)")
nb.insert(i0 + 2, "            elif _FIT_DEDUP and _BARGAIN_FIT:")
i1 = nb.index("            if not _ok:")
nb[i1:i1] = ["            if _ok is None:",
             "                _late.setdefault(cand, n)",
             "                continue"]
tail = ["            _late_row((n, cand.name))",
        "            return self._take_pull(n, cand, slot)"]
L[a:e + 1] = gen + nb + tail

# 4. the other two exits record the late row
p = at("        if _paying:")
q = at("            out = self._take_pull(n, cand, slot, carry=carry)", p)
L[q:q] = ["            _late_row((n, cand.name))"]
r = at("        self.led.record(self.cycle, \"ROUTE\", slot, \"reach_failed\",", q)
L[r:r] = ["        _late_row(None)"]

open(P, "w", encoding="utf-8", newline="").write("\r\n".join(L))
print("ok")
