"""THE SEED FOLLOWS ITS OFFER (TETHER_SEED_LIFT; the reviewer 2026-11-04 r1126). r978's junction
seeds put a molecule's site first in the step's mint order, but they sat at DERIVED readings
(o10.dcol, o10.drow, ...) which are never routed, so on ls20 the 8c-lifted sources sat at
positions 3-17 and 24 of their 28 turns were deferred behind a shape slot. When 8c re-files an
offer at y to its source X, the seed now moves with it. Seconds: the 8c fixture
(tests/test_derived_lift.py) plus a seed.

MF-S1  the seed at o0.drow moves to o0.row (which has none) once, as filed; the two-source
       seed (o0.speed) stays, counted; lifted + left are the seeds at derived slots (> 0)
MF-S2  _seed_order walks o0.row FIRST though it was routed LAST; every other route keeps its order
MF-S3  (record only, r1121 (4)) a step's mint at the offer slot is read into the flush's outcome
The red is behavioural, the arm OFF on this tree: TETHER_SEED_LIFT=0 fails MF-S1 (the seed stays).

    python tests/test_seed_lift.py
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

DERIVED = {"o0.drow": ("o0.row",), "o0.speed": ("o0.row", "o0.col")}
TYPES = {"o0.row": "POSITION", "o0.col": "POSITION", "o0.drow": "DELTA", "o0.speed": "DELTA",
         "o0.dcol_o1": "DELTA"}


def main():
    env = world.bind(gridworld.family("default", 0))
    tr = next(a for a in arc_predict.predict() if a.name == "translate")
    ag = tether.Agent(env, gamma.Gamma([*env.atoms(), tr], game="fam_default_0"),
                      tether.Config(), ledger.Ledger())
    ag.step()
    ag.slot_types = {**ag.slot_types, **TYPES}
    ag.env.derived = lambda: DERIVED
    inc = next(a for a in ag.gamma.atoms if a.name == "inc")
    prov = {"molecule": "M", "bond": "→", "object": "o0", "seen": True, "left": "o0.dcol_o1",
            "leaves": [], "occasions": 3, "junctions": 1, "source": "lookup", "entries": 1}
    ag._mol_offers = {y: [{"term": Term((inc,)), "operand": "o0.dcol_o1", "offered": True,
                           "why": "molecule", "prov": {**prov, "right": y, "offer": "inc"}}]
                      for y in DERIVED}
    ag._mint_seeds = {"o0.drow": {"o0.dcol_o1": False, "o0.col": True},   # o0.row has none
                      "o0.speed": {"o0.dcol_o1": True}}
    ag._lift_branches, ag._lift_n = {}, collections.Counter()
    ag._lift_derived()
    seeds, n = dict(ag._mint_seeds), dict(ag._lift_n)
    assert "o0.drow" not in seeds and seeds.get("o0.row") == {"o0.dcol_o1": False, "o0.col": True} \
        and "o0.speed" in seeds, ("MF-S1: the drow seed did not follow its offer to o0.row", seeds)
    assert n.get("seed lifted") == 1 and n.get("seed left at a derived slot") == 1, ("MF-S1", n)
    print(f"  MF-S1 seed o0.drow -> o0.row {seeds['o0.row']}; counts {n}")
    w = ag._window_at if tether._BREAK_WINDOW else 0
    ag._mol_key = (id(ag.trace), w, len(ag.trace))          # the pass above is this window's
    ag._contact_slots = ()
    routed = [(s, tether.MECHANISM, None, "") for s in ("o0.col", "o0.colour", "o0.row")]
    out = ag._seed_order(routed)
    rest = [r[0] for r in out if r[0] != "o0.row"]
    assert out[0][0] == "o0.row" and rest == ["o0.col", "o0.colour"], (
        "MF-S2: o0.row is not walked first", [r[0] for r in out])
    print(f"  MF-S2 routed {[r[0] for r in routed]} -> walked {[r[0] for r in out]}")
    ag._sm = {"run": 0, "deferred": [], "stop": "o0.colour"}   # a mint this step hit its bound
    ag._mint_at("o0.row", tether.MECHANISM)
    got = ag._mol_flush().get("outcome")
    assert got == {"o0.row": "mint_deferred"}, ("MF-S3: the flush has no outcome", got)
    print(f"  MF-S3 flush outcome {got}")
    print("test_seed_lift OK")


if __name__ == "__main__":
    main()
