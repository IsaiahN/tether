"""BUILD 4 ITEM 13, CONTACT-SEEDED CANDIDATE GENERATION (TETHER_CONTACT_SEED; the reviewer
2026-11-03 r978). The step's mint slots are ordered by two seeds ranked together -- contact slots
that changed this step, and settled residual-lit → junctions whose readings carry no term (a site
R with operand L) -- seen first, then the old order; nothing dropped. About 10 s.

MF-C1  a contact that changed o1.row orders a routed [o1.col, o1.row] as o1.row first
MF-C2  a settled → o1.dcol → o1.drow, lit by o1.drow's residual, with no term on either reading
       (the molecule pass over a hand-built window) seeds o1.drow: ordered first, and o1.dcol
       first among its binds; RED on HEAD (no seeds)
MF-C3  no seeds: the routed order is the old one, and no mint_seeds row
MF-C4  (r979) at a seeded slot the mint's own outcome is counted: a stubbed _mint_in_step writing
       a park row (verdict budget_spent) gives {"park: budget_spent": 1}; an unseeded slot counts
       nothing
MF-OFF the arm OFF (a child): no mint_seeds row, no seeds

    python tests/test_contact_seed.py
"""
from __future__ import annotations

import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import composer  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

M = tether.MECHANISM


def agent():
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    ag.step()
    return ag, led


def seeds_rows(led):
    return [r.get("detail", r) for r in led.rows() if r.get("event") == "mint_seeds"]


def main():
    if "--off" in sys.argv:
        assert not tether._CONTACT_SEED
        ag, led = agent()
        for _ in range(5):
            ag.step()
        assert not seeds_rows(led) and not ag._seed_ops, "OFF"
        print("off ok")
        return
    assert tether._CONTACT_SEED, "the arm is ON by default"
    ag, led = agent()
    ag._mol_key = None
    ag.trace = [({"o1.row": 0, "o1.col": 0}, "ACTION1", {"o1.row": 1, "o1.col": 0})]
    ag._window_at, ag._contact_slots, ag._lookup_pairs = 0, {"o1.row", "o1.col"}, {}
    routed = [("o1.col", M, None, ""), ("o1.row", M, None, "")]
    c1 = [r[0] for r in ag._seed_order(routed)]
    assert c1 == ["o1.row", "o1.col"], ("MF-C1", c1)

    ag, led = agent()
    fr = [{"o1.dcol": a, "o1.drow": b, "o3.x": 0}
          for a, b in ((0, 0), (1, 0), (1, 1), (2, 1), (2, 2))]
    one = next(m for m, r in composer.recipe_rows().items() if len(r["junctions"]) == 1)
    ag.trace = [(fr[t], "ACTION1", fr[t + 1]) for t in range(4)]
    ag._window_at, ag._mol_key, ag._contact_slots = 0, None, set()
    ag.bound = {"o3.x": "idn"}
    ag._read_terms = {}
    ag._lookup_pairs = {"o1.drow": [{"molecule": one, "left": "a", "right": "b",
                                     "left_reading": "o1.dcol", "right_reading": "o1.drow",
                                     "held": ["→"], "via": [], "occasions": {}}]}
    c2 = [r[0] for r in ag._seed_order([("o2.x", M, None, ""), ("o1.drow", M, None, "")])]
    b2 = ag._seed_binds("o1.drow", ["o5.r", "o1.dcol"])
    row2 = seeds_rows(led)[-1]
    assert c2 == ["o1.drow", "o2.x"] and b2 == ["o1.dcol", "o5.r"] \
        and row2["junction_sample"] == {"o1.drow": ["o1.dcol"]}, ("MF-C2", c2, b2, row2)

    ag, led = agent()
    ag.trace, ag._window_at, ag._mol_key = [], 0, None
    ag._contact_slots, ag._lookup_pairs = set(), {}
    n0 = len(seeds_rows(led))
    routed = [("o1.col", M, None, ""), ("o1.row", M, None, "")]
    c3 = ag._seed_order(list(routed))
    assert c3 == routed and len(seeds_rows(led)) == n0, ("MF-C3", c3)

    ag._seeded_now, ag._seed_outcome = {"o1.row"}, tether.collections.Counter()

    def stub(slot, _b, a=ag):
        a.led.record(a.cycle, "MINT", slot, "park", of=(slot,), verdict="budget_spent")
    ag._mint_in_step = stub
    ag._mint_at("o1.row", M)
    ag._mint_at("o1.col", M)
    c4 = dict(ag._seed_outcome)
    assert c4 == {"park: budget_spent": 1}, ("MF-C4", c4)

    env = {**os.environ, "TETHER_CONTACT_SEED": "0", "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run([sys.executable, "-B", __file__, "--off"], env=env, capture_output=True,
                         text=True, timeout=300)
    assert out.returncode == 0, out.stderr[-2000:]
    print(f"  MF-C1 contact on o1.row: {c1}")
    print(f"  MF-C2 junction seed: order {c2}, binds {b2}, row {row2['junction_sample']}")
    print(f"  MF-C3 no seeds: {[r[0] for r in c3]}")
    print(f"  MF-C4 the seeded slot's mint outcome: {c4}")
    print(f"  MF-OFF {out.stdout.strip().splitlines()[-1]}")
    print("test_contact_seed OK")


if __name__ == "__main__":
    main()
