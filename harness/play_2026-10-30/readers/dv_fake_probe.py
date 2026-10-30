"""1a: what the fake ARC game offers K1: per searching mint, the decoder size and the slot's peers,
and the space_closed causes. argv: steps."""
import collections
import json
import sys

sys.dont_write_bytecode = True
sys.path[:0] = ["c:/Users/Admin/Documents/GitHub/tether", "c:/Users/Admin/Documents/GitHub/tether/tests"]
import arc_holdout  # noqa: E402
import tether  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402

tether._AGENT_SEED = False
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
seen = []
orig = tether.Agent._divide_open


def spy(self, slot, tri, kind, base, units):
    seen.append((self.cycle, slot, tri[5], len(tri[7]), self._space.get(slot) is not None))
    return orig(self, slot, tri, kind, base, units)


tether.Agent._divide_open = spy
n = int(sys.argv[1])
for _ in range(n):
    env.observe()
    ag.step()
    if env.terminal():
        break
ag.end_run("cap")
rows = led.rows()
print("divide rows", sum(1 for r in rows if r["event"] == "divide"))
print("closes", collections.Counter(r["detail"]["cause"] for r in rows if r["event"] == "space_closed"))
print("decoder sizes seen", sorted({s[2] for s in seen}), "peers lens", sorted({s[3] for s in seen}))
carried = [r["detail"] for r in rows if r["event"] == "divide" and r["detail"]["carried"]]
print("mints with carried > 0:", len(carried), json.dumps(carried[:3])[:600])
