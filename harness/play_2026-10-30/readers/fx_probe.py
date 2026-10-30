import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "C:/Users/Admin/Documents/GitHub/tether")
import numpy as np
import arc_percept as P

def old():
    g = np.zeros((64, 64), dtype=int)
    g[30:34, 30:34] = 3          # the fake's mover
    g[5:9, 5:9] = 7              # the fake's static block
    g[40:43, 10:15] = 2
    g[50:52, 50:56] = 4
    return g

def kind_a():                    # the static recoloured in place; the rest gone; new pieces elsewhere
    g = np.zeros((64, 64), dtype=int)
    g[5:9, 5:9] = 1
    g[15:20, 40:45] = 5
    g[20:22, 20:30] = 6
    g[56:60, 2:5] = 8
    return g

def kind_b():                    # every piece moved far, colour and shape kept
    g = np.zeros((64, 64), dtype=int)
    g[10:14, 50:54] = 3
    g[45:49, 45:49] = 7
    g[10:13, 12:17] = 2
    g[10:12, 25:31] = 4
    return g

for name, f in (("a", kind_a), ("b", kind_b)):
    o = P.Objects(); o(old()); before = dict(o.tracked); o(f())
    print(name, {k: o.call_log[-1].get(k) for k in ("found", "claimed", "median", "colour_share", "broke")}, o.matches)
    print("   carried", sorted(set(o.matches) & set(before)), "tracked now", {k: (v.get("covered") is not None) for k, v in o.tracked.items()})
