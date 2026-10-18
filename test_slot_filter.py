"""C-S1-1, SPEED-1 S1 (the reviewer 2026-10-15 11:05). WRITTEN, NOT RUN: it runs in the
end-of-step-7 checklist.

  (a)  restated 2026-10-18 (the reviewer 09:17, ruling A), each regime set in the child and printed
       back. Since K1 (089789e) its T4/T5 cut makes an answer depend on a step's cost, so OFF,
       the dearer path, is cut at the default cap where ON is not:
       (i)  with the cut unbound (STEP_BUDGET 10^12, C1's scheduler on), the _index_reach answers
            (views, causes, refusal counts) are identical ON and OFF, call for call -- the filter
            changes cost, never answers. Not with TETHER_STEP_BUDGET=0: that also removes C1's rank
       (ii) at the default cap, ON's calls equal the uncapped ON's and no ON call is cut (OFF's
            cut calls are reported) -- cheaper reaches further, never wronger
  (b)  WHOLE-GAME IDENTITY: the same fake game, same seed and arms, gives the identical sequence
       of actions (as the wrapper receives them) and choice rows ON and OFF, the cut unbound
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
tether.STEP_BUDGET = {cap} or tether.STEP_BUDGET
if {wrong}:
    real = tether._lands
    tether._lands = lambda role, a, b, slot, sub: real(role, a, b, slot + ".wrong", sub)
    # under C4 (TETHER_REACH_SHARE) the filter keeps its rows through _landing_rows, never _lands
    rows_real = tether._landing_rows
    tether._landing_rows = lambda role, held, key, slot, sub, t: rows_real(
        role, held, key, slot + ".wrong", sub, t)
calls, k1cut, last = [], [], {{}}
orig = tether.Agent._index_reach
def spy(self, lib, lit, slot, mine, others, **kw):
    last["lib"] = lib
    views, causes, refused = orig(self, lib, lit, slot, mine, others, **kw)
    calls.append([slot, mine, list(others),
                  sorted([n, c.slot, i["library"], i["role"], i["entries"]]
                         for n, (c, i) in views.items()),
                  sorted([list(k), i["library"], i["entries"]]
                         for k, (_a, _b, i) in causes.items()),
                  sorted(refused.items())])
    k1cut.append(bool(getattr(self, "_k1_trunc", False)))   # K1's T4/T5 cut fired by this call
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
    # called as the agent calls it: under SPEED-2 (TETHER_SPEED2_COUNT) with a tally, so the
    # refusals are counted, never rows -- the slot memo it is compared with holds landings only
    _tl = (lambda: __import__("collections").Counter()) if tether._SPEED2_COUNT else (lambda: None)
    got = ag._compiled(last["lib"], key, role, o, x, None, atoms, sig, slot=slot, tally=_tl())
    tether._bound = real
    memo = tether._BOUND_MEMO if ag._atoms_token else ag._bound_cache
    mkey = sk[:6]
    memo[mkey] = tuple(r for r in memo[mkey] if r != before[0])
    smemo.clear()
    cut = ag._compiled(last["lib"], key, role, o, x, None, atoms, sig, slot=slot, tally=_tl())
    pre = {{"binds": len(nb), "same": tuple(got) == before, "rows": len(got),
            "cut_differs": tuple(cut) != before}}
print("OUT " + json.dumps({{"calls": calls, "acts": acts, "rows": rows, "pre": pre, "cut": k1cut,
                            "cap": tether.STEP_BUDGET,
                            "filtered": tether._INDEX_N["bound_slot"]}}, default=repr))
"""
UNBOUND = 10 ** 12      # (i)'s cap: no step of this game comes near it, so K1's cut never fires


def _children(spec: dict) -> dict:
    """name -> (arms, cap, wrong); at most three children at once. cap 0 keeps the default."""
    out, todo = {}, list(spec.items())
    while todo:
        batch, todo = todo[:3], todo[3:]
        procs = {}
        for name, (arms, cap, wrong) in batch:
            env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
            # C-seed-X: two separately born agents compared under ONE temperament, or the per-birth
            # seed alone makes their paths differ (the same pin as test_speed2_count)
            env.update({"TETHER_AGENT_SEED": "0"}, **arms)
            procs[name] = subprocess.Popen(
                [sys.executable, "-B", "-c", CHILD.format(wrong=wrong, cap=cap)], env=env,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, stdin=subprocess.DEVNULL)
        for name, p in procs.items():
            so, se = p.communicate()
            assert p.returncode == 0, (name, se[-3000:])
            out[name] = json.loads([ln for ln in so.splitlines() if ln.startswith("OUT ")][-1][4:])
    return out


def main() -> None:
    filt = {"TETHER_SLOT_FILTER": "0"}
    r = _children({"on": ({}, 0, False), "off": (filt, 0, False), "on_u": ({}, UNBOUND, False),
                   "off_u": (filt, UNBOUND, False), "bad_u": ({}, UNBOUND, True)})
    on, off, on_u, off_u, bad = r["on"], r["off"], r["on_u"], r["off_u"], r["bad_u"]
    # each child ran the regime it was handed
    caps = {n: v["cap"] for n, v in r.items()}
    assert on["cap"] == off["cap"] < UNBOUND == on_u["cap"] == off_u["cap"] == bad["cap"], caps
    # THE TREATMENT-EXECUTED CHECK: the ON runs took the filtered branch, the OFF runs never did
    filtered = {n: v["filtered"] for n, v in r.items()}
    assert on["filtered"] > 0 and on_u["filtered"] > 0 and bad["filtered"] > 0, filtered
    assert off["filtered"] == off_u["filtered"] == 0, filtered
    # THE PANEL PRECONDITION: (a) and MF can only discriminate if some call answered something
    assert any(c[3] or c[4] for c in on_u["calls"]), "precondition: no view or cause was reached"
    assert not any(on_u["cut"]) and not any(off_u["cut"]), "precondition: the unbound cap was cut"
    assert on_u["calls"] == off_u["calls"], "(a)(i) answers differ ON vs OFF, the cut unbound"
    print(f"  (a)(i) cap {UNBOUND}: {len(on_u['calls'])} _index_reach answers identical ON and OFF")
    assert on["calls"] == on_u["calls"], "(a)(ii) ON at the default cap differs from ON uncapped"
    assert not any(on["cut"]), "(a)(ii) an ON call was cut at the default cap"
    print(f"  (a)(ii) cap {on['cap']}: ON's {len(on['calls'])} calls equal the uncapped ON's, "
          f"0 cut; OFF cut {sum(off['cut'])} of {len(off['cut'])} calls at that cap")
    on, off = on_u, off_u
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
    assert bad["calls"] != off["calls"], "MF MUST-FAIL did not fail: the wrong slot changed nothing"
    print("  MF must-fail fired: filtering on the wrong slot changes (a)")
    print("slot filter: OK")


if __name__ == "__main__":
    main()
