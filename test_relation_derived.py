"""B2b, TETHER_RELATION_SET (the reviewer 2026-10-11 10:30 CDT): a pair slot is a DERIVED reading --
not bet on, predicted from the predicted sources, searched only on a relational surprise.

  m1 held: the derived prediction holds and the sources held -> no residual entry, no search;
  m2 blocked move: the sources held, the observed relation differs -> exactly ONE residual entry
     and one `relational_surprise` row;
  m3 a source missed -> no entry (the source's own residual carries the surprise);
  m4 live, gridworld_s0 ON for 3 cycles: NO `bet` row on any pair slot, and a `@derived` row per
     cycle; OFF: no `@derived` row.
  m5 derivation order (the reviewer 2026-10-11 10:44 CDT): in the operand list every ordinary slot
     precedes every derived slot (an ordinary operand is tried first), and every derived slot is
     still in the list (reached once the ordinary ones are spent) -- an order, never a cut.

    python test_relation_derived.py
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
import gamma, ledger, tether, world
from conform import panel
g, seed = panel._gridworld("gridworld_s0")
env = world.bind(g)
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"t_{seed}"), tether.Config(), ledger.Ledger())
out = {}
if tether.__dict__.get("SlotResidual") and g.derived():
    S = tether.SlotResidual
    k = sorted(g.derived())[0]
    srcs = g.derived()[k]
    ag.alphabet = ag._alphabets(env)
    def case(src_bits, after_k, dpred_k):
        res = {s: S(s, tether.TRANSITION, 1, 1, src_bits) for s in srcs}
        n0 = len(ag.led.rows())
        ag._relational_surprise({k: srcs}, {k: dpred_k}, res, {k: after_k}, {k: dpred_k})
        rows = [r["event"] for r in ag.led.rows()[n0:]]
        return [k in res, rows.count("relational_surprise")]
    out["m1"] = case(0, 2, 2)
    out["m2"] = case(0, 3, 2)
    out["m3"] = case(1.0, 3, 2)
n0 = len(ag.led.rows())
for _ in range(3):
    ag.step()
rows = ag.led.rows()[n0:]
pair = set(g.derived())
out["pair_bets"] = sum(1 for r in rows if r["event"] == "bet" and r["slot"] in pair)
out["derived_rows"] = sum(1 for r in rows if r["event"] == "derived")
out["n_pair"] = len(pair)
b = [x for x in ag._bindings("o0.row", []) if x is not None]
der = [i for i, x in enumerate(b) if x in pair]
ordi = [i for i, x in enumerate(b) if x not in pair]
out["m5"] = [bool(der) and bool(ordi) and max(ordi) < min(der),
             len(der) == len([x for x in pair if x != "o0.row"])]
print(json.dumps(out))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_RELATION_SET="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=os.path.dirname(os.path.abspath(__file__)), timeout=600)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    off = _run(False)
    assert off["n_pair"] == 0 and off["derived_rows"] == 0, off
    print("  OFF: no derived slots, no @derived row")
    on = _run(True)
    assert on["n_pair"] == 150, on
    assert on["m1"] == [False, 0], on
    assert on["m2"] == [True, 1], on
    assert on["m3"] == [False, 0], on
    print(f"  m1 held -> {on['m1']}; m2 blocked -> {on['m2']}; m3 source missed -> {on['m3']}")
    assert on["pair_bets"] == 0 and on["derived_rows"] == 3, on
    print(f"  m4 live 3 cycles: {on['pair_bets']} bets on {on['n_pair']} pair slots; "
          f"{on['derived_rows']} @derived rows")
    assert on["m5"] == [True, True], on
    print(f"  m5 operand order: ordinary before derived, all derived reached -> {on['m5']}")
    print("relation derived: OK")
