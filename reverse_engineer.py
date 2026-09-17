"""Reverse-engineer a human-panel replay into chunks and explain the derivation.

PROCTOR-SIDE. Reads a human replay (the answer set), perceives each frame in the AGENT's own
vocabulary (arc_percept.components -> the frozen 8 attributes + relations), chunks the action
sequence (~5-10 actions, never across a level boundary), and describes each chunk's EFFECT --
what changed, in the frozen vocabulary, relatively (colour is a distinctness id, never a literal).

It EXPLAINS the derivation; it is not how to win. The output (the answer key) is written under
replays/ (gitignored, out of the agent's reach). A chunk whose effect cannot be stated in the
frozen vocabulary is logged as an inexpressibility gap -- evidence, never a reason to add
perception (docs/TRAINING_PLAN.md sec 13; VOCABULARY_FROZEN.md).
"""
from __future__ import annotations

import json
import sys

import arc_percept

# anchor: Isaiah's ~5-10-action window (2026-09-14), midpoint 8 -- a declared convention, not
# derived, adjustable; big enough to house a multi-step routine past max_depth 3.
CHUNK = 8


def load_replay(path: str) -> list[dict]:
    """One record per step: {action_id, grid, level, state, avail}."""
    steps = []
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        d = json.loads(line).get("data", {})
        frame = d.get("frame")
        if frame is None:
            continue
        grid = frame[-1] if frame and isinstance(frame[0], list) else frame
        # A board-less frame (empty grid) is a transition, not a state -- perception raises on
        # it (`as_index_grid` returns None). Skip it: it carries no objects to read. cn04 has one
        # at frame 390 of 779, and it crashed the whole game's answer key.
        if not grid or not grid[0]:
            continue
        ai = d.get("action_input") or {}
        steps.append({"action_id": ai.get("id"),
                      "xy": (ai.get("data") or {}),
                      "grid": grid,
                      "level": d.get("levels_completed"),
                      "state": d.get("state"),
                      "avail": d.get("available_actions")})
    return steps


def _actors(objs: list[dict]) -> list[dict]:
    """Drop the background: the single largest component (the board field is one connected
    same-colour region and swamps the diff). What remains are the actor objects -- the things
    that move and change. A reading, not a rule: if a game has no dominant field this keeps
    everything but the biggest, which is the honest default."""
    if not objs:
        return []
    big = max(objs, key=lambda o: len(o["shape"]))
    return [o for o in objs if o is not big]


# anchor: two objects are "the same object" across a chunk only if the smaller keeps at least
# this fraction of the larger's cells -- SIZE is what an object conserves under movement, where
# position is not. A projectile stays ~4 cells wherever it flies; a region that contracts loses
# cells gradually and stays above the floor; a genuinely new object has no size-mate. 0.5 is a
# declared floor, not derived, adjustable -- it is the identity gate, and position only breaks
# ties among the pairs that pass it.
SIZE_KEEP = 0.5


def _cost(b: dict, a: dict) -> float:
    """How unlike a before-object and an after-object are, in the frozen attributes only. SIZE
    difference dominates (the conserved identity); position drift is a light tiebreak, so a
    far-moving object of the same size still matches. Does NOT require shape or colour to match
    -- a contraction changes shape and a recolour changes colour, and matching on either mis-reads
    those as vanish+appear (the F129b defect, and the too-tight position cutoff after it)."""
    cb, ca = len(b["cells"]), len(a["cells"])
    return abs(ca - cb) + 0.1 * (abs(a["row"] - b["row"]) + abs(a["col"] - b["col"])
                                 + abs(a["h"] - b["h"]) + abs(a["w"] - b["w"]))


def _match(before: list[dict], after: list[dict]) -> list[dict]:
    """Match actor objects across two frames on conserved SIZE (position as tiebreak), then report
    each matched pair's change as attribute DELTAS (drow, dcol, dh, dw, dcells) plus a relative
    colour verdict (same/different -- never a literal). A pair failing the SIZE_KEEP gate is not
    one object: the before vanished, the after appeared. Background (largest component) dropped."""
    before, after = _actors(before), _actors(after)
    pairs = sorted((( _cost(b, a), bi, ai)
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
                            "recolour": recol, "shape": len(b["cells"])})
    for bi in ub:
        effects.append({"kind": "vanish", "at": (before[bi]["row"], before[bi]["col"]),
                        "shape": len(before[bi]["cells"])})
    for ai in ua:
        effects.append({"kind": "appear", "at": (after[ai]["row"], after[ai]["col"]),
                        "shape": len(after[ai]["cells"])})
    return effects


