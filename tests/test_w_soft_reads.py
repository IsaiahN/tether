"""M2, SOFT READS ONLY (TETHER_W_SOFT_READS, default ON; the reviewer 2026-10-23 09:18,
09:25): a write to a W-2 cache (_Kept) no longer marks the entry seen, so a SOFT fold drops the
entries not READ since the last fold. Each arm state in its own process (arms resolve at import).
  ON   first fold: a written-and-read entry stays, a written-only entry goes (1 evicted); second
       fold: the kept entry, not read since, goes, and a fresh write-only one goes too (2)
  MF   OFF (the old rule): the first fold evicts 0 (every written entry is "seen"); the second
       drops the two not touched since and keeps the fresh write (2, keeps c)
  HARD both states: a hard fold drops everything
    python tests/test_w_soft_reads.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import tether
c = tether._Kept()
c["a"] = 1
c["b"] = 2
c.get("a")
first = c.evict(hard=False)
keys1 = sorted(c)
c["c"] = 3
second = c.evict(hard=False)
keys2 = sorted(c)
h = tether._Kept()
h["x"] = 1
h.get("x")
hard = h.evict(hard=True)
print(json.dumps({"on": tether._W_SOFT_READS, "first": first, "keys1": keys1, "second": second,
                  "keys2": keys2, "hard": hard, "hard_left": len(h)}))
'''


def child(state: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_W_SOFT_READS=state)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, str(_repo.ROOT)], env=env,
                         capture_output=True, text=True, timeout=300, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    on, off = child("1"), child("0")
    assert on["on"] and not off["on"], (on, off)
    assert (on["first"], on["keys1"]) == (1, ["a"]), ("ON first fold", on)
    assert (on["second"], on["keys2"]) == (2, []), ("ON second fold", on)
    print(f"  ON: first SOFT fold evicts {on['first']} (keeps {on['keys1']}), "
          f"second {on['second']}")
    assert (off["first"], off["keys1"]) == (0, ["a", "b"]), ("MF OFF first fold", off)
    assert (off["second"], off["keys2"]) == (2, ["c"]), ("MF OFF second fold", off)
    print(f"  MF OFF: the first SOFT fold evicts {off['first']} (inert, as E4b read), the "
          f"second {off['second']} (keeps {off['keys2']}: its write marked it seen)")
    for s in (on, off):
        assert (s["hard"], s["hard_left"]) == (1, 0), ("HARD", s)
    print("  HARD: drops everything in both states")
    print("w_soft_reads: OK")


if __name__ == "__main__":
    main()
