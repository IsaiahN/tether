"""BUILD 3 ITEM 8c, CUT C: A DERIVED SLOT'S OFFER LIFTED TO ITS SOURCE (TETHER_DERIVED_LIFT; the
reviewer 2026-11-04 r1100, r1103). Measured on ls20 (census18, the 8a A/B): every molecule offer sat
at a change reading (o.drow, o.dh, ...), a DERIVED slot never bet on (B2b), so none was typed or
priced (typed 0, reached_pays 0, every pass). Seconds: a gridworld agent holding ARC's translate,
slot types and the derived map set by hand, three offers filed as MOLECULE_APPLY files them.

MF-L1  (a) the drow offer is RE-FILED, never copied: it leaves o0.drow and sits once at o0.row as
       translate, with "lifted_from"; lifted + unlifted == offers at derived slots (> 0)
MF-L2  (d) o0.speed (two sources) and o0.dh (a SHAPE source no instrument accepts) stay where they
       are, each counted with its reason
MF-L3  _trees builds translate<chain(x)> at o0.row for the offered operand; _library_chains yields
       translate there with that operand; pays sees it, so a molecule_offer row is written
MF-L4  (b) the lifted tree's binding bits exceed the bare chain's alone (the operand tree is priced)
MF-L5  (c) B2b holds: the derived slot stays out of betting with the arm on
The red is behavioural, the arm OFF on this tree: TETHER_DERIVED_LIFT=0 fails MF-L1.

    python tests/test_derived_lift.py
"""
from __future__ import annotations

import collections
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

DERIVED = {"o0.drow": ("o0.row",), "o0.speed": ("o0.row", "o0.col"), "o0.dh": ("o0.shape",)}
TYPES = {"o0.row": "POSITION", "o0.col": "POSITION", "o0.drow": "DELTA", "o0.speed": "DELTA",
         "o0.dh": "EXTENT", "o0.shape": "SHAPE", "o0.dcol_o1": "DELTA"}


def agent():
    env = world.bind(gridworld.family("default", 0))
    tr = next(a for a in arc_predict.predict() if a.name == "translate")
    ag = tether.Agent(env, gamma.Gamma([*env.atoms(), tr], game="fam_default_0"),
                      tether.Config(), ledger.Ledger())
    ag.slot_types = {**ag.slot_types, **TYPES}
    ag.env.derived = lambda: DERIVED
    return ag, tr


def offer(chain, y):
    prov = {"molecule": "M", "bond": "→", "object": "o0", "seen": True, "left": "o0.dcol_o1",
            "right": y, "leaves": ["o0.dcol_o1", y], "occasions": 3, "junctions": 1,
            "source": "lookup", "offer": chain.name, "entries": 1}
    return {"term": chain, "operand": "o0.dcol_o1", "prov": prov, "offered": True,
            "why": "molecule"}


def main():
    ag, tr = agent()
    inc = next(a for a in ag.gamma.atoms if a.name == "inc")
    chain = Term((inc,))
    ag._mol_offers = {y: [offer(chain, y)] for y in DERIVED}
    ag._lift_branches, ag._lift_n = {}, collections.Counter()
    ag._lift_derived()
    at_row = ag._mol_offers.get("o0.row", [])
    assert "o0.drow" not in ag._mol_offers and len(at_row) == 1 \
        and at_row[0]["term"].atoms == (tr,) and at_row[0]["prov"]["lifted_from"] == "o0.drow", (
        "MF-L1: the drow offer is not re-filed once at o0.row", sorted(ag._mol_offers), at_row)
    n = dict(ag._lift_n)
    assert sum(n.values()) == len(DERIVED) > 0 and n.get("lifted") == 1, ("MF-L1 counts", n)
    reasons = sorted(k for k in n if k != "lifted")
    assert ag._mol_offers.get("o0.speed") and ag._mol_offers.get("o0.dh") and reasons == [
        "unlifted: no instrument from EXTENT to SHAPE", "unlifted: two or more sources"], (
        "MF-L2", sorted(ag._mol_offers), n)
    trees = ag._trees(Term((tr,)), "o0.dcol_o1", None, "o0.row")
    lifted = [t for t in trees if t.operand_term is not None and t.operand_term.name == chain.name]
    assert lifted, ("MF-L3: _trees builds no translate<chain(x)>", [t.name for t in trees])
    stats, ops = collections.Counter(), {}
    got = ag._library_chains("o0.row", "POSITION", "POSITION", stats, ops)
    assert any(c.atoms == (tr,) for c in got) and "o0.dcol_o1" in ops.get(Term((tr,)).name, ()), (
        "MF-L3: _library_chains does not yield translate with the operand", [c.name for c in got])
    ag._pays_ev("o0.row", lifted[0], 1.0, 0.5, 4.0)
    mo = [r for r in ag.led.rows() if r["event"] == "molecule_offer"]
    assert len(mo) == 1 and mo[0]["detail"]["term"] == lifted[0].name, ("MF-L3 pays", mo)
    flat = Term((tr,), operand="o0.dcol_o1")
    b_tree, b_flat = ag._bind_bits(lifted[0], "o0.row"), ag._bind_bits(flat, "o0.row")
    assert b_tree > b_flat, ("MF-L4: the operand tree is not priced", b_tree, b_flat)
    code = ag.gamma.code()          # r1108: the chain's own bits alone, as _bind_bits prices a tree
    b_chain = code.bits((Term(chain.atoms), ()))[0] - code.end
    assert b_tree > b_chain, ("MF-L4: the tree costs no more than the chain it carries", b_tree,
                              b_chain)
    lifted_left = [s for s in DERIVED for o_ in ag._mol_offers.get(s, ())
                   if "lifted_from" in o_["prov"]]
    assert not (set(DERIVED) & set(ag.bound)) and not lifted_left, (
        "MF-L5: a derived slot was bound or kept a lifted offer", sorted(ag.bound), lifted_left)
    print(f"  MF-L1 o0.drow re-filed at o0.row as {at_row[0]['prov']['offer']}; counts {n}")
    print(f"  MF-L2 stayed: o0.speed, o0.dh -- {reasons}")
    print(f"  MF-L3 _trees {lifted[0].name}; _library_chains yields translate with o0.dcol_o1; "
          f"molecule_offer row pays={mo[0]['detail']['pays']}")
    print(f"  MF-L4 bind bits: the lifted tree {b_tree:.3f} > flat translate<x> {b_flat:.3f}; "
          f"> the chain's own bits alone ({chain.name}(o0.dcol_o1)) {b_chain:.3f}")
    print("  MF-L5 no derived slot bound, no lifted offer left at one")
    print("test_derived_lift OK")


if __name__ == "__main__":
    main()
