"""The composable-relation sensors (Isaiah, 2026-09-15): the ~15 relations `RELATIONS.md` marks
COMPOSABLE from the frozen set, built as new INSTRUMENTS. The agent perceives 8 per-object
attributes + `touching` (~9 of ~24 things its own frozen vocabulary can compute); these ground the
rest. Each is a READING over object attributes (position/extent/shape/delta/touching) — usable in
the mutation-observer's per-frame attribute vector AND in composition/lookup.

Nothing here is new vocabulary: every relation is composable from the frozen 8 + touching
(`RELATIONS.md` Part 1-2), so this is GROUNDING what the set already expresses, not extending it.
Provenance: sensor, 2026-09-15, Isaiah-authorised, composable-from-frozen-set.

An object is the `arc_percept.components` record: `row col h w colour shape cells`. `shape` is the
normalised offset frozenset (the structural id). Dynamic relations take the before-state too.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True


def _centroid(o: dict) -> tuple[float, float]:
    return o["row"] + o["h"] / 2.0, o["col"] + o["w"] / 2.0


def _oriented(o: dict) -> int:
    """-1 col-major (taller than wide), +1 row-major (wider than tall), 0 square."""
    return (o["w"] > o["h"]) - (o["w"] < o["h"])


def _cheby(a: dict, b: dict) -> int:
    """Gap between bounding boxes, 0 = touching/overlapping, Chebyshev on the box edges."""
    dr = max(0, a["row"] - (b["row"] + b["h"]), b["row"] - (a["row"] + a["h"]))
    dc = max(0, a["col"] - (b["col"] + b["w"]), b["col"] - (a["col"] + a["w"]))
    return max(dr, dc)


# -- STATIC (single frame, one object pair) --------------------------------------------------

def aligned(a: dict, b: dict) -> bool:
    """Equality on one axis — centroids share a row or a column."""
    ca, cb = _centroid(a), _centroid(b)
    return ca[0] == cb[0] or ca[1] == cb[1]


def parallel(a: dict, b: dict) -> bool:
    """Same orientation — both extend along the same axis (`RELATIONS.md` 1.3)."""
    return _oriented(a) == _oriented(b) and _oriented(a) != 0


def perpendicular(a: dict, b: dict) -> bool:
    """One extends in row, the other in column."""
    return _oriented(a) != 0 and _oriented(b) != 0 and _oriented(a) != _oriented(b)


def concentric(a: dict, b: dict) -> bool:
    """Equal centroid, unequal extent."""
    return _centroid(a) == _centroid(b) and (a["h"], a["w"]) != (b["h"], b["w"])


def congruent(a: dict, b: dict) -> bool:
    """Same shape id and size — the one relation the label can carry (`RELATIONS.md` 1.3)."""
    return a["shape"] == b["shape"] and (a["h"], a["w"]) == (b["h"], b["w"])


def adjacent(a: dict, b: dict) -> bool:
    """Contact or distance one — bounding boxes at gap <= 1."""
    return _cheby(a, b) <= 1


def disjoint(a: dict, b: dict) -> bool:
    """No contact — the negation of touching, at the box level."""
    return _cheby(a, b) > 0


def offset(a: dict, b: dict) -> tuple[int, int]:
    """The constant separation between two positions — a READING, not a truth (`RELATIONS.md` 1.3).
    A relation that carries a value composes where a bare predicate cannot."""
    return b["row"] - a["row"], b["col"] - a["col"]


# -- DYNAMIC (needs the before-state of each object) -----------------------------------------

def _delta(before: dict, after: dict) -> tuple[int, int]:
    return after["row"] - before["row"], after["col"] - before["col"]


def no_relative_motion(ba: dict, bb: dict, a: dict, b: dict) -> bool:
    """Deltas equal — the pair moves as one."""
    return _delta(ba, a) == _delta(bb, b)


def translation(ba: dict, bb: dict, a: dict, b: dict) -> bool:
    """Relative position changes, orientation does not — deltas differ, shape ids constant."""
    return (_delta(ba, a) != _delta(bb, b)
            and a["shape"] == ba["shape"] and b["shape"] == bb["shape"])


def sliding(ba: dict, bb: dict, a: dict, b: dict) -> bool:
    """Contact maintained, tangential relative motion — touching persists and deltas differ."""
    return adjacent(a, b) and adjacent(ba, bb) and _delta(ba, a) != _delta(bb, b)


# WHAT IS NOT HERE, AND WHY (kept honest against RELATIONS.md's own markings):
#   intersecting  -- needs cell/bbox overlap; `_overlap` is IoU of normalised shapes, and cell
#                    overlap is 0 under solidity. A different sensor (bounding-box overlap), noted
#                    in RELATIONS.md 1.1 as a genuine build, not composed here.
#   collinear     -- degenerate for a pair (any two centroids are collinear); a >=3-object relation.
#   orbiting/oscillating -- need multi-frame history (distance-constant/direction-cycling, sign
#                    alternation); the mutation-observer accumulates that, so they live there.

# THE INSTRUMENT SET, by kind, so the mutation-observer and composition/lookup can enumerate them.
STATIC = {"aligned": aligned, "parallel": parallel, "perpendicular": perpendicular,
          "concentric": concentric, "congruent": congruent, "adjacent": adjacent,
          "disjoint": disjoint, "offset": offset}
DYNAMIC = {"no_relative_motion": no_relative_motion, "translation": translation, "sliding": sliding}


def read_pair(a: dict, b: dict, ba: dict | None = None, bb: dict | None = None) -> dict:
    """The full composable-relation reading for one ordered object pair — the mutation-observer's
    per-pair cue vector. Dynamic relations resolve only when the before-state is supplied."""
    out = {name: fn(a, b) for name, fn in STATIC.items()}
    if ba is not None and bb is not None:
        out.update({name: fn(ba, bb, a, b) for name, fn in DYNAMIC.items()})
    return out
