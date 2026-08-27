"""2b. Segmented objects as slots, tracked by overlap, dying only on evidence.

`DISCOVERY` Q6, SETTLED: classical segmentation, no downsampling, permanence by overlap,
death only on evidence. §12.3's first four sensors are what a slot's predictable state IS --
`components`, `colour`, `position`, `extent` -- and §4 says the slots ARE segmented objects.

WHAT A SLOT IS HERE. `POSITION` and `EXTENT` are two-dimensional and the loop takes one int
per slot, so an object contributes several: `row`, `col`, `h`, `w`, `colour`. Separate axes
rather than one encoded number, because that is the only encoding in which a `translate` atom
acts on a slot sensibly -- one axis at a time is what a per-slot term can say.

TWO CHOICES THE CORPUS DOES NOT SETTLE, MADE HERE AND STATED:

  4-CONNECTIVITY, not 8. *Connected same-symbol components, the boundary is where cohesion
  drops* does not say which. Four is the conservative reading: it splits diagonal touches into
  separate objects, so the agent sees MORE slots rather than fewer. **Over-segmentation is
  recoverable -- the agent can learn two slots move together -- and under-segmentation is the
  loud/silent failure**, where one slot hides a rule operating below it.

  NO BACKGROUND COLOUR. Every same-symbol region is a component, INCLUDING colour 0. Treating
  0 as background is domain knowledge about what a board means, and this file is not entitled
  to it. It costs slots and refuses an assumption; the agent may learn that a colour behaves
  like a background, which is the whole point.
"""
from __future__ import annotations

import sys
from typing import Any

sys.dont_write_bytecode = True


def components(board: Any) -> list[dict]:
    """§12.3 sensor 1. Connected same-symbol regions, 4-connectivity, flood fill.

    Returns one dict per object with its cells and the four sensors that make up a slot's
    predictable state: colour, position (top-left of the bounding box), extent.
    """
    h, w = len(board), len(board[0])
    seen = [[False] * w for _ in range(h)]
    out: list[dict] = []
    for r0 in range(h):
        for c0 in range(w):
            if seen[r0][c0]:
                continue
            hue = int(board[r0][c0])
            stack, cells = [(r0, c0)], []
            seen[r0][c0] = True
            while stack:
                r, c = stack.pop()
                cells.append((r, c))
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < h and 0 <= cc < w and not seen[rr][cc] \
                            and int(board[rr][cc]) == hue:
                        seen[rr][cc] = True
                        stack.append((rr, cc))
            rows = [r for r, _ in cells]
            cols = [c for _, c in cells]
            r0_, c0_ = min(rows), min(cols)
            out.append({"cells": frozenset(cells), "colour": hue,
                        "row": r0_, "col": c0_,
                        "h": max(rows) - r0_ + 1, "w": max(cols) - c0_ + 1,
                        "shape": frozenset((r - r0_, c - c0_) for r, c in cells)})
    return out


def shape_of(obj: dict) -> frozenset:
    """§12.3 sensor 5, `OBJ -> SHAPE`: the cell pattern at NORMALIZED OFFSETS.

    Normalized means relative to the object's own top-left, so it is POSITION-INDEPENDENT --
    which is what makes it identity under translation as well as under recolour.
    """
    return obj["shape"]


def overlap(a: frozenset, b: frozenset) -> float:
    """§12.3 sensor 6, typed `OBJ x OBJ -> RATIO`. Intersection over union.

    A RATIO and not a BOOL, which is why tracking matches by MAXIMUM overlap and there is no
    threshold to anchor. A cutoff here would be the `EPS`/`WARM` mistake one layer out: a
    number introduced where the specification says measurement.
    """
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


class Objects:
    """The decomposition, stateful because tracking is.

    Identity is founded at first sight and carried by maximum overlap, so it survives recolour
    and reshape. **An object not found is NOT dead** -- it persists through non-observation,
    and dies only when its cells are taken over by other live objects, which is Q6's *death
    only on evidence*. Dropping a slot because nothing matched would be a silent slot-set
    change, which is blocker 2's defect from the other direction -- and `_present` would now
    make it loud, so the rule and the detector agree.
    """

    def __init__(self) -> None:
        self.tracked: dict[str, dict] = {}
        self._next = 0

    def __call__(self, board: Any) -> dict[str, int]:
        found = components(board)
        claimed: set[str] = set()
        fresh: dict[str, dict] = {}

        # match each new component to the tracked object it overlaps most. Ties break on the
        # name so a run is reproducible; a zero-overlap component has no predecessor and is
        # a birth rather than a bad match.
        for obj in found:
            best, score = None, 0.0
            for name, old in self.tracked.items():
                if name in claimed:
                    continue
                r = overlap(obj["cells"], old["cells"])
                if r > score or (r == score and r > 0 and (best is None or name < best)):
                    best, score = name, r
            if best is None or score == 0.0:
                # OVERLAP ALONE CANNOT TRACK A MOVE. An object smaller than its own
                # displacement has zero cell overlap with itself one frame later, so a
                # translation would read as a death and a birth -- and `translate` is in the
                # specified atom set, which is unobservable if translation destroys identity.
                # §12.3 sensor 5 is the answer: SHAPE at normalized offsets is
                # position-independent, so it carries identity across a move.
                best = next((n for n, old in sorted(self.tracked.items())
                             if n not in claimed and shape_of(old) == shape_of(obj)), None)
            if best is None:
                best = f"o{self._next}"
                self._next += 1
            claimed.add(best)
            fresh[best] = obj

        # DEATH ONLY ON EVIDENCE. An unmatched tracked object keeps its slots unless another
        # live object now holds its cells. Not found is occluded, not gone.
        live = frozenset().union(*(o["cells"] for o in fresh.values())) if fresh else frozenset()
        for name, old in self.tracked.items():
            if name in fresh:
                continue
            if not (old["cells"] & live):
                fresh[name] = old          # occluded: persists, unchanged
        self.tracked = fresh

        state: dict[str, int] = {}
        for name, obj in self.tracked.items():
            for attr in ("row", "col", "h", "w", "colour"):
                state[f"{name}.{attr}"] = int(obj[attr])
        return state
