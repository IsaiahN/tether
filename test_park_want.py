"""TETHER_PARK_WANT (the reviewer 2026-10-12 08:43, 08:52 CDT): when nothing in a mint paid, the
park return now writes the unpaid objective want the mint ranked, through the tail's own writer.

  p1 MUST-PASS, arm ON: the pinned park row carries want, want_paid False, want_seen and
     bound_at_park, and agent.wants[slot] equals the want.
  p2 MUST-FAIL, arm OFF: the same mint parks with `wanted` set (read off _mint's locals at return)
     and writes no want; the row has no bound_at_park.
  p3 every park return that is under_floor or no_support has `wanted` None, and no such row
     carries a want, under both arms.
  p4 the rows before the pinned park are identical ON and OFF (the tail path is unchanged); the
     arms row differs by tether._PARK_WANT alone.
  p5 MUST-FAIL MUTANT: the helper's effect deferred until after the park row is recorded -> the
     row lacks the want, and p1's row assertion catches it.

    python test_park_want.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

# Found by search under default arms (every _mint return read by setprofile): on gridworld_s1 the
# first mint that parks with `wanted` set is o5.distance in cycle 5 (priced_out_at_depth, seen 1,
# no bound term). Six steps reach it.
MEMBER, SLOT, CYCLE, STEPS = "gridworld_s1", "o5.distance", 5, 6

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
import gamma, ledger, tether, world
from conform import panel
MEMBER, STEPS, MODE = sys.argv[1], int(sys.argv[2]), sys.argv[3]
tether._PARK_WANT = MODE != "off"
g, seed = panel._gridworld(MEMBER)
env = world.bind(g)
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"t_{seed}"), tether.Config(), ledger.Ledger())
if MODE == "mutant":
    orig_retain, orig_record, pending = tether.Agent._retain_unpaid_want, ag.led.record, []
    def deferred(self, slot, wanted, detail):
        pending.append((slot, wanted, detail))
    def record(*a, **k):
        e = orig_record(*a, **k)
        while pending:
            orig_retain(ag, *pending.pop())
        return e
    tether.Agent._retain_unpaid_want, ag.led.record = deferred, record
CODE = tether.Agent._mint.__code__
parks = []
def prof(frame, event, arg):
    if event == "return" and frame.f_code is CODE and frame.f_locals.get("best") is None:
        L = frame.f_locals
        parks.append({"cycle": L["self"].cycle, "slot": L["slot"],
                      "wanted": None if L["wanted"] is None else L["wanted"][1].name})
sys.setprofile(prof)
for _ in range(STEPS):
    ag.step()
sys.setprofile(None)
rows = ag.led.rows()
print(json.dumps({"parks": parks, "rows": rows, "wants": dict(ag.wants)}, default=str))
'''


def _run(mode: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run([sys.executable, "-c", PROBE, MEMBER, str(STEPS), mode], cwd=here, env=env,
                         capture_output=True, text=True, timeout=900)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _park_row(run: dict) -> tuple[int, dict]:
    hit = [(i, r) for i, r in enumerate(run["rows"]) if r["step"] == "MINT" and r["event"] == "park"
           and r["slot"] == SLOT and r["cycle"] == CYCLE]
    assert len(hit) == 1, f"pinned park row not found ({len(hit)}): re-run the search"
    return hit[0]


def _p1(run: dict) -> str | None:
    _i, row = _park_row(run)
    d = row["detail"]
    if not d.get("want") or d.get("want_paid") is not False or not d.get("want_seen"):
        return f"park row lacks the want: {sorted(d)}"
    if "bound_at_park" not in d:
        return "park row lacks bound_at_park"
    if run["wants"].get(SLOT) != d["want"]:
        return f"wants[{SLOT}] {run['wants'].get(SLOT)!r} != row want {d['want']!r}"
    return None


def _p3(run: dict) -> None:
    for r in run["rows"]:
        if r["step"] == "MINT" and r["event"] == "park" and \
                r["detail"].get("verdict") in ("under_floor", "no_support"):
            assert "want" not in r["detail"], f"{r['detail']['verdict']} park row carries a want"
    verdicts = {(r["cycle"], r["slot"]): r["detail"].get("verdict") for r in run["rows"]
                if r["step"] == "MINT" and r["event"] == "park"}
    n = 0
    for p in run["parks"]:
        if verdicts.get((p["cycle"], p["slot"])) in ("under_floor", "no_support"):
            n += 1
            assert p["wanted"] is None, f"wanted set on a {verdicts[(p['cycle'], p['slot'])]} park"
    assert n, "no under_floor/no_support park in the window: p3 examined nothing"


def main() -> None:
    on, off, mut = _run("on"), _run("off"), _run("mutant")

    err = _p1(on)
    assert err is None, f"p1 ON: {err}"
    i_on, row_on = _park_row(on)

    i_off, row_off = _park_row(off)
    p = [x for x in off["parks"] if x["cycle"] == CYCLE and x["slot"] == SLOT]
    assert p and p[-1]["wanted"], "p2: the pinned mint no longer parks with `wanted` set"
    assert _p1(off) is not None and "want" not in row_off["detail"] \
        and "bound_at_park" not in row_off["detail"], "p2 MUST-FAIL: OFF wrote a want on the park"

    _p3(on)
    _p3(off)

    a_on, a_off = on["rows"][0]["detail"], off["rows"][0]["detail"]
    assert on["rows"][0]["event"] == "arms" and \
        set(a_on["on"]) ^ set(a_off["on"]) == {"tether._PARK_WANT"}, \
        "p4: arms rows differ beyond the arm"
    assert i_on == i_off and on["rows"][1:i_on] == off["rows"][1:i_off], \
        "p4: rows before the pinned park differ ON vs OFF"

    assert _p1(mut) is not None, "p5 MUST-FAIL: the deferred-write mutant passed p1"
    assert mut["wants"].get(SLOT) == row_on["detail"]["want"], \
        "p5: the mutant did not write the want at all, so it tests nothing"

    print(f"p1 ON park row {SLOT}@c{CYCLE} want {row_on['detail']['want']!r} seen "
          f"{row_on['detail']['want_seen']} bound_at_park {row_on['detail']['bound_at_park']}; "
          f"p2 OFF no want (wanted {p[-1]['wanted']!r}); p3 under_floor/no_support wanted None "
          f"both arms; p4 {i_on} rows before identical; p5 row-order mutant caught")


if __name__ == "__main__":
    main()
