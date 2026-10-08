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

import os
import sys
from typing import Any

sys.dont_write_bytecode = True

# THE OBSERVER ARM, SEAT-SIDE SWITCH, DEFAULT OFF -- the same switch `arc_world` reads.
# Item 1 clause 1 lives behind it here: the rest of the corpus's cheap mutation set,
# `observer._MUT_ATTR`'s `dh dw dcells recolour`, carried PER OBJECT rather than
# counted. Its `recolour` is published here as `colour_changed`: `observer` is SEAT-SIDE
# and its key never enters the agent's registry, where `recolour` is already taken.
# aggregated to a count (`F165`).
_OBSERVER = bool(os.environ.get("TETHER_OBSERVER"))

# THE SHAPE-DELTA ARM, DEFAULT OFF. `dholes`/`dperimeter`: how a matched object's CELL-SET
# quantities moved frame-to-frame. The reviewer cleared these on one test and it is worth
# keeping at the site -- **no atom accepts `OBJECT_BEFORE`.** It reaches exactly two SENSORS
# (`overlap`, `delta`) and zero atoms, so the agent cannot get at the previous object and
# genuinely cannot compose a cross-frame delta itself. The tracker holds both frames; the
# agent does not. That makes these PERCEPTION, on the same footing as `drow`/`dcol`, and not
# a composition being handed over.
#
# THE OTHER SEVEN HEAVY DELTAS ARE DELIBERATELY ABSENT. `dArea`, `dGirth`, `dDensity`,
# `dSolid`, `dOrientation` are arithmetic over quantities already published, and `dCells` IS
# `dcells` under a different capitalisation. Only the two whose BASE is a cell-set computation
# survive -- `holes` counts enclosed regions and `perimeter` counts exposed edges, and neither
# is reachable from `h`/`w`/`dcells`.
#
# PAIRS WITH ARM I RATHER THAN STANDING ALONE: the `holes` and `perimeter` ATOMS only resolve
# when `TETHER_SHAPE_DECODE` is on, so with arm I off the agent reads a delta of a quantity it
# cannot itself measure. Both arms belong on together; that is a measurement, not a default.
_SHAPE_DELTA = bool(os.environ.get("TETHER_SHAPE_DELTA"))

# THE CELL-CHANGE ARM, DEFAULT OFF (the reviewer, 2026-10-07; INDEX F492). WHERE a matched object's
# cells changed since the last frame: the cells added and removed, each as a count (EXTENT -- the
# type set has no COUNT, see `contact`) and a centroid (POSITION, floor of the mean). The shape id
# names a new outline and says nothing of WHERE it differs, so a contained object's move reaches
# its container only as a fresh name. Read only where `identity_of` is sure; otherwise unknown.
_CELL_CHANGE = bool(os.environ.get("TETHER_CELL_CHANGE"))
_CHANGE_ATTRS = ("add_n", "add_row", "add_col", "rem_n", "rem_row", "rem_col")

# THE EMBEDDED INSTRUMENT SET, DEFAULT OFF -- Part 12 item 3, Isaiah: *"we can't have the
# agent waste time reinventing gravity."* Distance, speed, persistence and the rest are PAID
# BILLS, available from frame 0 rather than derived at runtime.
#
# `age` IS THE FIRST AND IT UNBLOCKS SIX OF THE ELEVEN, because they were all waiting on the
# same absent quantity rather than on six mechanisms. Default OFF because a new published
# attribute widens the slot set, and §12.12 prices that in EPISODES FORGONE before it is
# defaulted on -- 26s an action buys 4-9 episodes in the whole competition window.
_INSTRUMENTS = bool(os.environ.get("TETHER_INSTRUMENTS"))


