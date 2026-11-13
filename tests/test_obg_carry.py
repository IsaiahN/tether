"""10a CARRY (TETHER_OBG_CARRY; the reviewer 2026-11-12; Isaiah 23:10: "learned search order should
carry over ... search would naturally be getting smarter over time reinforced by usage and
results"). ORDER_BY_GROUND's record [ended, paid] per cue rides the lineage as increments (obg_n)
and load sums it, in the store and in the archive chain alike.

OC1  the store (TETHER_MEMORY_STORE on): a saved record [price 5/0, class 1/1] loads equal in a
     fresh agent; a second save with nothing new loads the same (increments, never a double
     count); that agent adds one ended price hold, saves, and the next agent loads 6/0
OC2  the archive chain (TETHER_MEMORY_STORE=0): the same three readings
OC3  a loaded record of price 5/0 puts class first at the next generation's first pick order
     (_obg_first reads the carried record)
MF-OC1 the plant: the save leaves obg_n out -> the fresh agent loads 0/0 -> RED
MF-OC2 the plant: load does not mark the loaded record written -> the loaded agent's next save
     carries its ancestors' counts again -> the next agent loads a double count -> RED
OC4  gridworld 12 steps with no lineage, the arm ON vs OFF: identical
Seconds.

    python tests/test_obg_carry.py
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
CARRY = r'''
import os, sys, tempfile
from pathlib import Path
sys.path.insert(0, os.getcwd())
import gamma, gridworld, ledger, lineage, tether, world
mode = sys.argv[1]
if mode == "no_mark":
    _orig = lineage._obg_load
    def _obg_load(ag, summed):
        keep = {c: list(v) for c, v in ag._obg_written.items()}
        out = _orig(ag, summed)
        ag._obg_written = keep
        return out
    lineage._obg_load = _obg_load
def agent():
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        ledger.Ledger())
d = Path(tempfile.mkdtemp(prefix="obg_"))
a = agent()
a._obg = {"price": [5, 0], "class": [1, 1]}
if mode == "no_save":
    tether._OBG_CARRY = False
lineage.write(d, a, "default")
tether._OBG_CARRY = True
b = agent()
lineage.load(d, b)
first = {k: list(v) for k, v in b._obg.items()}
lineage.write(d, a, "default")            # nothing new since a's last save
c = agent()
lineage.load(d, c)
again = {k: list(v) for k, v in c._obg.items()}
c._obg["price"][0] += 1                   # one more ended price hold in c's lifetime (c is the tip)
lineage.write(d, c, "default")
e = agent()
lineage.load(d, e)
grown = {k: list(v) for k, v in e._obg.items()}
print(repr((first, again, grown, tether.Agent._obg_first(e._obg))))
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


def child(code: str, *args: str, env_extra: dict | None = None) -> str:
    env = {**os.environ, "TETHER_AGENT_SEED": "0", "PYTHONIOENCODING": "utf-8",
           **(env_extra or {})}
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=600,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return p.stdout


def carry(mode: str, store: str) -> tuple:
    out = child(CARRY, mode, env_extra={"TETHER_MEMORY_STORE": store})
    return eval(out.strip().splitlines()[-1])  # noqa: S307  our own child's repr


SAVED = {"price": [5, 0], "class": [1, 1]}
GROWN = {"price": [6, 0], "class": [1, 1]}


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


def gw(path: str, arm: str) -> list[dict]:
    child(GW, path, env_extra={"TETHER_OBG_CARRY": arm})
    with open(path, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh]


def main() -> int:
    oks = []
    for name, store in (("OC1 the store", "1"), ("OC2 the archive chain", "0")):
        first, again, grown, lead = carry("plain", store)
        ok = first == SAVED and again == SAVED and grown == GROWN
        print(f"  {name}: loaded {first}; after a save with nothing new {again}; "
              f"after one more ended price hold {grown}")
        print(f"{name}: the record carries as increments: {'GREEN' if ok else 'RED'}")
        oks.append(ok)
        if store == "1":
            ok3 = lead == "class"
            print(f"OC3 the carried record puts {lead} first: {'GREEN' if ok3 else 'RED'}")
            oks.append(ok3)
    first, *_ = carry("no_save", "1")
    red1 = first != SAVED
    print(f"MF-OC1 the save leaves obg_n out: loaded {first} -> "
          f"{'RED (as required)' if red1 else 'GREEN'}")
    for name, store in (("store", "1"), ("archive", "0")):
        _f, _a, grown, _l = carry("no_mark", store)
        red2 = grown != GROWN
        print(f"MF-OC2 ({name}) load does not mark the record written: next agent loads {grown} -> "
              f"{'RED (as required)' if red2 else 'GREEN'}")
        oks.append(red2)
    with tempfile.TemporaryDirectory() as td:
        off = gw(os.path.join(td, "off.jsonl"), "0")
        on = gw(os.path.join(td, "on.jsonl"), "1")
    x, y = strip(off), strip(on)
    diff = sum(1 for u, v in zip(x, y, strict=False) if u != v) + abs(len(x) - len(y))
    ok4 = diff == 0
    print(f"  OC4 gw12: {len(off)} rows OFF, {len(on)} ON; differing {diff}")
    print(f"OC4 gw12 identical ON vs OFF: {'GREEN' if ok4 else 'RED'}")
    assert all(oks) and red1 and ok4
    print("obg_carry: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
