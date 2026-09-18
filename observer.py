"""The mutation-observer (Isaiah, 2026-09-15): each object carries the full attribute+relation set;
it is filled from frame 0 and updated in real time as frames arrive, and every frame COMPOUNDS the
cue + relational vector. A MUTATION — an attribute or relation that CHANGED between frames — is the
cue that directs the mapping: the delta names what to look up, so the search is directed instead of
undirected (`RELATIONS.md` Part 6, `TRAINING_PLAN.md` §13).

This is the perception grounding, in-bounds by construction: the per-object attributes are
the frozen 8, and the per-pair relations are `relations.py` (composable from the frozen set).
Nothing here bets or mints — it produces the cue/mutation stream the reverse-engineering maps in.
"""

from __future__ import annotations

import sys

import arc_percept
import detectors
import relations
import sensors_heavy
from reverse_engineer import _actors, _match

sys.dont_write_bytecode = True

_ATTRS = ("row", "col", "h", "w", "colour", "shape")


def _obj_vector(o: dict) -> dict:
    """The per-object attribute reading — the frozen 8 PLUS the heavy scalar/state sensors, so the
    vector emits the STATIC encodings that 1,355 of the 2,700 closure atoms read from one
    frame (was the frozen 6). 867 also need a per-object TEMPORAL encoding the observer does not
    yet emit; 478 touch BEHAVIOURAL/RULE (unbuilt). Encodings computed != condition evaluated."""
    vec = {a: o[a] for a in _ATTRS}
    vec.update(sensors_heavy.scalar(o))
    vec.update(sensors_heavy.state(o))
    return vec


def _frame_vector(objs: list[dict]) -> dict:
    """The full cue vector for one frame: every object's attributes and colour-source reading, and
    every ordered pair's composable relations. What each object 'carries', filled from the frame --
    the cue vector IS the agent's distinction horizon, so a reading it lacks is a distinction it
    cannot make (F169: the colour-source reading is why the recolour gap was mostly artifact)."""
    per_obj = {}
    lit: list[dict] = []
    for i, o in enumerate(objs):
        vec = _obj_vector(o)
        vec["colour_source"] = relations.colour_source(o, [x for j, x in enumerate(objs) if j != i])
        per_obj[i] = vec
        lit += detectors.light_static(o)
    per_pair = {}
    for i, a in enumerate(objs):
        for j, b in enumerate(objs):
            if i != j:
                per_pair[(i, j)] = {**relations.read_pair(a, b), **sensors_heavy.relation(a, b)}
                lit += detectors.light_relation(a, b)
    return {"objects": per_obj, "pairs": per_pair, "lit": lit}


# A `_match` "change" effect's delta keys -> the attribute that MUTATED. This is the cue: the
# mutation names which attribute changed, so the mapping looks up that attribute's atoms, not the
# whole space. The frozen 6 are `_match`'s deltas; the heavy ones come from sensors_heavy.temporal.
_MUT_ATTR = {"drow": "position", "dcol": "position", "dh": "extent", "dw": "extent",
             "dcells": "shape", "recolour": "colour"}
_HEAVY_MUT = {"dArea": "area", "dCells": "occupiedCells", "dDensity": "density", "dHoles": "holes",
              "dPerimeter": "perimeter", "dGirth": "girth", "dSolid": "solidity",
              "dOrientation": "orientation", "velocity": "velocity"}


def _mutations(effects: list[dict], before: list[dict], after: list[dict]) -> dict:
    """The mutations one frame->next fired, read off `_match`'s size-tracked effects: which
    attributes changed on the objects that persisted, and how many appeared / vanished. Both the
    frozen deltas AND the heavy ones (density, holes, solidity, velocity...) fire a directed cue."""
    changed: dict = {}
    appeared = vanished = 0
    for e in effects:
        if e["kind"] == "change":
            for dk, attr in _MUT_ATTR.items():
                if e.get(dk):  # non-zero delta, or True for recolour
                    changed[attr] = changed.get(attr, 0) + 1
            heavy = sensors_heavy.temporal(before[e["bi"]], after[e["ai"]])
            for dk, attr in _HEAVY_MUT.items():
                if heavy.get(dk):
                    changed[attr] = changed.get(attr, 0) + 1
        elif e["kind"] == "appear":
            appeared += 1
        elif e["kind"] == "vanish":
            vanished += 1
    return {"attributes": changed, "appeared": appeared, "vanished": vanished}


def observe(steps: list[dict]) -> list[dict]:
    """Run the observer across a replay's frames. Objects are tracked frame-to-frame by the
    size-conserved matching the answer key uses (`_match`), so a mutation is a change in the SAME
    object. Returns, per frame, the full cue vector (attributes + composable relations) and the
    mutations that fired — the directed cues the mapping follows."""
    frames = [arc_percept.components(s["grid"]) for s in steps]
    out = []
    prev_objs = None
    for t, objs in enumerate(frames):
        vec = _frame_vector(objs)
        muts = {"attributes": {}, "appeared": 0, "vanished": 0}
        if prev_objs is not None:
            # `_match` pairs on actor-filtered lists, so its bi/ai index those -- filter to match.
            muts = _mutations(_match(prev_objs, objs), _actors(prev_objs), _actors(objs))
        out.append({"frame": t, "n_objects": len(objs), "cue": vec, "mutations": muts})
        prev_objs = objs
    return out


def summarise(obs: list[dict]) -> dict:
    """A compact read of what the observer saw — how many frames, how much the cue vector compounds,
    and which attributes/relations mutate at all (the cues that ever fire on this game)."""
    fired: dict = {}
    lit: dict = {}
    for f in obs:
        for k, n in f["mutations"]["attributes"].items():
            fired[k] = fired.get(k, 0) + n
        for d in f["cue"].get("lit", []):
            lit[d["atom"]] = lit.get(d["atom"], 0) + 1
    return {"frames": len(obs),
            "max_objects": max((f["n_objects"] for f in obs), default=0),
            "attributes_that_mutate": fired,
            "primitive_atoms_lit": lit,
            "total_appeared": sum(f["mutations"]["appeared"] for f in obs),
            "total_vanished": sum(f["mutations"]["vanished"] for f in obs)}


if __name__ == "__main__":
    import json
    import sys as _s

    from reverse_engineer import load_replay
    path = _s.argv[1] if len(_s.argv) > 1 else "replays/ls20_human.ndjson"
    obs = observe(load_replay(path))
    print(json.dumps(summarise(obs), indent=1))
