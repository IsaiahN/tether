"""TRY_FIRST_ACTIONS (default ON; the reviewer r1821, r726's bound restored): the hold on the mint
and the goal split counts the unpressed offered actions only; untouched kinds keep steering
System 0's touches and no longer hold reasoning.

  P1    the dc22 capture (acts forced, c0-9: enough to part the gates, inside the six's 900 s cap),
        arm OFF: the mint held every cycle c1-9 as today (the target o39.col does not mint; over
        c0-29 it first mints at c23); arm ON: held c1-3, the target first mints at c4.
  MF1   the kinds planted back into the hold under the arm (_try_first_hold reads
        _try_first_open): held through c9 again, no target mint -> RED.
  P2    THE AIM IS UNCHANGED: per cycle, the untouched kinds System 0 aims at and every
        _contact_target pick made "untouched-kind" are the same ON as OFF on the same frames.
  MF2   no kind aim (TETHER_TOUCH_EACH_KIND=0): the picks change -> RED.
  gw12's OFF identity against the parent is the commit's check, not this file's.

    python tests/test_try_first_actions.py
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
TARGET = "o39.col"
CYCLES = 10
OFF_FIRST, OFF_HELD = None, 9           # over c0-29: first mint c23, held 19 (the census)
ON_FIRST, ON_HELD = 4, 3                # the build's own run on c0-29 agrees (the commit)

SPY = r'''
import atexit
_A = tether.Agent
AIM = {"kinds": {}, "picks": []}
if os.environ.get("TF_PLANT") == "kinds_back":
    _A._try_first_hold = lambda self: self._try_first_open()
_ct = _A._contact_target
def _ct2(self, before):
    out = _ct(self, before)
    if isinstance(out, tuple) and len(out) > 1 and out[1] == "untouched-kind":
        AIM["picks"].append([self.cycle, out[0]])
    return out
_A._contact_target = _ct2
_st = _A.step
def _st2(self, *a, **k):
    r = _st(self, *a, **k)
    AIM["kinds"][str(self.cycle)] = [len(ms) for ms in self._untouched_kinds(self.env.observe())]
    return r
_A.step = _st2
atexit.register(lambda: print("AIM", json.dumps(AIM)))
'''


def run(arm: bool, plant: str = "", touch: bool = True) -> tuple[list, dict]:
    code = pg.REPLAY.replace("tether._AGENT_SEED = False\n",
                             "tether._AGENT_SEED = False\n" + SPY, 1)
    assert SPY in code
    env = {k: v for k, v in os.environ.items() if not k.startswith(("TETHER_", "TF_"))}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_PAY_GAP="1", TETHER_TRY_FIRST_ACTIONS="1" if arm else "0")
    if plant:
        env["TF_PLANT"] = plant
    if not touch:
        env["TETHER_TOUCH_EACH_KIND"] = "0"
    led = os.path.join(tempfile.mkdtemp(), "t.jsonl")
    data = os.path.join(HERE, "tests", "data", "cue_key_path", "dc22_c24.json.gz")
    p = subprocess.run([sys.executable, "-B", "-c", code, data, str(CYCLES), led],
                       capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    aim = next(json.loads(x[4:]) for x in p.stdout.splitlines() if x.startswith("AIM "))
    with open(led, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()], aim


def reading(rows: list) -> tuple:
    held = len({r["cycle"] for r in rows if r["event"] == "try_first"})
    first = min((r["cycle"] for r in rows if r["event"] == "pay_gap" and r["slot"] == TARGET),
                default=None)
    return first, held


def main() -> int:
    off, aim_off = run(False)
    on, aim_on = run(True)
    f_off, h_off = reading(off)
    f_on, h_on = reading(on)
    print(f"P1 dc22 c0-{CYCLES - 1}: arm OFF target {TARGET} first mint c{f_off}, held {h_off} "
          f"cycles; arm ON first mint c{f_on}, held {h_on}")
    assert (f_off, h_off) == (OFF_FIRST, OFF_HELD), (f_off, h_off)
    assert (f_on, h_on) == (ON_FIRST, ON_HELD), (f_on, h_on)

    planted, _ = run(True, "kinds_back")
    f_p, h_p = reading(planted)
    print(f"MF1 kinds planted back into the hold (arm ON): first mint c{f_p}, held {h_p} -> "
          + ("RED" if (f_p, h_p) != (f_on, h_on) else "GREEN (the plant went unseen)"))
    assert (f_p, h_p) == (f_off, h_off) and (f_p, h_p) != (f_on, h_on), (f_p, h_p)

    same_k = aim_on["kinds"] == aim_off["kinds"]
    same_p = aim_on["picks"] == aim_off["picks"]
    print(f"P2 the aim: untouched kinds per cycle equal ON vs OFF: {same_k}; untouched-kind picks "
          f"{len(aim_on['picks'])} ON vs {len(aim_off['picks'])} OFF, equal: {same_p}")
    assert same_k and same_p, (aim_on["picks"][:4], aim_off["picks"][:4])
    _r, aim_nt = run(True, touch=False)
    print(f"MF2 no kind aim (TETHER_TOUCH_EACH_KIND=0): picks {len(aim_nt['picks'])} -> "
          + ("RED" if aim_nt["picks"] != aim_on["picks"] else "GREEN (the plant went unseen)"))
    assert aim_nt["picks"] != aim_on["picks"]
    print("try_first_actions: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
