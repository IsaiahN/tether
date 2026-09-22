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


def window(title: str, per_cycle: list[int]) -> str:
    """The measurement WINDOW against the cycles that were actually live. Raises on a dead window.

    REVIEWER, 2026-09-22, ruling 3, after the fifth instrument fault. A resolution census ran
    `sk48` for 6 cycles and read ZERO CALLS on both arms -- and `F274` had already established
    that sk48 does nothing before cycle 7, so the entire window sat inside the dead zone. **The
    reading was "the shape atoms are never called". The truth was "this window contains no
    cycle in which anything happens."**

    **A ZERO FROM A DEAD WINDOW IS NOT A NULL, IT IS A NON-MEASUREMENT** -- and it presents as
    the stronger claim, which is the same asymmetry the over-claiming-a-null law names: a null
    needs no defence, so nobody asks it for one.

    `per_cycle` is any per-cycle activity count the caller already has -- calls, mints, lookups.
    It does not matter which, only that a live cycle is distinguishable from a dead one.
    """
    live = [i for i, n in enumerate(per_cycle, 1) if n]
    lines = [f"  {title}",
             f"    window        {len(per_cycle)} cycles",
             f"    live cycles   {len(live)}",
             f"    first live    {live[0] if live else '--'}"]
    if not live:
        lines.append("    DEAD WINDOW   no cycle did anything -- this is a NON-MEASUREMENT")
        print("\n".join(lines))
        raise SplitError(f"{title}: the window contains no live cycle, so a zero here is a "
                         f"property of the window and not of the mechanism")
    return "\n".join(lines)


def progress(i: int, of: int, count: int, cumulative: int, t0: float) -> None:
    """ONE FLUSHED LINE PER CYCLE. Reviewer, 2026-09-22, made standard for every measurement
    script so it is not re-decided per script.

    **A LONG MEASUREMENT THAT CANNOT REPORT PROGRESS IS A GAMBLE ON IT FINISHING, and a silent
    run is indistinguishable from a hung one.** A 15-cycle census on `sk48` printed everything
    after its loop, **went dark for ~50 minutes, and had no partial answer to read when it had
    to be killed.** Restarted with this line, **the question it was run for was answered in ONE
    SECOND by cycle 1** -- and the cycles after it carried `F290`, which was not the question.

    So it is not only an ergonomic: **the partial output IS the finding more often than the
    total is.** A run reporting nothing until it completes cannot be read early, cannot be
    stopped on a sufficient answer, and loses everything if it is stopped at all.
    """
    import sys as _s
    import time as _t
    print(f"  cycle {i:3d}/{of}  calls {count:12,d}  cumulative {cumulative:14,d}  "
          f"{_t.time() - t0:6.0f}s", flush=True)
    _s.stdout.flush()


