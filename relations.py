"""The composable-relation sensors (Isaiah, 2026-09-15): the ~15 relations `RELATIONS.md` marks
COMPOSABLE from the frozen set, built as new INSTRUMENTS. The agent perceives 8 per-object
attributes + `touching` (~9 of ~24 things its own frozen vocabulary can compute); these ground the
rest. Each is a READING over object attributes (position/extent/shape/delta/touching) — usable in
the mutation-observer's per-frame attribute vector AND in composition/lookup.

Nothing here is new vocabulary: every relation is composable from the frozen 8 + touching
(`RELATIONS.md` Part 1-2), so this is GROUNDING what the set already expresses, not extending it.
Provenance: sensor, 2026-09-15, Isaiah-authorised, composable-from-frozen-set.

§12.3 AND THE CUE/TERM LINE (reviewer, 2026-09-15) — DO NOT ERASE. §12.3 forbids INSTALLING
`alignment`, `symmetry`, `containment`, `holes`, `counting-by-colour` as COMPOSABLE TERMS: the
agent should have to REACH for them, and reaching is the only evidence the composition system
works. `aligned` is on that list by name; `parallel`/`perpendicular`/`concentric`/`collinear` are
the same family. These are admitted here ONLY as CUES: a reading that NARROWS RETRIEVAL (which atoms
are relevant to this mutation), never an OPERAND the agent composes over. The distinction is
enforced at the wiring, not here: nothing in the betting path (`tether`/`gamma`/`arc_atoms`) imports
this module, so these values reach the mapping/retrieval and never the closure. Wiring any of these
as a composable term violates §12.3 and removes the ablation's evidence — the agent would compose
fluently over things it never reached for, invisibly. If a consumer ever makes a relation bettable
it must supply a CUE (narrow the search), never a TERM (an operand); Isaiah's schema is the cue
reading, the delta infers what to SEARCH for.

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


# -- COLOUR-SOURCE (composable, resolves the CI-1 recolour-referent demand -- F169) ----------

def colour_source(a: dict, others: list[dict]) -> dict | None:
    """Where a's colour comes from, as a composable reading: the NEAREST other object holding the
    same colour (Chebyshev on boxes), or None when NO object holds it -- a novel colour, sourced
    from a palette outside the object set. Measured (F169): resolves ~92% of the recolours the
    frozen touching/above referent could not, so the CI-1 'perception demand' was mostly a thin-cue
    artifact; only the ~8% novel remain. A CUE (narrows retrieval), never a term the agent bets."""
    same = [o for o in others if o["colour"] == a["colour"]]
    if not same:
        return None
    nearest = min(same, key=lambda o: _cheby(a, o))
    d = _cheby(a, nearest)
    return {"present_elsewhere": True, "nearest_dist": d, "touching_source": d == 0}


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
