"""10a+, WHAT I CAN DO AND WHAT I CAN'T (TETHER_CAN_LEDGER; the reviewer 2026-11-12; Isaiah
15:01-15:08). Every subject slot is read into CAN / BLOCKED / NOT_FOUND / GIVEN_UP at every
step; a crossing or an appearance is a row. Record-only.

CL1  classify: not movable -> BLOCKED; no route with actions untried -> NOT_FOUND; no route with
     every action tried -> BLOCKED; refuted -> GIVEN_UP; else CAN
CL2  a BLOCKED -> CAN crossing is "opened"; NOT_FOUND -> CAN is "discovered"; GIVEN_UP -> CAN with
     nothing learned is flagged "world or scope changed"; CAN -> BLOCKED is "closed"; a new item is
     an appearance
MF-CL1 the plant: the CAN'T classes collapsed into one -> the opening reads as a discovery -> RED
CL3  gridworld 12 steps, the arm ON vs OFF: identical once the can_* rows are dropped (record-only),
     and ON writes can_lists rows
Seconds.

    python tests/test_can_ledger.py
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
    env = {**os.environ, "TETHER_CAN_LEDGER": arm, "TETHER_AGENT_SEED": "0",
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
        r.pop("seq", None)          # the extra rows shift every later row's sequence number
        d = r.get("detail")
        if isinstance(d, dict):
            # timings, and fields that COUNT ledger rows (the can_* rows add to them)
            r["detail"] = {k: v for k, v in d.items()
                           if "wall" not in k and k != "s" and not k.endswith(("_ms", "_s"))
                           and k != "segment_rows" and not k.endswith("_seq")}
        out.append(json.dumps(r, sort_keys=True))
    return out


def main() -> int:
    slots = ["a.x", "b.x", "c.x", "d.x", "e.x"]
    now = cl.classify(slots, movable={"b.x", "c.x", "d.x", "e.x"}, routable={"d.x", "e.x"},
                      clock=set(), untried_actions=2, given_up={"e.x"})
    every = cl.classify(["c.x"], movable={"c.x"}, routable=set(), clock=set(),
                        untried_actions=0, given_up=set())
    ok1 = (now["a.x"][0] == cl.BLOCKED and now["b.x"][0] == cl.NOT_FOUND
           and now["d.x"][0] == cl.CAN and now["e.x"][0] == cl.GIVEN_UP
           and every["c.x"][0] == cl.BLOCKED)
    print(f"  CL1 lists: {now} / every action tried: {every}")
    print(f"CL1 classify: {'GREEN' if ok1 else 'RED'}")
    prev = {"y.x": (cl.BLOCKED, "not a movable slot"), "z.x": (cl.NOT_FOUND, "no route yet"),
            "g.x": (cl.GIVEN_UP, "refuted"), "c.x": (cl.CAN, "movable and routable")}
    nxt = {"y.x": (cl.CAN, "m"), "z.x": (cl.CAN, "m"), "g.x": (cl.CAN, "m"),
           "c.x": (cl.BLOCKED, "not a movable slot"), "n.x": (cl.CAN, "m")}
    cross, appear = cl.crossings(prev, nxt, learned_since=False)
    kinds = {r["item"]: r["kind"] for r in cross}
    flag = [r["item"] for r in cross if "flag" in r]
    ok2 = (kinds == {"y.x": "opened", "z.x": "discovered", "g.x": "returned", "c.x": "closed"}
           and flag == ["g.x"] and [a["item"] for a in appear] == ["n.x"])
    print(f"  CL2 crossings {kinds}; flagged {flag}; appeared {[a['item'] for a in appear]}")
    print(f"CL2 four crossing kinds + appearance: {'GREEN' if ok2 else 'RED'}")
    # the plant: one CAN'T class
    flat_prev = {k: ((cl.NOT_FOUND, w) if s != cl.CAN else (s, w)) for k, (s, w) in prev.items()}
    pc, _pa = cl.crossings(flat_prev, nxt, learned_since=False)
    red = {r["item"]: r["kind"] for r in pc}.get("y.x") != "opened"
    print(f"MF-CL1 classes collapsed: y.x reads {({r['item']: r['kind'] for r in pc})['y.x']}"
          f" -> {'RED (as required)' if red else 'GREEN'}")
    with tempfile.TemporaryDirectory() as td:
        off = gw(os.path.join(td, "off.jsonl"), "0")
        on = gw(os.path.join(td, "on.jsonl"), "1")
    lists = [r for r in on if r.get("event") == "can_lists"]
    crossn = [r for r in on if r.get("event") == "can_crossing"]
    a, b = strip(off), strip(on)
    diff = sum(1 for x, y in zip(a, b, strict=False) if x != y) + abs(len(a) - len(b))
    print(f"  gw12: can_lists {len(lists)}, can_crossing {len(crossn)}; first "
          f"{lists[0]['detail'] if lists else None}; differing without can_* rows {diff}")
    ok3 = diff == 0 and bool(lists)
    print(f"CL3 record-only on gw12: {'GREEN' if ok3 else 'RED'}")
    assert ok1 and ok2 and red and ok3
    print("can_ledger: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
