"""check: run every seat, once, and report what did not run.

    python check.py           human-readable, exit 1 on any failure
    python check.py --hook    one line of JSON for a Claude Code Stop hook

It SHELLS OUT to each component and imports none of them. A checker that imported the
thing it checks would share its state, and the seam is the property that makes the
others worth anything.

Four seats, and they see different things:

    ruff      the layer boundary   TID251 bans -- a domain fact imported by the loop
    lint      the static shape     dead code, unanchored constants, singletons
    kernel    its own record       14 witnessed checks over a live ledger
    gate      the demo's record    12 checks, domain-blind, reading rows only

A stage that could not run is reported as DID-NOT-RUN, never folded into a pass. The
whole point of the exercise was that silence about what was not checked is how a clean
report comes to describe a system nobody checked.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).parent.parent        # the repo, not this folder
HERE = Path(__file__).parent
PY = ROOT / ".venv" / "Scripts" / "python.exe"
if not PY.exists():
    PY = Path(sys.executable)

# (name, argv, what a non-zero exit means, the file it needs). The last field exists
# because FileNotFoundError only fires when the EXECUTABLE is missing: a missing SCRIPT
# starts Python fine and exits non-zero, so it was reported as a stage that ran and found
# something -- with an asserted cause. `gate FAIL -- the record is not well-formed` when
# the truth was that gate.py does not exist.
STAGES = (
    ("ruff", [str(PY), "-m", "ruff", "check", ".", "--exclude", ".venv",
      "--output-format=concise"],
     "a layer boundary crossed, or a lint rule broken", None),
    ("lint", [str(PY), str(HERE / "lint.py")],
     "dead code, an unanchored constant, or a singleton", HERE / "lint.py"),
    ("kernel", [str(PY), str(HERE / "kernel.py")],
     "a conformance check failed against its own record", HERE / "kernel.py"),
    ("stateful", [str(PY), str(HERE / "stateful.py"), "--fast"],
     "an invariant broke on a generated history", HERE / "stateful.py"),
    ("demo", [str(PY), "demo.py"], "the loop did not complete", ROOT / "demo.py"),
    ("gate", [str(PY), "gate.py", "runs/demo.jsonl"],
     "the record is not well-formed", ROOT / "gate.py"),
    ("tests", [str(PY), "test_gate.py"],
     "the gate's own defect suite regressed", ROOT / "test_gate.py"),
)

# stderr from an interpreter that never reached the program. A backstop for the cases a
# path check cannot cover, such as `-m ruff` with ruff uninstalled.
NEVER_STARTED = ("can't open file", "No module named", "cannot find the file")


def run_stage(argv: list[str], needs: Path | None = None) -> tuple[str, str]:
    """(status, detail). DID-NOT-RUN is its own state: a stage that could not start has
    not passed, and folding it into a FAIL asserts a cause that was never observed."""
    if needs is not None and not needs.exists():
        return "DID-NOT-RUN", f"{needs.name} does not exist"
    try:
        p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=120)
    except FileNotFoundError as e:
        return "DID-NOT-RUN", f"{type(e).__name__}: {e}"
    except subprocess.TimeoutExpired:
        return "DID-NOT-RUN", "timed out after 120s"
    if p.returncode == 0:
        return "ok", ""
    if p.returncode == 2:
        # by convention: the stage ran and could not check everything. Not a finding
        # about the code, so the caller must not attach one.
        last = [ln for ln in p.stdout.splitlines() if ln.strip()]
        return "INCOMPLETE", (last[-1].strip() if last else "")[:300]
    if not p.stdout.strip() and any(m in p.stderr for m in NEVER_STARTED):
        return "DID-NOT-RUN", p.stderr.strip().splitlines()[-1][:200]
    # the FINDINGS, not the tail. Every one of these tools prints what it found first
    # and a summary last, so the tail is the least informative part of the output.
    out = [ln.strip() for ln in (p.stdout + p.stderr).splitlines() if ln.strip()]
    hits = [ln for ln in out
            if not ln.startswith(("lint:", "conform:", "Found ", "[*]", "LINTER"))
            and not ln[0].isdigit()]
    return "FAIL", " · ".join(hits[:3])[:400]


def main(argv: list[str]) -> int:
    results = [(name, *run_stage(cmd, needs), why)
               for name, cmd, why, needs in STAGES]
    bad = [r for r in results if r[1] != "ok"]

    if "--hook" in argv:
        if not bad:
            line = f"check: {len(results)}/{len(results)} seats clean"
        else:
            line = "check: " + " | ".join(f"{n} {s}" for n, s, _d, _w in bad)
        print(json.dumps({"systemMessage": line}))
        return 0                      # report, never block the turn from ending

    for name, status, detail, why in results:
        print(f"  {name:<8} {status}")
        if status == "FAIL":
            print(f"           {why}")      # a cause, and only when one was observed
        if detail:
            print(f"           {detail}")
    print(f"\n  {len(results) - len(bad)}/{len(results)} seats clean")
    if any(s == "DID-NOT-RUN" for _n, s, _d, _w in results):
        print("  a stage reported DID-NOT-RUN has not passed; it was not asked.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
