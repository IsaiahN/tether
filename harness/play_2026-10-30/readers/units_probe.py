import sys
sys.dont_write_bytecode = True
sys.path[:0] = ["C:/TETHER_RUNS/S6_2026-10-19/wt_ivv", "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/conform"]
import gamma, ledger, panel, tether, world
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="u"), tether.Config(), ledger.Ledger())
for i in range(25):
    ag.step()
    us = ag.gamma.units_held()
    lib = ag.gamma.library
    by = {t.atoms: n for n, t in lib.items()}
    comp = [u for u in us if len(u.atoms) >= 2]
    match = [u for u in comp if u.atoms in by]
    print(i, "units", len(us), "composite", len(comp), "composite matching a library term", len(match), "lib", len(lib), "_not", len(ag._not))