def resolution(title: str, per_atom: dict) -> str:
    """EVERY ATOM THAT NEVER RESOLVED, NAMED, BEFORE ANY RESULT. Reviewer, 2026-09-22.

    `per_atom` maps atom name -> (resolved, not_resolved).

    **THREE ATOMS WERE FOUND DEAD IN TWO TICKS AND ALL THREE WERE INVISIBLE**: `holes` (omitted
    from arm I's decode by a closure boundary), `area` and `centroid` (reading `rec["cells"]`,
    a key no site writes). Each returned NOT_RESOLVED on 100% of its calls, **and a
    NOT_RESOLVED atom is indistinguishable from an atom that legitimately abstains** -- which
    is the write-site law in its perception form: reading zero, the record cannot tell you
    whether the thing is broken, perfect, or absent.

    **IT REPORTS RATHER THAN RAISES, AND THAT IS DELIBERATE.** A never-resolving atom does not
    invalidate the run the way an unaccounted split invalidates a percentage -- it may be
    genuinely inapplicable to the board. What it must not be is SILENT. **What DOES raise is
    calling this with nothing**, because a run that did not take the census cannot claim the
    atoms were checked.

    Atoms with ZERO CALLS are listed apart: never-reached and never-resolving are different
    findings, and merging them is how "not called" would read as "broken".
    """
    if not per_atom:
        raise SplitError(f"{title}: the resolution census is empty -- a run that did not take "
                         f"it cannot report that its atoms resolved")
    # THE SHAPE IS CHECKED BEFORE IT IS UNPACKED, AND THIS GUARD EXISTS BECAUSE IT FAILED.
    # 2026-09-22: the declared step-1 run passed `{"resolved": n, "NOT_RESOLVED": m}` where a
    # 2-tuple was documented. A 2-key dict UNPACKS -- into its KEYS -- so `ok` became the
    # string `"resolved"`, `ok == 0` was never true, `ok + no == 0` was never true, and the
    # census printed **"never-resolved none, zero calls none" WHATEVER THE DATA SAID.**
    # A guard that cannot fail loudly hands out a clean bill of health from a blind
    # instrument, which is the exact confabulation this module was built to stop -- one
    # level up, in the module itself.
    for name, v in per_atom.items():
        ints = (isinstance(v, (tuple, list)) and len(v) == 2
                and all(type(x) is int for x in v))
        if not ints:
            raise SplitError(
                f"{title}: atom {name!r} maps to {v!r}; resolution() takes "
                f"(resolved, not_resolved) as two ints. A dict unpacks into its KEYS and "
                f"this census would have read as clean.")
    dead, uncalled, live = [], [], []
    for name, (ok, no) in sorted(per_atom.items()):
        if ok + no == 0:
            uncalled.append(name)
        elif ok == 0:
            dead.append((name, no))
        else:
            live.append((name, ok, ok + no))
    lines = [f"  {title}", f"    atoms in census {len(per_atom)}"]
    if dead:
        lines.append("    NEVER RESOLVED (broken, unreached, or absent -- named, not silent):")
        lines += [f"      {n:<16} 0 of {no} calls" for n, no in dead]
    else:
        lines.append("    never-resolved  none")
    note = "   <-- not reached is NOT the same finding as not resolving" if uncalled else ""
    lines.append(f"    zero calls      {', '.join(uncalled) if uncalled else 'none'}{note}")
    lines += [f"    {n:<16} {ok}/{tot} resolved" for n, ok, tot in live]
    return "\n".join(lines)


def _selftest() -> int:
    """REINTRODUCE THE DEFECT, NEVER DISABLE THE CHECK. Each case is one real fault."""
    bad = 0

    # THE FALSE ALL-CLEAR, 2026-09-22: a dict where a 2-tuple belongs. It unpacked into its
    # KEYS and the census reported "never-resolved none" over data full of dead atoms.
    try:
        resolution("dict instead of a tuple", {"holes": {"resolved": 0, "NOT_RESOLVED": 40}})
        print("census: a dict-shaped resolution census was ACCEPTED -- the false all-clear")
        bad += 1
    except SplitError:
        pass
    # and the shape it does take must still work, with the dead atom NAMED
    got = resolution("real census", {"holes": (0, 40), "area": (0, 0), "corners": (12, 12)})
    if "holes" not in got or "NEVER RESOLVED" not in got:
        print("census: a genuinely dead atom was not named")
        bad += 1
    if "area" not in got:
        print("census: a zero-call atom was not listed apart")
        bad += 1

    # `progress` is exercised here rather than only by measurement scripts, which live outside
    # the repo -- the ISOLATED seat is right that a helper with no caller in-tree is dead code.
    import time as _t
    progress(1, 3, 1242, 1242, _t.time())

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

    # THE FIFTH FAULT: a 6-cycle window on a board that is dead until cycle 7.
    try:
        window("sk48 as first measured", [0, 0, 0, 0, 0, 0])
        print("census: a DEAD WINDOW was accepted")
        bad += 1
    except SplitError:
        pass
    live = window("a window with live cycles", [0, 0, 3, 7, 0, 2])
    if "first live    3" not in live or "live cycles   3" not in live:
        print("census: a live window did not report its first live cycle and count")
        bad += 1

    # THE THREE DEAD ATOMS, as the census would have shown them before any result.
    blk = resolution("as it stood two ticks ago",
                     {"holes": (0, 3140), "area": (0, 0), "centroid": (0, 0),
                      "bbox_area": (62448, 62448)})
    if "holes" not in blk or "0 of 3140" not in blk:
        print("census: a never-resolving atom was not named")
        bad += 1
    if "area, centroid" not in blk:
        print("census: zero-call atoms were not listed apart from never-resolving ones")
        bad += 1
    try:
        resolution("a run that skipped it", {})
        print("census: an EMPTY resolution census was accepted")
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
