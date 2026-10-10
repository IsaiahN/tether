"""The routine mint forms an intent and does not take it (the reviewer 2026-10-10 12:27Z, 12:36Z).
`_mint_routine` asks `_goal_split(commit=False)` which press would serve the objective; that press
is not made this turn, so no PLAN intent row is written and `_took` is not called. FORMED stays
(`_goal_want`, `_intent_kinds`); TAKEN goes.

The same gridworld member is run twice in one script, once as built and once with the old
behaviour restored (the mint's call forced back to commit=True):
  1. every action is identical;
  2. the old run's extra rows are exactly the untaken intent (and decision) rows: one per mint
     whose split realised, which is counted and must be at least one (precondition);
  3. every other row is identical (an accept row's own seq, which shifts with each removed row,
     is checked to equal its row's seq instead), and the routine rows' intent_alphabet is
     identical.

    python test_early_mint.py
"""
from __future__ import annotations

import sys
from collections import Counter

import gamma
import gate
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True

CYCLES = 20     # anchor: a declared convention, not measured; long enough on gridworld s0 for the
                #   mint to fire (counted, asserted >= 1); movable


def _run(old: bool) -> tuple[list[dict], int]:
    """(rows, uncommitted splits that realised)."""
    env = world.bind(gridworld.family("default", 0, CYCLES))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="early_mint_fixture"), tether.Config(),
                      ledger.Ledger())
    inner, formed = ag._goal_split, [0]

    def split(before, commit=True):
        act = inner(before, commit=commit or old)
        formed[0] += (not commit) and act is not None
        return act
    ag._goal_split = split
    for _ in range(CYCLES):
        ag.step()
    ag.end_run("cap")
    return ag.led.rows(), formed[0]


def _bare(rows: list[dict]) -> list[tuple]:
    """A row without its position. An `accept` row also names its OWN seq in its detail (the
    term's stamp), which moves with every row removed before it, so that field is left out
    here and checked separately to equal the row's own seq."""
    return [(r["cycle"], r["step"], r["slot"], r["event"],
             repr({k: v for k, v in r["detail"].items()
                   if not (r["event"] == "accept" and k == "seq")})) for r in rows]


if __name__ == "__main__":
    new, formed = _run(old=False)
    old, formed_old = _run(old=True)
    assert formed >= 1 and formed == formed_old, (formed, formed_old)
    acts = [[r["detail"].get("action") for r in rows if r["event"] == "repeat"]
            for rows in (new, old)]
    assert acts[0] == acts[1], "an action differs: the early side effect was load-bearing"
    taken = {"intent", "decision"}
    # MULTISETS, NOT SETS: the untaken intent row is often a byte-identical twin of the intent
    # row the taken split writes the same cycle, and a set comparison hides exactly that.
    extra = list((Counter(_bare(old)) - Counter(_bare(new))).elements())
    assert not Counter(_bare(new)) - Counter(_bare(old)), "the fix added a row"
    assert all(e[3] in taken for e in extra), [e[3] for e in extra if e[3] not in taken]
    n_int = sum(e[3] == "intent" for e in extra)
    assert n_int == formed, (n_int, formed)
    keep = [r for r in old if r["event"] not in taken]
    assert _bare([r for r in new if r["event"] not in taken]) == _bare(keep)
    for rows in (new, old):
        assert all(r["detail"]["seq"] == r["seq"] for r in rows if r["event"] == "accept")
    alpha = [[r["detail"].get("intent_alphabet") for r in rows if r["event"] == "routine"]
             for rows in (new, old)]
    assert alpha[0] == alpha[1], alpha
    out = gate.check(new)
    assert out["verdict"] == gate.PASS, out
    print(f"  gridworld s0, {CYCLES} cycles: {len(acts[0])} actions identical; the mint formed "
          f"{formed} intents it did not take; the old run's extra rows are those {n_int} intent "
          f"rows and {len(extra) - n_int} decision rows; every other row identical; "
          f"intent_alphabet on {len(alpha[0])} routine rows identical; full gate passes")
    print("ok")
