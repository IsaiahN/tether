"""1a prototype for K1-K4: at every REUSE of a carried cell inside _cannot_pay, recompute its stored
prefix (rows, charged, first refuting row) from row 0 and compare. argv: world (fake|grid), steps,
drop (none|decoder|peers|window)."""
import collections
import sys
import time

sys.dont_write_bytecode = True
sys.path[:0] = ["c:/Users/Admin/Documents/GitHub/tether", "c:/Users/Admin/Documents/GitHub/tether/tests"]
import tether  # noqa: E402
from tether import NOT_RESOLVED  # noqa: E402

tether._AGENT_SEED = False
world_name, n, drop = sys.argv[1], int(sys.argv[2]), sys.argv[3]
DROP = {"none": (), "decoder": (5,), "peers": (7, 8), "window": (3,)}[drop]
key0 = tether.Agent._divide_key


def key(self, slot, held):
    k = list(key0(self, slot, held))
    for i in DROP:
        k[i] = None
    return tuple(k)


tether.Agent._divide_key = key


def shadow(ag, term, slot, robs, rows):
    wrong, ref = 0, None
    for i in range(rows):
        state, action, actual, intent, landed = robs[i]
        if not ag._applies(term, state):
            wrong += 1
        elif ag._out_of_step_range(term, slot, state, actual):
            wrong += 1
            ref = i if ref is None else ref
        else:
            ops = ag._ops(term, state)
            if ops is None:
                wrong += 1
            else:
                got = ag._value_of(term, slot, state, ag._eval_ctx(
                    slot, state, action=action, operands=ops, intent=intent, landed=landed,
                    guard_ref=term.guard_ref))
                if got is NOT_RESOLVED:
                    wrong += 1
                elif got % ag.alphabet[slot] != actual % ag.alphabet[slot]:
                    wrong += 1
                    ref = i if ref is None else ref
    return wrong, ref


stats = collections.Counter()
cp0 = tether.Agent._cannot_pay


def cp(self, term, slot, robs, cost, base, rkey=None):
    dv = self._dv
    if dv is not None and isinstance(rkey, tuple):
        c = rkey[0].get(term) or rkey[1].get(term)
        if c is not None and len(c) > 2 and (c[3] is None or c[3] == self.cycle) and c[4] < dv["mint"]:
            if c[0] <= len(robs):
                stats["reused"] += 1
                stats["rows"] += c[0]
                w, r = shadow(self, term, slot, robs, c[0])
                if (w, r) != (c[1], c[2]):
                    stats["MISMATCH"] += 1
    return cp0(self, term, slot, robs, cost, base, rkey)


tether.Agent._cannot_pay = cp
t0 = time.time()
if world_name == "fake":
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
    if world_name == "fake":
        env.observe()
    ag.step()
    if world_name == "fake" and env.terminal():
        break
ag.end_run("cap")
rows = led.rows()
closes = collections.Counter(r["detail"]["cause"] for r in rows if r["event"] == "space_closed")
brk = sum(1 for r in rows if r["event"] == "frame_break")
print(world_name, "drop", drop, "steps", n, "wall", round(time.time() - t0, 1), dict(stats),
      "breaks", brk, "closes", dict(closes))
