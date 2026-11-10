"""C1 PHASE 1, record only (the reviewer 2026-11-09 r1584 1, 5; the D2 header parts 1 and 6 (a)).

  N1  gamma.settle(null="beat") counts beat_null, null="tied" counts tied_null, no null counts
      neither; confirmations rise by one each time (beat_null + tied_null <= confirmations)
  N2  on a gridworld run, every settle-path settle is counted once: the terms' beat_null sum equals
      the settle rows with risky true, tied_null the rows with risky false (item 6's own reading)
  B1  every transition bet row reads back its board_fp (16 hex) and action by its seq, with its
      slot, with no second store
  N3  with TETHER_SETTLE_PRED OFF the settle rows carry no risky and the tallies are the same:
      they count from _settle_pred's reading, not from the row field (r1591)
  MF  the null cannot hide in the total: settling a term null="beat" and another null="tied"
      leaves them DIFFERENT on beat_null

    python tests/test_c1_null.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import world  # noqa: E402


def check_n1_mf() -> None:
    env = world.bind(gridworld.family("default", 0))
    g = gamma.Gamma(env.atoms(), game="g")
    name = next(iter(g.library))
    st0 = g.standing.setdefault(name, gamma.Standing())
    c0 = st0.confirmations
    g.settle(name, slot="s", null="beat")
    g.settle(name, slot="s", null="tied")
    g.settle(name, slot="s")
    st = g.standing[name]
    assert (st.beat_null, st.tied_null, st.confirmations - c0) == (1.0, 1.0, 3.0), st
    assert st.beat_null + st.tied_null <= st.confirmations
    other = [n for n in g.library if n != name][0]
    g.settle(other, slot="s", null="tied")
    assert g.standing[other].beat_null != st.beat_null, "MUST-FAIL: beat and tied counted alike"
    print("  N1/MF: beat, tied and an unread settle counted apart; beat_null + tied_null <= "
          "confirmations")


# r1654: each 40-step run in its OWN process. Under the purse (counted heads) a second run in a
# warm process spends fewer heads for the same work, so two runs sharing a process part at a cut
# whatever the arm; a fresh process per run is the identity N3 claims
PROBE = r'''
import json, sys
import _repo
import gamma, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
for _ in range(40):
    ag.step()
tally = [sum(s.beat_null for s in ag.gamma.standing.values()),
         sum(s.tied_null for s in ag.gamma.standing.values())]
print(json.dumps({"tally": tally, "rows": ag.led.rows()}, default=str))
'''


def _start(pred: bool) -> subprocess.Popen:
    env = dict(os.environ, TETHER_SETTLE_PRED="1" if pred else "0", PYTHONDONTWRITEBYTECODE="1")
    return subprocess.Popen([sys.executable, "-c", PROBE], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, env=env, cwd=_repo.ROOT)


def _finish(p: subprocess.Popen) -> dict:
    out, err = p.communicate(timeout=1700)
    assert p.returncode == 0, err[-2500:]
    return json.loads(out.strip().splitlines()[-1])


def _tally(run: dict) -> tuple:
    return tuple(run["tally"])


def check_n2_b1_n3() -> None:
    # r1660: ON and OFF side by side, each in its own process, so the pair fits the 1800 s cap
    on_p, off_p = _start(True), _start(False)
    ag, off = _finish(on_p), _finish(off_p)
    rows = ag["rows"]
    settles = [r["detail"] for r in rows if r["event"] == "settle"
               and r["detail"].get("status") == "accepted"]
    risky = sum(1 for d in settles if d.get("risky") is True)
    # TETHER_SETTLE_BEAT_NULL (default ON, r1633): a tied settle counts tied_null but does not
    # tip, and is written as its own settle_tied row rather than an accepted settle
    quiet = (sum(1 for d in settles if d.get("risky") is False)
             + sum(1 for r in rows if r["event"] == "settle_tied"))
    beat, tied = _tally(ag)
    assert settles, "occasion: no settle-path settle in 40 gridworld steps"
    assert (beat, tied) == (risky, quiet), ((beat, tied), (risky, quiet))
    bets = [r for r in rows if r["event"] == "bet" and r["detail"].get("channel") == "transition"]
    assert bets, "occasion: no transition bet"
    by_seq = {r["seq"]: r for r in rows}
    for r in bets:
        d = by_seq[r["seq"]]["detail"]
        assert re.fullmatch(r"[0-9a-f]{16}", d.get("board_fp") or ""), d
        assert d.get("action") and r["slot"], r
    print(f"  N2: {len(settles)} settle-path settles, beat_null {beat:g} = risky {risky}, "
          f"tied_null {tied:g} = not risky {quiet}")
    print(f"  B1: {len(bets)} transition bet rows, each with board_fp, action and slot by seq")
    off_settles = [r["detail"] for r in off["rows"] if r["event"] == "settle"
                   and r["detail"].get("status") == "accepted"]
    assert not any("risky" in d for d in off_settles), "the arm is OFF and risky was written"
    assert _tally(off) == (beat, tied), (_tally(off), (beat, tied))
    print(f"  N3: TETHER_SETTLE_PRED OFF: no risky on {len(off_settles)} settle rows; the tallies "
          f"still count from _settle_pred's reading, {_tally(off)}")


def main() -> int:
    check_n1_mf()
    check_n2_b1_n3()
    print("c1_null: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
