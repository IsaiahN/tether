"""Occasions for candidate (a): _compiled asks by (role, o == x, sig held, plain names), with
time spent, on the fake run (24 steps, the arms as the tree defaults)."""
import json
import sys
import time
from collections import Counter

sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout  # noqa: E402
import tether  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402

n, t, gens = Counter(), Counter(), Counter()
orig = tether.Agent._compiled


def spy(self, lib, key, role, o, x, comp, atoms, sig, slot=None, tally=None):
    plain = all(tether._PLAIN.fullmatch(s) and "PH" not in s for s in (o, x))
    k = (role, "o==x" if o == x else "o!=x", "sig" if sig is not None else "nosig",
         "plain" if plain else "named", "slot" if slot is not None else "whole")
    t0 = time.perf_counter()
    got = orig(self, lib, key, role, o, x, comp, atoms, sig, slot, tally)
    t[str(k)] += time.perf_counter() - t0
    n[str(k)] += 1
    if isinstance(got, list):
        return got
    gens[str(k)] += 1
    return _timed(got, str(k))


def _timed(g, k):
    # the unheld branch returns a generator: its _lib_view and comp() run as the caller iterates,
    # so each next() is timed where it happens, and an early stop by the caller is kept
    while True:
        t0 = time.perf_counter()
        try:
            v = next(g)
        except StopIteration:
            t[k] += time.perf_counter() - t0
            return
        t[k] += time.perf_counter() - t0
        yield v


tether.Agent._compiled = spy
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
t0 = time.perf_counter()
for _ in range(24):
    ag.step()
total = time.perf_counter() - t0
for k in sorted(n, key=lambda k: -t[k]):
    print(f"{n[k]:7d} {t[k]:8.2f}s gens {gens[k]:6d}  {k}")
print(json.dumps({"total_s": round(total, 2), "calls": sum(n.values()),
                  "compiled_s": round(sum(t.values()), 2)}))
