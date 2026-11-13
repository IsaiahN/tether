""""A => B", FIRST IMPLEMENTATION (TETHER_CAN_PRODUCE; the reviewer 2026-11-12; DESIGN 10d item 3).
Each reading predicts, from EARLIER readings only, the kinds the last press produced (appeared or
opened after it), settles them against this reading, then learns. Record-only.

CP1  the book: after A produced K once, A predicts K; a reading with K hits, one without misses
     (score [2, 1]); press B predicts nothing
CP2  honesty: on a fresh book the first reading that shows K after A predicts nothing -- a
     prediction never uses the reading it is settled on
MF-CP1 the plant: the agent learns BEFORE it predicts -> the first reading "hits" K -> RED
CP3  gridworld 12 steps, the arm ON vs OFF: identical once the can_* rows are dropped
Seconds.

    python tests/test_can_produce.py
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

import can_ledger as cl  # noqa: E402
import tether  # noqa: E402

HERE = _repo.ROOT


def agent_first_reading(plant: bool) -> list:
    """Agent._can_produce on a fresh book, one reading where K appeared after press A."""
    rows = []
    ns = types.SimpleNamespace(cycle=1)
    ns._can_kind_key = lambda item: ("K", item.split(".", 1)[1])
    ns.led = types.SimpleNamespace(record=lambda *_a, **k: rows.append(k))
    if plant:
        book = ns.__dict__.setdefault("_can_prod", cl.ProductionBook())
        book.learn("A", {("K", "row")})
    tether.Agent._can_produce(ns, "A", [], [{"item": "o3.row", "list": "CAN"}])
    return rows


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
    env = {**os.environ, "TETHER_CAN_PRODUCE": arm, "TETHER_AGENT_SEED": "0",
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
        if str(r.get("event", "")).startswith("can_") or (
                r.get("slot") == "@run" and r.get("event") == "arms"):
            continue
        r = dict(r)
        r.pop("seq", None)
        d = r.get("detail")
        if isinstance(d, dict):
            r["detail"] = {k: v for k, v in d.items()
                           if "wall" not in k and k != "s" and not k.endswith(("_ms", "_s"))
                           and k != "segment_rows" and not k.endswith("_seq")}
        out.append(json.dumps(r, sort_keys=True))
    return out


def main() -> int:
    b = cl.ProductionBook()
    k = ("K", "row")
    b.learn("A", {k})
    p1 = b.predict("A")
    h1, _m1 = b.settle("A", p1, {k})
    h2, m2 = b.settle("A", b.predict("A"), set())
    ok1 = p1 == [k] and h1 == [k] and m2 == [k] and not h2 and b.score[("A", k)] == [2, 1] \
        and b.predict("B") == []
    print(f"  CP1 predict {p1}; hit {h1}; then miss {m2}; score {b.score[('A', k)]}")
    print(f"CP1 the book predicts, settles, scores: {'GREEN' if ok1 else 'RED'}")
    rows = agent_first_reading(plant=False)
    ok2 = rows == []
    print(f"  CP2 first reading rows: {rows}")
    print(f"CP2 a prediction never uses its own reading: {'GREEN' if ok2 else 'RED'}")
    prows = agent_first_reading(plant=True)
    red = bool(prows) and bool(prows[0].get("hit"))
    print(f"MF-CP1 learned before predicting: {prows} -> {'RED (as required)' if red else 'GREEN'}")
    with tempfile.TemporaryDirectory() as td:
        off = gw(os.path.join(td, "off.jsonl"), "0")
        on = gw(os.path.join(td, "on.jsonl"), "1")
    x, y = strip(off), strip(on)
    diff = sum(1 for u, v in zip(x, y, strict=False) if u != v) + abs(len(x) - len(y))
    n = sum(1 for r in on if r.get("event") == "can_produce")
    hits = sum(len(r["detail"].get("hit", [])) for r in on if r.get("event") == "can_produce")
    print(f"  CP3 gw12: can_produce rows {n} (hits {hits}); differing without can_* rows {diff}")
    ok3 = diff == 0
    print(f"CP3 record-only on gw12: {'GREEN' if ok3 else 'RED'}")
    assert ok1 and ok2 and red and ok3
    print("can_produce: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
