"""R4, MEMO ADMISSION (TETHER_MEMO_ADMIT; the reviewer 2026-10-17 17:35 C, amended 23:52 (A)).

  E    the fake ARC game (12 actions, C-seed-X), the arm ON vs OFF: every row identical except the
       WORK accounting -- @budget's spent / late_asked and lookup_tiers' late_asked (a first-ask
       answer is recomputed, which is real work) -- and the @memo / @run rows; every decision
       (offer, bind, bet, mint, want) is the same, since each memo holds a pure function of its key
  A    _admit: False on a key's first ask, True on its second; always True with the arm off
  C    a boundary (retarget) clears the agent-level instance memos and keeps the asked keys; the
       instance-keyed bound memos are CLEARED under TETHER_CONSOLIDATE (one @consolidate row) and
       untouched with it OFF (the 10-15 06:01 carry; restated the reviewer 2026-10-18 05:28)
  MF   the fake and gridworld_s2 (15 steps): the agent-level memos hold FEWER entries with the arm
       ON than OFF (OFF stores every first ask); peak commit reported beside them
  H    the @memo row carries the bound memos' hit counter (lookups, hits, carried hits)

    python test_memo_admit.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.getcwd(), "conform"))
import tether
tether._AGENT_SEED = False
world_ = sys.argv[1]
led = os.path.join(tempfile.mkdtemp(), "m.jsonl")
if world_ == "fake":
    import tether_agent
    from test_entry import FakeWrapper
    captured = {}
    real = tether.Agent.end_run
    def end_run(self, how="cap"):
        captured["ag"] = self
        return real(self, how)
    tether.Agent.end_run = end_run
    tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led)
    ag = captured["ag"]
else:
    import gamma, ledger, panel, world
    g, seed = panel._gridworld("gridworld_s2")
    env = world.bind(g)
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"gate_{seed}"), tether.Config(),
                      ledger.Ledger(path=led))
    for _ in range(15):
        ag.step()
sizes = {"reach_index": len(ag._reach_index), "reach_verdicts": len(ag._reach_verdicts),
         "reach_fold": len(ag._reach_fold), "compile": len(ag._compile_cache),
         "units_for": len(ag._units_for_memo)}
print("RESULT", json.dumps({"sizes": sizes, "ledger": led}))
'''


def child(world_: str, arm: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "TETHER_MEMO_ADMIT": arm,
                "TETHER_MEMO_CLEAR": "1"})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, world_], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    out = json.loads(next(x for x in p.stdout.splitlines() if x.startswith("RESULT "))[7:])
    with open(out["ledger"], encoding="utf-8") as fh:
        out["rows"] = [json.loads(x) for x in fh if x.strip()]
    return out


WORK = {("@budget", "spent"), ("@budget", "late_asked"), ("*", "late_asked")}


def main() -> int:
    on, off = child("fake", "1"), child("fake", "0")
    a = [r for r in on["rows"] if r["slot"] not in ("@run", "@memo")]
    b = [r for r in off["rows"] if r["slot"] not in ("@run", "@memo")]
    assert len(a) == len(b), (len(a), len(b))
    work = 0
    for x, y in zip(a, b, strict=True):
        assert (x["cycle"], x["step"], x["slot"], x["event"]) == (
            y["cycle"], y["step"], y["slot"], y["event"]), (x, y)
        diff = {k for k in set(x["detail"]) | set(y["detail"])
                if x["detail"].get(k) != y["detail"].get(k)}
        assert all((x["slot"] if x["slot"] == "@budget" else "*", k) in WORK for k in diff), (
            x["slot"], x["event"], diff)                                                       # E
        work += bool(diff)
    print(f"E fake: {len(a)} rows in the same order; {work} differ ONLY in work accounting "
          "(@budget spent / late_asked, lookup_tiers late_asked); every decision row identical")

    sys.path.insert(0, HERE)
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    was = tether._MEMO_ADMIT, tether._MEMO_CLEAR
    tether._MEMO_ADMIT, tether._MEMO_CLEAR = True, True     # the split (00:10): ADMIT defaults OFF
    assert ag._admit("compile", "k") is False and ag._admit("compile", "k") is True          # A
    tether._MEMO_ADMIT = False
    assert ag._admit("compile", "k2") is True
    tether._MEMO_ADMIT = True
    print("A first ask: not stored; second ask: stored; the arm off: always stored")
    for _ in range(6):
        env.observe()
        ag.step()
    ag._reach_index["x"] = ag._compile_cache["x"] = ag._reach_fold["x"] = 1
    asked = {m: len(v) for m, v in ag._seen_keys.items()}
    exempt = (len(tether._BOUND_MEMO), len(tether._BOUND_SLOT_MEMO), len(tether._PAIRS_SEEN))
    ag.retarget(env, 1, how=tether.ADVANCE)
    assert not ag._reach_index and not ag._compile_cache and not ag._reach_fold, "C: not cleared"
    assert {m: len(v) for m, v in ag._seen_keys.items()} == asked, "C: asked keys lost"       # C
    now = (len(tether._BOUND_MEMO), len(tether._BOUND_SLOT_MEMO), len(tether._PAIRS_SEEN))
    if tether._CONSOLIDATE:
        assert sum(exempt) and now == (0, 0, 0), ("C: the bound memos not cleared", exempt, now)
    else:
        assert now == exempt, "C: an exempt memo changed"
    tether._MEMO_ADMIT, tether._MEMO_CLEAR = was
    print(f"C the boundary cleared the agent-level memos, kept the asked keys {asked}; the bound "
          f"memos {exempt} -> {now} (TETHER_CONSOLIDATE {tether._CONSOLIDATE})")

    for w in ("fake", "gridworld"):
        s_on = on["sizes"] if w == "fake" else child(w, "1")["sizes"]
        s_off = off["sizes"] if w == "fake" else child(w, "0")["sizes"]
        assert sum(s_on.values()) < sum(s_off.values()), (w, s_on, s_off)                     # MF
        print(f"MF {w}: agent-level memo entries ON {sum(s_on.values())} {s_on} against OFF "
              f"{sum(s_off.values())} {s_off}")
    m = [r["detail"] for r in on["rows"] if r["slot"] == "@memo"]
    assert m and set(m[-1]["hits"]) >= {"bound_slot", "bound_slot_hit", "bound_slot_hit_carried",
                                        "bound_whole_hit_carried"}, m                      # H
    print(f"H the @memo row ({m[-1]['at']}) carries the bound memos' hit counter {m[-1]['hits']}")
    print("memo_admit: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
