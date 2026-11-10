"""C5 THE TRANSLATION TABLE (the reviewer 2026-11-10 r1638, r1640, r1641), arm TETHER_TRANSLATE.

  T1  the table: per process an ordered recipe -- the first entry a formula step, every later one
      marked "+" (at once) or "->" (in sequence), each with its BECAUSE
  T2  the reader: an exit choice writes a "translate" row naming the step that decided, the recipe
      and provenance "prior"
  T3  the ground's book: a turn whose next frame explained bits books "paid" on the step that
      decided it, one that explained none books "missed"
  T4  MF: a step the ground refused (missed MIN_REPEAT times, never paid) is skipped: refusing
      "least-tried" takes the tried counts off the exit choice; unrefused, they are on it
  T5  OFF: no reader rows
  T6  G4 (r1647): MF the which-exit row compares every step with its book and says why; a site the
      ground cannot book says "no credit reading at this site yet" and carries no paid/refused

    python tests/test_translate.py
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

STEPS = {"PERCEIVE", "ROUTE", "MINT", "ACCEPT", "SETTLE", "PROMOTE", "7", "2", "REPEAT"}


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="translate"), tether.Config(),
                        ledger.Ledger())


def _rows(ag: tether.Agent, ev: str) -> list:
    return [r["detail"] for r in ag.led.rows() if r["event"] == ev]


def check_t1() -> None:
    for proc, recipe in tether.TRANSLATE.items():
        assert recipe[0][0] in STEPS, (proc, recipe[0])
        assert all(m in ("+", "->") for m, _k, _b in recipe[1:]), proc
        assert all(b for _m, _k, b in recipe), proc
    print(f"  T1: {len(tether.TRANSLATE)} processes, each an ordered recipe with its marks and "
          f"BECAUSE")


def check_t2_t3() -> None:
    ag = _agent()
    for _ in range(4):
        ag.step()
    rows = [d for d in _rows(ag, "translate") if d["process"] == "which exit"]
    assert rows and all(d["provenance"] == "prior" and d["because"] for d in rows), rows[:1]
    n = len(tether.TRANSLATE["which exit"])
    assert all(d["checked"] == f"{n} of {n} steps" and len(d["book"]) == n and d["why_won"]
               for d in rows), "MF: a which-exit row without what it compared"
    ag._translate("what to look up", "owed", at="x")
    other = _rows(ag, "translate")[-1]
    assert other["credit"] == "no credit reading at this site yet" and "book" not in other \
        and "refused" not in other, "MF: an unbooked site read as booked"
    book = {k: v for k, v in ag._tr_rec.items() if k[0] == "which exit"}
    assert sum(p + m for p, m in book.values()) >= len(rows) - 1, (book, len(rows))
    ag._tr_last = ("which exit", "draw")
    ag._ex_last = (ag._lk(), "probe", ag.pe_integral() - ag.outstanding(), ag.cycle)
    before = list(ag._tr_rec.get(("which exit", "draw"), [0, 0]))
    ag._ex_settle()
    assert ag._tr_rec[("which exit", "draw")] == [before[0], before[1] + 1], "a zero is a miss"
    print(f"  T2-T3: {len(rows)} exit choices read as recipe steps; the ground's book {book}; "
          f"nothing explained books a miss")


def check_t4() -> None:
    ag = _agent()
    ag._tr_rec[("which exit", "least-tried")] = [0, tether.MIN_REPEAT]
    for _ in range(3):
        ag.step()
    off = [r["detail"] for r in ag.led.rows()
           if r["event"] == "choice" and r["detail"].get("site") == "exit"]
    assert off and all(d["seen"] is None for d in off), "MF: a refused step still decided"
    ag2 = _agent()
    for _ in range(3):
        ag2.step()
    on = [r["detail"] for r in ag2.led.rows()
          if r["event"] == "choice" and r["detail"].get("site") == "exit"]
    assert on and all(d["seen"] is not None for d in on), "MF: tried counts missing unrefused"
    print(f"  T4: least-tried refused: {len(off)} exit choices with no tried counts; unrefused, "
          f"{len(on)} with them")


def check_t5() -> None:
    keep, tether._TRANSLATE = tether._TRANSLATE, False
    try:
        ag = _agent()
        for _ in range(3):
            ag.step()
    finally:
        tether._TRANSLATE = keep
    assert not _rows(ag, "translate"), "OFF: a reader row"
    print("  T5: OFF, no reader rows")


if __name__ == "__main__":
    for c in (check_t1, check_t2_t3, check_t4, check_t5):
        c()
    print("translate: OK")
