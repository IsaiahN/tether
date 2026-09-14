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


def _match(before: list[dict], after: list[dict]) -> list[dict]:
    """Match objects across two frames by shape then nearest position; report per-object effect
    in the frozen vocabulary. Colour is compared only as SAME/DIFFERENT (a distinctness id).
    Background excluded first."""
    before, after = _actors(before), _actors(after)
    effects = []
    used = set()
    for b in before:
        cand = [(i, a) for i, a in enumerate(after) if i not in used and a["shape"] == b["shape"]]
        cand.sort(key=lambda ia: abs(ia[1]["row"] - b["row"]) + abs(ia[1]["col"] - b["col"]))
        if cand:
            i, a = cand[0]
            used.add(i)
            drow, dcol = a["row"] - b["row"], a["col"] - b["col"]
            if drow or dcol:
                effects.append({"kind": "move", "drow": drow, "dcol": dcol,
                                "shape": len(b["shape"])})
        else:
            # shape not found in after: recolour (same cells, diff colour), reshape, or vanish
            same_pos = [a for a in after if a["row"] == b["row"] and a["col"] == b["col"]]
            if same_pos:
                effects.append({"kind": "recolour_or_reshape", "at": (b["row"], b["col"])})
            else:
                effects.append({"kind": "vanish", "at": (b["row"], b["col"]),
                                "shape": len(b["shape"])})
    for i, a in enumerate(after):
        if i not in used and not any(a["shape"] == b["shape"] and a["row"] == b["row"]
                                     and a["col"] == b["col"] for b in before):
            effects.append({"kind": "appear", "at": (a["row"], a["col"]), "shape": len(a["shape"])})
    return effects


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
        out.append({"level": c["level"], "ends_level": c["ends_level"],
                    "n_actions": len(c["idx"]), "actions": acts,
                    "n_obj_before": len(before), "n_obj_after": len(after),
                    "effects": _match(before, after)})
    return {"game": path, "n_steps": len(steps), "n_chunks": len(chunks),
            "levels": max((s["level"] or 0) for s in steps), "chunks": out}


def _summary(res: dict) -> dict:
    """Per-level effect tally over actor objects -- the shape of the answer key."""
    per_level: dict = {}
    for c in res["chunks"]:
        lv = per_level.setdefault(c["level"], {"chunks": 0, "actions": 0, "effects": {}})
        lv["chunks"] += 1
        lv["actions"] += c["n_actions"]
        for e in c["effects"]:
            lv["effects"][e["kind"]] = lv["effects"].get(e["kind"], 0) + 1
    return per_level


if __name__ == "__main__":
    res = analyse(sys.argv[1] if len(sys.argv) > 1 else "replays/ls20_human.ndjson")
    print(f"steps={res['n_steps']} chunks={res['n_chunks']} levels={res['levels']}")
    print("=== per-level effect tally (actors only) ===")
    for lv, d in sorted(_summary(res).items(), key=lambda kv: (kv[0] is None, kv[0])):
        print(f"  L{lv}: {d['chunks']} chunks, {d['actions']} actions, effects={d['effects']}")
    print("=== first chunks ===")
    for c in res["chunks"][:5]:
        eff = {}
        for e in c["effects"]:
            eff[e["kind"]] = eff.get(e["kind"], 0) + 1
        print(f"  L{c['level']} acts={c['actions']} effects={eff}"
              f"{' [ENDS LEVEL]' if c['ends_level'] else ''}")
