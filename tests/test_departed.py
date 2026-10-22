"""A slot that leaves the board within a step (the reviewer 2026-10-12 22:35-22:48 CDT). Its miss is
recorded where perceive records every miss; no explanation reader -- route's bins, the library fit,
the mint, D5's pending split, settle's judgement -- acts on a slot that no longer exists. Game-free:
a gridworld whose listing changes after cycle 1, so the run-level NOVEL test cannot shield the mint.

  case 0  a slot listed from the start leaves in the FIRST step (cycle 0). The behaviour change the
          fix makes there: the pin sorts it NOVEL (the run-level test shields every reader), this
          tree writes the not-sorted row. Neither crashes; the must-fail is the pin's NOVEL row.
  case 1  a slot listed for one step only (no history, unbound) leaves
  case 2  a slot listed from the start (two transitions of history) leaves
  case 3  as 2, bound and with a refusal filed the step before it leaves (constructed state)
  case 4  as 2, bound and with a D5 split pending the step before it leaves (constructed; D5 only).
          P is made to hold on the departing step, so _d5_select keeps the binding and the bet has
          a maker (a not-P step pops it, and settle would have nothing to name). On a tree without
          the fix, route runs before _d5_splits, so this case fails at door 2 first; door 4 itself
          is proven by the d5-open mutant.
  case 5  settle's D5 shadow check on a departed slot (constructed, settle called directly: on a
          tree without the fix every full step fails in route before settle; D5 only)

  Each, on this tree: the step runs; the bet row is charged (vanished, log2 of its bet alphabet)
  and outstanding grows by it; the slot's one ROUTE row says it was not sorted; no MINT, ACCEPT,
  library or judging row lands on it (case 4: one d5_split_not_run row; case 3: the refusal is
  named on the route row and settle says not_judged); nothing stale is left in _refuted_slot,
  _shadow, _d5_candidates or _d5_pending; speak names the reason, never "None".
  MUST-FAIL: every case raises on a tree without the fix (argv[1], the pin worktree); the line that
  raised is read from the traceback and reported (case 5 must fail in settle).
  MUTANTS: settle left open (case 3 must catch it); _d5_splits left open (case 4 must catch it).

  The record's readers of a departure (the reviewer 2026-10-12 23:30), against a tree at 2092625
  (argv[3]), constructed and called directly, arm-free:
  case 6   _characterise describes a departed slot's effect as "gone" (2092625: "exact")
  case 7a  a park bet, then an unbound departure and nothing else: no reading, settled_by names
           the departure (2092625: no reading, "no change after the park")
  case 7b  a park bet, then a departure from a term that predicted a change: no reading
           (2092625: graded wrong on the departure)
  case 7c  a park bet, a real change, then an unbound departure: graded on the real change, the
           same on both trees
  case 7d  as 7c with the departure from a term that predicted a change: graded on the real change
           (2092625: graded wrong on the departure)

    python tests/test_departed.py <tree-without-the-fix> [all-on env file] [tree at 2092625]

The ALL-ON half runs only when the env file is given, and the output says which halves ran.
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

APPEAR, LEAVE, K = "o3.col", "o4.row", 3

PROBE = r'''
import dataclasses, json, sys, traceback
sys.dont_write_bytecode = True
tree, case, mutant = sys.argv[1], int(sys.argv[2]), sys.argv[3]
sys.path = [tree] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
import gamma, gridworld, ledger, tether, world
APPEAR, LEAVE, K = @CONST@
slot = APPEAR if case == 1 else LEAVE

class Departs(gridworld.GridWorld):
    def _listed(self, s):
        if s == APPEAR and case == 1:
            return self._steps == K
        if s == LEAVE and case != 1:
            return self._steps < (1 if case == 0 else K)
        return True
    def slots(self):
        return [s for s in super().slots() if self._listed(s)]
    def alphabet(self):
        a = super().alphabet()
        return {k: v for k, v in a.items() if self._listed(k)} if isinstance(a, dict) else a
    def observe(self):
        return {k: v for k, v in super().observe().items() if self._listed(k)}

g = gridworld.family("default", 0)
g.__class__ = Departs
env = world.bind(g)
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="departed"), tether.Config(), ledger.Ledger())
if mutant == "settle":
    _s = ag.settle
    ag.settle = lambda res: _s({k: dataclasses.replace(r, gone=False) for k, r in res.items()})
if mutant == "d5":
    _d = ag._d5_splits
    ag._d5_splits = lambda gone=frozenset(): _d()
err, out_before, out_after, dep, site = None, None, None, None, None


def _site(e):
    frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename.endswith("tether.py")]
    return f"{frames[-1].name}:{frames[-1].lineno}" if frames else None


if case == 5:
    for _i in range(K - 1):
        ag.step()
    ag._shadow[slot] = 0
    ag.alphabet = {k: v for k, v in ag.alphabet.items() if k != slot}
    try:
        r5 = tether.SlotResidual(slot, tether.TRANSITION, 0, 0, 1.0, True)
    except TypeError:
        r5 = tether.SlotResidual(slot, tether.TRANSITION, 0, 0, 1.0)
    try:
        ag.settle({slot: r5})
    except Exception as e:
        err, site = repr(e)[:300], _site(e)
    print(json.dumps({"err": err, "site": site, "d5": getattr(tether, "_D5", None),
                      "stale": {k: slot in getattr(ag, k, {}) for k in
                                ("_refuted_slot", "_shadow", "_d5_candidates", "_d5_pending")}}))
    sys.exit(0)
try:
    for i in range(K + 2):
        if case in (3, 4) and i == K - 1:
            ag.bound[slot] = tether.IDN
            if case == 3:
                ag._refuted_slot[slot] = tether.IDN
            else:
                ag._d5_pending[slot] = ("P", {}, tether.IDN)
                ag._d5_holds = lambda *a, **k: True
        out_before = ag.outstanding(slot)
        ag.step()
        if any(r.get("slot") == slot and r.get("event") == "bet"
               and (r.get("detail") or {}).get("vanished") for r in ag.led.rows()):
            dep, out_after = ag.cycle - 1, ag.outstanding(slot)
            break
except Exception as e:
    err, site = repr(e)[:300], _site(e)
rows = [r for r in ag.led.rows() if r.get("slot") == slot]
import speak
said = [s for _seq, s in speak.sentences(ag.led.rows())]
print(json.dumps({"err": err, "site": site, "dep": dep, "out": [out_before, out_after],
                  "rows": rows,
                  "said": [s for s in said if slot in s],
                  "stale": {k: slot in getattr(ag, k, {}) for k in
                            ("_refuted_slot", "_shadow", "_d5_candidates", "_d5_pending")},
                  "d5": getattr(tether, "_D5", None)}, default=str))
'''.replace("@CONST@", repr((APPEAR, LEAVE, K))[1:-1])


RECORD = r'''
import json, math, sys
sys.dont_write_bytecode = True
tree, case = sys.argv[1], sys.argv[2]
sys.path = [tree] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
import gamma, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="departed"), tether.Config(), ledger.Ledger())
a, b = sorted(ag.slots)[:2]
if case == "6":
    res = {a: tether.SlotResidual(a, tether.TRANSITION, 2, 2, math.log2(5), True),
           b: tether.SlotResidual(b, tether.TRANSITION, 1, 3, 1.0)}
    print(json.dumps({"effect": list(ag._characterise(res).effect)}))
    sys.exit(0)


def bet(frm, act, mass, gone):
    ag.led.record(ag.cycle, "PERCEIVE", a, "bet", channel=tether.TRANSITION, from_value=frm,
                  actual=act, mass=mass, **({"vanished": True} if gone else {}))


ag._process_bet("parked_explained", a)
for row in {"7a": [(2, 2, 2.0, True)], "7b": [(1, 2, 2.0, True)],
            "7c": [(1, 2, 0.0, False), (2, 2, 2.0, True)],
            "7d": [(1, 2, 0.0, False), (2, 3, 2.0, True)]}[case]:
    bet(*row)
ag._settle_process("level", "cap")
got = [r for r in ag.led.rows() if r["event"] == "process_settle"][-1]["detail"]
print(json.dumps({"right": got["right"], "by": got["settled_by"]}))
'''
LEFT = "the slot left the board after the park: no ground reading on its explanation"
NO_CHANGE = "no change after the park: no ground reading"
GRADED = "the world's grade of the slot's last change after the park"
EXPECT = {"6": ({"effect": ["gone", "over"]}, {"effect": ["exact", "over"]}),
          "7a": ({"right": None, "by": LEFT}, {"right": None, "by": NO_CHANGE}),
          "7b": ({"right": None, "by": LEFT}, {"right": False, "by": GRADED}),
          "7c": ({"right": True, "by": GRADED}, {"right": True, "by": GRADED}),
          "7d": ({"right": True, "by": GRADED}, {"right": False, "by": GRADED})}


def _record(tree: str, case: str, env: dict) -> dict:
    out = subprocess.run([sys.executable, "-c", RECORD, tree, case], capture_output=True,
                         text=True, env=env, timeout=600)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _env(env_file: str | None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["PYTHONDONTWRITEBYTECODE"], env["PYTHONHASHSEED"] = "1", "0"
    if env_file:
        with open(env_file, encoding="utf-8") as fh:
            for line in fh:
                if "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env


def _run(tree: str, case: int, env: dict, mutant: str = "none") -> dict:
    out = subprocess.run([sys.executable, "-c", PROBE, tree, str(case), mutant],
                         capture_output=True, text=True, env=env, timeout=600)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _check(r: dict, case: int, label: str) -> None:
    assert r["err"] is None, f"{label}: {r['err']}"
    assert r["dep"] is not None and r["dep"] >= 2, f"{label}: departure at cycle {r['dep']} (panel)"
    at = [x for x in r["rows"] if x["cycle"] == r["dep"]]
    bet = [x for x in at if x["event"] == "bet"]
    assert len(bet) == 1 and bet[0]["detail"]["vanished"] is True, f"{label}: bet rows {bet}"
    mass = bet[0]["detail"]["mass"]
    assert abs(mass - math.log2(bet[0]["detail"]["alphabet"])) < 1e-9, f"{label}: mass {mass}"
    before, after = r["out"]
    assert abs((after - before) - mass) < 1e-9, \
        f"{label}: outstanding {before} -> {after}, mass {mass}"
    route = [x for x in at if x["step"] == "ROUTE"]
    assert len(route) == 1 and route[0]["event"] == "route" and route[0]["detail"]["bin"] is None, \
        f"{label}: route rows {route}"
    assert "left the board" in route[0]["detail"]["why_not"], f"{label}: {route[0]['detail']}"
    acts = [(x["step"], x["event"]) for x in at if x["step"] in ("MINT", "ACCEPT", "SETTLE")]
    allowed = {("MINT", "d5_split_not_run")} if case == 4 else set()
    allowed |= {("SETTLE", "not_judged")} if case in (3, 4) else set()
    if case in (3, 4):
        assert ("SETTLE", "not_judged") in acts, f"{label}: settle wrote no not_judged row"
    assert set(acts) <= allowed, f"{label}: explanation acts on a departed slot {acts}"
    if case == 3:
        assert route[0]["detail"].get("refusal_not_priced") == "idn", \
            f"{label}: {route[0]['detail']}"
    if case == 4:
        assert ("MINT", "d5_split_not_run") in acts, f"{label}: pending split not consumed"
    assert not any(r["stale"].values()), f"{label}: stale {r['stale']}"
    assert any("it left the board" in s for s in r["said"]), f"{label}: speak {r['said']}"
    assert not any("None" in s for s in r["said"]), f"{label}: speak printed None {r['said']}"


def main() -> None:
    here = _repo.ROOT
    pin = sys.argv[1]
    env_file = sys.argv[2] if len(sys.argv) > 2 else None
    modes = [("OFF", _env(None))] + ([("ALL-ON", _env(env_file))] if env_file else [])
    ran = []
    for mode, env in modes:
        r0, p0 = _run(here, 0, env), _run(pin, 0, env)
        rows0 = [x for x in r0["rows"] if x["cycle"] == r0["dep"] and x["step"] == "ROUTE"]
        pins0 = [x for x in p0["rows"] if x["cycle"] == 0 and x["step"] == "ROUTE"]
        assert r0["err"] is None and r0["dep"] == 0, f"{mode} case 0: {r0['err']} dep {r0['dep']}"
        assert len(rows0) == 1 and rows0[0]["detail"]["bin"] is None, f"{mode} case 0: {rows0}"
        assert "left the board" in rows0[0]["detail"]["why_not"], f"{mode} case 0: {rows0}"
        assert p0["err"] is None and [x["detail"]["bin"] for x in pins0] == ["novel"], \
            f"{mode} case 0 MUST-DIFFER: the pin's cycle-0 row is {pins0} ({p0['err']})"
        ran.append(f"{mode} c0 (pin: novel)")
        for case in (1, 2, 3, 4, 5):
            r = _run(here, case, env)
            if case in (4, 5) and not r["d5"]:
                ran.append(f"{mode} c{case} n/a (D5 off)")
                continue
            if case == 5:
                assert r["err"] is None and not any(r["stale"].values()), f"{mode} case 5: {r}"
            else:
                _check(r, case, f"{mode} case {case}")
            p = _run(pin, case, env)
            assert p["err"] is not None, f"{mode} case {case} MUST-FAIL: the pin tree did not raise"
            if case == 5:
                assert (p["site"] or "").startswith("settle:"), \
                    f"{mode} case 5 pin site {p['site']}"
            ran.append(f"{mode} c{case} (pin {p['site']})")
    last = modes[-1]
    m1 = _run(here, 3, last[1], "settle")
    judged = [x for x in m1["rows"] if x["cycle"] == m1["dep"] and x["step"] == "SETTLE"
              and x["event"] != "not_judged"]
    assert m1["err"] is not None or any(m1["stale"].values()) or judged, \
        "MUTANT settle-open was not caught"
    ran.append(f"{last[0]} mutant settle-open caught")
    if last[0] == "ALL-ON":
        m2 = _run(here, 4, last[1], "d5")
        assert m2["err"] is not None, "MUTANT d5-open was not caught"
        ran.append("ALL-ON mutant d5-open caught")
    if len(sys.argv) > 3:
        for case, (want, want_pin) in EXPECT.items():
            got, pin_got = _record(here, case, _env(None)), _record(sys.argv[3], case, _env(None))
            assert got == want, f"case {case}: {got}, wanted {want}"
            assert pin_got == want_pin, f"case {case} at 2092625: {pin_got}, wanted {want_pin}"
            ran.append(f"c{case} " + ("same" if want == want_pin else "differs") + " at 2092625")
    else:
        ran.append("cases 6-7 not run (no 2092625 tree given)")
    print("test_departed: pass (" + "; ".join(ran) + ")")


if __name__ == "__main__":
    main()
