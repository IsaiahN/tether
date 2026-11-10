"""C1 PHASE 4, PARTS 3-4: CROWDING OUT AND RE-ENTRY (the reviewer 2026-11-09 r1593 (A), r1597),
arm TETHER_CROWD_OUT. The incumbent "inc . dec" says exactly what idn says (c34's shape: the
same left as the null, a dearer statement).

  C1  MF (c): ON, at a refit of the bound slot the incumbent fails its bargain against the null
      (cost + left < left(idn) false) and the null takes the slot: unbound, owed, crowded_out
  C2  MF (d): an incumbent whose cost + left IS below left(idn) ("inc" on a slot that counts up)
      keeps the slot; no crowded_out row
  C3  MF (a): the same idn-like incumbent with a beat on the slot (beat_on) is not displaced by
      the null
  C4  MF (b): OFF, the idn-like incumbent keeps the slot; idn is never offered against it
  C5  part 4: the crowded claim is skipped at the slot's next refit; it re-enters when the library
      grows ("library_grew") or the level changes ("arrangement"), with a re_entered row
  C6  gamma: a settle that beat the null adds the slot to beat_on, a tied one does not; replay
      clears it

    python tests/test_c1_crowd.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

LIKE_IDN = "inc . dec"
RANDOM = [(1, 6), (6, 2), (2, 7), (7, 4), (4, 1), (1, 5), (5, 0)]   # nothing in the atoms fits
COUNT = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)]    # inc fits every row


def _hand(series: list, incumbent: str) -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="c1_crowd"), tether.Config(),
                      ledger.Ledger())
    lib = ag.gamma.library
    if LIKE_IDN not in lib:
        ag.gamma.accept(gamma.Term((lib["inc"].atoms[0], lib["dec"].atoms[0])), 0, "r")
    ag.trace = [({"x": b}, "A", {"x": a}, IFace.TOUCH, None) for b, a in series]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x"]
    ag.alphabet["x"] = 8
    ag.bound["x"] = incumbent
    return ag


def _refit(ag: tether.Agent, on: bool) -> str | None:
    keep, tether._CROWD_OUT = tether._CROWD_OUT, on
    try:
        return ag._fit_counted("x", ag.bound.get("x"))
    finally:
        tether._CROWD_OUT = keep


def _rows(ag: tether.Agent, ev: str) -> list:
    return [r["detail"] for r in ag.led.rows() if r["event"] == ev]


def check_c1_c5() -> None:
    ag = _hand(RANDOM, LIKE_IDN)
    fit = _refit(ag, True)
    co = _rows(ag, "crowded_out")
    assert fit is None and "x" not in ag.bound and "x" in ag.owed_import, (fit, ag.bound)
    assert co and co[-1]["term"] == LIKE_IDN and co[-1]["crowder"] == tether.IDN, co
    d = co[-1]
    assert d["incumbent_left"] == d["null_left"] and d["incumbent_cost"] > 0, d
    print(f"  C1: the idn-like incumbent fails its bargain against the null (cost "
          f"{d['incumbent_cost']} + left {d['incumbent_left']} vs null left {d['null_left']}): "
          f"unbound, owed, crowded_out")
    assert ag._crowd_blocked("x", LIKE_IDN), "C5: the crowded claim was not held out"
    lib = ag.gamma.library
    ag.gamma.accept(gamma.Term((lib["dbl"].atoms[0], lib["neg"].atoms[0])), 0, "r")
    assert not ag._crowd_blocked("x", LIKE_IDN)
    assert _rows(ag, "re_entered")[-1]["reason"] == "library_grew"
    ag._crowd_note("x", LIKE_IDN, tether.IDN)
    ag.level += 1
    assert not ag._crowd_blocked("x", LIKE_IDN)
    assert _rows(ag, "re_entered")[-1]["reason"] == "arrangement"
    print("  C5: held out of the slot until the library grew (re_entered library_grew), and "
          "again until the level changed (re_entered arrangement)")


def check_c2() -> None:
    ag = _hand(COUNT, "inc")
    _refit(ag, True)
    assert ag.bound.get("x") == "inc" and not _rows(ag, "crowded_out"), \
        "MUST-FAIL (d): an incumbent that pays against the null was displaced"
    print("  C2: inc on a counting slot pays against the null and keeps the slot")


def check_c3() -> None:
    ag = _hand(RANDOM, LIKE_IDN)
    ag.gamma.standing.setdefault(LIKE_IDN, gamma.Standing()).beat_on.add("x")
    _refit(ag, True)
    assert ag.bound.get("x") == LIKE_IDN and not _rows(ag, "crowded_out"), \
        "MUST-FAIL (a): a claim with a beat here was displaced by the null"
    print("  C3: the same incumbent with a beat on the slot keeps it (class gate)")


def check_c4() -> None:
    ag = _hand(RANDOM, LIKE_IDN)
    _refit(ag, False)
    assert ag.bound.get("x") == LIKE_IDN and not _rows(ag, "crowded_out"), \
        "MUST-FAIL (b): OFF offered the null against a bound term"
    print("  C4: OFF, the idn-like incumbent keeps the slot")


def check_c6() -> None:
    env = world.bind(gridworld.family("default", 0))
    g = gamma.Gamma(env.atoms(), game="g")
    lib = g.library
    n = g.accept(gamma.Term((lib["inc"].atoms[0], lib["dbl"].atoms[0])), 0, "r").name
    g.keep_evidence = True
    g.settle(n, slot="a", null="beat")
    g.settle(n, slot="b", null="tied")
    assert g.standing[n].beat_on == {"a"}, g.standing[n].beat_on
    h = gamma.Gamma(env.atoms(), game="g")
    h.accept(gamma.Term((h.library["inc"].atoms[0], h.library["dbl"].atoms[0])), 0, "r")
    h.replay([list(r) for r in g.evidence])
    assert h.standing[n].beat_on == set(), h.standing[n].beat_on
    print("  C6: beat_on gains the beat slot only; replay clears it")


def main() -> int:
    check_c1_c5()
    check_c2()
    check_c3()
    check_c4()
    check_c6()
    print("c1_crowd: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
