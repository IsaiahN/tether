"""THE OVERRUN SAFETY NET, single-agent form: C1 widened (Isaiah 2026-10-22 12:36-12:37; the
reviewer 12:37, 15:17, 15:24, 15:34). One deadline every growing loop on the step path reads at
its head, shared by every module, so gamma, composer, arc_world and the rest read it without
importing tether.

AT is the agent's thinking deadline (the runner's deadline less the end-path reserve), set by
Agent.step for the step and cleared after it, so nothing outside a step (the end path above all)
is ever cut. A cut is a filter's stop, never a verdict (Fig 9 :60): it unwinds to step, which
records what was not reached.

CapReached is a BaseException, so no "except Exception" anywhere can swallow a cut
(interface._is_relational has one) and a fault catch never reads a cut as a fault. hold() keeps
a unit whole: inside it no head raises, and a hold inside a hold stays held until the outer one
exits."""
from __future__ import annotations

import contextlib
import functools
import time

import armflag

_CAP_INNER = armflag.arm("TETHER_CAP_INNER", default=True)
AT: float | None = None
_HOLD = 0
_now = time.time


class CapReached(BaseException):
    """The thinking deadline passed at a loop head: the step stops between whole units."""


def head() -> None:
    """A growing loop's head: raise CapReached once the thinking deadline has passed, unless
    held."""
    if AT is None or _HOLD or not _CAP_INNER:
        return
    if _now() >= AT:
        raise CapReached


@contextlib.contextmanager
def hold():
    """No head raises inside; restored on any exit, a BaseException's included; re-entrant."""
    global _HOLD
    _HOLD += 1
    try:
        yield
    finally:
        _HOLD -= 1


def held(fn):
    """The entry head, then the whole function held: a unit the end path reads, kept whole."""
    @functools.wraps(fn)
    def run(*a, **k):
        head()
        with hold():
            return fn(*a, **k)
    return run


def holding(fn):
    """The whole function held with NO entry head of its own: for a unit whose caller has already
    written state that must meet it (step's _ruin_step key, then perceive's press; the reviewer
    2026-10-22 15:40), so the last cut before it falls before that write."""
    @functools.wraps(fn)
    def run(*a, **k):
        with hold():
            return fn(*a, **k)
    return run
