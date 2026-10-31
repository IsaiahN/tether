"""13 HARNESS_LEVEL_RESET (TETHER_HARNESS_LEVEL_RESET, default ON; the reviewer r464 2).
Minimal gates: one must-fail, one must-hold, each in its own process.
  check_mustfail_reset  a synthetic two-level engine game (no ARC content): one move clears level
                        1, then RESET is the next press. With the harness's _mode run, OFF goes back
                        to level 1 with score 0; ON stays on level 2 with its score
  check_off_identity    MUST-HOLD: TETHER_HARNESS_LEVEL_RESET=0 (off_env) byte-equal to cba1dd5 on
                        the fake whole run
    python tests/test_harness_level_reset.py [check ...]
"""
from __future__ import annotations

import io
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "cba1dd5"        # general-agent's release, before 13


def _two_levels():
    """A plumbing game: one block, two levels; ACTION1 moves the block and clears the level."""
    from arcengine import ARCBaseGame, GameAction, Level, Sprite

    class Two(ARCBaseGame):
        def __init__(self) -> None:
            levels = [Level(sprites=[Sprite([[3]], name="block", x=10, y=10)], grid_size=(16, 16))
                      for _ in range(2)]
            super().__init__(game_id="two", levels=levels, available_actions=[1], seed=0)

        def step(self) -> None:
            if self.action.id == GameAction.ACTION1:
                self.try_move("block", 1, 0)
                self.next_level()
            self.complete_action()
    return Two()


def _after_clear_then_reset(on: bool) -> tuple[int, int]:
    from arcengine import ActionInput, GameAction

    import arc_holdout
    os.environ.pop("ONLY_RESET_LEVELS", None)
    arc_holdout._HARNESS_LEVEL_RESET = on
    arc_holdout._mode()                              # the call the harness makes before an Arcade
    g = _two_levels()
    g.perform_action(ActionInput(id=GameAction.ACTION1))
    assert g.level_index == 1, ("occasion: level 1 not cleared", g.level_index)
    g.perform_action(ActionInput(id=GameAction.RESET))
    return g.level_index, g._score


def check_mustfail_reset() -> None:
    off = _after_clear_then_reset(False)
    assert off == (0, 0), ("MUST-FAIL: OFF should wipe to level 1, score 0", off)
    on = _after_clear_then_reset(True)
    assert on == (1, 1), ("ON should stay on the reached level with its score", on)
    print(f"  OFF: RESET right after clearing level 1 -> level index {off[0]}, score {off[1]} "
          f"(full reset); ON: level index {on[0]}, score {on[1]} (level reset)")


def check_off_identity() -> None:
    import tarfile
    import tempfile

    from _batch import off_env
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d))
    off = _norm(_child(root, off_env("TETHER_HARNESS_LEVEL_RESET")))
    diff = sum(1 for x, y in zip(base, off, strict=False) if x != y) + abs(len(base) - len(off))
    assert len(base) > 50 and diff == 0, ("OFF", len(base), len(off), next(
        (i for i, (x, y) in enumerate(zip(base, off, strict=False)) if x != y), None))
    print(f"  OFF (TETHER_HARNESS_LEVEL_RESET=0, fake): {len(base)} rows against {BASE}, "
          f"0 differences")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        assert r.returncode == 0, n
    print(f"harness_level_reset: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
