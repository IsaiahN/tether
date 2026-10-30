"""1d smoke on B2's fixture (gridworld default seed 0 size 4, budget 40, echoes off, seed pinned):
per step the owed queue, releases by reason, supersedes, derived asks run, and the mint_rank rows.
argv: steps, on (1|0)."""
import collections
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, "c:/Users/Admin/Documents/GitHub/tether")
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

tether._AGENT_SEED = False
tether._OWED_REJUDGE = sys.argv[2] == "1"
env = world.bind(gridworld.family("default", 0, 4))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(budget=40), led)
ag._ds_echo = lambda _d: []
for step in range(int(sys.argv[1])):
    n0 = len(led.rows())
    ag.step()
    new = led.rows()[n0:]
    rel = collections.Counter(r["detail"]["why"] for r in new if r["event"] == "owed_released")
    sup = sum(1 for r in new if r["event"] == "owed_superseded")
    run = sum(r["detail"]["derived_run"] for r in new if r["event"] == "step_derived")
    dfr = sum(r["detail"]["derived_deferred"] for r in new if r["event"] == "step_derived")
    rk = [r["detail"] for r in new if r["event"] == "mint_rank"]
    print(f"step {step + 1}: owed {len(ag._dw_owed)} released {dict(rel)} superseded {sup} "
          f"derived_run {run} deferred {dfr} mint_rank {[(d['order'], d['rank']) for d in rk]}")
ag.end_run("cap")
rel = collections.Counter(r["detail"]["why"] for r in led.rows() if r["event"] == "owed_released")
print("ON" if tether._OWED_REJUDGE else "OFF", "total released", dict(rel), "rows", len(led.rows()))
for c in (2, 3):
    asked = [(r["slot"], "owed" if "owed_since" in r["detail"] else "fresh") for r in led.rows()
             if r["cycle"] == c and r["event"] == "derived_asked"]
    parks = {r["slot"]: r["detail"].get("budget_exhausted") for r in led.rows()
             if r["cycle"] == c and r["event"] == "park"}
    print(f"cycle {c}: {len(asked)} derived asks run: owed {sum(1 for _s, k in asked if k == 'owed')}"
          f", fresh {sum(1 for _s, k in asked if k == 'fresh')}; parked exhausted "
          f"{[s for s, k in asked if parks.get(s)]}; first five {asked[:5]}")
