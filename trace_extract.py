"""Human-trace effect extraction (read-only, seat-side).

For each consecutive pair of frames in a human replay, record the effect the human's
action produced (which object slots changed, and how) and the effect of the step before
it. This produces the raw material for the cross-trace dependency rule. It writes a
ledger of effects and changes nothing the agent decides with.

Walks the existing replays/<game>_human.ndjson files through reverse_engineer.load_replay
so it reads exactly the frames the feeder reads.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

import reverse_engineer

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "replays" / "effects"


def _changed_cells(a, b):
    """Coarse effect: the set of cells whose colour changed between two boards."""
    a = np.asarray(a)
    b = np.asarray(b)
    if a.shape != b.shape:
        return None
    return np.argwhere(a != b)


def effects_for(game: str) -> list[dict]:
    steps = reverse_engineer.load_replay(str(ROOT / "replays" / f"{game}_human.ndjson"))
    rows = []
    prev_effect = None
    for i in range(len(steps) - 1):
        a = steps[i].get("grid")
        b = steps[i + 1].get("grid")
        if a is None or b is None:
            continue
        cells = _changed_cells(a, b)
        if cells is None or len(cells) == 0:
            effect = None
        else:
            rmin, cmin = cells.min(axis=0)
            rmax, cmax = cells.max(axis=0)
            effect = {"n": int(len(cells)), "box": [int(rmin), int(cmin), int(rmax), int(cmax)]}
        rows.append({
            "game": game,
            "step": i,
            "effect": effect,
            # the dependency candidate: the effect that immediately preceded this one
            "depends_on_prev": prev_effect is not None and effect is not None,
        })
        if effect is not None:
            prev_effect = effect
    return rows


def main(argv: list[str]) -> int:
    games = argv or sorted(p.name.replace("_human.ndjson", "")
                           for p in (ROOT / "replays").glob("*_human.ndjson"))
    OUT.mkdir(parents=True, exist_ok=True)
    totals = {}
    for g in games:
        rows = effects_for(g)
        with (OUT / f"{g}_effects.jsonl").open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")
        moved = sum(1 for r in rows if r["effect"] is not None)
        totals[g] = (len(rows), moved)
        print(f"{g}: steps={len(rows)} with_effect={moved}", flush=True)
    print("TOTAL", sum(v[0] for v in totals.values()), "steps,",
          sum(v[1] for v in totals.values()), "with an effect", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
