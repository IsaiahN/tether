"""THE TWO-SLOT OPERAND (TETHER_TWO_SLOT_OPERAND; the reviewer 2026-11-04 r1145; Fig 12 :46 "A bond
is the typed relation between two operands"). An operand tree read ONE slot (operands=(value,)),
so a settled junction between two pair offsets (o.dcol_ox -> o.dcol_oy) had no term at the mover.
Now a tree whose own term names a second slot reads it: translate<subtract<x>(y)> computes y − x
and adds it at the one source that moved. Seeded from the settled junction only; never enumerated.
Seconds: a synthetic window (o1 moves in col; o2, o3 stay), forced verdicts, no game.

MF-W1  the settled junction o1.dcol_o2 -> o1.dcol_o3 (both termless) is offered at the mover o1.col
       as translate<subtract<o1.dcol_o2>(o1.dcol_o3)>; _trees builds it; _ops reads 7 − 5 = 2, so
       the predicted o1.col is col + 2 on every frame; the row counts {offered 1}
MF-W2  an untyped pair (POSITION − COLOUR) is refused with its reason, nothing offered
MF-W3  the node's price is reported and exceeds the single-slot operand's
MF-W4  with no settled junction nothing is offered (seeded, not enumerated)
The red is behavioural, the arm OFF on this tree: TETHER_TWO_SLOT_OPERAND=0 fails MF-W1.

    python tests/test_two_slot.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_predict  # noqa: E402
import composer  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import test_molecule_apply as tm  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402
from gamma import Ctx, Term  # noqa: E402

LIT = "ZZZ|Gap"
X, Y, M = "o1.dcol_o2", "o1.dcol_o3", "o1.col"
FR = [{M: c, "o2.col": 5, "o3.col": 7, X: 5 - c, Y: 7 - c, "o9.x": 0} for c in range(5)]
TYPES = {M: "POSITION", "o2.col": "POSITION", "o3.col": "POSITION", X: "DELTA", Y: "DELTA"}


def run(per_object, types=None):
    held = {a.name: a for a in arc_predict.predict()}
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma([*env.atoms(), held["translate"], held["subtract"]],
                                       game="fam_default_0"), tether.Config(), led)
    ag.step()
    keep = (composer.candidates, composer.recipe_rows, tether._mol_junctions,
            tether.Agent.__dict__["_per_object"])
    try:
        composer.candidates = lambda *_a, **_k: []
        composer.recipe_rows = lambda: {}
        tether._mol_junctions = lambda: {LIT: 2}
        tether.Agent._per_object = staticmethod(per_object)
        ag.trace = [(FR[t], "ACTION1", FR[t + 1]) for t in range(4)]
        ag._window_at, ag._mol_key = 0, None
        ag.slot_types = {**ag.slot_types, **(types or TYPES)}
        ag.bound = {}
        ag._lookup_pairs = {Y: [{"molecule": LIT, "left": "a", "right": "b", "left_reading": X,
                                 "right_reading": Y, "held": ["→"], "via": [], "occasions": {}}]}
        ag._molecule_pass()
    finally:
        (composer.candidates, composer.recipe_rows, tether._mol_junctions,
         tether.Agent._per_object) = keep
    row = [r.get("detail", r) for r in led.rows() if r.get("event") == "molecule_apply"][-1]
    return ag, held, row


def main():
    ag, held, row = run(tm.only({"→"}))
    tr = held["translate"]
    offers = [o_ for o_ in ag._mol_offers.get(M, ()) if o_["prov"].get("two_slot") == [Y, X]]
    trees = [t for t in ag._trees(Term((tr,)), Y, None, M)
             if t.operand_term is not None and t.operand_term.operand == X]
    assert len(offers) == 1 and trees and row.get("two_slot") == {"offered": 1}, (
        "MF-W1: the settled pair junction is not offered at the mover",
        ag._mol_offers.get(M), row.get("two_slot"), row.get("not_offered"))
    tree = trees[0]
    preds = [tr.fn(f[M], Ctx(operands=ag._ops(tree, f))) for f in FR]
    assert preds == [f[M] + 2 for f in FR], ("MF-W1: the prediction", preds)
    print(f"  MF-W1 {tree.name} at {M}: _ops {ag._ops(tree, FR[0])}, predicted {preds}; "
          f"row two_slot {row['two_slot']}")
    _ag, _h, row2 = run(tm.only({"→"}), {**TYPES, Y: "POSITION", X: "COLOUR"})
    assert row2.get("two_slot") == {"POSITION − COLOUR is not defined": 1} and not [
        o_ for o_ in _ag._mol_offers.get(M, ()) if o_["prov"].get("two_slot")], ("MF-W2", row2)
    print(f"  MF-W2 refused: {row2['two_slot']}")
    b_tree = ag._bind_bits(tree, M)
    b_one = ag._bind_bits(Term((tr,), operand=Y), M)
    assert b_tree > b_one, ("MF-W3", b_tree, b_one)
    print(f"  MF-W3 bind bits: the node {b_tree:.3f} > a single-slot operand {b_one:.3f}")
    ag4, _h4, row4 = run(tm.only(set()))
    assert not [o_ for o_ in ag4._mol_offers.get(M, ()) if o_["prov"].get("two_slot")] \
        and "two_slot" not in row4, ("MF-W4", row4.get("two_slot"))
    print("  MF-W4 no settled junction: nothing offered, no two_slot count")
    print("test_two_slot OK")


if __name__ == "__main__":
    main()
