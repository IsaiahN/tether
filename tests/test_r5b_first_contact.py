"""R5b (the reviewer 2026-11-06 r1321, r1322): no bind, pull or install on a slot the world's own
clock writes ((B), TETHER_OWN_COUNTERS_DERIVED), at ANY site. R5 closed the per-slot route; the
carry sweep is closed by construction (it sweeps parked mint records, and ACCEPT never mints an own
slot); first_contact (PERCEIVE) had no such filter. It now reads env.own_counted() at its own site
-- it runs before the step's _charge, so self._own_now there is the last step's, empty on a
level's first step. About a minute (the su15 run is 8 cycles, offline).

MF-R5b    a fresh gridworld agent, a carried kind planted as settled on two slots' forms, one of
          them own-counted through env.own_counted() (never by writing _own_now), on the level's
          FIRST step (_own_now empty): no first_contact bind on the own slot, and the skip is
          booked (first_contact_own_askings, per asking). RED at 02bc3f0.
CONTROL   the uncounted slot with the same plant still binds by first_contact
CONTROL   TETHER_OWN_COUNTERS_DERIVED off: the own slot binds as before (the filter is (B)'s)
INVARIANT su15, 8 cycles: no first_contact / pull / reuse_install / rebind row on an own slot
          (arc_world.own_counted: an object's age and stability); the occasions per row kind
          printed, a kind with none printed "unwitnessed", never as a pass

    python tests/test_r5b_first_contact.py
"""
from __future__ import annotations

import collections
import json
import os
import sys
import tempfile

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402
from gamma import Gamma  # noqa: E402


def _fresh() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="r5b_fixture"), tether.Config(),
                        ledger.Ledger())


def _planted_first_step(own_on: bool) -> tuple:
    probe = _fresh()
    probe.step()
    slots = sorted(s for s in probe.slots if not s.startswith("@"))
    own, ctl = slots[0], slots[1]
    kind = next(n for n, t in probe.gamma.library.items() if not t.operand and n != tether.IDN)
    ag = _fresh()
    assert ag.cycle == 0 and not ag._own_now, "precondition: the level's first step, set empty"
    ag.gamma.settled_forms[kind] = {Gamma.unbound_form(own), Gamma.unbound_form(ctl)}
    ag.gamma.carried[kind] = {}
    ag.env.own_counted = lambda: frozenset({own})
    keep = tether._OWN_COUNTERS_DERIVED
    tether._OWN_COUNTERS_DERIVED = own_on
    try:
        ag.step()
    finally:
        tether._OWN_COUNTERS_DERIVED = keep
    fc = {r["slot"] for r in ag.led.rows() if r["event"] == "first_contact"}
    return own, ctl, fc, ag.gamma.book.get("first_contact_own_askings", 0)


def check_first_contact() -> None:
    own, ctl, fc, booked = _planted_first_step(True)
    assert own not in fc, ("MF-R5b: first_contact bound an own-counted slot", own)
    assert booked >= 1, ("MF-R5b: the skip was not booked", booked)
    assert ctl in fc, ("CONTROL: the uncounted slot did not bind", sorted(fc)[:6])
    own0, _c, fc0, _b = _planted_first_step(False)
    assert own0 in fc0, ("CONTROL: (B) off, the own slot should bind as before", own0)
    print(f"  MF-R5b {own}: not bound at first contact on the first step (booked {booked});"
          f" CONTROL {ctl} bound; (B) off: {own0} bound")


def check_invariant_su15() -> None:
    import arc_holdout
    with tempfile.TemporaryDirectory() as d:
        led = os.path.join(d, "su15.jsonl")
        arc_holdout.play("su15", 8, led_path=led)
        if not os.path.exists(led):     # the game is not fetched here: say so, never a pass
            print("  INVARIANT su15: UNWITNESSED here (game not fetched)")
            return
        with open(led, encoding="utf-8") as fh:
            rows = [json.loads(x) for x in fh]
    if not rows:
        print("  INVARIANT su15: UNWITNESSED here (an empty ledger)")
        return
    kinds = ("first_contact", "pull", "reuse_install", "rebind")
    occ = collections.Counter(r["event"] for r in rows if r["event"] in kinds)
    bad = [(r["cycle"], r["event"], r["slot"]) for r in rows if r["event"] in kinds
           and r["slot"].rsplit(".", 1)[-1] in ("age", "stability")]
    assert not bad, ("INVARIANT: a bind on an own-counted slot", bad[:6])
    print("  INVARIANT su15 8 cycles, rows on own slots 0; occasions:",
          {k: occ[k] if occ[k] else "unwitnessed" for k in kinds})


def main() -> int:
    for c in (check_first_contact, check_invariant_su15):
        c()
    print("test_r5b_first_contact OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
