"""C-S1-1, SPEED-1 S1 (the reviewer 2026-10-15 11:05). WRITTEN, NOT RUN: it runs in the
end-of-step-7 checklist.

  (a)  the same game's _index_reach answers (views, causes, refusal counts) are identical with
       TETHER_SLOT_FILTER ON and OFF, call for call
  (b)  WHOLE-GAME IDENTITY: the same fake game, same seed and arms, gives the identical sequence
       of actions (as the wrapper receives them) and choice rows ON and OFF
  (c)  with the WHOLE view already held, the filtered call binds 0 rows and returns the same
       answer it bound before (the reviewer 2026-10-15 11:14 N1)
  MF   MUST-FAIL: filtering on the wrong slot changes (a)
  MF-W MUST-FAIL: a held whole view with one kept row removed gives a different filtered answer,
       so (c)'s "same" can see a wrong whole

    python test_slot_filter.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

CHILD = """
import json, sys
sys.dont_write_bytecode = True
import arc_holdout, tether
from test_entry import FakeWrapper
if {wrong}:
    real = tether._lands
    tether._lands = lambda role, a, b, slot, sub: real(role, a, b, slot + ".wrong", sub)
calls, last = [], {{}}
orig = tether.Agent._index_reach
def spy(self, lib, lit, slot, mine, others):
    last["lib"] = lib
    views, causes, refused = orig(self, lib, lit, slot, mine, others)
    calls.append([slot, mine, list(others),
                  sorted([n, c.slot, i["library"], i["role"], i["entries"]]
                         for n, (c, i) in views.items()),
                  sorted([list(k), i["library"], i["entries"]]
                         for k, (_a, _b, i) in causes.items()),
                  sorted(refused.items())])
    return views, causes, refused
tether.Agent._index_reach = spy
acts = []
step = FakeWrapper.step
def sent(self, action, data=None, reasoning=None):
    acts.append([repr(action), repr(data)])
    return step(self, action, data, reasoning)
FakeWrapper.step = sent
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), 'fake')
[ag.step() for _ in range(30)]
rows = [[r["cycle"], r["slot"], r["detail"]] for r in led.rows() if r["event"] == "choice"]
pre = None
smemo = tether._BOUND_SLOT_MEMO if ag._atoms_token else ag._bound_slot_cache
if tether._SLOT_FILTER and not {wrong}:
    sk = next(k for k, v in smemo.items() if v)
    _tok, sig, key, role, o, x, slot = sk
    before = smemo[sk]
    atoms = {{a.name: a for a in ag.gamma.atoms}}
    ag._compiled(last["lib"], key, role, o, x, None, atoms, sig)   # the whole view, held
    smemo.clear()
    nb, real = [], tether._bound
    tether._bound = lambda *a: nb.append(1) or real(*a)
    got = ag._compiled(last["lib"], key, role, o, x, None, atoms, sig, slot=slot)
    tether._bound = real
    memo = tether._BOUND_MEMO if ag._atoms_token else ag._bound_cache
    mkey = sk[:6]
    memo[mkey] = tuple(r for r in memo[mkey] if r != before[0])
    smemo.clear()
    cut = ag._compiled(last["lib"], key, role, o, x, None, atoms, sig, slot=slot)
    pre = {{"binds": len(nb), "same": tuple(got) == before, "rows": len(got),
            "cut_differs": tuple(cut) != before}}
print("OUT " + json.dumps({{"calls": calls, "acts": acts, "rows": rows, "pre": pre,
                            "filtered": tether._INDEX_N["bound_slot"]}}, default=repr))
"""


def _child(arms: dict, wrong: bool = False) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    # C-seed-X: two separately born agents compared under ONE temperament, or the per-birth
    # seed alone makes their paths differ (the same pin as test_speed2_count)
    env.update({"TETHER_AGENT_SEED": "0"}, **arms)
    r = subprocess.run([sys.executable, "-B", "-c", CHILD.format(wrong=wrong)], env=env,
                       capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
    return json.loads(out[-1][4:])


def main() -> None:
    on, off = _child({}), _child({"TETHER_SLOT_FILTER": "0"})
    # THE TREATMENT-EXECUTED CHECK: the ON run took the filtered branch, the OFF run never did
    assert on["filtered"] > 0 and off["filtered"] == 0, (on["filtered"], off["filtered"])
    # THE PANEL PRECONDITION: (a) and MF can only discriminate if some call answered something
    assert any(c[3] or c[4] for c in on["calls"]), "precondition: no view or cause was reached"
    assert on["calls"] == off["calls"], "(a) _index_reach answers differ ON vs OFF"
    print(f"  (a) {len(on['calls'])} _index_reach answers identical ON and OFF")
    assert on["acts"], "precondition: the game sent no action, so (b) compares nothing"
    assert on["acts"] == off["acts"], "(b) the actions sent differ ON vs OFF"
    assert on["rows"] == off["rows"], "(b) the choice rows differ ON vs OFF"
    print(f"  (b) {len(on['acts'])} actions and {len(on['rows'])} choice rows identical ON and OFF")
    pre = on["pre"]
    assert pre and pre["rows"], ("precondition: no non-empty slot answer to pre-hold", pre)
    assert pre["binds"] == 0 and pre["same"], ("(c) a held whole view was bound again", pre)
    print(f"  (c) whole view held: the filtered call bound 0 rows, same {pre['rows']} rows")
    assert pre["cut_differs"], "MF-W MUST-FAIL did not fail: a cut whole view gave the same answer"
    print("  MF-W must-fail fired: a whole view missing a kept row gives a different answer")
    bad = _child({}, wrong=True)
    assert bad["calls"] != off["calls"], "MF MUST-FAIL did not fail: the wrong slot changed nothing"
    print("  MF must-fail fired: filtering on the wrong slot changes (a)")
    print("slot filter: OK")


if __name__ == "__main__":
    main()
