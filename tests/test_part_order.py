"""10b, A GOAL'S PARTS, MOST LIKELY TO FAIL FIRST (TETHER_PART_ORDER; the reviewer 2026-11-12;
Fig 3 :22-23; fail-first). A held goal's parts: "A then B" as specified; otherwise fewest routes
first, a part with no route last (it orders, never refuses); the first part stalling parks the goal.

PO1  the order: routes {a: 3, b: 1, c: 0, d: 1} -> b, d, a, c (fewest first, a tie by link order,
     none last); an "A then B" keeps its order whatever the routes
PO2  fail-first: the first part stuck -> park; another part stuck, the first moving -> no park; a
     one-part goal -> no park
MF-PO1 the plant: _part_order returns link order -> PO1 reads a, b, c, d -> RED
PO3  gridworld 12 steps, the arm ON vs OFF: identical (gridworld holds no goal in 12 steps, so this
     proves only that nothing else moved; the retest reads the holds)
Seconds.

    python tests/test_part_order.py
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


def order(plant: bool = False) -> tuple:
    table = {"A1": {"delta": {("c", "a", "+"): 1, ("c", "b", "+"): 1}},
             "A2": {"delta": {("c", "a", "-"): 1, ("c", "d", "+"): 1}},
             "A3": {"delta": {("c", "a", "+"): 1}}}
    ns = types.SimpleNamespace(iface=types.SimpleNamespace(table=table))
    ns._part_routes = lambda sl: tether.Agent._part_routes(ns, sl)
    fn = (lambda slots, _ordered: list(slots)) if plant else \
        (lambda slots, ordered: tether.Agent._part_order(ns, slots, ordered))
    return fn(["a", "b", "c", "d"], False), fn(["a", "b", "c", "d"], True)


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
    env = {**os.environ, "TETHER_PART_ORDER": arm, "TETHER_AGENT_SEED": "0",
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
    flat, spec = order()
    ok1 = flat == ["b", "d", "a", "c"] and spec == ["a", "b", "c", "d"]
    print(f"  PO1 fewest routes first: {flat}; A then B: {spec}")
    print(f"PO1 the parts' order: {'GREEN' if ok1 else 'RED'}")
    ff = tether.Agent._fail_first
    h = {"part_order": ["b", "a"], "slots": ["a", "b"]}
    r_first = ff(h, lambda sl: sl == "b")
    r_other = ff(h, lambda sl: sl == "a")
    r_one = ff({"part_order": ["a"], "slots": ["a"]}, lambda _sl: True)
    ok2 = r_first and not r_other and not r_one
    print(f"  PO2 first stuck {r_first}; other stuck {r_other}; one part {r_one}")
    print(f"PO2 fail-first parks on the first part only: {'GREEN' if ok2 else 'RED'}")
    pflat, _ps = order(plant=True)
    red = pflat != ["b", "d", "a", "c"]
    print(f"MF-PO1 link order: {pflat} -> {'RED (as required)' if red else 'GREEN'}")
    with tempfile.TemporaryDirectory() as td:
        off = gw(os.path.join(td, "off.jsonl"), "0")
        on = gw(os.path.join(td, "on.jsonl"), "1")
    x, y = strip(off), strip(on)
    diff = sum(1 for u, v in zip(x, y, strict=False) if u != v) + abs(len(x) - len(y))
    print(f"  PO3 gw12: {len(off)} rows OFF, {len(on)} ON; differing {diff}")
    ok3 = diff == 0
    print(f"PO3 gw12 identical ON vs OFF: {'GREEN' if ok3 else 'RED'}")
    assert ok1 and ok2 and red and ok3
    print("part_order: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
