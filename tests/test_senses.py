"""P4, 8b-1 (TETHER_SENSES; the reviewer r1838; DESIGN_STEP8 B2/B3/B6): a sense is a head's paid /
missed record under the facet key it was minted under.

  SN1   a head minted under a context, settled twice and refuted once, reads paid 2 / missed 1
        under that context and nothing under a context with another src.
  MF-SN THE ROLE-BLIND COLLAPSE (the plant: src dropped from the key): AGENT|translate minted under
        SELF and under WORLD reads as ONE sense -- SN1's "nothing under another src" fails -> RED.
  SN2   the merge, read and never stored: two contexts one facet apart (src), paid 2 each, read as
        one sense (paid 4, merged); a miss in one splits them again (paid 2, not merged).
  SN3   on the dc22 capture (acts forced, c0-18): the agent's own mint on o39.col writes
        sense_pick, its settle writes sense_note paid; after it, every ask on o39.col under the
        pick's door kind and dk gets the paid term first from _sense_terms (P5's stage 0,
        _library_fit's front), and no ask under another dk gets it (a sense is per context).
  gw12's OFF identity against the parent is the commit's check, not this file's.

    python tests/test_senses.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import test_pay_gap as pg

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

HERE = _repo.ROOT
DK = ("POSITION", "+", 1)


def _agent():
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    ag._slot_dk = lambda _s: DK
    return ag


def planted(src_of, drop_src: bool) -> tuple:
    """Mint AGENT|translate on one slot under SELF (settled twice, refuted once) and under WORLD
    (settled once); return the senses read under the SELF context and under the WORLD one."""
    real = tether.source_of
    tether.source_of = lambda _ag, _slot: ("*" if drop_src else src_of[0], None, 0, 0)
    try:
        ag = _agent()
        slot = sorted(ag.slots)[0]
        src_of[0] = "SELF"
        ag._sense_pick(slot, "t_self", "AGENT|translate", "PROCESS")
        ag._sense_settle(slot, "t_self", True)
        ag._sense_settle(slot, "t_self", True)
        ag._sense_settle(slot, "t_self", False)
        src_of[0] = "WORLD"
        ag._sense_pick(slot, "t_world", "AGENT|translate", "PROCESS")
        ag._sense_settle(slot, "t_world", True)
        subj = tether._kind_text(ag._kind(slot.split(".", 1)[0]))
        # with src dropped from the key, the reading drops it too: both read the one record
        return (tether.sense_lookup(ag, ("*" if drop_src else "SELF", subj, DK, "*")),
                tether.sense_lookup(ag, ("*" if drop_src else "WORLD", subj, DK, "*")))
    finally:
        tether.source_of = real


def sn1(drop_src: bool) -> bool:
    self_s, world_s = planted(["SELF"], drop_src)
    print(f"   under SELF: {self_s}; under WORLD: {world_s}")
    return (len(self_s) == 1 and self_s[0][:3] == ("AGENT|translate", 2, 1)
            and len(world_s) == 1 and world_s[0][:3] == ("AGENT|translate", 1, 0))


def sn2() -> tuple:
    real = tether.source_of
    src = ["SELF"]
    tether.source_of = lambda _ag, _slot: (src[0], None, 0, 0)
    try:
        ag = _agent()
        slot = sorted(ag.slots)[0]
        subj = tether._kind_text(ag._kind(slot.split(".", 1)[0]))
        for s, name in (("SELF", "a"), ("COUPLED", "b")):
            src[0] = s
            ag._sense_pick(slot, name, "AGENT|translate", "PROCESS")
            ag._sense_settle(slot, name, True)
            ag._sense_settle(slot, name, True)
        merged = tether.sense_lookup(ag, ("SELF", subj, DK, "*"))
        src[0] = "COUPLED"
        ag._sense_settle(slot, "b", False)
        split = tether.sense_lookup(ag, ("SELF", subj, DK, "*"))
    finally:
        tether.source_of = real
    print(f"   two contexts one facet apart: {merged}; after a miss in one: {split}")
    return (merged == [("AGENT|translate", 4, 0, DK, True)]
            and split == [("AGENT|translate", 2, 0, DK, False)])


SPY = r'''
import atexit
_A = tether.Agent
CALLS = []
_st = _A._sense_terms
def _st2(self, slot):
    out = _st(self, slot)
    if slot == "o39.col":
        dk = self._slot_dk(slot)
        k = tether.facet_key(self, dk, "o39", slot) if dk else None
        CALLS.append([self.cycle, k and [k[1], list(k[2])], out[:2]])
    return out
_A._sense_terms = _st2
atexit.register(lambda: print("SN3 " + json.dumps(CALLS)))
'''


def sn3() -> tuple:
    code = pg.REPLAY.replace("tether._AGENT_SEED = False\n",
                             "tether._AGENT_SEED = False\n" + SPY, 1)
    assert SPY in code
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    led = os.path.join(tempfile.mkdtemp(), "t.jsonl")
    data = os.path.join(HERE, "tests", "data", "cue_key_path", "dc22_c24.json.gz")
    p = subprocess.run([sys.executable, "-B", "-c", code, data, "19", led], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    calls = next(json.loads(x[4:]) for x in p.stdout.splitlines() if x.startswith("SN3 "))
    with open(led, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    picks = [(r["cycle"], r["slot"], r["detail"]["head"],
              [r["detail"]["subj"], r["detail"]["pred"]])
             for r in rows if r["event"] == "sense_pick"]
    notes = [(r["cycle"], r["slot"], r["detail"]["head"], r["detail"]["outcome"]) for r in rows
             if r["event"] == "sense_note"]
    return picks, notes, calls


def main() -> int:
    ok1 = sn1(False)
    print("SN1 paid 2 / missed 1 under SELF, nothing of it under WORLD: "
          + ("GREEN" if ok1 else "RED"))
    assert ok1
    bad = sn1(True)
    print("MF-SN the src facet dropped (the role-blind collapse): "
          + ("RED" if not bad else "GREEN (the plant went unseen)"))
    assert not bad
    ok2 = sn2()
    print("SN2 merged while both pay, split by a miss: " + ("GREEN" if ok2 else "RED"))
    assert ok2
    picks, notes, calls = sn3()
    paid = [n for n in notes if n[3] == "paid"]
    print(f"   sense_pick {picks}; sense_note {notes}")
    pick = next((p_ for p_ in picks if paid and p_[2] == paid[0][2]), None)
    after = [c for c in calls if paid and c[0] > paid[0][0]]
    same = [c for c in after if pick and c[1] == pick[3]]
    other = [c for c in after if pick and c[1] and c[1][1] != pick[3][1]]
    print(f"   asks on o39.col after the settle, same context: {same[:2]}; another dk: {other[:2]}")
    ok3 = (bool(paid) and paid[0][1] == "o39.col" and bool(same) and bool(other)
           and all(c[2] and c[2][0] == paid[0][2] for c in same)
           and not any(paid[0][2] in c[2] for c in other))
    print("SN3 dc22 c0-18: the paid head comes first under its context and only there: "
          + ("GREEN" if ok3 else "RED"))
    assert ok3
    print("senses: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
