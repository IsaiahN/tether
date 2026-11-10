"""MUSING's switch and its alias (r1253): TETHER_MUSING=0 turns musing off; TETHER_MC6=0 still
turns it off; both unset gives ON; when both are set, TETHER_MUSING wins.
    python tests/test_musing_alias.py
"""
from __future__ import annotations

import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
PROBE = "import sys; sys.dont_write_bytecode = True; import tether; print(tether._MUSING)"


def _read(extra: dict) -> str:
    env = {k: v for k, v in os.environ.items() if k not in ("TETHER_MUSING", "TETHER_MC6")}
    env.update(PYTHONDONTWRITEBYTECODE="1", **extra)
    p = subprocess.run([sys.executable, "-B", "-c", PROBE], env=env, cwd=str(_repo.ROOT),
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-1500:]
    return p.stdout.strip().splitlines()[-1]


def main() -> int:
    got = {name: _read(extra) for name, extra in (
        ("unset", {}), ("MUSING=0", {"TETHER_MUSING": "0"}), ("MC6=0", {"TETHER_MC6": "0"}),
        ("MUSING=1 MC6=0", {"TETHER_MUSING": "1", "TETHER_MC6": "0"}),
        ("MUSING=0 MC6=1", {"TETHER_MUSING": "0", "TETHER_MC6": "1"}))}
    want = {"unset": "True", "MUSING=0": "False", "MC6=0": "False", "MUSING=1 MC6=0": "True",
            "MUSING=0 MC6=1": "False"}
    assert got == want, got
    print(f"musing_alias: {got}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
