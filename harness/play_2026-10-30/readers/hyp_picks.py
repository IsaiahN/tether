"""4's fixture read (no tree change): goal_hypotheses picks over 24 steps of gridworld default 0 and the
fake, with each pick's source and the template behind it. argv: tree, world."""
import sys

sys.dont_write_bytecode = True
tree, which = sys.argv[1], sys.argv[2]
sys.path[:0] = [tree, tree + "/tests"]
import tether  # noqa: E402

tether._AGENT_SEED = False
if which == "fake":
    import arc_holdout  # noqa: E402
    from test_entry import FakeWrapper  # noqa: E402
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
else:
    import gamma  # noqa: E402
    import gridworld  # noqa: E402
    import ledger  # noqa: E402
    import world  # noqa: E402
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
picks = []
for _ in range(24):
    n0 = len(ag.led.rows())
    ag.step()
    for r in ag.led.rows()[n0:]:
        if r["event"] == "goal_hypotheses" and r["detail"].get("pick"):
            t = r["detail"]["pick"]
            picks.append((r["cycle"], t, r["detail"].get("source"), ag._inv_tpl.get(t),
                          r["detail"].get("open"), r["detail"].get("candidates")))
rows = [r for r in ag.led.rows() if r["event"] == "goal_hypotheses"]
print(which, "goal_hypotheses rows", len(rows), "with a pick", len(picks), "shelf", len(ag._goal_shelf))
for p in picks[:8]:
    print("  ", p)
