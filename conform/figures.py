"""figures: an INDEX entry from F506 on must carry a FIGURE CENSUS (Isaiah, 2026-10-07).

    python conform/figures.py      self-test, then every entry from F506 on; exit 1 on any refusal

*"the tether figures dictate logic and decisions"* -- so every proposal and ruling carries a census:
the figures that bear, QUOTED from the SVG text and named, and any figure strained. A block counts
when it has the header, at least one named figure with a quoted fragment, and a strained line.
Entries written before the rule are annotated forward, never rewritten, so they are not judged.
The self-test runs every time: a seat whose refusal is never exercised cannot be told from one
that cannot refuse.

AND FROM F517 ON, A DERIVATION BEFORE THE CONCLUSION (Isaiah's priority, 2026-10-09; the reviewer
12:09Z P3). A census written after the conclusion cannot refuse it: the reviewer's 11:29Z "one
bargain" stood until a derivation was asked for, and Fig 12 refused it. So an entry opens a
DERIVATION block -- at least one quoted figure or formula line -- before any CONCLUSION or RULING
block and before its FIGURE CENSUS. Procedure: .claude/skills/tether-derive-first/SKILL.md.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
# anchor: the first entry after the rule (2026-10-07); earlier ones are annotated, not judged.
FIRST = 506
# anchor: the first entry after the derive-first priority (2026-10-09); earlier ones are not judged.
FIRST_DERIVATION = 517
_ENTRY = re.compile(r"^#### F(\d+)\b", re.M)
_QUOTED = re.compile(r"(?:Fig(?:ure)?\.?\s*\d+|(?:Operators|Symbols) table)"
                     r"[^\n]*?\"[^\"\n]{3,}\"")
_FORMULA = re.compile(r"formula[^\n]*?\"[^\"\n]{3,}\"", re.I)
# a block label at the start of a line (bold or not): the entry's own structure, never prose
_DERIVATION = re.compile(r"^[ *]*DERIVATION\b", re.M)
_CONCLUSION = re.compile(r"^[ *]*(?:CONCLUSION|RULING)\b", re.M)


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


def lacks_derivation(body: str) -> str | None:
    """None when a DERIVATION block quoting a figure or formula line comes before the conclusion
    and before the census, else what is wrong."""
    d = _DERIVATION.search(body)
    if not d:
        return "no DERIVATION block before the conclusion"
    census = body.find("FIGURE CENSUS")
    if 0 <= census < d.start():
        return "the DERIVATION comes after the FIGURE CENSUS"
    concl = _CONCLUSION.search(body)
    if concl and concl.start() < d.start():
        return "the DERIVATION comes after the conclusion"
    ends = [x for x in (census, concl.start() if concl else -1) if x > d.start()]
    block = body[d.start():min(ends) if ends else len(body)]
    if not (_QUOTED.search(block) or _FORMULA.search(block)):
        return "the DERIVATION quotes no figure or formula line"
    return None


def check(text: str) -> list[str]:
    out = []
    for n, body in entries(text):
        if n >= FIRST and (why := lacks(body)):
            out.append(f"F{n}: {why}")
        if n >= FIRST_DERIVATION and (why := lacks_derivation(body)):
            out.append(f"F{n}: {why}")
    return out


def selftest() -> None:
    # the census rule alone: numbered between FIRST and FIRST_DERIVATION
    bare = "#### F510 -- a ruling with no census.\n\nbody\n"
    good = ('#### F511 -- a ruling.\n\n**FIGURE CENSUS.** Fig 2 -- "the ground is the anchor". '
            "None strained.\n")
    old = "#### F12 -- an entry from before the rule.\n\nbody\n"
    assert check(bare) == ["F510: no FIGURE CENSUS block"], check(bare)
    assert check(good) == [], check(good)
    assert check(old) == [], check(old)
    # the derivation rule, from FIRST_DERIVATION on
    census = '\n**FIGURE CENSUS.** Fig 2 -- "the ground is the anchor". None strained.\n'
    derived = '**DERIVATION.** Fig 9 -- "Residual first, frame second."\n\n'
    no_deriv = "#### F950 -- a ruling.\n\nRULING: do it.\n" + census
    late = "#### F951 -- a ruling.\n" + census + derived
    after = "#### F954 -- a ruling.\n\nRULING: do it.\n" + derived + census
    empty = "#### F952 -- a ruling.\n\n**DERIVATION.** it follows.\n\nRULING: do it.\n" + census
    right = "#### F953 -- a ruling.\n\n" + derived + "RULING: do it.\n" + census
    assert check(no_deriv) == ["F950: no DERIVATION block before the conclusion"], check(no_deriv)
    assert check(late) == ["F951: the DERIVATION comes after the FIGURE CENSUS"], check(late)
    assert check(after) == ["F954: the DERIVATION comes after the conclusion"], check(after)
    assert check(empty) == ["F952: the DERIVATION quotes no figure or formula line"], check(empty)
    assert check(right) == [], check(right)


if __name__ == "__main__":
    selftest()
    bad = check((ROOT / "docs" / "INDEX.md").read_text(encoding="utf-8"))
    for b in bad:
        print(b)
    print(f"figures: {len(bad)} entries from F{FIRST} on without a census" if bad
          else f"figures: every entry from F{FIRST} on carries a census")
    sys.exit(1 if bad else 0)
