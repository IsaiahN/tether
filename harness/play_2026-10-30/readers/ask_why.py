"""1b: why no ask -- per step, at _distinguish's call: open spaces, the key match, cells covering the
current residual count, survivors; and how often _exit_choice / _distinguish were reached.
argv: world (fake|grid), steps."""
import collections
import sys

sys.dont_write_bytecode = True
sys.path[:0] = ["c:/Users/Admin/Documents/GitHub/tether", "c:/Users/Admin/Documents/GitHub/tether/tests"]
import tether  # noqa: E402
from tether import IDN  # noqa: E402

tether._AGENT_SEED = False
which, n = sys.argv[1], int(sys.argv[2])
calls = collections.Counter()
d0, x0 = tether.Agent._distinguish, tether.Agent._exit_choice


def dist(self, before):
    calls["distinguish"] += 1
    for s in sorted(self._space):
        seen = self._tally.get(s)
        held = self.gamma.library[self.bound.get(s, IDN)]
        key_ok = seen is not None and seen[0] == self._divide_key(s, held)
        robs = len(self._residual_obs(s, held, self.history(s)))
        cells = [c for d in (seen[1], seen[2]) for c in d.values()] if seen else []
        full = sum(1 for c in cells if c[0] == robs)
        noref = sum(1 for c in cells if c[0] == robs and c[2] is None)
        print(f"  c{self.cycle} {s}: key_ok {key_ok} robs {robs} cells {len(cells)} "
              f"rows-max {max((c[0] for c in cells), default=None)} full {full} survivors {noref} "
              f"S1 {len(self._survivors(s))}")
    return d0(self, before)


def xc(self, before):
    calls["exit_choice"] += 1
    return x0(self, before)


tether.Agent._distinguish, tether.Agent._exit_choice = dist, xc
if which == "fake":
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
else:
    import gamma
    import gridworld
    import ledger
    import world
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), led)
for _ in range(n):
    if which == "fake":
        env.observe()
    ag.step()
    if which == "fake" and env.terminal():
        break
by = collections.Counter(r["detail"].get("by") for r in led.rows() if r["event"] == "act")
print("calls", dict(calls), "exits", dict(by))
