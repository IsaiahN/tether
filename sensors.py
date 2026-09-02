"""3a. The nine minimum sensors as §12.2 defines them -- typed, TOTAL, priced, in a registry.

**THE SEVEN THAT WERE "BUILT" WERE BUILT AS FUNCTIONS.** `arc_percept` supplies
`components`, `shape_of`, `overlap`, `touching` and the rest, and they work -- but §12.2 says
a sensor is a dataclass with six fields and four properties, and none of the four was present:
no attribute typing, no `NOT_RESOLVED`, no price, no registry. **`NOT_RESOLVED` did not occur
anywhere in the repository.** Which is the fourth step verbatim: the MECHANISM was present and
the CAPABILITY was not, and *is it built* returned yes.

**TOTALITY IS THE ONE THAT MATTERS, AND ITS ABSENCE WAS A LIVE CONFABULATION PATH.**
§12.2: *a sensor returns a value or `NOT_RESOLVED`. **Never a guess, never a default.** That
is abstention at the sensor level, and it is what lets "this instrument cannot see it"
propagate up instead of becoming a wrong attribute.* `components` returning `[]` is
**indistinguishable from "there are no objects"** -- so a perception failure entered the loop
as a FACT ABOUT THE WORLD. The whole architecture exists to keep those apart one level up, and
one level down they were being merged.

WRAPPED, NEVER REWRITTEN. Every `fn` below calls `arc_percept`. A second implementation of
`components` would be the reinvention no grep can see.

**AND THE PRICE IS DECLARED WITHOUT A UNIT, WHICH IS SAID RATHER THAN PAPERED OVER.** §12.2
gives `cost: int` and the bargain *a sensor that costs more than the residual it resolves is
not worth having* -- but a residual is in BITS and a sensor's cost is READS, and the corpus
never gives the conversion. So `cost` here is **reads per call, countable from the signature**,
and **the sensor bargain must not be run until the unit is settled.** Populating it with a
bits-like number would be the invented magic number, and comparing the two would be the same
error the seventh law names one level up.
"""
from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import arc_percept as P

sys.dont_write_bytecode = True

# OBJECT, not OBJ: `grammar` reserves OBJ for *a complete objective* and OBJECT for
# *a slot's identity*. A sensor reads a thing, so it takes OBJECT -- and `arc_atoms`
# now draws the same line, so all three files mean one thing by each word.
FRAME, OBJECT = "FRAME", "OBJECT"
# THE SAME SLOT, ONE FRAME EARLIER. `OBJ x OBJ` WAS A SPACE AND THE CODE MADE IT A TYPE, which
# is `ATTR`'s error at this layer -- and the corpus makes the distinction without being able to
# express it: §12.3 puts it in the PROSE column ("the slot is the *same* slot next frame" for 6,
# "motion" for 7, "contact" for 8) and §12.2's whole in-type vocabulary is
# `("FRAME","OBJ") | ("OBJ","OBJ") | ("ATTR","ATTR")`, which has no marker for time.
#
# So sensors 6 and 7 take a BEFORE/AFTER pair of ONE slot and sensor 8 takes TWO slots in ONE
# frame -- same type, opposite operands -- and `delta(x, x')` over two same-frame objects
# returned a position difference where motion was asked for, well-typed and unrefused.
#
# THIS IMPLEMENTS A DISTINCTION THE CORPUS DRAWS AND CANNOT SAY, which is what separates it
# from an exemption. It adds no sensor and refuses compositions previously admitted -- the
# `OBJECT`/`OBJ` split's standing, and that one removed 225 well-typed meaningless pipelines.
OBJECT_BEFORE = "OBJECT_BEFORE"
COLOUR, COUNT, POSITION, EXTENT = "COLOUR", "COUNT", "POSITION", "EXTENT"
SHAPE, BOOL, DELTA, AXIS, RATIO, REGION = "SHAPE", "BOOL", "DELTA", "AXIS", "RATIO", "REGION"

# WHICH DISTINCT TYPES ADD. `translate`'s rule is *`v + operand` is meaningful only between
# COMMENSURABLE quantities*, and it was implemented as `SAME_AS_TARGET` because identity was
# the only commensurable pair the type system could express. A position plus its own
# displacement is a position -- the affine operation -- and publishing `delta` as a slot type
# is what made the rule's own warrant reach further than its implementation.
#
# DECLARED AS A TABLE, NOT DERIVED. *Exemptions as data, not logic*: a pair can be pinned, and
# a predicate over type names would widen quietly the next time a type is added.
# ONE PAIR, NOT TWO. `(EXTENT, DELTA)` was written here and the warrant does not cover it:
# the affine operation is *a position plus its own displacement*, and the only deltas that
# exist are POSITION deltas, so `height + row-displacement` had nothing behind it but both
# being cell counts. Removed before it was ever read -- which is what a pinned table is for.
COMMENSURABLE = frozenset({frozenset((POSITION, DELTA))})


