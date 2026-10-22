"""THE PACING VALUES (Isaiah 2026-10-21 18:58, via the reviewer 19:02): K-W tether.STEP_BUDGET
50,000 and K-M arc_holdout.ARC_WORK_BUDGET 5,000 by default, each a declared VALUE (conform/arms.py
VALUES). Each probe is a fresh process, because both are read at import.

  (1) the defaults: STEP_BUDGET 50,000; ARC_WORK_BUDGET 5,000; the toy world's Config() keeps
      15,000, so its falsifier (~13,298 candidates) is never truncated.
  (2) the override restores the old pacing: TETHER_STEP_BUDGET_N=1000000 and
      TETHER_WORK_BUDGET_N=15000 read back.
  (3) both names are declared in the arms seat's VALUES, with their reasons.
  The ledgers' @budget and stream rows (50,000 / 5,000) and the benchmark games against S3G are
  read apart.

    python tests/test_pacing_values.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT
PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
sys.path = [sys.argv[1]] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
import arc_holdout, tether
print(json.dumps({"step": tether.STEP_BUDGET, "arc": arc_holdout.ARC_WORK_BUDGET,
                  "toy": tether.Config().work_budget}))
'''


def probe(extra: dict) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", **extra)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, HERE], env=env, capture_output=True,
                         text=True, timeout=600, cwd=HERE)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    d = probe({})
    assert d == {"step": 50000, "arc": 5000, "toy": 15000}, d
    print(f"(1) defaults: STEP_BUDGET {d['step']:,}, ARC_WORK_BUDGET {d['arc']:,}, "
          f"toy Config {d['toy']:,}")
    o = probe({"TETHER_STEP_BUDGET_N": "1000000", "TETHER_WORK_BUDGET_N": "15000"})
    assert o == {"step": 1000000, "arc": 15000, "toy": 15000}, o
    print(f"(2) the override: STEP_BUDGET {o['step']:,}, ARC_WORK_BUDGET {o['arc']:,} "
          f"(the old pacing)")
    sys.path.insert(0, os.path.join(HERE, "conform"))
    import arms
    for n in ("TETHER_STEP_BUDGET_N", "TETHER_WORK_BUDGET_N"):
        assert n in arms.VALUES and "COUNT" in arms.VALUES[n], n
    print("(3) both declared in arms.VALUES as counts")
    print("test_pacing_values: pass")


if __name__ == "__main__":
    main()
