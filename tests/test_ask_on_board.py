"""11 ASK_ON_BOARD (TETHER_ASK_ON_BOARD, default ON; the reviewer r452 A).
Minimal gates: one must-fail (with the occasion), one must-hold, each in its own process.
  check_mustfail_off_board  a gridworld agent whose 1b space holds a gap on a slot absent from this
                            step's `before` (two survivors): OFF picks it and raises KeyError on
                            that slot; ON skips it, keeps it in the space, and with a second gap on
                            the board asks that one, its ask row carrying gaps_off_board 1
  check_off_identity        MUST-HOLD: TETHER_ASK_ON_BOARD=0 (off_env) byte-equal to eadee1a on the
                            fake whole run; ON's run is compared too
    python tests/test_ask_on_board.py [check ...]
"""
from __future__ import annotations

import io
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "eadee1a"        # general-agent after 10 ARRIVAL_ALIAS
GONE, HERE = "o99.col", "o0.row"     # a slot on no board, and one on this board


def _agent(on: bool, gaps: tuple):
    """A gridworld agent after 3 steps, 1b's space holding `gaps`, each with two survivors that
    differ only under the first action (test_ask's constructed gap)."""
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    tether._ASK_ON_BOARD = on
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), led)
    for _ in range(3):
        ag.step()
    first = tuple(ag.actions)[0]
    step_ = gamma.Atom("aob_step", lambda v, c: v + 1 if c.action == first else v, "val", "val")
    still = gamma.Atom("aob_still", lambda v, _c: v, "val", "val")
    terms = [gamma.Term((step_,)), gamma.Term((still,))]
    ag._space = {s: {"kind": (), "opened": ag.cycle, "mints": 1, "base": None} for s in gaps}
    ag._space_bounds = lambda s, _mode: ([(t, 0.0) for t in terms], 1.0) if s in gaps else None
    ag._ask_cyc = (None, None)
    before = env.observe()
    assert GONE not in before and HERE in before, sorted(before)[:8]
    return ag, led, before, first


def check_mustfail_off_board() -> None:
    ag, _led, before, _first = _agent(False, (GONE,))
    try:
        ag._ask(before)
        raised = None
    except KeyError as e:
        raised = e.args[0]
    assert raised == GONE, ("MUST-FAIL: OFF should raise KeyError on the absent slot", raised)
    ag, led, before, _first = _agent(True, (GONE,))
    assert ag._ask(before) == (None, None)
    assert GONE in ag._space, "ON released the gap"
    ag, led, before, first = _agent(True, (GONE, HERE))
    n0 = len(led.rows())
    r, gap = ag._ask(before)
    asks = [x["detail"] for x in led.rows()[n0:] if x["event"] == "ask"]
    assert len(asks) == 1 and gap == HERE and r is not None and r.action == first, (asks, gap, r)
    d = asks[0]
    assert d["gap_asked"] == HERE and d["gaps_off_board"] == 1 and d["gaps_eligible"] == 1, d
    assert GONE in ag._space, "ON released the gap"
    print(f"  OFF: KeyError {raised!r} on the gap whose slot is on no board; ON: that gap is "
          f"skipped and kept in the space; with {HERE} on the board the ask takes {first} on "
          f"{HERE}, gaps_off_board {d['gaps_off_board']}, gaps_eligible {d['gaps_eligible']}")


def check_off_identity() -> None:
    import tarfile
    import tempfile

    from _batch import off_env
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d))
    off = _norm(_child(root, off_env("TETHER_ASK_ON_BOARD")))
    diff = sum(1 for x, y in zip(base, off, strict=False) if x != y) + abs(len(base) - len(off))
    assert len(base) > 50 and diff == 0, ("OFF", len(base), len(off), next(
        (i for i, (x, y) in enumerate(zip(base, off, strict=False)) if x != y), None))
    on_rows = _child(root)
    on = _norm(on_rows)
    asks = sum(1 for r in on_rows if r["event"] in ("ask", "ask_none"))
    on_diff = sum(1 for x, y in zip(base, on, strict=False) if x != y) + abs(len(base) - len(on))
    assert asks > 0 or on_diff == 0, ("ON differs with no ask row", on_diff)
    print(f"  OFF (TETHER_ASK_ON_BOARD=0, fake): {len(base)} rows against {BASE}, 0 differences; "
          f"ON: {asks} ask / ask_none rows, {on_diff} rows differ")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        assert r.returncode == 0, n
    print(f"ask_on_board: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
