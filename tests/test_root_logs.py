"""8e, THE ROOT LOGS (the reviewer r1801, r1831): a ledger at the repo root writes its narrate,
nsm and pipeline logs to logs/ (git-ignored), never to the root.

  RL1   a Ledger whose path is in the repo root creates logs/narrate.log, logs/nsm.log and
        logs/pipeline.log, and no narrate.log, nsm.log or pipeline.log at the root.
  MF-RL1 narrate.log_beside put back to "beside the ledger" (the plant): root files appear -> RED.
  A ledger anywhere else keeps its logs beside it (RL2).

    python tests/test_root_logs.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import ledger  # noqa: E402
import narrate  # noqa: E402

ROOT = Path(_repo.ROOT)
NAMES = ("narrate.log", "nsm.log", "pipeline.log")


def at_root(plant: bool) -> tuple[list, list]:
    """(root log names that exist after a root-level ledger, logs/ names that exist)."""
    assert not any((ROOT / n).exists() for n in NAMES), "a root log exists before the check"
    probe = ROOT / "_root_logs_probe.jsonl"
    real = narrate.log_beside
    if plant:
        narrate.log_beside = lambda path, name: path.with_name(name)
    try:
        led = ledger.Ledger(probe)
        led.close()
        made = [n for n in NAMES if (ROOT / n).exists()]
        in_logs = [n for n in NAMES if (ROOT / "logs" / n).exists()]
    finally:
        narrate.log_beside = real
        probe.unlink(missing_ok=True)
        for n in made if "made" in locals() else NAMES:
            (ROOT / n).unlink(missing_ok=True)       # only files this check created
    return made, in_logs


def main() -> int:
    made, in_logs = at_root(False)
    print(f"   root files {made}; logs/ {in_logs}")
    ok = not made and sorted(in_logs) == sorted(NAMES)
    print("RL1 a root-level ledger writes its logs to logs/: " + ("GREEN" if ok else "RED"))
    assert ok
    made_p, _ = at_root(True)
    print(f"   the plant (beside the ledger): root files {made_p}")
    print("MF-RL1 the old rule writes the root files: " + ("RED" if made_p
                                                          else "GREEN (the plant went unseen)"))
    assert made_p
    d = Path(tempfile.mkdtemp(prefix="rl_"))
    led = ledger.Ledger(d / "run.jsonl")
    led.close()
    ok2 = all((d / n).exists() for n in NAMES)
    print("RL2 a ledger elsewhere keeps its logs beside it: " + ("GREEN" if ok2 else "RED"))
    assert ok2
    print("root_logs: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
