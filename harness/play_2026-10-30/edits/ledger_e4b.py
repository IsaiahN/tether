"""Insert the E4b harness LEDGER line after (C)'s line, CRLF kept; refuses if already there."""
import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
raw = open(p, "rb").read()
lines = raw.split(b"\r\n")
MARK = "- **E4b's STREAM HARNESS".encode()
assert not any(ln.startswith(MARK) for ln in lines), "already inserted"
idx = [i for i, ln in enumerate(lines) if ln.startswith("- **(C), THE EXACT SPEED BUILD".encode())]
assert len(idx) == 1, idx
new = (
    "- **E4b's STREAM HARNESS: THE SLICE RULE (A) AND THE ONE WHOLE-RUN NET (b) (Isaiah 2026-10-23 \"i like c and then "
    "a\", the cap \"120\" at 07:07 to the reviewer and in the seat's window; the reviewer 06:29 B1, 06:54 (a)(b), 07:08 "
    "(i)).** harness/mem_store/e4_stream.py, harness only. (A): --slice-min-s / --slice-max-s; a slice takes another "
    "step while under MIN, or under MAX with no act yet; a step under way finishes, because a cut sets "
    "tether.Agent.step's _cut and ends thinking for the rest of the ONE life (tether.py:15591-15608), so a per-slice "
    "ceiling cut would empty every later game; switch.tsv gains acts, first_act_s, extended, unreached, overrun_s at "
    "the end. (b): --deadline-at, an epoch the launcher computes (its clock before the supervisor + the supervisor's "
    "wall - a chosen margin, 300 s for E4b: the agent's own _end_reserve is the LAST end path, ft09's 1.6 s, and a "
    "25-game end path is unmeasured), set ONCE on the agent before the first game; if it fires, the slice ends "
    "\"cut\", the games not started are \"unreached at this budget\", the end path still writes; stream.result.json "
    "carries deadline_at, deadline_fired, budget_unreached, end_path_s. THE RULING IT SUPERSEDES, for that one net "
    "only: the reviewer 2026-10-22 15:24 \"none to be added\" (E9's single-agent scope); tests/test_cap_inner.py ES now "
    "asserts exactly one .deadline assignment, outside every loop, with two must-fails (a second one, or the one "
    "moved, inside the per-game loop). No per-game deadline, no cut at a slice."
).encode()
lines.insert(idx[0] + 1, new)
open(p, "wb").write(b"\r\n".join(lines))
print("inserted after line", idx[0] + 1)
