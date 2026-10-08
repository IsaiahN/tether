"""cue_bridge: which library READINGS changed this frame, from the observer's cue (M1,
docs/cohesion/METAPROGRAMMING_DESIGN.md; the reviewer's ruling 2026-10-08 20:45Z, path B).

`changed_readings(cue) -> {reading: count}`, the input `Library.light` ranks entries by. It
reads `cue["mutations"]["deltas"]`, the observer's per-delta counts, and never the classes
beside them: a class names a change ("position"), the delta describes it ("drow"), so a one-row
move lights drow and not dcol. Value-free: counts of objects that changed, never a value a
frame held (colours are redrawn each load; boards may be turned).

ONE TABLE, DATA. A delta the library reads maps to its reading; a delta it has no reading for
is declared KNOWN-AND-UNMAPPED and counted, never dropped; a delta in neither list raises, so a
new observer delta fails here and in the perception seat rather than lighting nothing in
silence. `tether._CUE_ATTR` (class -> world attribute) and `inherited.RAW_TAGS` (attribute ->
tag) state DIFFERENT correspondences, so this table is not derived from them.
"""
from __future__ import annotations

# observer delta key -> library reading
READING = {
    "drow": "drow", "dcol": "dcol", "dh": "dh", "dw": "dw", "dcells": "dcells",
    "recolour": "colour_changed",       # the observer's name for it; the library's reading
    "dHoles": "dholes",                 # heavy deltas are camel-cased in sensors_heavy
    "dPerimeter": "dperimeter",
}
# observer deltas the library holds no reading for: seen, counted, not lit
UNMAPPED = ("dArea", "dCells", "dDensity", "dGirth", "dSolid", "dOrientation", "velocity")
# objects that appeared / vanished this frame, as the library's frame readings
EVENTS = {"appeared": "came", "vanished": "gone"}


def changed_readings(cue: dict | None, unmapped: dict | None = None) -> dict[str, int]:
    """The readings that moved this frame, with how many objects moved on each. A blind frame
    (no cue) is an abstention and reads {}. Pass `unmapped` to collect the deltas seen that the
    library cannot read."""
    if not cue:
        return {}
    muts = cue.get("mutations") or {}
    out: dict[str, int] = {}
    for key, n in (muts.get("deltas") or {}).items():
        if not n:
            continue
        if key in READING:
            out[READING[key]] = out.get(READING[key], 0) + int(n)
        elif key in UNMAPPED:
            if unmapped is not None:
                unmapped[key] = unmapped.get(key, 0) + int(n)
        else:
            raise KeyError(f"cue delta {key!r} is in neither cue_bridge.READING nor UNMAPPED: "
                           f"a new observer delta needs a row here before it can light anything")
    for key, reading in EVENTS.items():
        if muts.get(key):
            out[reading] = out.get(reading, 0) + int(muts[key])
    return out
