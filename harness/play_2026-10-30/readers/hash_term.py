import sys
sys.dont_write_bytecode = True
sys.path[:0] = ["C:/TETHER_RUNS/S6_2026-10-19/wt_ivv", "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/conform"]
import gamma, ledger, panel, tether, world
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="h"), tether.Config(), ledger.Ledger())
for _ in range(3):
    ag.step()
lib = ag.gamma.library
ok = bad = 0
for n, t in list(lib.items()):
    try:
        hash((ag.slots[0], t)); ok += 1
    except TypeError as e:
        bad += 1; print("unhashable", n, e); break
print("hashable", ok, "unhashable", bad, "library", len(lib))
