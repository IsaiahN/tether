"""ALPHA-PRICE, F2 (the reviewer 2026-10-20 13:38 CDT): a correct prediction of a value the slot
has never shown costs 0 bits. Game-free: a gridworld whose one slot climbs to a new value every
step, its alphabet growing to just hold it, and whose prediction for that slot is right (the raw
next value, coded as _predict codes it, T:6800). Each arm in its own process (the flag resolves
at import).

  P1 MUST-PASS (arm ON): every bet on the slot costs 0 bits; its code is the raw prediction under
     the row's alphabet; no SETTLE row on the slot names a miss; gate check 13 passes on the run.
  P2 MUST-FAIL (arm OFF, today's coding): the same bets are charged log2(alphabet) and gate check
     13 turns red on the run ("predicted ... coded ... under ...").

    python test_alpha_price.py
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys

sys.dont_write_bytecode = True

SLOT = "o4.row"
STEPS = 4

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, slot, steps = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path = [tree] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
import gamma, gate, gridworld, ledger, tether, world

class Grow(gridworld.GridWorld):
    """One slot reads 100 + steps taken; its alphabet holds exactly the values shown so far."""
    def observe(self):
        o = super().observe()
        o[slot] = 100 + self._steps
        return o
    def alphabet(self):
        a = super().alphabet()
        a = dict(a) if isinstance(a, dict) else dict.fromkeys(self.slots(), int(a))
        a[slot] = 100 + self._steps + 1
        return a

g = gridworld.family("default", 0)
g.__class__ = Grow
env = world.bind(g)
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="alpha_price"), tether.Config(),
                  ledger.Ledger())
real = ag._predict

def right(s, state, action):
    if s != slot:
        return real(s, state, action)
    ag._pred_raw[s] = state[s] + 1          # the next value, never shown before
    return ag._pred_raw[s] % ag.alphabet[s]  # coded as _predict codes it (T:6800)

ag._predict = right
for _ in range(steps):
    ag.step()
rows = ag.led.rows()
bets = [r for r in rows if r.get("event") == "bet" and r.get("slot") == slot]
settle = [[r["cycle"], r["event"]] for r in rows
          if r.get("step") == "SETTLE" and r.get("slot") == slot]
v = gate._aliasing(rows)
print(json.dumps({"arm": tether._ALPHA_PRICE, "bets": [r["detail"] for r in bets], "settle": settle,
                  "gate13": v}, default=str))
'''


def _run(arm: str) -> dict:
    here = os.path.dirname(os.path.abspath(__file__))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_ALPHA_PRICE=arm, TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-c", PROBE, here, SLOT, str(STEPS)], env=env,
                         capture_output=True, text=True, timeout=600)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    on, off = _run("1"), _run("0")
    assert on["arm"] is True and off["arm"] is False, (on["arm"], off["arm"])
    assert len(on["bets"]) == STEPS and len(off["bets"]) == STEPS, \
        (len(on["bets"]), len(off["bets"]))
    # P1
    for d in on["bets"]:
        assert d["actual"] == d["predicted"], d
        assert d["mass"] == 0.0, d
        assert d["predicted_code"] == d["predicted"] % d["alphabet"], d
    misses = [s for s in on["settle"] if "miss" in s[1] or "refut" in s[1]]
    assert not misses, misses
    assert on["gate13"] is None, on["gate13"]
    # P2
    for d in off["bets"]:
        assert d["actual"] == d["predicted"], d
        assert abs(d["mass"] - math.log2(d["alphabet"])) < 1e-9, d
    assert off["gate13"] is not None and "coded" in str(off["gate13"]), off["gate13"]
    off_miss = [s for s in off["settle"] if "miss" in s[1] or "refut" in s[1]]
    print(f"test_alpha_price: pass (ON: {STEPS} correct bets on {SLOT} at 0 bits, settle rows "
          f"{on['settle']}, gate 13 passes; OFF: charged "
          f"{[round(d['mass'], 2) for d in off['bets']]} bits, settle miss rows {off_miss}, "
          f"gate 13 red)")


if __name__ == "__main__":
    main()
