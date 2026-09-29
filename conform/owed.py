"""owed: every check that currently passes WITHOUT HAVING CHECKED ANYTHING.

**ISAIAH, 2026-09-29, ruling 6:** *unrunnable / vacuous checks count as passing for now, but
must be regression-tested post hoc once ARC boards return. Keep a list of them so that is
possible.*

**THE LIST IS GENERATED, NOT WRITTEN DOWN, AND THAT IS THE WHOLE POINT.** A hand-kept list of
what is currently vacuous is stale the moment a check starts or stops examining rows, and it
would go stale SILENTLY -- the same failure as the thing it tracks. `lint` and `kernel` already
classify every check and then print only the COUNTS; the names sit in the result dicts and
nobody was reading them.

    VACUOUS      it ran and examined NOTHING -- zero rows, zero candidates
    UNRUNNABLE   the record lacks the field it needs
    SUPPRESSED   deliberately held off

**A GREEN SUITE CONTAINING VACUOUS CHECKS IS NOT A LIE, BUT IT IS NOT THE CLAIM A READER TAKES
FROM IT EITHER.** This makes the difference legible without turning the suite red -- which is
what Isaiah ruled: they count as passing FOR NOW.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.dont_write_bytecode = True

NOT_A_READING = ("VACUOUS", "UNRUNNABLE", "SUPPRESSED")


def collect() -> dict[str, list[tuple[str, str]]]:
    """Name every check whose status is not a reading. `{source: [(id, why), ...]}`."""
    out: dict[str, list[tuple[str, str]]] = {}
    import lint
    res = lint.run([Path(p) for p in sorted(Path(".").glob("*.py"))])
    # **NOT EVERY VALUE IS A `{status, why}` DICT** -- some entries are plain lists, so a bare
    # `.get` raises. Found by running it, not by reading a type hint. A non-dict cannot BE
    # vacuous, so it is skipped rather than guessed at.
    out["lint"] = sorted(
        (rid, "; ".join(d.get("why", ()))[:90])
        for rid, d in res.items()
        if isinstance(d, dict) and d.get("status") in NOT_A_READING)
    return out


def main() -> int:
    found = collect()
    total = sum(len(v) for v in found.values())
    print("  checks that pass WITHOUT having checked anything -- ruling 6's list")
    print("")
    for src, items in sorted(found.items()):
        print(f"  {src}: {len(items)}")
        for cid, why in items:
            print(f"      {cid:<28} {why}")
    print("")
    if total:
        print(f"  {total} owed a re-run when the board stop lifts.")
    else:
        print("  lint: none -- every static check examined something.")
    # **A ZERO FROM A NARROW REPORTER READS LIKE A ZERO FROM A WIDE ONE, SO THE SCOPE PRINTS.**
    # `lint` is STATIC: it scans source, always has candidates, and will almost never be
    # vacuous. The checks the board stop actually silences are elsewhere --
    #   kernel  classifies UNRUNNABLE/VACUOUS/UNIMPL but needs a RUN FILE to classify against,
    #           and an ARC run is precisely what is stopped
    #   arc_*   forbidden entirely by the stop; nothing to enumerate from here
    # So a zero here means THE STATIC LAYER IS CLEAN, never *nothing is owed*.
    print("")
    print("  SCOPE: static `lint` only. `kernel` needs a run file, and the ARC paths cannot")
    print("  run under the stop -- both are OUT of this count. A zero here means the static")
    print("  layer is clean, NOT that nothing is owed.")
    # **NEVER A FAILING EXIT.** Isaiah ruled these count as passing for now; a red gate here
    # would be this seat overriding him. It REPORTS, as the focus streak does.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
