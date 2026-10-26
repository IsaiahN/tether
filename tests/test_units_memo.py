"""R1, THE UNITS MEMO, TETHER_UNITS_MEMO (the reviewer 2026-10-17 17:43, 17:47).

  E   the fake ARC game, 12 actions, C-seed-X, the arm ON vs OFF: the ledgers identical row for row
  S   a term SETTLES mid-run: the memo misses, the new unit is present, and the held units equal a
      fresh uncached build
  MF  the settled set dropped from the key: the same settle leaves the held units STALE (the unit
      missing) -- so the key is what makes the memo exact
  (p) THE PRICING WINDOW'S CHECK BY VERSION (gamma.Gamma.code_ver; the reviewer 2026-10-25 22:46,
      23:46): P3 the fake game ON and OFF, every _inv_pairs ran to its check, 0 raised (the OFF
      child raised "the code moved" with nothing moved, since 5f4aa88); P1 a real settle inside
      the window raises, ON, TETHER_UNITS_MEMO=0 and TETHER_UNITS_VER=0 (the scanned key), and the
      clean twin prices; P2 each of code_ver()'s five parts moves it alone

    python tests/test_units_memo.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(_repo.ROOT, "conform"))
from identity_mod_rows import mask_timings  # noqa: E402  the one shared timing list

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
n = [0, 0]
_orig = tether.Agent._inv_pairs
def _count(self, *a):
    n[0] += 1
    yield from _orig(self, *a)
    n[1] += 1               # the generator ran to its end, so (p)'s check ran and passed
tether.Agent._inv_pairs = _count
led = os.path.join(tempfile.mkdtemp(), "u.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led)
print("INV", n[0], n[1])
print(led)
'''

# (p) THE PRICING WINDOW (the reviewer 2026-10-25 22:46, 23:46): _inv_pairs over one condition and
# one then-term, CLEAN, and PLANTED with a real settle inside the window (through the truth-key
# call, between the code's capture and its check). Its own process, because TETHER_UNITS_VER
# resolves at import (the containers' type and Standing's flip hook).
WINDOW = r'''
import sys, types
sys.dont_write_bytecode = True
sys.path.insert(0, "conform")
import gamma, ledger, panel, tether, world
env = world.bind(panel._gridworld("gridworld_s2")[0])
atoms = env.atoms()
def run(plant):
    g = gamma.Gamma(atoms, game="units_memo_window")
    ag = tether.Agent(env, g, tether.Config(), ledger.Ledger())
    t, n = gamma.Term((atoms[0], atoms[1])), 2
    if plant:
        key = ag._inv_truth_key
        def planted(truth):
            s = gamma.Term((atoms[0], atoms[2]))
            g.library[s.name] = s
            g.standing.setdefault(s.name, gamma.Standing()).settled_at = 0
            return key(truth)
        ag._inv_truth_key = planted
    try:
        out = list(ag._inv_pairs([("c", types.SimpleNamespace(term=t), [True] * n)],
                                 [(t, [0.0] * n)], [0.0] * n, g.units_held(), [None] * n))
        return f"priced {len(out)}"
    except RuntimeError as e:
        return f"raised: {e}"
print("CLEAN", run(False))
print("PLANT", run(True))
'''


def _env(extra: dict | None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(extra or {})})
    return env


def child(extra: dict | None = None) -> tuple[list, tuple]:
    p = subprocess.run([sys.executable, "-B", "-c", CHILD], capture_output=True, text=True,
                       env=_env(extra), cwd=_repo.ROOT,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    *_, inv, led = p.stdout.strip().splitlines()
    calls, ran = map(int, inv.split()[1:])
    return [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()], (calls, ran)


def window(extra: dict | None = None) -> dict:
    p = subprocess.run([sys.executable, "-B", "-c", WINDOW], capture_output=True, text=True,
                       env=_env(extra), cwd=_repo.ROOT,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    return dict(x.split(" ", 1) for x in p.stdout.strip().splitlines()
                if x[:5] in ("CLEAN", "PLANT"))


def keep(rows: list) -> list:
    return [r for r in rows if r.get("slot") != "@run" and r.get("event") not in ("header", "arms")]


def settle(g, a, b) -> object:
    import gamma
    t = gamma.Term((a, b))
    g.library[t.name] = t
    g.standing.setdefault(t.name, gamma.Standing()).settled_at = 0
    return t


def main() -> int:
    (on, inv_on), (off, inv_off) = child(), child({"TETHER_UNITS_MEMO": "0"})
    # wall timings masked by the shared list, imported (it postdates E: goal_hypotheses.wall_s,
    # 89c1ee9; read only once the OFF child ran to its end)
    on, off = mask_timings(keep(on)), mask_timings(keep(off))
    diff = next(((i, x, y) for i, (x, y) in enumerate(zip(on, off, strict=False)) if x != y), None)
    assert len(on) == len(off) and diff is None, (len(on), len(off), diff)                # E
    print("E", len(on), "rows identical, the memo ON vs OFF")
    # P3 (the reviewer 23:46): the window stays write-free over a real run -- every pricing ran to
    # its check and none raised, ON and OFF; the calls are the occasion
    assert inv_on[0] > 0 and inv_on == (inv_on[0], inv_on[0]), ("P3 ON", inv_on)
    assert inv_off == inv_on, ("P3 OFF", inv_off, inv_on)
    print(f"P3 the fake ARC game: _inv_pairs {inv_on[0]} calls, {inv_on[1]} checks run, 0 raised "
          f"(ON); OFF the same {inv_off}")
    # P1: a real settle inside the window raises in every arm state; the clean twin does not
    for arms in ({}, {"TETHER_UNITS_MEMO": "0"}, {"TETHER_UNITS_VER": "0"}):
        w = window(arms)
        assert w["CLEAN"].startswith("priced") and "the code moved" in w["PLANT"], (arms, w)
        print(f"P1 {arms or 'ON'}: clean {w['CLEAN']}; a settle in the window {w['PLANT'][:60]}")
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
    # P2: each part of code_ver() moves it alone
    import ledger
    import tether
    vg = gamma.Gamma(atoms, game="units_memo_ver")
    ag = tether.Agent(env, vg, tether.Config(), ledger.Ledger())
    moves = {}
    for part, write in (("_WRITES (a library write)",
                         lambda: vg.library.__setitem__("probe", gamma.Term((atoms[0], atoms[3])))),
                        ("the atoms", lambda: setattr(vg, "atoms", vg.atoms + [atoms[0]])),
                        ("Rank.ver (Rank.note)", lambda: ag.rank.note("probe", 0)),
                        ("the rank's install", lambda: setattr(vg, "unit_rank", None)),
                        ("_paid_ver (carry_used)", lambda: vg.carry_used({}))):
        v = vg.code_ver()
        write()
        moves[part] = vg.code_ver() != v
    assert all(moves.values()), ("P2", moves)
    print("P2 each part moves code_ver() alone:", ", ".join(moves))
    print("units_memo: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