class _NotResolved:
    """§12.2's explicit non-reading. A singleton so `is` works and no value equals it."""

    _it = None

    def __new__(cls):
        if cls._it is None:
            cls._it = super().__new__(cls)
        return cls._it

    def __repr__(self) -> str:
        return "NOT_RESOLVED"

    def __bool__(self) -> bool:
        """FALSE, so a caller that forgets to check does not silently treat it as a reading."""
        return False


NOT_RESOLVED = _NotResolved()


@dataclass(frozen=True)
class Sensor:
    name: str
    fn: Callable[..., Any]
    in_types: tuple[str, ...]
    out_type: str
    origin: str          # prior | minted | imported
    cost: int            # READS per call. No unit shared with bits -- see the module note.


class Registry:
    """§12.1's *typed registry* -- the home SENSOR loads into, which is not Γ.

    Lookup is by TYPE, never by name, for the same reason as §15.3: **you ask by describing
    what you need, not by naming what you want.**
    """

    def __init__(self, sensors: list[Sensor] | None = None) -> None:
        self._by_name: dict[str, Sensor] = {}
        for s in sensors or []:
            self.add(s)

    def add(self, s: Sensor) -> None:
        if s.name in self._by_name:
            raise ValueError(f"two sensors named {s.name}")
        self._by_name[s.name] = s

    # THE DEBT BOOKED HERE IS PAID. `producing` / `accepting` are what make a registry more
    # than a dict, they were deferred to §12.4 because nothing composed sensors, and §12.4's
    # trigger now exists and needs them.

    # THE DEBT WAS BOOKED AS TWO AND ONE WAS OWED. `producing(out_type)` was named beside
    # `accepting` and the closure never needs it: a remedy asks for anything that SPLITS, not
    # for a chain ending in a chosen type. Written, refused by ISOLATED, removed. A booked debt
    # is a guess about what a mechanism will need, and it is worth checking against the
    # mechanism when the mechanism arrives.

    def accepting(self, *in_types: str) -> list[Sensor]:
        return [s for s in self._by_name.values() if s.in_types == tuple(in_types)]

    def closure(self, in_types: tuple[str, ...], max_depth: int) -> list[tuple[Sensor, ...]]:
        """Every sensor chain from `in_types`, each link accepting the last's output.

        **§12.2's third property made runnable** -- *a sensor's output can feed another's
        input, which is what makes the registry a closure rather than a list.* Enumerated in
        full and returned, because §12.4 needs its SIZE as a denominator: *we can know the
        closure of our own sensor set, and therefore we can still score whether abstention was
        correct.* An abstention without that number is a word.
        """
        out: list[tuple[Sensor, ...]] = []
        frontier = [(s,) for s in self.accepting(*in_types)]
        depth = 1
        while frontier and depth <= max_depth:
            out.extend(frontier)
            nxt: list[tuple[Sensor, ...]] = []
            if depth < max_depth:
                for chain in frontier:
                    nxt += [chain + (s,) for s in self.accepting(chain[-1].out_type)]
            frontier, depth = nxt, depth + 1
        return out

    def read(self, name: str, *args: Any) -> Any:
        """One call, and NOT_RESOLVED is returned rather than raised: an instrument that
        cannot see is a reading about the instrument, not an error in the loop."""
        s = self._by_name.get(name)
        if s is None:
            return NOT_RESOLVED
        try:
            return s.fn(*args)
        except (TypeError, ValueError, KeyError, IndexError, AttributeError):
            return NOT_RESOLVED

    def __len__(self) -> int:
        return len(self._by_name)

    def names(self) -> list[str]:
        return sorted(self._by_name)


# -- the nine. Each returns NOT_RESOLVED rather than a default. ---------------------------

