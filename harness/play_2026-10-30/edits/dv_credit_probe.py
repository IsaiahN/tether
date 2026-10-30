"""CREDIT probe: per searching mint, (cycle, slot, mint_k, chains_met_before, chains_new, credited)
beside the park row's seen / budget_exhausted. argv: world (fake|grid), steps."""
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
park = {(r["cycle"], r["slot"]): r["detail"] for r in rows if r["event"] == "park"}
tot = {"met": 0, "new": 0, "cred": 0, "capped_met_new0": 0, "capped_met": 0}
for r in rows:
    if r["event"] != "divide":
        continue
    d, p = r["detail"], park.get((r["cycle"], r["slot"]), {})
    capped = bool(p.get("budget_exhausted"))
    tot["met"] += d["chains_met_before"]
    tot["new"] += d["chains_new"]
    tot["cred"] += d.get("credited", 0)
    if capped and d["chains_met_before"] > 0:
        tot["capped_met"] += 1
        tot["capped_met_new0"] += d["chains_new"] == 0
    print(r["cycle"], r["slot"], d["mint_k"], "met", d["chains_met_before"], "new", d["chains_new"],
          "cred", d.get("credited"), "seen", p.get("candidates_seen"), "capped", capped)
print("CREDIT", tether._DIVIDE_CREDIT, which, n, "wall", round(time.time() - t0, 1), tot)
