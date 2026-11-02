"""THE arms_today CENSUS (the reviewer 2026-11-01 r735; Isaiah 12:29, no unguarded fixes):
every default-ON arm whose definition line was first written on 2026-11-01 must be in
tether.arms_today(), and every entry there must read True. Dated by the earliest commit, across
every ref, that added the definition line (git log --all -G -p), never by a comment and never by
blame on this branch: a branch that took the lines as a snapshot would date them to the copy
(the reviewer 2026-11-02 r783). A line no commit added FAILS by name; there is no fallback. So an
arm built that day and left out of the submission worker's refuse-if-OFF guard fails here. Needs
git (the repo, not the submission bundle). The _CHECK instruments are OFF by design and match no
default=True.

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


def first_written(root: str) -> dict[str, tuple[str, str]]:
    """Each default-ON arm line ever added, mapped to (date, commit) of the earliest adding it."""
    out = subprocess.run(["git", "-C", root, "log", "--all", "--date=short",
                          "--format=@@ %h %ad", "-p", "-E", "-G", ARM.pattern[1:], "--", "*.py"],
                         capture_output=True, text=True, check=True).stdout
    seen: dict[str, tuple[str, str]] = {}
    commit = day = ""
    for line in out.splitlines():
        if line.startswith("@@ "):
            parts = line.split()
            if len(parts) == 3:
                commit, day = parts[1], parts[2]
        elif line.startswith("+") and ARM.match(line[1:]):
            code = line[1:].rstrip("\r")
            if code not in seen or day < seen[code][0]:
                seen[code] = (day, commit)
    return seen


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    import tether
    today = tether.arms_today()
    dated = first_written(root)
    built, unfound = [], []
    for path in sorted(glob.glob(os.path.join(root, "*.py"))):
        with open(path, encoding="utf-8") as fh:
            for code in fh.read().splitlines():
                m = ARM.match(code)
                if not m:
                    continue
                name = f"{os.path.basename(path)[:-3]}.{m.group(1)}"
                if code.rstrip("\r") not in dated:
                    unfound.append(name)
                    continue
                day, commit = dated[code.rstrip("\r")]
                print(f"  {name} first written {day} at {commit}")
                if day == DAY:
                    built.append(name)
    assert not unfound, ("no commit in this repository added these arm lines", unfound)
    assert built, "occasions: no default-ON arm dated today was found"
    missing = sorted(set(built) - set(today))
    assert not missing, ("built today, default ON, not guarded by arms_today", missing)
    off = sorted(k for k, v in today.items() if not v)
    assert not off, ("arms_today reads OFF", off)
    print(f"test_arms_today: {len(built)} default-ON arms dated {DAY}, all in arms_today "
          f"({len(today)} entries), all True")


if __name__ == "__main__":
    main()
