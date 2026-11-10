"""F, THE SUBJECT READ BEFORE THE COMPILE (the reviewer 2026-11-07 r1419): a library text whose
subject is not a movable slot is refused before compile_candidate. The fake ARC game, a few steps,
under tether.F_PRE_CHECK (each refused text compiled anyway and compared).

  P1  the pre-filter fires (F_PRE_N["refused"] > 0, the precondition)
  P2  THE MUST-HOLD: every refused text that compiles has the subject that was read (mismatch 0)

    python tests/test_subject_prefilter.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT


def child() -> dict:
    sys.path.insert(0, HERE)
    sys.path.insert(1, os.path.join(HERE, "tests"))
    os.chdir(HERE)
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    tether.F_PRE_CHECK = True
    _env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    for _ in range(int(os.environ.get("SPF_STEPS", "6"))):
        ag.step()
    return dict(tether.F_PRE_N)


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--child":
        print(json.dumps(child(), sort_keys=True))
        return 0
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--child"],
                       capture_output=True, text=True, env=env, cwd=HERE,
                       stdin=subprocess.DEVNULL, timeout=600)
    assert p.returncode == 0, p.stderr[-2000:]
    n = json.loads(p.stdout.strip().splitlines()[-1])
    assert n.get("refused", 0) > 0, ("P1 precondition: the pre-filter never fired", n)
    assert n.get("mismatch", 0) == 0, ("P2 must-hold: a compiled subject is not the one read", n)
    print(f"P1  refused before the compile: {n['refused']} (the compile would refuse "
          f"{n.get('compile_refused', 0)} of them)")
    print("P2  compiled subject == the subject read: mismatch 0")
    print("subject_prefilter: 2 of 2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
