"""THE arms_today CENSUS (the reviewer 2026-11-01 r735; Isaiah 12:29, no unguarded fixes):
every default-ON arm whose definition line git dates to 2026-11-01 must be in
tether.arms_today(), and every entry there must read True. Dated by `git blame` on the
definition line, never by a comment, so an arm built today and left out of the Kaggle worker's
refuse-if-OFF guard fails here. Needs git (the repo, not the Kaggle bundle). The _CHECK
instruments are OFF by design and match no default=True.

    python tests/test_arms_today.py
"""
from __future__ import annotations

import glob
import os
import re
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
DAY = "2026-11-01"
ARM = re.compile(r'^(_[A-Z0-9_]+) = armflag\.arm\("TETHER_[A-Z0-9_]+", default=True\)')


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    import tether
    today = tether.arms_today()
    built = []
    for path in sorted(glob.glob(os.path.join(root, "*.py"))):
        out = subprocess.run(["git", "-C", root, "blame", "--date=short", "--",
                              os.path.basename(path)],
                             capture_output=True, text=True, check=True).stdout
        for line in out.splitlines():
            head, _, code = line.partition(") ")
            m = ARM.match(code)
            if m and DAY in head:
                built.append(f"{os.path.basename(path)[:-3]}.{m.group(1)}")
    assert built, "occasions: no default-ON arm dated today was found"
    missing = sorted(set(built) - set(today))
    assert not missing, ("built today, default ON, not guarded by arms_today", missing)
    off = sorted(k for k, v in today.items() if not v)
    assert not off, ("arms_today reads OFF", off)
    print(f"test_arms_today: {len(built)} default-ON arms dated {DAY}, all in arms_today "
          f"({len(today)} entries), all True")


if __name__ == "__main__":
    main()
