"""The arrived_no_clear correction must be readable as subtext and reversible.

Fig 9 :53 "the gap does [choose], and the gap is only as good as its description":
a no-clear is a correction whose meaning is published on the goal's KIND, read back by the
proposer, and undone by a later paid success. No game identity, no answer, no threshold.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import snaps  # noqa: E402
import tether as T  # noqa: E402
from gamma import Gamma  # noqa: E402
from ledger import Ledger  # noqa: E402
from tether import Agent, Config  # noqa: E402
from world import bind  # noqa: E402


def _agent():
    w = snaps.Snap(snaps.spec_for(0, 3))
    return Agent(bind(w), Gamma(snaps._atoms()), Config(), Ledger())


def test_stop_is_published_and_read():
    ag = _agent()
    kind = (ag._ss_form("ALL(BECOME(o0.row, 1))"), ag._kind_key("o0.row"))
    ag._reflexes["steer"]["standing"].clear()
    # The steer reads only when 1 + paid < against: one witness is deliberately not enough
    # (Fig 10, a claim needs a basis). Two no-clears at this kind make the reading live.
    ag._ss_stop("objective", "subtext", kind)
    ag._ss_stop("objective", "subtext", kind)
    p = ag._ss_hyp_price("ALL(BECOME(o9.row, 1))", "o9.row")  # same kind, different object
    assert p > 0, ("the subtext stop did not price the same kind up", p, kind)
    print("stop published and read: OK", round(p, 3))


def test_reversible_by_paid_success():
    ag = _agent()
    kind = (ag._ss_form("ALL(BECOME(o0.row, 1))"), ag._kind_key("o0.row"))
    ag._reflexes["steer"]["standing"].clear()
    ag._ss_stop("objective", "subtext", kind)
    ag._ss_stop("objective", "subtext", kind)
    priced = ag._ss_hyp_price("ALL(BECOME(o9.row, 1))", "o9.row")
    assert priced > 0, priced
    for _ in range(4):
        ag._ss_pay("objective", "subtext", kind)   # a success at this kind undoes the stop
    paid = ag._ss_hyp_price("ALL(BECOME(o9.row, 1))", "o9.row")
    assert paid == 0.0, ("a paid success did not restore the kind", priced, paid)
    print("reversible by paid success: OK")


def test_arm_off_is_identity():
    ag = _agent()
    kind = (ag._ss_form("ALL(BECOME(o0.row, 1))"), ag._kind_key("o0.row"))
    ag._reflexes["steer"]["standing"].clear()
    T._CORRECTION_SUBTEXT = False
    ag._ss_stop("objective", "subtext", kind)
    p = ag._ss_hyp_price("ALL(BECOME(o9.row, 1))", "o9.row")
    T._CORRECTION_SUBTEXT = True
    assert p == 0.0, ("arm OFF still read the subtext line", p)
    print("arm OFF identity: OK")


def test_must_fail_no_stop_no_price():
    # If the correction line is not published, nothing prices the kind up -- this is the
    # failure path that must remain real: the stop is what makes the check able to fire.
    ag = _agent()
    ag._reflexes["steer"]["standing"].clear()
    p = ag._ss_hyp_price("ALL(BECOME(o9.row, 1))", "o9.row")
    assert p == 0.0, ("a kind with no stop was priced up -- proxy", p)
    print("MF no-stop: OK")


if __name__ == "__main__":
    test_stop_is_published_and_read()
    test_reversible_by_paid_success()
    test_arm_off_is_identity()
    test_must_fail_no_stop_no_price()
    print("correction-subtext: OK")
