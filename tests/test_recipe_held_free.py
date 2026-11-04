"""TETHER_RECIPE_HELD_FREE (the reviewer 2026-11-04 r985; Fig 12 :107-108 "where the arrangement
is recorded, re-deriving it is a lookup and the actions were spent once"). Under RECIPE_DEDUP a
chain the agent holds as a recipe is tested once, before its instances are generated, and takes no
try. The demo world (world.Transitions), 16 cycles, seed pinned. About a minute.

MF-H1  a small work budget (60): OFF the budget is spent on held instances (recipe-held tries > 0)
       and nothing is minted; ON no try goes there, more is priced, and a term is minted; RED on
       HEAD (no arm: ON is OFF)
MF-H2  MUST-STAY, an ample budget (15000): the minted terms are identical ON and OFF, and there
       are some -- no previously minted term becomes unmintable
OFF identity is checked apart (conform/identity_mod_rows.py on a gridworld ledger)

    python tests/test_recipe_held_free.py
"""
from __future__ import annotations

import collections
import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def run(on: bool, budget: int) -> tuple:
    tether._RECIPE_HELD_FREE = on
    env = world.bind(world.Transitions())
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms()), tether.Config(work_budget=budget), led)
    ag.run(16)
    cut, priced = collections.Counter(), 0
    for r in led.rows():
        if r.get("event") == "park":
            d = r.get("detail", r)
            cut.update(d.get("cut_counts") or {})
            priced += d.get("candidates_priced") or 0
    minted = [(r.get("slot"), (r.get("detail") or {}).get("term")) for r in led.rows()
              if r.get("event") == "mint"]
    return cut.get("recipe-held", 0), cut.get("recipe-held: instances not generated", 0), \
        priced, minted


def main():
    was = getattr(tether, "_RECIPE_HELD_FREE", None)
    try:
        h_off, f_off, p_off, m_off = run(False, 60)
        h_on, f_on, p_on, m_on = run(True, 60)
        assert h_off > 0 and not m_off and h_on == 0 and f_on > 0 and p_on > p_off and m_on, (
            "MF-H1", h_off, f_off, p_off, m_off, h_on, f_on, p_on, m_on)
        _h, _f, _p, a_off = run(False, 15000)
        _h, _f, _p, a_on = run(True, 15000)
        assert a_off == a_on and a_off, ("MF-H2", a_off, a_on)
    finally:
        tether._RECIPE_HELD_FREE = was
    print(f"  MF-H1 budget 60: OFF held tries {h_off}, priced {p_off}, minted {m_off}; "
          f"ON held tries {h_on} ({f_on} not generated), priced {p_on}, minted {m_on}")
    print(f"  MF-H2 budget 15000: minted identical, {a_on}")
    print("test_recipe_held_free OK")


if __name__ == "__main__":
    main()
