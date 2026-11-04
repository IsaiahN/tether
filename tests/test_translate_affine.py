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
MF-T4  (r1108) a TARGET_OPERAND row on a TEMPLATE atom enters compile_term.signature, so compiles
       made with the arm on and off cannot share a key: with a row declared on `above` (inside the
       test, restored after) the signature differs ON vs OFF, and with none it is today's tuple;
       and, asserted as the observed fact (no closure cache exists), enumerate_closure at a
       POSITION input starts a translate chain with the arm ON and none OFF. RED: the signature
       without the rows (52a642e) reads the same ON and OFF
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
    t4()
    print("test_translate_affine OK")


def t4():
    import compile_term
    env = world.bind(gridworld.family("default", 0))
    tr = next(a for a in arc_predict.predict() if a.name == "translate")
    g = gamma.Gamma([*env.atoms(), tr], game="fam_default_0")
    atoms = {a.name: a for a in g.atoms}
    above = atoms["above"]
    plain = compile_term.signature(atoms)
    was, had = gamma._TRANSLATE_AFFINE, above.fn in gamma.TARGET_OPERAND
    try:
        gamma.TARGET_OPERAND.setdefault(above.fn, {})["EXTENT"] = "DELTA"
        gamma._TRANSLATE_AFFINE = True
        s_on = compile_term.signature(atoms)
        gamma._TRANSLATE_AFFINE = False
        s_off = compile_term.signature(atoms)
    finally:
        gamma._TRANSLATE_AFFINE = was
        if had:
            gamma.TARGET_OPERAND[above.fn].pop("EXTENT", None)
        else:
            gamma.TARGET_OPERAND.pop(above.fn, None)
    assert s_on != s_off and s_off == plain and compile_term.signature(atoms) == plain, (
        "MF-T4: a template atom's TARGET_OPERAND row does not enter the signature", s_on == s_off)
    starts = {}
    try:
        for flag in (False, True):
            gamma._TRANSLATE_AFFINE = flag
            starts[flag] = any(t.atoms[0] is tr for t in g.enumerate_closure(
                "POSITION", "POSITION", 1, 500))
    finally:
        gamma._TRANSLATE_AFFINE = was
    assert starts == {False: False, True: True}, ("MF-T4: closure at POSITION", starts)
    print(f"  MF-T4 a template row moves the signature (ON != OFF, OFF == today's); "
          f"closure at POSITION starts with translate: {starts}")
    t5(g, tr, atoms["inc"])


def t5(g, tr, inc):
    """MF-T5: a SETTLED unit headed by translate whose fold the walk refuses at POSITION
    (translate . inc: a POSITION into an atom taking 'val' only) is not a start. Before, the head
    check admitted it and enumerate_closure raised unpacking _iter_step's None (8c A/B, arm B)."""
    unit = Term((tr, inc))
    assert gamma.accepts_type(unit, "POSITION") and gamma.Gamma._iter_step(
        "POSITION", None, unit) is None, "MF-T5 premise: the head admits, the fold refuses"
    held = g.units()
    g.units = lambda: [*held, unit]
    try:
        got = [t.name for t in g.enumerate_closure("POSITION", "POSITION", 2, 500)]
    except TypeError as e:
        raise AssertionError(("MF-T5: enumerate_closure raised at a POSITION start", e)) from e
    finally:
        del g.units
    assert got and not any(n.startswith(unit.name) for n in got), ("MF-T5", unit.name, got[:5])
    print(f"  MF-T5 {unit.name} at POSITION: head admits, fold refuses, not a start "
          f"({len(got)} chains yielded, none from it)")


if __name__ == "__main__":
    main()
