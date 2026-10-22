"""S2a, ROUTE TIER 0 (TETHER_FIT_TIER0; the reviewer 2026-10-20 19:54 CDT). gridworld_arc_s1, 25
steps, the agent seed pinned, three processes: ON, OFF, and the CHECK run (ON +
TETHER_FIT_TIER0_CHECK: every skip also runs the full fit, whose result is used).

  PRECONDITION: the ON run stores no-fit verdicts and skips on them (tier0 rows > 0), or every
     must-fail below is vacuous.
  (b) the CHECK run: every skipped fit, run anyway, returned None and left the library unmoved;
     and its decisions are OFF's (rows identical to OFF's once the tier0 / tier0_check rows are
     dropped, the arms row's on / off lists, the proposal's
     wall_s and the check's own book counters masked).
  (a) a planted bet MISS on a stored slot (route called with mass > 0): the full fit runs and the
     stored verdict is dropped; with mass 0 and nothing moved, the fit is skipped.
  (d) a planted library change (a new term): every stored slot's key moves, so each wakes.
  (e) a call at an exhausted step budget, and one whose walk ends at it, store nothing;
     a full call stores (the reviewer 20:15).
  OFF: no tier0 row, and a call per owed slot per step.

    python test_fit_tier0.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, panel, tether, world

env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="tier0"), tether.Config(), ledger.Ledger())
calls = []
real = tether.Agent._library_fit


def counted(self, slot, exclude):
    calls.append((self.cycle, slot))
    return real(self, slot, exclude)


tether.Agent._library_fit = counted
for _ in range(25):
    ag.step()
rows = ag.led.rows()
out = {"arm": tether._FIT_TIER0, "check": tether._FIT_TIER0_CHECK, "calls": len(calls),
       "tier0": sum(1 for r in rows if r["event"] == "tier0"),
       "checks": [r["detail"]["agree"] for r in rows if r["event"] == "tier0_check"],
       "stored": sorted(ag._fit_none),
       "rows": rows}
if tether._FIT_TIER0 and not tether._FIT_TIER0_CHECK and ag._fit_none:
    s = sorted(ag._fit_none)[0]
    ag.owed_import.add(s)
    key0 = ag._fit_none[s][0]
    same = ag._fit_key(s, ag.bound.get(s)) == key0
    # (d) a planted term moves every stored slot's key; removed, they stand again
    keys = {sl: ag._fit_key(sl, ag.bound.get(sl)) for sl in ag._fit_none}
    lib = ag.gamma.library
    lib["zz_planted"] = next(iter(lib.values()))
    moved = [sl for sl in keys if ag._fit_key(sl, ag.bound.get(sl)) != keys[sl]]
    del lib["zz_planted"]
    back = all(ag._fit_key(sl, ag.bound.get(sl)) == keys[sl] for sl in keys)
    # (a) route: a held bet skips the fit, a missed one runs it and drops the verdict
    del calls[:]
    ag.route({s: tether.SlotResidual(s, "x", 0, 0, 0.0)})
    held = [c for c in calls if c[1] == s]
    del calls[:]
    ag.route({s: tether.SlotResidual(s, "x", 0, 1, 3.0)})
    missed = [c for c in calls if c[1] == s]
    dropped = s not in ag._fit_none
    # (e) the budget (the reviewer 20:15): a call at an exhausted budget (_lookup not asked) and a
    # call that ends at it (its walk cut) store nothing; a full call stores
    b0, store = tether.STEP_BUDGET, {}
    try:
        tether.STEP_BUDGET = ag._spent                    # spent before the call: not asked
        ag._fit_none.pop(s, None)
        ag._fit_tier0(s, ag.bound.get(s))
        store["owed"] = s in ag._fit_none
    finally:
        tether.STEP_BUDGET = b0
    ag._spent = 0
    ag._lookup = lambda _s, _h: setattr(ag, "_spent", ag._spent + tether.STEP_BUDGET)
    ag._fit_none.pop(s, None)
    ag._fit_tier0(s, ag.bound.get(s))                     # asked, and its walk ran to the budget
    store["walk"] = s in ag._fit_none
    del ag._lookup
    ag._spent = 0
    ag._fit_tier0(s, ag.bound.get(s))
    store["full"] = s in ag._fit_none
    out.update(key_same=same, held_calls=len(held), missed_calls=len(missed), dropped=dropped,
               woke=len(moved), of=len(keys), back=back, store=store)
print(json.dumps(out, default=str))
'''


def _run(on: str, check: str) -> dict:
    here = os.path.dirname(os.path.abspath(__file__))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_AGENT_SEED="0", TETHER_FIT_TIER0=on,
               TETHER_FIT_TIER0_CHECK=check)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, here], env=env, capture_output=True,
                         text=True, timeout=1200, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "conform"))
    from identity_mod_rows import compare
    on, off, chk = _run("1", "0"), _run("0", "0"), _run("1", "1")
    assert on["arm"] is True and off["arm"] is False and chk["check"] is True
    assert on["tier0"] > 0 and on["stored"], f"PRECONDITION: nothing stored or skipped: {on}"
    assert chk["checks"] and all(chk["checks"]), chk["checks"]
    for rs in (off["rows"], chk["rows"]):    # the arm lists differ by design (timings: compare)
        for r in rs:
            if r["event"] == "books":
                for k in ("fit_tier0_skip", "fit_tier0_agree", "fit_tier0_disagree"):
                    r["detail"].pop(k, None)
            elif r["event"] == "arms" and r["slot"] == "@run":
                r["detail"].pop("on", None)
                r["detail"].pop("off", None)
    bad = compare(off["rows"], chk["rows"], {"tier0", "tier0_check"})
    assert not bad, bad[:3]
    assert on["key_same"] and on["held_calls"] == 0, on
    assert on["missed_calls"] == 1 and on["dropped"], on
    assert on["woke"] == on["of"] > 0 and on["back"], on
    assert on["store"] == {"owed": False, "walk": False, "full": True}, on["store"]
    assert off["tier0"] == 0 and not off["stored"], off
    assert on["calls"] < off["calls"], (on["calls"], off["calls"])
    print(f"test_fit_tier0: pass (ON {on['tier0']} skips, {on['calls']} fits vs OFF "
          f"{off['calls']}; (b) the CHECK run's {len(chk['checks'])} skipped fits all agreed, its "
          f"rows OFF's; (a) held 0 calls, missed {on['missed_calls']} and dropped; (d) a planted "
          f"term woke {on['woke']} of {on['of']}; (e) budget-capped calls stored nothing, a "
          f"full call stored)")


if __name__ == "__main__":
    main()
