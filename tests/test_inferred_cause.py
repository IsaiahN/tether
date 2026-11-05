"""BUILD 4 ITEM 14a, INFERRED CAUSES (TETHER_INFERRED_CAUSE; the reviewer 2026-11-04 r1171; Isaiah
11-03 14:29). Where an invention finds no visible condition, a hidden cause is read from the agent's
own record (a count of presses since the slot last changed, or a latch), seeded from the trace and
priced by the invention's bargain. Seconds: a gridworld agent stepped once, its trace then set by
hand for one slot, _invent called as the park calls it.

MF-C1  o0.row changes on every 3rd press of ACTION1, 8 times (ACTION2 presses between): no visible
       condition holds; ON holds "presses of action ACTION1 since o0.row changed == 3", a guarded
       inc that fits every row -- the non-change rows too (r1171 guard 2), and the occasion's
       candidate count is reported (guard 3)
MF-C3  the same changes, o1.row equal to o0.row exactly there (ARC's atoms): a visible condition, so
       no cause is formed; and an @goal slot is never a condition (guard 1)
The red is behavioural, the arm OFF on this tree: TETHER_INFERRED_CAUSE=0 fails MF-C1.

    python tests/test_inferred_cause.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_atoms  # noqa: E402
import arc_predict  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

S = "o0.row"
# eight changes, each at the 3rd ACTION1 press since the last; every other block has an ACTION2
# between (the non-change rows a coincidental count would mispredict). Eight, because a cause's
# description costs a constant and the residual it removes grows with the changes: on three the
# bargain refuses it (cost 10.7 bits against 7.0), which is the bargain working
BLOCKS = [["ACTION1", "ACTION1", "ACTION1"], ["ACTION1", "ACTION2", "ACTION1", "ACTION1"]] * 4
ACTS = [a for b in BLOCKS for a in b]
MOVED = {sum(len(b) for b in BLOCKS[:k + 1]) - 1 for k in range(len(BLOCKS))}


def agent(witness: bool, slot: str = S, other: str = "o1.row", arc: bool = False):
    env = world.bind(gridworld.family("default", 0))
    atoms = {a.name: a for a in env.atoms()}
    if arc:      # ARC's own comparison atoms, so a visible POSITION equality compiles
        atoms.update({a.name: a for a in arc_atoms.three_spaces(arc_predict.predict())})
    ag = tether.Agent(env, gamma.Gamma(list(atoms.values()), game="fam_default_0"),
                      tether.Config(), ledger.Ledger())
    ag.step()
    rows, v = [], 0
    for i, a in enumerate(ACTS):
        before = {slot: v, other: (v if i in MOVED else v + 7) if witness else 9}
        v2 = v + 1 if i in MOVED else v
        rows.append((before, a, {**before, slot: v2}, None, None))
        v = v2
    ag.trace = rows
    ag._lib_offers.pop(slot, None)
    ag._inv_seen.pop(slot, None)
    return ag


def invent(ag, slot: str = S):
    hist = ag.history(slot)
    idn = ag.gamma.library[tether.IDN]
    base = sum(ag._left(idn, slot, [r]) for r in hist)
    n0 = len(ag.led.rows())
    ag._invent(slot, hist, base, base, "budget_spent")
    rows = [r["detail"] for r in ag.led.rows()[n0:] if r.get("event") == "invent"]
    return hist, rows


def main():
    ag = agent(witness=False)
    hist, rows = invent(ag)
    causes = [c for c in ag._invented.values() if isinstance(c, tether.Cause)]
    assert rows and causes == [tether.Cause("count", S, "ACTION1", 3)], (
        "MF-C1: no inferred cause is held where no visible condition holds", rows, causes)
    d = rows[-1]
    term = ag.gamma.library[ag.bound[S]]
    assert d["conditions_held"] == 0 and d["causes"]["candidates"] >= 1 and \
        ag._left(term, S, hist) == 0.0, ("MF-C1 fit", d, ag._left(term, S, hist))
    print(f"  MF-C1 held {d['condition']!r} as {term.name}; fits all {len(hist)} rows; "
          f"causes {d['causes']}")
    # o1.row equals o0.row exactly at the changes; with ARC's comparison atoms the visible
    # equality compiles (gridworld's same takes EXTENT only), so the invention has a condition
    ag2 = agent(witness=True, arc=True)
    _h2, rows2 = invent(ag2)
    assert rows2 and rows2[-1]["conditions_held"] > 0 and "causes" not in rows2[-1] and not [
        c for c in ag2._invented.values() if isinstance(c, tether.Cause)], ("MF-C3", rows2)
    texts = ag2._inv_conditions({S: 1, "@goal.completed": 0, "o1.row": 1})
    assert texts and not [t for t in texts if "@" in t], ("MF-C3 guard 1", texts[:5])
    print(f"  MF-C3 a visible condition holds ({rows2[-1]['conditions_held']}): no cause; "
          f"{len(texts)} conditions, none on an @ slot")
    print("test_inferred_cause OK")


if __name__ == "__main__":
    main()
