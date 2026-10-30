"""Smoke for 1a DIVIDE on gridworld: N steps, then the divide and space_closed rows. argv: steps, seed."""
import collections
import json
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, "c:/Users/Admin/Documents/GitHub/tether")
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

tether._AGENT_SEED = False
n, seed = int(sys.argv[1]), int(sys.argv[2])
env = world.bind(gridworld.family("default", seed))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"), tether.Config(), led)
t0 = time.time()
for _ in range(n):
    ag.step()
ag.end_run("cap")
rows = led.rows()
ev = collections.Counter(r["event"] for r in rows if r["event"] in ("divide", "space_closed", "park"))
print("arm", tether._DIVIDE, "steps", n, "wall", round(time.time() - t0, 1), "events", dict(ev))
for r in rows:
    if r["event"] in ("divide", "space_closed"):
        d = {k: v for k, v in r["detail"].items() if k != "reads"}
        print(r["cycle"], r["slot"], r["event"], json.dumps(d, default=str)[:300])
