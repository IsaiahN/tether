"""10a+ -> "A then B" (TETHER_CAN_OFFER; the reviewer 2026-11-12; Isaiah 15:01). An OPENED crossing
files its opener (the press before it, its src) under the item's KIND; a closed or newly blocked
item of that kind gets a can_offer row naming the openers. Record-only.

CO1  the book: openers offered most seen first
CO2  the agent: o3.row opened after ACTION1 (BY:k) -> o4.row (the same kind) closed is offered
     "ACTION1, BY:k"; o4.col (another reading) is offered nothing
MF-CO1 the plant: the key is the item itself, not its kind -> o4.row is offered nothing -> RED
CO3  gridworld 12 steps, the arm ON vs OFF: identical once the can_* rows are dropped
Seconds.

    python tests/test_can_offer.py
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

import can_ledger as cl  # noqa: E402

HERE = _repo.ROOT
CO2 = r'''
import os, sys
sys.path.insert(0, os.getcwd())
import gamma, gridworld, ledger, tether, world
if sys.argv[1] == "plant":
    tether.Agent._can_kind_key = lambda self, item: (item,)
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
ag.step()
ag._can_offer_note({"item": "o3.row", "kind": "opened"}, "ACTION1", "BY:k")
ag._can_offer_note({"item": "o3.row", "kind": "discovered"}, "ACTION2", "SELF")
ag._can_offer_row("o4.row")
ag._can_offer_row("o4.col")
rows = [r for r in led.rows() if r.get("event") in ("can_opener", "can_offer")]
print(repr([(r["event"], r["detail"].get("item"), r["detail"].get("offers")) for r in rows]))
'''


def co2(mode: str):
    p = subprocess.run([sys.executable, "-B", "-c", CO2, mode], cwd=HERE, capture_output=True,
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
    env = {**os.environ, "TETHER_CAN_OFFER": arm, "TETHER_AGENT_SEED": "0",
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
    b = cl.OpenerBook()
    b.note(("K", "row"), "ACTION3", "SELF")
    b.note(("K", "row"), "ACTION1", "BY:k")
    b.note(("K", "row"), "ACTION1", "BY:k")
    got = b.offers(("K", "row"))
    ok1 = [(g["press"], g["seen"]) for g in got] == [("ACTION1", 2), ("ACTION3", 1)] \
        and b.offers(("K", "col")) == []
    print(f"  CO1 {got}")
    print(f"CO1 openers, most seen first: {'GREEN' if ok1 else 'RED'}")
    rows = co2("on")
    offers = {it: off for ev, it, off in rows if ev == "can_offer"}
    openers = [it for ev, it, _o in rows if ev == "can_opener"]
    print(f"  CO2 openers filed {openers}; offers {offers}")
    ok2 = (openers == ["o3.row"] and "o4.col" not in offers
           and [(o["press"], o["src"]) for o in offers.get("o4.row", [])] == [("ACTION1", "BY:k")])
    print(f"CO2 a like item closed is offered its kind's opener: {'GREEN' if ok2 else 'RED'}")
    prows = co2("plant")
    poff = {it for ev, it, _o in prows if ev == "can_offer"}
    red = "o4.row" not in poff
    print(f"MF-CO1 keyed by the item, not its kind: offers {sorted(poff)} -> "
          f"{'RED (as required)' if red else 'GREEN'}")
    with tempfile.TemporaryDirectory() as td:
        off = gw(os.path.join(td, "off.jsonl"), "0")
        on = gw(os.path.join(td, "on.jsonl"), "1")
    x, y = strip(off), strip(on)
    diff = sum(1 for u, v in zip(x, y, strict=False) if u != v) + abs(len(x) - len(y))
    n_op = sum(1 for r in on if r.get("event") == "can_opener")
    n_of = sum(1 for r in on if r.get("event") == "can_offer")
    print(f"  CO3 gw12: openers {n_op}, offers {n_of}; differing without can_* rows {diff}")
    ok3 = diff == 0
    print(f"CO3 record-only on gw12: {'GREEN' if ok3 else 'RED'}")
    assert ok1 and ok2 and red and ok3
    print("can_offer: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
