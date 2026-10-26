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

  Run twice (the reviewer 2026-10-26 01:04, 01:29, 01:40, ruled; red since 0996891, 10-15,
  TETHER_A1_TIES: the first press is a recorded tie draw, so the hard pin gridworld_s1 o5.distance
  c5 went stale by construction). Every child runs with TETHER_AGENT_SEED=0 (cab5bd5 made the birth
  seed the OS's; the precedent is the other tests' _AGENT_SEED = False), so the fixture is one
  fixed being, and the arms row read back shows it. Both pins are FOUND IN THE RUN by one search:
  the first park with `wanted` set (from _mint's locals) over an order of (board, steps) written
  here, by cycle, every searched board's count printed. The order is fixed before any result and
  is never widened by seed.
  ORIGINAL under TETHER_A1_TIES=0 (after the PROBE's TETHER_ strip, both arms): gridworld_s1 then
           gridworld_s0, 12 steps. At seed 0 on 8799990 it found gridworld_s0 o0.row c11.
  TWIN     under the shipped defaults: s0, s1 at 12; s0, s1 at 24; then s2, arc_s0, arc_s1, arc_s2
           at 12, then at 24. At seed 0 on 8799990 it found gridworld_s0 at 24 steps, o0.row c19
           (none on s0/s1 at 12).
  The widening read at seed 0 on 8799990 (shipped defaults; parks with wanted / parks):
    board             12 steps   24 steps
    gridworld_s0      0 / 24     5 / 57   first c19 o0.row
    gridworld_s1      0 / 14     14 / 47  first c16 o0.col
    gridworld_s2      0 / 16     18 / 47  first c13 o0.col
    gridworld_arc_s0  0 / 23     1 / 52   first c23 o0.col
    gridworld_arc_s1  0 / 23     0 / 47
    gridworld_arc_s2  0 / 18     4 / 47   first c12 o0.col
  p1-p5 then run on runs that END at the found pin (its cycle + 1 steps), as the first pin did:
  p1 reads agent.wants[slot] at the run's end, which a later park on the same slot overwrites.
  GUARD: a short run must be the search run's prefix (rows through the imported mask_timings),
  else red "the short run is not the search run's prefix: a second unpinned draw".
  OCCASION: no park with `wanted` set anywhere in an order is red as a finding (the park-want
  occasion is gone), not a stale pin. MF-OCC: the occasion check given the searched runs with no
  wants reads red with its message.
  p4 compares the rows through the imported conform/identity_mod_rows.mask_timings, and says
  whether the raw rows differed only in a timing field.

    python tests/test_park_want.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(_repo.ROOT, "conform"))
from identity_mod_rows import mask_timings  # noqa: E402  the one shared timing list

SEED = {"TETHER_AGENT_SEED": "0"}               # every child: one fixed being
ORIGINAL_ARMS = {"TETHER_A1_TIES": "0"}         # the arm state the first (hard) pin was found under
ORIGINAL_ORDER = (("gridworld_s1", 12), ("gridworld_s0", 12))
TWIN_ORDER = (tuple((m, n) for n in (12, 24) for m in ("gridworld_s0", "gridworld_s1"))
              + tuple((m, n) for n in (12, 24) for m in ("gridworld_s2", "gridworld_arc_s0",
                                                         "gridworld_arc_s1", "gridworld_arc_s2")))

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


def _run(mode: str, member: str, steps: int, arms: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **SEED, **(arms or {})})
    here = _repo.ROOT
    out = subprocess.run([sys.executable, "-c", PROBE, member, str(steps), mode], cwd=here, env=env,
                         capture_output=True, text=True, timeout=900)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _park_row(run: dict, slot: str, cycle: int) -> tuple[int, dict]:
    hit = [(i, r) for i, r in enumerate(run["rows"]) if r["step"] == "MINT" and r["event"] == "park"
           and r["slot"] == slot and r["cycle"] == cycle]
    assert len(hit) == 1, f"pinned park row not found ({len(hit)}): re-run the search"
    return hit[0]


def _p1(run: dict, slot: str, cycle: int) -> str | None:
    _i, row = _park_row(run, slot, cycle)
    d = row["detail"]
    if not d.get("want") or d.get("want_paid") is not False or not d.get("want_seen"):
        return f"park row lacks the want: {sorted(d)}"
    if "bound_at_park" not in d:
        return "park row lacks bound_at_park"
    if run["wants"].get(slot) != d["want"]:
        return f"wants[{slot}] {run['wants'].get(slot)!r} != row want {d['want']!r}"
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


def _first_wanted(label: str, searched: list) -> tuple[str, int, str, int]:
    """The pin: the first park with `wanted` set over the searched (board, steps, run), in order."""
    for member, steps, run in searched:
        w = [p for p in run["parks"] if p["wanted"]]
        if w:
            return member, steps, w[0]["slot"], w[0]["cycle"]
    raise AssertionError(f"{label}: no park with wanted set in its order: the park-want occasion "
                         f"is gone (a finding, not a stale pin)")


