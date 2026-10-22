"""L1, THE NORMALIZED CODE, TETHER_PRIOR_CODE (the reviewer 2026-10-17 18:13 (a), 18:40).

  KRAFT  the fake ARC game, 12 actions, C-seed-X, the arm ON: at every step the 2^-cost over the
         units plus END sums to 1 (<= 1 is the ruled bound)
  NOLIB  no library and nothing learned: every unit and END cost log2(A + 1), so a term costs
         term_bits(k, A) -- the code IS today's uniform code
  OFF    the arm OFF: every park row's floor is term_bits(1, A)
  ADMIT  the first under_floor park on the fake (base b): the weight w* the code needs for one
         unit to bring the floor under b is SOLVED from that moment's code, planted through
         Rank.note (the one writer), and the same slot's re-mint is no longer under_floor
  MF-W   w* - 1 planted: the re-mint still parks under_floor
  MF-0   nothing planted: the re-mint still parks under_floor

    python tests/test_prior_code.py
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT

CHILD = r'''
import json, math, os, sys, tempfile
sys.dont_write_bytecode = True
import arc_holdout, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
plant, unit = int(sys.argv[1]), sys.argv[2]
led = os.path.join(tempfile.mkdtemp(), "p.jsonl")
env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", led_path=led)
kraft, park = [], None
for _ in range(12):
    env.observe()
    ag.step()
    if tether.G_PRIOR_CODE:
        kraft.append(ag.gamma.code().kraft())
    rows = [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()]
    uf = [r for r in rows if r["event"] == "park" and r["detail"].get("verdict") == "under_floor"]
    if uf and park is None:
        park = uf[0]
        if plant >= 0:
            break
    if env.terminal():
        break
out = {"kraft": kraft, "A": ag.gamma.alphabet,
       "floors": sorted({r["detail"]["floor_bits"] for r in rows if r["event"] == "park"
                         and r["detail"].get("floor_bits") is not None})}
if park is not None and plant >= 0:
    slot, b = park["slot"], park["detail"]["base_bits"]
    c = ag.gamma.code()
    assert unit in ag.gamma.library, unit
    z, end_w = c.info["z"], c.info["end_w"]
    wu = z * 2 ** -c.cost[ag.gamma.library[unit].atoms] - 1
    top = max(z * 2 ** -v for v in c.cost.values())       # the heaviest unit's (w + 1)
    def floor(d):
        zz = z + d
        return math.log2(zz / max(wu + 1 + d, top)) + math.log2(zz / end_w)
    need = next(d for d in range(1, 10 ** 7) if floor(d) < b)
    give = {"need": need, "need-1": need - 1, "zero": 0}[sys.argv[3]]
    for _ in range(give):
        ag.rank.note(unit, ag.cycle)
    n0 = len(ag.led)
    ag._mint(slot)
    after = [r for r in ag.led.rows(n0) if r["slot"] == slot and r["step"] == "MINT"
             and r["event"] in ("park", "mint")]
    out.update({"slot": slot, "base": b, "need": need, "gave": give,
                "floor_now": round(ag.gamma.code().floor, 3),
                "after": [(r["event"], r["detail"].get("verdict")) for r in after]})
print("RESULT", json.dumps(out))
'''


def child(plant: int, mode: str = "need", unit: str = "translate", arm: str = "1") -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "TETHER_PRIOR_CODE": arm})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, str(plant), unit, mode],
                       capture_output=True, text=True, env=env, cwd=HERE,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    line = next(x for x in p.stdout.splitlines() if x.startswith("RESULT "))
    return json.loads(line[len("RESULT "):])


def nolib() -> None:
    sys.path.insert(0, HERE)
    import arc_atoms
    import arc_predict
    import arc_world  # noqa: F401  -- its observer arm publishes contact / bbox / inside
    import gamma
    import inherited
    import tether
    g = gamma.Gamma(arc_atoms.three_spaces(arc_predict.predict()), game="nolib")
    real = inherited.recipe_length
    inherited.recipe_length = lambda: None
    try:
        c = g._code_built(g.units_held())
    finally:
        inherited.recipe_length = real
    a = g.alphabet
    u = math.log2(a + 1)
    assert all(abs(v - u) < 1e-9 for v in c.cost.values()) and abs(c.end - u) < 1e-9, "NOLIB"
    t = gamma.Term(tuple(g.atoms[:3]))
    b, k = c.bits((t, ()))
    assert abs(b - tether.term_bits(k, a)) < 1e-9 and abs(c.floor - tether.term_bits(1, a)) < 1e-9
    print("NOLIB no library, nothing learned: every unit and END cost log2(", a, "+ 1) =",
          round(u, 3), "; a 3-atom term", round(b, 3), "= term_bits(3,", a, ")")


def main() -> int:
    on = child(-1)
    k = on["kraft"]
    assert k and all(x <= 1 + 1e-9 for x in k), k                                          # KRAFT
    print("KRAFT", len(k), "steps, the sum over units plus END: min", round(min(k), 12), "max",
          round(max(k), 12), "; A =", on["A"], "; floors", on["floors"])
    nolib()                                                                                 # NOLIB
    off = child(-1, arm="0")
    want = round((1 + 1) * math.log2(off["A"] + 1), 3)
    assert off["floors"] == [want], (off["floors"], want)                                   # OFF
    print("OFF the arm off: every park floor is term_bits(1, A) =", want)
    ad = child(0, "need")
    assert ad["after"] and all(v != "under_floor" for _, v in ad["after"]), ad              # ADMIT
    print("ADMIT", ad["slot"], "base", ad["base"], ": w* =", ad["need"], "notes on translate "
          "(solved from the code) -> floor", ad["floor_now"], "; re-mint", ad["after"])
    mw = child(0, "need-1")
    assert mw["after"] and all(v == "under_floor" for _, v in mw["after"]), mw              # MF-W
    print("MF-W w* - 1 =", mw["gave"], "-> floor", mw["floor_now"], "; re-mint", mw["after"])
    m0 = child(0, "zero")
    assert m0["after"] and all(v == "under_floor" for _, v in m0["after"]), m0              # MF-0
    print("MF-0 nothing planted -> floor", m0["floor_now"], "; re-mint", m0["after"])
    print("prior_code: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
