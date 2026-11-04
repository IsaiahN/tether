"""TRANSLATE IS AFFINE (TETHER_TRANSLATE_AFFINE; the reviewer 2026-11-04 r1103). `translate` ("v +
operand", SAME_AS_TARGET) declared accepts ['val'] only, so it could never bind at a POSITION slot,
though its own warrant is "a position plus its own displacement" (arc_atoms.py:882). Under the arm a
POSITION target takes a DELTA operand ONLY (gamma.TARGET_OPERAND, declared by arc_predict, off the
Atom); a point plus a point is refused for typing with its reason. Seconds: a gridworld agent with
its slot types set by hand, and ARC's translate.

MF-T1  translate<o0.drow> binds at o0.row: the head accepts POSITION and the operand fits
MF-T2  translate<o1.row> at o0.row is REFUSED (point + point), and the reason is recorded
MF-T3  every other target keeps today's rule: the 'val' head check and the operand check at
       non-POSITION targets read the same with the arm on and off (> 0 cases)
The red is behavioural, the arm OFF on this tree: TETHER_TRANSLATE_AFFINE=0 fails MF-T1 at the head.

    python tests/test_translate_affine.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_predict  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402
from gamma import Term  # noqa: E402

TYPES = {"o0.row": "POSITION", "o1.row": "POSITION", "o0.drow": "DELTA", "o0.colour": "COLOUR",
         "o0.h": "EXTENT", "o0.add_row": "add_row"}


def agent():
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    ag.slot_types = {**ag.slot_types, **TYPES}
    return ag


def main():
    tr = next(a for a in arc_predict.predict() if a.name == "translate")
    cand = Term((tr,), operand="o0.drow")
    ag = agent()
    head, fits = tether._head_accepts(cand, "POSITION"), ag._operand_fits(cand, "o0.row", "o0.drow")
    assert head and fits, ("MF-T1: translate<o0.drow> does not bind at o0.row", head, fits)
    bad = ag._operand_fits(Term((tr,), operand="o1.row"), "o0.row", "o1.row")
    why = dict(ag.__dict__.get("_affine_refused") or {})
    assert not bad and any("POSITION + POSITION" in k for k in why), ("MF-T2", bad, why)
    cases = [(t, b) for t in ("o0.colour", "o0.h", "o0.add_row") for b in ("o0.drow", "o1.row",
                                                                             "o0.h", None)]
    on = [(tether._head_accepts(cand, TYPES[t]), ag._operand_fits(cand, t, b)) for t, b in cases]
    was = gamma._TRANSLATE_AFFINE
    try:
        gamma._TRANSLATE_AFFINE = False
        off = [(tether._head_accepts(cand, TYPES[t]), agent()._operand_fits(cand, t, b))
               for t, b in cases]
        val_off = tether._head_accepts(cand, "val")
    finally:
        gamma._TRANSLATE_AFFINE = was
    moved = [c for c, a, b in zip(cases, on, off, strict=True) if a != b]
    assert len(cases) > 0 and on == off and val_off and tether._head_accepts(cand, "val"), (
        "MF-T3: a non-POSITION target moved", moved)
    print(f"  MF-T1 translate<o0.drow> at o0.row: head {head}, operand fits {fits}")
    print(f"  MF-T2 translate<o1.row> at o0.row refused: {why}")
    print(f"  MF-T3 {len(cases)} non-POSITION (target, operand) cases read the same on and off; "
          f"'val' accepted both ways")
    print("test_translate_affine OK")


if __name__ == "__main__":
    main()
