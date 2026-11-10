"""THE LATE ROUND HONOURS A DECLARED HEAD (TETHER_LATE_DECLARED; the reviewer 2026-11-04 r1121). L3
defers a head that does not accept the slot type to `_library_fit`'s late round, where the head
check is skipped -- right for a head whose typing is not known. `translate` DECLARES its typing
(gamma.TARGET_OPERAND), and on ls20 25 of 26 late closures were translate at add_row, rem_n, shape,
... So a declared head that does not accept the slot is refused with its reason, never walked late.
Seconds: the L3 fixture of tests/test_limbs.py, a stepped gridworld agent holding ARC's translate.

MF-D1  translate<x> at a slot typed add_n: OFF it is deferred and closes late (typed_late closed 1);
       ON it is refused, tallied "declared head: translate takes no add_n", and nothing is pulled
MF-D2  an UNDECLARED mismatched head still closes late with the arm ON (L3 kept)
MF-D3  translate<x> at a POSITION slot (declared, accepted) closes in the typed round, both ways
The red is behavioural, the arm OFF on this tree: TETHER_LATE_DECLARED=0 fails MF-D1.

    python tests/test_late_declared.py
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

TR = next(a for a in arc_predict.predict() if a.name == "translate")


def lookup(stype: str, head=TR) -> tuple:
    """`_library_fit` at one slot typed `stype`, holding one term headed by `head` that closes it.
    Returns the pull, the typed_late rows, and the refusal tally."""
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma([*env.atoms(), TR], game="late_declared_fixture"),
                      tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    slot = next(s for s in sorted(ag.slots) if ag.history(s))
    other = next(s for s in sorted(ag.slots) if s != slot)
    ag.slot_types = {**ag.slot_types, slot: stype, other: "DELTA"}
    ag.bound.pop(slot, None)
    term = ag.gamma.accept(Term((head,), operand=other), seq=0, residual="fixture")
    held = ag.gamma.library[tether.IDN]
    ag._left = lambda t, _s, _h, **_k: 0.0 if t is term else 5.0 if t is held else 10.0
    ag._bits = lambda _x: 1.0
    ag._units_for = lambda _s: ()
    ag._rebindings = lambda t, _s, _g=None, _r=None: iter([t])
    ag._take_pull = lambda n, _cand, _slot, **_k: n
    ag._carry_credit = lambda *_a: False
    ag._think_or_act = lambda _s, **_k: (True, "ok")
    keep = (tether._may_bind, tether.retrieval.retrieve)
    try:
        tether._may_bind = lambda _c, _t: True
        tether.retrieval.retrieve = lambda *_a, **_k: iter([term.name])
        n0 = len(ag.led.rows())
        before = dict(ag.__dict__.get("_late_refused") or {})   # stepping refuses too (EXTENT)
        got = ag._library_fit(slot, None)
    finally:
        tether._may_bind, tether.retrieval.retrieve = keep
    late = [r["detail"] for r in ag.led.rows()[n0:] if r.get("event") == "typed_late"]
    now = dict(ag.__dict__.get("_late_refused") or {})
    return got, term.name, late, {k: v - before.get(k, 0) for k, v in now.items()
                                  if v != before.get(k, 0)}


def both(stype: str, head=TR) -> dict:
    """{False: the arm forced OFF, True: the arm as loaded} -- so TETHER_LATE_DECLARED=0 is red."""
    was = tether._LATE_DECLARED
    out = {}
    try:
        for key, flag in ((False, False), (True, was)):
            tether._LATE_DECLARED = flag
            out[key] = lookup(stype, head)
    finally:
        tether._LATE_DECLARED = was
    return out


def main():
    r = both("add_n")
    got_off, name, late_off, _ = r[False]
    assert got_off == name and late_off and late_off[0]["closed"] == 1, (
        "MF-D1 premise: OFF, translate at add_n does not close late", r[False])
    got_on, _n, late_on, why = r[True]
    assert got_on is None and not late_on and why == {
        "declared head: translate takes no add_n": 1}, (
        "MF-D1: translate at add_n is not refused with the arm ON", r[True])
    print(f"  MF-D1 translate at add_n: OFF closes late ({late_off[0]}); ON refused {why}")
    inc = next(a for a in gridworld.family("default", 0, 4).atoms() if a.name == "inc")
    u = both("add_n", inc)
    assert all(u[f][0] == u[f][1] and u[f][2] and u[f][2][0]["closed"] == 1 for f in u), (
        "MF-D2: an undeclared head no longer closes late", u)
    print(f"  MF-D2 undeclared inc at add_n closes late both ways: {u[True][2][0]}")
    p = both("POSITION")
    assert all(p[f][0] == p[f][1] and not p[f][2] for f in p), ("MF-D3", p)
    print("  MF-D3 translate at POSITION closes in the typed round both ways, no late round")
    print("test_late_declared OK")


if __name__ == "__main__":
    main()
