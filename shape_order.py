"""THE SHAPE OF THE GAP AS THE WALK'S ORDER (step 8b-2, TETHER_SHAPE_WALK; the reviewer 2026-11-12
r1838, DESIGN_STEP8 B4; WATSON_2026-11-12_rank_ideas_by_the_shape_of_the_gap).

Isaiah 11-12 09:24: "even if i can only think 5-10 thoughts, these are the ten most likely". Fig 9
:25-32: "describe the effect rather than the cause -> you get a kind of thing, never the answer
itself"; :53 "Nobody chooses. The gap does, and the gap is only as good as its description."

`make_order_key` turns the gap's description into the key `Gamma.ordered_closure` walks by. It
ORDERS and never refuses (Fig 9 :40-41); the bargain still decides what is accepted (Fig 9 :60).

THE KEY, lower first:
  (stage, -E, -sense, -authority, -fits_whole, atoms)

  The walk's yields come out in EXACT (stage, E) order: both are optimistic for an open
  prefix. The later fields are tiebreaks only, read off the prefix as it stands.
  stage  0 when the chain starts with a head that paid under this context (recall), else 1.
  E      how many of the gap's WANTED readings the chain's atoms touch, read off the library's own
         declarations: an atom's `affects` and its `reads` (DESIGN_STEP8 Q3, widened: of the 79
         implemented entries only 4 declare `affects` -- recolour, reflect, rotate, translate -- so
         `affects` alone would leave E at 0 for almost every chain; `reads` is what the rest
         declare). For an OPEN prefix E is optimistic: what it touches plus what the remaining
         depth could still add, so ordered_closure's yields come out in exact E order.
  sense  1 when a sense of the chain's head predicts this gap (8b-1; 0 until it lands).
  authority  8c's tiebreak (0 until it lands).
  fits_whole retrieval.fits over the WHOLE chain's key, not its first unit.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any


def declared_readings(library: dict[str, Any]) -> dict[str, frozenset]:
    """atom name -> the readings its library entry declares it affects or reads.

    Built ONCE per library from each implemented entry's `run.impl` ("arc_atoms:translate" ->
    the atom `translate`). An atom with no implemented entry declares nothing (empty set)."""
    out: dict[str, frozenset] = {}
    for _key, e in library.items():
        if not isinstance(e, dict):
            continue
        impl = (e.get("run") or {}).get("impl")
        if not impl or ":" not in impl:
            continue
        name = impl.split(":", 1)[1]
        rs = frozenset(str(r) for r in (*(e.get("affects") or ()), *(e.get("reads") or ())))
        out[name] = out.get(name, frozenset()) | rs
    return out


def wanted(reading: str, extra: Iterable[str] = ()) -> frozenset:
    """The readings a term explaining `reading` would touch: the reading itself and its change
    (`col` <-> `dcol`, the delta naming the observer already uses), plus any the caller adds (the
    delta kind's own reading, the gap's varying readings)."""
    w = {reading}
    if reading.startswith("d") and len(reading) > 1:
        w.add(reading[1:])
    else:
        w.add("d" + reading)
    w.update(extra)
    return frozenset(w)


def make_order_key(want: frozenset, readings: dict[str, frozenset],
                   paid_heads: Iterable[tuple] = (),
                   sense_heads: Iterable[tuple] = (),
                   authority: Callable[[tuple], float] | None = None,
                   fits_whole: Callable[[tuple], int] | None = None,
                   ) -> Callable[[tuple, bool, int], tuple]:
    """The key for `Gamma.ordered_closure(order_key=...)`. `paid_heads` / `sense_heads` are atom
    tuples (a settled unit's atoms) that paid / have a sense predicting this gap under the
    context (8b-1); `authority(chain)` is 8c's tiebreak. All default to nothing."""
    paid = [tuple(h) for h in paid_heads if h]
    sensed = [tuple(h) for h in sense_heads if h]
    # what ANY single atom can add: the optimism bound for an open prefix
    reachable = frozenset().union(*readings.values()) & want if readings else frozenset()

    def starts(chain: tuple, heads: list, closed: bool) -> bool:
        """The chain starts with a head -- or, for an OPEN prefix, could still grow into one
        (it is itself a prefix of a head), so the prefix's stage stays optimistic."""
        names = tuple(a.name for a in chain)
        return any(names[:len(h)] == h or (not closed and h[:len(names)] == names)
                   for h in heads)

    def key(chain: tuple, closed: bool, depth_left: int) -> tuple:
        touched: set = set()
        for a in chain:
            touched |= readings.get(a.name, frozenset()) & want
        e = len(touched)
        if not closed:
            # optimistic: each further unit may add at most... every reachable reading not yet
            # touched (a unit can be a settled chunk of several atoms, so no per-step cap)
            e += len(reachable - touched) if depth_left > 0 else 0
        stage = 0 if paid and starts(chain, paid, closed) else 1
        sense = 1 if sensed and starts(chain, sensed, closed) else 0
        auth = authority(chain) if authority is not None else 0.0
        fw = fits_whole(chain) if (closed and fits_whole is not None) else 0
        # NO NAME IN THE KEY (Isaiah 11-08: "cant use text order"): equal keys keep the walk's
        # insertion order, which is the units' own order.
        return (stage, -e, -sense, -auth, -fw, len(chain))

    return key
