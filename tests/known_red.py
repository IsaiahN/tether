"""THE KNOWN-RED CHECK (the reviewer r1720 1, r1722 3): tests red before tonight's work, each
carried with the message it fails with. The check passes while every one fails EXACTLY as
recorded, and goes red if one starts passing or fails differently -- so a known-red is never read
as green and never drifts unseen. Each still owes a ruling (a regression, a moved baseline, or a
test defect).

    python tests/known_red.py
"""
from __future__ import annotations

import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

# test file -> the line it fails with, as recorded (red at dd1dad3 and 31f3d1e)
KNOWN = {
    "test_k1.py": "AssertionError: (False, (58, 0))",
    "test_carry_w.py": "AssertionError: check_off_identity",
    "test_index_carry.py": "ValueError: too many values to unpack (expected 2)",
}


def main() -> int:
    bad = []
    here = os.path.dirname(os.path.abspath(__file__))
    for name, msg in KNOWN.items():
        r = subprocess.run([sys.executable, "-B", os.path.join(here, name)], cwd=_repo.ROOT,
                           stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
        out = r.stdout + r.stderr
        ok = r.returncode != 0 and msg in out
        print(f"  {name}: {'KNOWN-RED as recorded' if ok else f'CHANGED (rc {r.returncode})'}")
        if not ok:
            bad.append(name)
    if bad:
        print("known_red: CHANGED", bad)
        return 1
    print("known_red: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
