"""The latch habitat's must-fail checks.

Each check is a refuter: it would fail if the two-step structure were absent or faked. The
world is a MEANS, not a benchmark -- these tests assert it can EXHIBIT the capability, never
that the agent clears it. Per-game/per-seed, never pooled; arm state stated.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.dont_write_bytecode = True

import latchworld  # noqa: E402
import world  # noqa: E402

SEEDS = range(12)


def _drive(w, seq):
    for a in seq:
        w.step(a)


def test_01_contract_binds():
    """The agent's adapter accepts every world; this one fills all eight."""
    for s in SEEDS:
        assert world.bind(latchworld.LatchWorld(seed=s)) is not None


def test_02_goal_reachable_by_construction():
    """PANEL PRECONDITION: the arm+fire sequence can move the goal on EVERY seed.

    A world whose goal cannot move under its own advertised actions is the F398 defect --
    an unreadable null, not a finding. Repeated arm+fire must reach any target colour.
    """
    for s in SEEDS:
        w = latchworld.LatchWorld(seed=s)
        before = w.state[f"o{w.goal}.colour"]
        _drive(w, ("press_" + str(w.arm), "press_" + str(w.fire)))
        assert w.state[f"o{w.goal}.colour"] == (before + 1) % 4, (
            f"seed {s}: arm+fire did not advance the goal")
        # and repeated pairs clear the objective: the target is 1-3 advances away on a
        # 4-colour cycle, so drive until cleared (bounded by the cycle length), not a fixed
        # count, which would overshoot the target.
        for _ in range(4):
            if w._completed() == 1:
                break
            _drive(w, ("press_" + str(w.arm), "press_" + str(w.fire)))
        assert w._completed() == 1, f"seed {s}: repeated arm+fire never cleared"


def test_03_single_action_never_moves_goal():
    """REFUTER: no advertised action, however repeated, moves the goal on a wired board.

    This is the whole point of the habitat -- it makes a single-action policy incapable of
    clearing, so a two-step routine has something to buy. If any one action moved the goal
    this world would be another `click_only` and the test must fail.
    """
    for s in SEEDS:
        for i in range(len(latchworld.ACTIONS)):
            w = latchworld.LatchWorld(seed=s)
            before = w.state[f"o{w.goal}.colour"]
            for _ in range(8):
                w.step("press_" + str(i))
            assert w.state[f"o{w.goal}.colour"] == before, (
                f"seed {s}: press_{i} alone moved the goal -- not a two-step world")


def test_04_latch_is_perceivable():
    """The causal chain is published; a hidden latch would make the residual unreadable."""
    for s in SEEDS:
        w = latchworld.LatchWorld(seed=s)
        assert latchworld.ARMED_SLOT in w.observe()
        assert latchworld.ARMED_SLOT in w.slots()
        w.step("press_" + str(w.arm))
        assert w.state[latchworld.ARMED_SLOT] == 1, f"seed {s}: arm not perceivable"
        w.step("press_" + str(w.fire))
        assert w.state[latchworld.ARMED_SLOT] == 0, f"seed {s}: fire did not consume the latch"


def test_05_fire_alone_and_distractors():
    """Firing before arming changes a distractor, never the goal; a press always moves some slot."""
    for s in SEEDS:
        w = latchworld.LatchWorld(seed=s)
        snap = dict(w.state)
        before = w.state[f"o{w.goal}.colour"]
        w.step("press_" + str(w.fire))
        assert w.state[f"o{w.goal}.colour"] == before
        assert w.state != snap, f"seed {s}: a press changed nothing -- no residual"


def test_06_control_arm_is_directly_reachable():
    """With the latch removed the goal is reachable by pressing it once -- the control."""
    for s in SEEDS:
        w = latchworld.LatchWorld(seed=s, wired=False)
        before = w.state[f"o{w.goal}.colour"]
        w.step("press_" + str(w.goal))
        assert w.state[f"o{w.goal}.colour"] == (before + 1) % 4


def test_07_deterministic_and_goal_not_stored_writable():
    """Same seed is the same board; the goal slot is derived, never a stored field."""
    a = latchworld.LatchWorld(seed=7)
    b = latchworld.LatchWorld(seed=7)
    assert a.state == b.state and (a.arm, a.fire, a.goal) == (b.arm, b.fire, b.goal)
    assert latchworld.GOAL_SLOT not in a.state


def test_08_one_vocabulary_with_world2d():
    """The atom set is reused verbatim -- contact, not vocabulary, is the variable."""
    import world2d
    assert [a.name for a in latchworld.LatchWorld(seed=0).atoms()] == [
        a.name for a in world2d.World2D(seed=0).atoms()]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: OK")
    print("latchworld: all OK")