def _search(label: str, order: tuple, arms: dict | None) -> tuple[tuple, list]:
    """The ONE search, for both pins: the order run until a park with `wanted` set, every searched
    board's count printed."""
    searched = []
    for member, steps in order:
        run = _run("on", member, steps, arms)
        searched.append((member, steps, run))
        n = sum(1 for p in run["parks"] if p["wanted"])
        print(f"{label} search {member} {steps} steps: parks {len(run['parks'])}, with wanted {n}")
        if n:
            break
    return _first_wanted(label, searched), searched


def _check(label: str, on: dict, off: dict, mut: dict, slot: str, cycle: int,
           arms_off: tuple = ()) -> str:
    """p1-p5 at one pin; the same assertions for the ORIGINAL and the TWIN."""
    err = _p1(on, slot, cycle)
    assert err is None, f"{label} p1 ON: {err}"
    i_on, row_on = _park_row(on, slot, cycle)

    i_off, row_off = _park_row(off, slot, cycle)
    p = [x for x in off["parks"] if x["cycle"] == cycle and x["slot"] == slot]
    assert p and p[-1]["wanted"], f"{label} p2: the pinned mint no longer parks with `wanted` set"
    assert _p1(off, slot, cycle) is not None and "want" not in row_off["detail"] \
        and "bound_at_park" not in row_off["detail"], \
        f"{label} p2 MUST-FAIL: OFF wrote a want on the park"

    _p3(on)
    _p3(off)

    a_on, a_off = on["rows"][0]["detail"], off["rows"][0]["detail"]
    assert on["rows"][0]["event"] == "arms" and \
        set(a_on["on"]) ^ set(a_off["on"]) == {"tether._PARK_WANT"}, \
        f"{label} p4: arms rows differ beyond the arm"
    for a in ("tether._AGENT_SEED", *arms_off):     # the pinned seed (and the arm state) read back
        assert a in a_on.get("off", []) and a in a_off.get("off", []), f"{label}: {a} not OFF"
    raw = on["rows"][1:i_on] == off["rows"][1:i_off]
    masked = mask_timings(json.loads(json.dumps(on["rows"][1:i_on]))) == \
        mask_timings(json.loads(json.dumps(off["rows"][1:i_off])))
    assert i_on == i_off and masked, f"{label} p4: rows before the pinned park differ ON vs OFF"

    assert _p1(mut, slot, cycle) is not None, \
        f"{label} p5 MUST-FAIL: the deferred-write mutant passed p1"
    assert mut["wants"].get(slot) == row_on["detail"]["want"], \
        f"{label} p5: the mutant did not write the want at all, so it tests nothing"

    return (f"{label}: p1 ON park row {slot}@c{cycle} want {row_on['detail']['want']!r} seen "
            f"{row_on['detail']['want_seen']} bound_at_park {row_on['detail']['bound_at_park']}; "
            f"p2 OFF no want (wanted {p[-1]['wanted']!r}; OFF's p1 reads "
            f"{_p1(off, slot, cycle)[:40]!r}); p3 under_floor/no_support wanted None both arms; "
            f"p4 {i_on} rows before identical "
            f"({'raw' if raw else 'timings masked; raw differed'}); p5 row-order mutant caught")


def main() -> None:
    for label, order, arms, arms_off in (
            ("ORIGINAL (TETHER_A1_TIES=0)", ORIGINAL_ORDER, ORIGINAL_ARMS, ("tether._A1_TIES",)),
            ("TWIN (shipped defaults)", TWIN_ORDER, None, ())):
        (member, steps, slot, cycle), searched = _search(label, order, arms)
        print(f"{label} pin found: {member} {steps} steps {slot} c{cycle} (seed 0)")
        try:
            _first_wanted(label, [(m, n, {"parks": [{**p, "wanted": None} for p in r["parks"]]})
                                  for m, n, r in searched])
        except AssertionError as e:
            print(f"{label} MF-OCC no wants in the searched runs -> red: {e}")
        else:
            raise AssertionError(f"{label} MF-OCC: the occasion check passed with no want")
        # p1-p5 on runs that END at the pin (cycle + 1 steps, as the first pin's "Six steps reach
        # it" did): p1 reads agent.wants[slot] at the run's end, and a later park on the same
        # slot would overwrite it
        n = cycle + 1
        on = searched[-1][2] if n == steps else _run("on", member, n, arms)
        if on is not searched[-1][2]:       # the GUARD: the short run is the search run's prefix
            long_rows = searched[-1][2]["rows"][:len(on["rows"])]
            same = mask_timings(json.loads(json.dumps(on["rows"]))) == \
                mask_timings(json.loads(json.dumps(long_rows)))
            assert same, (f"{label}: the short run is not the search run's prefix: a second "
                          f"unpinned draw")
            how = "raw" if on["rows"] == long_rows else "timings masked; raw differed"
            print(f"{label} GUARD the {n}-step run is the search run's prefix, "
                  f"{len(on['rows'])} rows ({how})")
        print(f"{label} p1-p5 at the pin, on runs of {n} steps")
        print(_check(label, on, _run("off", member, n, arms), _run("mutant", member, n, arms),
                     slot, cycle, arms_off))


if __name__ == "__main__":
    main()
