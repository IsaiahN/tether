"""THE CHOICE TALLY (TETHER_CHOICE_TALLY, default ON; TETHER_CHOICE_TALLY_CHECK; Isaiah 2026-10-23
09:12 "these should be deduped and tallied"; the reviewer 09:13, 10:40). Each arm state in its own
process (arms resolve at import).
  U    the ledger alone: a key's first objective_domain choice row is appended, its repeats are not;
       flush_tally writes one choice_tally row per repeated key (ref, n, first and last cycle);
       `written` counts both; since_written returns both in call order; OFF appends every row
  P    THE PLANT (as test_fit_dedup's rows plant): gridworld_arc_s1, 15 steps, an objective_domain
       choice row recorded inside every _left call (so the fit's dedup captures and replays them):
       ON, OFF and CHECK give the same acting rows, and the same count per key (OFF: its rows; ON:
       1 + the tally rows' n); every other row equal (rest(): wall_s dropped, cited seqs ranked);
       the gate's verdict equal; CHECK never fires
  L    THE LIFE (the reviewer 10:52): the plant cut mid-step at cycle 7, call 80 of 164
       (CapReached from inside _left, so the step's finally flushes after the cut row), the
       after_cut steps, three
       repeated rows written outside any step, end_run: ON (CHECK) and OFF equal as in P
  MF1  CHECK with a deliberately wrong n (+1 before the flush) raises
  MF2  CHECK with a tally key that drops "frontier" (a decision field) raises: two rows that differ
       in it were merged
  MF-LIFE  L with end_run's flush removed: the end repeats are lost (1 of 3)
    python tests/test_choice_tally.py
"""
from __future__ import annotations

import bisect
import collections
import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gate  # noqa: E402
from conform.identity_mod_rows import TIMINGS  # noqa: E402
from ledger import GENERAL as GEN  # noqa: E402
from ledger import SPECIFIED as SPEC  # noqa: E402

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, mode = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, panel, tether, world

def row(led, cyc, slot, fr, pick="1", step="PERCEIVE"):
    led.record(cyc, step, slot, "choice", site="objective_domain", options=2,
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

if mode == "order":
    import gate, tempfile, pathlib
    out = {}
    tmp = tempfile.mkdtemp()
    for case in ("earlier", "later", "mode"):
        path = pathlib.Path(tmp) / (case + ".jsonl")     # the FILE the gate reads: a row's mode
        led = ledger.Ledger(path=str(path))                # is stamped there at record time
        ledger._LEDGER_HANDLE = False                      # opened per row, so nothing is held
        if case == "earlier":           # PERCEIVE, ROUTE, then a repeat at PERCEIVE
            row(led, 0, "o1.x", [["'2'", 0.0, 2]])
            led.record(0, "ROUTE", "o1.x", "other", a=1)
            row(led, 0, "o1.x", [["'2'", 0.0, 2]])
        elif case == "later":           # a repeat at MINT between PERCEIVE and ROUTE
            row(led, 0, "o2.y", [["'3'", 0.0, 3]], step="MINT")
            led.record(1, "PERCEIVE", "o2.y", "other", a=1)
            row(led, 1, "o2.y", [["'3'", 0.0, 3]], step="MINT")
            led.record(1, "ROUTE", "o2.y", "other", a=2)
        else:                           # the same key under another mode
            row(led, 0, "o3.z", [["'4'", 0.0, 4]])
            led.mode = ledger.GENERAL
            row(led, 0, "o3.z", [["'4'", 0.0, 4]])
        led.flush_tally(1)
        rows = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln]
        v = gate.check(rows)
        out[case] = {"gate": [v["verdict"], v["check"], v["token"], v.get("note")],
                     "choice_modes": [r["mode"] for r in rows if r["event"] == "choice"],
                     "full": getattr(led, "tally_full", None)}
    print(json.dumps({"order": ledger._CHOICE_TALLY_ORDER, "out": out}))
    raise SystemExit

