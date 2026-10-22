"""The probe's record keeps F500's order (the reviewer 2026-10-14 07:33, 07:42). The flipped panel's
fake member was refused by the gate (step-order, "o1.stability: MINT after ACCEPT", seq 2129): the
probe flush wrote a MINT row for every starved slot, a slot whose own turn had already minted and
accepted this cycle included.

  (a) a starved slot whose turn ran this cycle: no MINT row lands on it after its ACCEPT; it is
      named on the "@probe" row's already_turned, which B5 reads as probed;
  (b) a starved slot whose turn did not run: it takes its own MINT "probe" row, as before;
  (c) nothing starved: one "@probe" row, as before.

Step order is read with gate._steps, not gate.check: a hand record carries no PERCEIVE bets.

    python tests/test_probe_flush.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gamma
import gate
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="probe_flush_fixture"),
                        tether.Config(), ledger.Ledger())


def _probes(ag, slot: str) -> list[dict]:
    return [r for r in ag.led.rows() if r["slot"] == slot and r["event"] == "probe"]


def test_a_turned_starved_slot_takes_no_mint_after_its_accept():
    ag = _agent()
    s = next(x for x in ag.slots if not x.startswith("@"))
    ag.led.record(ag.cycle, "MINT", s, "mint", term="t")
    ag.led.record(ag.cycle, "ACCEPT", s, "accept", term="t")
    ag._starved = {s}
    ag._flush_probe({s})
    assert gate._steps(ag.led.rows()) is None, gate._steps(ag.led.rows())
    assert not _probes(ag, s), _probes(ag, s)
    at = _probes(ag, "@probe")
    assert len(at) == 1 and at[0]["detail"]["already_turned"] == [s], at
    assert not ag._starved


def test_b_an_unturned_starved_slot_keeps_its_own_row():
    ag = _agent()
    s = next(x for x in ag.slots if not x.startswith("@"))
    ag._starved = {s}
    ag._flush_probe(set())
    assert gate._steps(ag.led.rows()) is None
    assert len(_probes(ag, s)) == 1 and not _probes(ag, "@probe")


def test_c_nothing_starved_writes_one_probe_row():
    ag = _agent()
    ag._flush_probe(set())
    at = _probes(ag, "@probe")
    assert len(at) == 1 and "already_turned" not in at[0]["detail"], at


if __name__ == "__main__":
    test_a_turned_starved_slot_takes_no_mint_after_its_accept()
    print("  (a) a starved slot past its turn: no MINT after its ACCEPT; named on @probe")
    test_b_an_unturned_starved_slot_keeps_its_own_row()
    print("  (b) a starved slot before its turn keeps its own probe row")
    test_c_nothing_starved_writes_one_probe_row()
    print("  (c) nothing starved: one @probe row")
    print("probe flush: OK")
