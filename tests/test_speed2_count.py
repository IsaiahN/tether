"""C-SPEED2-1, SPEED-2 item 1 (the reviewer 2026-10-15 17:31, 17:32 C1-C3).

  R    the same fake game gives identical _index_reach answers (views, causes, refusal counts),
       call for call, and identical actions and choice rows, with TETHER_SPEED2_COUNT ON and OFF
  C1   not vacuous: the ON run counted refusals (> 0), reused a pair's count (a slot-memo hit),
       and split at least one named compile whose partner is a compound pair owner ("~")
  C    the slot memo holds no Refusal row under ON (and holds some under OFF, the
       precondition that ON has rows to drop)
  MF   MUST-FAIL, a planted fault: a pair's Counter not added when the pair is asked again;
       R must fail on it
  8 steps per child (the fake game costs ~10 s a step; three children under 5 minutes).
  Both children run under the old seed constant (C-seed-X), since they compare two births.

    python tests/test_speed2_count.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

CHILD = """
import json, sys
sys.dont_write_bytecode = True
from collections import Counter
import arc_holdout, tether
from test_entry import FakeWrapper
if {plant}:
    real_pc = tether.Agent._pair_count
    def planted(self, lib, key, role, o, x, atoms, sig, mkey):
        again = tether._pair_tally_of(self, mkey) is not None
        got = real_pc(self, lib, key, role, o, x, atoms, sig, mkey)
        return (Counter(), got[1]) if again else got
    tether.Agent._pair_count = planted
calls, compound = [], []
orig = tether.Agent._index_reach
def spy(self, lib, lit, slot, mine, others):
    views, causes, refused = orig(self, lib, lit, slot, mine, others)
    calls.append([slot, mine, list(others),
                  sorted([n, c.slot, i["library"], i["role"], i["entries"]]
                         for n, (c, i) in views.items()),
                  sorted([list(k), i["library"], i["entries"]]
                         for k, (_a, _b, i) in causes.items()),
                  sorted(refused.items())])
    return views, causes, refused
tether.Agent._index_reach = spy
real_c = tether.Agent._compiled
def cspy(self, lib, key, role, o, x, comp, atoms, sig, slot=None, tally=None):
    n = tether._INDEX_N["named_split"]
    got = real_c(self, lib, key, role, o, x, comp, atoms, sig, slot=slot, tally=tally)
    if tether._INDEX_N["named_split"] > n and "~" in o + x:
        compound.append([role, o, x])
    return got
tether.Agent._compiled = cspy
acts = []
step = FakeWrapper.step
def sent(self, action, data=None, reasoning=None):
    acts.append([repr(action), repr(data)])
    return step(self, action, data, reasoning)
FakeWrapper.step = sent
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), 'fake')
[ag.step() for _ in range(8)]
rows = [[r["cycle"], r["slot"], r["detail"]] for r in led.rows() if r["event"] == "choice"]
n = tether._INDEX_N
smemo = tether._BOUND_SLOT_MEMO if ag._atoms_token else ag._bound_slot_cache
stored = sum(isinstance(c, tether.compile_term.Refusal)
             for rows_ in smemo.values() for r in rows_ for c in r[1:])
print("OUT " + json.dumps({{"calls": calls, "acts": acts, "rows": rows, "compound": compound,
                            "hits": n["bound_slot_hit"], "pair_count": n["pair_count"],
                            "named_split": n["named_split"], "stored": stored}}, default=repr))
"""


def _child(arms: dict, plant: bool = False) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"TETHER_AGENT_SEED": "0"}, **arms)
    r = subprocess.run([sys.executable, "-B", "-c", CHILD.format(plant=plant)], env=env,
                       capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
    return json.loads(out[-1][4:])


def main() -> None:
    on, off = _child({}), _child({"TETHER_SPEED2_COUNT": "0"})
    refused = sum(n for c in on["calls"] for _k, n in c[5])
    print(f"  C1 refused {refused}, pair counts {on['pair_count']}, slot-memo hits {on['hits']},"
          f" named splits {on['named_split']}, compound partners {len(on['compound'])}"
          f" (OFF: pair counts {off['pair_count']}, named splits {off['named_split']})")
    assert off["pair_count"] == 0 and off["named_split"] == 0, "OFF took the SPEED-2 path"
    assert refused > 0, "C1: no refusal counted, so R compares no count"
    assert on["pair_count"] > 0 and on["hits"] > 0, "C1: no pair count reused on a memo hit"
    assert on["compound"], "C1: no compound partner took the named split"
    assert off["stored"] > 0, "C precondition: OFF stores no refusal row in a slot memo"
    assert on["stored"] == 0, ("C: a refusal row stored in a slot memo under ON", on["stored"])
    print(f"  C  slot-memo refusal rows: ON 0, OFF {off['stored']}")
    assert on["calls"] == off["calls"], "R: _index_reach answers differ ON vs OFF"
    print(f"  R  {len(on['calls'])} _index_reach answers identical ON and OFF")
    assert on["acts"] and on["acts"] == off["acts"], "R: the actions sent differ ON vs OFF"
    assert on["rows"] == off["rows"], "R: the choice rows differ ON vs OFF"
    print(f"  R  {len(on['acts'])} actions and {len(on['rows'])} choice rows identical ON and OFF")
    bad = _child({}, plant=True)
    assert bad["calls"] != off["calls"], "MF MUST-FAIL did not fail: an unadded count passed R"
    print("  MF must-fail fired: a pair's Counter not added on reuse changes R")
    print("speed2 count: OK")


if __name__ == "__main__":
    main()
