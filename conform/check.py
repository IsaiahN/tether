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
    panel     the measured worlds  the same 12 checks over stamped gridworld and fake ledgers
    figures   the record's reasons every entry from F506 on carries a FIGURE CENSUS

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
    # THE AIM SEAT. `focus.py` binds WHICH LEVEL a commit sits at and says nothing about
    # WHETHER THE WORK WAS ON THE LIST -- three of this session's drifts were clean L1
    # commits. This one binds the declared ITEM, and its cases reintroduce both.
    # EVERY Ctx A TERM IS EVALUATED IN GOES THROUGH ONE CONSTRUCTOR. `acted_self` was set at
    # 3 of 11 constructions -- the three PRICING ones -- so a guarded term read as IDENTITY
    # wherever it was judged, and `bears_on` refused all 23 perfect `?ACTED_SELF` candidates
    # per seed on click_only. Its self-test reintroduces a direct construction and refuses to
    # pass unless the seat goes red on it.
    # EVERY CONSUMER OF A HISTORY/TRACE RECORD UNPACKS IT AT THE PRODUCER'S WIDTH. Fifteen
    # sites disagreed at FOUR widths with eight hiding the tail behind `*_`: `_invent`
    # unpacked three and raised on its first call (so the arm had never executed), and
    # `bears_on` threw `landed` away so the field the guard needs was not in scope. The
    # canonical width is READ FROM `history()` rather than typed here -- a number written
    # into the seat is the next thing to go stale, which is the failure one level up.
    ("recshape", [str(PY), str(HERE / "recshape.py")],
     "a history/trace record is unpacked at the wrong width or behind a star, so a "
     "widening breaks a run instead of a test",
     HERE / "recshape.py"),
    ("evalctx", [str(PY), str(HERE / "evalctx.py")],
     "a term-evaluating Ctx was built outside `Agent._eval_ctx`, so a guard can read as "
     "identity where the term is judged",
     HERE / "evalctx.py"),
    ("aim", [str(PY), str(HERE / "aim.py")],
     "the aim seat stopped refusing work that names no declared item",
     HERE / "aim.py"),
    # THE LANDED-ON FIELD, ASSERTED AGAINST THE WORLD AND NOT AGAINST THE AGENT'S OWN RECORD.
    # `a561fb2` carried what the agent AIMED AT in a field a guard read as what it ACTED ON,
    # and measured clean for five hours because the broken build was perfectly self-consistent.
    # Its failure path is exercised: reintroducing that defect reads 15/25 and fires.
    ("landed", [str(PY), str(HERE / "landed.py")],
     "the trace says what the agent WANTED instead of what the press HIT",
     HERE / "landed.py"),
    # THE CONDITION COMPILER's own grammar suite. Five texts that MUST NOT parse, including a
    # real line of corpus prose and a bare reading -- a grammar that accepts `holes(o1)` as a
    # condition has invented the comparison nobody wrote.
    # THE ARMS SEAT. Eighteen capability switches, every one default OFF, and nothing in the
    # repository sets one -- so the agent that runs is the most starved variant of itself and
    # nobody chose that. Each site's reason is good; no place held the SUM, which is the
    # ground-focus seat's own origin one level up. It flips nothing: it refuses an arm entering
    # silently, a stale row, and half of a pair whose own site declares they belong together.
    ("arms", [str(PY), str(HERE / "arms.py")],
     "an arm entered without a row, a row went stale, or half a declared pair is on",
     HERE / "arms.py"),
    # THE LAYER SEAT -- Isaiah, 2026-10-05: *"my leg isn't in one room and I in another."*
    # The seam was enforced by a ruff ban that NAMED `world.ACTIONS` and nothing else, so
    # `gridworld` -- the world all of this week's work ran in -- was uncovered. Extending the
    # name list would have been the same defect a third time; this is per LAYER, so a world
    # nobody has written yet is covered because nobody has to list it.
    ("layers", [str(PY), str(HERE / "layers.py")],
     "the agent imported a world directly instead of reaching it through the Env contract",
     HERE / "layers.py"),
    # THE WIRING SEAT, AND IT WAS THE ONLY CHECK IN THIS FOLDER THAT NOTHING RAN. Its own
    # docstring says it was made "a check that fires rather than a census that is run" -- and
    # then it was never wired, which is the exact class it exists to catch. It was RED when
    # found: `any_same` had gone never-occurred -> settled and nobody saw.
    ("wiring", [str(PY), str(HERE / "wiring.py")],
     "a capability changed between never-occurred and occurred without the manifest moving",
     HERE / "wiring.py"),
    # THE END-TO-END FIXTURE -- Isaiah, 2026-09-24: *"I need this stuff wired together and not
    # orphaned... why can't the system be built out end to end without games?"* One pass through
    # every stage on the TOY world, pass/fail, no score. **It proves WIRED and never CAPABLE**,
    # and its own docstring says so, because mechanism reported as capability is `M2` clause 7's
    # whole subject.
    ("fixture", [str(PY), str(HERE / "fixture.py")],
     "an end-to-end stage changed between reached and dead without the manifest moving",
     HERE / "fixture.py"),
    ("condition", [str(PY), "condition.py"],
     "the condition grammar accepted something it must refuse, or three-valued logic broke",
     ROOT / "condition.py"),
    ("demo", [str(PY), "demo.py"], "the loop did not complete", ROOT / "demo.py"),
    ("gate", [str(PY), "gate.py", "runs/demo.jsonl"],
     "the record is not well-formed", ROOT / "gate.py"),
    # THE GATE OVER THE WORLDS WE MEASURE (F505): the demo alone left every panel claim resting
    # on a gate that never saw it. It judges stamped ledgers and never runs them.
    ("panel", [str(PY), str(HERE / "panel.py")],
     "a panel ledger is missing, stale, or refused by the gate", HERE / "panel.py"),
    # THE FIGURES DICTATE LOGIC AND DECISIONS (Isaiah, 2026-10-07): an INDEX entry from F506 on
    # carries a FIGURE CENSUS -- the bearing figures quoted, any strained named.
    # THE LIBRARY AGREES WITH WHAT THE CODE BUILDS, PER ARM (the reviewer, 2026-10-08 17:52Z):
    # inherited.py keys the agent's reach on agent_atoms.json, and v4 let 21 built atoms fall out
    # of it unseen. Run with its must-fails, so a pass shows both the catch and a clean library.
    ("library", [str(PY), str(HERE / "libagree.py"), "--must-fail"],
     "the library and the atoms the code builds disagree, or a planted drift went uncaught",
     HERE / "libagree.py"),
    # THE COMPILER MEANS WHAT THE LIBRARY SAYS (M2, the reviewer 2026-10-08 21:08Z): every
    # compiled candidate agrees with condition.evaluate, every refusal carries its reason, and a
    # swapped binding is caught.
    ("compile", [str(PY), "test_compile.py"],
     "a compiled library term disagrees with condition.evaluate, or a planted swap went uncaught",
     ROOT / "test_compile.py"),
    ("figures", [str(PY), str(HERE / "figures.py")],
     "an INDEX entry from F506 on carries no FIGURE CENSUS", HERE / "figures.py"),
    ("tests", [str(PY), "test_gate.py"],
     "the gate's own defect suite regressed", ROOT / "test_gate.py"),
    # A SUITE THAT NO SEAT RUNS IS A SUITE THAT ROTS, and this one sat outside the gate for
    # six commits while every one of them reported `8/8 seats clean`. The M2 checks each
    # CONSTRUCT the defect they guard against and each has been shown to fail when its
    # mechanism is removed -- which is worth exactly nothing if nothing runs them.
    ("m2", [str(PY), "test_m2.py"],
     "an M2_STANDARD mechanism regressed, or its tripwire fired", ROOT / "test_m2.py"),
    # THE ENTRY SEAT -- the reviewer, 2026-10-06. Every ARC path goes through `wire()`, and
    # every one of them opened with two or three consecutive RESETs until F452/F454 (Isaiah,
    # 2026-09-29: never RESET,RESET). It runs the Kaggle path offline on a FAKE wrapper and
    # plants the pair, so the guard's failure path is exercised, not assumed.
    ("entry", [str(PY), "test_entry.py"],
     "an ARC path sent RESET,RESET, or the guard stopped refusing it", ROOT / "test_entry.py"),
    ("percept", [str(PY), "test_perception.py"],
     "a perception detector regressed (Contain/Topology/perimeter/background)",
     ROOT / "test_perception.py"),
)

