"""G END, BASELINE_FROM_OTHERS (the reviewer 2026-11-01 r750 3), on the fake world: a board whose
first press changed little (so the every-press intersection is near empty) still ends an actuator
whose press changes only what touching OTHER objects changed; with the arm OFF the intersection
leaves that press a non-zero net change and nothing ends (the must-fail).

    python tests/test_baseline_from_others.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")


def main():
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    assert tether._BASELINE_FROM_OTHERS, "the arm is ON by default"
    env, ag, _led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    for _ in range(6):
        ag.step()
    st = env.observe()
    slots = sorted(k for k in st if k.startswith("o"))
    own, bg = frozenset(slots[:3]), frozenset(slots[3:8])
    ag._actuators = {"o0": (8, 1, own | bg), "o1": (5, 1, bg)}   # o1's touch changed bg
    ag._press_every = {slots[0]}                    # the first press changed one slot
    ag._act_refuted, ag._act_seen = set(), {}
    ag.iface.last_changed = tuple(bg)               # o0's press changed only what o1's did
    why_on = ag._act_end("o0", st)
    assert why_on == "no change", ("ON: net of the others' change is 0", why_on)
    tether._BASELINE_FROM_OTHERS = False
    try:
        ag._act_refuted, ag._act_seen = set(), {}
        why_off = ag._act_end("o0", st)
    finally:
        tether._BASELINE_FROM_OTHERS = True
    assert why_off is None, ("must-fail: the intersection leaves a net change", why_off)
    order = [o for o, _n, _ow in ag._act_order(st)]
    assert "o1" not in order, ("an object whose whole change is the others' is no actuator", order)
    print(f"test_baseline_from_others: o0's press over the others' change ends it ({why_on}); OFF "
          f"the one-slot intersection leaves it running; actuators ranked {order}")


if __name__ == "__main__":
    main()