import cap
_left_ = tether.Agent._left
_calls = {}
def _left_w(self, term, slot, hist, *a, **k):
    row(self.led, self.cycle, slot, [[repr(len(hist) % 3), 0.0, 1]],
        step=self._running_step)          # labelled as the real writer labels (tether.py:8216)
    _calls[self.cycle] = _calls.get(self.cycle, 0) + 1
    if mode.startswith("life") and self.cycle == 7 and _calls[7] == 80:
        raise cap.CapReached()       # a cut mid-step, after this step's repeats began
    return _left_(self, term, slot, hist, *a, **k)
tether.Agent._left = _left_w
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="tally"), tether.Config(), ledger.Ledger())
for _ in range(15 if mode == "plant" else 9):
    ag.step()
if mode.startswith("life"):
    for _ in range(3):
        row(ag.led, ag.cycle, "o9.z", [["'7'", 0.0, 7]])    # repeats written outside any step
    if mode == "life_mf":
        ag.led.flush_tally = lambda cycle: None             # end_run's flush removed
    ag.end_run("cap")
print(json.dumps({"on": ledger._CHOICE_TALLY, "check": ledger._CHOICE_TALLY_CHECK,
                  "calls": _calls, "full": getattr(ag.led, "tally_full", None),
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


def tallied(r: dict) -> bool:
    return r["event"] == "choice_tally" or (r["event"] == "choice"
                                            and r["detail"].get("site") == "objective_domain")


def rest(rows: list) -> list:
    """Every other row, with two changes, each named (the reviewer 2026-10-23 10:52 (b), (d)):
    WALL_S  goal_hypotheses' wall_s (tether.py:6420) is a wall-clock timing: two OFF runs differ
            in it, and nothing in the agent reads it (only conform/identity_mod_rows.py's TIMINGS
            list), so it is dropped.
    SEQ     a field that cites a row by ledger seq is replaced by the number of non-tallied rows
            before it, so ON and OFF must cite the SAME place among the other rows; the tally
            appends fewer rows by design, so the raw seq shifts. Fields: process_bet's plan_seq
            (tether.py:6713, value from :12896), repeat's gamma_read.fed[].seq (:12913, :12921,
            :15994), process_settle's bet_seq (:6763), resolution's signal_seq and fed[][0]
            (:3356). The agent reads seqs only as an ORDER (:3354 x > seq, :6750 r["seq"] >
            b["seq"], :9355 stamp seq < _seq_at_level), each between appended rows, which the
            rank keeps."""
    kept = sorted(r["seq"] for r in rows if not tallied(r))

    def rank(v):
        return ["rank", bisect.bisect_left(kept, v)] if isinstance(v, int) else v

    out = []
    for r in rows:
        if tallied(r) or r["event"] == "arms":
            continue
        d = json.loads(json.dumps(r["detail"]))
        for ev, field in TIMINGS:                     # WALL_S: the one list, imported (step clock)
            if r["event"] == ev:
                d.pop(field, None)
        if r["event"] == "process_bet" and "plan_seq" in d:
            d["plan_seq"] = rank(d["plan_seq"])                              # SEQ
        if r["event"] == "process_settle" and "bet_seq" in d:
            d["bet_seq"] = rank(d["bet_seq"])                                # SEQ
        if r["event"] == "resolution":
            d["signal_seq"] = rank(d.get("signal_seq"))                      # SEQ
            d["fed"] = [[rank(x), ro] for x, ro in d["fed"]] if d.get("fed") else d.get("fed")
        if r["event"] == "repeat" and isinstance(d.get("gamma_read"), dict):
            for e in d["gamma_read"].get("fed", ()):
                e["seq"] = rank(e.get("seq"))                                # SEQ
        out.append((r["cycle"], r["step"], r["slot"], r["event"], json.dumps(d, sort_keys=True)))
    return out


def acting(rows: list) -> list:
    return [(r["cycle"], r["detail"].get("action"), r["detail"].get("by")) for r in rows
            if r["slot"] == "@loop" and r["event"] == "repeat"]


def main() -> None:
    u = child("unit", TETHER_CHOICE_TALLY="1")
    # the guard: cycle 1's o1.x is the first row of (1, "o1.x"), so it goes in full ("step")
    assert u["on"] and (u["entries"], u["written"]) == (5, 6), ("U counts", u)
    tal = [d for s, e, d in u["rows"] if e == "choice_tally"]
    assert len(tal) == 1 and tal[0]["n"] == 1 and tal[0]["ref"] == 0, ("U tally", tal)
    assert u["since"] == [["o1.x", "choice"], ["o2.y", "choice"], ["o1.x", "other"]], u["since"]
    un = child("unit", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_ORDER="0")
    assert (un["entries"], un["written"]) == (4, 6), ("U without the guard", un)
    o = child("unit", TETHER_CHOICE_TALLY="0")
    assert not o["on"] and (o["entries"], o["written"]) == (5, 5), ("U OFF", o)
    print(f"  U: ON 4 rows + 1 tally row (n 1) of 6 writes; without the guard 3 + 1 (n 2); "
          f"since_written in call order; OFF {o['entries']} entries")
    m1 = child("mf1", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_CHECK="1")
    assert m1["err"] and "CHOICE_TALLY CHECK" in m1["err"], ("MF1", m1)
    # MF2 isolates CHECK, so the guard is off: with it on, a row with a field outside the key is
    # never tallied ("field"), and the merge cannot happen at all
    m2 = child("mf2", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_CHECK="1",
               TETHER_CHOICE_TALLY_ORDER="0")
    assert m2["err"] and "CHOICE_TALLY CHECK" in m2["err"], ("MF2", m2)
    m2g = child("mf2", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_CHECK="1")
    assert m2g["err"] is None and m2g["entries"] == 5, ("MF2 under the guard: in full", m2g)
    c0 = child("unit", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_CHECK="1")
    assert c0["err"] is None, ("CHECK clean", c0)
    print("  MF1 (n + 1) and MF2 (a key without frontier, guard off) raise under CHECK; under the "
          "guard MF2's rows go in full; the clean case does not raise")
    og = child("order", TETHER_CHOICE_TALLY="1")
    on_ = child("order", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_ORDER="0")
    e, la, mo = og["out"]["earlier"], og["out"]["later"], og["out"]["mode"]
    assert og["order"] and e["gate"][:3] == ["refuse", "steps", "step-order"] \
        and e["gate"][3] == "o1.x: PERCEIVE after ROUTE" and e["full"]["step"] == 1, e
    assert la["gate"][:3] == ["refuse", "steps", "step-order"] \
        and la["gate"][3] == "o2.y: ROUTE after MINT" and la["full"]["step"] == 1, la
    assert mo["choice_modes"] == [SPEC, GEN] and mo["full"]["mode"] == 1, mo
    assert not on_["order"] and [on_["out"][c]["gate"][0] for c in ("earlier", "later")] == [
        "pass", "pass"] and on_["out"]["mode"]["choice_modes"] == [SPEC], on_
    print("  MF-ORDER-1 (a repeat at an EARLIER step), -2 (at a LATER step, before a ROUTE row), "
          "-3 (another mode): the guard writes each in full and the file gate refuses 1 and 2 "
          "(step-order) and holds 3's row; without the guard each is tallied away and the gate "
          "passes")
    on = child("plant", TETHER_CHOICE_TALLY="1")
    ong = child("plant", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_ORDER="0")
    off = child("plant", TETHER_CHOICE_TALLY="0")
    ck = child("plant", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_CHECK="1")
    n_off = sum(1 for r in off["rows"] if r["event"] == "choice"
                and r["detail"].get("site") == "objective_domain")
    assert n_off > 50, ("P: precondition, too few planted rows", n_off)
    assert acting(on["rows"]) == acting(off["rows"]) == acting(ck["rows"]), "P: acting rows"
    assert per_key(on["rows"]) == per_key(off["rows"]) == per_key(ck["rows"]), "P: per-key counts"
    assert rest(on["rows"]) == rest(off["rows"]) == rest(ck["rows"]), "P: the other rows"
    g = [gate.check(x["rows"]) for x in (on, off, ck)]
    assert [v["verdict"] for v in g] == ["pass"] * 3, ("P: the gate's accepting path", g)
    assert per_key(ong["rows"]) == per_key(off["rows"]), "P: per-key counts without the guard"
    print(f"  P: {n_off} planted rows OFF -> {len(on['rows'])} rows ON (guard; in full by it: "
          f"{on['full']}) and {len(ong['rows'])} without the guard, of {len(off['rows'])} OFF; "
          f"{len(per_key(off['rows']))} keys, the same count per key; acting rows equal; other "
          f"rows equal (wall_s dropped, cited seqs ranked); gate {g[0]['verdict']} on all three; "
          "CHECK clean")
    lo = child("life", TETHER_CHOICE_TALLY="1", TETHER_CHOICE_TALLY_CHECK="1")
    lf = child("life", TETHER_CHOICE_TALLY="0")
    mf = child("life_mf", TETHER_CHOICE_TALLY="1")
    ev = [r["event"] for r in lo["rows"]]
    cut_c = next(r["cycle"] for r in lo["rows"] if r["event"] == "cap_mid_step")
    # the cut at cycle 7 (of 9 steps, from the measured per-cycle _left counts) leaves one step
    assert ev.count("cap_mid_step") == 1 and ev.count("after_cut") == 1, (
        "L: precondition, the cut", ev.count("cap_mid_step"), ev.count("after_cut"), lo["calls"])
    assert any(r["event"] == "choice_tally" and r["detail"]["last_cycle"] >= cut_c - 1
               for r in lo["rows"]), "L: treatment, no tally row for the cut step"
    kz = [k for k in per_key(lf["rows"]) if '"o9.z"' in k]
    assert len(kz) == 1 and per_key(lf["rows"])[kz[0]] == 3, ("L: OFF's end rows", kz)
    assert per_key(lo["rows"]) == per_key(lf["rows"]), "L: per-key counts after a cut and life end"
    assert acting(lo["rows"]) == acting(lf["rows"]) and rest(lo["rows"]) == rest(lf["rows"]), "L"
    gl = [gate.check(x["rows"]) for x in (lo, lf)]
    assert [v["verdict"] for v in gl] == ["pass", "pass"], ("L: the gate's accepting path", gl)
    # MF-LIFE's occasion (the sweep, 2026-10-23): in the guarded life the o9.z key has ONE row
    # and a choice_tally row referring to it with n == 2, so two repeats were pending at end_run
    oz = [r for r in lo["rows"] if r["event"] == "choice" and r["slot"] == "o9.z"]
    tz = [r for r in lo["rows"] if r["event"] == "choice_tally" and oz
          and r["detail"]["ref"] == oz[0]["seq"]]
    assert len(oz) == 1 and len(tz) == 1 and tz[0]["detail"]["n"] == 2, ("MF-LIFE occasion", oz, tz)
    assert per_key(mf["rows"])[kz[0]] == 1, ("MF-LIFE: end_run without its flush kept the total",
                                              per_key(mf["rows"])[kz[0]])
    print(f"  L: a cut at cycle {cut_c} mid-tally, {ev.count('after_cut')} after_cut steps, "
          f"3 repeats outside a step, end_run: per-key counts, acting and other rows equal ON "
          f"(CHECK) and OFF; gate {gl[0]['verdict']} on both. MF-LIFE: end_run without its "
          "flush shows 1 of 3")
    print("choice_tally: OK")


if __name__ == "__main__":
    main()