def _signature(effects: list[dict]) -> dict:
    """The chunk's net effect as one compact, ground-checkable signature in frozen attributes.
    This is the answer-key layer the RL goal-selection reads -- an EFFECT, not a derivation."""
    ch = [e for e in effects if e["kind"] == "change"]
    return {"moved": sum(1 for e in ch if e["drow"] or e["dcol"]),
            "resized": sum(1 for e in ch if e["dh"] or e["dw"] or e["dcells"]),
            "recoloured": sum(1 for e in ch if e["recolour"]),
            "vanished": sum(1 for e in effects if e["kind"] == "vanish"),
            "appeared": sum(1 for e in effects if e["kind"] == "appear"),
            # the net translation, if the movers agree on one -- a translate is the cheapest
            # thing to express, so it is worth naming when it is present and uniform.
            "uniform_translate": _uniform([(e["drow"], e["dcol"]) for e in ch
                                           if e["drow"] or e["dcol"]])}


def _uniform(deltas: list[tuple]) -> tuple | None:
    return deltas[0] if deltas and len(set(deltas)) == 1 else None


# The frozen vocabulary the composition may name (VOCABULARY_FROZEN.md, arc_atoms sha 3f85bced).
# ACTION-AGNOSTIC: nothing here names an action -- a composition is what makes a transformation
# possible (attributes/relations), never the button that triggers it (Isaiah, 2026-09-14).
FROZEN_EXTRACTORS = frozenset({"colour", "row", "col", "h", "w", "drow", "dcol", "shape"})
FROZEN_RELATIONS = frozenset({"touching", "above"})   # arity-2 relations the agent can bet on today


def _touch(b: dict, o: dict) -> bool:
    """4-adjacency between two objects' absolute cells -- the frozen `touching` relation."""
    bc = b["cells"]
    for (r, c) in o["cells"]:
        if (r + 1, c) in bc or (r - 1, c) in bc or (r, c + 1) in bc or (r, c - 1) in bc:
            return True
    return False


def _referent(o: dict, colour: int, others: list[dict]) -> str | None:
    """For a recolour, name the frozen relation to an object that already holds the new colour --
    `touching` or `above`. Returns the relation name, or None if no such referent (which makes the
    recolour RULE inexpressible in the frozen set: the key does not invent the missing relation)."""
    for x in others:
        if x is o or x["colour"] != colour:
            continue
        if _touch(o, x):
            return "same(colour, touching)"
        if x["row"] < o["row"] and not (x["col"] + x["w"] <= o["col"]
                                         or o["col"] + o["w"] <= x["col"]):
            return "same(colour, above)"
    return None


def _compose(before: list[dict], after: list[dict]) -> dict:
    """Reverse-engineer a chunk's before->after transformation into a COMPOSITION over the frozen
    vocabulary -- action-agnostic -- and a per-statement expressibility verdict. A statement that
    cannot be written in the frozen set is a gap (with what it would need), never a reason to add
    perception. This is the answer key's derivation layer; the effect signature is its verification
    layer."""
    ba, aa = _actors(before), _actors(after)
    # reuse the same size-conserved matching the signature uses, but keep the object refs
    pairs = sorted((( _cost(b, a), bi, ai) for bi, b in enumerate(ba) for ai, a in enumerate(aa)),
                   key=lambda t: t[0])
    ub, ua = set(range(len(ba))), set(range(len(aa)))
    stmts, gaps = [], []
    matched = []
    for _c, bi, ai in pairs:
        if bi not in ub or ai not in ua:
            continue
        cb, ca = len(ba[bi]["cells"]), len(aa[ai]["cells"])
        if min(cb, ca) < SIZE_KEEP * max(cb, ca):
            continue
        ub.discard(bi)
        ua.discard(ai)
        matched.append((ba[bi], aa[ai]))
    for b, a in matched:
        if a["row"] != b["row"] or a["col"] != b["col"]:
            stmts.append({"op": "translate", "attrs": ["row", "col"],
                          "delta": [a["row"] - b["row"], a["col"] - b["col"]], "expressible": True})
        if a["h"] != b["h"] or a["w"] != b["w"]:
            stmts.append({"op": "rescale", "attrs": ["h", "w"],
                          "delta": [a["h"] - b["h"], a["w"] - b["w"]], "expressible": True})
        elif len(a["cells"]) != len(b["cells"]) or a["shape"] != b["shape"]:
            stmts.append({"op": "reshape", "attrs": ["shape"], "expressible": True})
        if a["colour"] != b["colour"]:
            ref = _referent(a, a["colour"], [o for o in aa if o is not a])
            if ref:
                stmts.append({"op": "recolour", "attrs": ["colour"], "rule": ref,
                              "expressible": True})
            else:
                stmts.append({"op": "recolour", "attrs": ["colour"], "rule": None,
                              "expressible": False})
                gaps.append({"gap": "recolour rule references no touching/above object of the new "
                             "colour -- the referent is a relation not in the frozen set",
                             "fix?": "a colour-source relation (nearest-same, contains, or a "
                             "global palette map) -- re-derived at threshold, not taken here"})
    # population change -- count is frozen, but the TRIGGER (why things spawn/die) is usually not
    n_van, n_app = len(ub), len(ua)
    if n_van or n_app:
        stmts.append({"op": "population", "attrs": ["count"], "vanished": n_van,
                      "appeared": n_app, "expressible": True,
                      "note": "count change is frozen; the spawn/death TRIGGER is not modelled"})
        if n_van + n_app >= 3:
            gaps.append({"gap": "systematic spawn/death within the chunk -- the trigger is a "
                         "conditional/event the one-in-one-out atom signature cannot bet on",
                         "fix?": "arity>=2 event relation (NSM frame holds arity) -- re-derived "
                         "at threshold"})
    return {"statements": stmts, "gaps": gaps,
            "expressible": all(s["expressible"] for s in stmts) and not gaps,
            "n_matched": len(matched)}


