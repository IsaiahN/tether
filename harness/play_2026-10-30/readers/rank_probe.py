"""1d: at each plain mint candidate (_mint_in_step) its _understanding, and per step how many derived
asks are fresh or owed. Shows whether a zero-rank plain candidate ever meets a derived ask in a step.
argv: world (fake|grid), steps."""
import collections
import sys

sys.dont_write_bytecode = True
sys.path[:0] = ["c:/Users/Admin/Documents/GitHub/tether", "c:/Users/Admin/Documents/GitHub/tether/tests"]
import tether  # noqa: E402

tether._AGENT_SEED = False
which, n = sys.argv[1], int(sys.argv[2])
cand = collections.defaultdict(list)
m0 = tether.Agent._mint_in_step


def spy(self, slot, b):
    cand[self.cycle].append((slot, round(self._understanding(slot), 3)))
    return m0(self, slot, b)


tether.Agent._mint_in_step = spy
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
asked = collections.Counter(r["cycle"] for r in led.rows() if r["event"] == "derived_asked")
defer = collections.Counter(r["cycle"] for r in led.rows() if r["event"] == "derived_deferred")
zero = pos = tie_steps = 0
for c in sorted(set(cand) | set(asked) | set(defer)):
    us = [u for _s, u in cand.get(c, [])]
    z = sum(1 for u in us if u == 0)
    zero += z
    pos += len(us) - z
    if z and (asked[c] or defer[c]):
        tie_steps += 1
    print(c, "plain", cand.get(c, []), "derived asked", asked[c], "deferred", defer[c])
print(f"{which}: plain candidates rank>0 {pos}, rank 0 {zero}; steps with a rank-0 plain candidate "
      f"AND a derived ask (asked or deferred): {tie_steps}")
