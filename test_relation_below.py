"""B1, TETHER_RELATION_SET (the reviewer 2026-10-11 14:19Z, plan accepted 14:33Z): `below`, the
own-slot converse of `above`. The arm is read at import, so each half runs in its own process.

  OFF: Gamma holds no `below`; "o0.row < o3.row" compiles as today -- `above` run on o3.row
       with o0.row as the operand (the binding reversed, o3 the subject).
  ON:  Gamma holds `below`; the same condition runs on o0.row with o3.row as the operand, so the
       LEFT party is the subject (F1's case); below(1 vs 3) = 1, (3 vs 1) = 0, (2 vs 2) = 0;
       and like `above` it refuses an unordered reading ("o0.colour < o3.colour").

    python test_relation_below.py
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
import compile_term
from test_goal_condition import _agent
ag = _agent()
atoms = {a.name: a for a in ag.gamma.atoms}
c = compile_term.compile_candidate({"condition": "o0.row < o3.row"}, atoms)
out = {"below": "below" in atoms, "slot": c.slot, "operand": c.operand,
       "chain": [a.name for a in c.term.atoms]}
if "below" in atoms:
    b = atoms["below"]
    from gamma import Ctx
    out["values"] = [b.fn(v, Ctx(operands=(o,))) for v, o in ((1, 3), (3, 1), (2, 2))]
    r = compile_term.compile_candidate({"condition": "o0.colour < o3.colour"}, atoms)
    out["colour"] = type(r).__name__
print(json.dumps(out))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_RELATION_SET="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=os.path.dirname(os.path.abspath(__file__)), timeout=240)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    off = _run(False)
    assert not off["below"], off
    assert off["slot"] == "o3.row" and off["operand"] == "o0.row" and off["chain"] == ["above"], off
    print(f"  OFF: no `below`; '<' runs above on {off['slot']} with operand {off['operand']}")
    on = _run(True)
    assert on["below"], on
    assert on["slot"] == "o0.row" and on["operand"] == "o3.row" and on["chain"] == ["below"], on
    assert on["values"] == [1, 0, 0], on
    assert on["colour"] == "Refusal", on
    print(f"  ON: '<' runs below on {on['slot']} with operand {on['operand']}; values "
          f"{on['values']}; colour '<' refused")
    print("relation below: OK")
