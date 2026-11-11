"""C1 PHASE 3, PART 2: THE REFUSAL RANK (the reviewer 2026-11-09 r1584 (a)(b), r1595 (A)), arm
TETHER_REFUSE_RANK.

  R1  gamma.refusal_from_miss moves the candidate miss, as it stands after decay, into refusals:
      misses + refusals == rejections still, and track_of falls (Laplace, never a cliff)
  R2  MF (r1584 (a)): a term with many misses and no persistent-flat run (a hit between them) is
      not converted, and its track_of is unchanged
  R3  two terms tied at the top (same run, beat_null and settled_at) BOTH take the refusal; a
      third with a shorter run does not (r1595: all at the top, never a name)
  R4  a term settled on the slot already took its miss as a refusal: ranked, nothing moved
  R5  gridworld 40 steps: arm OFF writes no refusal_ranked row; arm ON, every refused term is at
      the top of its row's ranking

    python tests/test_c1_rank.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")
# Piece 1: these checks read the CYCLE clock (TETHER_FADE_BY_STORE=0, r1677); the store clock is
# tests/test_store_clock.py
os.environ.setdefault("TETHER_FADE_BY_STORE", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="c1_rank"), tether.Config(),
                        ledger.Ledger())


def _hand(series: dict) -> tether.Agent:
    """Hand slots, each a list of (before, after) values on the same steps."""
    ag = _agent()
    n = len(next(iter(series.values())))
    ag.trace = [({s: v[i][0] for s, v in series.items()}, "A",
                 {s: v[i][1] for s, v in series.items()}, IFace.TOUCH, None) for i in range(n)]
    ag._trace_pos = None
    for s in series:
        ag.slots = [*ag.slots, s]
        ag.alphabet[s] = 8
    return ag


def _miss(ag: tether.Agent, slot: str, name: str, held: bool = False) -> None:
    """One candidate miss counted at this tick, as the settle path counts it."""
    ag.gamma.refute(name, slot=slot)
    ag._refuted_slot[slot] = name
    ag._miss_at[slot] = (name, ag.gamma.tick, held)


def check_r1() -> None:
    g = _agent().gamma
    g.tick = 5
    g.refute("inc", slot="s")
    g.refute("inc", slot="s")
    st = g.standing["inc"]
    t0 = g.track_of("inc")
    g.tick = 6
    moved = g.refusal_from_miss("inc", 5)
    assert 0 < moved < 1 and abs(st.misses + st.refusals - st.rejections) < 1e-9, st
    assert g.track_of("inc") < t0, (g.track_of("inc"), t0)
    print(f"  R1: moved {moved:.4f} (one miss after one cycle's decay); misses + refusals == "
          f"rejections; track_of {t0:.4f} -> {g.track_of('inc'):.4f}")


def check_r2() -> None:
    alt = [(1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5)]   # idn misses, hits, misses
    ag = _hand({"x": alt})
    ag.gamma.tick = 9
    for _ in range(4):
        _miss(ag, "x", "idn")
    t0 = ag.gamma.track_of("idn")
    assert ag._flat_run("idn", "x") == 0
    ag._refuse_rank(["x"])
    assert ag.gamma.track_of("idn") == t0, "MUST-FAIL: misses with no persistent-flat run moved"
    assert not [r for r in ag.led.rows() if r["event"] == "refusal_ranked"]
    print(f"  R2: 4 misses, a hit between each: run 0, nothing ranked, track_of {t0:.4f} unchanged")


def check_r3_r4() -> None:
    up = [(1, 2), (2, 3), (3, 4), (4, 5)]          # idn misses every row
    three = [(1, 4), (1, 4), (1, 4), (1, 4)]       # inc (+1) misses every row
    short = [(1, 1), (1, 1), (1, 3), (3, 5)]       # dbl . inc-ish: a run too short to count
    ag = _hand({"x": up, "y": three, "z": short})
    ag.gamma.tick = 9
    _miss(ag, "x", "idn")
    _miss(ag, "y", "inc")
    _miss(ag, "z", "neg")
    runs = {s: ag._flat_run(n, s) for s, n in (("x", "idn"), ("y", "inc"), ("z", "neg"))}
    assert runs["x"] == runs["y"] == 4 and runs["z"] < 4, runs
    before = {n: ag.gamma.track_of(n) for n in ("idn", "inc", "neg")}
    ag.gamma.tick = 10
    ag._refuse_rank(["x", "y", "z"])
    row = [r for r in ag.led.rows() if r["event"] == "refusal_ranked"][-1]["detail"]
    assert sorted(n for _, n, _ in row["refused"]) == ["idn", "inc"], row
    assert ag.gamma.track_of("idn") < before["idn"] and ag.gamma.track_of("inc") < before["inc"]
    assert ag.gamma.track_of("neg") == before["neg"], "the shorter run was refused"
    print(f"  R3: runs {runs}; both tied at the top refused {row['refused']}; the shorter run kept "
          f"its track_of")
    ag2 = _hand({"x": up})
    ag2.gamma.tick = 9
    _miss(ag2, "x", "idn", held=True)
    m0 = ag2.gamma.standing["idn"].misses
    ag2.gamma.tick = 10
    ag2._refuse_rank(["x"])
    row2 = [r for r in ag2.led.rows() if r["event"] == "refusal_ranked"][-1]["detail"]
    assert row2["refused"] == [["x", "idn", 0.0]] and ag2.gamma.standing["idn"].misses == m0
    print("  R4: settled on the slot: ranked, 0 moved (its miss was already a refusal)")


def _run(on: bool) -> tether.Agent:
    keep, tether._REFUSE_RANK = tether._REFUSE_RANK, on
    try:
        env = world.bind(gridworld.family("default", 0))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(),
                          ledger.Ledger())
        for _ in range(40):
            ag.step()
        return ag
    finally:
        tether._REFUSE_RANK = keep


def check_r5() -> None:
    off = _run(False)
    assert not [r for r in off.led.rows() if r["event"] == "refusal_ranked"]
    on = _run(True)
    rows = [r["detail"] for r in on.led.rows() if r["event"] == "refusal_ranked"]
    for d in rows:
        top = d["ranked"][0][2:]
        tops = {(s, n) for s, n, *k in d["ranked"] if k == top}
        assert {(s, n) for s, n, _ in d["refused"]} == tops, d
    print(f"  R5: gridworld 40 steps: OFF no refusal_ranked row; ON {len(rows)} rows, each "
          f"refusing exactly its top tie")


def main() -> int:
    check_r1()
    check_r2()
    check_r3_r4()
    check_r5()
    print("c1_rank: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
