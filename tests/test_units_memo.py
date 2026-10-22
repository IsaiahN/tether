"""R1, THE UNITS MEMO, TETHER_UNITS_MEMO (the reviewer 2026-10-17 17:43, 17:47).

  E   the fake ARC game, 12 actions, C-seed-X, the arm ON vs OFF: the ledgers identical row for row
  S   a term SETTLES mid-run: the memo misses, the new unit is present, and the held units equal a
      fresh uncached build
  MF  the settled set dropped from the key: the same settle leaves the held units STALE (the unit
      missing) -- so the key is what makes the memo exact

    python tests/test_units_memo.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
led = os.path.join(tempfile.mkdtemp(), "u.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led)
print(led)
'''


def child(extra: dict | None = None) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(extra or {})})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD], capture_output=True, text=True,
                       env=env, cwd=_repo.ROOT,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    led = p.stdout.strip().splitlines()[-1]
    return [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()]


def keep(rows: list) -> list:
    return [r for r in rows if r.get("slot") != "@run" and r.get("event") not in ("header", "arms")]


def settle(g, a, b) -> object:
    import gamma
    t = gamma.Term((a, b))
    g.library[t.name] = t
    g.standing.setdefault(t.name, gamma.Standing()).settled_at = 0
    return t


def main() -> int:
    on, off = keep(child()), keep(child({"TETHER_UNITS_MEMO": "0"}))
    diff = next(((i, x, y) for i, (x, y) in enumerate(zip(on, off, strict=False)) if x != y), None)
    assert len(on) == len(off) and diff is None, (len(on), len(off), diff)                # E
    print("E", len(on), "rows identical, the memo ON vs OFF")
    sys.path.insert(0, os.path.join(_repo.ROOT, "conform"))
    import panel

    import gamma
    import world
    env = world.bind(panel._gridworld("gridworld_s2")[0])
    atoms = env.atoms()
    g = gamma.Gamma(atoms, game="units_memo")
    u1 = g.units_held()
    t = settle(g, atoms[0], atoms[1])
    u2 = g.units_held()
    assert u2 is not u1 and any(u.atoms == t.atoms for u in u2), "S: the memo did not miss"
    assert [u.name for u in u2] == [u.name for u in g._units_built()], "S: not a fresh build"
    print("S a term settled: the memo missed;", len(u1), "->", len(u2), "units, equal to a fresh "
          "build")                                                                          # S
    h = gamma.Gamma(atoms, game="units_memo_mf")
    key = gamma.Gamma._units_key
    gamma.Gamma._units_key = lambda self: (len(self.atoms),)
    try:
        v1 = h.units_held()
        s2 = settle(h, atoms[0], atoms[2])
        v2 = h.units_held()
        assert v2 is v1 and not any(u.atoms == s2.atoms for u in v2), "MF: not stale"
    finally:
        gamma.Gamma._units_key = key
    print("MF the settled set dropped from the key: the units stayed stale (", len(v2),
          "units, the settled one missing)")                                               # MF
    print("units_memo: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
