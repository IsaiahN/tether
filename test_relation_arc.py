"""ARC B2, TETHER_RELATION_SET (the reviewer 2026-10-11 10:11, 10:20, 11:48 CDT): on ARC the five
pair relations are published over the CONTACT pairs plus every pair whose subject is in the
agent's actor set (`relate`), computed from the frame's read and derivable from any state.

A synthetic frame of four objects: A alone, B and C touching (the one contact pair), D far away.
  a1 OFF: no pair slot, `derived()` empty;
  a2 ON, relate(empty): exactly the contact pairs, both ways, each value the hand computation, every
     slot typed, sized, owned and declared relational; MUST-FAIL: no non-contact, non-actor pair;
  a3 relate({A}): A's pairs with every other object are added, nothing else;
  a4 derive() over a predicted state moves with the predicted row;
  a5 relate() stays AGENT-SIDE: no call reaches the wrapper (the game channel) and the frame is the
     same object, under different subject sets.
  a6 THE SPARSE DECLARATION TIED TO THE WORLD (the reviewer 2026-10-11 14:50 CDT; Fig 10): with the
     observer on, over a frame holding a ring with a peg in its hole and two interleaved boxes,
     every emitted a~b.inside is 1 and every emitted a~b.bbox is > 0 (relations.SPARSE_PAIR's
     premise: emitted only where it holds), and at least one of each is emitted.

    python test_relation_arc.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
import numpy as np
from arcengine import FrameDataRaw, GameState
import arc_atoms, arc_percept, arc_predict, relations
from arc_world import ArcWorld

class _Four:
    def __init__(self):
        self.calls = 0
    def _frame(self):
        f = FrameDataRaw(game_id="relarc", state=GameState.NOT_FINISHED, levels_completed=0,
                         win_levels=3, available_actions=[1, 2])
        b = np.zeros((14, 14), dtype=int)
        b[2][0] = 3                                  # A
        b[6][4] = 5; b[7][4] = 5                     # B
        b[8][4] = 6                                  # C, touching B
        b[11][11] = 2                                # D
        f.frame = [b]
        return f
    def reset(self):
        self.calls += 1
        return self._frame()
    def step(self, *a, **k):
        self.calls += 1
        return self._frame()

w = _Four()
env = ArcWorld(w, arc_percept.Objects(), arc_atoms.three_spaces(arc_predict.predict()),
               palette=7, platform=())
env.observe()                                    # the first read decomposes the frame
tr = env._decompose.tracked
at = {(o["row"], o["col"]): n for n, o in tr.items()}
A, B, C, D = at[(2, 0)], at[(6, 4)], at[(8, 4)], at[(11, 11)]
out = {"names": [A, B, C, D], "others": sorted(tr),
       "contact": sorted([a, b] for a, bs in env.contacts().items() for b in bs)}
def pairs_of(keys):
    return sorted({(k.split(".", 1)[0], k.rsplit("_", 1)[1]) for k in keys
                   if relations.pair_attr(k.rsplit(".", 1)[1])})
obs = env.observe()
out["off_or_on_pairs"] = pairs_of(obs)
out["derived_n"] = len([k for k in env.derived()                 # the PAIR slots derived
                         if relations.pair_attr(k.rsplit(".", 1)[1])])
ok_vals = all(obs[f"{a}.{rel}_{b}"] == v for a, b in pairs_of(obs)
              for rel, v in relations.pair_values(tr[a], tr[b]).items())
types, alpha, own, rels = env.slot_types(), env.alphabet(), env.slot_owner(), env.relational_slots()
declared = all(types[k] == relations.PAIR_RELATIONS[relations.pair_attr(k.rsplit(".", 1)[1])]
               and alpha[k] >= 2 and own[k] == k.split(".", 1)[0] and k.rsplit(".", 1)[1] in rels
               for k in obs if relations.pair_attr(k.rsplit(".", 1)[1]))
out["values_ok"], out["declared"] = ok_vals, declared
frame, calls = env._frame, w.calls
env.relate({A})
out["actor_pairs"] = pairs_of(env.observe())
pred = dict(env.observe()); pred[f"{A}.row"] = pred[f"{A}.row"] + 3
d0, d1 = env.derive(env.observe()), env.derive(pred)
out["drow_moves"] = [d0.get(f"{A}.drow_{D}"), d1.get(f"{A}.drow_{D}")]
env.relate(set()); env.relate({B, D}); env.relate({A})
out["agent_side"] = [w.calls - calls, env._frame is frame]
print(json.dumps(out))
'''


SPARSE = r'''
import json, sys
sys.dont_write_bytecode = True
import numpy as np
from arcengine import FrameDataRaw, GameState
import arc_atoms, arc_percept, arc_predict
from arc_world import ArcWorld

class _Ring:
    def _frame(self):
        f = FrameDataRaw(game_id="sparse", state=GameState.NOT_FINISHED, levels_completed=0,
                         win_levels=3, available_actions=[1, 2])
        b = np.zeros((14, 14), dtype=int)
        for r in range(1, 6):
            for c in range(1, 6):
                if r in (1, 5) or c in (1, 5):
                    b[r][c] = 3                      # the ring, hole rows/cols 2-4
        b[3][3] = 5                                  # the peg in the hole
        for c in range(8, 12):
            b[9][c] = 2                              # a bar ...
        for r in range(7, 12):
            b[r][10] = 4                             # ... crossed by another: interleaved boxes
        b[9][10] = 2
        f.frame = [b]
        return f
    def reset(self):
        return self._frame()
    def step(self, *a, **k):
        return self._frame()

env = ArcWorld(_Ring(), arc_percept.Objects(), arc_atoms.three_spaces(arc_predict.predict()),
               palette=7, platform=())
obs = env.observe()
ins = {k: v for k, v in obs.items() if k.endswith(".inside") and "~" in k}
box = {k: v for k, v in obs.items() if k.endswith(".bbox") and "~" in k}
print(json.dumps({"inside": ins, "bbox": box}))
'''


def _sparse() -> dict:
    env = dict(os.environ, TETHER_OBSERVER="1", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", SPARSE], capture_output=True, text=True, env=env,
                       cwd=os.path.dirname(os.path.abspath(__file__)), timeout=600)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_RELATION_SET="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=os.path.dirname(os.path.abspath(__file__)), timeout=600)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    off = _run(False)
    assert off["off_or_on_pairs"] == [] and off["derived_n"] == 0, off
    assert off["actor_pairs"] == [], off
    print("  a1 OFF: no pair slot, derived() empty, relate() publishes nothing")
    on = _run(True)
    A, B, C, D = on["names"]
    contact = on["contact"]
    assert [B, C] in contact and [A, D] not in contact and [A, B] not in contact, contact
    assert on["off_or_on_pairs"] == contact, on                     # a2
    assert [A, D] not in on["off_or_on_pairs"] and [A, B] not in on["off_or_on_pairs"], on  # MF
    assert on["values_ok"] and on["declared"], on
    assert on["derived_n"] == 5 * len(contact), on
    print(f"  a2 relate(empty): only the {len(contact)} contact pairs (none A-B, A-D), "
          "values and declarations ok")
    add = [[A, x] for x in on["others"] if x != A]
    want = sorted({tuple(p) for p in contact + add})
    assert on["actor_pairs"] == [list(p) for p in want], on
    print(f"  a3 relate({{A}}): adds A's pairs with all {len(add)} other objects, nothing else")
    assert on["drow_moves"][0] is not None and on["drow_moves"][1] == on["drow_moves"][0] - 3, on
    print(f"  a4 derive: A.drow_D {on['drow_moves'][0]} -> {on['drow_moves'][1]} with A.row + 3")
    assert on["agent_side"] == [0, True], on
    print("  a5 relate() reaches no wrapper call and leaves the frame as it was")
    sp = _sparse()
    assert sp["inside"] and sp["bbox"], sp                          # non-vacuous
    assert all(v == 1 for v in sp["inside"].values()), sp
    assert all(v > 0 for v in sp["bbox"].values()), sp
    print(f"  a6 observer emits only where it holds: {len(sp['inside'])} inside all 1, "
          f"{len(sp['bbox'])} bbox all > 0 (relations.SPARSE_PAIR's premise)")
    print("relation arc: OK")
