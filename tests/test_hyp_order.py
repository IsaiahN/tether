"""B1, THE ORDER INSIDE A KEY GROUP (TETHER_HYP_ORDER; the reviewer 2026-11-08 r1443, r1470, r1471).
gridworld_arc_s1, the agent seed pinned, every hold refused so the whole group is walked.

O1  the walk inside one key group is S-class first (a live residual, then routable, then the
    rest), then turnable, then the text -- the member the hash draw puts LAST is made the live
    one, so it is checked FIRST
O2  the group's membership is the same under B1 and the draw (B1 orders; it admits nothing)
MF  the arm OFF: the draw order, which checks that live member last

    python tests/test_hyp_order.py
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
tree = sys.argv[1]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import compile_term, frontier, gamma, ledger, panel, tether, world
from collections import Counter


class H:
    """test_hyp_draw's reads of B1, from outside: the class as the body reads it, B1's order, and
    the draw's order with contingent-first."""
    @staticmethod
    def classer(ag, rs):
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

    @staticmethod
    def b1_order(ag, group, xcls, snap=None):
        """B1 as the body orders it (r1473, r1474, r1477, r1478): class, times parked, turnable,
        then rounds -- each subject's least-checked candidate, the least-tried subject first --
        then the explore draw; no slot name and no text. snap: the tried counts the pass saw."""
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

    @staticmethod
    def draw_order(ag, group):
        cset = set(ag.agency.contingent()) if tether._GOAL_CONTINGENT else set()
        by = {x[1]: x for x in group}
        order = frontier.draw_order([x[1] for x in group],
                                    f"{ag.cycle}:goal_hypothesis:None", ag.draw_seed)
        if any(by[t][2].slot in cset for t in order):
            order = ([t for t in order if by[t][2].slot in cset]
                     + [t for t in order if by[t][2].slot not in cset])
        return order

tether._ONE_TERM = False          # membership must not read the live set this fixture moves
tether._HYP_LEARN = False         # B1's witness: order on, learn off (r1475)
env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="hyporder"), tether.Config(),
                  ledger.Ledger())
for _ in range(6):
    ag.step()
if ag._hyp is not None:
    ag._hyp_end("lost")
before = ag.env.observe()
RK, RS, calls, SNAP = [], [], [], []


def walk(order_on):
    RK.clear(), RS.clear(), calls.clear(), SNAP.clear()
    SNAP.extend((Counter(ag._subj_tried), Counter(ag._cand_checked)))   # what the pass sees
    ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, {}, None
    tx = {id(v): k for k, v in ag._compile_cache.items()}
    real_rfs, real_fc = tether.Agent._route_first_set, tether.Agent._family_counts

    def hold(key, c, b, *_rt):
        calls.append(id(c))
        return None, "no route"

    def rfs(b):
        out = real_rfs(ag, b)
        RS.append(out)
        return out

    def fc(r, *a, **k):
        RK.extend(r)
        return real_fc(ag, r, *a, **k)
    ag._hyp_hold, ag._route_first_set, ag._family_counts = hold, rfs, fc
    tether._HYP_ORDER = order_on
    try:
        ag._hyp_propose(before)
    finally:
        tether._HYP_ORDER = True
        del ag._hyp_hold, ag._route_first_set, ag._family_counts
    groups = []
    for x in RK:
        if groups and groups[-1][0][0] == x[0]:
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups, list(calls)


def variant(route_first):
    """(a) route-first on: the group mixes S0 and S1 (a two-slot member with no routable party is
    refused before admission); (b) off: routable is unread, so it mixes S0 and S2."""
    keep = dict(ag._outstanding)
    tether._HYP_ROUTE_FIRST = route_first
    try:
        groups, _ = walk(False)
        big = max(groups, key=len)
        xcls = H.classer(ag, RS[0] if RS else None)
        by = {x[1]: x for x in big}
        draw = H.draw_order(ag, big)
        # the draw's last member not already live: made live, it must come in B1's S0 block
        st = next(t for t in reversed(draw) if xcls(by[t]) > 0)
        star = by[st][2].slot
        ag._outstanding[star] = max(ag._outstanding.get(star, 0), 1)
        out = {"group": len(big), "star_text": st, "star_was": xcls(by[st])}
        for name, on in (("b1", True), ("off", False)):
            gs, cl = walk(on)
            g = next(g for g in gs if g[0][0] == big[0][0])
            ids = {id(x[2]): x for x in g}
            seq = [ids[i] for i in cl if i in ids]
            xcls = H.classer(ag, RS[0] if RS else None)
            out[name] = {"members": sorted(x[1] for x in g), "seq": [x[1] for x in seq],
                         "classes": [xcls(x) for x in seq],
                         "want": H.b1_order(ag, g, xcls, tuple(SNAP)),
                         "star_at": [x[1] for x in seq].index(st) + 1}
        return out
    finally:
        ag._outstanding.clear()
        ag._outstanding.update(keep)
        tether._HYP_ROUTE_FIRST = True


