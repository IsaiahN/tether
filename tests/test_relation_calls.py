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
6/7, the sparse observer pairs (14:31 CDT): inside(o, x) -> x~o.inside (HOLE), bbox(o, x) -> the
  sorted a~b.bbox; an absent pair with both objects present IS 0 (relations.SPARSE_PAIR), only
  where a condition is evaluated:
  s1 B in A's BOX, not its hole: inside(B, A) == 0 True, == 1 False -- never None; the box slot
     B.inside_A reads 1 on the same scene (the trap's must-fail);
  s2 B in A's hole: inside(B, A) == 1 True;
  s3 A absent: None, not 0;
  s4 the survivorship guard: over three rows (holds once, absent twice with both present) the
     positive form reads [True, False, False], not [True, None, None];
  s5 bbox(o, x) > 0: interleaved boxes True; separate objects False, not None;
  s6 the direction pin: with only A~B.inside (B inside A), inside(A, B) == 1 reads False;
  s7 (15:08 CDT) inside(B, A) > 0 -- the library's only spelling -- is == 1 spelled again: False at
     box-not-hole through the sparse default (never None), True in the hole; != 0 the same;
  s8 inside(B, A) > 1 refused "a BOOL is 0 or 1";
  OFF: both refused as before (the gate's must-fail).

    python tests/test_relation_calls.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

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
i1, i0 = comp("inside(B, A) == 1"), comp("inside(B, A) == 0")
bb, rev = comp("bbox(o, x) > 0"), comp("inside(A, B) == 1")
both = {"A.row": 0, "B.row": 1}
if not isinstance(i1, str):
    hole = {**both, "A~B.inside": 1}
    out["inside"] = {"slot": i1.slot,
                     "s1": [C.run(i0, both), C.run(i1, both),
                            int(relations.within({"row": 1, "col": 1, "h": 1, "w": 1},
                                                 {"row": 0, "col": 0, "h": 3, "w": 3}))],
                     "s2": C.run(i1, hole), "s3": C.run(i1, {"B.row": 1}),
                     "s4": [C.run(i1, r) for r in (hole, both, both)],
                     "s6": C.run(rev, {**both, "A~B.inside": 1})}
    g7, n7 = comp("inside(B, A) > 0"), comp("inside(B, A) != 0")
    out["inside"]["s7"] = (g7 if isinstance(g7, str) else
                           [C.run(g7, both), C.run(g7, hole), C.run(n7, both), C.run(n7, hole)])
    out["inside"]["s8"] = comp("inside(B, A) > 1")
if not isinstance(bb, str):
    out["bbox"] = {"slot": bb.slot, "s5": [C.run(bb, {"o.row": 0, "x.row": 1, "o~x.bbox": 4}),
                                          C.run(bb, {"o.row": 0, "x.row": 5})]}
out["refused_off"] = [c if isinstance(c, str) else "compiled"
                      for c in (comp("inside(B, A) == 1"), comp("bbox(o, x) > 0"))]
print(json.dumps(out))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_RELATION_SET="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=_repo.ROOT, timeout=300)
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
    assert "compiled" not in off["refused_off"], off
    ins = on["inside"]
    assert ins["slot"] == "A~B.inside", ins                         # B inside A: A~B
    assert ins["s1"] == [True, False, 1], ins
    print(f"  s1 box-not-hole: inside==0 {ins['s1'][0]}, ==1 {ins['s1'][1]}; box slot "
          f"inside_x {ins['s1'][2]} (the trap)")
    assert ins["s2"] is True and ins["s3"] is None, ins
    print(f"  s2 in the hole: {ins['s2']}; s3 A absent: {ins['s3']}")
    assert ins["s4"] == [True, False, False], ins
    print(f"  s4 survivorship guard: {ins['s4']}")
    assert on["bbox"]["slot"] == "o~x.bbox" and on["bbox"]["s5"] == [True, False], on
    print(f"  s5 bbox > 0: overlap {on['bbox']['s5'][0]}, separate {on['bbox']['s5'][1]}")
    assert ins["s6"] is False, ins
    print("  s6 direction pin: inside(A, B) == 1 with only A~B.inside reads False")
    assert ins["s7"] == [False, True, False, True], ins
    print(f"  s7 inside > 0 / != 0: box-not-hole {ins['s7'][0]} (not None), hole {ins['s7'][1]}")
    assert ins["s8"] == "a BOOL is 0 or 1", ins
    print(f"  s8 inside > 1: {ins['s8']!r}")
    print("relation calls: OK")
