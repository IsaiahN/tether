"""(C), THE EXACT SPEED BUILD (TETHER_HYP_MOVABLE_ONCE, TETHER_HYP_MOVABLE_CHECK; the reviewer
2026-10-23 05:00, 05:25; Isaiah "i like c and then a"). gridworld_arc_s1, the agent and hash seeds
pinned, 30 steps, each arm state in its own process (arms resolve at import).

  P   precondition: _movable_by runs INSIDE _goal_hypothesis on this world (else nothing is tested)
  E   ON and OFF write the same ledger, every row (timing keys masked: none are expected here)
  S   ON reads agency.contingent() at most once per _goal_hypothesis call that reaches _movable_by;
      OFF reads it once per _movable_by call inside the scope
  C   CHECK (ON + TETHER_HYP_MOVABLE_CHECK=1): every scoped lookup re-read per call, no raise
  MF  CHECK with a planted stale contingent set (one slot added to the scoped read) RAISES
      "HYP_MOVABLE_ONCE stale: contingent"; the same plant with CHECK off does not raise

    python tests/test_hyp_movable_once.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import json, os, sys
sys.dont_write_bytecode = True
tree, led, mode = sys.argv[1:4]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, panel, tether, world
from instruments import Agency

n = {"gh": 0, "gh_mv": 0, "mv_in": 0, "cont_in": 0}
inside = [False]
_c = Agency.contingent
def contingent(self):
    if inside[0]:
        n["cont_in"] += 1
    return _c(self)
Agency.contingent = contingent
_gh = tether.Agent._goal_hypothesis
def gh(self, before):
    n["gh"] += 1
    m0 = n["mv_in"]
    inside[0] = True
    try:
        return _gh(self, before)
    finally:
        inside[0] = False
        n["gh_mv"] += n["mv_in"] > m0
tether.Agent._goal_hypothesis = gh
_mv = tether.Agent._movable_by
planted = [False]
def mv(self, slot):
    if inside[0]:
        n["mv_in"] += 1
    once = getattr(self, "_mv_once", None)
    if mode == "mf" and once and not planted[0]:
        once["moving"].add("o99.planted")
        planted[0] = True
    return _mv(self, slot)
tether.Agent._movable_by = mv
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="mvonce"), tether.Config(),
                  ledger.Ledger(path=led))
raised = None
try:
    for _ in range(30):
        ag.step()
except AssertionError as e:
    raised = str(e)
print(json.dumps({"n": n, "raised": raised, "on": tether._HYP_MOVABLE_ONCE,
                  "check": tether._HYP_MOVABLE_CHECK}))
'''


def child(tmp: str, name: str, mode: str, **arms: str) -> tuple[dict, list]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0", **arms)
    led = os.path.join(tmp, name + ".jsonl")
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, str(_repo.ROOT), led, mode], env=env,
                         capture_output=True, text=True, timeout=600, cwd=str(_repo.ROOT))
    assert out.returncode == 0, out.stderr[-3000:]
    rows = []
    if os.path.exists(led):
        with open(led, encoding="utf-8") as fh:
            rows = [json.loads(x) for x in fh]
    return json.loads(out.stdout.strip().splitlines()[-1]), rows


def masked(rows: list) -> list:
    keep = []
    for r in rows:
        d = r.get("detail") or {}
        if r.get("slot") == "@run" and r.get("event") == "arms":
            continue    # the arms row lists the arm states, which differ by construction
        keep.append((r.get("cycle"), r.get("step"), r.get("slot"), r.get("event"),
                     json.dumps({k: v for k, v in d.items() if not k.endswith("_s")},
                                sort_keys=True, default=str)))
    return keep


def main() -> None:
    tmp = tempfile.mkdtemp(prefix="mvonce_")
    on, r_on = child(tmp, "on", "plain", TETHER_HYP_MOVABLE_ONCE="1")
    off, r_off = child(tmp, "off", "plain", TETHER_HYP_MOVABLE_ONCE="0")
    assert on["on"] and not off["on"], (on, off)
    assert on["n"]["mv_in"] > 0 and on["n"]["gh_mv"] > 0, ("P: no _movable_by inside", on)
    print(f"  P: _goal_hypothesis {on['n']['gh']} calls, {on['n']['gh_mv']} reaching _movable_by, "
          f"{on['n']['mv_in']} scoped _movable_by calls")
    assert masked(r_on) == masked(r_off), "E: the ledgers differ"
    print(f"  E: ON and OFF ledgers equal, {len(masked(r_on))} rows (the arms row aside)")
    assert on["n"]["cont_in"] <= on["n"]["gh_mv"], ("S ON", on["n"])
    assert off["n"]["cont_in"] == off["n"]["mv_in"], ("S OFF", off["n"])
    print(f"  S: contingent() inside the scope: ON {on['n']['cont_in']} (calls reaching it "
          f"{on['n']['gh_mv']}); OFF {off['n']['cont_in']} (= its {off['n']['mv_in']} lookups)")
    ck, r_ck = child(tmp, "check", "plain", TETHER_HYP_MOVABLE_ONCE="1",
                     TETHER_HYP_MOVABLE_CHECK="1")
    assert ck["check"] and ck["raised"] is None, ("C", ck)
    assert masked(r_ck) == masked(r_on), "C: CHECK changed the ledger"
    print(f"  C: CHECK re-read {ck['n']['mv_in']} scoped lookups, no raise, ledger equal to ON")
    mf, _ = child(tmp, "mf", "mf", TETHER_HYP_MOVABLE_ONCE="1", TETHER_HYP_MOVABLE_CHECK="1")
    assert mf["raised"] and "HYP_MOVABLE_ONCE stale: contingent" in mf["raised"], ("MF", mf)
    nc, _ = child(tmp, "mf_nocheck", "mf", TETHER_HYP_MOVABLE_ONCE="1")
    assert nc["raised"] is None, ("MF control", nc)
    print(f"  MF: a planted stale slot RAISES under CHECK ({mf['raised'][:60]}); with CHECK off "
          "it does not")
    print("hyp_movable_once: OK")


if __name__ == "__main__":
    main()
