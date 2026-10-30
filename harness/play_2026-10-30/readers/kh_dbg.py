import sys
sys.path.insert(0, "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv")
sys.dont_write_bytecode = True
import test_kind_hoist as t
on, off = t._run("1"), t._run("0")
for n in ("_kdk_last", "_kind_last"):
    a, b = on["stores"][n], off["stores"][n]
    print(n, len(a), len(b))
    da = sorted(set(a) - set(b)); db = sorted(set(b) - set(a))
    print(" ON only", len(da), da[:3]); print(" OFF only", len(db), db[:3])
