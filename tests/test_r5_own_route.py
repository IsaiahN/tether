"""R5 (the reviewer 2026-11-06 r1317, r1319): a slot the world's own clock writes owes nothing ((B),
TETHER_OWN_COUNTERS_DERIVED: never charged in _charge, never minted at ACCEPT, skipped by the event
route), so the per-slot route no longer sends its miss to _defer_lookup or the library: before R5
item 25's chooser read its gain as 0 and deferred it "act" -- "owed, asked first next step" -- at
every asking (su15, 60 cycles: 1,471 such rows on 52 own-counted slots, none ever looked up).
A stepped gridworld agent, seed pinned; seconds.

MF-R5a  an own-counted slot with a live miss (out of its range, trace >= 2) under the chooser:
        no lookup_deferred row, no _defer_lookup call, not in _owed_q / owed_import; its ROUTE row
        is bin mechanism with the (B) reading; route hands back (slot, mechanism, None), the bin
        ACCEPT's own_counter_unminted skip reads (slot in _own_now and b in MECHANISM...)
CONTROL an uncounted slot with the same miss is still asked (_defer_lookup is called for it)
CONTROL a slot already owed (in _owed_q and owed_import) that becomes own-counted is closed with an
        owed_closed row naming (B), and leaves both
CONTROL an own-counted slot whose miss is IN its range still takes r674's hold (bin held,
        miss_grade in_range_hold, no own_counted reading): R5 changes only the asking branch

    python tests/test_r5_own_route.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="r5_fixture"), tether.Config(),
                      ledger.Ledger())
    for _ in range(3):
        ag.step()
    return ag


def _miss(slot: str) -> tether.SlotResidual:
    return tether.SlotResidual(slot, "x", 0, 10 ** 6, 1.0)    # far outside any range: no hold


def main() -> int:
    assert tether._THINK_CHOOSER and tether._STEP_ACT, "precondition: the chooser and governor"
    ag = _agent()
    assert len(ag.trace) >= 2, "precondition: past the NOVEL bin"
    slots = sorted(s for s in ag.slots if not s.startswith("@"))
    own, ctl, owed = slots[:3]
    held = next(s for s in slots[3:] if isinstance((ag._range.get(s) or (None,))[0], int)
                and s not in ag._miss_held)
    ag._own_now = frozenset({own, owed, held})
    ag._owed_q[owed] = (ag.cycle - 1, "o_prior")
    ag.owed_import.add(owed)
    asked: list = []
    real = ag._defer_lookup
    ag._defer_lookup = lambda s: asked.append(s) or real(s)
    ag._library_fit = lambda _s, _ex: None
    n0 = len(ag.led.rows())
    in_range = tether.SlotResidual(held, "x", 0, ag._range[held][0], 1.0)
    out = ag.route({own: _miss(own), ctl: _miss(ctl), owed: _miss(owed), held: in_range})
    rows = ag.led.rows()[n0:]
    deferred = [r for r in rows if r["event"] == "lookup_deferred" and r["slot"] == own]
    route = [r for r in rows if r["event"] == "route" and r["slot"] == own]
    assert not deferred and own not in asked, ("MF-R5a: deferred", deferred, asked)
    assert own not in ag._owed_q and own not in ag.owed_import, "MF-R5a: an own slot left owed"
    assert [r["detail"]["bin"] for r in route] == ["mechanism"], route
    assert "own_counted" in route[0]["detail"], route[0]["detail"]
    got = next(t for t in out if t[0] == own)
    assert got[1] == tether.MECHANISM and got[2] is None, got
    assert ctl in asked, ("CONTROL: the uncounted slot was not asked", asked)
    closed = [r for r in rows if r["event"] == "owed_closed" and owed in r["detail"]["unasked"]]
    assert closed and closed[0]["detail"]["how"] == "own_counted", ("CONTROL: closed", closed)
    assert owed not in ag._owed_q and owed not in ag.owed_import, "CONTROL: the old debt stayed"
    hr = [r["detail"] for r in rows if r["event"] == "route" and r["slot"] == held]
    assert [(d["bin"], d.get("miss_grade"), "own_counted" in d) for d in hr] == [
        ("held", "in_range_hold", False)], ("CONTROL: the in-range hold moved", hr)
    print(f"  MF-R5a {own}: no deferral, not owed, route bin mechanism with the (B) reading")
    print(f"  CONTROL {ctl} (uncounted) asked: {ctl in asked}")
    print(f"  CONTROL {owed} (owed, then own-counted): owed_closed how=own_counted")
    print(f"  CONTROL {held} (own-counted, an in-range miss): held, in_range_hold, as before R5")
    print("test_r5_own_route OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
