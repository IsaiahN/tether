"""BUILD 3 item 10, THE DESCRIBED LOOKUP'S WINDOWS (the reviewer 2026-11-04 r1045, r1053; Fig 8 :39
"a search that finds nothing is never a proof of absence"). The 12-step gridworld: its position
slots' description key moves between asks (delta sign, contact, target order), and at 630ad50 every
ask read the same first window of 32 of 1716 lit entries.

MF-W1  TETHER_WINDOW_BACKOFF: an ask whose window keeps 0 asks the next ranked window at once -- an
       ask reaches a window index > 0; RED on 630ad50 (one window per ask)
MF-W2  a list asked to its end records no_entry with asked == listed and not_asked 0; RED on 630ad50
       (asked 0, not_asked 1716)
MF-N1  TETHER_NOFIT_BY_READS is exact: per ask, the kept entries and the no_entry verdicts are the
       same keyed by the readings as by the whole description
MF-N2  with one window per ask (TETHER_WINDOW_BACKOFF=0), a later ask with the same readings skips
       what was judged (judged > 0) and so takes a window the first ask did not; RED on 630ad50
       (the same first window every ask)

    python tests/test_window_backoff.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve()


def run() -> dict:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    asks: list = []
    real_lit, real_topk = tether.Agent._described_lit, tether.Agent._topk

    def topk(self, full, lit, tiers, att, tg, key):
        judged = sum(len(v) for v in self._tk_nofit.values())   # before this window
        win, nxt = real_topk(self, full, lit, tiers, att, tg, key)
        if not asks or asks[-1]["key"] != repr(key) or asks[-1]["cycle"] != self.cycle:
            asks.append({"cycle": self.cycle, "slot": key[0], "key": repr(key), "windows": [],
                         "kept": [], "reads": sorted(str(att.get(s)) for s in tg)})
        asks[-1]["windows"].append({"entries": [k for k, _w in win], "judged": judged})
        return win, nxt

    def lit_(self, lib, lit, tiers, att, tg, head_keys=None):
        got = real_lit(self, lib, lit, tiers, att, tg, head_keys)
        if asks and head_keys is not None:
            asks[-1]["kept"].append([k for k, _w in got])
        return got
    tether.Agent._topk, tether.Agent._described_lit = topk, lit_
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    for _ in range(12):
        ag.step()
    miss = [r["detail"] for r in led.rows() if r["event"] == "no_entry"]
    return {"asks": asks, "no_entry": [{"asked": d.get("asked"), "not_asked": d.get("not_asked"),
                                        "listed": sum((d.get("listed") or {}).values())}
                                       for d in miss]}


def child(extra: dict) -> dict:
    env = {**{k: v for k, v in os.environ.items() if not k.startswith("TETHER_")},
           "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "TETHER_AGENT_SEED": "0",
           **extra}
    r = subprocess.run([sys.executable, "-B", str(HERE), "--run"], env=env, capture_output=True,
                       text=True, timeout=900)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def main():
    if "--run" in sys.argv:
        print(json.dumps(run()))
        return
    on = child({})
    asks = on["asks"]
    assert asks, "no described-lookup ask on gridworld"
    deep = [a for a in asks if len(a["windows"]) > 1]
    assert deep, ("MF-W1: no ask went past its first window", [len(a["windows"]) for a in asks])
    full = [m for m in on["no_entry"] if m["listed"]]
    assert full and all(m["asked"] == m["listed"] and m["not_asked"] == 0 for m in full), (
        "MF-W2", on["no_entry"])

    by_desc = child({"TETHER_NOFIT_BY_READS": "0"})

    def verdicts(r):
        return ([(a["cycle"], a["slot"], [k for ks in a["kept"] for k in ks]) for a in r["asks"]],
                r["no_entry"])
    assert verdicts(on)[0] == verdicts(by_desc)[0], "MF-N1: kept entries differ by the key"
    assert [(m["listed"]) for m in on["no_entry"]] == [m["listed"] for m in by_desc["no_entry"]], (
        "MF-N1: no_entry verdicts differ by the key")

    one = child({"TETHER_WINDOW_BACKOFF": "0"})
    same = [(a, b) for i, a in enumerate(one["asks"]) for b in one["asks"][i + 1:]
            if a["reads"] == b["reads"]]
    assert same, "MF-N2 has no occasion: no two asks with the same readings"
    a, b = same[0]
    assert b["windows"][0]["judged"] > 0 and \
        set(b["windows"][0]["entries"]) - set(a["windows"][0]["entries"]), (
        "MF-N2: the later ask re-read the first ask's window", a["windows"][0], b["windows"][0])
    print(f"  MF-W1 {len(asks)} asks; windows per ask {[len(a['windows']) for a in asks]}")
    print(f"  MF-W2 {len(full)} full-list misses, each asked == listed "
          f"({full[0]['listed']}), not_asked 0")
    print(f"  MF-N1 kept entries and {len(on['no_entry'])} no_entry verdicts identical keyed by "
          "the readings and by the whole description")
    print(f"  MF-N2 one window per ask: the later ask (c{b['cycle']} {b['slot']}) judged "
          f"{b['windows'][0]['judged']} already and took "
          f"{len(set(b['windows'][0]['entries']) - set(a['windows'][0]['entries']))} entries the "
          f"first (c{a['cycle']} {a['slot']}) did not")
    print("test_window_backoff OK")


if __name__ == "__main__":
    main()
