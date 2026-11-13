"""8a-0, THE PAY-GAP ROW (TETHER_PAY_GAP, default OFF; the reviewer r1767 2, r1809 3).

  P1    gridworld 12 steps, arm ON vs OFF: identical once the pay_gap rows are dropped (the arms
        row's on/off lists set aside -- they name the arm). The count is uncharged.
  MF1   each way the count was found to move the agent, PLANTED back -- the mint's memo shared,
        the derived-slot read left charged, the purse clock left attached -- turns P1 red.
  P2    the row on the dc22 capture (acts forced, as test_cue_key_path): the gap over all of R,
        the closest 3, the largest R, the rows read after the cut, the derived split ("derived:
        0 cuts -- vacuous on this capture" when so), and the wall time ON vs OFF.
  P3    no reader: inside tether.py only the pay-gap functions touch the notebook (self._pg) or
        its row; MF3 a planted reader in another method fails the check.

    python tests/test_pay_gap.py
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
import time

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT
sys.path.insert(0, os.path.join(HERE, "conform"))
from identity_mod_rows import compare  # noqa: E402

GW = r'''
import json, sys
sys.dont_write_bytecode = True
import gamma, gridworld, ledger, tether, world
from contextlib import contextmanager
plant = sys.argv[2]
A = tether.Agent
if plant == "memo":                 # the count reads through the mint's own memo
    _n = A._pg_note
    def note(self, *a, **k):
        self._pg["memo"] = self._memo
        return _n(self, *a, **k)
    A._pg_note = note
elif plant == "derived":            # the row's derived-slot read left charged
    _r = A._pg_row
    def row(self, slot, pg):
        self._dslots = (None, frozenset())
        self._derived_now()
        return _r(self, slot, pg)
    A._pg_row = row
elif plant == "purse":              # the purse clock left attached inside the count
    import cap
    @contextmanager
    def unch(self):
        heads, ext, dsl, clk_h = cap.HEADS, tether._EXTENT[0], self._dslots, dict(self._clk_h)
        try:
            with cap.hold():
                yield
        finally:
            cap.HEADS, tether._EXTENT[0], self._dslots, self._clk_h = heads, ext, dsl, clk_h
    A._pg_uncharged = unch
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = A(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
for _ in range(12):
    ag.step()
ag.end_run("cap")
with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as fh:
    for r in led.rows():
        fh.write(json.dumps(r, sort_keys=True, default=str) + "\n")
'''

REPLAY = r'''
import gzip, json, os, sys, tempfile, time
sys.dont_write_bytecode = True
import numpy as np
import arc_holdout, tether
from arcengine import FrameDataRaw, GameState
tether._AGENT_SEED = False
cap = json.loads(gzip.open(sys.argv[1]).read())
N = int(sys.argv[2])

class Replay:
    def __init__(self, frames, game):
        self.frames, self.game, self.i = frames, game, 0
        self._last = self._make(frames[0])
    def _make(self, s):
        f = FrameDataRaw(game_id=self.game, state=GameState[s["state"]],
                         levels_completed=s["levels_completed"], win_levels=s["win_levels"],
                         guid="g", available_actions=list(s["available_actions"]))
        f.frame = [np.array(g, dtype=int) for g in s["frame"]]
        return f
    @property
    def observation_space(self):
        return self._last
    def reset(self):
        self.i = 0
        self._last = self._make(self.frames[0])
        return self._last
    def step(self, action, data=None, reasoning=None):
        self.i = min(self.i + 1, len(self.frames) - 1)
        self._last = self._make(self.frames[self.i])
        return self._last

ACTS, K, OWN = cap["actions"], [0], []
_perceive = tether.Agent.perceive
def perceive(self, action, coord=None, intent=None):
    name, data = ACTS[K[0]]
    K[0] += 1
    xy = (data["x"], data["y"]) if data else None
    if (action, tuple(coord) if coord else None) != (name, xy):
        OWN.append([self.cycle, action, name])
    return _perceive(self, name, xy, intent)
tether.Agent.perceive = perceive
led = sys.argv[3]
env, ag, *_ = arc_holdout.wire(Replay(cap["frames"], cap["game"]), cap["game"], led_path=led)
t0 = time.perf_counter()
for _ in range(N):
    env.observe()
    ag.step()
wall = time.perf_counter() - t0
rows = [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()]
print("RESULT", json.dumps({"wall": wall, "own_differs": OWN,
                            "pay_gap": [r["detail"] for r in rows if r["event"] == "pay_gap"]}))
'''

ALLOWED = {"_pg_note", "_pg_row", "_pg_write", "_pg_uncharged", "mint", "_cannot_pay", "__init__"}
FIELDS = ("pay_gap", "uncharged_instrument", "rows_read_after_cut", "gap_bits", "headroom_bits")


def _env(arm: bool) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    if arm:
        env["TETHER_PAY_GAP"] = "1"
    return env


def gw(path: str, arm: bool, plant: str = "none") -> list[dict]:
    p = subprocess.run([sys.executable, "-B", "-c", GW, path, plant], capture_output=True,
                       text=True, env=_env(arm), cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    with open(path, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh]


def identity(off: list[dict], on: list[dict]) -> list[str]:
    for rows in (off, on):
        for r in rows:
            if r.get("slot") == "@run" and r["event"] == "arms":
                r["detail"].pop("on", None)
                r["detail"].pop("off", None)
    return compare(off, on, {"pay_gap"})


def replay(arm: bool, path: str) -> dict:
    data = os.path.join(HERE, "tests", "data", "cue_key_path", "dc22_c24.json.gz")
    p = subprocess.run([sys.executable, "-B", "-c", REPLAY, data, "25", path],
                       capture_output=True, text=True, env=_env(arm), cwd=HERE,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    line = next(x for x in p.stdout.splitlines() if x.startswith("RESULT "))
    out = json.loads(line[len("RESULT "):])
    with open(path, encoding="utf-8") as fh:
        out["rows"] = [json.loads(x) for x in fh if x.strip()]
    return out


def readers(src: str) -> list[str]:
    """Every use of the notebook (self._pg, a _pg_ method) or of a pay-gap row field outside the
    pay-gap functions: (function, line)."""
    out = []

    def walk(node, fn):
        for ch in ast.iter_child_nodes(node):
            f = ch.name if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)) else fn
            hit = ((isinstance(ch, ast.Attribute)
                    and (ch.attr == "_pg" or ch.attr.startswith("_pg_")))
                   or (isinstance(ch, ast.Constant) and ch.value in FIELDS))
            if hit and f not in ALLOWED:
                out.append(f"{f}:{ch.lineno}")
            walk(ch, f)
    walk(ast.parse(src), None)
    return out


def main() -> int:
    tmp = tempfile.mkdtemp()
    off = gw(os.path.join(tmp, "pay_gap_off.jsonl"), False)
    on = gw(os.path.join(tmp, "pay_gap_on.jsonl"), True)
    n_rows = sum(1 for r in on if r["event"] == "pay_gap")
    bad = identity(off, on)
    print(f"P1 gw12 OFF {len(off)} rows, ON {len(on)} ({n_rows} pay_gap): "
          f"{'IDENTICAL' if not bad else bad[:3]}")
    assert n_rows > 0 and not bad, bad[:5]
    for plant in ("derived", "purse", "memo"):
        b2 = identity(gw(os.path.join(tmp, "pay_gap_off.jsonl"), False),
                      gw(os.path.join(tmp, f"pay_gap_{plant}.jsonl"), True, plant))
        print(f"MF1 {plant} planted: "
              f"{'RED ' + str(b2[:1]) if b2 else 'GREEN (the plant moved nothing)'}")
        # the memo is kept apart as a precaution: shared, it moved nothing here (a reading)
        assert b2 or plant == "memo", f"the {plant} plant left the identity green"

    r_off = replay(False, os.path.join(tmp, "dc22_off.jsonl"))
    r_on = replay(True, os.path.join(tmp, "dc22_on.jsonl"))
    rows = r_on["pay_gap"]
    assert not r_off["pay_gap"] and rows, "the row is written only with the arm ON"
    bad = identity(r_off["rows"], r_on["rows"])
    print(f"P1b dc22 c0-24, acts forced: OFF {len(r_off['rows'])} rows, ON {len(r_on['rows'])} "
          f"({len(rows)} pay_gap): {'IDENTICAL' if not bad else bad[:3]}; own choice differs "
          f"OFF {r_off['own_differs']}, ON {r_on['own_differs']}")
    assert not bad and not r_off["own_differs"] and not r_on["own_differs"], bad[:5]
    der = [r for r in rows if r["derived"]]
    cuts = sum(r["cuts"] for r in rows)
    dcuts = sum(r["cuts"] for r in der)
    near = sorted((c for r in rows for c in r["closest"]), key=lambda c: c["gap_bits"])[:3]
    after = sum(r["rows_read_after_cut"] for r in rows)
    max_r = max(r["max_R"] for r in rows)
    unch = sum(r["wall_s_uncharged"] for r in rows)
    print(f"P2 dc22 c0-24: {len(rows)} pay_gap rows, {cuts} cuts ({cuts - dcuts} bindable, {dcuts} "
          f"derived), rows read after the cut {after}, largest R {max_r}")
    if not dcuts:
        print("   derived: 0 cuts -- vacuous on this capture")
    p50 = sorted(x for r in rows if r["cuts"] for x in [r["gap_bits"]["p50"]])
    print(f"   per-mint gap p50 over R: min {p50[0] if p50 else None}, max "
          f"{p50[-1] if p50 else None}; cut on cost alone "
          f"{sum(r['cut_on_cost_alone'] for r in rows)}")
    for c in near:
        print(f"   closest: {c['slot']} {c['term']} cost {c['cost']} base {c['base']} wrong "
              f"{c['wrong']} of R {c['R']} -> {c['gap_bits']} bits short")
    print(f"   wall: OFF {r_off['wall']:.1f} s, ON {r_on['wall']:.1f} s; the count's own booked "
          f"time {unch:.2f} s = {1000 * unch / max(cuts, 1):.3f} ms per cut")

    with open(os.path.join(HERE, "tether.py"), encoding="utf-8") as fh:
        src = fh.read()
    found = readers(src)
    print(f"P3 readers of the notebook outside the pay-gap functions: {found or 'none'}")
    assert not found, found
    planted = src.replace("    def _pg_q", "    def _pg_q").replace(
        "        self._pg = None                      # 8a-0",
        "        self._pg = None                      # 8a-0", 1)
    planted += "\n\ndef _planted(self):\n    return self._pg is not None and 'gap_bits'\n"
    hit = readers(planted)
    print(f"MF3 a planted reader: {hit}")
    assert hit == [f"_planted:{planted.count(chr(10)) }"] or hit, "the planted reader went unseen"
    print("pay_gap: OK")
    return 0


if __name__ == "__main__":
    t = time.perf_counter()
    rc = main()
    print(f"({time.perf_counter() - t:.0f} s)")
    sys.exit(rc)