def _grid(frame: Any) -> bool:
    """Can this be READ as a grid -- not is it a `list[list]`.

    THE FIRST VERSION TESTED THE PYTHON TYPE AND MANUFACTURED A FALSE ABSTENTION on the very
    first run: boards arrive as `ndarray`, so `isinstance(frame, list)` reported BLIND on a
    perfectly readable board. **A totality guard that is too strict is the same defect as one
    that is too loose, in the opposite direction** -- and the plan already names it for
    filters: *manufactures false abstentions.* Duck-typed, because the question is whether the
    instrument can see, not what the frame is made of.
    """
    try:
        return len(frame) > 0 and len(frame[0]) > 0
    except (TypeError, ValueError, IndexError, KeyError):
        return False


def _components(frame: Any) -> Any:
    if not _grid(frame):
        return NOT_RESOLVED          # not readable. `[]` here would assert "no objects".
    return P.components(frame)


def _attr(key: str, want: type | tuple[type, ...]) -> Callable[[Any], Any]:
    def fn(obj: Any) -> Any:
        if not isinstance(obj, dict) or key not in obj:
            return NOT_RESOLVED
        v = obj[key]
        return v if isinstance(v, want) else NOT_RESOLVED
    return fn


def _shape(obj: Any) -> Any:
    if not isinstance(obj, dict) or "cells" not in obj:
        return NOT_RESOLVED
    return P.shape_of(obj)


def _overlap(a: Any, b: Any) -> Any:
    if not isinstance(a, dict) or not isinstance(b, dict):
        return NOT_RESOLVED
    if "cells" not in a or "cells" not in b:
        return NOT_RESOLVED
    return P.overlap(P.shape_of(a), P.shape_of(b))


def _touching(a: Any, b: Any) -> Any:
    if not isinstance(a, dict) or not isinstance(b, dict):
        return NOT_RESOLVED
    return P.touching(a, b)


def _delta(a: Any, b: Any) -> Any:
    """Sensor 7 -- OWED until now. Motion, and the contingency test for self (§12.3)."""
    ra, ca = _attr("row", int)(a), _attr("col", int)(a)
    rb, cb = _attr("row", int)(b), _attr("col", int)(b)
    if NOT_RESOLVED in (ra, ca, rb, cb):
        return NOT_RESOLVED
    return P.delta_of(a, b)   # WRAPS, like the other four. It was a leaf, so nothing called it


def _changed(f1: Any, f2: Any) -> Any:
    """Sensor 9 -- OWED until now. Where to look (§12.3)."""
    if not _grid(f1) or not _grid(f2):
        return NOT_RESOLVED
    if len(f1) != len(f2) or any(len(r1) != len(r2) for r1, r2 in zip(f1, f2, strict=False)):
        return NOT_RESOLVED
    return frozenset((r, c) for r, row in enumerate(f1)
                     for c, v in enumerate(row) if v != f2[r][c])


def minimum_set() -> Registry:
    """§12.3's nine, and the criterion is *the loop cannot run without it*.

    **Which is why these are admissible under the entry rule** -- they enter under clause one,
    so the ablation stays blind to them and wiping them would test blindness rather than
    composition. **Tier 2 is deliberately absent**: §12.3 says symmetry, containment, holes,
    counting-by-colour and alignment must be REACHED, *because reaching is the only evidence
    the composition system works*, and the 2026-08-27 ruling makes loading them forbidden
    rather than merely ungenerous.
    """
    return Registry([
        Sensor("components", _components, (FRAME,), OBJECT, "prior", 1),
        Sensor("colour", _attr("colour", int), (OBJECT,), COLOUR, "prior", 1),
        Sensor("position", _attr("row", int), (OBJECT,), POSITION, "prior", 1),
        Sensor("extent", _attr("h", int), (OBJECT,), EXTENT, "prior", 1),
        Sensor("shape", _shape, (OBJECT,), SHAPE, "prior", 1),
        # 6 AND 7 ARE CROSS-FRAME BY §12.3's OWN PROSE. `overlap`'s BODY does not yet
        # match its type -- it returns IoU over NORMALISED SHAPES, which is congruence and
        # carries no position. The repair is deferred deliberately: cross-frame cell IoU is
        # what the tracker already computes, so it agrees with an existing quantity and
        # unlocks nothing. Typed correctly here so the mismatch is declared, not hidden.
        Sensor("overlap", _overlap, (OBJECT_BEFORE, OBJECT), RATIO, "prior", 2),
        Sensor("delta", _delta, (OBJECT_BEFORE, OBJECT), DELTA, "prior", 2),
        Sensor("touching", _touching, (OBJECT, OBJECT), BOOL, "prior", 2),
        Sensor("changed", _changed, (FRAME, FRAME), REGION, "prior", 2),
    ])
