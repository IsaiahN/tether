"""S0, THE PER-CANDIDATE DRAW (TETHER_HYP_DRAW; the reviewer 2026-10-20 18:18 CDT).
gridworld_arc_s1, the agent seed pinned, one process, the arm toggled at the call.

  (1a) LAZY == EAGER UNDER THE NEW DRAW, on test_goal_hyp's world (25 steps): before every
       proposal an oracle copy of the agent runs the EAGER path (every tied member route-checked)
       and records which were routable; the real proposal, lazy, must pick the lowest-hash
       routable of them (frontier.draw_order), with checks lazy <= eager on each, < in total.
  (1b) A PLANTED TIE GROUP of 50 (the board's own conditions, one rank group), the routable
       members known (every tenth): the lazy pick is the lowest-hash routable, found at its
       place in the hash order (checks < 50); OFF checks all 50.
  The OFF arm's bit-for-bit identity (2) and the other A1 sites (3) are ledger runs, not here.

    python test_hyp_draw.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

PROBE = r'''
import copy, json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import frontier, gamma, ledger, panel, tether, world
from tether import term_bits

DKEY = "{}:goal_hypothesis:None"


def fresh():
    env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="hypdraw"), tether.Config(),
                        ledger.Ledger())


def text_of(ag):
    rev = {id(v): k for k, v in ag._compile_cache.items()}
    return lambda c: rev.get(id(c))


def last_pick(ag):
    rows = [r["detail"] for r in ag.led.rows() if r["event"] == "goal_hypotheses"]
    return rows[-1] if rows else {}


# (1a) the oracle around every real proposal
orig = tether.Agent._hyp_propose
pairs = []


def wrapped(self, before):
    if getattr(self, "_oracle", False):
        return orig(self, before)
    cp = copy.deepcopy(self)
    cp._oracle = True
    seen = {}
    real_hold = cp._hyp_hold

    def hold(key, c, b):
        link, why = real_hold(key, c, b)
        seen[text_of(cp)(c)] = link is not None
        return link, why
    cp._hyp_hold = hold
    tether._HYP_DRAW = False
    try:
        orig(cp, before)
    finally:
        tether._HYP_DRAW = True
    routable = [t for t, ok in seen.items() if ok]
    want = (frontier.draw_order(routable, DKEY.format(self.cycle), self.draw_seed)[0]
            if routable else None)
    out = orig(self, before)
    d = last_pick(self)
    pairs.append({"c": self.cycle, "want": want, "got": d.get("pick") if routable else None,
                  "lazy": d.get("checked"), "eager": len(seen), "routable": len(routable)})
    return out


tether.Agent._hyp_propose = wrapped
ag = fresh()
for _ in range(25):
    ag.step()
tether.Agent._hyp_propose = orig

# (1b) a planted tie group of 50
ag = fresh()
for _ in range(6):
    ag.step()
if ag._hyp is not None:
    ag._hyp_end("lost")
before = ag.env.observe()
calls = []


def stub(routable):
    tx = text_of(ag)

    def hold(key, c, b):
        t = tx(c)
        calls.append(t)
        if t in routable:
            return ({"linked": True, "slots": [c.slot], "route": "x", "displaced": [],
                     "_held": {}}, None)
        return None, "no route"
    return hold


def propose(on, routable):
    calls.clear()
    ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, {}, None
    ag._hyp_hold = stub(routable)
    tether._HYP_DRAW = on
    try:
        ag._hyp_propose(before)
    finally:
        tether._HYP_DRAW = True
        del ag._hyp_hold
    return last_pick(ag), list(calls)


_d, pool = propose(False, set())                 # every open condition, checked
bits = {}
for t in pool:
    c = ag._compile_cache[t]
    bits.setdefault(round(term_bits(ag.gamma.length(c.term), ag.gamma.alphabet), 6), []).append(t)
big = sorted(max(bits.values(), key=len))[:50]
ag._inv_conditions = lambda _b: list(big)
routable = set(big[::10])
on, on_calls = propose(True, routable)
off, off_calls = propose(False, routable)
order = frontier.draw_order(big, DKEY.format(ag.cycle), ag.draw_seed)
want = next(t for t in order if t in routable)
print(json.dumps({"pairs": pairs, "group": len(big), "routable": sorted(routable),
                  "want": want, "want_at": order.index(want) + 1,
                  "on": {"pick": on.get("pick"), "checked": on.get("checked"),
                         "calls": len(on_calls), "wall_s": on.get("wall_s"),
                         "group_n": on.get("group_n")},
                  "off": {"pick": off.get("pick"), "checked": off.get("checked"),
                          "calls": len(off_calls), "wall_s": off.get("wall_s")}}, default=str))
'''


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, here], env=env, capture_output=True,
                         text=True, timeout=1200, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    r = json.loads(out.stdout.strip().splitlines()[-1])
    live = [p for p in r["pairs"] if p["want"] is not None]
    assert live, r["pairs"]
    assert all(p["got"] == p["want"] for p in live), live
    assert all(p["lazy"] <= p["eager"] for p in live), live
    assert sum(p["lazy"] for p in live) < sum(p["eager"] for p in live), live
    assert r["group"] == 50, r["group"]
    assert r["on"]["pick"] == r["want"] and r["on"]["checked"] == r["want_at"] < 50, r
    assert r["off"]["checked"] == 50 and r["off"]["wall_s"] is None, r["off"]
    print(f"test_hyp_draw: pass ((1a) {len(live)} proposals, every lazy pick the lowest-hash "
          f"routable; checks lazy {[p['lazy'] for p in live]} vs eager "
          f"{[p['eager'] for p in live]}; (1b) tie group 50, routable {len(r['routable'])}, "
          f"ON picked the lowest-hash routable at check {r['on']['checked']}, OFF checked "
          f"{r['off']['checked']}; ON wall {r['on']['wall_s']} s)")


if __name__ == "__main__":
    main()
