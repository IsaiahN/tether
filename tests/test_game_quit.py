"""31 THE GAME-LEVEL QUIT (TETHER_GAME_QUIT, default ON; the reviewer 2026-11-06 r1291; Isaiah
r892 (2): "Quitting is the last resort, and only where an external budget exists"). gridworld
default seed 0, the agent seed pinned, 6 steps; the clocks and rates PLANTED (tests/_repo.py), the
budget readings planted as the runner would set them. Each check its own process.
  check_q1_no_budget        games_waiting None: never, everything exhausted and run_rate set
  check_q1b_no_run_rate     games waiting, run_rate None (no game finished): never
  check_q2_open_line_stays  the proposer still open (a next line at the seed) and stay > go: stays
  check_q3_spent_quits      every escalation spent and the game's level rate under the run's: a
                            game_quit row and ag._quit
  check_q3b_currency        a game whose lines all read under rho but whose levels in the slice
                            beat go: STAYS (rho is not the currency)
  check_q3c_step_reaches    one real step with the budget planted ends in a quit (the step's end
                            calls the weighing)
  check_q4_no_verdict       a quit books nothing: the books and every standing unchanged, and the
                            quit's own standing not created by the read
  check_q5_runner           b_worker and e4_stream set the budget readings, break with ending
                            "quit" and call the second-meeting close; the share's next slice is
                            larger after an early end (planted clock)
  check_q5b_fixed_slices    under fixed slices games wait only while the run deadline binds
                            (r1292): not binding, None and no quit; binding, set and a quit
  check_q6_met_advanced     met again with the same or larger slice and advanced: one against
  check_q6b_met_not         met again and not advanced: one paid
    python tests/test_game_quit.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys
import time

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    assert tether._GAME_QUIT, "TETHER_GAME_QUIT is OFF"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    return ag


def _plant(ag, waiting=3, run_rate=0.01, played=100.0, left=100.0, levels=0, open_line=False):
    """The runner's readings and the clocks: `played` seconds into the game, `left` seconds of
    its slice to go, one second per step; the proposer exhausted unless `open_line`."""
    now = time.time()
    ag._tc_rates = lambda: (1.0, 0.0001)
    ag.deadline = None
    ag.slice_from, ag.slice_until = now - played, now + left
    ag.games_waiting, ag.run_rate = waiting, run_rate
    ag._game_levels, ag._quit, ag._hyp = levels, False, None
    known = sum(len(v.get("delta", {})) for v in ag.iface.table.values())
    ag._hyp_exhausted = None if open_line else known


def _rows(ag, event):
    return [r["detail"] for r in ag.led.rows() if r["event"] == event]


def check_q1_no_budget() -> None:
    ag = _agent()
    _plant(ag, waiting=None)
    ag._quit_weigh()
    assert not ag._quit and not _rows(ag, "game_quit")
    print("  no games waiting: no quit")


def check_q1b_no_run_rate() -> None:
    ag = _agent()
    _plant(ag, run_rate=None)
    ag._quit_weigh()
    assert not ag._quit and not _rows(ag, "game_quit")
    print("  games waiting, no game finished yet: no quit")


def check_q2_open_line_stays() -> None:
    ag = _agent()
    _plant(ag, run_rate=0.005, open_line=True)      # go 0.5 x p 2/3 = 0.33 < stay 2/3
    ag._quit_weigh()
    assert not ag._quit and not _rows(ag, "game_quit")
    _plant(ag, run_rate=0.005)                      # the same, every line spent: stay 0
    ag._quit_weigh()
    assert ag._quit, "the control did not quit: the open line was not what held it"
    print("  proposer open (stay 0.667 > p x go 0.333): stays; the same budget, spent: quits")


def check_q3_spent_quits() -> None:
    ag = _agent()
    _plant(ag)
    ag._quit_weigh()
    q = _rows(ag, "game_quit")
    assert ag._quit and len(q) == 1, q
    r = q[0]
    assert r["stay"] == 0 and r["go"] > 0 and r["line"] == "none" and r["games_waiting"] == 3, r
    assert r["escalation"]["proposer_exhausted"] and ag._quit_last["desc"] == r["desc"], r
    print(f"  spent, game rate 0: quit (go {r['go']:.3f}, p {r['p']}, stay 0)")


def check_q3b_currency() -> None:
    ag = _agent()
    _plant(ag, levels=2)              # 2 levels in 100 s: 2.0 levels in the slice, against go 1.0
    ag._tc_rho = lambda: 1e9          # every line's bits rate under rho
    ag._quit_weigh()
    assert not ag._quit and not _rows(ag, "game_quit")
    print("  bits under rho, levels in the slice 2.0 > p x go 0.667: stays")


def check_q3c_step_reaches() -> None:
    ag = _agent()
    _plant(ag, run_rate=1.0, open_line=True)        # go 100 levels: quits whatever the line holds
    ag.step()
    assert ag._quit and _rows(ag, "game_quit")
    print("  one real step under the planted budget ends in a game_quit row")


def check_q4_no_verdict() -> None:
    import copy
    ag = _agent()
    _plant(ag)
    book = dict(ag.gamma.book)
    st = {f: copy.deepcopy(r["standing"]) for f, r in ag._reflexes.items()}
    ag._quit_weigh()
    assert ag._quit
    assert dict(ag.gamma.book) == book
    assert {f: r["standing"] for f, r in ag._reflexes.items()} == st
    assert not ag._reflexes["quit"]["standing"], "the read created a quit standing"
    print(f"  quit with the books and {len(st)} standing stores unchanged")


def check_q5_runner() -> None:
    import tether
    assert tether._GAME_QUIT, "TETHER_GAME_QUIT is OFF"
    from pathlib import Path
    for p in ("kaggle/b_worker.py", "harness/mem_store/e4_stream.py"):
        s = Path(_repo.ROOT, p).read_text(encoding="utf-8")
        for line in ("ag.games_waiting = arc_holdout.games_waiting(",
                     "ag.run_rate = run_levels / run_secs",
                     'if getattr(ag, "_quit", False):', 'ending = "quit"', "ag.quit_met_close()"):
            assert line in s, (p, line)
    # b_worker's share, read at a slice's start: mx = (DL - now - longest) * N / left
    s = Path(_repo.ROOT, "kaggle/b_worker.py").read_text(encoding="utf-8")
    assert "mn = mx = max(0.0, (DL - time.time() - longest) * N / left)" in s
    dl, longest, n, left = 1000.0, 10.0, 1, 2
    early, late = (dl - 100.0 - longest) * n / left, (dl - 300.0 - longest) * n / left
    assert early > late
    print(f"  both runners carry the quit; the next slice {early:.0f} s after a quit at 100 s, "
          f"{late:.0f} s after the full slice")


def check_q5b_fixed_slices() -> None:
    import arc_holdout
    ag = _agent()
    dl, end, fixed = 2000.0, 1000.0, 300.0      # 1000 s left after this slice's end
    fits = arc_holdout.games_waiting(3, False, dl, end, fixed)     # 2 x 300 <= 1000
    binds = arc_holdout.games_waiting(5, False, dl, end, fixed)    # 4 x 300 > 1000
    assert fits is None and binds == 4, (fits, binds)
    assert arc_holdout.games_waiting(3, True, dl, end, fixed) == 2     # the share: always
    _plant(ag, waiting=fits)
    ag._quit_weigh()
    assert not ag._quit and not _rows(ag, "game_quit")
    _plant(ag, waiting=binds)
    ag._quit_weigh()
    assert ag._quit and _rows(ag, "game_quit")
    print("  fixed slices: the later games fit -> no games waiting, no quit; the deadline "
          "binds -> 4 waiting, a quit")


def _met(levels: int) -> dict:
    ag = _agent()
    now = time.time()
    ag.slice_from, ag.slice_until = now - 100.0, now + 100.0     # a 200 s meeting
    ag.met_again, ag._game_levels = {"desc": ["avatar"], "slice_s": 150.0}, levels
    ag.quit_met_close()
    st = ag._reflexes["quit"]["standing"][(("avatar",),)]
    assert ag.met_again is None and len(_rows(ag, "quit_settled")) == 1
    return st


def check_q6_met_advanced() -> None:
    st = _met(1)
    assert st["against"] == 1 and st["paid"] == 0, st
    print("  met again, advanced: one against on the quit")


def check_q6b_met_not() -> None:
    st = _met(0)
    assert st["paid"] == 1 and st["against"] == 0, st
    print("  met again, not advanced: one paid")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    bad = [n for n in names if subprocess.run([sys.executable, "-B", __file__, n],
                                              cwd=str(_repo.ROOT),
                                              stdin=subprocess.DEVNULL).returncode]
    assert not bad, bad
    print(f"game_quit: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
