"""B1, TETHER_RELATION_SET (the reviewer 2026-10-11 14:19Z, plan accepted 14:33Z): `below`, the
own-slot converse of `above`. The arm is read at import, so each half runs in its own process.

  OFF: Gamma holds no `below`; "o0.row < o3.row" compiles as today -- `above` run on o3.row
       with o0.row as the operand (the binding reversed, o3 the subject).
  ON:  Gamma holds `below`; the same condition runs on o0.row with o3.row as the operand, so the
       LEFT party is the subject (F1's case); below(1 vs 3) = 1, (3 vs 1) = 0, (2 vs 2) = 0;
       and like `above` it refuses an unordered reading ("o0.colour < o3.colour").
  F1 (the reviewer 14:57Z): linked through the goal chain (_link_goal), the want lands on
       o0.row -- the movable party -- ON, and on o3.row OFF.

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
import tether
tether._GOAL_CONDITION = tether._GOAL_PAIR = tether._GOAL_LINK = True
for sl in ("o0.row", "o3.row"):
    ag.wants.pop(sl, None)
    ag._want_terms.pop(sl, None)
link = ag._link_goal("f1-case", c)
out["linked"] = bool(link.get("linked"))
out["wanting"] = sorted(sl for sl in ("o0.row", "o3.row") if sl in ag._want_scope)
m = compile_term.compile_candidate({"condition": "o3.row > o0.row"}, atoms)
mirror = {}
for label, moving in (("none", ()), ("o0", ("o0.row",)), ("o3", ("o3.row",))):
    ag.agency = type(ag.agency)()
    for sl in moving:
        ag.agency.note("A", {sl}, sorted(ag.slots))
        ag.agency.note("B", set(), sorted(ag.slots))
    for sl in ("o0.row", "o3.row"):
        ag.wants.pop(sl, None)
        ag._want_terms.pop(sl, None)
        ag._want_scope.pop(sl, None)
    ag._goal_links.clear()
    ag._link_goal("mirror-" + label, m)
    mirror[label] = sorted(sl for sl in ("o0.row", "o3.row") if sl in ag._want_scope)
out["mirror"] = mirror
# (d) the reviewer 12:12 CDT: linked before anything is read, the want must MOVE when o0.row
# then reads as moving -- one want, the release counted
ag.agency = type(ag.agency)()
for sl in ("o0.row", "o3.row"):
    ag.wants.pop(sl, None)
    ag._want_terms.pop(sl, None)
    ag._want_scope.pop(sl, None)
ag._goal_links.clear()
ag._goal_conds["mirror-d"] = m
ag._link_goal("mirror-d", m)
first = sorted(sl for sl in ("o0.row", "o3.row") if sl in ag.wants)
unl0 = ag.gamma.book.get("goal_unlinked", 0)
ag.agency.note("A", {"o0.row"}, sorted(ag.slots))
ag.agency.note("B", set(), sorted(ag.slots))
ag._respell_goals()
ag._respell_goals()                  # the reading did not change: no second move, no row
rows = [r for r in ag.led.rows() if r["event"] == "goal_respelled"]
out["respell"] = [first, sorted(sl for sl in ("o0.row", "o3.row") if sl in ag.wants),
                  ag.gamma.book.get("goal_unlinked", 0) - unl0, len(rows)]
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
    assert off["linked"] and off["wanting"] == ["o3.row"], off
    print(f"  OFF: no `below`; '<' runs above on {off['slot']} with operand {off['operand']}; "
          f"the linked want lands on {off['wanting']}")
    assert off["mirror"] == {"none": ["o3.row"], "o0": ["o3.row"], "o3": ["o3.row"]}, off
    print("  OFF mirror 'o3.row > o0.row': the want stays on o3.row whatever moves")
    assert off["respell"] == [["o3.row"], ["o3.row"], 0, 0], off
    print("  OFF (d): linked on o3.row, o0.row then moves -- it stays on o3.row")
    on = _run(True)
    assert on["below"], on
    assert on["slot"] == "o0.row" and on["operand"] == "o3.row" and on["chain"] == ["below"], on
    assert on["values"] == [1, 0, 0], on
    assert on["colour"] == "Refusal", on
    assert on["linked"] and on["wanting"] == ["o0.row"], on
    print(f"  ON: '<' runs below on {on['slot']} with operand {on['operand']}; values "
          f"{on['values']}; colour '<' refused; the linked want lands on {on['wanting']} (F1)")
    # BOTH SPELLINGS: the movable party, by the agent's own contingency reading; none moving
    # keeps the written spelling (the must-fail: the pick is the reading, not the order)
    assert on["mirror"] == {"none": ["o3.row"], "o0": ["o0.row"], "o3": ["o3.row"]}, on
    print(f"  ON mirror 'o3.row > o0.row' (both spellings): {on['mirror']}")
    assert on["respell"] == [["o3.row"], ["o0.row"], 1, 1], on       # one move, one row
    print("  ON (d): linked on o3.row before anything is read; o0.row then moves -> the one "
          "want is on o0.row, the release counted once")
    print("relation below: OK")
