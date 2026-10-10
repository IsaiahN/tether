"""7c M6 invent (TETHER_M6_INVENT; ISAIAH_RULINGS "Mint, invent, import"; the reviewer 2026-10-10
23:14Z). A hand trace on the ARC atom set: o1.row steps by o1.col exactly when o0.col == o1.col,
and stays otherwise. The agent names that condition, prices it at its whole length by the bargain,
and holds it in a private in-memory library copy.

  must-pass: the invention pays and is bound; its bet steps on the condition and holds off it;
  M6-a. a restating invention (one condition per changed row) does not pay; the single one does;
  M6-b. no depth discount: the price is term_bits of the WHOLE length, past max_depth too;
  M6-c. an under_floor park never triggers;
  spec 1. a condition naming a colour index is refused for carry; the shared library is untouched;
  spec 2. a condition naming no reading is refused at creation, and recorded;
  OFF: a 13-cycle gridworld_arc_s1 run never reaches _invent.

    python test_m6.py
"""
from __future__ import annotations

import os
import sys
import tempfile

import gamma
import ledger
import tether
import world

sys.dont_write_bytecode = True
sys.path.insert(0, "conform")
import panel  # noqa: E402

SLOT = "o1.row"


def _agent(member: str = "gridworld_arc_s0"):
    g, seed = panel._gridworld(member)
    env = world.bind(g)
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"m6_{seed}"), tether.Config(),
                      ledger.Ledger())
    ag.step()
    return ag


def _trace(ag, n: int = 36) -> list:
    st0 = dict(ag.trace[-1][0])
    rows = []
    for i in range(n):
        st = dict(st0)
        st["o1.col"], st["o0.col"], st[SLOT] = 1, i % 3, 2
        rows.append((st, "ACTION1", 3 if st["o0.col"] == st["o1.col"] else 2, None, None))
    return rows


def _base(ag, hist) -> float:
    return ag._left(ag.gamma.library[tether.IDN], SLOT, hist)


if __name__ == "__main__":
    tether._M6_INVENT = True
    ag = _agent()
    hist = _trace(ag)
    base = _base(ag, hist)
    ag._invent(SLOT, hist, base, base, "priced_out_at_depth")
    inv = [r["detail"] for r in ag.led.rows() if r["event"] == "invent"]
    assert inv and "?INVENTED" in str(inv[-1]["pick"]), inv
    d = inv[-1]
    term = ag.gamma.library[ag.bound[SLOT]]
    on, off = dict(hist[1][0]), dict(hist[0][0])
    assert ag._predict(SLOT, on, "ACTION1") == 3 and ag._predict(SLOT, off, "ACTION1") == 2
    print(f"  must-pass: '{d['condition']}' -> {d['pick']}, cost {d['term_bits']} + left "
          f"{d['left_bits']} < base {d['base_bits']}; bets 3 on the condition, 2 off it")
    c = ag._invented[d["key"]]
    f = gamma.Term(term.atoms, operand=term.operand)
    moved = sum(1 for r in hist if r[2] != r[0][SLOT])
    one = ag._inv_cost(f, [c]) + ag._inv_left(f, [c], SLOT, hist)
    many = ag._inv_cost(f, [c] * moved) + ag._inv_left(f, [c] * moved, SLOT, hist)
    assert one < base <= many, (one, base, many)
    print(f"  M6-a: one condition {one:.3f} < base {base:.3f}; one per changed row ({moved}) "
          f"{many:.3f} does not pay")
    deep = gamma.Term(tuple(f.atoms) * (ag.cfg.max_depth + 1), operand=f.operand)
    k = ag.gamma.length(deep) + ag.gamma.length(c.term)
    assert k > ag.cfg.max_depth
    assert ag._inv_cost(deep, [c]) == tether.term_bits(k, ag.gamma.alphabet)
    assert ag._inv_cost(deep, [c]) > tether.term_bits(ag.cfg.max_depth, ag.gamma.alphabet)
    print(f"  M6-b: length {k} past max_depth {ag.cfg.max_depth} is priced at its whole length")
    u = _agent()
    u._invent(SLOT, _trace(u), _base(u, _trace(u)), 0.0, "under_floor")
    assert not [r for r in u.led.rows() if r["event"] == "invent"] and not u._invented
    print("  M6-c: an under_floor park writes no invent row and invents nothing")
    lib = ag._inv_library()
    key = lib.invent_atom("red", "o1.colour == 3", game="m6", cycle=0)
    rec = lib.carry(key, "elsewhere")
    assert rec["carried"] is False and key not in tether._library().runtime
    assert d["key"] not in tether._library().runtime
    print(f"  spec 1: refused for carry ({rec['why']}); the shared library holds neither")
    n0 = len(ag._invented)
    got = ag._hold_invention(SLOT, "o9.zork != 0", c, f, 1.0, base, hist, {"verdict": "x"})
    last = [r["detail"] for r in ag.led.rows() if r["event"] == "invent"][-1]
    assert got is None and last["pick"] == "refused at creation" and len(ag._invented) == n0
    print(f"  spec 2: refused at creation and recorded ({last['why']})")
    tmp = os.path.join(tempfile.mkdtemp(), "g.json")
    ag.gamma.save(tmp)
    with open(tmp, encoding="utf-8") as fh:
        saved = fh.read()
    assert gamma.INVENTED_GUARD not in saved and d["key"] not in saved
    print("  carry: gamma.save writes no invented guard (M7, gated)")
    tether._M6_INVENT = False
    off = _agent("gridworld_arc_s1")

    def _never(*_a, **_k):
        raise AssertionError("_invent ran with the arm OFF")
    off._invent = _never
    for _ in range(12):
        off.step()
    print("  OFF: 13 steps of gridworld_arc_s1, _invent never ran")
    print("ok")
