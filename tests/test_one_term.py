"""(c), ONE TERM (TETHER_ONE_TERM; the reviewer 2026-11-08 r1453, r1454; Fig 12 :23-27): the library
writes ONE spelling per unordered pair, and the proposal pass chooses its subject before any compile
-- the better class (live residual, routable, the rest) among the parties passing the subject-side
checks, a tie to the smaller text, no draw; the other spelling stays text until a hold fails on the
subject side. test_group_row's agent; for the choice checks the generator is stubbed to the pair
under test (groups off) and the route is stubbed per slot; on the panel o0.row < o5.row, so
W = "o0.row > o5.row" and its other spelling P = "o5.row < o0.row" are open.

G    the generator on a two-object state: every term spelled ONCE folded, both ways unfolded, and
     the written spellings with their recorded partners are exactly the unfolded set
F1   (i) o5.row live (S0), o0.row the rest (S2): written once, P (subject o5.row) chosen
F2a  (ii) a symmetric pair under the 16c mirror: written once, no alternate
F2b  the same pair with 16c off: one alternate
F3   (iii) a tie (both routable) goes to W; W has no route: P compiled only after W's hold, once,
     held and picked
F4   (iv) the better party (o5.row, live) tried: W written, no alternate
F5   r1438: P arrived without a clear bars W too: refused once, nothing picked
F6   the tie of F3 gives W at every seed of a would-be draw
MF1  a fold template that matches nothing writes both orders: G catches it
MF2  a subject drawn by seed: F6 catches it

    python tests/test_one_term.py
"""
from __future__ import annotations

import hashlib
import re
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether
compile_term = tether.compile_term
W, P = "o0.row > o5.row", "o5.row < o0.row"
S, SC = "o0.row == o5.row", "o5.row == o0.row"
ALL3 = ("o0.row", "o5.row", "o1.row")


def propose(pairs, on=True, live=(), rfs=ALL3, routes=ALL3, tried=None, both=True, log=None):
    ag, atoms, _st = G.agent()
    before = ag.trace[-1][2]
    assert before["o0.row"] < before["o5.row"], "panel"
    ag.wants.clear()
    ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, dict(tried or {}), None
    ag._compile_cache.clear()
    ag._outstanding = dict.fromkeys(live, 1.0)

    def gen(_b, fold=False):
        ag._inv_tpl = {}        # as the generator: this call's texts only (no template forms here)
        if not fold:
            return [t for w, p in pairs for t in (w, p)]
        ag._inv_alt = {w: (p, p) for w, p in pairs}
        return [w for w, _p in pairs]
    ag._inv_conditions = gen
    ag._hyp_route = lambda sl, *_a: "a route" if sl in routes else None
    ag._route_first_set = lambda _b: set(rfs)
    if log is not None:
        cc, hold = compile_term.compile_candidate, ag._hyp_hold

        def cc_log(cand, *a, **k):
            log.append(("compile", cand.get("condition")))
            return cc(cand, *a, **k)

        def hold_log(key, c, *a, **k):
            log.append(("hold", getattr(c, "slot", None)))
            return hold(key, c, *a, **k)
        compile_term.compile_candidate, ag._hyp_hold = cc_log, hold_log
    was = tether._ONE_TERM, tether._GROUP_PROPOSE, tether._GOAL_BOTH_SIDES
    tether._ONE_TERM, tether._GROUP_PROPOSE, tether._GOAL_BOTH_SIDES = on, False, both
    try:
        ag._hyp_propose(before)
    finally:
        tether._ONE_TERM, tether._GROUP_PROPOSE, tether._GOAL_BOTH_SIDES = was
        if log is not None:
            compile_term.compile_candidate = cc
    return [r for r in ag.led.rows() if r["event"] == "goal_hypotheses"][-1]["detail"]


def gen_check():
    """G: the folded generator spells each term once; written + partners == the unfolded set."""
    ag, _atoms, _st = G.agent()
    st = {"o0.row": 1, "o5.row": 3, "o0.colour": 2, "o5.colour": 4}
    both = ag._inv_conditions(st)
    once = ag._inv_conditions(st, fold=True)
    alt = dict(ag._inv_alt)
    pairs = [t for t in once if t in alt]
    return (len(pairs) > 0 and len(set(once)) == len(once)
            and not any(alt[t][0] in once for t in pairs)
            and set(once) | {alt[t][0] for t in pairs} == set(both)
            and len(both) == len(once) + len(pairs), len(both), len(once), len(pairs))


