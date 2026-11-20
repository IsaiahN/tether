"""Fresh-process runner for a single world2d agent episode.

One process per episode: the agent's purse counter (cap.HEADS) and other module globals
accumulate across Agent constructions in one interpreter, so two agents in a single process
are NOT the same arm and their mint counts are not comparable. The measurement must be a
fresh process per run. This helper is invoked by tests/test_world2d.py.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["TETHER_AGENT_SEED"] = "0"

import tether  # noqa: E402
import world2d  # noqa: E402
from gamma import Gamma  # noqa: E402
from ledger import Ledger  # noqa: E402
from world import bind  # noqa: E402


def main():
    seed = int(sys.argv[1])
    steps = int(sys.argv[2])
    hooks = sys.argv[3] == "1"
    out = sys.argv[4]
    w = world2d.World2D(seed=seed, hooks=hooks)
    a = tether.Agent(bind(w), Gamma(w.atoms()), tether.Config(), Ledger())
    for _ in range(steps):
        a.step()
    with open(out, "w", encoding="utf-8") as fh:
        for r in a.led.rows():
            fh.write(json.dumps(r, default=str) + "\n")
    # a one-line receipt: this is the actual run the ledger belongs to
    print(f"world2d seed={seed} steps={steps} hooks={hooks} rows={len(a.led)} "
          f"mints={sum(1 for r in a.led.rows() if r.get('event') == 'mint')}")


if __name__ == "__main__":
    main()
