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
     "an invariant broke on a generated history for the REFERENCE loop",
     HERE / "stateful.py"),
    ("shipped", [str(PY), str(HERE / "stateful.py"), "--fast", "--tether"],
     "an invariant broke on a generated history for tether.Agent",
     HERE / "stateful.py"),
    # THE SPLIT GUARD. Its own defect suite, run for the reason the M2 note below gives: a
    # suite nothing runs is a suite that rots. Each case REINTRODUCES one of the three
    # instrument faults of 2026-09-22, the sharpest being a split whose branches collapsed
    # into the total and printed percentages that read like a finding.
    ("census", [str(PY), "census.py"],
     "the split guard stopped refusing a split that does not account for its population",
     ROOT / "census.py"),
    ("demo", [str(PY), "demo.py"], "the loop did not complete", ROOT / "demo.py"),
    ("gate", [str(PY), "gate.py", "runs/demo.jsonl"],
     "the record is not well-formed", ROOT / "gate.py"),
    ("tests", [str(PY), "test_gate.py"],
     "the gate's own defect suite regressed", ROOT / "test_gate.py"),
    # A SUITE THAT NO SEAT RUNS IS A SUITE THAT ROTS, and this one sat outside the gate for
    # six commits while every one of them reported `8/8 seats clean`. The M2 checks each
    # CONSTRUCT the defect they guard against and each has been shown to fail when its
    # mechanism is removed -- which is worth exactly nothing if nothing runs them.
    ("m2", [str(PY), "test_m2.py"],
     "an M2_STANDARD mechanism regressed, or its tripwire fired", ROOT / "test_m2.py"),
    ("percept", [str(PY), "test_perception.py"],
     "a perception detector regressed (Contain/Topology/perimeter/background)",
     ROOT / "test_perception.py"),
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

    # THE GROUND-FOCUS LINE. Deliberately NOT a seat in STAGES: it must never make this
    # process exit non-zero, because pre-commit runs before the commit that would clear the
    # streak exists, so a blocking focus seat here would deadlock. It only ever reports. The
    # block lives in the commit-msg hook. See conform/focus.py and CLAUDE.md.
    foc = subprocess.run([str(PY), str(HERE / "focus.py"), "--streak"],
                         cwd=ROOT, capture_output=True, text=True)
    focus_line = (foc.stdout or foc.stderr).strip()

    if "--hook" in argv:
        if not bad:
            line = f"check: {len(results)}/{len(results)} seats clean"
        else:
            line = "check: " + " | ".join(f"{n} {s}" for n, s, _d, _w in bad)
        if focus_line:
            line = f"{line} | {focus_line}"
        print(json.dumps({"systemMessage": line}))
        return 0                      # report, never block the turn from ending

    for name, status, detail, why in results:
        print(f"  {name:<8} {status}")
        if status == "FAIL":
            print(f"           {why}")      # a cause, and only when one was observed
        if detail:
            print(f"           {detail}")
    # THE THREE STATES SURVIVE INTO THE SUMMARY. Inside a seat, `found something`,
    # `could not check everything` and `never ran` are kept apart on purpose; folding
    # them into clean-vs-not put INCOMPLETE back on the side of a finding, which is the
    # exact reading it was added to prevent.
    n_found = sum(1 for _n, s, _d, _w in results if s == "FAIL")
    print(f"\n  {len(results) - len(bad)}/{len(results)} seats clean, "
          f"{n_found} found something")
    for state, note in (("INCOMPLETE", "ran and could not check everything, which is "
                                       "not a finding about the code."),
                        ("DID-NOT-RUN", "has not passed; it was not asked.")):
        n = sum(1 for _n, s, _d, _w in results if s == state)
        if n:
            print(f"  {n} stage(s) reported {state}: {note}")
    if focus_line:
        print(f"  {focus_line}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
