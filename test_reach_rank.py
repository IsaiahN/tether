"""E1 part 2 (TETHER_REACH_RANK; Isaiah 2026-10-17 06:42, the reviewer 06:49): the CAUSE candidates'
ranking and budget, on the pure functions reach.cause_tiers and reach.next_ring. Fixtures only (a
substituted habitat, Fig 11 :70: wiring, never capability); the in-agent reading is lf52's rows.

  F1  the cause is the agent's own target: tier 0, first, so it is asked on step 1
  F2  a motionless switch across the board (no change, no contact path): the last tier, reached
      once every ring has been tried while unexplained, and NEVER absent from the tiers
      MF-F2 the tiers without the last ring drop it, and the coverage check says so
  F3  two co-causes in one ring: one tier, so both are tested in the same step; a cause found
      there stops the advance (the blocking guard)
  F4  the kind boost: a known kind goes first in its tier, after R0
  F5  the budget: one ring per step while unexplained; "every tier reached" only at the last
  F6  contingency on change events: a moving trigger before a timer before a motionless
      enabling switch, the switch kept
"""
import sys

sys.dont_write_bytecode = True

import reach  # noqa: E402


def covers(tiers: list, objects: list, mine: str) -> bool:
    flat = [o for t in tiers for o in t]
    return sorted(flat) == sorted(o for o in objects if o != mine) and len(flat) == len(set(flat))


def reached_after(tiers: list, steps: int) -> set:
    ring, out = 0, set()
    for _ in range(steps):
        out |= {o for t in tiers[:ring + 1] for o in t}
        ring, _done = reach.next_ring(ring, len(tiers), explained=False)
    return out


def main() -> int:
    objs = ["m", "t", "a", "b", "s", "x"]
    adj = {"m": {"a"}, "a": {"m", "b"}, "b": {"a"}}
    age = {"x": 2, "t": 0}

    tiers = reach.cause_tiers("m", "t", age, adj, objs)
    assert tiers[0][0] == "t", tiers                                     # F1
    assert tiers[0] == ("t", "x"), tiers                                 # R1 after R0
    print("F1 own target first in tier 0:", tiers)

    assert covers(tiers, objs, "m"), tiers                               # F2
    assert tiers[-1] == ("s",), tiers
    assert "s" not in reached_after(tiers, len(tiers) - 1)
    assert "s" in reached_after(tiers, len(tiers))
    assert not covers(tiers[:-1], objs, "m")                             # MF-F2
    print(f"F2 switch reached at step {len(tiers)}, never excluded; MF-F2 red")

    adj3 = {"m": {"c1", "c2"}}
    t3 = reach.cause_tiers("m", None, {}, adj3, ["m", "c1", "c2", "z"])
    ring1 = next(t for t in t3 if "c1" in t)
    assert "c2" in ring1, t3                                             # F3
    ring, done = reach.next_ring(0, len(t3), explained=True)
    assert (ring, done) == (0, False)
    print("F3 co-causes in one tier:", ring1, "; a found cause holds the ring")

    t4 = reach.cause_tiers("m", "t", {"x": 1, "y": 1}, {}, ["m", "t", "x", "y"],
                           boosted=frozenset({"y"}))
    assert t4[0] == ("t", "y", "x"), t4                                  # F4
    print("F4 boosted kind first after R0:", t4[0])

    # F6 (the reviewer 06:54, 07:19): a motionless switch ENABLES an effect a moving trigger sets
    # off, and a timer ticks every frame; all in one tier. Contingency on change events: the
    # trigger changes just before each effect (dP 0.5), the timer every transition (dP 0), the
    # switch never (constant). So trigger, then timer, then the switch -- deferred, never absent
    changed = [{"timer"}, {"timer", "trig"}, {"timer"}, {"timer"}, {"timer", "trig"}, {"timer"}]
    effect = [False, False, True, False, False, True]
    dp, const = reach.trail(changed, effect, ["trig", "timer", "sw"])
    assert dp == {"trig": 0.5, "timer": 0.0} and const == {"sw"}, (dp, const)
    t6 = reach.cause_tiers("m", None, {}, {"m": {"sw", "trig", "timer"}},
                           ["m", "sw", "timer", "trig"], dp=dp, constant=const)
    assert t6[0] == ("trig", "timer", "sw"), t6
    print("F6 trigger, then the timer, then the enabling switch (kept):", t6, dp)

    ring, steps = 0, []
    for _ in range(5):
        ring, done = reach.next_ring(ring, 3, explained=False)
        steps.append((ring, done))
    assert steps == [(1, False), (2, False), (2, True), (2, True), (2, True)], steps   # F5
    print("F5 one ring per step:", steps)
    print("reach_rank: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
