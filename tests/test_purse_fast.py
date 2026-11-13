"""10a, THE PURSE'S CHEAP BOUND (TETHER_PURSE_FAST; the reviewer 2026-11-12, the dc22 profile:
18M purse checks in 25 steps, each summing the idle scopes). While the heads since the step began
are under the allowance, the purse is not spent (spent <= those heads), so the sum is skipped.

PF1  _purse_out ON equals OFF over a grid: heads before / at / after the step's start, idle heads
     0..60 (an idle scope open or closed), allowances -5..130 -- every answer and every _p_cross
MF-PF1 the plant: the bound taken with <= (the allowance itself reads "not spent") -> differs -> RED
PF2  gridworld 12 steps, the arm ON vs OFF: the ledgers identical (timings, arms row dropped)
Seconds.

    python tests/test_purse_fast.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import types

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import cap  # noqa: E402
import tether  # noqa: E402

HERE = _repo.ROOT


def answers(plant: bool = False) -> list:
    out = []
    h0 = 1000
    for heads in (990, 1000, 1001, 1040, 1060, 1100, 1129, 1130, 1131, 1200):
        for idle, open_idle in ((0, False), (25, False), (25, True), (60, True)):
            for allow in (-5, 0, 1, 40, 99, 100, 129, 130):
                got = []
                for arm in (True, False):
                    tether._PURSE_FAST = arm
                    ns = types.SimpleNamespace(
                        _clk_hs=[], _clk_h0=h0,
                        _clk_h={"PERCEIVE": 0 if open_idle else idle},
                        _clk_stack=[("PERCEIVE", None)] if open_idle else [], _p_cross=None)
                    if open_idle:       # the open idle scope began `idle` heads before now
                        ns._clk_hs = [heads - idle]
                    ns._allowance = lambda a=allow: a
                    ns._purse_spent = lambda ns=ns: tether.Agent._purse_spent(ns)
                    cap.HEADS = heads
                    if plant and arm:
                        r = False if 0 <= heads - h0 <= allow else _off(ns)
                    else:
                        r = tether.Agent._purse_out(ns)
                    got.append((r, ns._p_cross))
                out.append(got[0] == got[1])
    tether._PURSE_FAST = True
    return out


def _off(ns) -> bool:
    tether._PURSE_FAST = False
    try:
        return tether.Agent._purse_out(ns)
    finally:
        tether._PURSE_FAST = True


GW = r'''
import json, sys
import gamma, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
for _ in range(12):
    ag.step()
ag.end_run("cap")
with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as fh:
    for r in led.rows():
        fh.write(json.dumps(r, sort_keys=True, default=str) + "\n")
'''


def gw(path: str, arm: str) -> list[dict]:
    env = {**os.environ, "TETHER_PURSE_FAST": arm, "TETHER_AGENT_SEED": "0",
           "PYTHONIOENCODING": "utf-8"}
    p = subprocess.run([sys.executable, "-B", "-c", GW, path], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=600,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    with open(path, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh]


def strip(rows: list[dict]) -> list[str]:
    out = []
    for r in rows:
        if r.get("slot") == "@run" and r.get("event") == "arms":
            continue
        r = dict(r)
        r.pop("wall_s", None)
        d = r.get("detail")
        if isinstance(d, dict):
            r["detail"] = {k: v for k, v in d.items()
                           if "wall" not in k and k != "s" and not k.endswith(("_ms", "_s"))}
        out.append(json.dumps(r, sort_keys=True))
    return out


def main() -> int:
    a = answers()
    ok1 = all(a)
    print(f"  PF1: {sum(a)} of {len(a)} grid points equal ON vs OFF")
    print(f"PF1 the cheap bound gives the same answer: {'GREEN' if ok1 else 'RED'}")
    p = answers(plant=True)
    red = not all(p)
    print(f"  plant (<=): {len(p) - sum(p)} grid points differ")
    print(f"MF-PF1 the bound at the allowance itself: {'RED (as required)' if red else 'GREEN'}")
    with tempfile.TemporaryDirectory() as td:
        off = gw(os.path.join(td, "off.jsonl"), "0")
        on = gw(os.path.join(td, "on.jsonl"), "1")
    x, y = strip(off), strip(on)
    diff = sum(1 for u, v in zip(x, y, strict=False) if u != v) + abs(len(x) - len(y))
    print(f"  gw12: {len(off)} rows OFF, {len(on)} ON; differing {diff}")
    ok2 = diff == 0
    print(f"PF2 gw12 identical ON vs OFF: {'GREEN' if ok2 else 'RED'}")
    assert ok1 and red and ok2
    print("purse_fast: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
