"""BUILD 5 ITEM 17 (v) (a), CHAIN-CONNECTED (TETHER_CONNECTED; the reviewer 2026-11-05 r1208; Fig 6
:29-32). connected(o, x) compiles onto o.connected_x, a BOOL derived where conditions are read, from
the frame's own *.touches_* slots (the touch graph's components); perception is unchanged. The
completion offers connected(a, b) == 1 for pairs joined at the last met row. Seconds:
test_group_row's agent; frames forced from its own state, every touch cleared but the ones set.

MF-N1  o0-o1-o2 touching in a chain, o0 and o2 not touching: connected(o0, o2) reads True; break
       the o1-o2 touch and it reads False; with o2 absent it reads None
MF-N2  the objective held exactly when the chain was whole: "connected(o0, o2) == 1" is the cheapest
       that pays (errors 0), each single touch errs, and the completion holds it, invented on
       touching, with no single slot to want
MF-N3  OFF: "no pairwise atom", as before; no connected goal offered
The red is behavioural: TETHER_CONNECTED=0 fails MF-N1.

    python tests/test_connected.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

C, tether = G.C, G.tether


def main():
    ag, atoms, st = G.agent()
    base = {k: (0 if ".touches_" in k else v) for k, v in st.items()}

    def touch(*pairs):
        f = dict(base)
        for a, b in pairs:
            f[f"{a}.touches_{b}"] = f[f"{b}.touches_{a}"] = 1
        return f
    chain = touch(("o0", "o1"), ("o1", "o2"))
    c = C.compile_candidate({"condition": "connected(o0, o2) == 1"}, atoms)
    assert isinstance(c, C.Compiled) and c.via == C.CONNECTED_VIA, ("MF-N1: not compiled", c)
    assert C.run(c, chain) is True, "MF-N1: the chain does not read connected"
    assert C.run(c, touch(("o0", "o1"))) is False, "MF-N1: a broken chain reads connected"
    assert C.run(c, G.without(chain, ["o2"])) is None, "MF-N1: an absent object is not None"

    cases = [(chain, True), (touch(("o0", "o1")), False), (touch(("o1", "o2")), False),
             (base, False)]
    rows = [cases[i % 4] for i in range(36)] + [(chain, True)]
    best, detail = ag._goal_candidates(rows)
    assert detail["offered"].get("connected", 0) >= 1, ("MF-N2: none offered", detail["offered"])
    assert best is not None and best[4] == "connected(o0, o2) == 1" and best[3] == 0, (
        "MF-N2: connected is not the cheapest that pays", detail["cheapest"])
    single = C.compile_candidate({"condition": "o0.touches_o1 == 1"}, atoms)
    assert isinstance(single, C.Compiled) and ag._goal_price([single], rows)[2] > 0, (
        "MF-N2: a single touch does not err", single)
    ag._reach_hist = rows
    ag._goal_condition()
    row = [r for r in ag.led.rows() if r["event"] == "goal_condition"][-1]["detail"]
    assert row.get("pick") == "connected(o0, o2) == 1" and row.get("key", "").startswith(
        "AGENT-INVENTED|"), ("MF-N2: the completion does not hold it", row)
    assert row["link"] == {"linked": False, "why": "a connection names no single slot to want"}

    C._CONNECTED = False
    try:
        off = C.compile_candidate({"condition": "connected(o0, o2) == 1"}, atoms)
        _b, d_off = ag._goal_candidates(rows)
    finally:
        C._CONNECTED = True
    assert isinstance(off, C.Refusal) and "no pairwise atom" in off.reason, ("MF-N3", off)
    assert "connected" not in d_off["offered"], ("MF-N3: offered OFF", d_off["offered"])
    print(f"test_connected: pass (MF-N1 chain True, broken False, absent None; MF-N2 "
          f"'connected(o0, o2) == 1' cheapest that pays of {detail['conditions']} "
          f"({detail['offered']['connected']} connected offered), held as {row['key']}, no slot "
          f"to want; MF-N3 OFF refused, none offered)")


if __name__ == "__main__":
    main()
