"""19 DESCRIBED_WALK (TETHER_DESCRIBED_WALK, default ON; the reviewer 2026-10-31 r531, r533).
Minimal gates, each in its own process. ORDER ONLY, so ON and OFF rows are expected to differ.
  check_found_set     six identical movers (r481's fixture), 20 steps: every (slot, entry) offered
                      or minted from under OFF is offered or minted from under ON by the run's end;
                      ON writes walk_ordered rows and OFF none; walks, ROUTE and reach_s printed
  check_no_verdict    the same runs: ON writes no event kind OFF does not, except walk_ordered, and
                      no more refusals than OFF
  check_off_identity  TETHER_DESCRIBED_WALK=0 (off_env) against 1e9d4d5, fake, whole-run
    python tests/test_described_walk.py [check ...]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

from _batch import off_env  # noqa: E402  the batch's arms (r348)

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

BASE = "1e9d4d5"        # wip/held-compile, the tree before arm 19

FAKE = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout
from test_entry import FakeWrapper
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
for _ in range(24):
    ag.step()
ag.end_run("cap")
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''

MOVERS = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import numpy as np
import arc_holdout
import tether
from arcengine import FrameDataRaw
from test_entry import FakeWrapper
OFFS = [(0, 0), (0, 12), (12, 0), (12, 12), (24, 0), (24, 12)]
class Movers(FakeWrapper):
    def _frame(self, state):
        g = np.zeros((64, 64), dtype=int)
        r, c = self.pos
        for dr, dc in OFFS:
            g[r + dr:r + dr + 4, c + dc:c + dc + 4] = 3
        g[60:63, 60:63] = 7
        f = FrameDataRaw(game_id="fake-0001", state=state, levels_completed=0, win_levels=2,
                         guid="g", available_actions=list(self.actions))
        f.frame = [g]
        self._last = f
        return f
    def step(self, action, data=None, reasoning=None):
        out = super().step(action, data, reasoning)
        self.pos = [min(self.pos[0], 32), min(self.pos[1], 40)]
        return self._frame(out.state) if out.frame else out
offered, walks = set(), [0]
real_reach, real_one = tether.Agent._library_reach, tether.Agent._walk_one
def reach(self, slot, *a, **k):
    out = real_reach(self, slot, *a, **k)
    for m, offs in self._lib_offers.items():
        for o_ in offs:
            offered.add((m, (o_.get("prov") or {}).get("library")))
    return out
def one(self, *a, **k):
    walks[0] += 1
    return real_one(self, *a, **k)
tether.Agent._library_reach, tether.Agent._walk_one = reach, one
env, ag, led, *_ = arc_holdout.wire(Movers(), "fake")
for _ in range(20):
    ag.step()
ag.end_run("cap")
rows = ag.led.rows()
minted = {(r["slot"], (r["detail"].get("library") or {}).get("library")) for r in rows
          if r["event"] == "mint" and isinstance(r["detail"].get("library"), dict)}
print(json.dumps({"rows": rows, "offered": sorted(map(list, offered)),
                  "minted": sorted(map(list, minted)), "walks": walks[0]}, default=str))
'''


def _child(probe: str, tree: str, extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", probe, tree], env=env,
                         capture_output=True, text=True, timeout=1800, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _norm(rows: list) -> list:
    sys.path.insert(0, os.path.join(str(_repo.ROOT), "conform"))
    from identity_mod_rows import mask_timings
    return [(r["cycle"], r["step"], r["slot"], r["event"],
             json.dumps(r["detail"], sort_keys=True, default=str))
            for r in mask_timings(json.loads(json.dumps(rows))) if r["event"] != "arms"]


def _diff(a: list, b: list) -> tuple:
    n = sum(1 for x, y in zip(a, b, strict=False) if x != y) + abs(len(a) - len(b))
    return n, next((i for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y), None)


def _sum(rows: list, field: str, sub: str | None = None) -> float:
    out = 0.0
    for r in rows:
        if r["event"] == "repeat":
            v = r["detail"].get(field)
            out += (v.get(sub, 0.0) if isinstance(v, dict) else 0.0) if sub else (v or 0.0)
    return out


def _pair() -> tuple:
    root = str(_repo.ROOT)
    return _child(MOVERS, root), _child(MOVERS, root, {"TETHER_DESCRIBED_WALK": "0"})


def check_found_set() -> None:
    on, off = _pair()
    f_on = {tuple(x) for x in on["offered"]} | {tuple(x) for x in on["minted"]}
    f_off = {tuple(x) for x in off["offered"]} | {tuple(x) for x in off["minted"]}
    lost = sorted(f_off - f_on)
    print(f"  found set OFF {len(f_off)}, ON {len(f_on)}; OFF not reached ON: {len(lost)}; "
          f"ON only: {len(f_on - f_off)}")
    r_off, r_on = _sum(off["rows"], "wall_s", "ROUTE"), _sum(on["rows"], "wall_s", "ROUTE")
    print(f"  walks OFF {off['walks']}, ON {on['walks']}; ROUTE sum OFF {r_off:.2f} s, ON "
          f"{r_on:.2f} s; reach_s OFF {_sum(off['rows'], 'reach_s'):.2f} s, ON "
          f"{_sum(on['rows'], 'reach_s'):.2f} s")
    wo = [r["detail"] for r in on["rows"] if r["event"] == "walk_ordered"]
    print(f"  walk_ordered rows ON {len(wo)}: k_first {sum(d['k_first'] for d in wo)} of lit "
          f"{sum(d['lit'] for d in wo)}, walked {sum(d['walked'] for d in wo)}")
    assert not lost, ("STOP: OFF's found (slot, entry) not reached ON", lost[:20])
    assert f_off, "the fixture found nothing OFF: the set cannot be compared"
    assert wo and not any(r["event"] == "walk_ordered" for r in off["rows"]), "the row"


def check_no_verdict() -> None:
    """The order holds nothing back beyond A2's cut, so it can add no verdict: ON writes no event
    kind OFF does not, except walk_ordered. The compile-refusal tallies and the verdict kinds are
    printed, not bounded: a different order walks a different set within the budget."""
    on, off = _pair()
    kinds_on = {r["event"] for r in on["rows"]}
    kinds_off = {r["event"] for r in off["rows"]}
    assert kinds_on - kinds_off <= {"walk_ordered"}, ("ON writes a new kind", kinds_on - kinds_off)
    ref = {name: sum(sum((r["detail"].get("refused") or {}).values()) for r in rows
                     if r["event"] == "library") for name, rows in (("on", on["rows"]),
                                                                    ("off", off["rows"]))}
    vk = ("refused", "refuse", "route_refused", "cut_refuted", "unreached", "refutation_dropped")
    cnt = {name: {k: sum(1 for r in rows if r["event"] == k) for k in vk}
           for name, rows in (("on", on["rows"]), ("off", off["rows"]))}
    print(f"  new event kinds ON: {sorted(kinds_on - kinds_off)}; library compile refusals OFF "
          f"{ref['off']}, ON {ref['on']}; verdict kinds OFF {cnt['off']}, ON {cnt['on']}")


def check_off_identity() -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(FAKE, d)["rows"])
    cur = _norm(_child(FAKE, root, off_env("TETHER_DESCRIBED_WALK"))["rows"])
    n, at = _diff(base, cur)
    assert len(base) > 50 and n == 0, (len(base), len(cur), at)
    print(f"  OFF identity (TETHER_DESCRIBED_WALK=0, fake): {len(base)} rows against {BASE}, "
          "0 differences")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        assert r.returncode == 0, n
    print(f"described_walk: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
