"""One public game OFFLINE, confirm-only, cold library. argv: tree game cycles led"""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
tree, game, cycles, led = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, tree)
os.chdir(tree)
import arc_holdout  # noqa: E402

t0 = time.perf_counter()
rep = arc_holdout.play(game, cycles, led_path=led)
print(json.dumps({"game": game, "cycles": cycles, "wall_s": round(time.perf_counter() - t0, 1),
                  "report": {k: str(v)[:200] for k, v in rep.items()}}, indent=1))
