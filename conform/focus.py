"""focus: the ground is the only metric, made into a check that fires.

Every commit names which LEVEL its subject sits at. This is the reviewer's axis (2026-09-12),
and it REPLACES the earlier contact/instrument one because that one was too coarse: it filed a
measurement ABOUT THE AGENT (legitimate) in the same bucket as channel plumbing (the drift). The
separating line is the SUBJECT, not the register:

    Focus: L1 <agent facet>   the agent -- what it perceives, binds, composes, does
    Focus: L2 <what>          the record OF the agent -- censuses, corpus reads, meta-findings
    Focus: L3 <what>          the record OF THE RECORD -- the workbook, the splits, the publish path

Keep everything at L1. L2/L3 is allowed only where it states a law that transfers off this
project -- and it is COUNTED, because the drift that removed the last agent was accumulation away
from L1: never invisible, just never counted (reviewer, 2026-09-12). A note after the level is
required, so a bare level cannot be rubber-stamped.

Two jobs, and only one of them blocks:

    python focus.py --streak     report the non-L1 streak. NEVER exits non-zero.
    python focus.py --msg FILE   enforce against an incoming commit message. Exits 1 to block.

The block lives here and not in check.py on purpose: pre-commit runs BEFORE the commit that
would clear the streak exists, so a blocking seat there cannot be cleared and deadlocks. The
commit-msg hook sees the incoming classification, so it can. See CLAUDE.md 'THE GROUND-FOCUS SEAT'.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).parent.parent

# anchor: a DECLARED CONVENTION, not a measurement -- the seat authors it (Figure 10) and the
# reviewer moves it. Set so a short off-agent run passes and a stall is caught long before the
# 45 that prompted this. It is not claimed correct; it is claimed visible and movable.
STALL = 5

_TRAILER = re.compile(r"^Focus:\s*L([123])\b(.*)$", re.M | re.I)
_EXEMPT = re.compile(r"^(Merge|Revert|fixup!|squash!|amend!)\b")


def classify(msg: str) -> tuple[int | None, str]:
    """(level, note). level is 1/2/3, or None when there is no trailer -- the pre-convention
    state, which is also the legacy boundary the streak stops at."""
    m = _TRAILER.search(msg)
    if not m:
        return None, ""
    return int(m.group(1)), m.group(2).strip(" -:—\t")


def streak() -> int:
    """Consecutive most-recent commits at L2 or L3, counted back until the first L1 or the first
    commit with no level at all -- the legacy boundary, so pre-convention commits do not count and
    the streak starts clean."""
    out = subprocess.run(
        ["git", "log", "-n", "80", "--format=%B%x1e"],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout
    n = 0
    for entry in out.split("\x1e"):
        if not entry.strip():
            continue
        level, _note = classify(entry)
        if level is None or level == 1:
            break
        n += 1
    return n


def enforce(path: str) -> int:
    msg = Path(path).read_text(encoding="utf-8")
    first = next((ln for ln in msg.splitlines() if ln.strip()), "")
    if _EXEMPT.match(first):
        return 0
    level, note = classify(msg)
    if level is None:
        print("FOCUS: commit has no `Focus:` level trailer. Add exactly one, with a note:\n"
              "  Focus: L1 <agent facet>   the agent -- perceives, binds, composes, does\n"
              "  Focus: L2 <what>          the record OF the agent -- censuses, corpus reads\n"
              "  Focus: L3 <what>          the record OF THE RECORD -- workbook, publish path")
        return 1
    if not note:
        print(f"FOCUS: L{level} needs a note after it -- name the subject in a few words. "
              f"A bare level cannot be rubber-stamped.")
        return 1
    if level == 1:
        return 0
    # L2/L3: off the agent. Allowed until the streak reaches the stall, then cleared or escalated.
    s = streak()
    if s >= STALL and not re.search(r"escalat", msg, re.I):
        print(f"FOCUS: {s} commits off the agent (L2/L3) since the last L1, and the ground is "
              f"unchanged at the binding-starvation break.\n"
              f"The drift that removed the last agent was accumulation away from L1. Either move "
              f"this commit to L1 -- the agent: what it perceives, binds, composes, does -- or "
              f"escalate to the reviewer through the workbook and write 'escalated' in the msg.")
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--msg" in argv:
        i = argv.index("--msg")
        return enforce(argv[i + 1])
    # --streak, and the default: report, never block.
    s = streak()
    mark = "  <-- STALL, next off-agent commit is refused" if s >= STALL else ""
    print(f"focus: {s} commits off the agent (L2/L3) since last L1 (stall {STALL}){mark}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
