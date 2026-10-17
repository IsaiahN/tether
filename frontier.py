"""A1-CONVERT: THE ONE SHAPE OF A CHOICE (the reviewer 2026-10-15 09:12, 09:19, 09:33, 09:38;
Isaiah 09:11, 09:27). Imported by tether (the agent's choices) and by interface (how an intent
is realised), so neither copies it and neither imports the other for it.

    1  the residual gates (Fig 8 "Residual first, frame second"; Fig 7 "The room is summoned by the
       residual"): if any option's residual reading is > 0, the options at 0 leave;
    2  two readings held apart, never summed (Fig 12): (bits, actions); an option the others beat on
       the axes both read leaves (an axis no option reads is not an axis; None neither beats nor
       is beaten);
    3  among the frontier, the larger residual reading;
    4  the least-known, by the site's record count;
    5  the recorded draw, seeded as the hold is (tether _held_now), never a name or a position.

A reading is a number or None. `by` names the step that left exactly one option.
"""
from __future__ import annotations

import hashlib
import sys

sys.dont_write_bytecode = True

# THE OFF VALUE (TETHER_AGENT_SEED=0): the constant every run drew with before the agent drew its
# own. ON, each caller passes the agent's seed (HOLD_SEED, the reviewer 2026-10-15 14:56, 15:04).
SEED = "0"
BY = ("gate", "frontier", "residual", "learning", "draw")


def _beats(a: tuple, b: tuple) -> bool:
    ax = [(x, y) for x, y in ((a[1], b[1]), (a[2], b[2])) if x is not None and y is not None]
    return bool(ax) and all(x <= y for x, y in ax) and any(x < y for x, y in ax)


def draw_key(key: str, name, seed: str | None = None) -> int:
    """The recorded draw as a SORT POSITION, for a stream that is walked rather than picked from
    (A1 group 2, sites 4, 6-8): the same seed and hash as the pick's draw, one value per item, so a
    run tied on every reading is ordered by the draw, never by a name or a list position."""
    s = SEED if seed is None else seed
    h = hashlib.blake2b(f"{s}:{key}:{name!r}".encode(), digest_size=8).digest()
    return int.from_bytes(h, "big")


def frontier_pick(options: list, residual: dict | None, seen: dict | None, key: str,
                  seed: str | None = None) -> tuple:
    """options: (name, bits, actions). Returns (name, by, frontier names). An empty list is
    refused by name: there is nothing to choose, and the caller must not ask."""
    if not options:
        raise ValueError("frontier_pick: no options to choose among")
    room = options
    if residual is not None and any(residual.get(o[0], 0) > 0 for o in options):
        room = [o for o in options if residual.get(o[0], 0) > 0]
        if len(room) == 1:
            return room[0][0], "gate", [room[0][0]]
    # whether an option is beaten depends only on its two readings, and equal readings never beat
    # each other: so the frontier is taken over the DISTINCT readings, the same set as every pair
    # (D, 2026-10-16 night: an invention's exact tie of ~10^5 options made the pairwise check hang)
    reads = {(o[1], o[2]) for o in room}
    beaten = {r for r in reads if any(_beats((None, *q), (None, *r)) for q in reads if q != r)}
    front = [o[0] for o in room if (o[1], o[2]) not in beaten]
    pool = front
    if len(pool) == 1:
        return pool[0], "frontier", front
    for step, reading, best in (("residual", residual, max), ("learning", seen, min)):
        if reading is None:
            continue
        top = best(reading.get(n, 0) for n in pool)
        pool = [n for n in pool if reading.get(n, 0) == top]
        if len(pool) == 1:
            return pool[0], step, front
    pool = sorted(pool, key=repr)
    s = SEED if seed is None else seed
    h = hashlib.blake2b(f"{s}:{key}:{pool!r}".encode(), digest_size=8).digest()
    return pool[int.from_bytes(h, "big") % len(pool)], "draw", front
