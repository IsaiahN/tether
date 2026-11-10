"""BUILD 5 ITEM 19 (c), COMPOUNDS FROM UNBUNDLING (TETHER_GOAL_UNBUNDLE; the reviewer 2026-11-05
r1229, r1230). A stalled group whose members split by stuck()'s own predicate keeps the members
that fell; the next proposal offers kept AND c for a candidate on a flat member, priced
bits(c) - gain(kept). Seconds: test_group_propose's held group "ALL kind(o5): o5.row == o1.row".

MF-U1  RED FIRST: two members' readings fall (0.5 -> 0.25, 1 bit each), the rest stay flat; the
       hold ends at its ceiling; a goal_unbundled row names fell, flat, gain 2.0 and kept_bits; the
       next proposal over c (on a flat member, a different template) holds the compound, its
       wants on c and on both kept members. OFF: no row, and the bare c is held
MF-U2  every member flat: no split, no row, the bare c is held
MF-U3  the compound's price is bits(c) - gain, read off the sort: 1 bit per member gives 2.0 below
       the bare c, 2 bits per member gives 4.0 below
(Route knowledge is stubbed as test_group_propose does; the readings are planted at _hyp_check.)
The red is behavioural: TETHER_GOAL_UNBUNDLE=0 fails MF-U1.

    python tests/test_goal_unbundle.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_propose as P  # noqa: E402

tether = P.tether
N = tether.MIN_REPEAT + 1


def held_group():
    """The group held (test_group_propose's MF-P1, the arm as configured)."""
    ag, row = P.propose(None)
    assert ag._hyp is not None and isinstance(ag._hyp["cond"], tether._Group), ("the hold", row)
    return ag


def stall(ag, drop: float | None) -> list:
    """Readings planted (fell: the first two members, 0.5 -> 0.5 / drop), ended at the ceiling
    through _hyp_check."""
    h = ag._hyp
    slots = [p.slot for p in h["cond"].parts]
    for i, sl in enumerate(slots):
        h["reads"][sl] = ([0.5] * (N - 1) + [0.5 / drop] if drop and i < 2 else [0.5] * N)
    h["own_last"], h["steps"] = True, h["budget"]
    ag._hyp_check()
    end = [r for r in ag.led.rows() if r["event"] == "goal_hypothesis_end"][-1]["detail"]
    assert ag._hyp is None and end["why"] == "stalled", ("the ceiling", end)
    return slots


def offer(ag, slots: list) -> tuple:
    b = ag.trace[-1][2]
    owner = slots[2].split(".", 1)[0]
    other = next(o for o in ("o0", "o2", "o3", "o4", "o5")
                 if o != owner and b[f"{o}.col"] != b[f"{owner}.col"])
    c = f"{owner}.col == {other}.col"
    ag.wants.clear()
    ag._hyp, ag._hyp_exhausted = None, None
    ag._inv_conditions = lambda _b, **_k: [c]
    ag._route_first_set = lambda _b: None
    was = tether._GROUP_PROPOSE
    tether._GROUP_PROPOSE = False
    try:
        ag._hyp_propose(b)
    finally:
        tether._GROUP_PROPOSE = was
    return c, [r for r in ag.led.rows() if r["event"] == "goal_hypotheses"][-1]["detail"]


def unbundled(ag) -> list:
    return [r["detail"] for r in ag.led.rows() if r["event"] == "goal_unbundled"]


def run(drop: float | None, on: bool = True) -> tuple:
    was = tether._GOAL_UNBUNDLE
    tether._GOAL_UNBUNDLE = on
    try:
        ag = held_group()
        slots = stall(ag, drop)
        c, row = offer(ag, slots)
        return ag, slots, c, row, unbundled(ag)
    finally:
        tether._GOAL_UNBUNDLE = was


def main():
    _a, _s, c0, off, rows0 = run(2.0, on=False)
    assert not rows0 and off.get("pick") == c0, ("MF-U1 (red first): OFF", off)

    ag, slots, c, row, rows = run(2.0, on=tether._GOAL_UNBUNDLE)
    assert len(rows) == 1, ("MF-U1: no goal_unbundled row", rows)
    u = rows[0]
    assert u["fell"] == slots[:2] and u["flat"] == slots[2:] and u["gain"] == 2.0, ("MF-U1", u)
    assert row.get("pick", "").startswith(f"{c} and kept("), ("MF-U1: not held", row)
    assert set(ag._hyp["slots"]) == {c.split(" ")[0], *slots[:2]}, ("MF-U1: wants", ag._hyp)
    bits = {x["if"]: x["bits"] for x in row["ranked"]}
    d1 = round(bits[c] - bits[row["pick"]], 6)
    assert d1 == 2.0, ("MF-U3: the price is not bits(c) - gain", bits)

    _a, _s, c2, flat, rows2 = run(None)
    assert not rows2 and flat.get("pick") == c2, ("MF-U2: all flat split", rows2, flat)

    _a, _s, c3, row3, rows3 = run(4.0)
    bits3 = {x["if"]: x["bits"] for x in row3["ranked"]}
    d3 = round(bits3[c3] - bits3[row3["pick"]], 6)
    assert rows3[0]["gain"] == 4.0 and d3 == 4.0, ("MF-U3: a steeper fall", rows3, bits3)
    print(f"test_goal_unbundle: pass (MF-U1 fell {u['fell']} flat {u['flat']} gain {u['gain']} "
          f"kept_bits {u['kept_bits']}; held {row['pick']!r} at {bits[row['pick']]} bits against "
          f"the bare {bits[c]} (OFF: {off['pick']!r}); MF-U2 all flat: no row, {flat['pick']!r}; "
          f"MF-U3 gain 2.0 -> {d1} below, gain 4.0 -> {d3} below)")


if __name__ == "__main__":
    main()
