# RELATIONS.md (cited below) are docs/library-closure/ files DELETED 2026-10-11 (Section A);
# git holds them at the parent of the deleting commit (DOCS_CONSOLIDATION.md section A).
# RELATIONS.md's live successor: library/relations.json + LIBRARY_SPEC section 3.
"""The composable-relation sensors (Isaiah, 2026-09-15): the ~15 relations `RELATIONS.md` marks
COMPOSABLE from the frozen set, built as new INSTRUMENTS. The agent perceives 8 per-object
attributes + `touching` (~9 of ~24 things its own frozen vocabulary can compute); these ground the
rest. Each is a READING over object attributes (position/extent/shape/delta/touching) — usable in
the mutation-observer's per-frame attribute vector AND in composition/lookup.

Nothing here is new vocabulary: every relation is composable from the frozen 8 + touching
(`RELATIONS.md` Part 1-2), so this is GROUNDING what the set already expresses, not extending it.
Provenance: sensor, 2026-09-15, Isaiah-authorised, composable-from-frozen-set.

SUPERSEDED: Isaiah 10-14 innate atoms ("ALL atoms/concepts are innate"; Isaiah 09-19 dissolved
the reaching circle); 10-20 GQ2 states goal hypotheses in the existing vocabulary and installs no
atom (the reviewer 2026-10-20 14:27 (a)). The note below is kept as the record.

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

AND THE WIRING SENTENCE ABOVE IS STALE (DS, the reviewer 2026-10-20 08:36 (7)): `tether`
imports this module, the relations are OPERANDS there (as the pair slots' sources), and the
world publishes them as declared-derived SLOTS. What holds is the line
itself: a relation is a cue and an operand, never a bound SUBJECT -- under TETHER_DERIVED_SUBJECT
no term is bound to a derived slot, and the lookup reads a pair reading through its base
(TETHER_CUE_NORM).

An object is the `arc_percept.components` record: `row col h w colour shape cells`. `shape` is the
normalised offset frozenset (the structural id). Dynamic relations take the before-state too.
"""

from __future__ import annotations

import sys

import armflag
import cap

sys.dont_write_bytecode = True

# E0, THE PERCEPT DECLARES WHAT IT DERIVES (the reviewer 2026-10-17 12:53, 12:59; Fig 12 :125 one
# description; the stability ruling at 10:05): an attribute the percept computes by its own rule
# from readings it already publishes (h / w and the frame deltas from the object's shape, motion
# from row / col, colour_changed from colour; gridworld's proximity and distance from positions)
# is declared through derived(), so it is predicted from its sources and carries a residual only
# when its sources held (B2b's relational surprise). Read by arc_world and gridworld; one flag.
# OFF: only the pair slots are declared, as before (610654c)
_DERIVED_PERCEPT = armflag.arm("TETHER_DERIVED_PERCEPT", default=True)


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


# -- PAIR RELATIONS AS SLOTS (B2, TETHER_RELATION_SET; the reviewer 2026-10-11 14:19Z, 14:33Z) ---

# One slot per (relation, partner) on the SUBJECT object, named `{a}.{rel}_{b}` so every reader
# of `obj.attr` sees owner `a` and attribute `{rel}_{b}`. Relative quantities only, keyed on the
# world's persistent object names, never on colour or game: the box gap, the row/col offset, box
# containment and box contact. A pair slot exists only while both objects do (came/gone).
PAIR_RELATIONS: dict[str, str] = {"dist": "EXTENT", "drow": "DELTA", "dcol": "DELTA",
                                  "inside": "BOOL", "touches": "BOOL"}


# THE SPARSE OBSERVER PAIRS (the reviewer 2026-10-11 14:31 CDT): arc_world's observer emits
# `a~b.inside` and `a~b.bbox` ONLY where the relation holds, so with both objects present an
# absent pair IS this value. Declared once here (cited at arc_world's two emission sites), and
# applied ONLY where a library condition is evaluated -- perception never sees a synthesised zero.
SPARSE_PAIR: dict[str, int] = {"inside": 0, "bbox": 0}


def within(a: dict, b: dict) -> bool:
    """a's box lies inside b's box (edges may coincide)."""
    return (b["row"] <= a["row"] and a["row"] + a["h"] <= b["row"] + b["h"]
            and b["col"] <= a["col"] and a["col"] + a["w"] <= b["col"] + b["w"])


