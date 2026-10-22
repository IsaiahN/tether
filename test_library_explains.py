"""(iv), RECOGNITION EXPLAINS (TETHER_LIBRARY_EXPLAINS; the reviewer 2026-10-21 21:52, 2026-10-22
01:55). A planted trace where y's next value is x's value now: the library term take<x> explains y
exactly, idn misses it. The term is SERVED (route's rebind), then judged by settle.

  LE1  ON: served, it makes the bet and settles -> outstanding(y) falls by the bits it explains
       (base under idn minus its leftover, 0), and a SETTLE "library_explained" row says so.
  LE2  ON: served, but the bet is not its own (no maker) -> nothing credited, no row.
  LE3  a MINTED bind credits exactly as before: the mint's explained / overclaimed and outstanding
       are the same with the arm ON and OFF.
  ID   OFF: LE1's sequence credits nothing and writes no row; its ledger equals ON's less the
       one library_explained row.

    python test_library_explains.py
"""
from __future__ import annotations

import sys

import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True
sys.path.insert(0, "conform")
from identity_mod_rows import compare  # noqa: E402  the one identity reader, imported

SEQ = [0, 3, 5, 1, 6, 2, 7, 4] * 2          # y's next value is x's value now


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="library_explains"),
                      tether.Config(), ledger.Ledger())
    states = [{"x": SEQ[i], "y": SEQ[i - 1] if i else 7} for i in range(len(SEQ))]
    ag.trace = [(states[i], "A", states[i + 1], None, None) for i in range(len(SEQ) - 1)]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x", "y"]
    ag.alphabet["x"] = ag.alphabet["y"] = 8
    ag.bound = {}
    return ag


def _served(arm: bool, maker: bool) -> tuple[float, float, list, list]:
    tether._LIBRARY_EXPLAINS = arm
    try:
        ag = _agent()
        term = ag.gamma.build(("take",), operand="x")
        ag.gamma.accept(term, seq=len(ag.led), residual="fixture")
        base = ag._left(ag.gamma.library[tether.IDN], "y", ag.history("y"))
        ag._outstanding["y"] = base
        ag._serve("y", term.name)                 # the route's REBIND, as at its bind site
        ag.bound["y"] = term.name
        ag.candidates[term.name] = ag.cycle
        ag._cand_level[term.name] = ag.level
        ag.cycle += 1
        ag._pred_by = {"y": term.name} if maker else {}
        ag.settle({"y": tether.SlotResidual("y", "transition", 1, 1, 0.0)})
        rows = [r for r in ag.led.rows() if r["event"] == "library_explained"]
        return base, ag.outstanding("y"), rows, ag.led.rows()
    finally:
        tether._LIBRARY_EXPLAINS = False


def _minted(arm: bool) -> tuple:
    tether._LIBRARY_EXPLAINS = arm
    try:
        ag = _agent()
        base = ag._left(ag.gamma.library[tether.IDN], "y", ag.history("y"))
        ag._outstanding["y"] = base
        ag.mint("y")
        acc = [(r["event"], r["detail"]["explained"], r["detail"].get("overclaimed"))
               for r in ag.led.rows() if r["slot"] == "y" and "explained" in r["detail"]]
        return ag.bound.get("y"), ag.outstanding("y"), acc
    finally:
        tether._LIBRARY_EXPLAINS = False


def main() -> int:
    tether._AGENT_SEED = False     # C-seed-X: separately born agents compared, one temperament
    base, after, rows, on_rows = _served(True, True)
    assert base > 0 and rows and abs(after - (base - rows[0]["detail"]["explained"])) < 1e-9, (
        base, after, rows)
    assert rows[0]["detail"]["explained"] == round(base, 3) and after < 1e-9, (base, after, rows)
    print(f"  LE1: served take<x> bet and settled: outstanding(y) {base:.3f} -> {after:.3f}, "
          f"explained {rows[0]['detail']['explained']}")
    b2, a2, r2, _ = _served(True, False)
    assert not r2 and abs(a2 - b2) < 1e-9, (b2, a2, r2)
    print(f"  LE2: served but the bet not its own: outstanding(y) {b2:.3f} -> {a2:.3f}, no row")
    on, off = _minted(True), _minted(False)
    assert on == off and on[0] and on[2], (on, off)
    print(f"  LE3: a minted bind credits as before: bound {on[0]}, outstanding {on[1]:.3f}, "
          f"accept rows {on[2]} (ON = OFF)")
    b0, a0, r0, off_rows = _served(False, True)
    for rs in (on_rows, off_rows):                             # the arm lists differ by design
        for r in rs:
            if r["event"] == "arms" and r["slot"] == "@run":
                r["detail"].pop("on", None)
                r["detail"].pop("off", None)
    bad = compare(off_rows, on_rows, {"library_explained"})   # positions mapped past the new row
    assert not r0 and abs(a0 - b0) < 1e-9 and not bad, (b0, a0, len(r0), bad[:3])
    print(f"  ID: OFF credits nothing (outstanding {b0:.3f} -> {a0:.3f}), no row, and its "
          f"{len(off_rows)} rows equal ON's less the one library_explained row (compare())")
    print("library_explains: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
