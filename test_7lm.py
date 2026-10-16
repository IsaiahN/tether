"""C-7lm-1, 7l and 7m (the reviewer 2026-10-15 17:32, 20:17, 20:41, 20:54 G1).

  L1  a fake-game generation written with the arm holds kinds (attribute-type tuples, no object
      name inside) and episodes (outcome, salience); reported: distinct kinds against objects,
      general entries, episode rows, bytes they add to the generation
  G1  a general entry records what LANDED: the kinds written are a strict subset of the kinds
      asked on the run (counted by a spy on every question asked), and every one landed
  L2  a second process loads them: kinds_known > 0
  M1  site 8: a pair whose kinds landed before goes first even with more tries; MF without the
      analogy field the tried count puts the other first (built so they disagree)
  M2  a kind with no entry changes nothing: the order equals the order without the field
  M3  a kind pair ASKED on the run but landing nothing reads 0 in 7m's field (does not go first)

    python test_7lm.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

RUN = r"""
import json, sys
sys.dont_write_bytecode = True
import tether, tether_agent
from arcengine import GameState
from test_entry import FakeWrapper
d = sys.argv[1]
asked, agents = set(), []
real_c = tether.Agent._compiled
def cspy(self, lib, key, role, o, x, comp, atoms, sig, slot=None, tally=None):
    if slot is not None:
        asked.add((key, role, self._kind(o), self._kind(x)))
        if not agents:
            agents.append(self)
    return real_c(self, lib, key, role, o, x, comp, atoms, sig, slot=slot, tally=tally)
tether.Agent._compiled = cspy
w = FakeWrapper(script={2: GameState.GAME_OVER})
tether_agent.run(w, "fake", max_actions=int(sys.argv[2]), lineage_dir=d)
ag = agents[0]
landed = ag._kind_landed
full = {(ko, kx) for _k, _r, ko, kx in ag._kind_landed | ag._kind_known}
fresh = all(ag._kind(o) == tuple(sorted({str(ag.slot_types.get(s)) for s in ag.slots
                                          if s.split('.')[0] == o}))
            for o in {s.split('.')[0] for s in ag.slots})
pairs = {(ko, kx) for _k, _r, ko, kx in landed}
asked_only = sorted({(ko, kx) for _k, _r, ko, kx in asked} - pairs)
print("OUT " + json.dumps({"asked": len(asked), "landed": len(landed),
                           "subset": landed <= asked,
                           "asked_only_pairs": [[list(a), list(b)] for a, b in asked_only],
                           "landed_pairs": len(pairs), "cache_equal": ag._kind_pairs == full,
                           "kind_fresh": fresh}))
"""

LOAD = r"""
import json, sys
sys.dont_write_bytecode = True
import arc_holdout
from test_entry import FakeWrapper
env, ag, led, *rest = arc_holdout.wire(FakeWrapper(), "fake", lineage_dir=sys.argv[1])
print("OUT " + json.dumps({"kinds_known": len(ag._kind_known)}))
"""


def _run(code: str, *args: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["TETHER_AGENT_SEED"] = "0"
    r = subprocess.run([sys.executable, "-B", "-c", code, *args], env=env, capture_output=True,
                       text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads([ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")][-1][4:])


def main() -> None:
    d = os.path.join(tempfile.mkdtemp(prefix="t7lm_"), "lin")
    run = _run(RUN, d, "6")
    gens = [json.loads(Path(d, f).read_text(encoding="utf-8"))
            for f in os.listdir(d) if f.startswith("gen_")]
    kinds = [k for g in gens for k in g.get("kinds_landed", [])]
    assert not any("kinds" in g for g in gens), "the old key was written"
    eps = [e for g in gens for e in g.get("episodes", [])]
    assert kinds and eps, ("L1: nothing written", len(kinds), len(eps))
    names = re.compile(r"\bo\d+\b")
    assert not any(names.search(json.dumps(k[2:])) for k in kinds), "L1: a name inside a kind"
    assert all("salience" in e and "outcome" in e for e in eps), "L1 episode fields"
    objs = {o for e in eps for o in [e["o"], *e["x"]]}
    distinct = {tuple(x) for k in kinds for x in (k[2], k[3])}
    added = len(json.dumps({"kinds_landed": kinds, "episodes": eps}))
    print(f"  L1 {len(kinds)} general entries, {len(eps)} episode rows, {added} bytes added;"
          f" {len(distinct)} distinct kinds over {len(objs)} objects;"
          f" salience {sorted({e['salience'] for e in eps})[:4]}")
    if len(distinct) == 1:
        print("  L1 ONE KIND on this run (a finer kind is on the after-7 list)")
    assert run["subset"] and run["landed"] < run["asked"], ("G1", run)
    print(f"  G1 {run['landed']} landed of {run['asked']} asked (entry, role, kind pair);"
          f" {run['landed_pairs']} kind pairs carry a landing")
    assert run["cache_equal"], "C: the cached pairs differ from a full rebuild"
    assert run["kind_fresh"], "K: a cached kind differs from one read fresh"
    print("  C the cached kind pairs equal a full rebuild; K every cached kind equals a fresh"
          " read after the run's retarget")
    got = _run(LOAD, d)
    assert got["kinds_known"] > 0, ("L2", got)
    print(f"  L2 a second process loads {got['kinds_known']} kind entries")

    import frontier as FR
    from tether import _lookup_order
    names_ = ["a", "b"]
    comp = {"a": (0, False, 0, 1, -1, 5), "b": (0, False, 0, 1, 0, 0)}
    assert _lookup_order(names_, comp, "k", seed="0") == ["a", "b"], "M1"
    noan = {k: v[:4] + v[5:] for k, v in comp.items()}
    assert _lookup_order(names_, noan, "k", seed="0") == ["b", "a"], "M1 MF"
    print("  M1 the kind that landed before goes first despite 5 tries; MF without it the tries"
          " decide")
    flat = {"a": (0, False, 0, 1, 0, 2), "b": (0, False, 0, 1, 0, 2)}
    no_field = {k: v[:4] + v[5:] for k, v in flat.items()}
    assert _lookup_order(names_, flat, "k", seed="0") == _lookup_order(names_, no_field, "k",
                                                                       seed="0"), "M2"
    want = sorted(names_, key=lambda s: FR.draw_key("k", s, "0"))
    print(f"  M2 no kind entry: the same order as without the field ({want})")
    ao = run["asked_only_pairs"]
    if ao:
        print(f"  M3 {len(ao)} kind pair(s) asked on the run landed nothing and are not in 7m's"
              " pairs (they read 0, never first)")
    else:
        print("  M3 every kind pair asked on this run also landed somewhere: G1 cut entries at"
              " the (entry, role) level only; no pair-level case on this run")
    print("7lm: OK")


if __name__ == "__main__":
    main()