def as_index_grid(frame: Any) -> list[list[int]] | None:
    """THE INPUT ADAPTER, AHEAD OF LAYER 1. Two front ends, one output.

    An index-frame passes through; an image is quantized so that DISTINCT pixels become
    DISTINCT labels. Everything below reads a grid of distinct-labeled cells and cannot tell
    which ran. Detected per call from the shape of what arrived -- thin I/O, never a flag.

    `None` where the frame is not readable as either. An empty grid would assert *no board*.

    EXACT EQUALITY, AND NO TOLERANCE. Two pixels are the same label iff their channels are
    equal. A colour-distance cutoff would be an invented number at the one place the whole
    pipeline's distinctness is decided, and a render that anti-aliases will therefore split a
    region rather than silently merge two -- which is the direction that fails loudly.

    ---------------------------------------------------------------------------------------
    DO NOT REMOVE. This comment is long because it is the only record of a capability the
    build does not exercise: index-mode is what runs, and everything below describes the
    image-mode path that the same adapter takes when hue exists. Trimmed as dead-code notes,
    it takes the specification with it.

    Walk the RGB case. The rainbow is an ordered strip, and you read it in adjacent pairs --
    RO, OY, YG, GB, BI, IV -- so any hue falls between two anchors. A colour landing between
    green and blue is a GB, and it is `GB1` if it is the first thing met there, `GB2` if it is
    the second. The number is the ORDER IT WAS MET and never a rank: `GB2` is not more than
    `GB1`, it is later. Next play the palette rotates and every hue is wrong, and the agent
    does not go looking for the old ones -- it recognises the object by its SHAPE, which
    survives translation and recolour, and hands it the name it already had. The placement is
    re-taken; the identity never moved.

    AND THE STRIP IS STRUCK -- RULED 2026-09-05, AND THE REASON IS THE RULING AND NOT THE
    FORMAT. An earlier version of this comment said the strip had no producer BECAUSE a frame
    of indices carries no wavelength, and that hand real hue would bring it alive. Both are
    wrong. **Colour is COMPARABLE and not ORDERED**, and a band position is a more-and-less --
    so the strip is refused by the type ruling whatever the frame carries. Colour is a
    SEPARATOR: grouping needs distinctness, never order, and a band answers *how do these hues
    relate on a spectrum*, which is a question nothing here asks.

    So image-mode does NOT bring the strip alive. It does the opposite: it takes a real image
    and REMOVES everything except distinctness, distilling it to the same arbitrary integer
    labels an index frame already carries. Adding a spectrum would be adding meaning; image-mode
    subtracts until only *these are different* is left.

    AND IT PROVES NOTHING THE SIMPLE PATH DOES NOT, which is what settles it rather than the
    tidiness. The gradient machinery is already exercised on POSITION, EXTENT and DELTA -- the
    types with real orderings. A colour band would test that same machinery on an ordering
    colour must not have: redundant where it is not wrong, and wrong where it is not redundant.

    The walk above stays because a road not taken is worth recording WITH THE REASON, and the
    reason is this paragraph rather than the shape of the frame.

    AND THE SEAM IS THE POINT: both paths hand the next layer the same thing, a grid of
    distinct labels. Nothing downstream can tell which one ran, and that is the property the
    adapter exists to have. It is left legible here on purpose.
    ---------------------------------------------------------------------------------------
    """
    try:
        h = len(frame)
        if h == 0 or len(frame[0]) == 0:
            return None
        probe = frame[0][0]
    except (TypeError, ValueError, IndexError, KeyError):
        return None
    if not hasattr(probe, "__len__"):
        try:
            return [[int(v) for v in row] for row in frame]
        except (TypeError, ValueError):
            return None
    seen: dict[tuple, int] = {}
    out: list[list[int]] = []
    for row in frame:
        line = []
        for px in row:
            key = tuple(int(c) for c in px)
            line.append(seen.setdefault(key, len(seen)))
        out.append(line)
    return out


def components(board: Any) -> list[dict]:
    """§12.3 sensor 1. Connected same-symbol regions, 4-connectivity, flood fill.

    Returns one dict per object with its cells and the four sensors that make up a slot's
    predictable state: colour, position (top-left of the bounding box), extent.
    """
    board = as_index_grid(board)
    if board is None:
        # NOT `[]`. `sensors.py` names this exact hazard: *`components` returning `[]` is
        # indistinguishable from "there are no objects", so a perception failure enters the
        # loop as a fact about the world.* Raising keeps it a failure -- `Registry.read`
        # catches it into NOT_RESOLVED, which is the reading this deserves.
        raise ValueError("frame is readable as neither an index grid nor an image")
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


def delta_of(old: dict, new: dict) -> tuple[int, int]:
    """§12.3 sensor 7, `OBJ x OBJ -> DELTA`: **one object at two times, not two objects at
    one.**

    **THE SIGNATURE DOES NOT SAY WHICH, AND THE CORPUS SEPARATES THEM ONLY IN PROSE.** Of
    §12.3's three `OBJ x OBJ` sensors, `overlap` and `delta` are DIACHRONIC -- *the slot is
    the same slot next frame*, *motion and the contingency test for self* -- and `touching` is
    SYNCHRONIC, *contact, the default causal hypothesis*. The witness is in this file:
    `overlap(obj["cells"], old["cells"])` already reads one `OBJ x OBJ` sensor across time.

    **AND THE SENSOR EXISTED WITHOUT THIS FUNCTION, WHICH IS WHY NOTHING CALLED IT.** Four of
    the six wrap a perception function and all four are called every step; `_delta` and
    `_changed` were written as leaves and neither is called from the loop. **A sensor with no
    implementation here has nothing the tracker can reach for.**
    """
    return int(new["row"]) - int(old["row"]), int(new["col"]) - int(old["col"])


def shape_of(obj: dict) -> frozenset:
    """§12.3 sensor 5, `OBJ -> SHAPE`: the cell pattern at NORMALIZED OFFSETS.

    Normalized means relative to the object's own top-left, so it is POSITION-INDEPENDENT --
    which is what makes it identity under translation as well as under recolour.
    """
    return obj["shape"]


def identity_of(name: str, matches: dict, tracked: dict) -> str | None:
    """How `name` was re-found on the latest frame: "overlap", "unique-shape", "look-alike",
    "birth", or None when it is not tracked. ONE RULE FOR THE WHOLE AGENT: `ArcWorld.identity`
    (read by `restarted`, F479) and the cell-change readings both call this, so the two cannot
    drift. Sure = "overlap" or "unique-shape".

    A swap is possible only between twins BOTH re-found by shape in the same frame: a twin
    re-found by overlap was claimed first, so the shape search could not hand over its
    name. So "look-alike" is a shape match sharing its shape with another SHAPE match."""
    route = matches.get(name, (None,))[0]
    if name not in tracked or route is None:
        return None
    if route != "shape":
        return route
    mine = shape_of(tracked[name])
    twins = any(shape_of(tracked[n]) == mine
                for n, (r, _s) in matches.items() if n != name and r == "shape" and n in tracked)
    return "look-alike" if twins else "unique-shape"


