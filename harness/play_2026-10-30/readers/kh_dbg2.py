import sys
sys.path.insert(0, "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv")
sys.dont_write_bytecode = True
import test_kind_hoist as t
a, b = t._run("1"), t._run("1")
print("ON vs ON (hash seed unpinned):", {n: a["stores"][n] == b["stores"][n] for n in a["stores"]})
