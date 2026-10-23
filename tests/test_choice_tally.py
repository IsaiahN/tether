"""THE CHOICE TALLY (TETHER_CHOICE_TALLY, default ON; TETHER_CHOICE_TALLY_CHECK; Isaiah 2026-10-23
09:12 "these should be deduped and tallied"; the reviewer 09:13, 10:40). Each arm state in its own
process (arms resolve at import).
  U    the ledger alone: a key's first objective_domain choice row is appended, its repeats are not;
       flush_tally writes one choice_tally row per repeated key (ref, n, first and last cycle);
       `written` counts both; since_written returns both in call order; OFF appends every row
  P    THE PLANT (as test_fit_dedup's rows plant): gridworld_arc_s1, 15 steps, an objective_domain
       choice row recorded inside every _left call (so the fit's dedup captures and replays them):
       ON, OFF and CHECK give the same acting rows, and the same count per key (OFF: its rows; ON:
       1 + the tally rows' n); every other row equal (seq masked); CHECK never fires
  MF1  CHECK with a deliberately wrong n (+1 before the flush) raises
  MF2  CHECK with a tally key that drops "frontier" (a decision field) raises: two rows that differ
       in it were merged
    python tests/test_choice_tally.py
"""
from __future__ import annotations

import collections
import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, mode = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, panel, tether, world

def row(led, cyc, slot, fr, pick="1"):
    led.record(cyc, "PERCEIVE", slot, "choice", site="objective_domain", options=2,
               frontier=fr, residual=None, seen=None, pick=pick, by="learning")

if mode in ("unit", "mf1", "mf2"):
    if mode == "mf2":
        ledger.TALLY_FIELDS = tuple(f for f in ledger.TALLY_FIELDS if f != "frontier")
    led = ledger.Ledger()
    row(led, 0, "o1.x", [["'2'", 0.0, 2]])
    row(led, 0, "o1.x", [["'2'", 0.0, 2]])
    w_mid = led.written
    row(led, 1, "o1.x", [["'2'", 0.0, 2]] if mode != "mf2" else [["'5'", 1.0, 5]])
    row(led, 1, "o2.y", [["'3'", 0.0, 3]])
    led.record(1, "ROUTE", "o1.x", "other", a=1)
    since = [(r["slot"], r["event"]) for r in led.since_written(w_mid)]
    if mode == "mf1":
        next(iter(led._tstep.values()))[1] += 1
    try:
        led.flush_tally(1)
        err = None
    except AssertionError as e:
        err = str(e)[:200]
    print(json.dumps({"on": ledger._CHOICE_TALLY, "entries": len(led), "written": led.written,
                      "since": since, "err": err,
                      "rows": [(r["slot"], r["event"], r["detail"]) for r in led.rows()]}))
    raise SystemExit

_left_ = tether.Agent._left
def _left_w(self, term, slot, hist, *a, **k):
    row(self.led, self.cycle, slot, [[repr(len(hist) % 3), 0.0, 1]])
    return _left_(self, term, slot, hist, *a, **k)
tether.Agent._left = _left_w
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="tally"), tether.Config(), ledger.Ledger())
for _ in range(15):
    ag.step()
print(json.dumps({"on": ledger._CHOICE_TALLY, "check": ledger._CHOICE_TALLY_CHECK,
                  "rows": ag.led.rows()}, default=str))
'''


def child(mode: str, **arms: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0", **arms)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, str(_repo.ROOT), mode], env=env,
                         capture_output=True, text=True, timeout=900, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def key(r: dict) -> str:
    return json.dumps([r["slot"], r["step"], r["detail"]], sort_keys=True)


def per_key(rows: list) -> collections.Counter:
    """Each objective_domain key's count: its rows, plus the tally rows' n against their ref."""
    by_seq = {r["seq"]: r for r in rows}
    c: collections.Counter = collections.Counter()
    for r in rows:
        if r["event"] == "choice" and r["detail"].get("site") == "objective_domain":
            c[key(r)] += 1
        elif r["event"] == "choice_tally":
            c[key(by_seq[r["detail"]["ref"]])] += r["detail"]["n"]
    return c


def rest(rows: list) -> list:
    return [(r["cycle"], r["step"], r["slot"], r["event"], json.dumps(r["detail"], sort_keys=True))
            for r in rows if r["event"] not in ("choice_tally", "arms")
            and not (r["event"] == "choice" and r["detail"].get("site") == "objective_domain")]


def acting(rows: list) -> list:
    return [(r["cycle"], r["detail"].get("action"), r["detail"].get("by")) for r in rows
            if r["slot"] == "@loop" and r["event"] == "repeat"]


def main() -> None:
    u = child("unit", TETHER_CHOICE_TALLY="1")
    assert u["on"] and (u["entries"], u["written"]) == (5, 6), ("U counts", u)
    tal = [d for s, e, d in u["rows"] if e == "choice_tally"]
    assert len(tal) == 1 and tal[0]["n"] == 2 and tal[0]["ref"] == 0, ("U tally", tal)
    assert u["since"] == [["o1.x", "choice"], ["o2.y", "choice"], ["o1.x", "other"]], u["since"]
    o = child("unit", TETHER_CHOICE_TALLY="0")
    assert not o["on"] and (o["entries"], o["written"]) == (5, 5), ("U OFF", o)
    print(f"  U: ON 5 entries of 6 calls, one tally row n 2; since_written in call order; "
          f"OFF {o['entries']} entries")
    m1 = child("mf1", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_CHECK="1")
    assert m1["err"] and "CHOICE_TALLY CHECK" in m1["err"], ("MF1", m1)
    m2 = child("mf2", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_CHECK="1")
    assert m2["err"] and "CHOICE_TALLY CHECK" in m2["err"], ("MF2", m2)
    c0 = child("unit", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_CHECK="1")
    assert c0["err"] is None, ("CHECK clean", c0)
    print("  MF1 (n + 1) and MF2 (a key without frontier) raise under CHECK; the clean case does "
          "not")
    on = child("plant", TETHER_CHOICE_TALLY="1")
    off = child("plant", TETHER_CHOICE_TALLY="0")
    ck = child("plant", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_CHECK="1")
    n_off = sum(1 for r in off["rows"] if r["event"] == "choice"
                and r["detail"].get("site") == "objective_domain")
    assert n_off > 50, ("P: precondition, too few planted rows", n_off)
    assert acting(on["rows"]) == acting(off["rows"]) == acting(ck["rows"]), "P: acting rows"
    assert per_key(on["rows"]) == per_key(off["rows"]) == per_key(ck["rows"]), "P: per-key counts"
    assert rest(on["rows"]) == rest(off["rows"]) == rest(ck["rows"]), "P: the other rows"
    print(f"  P: {n_off} planted rows OFF -> {len(on['rows'])} rows ON of {len(off['rows'])}; "
          f"{len(per_key(off['rows']))} keys, the same count per key; acting rows equal; CHECK "
          "clean")
    print("choice_tally: OK")


if __name__ == "__main__":
    main()
