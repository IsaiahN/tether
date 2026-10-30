"""Commit 2's last edits: the child cap from the measured run, and the 4d-x LEDGER line. argv: repo"""
import sys
from pathlib import Path

R = Path(sys.argv[1])
t = R / "tests" / "test_stream_win.py"
s = t.read_text(encoding="utf-8")
old = "capture_output=True, text=True, timeout=280, stdin=subprocess.DEVNULL,"
assert s.count(old) == 1
t.write_text(s.replace(old, "capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL,"),
             encoding="utf-8", newline="\n")
L = R / "docs" / "LEDGER.md"
lines = L.read_text(encoding="utf-8").split("\n")
at = [i for i, x in enumerate(lines) if x.startswith("- **4a, (iv) RECOGNITION EXPLAINS + (B) STABILITY / AGE, SWITCHED ON")]
assert len(at) == 1, at
assert not any(x.startswith("- **4d-x, A WIN ENDS THE STREAM'S SLICE") for x in lines)
new = ("- **4d-x, A WIN ENDS THE STREAM'S SLICE (2026-10-22; the reviewer 08:39, 08:47, 08:54, 09:03, 09:11, "
       "10:14; found by tests/test_ending_words.py at the 4d move).** harness/mem_store/e4_stream.py:169-170 "
       "compared terminal() to 'win', a word F1b (29d3f59) renamed to ledger.WIN = 'game_win'; the branch was "
       "dead in every stream run so far (0 of 25 switch.tsv record a win), so a won game would not have ended "
       "its slice; fixed in the commit whose subject begins \"Focus: L2 harness -- 4d-x\"; no past result "
       "changes. e4_stream.py was committed at 9b33fa7 as \"byte for byte as they ran\" (a note in that "
       "commit's message only, no file carries it): this line is the pointer to its one later edit. "
       "harness/game_one.py:112's bare \"game_win\" (live, the same word copied) also reads ledger.WIN now. "
       "tests/test_stream_win.py, the must-fail: e4_stream's real loop on a cold agent whose step is a STUB "
       "(an acted turn; e4_stream.py:151 discards the return), terminal() patched to WIN from step 2: NEW "
       "ends at 2 with game_win, OLD (the literal put back in memory) runs to 4 with \"slice\"; guards: the "
       "patch target occurs once, the children write only into throwaway folders (git status equal before "
       "and after), the stream's default lineage (None) untouched; first run T4D/SW2 rc 0, 11.4 s, the real "
       "lineage's 58 files unchanged. ONE REAL-STEP OBSERVATION: the diagnostic T4D/SW1/diag ran NEW with "
       "real steps on lf52 (cold): steps 2, ending game_win. It also measured the cold goal-hypothesis phase "
       "at 482.4 s and 964.2 s per step (the ledger's @goal goal_hypotheses wall_s; step 1 and most of step 2 "
       "beside the 10732 spinner, 1 of 4 cores at Normal priority, stopped 2026-10-22 15:16:08Z) -- C1's data. "
       "Not touched: the bare 'death' literals compared against terminal()/how in tether.py (3269, 3436, 3461) "
       "and tether_agent.py:59, and arc_world.py:1199's returned \"death\" -- on the post-Kaggle list as one "
       "line, replace with ledger.DEATH.")
lines.insert(at[0] + 1, new)
L.write_text("\n".join(lines), encoding="utf-8", newline="\n")
print("ok", at[0] + 2)
