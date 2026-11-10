"""TETHER_D5_NESTED (the reviewer 2026-11-10 r1626 (N), r1627): (N1) a live split's leaf part is cut
on its own misses; (N2) a leaf's demotion leaves the outer split live. On gridworld_s0 after one
step, a synthetic history of o0.row under the split P = "KNOWN_EFFECT ?.col" (part A the null,
part B dec = row - 1): up rows move the row down (known "?.row-"), down rows up ("?.row+").

  (a) MUST-FAIL: dec's miss on a down row is searched over its own rows and gives a nested
      candidate "KNOWN_EFFECT ?.row-"; a held up row is no news; the next down miss confirms it;
      the split at MINT mints a new part on the down rows only (the mint's row filter), and the
      walk binds the new part on a down step (dec's prediction its shadow) and dec on an up step.
      OFF: no candidate, no inner node;
  (b) MUST-FAIL: dec's demotion leaves the outer split live (part_demoted, a re-mint queued, and
      the re-mint runs at MINT); OFF: dissolved;
  (b') part A's demotion still dissolves, ON and OFF;
  (c) the outer split is still broken by its own shadow, ON;
  (e) a carried inner condition loads apart from the top-level ones, is tried first inside a
      matching outer split, and is not read by a top-level cut.

    python tests/test_d5_nested.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
import gamma, ledger, tether, world
from conform import panel
S, P = "o0.row", "KNOWN_EFFECT ?.col"
g, seed = panel._gridworld("gridworld_s0")
env = world.bind(g)
def agent():
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"t_{seed}"), tether.Config(),
                      ledger.Ledger())
    ag.step()
    return ag
def row(ag, act, r):
    b = dict(g.state)
    b[S] = r
    a = dict(b)
    a[S] = (r - 1) % 5 if act == "up" else (r + 1) % 5
    ag._kn_eff[id(b)] = frozenset({"?.row", "?.row-" if act == "up" else "?.row+"})
    return (b, act, a, None, None)
def d5(ag, n0):
    return [[x["event"], x["detail"].get("P"), x["detail"].get("nested")]
            for x in ag.led.rows()[n0:] if x["slot"] == "@d5"]
def settle_step(ag, act, r, name="dec"):
    t = row(ag, act, r)
    ag.trace.append(t)
    ag._kn_eff_now = ag._kn_eff[id(t[0])]
    ag._pred_by = {S: name}
    ag.bound[S] = name
    pred = (r - 1) % 5
    n0 = len(ag.led.rows())
    ag.settle({S: tether.SlotResidual(S, tether.TRANSITION, pred, t[2][S],
                                      0.0 if pred == t[2][S] else 2.32)})
    return d5(ag, n0), t[2][S]
out = {}
ag = agent()
ag.trace, r = [], 2
for act in ["up", "down", "up", "down", "up", "down", "up"]:
    ag.trace.append(row(ag, act, r))
    r = ag.trace[-1][2][S]
ag._parts = {S: {"P": P, "A": tether.NULL_MAKER, "B": "dec"}}
ag._d5_rows = {S: [(i, "dec") for i in range(7)]}
out["cut"], r = settle_step(ag, "down", r)
out["up"], r = settle_step(ag, "up", r)
out["confirm"], r = settle_step(ag, "down", r)
seen, real_mint = [], ag.mint
def spy(s):
    f = ag._row_filter.get(s)
    seen.append([t[1] for t in ag.history(s) if f is None or f(t)])
    return real_mint(s)
ag.mint = spy
n0 = len(ag.led.rows())
ag._d5_splits()
del ag.mint
out["split"] = d5(ag, n0)
out["filter"] = seen[:1]
out["inner"] = (ag._parts[S].get("inner") or {}).get("A")
t = row(ag, "down", 1)
ag._kn_eff_now = ag._kn_eff[id(t[0])]
ag._d5_select([S], t[0], "down")
out["walk_down"] = [ag.bound.get(S), ag._shadow_in.get(S)]
t = row(ag, "up", 3)
ag._kn_eff_now = ag._kn_eff[id(t[0])]
ag._d5_select([S], t[0], "up")
out["walk_up"] = ag.bound.get(S)
inner_b = (ag._parts[S].get("inner") or {}).get("B")
out["inner_b"] = inner_b
for case, name, a_name in (("b", "dec", tether.NULL_MAKER), ("bA", "inc", "inc")):
    ag2 = agent()
    ag2.trace, ag2._d5_rows = [], {S: []}
    ag2._parts = {S: {"P": P, "A": a_name, "B": "dec"}}
    ag2.gamma.refute = lambda *a, **k: True
    ag2.gamma.is_settled = lambda *a, **k: True
    b = dict(g.state)
    b[S] = 2
    ag2._kn_eff[id(b)] = frozenset({"?.row", "?.row+"} if case == "b" else {"?.col", "?.col+"})
    a = dict(b)
    a[S] = 3 if case == "b" else 2
    ag2.trace.append((b, "down" if case == "b" else "right", a, None, None))
    ag2._kn_eff_now = ag2._kn_eff[id(b)]
    ag2._pred_by = {S: name}
    ag2.bound[S] = name
    n0 = len(ag2.led.rows())
    ag2.settle({S: tether.SlotResidual(S, tether.TRANSITION, 1, a[S], 2.32)})
    out[case] = d5(ag2, n0) + [S in ag2._parts, dict(ag2._d5_remint)]
    if case == "b":
        n0 = len(ag2.led.rows())
        ag2._d5_splits()
        out["remint"] = [x["event"] for x in ag2.led.rows()[n0:] if x["slot"] == "@d5"]
ag3 = agent()
ag3.trace = [row(ag3, "down", 2)]
ag3._parts = {S: {"P": P, "A": tether.NULL_MAKER, "B": "dec"}}
ag3._shadow[S] = 3
ag3._pred_by = {S: "dec"}
n0 = len(ag3.led.rows())
ag3.settle({S: tether.SlotResidual(S, tether.TRANSITION, 1, 3, 2.32)})
out["c"] = [x[0] for x in d5(ag3, n0)] + [S in ag3._parts]
ag4 = agent()
sk = ag4._kind_key(S)
first = "KNOWN_EFFECT ?.zz-"
ag4._reinvent_carried([
    {"kind": "condition", "name": "x_1", "slot_kind": sk, "P": ag4._p_kind(first),
     "within": ag4._p_kind(P)},
    {"kind": "condition", "name": "x_2", "slot_kind": sk, "P": ag4._p_kind("KNOWN_EFFECT ?.dcol")}])
out["e_load"] = [len(ag4._cond_in), len(ag4._cond_in_within)]
ag4.trace, r = [], 2
for act in ["up", "down", "up", "down", "up", "down", "up", "down"]:
    ag4.trace.append(row(ag4, act, r))
    if act == "up":
        ag4._kn_eff[id(ag4.trace[-1][0])] |= {"?.zz-"}
    r = ag4.trace[-1][2][S]
ag4._d5_rows = {S: [(i, "dec") for i in range(8)]}
inside = ag4._d5_cut(S, "dec", (P,))
top = ag4._d5_cut(S, "dec")
out["e_order"] = [inside[0] if inside else None, top[0] if top else None]
print(json.dumps(out, default=str))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_D5_NESTED="1" if on else "0", TETHER_D5_ACTION="1",
               TETHER_CONDITION_CARRY="1", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=_repo.ROOT, timeout=900)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    on, off = _run(True), _run(False)
    nest = ["KNOWN_EFFECT ?.row-", True]
    assert on["cut"] == [["cut_candidate", *nest]] and on["up"] == [], on
    assert on["confirm"] == [["cut_confirmed", *nest]], on
    assert on["split"] == [["split", *nest]] and on["inner"] == "dec", on
    assert on["filter"] == [["down"] * 5], on
    assert on["walk_down"][0] == on["inner_b"] and on["walk_down"][1], on
    assert on["walk_up"] == "dec", on
    assert off["cut"] == [] and off["confirm"] == [] and off["split"] == [], off
    assert off["inner"] is None, off
    print(f"  (a) inner cut {on['cut'][0][1]} -> confirmed -> split; new part {on['inner_b']} "
          f"minted on {on['filter'][0]}; walk: down -> new part (shadow {on['walk_down'][1]}), "
          f"up -> dec. OFF: no candidate, no inner node (MUST-FAIL)")
    assert on["b"][0][0] == "part_demoted" and on["b"][1] is True and on["b"][2], on
    assert on["remint"] == ["part_reminted"], on
    assert off["b"][0][0] == "dissolved" and off["b"][1] is False, off
    print(f"  (b) leaf demoted: ON {on['b'][0][0]}, split live, re-mint {on['remint']}; "
          f"OFF {off['b'][0][0]} (MUST-FAIL)")
    for d in (on, off):
        assert d["bA"][0][0] == "dissolved" and d["bA"][1] is False, d
    print("  (b') part A demoted: dissolved, ON and OFF")
    assert on["c"] == ["partition_broken", False], on
    print("  (c) the outer shadow right on a not-P row: partition_broken, ON")
    assert on["e_load"] == [1, 1], on
    assert on["e_order"] == ["KNOWN_EFFECT ?.zz-", "KNOWN_EFFECT ?.row-"], on
    print(f"  (e) a carried inner condition loads apart ({on['e_load']}); inside the split "
          f"{on['e_order'][0]} first, at top level {on['e_order'][1]} (not read there)")
    print("d5 nested: OK")
