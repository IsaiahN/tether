"""10a, THE PASS'S KIND TABLE (TETHER_KIND_PASS; the reviewer 2026-11-12, from the dc22 profile:
the goal proposer's cost is the group FORM -- 3.6M _kind calls in 25 steps -- not its text grammar).
One table per _group_cands pass: owner -> kind, kind -> owners in _owners' order. Exact.

KP1  gridworld after one step: _group_cands over the pair-distance texts (o.dist_x / drow_x /
     dcol_x == k) forms the same group rows, the same members in the same order, ON and OFF
MF-KP1 the plant: the table's member lists reversed -> the members' order differs -> RED
KP2  gridworld 12 steps, the arm ON vs OFF: the ledgers identical (timings and the arms row
     dropped)
Seconds.

    python tests/test_kind_pass.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

HERE = _repo.ROOT
KP1 = r'''
import os, sys
sys.path.insert(0, os.getcwd())
import gamma, gridworld, ledger, tether, world
got = {}
orig = tether.Agent._group_cands
def wrap(self, items, before, atoms, guard=None):
    got.setdefault("x", (dict(before), atoms))
    return orig(self, items, before, atoms, guard)
tether.Agent._group_cands = wrap
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                  ledger.Ledger())
ag.step()
before, atoms = got["x"]
objs = ["o0", "o1", "o2", "o3", "o4", "o5"]
items = {f"{o}.{r}_{x} == {k}": "library" for o in objs for x in objs if x != o
         for r in ("dist", "drow", "dcol") for k in (2, 5)}
if sys.argv[1] == "plant":
    real = orig
    def planted(self, items, before, atoms, guard=None):
        out, seen = [], set()
        owners = self._owners(before)
        self._own_pass = (before, owners)
        of = {o: self._kind(o) for o in owners}
        by = {}
        for o in reversed(owners):
            by.setdefault(of[o], []).append(o)
        self._kind_pass = (before, of, by)
        try:
            return self._group_cands_pass(items, before, atoms, out, seen, guard)
        finally:
            self._own_pass = None
            self._kind_pass = None
    on = planted(ag, items, before, atoms)
else:
    tether._KIND_PASS = True
    on = orig(ag, items, before, atoms)
tether._KIND_PASS = False
off = orig(ag, items, before, atoms)
def rows(xs):
    return [(k, t, tuple(p.slot for p in g.parts), tk) for k, t, g, tk, s in xs]
print(repr((len(on), rows(on) == rows(off), rows(on)[:1])))
'''


def kp1(mode: str):
    p = subprocess.run([sys.executable, "-B", "-c", KP1, mode], cwd=HERE, capture_output=True,
                       text=True, encoding="utf-8", timeout=600, stdin=subprocess.DEVNULL,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    assert p.returncode == 0, p.stderr[-3000:]
    return eval(p.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


GW = r'''
import json, sys
import gamma, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
for _ in range(12):
    ag.step()
ag.end_run("cap")
with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as fh:
    for r in led.rows():
        fh.write(json.dumps(r, sort_keys=True, default=str) + "\n")
'''


def gw(path: str, arm: str) -> list[dict]:
    env = {**os.environ, "TETHER_KIND_PASS": arm, "TETHER_AGENT_SEED": "0",
           "PYTHONIOENCODING": "utf-8"}
    p = subprocess.run([sys.executable, "-B", "-c", GW, path], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=600,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    with open(path, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh]


def strip(rows: list[dict]) -> list[str]:
    out = []
    for r in rows:
        if r.get("slot") == "@run" and r.get("event") == "arms":
            continue
        r = dict(r)
        r.pop("wall_s", None)
        d = r.get("detail")
        if isinstance(d, dict):
            r["detail"] = {k: v for k, v in d.items()
                           if "wall" not in k and k != "s" and not k.endswith(("_ms", "_s"))}
        out.append(json.dumps(r, sort_keys=True))
    return out


def main() -> int:
    n, same, first = kp1("on")
    print(f"  KP1: {n} group rows formed; ON == OFF {same}; first {first}")
    ok1 = n > 0 and same
    print(f"KP1 the same group rows, members in the same order: {'GREEN' if ok1 else 'RED'}")
    pn, psame, _pf = kp1("plant")
    red = not psame
    print(f"  plant: {pn} rows; equal to OFF {psame}")
    print(f"MF-KP1 the member lists reversed: {'RED (as required)' if red else 'GREEN'}")
    with tempfile.TemporaryDirectory() as td:
        off = gw(os.path.join(td, "off.jsonl"), "0")
        on = gw(os.path.join(td, "on.jsonl"), "1")
    a, b = strip(off), strip(on)
    diff = sum(1 for x, y in zip(a, b, strict=False) if x != y) + abs(len(a) - len(b))
    print(f"  gw12: {len(off)} rows OFF, {len(on)} ON; differing {diff}")
    ok2 = diff == 0
    print(f"KP2 gw12 identical ON vs OFF: {'GREEN' if ok2 else 'RED'}")
    assert ok1 and red and ok2
    print("kind_pass: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
