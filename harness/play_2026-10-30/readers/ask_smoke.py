"""1b smoke: N steps on a world, then the ask rows, the exits taken, and the row count by event.
argv: world (fake|grid), steps."""
import collections
import json
import sys
import time

sys.dont_write_bytecode = True
sys.path[:0] = ["c:/Users/Admin/Documents/GitHub/tether", "c:/Users/Admin/Documents/GitHub/tether/tests"]
import tether  # noqa: E402

tether._AGENT_SEED = False
which, n = sys.argv[1], int(sys.argv[2])
t0 = time.time()
if which == "fake":
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
else:
    import gamma
    import gridworld
    import ledger
    import world
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), led)
for _ in range(n):
    if which == "fake":
        env.observe()
    ag.step()
    if which == "fake" and env.terminal():
        break
rows = led.rows()
ev = collections.Counter(r["event"] for r in rows)
print("ASK", tether._ASK, which, n, "wall", round(time.time() - t0, 1), "rows", len(rows),
      "ask rows", ev["ask"], "choice rows", ev["choice"])
asks = [r["detail"] for r in rows if r["event"] == "ask"]
if asks:
    import statistics
    sv = [d["survivors"] for d in asks]
    taken = [d for d in asks if d["chosen"] is not None]
    share = [d["largest"] / d["survivors"] for d in taken]
    print(f"asks {len(asks)}; gaps_eligible max {max(d['gaps_eligible'] for d in asks)}; survivors "
          f"median {statistics.median(sv)} max {max(sv)}; vectors median "
          f"{statistics.median(d['vectors'] for d in asks)} max {max(d['vectors'] for d in asks)}; "
          f"abstained {len(asks) - len(taken)}; largest-block share over taken: "
          f"{[round(x, 3) for x in share][:12]}; evaluations max "
          f"{max(d['evaluations'] for d in asks)}; wall_s sum {round(sum(d['wall_s'] for d in asks), 3)}"
          f" max {max(d['wall_s'] for d in asks)}")
for r in rows:
    if r["event"] == "ask":
        d = {k: v for k, v in r["detail"].items() if k != "reads"}
        print(r["cycle"], json.dumps(d)[:240])
