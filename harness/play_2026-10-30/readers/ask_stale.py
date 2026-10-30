"""r346 3: at every 1b ask, was every valid cell of the asked space current (its stamp == len(history(slot)))?
Asks total / on a current record / on a row-stale record, per ask the stamps against the history length.
argv: world (fake|grid), steps."""
import collections
import sys

sys.dont_write_bytecode = True
sys.path[:0] = ["c:/Users/Admin/Documents/GitHub/tether", "c:/Users/Admin/Documents/GitHub/tether/tests"]
import tether  # noqa: E402

tether._AGENT_SEED = False
which, n = sys.argv[1], int(sys.argv[2])
seen = []
a0 = tether.Agent._ask


def spy(self, before):
    n0 = len(self.led.rows())
    out = a0(self, before)
    asks = [r for r in self.led.rows()[n0:] if r["event"] == "ask"]
    if asks:
        slot = asks[-1]["slot"]
        got = self._space_bounds(slot)
        stamps = collections.Counter((got[2] if got and len(got) > 2 else {}).values())
        h = len(self.history(slot))
        seen.append((self.cycle, slot, h, dict(stamps), asks[-1]["detail"]["survivors"]))
    return out


tether.Agent._ask = spy
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
cur = sum(1 for _c, _s, h, st, _n in seen if st and set(st) == {h})
stale = sum(1 for _c, _s, h, st, _n in seen if st and set(st) != {h})
none = sum(1 for _c, _s, _h, st, _n in seen if not st)
print(f"{which} {n}: asks {len(seen)}; on a current record {cur}; row-stale {stale}; no stamps {none}")
for c, s, h, st, sv in seen:
    print(f"  c{c} {s}: history {h}; cell stamps {st}; survivors {sv}")
