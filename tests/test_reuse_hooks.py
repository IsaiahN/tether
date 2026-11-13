"""P6's hooks (TETHER_REUSE_BOOK; the reviewer's reuse.py, r1838; DESIGN_STEP8 P6 H1-H7).

  RH1   on the dc22 capture (acts forced, c0-9): after the replay the agent's book holds chances
        (H2: T0's entries and the walk's stage-0 heads, each offered under its context) and a paid
        use (H3: the sense settled at c8).
  MF-RH1 note_use made a no-op (the plant): the book holds no use -> RED.
  RH2   save -> load (H5, H1): a book's counts written by lineage.write come back in a fresh agent's
        book through reuse_n, and the age window is derived from them.
  gw12's OFF identity against the parent is the commit's check, not this file's.

    python tests/test_reuse_hooks.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import test_pay_gap as pg

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

HERE = _repo.ROOT

SPY = r'''
import atexit, os
import reuse
if os.environ.get("PLANT_NO_USE"):
    reuse.ReuseBook.note_use = lambda self, *a, **k: False
_A = tether.Agent
AG = []
_i = _A.__init__
def _i2(self, *a, **k):
    _i(self, *a, **k)
    AG.append(self)
_A.__init__ = _i2
def rep():
    b = AG[-1]._reuse if AG else None
    print("RH " + json.dumps({"chances": sum(b.chances.values()) if b else None,
                              "uses": sum(b.uses.values()) if b else None,
                              "paid": sum(b.paid.values()) if b else None,
                              "heads_used": sorted({h for (_c, h) in b.uses}) if b else None}))
atexit.register(rep)
'''


def rh1(plant: bool) -> dict:
    code = pg.REPLAY.replace("tether._AGENT_SEED = False\n",
                             "tether._AGENT_SEED = False\n" + SPY, 1)
    assert SPY in code
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    if plant:
        env["PLANT_NO_USE"] = "1"
    led = os.path.join(tempfile.mkdtemp(), "t.jsonl")
    data = os.path.join(HERE, "tests", "data", "cue_key_path", "dc22_c24.json.gz")
    p = subprocess.run([sys.executable, "-B", "-c", code, data, "10", led], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return next(json.loads(x[3:]) for x in p.stdout.splitlines() if x.startswith("RH "))


def _agent():
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        ledger.Ledger())


def rh2() -> tuple:
    d = Path(tempfile.mkdtemp(prefix="reuse_"))
    a = _agent()
    ctx = ("SELF", "COLOUR/POSITION", ("POSITION", "+", 1), "*")
    for _ in range(3):
        a._reuse.note_chance(ctx, "LIB|X")
    a._reuse.note_use(ctx, "LIB|X", paid=True)
    a._reuse.note_use(ctx, "LIB|X", paid=True)
    want = (dict(a._reuse.chances), dict(a._reuse.uses), dict(a._reuse.paid))
    lineage.write(d, a, "default")
    b = _agent()
    rep = lineage.load(d, b)
    got = (dict(b._reuse.chances), dict(b._reuse.uses), dict(b._reuse.paid))
    print(f"   written {want}; loaded {got}; window {b._reuse.window} "
          f"(the load's row: {rep.get('reuse_window')})")
    return got == want, b._reuse.window


def main() -> int:
    on = rh1(False)
    print(f"   dc22 c0-9 book: {on}")
    ok1 = bool(on["chances"]) and bool(on["uses"]) and bool(on["paid"])
    print("RH1 the book holds chances and a paid use after the replay: "
          + ("GREEN" if ok1 else "RED"))
    assert ok1, on
    pl = rh1(True)
    print(f"   the plant (note_use a no-op): {pl}")
    print("MF-RH1 no use is written: " + ("RED" if not pl["uses"]
                                          else "GREEN (the plant went unseen)"))
    assert not pl["uses"], pl
    ok2, window = rh2()
    print("RH2 save -> load brings the book back and derives its window: "
          + ("GREEN" if ok2 and window is not None else "RED"))
    assert ok2 and window is not None
    print("reuse_hooks: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
