import json, sys
sys.dont_write_bytecode = True
T = "C:/Users/Admin/Documents/GitHub/tether"
sys.path[:0] = [T, T + "/tests"]
import numpy as np
from arcengine import GameState
import arc_holdout, tether
from gamma import Term
from test_entry import FakeWrapper

def after_board():
    g = np.zeros((64, 64), dtype=int)
    g[5:9, 5:9] = 1          # the static, recoloured: not exact
    g[50:52, 50:56] = 4      # kept EXACTLY: re-found
    g[15:20, 40:45] = 5
    g[20:22, 20:30] = 6
    return g

class Two(FakeWrapper):
    def __init__(self):
        self.new = None
        super().__init__()
    def _frame(self, state):
        f = super()._frame(state)
        if self.new is None:
            g = f.frame[0].copy(); g[40:43, 10:15] = 2; g[50:52, 50:56] = 4
        else:
            g = self.new()
        f.frame = [g]
        return f

w = Two()
env, ag, led, *_ = arc_holdout.wire(w, "fake")
for _ in range(3):
    ag.step()
ag.gamma.keep_evidence = True
slots = sorted(s for s in ag.slots if "." in s and not s.startswith("@") and "~" not in s)
owners = sorted({s.split(".")[0] for s in slots})
print("owners", owners, "identity", {o: env.identity(o) for o in owners})
reads = [a for a in ag.gamma.library.values() if getattr(a, "reads_operand", False)]
print("operand-reading atoms", len(reads), [t.name for t in reads[:5]])
tr = ag.gamma.library["translate"]
names = {}
for o in owners:
    if f"{o}.row" in ag.slots and f"{o}.col" in ag.slots:
        names[o] = ag._install_reuse(Term(tr.atoms, operand=f"{o}.row"), f"{o}.col")
print("installed", names)
for o, n in names.items():
    ag.gamma.settle(n, "w", f"{o}.col")
print("evidence rows", len(ag.gamma.evidence))
w.new = after_board
w._frame(GameState.NOT_FINISHED)
assert env.arrive()
ag.step()
rows = ag.led.rows()
ir = [r for r in rows if r["event"] == "instance_retired"]
print("arm", tether._INSTANCE_RETIRE, "instance_retired rows", [r["detail"] for r in ir])
print("still live", {o: n in ag.gamma.library for o, n in names.items()}, "retired", sorted(ag.gamma.retired))
k = Term(tr.atoms).name
print("kind", k, "live", k in ag.gamma.library, "stamp", ag.gamma.stamps.get(k), "standing", ag.gamma.standing.get(k))
print("frame_break rows", [(r["cycle"], r["detail"].get("kept")) for r in rows if r["event"] == "frame_break"])
