"""Heavy sensors -- the mapping layer that was built to make the 2,700 searchable.

SUPERSEDED, AND PENDING DELETION -- reviewer, 2026-09-23. Do not build on this module. Read
the four corrections below before using any reading in it.

  1  IT IS NOT LINT-GUARDED. This docstring claimed "lint-guarded out of the betting path
     (like observer/detectors)" and `conform/lint.py`'s `_CUE_MODULES` is
     {relations, observer, mapping, detectors, composer} -- this module is NOT in it. It
     stays out of the betting path only as a side effect of its two importers being guarded.
  2  IT WAS NEVER WIRED, WHICH IS WHY IT WAS NEVER VALIDATED. Measured with all five arms
     ON: it does not appear in `sys.modules` after the agent steps. No flag turns it on;
     there is no import edge to turn on.
  3  `_holes` IS WRONG. It seeds its flood from the bbox BORDER cells, so an object occupying
     its own border blocks the flood and every interior cell reads as enclosed -- and it
     counts CELLS where the agent's atom counts enclosed REGIONS. 56 disagreements of 263
     objects on wa30; a 5x5 ring reads 9 against the correct 1. The one implementation is
     now `arc_percept.holes_of`, with `perimeter_of` beside it.
  4  MOST OF ITS 45 READINGS ARE NOT NEW. `contactPoints` IS the published `contact`;
     `dCells` IS `dcells`; `height`/`width` are `h`/`w`; `area`/`perimeter`/`holes` collide
     with registered ATOMS; and roughly twenty more are arithmetic over readings already
     published, which is the agent's job rather than perception's. The two that survived --
     `dholes` and `dperimeter` -- were extracted and now live behind `TETHER_SHAPE_DELTA`.

DELETION IS BLOCKED ON A SCOPE QUESTION, NOT ON WORK. `observer.py` consumes `scalar`,
`state`, `relation` and `temporal` -- the whole surface -- so removing this file means
removing the seat-side mapping cluster (observer, detectors, mapping, synth) with it. That is
wider than the ruling, so it is asked rather than assumed."""
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


def _holes(o: dict) -> int:
    """ENCLOSED holes -- interior background surrounded by the object, NOT bbox-minus-cells (which
    counts concavity: an L-shape has no hole). Flood-fill background from the bbox border; whatever
    it cannot reach is enclosed."""
    cells = {tuple(c) for c in o["cells"]}
    if not cells:
        return 0
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    r0, r1, c0, c1 = min(rs), max(rs), min(cs), max(cs)
    seen: set = set()
    stack = [(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)
             if (r, c) not in cells and (r in (r0, r1) or c in (c0, c1))]
    seen.update(stack)
    while stack:
        r, c = stack.pop()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if r0 <= nr <= r1 and c0 <= nc <= c1 and (nr, nc) not in cells and (nr, nc) not in seen:
                seen.add((nr, nc))
                stack.append((nr, nc))
    return (r1 - r0 + 1) * (c1 - c0 + 1) - len(cells) - len(seen)


def _perimeter(o: dict) -> int:
    """True cell-edge perimeter -- each cell edge with no in-object neighbour. The bbox perimeter
    2*(h+w) undercounts holes and concavity (a ring's inner boundary is real perimeter)."""
    cs = {tuple(c) for c in o["cells"]}
    p = 0
    for r, c in cs:
        p += sum((nr, nc) not in cs for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))
    return p


def scalar(o: dict) -> dict:
    """SCALAR/EXTENT/COUNT/COLOUR: ordinal magnitudes an object carries -- 699+ atoms.
    A scalar is a scalar; these are every magnitude the grid exposes per object."""
    h, w = o["h"], o["w"]
    cells = len(o["cells"])
    area = h * w
    return {
        "height": h, "width": w, "area": area, "occupiedCells": cells,
        "density": round(cells / area, 3) if area else 0.0,
        "perimeter": _perimeter(o), "extent": max(h, w), "girth": min(h, w),
        "aspect": round(max(h, w) / max(min(h, w), 1), 3),
        "colour": o["colour"], "holes": _holes(o),
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
    # TRUE cell-adjacency: A-cells with a 4-neighbour in B. The old bbox-gap test false-fired on
    # objects whose boxes abut but whose cells only touch diagonally.
    contact = 0 if inter else sum((r + dr, c + dc) in cb
                                  for r, c in ca for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    # spatial containment: a is a hollow container, b's box sits inside a's, and they are disjoint
    # (b in a's hole). The old cell-superset test never fired -- distinct objects share no cells.
    a_holes = ah * aw - len(ca)
    b_in_a = ar <= br and ac <= bc and ar + ah >= br + bh and ac + aw >= bc + bw
    return {
        "overlapArea": len(inter),
        "contactPoints": contact,
        "distance": max(abs((ar + ah / 2) - (br + bh / 2)), abs((ac + aw / 2) - (bc + bw / 2))),
        "contains": int(a_holes > 0 and b_in_a and not inter and len(ca) > len(cb)),
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
