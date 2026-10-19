"""Each public game's first frame: grid shape and available actions (offline). argv: repo"""
import os
import sys
sys.dont_write_bytecode = True
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, sys.argv[1])
os.chdir(sys.argv[1])
import logging  # noqa: E402
logging.disable(logging.INFO)
import numpy as np  # noqa: E402
import arc_holdout  # noqa: E402
from arc_agi import Arcade  # noqa: E402
arc = Arcade(operation_mode=arc_holdout._mode())
for g in sorted(os.listdir("environment_files")):
    w = arc.make(g)
    fr = getattr(w, "observation_space", None) or w.reset()
    f = fr.frame
    shp = [np.asarray(x).shape for x in f] if isinstance(f, list) else np.asarray(f).shape
    print(g, "frames", len(f) if isinstance(f, list) else 1, "shape", shp[0] if isinstance(shp, list) else shp,
          "actions", list(fr.available_actions or ()), "levels", getattr(fr, "levels_completed", None))
