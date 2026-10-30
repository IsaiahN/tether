import sys
sys.path.insert(0, "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv")
sys.dont_write_bytecode = True
import tether
from test_goal_pair import ROWS
from test_gt_which import _linked
ag = _linked()
print("A1_TIES", tether._A1_TIES)
print("wants", {k: v for k, v in ag.wants.items() if k.startswith(("o0.", "o3.", "o4."))})
print("scope", dict(ag._want_scope))
print("goal_text", dict(ag._goal_text))
base = dict(next(st for st, hit in ROWS if not hit), **{"o3.col": 3})
for c in (0, 1, 2):
    why = {}
    print("o0.col", c, ag.goal_residual("o0.col", dict(base, **{"o0.col": c}), why=why), why)
