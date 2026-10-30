p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/test_k1.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"


def rep(old, new):
    global s
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    assert s.count(old) == 1, (old[:60], s.count(old))
    s = s.replace(old, new)


rep('''    keys = [k for k in lib.seed if not lib.seed[k].get("ingredients")][:3]
    k_mirror, k_t3, k_old = keys
''', '''    keys = [k for k in lib.seed if not lib.seed[k].get("ingredients")][:5]
    k_mirror, k_t3, k_old, k_lo1, k_lo2 = keys
''')
rep('''    print("OLD a carried landing with no delta kind sits in T2, after T1, before T3")
    ag._kind_known = set()
''', '''    print("OLD a carried landing with no delta kind sits in T2, after T1, before T3")
    # OLD + T1d, the seam that crashed (the reviewer 2026-10-21 03:05): T2 held AND two landed-only
    # entries, their recency opposite to their names, so T1d must order by the recency dict
    lo_a, lo_b = sorted((k_lo1, k_lo2))
    ag._kind_landed_dk[(("MOTION", "-", 1), lo_a, ko)] = 1
    ag._kind_landed_dk[(("MOTION", "-", 1), lo_b, ko)] = 1
    ag._kdk_last[(("MOTION", "-", 1), lo_a, ko)] = ("fake", 0, 0, 1)
    ag._kdk_last[(("MOTION", "-", 1), lo_b, ko)] = ("fake", 0, 0, 2)
    out, n = ag._tiers(lib, [(k_t3, 1.0)], ("MOTION", "-", 1), mine, {}, {})
    order = [k for k, _w in out]
    assert n["T2"] == 1 and n["T1d"] == 2, n                                               # OLD+T1d
    if tether._CONSOLIDATE:
        assert order.index(lo_b) < order.index(lo_a), (lo_a, lo_b, order)
    print("OLD+T1d T2 and T1d both held: listed, T1d ordered by recency (the later landing first)")
    for k_ in (lo_a, lo_b):
        del ag._kind_landed_dk[(("MOTION", "-", 1), k_, ko)]
        del ag._kdk_last[(("MOTION", "-", 1), k_, ko)]
    ag._kind_known = set()
''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
