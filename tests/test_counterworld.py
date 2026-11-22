"""The counter habitat's must-fail checks. A MEANS, not a benchmark: these assert the world
can EXHIBIT a count-conditioned numeric cause, never that the agent discovers it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.dont_write_bytecode = True

import counterworld  # noqa: E402
import world  # noqa: E402
import world2d  # noqa: E402

SEEDS = range(12)


def _drive(w, action, n):
    for _ in range(n):
        w.step(action)


def test_01_contract_binds():
    for s in SEEDS:
        assert world.bind(counterworld.CounterWorld(seed=s)) is not None


def test_02_reachable_by_construction():
    """PANEL PRECONDITION: N-period presses clear any target (bounded by the grid cycle)."""
    for s in SEEDS:
        w = counterworld.CounterWorld(seed=s)
        for _ in range(counterworld.GRID + 1):
            if w._completed() == 1:
                break
            _drive(w, "press_" + str(w.counter), w.period)
        assert w._completed() == 1, f"seed {s}: counter presses never cleared"


def test_03_refuter_no_single_press_cadence():
    """Every single press leaves the goal size unchanged; only the Nth counter press moves it.

    If any action advanced the goal on EACH press, this world would be click_only and the
    count-cause mechanism would have nothing to discover -- the test must fail then.
    """
    for s in SEEDS:
        for i in range(len(counterworld.ACTIONS)):
            w = counterworld.CounterWorld(seed=s)
            before = w.state[f"o{w.goal}.size"]
            w.step("press_" + str(i))
            assert w.state[f"o{w.goal}.size"] == before, f"seed {s}: a single press moved the goal"


def test_04_period_is_exact():
    """Goal advances on the Nth counter press and not before; count resets after firing."""
    for s in SEEDS:
        w = counterworld.CounterWorld(seed=s)
        before = w.state[f"o{w.goal}.size"]
        for k in range(1, w.period):
            w.step("press_" + str(w.counter))
            assert w.state[f"o{w.goal}.size"] == before, f"seed {s}: advanced early at {k}"
        w.step("press_" + str(w.counter))
        assert w.state[f"o{w.goal}.size"] == (before + 1) % counterworld.GRID
        # after firing, another period-1 presses do not advance it again
        for _ in range(w.period - 1):
            w.step("press_" + str(w.counter))
        assert w.state[f"o{w.goal}.size"] == (before + 1) % counterworld.GRID


def test_05_non_counter_never_moves_goal():
    """Repeating a non-counter action never advances the goal, whatever its count."""
    for s in SEEDS:
        for i in range(len(counterworld.ACTIONS)):
            if i == counterworld.CounterWorld(seed=s).counter:
                continue
            w = counterworld.CounterWorld(seed=s)
            before = w.state[f"o{w.goal}.size"]
            _drive(w, "press_" + str(i), 20)
            assert w.state[f"o{w.goal}.size"] == before, (
                f"seed {s}: non-counter press {i} moved goal")


def test_06_goal_slot_derived_and_goal_type_numeric():
    """The goal lives on a numeric (EXTENT) slot -- same type as a count cause -- not a BOOL."""
    for s in SEEDS:
        w = counterworld.CounterWorld(seed=s)
        assert counterworld.GOAL_SLOT not in w.state
        assert w.slot_types()[f"o{w.goal}.size"] == "EXTENT"


def test_07_control_arm_direct():
    for s in SEEDS:
        w = counterworld.CounterWorld(seed=s, wired=False)
        before = w.state[f"o{w.goal}.size"]
        w.step("press_" + str(w.goal))
        assert w.state[f"o{w.goal}.size"] == (before + 1) % counterworld.GRID


def test_08_deterministic_and_one_vocabulary():
    a = counterworld.CounterWorld(seed=7)
    b = counterworld.CounterWorld(seed=7)
    assert a.state == b.state and (a.counter, a.period, a.goal) == (b.counter, b.period, b.goal)
    assert [x.name for x in a.atoms()] == [x.name for x in world2d.World2D(seed=0).atoms()]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: OK")
    print("counterworld: all OK")
