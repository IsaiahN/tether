"""SHAPE NAMES (TETHER_SHAPE_NAMES, default ON; Isaiah 2026-11-16 "it's a ball (shaped like a ball,
acts like a ball)"). Each object's `shape_name` is the first declared geometric predicate its own
cells satisfy (arc_percept._SHAPE_TESTS), published by Objects like any reading.
  S1  each name on a canonical example and a turned / mirrored one, through Objects on a grid
  S2  colour and position do not change the name
  S3  a STATE reading: unchanged across a frame where the cells are unchanged; alphabet declared
  S4  SHAPE_ATOMS names only library/given.json entries; disc -> the circle / sphere atoms
  MF-S1 TETHER_SHAPE_NAMES=0 -> no shape_name reading -> RED as required
  S5  gridworld 12 steps ON and OFF both pass the gate (gridworld does not read arc_percept, so
      this is a no-harm check only)
Seconds.
    python tests/test_shape_names.py
"""
from __future__ import annotations

import json
import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_atoms  # noqa: E402
import arc_percept  # noqa: E402
import arc_world  # noqa: E402

# each name: (canonical cells, a turned / mirrored version)
SHAPES = {
    "dot": ([(0, 0)], [(0, 0)]),
    "line": ([(0, c) for c in range(4)], [(r, 0) for r in range(4)]),
    "square": ([(r, c) for r in range(3) for c in range(3)],
               [(r, c) for r in range(2) for c in range(2)]),
    "rectangle": ([(r, c) for r in range(2) for c in range(4)],
                  [(r, c) for r in range(4) for c in range(2)]),
    "ring": ([(r, c) for r in range(3) for c in range(4) if r in (0, 2) or c in (0, 3)],
             [(r, c) for r in range(4) for c in range(3) if r in (0, 3) or c in (0, 2)]),
    "plus": ([(1, 0), (1, 1), (1, 2), (0, 1), (2, 1)],
             [(2, c) for c in range(5)] + [(r, 2) for r in range(5)]),
    "L": ([(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 0), (0, 1), (0, 2), (1, 2)]),
    "T": ([(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)], [(0, 1), (1, 1), (2, 1), (2, 0), (2, 2)]),
    "diamond": ([(r, c) for r in range(5) for c in range(5) if abs(r - 2) + abs(c - 2) <= 2],
                [(r, c) for r in range(7) for c in range(7) if abs(r - 3) + abs(c - 3) <= 3]),
    "disc": ([(r, c) for r in range(4) for c in range(4) if (r, c) not in
              {(0, 0), (0, 3), (3, 0), (3, 3)}],
             [(r, c) for r in range(5) for c in range(5) if (r - 2) ** 2 + (c - 2) ** 2 <= 5]),
    "irregular": ([(0, 0), (0, 1), (1, 1), (1, 2)], [(0, 1), (1, 0), (1, 1), (2, 0)]),
}


def board(cells, colour=3, at=(2, 2), size=12):
    b = [[0] * size for _ in range(size)]
    for r, c in cells:
        b[at[0] + r][at[1] + c] = colour
    return b


def named(obs, b, colour):
    st = obs(b)
    names = [k.rsplit(".", 1)[0] for k, v in st.items() if k.endswith(".colour") and v == colour]
    assert len(names) == 1, (names, colour)
    return st, names[0]


def read(cells, colour=3, at=(2, 2)):
    st, n = named(arc_percept.Objects(), board(cells, colour, at), colour)
    return arc_percept.SHAPE_NAMES[st[f"{n}.shape_name"]]


def main() -> int:
    assert arc_percept._SHAPE_NAMES is True, "the arm defaults ON"
    for want, (canon, turned) in SHAPES.items():
        got = (read(canon), read(turned))
        assert got == (want, want), ("S1", want, got)
        print(f"S1 {want:9s}: canonical and turned/mirrored both '{want}': GREEN")
    for want, (canon, _t) in SHAPES.items():
        for colour, at in ((5, (0, 0)), (9, (6, 5))):
            assert read(canon, colour, at) == want, ("S2", want, colour, at)
    print("S2 colour and position do not change the name: GREEN")

    obs = arc_percept.Objects()
    disc = SHAPES["disc"][1]
    st1, n1 = named(obs, board(disc, 4), 4)
    st2, n2 = named(obs, board(disc, 4), 4)
    assert n1 == n2 and st1[f"{n1}.shape_name"] == st2[f"{n2}.shape_name"], "S3: not a state"
    assert arc_world._OBJ_DERIVED["shape_name"] == ("shape",)
    assert arc_world.ALPHABET["shape_name"](12, 12, {}) == len(arc_percept.SHAPE_NAMES)
    assert arc_atoms.ATTRIBUTE_TYPE["shape_name"] == arc_atoms.NAME
    assert arc_atoms.NAME in arc_atoms.COMPARABLE and arc_atoms.NAME not in arc_atoms.ORDERED
    import arc_predict
    built = {a.name: a for a in arc_atoms.three_spaces(arc_predict.predict())}
    assert "shape_name" in built, "S3: the reading's atom was not built"
    print(f"S3 a state reading ({arc_percept.SHAPE_NAMES[st1[n1 + '.shape_name']]}); alphabet "
          f"{len(arc_percept.SHAPE_NAMES)} declared; type NAME (equality, no order): GREEN")

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "library", "given.json"), encoding="utf-8") as f:
        entries = json.load(f)["entries"]
    for name, atoms in arc_percept.SHAPE_ATOMS.items():
        assert name in arc_percept.SHAPE_NAMES, ("S4 unknown name", name)
        for a in atoms:
            assert a in entries, ("S4 not a library entry", name, a)
    assert set(arc_percept.SHAPE_ATOMS["disc"]) == {"TOPOLOGICAL|Circle", "TOPOLOGICAL|Sphere"}
    print(f"S4 SHAPE_ATOMS names only library entries {dict(arc_percept.SHAPE_ATOMS)}: GREEN")

    arc_percept._SHAPE_NAMES = False
    st_off, _n = named(arc_percept.Objects(), board(disc, 4), 4)
    arc_percept._SHAPE_NAMES = True
    assert not any(k.endswith(".shape_name") for k in st_off)
    print("MF-S1 the arm OFF: no shape_name reading -> RED (as required)")

    import gamma
    import gate
    import gridworld
    import ledger
    import tether
    import world
    for on in (True, False):
        arc_percept._SHAPE_NAMES = on
        env = world.bind(gridworld.family("default", 0))
        led = ledger.Ledger()
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
        for _ in range(12):
            ag.step()
        ag.end_run("cap")
        v = gate.check(led.rows())["verdict"]
        assert v == "pass", ("S5: the gate refused", on, v)
    arc_percept._SHAPE_NAMES = True
    print("S5 gridworld 12 steps ON and OFF: both pass the gate: GREEN")
    print("shape_names: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
