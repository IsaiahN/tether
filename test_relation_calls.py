"""THE CALL CLOSES 5 AND 9, TETHER_RELATION_SET (the reviewer 2026-10-11 14:17 CDT).

5, the face count: contact(o, x) > 0 / != 0 -> the face atom touches<x>; == 0 -> touches . negate;
  any other value refused ("the face count's pair part is held back"). NEVER the box slot
  touches_x, whose gap 0 counts a corner.
9, an EXTENT "== 0": sign . holds . negate (an extent is never negative; sign on it is "nonzero").

  c1 ON: "contact(o, x) == 1" refused with the held-back reason;
  c2 ON: "contact(o, x) > 0" compiles to touches<x>; at a CORNER-ONLY contact it reads False while
     the box slot touches_x reads 1 (the trap's must-fail); at a shared face it reads True;
  c3 ON: "contact(o, x) == 0" reads True at the corner;
  e1 ON: "o1.residual == 0" compiles to sign . holds . negate: 0 -> True, 1 -> False;
  OFF: both refused as before (the gate's must-fail).

    python test_relation_calls.py
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
import compile_term as C, relations
from compile_census import arc_atoms_wired
atoms = arc_atoms_wired()
def comp(t):
    c = C.compile_candidate({"condition": t}, atoms)
    return c if isinstance(c, C.Compiled) else c.reason
def obj(r, q):
    return {"row": r, "col": q, "structure": frozenset({(0, 0)})}
A, corner, face = obj(0, 0), obj(1, 1), obj(0, 1)
box = lambda o: {"row": o["row"], "col": o["col"], "h": 1, "w": 1}
out = {}
for t in ("contact(o, x) == 1", "contact(o, x) > 0", "contact(o, x) == 0", "o1.residual == 0"):
    c = comp(t)
    out[t] = c if isinstance(c, str) else [a.name for a in c.term.atoms]
g = comp("contact(o, x) > 0")
z = comp("contact(o, x) == 0")
e = comp("o1.residual == 0")
if not isinstance(g, str):
    out["corner_face_box"] = [C.run(g, {"o": A, "x": corner}), C.run(g, {"o": A, "x": face}),
                              relations.pair_values(box(A), box(corner))["touches"]]
    out["corner_zero"] = C.run(z, {"o": A, "x": corner})
if not isinstance(e, str):
    out["extent"] = [C.run(e, {"o1.residual": 0}), C.run(e, {"o1.residual": 1})]
print(json.dumps(out))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_RELATION_SET="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=os.path.dirname(os.path.abspath(__file__)), timeout=300)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    off = _run(False)
    assert "no pairwise atom" in off["contact(o, x) > 0"], off
    assert off["o1.residual == 0"] == "holds does not accept EXTENT", off
    print("  OFF: contact and the EXTENT zero refused as before")
    on = _run(True)
    assert on["contact(o, x) == 1"] == "the face count's pair part is held back (TETHER_OBSERVER)"
    print(f"  c1 contact == 1: {on['contact(o, x) == 1']!r}")
    assert on["contact(o, x) > 0"] == ["touches"], on
    assert on["corner_face_box"] == [False, True, 1], on
    print(f"  c2 contact > 0 -> touches<x>: corner {on['corner_face_box'][0]}, face "
          f"{on['corner_face_box'][1]}; the box slot touches_x at the corner reads "
          f"{on['corner_face_box'][2]} (the trap)")
    assert on["contact(o, x) == 0"] == ["touches", "negate"] and on["corner_zero"] is True, on
    print("  c3 contact == 0 -> touches . negate: True at the corner")
    assert on["o1.residual == 0"] == ["sign", "holds", "negate"] and on["extent"] == [True, False]
    print(f"  e1 o1.residual == 0 -> sign . holds . negate: 0 {on['extent'][0]}, "
          f"1 {on['extent'][1]}")
    print("relation calls: OK")
