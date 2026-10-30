"""Insert the (C) LEDGER line after item 6's line, CRLF kept; refuses if the line is already there."""
import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
raw = open(p, "rb").read()
assert b"\r\n" in raw
lines = raw.split(b"\r\n")
MARK = "- **(C), THE EXACT SPEED BUILD".encode()
assert not any(ln.startswith(MARK) for ln in lines), "already inserted"
idx = [i for i, ln in enumerate(lines) if ln.startswith("- **ITEM 6, THE TESTS READ A LINEAGE FILE".encode())]
assert len(idx) == 1, idx
new = (
    "- **(C), THE EXACT SPEED BUILD (TETHER_HYP_MOVABLE_ONCE, default ON; TETHER_HYP_MOVABLE_CHECK, default OFF; the "
    "reviewer 2026-10-23 05:00, 05:25, 05:38, 06:29 gate list; Isaiah \"i like c and then a\").** The pre-flight's ft09 "
    "(2 steps at ~217 s, against E4a's 19) was localized by game_one --profile from the S3O point: 99% of the step in "
    "_hyp_propose_body, 76% in _movable_by, which rebuilt agency.contingent() (quadratic) and env.derived() (the whole "
    "board) on every call (the path arrived at 8ef01f2, GQ2, after E4a). Neither can change inside one _goal_hypothesis "
    "call: Agency.note runs only in perceive (tether.py:8742) and the frame moves only at env.step inside perceive, which "
    "runs after _goal_hypothesis. ON: one call reads each once, at its first _movable_by, for every _movable_by inside "
    "it; the scope opens at the call's entry and clears in its finally; _movable_by's other callers read per call. CHECK "
    "re-reads per call and raises on a difference. Static census (CV/cv_census.py): 53 Agent methods reached from "
    "_goal_hypothesis_run, 0 calls that step, perceive or write the agency record. tests/test_hyp_movable_once.py "
    "(gridworld_arc_s1, 30 steps, seeds pinned): 444 scoped lookups; ON and OFF ledgers equal over 28,390 rows; "
    "contingent() 9 reads ON against 444 OFF; CHECK clean; a planted stale slot raises under CHECK only. CV "
    "(C:/TETHER_RUNS/S6_2026-10-19/CV, wt_c 4b61e06, each box on its own copy of the S3O point; cv_read.out sha16 "
    "f2d709670af93e29): sp80, vc33, sc25 ON/OFF/CHECK, 8 cycles: ledgers equal but the arms row and end_path timings "
    "(4,172 / 3,079 / 8,614 rows), generations equal with handles masked, no CHECK raise; ft09 and tr87 at play cap 450, "
    "ON against OFF: first step 66.2 s / 216.4 s and 97.2 s / 216.3 s, actions 7 / 1 and 7 / 6, peak 662 / 467 and "
    "2,659 / 2,456 MB; the shared prefix equal (ft09 cycle 0, 810 rows; tr87 cycles 0-4, 18,420 rows; the arms row "
    "only); ft09 CHECK 1 step, 222.8 s, no raise. ft09's steps 2-3 ON (143 s, 206 s) are the next cost to read. "
    "ROLLBACK: TETHER_HYP_MOVABLE_ONCE=0 restores the per-call path with no code change; the code rollback is a revert "
    "commit, never a force-push."
).encode()
lines.insert(idx[0] + 1, new)
open(p, "wb").write(b"\r\n".join(lines))
print("inserted after line", idx[0] + 1)
