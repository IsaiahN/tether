"""THE FORCED-FOLD CHILD (the reviewer 2026-10-19 07:57 item 4a): e4_stream.py unchanged, with Agent._size_fold
replaced by one that folds ("size") at the start of agent cycles 0 and 1 -- the two points where a3_on's size
trigger fired (a3_on/stream.jsonl.body.jsonl rows 2-3: fold 2 at cycle 0, fold 3 at cycle 1) -- and nowhere else,
setting _fold_last_commit as the real trigger does. The real trigger's ceiling test is the only thing bypassed.
argv: repo <e4_stream.py's own argv after repo>"""
import os
import runpy
import sys

sys.dont_write_bytecode = True
REPO = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
os.chdir(REPO)
import tether  # noqa: E402

FORCE = (0, 1)
_fired: set = set()


def _forced(self) -> None:
    if self.cycle in FORCE and self.cycle not in _fired:
        _fired.add(self.cycle)
        self._fold_last_commit = tether._commit_bytes()
        self._consolidate("size")


tether.Agent._size_fold = _forced
print("FORCED_SIZE_FOLD at cycles", FORCE, flush=True)
sys.argv = [os.path.join(HERE, "e4_stream.py"), *sys.argv[1:]]
runpy.run_path(sys.argv[0], run_name="__main__")
