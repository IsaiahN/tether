"""C1 PHASE 3, PART 1: THE TIP-OVER (the reviewer 2026-11-09 r1584 1, r1592 3, r1594), arm
TETHER_SETTLE_BEAT_NULL.

  T1  gamma.settle(tip=False): confirmations rise, the term is not settled (anywhere or on the
      slot), and its evidence row carries "untipped"; tip=True settles as before
  T2  replay: a carried "untipped" settle row does not tip on load (MF: the arm leaking through the
      save); a plain row tips, as before (path 4 unchanged)
  T3  gridworld, 40 steps ON: every tipping settle row beat the null (risky true), the tied ones are
      settle_tied rows and leave the term a candidate there, and _settled_lvl holds only terms with
      a tipping row in the level (path 3, promotion's gate, by construction). OFF on the same run
      tips on a tied occasion (the occasion exists)
  T4  win credit (path 1): at a level advance, a bound term that tipped on a beat in the level is
      tipped; one that did not is counted (confirmations) and not tipped (MF)

    python tests/test_c1_tip.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _gamma() -> gamma.Gamma:
    """With two composed (non-innate) terms, since replay leaves innate atoms as record."""
    env = world.bind(gridworld.family("default", 0))
    g = gamma.Gamma(env.atoms(), game="g")
    lib = g.library
    for p, q in (("inc", "dbl"), ("dec", "dbl")):
        g.accept(gamma.Term((lib[p].atoms[0], lib[q].atoms[0])), 0, "r")
    return g


def check_t1_t2() -> None:
    g = _gamma()
    g.keep_evidence = True
    a, b = "inc . dbl", "dec . dbl"
    g.settle(a, slot="s", null="tied", tip=False)
    st = g.standing[a]
    assert (st.confirmations, g.is_settled(a), g.is_settled(a, "s")) == (1.0, False, False), st
    assert g.evidence[-1][5:] == [gamma.UNTIPPED], g.evidence[-1]
    g.settle(b, slot="s", null="beat")
    assert g.is_settled(b, "s") and len(g.evidence[-1]) == 5, g.evidence[-1]
    print("  T1: tip=False counts and does not settle, its row carries 'untipped'; tip=True "
          "settles")
    rows = [list(r) for r in g.evidence]
    h = _gamma()
    keep, tether._SETTLE_BEAT_NULL = tether._SETTLE_BEAT_NULL, False    # r1595 (1): loaded OFF
    try:
        h.replay(rows)
    finally:
        tether._SETTLE_BEAT_NULL = keep
    assert not h.is_settled(a), "MUST-FAIL: a carried untipped settle tipped on load"
    assert h.standing[a].confirmations == 1.0 and h.is_settled(b), h.standing
    print("  T2: replay with the arm OFF: the untipped row counts and does not tip (a fact about "
          "the row, r1595 (1)); the plain row tips (path 4)")


def _run(on: bool, n: int = 40) -> tether.Agent:
    keep, tether._SETTLE_BEAT_NULL = tether._SETTLE_BEAT_NULL, on
    try:
        env = world.bind(gridworld.family("default", 0))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(),
                          ledger.Ledger())
        for _ in range(n):
            ag.step()
        return ag
    finally:
        tether._SETTLE_BEAT_NULL = keep


def check_t3() -> None:
    off = _run(False)
    off_tied = [r for r in off.led.rows() if r["event"] == "settle"
                and r["detail"].get("risky") is False]
    assert off_tied, "occasion: OFF never tipped on a tied settle in 40 steps"
    ag = _run(True)
    rows = ag.led.rows()
    tips = [r for r in rows if r["event"] == "settle" and r["detail"].get("status") == "accepted"]
    tied = [r for r in rows if r["event"] == "settle_tied"]
    assert tied, "occasion: no tied settle ON"
    assert all(r["detail"].get("risky") is True for r in tips), [r["detail"] for r in tips]
    lvl = ag.level
    tipped_here = {r["detail"]["term"] for r in tips if r.get("level", lvl) == lvl}
    assert ag._settled_lvl <= tipped_here, (ag._settled_lvl, tipped_here)
    last = {}
    for r in rows:
        if r["event"] in ("settle", "settle_tied", "demote"):
            last[(r["detail"].get("term"), r["slot"])] = r["event"]
    for (name, slot), ev in last.items():
        if ev == "settle_tied":
            assert not ag.gamma.is_settled(name, slot), (name, slot)
    print(f"  T3: ON, {len(tips)} tipping settles all beat the null, {len(tied)} settle_tied rows "
          f"left their terms candidates; _settled_lvl {sorted(ag._settled_lvl)} only tipped "
          f"terms. OFF tipped {len(off_tied)} times on a tied occasion")


def check_t4() -> None:
    keep, tether._SETTLE_BEAT_NULL = tether._SETTLE_BEAT_NULL, True
    try:
        ag = _run(True, 20)
        tether._SETTLE_BEAT_NULL = True
        lib = ag.gamma.library
        names = [ag.gamma.accept(gamma.Term((lib[p].atoms[0], lib[q].atoms[0], lib[p].atoms[0])),
                                 0, "r").name for p, q in (("inc", "dbl"), ("dec", "dbl"))]
        assert not any(ag.gamma.is_settled(n) for n in names), "fixture: two unsettled terms"
        beat, quiet = names
        ag.bound = {"o0.row": beat, "o0.col": quiet}
        ag._settled_lvl = {beat}
        c0 = {n: getattr(ag.gamma.standing.get(n), "confirmations", 0.0) for n in names}
        ag.retarget(ag.env, ag.level + 1, how=tether.ADVANCE)
    finally:
        tether._SETTLE_BEAT_NULL = keep
    g = ag.gamma
    assert g.is_settled(beat), "the beat term was not tipped by the win credit"
    assert not g.is_settled(quiet), "MUST-FAIL: win credit tipped a term with no beat in the level"
    assert g.standing[quiet].confirmations == c0[quiet] + 1.0, g.standing[quiet]
    wc = [r for r in ag.led.rows() if r["event"] == "win_credit"][-1]["detail"]
    assert (wc["terms"], wc["tipped"]) == (2, 1), wc
    print(f"  T4: win credit at an advance: {wc['terms']} counted, {wc['tipped']} tipped (the "
          f"one with a beat in the level)")


def main() -> int:
    check_t1_t2()
    check_t3()
    check_t4()
    print("c1_tip: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
