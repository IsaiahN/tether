"""0b WORDS_CARRY (TETHER_WORDS_CARRY, default ON; BUILD_SEQUENCE 0b, the reviewer r1942; built on
Isaiah's 2026-11-16 "build out" the sequence). Within one game, what each action did carries to the
next board as an expectation; the first press on a later board checks it.
  W1  board 0: the hold counts every unpressed action (as OFF)
  W2  board 1: actions pressed on board 0 are not held; a never-pressed one is
  W3  the same kind-shape -> verdict "met"; more objects moved -> "met, condition changed"
  W4  a different shape -> "contradicted": held again on this board until pressed again
  MF-W1 TETHER_WORDS_CARRY=0 -> board 1 holds every unpressed action again -> RED as required
  W5  gridworld 12 steps ON and OFF both pass the gate
Seconds.
    python tests/test_words_carry.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

ACTS = ("A1", "A2", "A3")


def press(i, a, sig):
    """What audit does for one press: the seam's note, then the check."""
    i.note_sent(a)
    if IFace._WORDS_CARRY:
        i._words_check(a, sig)


def main() -> int:
    assert IFace._WORDS_CARRY is True, "the arm defaults ON"
    i = IFace.Interface()
    assert i.untried_here(ACTS) == 3
    press(i, "A1", (("o1.col", 1),))
    press(i, "A2", (("o1.row", -1),))
    assert i.untried_here(ACTS) == 1, i.untried_here(ACTS)
    print("W1 board 0: the hold counts the unpressed action only (as OFF): GREEN")

    i.situate(1, True, new_board=True)
    assert i.untried_here(ACTS) == 1, ("W2: A1/A2 should carry, A3 held", i.untried_here(ACTS))
    print("W2 board 1: carried actions are not held, the never-pressed one is: GREEN")

    press(i, "A1", (("o4.col", 1),))
    assert i.last_words["verdict"] == "met", i.last_words
    i2 = IFace.Interface()
    press(i2, "A1", (("o1.col", 1),))
    i2.situate(1, True, new_board=True)
    press(i2, "A1", (("o4.col", 1), ("o5.col", 1)))
    assert i2.last_words["verdict"] == "met, condition changed", i2.last_words
    print("W3 same shape -> met; same shape, more objects -> met, condition changed: GREEN")

    press(i, "A2", (("o4.col", 1),))           # A2 moved rows on board 0, columns here
    assert i.last_words["verdict"] == "contradicted", i.last_words
    assert i.untried_here(ACTS) == 2, ("W4: A2 back in the hold beside A3", i.untried_here(ACTS))
    press(i, "A2", (("o4.col", 1),))
    assert i.untried_here(ACTS) == 1, ("W4: pressed again, A2 leaves the hold",
                                       i.untried_here(ACTS))
    print("W4 contradicted -> held again until pressed again here: GREEN")

    IFace._WORDS_CARRY = False
    j = IFace.Interface()
    press(j, "A1", (("o1.col", 1),))
    j.situate(1, True, new_board=True)
    n = j.untried_here(ACTS)
    IFace._WORDS_CARRY = True
    assert n == 3, n
    print("MF-W1 the arm OFF: board 1 holds all 3 actions again -> RED (as required)")

    for on in (True, False):
        IFace._WORDS_CARRY = on
        env = world.bind(gridworld.family("default", 0))
        led = ledger.Ledger()
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                          led)
        for _ in range(12):
            ag.step()
        ag.end_run("cap")
        v = gate.check(led.rows())["verdict"]
        assert v == "pass", ("W5: the gate refused", on, v)
    IFace._WORDS_CARRY = True
    print("W5 gridworld 12 steps ON and OFF: both pass the gate: GREEN")
    print("words_carry: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
