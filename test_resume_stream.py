"""The re-walk's must-fails (the reviewer 2026-10-10 04:31Z). A frontier hit continues the closure
stream the last mint suspended instead of re-enumerating it, and only when the stream's order is
unchanged, so every row is the same with the resume on or off (the arms header aside, which lists
the switch). Read per arm as (rows equal to OFF, chains enumerated, resumes, hits):
  1. as built: rows equal, fewer chains, resumes > 0;
  2. the ranking flips every other cycle: rows equal (it falls back); with the depth-1 ORDER left
     out of the signature, rows differ;
  3. the unit order rotates every other cycle (same set): rows equal; with the UNIT ORDER left out
     of the signature, rows differ.
Cases 2 and 3 run with the work budget CUT, since order decides only what a cut walk reaches.

    python test_resume_stream.py
"""
from __future__ import annotations

import sys

import gamma
import gridworld
import ledger
import retrieval
import tether
import world

sys.dont_write_bytecode = True

CYCLES = 12                                   # the first hit on this board lands at cycle 9
CUT = 300                                     # a work budget that cuts walks on this board
AG: list = []
N = {"enum": 0, "resume": 0, "hit": 0}

_enum, _resume, _lookup = (gamma.Gamma.enumerate_closure, tether._Kept.resume,
                           tether.Agent._frontier_lookup)
_fits, _sig = retrieval.fits, tether._stream_sig


def _spy_enum(self, *a, **k):
    for c in _enum(self, *a, **k):
        N["enum"] += 1
        yield c


def _spy_resume(self):
    N["resume"] += 1
    return _resume(self)


def _spy_lookup(self, slot, key):
    e = _lookup(self, slot, key)
    N["hit"] += e is not None
    return e


gamma.Gamma.enumerate_closure = _spy_enum
tether._Kept.resume = _spy_resume
tether.Agent._frontier_lookup = _spy_lookup


def _odd() -> bool:
    return bool(AG) and AG[0].cycle % 2 == 1


def _flipped_fits(*a, **k):
    f = _fits(*a, **k)
    return -f if _odd() else f


def _rotated_rank(t):
    return [-ord(c) for c in t.name] if _odd() else t.name


def _run(resume: bool, perturb: str = "", blind: int | None = None) -> tuple:
    """A perturbed run cuts every walk short (work_budget CUT): order decides only what a CUT walk
    reaches, so with whole walks a blinded signature would pass and the must-fail be vacuous."""
    for k in N:
        N[k] = 0
    tether._RESUME_STREAM = resume
    retrieval.fits = _flipped_fits if perturb == "rank" else _fits
    tether._stream_sig = ((lambda *a: tuple(x for i, x in enumerate(_sig(*a)) if i != blind))
                          if blind is not None else _sig)
    env = world.bind(gridworld.family("default", 1, CYCLES))
    cfg = tether.Config(work_budget=CUT) if perturb else tether.Config()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="dt_default_1"), cfg, ledger.Ledger())
    if perturb == "units":
        ag.gamma.unit_rank = _rotated_rank
    AG[:] = [ag]
    for _ in range(CYCLES):
        ag.step()
    return ag.led.rows()[1:], dict(N)


def _read(name, rows, n, off) -> tuple:
    same = rows == off
    print(f"  {name:<34} rows equal to OFF {same}; enumerated {n['enum']}; resumes "
          f"{n['resume']}; hits {n['hit']}")
    return same


if __name__ == "__main__":
    ok = True
    off, n_off = _run(False)
    _read("as built, OFF", off, n_off, off)
    rows, n = _run(True)
    ok &= _read("as built, ON", rows, n, off) and n["enum"] < n_off["enum"] and n["resume"] > 0
    for perturb, blind, what in (("rank", 1, "depth-1 order"), ("units", 0, "unit order")):
        off_p, n_off_p = _run(False, perturb)
        assert n_off_p["hit"] > 0, f"{perturb}: no frontier hits, so nothing could fall back"
        rows, n = _run(True, perturb)
        ok &= _read(f"{perturb} perturbed, ON", rows, n, off_p)
        rows, n = _run(True, perturb, blind)
        ok &= not _read(f"{perturb} perturbed, ON, {what} blinded", rows, n, off_p)
    print("ok" if ok else "FAIL")
    sys.exit(0 if ok else 1)
