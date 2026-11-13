"""P2 (the reviewer r1838; DESIGN_STEP8 D1): TETHER_SWEEP_DELTA's walk. gamma.enumerate_closure with
must_contain yields exactly the chains of the full closure built with one of the named units, and
nothing else; the sweep's _reach passes the units settled since the park.

  SD1   for each of three atom units u of the gridworld world: the set yielded with
        must_contain={u} == the full closure's chains that contain u (depth 3, no budget cut).
  MF    the keyword ignored (every chain yielded): SD1's equality fails -> RED.
  gw12's OFF identity against the parent is the commit's check, not this file's.

    python tests/test_sweep_delta.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ["TETHER_AGENT_SEED"] = "0"

import gamma  # noqa: E402
import gridworld  # noqa: E402
import world  # noqa: E402

DEPTH = 3
BUDGET = 10 ** 9


def names(g: gamma.Gamma, must: frozenset | None) -> set:
    return {t.name for t in g.enumerate_closure("val", "val", DEPTH, BUDGET, must_contain=must)}


def check(g: gamma.Gamma, plant: bool) -> list:
    full = {t.name: t for t in g.enumerate_closure("val", "val", DEPTH, BUDGET)}
    units = [u for u in g.units() if len(u.atoms) == 1 and u.atoms[0].name != gamma.IDN_NAME]
    bad = []
    for u in units[:3]:
        want = {n for n, t in full.items() if any(a.name == u.atoms[0].name for a in t.atoms)}
        got = names(g, None if plant else frozenset({u.name}))
        print(f"   unit {u.name}: full {len(full)}, containing it {len(want)}, yielded {len(got)}")
        if got != want:
            bad.append((u.name, len(got - want), len(want - got)))
    return bad


def main() -> int:
    env = world.bind(gridworld.family("default", 0))
    g = gamma.Gamma(env.atoms(), game="fam_default_0")
    bad = check(g, plant=False)
    print("SD1 must_contain yields exactly the chains built with the unit: "
          + ("GREEN" if not bad else f"RED {bad}"))
    assert not bad, bad
    planted = check(g, plant=True)
    print("MF the keyword ignored: " + (f"RED {planted}" if planted
                                         else "GREEN (the plant went unseen)"))
    assert planted, "ignoring must_contain left SD1 green"
    print("sweep_delta: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
