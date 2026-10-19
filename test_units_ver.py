"""S6 (iv), THE UNITS VERSION, TETHER_UNITS_VER (the reviewer 2026-10-19 14:56 (iv), 15:05).

  E   the fake ARC game, 12 actions, C-seed-X, the arm ON vs OFF: the ledgers identical row for row
  W   every write that can move the settled set -- library[k] = t, standing.setdefault (a new key),
      standing[k] = a SETTLED Standing, settled_at None -> tick, tick -> None, standing.pop,
      library.update -- leaves units_held equal to a fresh build and to the scanned key's units
  K   a write that does not move the key (an unsettled standing added; a re-settle tick -> tick)
      keeps the held tuple (the same object), as R1's scan did
  R   a library rebound to a plain dict falls back to the scan: a settle there is still seen
  MF  the watch removed from Standing (its __setattr__ the plain one): a settle leaves the held
      units STALE -- so the watch is what makes the count exact
  P   Standing.settled reads settled_at ONLY (the reviewer 15:15's condition): every other field,
      mutated in place or reassigned, and a decay at a far tick leave `settled` and the held units
      as a fresh build reads them
  MF-P  `settled` widened to read settled_on too: P's sweep FAILS (an in-place settled_on.clear()
      flips it unwatched) -- so P is what would catch a new input the watch does not cover

    python test_units_ver.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

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
                       env=env, cwd=os.path.dirname(os.path.abspath(__file__)),
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    led = p.stdout.strip().splitlines()[-1]
    return [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()]


def keep(rows: list) -> list:
    return [r for r in rows if r.get("slot") != "@run" and r.get("event") not in ("header", "arms")]


def exact(g, what: str) -> tuple:
    """units_held equals a fresh build, and the scanned key's (R1's) units."""
    u = g.units_held()
    assert [x.name for x in u] == [x.name for x in g._units_built()], f"{what}: not a fresh build"
    assert g._units_memo[0] == g._units_key(), f"{what}: the held key is not the scanned key"
    return u


def pin(gamma, atoms) -> int:
    """P: every Standing field but settled_at, and the tick, mutated on a settled term; `settled`
    must not move and the held units must equal a fresh build. Returns the fields swept."""
    import dataclasses
    g = gamma.Gamma(atoms, game="units_ver_pin")
    t = gamma.Term((atoms[0], atoms[4]))
    g.library[t.name] = t
    st = g.standing.setdefault(t.name, gamma.Standing())
    st.settled_at = 0
    st.settled_on.add("o0.x")
    exact(g, "P start")
    n = 0
    for f in dataclasses.fields(gamma.Standing):
        if f.name == "settled_at":
            continue
        v = getattr(st, f.name)
        if isinstance(v, set):
            v.add("o1.y")
            v.clear()
        elif isinstance(v, dict):
            v["o1.y"] = 9.0
            v.clear()
        else:
            setattr(st, f.name, v + 5)
        n += 1
        assert st.settled, f"P: {f.name} flipped `settled` without a settled_at write"
        exact(g, f"P: {f.name}")
    st.decay(10 ** 6, None)
    assert st.settled, "P: a decay at a far tick flipped `settled`"
    exact(g, "P: decay")
    return n


def main() -> int:
    on, off = keep(child()), keep(child({"TETHER_UNITS_VER": "0"}))
    diff = next(((i, x, y) for i, (x, y) in enumerate(zip(on, off, strict=False)) if x != y), None)
    assert len(on) == len(off) and diff is None, (len(on), len(off), diff)                # E
    print("E", len(on), "rows identical, the count ON vs OFF")
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "conform"))
    import panel

    import gamma
    import world
    assert gamma._UNITS_VER and gamma._UNITS_MEMO, "run with the arm at its default (ON)"
    env = world.bind(panel._gridworld("gridworld_s2")[0])
    atoms = env.atoms()
    g = gamma.Gamma(atoms, game="units_ver")
    assert type(g.library) is gamma._Watched and type(g.standing) is gamma._Watched
    n0 = len(exact(g, "start"))
    t1, t2, t3 = (gamma.Term((atoms[0], atoms[i])) for i in (1, 2, 3))
    g.library[t1.name] = t1
    exact(g, "library[k] = t")
    g.standing.setdefault(t1.name, gamma.Standing()).settled_at = 0
    n1 = len(exact(g, "settled_at None -> tick"))
    assert n1 == n0 + 1, ("W: the settled term is not a unit", n0, n1)
    g.library.update({t2.name: t2})
    g.standing[t2.name] = gamma.Standing(settled_at=0)
    assert len(exact(g, "library.update + standing[k] = settled")) == n0 + 2
    g.standing[t1.name].settled_at = None
    assert len(exact(g, "settled_at tick -> None")) == n0 + 1
    g.standing.pop(t2.name)
    assert len(exact(g, "standing.pop")) == n0
    print("W every writer: units_held equal to a fresh build and the scanned key;", n0, "->",
          n0 + 1, "-> ... ->", n0, "units")                                                # W
    u = exact(g, "before K")
    g.standing.setdefault(t3.name, gamma.Standing())
    assert g.units_held() is u, "K: an unsettled standing moved the held tuple"
    g.standing[t1.name].settled_at = 0
    u = exact(g, "re-settle setup")
    g.standing[t1.name].settled_at = 7
    assert g.units_held() is u, "K: a re-settle moved the held tuple"
    print("K a write that leaves the key: the held tuple kept (the same object)")          # K
    h = gamma.Gamma(atoms, game="units_ver_r")
    h.library = dict(h.library)
    exact(h, "R start")
    h.library[t1.name] = t1
    dict.__setitem__(h.standing, t1.name, gamma.Standing())
    m_before = gamma._WRITES[0]
    object.__setattr__(h.standing[t1.name], "settled_at", 0)
    assert gamma._WRITES[0] == m_before
    assert any(x.atoms == t1.atoms for x in exact(h, "R: a plain library")), "R: the settle missed"
    print("R a plain (rebound) library: the scan, and the settle seen")                    # R
    f = gamma.Gamma(atoms, game="units_ver_mf")
    watch = gamma.Standing.__setattr__
    gamma.Standing.__setattr__ = object.__setattr__
    try:
        f.library[t1.name] = t1
        st = f.standing.setdefault(t1.name, gamma.Standing())
        v1 = f.units_held()
        st.settled_at = 0
        v2 = f.units_held()
        assert v2 is v1 and not any(x.atoms == t1.atoms for x in v2), "MF: not stale"
        assert f._units_key() != f._units_memo[0], "MF: the scan would have seen it"
    finally:
        gamma.Standing.__setattr__ = watch
    print("MF the watch removed from Standing: the held units stayed stale (", len(v2),
          "units, the settled one missing)")                                              # MF
    n = pin(gamma, atoms)
    print("P", n, "Standing fields and a far-tick decay: `settled` unmoved, units exact")   # P
    real = gamma.Standing.settled
    gamma.Standing.settled = property(lambda s: s.settled_at is not None and bool(s.settled_on))
    try:
        pin(gamma, atoms)
    except AssertionError as e:
        caught = str(e)
    else:
        caught = None
    finally:
        gamma.Standing.settled = real
    assert caught and "settled_on" in caught, ("MF-P: the widened `settled` was not caught", caught)
    print("MF-P `settled` widened to read settled_on: P failed:", caught)                 # MF-P
    print("units_ver: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
