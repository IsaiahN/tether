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
    ('''_TIERS_INDEX_CHECK = armflag.arm("TETHER_TIERS_INDEX_CHECK")
''', '''_TIERS_INDEX_CHECK = armflag.arm("TETHER_TIERS_INDEX_CHECK")
# THE _tiers NAME TIE -> THE RECORDED DRAW (the reviewer 2026-10-20 23:55 (ii), 2026-10-21 03:05;
# Isaiah's 10-15 A1 rule: never a name, a text or a position): every _tiers order whose numbers tie
# fell to the entry's NAME; it falls to the recorded draw (frontier.draw_key, keyed per lookup).
# OFF: the name (03b793e)
_TIERS_DRAW = armflag.arm("TETHER_TIERS_DRAW", default=True)
'''),
    ('''def _lookup_order(names: list, comp: dict, dk: str, evidence=None, seed=None) -> list:
''', '''def _draw_ties(items, num, key: str, seed) -> list:
    """(name, value) items ordered by num(item); a run equal on num is ordered by the recorded draw
    of its names (A1: never a name). Only a tied run is hashed. Sorting by (num, draw) exactly."""
    out = sorted(items, key=lambda kv: (num(kv), kv[0]))
    i = 0
    while i < len(out):
        j, at = i + 1, num(out[i])
        while j < len(out) and num(out[j]) == at:
            j += 1
        if j - i > 1:
            out[i:j] = sorted(out[i:j], key=lambda kv: (FR.draw_key(key, kv[0], seed), kv[0]))
        i = j
    return out


def _lookup_order(names: list, comp: dict, dk: str, evidence=None, seed=None) -> list:
'''),
    ('''        def ranked(cnt: Counter) -> list:
            return sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
''', '''        # every order below ends in a tie-break: the recorded draw, keyed per lookup (OFF: the name)
        tie_key = f"{self.cycle}:{mine}:{dk}:tiers"

        def order(items, num) -> list:
            if _TIERS_DRAW:
                return _draw_ties(list(items), num, tie_key, self.draw_seed)
            return sorted(items, key=lambda kv: (num(kv), kv[0]))

        def ranked(cnt: Counter) -> list:
            return order(cnt.items(), lambda kv: (-kv[1],))
'''),
    ('''                put(f"T1{g_}", sorted(((k, float(m)) for k, m in off[g_].items()),
                                      key=lambda kv, g_=g_: (-kv[1], -land[g_][kv[0]],
                                                             -last.get(kv[0], 0), kv[0])))
''', '''                put(f"T1{g_}", order(((k, float(m)) for k, m in off[g_].items()),
                                     lambda kv, g_=g_: (-kv[1], -land[g_][kv[0]],
                                                        -last.get(kv[0], 0))))
'''),
    ('''                put("T2", sorted(n_.items(), key=lambda kv: (-kv[1], -l_[kv[0]], kv[0])))
''', '''                put("T2", order(n_.items(), lambda kv: (-kv[1], -l_[kv[0]])))
'''),
    ('''                put("T1d", sorted(landed_only.items(),
                                  key=lambda kv: (-kv[1], -last.get(kv[0], 0), kv[0])))
''', '''                put("T1d", order(landed_only.items(), lambda kv: (-kv[1], -last.get(kv[0], 0))))
'''),
    ('''            put("T5", [(k, float(m)) for k, m in sorted(
                score.items(), key=lambda kv: (molecule(kv[0]), -kv[1], kv[0]))])
''', '''            put("T5", [(k, float(m)) for k, m in order(
                score.items(), lambda kv: (molecule(kv[0]), -kv[1]))])
'''),
])
edit("conform/arms.py", [
    ('''    "TETHER_TIERS_INDEX": "(C), THE TIERS INDEX (the reviewer 2026-10-21 03:05): _tiers reads its "
''', '''    "TETHER_TIERS_DRAW": "THE _tiers NAME TIE (the reviewer 2026-10-20 23:55 (ii), 2026-10-21 03:05; "
                         "Isaiah's 10-15 A1 rule): a tie on _tiers' numbers falls to the recorded "
                         "draw (frontier.draw_key, keyed per lookup), never the entry's name, at "
                         "T1a-c, T2, T1d and T5. OFF: the name (03b793e). default ON",
    "TETHER_TIERS_INDEX": "(C), THE TIERS INDEX (the reviewer 2026-10-21 03:05): _tiers reads its "
'''),
])
print("ok")
