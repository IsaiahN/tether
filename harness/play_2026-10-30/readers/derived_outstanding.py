"""1d premise check: for gridworld's declared-derived slots (B2's fixture: family default seed 0 size 4,
budget 40, echoes off), per step: owed derived asks, and outstanding / _understanding for every
derived slot and for the ACCEPT loop's slots. argv: steps."""
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, "c:/Users/Admin/Documents/GitHub/tether")
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

tether._AGENT_SEED = False
env = world.bind(gridworld.family("default", 0, 4))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(budget=40), ledger.Ledger())
ag._ds_echo = lambda _d: []
for step in range(int(sys.argv[1])):
    ag.step()
    der = sorted(env.derived()) if hasattr(env, "derived") else []
    d_out = {d: (ag.outstanding(d), round(ag._understanding(d), 3)) for d in der}
    nz = {d: v for d, v in d_out.items() if v[0] > 0}
    plain = [s for s in ag.slots if s not in der]
    p_out = sorted((round(ag._understanding(s), 3), s) for s in plain if ag.outstanding(s) > 0)[-3:]
    src = env.derived()
    owed = sorted(ag._dw_owed)
    live = [d for d in owed if any(ag.outstanding(s) > 0 for s in src.get(d, ()))]
    rk = sorted({round(max((ag._understanding(s) for s in src.get(d, ())), default=0), 3)
                 for d in owed})
    print(f"step {step + 1}: derived {len(der)}, owed {len(ag._dw_owed)}, derived with outstanding>0 "
          f"{len(nz)}; owed with a source outstanding>0 {len(live)}; owed ranks by best source "
          f"{rk[:6]}; top plain by _understanding {p_out}")
