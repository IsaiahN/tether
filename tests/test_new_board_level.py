"""24 (C) THE LEVEL AT A GAME SWITCH (TETHER_NEW_BOARD_LEVEL, default ON; the reviewer 2026-11-05
r1250). gridworld default seed 0, 6 steps; a world reporting its own level count planted.
  check_l1_world_level  ON: a new board starts at the world's level (0), not the previous game's
                        3; OFF: 3, as before; a world with no levels(): self.level both ways
  check_l2_site         the NEW_BOARD retarget reads _new_board_level (AST), the one site
    python tests/test_new_board_level.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True


def check_l1_world_level() -> None:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    assert tether._NEW_BOARD_LEVEL, "TETHER_NEW_BOARD_LEVEL is OFF"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    ag.level = 3
    plain = ag._new_board_level()
    assert plain == 3 or hasattr(ag.env, "levels"), plain
    ag.env.levels = lambda: (0, 5)
    on = ag._new_board_level()
    tether._NEW_BOARD_LEVEL = False                 # MUST-FAIL: the old number runs on
    off = ag._new_board_level()
    assert (on, off) == (0, 3), (on, off)
    print(f"  previous game at level 3: ON {on}, OFF {off}; a world with no levels(): {plain}")


def check_l2_site() -> None:
    import ast
    import inspect

    import tether
    src = inspect.getsource(tether)
    calls = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Call)
             and getattr(n.func, "attr", "") == "retarget"
             and any(getattr(k.value, "id", "") == "NEW_BOARD" for k in n.keywords)]
    assert len(calls) == 1, len(calls)
    lv = calls[0].args[1]
    assert isinstance(lv, ast.Call) and lv.func.attr == "_new_board_level", ast.dump(lv)
    print("  the one NEW_BOARD retarget reads _new_board_level()")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    bad = [n for n in names if subprocess.run([sys.executable, "-B", __file__, n],
                                              cwd=str(_repo.ROOT),
                                              stdin=subprocess.DEVNULL).returncode]
    assert not bad, bad
    print(f"new_board_level: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
