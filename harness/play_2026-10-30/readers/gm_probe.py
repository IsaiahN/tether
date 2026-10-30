import sys
sys.path[:0] = ["C:/TETHER_RUNS/S6_2026-10-19/wt_ivv", "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/conform"]
sys.dont_write_bytecode = True
import gamma, ledger, panel, tether, world
from gamma import Term
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="gm"), tether.Config(), ledger.Ledger())
for _ in range(3):
    ag.step()
st = dict(ag.trace[-1][0])
A = {a.name: a for a in ag.gamma.atoms}
print("arm", tether._GROUP_MEMBER, "peers of o0.row", ag._peer_cache.get("o0.row") if ag._peer_cache else None)
for name in ("aligned", "all_same", "none_same"):
    if name not in A:
        print(name, "absent"); continue
    chain = (A[name], A["holds"], A["all"]) if A[name].out_type == "BOOL" else (A[name], A["all"])
    t = Term(chain)
    ag.wants["o0.row"], ag._want_terms["o0.row"] = t.name, t
    ag._want_scope.pop("o0.row", None)
    out = []
    for rows in ([1, 1, 1, 2, 3, 4], [1, 1, 1, 2, 3, 1], [5, 5, 5, 5, 5, 5]):
        s = dict(st, **{f"o{i}.row": v for i, v in enumerate(rows)})
        c = {}
        out.append((rows, ag.goal_residual("o0.row", s, c), c))
    print(name, t.name, [(r[0][-1], r[1], r[2]) for r in out])
