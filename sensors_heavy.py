"""Heavy sensors -- the mapping layer that makes the 2,700 searchable.

PROCTOR-SIDE, lint-guarded out of the betting path (like observer/detectors). Each atom in
`docs/library-closure` is a detector: attributes + a boolean condition. An atom is SEARCHABLE
when the encodings its attributes need are computed. The observer computed 4 encodings; this
computes the rest, so a condition can be checked against a board instead of being told.

Every quantity here is read off the grid the loop already has -- a scalar shows as a palette
band or an extent (ATTRIBUTE_REACH), so this NAMES what is perceived, it adds no sense."""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

# encodings actually computed here from a single frame (no history)
STATIC = {"POSITION", "EXTENT", "COLOUR", "SHAPE", "SCALAR", "SCALAR_DEFAULT", "COUNT",
          "RELATION", "STATE"}
# the frame history the loop carries, but NOT yet emitted per object -- 867 atoms need this
# on top of STATIC and cannot be reached until the observer emits a per-object temporal delta.
TEMPORAL = {"TEMPORAL", "EVENT"}
# NOT built: 478 atoms touch BEHAVIOURAL (the agent's own action/goal stream, not the board)
# or RULE (a board rule to infer). Named so the gap is visible, not hidden.
UNBUILT = {"BEHAVIOURAL", "RULE"}


def scalar(o: dict) -> dict:
    """SCALAR/EXTENT/COUNT/COLOUR: ordinal magnitudes an object carries -- 699+ atoms.
    A scalar is a scalar; these are every magnitude the grid exposes per object."""
    h, w = o["h"], o["w"]
    cells = len(o["cells"])
    area = h * w
    return {
        "height": h, "width": w, "area": area, "occupiedCells": cells,
        "density": round(cells / area, 3) if area else 0.0,
        "perimeter": 2 * (h + w), "extent": max(h, w), "girth": min(h, w),
        "aspect": round(max(h, w) / max(min(h, w), 1), 3),
        "colour": o["colour"], "holes": max(area - cells, 0),
        "boundingBox": area, "parts": cells, "magnitude": cells,
    }


def position(o: dict) -> dict:
    """POSITION: five integers today, kept and named."""
    return {"row": o["row"], "col": o["col"],
            "centroidRow": o["row"] + o["h"] / 2, "centroidCol": o["col"] + o["w"] / 2,
            "top": o["row"], "left": o["col"],
            "bottom": o["row"] + o["h"], "right": o["col"] + o["w"]}


def _cells(o): return set(map(tuple, o["cells"])) if o.get("cells") else set()


def relation(a: dict, b: dict) -> dict:
    """RELATION: two objects; the predicate resolved -- 384 atoms.
    contact/overlap/containment/distance/alignment, read off two object boxes."""
    ca, cb = _cells(a), _cells(b)
    inter = ca & cb
    ar, ac, ah, aw = a["row"], a["col"], a["h"], a["w"]
    br, bc, bh, bw = b["row"], b["col"], b["h"], b["w"]
    # bounding-box gap (0 = touching/overlapping)
    dr = max(0, max(br - (ar + ah), ar - (br + bh)))
    dc = max(0, max(bc - (ac + aw), ac - (bc + bw)))
    return {
        "overlapArea": len(inter),
        "contactPoints": 0 if inter else (1 if dr == 0 and dc <= 1 or dc == 0 and dr <= 1 else 0),
        "distance": max(abs((ar + ah / 2) - (br + bh / 2)), abs((ac + aw / 2) - (bc + bw / 2))),
        "contains": int(ca >= cb and len(ca) > len(cb)),
        "alignedRow": int(ar == br), "alignedCol": int(ac == bc),
        "larger": int(len(ca) > len(cb)), "sameColour": int(a["colour"] == b["colour"]),
        "sameShape": int(a.get("shape") == b.get("shape")),
    }


def state(o: dict) -> dict:
    """STATE: a discrete condition, an integer with no order -- 115 atoms.
    A per-object categorical: solid vs hollow, orientation, shape class."""
    h, w = o["h"], o["w"]
    cells = len(o["cells"])
    return {
        "solid": int(cells == h * w),
        "orientation": 0 if h == w else (1 if h > w else 2),
        "shapeClass": o.get("shape", 0),
        "singleCell": int(cells == 1),
    }


def temporal(before: dict, after: dict) -> dict:
    """TEMPORAL/EVENT: how one matched object's heavy attributes moved frame->frame -- 867 atoms.
    The frozen 6's deltas are `_match`'s already; these are the heavy ones, so a directed cue can
    fire on a density/holes/solidity change, not only on position/extent/shape/colour."""
    sb, sa = scalar(before), scalar(after)
    tb, ta = state(before), state(after)
    return {
        "dArea": sa["area"] - sb["area"],
        "dCells": sa["occupiedCells"] - sb["occupiedCells"],
        "dDensity": round(sa["density"] - sb["density"], 3),
        "dHoles": sa["holes"] - sb["holes"],
        "dPerimeter": sa["perimeter"] - sb["perimeter"],
        "dGirth": sa["girth"] - sb["girth"],
        "dSolid": ta["solid"] - tb["solid"],
        "dOrientation": ta["orientation"] - tb["orientation"],
        "velocity": max(abs(after["row"] - before["row"]), abs(after["col"] - before["col"])),
    }
