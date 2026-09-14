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
        recol = a["colour"] != b["colour"]
        if drow or dcol or dh or dw or dcells or recol:
            effects.append({"kind": "change", "drow": drow, "dcol": dcol,
                            "dh": dh, "dw": dw, "dcells": dcells,
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
        acts = [steps[i]["action_id"] for i in c["idx"]]
        eff = _match(before, after)
        out.append({"level": c["level"], "ends_level": c["ends_level"],
                    "n_actions": len(c["idx"]), "actions": acts,
                    "n_obj_before": len(before), "n_obj_after": len(after),
                    "effects": eff, "signature": _signature(eff)})
    return {"game": path, "n_steps": len(steps), "n_chunks": len(chunks),
            "levels": max((s["level"] or 0) for s in steps), "chunks": out}


def _summary(res: dict) -> dict:
    """Per-level effect tally over actor objects -- the shape of the answer key."""
    per_level: dict = {}
    for c in res["chunks"]:
        lv = per_level.setdefault(c["level"], {"chunks": 0, "actions": 0, "sig": {}})
        lv["chunks"] += 1
        lv["actions"] += c["n_actions"]
        for k, v in c["signature"].items():
            if k == "uniform_translate":
                continue
            lv["sig"][k] = lv["sig"].get(k, 0) + v
    return per_level


if __name__ == "__main__":
    res = analyse(sys.argv[1] if len(sys.argv) > 1 else "replays/ls20_human.ndjson")
    print(f"steps={res['n_steps']} chunks={res['n_chunks']} levels={res['levels']}")
    print("=== per-level net-effect signature (actors only) ===")
    for lv, d in sorted(_summary(res).items(), key=lambda kv: (kv[0] is None, kv[0])):
        print(f"  L{lv}: {d['chunks']} chunks, {d['actions']} actions, {d['sig']}")
    print("=== first chunks (net signature) ===")
    for c in res["chunks"][:8]:
        s = c["signature"]
        print(f"  L{c['level']} acts={c['n_actions']} {s}"
              f"{' [ENDS LEVEL]' if c['ends_level'] else ''}")