def chunk_replay(steps: list[dict], size: int = CHUNK) -> list[dict]:
    """Chunk by action, never across a level boundary."""
    chunks, cur = [], []
    for i, s in enumerate(steps):
        cur.append(i)
        level_boundary = (i + 1 < len(steps) and steps[i + 1]["level"] != s["level"])
        if len(cur) >= size or level_boundary or i == len(steps) - 1:
            chunks.append({"idx": cur[:], "level": s["level"],
                           "ends_level": level_boundary})
            cur = []
    return chunks


def analyse(path: str) -> dict:
    steps = load_replay(path)
    chunks = chunk_replay(steps)
    perceived = [arc_percept.components(s["grid"]) for s in steps]
    out = []
    for c in chunks:
        i0, i1 = c["idx"][0], c["idx"][-1]
        before, after = perceived[i0], perceived[i1]
        eff = _match(before, after)
        # ACTION-AGNOSTIC: the chunk is a WINDOW OF FRAMES, not a sequence of actions. Frame
        # indices are proctor window markers; the answer key's content -- signature + composition
        # -- names no action (Isaiah, 2026-09-14).
        out.append({"level": c["level"], "ends_level": c["ends_level"],
                    "frames": [i0, i1], "n_frames": len(c["idx"]),
                    "n_obj_before": len(before), "n_obj_after": len(after),
                    "signature": _signature(eff), "composition": _compose(before, after)})
    return {"game": path, "n_steps": len(steps), "n_chunks": len(chunks),
            "levels": max((s["level"] or 0) for s in steps), "chunks": out}


def answer_key(path: str) -> dict:
    """The per-game answer key (TRAINING_PLAN.md §13): every chunk's ground-checkable EFFECT
    (verification) and action-agnostic COMPOSITION (the reasoning that makes it possible), plus the
    inexpressibility gaps for the demand log. Proctor-side -- written under replays/, out of the
    agent's reach; never fed to the agent as a target."""
    res = analyse(path)
    gaps = [{"level": c["level"], "frames": c["frames"], **g}
            for c in res["chunks"] for g in c["composition"]["gaps"]]
    expressible = sum(1 for c in res["chunks"] if c["composition"]["expressible"])
    return {"game": res["game"], "n_chunks": res["n_chunks"], "levels": res["levels"],
            "expressible_chunks": expressible,
            "inexpressible_chunks": res["n_chunks"] - expressible,
            "n_gaps": len(gaps), "gaps": gaps, "chunks": res["chunks"]}


def _summary(res: dict) -> dict:
    """Per-level effect tally over actor objects -- the shape of the answer key."""
    per_level: dict = {}
    for c in res["chunks"]:
        lv = per_level.setdefault(c["level"], {"chunks": 0, "frames": 0, "sig": {}, "inexpr": 0})
        lv["chunks"] += 1
        lv["frames"] += c["n_frames"]
        lv["inexpr"] += 0 if c["composition"]["expressible"] else 1
        for k, v in c["signature"].items():
            if k == "uniform_translate":
                continue
            lv["sig"][k] = lv["sig"].get(k, 0) + v
    return per_level


if __name__ == "__main__":
    import json as _json
    game_path = sys.argv[1] if len(sys.argv) > 1 else "replays/ls20_human.ndjson"
    key = answer_key(game_path)
    print(f"chunks={key['n_chunks']} levels={key['levels']} "
          f"expressible={key['expressible_chunks']} inexpressible={key['inexpressible_chunks']} "
          f"gaps={key['n_gaps']}")
    print("=== per-level (signature + inexpressible chunk count) ===")
    per_lv = sorted(_summary({"chunks": key["chunks"]}).items(),
                    key=lambda kv: (kv[0] is None, kv[0]))
    for lv, d in per_lv:
        print(f"  L{lv}: {d['chunks']} chunks ({d['inexpr']} inexpr), "
              f"{d['frames']} frames, {d['sig']}")
    print("=== first chunks (composition) ===")
    for c in key["chunks"][:6]:
        comp = c["composition"]
        ops = [s["op"] for s in comp["statements"]]
        print(f"  L{c['level']} frames{c['frames']} expressible={comp['expressible']} ops={ops}")
    if len(sys.argv) > 2 and sys.argv[2] == "--write":
        out = f"replays/{game_path.split('/')[-1].split('_')[0]}_answer_key.json"
        with open(out, "w", encoding="utf-8") as fh:
            _json.dump(key, fh, indent=1, default=str)
        print(f"WROTE {out} (proctor-side, out of the agent's reach)")
