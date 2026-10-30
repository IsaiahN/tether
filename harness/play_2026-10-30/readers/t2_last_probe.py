"""Does _tiers fail when T2 has a candidate AND T1d has a landed-only entry (CONSOLIDATE on)? test_k1's OLD setup
plus one landed-only entry. In-process, the fake world, no lineage."""
import sys
from collections import Counter
sys.dont_write_bytecode = True
sys.path[:0] = ["C:/TETHER_RUNS/S6_2026-10-19/wt_ivv"]
import arc_holdout, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
print("CONSOLIDATE", tether._CONSOLIDATE, "DELTA_KIND", tether._DELTA_KIND, "kind_store", ag._kind_store is not None)
lib = tether._library()
mine = sorted(set(env.slot_owner().values()))[0]
ko = ag._kind(mine)
k_t3, k_old, k_land = [k for k in lib.seed if not lib.seed[k].get("ingredients")][:3]
ag._kind_known = {(k_old, "STATE", ko, ko)}                    # T2: a carried landing with no dk
ag._kind_landed_dk = Counter({(("MOTION", "-", 1), k_land, ko): 1})   # T1d: landed, never offered
try:
    out, n = ag._tiers(lib, [(k_t3, 1.0)], ("MOTION", "-", 1), mine, {}, {})
    print("no failure:", {t: c for t, c in n.items() if c})
except Exception as e:
    print("FAILED:", type(e).__name__, e)