def parked():
    """r1473: B1 picks the group's first member; it ends "parked" by the real _hyp_end (r1379
    shelves it, never bars it); the next walk checks a different member first, the parked text
    still admitted. MF: the count read as empty -- the tier removed -- and it comes first again."""
    keep = dict(ag._outstanding)
    try:
        ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, {}, None

        def ok(key, c, b, *_rt):
            return ({"linked": True, "slots": [c.slot], "route": "x", "displaced": [],
                     "_held": {}}, None)
        ag._hyp_hold = ok
        t0 = (Counter(ag._subj_tried), Counter(ag._cand_checked))   # the tried counts it saw

        def tried_as_at_pick():
            """Only the parked count differs between the walks (r1478's tried tiers held)."""
            for c, c0 in zip((ag._subj_tried, ag._cand_checked), t0, strict=True):
                c.clear()
                c.update(c0)
        try:
            ag._hyp_propose(before)
        finally:
            del ag._hyp_hold
        first, tk = ag._hyp["text"], ag._hyp["tkey"]
        n0 = ag._parked_n[tk]
        ag._hyp_end("parked")
        n = ag._parked_n[tk] - n0
        tried_as_at_pick()
        gs, cl = walk(True)
        g = next(g for g in gs if any(x[1] == first for x in g))
        ids = {id(x[2]): x for x in g}
        seq = [ids[i][1] for i in cl if i in ids]
        saved = Counter(ag._parked_n)
        ag._parked_n.clear()
        tried_as_at_pick()
        gs2, cl2 = walk(True)
        ag._parked_n.update(saved)
        g2 = next(g for g in gs2 if any(x[1] == first for x in g))
        ids2 = {id(x[2]): x for x in g2}
        seq2 = [ids2[i][1] for i in cl2 if i in ids2]
        return {"parked": first, "count": n, "group": len(g), "seq_head": seq[:3],
                "parked_at": seq.index(first) + 1 if first in seq else None,
                "mf_head": seq2[:3]}
    finally:
        ag._outstanding.clear()
        ag._outstanding.update(keep)


def distribute():
    """r1474: subject A's every unroutable candidate and later-named subject B's one routable, one
    key group and one block (class, parked, turnable equal): B is checked 2nd, not last. A has as
    many as this world gives beside a later-named subject (r1474 asked 10; the point is one)."""
    groups, _ = walk(False)
    xcls = H.classer(ag, RS[0] if RS else None)
    cset = set(ag.agency.contingent()) if tether._GOAL_CONTINGENT else set()
    for g in sorted(groups, key=len, reverse=True):
        blocks = {}
        for x in g:
            if x[1] not in ag._compile_cache:       # singles only: a group row is not planted
                continue
            blocks.setdefault((xcls(x), ag._parked_n[x[3]], x[2].slot not in cset),
                              {}).setdefault(x[2].slot, []).append(x[1])
        for subj in blocks.values():
            # A: the most candidates of any subject that has a later-named subject B in its block
            ab = [(len(subj[s]), s, t) for s in subj for t in subj if t > s]
            a, b = (max(ab)[1:] if ab and max(ab)[0] >= 5 else (None, None))
            if a and b:
                break
        else:
            continue
        break
    plant = sorted(subj[a]) + [sorted(subj[b])[0]]
    want = plant[-1]
    ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, {}, None
    tx = {id(v): k for k, v in ag._compile_cache.items()}
    seq = []

    def hold(key, c, b_, *_rt):
        seq.append(tx.get(id(c)))
        if tx.get(id(c)) == want:
            return ({"linked": True, "slots": [c.slot], "route": "x", "displaced": [],
                     "_held": {}}, None)
        return None, "no route"
    ag._hyp_hold, ag._inv_conditions = hold, (lambda _b, **_k: list(plant))
    was = tether._GROUP_PROPOSE
    tether._GROUP_PROPOSE = False
    try:
        ag._hyp_propose(before)
    finally:
        tether._GROUP_PROPOSE = was
        del ag._hyp_hold, ag._inv_conditions
    if ag._hyp is not None:
        ag._hyp_end("lost")
    return {"a": a, "b": b, "planted": len(plant), "want": want, "seq": seq[:12],
            "want_at": seq.index(want) + 1 if want in seq else None,
            "text_at": sorted(plant).index(want) + 1}


