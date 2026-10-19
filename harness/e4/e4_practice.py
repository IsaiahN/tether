"""E4 (a): one practice world for a wall time, built as conform/panel.py builds the member; the seed drawn at
birth (not pinned). Rows reach the ledger as they are recorded. argv: repo member ledger cap_s"""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
repo, name, led_path, cap_s = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, repo)
sys.path.insert(0, os.path.join(repo, "conform"))
os.chdir(repo)
os.makedirs(os.path.dirname(led_path), exist_ok=True)
t0 = time.time()
if name == "fake":
    import test_entry
    import tether_agent
    rep = tether_agent.run(test_entry.FakeWrapper(), "fake", 10 ** 6, led_path=led_path,
                           deadline=t0 + cap_s)
    out = {"world": name, "wall_s": round(time.time() - t0, 1), "report": str(rep)[:400]}
else:
    import gamma
    import ledger
    import panel
    import tether
    import world
    g, seed = panel._gridworld(name)
    env = world.bind(g)
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"dt_default_{seed}"), tether.Config(),
                      ledger.Ledger(led_path))
    steps = 0
    while time.time() - t0 < cap_s and not getattr(env, "terminal", lambda: None)():
        ag.step()
        steps += 1
    ag.end_run("cap")
    ag.led.close()
    out = {"world": name, "wall_s": round(time.time() - t0, 1), "steps": steps, "level": ag.level,
           "terminal": getattr(env, "terminal", lambda: None)()}
with open(led_path + ".result.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, default=str)
print(json.dumps(out, default=str), flush=True)
