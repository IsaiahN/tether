"""C1 PHASE 3, PART 1: THE TIP-OVER (the reviewer 2026-11-09 r1584 1, r1592 3, r1594), arm
TETHER_SETTLE_BEAT_NULL.

  T1  gamma.settle(tip=False): confirmations rise, the term is not settled (anywhere or on the
      slot), and its evidence row carries "untipped"; tip=True settles as before
  T2  replay: a carried "untipped" settle row does not tip on load (MF: the arm leaking through the
      save); a plain row tips, as before (path 4 unchanged)
  T3  a hand fixture (r1652 (2): the occasion is built, never waited for in a long run): a
      candidate's correct prediction where "no change" would also have held (tied) and one where
      it would have missed (beat). ON: the beat tips (risky true) and the tied writes settle_tied
      and leaves the term a candidate; _settled_lvl holds only the tipped term. MF: OFF, the tied
      occasion tips (risky false)
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


S = "o0.row"


def _occasion(on: bool, tied: bool) -> tuple:
    """One settle-path occasion, built by hand: the candidate term made the slot's prediction,
    the ground agreed (mass 0), born before this cycle, in this level. Tied: the prediction equals
    the slot's previous value (no change would also have held); beat: it differs."""
    keep, tether._SETTLE_BEAT_NULL = tether._SETTLE_BEAT_NULL, on
    try:
        env = world.bind(gridworld.family("default", 0))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(),
                          ledger.Ledger())
        ag.step()
        lib = ag.gamma.library
        name = ag.gamma.accept(gamma.Term((lib["inc"].atoms[0], lib["dbl"].atoms[0])), 0,
                               "r").name
        ag.candidates[name], ag._cand_level[name] = 0, ag.level
        b = dict(ag.trace[-1][0])
        a = ag.alphabet.get(S) or 8
        frm = 2
        b[S] = frm
        act = frm if tied else (frm + 1) % a
        ag.trace[-1] = (b, ag.trace[-1][1], dict(ag.trace[-1][2], **{S: act}),
                        *ag.trace[-1][3:])
        ag._pred_by, ag.bound[S] = {S: name}, name
        n0 = len(ag.led.rows())
        ag.settle({S: tether.SlotResidual(S, tether.TRANSITION, act, act, 0.0)})
        rows = [r for r in ag.led.rows()[n0:] if r["slot"] == S
                and r["event"] in ("settle", "settle_tied")]
        return ag, name, rows
    finally:
        tether._SETTLE_BEAT_NULL = keep


def check_t3() -> None:
    off, off_name, off_rows = _occasion(False, tied=True)
    assert off_rows and off_rows[-1]["event"] == "settle", ("fixture: no settle", off_rows)
    assert off_rows[-1]["detail"].get("risky") is False and off.gamma.is_settled(off_name, S), \
        "MF: OFF, the tied occasion did not tip"
    ag, name, rows = _occasion(True, tied=True)
    assert rows and rows[-1]["event"] == "settle_tied", rows
    assert not ag.gamma.is_settled(name, S) and name not in ag._settled_lvl, "tied tipped ON"
    bg, bname, brows = _occasion(True, tied=False)
    assert brows and brows[-1]["event"] == "settle" and brows[-1]["detail"].get("risky") is True
    assert bg.gamma.is_settled(bname, S) and bg._settled_lvl <= {bname}, bg._settled_lvl
    print("  T3: by hand: ON the beat tips (risky true) and the tied writes settle_tied, the term "
          "a candidate; _settled_lvl holds only the tipped term. OFF the tied occasion tips "
          "(risky false)")


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
