"""Reading one frame against the next: which objects are the actors, and what changed.

SPLIT OUT OF `reverse_engineer.py` (reviewer ruling, 2026-09-20). These four were never
replay-bound -- they are pure functions over perceived object dicts -- and they lived in the
answer-key module only because that is where they were first needed. The cost of that housing
was structural: `observer.py` had to import the ANSWER-KEY READER to reach them, so anything
importing the observer pulled a replay reader transitively.

THE FIREWALL IS THE IMPORT GRAPH, NOT A RULE THAT REMEMBERS. Same move as `closure_map.py`:
the reviewer refused a provenance-aware lint rule because runtime provenance cannot be checked
statically, and *a firewall that only holds when the caller is careful is a convention with a
lint rule painted on it.* So the split does the work.

THIS MODULE IMPORTS NOTHING, which is the property under test. It reads whatever object lists
it is handed -- live frames at runtime, replay frames when the seat is grading -- and it cannot
tell the difference, because it never opens anything. The SOURCE distinction lives in the
caller, which is where the reviewer ruled it belongs.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

# anchor: two objects are "the same object" across a chunk only if the smaller keeps at least
# this fraction of the larger's cells -- SIZE is what an object conserves under movement, where
# colour and shape do not. 0.5 is a declared floor, not derived, adjustable -- it is the identity
# gate, and position only breaks ties among the pairs that pass it.
SIZE_KEEP = 0.5


def actors(objs: list[dict]) -> list[dict]:
    """Drop the background: the single largest component (the board field is one connected
    same-colour region and swamps the diff). What remains are the actor objects -- the things
    that move and change. A reading, not a rule: if a game has no dominant field this keeps
    everything but the biggest, which is the honest default."""
    if not objs:
        return []
    big = max(objs, key=lambda o: len(o["shape"]))
    return [o for o in objs if o is not big]


def cost(b: dict, a: dict) -> float:
    """How unlike a before-object and an after-object are, in the frozen attributes only. SIZE
    difference dominates (the conserved identity); position drift is a light tiebreak, so a
    far-moving object of the same size still matches. Does NOT require shape or colour to match
    -- a contraction changes shape and a recolour changes colour, and matching on either mis-reads
    those as vanish+appear (the F129b defect, and the too-tight position cutoff after it)."""
    cb, ca = len(b["cells"]), len(a["cells"])
    return abs(ca - cb) + 0.1 * (abs(a["row"] - b["row"]) + abs(a["col"] - b["col"])
                                 + abs(a["h"] - b["h"]) + abs(a["w"] - b["w"]))


def match(before: list[dict], after: list[dict]) -> list[dict]:
    """Match actor objects across two frames on conserved SIZE (position as tiebreak), then report
    each matched pair's change as attribute DELTAS (drow, dcol, dh, dw, dcells) plus a relative
    colour verdict (same/different -- never a literal). A pair failing the SIZE_KEEP gate is not
    one object: the before vanished, the after appeared. Background (largest component) dropped."""
    before, after = actors(before), actors(after)
    pairs = sorted(((cost(b, a), bi, ai)
                    for bi, b in enumerate(before) for ai, a in enumerate(after)),
                   key=lambda t: t[0])
    ub, ua = set(range(len(before))), set(range(len(after)))
    effects = []
    for _cst, bi, ai in pairs:
        if bi not in ub or ai not in ua:
            continue
        cb, ca = len(before[bi]["cells"]), len(after[ai]["cells"])
        if min(cb, ca) < SIZE_KEEP * max(cb, ca):
            continue
        ub.discard(bi)
        ua.discard(ai)
        b, a = before[bi], after[ai]
        drow, dcol = a["row"] - b["row"], a["col"] - b["col"]
        dh, dw = a["h"] - b["h"], a["w"] - b["w"]
        dcells = len(a["cells"]) - len(b["cells"])
        dshape = a["shape"] != b["shape"]  # shape id changed: a pure rotate/reflect
        recol = a["colour"] != b["colour"]
        if drow or dcol or dh or dw or dcells or dshape or recol:
            effects.append({"kind": "change", "drow": drow, "dcol": dcol,
                            "dh": dh, "dw": dw, "dcells": dcells, "dshape": dshape,
                            "recolour": recol, "shape": len(b["cells"]),
                            "bi": bi, "ai": ai})
    for bi in ub:
        effects.append({"kind": "vanish", "at": (before[bi]["row"], before[bi]["col"]),
                        "shape": len(before[bi]["cells"])})
    for ai in ua:
        effects.append({"kind": "appear", "at": (after[ai]["row"], after[ai]["col"]),
                        "shape": len(after[ai]["cells"])})
    return effects
