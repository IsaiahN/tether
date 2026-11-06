"""R3 (the reviewer 2026-11-06 r1304, r1305, r1311): _lookup_fold's JSON pieces through one reused
encoder per argument set and a fold-local memo of str values (tether._fold_js). Pure: the same
bytes as json.dumps(v, ensure_ascii=False[, sort_keys=True]). Gridworld, seed pinned; about a
minute.

MF-R3a  MUST-STAY: for every slot of a 12-step gridworld agent, described by every reading of its
        object, and for a two-member event, the fold's full return (query, n, junctions, held_n,
        hexdigest, sample, named_of) is EQUAL with _fold_js and with the json.dumps it replaces,
        each from fresh bond state
CONTROL a memo planted with a wrong key (a str's JSON keyed by its length) makes MF-R3a's
        comparison differ, so the comparison can fail

    python tests/test_r3_fold_js.py
"""
from __future__ import annotations

import json
import os
import sys
from functools import partial

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def ref_js() -> tuple:
    return (partial(json.dumps, ensure_ascii=False),
            partial(json.dumps, ensure_ascii=False, sort_keys=True))


def wrong_js() -> tuple:
    memo: dict = {}

    def js(v):
        if type(v) is str:
            return memo.setdefault(len(v), json.dumps(v, ensure_ascii=False))
        return json.dumps(v, ensure_ascii=False)
    return js, partial(json.dumps, ensure_ascii=False, sort_keys=True)


def fold(ag, maker, ev, members, described, desc_of, hist, slot):
    real = tether._fold_js
    tether._fold_js = maker or real
    try:
        ag._bond_inc = {}
        q, n, j, h, dig, sample, named = ag._lookup_fold(ev, members, described, desc_of, hist,
                                                         slot=slot)
    finally:
        tether._fold_js = real
    return (q, n, j, h, dig.hexdigest(), json.dumps(sample, ensure_ascii=False),
            json.dumps({m: list(v.items()) for m, v in named.items()}, ensure_ascii=False))


def cases(ag):
    own = ag.env.slot_owner()
    slots = sorted(s for s in own if s in ag.slot_types)
    for slot in slots:
        hist = ag.history(slot)
        if len(hist) < 2:
            continue
        described = {s: ag.slot_types[s] for s, o in own.items()
                     if o == own[slot] and s in ag.slot_types}
        yield slot, (None, (slot,), described, {slot: described}, hist, slot)
    objs = sorted({own[s] for s in slots})
    s1, s2 = (next(s for s in slots if own[s] == o and len(ag.history(s)) > 1) for o in objs[:2])
    d1 = {s: ag.slot_types[s] for s in slots if own[s] == own[s1]}
    d2 = {s: ag.slot_types[s] for s in slots if own[s] == own[s2]}
    yield "event", ("e0", (s1, s2), {**d1, **d2}, {s1: d1, s2: d2}, ag.history(s1), s1)


def main():
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger(path=None))
    for _ in range(12):
        ag.step()
    assert tether._LOOKUP_FOLD and not tether._BOND_INC_CHECK, "precondition: the fold runs"
    diff, ctl, pairs, held, n_cases = [], [], 0, 0, 0
    for name, args in cases(ag):
        new, ref = fold(ag, None, *args), fold(ag, ref_js, *args)
        n_cases += 1
        pairs += ref[1]
        held += ref[3]
        if new != ref:
            diff.append((name, [i for i in range(7) if new[i] != ref[i]]))
        if fold(ag, wrong_js, *args) != ref:
            ctl.append(name)
    assert pairs and held, ("precondition: no pair held", pairs, held)
    assert not diff, ("MF-R3a", diff[:5])
    assert ctl, "CONTROL: a wrong memo key changed nothing, so the comparison cannot fail"
    print(f"  MF-R3a {n_cases} folds ({pairs} pairs, {held} held): _fold_js == json.dumps")
    print(f"  CONTROL a wrong memo key differs on {len(ctl)} of {n_cases} folds")
    print("test_r3_fold_js OK")


if __name__ == "__main__":
    main()
