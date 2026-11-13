"""10c, LIKE KINDS FIRST (TETHER_KIND_REUSE; the reviewer 2026-11-12; DESIGN 10c). A goal shelved
at a clear keeps the kinds of the objects its text named; a shelf template's instance on an object
of such a kind is ordered first inside its price group, inside the class tier. Order only.

KR1  _like_kind: an instance on a won kind -> 0; on another kind -> 1; a library candidate -> 1
KR2  _shelve_one keeps the kinds its text names (gridworld, o3.row == 5 -> o3's kind)
KR3  _b1_decided names "kind" when the class is equal and the kind cue differs, "class" otherwise
MF-KR1 the plant: _like_kind always 1 -> KR1's won-kind instance reads 1 -> RED
KR4  gridworld 12 steps, the arm ON vs OFF: identical (no shelf in 12 steps; the retest reads it)
Seconds.

    python tests/test_kind_reuse.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import types

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import tether  # noqa: E402

HERE = _repo.ROOT


def like(plant: bool = False) -> tuple:
    kinds = {"o1": ("A",), "o2": ("B",)}
    ns = types.SimpleNamespace(_kind=lambda o: kinds[o])
    ns._kind_tag = lambda o: tether.Agent._kind_tag(ns, o)
    ns._goal_shelf = {"S": {"kinds": [ns._kind_tag("o1")]}}
    fn = (lambda _x: 1) if plant else (lambda x: tether.Agent._like_kind(ns, x))
    c1, c2 = types.SimpleNamespace(slot="o1.row"), types.SimpleNamespace(slot="o2.row")
    return (fn(((0,), "t", c1, None, "S")), fn(((0,), "t", c2, None, "S")),
            fn(((0,), "t", c1, None, "library")))


KR2 = r'''
import os, sys
sys.path.insert(0, os.getcwd())
import gamma, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                  ledger.Ledger())
ag.step()
ag._goal_text["k"] = "o3.row == 5"
ag._goal_meta["k"] = {}
ag._shelve_one("k", "test", {"won": 1, "lost": 0}, "test")
print(repr((ag._goal_shelf["k"].get("kinds"), ag._kind_tag("o3"))))
'''

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


def child(code: str, *args: str, env_extra: dict | None = None):
    env = {**os.environ, "TETHER_AGENT_SEED": "0", "PYTHONIOENCODING": "utf-8",
           **(env_extra or {})}
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=600,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return p.stdout


def gw(path: str, arm: str) -> list[dict]:
    child(GW, path, env_extra={"TETHER_KIND_REUSE": arm})
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
    won, other, lib = like()
    ok1 = (won, other, lib) == (0, 1, 1)
    print(f"  KR1 won kind {won}, other kind {other}, library {lib}")
    print(f"KR1 like kinds read 0, the rest 1: {'GREEN' if ok1 else 'RED'}")
    kinds, tag = eval(child(KR2).strip().splitlines()[-1])  # noqa: S307  our own child's repr
    ok2 = kinds == [tag]
    print(f"  KR2 shelved kinds {kinds}; o3's {tag}")
    print(f"KR2 the shelf keeps the won text's kinds: {'GREEN' if ok2 else 'RED'}")
    c = types.SimpleNamespace(slot="o1.row")
    by = {"a": (None, "a", c), "b": (None, "b", c), "d": (None, "d", c)}
    keys = {"a": ((1, 0), (), 0, True, 0, 0, 0, 0), "b": ((1, 1), (), 0, True, 0, 0, 0, 0),
            "d": ((2, 0), (), 0, True, 0, 0, 0, 0)}
    tiers = ("class", "ttb", "parked", "turnable", "round", "subject_tried", "checked", "explore")
    k1 = tether.Agent._b1_decided(by, ["a", "b"], 1, tiers, lambda x: keys[x[1]], ())
    k2 = tether.Agent._b1_decided(by, ["b", "d"], 1, tiers, lambda x: keys[x[1]], ())
    ok3 = k1.get("decided_by") == "kind" and k2.get("decided_by") == "class"
    print(f"  KR3 {k1.get('decided_by')} / {k2.get('decided_by')}")
    print(f"KR3 the decided tier is named: {'GREEN' if ok3 else 'RED'}")
    pw, _po, _pl = like(plant=True)
    red = pw != 0
    print(f"MF-KR1 _like_kind always 1: won kind reads {pw} -> "
          f"{'RED (as required)' if red else 'GREEN'}")
    with tempfile.TemporaryDirectory() as td:
        off = gw(os.path.join(td, "off.jsonl"), "0")
        on = gw(os.path.join(td, "on.jsonl"), "1")
    x, y = strip(off), strip(on)
    diff = sum(1 for u, v in zip(x, y, strict=False) if u != v) + abs(len(x) - len(y))
    print(f"  KR4 gw12: {len(off)} rows OFF, {len(on)} ON; differing {diff}")
    ok4 = diff == 0
    print(f"KR4 gw12 identical ON vs OFF: {'GREEN' if ok4 else 'RED'}")
    assert ok1 and ok2 and ok3 and red and ok4
    print("kind_reuse: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
