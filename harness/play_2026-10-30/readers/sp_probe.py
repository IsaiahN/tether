import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "C:/Users/Admin/Documents/GitHub/tether")
import gamma, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
for _ in range(30):
    ag.step()
rows = [r for r in ag.led.rows() if r["event"] == "settle"]
print("settle rows", len(rows))
for r in rows[:4]:
    print({k: r["detail"].get(k) for k in ("term", "predicted_code", "actual_code", "from_value", "from_code", "risky")})
