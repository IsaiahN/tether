import sys
sys.dont_write_bytecode = True
T = "C:/Users/Admin/Documents/GitHub/tether"
sys.path[:0] = [T, T + "/tests"]
import arc_holdout
from test_entry import FakeWrapper
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
for _ in range(16):
    ag.step()
rows = [r for r in ag.led.rows() if r["event"] == "settle"]
print("settle rows", len(rows), "risky", sum(1 for r in rows if r["detail"].get("risky")))
for r in rows[:6]:
    print({k: r["detail"].get(k) for k in ("term", "predicted_code", "actual_code", "from_value", "from_code", "risky")})
