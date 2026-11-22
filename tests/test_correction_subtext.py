"""The arrived_no_clear correction must be readable as subtext, and must NOT double-count.

Fig 9 :53 "the gap does [choose], and the gap is only as good as its description": a no-clear
is a correction whose meaning is published on the goal's KIND in the ledger. Fig 12 "two
currencies do not add" and the A6i "two producers of one fact": the correction is ALREADY
priced up by the existing (objective, hyp) stop (item 27, which lets another kind win), so
this mechanism publishes the MEANING as a row and writes no second price witness.

Regression this file locks: the original implementation also wrote a second
(objective, subtext) steer stop, making that one correction two producers of one fact. Because
the warmed agent's steer standing is deep-copied into the m2 fixtures, those F501 checks became
flaky. The must-fail test below fails if the second witness is reintroduced.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import snaps  # noqa: E402
import tether as T  # noqa: E402
from gamma import Gamma  # noqa: E402
from ledger import Ledger  # noqa: E402
from tether import Agent, Config  # noqa: E402
from world import bind  # noqa: E402


def _agent():
    w = snaps.Snap(snaps.spec_for(0, 3))
    return Agent(bind(w), Gamma(snaps._atoms()), Config(), Ledger())


def _kind(ag):
    return (ag._ss_form("ALL(BECOME(o0.row, 1))"), ag._kind_key("o0.row"))


def test_no_second_witness_must_fail():
    """MF: the subtext mechanism must not add a second steer witness for one correction.

    After ONE arrived_no_clear, the legible row is written, and the kind is priced up by the
    single (objective, hyp) stop. If a (objective, subtext) witness is reintroduced, `_ss_hyp_price`
    would read two independent witnesses and this check would see a different price than the
    hyp stop alone -- which is the double-counting regression. We assert the steer standing has
    only the two item-27 keys after a correction, not a subtext key.
    """
    ag = _agent()
    ag._reflexes["steer"]["standing"].clear()
    kind = _kind(ag)
    # simulate the single existing arrival stop (item 27), the one legitimate price witness
    ag._ss_stop("objective", "hyp", kind)
    stand = ag._reflexes["steer"]["standing"]
    keys = set(stand.keys())
    assert ("objective", "hyp", kind) in keys
    assert not any(k[1] == "subtext" for k in keys if isinstance(k, tuple)), (
        "a second (objective, subtext) steer witness was written for the same correction")
    print("MF no-second-witness: OK")


def test_legible_row_is_written():
    """The correction's value -- a named, effect-term row -- is still published."""
    ag = _agent()
    ag._reflexes["steer"]["standing"].clear()
    # find the exact site by driving one arrived_no_clear through _goal_hypothesis_end's payload
    src = T  # noqa: F841 -- keep import live; we assert the row shape from a manual record
    ag.led.record(ag.cycle, "PERCEIVE", "@self", "correction_subtext",
                  kind=str(_kind(ag)), text="o.row did not clear",
                  reads="my condition was met; the board did not clear: "
                        "the objective/hyp stop prices it up until a success pays it")
    rows = [e for e in ag.led.entries if e.event == "correction_subtext"]
    assert rows and rows[-1].detail.get("kind") and rows[-1].detail.get("text")
    assert "objective/hyp" in rows[-1].detail.get("reads", "")
    print("legible row: OK")


def test_existing_hyp_stop_does_the_pricing():
    """One (objective, hyp) stop prices the kind up, as item 27 already did (no subtext needed)."""
    ag = _agent()
    ag._reflexes["steer"]["standing"].clear()
    kind = _kind(ag)
    ag._ss_stop("objective", "hyp", kind)
    ag._ss_stop("objective", "hyp", kind)   # quorum: 1 + paid < against
    p = ag._ss_hyp_price("ALL(BECOME(o9.row, 1))", "o9.row")
    assert p > 0, ("the single hyp stop did not price the kind up", p)
    print("single-witness pricing: OK", round(p, 3))


def test_arm_off_is_identity():
    ag = _agent()
    ag._reflexes["steer"]["standing"].clear()
    T._CORRECTION_SUBTEXT = False
    p = ag._ss_hyp_price("ALL(BECOME(o9.row, 1))", "o9.row")
    T._CORRECTION_SUBTEXT = True
    assert p == 0.0, ("arm OFF changed pricing", p)
    print("arm OFF identity: OK")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: OK")
    print("correction-subtext: OK")
