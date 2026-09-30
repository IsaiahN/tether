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


# ======================================================================================
# MOVED HERE INTACT UNDER RULING 6 -- Isaiah, 2026-09-30. NOT DELETED, NOT LOOSENED.
#
# These passed only on a PHANTOM-PADDED SCOPE. `_wide` appended four members no object
# carries; of the five failing at 0.8333 exactly ONE was real. Measured: with the phantoms
# gone the routine is refused UPSTREAM on both arms -- OFF because the objective is already
# satisfied (discrepancy 0), ON because there is no objective at all. Neither arm reaches
# the bargain, so `cost`, `left` and `base` are never computed.
#
# **ROUTINE FORMATION AGAINST A REAL GAP IS THEREFORE UNSHOWN**, and a green check asserting
# it was reading a gap made of members nothing can satisfy. Owed to the capability checkup
# after Phase 2 / ARC, when a world with a real gap exists.
#
# Two things moved: the function below, and the `"routine"` case of
# `check_the_suite_reaches_the_hard_cases` (the `routine_cut` and `routine_refused` cases
# STAY in the suite -- those are reached honestly).
#
# AND A NOTE ON WHERE THIS SITS. This file's own rule is that its LIST is generated and
# never hand-kept, because a hand-kept list goes stale silently. That rule is about
# `collect()`, which reads `lint`'s statuses. A check MOVED out of the suite is different:
# its presence here IS the record, it cannot go stale while it is the only copy, and
# `main()` names it below so a reader of the report sees it beside the generated entries.
# ======================================================================================

OWED_CHECKS = {
    "check_strategy_is_emitted_when_a_routine_drives":
        "passed only on a phantom-padded scope; routine formation against a REAL gap is "
        "unshown; owed to the capability checkup after Phase 2 / ARC",
    "check_the_suite_reaches_the_hard_cases::routine":
        "the `routine` coverage case only; reached solely via the phantom scope. "
        "`routine_cut` and `routine_refused` remain in the suite",
}


def check_strategy_is_emitted_when_a_routine_drives():
    """DEFECT: a multi-step plan executing and being counted as an uninformed probe.

    §22.2 reads transfer off a THREE-phase mix, and `STRATEGY` was structurally zero because
    nothing produced routines. Once one drives an action, a zero there is a gap rather than an
    honest reading -- which is what `tether.py`'s own comment said would happen.
    """
    # ITS HELPERS COME WITH IT, so the check is RUNNABLE where it sits rather than being a
    # quotation. A moved check that cannot be executed is a comment, and a comment is what
    # ruling 6 exists to avoid -- the point is to re-run it, not to remember it.
    from test_m2 import _agent, _wide
    ag = _agent()
    _wide(ag)
    for _ in range(8):
        ag.step()
    mix = ag.phases.report()["total"]
    assert mix.get("strategy", 0) > 0, f"a routine drove and the mix says {mix}"


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
    # **DISCOVERED AND RUN, NOT LISTED -- the reviewer, 2026-09-30, holding this addition to
    # the file's own rule.** `OWED_CHECKS` began as a hand-written name map, which is the
    # staleness this module exists to refuse: rename the function and the map still names the
    # old one, silently. So the functions are ENUMERATED from the module and EXECUTED, and a
    # moved check with no label is REPORTED rather than passed over -- the one failure a
    # hand-kept map cannot have.
    moved = {k: v for k, v in globals().items()
             if k.startswith("check_") and callable(v)}
    print(f"  MOVED OUT OF A SUITE UNDER RULING 6: {len(moved)} discovered, and RUN")
    unlabelled = []
    for name in sorted(moved):
        why = OWED_CHECKS.get(name)
        if why is None:
            unlabelled.append(name)
            why = "!! NO LABEL -- moved here without saying what it is owed for"
        try:
            moved[name]()
            verdict = "passes here TODAY (on the world it was moved off)"
        except AssertionError as exc:
            verdict = f"fails here: {str(exc)[:60]}"
        except Exception as exc:                      # noqa: BLE001
            verdict = f"DID NOT RUN -- {type(exc).__name__}: {str(exc)[:50]}"
        print(f"      {name}")
        print(f"          {why}")
        print(f"          -> {verdict}")
    # a label with no function is the other half of the same staleness
    orphans = [k for k in OWED_CHECKS if "::" not in k and k not in moved]
    for k in orphans:
        print(f"      {k}")
        print("          !! LABELLED BUT ABSENT -- no such function in this module")
    for k, why in sorted(OWED_CHECKS.items()):
        if "::" in k:                                  # a CASE inside a check that stays
            print(f"      {k}")
            print(f"          {why}")
            print("          -> a case, not a function; re-run with its parent check")
    if unlabelled or orphans:
        print("")
        print("  !! the moved set and its labels DISAGREE -- fix before trusting this list")
    print("")
    print("  SCOPE: static `lint` only. `kernel` needs a run file, and the ARC paths cannot")
    print("  run under the stop -- both are OUT of this count. A zero here means the static")
    print("  layer is clean, NOT that nothing is owed.")
    # **NEVER A FAILING EXIT.** Isaiah ruled these count as passing for now; a red gate here
    # would be this seat overriding him. It REPORTS, as the focus streak does.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
