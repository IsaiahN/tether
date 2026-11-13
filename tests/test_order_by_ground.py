"""10a, ORDER BY GROUND (TETHER_GOAL_ORDER_BY_GROUND; the reviewer 2026-11-12; Isaiah 14:59: "I can
walk and use my legs < i cannot see anymore (blind) circumstantial - the ground decides"). The
proposer's PRICE and CLASS cues are ordered by what paid on the holds they disagreed on; price
first (today's) until the ground says otherwise.

OB1  the order: price leads with no evidence, with too little, and while it pays; class leads
     once price has 3 disagreeing endings and pays less than class's record (or its 0.5 prior)
OB2  the key: price first leaves it; class first puts a dearer routable candidate before a
     cheaper unroutable one, and the key's last element stays the bits
OB3  wired: gridworld 12 steps with the record preset to price [5 ended, 0 paid] -> every
     goal_hypotheses row's order_first reads "class" (gridworld picks nothing in 12 steps, so the
     pick's own credit is read on dc22, not here)
MF-OB1 the plant: _obg_first pinned to "price" (validity ignored) -> OB3's rows read "price" -> RED
OB4  gridworld 12 steps, the arm ON vs OFF: identical once the order fields are dropped,
     unless the ground moved the order within the run (then it is named)
Seconds.

    python tests/test_order_by_ground.py
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

import tether  # noqa: E402

HERE = _repo.ROOT
GW = r'''
import json, sys
import gamma, gridworld, ledger, tether, world
if sys.argv[2] == "plant":
    tether.Agent._obg_first = staticmethod(lambda rec: "price")
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
if sys.argv[2] in ("preset", "plant"):
    ag._obg = {"price": [5, 0], "class": [0, 0]}
for _ in range(12):
    ag.step()
ag.end_run("cap")
with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as fh:
    for r in led.rows():
        fh.write(json.dumps(r, sort_keys=True, default=str) + "\n")
'''


def gw(path: str, arm: str, mode: str = "plain") -> list[dict]:
    env = {**os.environ, "TETHER_GOAL_ORDER_BY_GROUND": arm, "TETHER_AGENT_SEED": "0",
           "PYTHONIOENCODING": "utf-8"}
    p = subprocess.run([sys.executable, "-B", "-c", GW, path, mode], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=600,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    with open(path, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh]


def firsts(rows: list[dict]) -> list:
    return [r["detail"]["order_first"] for r in rows
            if r.get("event") == "goal_hypotheses"
            and isinstance(r.get("detail"), dict) and "order_first" in r["detail"]]


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
                           if "wall" not in k and k != "s" and not k.endswith(("_ms", "_s"))
                           and k not in ("order_by_ground", "order_first")}
        out.append(json.dumps(r, sort_keys=True))
    return out


def main() -> int:
    f = tether.Agent._obg_first
    cases = {"none": ({"price": [0, 0], "class": [0, 0]}, "price"),
             "too little": ({"price": [2, 0], "class": [0, 0]}, "price"),
             "price pays": ({"price": [5, 4], "class": [0, 0]}, "price"),
             "price fails": ({"price": [5, 0], "class": [0, 0]}, "class"),
             "class worse": ({"price": [5, 1], "class": [6, 0]}, "price"),
             "class better": ({"price": [5, 1], "class": [6, 4]}, "class")}
    got = {k: f(rec) for k, (rec, _w) in cases.items()}
    ok1 = all(got[k] == w for k, (_r, w) in cases.items())
    print(f"  OB1 {got}")
    print(f"OB1 the order follows the record: {'GREEN' if ok1 else 'RED'}")
    k = tether.Agent._obg_key
    a, b = ((1, 1, 1, 5.0), 2), ((1, 1, 1, 7.0), 1)        # cheap but unroutable; dear, routable
    p_first = sorted([a, b], key=lambda x: k(x[0], x[1], "price"))[0]
    c_first = sorted([a, b], key=lambda x: k(x[0], x[1], "class"))[0]
    ok2 = p_first is a and c_first is b and k(b[0], b[1], "class")[-1] == 7.0
    print(f"OB2 class first puts the routable dearer one first, bits last: "
          f"{'GREEN' if ok2 else 'RED'}")
    with tempfile.TemporaryDirectory() as td:
        pre = gw(os.path.join(td, "pre.jsonl"), "1", "preset")
        pl = gw(os.path.join(td, "pl.jsonl"), "1", "plant")
        off = gw(os.path.join(td, "off.jsonl"), "0")
        on = gw(os.path.join(td, "on.jsonl"), "1")
    fp, fpl, fon = firsts(pre), firsts(pl), firsts(on)
    print(f"  OB3 preset: first {fp}; plant: {fpl}")
    ok3 = bool(fp) and all(x == "class" for x in fp)
    print(f"OB3 a failing price record puts class first: {'GREEN' if ok3 else 'RED'}")
    red = not fpl or any(x != "class" for x in fpl)
    print(f"MF-OB1 pinned to price: {'RED (as required)' if red else 'GREEN'}")
    x, y = strip(off), strip(on)
    diff = sum(1 for u, v in zip(x, y, strict=False) if u != v) + abs(len(x) - len(y))
    moved = [z for z in fon if z != "price"]
    print(f"  OB4 gw12: {len(off)} rows OFF, {len(on)} ON; differing {diff}; ON firsts {fon}")
    ok4 = diff == 0 or bool(moved)
    print(f"OB4 gw12 identical unless the ground moved the order: {'GREEN' if ok4 else 'RED'}")
    assert ok1 and ok2 and ok3 and red and ok4
    print("order_by_ground: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
