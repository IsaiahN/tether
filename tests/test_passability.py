"""WALLS READABLE (TETHER_PASSABILITY; BUILD_SEQUENCE 1a, hand-test finding f; r1948/r1949). A
passability reading earned from contact, per colour: blocked (B4's partner) and entered (a credited
move onto an object); a route whose predicted step lands on a blocking colour is not offered.

P1  verdicts: blocked only -> blocking; then entered (a door that opened) -> mixed, not blocking
P2  the filter: the body beside an object of a blocking colour; the press stepping onto it is not
    offered, the other is; a pass_refused row names it
MF-P2 the plant: the reading removed (no contact) -> the press into the wall is offered -> RED
P3  B4 feeds it: a blocked press into a partner records a blocked contact with the partner's colour
MF-P3 the plant: TETHER_PASSABILITY=0 -> nothing recorded -> RED
P4  entered: a credited move onto an object records an entered contact with its colour
P5  gridworld 12 steps, the arm ON vs OFF: both complete and pass the gate (the OFF identity
    against development is the batch's check)
Seconds.

    python tests/test_passability.py
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
import gamma, gridworld, ledger, tether, world
mode = sys.argv[1]
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
ag.step()
ag._pass_contact = {}
W, C = 7, 8                                   # the wall's colour, another colour
base = {"o0.row": 5, "o0.col": 5, "o0.colour": 1, "o1.row": 9, "o1.col": 9, "o1.colour": C,
        "o2.row": 5, "o2.col": 6, "o2.colour": W}
rows = lambda ev: [r["detail"] for r in led.rows() if r.get("event") == ev]
out = {}
if mode == "verdict":
    ag._pass_note(W, 1, "o0", "o2", "A")
    out["after_block"] = ag._pass_verdict(W)
    ag._pass_note(W, 0, "o0", "o2", "A")
    out["after_enter"] = ag._pass_verdict(W)
    out["unknown"] = ag._pass_verdict(99)
    out["rows"] = [(d["was"], d["verdict"]) for d in rows("passability")]
elif mode in ("filter", "filter_plant"):
    a, b = ag.actions[0], ag.actions[1]
    ag.iface.table = {a: {"delta": {((), "o0.col", "self"): (2, 2)}},
                      b: {"delta": {((), "o0.col", "self"): (2, -2)}}}
    if mode == "filter":
        ag._pass_contact = {W: [0, 1]}
    out["offer"] = list(ag._pass_filter("o0.row", (a, b), dict(base)))
    out["a"], out["b"] = a, b
    out["refused"] = rows("pass_refused")
elif mode == "blocked":
    derived = {"o0.touches_o2": ("o0.row", "o0.col", "o2.row", "o2.col")}
    before = dict(base, **{"o0.touches_o2": 1})
    pred = dict(before, **{"o0.col": 6})
    ag._blocked_reading(derived, pred, before, dict(before), "A")
    out["contact"] = {repr(k): v for k, v in ag._pass_contact.items()}
    out["blocked_rows"] = len(rows("blocked"))
elif mode == "entered":
    ag.iface.last_changed = {"o0.col"}
    before = dict(base, **{"o1.row": 5, "o1.col": 6, "o2.row": 0, "o2.col": 0})
    after = dict(before, **{"o0.col": 6})
    ag._entered_reading(before, after, "A")
    out["contact"] = {repr(k): v for k, v in ag._pass_contact.items()}
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
            sum(1 for r in rows if r.get("event") in ("passability", "pass_refused")))))
'''


def child(code: str, *args: str, **arms: str):
    env = {**os.environ, "TETHER_AGENT_SEED": "0", "PYTHONIOENCODING": "utf-8", **arms}
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=900,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return eval(p.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


def main() -> int:
    v = child(CHILD, "verdict")
    ok1 = (v["after_block"] == "blocking" and v["after_enter"] == "mixed"
           and v["unknown"] == "unknown"
           and v["rows"] == [("unknown", "blocking"), ("blocking", "mixed")])
    print(f"  P1 {v}")
    print(f"P1 blocked -> blocking, then entered -> mixed: {'GREEN' if ok1 else 'RED'}")

    f = child(CHILD, "filter")
    ok2 = (f["offer"] == [f["b"]] and len(f["refused"]) == 1
           and f["refused"][0]["refused"][0][0] == f["a"])
    print(f"  P2 {f}")
    print(f"P2 the press onto the blocking colour is not offered: {'GREEN' if ok2 else 'RED'}")
    p = child(CHILD, "filter_plant")
    red2 = f["a"] in p["offer"]
    print(f"MF-P2 the reading removed: offer {p['offer']} -> "
          f"{'RED (as required)' if red2 else 'GREEN'}")

    b = child(CHILD, "blocked")
    ok3 = b["blocked_rows"] == 1 and b["contact"] == {"7": [0, 1]}
    print(f"P3 a blocked press records the partner's colour {b}: {'GREEN' if ok3 else 'RED'}")
    bo = child(CHILD, "blocked", TETHER_PASSABILITY="0")
    red3 = bo["contact"] == {} and bo["blocked_rows"] == 1
    print(f"MF-P3 the arm OFF: contact {bo['contact']} -> "
          f"{'RED (as required)' if red3 else 'GREEN'}")

    e = child(CHILD, "entered")
    ok4 = e["contact"] == {"8": [1, 0]}
    print(f"P4 a credited move onto an object records entered {e}: {'GREEN' if ok4 else 'RED'}")

    on = child(GW)
    off = child(GW, TETHER_PASSABILITY="0")
    ok5 = on[1] == "pass" and off[1] == "pass" and off[2] == 0
    print(f"  P5 gw12 ON {on}, OFF {off}")
    print(f"P5 gridworld runs pass the gate both ways: {'GREEN' if ok5 else 'RED'}")
    assert ok1 and ok2 and red2 and ok3 and red3 and ok4 and ok5
    print("passability: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
