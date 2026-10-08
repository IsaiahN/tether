"""One public game OFFLINE, confirm-only, cold library, from a pinned tree.
argv: tree game cycles led commit
Refuses before importing the agent unless the tree is at `commit` and clean; writes <led>.head."""
import datetime
import json
import os
import sys
import time

sys.dont_write_bytecode = True
tree, game, cycles, led, commit = (sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4],
                                   sys.argv[5])
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import rb_heads  # noqa: E402

rb_heads.refuse_unless_pinned(tree, commit)
with open(led[:-6] + ".head", "w") as fh:
    json.dump({"commit": commit, "source": "recorded", "at": datetime.datetime.now().isoformat()},
              fh)
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, tree)
os.chdir(tree)
import arc_holdout  # noqa: E402

t0 = time.perf_counter()
rep = arc_holdout.play(game, cycles, led_path=led)
print(json.dumps({"game": game, "cycles": cycles, "commit": commit,
                  "wall_s": round(time.perf_counter() - t0, 1),
                  "report": {k: str(v)[:200] for k, v in rep.items()}}, indent=1))
