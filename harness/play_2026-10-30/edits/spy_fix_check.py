"""r440 item 3: the spy's realise, checked in its own process. argv: tree mode [spy_file out_dir]
  mode none   no spy: the call sequence on the agent's own Interface.realise, results printed as JSON
  mode spy    the spy at spy_file installed (before the agent is built, as the box does), the same sequence
The sequence (test_ask.py:85's call shape, a gridworld agent after 2 steps): three split cases, one call without split,
one asker="goal" call (the spy's recording branch). A TypeError is printed as the result, not raised."""
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
tree, mode = sys.argv[1], sys.argv[2]
sys.path = [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
sys.path.insert(0, tree)
import interface as IFace  # noqa: E402
import tether  # noqa: E402

if mode == "spy":
    s = importlib.util.spec_from_file_location("kind_spy_under_test", sys.argv[3])
    ks = importlib.util.module_from_spec(s)
    s.loader.exec_module(ks)
    ks.install(sys.argv[4])
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import world  # noqa: E402

tether._AGENT_SEED = False
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
for _ in range(2):
    ag.step()
acts = tuple(ag.actions)
a, b, c = acts[:3]
before, ctx = env.observe(), IFace.Interface.context(env)
want = IFace.Intent(IFace.DISTINGUISH, subject="o0.row")


def res(r):
    return None if r is None else {"action": r.action, "coord": list(r.coord) if r.coord else None, "why": r.why}


out = []
for kw in ({"split": {a: [3], b: [2, 1], c: [1, 1, 1]}}, {"split": {a: [2, 2], b: [2, 1, 1], c: [4]}},
           {"split": {a: [4], b: [4], c: [4]}}, {}, {"asker": "goal"}):
    try:
        out.append(res(ag.iface.realise(want, acts, ctx, before, env, **kw)))
    except TypeError as e:
        out.append({"TypeError": str(e)})
for asker in (None, "goal"):   # a no-split call that realises an action (ELICIT, as tether.py:12531), spy branch too
    try:
        out.append(res(ag.iface.realise(IFace.Intent(IFace.ELICIT), acts, ctx, before, env, asker=asker)))
    except TypeError as e:
        out.append({"TypeError": str(e)})
print(json.dumps({"mode": mode, "spy": sys.argv[3] if mode == "spy" else None, "results": out}))
