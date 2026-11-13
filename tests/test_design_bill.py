"""THE DESIGN BILL (TETHER_MINT_READ_CHARGED, TETHER_REACH_FIRST; the reviewer 2026-11-13; Isaiah
00:10 "The trip back to the walk is apart of the design", 00:18 the "is this possible?" check moves
ahead of design; WATSON_2026-11-13_the_walkthrough_and_the_design_bill).

DB1  reach first: a slot out of reach is gated BEFORE the contact read -- the contact read never
     runs, the reach_gate row is written, and nothing is charged to MINT
MF-DB1 the plant: TETHER_REACH_FIRST=0 -> the contact read runs before the gate -> RED
DB2  charged: heads spent inside the contact read land on MINT's clock, not the enclosing idle
     scope's
MF-DB2 the plant: TETHER_MINT_READ_CHARGED=0 -> MINT's clock reads 0 for them -> RED
DB3  the novice/expert reading: two design reads of the same kind write design_read rows with
     sighting 0, then 1, and the heads each spent
DB4  both arms OFF: no design_read row is written (the r1871 path; the commit's gw12 identity
     against development is the seat's check)
Seconds.

    python tests/test_design_bill.py
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
import cap, gamma, gridworld, ledger, tether, world
mode = sys.argv[1]
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
ag.step()
slot = next(s for s in sorted(ag.slot_types) if s.endswith(".row"))
ag._try_first_hold = lambda: False
ag._sm = None
calls = []
def contact(s, n=10):
    calls.append(s)
    for _ in range(n):
        cap.head()
    return ("fp",)
ag._contact_fp = contact
ag._cf_rows[slot] = ("fp",)           # the same rows: contact_first owes, nothing is minted
ag._clk_stack, ag._clk_hs, ag._clk, ag._clk_h = [], [], {}, {}
if mode == "gated":
    ag._out_of_reach = lambda s: True
    with ag._step_scope("ACCEPT"):
        ag._mint_in_step(slot, "b")
else:
    ag._out_of_reach = lambda s: False
    for _ in range(2 if mode == "twice" else 1):
        with ag._step_scope("ACCEPT"):
            ag._mint_in_step(slot, "b")
rows = [r for r in led.rows() if r.get("slot") == slot and r.get("event") in
        ("reach_gate", "design_read", "contact_first")]
dr = [(r["detail"].get("what"), r["detail"].get("sighting"), r["detail"].get("heads"))
      for r in rows if r["event"] == "design_read"]
print(repr((len(calls), ag._clk_h.get("MINT", 0), ag._clk_h.get("ACCEPT", 0),
            [r["event"] for r in rows], dr)))
'''


def child(mode: str, **arms: str):
    env = {**os.environ, "TETHER_AGENT_SEED": "0", "PYTHONIOENCODING": "utf-8", **arms}
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, mode], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=600,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return eval(p.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


def main() -> int:
    n, mint_h, _acc, evs, _dr = child("gated")
    ok1 = n == 0 and "reach_gate" in evs and mint_h == 0
    print(f"  DB1 contact reads {n}; MINT heads {mint_h}; rows {evs}")
    print(f"DB1 an impossible job stops before design: {'GREEN' if ok1 else 'RED'}")
    pn, _m, _a, pevs, _d = child("gated", TETHER_REACH_FIRST="0")
    red1 = pn > 0
    print(f"MF-DB1 reach after the contact read: contact reads {pn}, rows {pevs} -> "
          f"{'RED (as required)' if red1 else 'GREEN'}")
    n2, mint2, acc2, _e, _d2 = child("once")
    ok2 = n2 == 1 and mint2 >= 10
    print(f"  DB2 MINT heads {mint2}; ACCEPT heads {acc2}")
    print(f"DB2 the trip back to the wall is charged to design: {'GREEN' if ok2 else 'RED'}")
    _n, pmint, pacc, _e2, _d3 = child("once", TETHER_MINT_READ_CHARGED="0")
    red2 = pmint < 10
    print(f"MF-DB2 label only: MINT heads {pmint}, ACCEPT heads {pacc} -> "
          f"{'RED (as required)' if red2 else 'GREEN'}")
    _n3, _m3, _a3, _e3, dr = child("twice")
    sights = [s for w, s, _h in dr if w == "contact"]
    ok3 = sights == [0, 1] and all(h >= 10 for w, _s, h in dr if w == "contact")
    print(f"  DB3 design_read rows {dr}")
    print(f"DB3 first sighting then a later one, with heads: {'GREEN' if ok3 else 'RED'}")
    _n4, _m4, _a4, e4, d4 = child("twice", TETHER_MINT_READ_CHARGED="0", TETHER_REACH_FIRST="0")
    ok4 = not d4 and "design_read" not in e4
    print(f"DB4 both arms OFF write no design_read row: {'GREEN' if ok4 else 'RED'}")
    assert ok1 and red1 and ok2 and red2 and ok3 and ok4
    print("design_bill: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
