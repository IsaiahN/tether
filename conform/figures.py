"""figures: an INDEX entry from F506 on must carry a FIGURE CENSUS (Isaiah, 2026-10-07).

    python conform/figures.py      self-test, then every entry from F506 on; exit 1 on any refusal

*"the tether figures dictate logic and decisions"* -- so every proposal and ruling carries a census:
the figures that bear, QUOTED from the SVG text and named, and any figure strained. A block counts
when it has the header, at least one named figure with a quoted fragment, and a strained line.
Entries written before the rule are annotated forward, never rewritten, so they are not judged.
The self-test runs every time: a seat whose refusal is never exercised cannot be told from one
that cannot refuse.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
# anchor: the first entry after the rule (2026-10-07); earlier ones are annotated, not judged.
FIRST = 506
_ENTRY = re.compile(r"^#### F(\d+)\b", re.M)
_QUOTED = re.compile(r"(?:Fig(?:ure)?\.?\s*\d+|(?:Operators|Symbols) table)"
                     r"[^\n]*?\"[^\"\n]{3,}\"")


def entries(text: str) -> list[tuple[int, str]]:
    marks = list(_ENTRY.finditer(text))
    ends = [m.start() for m in marks[1:]] + [len(text)]
    return [(int(m.group(1)), text[m.start():e]) for m, e in zip(marks, ends, strict=True)]


def lacks(body: str) -> str | None:
    """None when the entry carries a census, else what is missing."""
    i = body.find("FIGURE CENSUS")
    if i < 0:
        return "no FIGURE CENSUS block"
    block = body[i:]
    if not _QUOTED.search(block):
        return "the census quotes no figure"
    if not re.search(r"strain", block, re.I):
        return "the census does not say what it strains (or 'none strained')"
    return None


def check(text: str) -> list[str]:
    return [f"F{n}: {why}" for n, body in entries(text) if n >= FIRST and (why := lacks(body))]


def selftest() -> None:
    bare = "#### F900 -- a ruling with no census.\n\nbody\n"
    good = ('#### F901 -- a ruling.\n\n**FIGURE CENSUS.** Fig 2 -- "the ground is the anchor". '
            "None strained.\n")
    old = "#### F12 -- an entry from before the rule.\n\nbody\n"
    assert check(bare) == ["F900: no FIGURE CENSUS block"], check(bare)
    assert check(good) == [], check(good)
    assert check(old) == [], check(old)


if __name__ == "__main__":
    selftest()
    bad = check((ROOT / "docs" / "INDEX.md").read_text(encoding="utf-8"))
    for b in bad:
        print(b)
    print(f"figures: {len(bad)} entries from F{FIRST} on without a census" if bad
          else f"figures: every entry from F{FIRST} on carries a census")
    sys.exit(1 if bad else 0)
