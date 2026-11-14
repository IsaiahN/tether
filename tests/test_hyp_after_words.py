"""NO GOAL ADOPTION WHILE WORDS IS UNMET (TETHER_HYP_AFTER_WORDS; the reviewer r1939, design (a) of
r1938). While BOARD_TRY_FIRST holds -- an offered action unpressed on this board -- the proposer's
turn is held by "try_first", rowed by proposal_gated; a goal already held is untouched.

W1  the hold on: nothing proposed, a proposal_gated row with holder "try_first"
MF-W1 the plant: TETHER_HYP_AFTER_WORDS=0 -> a goal is proposed inside the hold -> RED
W2  TETHER_BOARD_TRY_FIRST=0 (no hold, so no gate): the proposal runs (MF-W2: tied to the hold)
W3  the hold clear: the proposal runs as before
W4  a goal already held: its check runs, nothing proposed, no try_first row
W5  gridworld 12 steps, the arm ON vs OFF: both complete and pass the gate (the commit's OFF
    identity against development is the seat's check)
Seconds.

    python tests/test_hyp_after_words.py
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
proposed, checked = [], []
ag._hyp_propose = lambda before: proposed.append(1)
ag._hyp_check = lambda: checked.append(1)
ag._goal_choice = lambda *a, **k: None
ag.routine, ag._hyp_exhausted = None, None
ag.__dict__["_gated_last"] = None    # rowed once per change of holder; step() may have rowed it
ag._try_first_hold = (lambda: 0) if mode == "clear" else (lambda: 2)
ag._hyp = {"slots": ["x"]} if mode == "held" else None
st = getattr(ag.env, "state", {})
n0 = len(led.rows())
ag._goal_hypothesis_run(dict(st() if callable(st) else st))
gated = [r["detail"].get("holder") for r in led.rows()[n0:] if r.get("event") == "proposal_gated"]
print(repr({"proposed": len(proposed), "checked": len(checked), "gated": gated}))
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
            sum(1 for r in rows if r.get("event") == "proposal_gated"
                and r["detail"].get("holder") == "try_first"))))
'''


def child(code: str, *args: str, **arms: str):
    env = {**os.environ, "TETHER_AGENT_SEED": "0", "PYTHONIOENCODING": "utf-8", **arms}
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=900,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return eval(p.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


def main() -> int:
    r = child(CHILD, "hold")
    ok1 = r["proposed"] == 0 and r["gated"] == ["try_first"]
    print(f"  W1 {r}")
    print(f"W1 the hold on: nothing proposed, held by try_first: {'GREEN' if ok1 else 'RED'}")
    p = child(CHILD, "hold", TETHER_HYP_AFTER_WORDS="0")
    red1 = p["proposed"] == 1        # W1's check fails on the plant: a goal adopted in the hold
    print(f"MF-W1 the arm OFF: proposed {p['proposed']} inside the hold -> "
          f"{'RED (as required)' if red1 else 'GREEN'}")

    n = child(CHILD, "hold", TETHER_BOARD_TRY_FIRST="0")
    ok2 = n["proposed"] == 1 and "try_first" not in n["gated"]
    print(f"  W2 {n}")
    print(f"W2 no hold (BOARD_TRY_FIRST off), so no gate: {'GREEN' if ok2 else 'RED'}")

    c = child(CHILD, "clear")
    ok3 = c["proposed"] == 1 and not c["gated"]
    print(f"W3 the hold clear: proposed {c['proposed']}: {'GREEN' if ok3 else 'RED'}")

    h = child(CHILD, "held")
    ok4 = h["checked"] == 1 and h["proposed"] == 0 and not h["gated"]
    print(f"W4 a goal already held is untouched {h}: {'GREEN' if ok4 else 'RED'}")

    on = child(GW)
    off = child(GW, TETHER_HYP_AFTER_WORDS="0")
    ok5 = on[1] == "pass" and off[1] == "pass" and off[2] == 0
    print(f"  W5 gw12 ON {on}, OFF {off}")
    print(f"W5 gridworld runs pass the gate both ways: {'GREEN' if ok5 else 'RED'}")
    assert ok1 and red1 and ok2 and ok3 and ok4 and ok5
    print("hyp_after_words: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
