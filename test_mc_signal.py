"""7a(4) MC1 + MC2's must-fails, by hand (the reviewer 2026-10-10 07:57Z). The signal is the
TRANSITION bet row the ground answered; ON, each gets exactly one resolution row: kind "level" at
retarget, kind "game" at end_run. The level half has no panel occasion (0 level ends), so it is
shown here.

  1. the sign: paid, failed, vanished-at-mass-0 (failed), suspended / @bracket / @objective (none);
  2. a real run, ON: a level ended by hand at retarget, then the run ended -- every signal has
     exactly one resolution of the right kind, the earlier rows are byte-identical after, the gate
     passes;
  3. MC1: the same hand-made bets with extra mints in one arm give identical signs and resolutions;
     a mutant sign reading an agent count, and one admitting the @bracket row, are both caught.

    python test_mc_signal.py
"""
from __future__ import annotations

import json
import sys

import gamma
import gate
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True


def _row(channel="transition", mass=0.0, **more):
    return {"step": "PERCEIVE", "event": "bet",
            "detail": {"channel": channel, "mass": mass, **more}}


def check_sign() -> None:
    sign = ledger.signal_sign
    got = [sign(_row()), sign(_row(mass=2.0)), sign(_row(mass=0.0, vanished=True)),
           sign(_row(suspended=True)), sign(_row("bracket")), sign(_row("reward"))]
    assert got == ["paid", "failed", "failed", None, None, None], got
    print(f"  sign: {got}")


def check_real_run() -> None:
    tether._MC_SIGNAL = True
    env = world.bind(gridworld.family("default", 1, 12))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="mc_signal_fixture"), tether.Config(),
                      ledger.Ledger())
    for _ in range(6):
        ag.step()
    before = [json.dumps(r, sort_keys=True, default=str) for r in ag.led.rows()]
    n_level = len(ag._signals)
    ag.retarget(env, ag.level + 1, how="death")
    for _ in range(3):
        ag.step()
    ag.end_run("cap")
    rows = ag.led.rows()
    after = [json.dumps(r, sort_keys=True, default=str) for r in rows[:len(before)]]
    assert after == before, "an earlier row changed"
    signals = [r["seq"] for r in rows if ledger.signal_sign(r) is not None]
    res = [r for r in rows if r["event"] == "resolution"]
    by = {}
    for r in res:
        by.setdefault(r["detail"]["signal_seq"], []).append(r["detail"])
    assert sorted(by) == sorted(signals), "a signal unresolved, or a resolution of a non-signal"
    assert all(len(v) == 1 for v in by.values()), "a signal resolved twice"
    kinds = [(by[s][0]["kind"], by[s][0]["how"]) for s in signals]
    assert kinds[:n_level] == [("level", "death")] * n_level and n_level > 0, kinds[:3]
    assert kinds[n_level:] == [("game", "cap")] * (len(signals) - n_level), kinds[-3:]
    assert gate._resolutions(rows) is None, gate._resolutions(rows)
    # NOT the whole gate: a level ended at level 0 already fails its step order on `@loop`, with
    # this arm OFF too (retarget writes cycle=self.level; LEDGER, recorded 2026-10-10).
    print(f"  real run: {len(signals)} signals, {n_level} resolved at the level (death), "
          f"{len(signals) - n_level} at the game (cap); earlier rows unchanged; gate check 14 "
          f"passes")


def _hand(extra_mints: int, sign) -> tuple[list, list]:
    tether._MC_SIGNAL = True
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="mc_signal_hand"), tether.Config(),
                      ledger.Ledger())
    ag.agent_count = lambda: ag.gamma.book.get("minted", 0)   # what a mutant would read
    for i, kw in enumerate(({}, {"mass": 2.0}, {"vanished": True}, {"suspended": True})):
        e = ag.led.record(i, "PERCEIVE", f"s{i}", "bet", channel="transition",
                          mass=kw.pop("mass", 0.0), **kw)
        if not kw.get("suspended"):
            ag._signals.append((e.seq, f"s{i}"))
    ag.led.record(5, "PERCEIVE", "@bracket", "bet", channel="bracket", mass=0.0, actual=None)
    for k in range(extra_mints):                              # a self-produced quantity grows
        at = ag.gamma.atoms
        ag.gamma._install(ag.gamma.build((at[k % len(at)].name, at[(k + 1) % len(at)].name),
                                         origin=gamma.IMPORTED), seq=-1, residual=None)
        ag.gamma.book["minted"] = ag.gamma.book.get("minted", 0) + 1
    ag.retarget(env, ag.level + 1, how="advance")
    rows = ag.led.rows()
    signs = [sign(r, ag) for r in rows]
    res = [r["detail"] for r in rows if r["event"] == "resolution"]
    return signs, res


def _lib(extra: int) -> int:
    """How big the library was in an arm: the extra mints must actually be there."""
    seen = {}
    _hand(extra, lambda _r, ag: seen.setdefault("n", len(ag.gamma.library)))
    return seen["n"]


def check_mc1() -> None:
    def honest(r, _ag):
        return ledger.signal_sign(r)

    def reads_a_count(r, ag):
        s = ledger.signal_sign(r)
        return None if s is None else f"{s}:{ag.agent_count()}"

    def admits_bracket(r, _ag):
        d = r.get("detail") or {}
        if r.get("event") != "bet" or d.get("suspended"):
            return None
        return "paid" if not d.get("vanished") and d.get("mass") == 0 else "failed"

    a, b = _hand(0, honest), _hand(9, honest)
    assert _lib(0) < _lib(9), "the extra mints did not grow the library"
    assert a == b, "the honest sign or the resolutions moved with mints"
    ma, mb = _hand(0, reads_a_count), _hand(9, reads_a_count)
    assert ma[0] != mb[0], "the mutant reading an agent count was not caught"
    bracket = _hand(0, admits_bracket)[0]
    assert bracket != a[0], "the mutant admitting the @bracket row was not caught"
    print(f"  MC1: signs {[s for s in a[0] if s]} and {len(a[1])} resolutions identical with 0 "
          f"and 9 extra mints; mutants caught (agent count; @bracket admitted)")


if __name__ == "__main__":
    for c in (check_sign, check_real_run, check_mc1):
        c()
    print("ok")
