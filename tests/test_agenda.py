"""THE AGENDA READER (TETHER_AGENDA; BUILD_SEQUENCE 2a; r1948/r1949). It runs a Tether card each
PLAN step, chosen by the residual's shape, and writes one decision row per step.

A1  a board with no progress where nothing is told apart: Which link first asks SEE; with SEE met
    and the hold on, it asks WORDS (SEE before WORDS)
MF-A1 the plant: TETHER_AGENDA=0 -> no agenda rows -> RED
A2  refuted_by: the first unmet link unchanged while the gap shrinks -> Which link first dropped for
    the board (a refuted_by row) and the next card by order (Instrument the middle) asked
A3  budget: the same question on one board with no new residual is not asked a third time
A4  a card's do_sym whose symbol has no reading writes "unbound", never a value
A5  gridworld 12 steps, the arm ON vs OFF: both complete and pass the gate; OFF writes no agenda
    rows (the OFF identity against development is the batch's check)
Seconds.

    python tests/test_agenda.py
"""
from __future__ import annotations

import os
import subprocess
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

HERE = _repo.ROOT
CHILD = r'''
import os, sys
sys.path.insert(0, os.getcwd())
import agenda, gamma, gridworld, ledger, tether, world
mode = sys.argv[1]
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
ag.step()
out = {}
rows = lambda: [r["detail"] for r in led.rows() if r.get("event") == "agenda"]
if mode == "off":
    out["reader"] = ag._agenda is None
    out["rows"] = len(rows())
else:
    R = agenda.Reader()
    n0 = len(rows())
    ag._hyp, ag._res = None, {}
    if mode == "see":
        st = ag.slot_types
        ag.slot_types = {}
        ag._try_first_hold = lambda: 2
        R.step(ag)
        ag.slot_types = st
        R.step(ag)
        out["questions"] = [(d["card"], d["question"].split(":", 1)[0]) for d in rows()[n0:]]
    elif mode == "refute":
        ag._try_first_hold = lambda: 0
        seq = [[3, 3], [3, 2], [2, 1], [1, 0], [1, 0]]
        for v in seq:
            ag._res = {"o0.row": list(v)}
            R.step(ag)
        ag._res = {"o0.row": [5, 5]}
        R.step(ag)
        out["cards"] = [(d["card"], d["question"][:12]) for d in rows()[n0:]]
    elif mode == "budget":
        ag._try_first_hold = lambda: 2
        for _ in range(5):
            R.step(ag)
        out["words"] = sum(1 for d in rows()[n0:] if d["question"].startswith("WORDS"))
    elif mode == "unbound":
        ag._try_first_hold = lambda: 2
        R.step(ag)
        out["sym"] = [d["sym"] for d in rows()[n0:] if d["card"] == "Which link first"]
print(repr(out))
'''

GW = r'''
import sys
import gamma, gate, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
for _ in range(12):
    ag.step()
ag.end_run("cap")
rows = led.rows()
print(repr((len(rows), gate.check(rows)["verdict"],
            sum(1 for r in rows if r.get("event") == "agenda"))))
'''


def child(code: str, *args: str, **arms: str):
    env = {**os.environ, "TETHER_AGENT_SEED": "0", "PYTHONIOENCODING": "utf-8", **arms}
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=900,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return eval(p.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


def main() -> int:
    s = child(CHILD, "see")
    q = [x for x in s["questions"] if x[0] == "Which link first"]
    ok1 = [x[1] for x in q] == ["SEE", "WORDS"]
    print(f"  A1 {s}")
    print(f"A1 SEE asked before WORDS: {'GREEN' if ok1 else 'RED'}")
    o = child(CHILD, "off", TETHER_AGENDA="0")
    red1 = o["reader"] and o["rows"] == 0
    print(f"MF-A1 the arm OFF: reader None, rows {o['rows']} -> "
          f"{'RED (as required)' if red1 else 'GREEN'}")

    r = child(CHILD, "refute")
    names = [c for c, _q in r["cards"]]
    ok2 = ("refuted_by" in [qq for _c, qq in r["cards"]]
           and names[-1] == "Instrument the middle")
    print(f"  A2 {r}")
    print(f"A2 a refuted card is dropped, the next by order asked: {'GREEN' if ok2 else 'RED'}")

    b = child(CHILD, "budget")
    ok3 = b["words"] == 2
    print(f"A3 the same question asked at most twice on one board ({b['words']}): "
          f"{'GREEN' if ok3 else 'RED'}")

    u = child(CHILD, "unbound")
    ok4 = bool(u["sym"]) and all(x == {"R⁺_s": "unbound"} for x in u["sym"])
    print(f"A4 an unbound symbol is written unbound {ascii(u)}: {'GREEN' if ok4 else 'RED'}")

    on = child(GW)
    off = child(GW, TETHER_AGENDA="0")
    ok5 = on[1] == "pass" and off[1] == "pass" and on[2] > 0 and off[2] == 0
    print(f"  A5 gw12 ON {on}, OFF {off}")
    print(f"A5 gridworld runs pass the gate both ways: {'GREEN' if ok5 else 'RED'}")
    assert ok1 and red1 and ok2 and ok3 and ok4 and ok5
    print("agenda: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
