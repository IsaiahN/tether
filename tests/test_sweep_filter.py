"""P1 (the reviewer r1838; DESIGN_STEP8 D2, F4): TETHER_SWEEP_FILTER and TETHER_EXHAUSTED_WORD, on
the dc22 capture (acts forced, c0-11: the sweeps after the c6-c10 accepts, and o39.col's park at
c10, whose search was priced out at its depth).

  P1    ON: no bind that _operand_fits refuses reaches the sweep's _left, and the filter acted
        (reuse_branch "sweep:operand-refused" > 0); the cost skips are counted (reuse_refused rows
        reason cost-at-or-over-base).
  MF1   both arms OFF: refused binds reach the sweep's _left (> 0) -> RED.
  P2    ON: every slot parked with a priced_out_at_depth search owes after its park, under that
        verdict (owed_import + abstained[slot]["verdict"] == "priced_out_at_depth").
  MF2   both arms OFF: such a slot does not owe -> RED.
  gw12's OFF identity against the parent is the commit's check, not this file's.

    python tests/test_sweep_filter.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import test_pay_gap as pg

sys.dont_write_bytecode = True
HERE = _repo.ROOT
CYCLES = 12

SPY = r'''
import atexit
_A = tether.Agent
OUT = {"refused_left": 0, "sweeps": 0, "owed": {}, "branch": {}}
_CUR = []
_of = _A._operand_fits
_sw = _A.sweep
def _sw2(self, term, origin_slot):
    OUT["sweeps"] += 1
    _CUR.append(term)
    try:
        return _sw(self, term, origin_slot)
    finally:
        _CUR.pop()
_A.sweep = _sw2
_lf = _A._left
def _lf2(self, t, slot, hist, *a, **k):
    if _CUR and t.atoms == _CUR[-1].atoms and getattr(t, "operand", None) is not None:
        if not _of(self, _CUR[-1], slot, t.operand):
            OUT["refused_left"] += 1
    return _lf(self, t, slot, hist, *a, **k)
_A._left = _lf2
_st = _A.step
def _st2(self, *a, **k):
    r = _st(self, *a, **k)
    OUT["owed"][str(self.cycle)] = {s: (self.abstained.get(s) or {}).get("verdict")
                                    for s in self.owed_import}
    OUT["branch"] = dict(self.chain.reuse_branch)
    return r
_A.step = _st2
atexit.register(lambda: print("SWF", json.dumps(OUT)))
'''


def run(arms_on: bool) -> tuple[list, dict]:
    code = pg.REPLAY.replace("tether._AGENT_SEED = False\n",
                             "tether._AGENT_SEED = False\n" + SPY, 1)
    assert SPY in code
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    if not arms_on:
        env.update(TETHER_SWEEP_FILTER="0", TETHER_EXHAUSTED_WORD="0")
    led = os.path.join(tempfile.mkdtemp(), "t.jsonl")
    data = os.path.join(HERE, "tests", "data", "cue_key_path", "dc22_c24.json.gz")
    p = subprocess.run([sys.executable, "-B", "-c", code, data, str(CYCLES), led],
                       capture_output=True, text=True, env=env, cwd=HERE,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    out = next(json.loads(x[4:]) for x in p.stdout.splitlines() if x.startswith("SWF "))
    with open(led, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()], out


def priced_out(rows: list) -> list:
    """(cycle, slot) of every park whose search was priced out at its depth (the row may carry the
    relabelled verdict, with the search's own word in stopped_by)."""
    return [(r["cycle"], r["slot"]) for r in rows if r["event"] == "park"
            and "priced_out_at_depth" in (r["detail"].get("verdict"),
                                          r["detail"].get("stopped_by"))]


def owes_after(out: dict, cycle: int, slot: str) -> bool:
    """The slot owes BECAUSE of its priced-out park: owed with that park's own verdict recorded
    (an earlier park's debt on the same slot carries another verdict, so it cannot pass this)."""
    return any(owed.get(slot) == "priced_out_at_depth"
               for c, owed in out["owed"].items() if int(c) >= cycle)


def main() -> int:
    on_rows, on = run(True)
    off_rows, off = run(False)
    skips = sum(1 for r in on_rows if r["event"] == "reuse_refused"
                and r["detail"].get("reason") == "cost-at-or-over-base")
    refused = on["branch"].get("sweep:operand-refused", 0)
    print(f"P1 dc22 c0-{CYCLES - 1} ON: sweeps {on['sweeps']}, refused binds reaching _left "
          f"{on['refused_left']}, binds the filter refused {refused}, cost skips {skips}")
    print(f"MF1 both arms OFF: sweeps {off['sweeps']}, refused binds reaching _left "
          f"{off['refused_left']} -> "
          + ("RED" if off["refused_left"] else "GREEN (no occasion: the plant went unseen)"))
    if not off["refused_left"]:
        print("ERROR: no refused bind reached the sweep's _left with the arm OFF -- no occasion")
        return 2
    assert on["refused_left"] == 0 and refused > 0, (on["refused_left"], refused)

    po_on, po_off = priced_out(on_rows), priced_out(off_rows)
    owed_on = [(c, s, owes_after(on, c, s)) for c, s in po_on]
    owed_off = [(c, s, owes_after(off, c, s)) for c, s in po_off]
    print(f"P2 ON: priced-out parks {po_on}; owing after their park: {owed_on}")
    print(f"MF2 both arms OFF: priced-out parks {po_off}; owing after: {owed_off} -> "
          + ("RED" if po_off and not all(o for _c, _s, o in owed_off)
             else "GREEN (the plant went unseen)"))
    if not po_on or not po_off:
        print("ERROR: no priced_out_at_depth park on this capture -- no occasion")
        return 2
    assert all(o for _c, _s, o in owed_on), owed_on
    assert not all(o for _c, _s, o in owed_off), owed_off
    print("sweep_filter: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
