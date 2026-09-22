"""THE SPLIT GUARD: a measured percentage is not reportable without its branch accounting.

REVIEWER, 2026-09-22, after THREE instrument faults in one tick -- all caught by reading the
output, none by a checker:

  - a comparison between two instruments that had NO CONSUMER (agreement between a
    cascade-walked tracker and a settled-only one -- names are arbitrary labels, so the
    disagreement cost nothing and the 42-77% it produced would have killed a build);
  - a depth histogram that was a property of the PARSE rather than of the boards;
  - a moved/held split where the `moved` branch was never populated, so every row fell into
    `held` and THE BRANCH FIGURE WAS THE OVERALL RATE RELABELLED.

**The third is the one this file exists for, because it reads like a result.** A split whose
branches collapse into the total prints percentages that look exactly like a clean finding where
the two populations happen to agree. It was caught only because the empty branch printed `n=0`
next to nothing at all -- had it printed no row, the number would have shipped.

THE RULE: before any percentage, print n in every branch, show the branches sum to the total,
flag any empty branch, and give the population IN and OUT. **If those lines are missing, the
number is not reportable.**

This is the one helper, so the checks are not re-typed per script and cannot drift between them.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True


class SplitError(AssertionError):
    """A split that does not account for its population. Raised, never warned.

    A WARNING WOULD DEFEAT THE PURPOSE. The faults this guards against all produced output that
    read as a finding; a line saying `warning: branch empty` above a plausible percentage is a
    line that gets skimmed. The number must not exist.
    """


def split(title: str, total: int, branches: dict[str, int],
          excluded: int = 0, why_excluded: str = "") -> str:
    """The branch accounting for one split, as a printable block. Raises if it does not add up.

    `total` is the population IN. `branches` must partition it exactly. `excluded` is the
    population dropped before the split, and it must be NAMED -- an exclusion without a reason
    is the boundary that goes quiet, and `conform/lint.py` records it as the second way a
    checker falls silent.
    """
    got = sum(branches.values())
    lines = [f"  {title}", f"    population IN {total}"]
    if excluded or why_excluded:
        if not why_excluded:
            raise SplitError(f"{title}: {excluded} excluded with no reason given")
        lines.append(f"    excluded      {excluded}  ({why_excluded})")
    for name, n in branches.items():
        lines.append(f"    {name:<24} n={n}")
    lines.append(f"    branches sum  {got}  {'==' if got == total else '!='} total {total}")

    empty = [k for k, v in branches.items() if v == 0]
    if empty:
        lines.append(f"    EMPTY BRANCH  {', '.join(empty)}  <-- the split did not run")
    if got != total:
        raise SplitError(f"{title}: branches sum to {got}, population is {total}")
    if empty:
        raise SplitError(f"{title}: empty branch(es) {empty} -- a split that collapses into "
                         f"its own total reads like a result")
    return "\n".join(lines)


def rate(name: str, hit: int, of: int) -> str:
    """A percentage WITH the counts that produced it, and the could-have-read-less check.

    A rate reading 100% or 0% must show the denominator could have gone the other way -- the
    standing rule from the seed work, here as a printed line rather than a remembered one.
    """
    if of <= 0:
        raise SplitError(f"{name}: denominator is {of}, so the rate has no subject")
    pct = 100.0 * hit / of
    edge = ""
    if hit == of:
        edge = "  <-- reads 100%: confirm the denominator could have read less"
    elif hit == 0:
        edge = "  <-- reads 0%: confirm the numerator could have read more"
    return f"    {name:<24} {hit}/{of} = {pct:.1f}%{edge}"


def _selftest() -> int:
    """REINTRODUCE THE DEFECT, NEVER DISABLE THE CHECK. Each case is one real fault."""
    bad = 0

    ok = split("control: a real split", 10, {"moved": 4, "held": 6})
    if "branches sum  10  == total 10" not in ok:
        print("census: a valid split did not report its accounting")
        bad += 1

    # THE FAULT THAT SHIPPED: `moved` never populated, everything fell into `held`.
    try:
        split("the collapsed split", 10, {"moved": 0, "held": 10})
        print("census: an EMPTY BRANCH was accepted")
        bad += 1
    except SplitError:
        pass

    # branches that do not account for the population
    try:
        split("a leaking split", 10, {"a": 3, "b": 4})
        print("census: branches that do not sum were accepted")
        bad += 1
    except SplitError:
        pass

    # an exclusion with no reason -- the boundary that goes quiet
    try:
        split("an unnamed exclusion", 8, {"a": 8}, excluded=2)
        print("census: an unexplained exclusion was accepted")
        bad += 1
    except SplitError:
        pass

    if "could have read less" not in rate("all of them", 7, 7):
        print("census: a 100% rate did not carry its check")
        bad += 1
    try:
        rate("no subject", 0, 0)
        print("census: a zero denominator was accepted")
        bad += 1
    except SplitError:
        pass

    print("census: ok" if not bad else f"census: {bad} FAILED")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