def overlaps(a: dict, b: dict) -> bool:
    """The two boxes share a cell (B4; the gap is 0 for touching AND overlapping, so a predicted
    move INTO a partner needs this). Internal to a reading, not a published relation."""
    return (a["row"] < b["row"] + b["h"] and b["row"] < a["row"] + a["h"]
            and a["col"] < b["col"] + b["w"] and b["col"] < a["col"] + a["w"])


def pair_values(ra: dict, rb: dict) -> dict[str, int]:
    """The five relations of the ordered pair (a, b), keyed by relation."""
    dr, dc = offset(ra, rb)
    gap = _cheby(ra, rb)
    return {"dist": gap, "drow": dr, "dcol": dc, "inside": int(within(ra, rb)),
            "touches": int(gap == 0)}


def pair_slots(objs: dict[str, dict]) -> dict[str, int]:
    """`{"{a}.{rel}_{b}": value}` over every ordered pair of the objects given."""
    return pair_slots_over(objs, [(a, b) for a in objs for b in objs if a != b])


def pair_slots_over(objs: dict[str, dict], pairs: list) -> dict[str, int]:
    """`{"{a}.{rel}_{b}": value}` over the ordered pairs given (ARC B2: contact and actor pairs)."""
    out: dict[str, int] = {}
    for a, b in pairs:
        cap.head()
        for rel, v in pair_values(objs[a], objs[b]).items():
            out[f"{a}.{rel}_{b}"] = v
    return out


def pair_attr(attr: str) -> str | None:
    """The relation an attribute names, if it is a pair attribute (`dist_o3` -> `dist`)."""
    rel, sep, _partner = attr.partition("_")
    return rel if sep and rel in PAIR_RELATIONS else None


# -- THE SETTLED TABLE (C; the reviewer 2026-10-11 09:28-13:17 CDT; Isaiah 09:26) -----------------