# stderr from an interpreter that never reached the program. A backstop for the cases a
# path check cannot cover, such as `-m ruff` with ruff uninstalled.
NEVER_STARTED = ("can't open file", "No module named", "cannot find the file")


# **120 -> 180, RULED BY ISAIAH 2026-09-28 AND MEASURED, NOT PICKED.** `shipped` reported
# DID-NOT-RUN for the first time since installation, and the profile said the limit was the
# problem rather than the tests:
#
#     the seat, `stateful.py --fast --tether`      2m01s
#     21 module-level property tests               115.2s of it
#     the two most expensive                       22.9s + 21.7s
#
# **So it had been within seconds of the limit and nobody knew, because the failure path had
# never fired** -- this folder's own *a guard whose failure path is never exercised is
# indistinguishable from one that cannot fail*, about its own runner.
#
# 180 is ~50% headroom over the measured 2m01s. **A seat that passes at 118s and fails at 121s
# is winning a coin flip rather than passing a check**, and the two readings taken minutes apart
# disagreed by exactly that margin. **It is a CALIBRATION constant: moving it disarms the guard
# while leaving it green, so it is recorded with its measurement. **ISAIAH RULED THIS VALUE AND
# IT IS ISAIAH'S TO MOVE** -- not the seat's and not the reviewer's, which is the same standing
# `STALL` has. Recorded because a calibration constant with the wrong owner written beside it
# is how one gets moved by whoever finds it inconvenient.
# anchor: 180s is ~50% headroom over the seat's MEASURED 2m01s, taken 2026-09-28 on
# `stateful.py --fast --tether`. Not a round number chosen for comfort -- the margin is what
# separates a check from a coin flip, and two readings minutes apart differed by the 3s that
# decided pass from DID-NOT-RUN.
STAGE_TIMEOUT = 180


def run_stage(argv: list[str], needs: Path | None = None) -> tuple[str, str]:
    """(status, detail). DID-NOT-RUN is its own state: a stage that could not start has
    not passed, and folding it into a FAIL asserts a cause that was never observed."""
    if needs is not None and not needs.exists():
        return "DID-NOT-RUN", f"{needs.name} does not exist"
    try:
        p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                           timeout=STAGE_TIMEOUT,
                           creationflags=getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0))
    except FileNotFoundError as e:
        return "DID-NOT-RUN", f"{type(e).__name__}: {e}"
    except subprocess.TimeoutExpired:
        return "DID-NOT-RUN", f"timed out after {STAGE_TIMEOUT}s"
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
    # HOW MANY, NOT ONLY WHICH: the ruff seat once showed 3 findings of 66 and the narrow fix it
    # invited stayed red (the reviewer 2026-10-08 17:56Z). The count is never truncated.
    shown = hits[:3]
    return "FAIL", (f"{len(shown)} of {len(hits)} finding line(s) shown: "
                    + " · ".join(shown))[:400]


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
