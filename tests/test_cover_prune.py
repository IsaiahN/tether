"""THE COVER'S PRODUCT PRUNED BY TYPING (TETHER_COVER_PRUNE; the reviewer 2026-11-04 r1178). The
r1176 probe: 3,598,710 cover paths built and then refused by the chain typing. A stream's walk is
prefix-closed, so the cover now walks its leaves depth-first in the product's own order and drops a
prefix the moment no stream can walk it. Seconds: test_lit_cover's fixture, two slots per leaf (no
slot shared between leaves, so the full product's tallies are exact), the pruned walk against the
full product (the arm forced OFF in the same process).

MF-P1  inc . dec . above (no stream types it: inc takes val only, above does not take val): both
       walks offer nothing and refuse the same 8 paths under the same reasons; the pruned walk
       builds none of them (lit_cover pruned 8)
MF-P2  inc . dec . neg (typed by the val stream): the same offers in the same order both ways, and
       nothing pruned
The red is behavioural, the arm OFF on this tree: TETHER_COVER_PRUNE=0 fails MF-P1 (pruned 0).

    python tests/test_cover_prune.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import composer  # noqa: E402
import test_lit_cover as tl  # noqa: E402
import test_molecule_apply as tm  # noqa: E402
import tether  # noqa: E402

AGENT = tm.agent


def run(mid: str, last: str, prune: bool):
    def agent():
        ag, led = AGENT()
        real = ag._molecule_pass

        def mp(*a, **k):
            ag.bound.update({"o1.row": "inc", "o1.w": "inc", "o1.col": mid, "o1.h": mid,
                             "o1.z": last, "o1.y": last})
            ag.slot_types = {**ag.slot_types, "o1.z": "EXTENT", "o1.y": "EXTENT"}
            return real(*a, **k)
        ag._molecule_pass = mp
        return ag, led
    node = composer.Bonded(composer.UNKNOWN, composer.Bonded(composer.UNKNOWN, "inc", mid), last)
    keep = tether._COVER_PRUNE
    tm.agent = agent
    try:
        tether._COVER_PRUNE = prune and keep
        order, row = tl.run(node, tm.only({"→"}))
    finally:
        tm.agent, tether._COVER_PRUNE = AGENT, keep
    lit = [(p["offer"], p["left"], p["right"]) for p in order if p.get("lit")]
    refused = {k: v for k, v in row["not_offered"].items() if k.startswith("cover:")}
    return lit, refused, row.get("lit_cover", {})


def main():
    on, off = run("dec", "above", True), run("dec", "above", False)
    assert on[0] == off[0] == [] and on[1] == off[1] and sum(off[1].values()) == 8 and \
        on[2].get("pruned") == 8, ("MF-P1: the pruned walk is not the full product's, or did "
                                   "not prune", on, off)
    print(f"  MF-P1 refused both ways {on[1]}; pruned {on[2].get('pruned')} of them unbuilt")
    on2, off2 = run("dec", "neg", True), run("dec", "neg", False)
    assert on2[0] == off2[0] and on2[0] and on2[1] == off2[1] and not on2[2].get("pruned"), (
        "MF-P2: the survivors differ", on2, off2)
    print(f"  MF-P2 the same {len(on2[0])} offers in the same order, nothing pruned")
    print("test_cover_prune OK")


if __name__ == "__main__":
    main()
