"""5, THE ARRIVAL GAP (TETHER_ARRIVAL_GAP, default ON; the reviewer 2026-10-28 r280, r283). A fake
game (test_entry.FakeWrapper plus two pieces) plays K steps; its board is then replaced between
steps and env.arrive() takes it, as e4_stream's "switch between" does. Each case asserts its
occasion before its failure; each arm runs in its own process (the flag resolves at import).
  MISS (a) few claimed: the static piece recoloured in place, the rest gone, new pieces elsewhere
       (median over claims high, so the appearance gate refuses it, as re86 / cn04 / s5i5 / wa30)
  MISS (b) all claimed: every piece moved far with colour and shape kept (median 0, colour share
       under the bar, as su15 / bp35)
  ON:  at the step after the arrival, an arrival_gap row decided by "bar: ordinary-max n=K" with
       the share above the bar, the break applied (a frame_break row, same cycle), and an
       appearance_disagrees row. MUST-FAIL OFF: no frame_break anywhere (the appearance gate
       keeps the claims, as on the 12 misses)
  HOLD no arrival_gap and no frame_break row on any ordinary step; ordinary readings counted
  FIRST the arrival after one step (no ordinary reading yet): "bar: none yet, appearance", the
       appearance call decides alone (kind (a): no break; a striped switch: break)
  OFF  identity: the arm OFF writes the same ledger as d12c74e on the plain fake and on the miss
       (a) arrival, arms rows aside and wall timings masked
    python tests/test_arrival_gap.py
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

BASE = "d12c74e"      # the tree before the arm

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, kind, k = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import numpy as np
from arcengine import GameState
import arc_holdout, gate
from test_entry import FakeWrapper

def miss_a():
    g = np.zeros((64, 64), dtype=int)
    g[5:9, 5:9] = 1
    g[15:20, 40:45] = 5
    g[20:22, 20:30] = 6
    g[56:60, 2:5] = 8
    return g

def miss_b():
    g = np.zeros((64, 64), dtype=int)
    g[10:14, 50:54] = 3
    g[45:49, 45:49] = 7
    g[10:13, 12:17] = 2
    g[10:12, 25:31] = 4
    return g

def stripes():
    g = np.zeros((64, 64), dtype=int)
    for i, col in enumerate((1, 2, 5, 6)):
        g[:, i * 16:(i + 1) * 16] = col
    return g

class Two(FakeWrapper):
    def __init__(self):
        self.new = None
        super().__init__()

    def _frame(self, state):
        f = super()._frame(state)
        if self.new is None:
            g = f.frame[0].copy()
            g[40:43, 10:15] = 2
            g[50:52, 50:56] = 4
        else:
            g = self.new()
        f.frame = [g]
        return f

w = Two()
env, ag, led, *_ = arc_holdout.wire(w, "fake")
switch_at = None
for i in range(8):
    if kind != "plain" and i == k:
        w.new = {"a": miss_a, "b": miss_b, "stripes": stripes}[kind]
        w._frame(GameState.NOT_FINISHED)
        assert env.arrive()
        switch_at = ag.cycle
    ag.step()
rows = ag.led.rows()
v = gate.check(rows)
print(json.dumps({"switch_at": switch_at, "n": getattr(ag, "_ag_n", None),
                  "max": getattr(ag, "_ag_max", None),
                  "gate": [v["verdict"], v.get("check"), v.get("token")], "rows": rows},
                 default=str))
'''


def child(tree: str, kind: str, k: int, extra: dict | None = None) -> dict:
    env = {k2: v for k2, v in os.environ.items() if not k2.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree, kind, str(k)], env=env,
                         capture_output=True, text=True, timeout=900, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def ev(rows: list, name: str) -> list:
    return [r for r in rows if r["event"] == name]


def _miss(kind: str) -> None:
    root = str(_repo.ROOT)
    on = child(root, kind, 4)
    c = on["switch_at"]
    gap, brk = ev(on["rows"], "arrival_gap"), ev(on["rows"], "frame_break")
    assert c is not None and len(gap) == 1 and gap[0]["cycle"] == c, ("MISS occasion", kind, c,
                                                                     gap)
    d = gap[0]["detail"]
    assert d["appearance"]["broke"] is False, ("MISS precondition: appearance broke", kind, d)
    assert d["bar_n"] > 0 and d["decided_by"].startswith("bar: ordinary-max"), (kind, d)
    assert d["share"] > d["bar"] and d["broke"] and d["applied"] >= 1, ("MISS ON: no break",
                                                                         kind, d)
    assert [r["cycle"] for r in brk] == [c], ("MISS ON: frame_break", kind, brk)
    dis = ev(on["rows"], "appearance_disagrees")
    assert len(dis) == 1 and dis[0]["cycle"] == c, ("MISS ON: appearance_disagrees", kind, dis)
    assert on["gate"][0] == "pass", ("MISS ON: gate", kind, on["gate"])
    assert on["n"] >= 4, ("HOLD: ordinary readings not counted", kind, on["n"])
    print(f"  MISS ({kind}) ON: arrival at cycle {c}: held {d['held']}, failed {d['failed']} "
          f"(carried {d['carried']}, changed {d['changed']}), share {d['share']} > bar "
          f"{d['bar']} ({d['decided_by']}); appearance found {d['appearance']['found']} "
          f"claimed {d['appearance']['claimed']} median {d['appearance']['median']} colour "
          f"{d['appearance']['colour_share']} said no break; break applied ({d['applied']} "
          f"record), appearance_disagrees written; gate pass")
    off = child(root, kind, 4, {"TETHER_ARRIVAL_GAP": "0"})
    assert off["switch_at"] is not None, ("MUST-FAIL OFF occasion", kind)
    assert not ev(off["rows"], "frame_break") and not ev(off["rows"], "arrival_gap"), (
        "MUST-FAIL OFF: a break or gap row", kind)
    print(f"  MISS ({kind}) MUST-FAIL OFF: the arrival at cycle {off['switch_at']} keeps its "
          "claims: no frame_break, no arrival_gap (the appearance gate refuses, as on the 12)")


def check_miss_a() -> None:
    _miss("a")


def check_miss_b() -> None:
    _miss("b")


def check_hold() -> None:
    root = str(_repo.ROOT)
    plain = child(root, "plain", 0)
    assert plain["n"] and plain["n"] >= 6, ("HOLD occasion: ordinary readings", plain["n"])
    assert not ev(plain["rows"], "arrival_gap") and not ev(plain["rows"], "frame_break"), "HOLD"
    assert plain["max"] == 0.0, ("HOLD: an ordinary step head read a held value failing",
                                 plain["max"])
    print(f"  HOLD: 8 ordinary steps: {plain['n']} ordinary readings, max {plain['max']}; no "
          "arrival_gap, no frame_break")


def check_first() -> None:
    root = str(_repo.ROOT)
    for kind, want in (("a", False), ("stripes", True)):
        r = child(root, kind, 1)
        gap = ev(r["rows"], "arrival_gap")
        assert len(gap) == 1, ("FIRST occasion", kind, gap)
        d = gap[0]["detail"]
        assert d["bar_n"] == 0 and d["decided_by"] == "bar: none yet, appearance", (kind, d)
        assert d["broke"] is want and d["appearance"]["broke"] is want, ("FIRST", kind, d)
        assert bool(ev(r["rows"], "frame_break")) is want, ("FIRST: frame_break", kind)
        assert not ev(r["rows"], "appearance_disagrees"), ("FIRST: a disagreement row", kind)
        print(f"  FIRST ({kind}): arrival after one step, no ordinary reading yet: decided by "
              f"appearance alone ({'break' if want else 'no break'}; share {d['share']})")


def _off_identity(kind: str, k: int) -> None:
    root = str(_repo.ROOT)
    sys.path.insert(0, os.path.join(root, "conform"))
    from identity_mod_rows import mask_timings

    def norm(rows):
        return [(r["cycle"], r["step"], r["slot"], r["event"],
                 json.dumps(r["detail"], sort_keys=True, default=str))
                for r in mask_timings(json.loads(json.dumps(rows))) if r["event"] != "arms"]
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = norm(child(d, kind, k)["rows"])
        cur = norm(child(root, kind, k, {"TETHER_ARRIVAL_GAP": "0"})["rows"])
        diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base)
                                                                              - len(cur))
        assert len(base) > 50 and diff == 0, ("OFF identity", kind, len(base), len(cur),
                                             next((i for i, (x, y) in enumerate(
                                                 zip(base, cur, strict=False)) if x != y),
                                                 None))
        print(f"  OFF identity ({kind}): {len(base)} rows against {BASE}, 0 differences "
              "(arms rows aside, wall timings masked)")


def check_off_identity_plain() -> None:
    _off_identity("plain", 0)


def check_off_identity_miss_a() -> None:
    _off_identity("a", 4)


def main() -> int:
    # names on the command line run only those checks, one per process, each under the 5-minute
    # cap (the reviewer 2026-10-28 r284, as test_window)
    want = set(sys.argv[1:])
    checks = [v for k, v in globals().items() if k.startswith("check_")
              and (not want or k in want)]
    assert not want or len(checks) == len(want), ("unknown check name", sorted(want))
    for c in checks:
        c()
        print("ok  ", c.__name__)
    print(f"arrival_gap: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