def _cells_at(cells) -> tuple[int, int, int] | tuple[int, None, None]:
    """A cell set as (count, centroid row, centroid col), floor of the mean; an empty set has
    a count of 0 and no position to read."""
    n = len(cells)
    if not n:
        return 0, None, None
    return n, sum(r for r, _c in cells) // n, sum(c for _r, c in cells) // n


def overlap(a: frozenset, b: frozenset) -> float:
    """§12.3 sensor 6, typed `OBJ x OBJ -> RATIO`. Intersection over union.

    A RATIO and not a BOOL, which is why tracking matches by MAXIMUM overlap and there is no
    threshold to anchor. A cutoff here would be the `EPS`/`WARM` mistake one layer out: a
    number introduced where the specification says measurement.
    """
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def touching(a: dict, b: dict) -> bool:
    """§12.3 sensor 8, `OBJ x OBJ -> BOOL`: contact, the default causal hypothesis.

    4-adjacency between any cell of one and any cell of the other, matching the connectivity
    segmentation uses -- two objects touch on the same relation that would have merged them
    had they shared a colour. Using 8 here and 4 there would mean `touching` could be true of
    objects the segmenter would never have joined, which is a different relation wearing the
    same name.
    """
    cells = b["cells"]
    return any((r + dr, c + dc) in cells
               for r, c in a["cells"]
               for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def holes_of(cells) -> int:
    """ENCLOSED REGIONS of a cell set -- a figure-eight is TWO, not two cells' worth.

    **THE ONE IMPLEMENTATION, and it is here because there were two.** `arc_atoms._holes` lived
    inside `_shape_facts()` and `sensors_heavy._holes` computed something else entirely under
    the same name: it seeded its flood from the bbox BORDER cells, so an object occupying its
    own border -- a ring, a filled rectangle -- blocked the flood and every interior cell read
    as enclosed. Measured on `wa30`, 263 objects: **56 disagreements, one of them 5 against
    640.** It also counted CELLS where this counts REGIONS. Two quantities, one name, and
    neither site said so.

    Translation-invariant, so an offset shape and an absolute cell set give the same answer --
    which is why one function serves both the SHAPE atom and the per-object delta.
    """
    v = {tuple(c) for c in cells}
    if not v:
        return 0
    rs = [r for r, _ in v]
    cs = [c for _, c in v]
    # flood the COMPLEMENT from outside the bounding box; whatever the flood misses is
    # enclosed. A one-cell margin is what lets the outside connect around the shape.
    lo_r, hi_r, lo_c, hi_c = min(rs) - 1, max(rs) + 1, min(cs) - 1, max(cs) + 1
    seen, stack = set(), [(lo_r, lo_c)]
    while stack:
        r, c = stack.pop()
        if (r, c) in seen or (r, c) in v:
            continue
        if not (lo_r <= r <= hi_r and lo_c <= c <= hi_c):
            continue
        seen.add((r, c))
        stack += [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    left = {(r, c) for r in range(lo_r, hi_r + 1) for c in range(lo_c, hi_c + 1)
            if (r, c) not in v and (r, c) not in seen}
    regions = 0
    while left:
        regions += 1
        stack = [left.pop()]
        while stack:
            r, c = stack.pop()
            for nb in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if nb in left:
                    left.discard(nb)
                    stack.append(nb)
    return regions


def enclosed_of(cells) -> frozenset:
    """THE ENCLOSED CELLS THEMSELVES, not how many -- what `holes_of` counts regions of.

    `inside` needs the interior as a SET so another object can be tested against it, and
    splitting this out keeps ONE flood-fill rather than a second one that drifts. Same margin
    flood as `holes_of`: seed outside the bbox, and whatever the flood cannot reach is enclosed.
    """
    v = {tuple(c) for c in cells}
    if not v:
        return frozenset()
    rs = [r for r, _ in v]
    cs = [c for _, c in v]
    lo_r, hi_r, lo_c, hi_c = min(rs) - 1, max(rs) + 1, min(cs) - 1, max(cs) + 1
    seen, stack = set(), [(lo_r, lo_c)]
    while stack:
        r, c = stack.pop()
        if (r, c) in seen or (r, c) in v:
            continue
        if not (lo_r <= r <= hi_r and lo_c <= c <= hi_c):
            continue
        seen.add((r, c))
        stack += [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    return frozenset((r, c) for r in range(lo_r, hi_r + 1) for c in range(lo_c, hi_c + 1)
                     if (r, c) not in v and (r, c) not in seen)


def perimeter_of(cells) -> int:
    """EXPOSED CELL EDGES -- one per neighbour a cell does not have, so a concave boundary and
    a hole's inner wall both count. Not the bounding-box outline. Same one-implementation
    reason as `holes_of`."""
    v = {tuple(c) for c in cells}
    return sum(1 for r, c in v
               for nb in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if nb not in v)


def contact_faces(a: dict, b: dict) -> int:
    """HOW MANY CELL FACES THE TWO SHARE. The integer `RELATIONS.md` 1.1 names and says is
    missing: *"a grid makes these countable -- the number of shared cell-faces is an integer,
    and the agent has no atom that returns it."*

    **PUBLISHED AS THE QUANTITY RATHER THAN AS THE THREE-WAY KIND, and that is the point.**
    `contact_kind` already computed this and threw it away, returning `face`/`edge`/`point` --
    a categorical the loop would need an encoding for, where the count is already an integer
    and already ordinal: 0 shared faces is a corner touch, 1 is an edge, 2+ is a face, which
    is exactly the increasing-constraint order the subdivision encodes. **Reconstructing the
    count from the kind is the adjacent-row error; the kind is derived FROM the count here.**

    Shares `touching`'s 4-adjacency for the reason `touching` gives.
    """
    other = b["cells"]
    return sum(1 for r, c in a["cells"]
               for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if (r + dr, c + dc) in other)


def contact_kind(a: dict, b: dict) -> str | None:
    """RELATIONS.md 1.1: contact SUBDIVIDES BY DIMENSION, and the subdivision carries
    information the boolean does not.

        point contact   corner to corner      pivoting; minimal constraint
        edge contact    one cell face shared  sliding along; one axis constrained
        face contact    a run of shared faces pushing; two axes constrained

    *A grid makes these countable -- the number of shared cell-faces is an integer, and the
    agent has no atom that returns it.* This counts it.

    SEAT-SIDE AND NOT AN ATOM. §16.5: *you do not invent the list, you read it off the
    world.* System 0 needs the contact list to know what it has not tried; that is reading
    the world, not a term the agent composes with. It shares `touching`'s 4-adjacency for
    the reason `touching` gives -- 8 here and 4 there would be a different relation under
    the same name -- so `face`/`edge` count SHARED FACES and `point` is diagonal-only.
    """
    faces = contact_faces(a, b)
    cells, other = a["cells"], b["cells"]
    if faces >= 2:
        return "face"
    if faces == 1:
        return "edge"
    if any((r + dr, c + dc) in other
           for r, c in cells for dr, dc in ((1, 1), (1, -1), (-1, 1), (-1, -1))):
        return "point"
    return None


def kind_of(obj: dict) -> tuple:
    """What counts as the same KIND. **SHAPE, with a HOLE where the colour was.**

    **THE OLD KEY WAS `(colour, shape)`, AND ITS DEFENCE ANSWERED A DIFFERENT OBJECTION THAN
    §16.4 RAISES.** It read: *it is not a taxonomy -- colour and shape are what the sensors
    already report, not a category anyone named.* **§16.4 does not test PROVENANCE, it tests
    SURVIVAL** -- *a taxonomy learned from the public set **will not survive contact with a
    private one***. **Colour fails that twice**: it permutes on a refresh, and §16.4's own
    example is *a wall it has never seen*, whose colour is one it has never seen either.

    **AND THE ASYMMETRY ARGUMENT WAS SOUND FOR A SCOPE NOBODY STATED.** *Splitting is
    recoverable, conflation is the silent failure, so the finer key wins* holds WITHIN an
    episode. Across one, colour is a random relabel, so the finer key buys **both** directions:
    the same thing splits, and two different things merge on a colour nobody chose.

    **SHAPE IS THE HALF THAT ALREADY CARRIES IT.** `shape_of` is §12.3 sensor 5 at normalized
    offsets -- *identity under translation **as well as under recolour***. The invariance this
    key needs was already stated one function up.

    **AND THE COARSENING IS NOT FREE, SO IT IS MADE LOUD RATHER THAN CLAIMED HARMLESS.** Two
    same-shape objects of different colours now share a row, which is the direction the old
    docstring called silent. `Affordances` therefore RECORDS the colours that bind to each key
    this episode, and reports any key carrying more than one. **The conflation the old note
    said nothing about is now the thing that says so.**
    """
    return (obj["shape"],)


class Affordances:
    """§16.4's seven, per kind, learned by interaction.

    *"Wall" is not a category, it is a profile -- and the profile is what transfers, because a
    private-set game with a wall it has never seen still has a thing that blocks.*

    WHAT IS READABLE HERE AND WHAT IS NOT. All seven are defined by behaviour UNDER CONTACT,
    and contact needs a mover. Four of them further need to know which object is MINE:
    `blocks` and `passes` are about movement INTO a thing, which presupposes an avatar, and
    §16.2's control mode is what supplies one. **On a board with no avatar those stay unread
    rather than false** -- an unread affordance and an absent one are different claims, and
    the profile records which it is.
    """

    SEVEN = ("blocks", "passes", "moves_when_touched", "changes_on_touch",
             "triggers_remote", "terminates", "consumed")

    def __init__(self) -> None:
        self.seen: dict[tuple, dict[str, bool]] = {}
        # WHICH COLOURS BOUND TO EACH KEY, THIS EPISODE. The variable's binding, not the key:
        # the table is permanent and this is not, so it drops at a boundary with `bound` and
        # the map. It is also the conflation witness -- a key with two colours in it is a row
        # carrying two things.
        self.bindings: dict[tuple, set[int]] = {}

    def boundary(self) -> None:
        """Drop the bindings, keep the table. **Vocabulary permanent, instances transient.**"""
        self.bindings = {}

    def note(self, before: dict[str, dict], after: dict[str, dict],
             mover: str | None) -> None:
        """One contact event teaches one kind, over TRACKED objects.

        IDENTITY IS READ, NOT RE-DERIVED. A first version took raw component lists and
        matched survivors BY KIND -- and since a kind carries shape, an object that merely
        RESHAPED had no survivor of its kind and read `consumed: True`. **The background
        region scored consumed because something moved through it.** `Objects` already owns
        identity, by overlap and then by shape, so this reads it instead of inventing a
        second and worse answer to the same question.

        `mover` is the avatar's name when the control mode found one, and None otherwise --
        which leaves the movement-into readings UNREAD rather than guessed.
        """
        for name, o in before.items():
            partners = [q for n, q in before.items() if n != name and touching(o, q)]
            if not partners:
                continue
            key = kind_of(o)
            row = self.seen.setdefault(key, {})
            self.bindings.setdefault(key, set()).add(int(o["colour"]))
            survivor = after.get(name)
            if survivor is None:
                row["consumed"] = True
            elif survivor["cells"] != o["cells"]:
                # DISPLACED OR TRANSFORMED, and §16.4 names them separately: *moves-when-
                # touched: it DISPLACES on contact* against *changes-on-touch: it recolours
                # or TRANSFORMS*. Cell-set inequality alone conflates them -- the background
                # region read `moves_when_touched` because something moved THROUGH it.
                # Shape and position already separate the two; no new sensor is needed.
                same_shape = shape_of(survivor) == shape_of(o)
                if same_shape:
                    row["moves_when_touched"] = True
                else:
                    row["changes_on_touch"] = True
                if survivor["colour"] != o["colour"]:
                    row["changes_on_touch"] = True
            if mover is not None and any(n == mover for n, q in before.items()
                                         if q in partners):
                # contact WITH the avatar: whether it yielded is the blocks/passes read
                yielded = survivor is not None and survivor["cells"] != o["cells"]
                row["blocks"], row["passes"] = not yielded, yielded

    def profile(self, obj: dict) -> dict[str, bool | None]:
        """Seven readings. `None` means UNREAD -- never observed in contact -- which is a
        different claim from False and is kept distinct for the same reason `unreached` is
        kept distinct from `unreachable`."""
        row = self.seen.get(kind_of(obj), {})
        return {name: row.get(name) for name in self.SEVEN}

    def report(self) -> dict:
        multi = {str(k): sorted(v) for k, v in self.bindings.items() if len(v) > 1}
        return {"kinds": len(self.seen),
                # THE COARSENING, MADE LOUD. The old key's own objection to a coarse key was
                # *nothing says so*; this is what says so.
                "keys_carrying_two_colours": multi,
                "bound_this_episode": {str(k): sorted(v) for k, v in self.bindings.items()},
                "profiles": {str(k): v for k, v in sorted(self.seen.items(), key=str)},
                "reads": "behaviour under contact, per kind -- not a substance taxonomy"}


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
        # THE MATCH EVIDENCE, KEPT INSTEAD OF DISCARDED. The matcher computes an overlap score
        # for every (new x tracked) pair and throws all of it away but the winning name -- so
        # HOW an identity was established, and how certain the match was, were unreadable.
        # `{name: (route, score)}` per frame: `overlap` with its IoU, `shape` where overlap was
        # zero and §12.3's sensor 5 carried identity across a move, `birth` where nothing did.
        self.matches: dict[str, tuple[str, float]] = {}
        # THE ENCOUNTER HALF. `{raw value: placement}` in the order met, and per object the
        # placements it has held. **The SPECTRAL half is struck** -- colour is COMPARABLE and
        # not ORDERED, so there is no band and no more-and-less; a placement is the *n*th
        # distinct thing met and nothing else.
        #
        # PER PLAY, per Seam 10: the counter resets at `boundary` and a placement is only
        # readable beside the play that minted it. The raw value stays the live GROUPING key --
        # deciding whether a new object joins an existing class needs the value, not the label.
        self.placements: dict[int, int] = {}
        self.changes: dict[str, list[int]] = {}

    def boundary(self) -> None:
        """Drop what was bound to THIS play. **`_shapes` is NOT dropped** -- it is the
        structure table and is run-stable by design; placements are per play by Seam 10."""
        self.placements = {}
        self.changes = {}

    def __call__(self, board: Any) -> dict[str, int]:
        # AT CALL TIME, NOT AT IMPORT: `sensors` imports THIS module, so a module-level
        # import is a cycle. By the time any board is decomposed `sensors` is fully loaded.
        from sensors import NOT_RESOLVED
        if not hasattr(self, "_shapes"):
            self._shapes: dict = {}
        found = components(board)
        claimed: set[str] = set()
        fresh: dict[str, dict] = {}
        self.matches = {}

        # match each new component to the tracked object it overlaps most. Ties break on the
        # name so a run is reproducible; a zero-overlap component has no predecessor and is
        # a birth rather than a bad match.
        # TWO PASSES, AND THE SECOND ONE IS THE FIX -- F247. Shape is the FALLBACK for a move
        # overlap cannot see, and run inside ONE loop it OUTRANKED overlap: a zero-overlap
        # shape match claimed a name whose EXACT cells a later component held, and that
        # component was then issued a second identity for the same object. 180 of 180
        # exact-cell births on five boards had a thief, and every thief scored 0.0.
        # A fallback that can beat the primary is not a fallback.
        assign: dict[int, tuple[str | None, float]] = {}
        # A CONTESTED OVERLAP: the object this component overlaps most was already claimed by an
        # earlier one. COUNTED, not ruled on -- whether it makes an identity unsure is open until
        # a reading needs it (the reviewer, 2026-10-07).
        self.contested = 0
        for i, obj in enumerate(found):
            if _CELL_CHANGE:
                top = max(((overlap(obj["cells"], old["cells"]), n)
                           for n, old in self.tracked.items()), default=(0.0, None))
                if top[0] > 0.0 and top[1] in claimed:
                    self.contested += 1
            best, score = None, 0.0
            for name, old in self.tracked.items():
                if name in claimed:
                    continue
                r = overlap(obj["cells"], old["cells"])
                if r > score or (r == score and r > 0 and (best is None or name < best)):
                    best, score = name, r
            if best is not None and score > 0.0:
                claimed.add(best)
            else:
                best, score = None, 0.0
            assign[i] = (best, score)
        for i, obj in enumerate(found):
            if assign[i][0] is not None:
                continue
            # OVERLAP ALONE CANNOT TRACK A MOVE. An object smaller than its own
            # displacement has zero cell overlap with itself one frame later, so a
            # translation would read as a death and a birth -- and `translate` is in the
            # specified atom set, which is unobservable if translation destroys identity.
            # §12.3 sensor 5 is the answer: SHAPE at normalized offsets is
            # position-independent, so it carries identity across a move.
            best = next((n for n, old in sorted(self.tracked.items())
                         if n not in claimed and shape_of(old) == shape_of(obj)), None)
            if best is not None:
                claimed.add(best)
            assign[i] = (best, 0.0)

        for i, obj in enumerate(found):
            best, score = assign[i]
            route = "overlap" if best is not None and score > 0.0 else "shape"
            if best is None:
                best = f"o{self._next}"
                self._next += 1
                route = "birth"
            claimed.add(best)
            self.matches[best] = (route, round(score, 4))
            # IDENTITY IS THE POINTER AND PLACEMENT IS THE VALUE, so a colour change APPENDS
            # rather than renames: `best` is the object for the rest of the play whatever it
            # becomes, and the change-list is where what-it-has-been is kept. Append-only --
            # nothing leaves, which is `outstanding`'s shape at a third site.
            hue = obj.get("colour")
            if hue is not None:
                place = self.placements.setdefault(int(hue), len(self.placements))
                held = self.changes.setdefault(best, [])
                if not held or held[-1] != place:
                    held.append(place)
            # SENSOR 7, AT THE ONE MOMENT BOTH FRAMES ARE IN HAND. A BIRTH GETS NO DELTA AND
            # NOT A ZERO: §12.2 requires a value or an explicit non-reading, and `0` would say
            # *it did not move* where the truth is *there was nothing to move from*. An absent
            # slot is what the loop already handles -- *a new slot has no history and owes
            # nothing yet* -- so absence is the reading.
            prev = self.tracked.get(best)
            if prev is not None:
                dr, dc = delta_of(prev, obj)
                obj = {**obj, "drow": dr, "dcol": dc}
                if _OBSERVER:
                    # THE REST OF THE CHEAP MUTATION SET -- observer item 1 clause 1, and the
                    # set is the CORPUS'S rather than mine. `observer._MUT_ATTR` names the
                    # frozen deltas as `drow dcol dh dw dcells recolour`; the tracker carried
                    # them. NAMED `colour_changed` HERE, NOT `recolour` -- `recolour` is
                    # ALREADY an atom (`arc_predict:104`, `val -> val`, the grid transform
                    # the corpus files under OPERATION). Publishing this attribute under
                    # that name put TWO atoms called `recolour` in ONE registry.
                    # the first two and computed nothing for the other four, WHILE HOLDING BOTH
                    # RECORDS -- this is the one moment both frames are in hand.
                    #
                    # AND `F165` IS WHY IT MATTERS: `observer._mutations` does compute them and
                    # then `changed[attr] = changed.get(attr, 0) + 1` -- AGGREGATED TO A COUNT
                    # PER ATTRIBUTE, which throws away WHICH OBJECT changed. A count cannot key
                    # a lookup; a per-object delta can. *Carried, not counted.*
                    #
                    # `colour_changed` and `dcells` are BOOL and DELTA respectively, and
                    # the split is
                    # not cosmetic: colour is CATEGORICAL, so `new - old` on a hue is arithmetic
                    # over labels and means nothing, while a cell-count change is a magnitude
                    # that does. Publishing a colour difference would have invented a quantity.
                    obj = {**obj,
                           "dh": obj["h"] - prev["h"],
                           "dw": obj["w"] - prev["w"],
                           "dcells": len(obj["cells"]) - len(prev["cells"]),
                           "colour_changed": int(obj["colour"] != prev["colour"])}
                if _SHAPE_DELTA:
                    # The one moment both frames are in hand, same as the deltas above. A
                    # BIRTH still gets neither -- absence is the reading, never a zero.
                    obj = {**obj,
                           "dholes": holes_of(obj["cells"]) - holes_of(prev["cells"]),
                           "dperimeter": (perimeter_of(obj["cells"])
                                          - perimeter_of(prev["cells"]))}
            if _INSTRUMENTS:
                # HOW MANY CONSECUTIVE FRAMES THIS OBJECT HAS BEEN TRACKED. Zero at birth.
                #
                # THE TRACKER KEPT NO HISTORY AT ALL -- `self.tracked = fresh` replaces the
                # whole map every frame, and there was no age, lifetime or first-seen counter
                # anywhere. So `persistence`, `continuity`, `duration`, `trajectory`,
                # `repetition` and `stability` -- six of the eleven instruments Isaiah named --
                # were blocked on ONE missing quantity rather than on six missing mechanisms.
                #
                # AN INTEGER, NOT A PREDICATE, AND THE SPLIT IS §12.0's. *Has it persisted* is
                # a judgement the agent should make against whatever threshold the board wants;
                # *how many frames* is the reading. Publishing the predicate would hand it the
                # answer, publishing the count hands it the means.
                obj = {**obj, "age": (prev.get("age", 0) + 1) if prev is not None else 0}
                if prev is not None:
                    # HOW FAR IT MOVED THIS FRAME -- Chebyshev, so one diagonal step is 1 and
                    # not 2, matching the 4-neighbour world the segmenter already assumes.
                    #
                    # `speed` AND `velocity` ARE ONE QUANTITY HERE, AND ONLY ONE IS PUBLISHED.
                    # Isaiah's list names both. A slot holds ONE INT, so a vector has nowhere
                    # to live and both collapse to the magnitude -- publishing two names for
                    # it is `A6i` by construction. DIRECTION is not lost: `drow`/`dcol` carry
                    # the signed components and `sign` reads them.
                    #
                    # AND IT IS PUBLISHED RATHER THAN COMPOSED, WHICH NEEDS SAYING. `abs_delta`
                    # already gives |drow| from one slot, but the MAX over two slots is a
                    # cross-slot read and a chain applies to one slot at a time -- the arity
                    # wall. Isaiah ruled this set a PAID BILL not to be re-derived at runtime,
                    # and that ruling names `speed` explicitly, so it governs over §12.2.1's
                    # general composed-is-the-agent's-job test.
                    obj = {**obj, "speed": max(abs(obj["row"] - prev["row"]),
                                               abs(obj["col"] - prev["col"]))}
                    # CONSECUTIVE FRAMES UNCHANGED, reset to 0 the frame anything moves.
                    #
                    # DISTINCT FROM `age`, AND THE PAIR IS THE POINT: an object that moves every
                    # frame has HIGH age and ZERO stability. `age` counts frames TRACKED;
                    # `stability` counts frames UNCHANGED. Two quantities, and publishing only
                    # one would have lost the distinction between *has been here a long time*
                    # and *has been doing nothing*.
                    #
                    # THE CELL SET, NOT THE BOUNDING BOX. `row/col/h/w` are unchanged by a
                    # rotation inside a square box and by any recolour, so a box-only test
                    # would read a spinning object as stable. Colour is compared too, because
                    # `colour_changed` exists precisely to say a recolour is a change.
                    same = (obj["cells"] == prev["cells"] and obj["colour"] == prev["colour"])
                    obj = {**obj, "stability": (prev.get("stability", 0) + 1) if same else 0}
                else:
                    # A BIRTH HAS NOT BEEN STABLE FOR ANY FRAMES. Zero rather than absent,
                    # unlike the DELTAS above: *how long has it been unchanged* has a true
                    # answer at birth and it is none, where *how far did it move* has no answer
                    # because there was nothing to move from.
                    obj = {**obj, "stability": 0}
            fresh[best] = obj

        # DEATH ONLY ON EVIDENCE. An unmatched tracked object keeps its slots unless another
        # live object now holds its cells. Not found is occluded, not gone.
        live = frozenset().union(*(o["cells"] for o in fresh.values())) if fresh else frozenset()
        for name, old in self.tracked.items():
            if name in fresh:
                continue
            hidden = old["cells"] & live
            if not hidden:
                fresh[name] = old          # occluded: persists, unchanged
                if _CELL_CHANGE:
                    fresh[name] = {**old, **dict.fromkeys(_CHANGE_ATTRS)}
                continue
            # COVERED IS NOT DEAD -- ISAIAH'S OVERLAY RULING. This branch used to DROP the
            # object, and dropping it is what re-birthed it under a new name when the coverer
            # moved off. The name persists, so the identity does; the cells stay in the record
            # marked `covered`, which is *NULL, not removed*; and the PUBLISHED attributes are
            # withheld below, so a term bound to them cannot be expressed on them. Express-
            # before-judge (`gamma.refute` fires only on `mass > 0`) then makes it SUSPENDED
            # rather than FAILED. The record keeps its fields so `shape_of`/`delta_of` still
            # resolve and so there is something for the on-exit confirmation to check.
            # AND COVERED IS NOT THE SAME AS DESTROYED, WHICH THE FIRST BUILD COULD NOT TELL
            # APART AND PAID FOR. Marking every taken-over object covered turns DEATH into
            # permanent limbo: nothing ever exits, `tracked` grows without bound -- measured
            # lf52 59 -> 253 objects by frame 399, 190 of them 'covered' -- and every
            # per-slot loop grows with it until a 2.8s board does not finish in 12 minutes.
            #
            # THE DISCRIMINATOR IS ISAIAH'S OWN WORDING: *attribution by MOVER.* An overlay is
            # something that MOVED onto this ground and will move off it. So the cover counts
            # only if a component now holding these cells is one the tracker matched to an
            # existing object that was somewhere ELSE last frame. Cells taken by a new or
            # static occupant are DEATH ON EVIDENCE exactly as before -- the rule this branch
            # replaced, kept for the case it was actually written for.
            movers = [n for n, o in fresh.items()
                      if (o["cells"] & hidden) and n in self.tracked
                      and not (self.tracked[n]["cells"] & hidden)]
            if not movers:
                continue                   # taken over for good: dead, as it always was
            fresh[name] = {**old, "covered": hidden, "covered_by": tuple(sorted(movers))}
        if _CELL_CHANGE:
            for name, obj in fresh.items():
                prev = self.tracked.get(name)
                if prev is None or name not in self.matches or obj.get("covered"):
                    continue
                if identity_of(name, self.matches, fresh) in ("overlap", "unique-shape"):
                    an, ar, ac = _cells_at(obj["cells"] - prev["cells"])
                    rn, rr, rc = _cells_at(prev["cells"] - obj["cells"])
                    obj.update(add_n=an, add_row=ar, add_col=ac, rem_n=rn, rem_row=rr, rem_col=rc)
                else:
                    obj.update(dict.fromkeys(_CHANGE_ATTRS))
        self.tracked = fresh

        state: dict[str, int] = {}
        for name, obj in self.tracked.items():
            # SENSOR 5, PUBLISHED AS AN ENCOUNTER INDEX. A shape is a frozenset and a slot
            # is an int, which is the whole of why it was never published -- *the composable
            # set was decided by which sensors happened to return integers*. **The id is a
            # LABEL, exactly like `colour`**: arbitrary, comparable, never orderable.
            # Measured cost of leaving it out: 43 of 43 cell-changes on three boards moved no
            # published attribute, and shape moved in every one.
            #
            # ITS SCOPE, CORRECTED 2026-09-04 -- THE OLD TEXT SAID "valid only for the episode
            # it was assigned in" AND THE CODE DOES NOT DO THAT. `_shapes` is created once
            # under the `hasattr` guard above and is reset NOWHERE, and `Objects()` is built
            # once per run, so **the id is RUN-STABLE**. Three rounds of design read the old
            # claim and planned a durable replacement for a scope problem that was not there.
            #
            # **THE REAL DEFECT IS THAT IT IS ARBITRARY ACROSS RUNS AND ACROSS GAMES**, being
            # assigned by ARRIVAL ORDER rather than by content: the same shape is `3` here and
            # `11` in the next run, so it cannot key anything that must survive either. That
            # is the placement-versus-identity split at run scope -- the index is a PLACEMENT,
            # and the frozenset under it is the identity.
            # A COVERED OBJECT PUBLISHES `NOT_RESOLVED`, NOT NOTHING -- *NULL, NOT ABSENT*.
            # Every attribute here is computed over a cell set that includes the hidden
            # cells, so publishing a value asserts a reading of what nobody can see. But
            # OMITTING the key says something else and something false: `env.slots()` is
            # this dict's keys, so an omitted key means THE OBJECT IS GONE and `_present`
            # pops its bindings.
            #
            # The corpus draws the line three times and the seat had to be told: Layer 5 of
            # PERCEPTION_PIPELINE -- *where an attribute cannot be read it is NULL, NOT
            # ABSENT; null records "the instrument could not see it here", which is a
            # different claim from "the thing is not there"*; WHAT_THE_AGENT_SEES says it in
            # those words; TRAINING_PLAN initialises the schema null. §12.2 is the same line
            # one layer down. **The slot leaves the set when the OBJECT is gone -- departed,
            # fragmented, merged -- never when it is merely unreadable.**
            #
            # Suspension then needs nothing: `_predict` already returns None on
            # NOT_RESOLVED, so a covered slot is not bet on, no residual is claimed, and
            # `refute` never fires. Judgement resumes when the values come back.
            covered = bool(obj.get("covered"))
            # `dh`/`dw`/`dcells`/`colour_changed` are present only under the observer arm and only
            # on a matched object -- a BIRTH still gets no delta and not a zero, which is the
            # same rule `drow`/`dcol` state above.
            for attr in ("row", "col", "h", "w", "colour", "drow", "dcol",
                         "dh", "dw", "dcells", "colour_changed",
                         "dholes", "dperimeter", "age", "speed", "stability", *_CHANGE_ATTRS):
                if attr in obj:
                    state[f"{name}.{attr}"] = (NOT_RESOLVED if covered or obj[attr] is None
                                               else int(obj[attr]))
            state[f"{name}.shape"] = (
                NOT_RESOLVED if covered
                else self._shapes.setdefault(obj["shape"], len(self._shapes)))
        return state
