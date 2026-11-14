"""THE GOAL'S FLOOR (TETHER_GOAL_FLOOR, default ON; the reviewer r1967; the lp85 replay r1966:
173 s in a stage whose cheapest condition cost term_bits(1), and none paid).
  F1  a history whose base k log2 n is under term_bits(1): ON returns none paid at once, with
      floor_bits on the row and nothing priced; OFF prices every condition and also picks none
  F2  the premise: every condition priced in F1's history costs at least the floor; every term
      the agent holds has length >= 1; term_bits never falls as length grows
  F3  the templates later steps read (_inv_tpl) are the same ON and OFF after the call
  F4  a history whose base is over the floor: ON and OFF give the same pick and the same row
  MF-F1 TETHER_GOAL_FLOOR OFF: no floor_bits, conditions priced -> RED as required
  F5  gridworld 12 steps ON and OFF both pass the gate
Seconds.
    python tests/test_goal_floor.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def agent():
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    ag.step()
    return ag


def history(ag, n, k):
    s0 = {key: v for key, v in ag.env.observe().items() if isinstance(v, int)}
    mover = next(key for key in sorted(s0) if key.endswith(".col") and key.startswith("o"))
    rows = []
    for t in range(n):
        st = dict(s0)
        st[mover] = t % 7
        rows.append((st, t >= n - k))
    return rows


def run(on, n, k, varies=True):
    tether._GOAL_FLOOR, tether._GOAL_VARIES = on, varies
    ag = agent()
    costs = []
    price = ag._goal_price

    def spy(conds, rows, truth=None):
        out = price(conds, rows, truth)
        costs.append(out[0])
        return out
    ag._goal_price = spy
    best, d = ag._goal_candidates(history(ag, n, k))
    tether._GOAL_FLOOR, tether._GOAL_VARIES = True, True
    return best, d, costs, dict(ag._inv_tpl), ag


def main() -> int:
    assert tether._GOAL_FLOOR is True, "the arm defaults ON"
    b_on, d_on, c_on, tpl_on, ag = run(True, 8, 1)
    floor = tether.term_bits(1, ag.gamma.alphabet)
    b_off, d_off, c_off, tpl_off, _ag = run(False, 8, 1)
    assert d_on["base_bits"] <= floor, (d_on, floor)
    assert b_on is None and b_off is None, ("F1: the pick differs", b_on, b_off)
    assert d_on["floor_bits"] == round(floor, 3) and d_on["conditions"] == 0 and not c_on, d_on
    assert d_off["conditions"] > 0 and c_off, d_off
    print(f"F1 base {d_on['base_bits']} <= floor {d_on['floor_bits']}: ON none paid with nothing "
          f"priced; OFF priced {len(c_off)} and none paid: GREEN")
    _b, _d, c_all, _t, _a = run(False, 8, 1, varies=False)
    assert c_all and min(c_all) >= floor - 1e-9, (c_all, floor)
    lens = [ag.gamma.length(t) for t in ag.gamma.library.values()]
    lens += [ag.gamma.length(tether.Term((a,))) for a in ag.gamma.atoms]
    assert lens and min(lens) >= 1, ("F2: a term of length 0", min(lens))
    bits = [tether.term_bits(z, ag.gamma.alphabet) for z in range(1, 40)]
    assert all(x <= y for x, y in zip(bits, bits[1:], strict=False)), "F2: not monotone"
    print(f"F2 the premise: every priced condition >= floor ({len(c_all)} here, min "
          f"{min(c_all):.3f}); {len(lens)} terms all of length >= 1; term_bits monotone in "
          "length: GREEN")
    assert tpl_on == tpl_off, "F3: the templates differ"
    print(f"F3 _inv_tpl the same ON and OFF ({len(tpl_on)} templates): GREEN")
    assert "floor_bits" not in d_off
    print("MF-F1 the arm OFF: no floor_bits, conditions priced -> RED (as required)")

    n, k = 64, 0
    while k * 6 <= floor:       # log2 64 = 6
        k += 1
    b_on, d_on, c_on, _t, _a = run(True, n, k)
    b_off, d_off, c_off, _t, _a = run(False, n, k)
    assert d_on["base_bits"] > floor, (d_on["base_bits"], floor)
    assert (b_on and b_on[4]) == (b_off and b_off[4]) and d_on == d_off, ("F4", d_on, d_off)
    print(f"F4 base {d_on['base_bits']} > floor: ON = OFF, pick {b_on and b_on[4]!r}, "
          f"{d_on['conditions']} conditions: GREEN")

    for on in (True, False):
        tether._GOAL_FLOOR = on
        env = world.bind(gridworld.family("default", 0))
        led = ledger.Ledger()
        ag3 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                           led)
        for _ in range(12):
            ag3.step()
        ag3.end_run("cap")
        v = gate.check(led.rows())["verdict"]
        assert v == "pass", ("F5", on, v)
    tether._GOAL_FLOOR = True
    print("F5 gridworld 12 steps ON and OFF: both pass the gate: GREEN")
    print("goal_floor: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
