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
            # SENSOR 7, AT THE ONE MOMENT BOTH FRAMES ARE IN HAND. A BIRTH GETS NO DELTA AND
            # NOT A ZERO: §12.2 requires a value or an explicit non-reading, and `0` would say
            # *it did not move* where the truth is *there was nothing to move from*. An absent
            # slot is what the loop already handles -- *a new slot has no history and owes
            # nothing yet* -- so absence is the reading.
            prev = self.tracked.get(best)
            if prev is not None:
                dr, dc = delta_of(prev, obj)
                obj = {**obj, "drow": dr, "dcol": dc}
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
            for attr in ("row", "col", "h", "w", "colour", "drow", "dcol"):
                if attr in obj:
                    state[f"{name}.{attr}"] = int(obj[attr])
        return state
