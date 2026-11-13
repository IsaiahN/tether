"""THE KNOWN-RED CHECK (the reviewer r1720 1, r1722 3): tests red before tonight's work, each
carried with the message it fails with. The check passes while every one fails EXACTLY as
recorded, and goes red if one starts passing or fails differently -- so a known-red is never read
as green and never drifts unseen. Each still owes a ruling (a regression, a moved baseline, or a
test defect).

An UNSTABLE red (the reviewer r1723 2(b), r1742) fails in more than one way from run to run: it is
checked FAILS-ONLY -- any failure keeps it known, its last line is logged, a pass turns it red.
test_index_carry fails with the recorded ValueError on 7543500 and with "KeyError:
('LINGUISTIC|Sentence', 'CAUSE')" at its own timing print (line 153) on 7543500 + the still-board
change, 2026-11-11.

    python tests/known_red.py
"""
from __future__ import annotations

import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

# test file -> the line it fails with, as recorded (red at dd1dad3 and 31f3d1e)
# 7b (r1900): test_k1 (first bad 2c2a136: check C spent the old knob; the walk reads the purse)
# and test_carry_w (first bad ec02ac3: a landing-time identity vs 10cbfae, rewritten ON vs OFF on
# the same tree, r1901)
# repaired and removed
KNOWN = {
    "test_index_carry.py": "ValueError: too many values to unpack (expected 2)",
}
UNSTABLE = {"test_index_carry.py"}          # r1723 2(b), r1742: fails-only


def main() -> int:
    bad = []
    here = os.path.dirname(os.path.abspath(__file__))
    for name, msg in KNOWN.items():
        r = subprocess.run([sys.executable, "-B", os.path.join(here, name)], cwd=_repo.ROOT,
                           stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
        out = r.stdout + r.stderr
        if name in UNSTABLE:
            ok = r.returncode != 0
            last = next((ln for ln in reversed(out.splitlines()) if ln.strip()), "")
            print(f"  {name}: {'UNSTABLE RED, fails' if ok else 'CHANGED (passes)'}: {last}")
        else:
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