# Core knowledge the library already holds, loaded SETTLED: inherited, the way a hatchling has it,
# and still refutable per (term, slot). Each entry is BOUND to the code that computes it, or named
# UNBOUND -- a settled entry with no binding is an inert arm, and the ALL-ON orphan check lists it.
# An atom binding is already settled in the only sense Gamma has (a PRIOR unit from birth), so no
# standing changes here. Kinds: atom (one-atom terms), reading (a published attribute), compose (a
# condition the compile path turns into a term), agent (the code that reads it), unbound (why).
SETTLED_BY = "inherited (Isaiah 2026-10-11)"
_TOWARD, _AWAY = "o0.dist_o3 < o0.dist_o3~1", "o0.dist_o3 > o0.dist_o3~1"
_CONTINGENT = "instruments.Agency.contingent"
_BLOCKED = "tether.Agent._blocked_reading"
_TRACKER = "arc_percept.Objects.__call__"
_CLOSURE = "gamma.Gamma.enumerate_closure"
_PATH = "no agent-side path: the world's BFS is the world's own"
SETTLED: dict[str, tuple] = {
    "HUMAN|Order": ("atom", ("above", "below")),
    "HUMAN|Number": ("atom", ("count",)),
    "THOUGHT|Comparison": ("atom", ("above", "below", "same")),
    "CYBERNETIC|Comparator": ("atom", ("same", "above", "below")),
    "NETWORK|Rank": ("atom", ("rank_in", "is_max", "is_min")),
    "DYNAMIC|Threshold": ("atom", ("above", "below")),
    "PHENOMENOLOGICAL|Proximity": ("reading", ("dist",)),
    "RAW DATA|Adjacency": ("reading", ("touches",)),
    "HUMAN|Geometry": ("reading", ("dist", "drow", "dcol")),
    "HUMAN|Topology": ("reading", ("inside",)),
    "HUMAN|Contain": ("reading", ("inside",)),
    "HUMAN|Surround": ("reading", ("inside",), "the partner inside the subject: the converse pair"),
    "RAW DATA|Inside": ("reading", ("inside",)),
    "RAW DATA|Outside": ("compose", "o0.inside_o3 == 0"),
    "RAW DATA|Enclosure": ("reading", ("inside",), "box; hole: ARC's a~b.inside"),
    "HUMAN|Chirality": ("reading", ("drow", "dcol")),
    "RAW DATA|offset": ("reading", ("drow", "dcol")),
    "NETWORK|Direction": ("reading", ("drow", "dcol"), "its sign through `sign`"),
    "PSYCHOLOGICAL|Approach": ("compose", _TOWARD, "requires TETHER_PREV_OFFER (or the window)"),
    "HUMAN|Avoid": ("compose", _AWAY, "requires TETHER_PREV_OFFER (or the window)"),
    "KINETIC|Pursuit": ("compose", _TOWARD, "requires TETHER_PREV_OFFER (or the window)"),
    "KINETIC|Flee": ("compose", _AWAY, "requires TETHER_PREV_OFFER (or the window)"),
    "MORPHOGENETIC|Gradient": ("compose", _TOWARD, "requires TETHER_PREV_OFFER (or the window)"),
    "CYBERNETIC|Goal seeking": ("agent", "tether.Agent._goal_choice"),
    "RAW DATA|Sequence": ("unbound", "event order across objects: not checked"),
    "HUMAN|Continuity": ("reading", ("age", "stability")),
    "HUMAN|Subitise": ("atom", ("count",)),
    "RAW DATA|THE SAME": ("atom", ("same",)),
    "HUMAN|Featural identity": ("atom", ("same", "all_same", "any_same")),
    "HUMAN|Causality": ("agent", _CONTINGENT),
    "ADVERSARIAL|Contingency": ("agent", _CONTINGENT),
    "HUMAN|Solidity": ("agent", _BLOCKED, "object contact; board edge not covered"),
    "HUMAN|Collide": ("agent", _BLOCKED, "object contact; board edge not covered"),
    "ADHERENCE|Obstacle": ("agent", _BLOCKED, "object contact; board edge not covered"),
    "ONTOLOGICAL|Anomaly": ("unbound", "rule level; object-level odd-one-out composes, no entry"),
    "HUMAN|Backchain": ("agent", _CLOSURE, "composition"),
    "THOUGHT|Inference": ("agent", _CLOSURE, "composition"),
    "THOUGHT|Reasoning chain": ("agent", _CLOSURE, "composition"),
    "HUMAN|Analogise": ("atom", ("same",), "over two pair slots"),
    "THOUGHT|Analogy": ("atom", ("same",), "over two pair slots"),
    "HUMAN|Abstract": ("atom", ("same",), "over two pair slots"),
    "HUMAN|Animacy": ("agent", _CONTINGENT),
    "HUMAN|Movement": ("agent", "tether.Agent._moved"),
    "ACTION|Push": ("agent", "tether.Agent._cascade_agency"),
    "EMBODIMENT|Self agency": ("agent", _CONTINGENT),
    "HUMAN|Intervene": ("agent", _CONTINGENT),
    "HUMAN|Persist": ("agent", _TRACKER, "a covered object keeps its name; NULL, not removed"),
    "HUMAN|beyond view": ("agent", _TRACKER, "a covered object keeps its name"),
    "HUMAN|Reveal": ("agent", _TRACKER, "a covered object reads again when uncovered"),
    "HUMAN|Layer": ("agent", _TRACKER, "the overlay rule"),
    "HUMAN|Extrapolate": ("unbound", "no reading carries a hidden object's motion forward"),
    "DESIRE|Goal": ("agent", "tether.Agent._goal_condition"),
    "NETWORK|Path": ("unbound", _PATH),
    "NETWORK|Short Path": ("unbound", _PATH),
    "HUMAN|Navigate": ("unbound", _PATH),
    "HUMAN|Wayfind": ("unbound", _PATH),
    "HUMAN|Dead reckon": ("unbound", _PATH),
    "HUMAN|Other's goal": ("unbound", "no reading of another agent's goal"),
    "HUMAN|Cohesion": ("agent", _TRACKER),
    "HUMAN|Track": ("agent", _TRACKER),
    "HUMAN|Support": ("unbound", "no support reading"),
    "HUMAN|Forward model": ("agent", "tether.Agent._predict"),
    "HUMAN|Trajectory": ("reading", ("speed", "drow", "dcol")),
    "HUMAN|Predict": ("agent", "tether.Agent._predict"),
}


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
