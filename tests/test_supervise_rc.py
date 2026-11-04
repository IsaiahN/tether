"""THE SUPERVISOR EXITS WITH THE CHILD'S rc (the reviewer 2026-11-04 r1094, r1097).
harness/supervise.py wrote the child's rc to sup.json and then returned 0, so every launcher that
exits with the supervisor's code logged "game rc 0" -- launch 1 of the 8a A/B died before its first
step (rc 1 in sup.json) and read as rc 0. Seconds; a child that only exits.

MF-S1  a child that exits 3 makes the supervisor exit 3, and sup.json says rc 3, ending EXIT
MF-S2  a child that exits 0 makes the supervisor exit 0
The red is today's code at 6a64e66: MF-S1 reads exit 0.

    python tests/test_supervise_rc.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
SUP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "harness",
                   "supervise.py")


def run(code: int) -> tuple[int, dict]:
    out = tempfile.mkdtemp(prefix="sup_rc_")
    child = [sys.executable, "-B", "-c", f"import sys; sys.exit({code})"]
    p = subprocess.run([sys.executable, "-B", SUP, "--out", out, "--watch-pid", str(os.getpid()),
                        "--max-s", "60", "--", *child], check=False, timeout=120)
    with open(os.path.join(out, "sup.json"), encoding="utf-8") as fh:
        return p.returncode, json.load(fh)


def main():
    rc3, sup3 = run(3)
    assert (rc3, sup3["rc"], sup3["ending"]) == (3, 3, "EXIT"), ("MF-S1", rc3, sup3)
    rc0, sup0 = run(0)
    assert (rc0, sup0["rc"]) == (0, 0), ("MF-S2", rc0, sup0)
    print(f"  MF-S1 child exit 3 -> supervisor exit {rc3} "
          f"(sup.json rc {sup3['rc']}, {sup3['ending']})")
    print(f"  MF-S2 child exit 0 -> supervisor exit {rc0}")
    print("test_supervise_rc OK")


if __name__ == "__main__":
    main()