def ties(seed: list, seeds=range(8)) -> list:
    """The tie's chosen spelling at each value of `seed` (read only by MF2's would-be draw)."""
    got = []
    for s in seeds:
        seed[0] = s
        got.append(propose([(W, P)])["ranked"][0]["if"])
    return got


def checks():
    out = {"G": gen_check()}
    on = propose([(W, P)], live=("o5.row",), rfs=("o5.row",))
    off = propose([(W, P)], on=False, live=("o5.row",), rfs=("o5.row",))
    out["F1"] = (on.get("open") == 1 and off.get("open") == 2
                 and on["ranked"][0]["if"] == P and on["ranked"][0]["subject"] == "o5.row"
                 and on["one_term"].get("subject from the other spelling") == 1, on, off)
    r2a = propose([(S, SC)])
    out["F2a"] = (r2a.get("open") == 1 and r2a["one_term"].get("alternates") == 0, r2a)
    r2b = propose([(S, SC)], both=False)
    out["F2b"] = (r2b.get("open") == 1 and r2b["one_term"].get("alternates") == 1, r2b)
    log: list = []
    r3 = propose([(W, P)], routes=("o5.row",), log=log)
    first_hold = next((i for i, e in enumerate(log) if e[0] == "hold"), None)
    p_at = [i for i, e in enumerate(log) if e == ("compile", P)]
    out["F3"] = (r3.get("pick") == P and first_hold is not None and len(p_at) == 1
                 and p_at[0] > first_hold and r3["one_term"].get("alternate routed") == 1
                 and r3["one_term"].get("alternate tried after: no route") == 1, r3, log[:12])
    tk_p = (P, "o5.row", "o0.row")
    r4 = propose([(W, P)], live=("o5.row",), tried={tk_p: ("stalled", None, P)})
    out["F4"] = (r4.get("pick") == W and r4["one_term"].get("alternates") == 0
                 and "subject from the other spelling" not in r4["one_term"], r4)
    r5 = propose([(W, P)], tried={tk_p: ("arrived_no_clear", None, P)})
    out["F5"] = (r5.get("pick") is None and r5["one_term"].get("pair refused") == 1
                 and r5["refused"].get("tried this level: its converse arrived") == 1, r5)
    out["F6"] = (set(ties([0])) == {W},)
    return out


def main():
    out = checks()
    bad = {k: v[1:] for k, v in out.items() if not v[0]}
    assert not bad, bad
    real_tpl, real_choice = tether._FOLD_TPL, tether._term_choice
    tether._FOLD_TPL = re.compile(r"(?!)")
    try:
        assert not gen_check()[0], "MF1: both orders written and G passed"
    finally:
        tether._FOLD_TPL = real_tpl
    seed = [0]
    tether._term_choice = lambda sides: sorted(
        sides, key=lambda z: hashlib.sha256(f"{seed[0]}:{z[1]}".encode()).hexdigest())
    try:
        drawn = ties(seed)
        assert set(drawn) != {W}, ("MF2: a drawn subject passed F6", drawn)
    finally:
        tether._term_choice = real_choice
    g = out["G"]
    print(f"G   {g[1]} texts unfolded, {g[2]} folded, {g[3]} pairs spelled once")
    print(f"F1  live o5.row: {P!r} chosen (open 1; OFF open 2)")
    print("F2a symmetric under 16c: one open, no alternate; F2b 16c off: one alternate")
    print(f"F3  tie to {W!r}; no route: {P!r} compiled after the hold, once, and picked")
    print("F4  the live party tried: W written, no alternate; F5 an arrival bars the pair")
    print("F6  the tie is W at 8 of 8 would-be seeds")
    print("MF1 a fold that matches nothing fails G; MF2 a drawn subject fails F6")
    print("one_term: 8 of 8, 2 must-fails")


if __name__ == "__main__":
    main()
