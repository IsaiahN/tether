"""− IS SUBTRACTION, WIRED AS AN ATOM (TETHER_SUBTRACT; the reviewer 2026-11-04 r1141, r1142; Isaiah
15:31). `subtract` is v − operand, "A with B removed or absent" (Operators Table :41-46), never ¬;
typed per target like translate: a point less a displacement is a point, a displacement less a
displacement is a displacement, a point less a point is refused at a POSITION target. Seconds: a
gridworld agent with its slot types set by hand, and ARC's subtract and translate.

MF-S1  subtract is held with the arm on; subtract<o0.drow> at o0.row: the head accepts POSITION, the
       operand fits, and 5 less 2 is 3
MF-S2  subtract<o1.row> at o0.row is REFUSED (point − point at a POSITION target), with its reason
MF-S3  subtract<o0.dcol> at o0.drow (DELTA − DELTA) fits
MF-S4  (r1052) priced the same way translate's term is: equal bind bits for subtract<x> and
       translate<x> at o0.row, and a molecule offer of subtract reaches pays (a molecule_offer row)
The red is behavioural, the arm OFF on this tree: TETHER_SUBTRACT=0 fails MF-S1 (no atom).

    python tests/test_subtract.py
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
from gamma import Ctx, Term  # noqa: E402

TYPES = {"o0.row": "POSITION", "o1.row": "POSITION", "o0.drow": "DELTA", "o0.dcol": "DELTA"}


def main():
    held = {a.name: a for a in arc_predict.predict()}
    assert "subtract" in held, ("MF-S1: no subtract atom", sorted(held))
    sub, tr = held["subtract"], held["translate"]
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma([*env.atoms(), sub, tr], game="fam_default_0"),
                      tether.Config(), ledger.Ledger())
    ag.slot_types = {**ag.slot_types, **TYPES}
    cand = Term((sub,), operand="o0.drow")
    head, fits = tether._head_accepts(cand, "POSITION"), ag._operand_fits(cand, "o0.row", "o0.drow")
    val = sub.fn(5, Ctx(operands=(2,)))
    assert head and fits and val == 3, ("MF-S1", head, fits, val)
    bad = ag._operand_fits(Term((sub,), operand="o1.row"), "o0.row", "o1.row")
    why = dict(ag.__dict__.get("_affine_refused") or {})
    assert not bad and any("POSITION − POSITION" in k for k in why), ("MF-S2", bad, why)
    dd = Term((sub,), operand="o0.dcol")
    assert tether._head_accepts(dd, "DELTA") and ag._operand_fits(dd, "o0.drow", "o0.dcol"), "MF-S3"
    # another object's delta (an own delta binds free, 0 bits, and would compare nothing)
    b_sub = ag._bind_bits(Term((sub,), operand="o1.drow"), "o0.row")
    b_tr = ag._bind_bits(Term((tr,), operand="o1.drow"), "o0.row")
    code = ag.gamma.code()
    c_sub, c_tr = (code.bits((Term((a,)), ()))[0] for a in (sub, tr))
    assert b_sub == b_tr > 0 and c_sub == c_tr > 0, (
        "MF-S4: not priced as translate is", b_sub, b_tr, c_sub, c_tr)
    prov = {"molecule": "M", "bond": "−", "object": "o0", "seen": True, "left": "o0.drow",
            "right": "o0.row", "leaves": ["o0.drow", "o0.row"], "occasions": 2, "junctions": 1,
            "source": "lookup", "offer": "subtract", "entries": 1}
    ag._mol_names = {"o0.row": {Term((sub,)).name: prov}}
    ag._mol_paid = {}
    ag._pays_ev("o0.row", Term((sub,), operand="o0.drow"), 1.0, 0.5, 4.0)
    mo = [r for r in ag.led.rows() if r["event"] == "molecule_offer"]
    assert len(mo) == 1 and mo[0]["detail"]["pays"] is True, ("MF-S4: no molecule_offer", mo)
    print(f"  MF-S1 subtract<o0.drow> at o0.row: head {head}, operand fits {fits}, "
          f"5 less 2 = {val}")
    print(f"  MF-S2 subtract<o1.row> at o0.row refused: {why}")
    print("  MF-S3 subtract<o0.dcol> at o0.drow (DELTA − DELTA) fits")
    print(f"  MF-S4 bind bits subtract {b_sub:.3f} == translate {b_tr:.3f}; code bits "
          f"{c_sub:.3f} == {c_tr:.3f}; molecule_offer pays True")
    print("test_subtract OK")


if __name__ == "__main__":
    main()
