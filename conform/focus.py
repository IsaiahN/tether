"""focus: the ground is the only metric, made into a check that fires.

Every commit declares what it moved, with a trailer:

    Focus: GROUND               levels_completed or traction on the board moved
    Focus: CONTACT -- <claim>   the agent can now reach X it could not; the claim is checkable
    Focus: INSTRUMENT           a measurement, the record, tooling. Not contact.

Two jobs, and only one of them blocks:

    python focus.py --streak     report the instrument-since-contact streak. NEVER exits non-zero.
    python focus.py --msg FILE   enforce against an incoming commit message. Exits 1 to block.

The block lives here and not in check.py on purpose: pre-commit runs BEFORE the commit that
would clear the streak exists, so a blocking seat there cannot be cleared and deadlocks. The
commit-msg hook sees the incoming classification, so it can.

Why this exists: F80..F125 were 45 findings with the ground unchanged at levels 0, and each
looked reasonable alone. The drift was visible only in the sum, and nothing computed the sum.
This computes it. See CLAUDE.md 'THE GROUND-FOCUS SEAT'.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).parent.parent

# anchor: a DECLARED CONVENTION, not a measurement -- the seat authors it (Figure 10) and the
# reviewer moves it. Set so a short instrument run passes and a stall is caught long before the
# 45 that prompted this. It is not claimed correct; it is claimed visible and movable.
STALL = 5

_TRAILER = re.compile(r"^Focus:\s*(GROUND|CONTACT|INSTRUMENT)\b(.*)$", re.M | re.I)
_EXEMPT = re.compile(r"^(Merge|Revert|fixup!|squash!|amend!)\b")


def classify(msg: str) -> tuple[str | None, str]:
    """(kind, claim). kind is None when there is no trailer -- the pre-convention state."""
    m = _TRAILER.search(msg)
    if not m:
        return None, ""
    return m.group(1).upper(), m.group(2).strip(" -:—\t")


def streak() -> int:
    """Consecutive most-recent commits marked INSTRUMENT, counted back until the first
    CONTACT/GROUND or the first commit with no trailer at all -- which is the legacy boundary,
    so the 677 pre-convention commits do not count and the streak starts clean."""
    out = subprocess.run(
        ["git", "log", "-n", "80", "--format=%B%x1e"],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout
    n = 0
    for entry in out.split("\x1e"):
        if not entry.strip():
            continue
        kind, _claim = classify(entry)
        if kind is None or kind in ("CONTACT", "GROUND"):
            break
        n += 1
    return n


def enforce(path: str) -> int:
    msg = Path(path).read_text(encoding="utf-8")
    first = next((ln for ln in msg.splitlines() if ln.strip()), "")
    if _EXEMPT.match(first):
        return 0
    kind, claim = classify(msg)
    if kind is None:
        print("FOCUS: commit has no `Focus:` trailer. Add exactly one:\n"
              "  Focus: GROUND               (levels/traction on the board moved)\n"
              "  Focus: CONTACT -- <claim>   (the agent can now reach X it could not)\n"
              "  Focus: INSTRUMENT           (measurement, record, tooling; not contact)")
        return 1
    if kind == "CONTACT" and not claim:
        print("FOCUS: CONTACT needs a checkable claim after it -- name what the agent can now "
              "reach that it could not. A CONTACT with no claim is an INSTRUMENT wearing the "
              "word.")
        return 1
    if kind in ("CONTACT", "GROUND"):
        return 0
    # INSTRUMENT: allowed until the streak reaches the stall, then it must be cleared or escalated.
    s = streak()
    if s >= STALL and not re.search(r"escalat", msg, re.I):
        print(f"FOCUS: {s} instrument-only commits since the last CONTACT or GROUND, and the "
              f"ground is unchanged at the binding-starvation break.\n"
              f"The answer to too many instruments is the next mechanism the framework names, "
              f"not one more instrument.\n"
              f"Either reclassify this commit as `Focus: CONTACT -- <claim>`, or escalate to the "
              f"reviewer through the workbook and write 'escalated' in the message.")
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--msg" in argv:
        i = argv.index("--msg")
        return enforce(argv[i + 1])
    # --streak, and the default: report, never block.
    s = streak()
    mark = "  <-- STALL, next instrument commit is refused" if s >= STALL else ""
    print(f"focus: instrument-only streak {s} since last contact (stall {STALL}){mark}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
