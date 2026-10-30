import collections, json, sys, time
sys.path.insert(0, "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv")
sys.dont_write_bytecode = True
import gamma, gridworld, ledger, tether, world
sys.path.insert(0, "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/conform"); import panel; env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="gh"), tether.Config(), ledger.Ledger())
t0 = time.time()
for i in range(int(sys.argv[1])):
    ag.step()
rows = ag.led.rows()
ev = collections.Counter(r["event"] for r in rows if r["event"].startswith(("goal_hyp", "routine")))
print("arm", tether._GOAL_HYP, "secs", round(time.time() - t0, 1), dict(ev))
for r in rows:
    if r["event"] in ("goal_hypotheses", "goal_hypothesis_end"):
        d = r["detail"]
        print(r["cycle"], r["event"], r["slot"], {k: d.get(k) for k in ("pick", "why", "route", "budget", "open", "checked", "candidates", "steps", "displaced")}, str(d.get("refused"))[:200])
    if r["event"] in ("routine", "routine_refused", "routine_recheck", "routine_hold", "routine_end"):
        print(r["cycle"], r["event"], r["slot"], str(r["detail"])[:160])
