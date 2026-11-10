"""THE COVER'S CHAIN TYPING AS A UNION (TETHER_COVER_CHAIN_TYPED; the reviewer 2026-11-04 r1169).
A cover chain is refused only if NO stream the mint would walk at its slot types it: the val stream
(val -> val), or any walk from the slot's own type (the OBJ stream, closed with `all`, and the
widened streams). Seconds: test_lit_cover's fixture, the slot o1.z typed EXTENT, the molecule's
ingredients and their slots' terms chosen per case.

MF-K1  inc . above . above at o1.z: above takes EXTENT and gives PRED, so no stream can walk the
       second above -- refused at the cover and counted, nothing offered
MF-K2  the union keeps what only the slot's own stream types: above . all (EXTENT -> PRED -> OBJ)
       at an EXTENT slot is accepted; with no slot type (the val stream alone) it is refused. On
       this fixture's atoms no 3-leaf cover chain is typed by the OBJ stream alone (val -> val,
       EXTENT -> PRED, PRED -> OBJ: nothing takes OBJ), so K2 asks the predicate the cover asks
The red is behavioural, the arm OFF on this tree: TETHER_COVER_CHAIN_TYPED=0 fails MF-K1.

    python tests/test_cover_chain_typed.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import composer  # noqa: E402
import gamma  # noqa: E402
import test_lit_cover as tl  # noqa: E402
import test_molecule_apply as tm  # noqa: E402

AGENT = tm.agent


def run(mid: str, last: str):
    def agent():
        ag, led = AGENT()
        real = ag._molecule_pass

        def mp(*a, **k):
            ag.bound.update({"o1.col": mid, "o1.z": last})
            ag.slot_types = {**ag.slot_types, "o1.z": "EXTENT"}
            return real(*a, **k)
        ag._molecule_pass = mp
        return ag, led
    node = composer.Bonded(composer.UNKNOWN, composer.Bonded(composer.UNKNOWN, "inc", mid), last)
    tm.agent = agent
    try:
        order, row = tl.run(node, tm.only({"→"}))
    finally:
        tm.agent = AGENT
    return [p for p in order if p.get("lit")], row


def main():
    lit, row = run("above", "above")
    why = {k: v for k, v in row["not_offered"].items() if k.startswith("cover: no stream types")}
    assert not lit and why and row["lit_cover"].get("refused for chain typing"), (
        "MF-K1: the cover offers a chain no stream can type", lit, row["not_offered"])
    print(f"  MF-K1 refused at the cover: {why}")
    ag, _l = AGENT()
    atoms = {a.name: a for a in ag.gamma.atoms}
    chain = gamma.Term((atoms["above"], atoms["all"]))
    ag.slot_types = {**ag.slot_types, "o1.z": "EXTENT"}
    kept = ag._chain_streams(chain, "o1.z")
    ag.slot_types = {k: v for k, v in ag.slot_types.items() if k != "o1.z"}
    val_only = ag._chain_streams(chain, "o1.z")
    assert kept and not val_only, ("MF-K2: the union drops what only the slot's own stream types",
                                   kept, val_only)
    print("  MF-K2 above . all at an EXTENT slot: kept by the slot's own stream; the val stream "
          "alone would refuse it")
    print("test_cover_chain_typed OK")


if __name__ == "__main__":
    main()
