"""8a-0, THE CUE KEY PATH (the reviewer r1796, r1804, r1805, r1806; DOC 1 / DOC 4 of r1505):
one real change, captured offline and replayed, followed through the agent's own lookup -- its
description, its facets, the postings it hits, the kind short list, the bound instance, the
outcome recorded back -- then the same change kind in another game and on another object.

  the change  (POSITION, +, 1) on a ".col" reading: lf52 o59.col at cycle 5
              (tests/data/cue_key_path/lf52_c5.json.gz, 7 frames) and dc22 o39.col at cycle 4,
              with o38.add_col at cycle 24 the second object of the same attribute types and dk
              (dc22_c24.json.gz, 31 frames). Captured from the offline game files with the start
              seed pinned; the replay returns the frames in order and every press is FORCED
              to the captured action (r1807), so the frames follow from the agent's acts
              however a later piece reorders its choices; its own choice is read beside it.
              A capture with no action for a press is a test ERROR (exit 2), not a status.
  MF1   a query keyed by instance (the slot name) hits no postings; the kind key (the reading) does
  MF2a  the same facet key hits the SAME facet postings in both games (r1806 a: the facet
        postings, never the whole lit, whose cue-side tiers differ between games by design)
  MF2b  the second object of the same kind (r1805: attribute types without the form) hits the
        same postings with zero walks, and its own bind still runs
  MF3   an entry that PRODUCES the observed effect and reads none of the changed readings is in
        the window
  MF4   such an entry ranks ahead of the forward list's tail (order by facets matched)
  MF5   nothing is cut: the target ask's lit is the same set with the facet arm on and off, and
        T0 served it (its own arguments, re-run after the replay; vacuous until the arm exists)
  MF6   the index writes no standing: every reflex's standing and the written rank standing are
        unchanged across each facet write and read (vacuous until the arm exists)
  MF7   the outcome is recorded back under the query's facets (an outcome facet in the offer /
        landing key)
  MF8   after a cached miss, an entry added with the key's facets is reached (executed from 8a-2,
        r1806 b)
  MF9   the same dk with a DIFFERENT set of attribute types never shares the key

EXPECTED_RED is today's red set; the test passes iff the measured red set equals it exactly, so a
red that turns green before its piece, or a green that turns red, fails it. 8a-1 removes
MF2a/MF3/MF4, 8a-2 MF2b/MF7/MF8. RETIRED (MF2b, MF8) are printed with their reading and never
asserted: each tests the 8a-2 lookup memory r1828 retired, a mechanism the agent no longer has
(r1844).

    python tests/test_cue_key_path.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT
DATA = os.path.join(HERE, "tests", "data", "cue_key_path")
EXPECTED_RED = {"MF2a", "MF3", "MF4", "MF7"}
RETIRED = {"MF2b", "MF8"}         # r1828 retired 8a-2's lookup memory; r1844

CHILD = r'''
import gzip, json, os, sys, tempfile
from collections import defaultdict
sys.dont_write_bytecode = True
import numpy as np
import arc_holdout, tether
from arcengine import FrameDataRaw, GameState
tether._AGENT_SEED = False
cap = json.loads(gzip.open(sys.argv[1]).read())
T_SLOT, T_CYC = sys.argv[2], int(sys.argv[3])
S_SLOT, S_CYC = (sys.argv[4], int(sys.argv[5])) if len(sys.argv) > 5 else (None, None)
DK = tuple(cap["want_dk"])

class Replay:
    def __init__(self, frames, game):
        self.frames, self.game, self.i = frames, game, 0
        self._last = self._make(frames[0])
    def _make(self, s):
        f = FrameDataRaw(game_id=self.game, state=GameState[s["state"]],
                         levels_completed=s["levels_completed"], win_levels=s["win_levels"],
                         guid="g", available_actions=list(s["available_actions"]))
        f.frame = [np.array(g, dtype=int) for g in s["frame"]]
        return f
    @property
    def observation_space(self):
        return self._last
    def reset(self):
        self.i = 0
        self._last = self._make(self.frames[0])
        return self._last
    def step(self, action, data=None, reasoning=None):
        self.i = min(self.i + 1, len(self.frames) - 1)
        self._last = self._make(self.frames[self.i])
        return self._last

SPY = {"reach": defaultdict(int), "offers": defaultdict(int), "tiers": {}, "window": {},
       "light": {}}
A = tether.Agent
_reach, _tiers, _dlit, _offs = A._index_reach, A._tiers, A._described_lit, A._offers_of
def reach(self, lib, lit, slot, *a, **k):
    SPY["reach"][(self.cycle, slot)] += 1
    return _reach(self, lib, lit, slot, *a, **k)
def tiers(self, lib, lit, dk, mine, *a, **k):
    out = _tiers(self, lib, lit, dk, mine, *a, **k)
    if dk is not None and tuple(dk) == DK:
        SPY["tiers"][self.cycle] = [k_ for k_, _w in out[0]]
        if self.cycle == T_CYC:
            SPY["t_args"] = (lib, list(lit), dk, mine, a, k)
    return out
def dlit(self, lib, lit, *a, **k):
    out = _dlit(self, lib, lit, *a, **k)
    SPY["window"][self.cycle] = [x[0] if isinstance(x, tuple) else x for x in (out or [])]
    return out
def offs(self, index, slot, frs):
    SPY["offers"][(self.cycle, slot)] += 1
    return _offs(self, index, slot, frs)
A._index_reach, A._tiers, A._described_lit, A._offers_of = reach, tiers, dlit, offs
# MF6: every reflex's standing and the rank keys' written standing, around each facet write / read
SPY["mf6"] = {"calls": 0, "changed": 0}
def standing(self):
    rf = sorted((f, repr(sorted(v.get("standing", {}).items(), key=str)))
                for f, v in self._reflexes.items())
    return repr(rf) + repr(sorted(self._rk_written.items(), key=str))
def watched(fn, ag_of):
    def run(*a, **k):
        ag_ = ag_of(a)
        before = standing(ag_)
        try:
            return fn(*a, **k)
        finally:
            SPY["mf6"]["calls"] += 1
            SPY["mf6"]["changed"] += standing(ag_) != before
    return run
if hasattr(A, "_fx_note"):
    A._fx_note = watched(A._fx_note, lambda a: a[0])
    tether.facet_index = watched(tether.facet_index, lambda a: a[0])
# r1807: the replay is valid only while the agent acts as the capture did, so every press is
# FORCED to the captured action (the agent's predictions and the press both read it); the
# agent's own choice is kept beside it as a reading
ACTS = cap.get("actions") or []
FORCED = []
_perceive = A.perceive
def perceive(self, action, coord=None, intent=None):
    k = len(FORCED)
    if k >= len(ACTS):
        sys.stderr.write(f"ERROR capture has no actions to cycle {self.cycle}\n")
        sys.exit(3)
    name, data = ACTS[k]
    xy = (data["x"], data["y"]) if data else None
    FORCED.append([self.cycle, [action, list(coord) if coord else None], [name, data and list(xy)]])
    return _perceive(self, name, xy, intent)
A.perceive = perceive
led = os.path.join(tempfile.mkdtemp(), "k.jsonl")
env, ag, *_ = arc_holdout.wire(Replay(cap["frames"], cap["game"]), cap["game"], led_path=led)
lib = tether._library()
Lib = type(lib)
_light = Lib.light
def light(self, changed, abduce=False, context=frozenset()):
    out = _light(self, changed, abduce, context)
    SPY["light"][(ag.cycle, str(abduce))] = (sorted(changed), [k for k, _w in out])
    return out
Lib.light = light
for _ in range(max(T_CYC, S_CYC or 0) + 1):
    env.observe()
    ag.step()
rows = [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()]
def row(ev, cyc, slot):
    return next((r for r in rows if r["event"] == ev and r["cycle"] == cyc and r["slot"] == slot),
                None)
fwd = SPY["light"].get((T_CYC, "False"), ([], []))
read = set(fwd[0])
prod_only = [k for k, _s in lib.produces(dict.fromkeys(fwd[0], 1))
             if not (set((lib.get(k) or {}).get("reads", [])) & read)] if fwd[0] else []
lit = SPY["tiers"].get(T_CYC, [])
fwd_in_lit = [k for k in fwd[1] if k in set(lit)]
key_fn = getattr(tether, "facet_key", None)
def key(owner):
    return key_fn(ag, DK, owner) if key_fn else (DK, ag._kind(owner))
owners = sorted({s.split(".")[0] for s in ag.slots})
t_owner = T_SLOT.split(".")[0]
t_kind = tether._unformed(ag._kind(t_owner))
other_types = next((o for o in owners if tether._unformed(ag._kind(o)) != t_kind), None)
has_index = hasattr(tether, "facet_index")
lb = row("library", T_CYC, T_SLOT)
out = {
    "game": cap["game"], "slot": T_SLOT, "cycle": T_CYC,
    "description": lb and lb["detail"].get("changed"),
    "facet_index": has_index,
    "facet_postings": sorted(tether.facet_index(ag, DK, t_owner)) if has_index else None,
    "listed": (row("lookup_tiers", T_CYC, T_SLOT) or {}).get("detail", {}).get("listed"),
    "lit_n": len(lit), "window": SPY["window"].get(T_CYC, []),
    "offered": lb and lb["detail"].get("offered"),
    "walks": SPY["reach"].get((T_CYC, T_SLOT), 0),
    "prod_only": prod_only, "prod_ranks": {k: lit.index(k) for k in prod_only if k in lit},
    "fwd_last_rank": max((lit.index(k) for k in fwd_in_lit), default=-1),
    "keys": [[list(k[0]), k[1], list(k[2])]
             for k in list(ag._kind_offered_dk) + list(ag._kind_landed_dk) if tuple(k[0]) == DK],
    "mf1": [len(_light(lib, {T_SLOT: 1})), len(_light(lib, {T_SLOT.split(".", 1)[1]: 1}))],
    "mf9": None if other_types is None else [str(key(t_owner)), str(key(other_types))],
    "arms": {"facet": bool(getattr(tether, "_FACET_INDEX", False)),
             "memory": bool(getattr(tether, "_FACET_MEMORY", False))},
    "forced": len(FORCED), "own_differs": [f for f in FORCED if f[1] != f[2]],
    "mf6": SPY["mf6"],
}
if SPY.get("t_args") and hasattr(tether, "_FACET_INDEX"):
    # MF5: the T_CYC ask's own arguments, run with the facet arm on and off after the replay (so
    # neither call's heads move a cycle); nothing cut = the same set of keys either way
    lib_, lit_, dk_, mine_, a_, k_ = SPY["t_args"]
    was, sets = tether._FACET_INDEX, {}
    with tether.cap.hold():
        for arm in (True, False):
            tether._FACET_INDEX = arm
            o_ = _tiers(ag, lib_, list(lit_), dk_, mine_, *a_, **k_)
            sets[arm] = ({k__ for k__, _w in o_[0]}, o_[1].get("T0", 0))
    tether._FACET_INDEX = was
    out["mf5"] = {"on": len(sets[True][0]), "off": len(sets[False][0]),
                  "same": sets[True][0] == sets[False][0], "t0": sets[True][1]}
if S_SLOT:
    o2 = S_SLOT.split(".")[0]
    out["second"] = {"slot": S_SLOT, "cycle": S_CYC,
                     "same_kind": tether._unformed(ag._kind(o2)) == t_kind,
                     "walks": SPY["reach"].get((S_CYC, S_SLOT), 0),
                     "binds": SPY["offers"].get((S_CYC, S_SLOT), 0)}
print("RESULT", json.dumps(out, default=str))
'''


def child(name: str, *args: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, os.path.join(DATA, name), *args],
                       capture_output=True, text=True, env=env, cwd=HERE,
                       stdin=subprocess.DEVNULL)
    if p.returncode == 3:
        # a capture that cannot drive the replay is a test ERROR, never a status
        print(f"{name}: {p.stderr.strip().splitlines()[-1]}")
        sys.exit(2)
    assert p.returncode == 0, p.stderr[-3000:]
    line = next(x for x in p.stdout.splitlines() if x.startswith("RESULT "))
    return json.loads(line[len("RESULT "):])


def statuses(a: dict, b: dict) -> dict:
    """Each must-fail -> (red?, the exact reason), from lf52 (a) and dc22 (b)."""
    st = {}
    for g in (a, b):
        i, k = g["mf1"]
        if not (i == 0 and k > 0):
            st["MF1"] = (True, f"{g['game']}: instance key {i} postings, kind key {k}")
    st.setdefault("MF1", (False, f"instance key 0 postings, kind key {a['mf1'][1]} / "
                                 f"{b['mf1'][1]}"))
    if not a["facet_index"]:
        st["MF2a"] = (True, "no facet index in tether (tether.facet_index absent)")
    else:
        pa, pb = a["facet_postings"], b["facet_postings"]
        st["MF2a"] = (not (pa == pb and pa),
                      f"facet postings lf52 {len(pa)} vs dc22 {len(pb)}, equal {pa == pb}")
    s = b["second"]
    ok = s["same_kind"] and s["walks"] == 0 and s["binds"] > 0
    st["MF2b"] = (not ok, f"{s['slot']} same kind {s['same_kind']}, walks {s['walks']} (want 0), "
                          f"binds {s['binds']}")
    held = {g["game"]: sum(1 for k in g["prod_only"] if k in g["window"]) for g in (a, b)}
    st["MF3"] = (min(held.values()) == 0, "produce-only in the window: " + ", ".join(
        f"{g['game']} {held[g['game']]} of {len(g['prod_only'])} (ranks "
        f"{sorted(g['prod_ranks'].values())[:3]} of {g['lit_n']}, window {len(g['window'])})"
        for g in (a, b)) + " -- rank of produce-only entries; AGENT|translate is an atom with "
        "no held view, so its rank is not this move's block (r1819)")
    ahead = {g["game"]: any(r < g["fwd_last_rank"] for r in g["prod_ranks"].values())
             for g in (a, b)}
    st["MF4"] = (not all(ahead.values()), "a produce-only entry ahead of the forward tail: " +
                 ", ".join(f"{g['game']} {ahead[g['game']]} (first "
                           f"{min(g['prod_ranks'].values(), default=None)}, forward tail "
                           f"{g['fwd_last_rank']})" for g in (a, b)))
    if not a["arms"]["facet"]:
        st["MF5"] = st["MF6"] = (False, "vacuous: no facet arm yet")
    else:
        m5 = [g.get("mf5") for g in (a, b)]
        st["MF5"] = ((True, "not measured") if None in m5 else (
            not all(m["same"] and m["t0"] for m in m5),
            "lit keys at the target ask, facet arm on / off: " + ", ".join(
                f"{g['game']} {g['mf5']['on']} / {g['mf5']['off']} same {g['mf5']['same']} "
                f"(T0 {g['mf5']['t0']})" for g in (a, b))))
        c6 = sum(g["mf6"]["calls"] for g in (a, b))
        ch6 = sum(g["mf6"]["changed"] for g in (a, b))
        st["MF6"] = (c6 == 0 or ch6 > 0, f"reflex standing / written rank standing changed across "
                                         f"{ch6} of {c6} facet writes and reads")
    rec = [k for g in (a, b) for k in g["keys"]]
    flat = all(len(k) == 3 for k in rec)
    st["MF7"] = (flat, f"{len(rec)} offer/landing keys, all (dk, entry, object kind): no outcome "
                       "facet" if flat else "an outcome facet in the key")
    st["MF8"] = ((True, "no invalidation of the lookup memory on a new entry (_dl_missed cleared "
                        "only at retarget)") if not a["arms"]["memory"]
                 else (True, "not yet executed"))
    m = a["mf9"] or b["mf9"]
    st["MF9"] = (m is None or m[0] == m[1], "no object with other attribute types in the replay"
                 if m is None else f"keys {m[0]} vs {m[1]}")
    return st


def main() -> int:
    a = child("lf52_c5.json.gz", "o59.col", "5")
    b = child("dc22_c24.json.gz", "o39.col", "4", "o38.add_col", "24")
    for g in (a, b):
        print(f"stages {g['game']}: description {g['description']}, listed {g['listed']}, lit "
              f"{g['lit_n']}, window {len(g['window'])}, offered {g['offered']}, walks "
              f"{g['walks']}")
        print(f"actions {g['game']}: {g['forced']} forced to the capture; the agent's own choice "
              f"differs at {g['own_differs']}")
    st = statuses(a, b)
    for mf in sorted(st, key=lambda x: (len(x), x)):
        red, why = st[mf]
        tag = "RETIRED" if mf in RETIRED else ""
        print(f"{mf:5} {'RED  ' if red else 'GREEN'} {why}" + (f"  [{tag}: r1828]" if tag else ""))
    red = {mf for mf, (r, _w) in st.items() if r and mf not in RETIRED}
    assert red == EXPECTED_RED, f"red set {sorted(red)} != expected {sorted(EXPECTED_RED)}"
    print(f"OK: the red set is the expected {sorted(EXPECTED_RED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
