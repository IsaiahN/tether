"""S0, THE PER-CANDIDATE WALK, NOW B1's WITNESS (TETHER_HYP_DRAW, TETHER_HYP_ORDER; the reviewer
2026-10-20 18:18 CDT; r1459, r1469, r1470, r1471). gridworld_arc_s1, the agent seed pinned, one
process, the arms toggled at the call.

  (1a) THE ORDER REACHES THE ORACLE'S WANT, on test_goal_hyp's world (25 steps). Before every
       proposal an oracle copy runs the EAGER path (every member route-checked), recording which
       candidates were routable and the ranked list (key groups = runs of one sort key). The
       want is in the FIRST key group holding a routable member -- the walk never leaves a group
       that routes (r1459's red: the old want ignored that cut). Under B1 the want is that group's
       best routable by (class, turnable, text); the real proposal must pick it after exactly the
       earlier groups plus its place in B1's order. A draw copy (B1 OFF) must pick the draw's
       first routable in the same group. Over all passes B1 reaches its want no later than the
       draw order would, and never picks a worse class than the draw.
  (1b) 50 PLANTED CONDITIONS of one price in bits, every tenth routable. They span more than one
       key group, so the walk is the first key group holding a routable: B1 picks its first
       routable in (class, turnable, text) order at that check; the draw picks the lowest-hash
       routable at its place (< 50); the eager path checks every member through that group.
  The OFF arm's bit-for-bit identity (2) and the other A1 sites (3) are ledger runs, not here.

    python tests/test_hyp_draw.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import copy, json, sys
from collections import Counter
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import compile_term, frontier, gamma, ledger, panel, tether, world
tether._HYP_LEARN = False         # B1's witness: order on, learn off (r1475)
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


def classer(ag, rs):
    """B1's tier 1 read from outside, as the body reads it: live residual, routable, the rest;
    the better of the subject and, for a one-atom order or mirror comparison, the operand."""
    live = {k for k, v in ag._outstanding.items() if v > 0}

    def cls(sl):
        return 0 if sl in live else (1 if rs is not None and sl in rs else 2)

    def xcls(x):
        c = x[2]
        cl = cls(c.slot)
        if cl and isinstance(c, compile_term.Compiled) and c.operand \
                and len(c.term.atoms) == 1 and c.term.atoms[0].name in compile_term.SWAP:
            cl = min(cl, cls(c.operand))
        return cl
    return xcls


FLIP = {">": "<", "<": ">", "==": "==", "!=": "!="}


def converse(t):
    """The other spelling of a two-slot comparison, the alternate a hold may fall back on."""
    p = (t or "").split(" ")
    return f"{p[2]} {FLIP[p[1]]} {p[0]}" if len(p) == 3 and p[1] in FLIP else None


def b1_order(ag, group, xcls, snap=None):
    """B1 as the body orders it (r1473, r1474, r1477, r1478): class, times parked, turnable,
    rounds (each subject's least-checked, the least-tried subject first), the explore draw; no
    name. snap: the tried counts the pass saw, when the pass has already run."""
    cset = set(ag.agency.contingent()) if tether._GOAL_CONTINGENT else set()
    pk = ag._parked_n
    st, ck = snap if snap is not None else (ag._subj_tried, ag._cand_checked)
    dpos = {t: i for i, t in enumerate(frontier.draw_order(
        [x[1] for x in group], f"{ag.cycle}:goal_hypothesis:explore", ag.draw_seed))}

    def pre(x):
        return (xcls(x), pk[x[3]], x[2].slot not in cset)
    n, rr = Counter(), {}
    for x in sorted(group, key=lambda x: (pre(x), x[2].slot, ck[x[3]], dpos[x[1]])):
        rr[id(x)] = n[(pre(x), x[2].slot)]
        n[(pre(x), x[2].slot)] += 1
    return [x[1] for x in sorted(group, key=lambda x: (pre(x), rr[id(x)], st[x[2].slot],
                                                       ck[x[3]], dpos[x[1]]))]


def draw_order(ag, group):
    cset = set(ag.agency.contingent()) if tether._GOAL_CONTINGENT else set()
    by = {x[1]: x for x in group}
    order = frontier.draw_order([x[1] for x in group], DKEY.format(ag.cycle), ag.draw_seed)
    if any(by[t][2].slot in cset for t in order):
        order = [t for t in order if by[t][2].slot in cset] + [t for t in order
                                                                if by[t][2].slot not in cset]
    return order


def lazy(ag, before, order_on):
    cp = copy.deepcopy(ag)
    cp._oracle = True
    tether._HYP_ORDER = order_on
    try:
        orig(cp, before)
    finally:
        tether._HYP_ORDER = True
    return last_pick(cp)


def wrapped(self, before):
    if getattr(self, "_oracle", False):
        return orig(self, before)
    cp = copy.deepcopy(self)
    cp._oracle = True
    ok_by_id, ranked, rs, ok_objs = {}, [], [], []
    real_hold, real_fc, real_rfs = cp._hyp_hold, cp._family_counts, cp._route_first_set

    def hold(key, c, b, *rt):        # _hyp_hold(key, c, before, routable=None) since de70db0
        link, why = real_hold(key, c, b, *rt)
        ok_by_id[id(c)] = link is not None
        if link is not None:
            ok_objs.append(c)        # an alternate spelling's hold (r1439's _try_alt) counts
        return link, why

    def fc(r, *a, **k):
        ranked.extend(r)
        return real_fc(r, *a, **k)

    def rfs(b):
        out = real_rfs(b)
        rs.append(out)
        return out
    cp._hyp_hold, cp._family_counts, cp._route_first_set = hold, fc, rfs
    tether._HYP_DRAW = False
    try:
        orig(cp, before)
    finally:
        tether._HYP_DRAW = True
    xcls = classer(self, rs[0] if rs else None)
    tx = text_of(cp)                 # after the run: an alternate is compiled during it
    ok_text = {tx(c) for c in ok_objs} - {None}

    def ok(x):                        # its own spelling held, or its converse (the alternate)
        return ok_by_id.get(id(x[2])) or converse(x[1]) in ok_text
    groups, prior = [], 0
    for x in ranked:
        if groups and groups[-1][0][0] == x[0]:
            groups[-1].append(x)
        else:
            groups.append([x])
    first = None
    for g in groups:
        if any(ok(x) for x in g):
            first = g
            break
        prior += len(g)
    want = got = dwant = dgot = None
    if first is not None:
        routable = {x[1] for x in first if ok(x)}
        bo, do = b1_order(self, first, xcls), draw_order(self, first)
        want = next(t for t in bo if t in routable)
        dwant = next(t for t in do if t in routable)
        dgot = lazy(self, before, False).get("pick")
        by = {x[1]: x for x in first}
        pairs.append({"c": self.cycle, "want": want, "dwant": dwant, "dgot": dgot,
                      "want_at_b1": prior + bo.index(want) + 1,
                      "want_at_draw": prior + do.index(want) + 1,
                      "dwant_at": prior + do.index(dwant) + 1,
                      "cls": xcls(by[want]), "dcls": xcls(by[dwant]), "group": len(first)})
    out = orig(self, before)
    d = last_pick(self)
    if first is not None:
        g_ = d.get("pick")
        pairs[-1].update(got=(pairs[-1]["want"] if g_ == converse(pairs[-1]["want"]) else g_),
                         got_text=g_, lazy=d.get("checked"))
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

    def hold(key, c, b, *_rt):       # _hyp_hold's signature since de70db0
        t = tx(c)
        calls.append(t)
        if t in routable:
            return ({"linked": True, "slots": [c.slot], "route": "x", "displaced": [],
                     "_held": {}}, None)
        return None, "no route"
    return hold


RS, RK = [], []


def propose(mode, routable):
    """mode: "b1" (the order), "draw" (B1 OFF), "eager" (S0 OFF, every member checked)."""
    calls.clear()
    RS.clear()
    RK.clear()
    ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, {}, None
    ag._hyp_hold = stub(routable)
    real_rfs, real_fc = tether.Agent._route_first_set, tether.Agent._family_counts

    def rfs(b):
        out = real_rfs(ag, b)
        RS.append(out)
        return out

    def fc(r, *a, **k):
        RK.extend(r)
        return real_fc(ag, r, *a, **k)
    ag._route_first_set, ag._family_counts = rfs, fc
    tether._HYP_DRAW, tether._HYP_ORDER = mode != "eager", mode == "b1"
    try:
        ag._hyp_propose(before)
    finally:
        tether._HYP_DRAW, tether._HYP_ORDER = True, True
        del ag._hyp_hold, ag._route_first_set, ag._family_counts
    return last_pick(ag), list(calls)


_d, pool = propose("eager", set())               # every open condition, checked
# the draw is among SINGLE candidates: a group (box 3) or a pair has no compiled text here
pool = [t for t in pool if t is not None]
bits = {}
for t in pool:
    c = ag._compile_cache[t]
    bits.setdefault(round(term_bits(ag.gamma.length(c.term), ag.gamma.alphabet), 6), []).append(t)
big = sorted(max(bits.values(), key=len))[:50]
ag._inv_conditions = lambda _b, **_k: list(big)
routable = set(big[::10])
snb = (Counter(ag._subj_tried), Counter(ag._cand_checked))   # the tried counts B1's pass saw
b1, b1_calls = propose("b1", routable)
xcls = classer(ag, RS[0] if RS else None)
on, on_calls = propose("draw", routable)
off, off_calls = propose("eager", routable)
# the planted 50 share bits, not the whole key: the walk is the first key group with a routable
groups, prior = [], 0
for x in RK:
    if groups and groups[-1][0][0] == x[0]:
        groups[-1].append(x)
    else:
        groups.append([x])
for g in groups:
    if any(x[1] in routable for x in g):
        xs = g
        break
    prior += len(g)
border = b1_order(ag, xs, xcls, snb)
bwant = next(t for t in border if t in routable)
order = draw_order(ag, xs)
want = next(t for t in order if t in routable)
print(json.dumps({"pairs": pairs, "group": len(big), "routable": sorted(routable),
                  "first_group": len(xs), "prior": prior,
                  "bwant": bwant, "bwant_at": prior + border.index(bwant) + 1,
                  "b1": {"pick": b1.get("pick"), "checked": b1.get("checked"),
                         "calls": len(b1_calls)},
                  "want": want, "want_at": prior + order.index(want) + 1,
                  "on": {"pick": on.get("pick"), "checked": on.get("checked"),
                         "calls": len(on_calls), "wall_s": on.get("wall_s"),
                         "group_n": on.get("group_n")},
                  "off": {"pick": off.get("pick"), "checked": off.get("checked"),
                          "calls": len(off_calls), "wall_s": off.get("wall_s")}}, default=str))
'''


def main() -> None:
    here = _repo.ROOT
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, here], env=env, capture_output=True,
                         text=True, timeout=1200, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    r = json.loads(out.stdout.strip().splitlines()[-1])
    live = r["pairs"]
    assert live, r["pairs"]
    # B1 picks the oracle's want after exactly the earlier groups and its place in the order
    assert all(p["got"] == p["want"] and p["lazy"] == p["want_at_b1"] for p in live), live
    # B1 OFF is the draw, unchanged: its first routable in the same group
    assert all(p["dgot"] == p["dwant"] for p in live), live
    # r1459: the order reaches its want no later than the draw order would, and never picks a
    # worse class than the draw
    assert sum(p["want_at_b1"] for p in live) <= sum(p["want_at_draw"] for p in live), live
    assert all(p["cls"] <= p["dcls"] for p in live), live
    assert r["group"] == 50, r["group"]
    assert r["b1"]["pick"] == r["bwant"] and r["b1"]["checked"] == r["bwant_at"], r
    assert r["on"]["pick"] == r["want"] and r["on"]["checked"] == r["want_at"] < 50, r
    # the eager path checks every member of the groups it walks, through the first that routes
    assert r["off"]["checked"] == r["prior"] + r["first_group"] < 50, r
    print(f"test_hyp_draw: pass ((1a) {len(live)} proposals: B1 picked the want at "
          f"{[p['want_at_b1'] for p in live]}, where the draw order puts it at "
          f"{[p['want_at_draw'] for p in live]}; the draw's own picks at "
          f"{[p['dwant_at'] for p in live]}; classes B1 {[p['cls'] for p in live]} vs draw "
          f"{[p['dcls'] for p in live]}; (1b) tie group 50, routable {len(r['routable'])}: B1 "
          f"picked at check {r['b1']['checked']}, the draw at {r['on']['checked']}, eager "
          f"checked {r['off']['checked']})")


if __name__ == "__main__":
    main()
