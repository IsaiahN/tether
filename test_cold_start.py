"""THE COLD START (Isaiah 2026-10-21 19:26: a fresh clone with no lineage runs, creates its
lineage and fills it by itself; the reviewer 19:47 (i), 22:59). The fake ARC game
(test_entry.FakeWrapper), in temp folders; the agent's own lineage is never read.

  CS1  a lineage path that does not exist (three levels deep) is created at load, the game
       plays, and a generation is written.
  MF1  MUST-FAIL: with lineage._ensure_dir made a no-op (the old code), the same play raises
       sqlite3.OperationalError at the store's open.
  CS2  an EXISTING lineage loads identically with and without the fix: two fresh processes,
       each a wire() on the folder CS1 wrote, report the same load and hold the same library.

    python test_cold_start.py
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

import arc_holdout  # noqa: E402
import lineage  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402

CHILD = r'''
import json, os, sys
sys.dont_write_bytecode = True
sys.path = [sys.argv[1]] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
os.chdir(sys.argv[1])
import arc_holdout, lineage
from test_entry import FakeWrapper
if sys.argv[3] == "noop":
    lineage._ensure_dir = lambda d: None
out = arc_holdout.wire(FakeWrapper(), "fake", lineage_dir=sys.argv[2])
ag, loaded = out[1], out[5]
print(json.dumps({"lineage": loaded["lineage"], "library": sorted(ag.gamma.library)},
                 sort_keys=True, default=str))
'''


class Arc:
    def make(self, _game):
        return FakeWrapper()


def child(d: Path, mode: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-B", "-c", CHILD, HERE, str(d), mode], env=env,
                         capture_output=True, text=True, timeout=600, cwd=HERE)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="cold_start_"))
    try:
        d = tmp / "a" / "b" / "lineage"
        assert not d.exists()
        r = arc_holdout.play("fake", 3, arc=Arc(), lineage_dir=str(d))["persistence"]
        gens = sorted(p.name for p in d.glob("gen_*.json"))
        assert d.is_dir() and r["lineage"]["written"] and gens, ("CS1", r["lineage"], gens)
        print(f"  CS1: {d.relative_to(tmp)} did not exist; created at load; played; wrote "
              f"{r['lineage']['hash']} ({len(gens)} generation file)")
        real = lineage._ensure_dir
        lineage._ensure_dir = lambda _d: None
        try:
            m = tmp / "x" / "y" / "lineage"
            try:
                arc_holdout.play("fake", 3, arc=Arc(), lineage_dir=str(m))
            except sqlite3.OperationalError as e:
                print(f"  MF1: without the fix, a missing folder raises "
                      f"sqlite3.OperationalError ({e})")
            else:
                raise AssertionError("MF1 did not fail: the old code played on a missing folder")
        finally:
            lineage._ensure_dir = real
        a, b = child(d, "fixed"), child(d, "noop")
        assert a == b, ("CS2", {k: (a[k] == b[k]) for k in a})
        print(f"  CS2: an existing lineage loads identically with and without the fix "
              f"(parent {a['lineage'].get('parent')}, {len(a['library'])} library entries)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("test_cold_start: pass")


if __name__ == "__main__":
    main()
