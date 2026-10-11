"""7a(10) D1-D3 (TETHER_D13; R3 part 2; the reviewer 2026-10-10 23:50Z). The agent's process
states bet on GROUND outcomes and each bet settles only at a level or game ending.

  must-pass: ON, snaps.ladder seeds 5 and 7 write process bets (plan_clears, parked_explained,
     the stall described as an effect) and every one is settled, with its ground reading;
  D3-a. a settle row is written only inside retarget or end_run, never mid-level;
  D3-b. the agent's own diagnosis never settles: emptying owed_import mid-level writes no settle
     and changes no verdict (a park bet is graded by the world's grade of the slot's last bet);
  D3-c. a park bet is graded on the slot's last CHANGE after the park (the reviewer 00:14Z): a
     parked slot that never moves again settles None, where the last-bet rule read it right;
  D1. a plan bet is about the ground: the same bet settles right on "advance", wrong on "death";
  OFF/ON: every row but the process rows is identical (seq stripped), so nothing chooses from it.

    python test_d13.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter

import gamma
import gridworld
import ledger
import snaps
import tether
import world

sys.dont_write_bytecode = True

made: list = []
real_init, real_settle = tether.Agent.__init__, tether.Agent._settle_process
inside: list = []


def _init(self, *a, **k):
    real_init(self, *a, **k)
    made.append(self)


def _guarded(self, scope, how):
    caller = sys._getframe(1).f_code.co_name
    assert caller in ("retarget", "end_run"), f"D3-a: settled from {caller}"
    inside.append(caller)
    return real_settle(self, scope, how)


def _ladder(seed: int, on: bool) -> list:
    was = tether._D13
    tether._D13 = on
    made.clear()
    try:
        snaps.ladder(seed, levels=5, steps=60, n_slots=4)
        made[0].end_run("run_end")
    finally:
        tether._D13 = was
    return made[0].led.rows()


def _strip(rows):
    out = []
    for r in rows:
        if r["event"] in ("process_bet", "process_settle", "arms"):
            continue
        r = {k: v for k, v in r.items() if k != "seq"}
        r["detail"] = {k: v for k, v in r["detail"].items() if k != "seq"}
        if isinstance(r["detail"].get("shadow"), dict):          # a row index, shifted too
            r["detail"]["shadow"] = {k: v for k, v in r["detail"]["shadow"].items()
                                     if k != "recorded_before"}
        out.append(json.dumps(r, sort_keys=True, default=str))
    return out


def _agent():
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="d13"), tether.Config(), ledger.Ledger())
    ag.step()
    return ag


if __name__ == "__main__":
    tether.Agent.__init__ = _init
    tether.Agent._settle_process = _guarded
    for seed in (5, 7):
        on = _ladder(seed, True)
        bets = [r["detail"] for r in on if r["event"] == "process_bet"]
        sets = [r["detail"] for r in on if r["event"] == "process_settle"]
        assert bets and len(sets) == len(bets), (len(bets), len(sets))
        kinds = Counter(b["kind"] for b in bets)
        stalls = Counter(b["stall"]["effect"] for b in bets if "stall" in b)
        verdict = Counter((s["kind"], s["right"]) for s in sets)
        print(f"  must-pass seed {seed}: bets {dict(kinds)}, stalls {dict(stalls)}; settled "
              f"{dict(verdict)}")
        off = _ladder(seed, False)
        assert _strip(on) == _strip(off)
        print(f"  OFF/ON seed {seed}: {len(_strip(on))} rows identical but for the process rows")
    print(f"  D3-a: {len(inside)} settles, every one from {sorted(set(inside))}")
    tether.Agent.__init__ = real_init
    tether.Agent._settle_process = real_settle
    tether._D13 = True
    ag = _agent()
    slot = sorted(ag.slots)[0]
    ag._park_bet(slot, {"verdict": "under_floor", "base_bits": 3.0, "floor_bits": 9.0})
    n0 = len(ag.led)
    ag.owed_import = set()
    ag.abstained.clear()
    ag.step()
    assert not [r for r in ag.led.rows()[n0:] if r["event"] == "process_settle"]
    a1 = _agent()
    a1._park_bet(slot, {"verdict": "under_floor"})
    a1._settle_process("level", "death")
    a2 = _agent()
    a2._park_bet(slot, {"verdict": "under_floor"})
    a2.owed_import = set()
    a2._settle_process("level", "death")
    g1 = [r["detail"]["right"] for r in a1.led.rows() if r["event"] == "process_settle"]
    g2 = [r["detail"]["right"] for r in a2.led.rows() if r["event"] == "process_settle"]
    assert g1 == g2 and len(g1) == 1, (g1, g2)
    print(f"  D3-b: emptying owed_import mid-level writes no settle, and the verdict ({g1[0]}) is "
          "the world's grade either way")
    q = _agent()
    for sl in sorted(q.slots):
        q._park_bet(sl, {"verdict": "under_floor"})
    seqs = {b["slot"]: b["seq"] for b in q._process_bets}
    for _ in range(4):
        q.step()
    rows = q.led.rows()
    quiet = []
    for sl, sq in seqs.items():
        after = [r["detail"] for r in rows if r["event"] == "bet" and r["slot"] == sl
                 and r["seq"] > sq]
        if after and not float(after[-1].get("mass", 0) or 0) and all(
                a.get("actual") == a.get("from_value") for a in after):
            quiet.append(sl)
    assert quiet, "fixture: no slot stayed still after the park, so D3-c would be vacuous"
    q._settle_process("level", "death")
    got = {r["detail"]["about"]: r["detail"]["right"] for r in q.led.rows()
           if r["event"] == "process_settle"}
    assert all(got[sl] is None for sl in quiet), {sl: got[sl] for sl in quiet}
    print(f"  D3-c: {len(quiet)} parked slots never moved after the park; their last bet paid "
          f"(the old rule read right), and each settles None")
    out = []
    for how in ("advance", "death"):
        p = _agent()
        p._process_bet("plan_clears", slot, plan_no=1, need=3)
        p._settle_process("level", how)
        out.append([r["detail"]["right"] for r in p.led.rows()
                    if r["event"] == "process_settle"][0])
    assert out == [True, False], out
    print("  D1: the same plan bet settles right on 'advance' and wrong on 'death'")
    tether._D13 = False
    print("ok")