def names():
    """r1478: two subjects equal on every tier, the name-first one tried 3 times, the other
    untried: the untried subject's candidate is checked first, whatever the names."""
    groups, _ = walk(False)
    xcls = H.classer(ag, RS[0] if RS else None)
    cset = set(ag.agency.contingent()) if tether._GOAL_CONTINGENT else set()
    for g in sorted(groups, key=len, reverse=True):
        blocks = {}
        for x in g:
            if x[1] in ag._compile_cache:
                blocks.setdefault((xcls(x), ag._parked_n[x[3]], x[2].slot not in cset),
                                  {}).setdefault(x[2].slot, []).append(x)
        pairs = [sorted(subj)[:2] for subj in blocks.values() if len(subj) >= 2]
        if pairs:
            a, b = pairs[0]
            subj = next(s for s in blocks.values() if a in s and b in s)
            break
    xa, xb = sorted(subj[a], key=lambda x: x[1])[0], sorted(subj[b], key=lambda x: x[1])[0]
    keep, keep_c = Counter(ag._subj_tried), Counter(ag._cand_checked)
    ag._subj_tried[a] = 3                  # the subject whose name comes first: tried 3 times
    ag._subj_tried[b] = 0
    ag._cand_checked[xa[3]] = ag._cand_checked[xb[3]] = 0
    seq = []
    tx = {id(v): k for k, v in ag._compile_cache.items()}

    def hold(key, c, b_, *_rt):
        seq.append(tx.get(id(c)))
        return None, "no route"
    ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, {}, None
    ag._hyp_hold, ag._inv_conditions = hold, (lambda _b, **_k: [xa[1], xb[1]])
    was = tether._GROUP_PROPOSE
    tether._GROUP_PROPOSE = False
    try:
        ag._hyp_propose(before)
    finally:
        tether._GROUP_PROPOSE = was
        del ag._hyp_hold, ag._inv_conditions
        ag._subj_tried.clear(), ag._subj_tried.update(keep)
        ag._cand_checked.clear(), ag._cand_checked.update(keep_c)
    return {"tried": a, "untried": b, "seq": seq[:2], "names_first": min(xa[1], xb[1])}


print(json.dumps({"a": variant(True), "b": variant(False), "c": parked(), "d": distribute(),
                  "e": names()}))
'''


def main():
    here = _repo.ROOT
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_AGENT_SEED="0")
    p = subprocess.run([sys.executable, "-B", "-c", PROBE, here], env=env, capture_output=True,
                       text=True, timeout=1200, cwd=here)
    assert p.returncode == 0, p.stderr[-3000:]
    r = json.loads(p.stdout.strip().splitlines()[-1])
    seen = set()
    for v, mix in (("a", {0, 1}), ("b", {0, 2})):
        x = r[v]
        b1, off = x["b1"], x["off"]
        assert x["group"] > 2 and len(b1["seq"]) == x["group"], ("the walked group", v, x)
        assert set(b1["classes"]) == mix, ("the group's classes", v, sorted(set(b1["classes"])))
        seen |= mix
        assert b1["seq"] == b1["want"] and b1["classes"] == sorted(b1["classes"]), ("O1", v, b1)
        assert b1["star_at"] <= b1["classes"].count(0), ("O1: made live, in the S0 block", v)
        assert b1["members"] == off["members"], ("O2", v)
        assert off["classes"] != sorted(off["classes"]), ("MF: the draw kept class order", v)
        assert off["star_at"] > off["classes"].count(0), ("MF: the draw's late member", v, off)
    assert seen == {0, 1, 2}, seen
    pk = r["c"]
    assert pk["count"] == 1, ("O3: one budget ending counted", pk)
    assert pk["seq_head"][0] != pk["parked"], ("O3: search moves past the parked text", pk)
    assert pk["parked_at"] is not None, ("O3: the parked text still admitted (r1379)", pk)
    assert pk["mf_head"][0] == pk["parked"], ("MF3: the tier read empty, it comes first", pk)
    d = r["d"]
    assert d["planted"] >= 6 and d["want_at"] <= 2, ("O4: B's candidate in the first round", d)
    assert d["text_at"] == d["planted"], ("MF4: plain text order checks it last", d)
    e = r["e"]
    assert e["seq"] and e["seq"][0].startswith(e["untried"] + " "), ("O5: the untried first", e)
    assert e["names_first"].startswith(e["tried"] + " "), ("MF5: the names would pick the tried", e)
    a, b = r["a"], r["b"]
    print(f"hyp_order: O1 (a) a key group of {a['group']} walked S0 then S1 "
          f"({a['b1']['classes'].count(0)} + {a['b1']['classes'].count(1)}), (b) of {b['group']} "
          f"S0 then S2 ({b['b1']['classes'].count(0)} + {b['b1']['classes'].count(2)}); the "
          f"draw's late member, made live, checked at {a['b1']['star_at']} and "
          f"{b['b1']['star_at']}; O2 membership equal; MF the draw checked it at "
          f"{a['off']['star_at']} and {b['off']['star_at']}, out of class order: 2 of 2, "
          f"1 must-fail; O3 {r['c']['parked']!r} parked once, the next walk checks "
          f"{r['c']['seq_head'][0]!r} first and the parked text at {r['c']['parked_at']}; MF3 "
          f"the tier read empty puts it first again; O4 {r['d']['b']}'s one routable checked "
          f"at {r['d']['want_at']} behind {r['d']['a']}'s {r['d']['planted'] - 1}; MF4 text order "
          f"checks it at {r['d']['text_at']}; O5 untried {r['e']['untried']} before "
          f"{r['e']['tried']} (tried 3x), MF5 the names would put {r['e']['tried']} first: "
          f"5 of 5, 4 must-fails")


if __name__ == "__main__":
    main()
