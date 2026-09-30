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
    "test_b5_still_fires_on_the_pinned_world":
        "its PRECONDITION stopped holding under the bargain-fit flip, not its verdict -- "
        "`seed 3 starves no slot`, so the reproduction lost its SUBJECT. Census: 0 of 60 "
        "seeds starve with the flip on, control recovers the pinned pair. NOT inverted: "
        "its own message forbids that without knowing whether the defect is gone or the "
        "trajectory moved past it. Owed a re-pin when a starving world exists",
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
             if k.startswith(("check_", "test_")) and callable(v)}
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



def test_b5_still_fires_on_the_pinned_world():
    """THE B5 REPRODUCTION, PINNED -- and the run shows the mechanism, not just the verdict.

    A strict expected-failure, same shape as the A5 one below: green while B5 truthfully fails,
    red the moment the fix lands, carrying its own invert-me instruction.

    **WHAT THE RUN SHOWS, AND IT RECONCILES TWO READINGS THAT LOOKED OPPOSED.**
    Measured here: `parks on ['s3']`, `probes on ['@probe', '@probe']`.

    Reading the source says the agent matches park to probe correctly -- `mint` adds the parked
    slot to `_starved`, and the flush writes one probe row PER STARVED SLOT. True. But the
    flush is `for slot in sorted(self._starved) or ["@probe"]`, and `@probe` is the fallback
    for an EMPTY `_starved`. Both probes here took it, so `_starved` was empty when they fired.

    That is `F269`'s temporal anti-correlation, visible in one run: *`bored()` is true EARLY,
    when nothing is bound and there is nothing to perturb FOR, and false LATE, which is exactly
    when slots starve.* The park and the probe never coincide, so the per-slot branch the
    repair added cannot be reached and the fallback answers instead.

    SO THE SLOT MISMATCH IS REAL AND IS NOT A LABELLING BUG. Arm M (`TETHER_STARVED_CONTACT`)
    is the built fix: it returns `probe` BEFORE the `bored()` gate whenever `_starved` is
    non-empty, so the flush has a slot to write. Turning it on is an ACTING-PATH change and is
    Isaiah's ruling, not the seat's.
    """
    # ITS IMPORTS COME WITH IT, so it is RUNNABLE here rather than quoted. `kernel` was a
    # module-level import at its old home; it travels inside the function now.
    import kernel

    import snaps
    from gamma import Gamma
    from ledger import Ledger
    from tether import Agent, Config
    from world import bind

    # **THE HAND-WRITTEN WORLD STOPPED STARVING ANYTHING -- 2026-09-28, and it is NOT a fix.**
    # The action-seam work changed which action lands on which step, and with it the one
    # `no_support` park this world produced. Measured by stashing the diff and re-running:
    #
    #     PRE    bad=['B5']   park verdicts {under_floor 7, depth_exhausted 5, no_support 1}
    #     POST   bad=[]       park verdicts {under_floor 7, depth_exhausted 5}
    #     and at 12/15/20/30 steps: still no `no_support`, still no B5
    #
    # **So it is not timing** -- A5's budget fix does not apply. B5's own message offers two
    # readings, *arm M is on* or *the probe now reaches the starved slot*, and NEITHER is true:
    # arm M is off and every probe row still reads `@probe`, the empty-`_starved` fallback.
    # **The reproduction lost its SUBJECT**, which is a third outcome the message does not
    # contemplate -- and the assertion below it is the thing that caught that, so the author
    # foresaw what the message did not.
    #
    # **RE-PINNED BY SEARCHING FOR THE PRECONDITION, NOT FOR THE VERDICT**, and the numbers are
    # what make that distinction checkable rather than a claim:
    #
    #     POPULATION  48 worlds -- `spec_for(seed, n)` for seed 0..23, n in (4, 5), 9 steps
    #     STARVE A SLOT (`no_support`)   2 of 48
    #     OF THOSE, B5 FIRES             2 of 2
    #
    # **I did not pick the world where B5 fires; B5 fires in every world where a slot starves.**
    # Choosing a world so a defect becomes OBSERVABLE is supplying a panel; choosing one so a
    # verdict comes out right is fitting, and the 2-of-2 is what separates them. Both worlds are
    # asserted, so the reproduction is now a pair rather than a single point.
    for seed in (3, 16):
        led = Ledger()
        ag = Agent(bind(snaps.Snap(snaps.spec_for(seed, 4))), Gamma(snaps._atoms()),
                   Config(), led)
        for _ in range(9):
            ag.step()
        rows = led.rows()
        # THE PRECONDITION FIRST, because a clean verdict on a world that starves nothing is
        # the null this whole entry exists to refuse.
        parked = {r.get("slot") for r in rows if r.get("event") == "park"
                  and (r.get("detail") or {}).get("verdict") == "no_support"}
        assert parked, (
            f"seed {seed} starves no slot -- it no longer exercises B5, and a verdict taken "
            f"here would be a reading of nothing")
        res = kernel.Linter.run(rows)
        bad = sorted(k for k, v in res.items() if v["status"] in ("FAIL", "SUPPRESSED"))
        assert "B5" in bad, (
            f"B5 NO LONGER FIRES on seed {seed} (bad={bad}) while {sorted(parked)} starved. "
            f"If arm M is on, or the probe now reaches the starved slot, this is the GOOD "
            f"outcome -- invert to `assert 'B5' not in bad`, rename it, and it becomes the "
            f"regression test. **CHECK WHICH BEFORE INVERTING**: a tripwire cannot tell *the "
            f"defect is gone* from *the trajectory moved past it*, and both happened today. "
            f"Do not delete it.")


if __name__ == "__main__":
    raise SystemExit(main())

