"""Item 3's fixture, carry credit (TETHER_CARRY_PRICE; the reviewer 2026-10-09 16:31Z to 21:37Z).

A minted term paid its cost at its own entry (DISCOVERY 503). Reused where it RE-GROUNDS -- pays on
the slot's own record alone, left < base -- it is priced on its leftover, and the library fit takes
the lowest WHOLE price instead of the first payer in fit order. Each check runs the same record with
the arm OFF and ON (the module flag, set here only):
  - two-level rebind (R-D4): OFF keeps the copy-forward, ON takes the general rule;
  - MF-D5: a carried rule is not credited before it re-grounds on the new record, and is after;
  - q2: credit on a slot with a DIFFERENT name than the one it was minted on;
  - one-slot lookup: a recording never re-grounds, so it earns nothing;
  - pooled-only (a GUARD, holds both ways): a term never minted pays on no single slot;
  - MF-D3: a pre-boundary record closed by the sweep is marked STALE (arm ON only); its promotion
    waits for a settle in this level in BOTH arms, which since P2 is P2's hold, not item 3's;
  - (r): a credited term still pays for NAMING it, log2(H+1) (the reviewer 21:55Z), so one whose
    reduction is no more than that does not pay; with the reference cost removed, it does.

    python test_carry.py
"""
from __future__ import annotations

import sys

import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="carry_fixture"),
                        tether.Config(), ledger.Ledger())


def _record(ag: tether.Agent, slots: dict[str, list[int]], alphabet: int = 2) -> None:
    """A fresh level's trace: each slot follows its sequence."""
    n = len(next(iter(slots.values())))
    states = [{s: seq[i] for s, seq in slots.items()} for i in range(n)]
    ag.trace = [(states[i], "A", states[i + 1], None, None) for i in range(n - 1)]
    ag._trace_pos = None
    for s in slots:
        if s not in ag.slots:
            ag.slots = [*ag.slots, s]
        ag.alphabet[s] = alphabet
    ag.bound = {}


def _boundary(ag: tether.Agent) -> None:
    """What `retarget` does to the carry state: a new level starts after everything held."""
    ag.level += 1
    ag._seq_at_level = len(ag.led) + 10_000
    ag._settled_lvl = set()


def _mint(ag: tether.Agent, names: tuple[str, ...], operand: str | None = None) -> str:
    t = ag.gamma.build(names, operand=operand)
    ag.gamma.accept(t, seq=len(ag.led), residual="fixture")
    return t.name


def _fit(ag: tether.Agent, slot: str, arm: bool) -> tuple[str | None, dict | None]:
    tether._CARRY_PRICE = arm
    try:
        got = ag._library_fit(slot, None)
    finally:
        tether._CARRY_PRICE = False
    rows = [r for r in ag.led.rows() if r["event"] == "pull" and r["slot"] == slot]
    return got, (rows[-1]["detail"].get("carry") if rows else None)


FLIP = [0, 1] * 8
GENERAL = ("inc", "inc", "inc")          # x -> x+3 = flip, mod 2: longer than one level can pay
# The two-level record: x swaps 0 and 3 in an alphabet of 5. No single atom does it (so the
# control cannot pick a prior); x -> 3 - x does, four atoms, longer than one short level can pay;
# the copy-forward `take<x~1>` does it after its one unseen start.
SWAP = [0, 3] * 4
SWAP_RULE = ("neg", "inc", "inc", "inc")


def _two_level(slot: str = "x") -> tuple[tether.Agent, str, str]:
    ag = _agent()
    _record(ag, {slot: SWAP}, 5)
    gen = _mint(ag, SWAP_RULE)
    copy = _mint(ag, ("take",), operand=f"{slot}~1")
    _boundary(ag)
    _record(ag, {slot: SWAP}, 5)
    return ag, gen, copy


def check_two_level_rebind() -> None:
    ag, gen, copy = _two_level()
    off, _ = _fit(ag, "x", False)
    ag2, gen2, copy2 = _two_level()
    on, carry = _fit(ag2, "x", True)
    print(f"  two-level: OFF -> {off}, ON -> {on}, carry={carry}")
    assert off == copy, f"the control must keep the copy-forward (else the test cannot fail): {off}"
    assert on == gen2, f"carry ON must take the general rule on the whole price: {on}"
    assert carry["credited"] and carry["carried"], carry


def check_mf_d5_no_credit_before_regrounding() -> None:
    ag = _agent()
    _record(ag, {"x": FLIP})
    gen = _mint(ag, GENERAL)
    _boundary(ag)
    _record(ag, {"x": [0, 0, 1, 1] * 4})  # a residual the flip law does not reduce
    rows0 = len(ag.led.rows())
    before, carry_b = _fit(ag, "x", True)
    assert any(r["event"] in ("pull", "reach_failed") for r in ag.led.rows()[rows0:]), "not asked"
    _record(ag, {"x": FLIP})              # and right on this one
    after, carry_a = _fit(ag, "x", True)
    print(f"  MF-D5: before re-grounding -> {before} {carry_b}; after -> {after}")
    assert before != gen, "credited before it re-grounded"
    assert after == gen and carry_a["credited"], carry_a


def check_q2_credit_on_another_slot_name() -> None:
    ag = _agent()
    _record(ag, {"x": FLIP})
    gen = _mint(ag, GENERAL)
    _boundary(ag)
    _record(ag, {"y": FLIP})
    off, carry_off = _fit(ag, "y", False)
    on, carry_on = _fit(ag, "y", True)
    print(f"  q2: OFF -> {off}; ON -> {on} {carry_on}")
    assert off != gen, f"OFF must charge the cost again, so the long rule does not pay: {off}"
    assert on == gen and carry_on["credited"], carry_on


def check_one_slot_lookup_earns_nothing() -> None:
    ag = _agent()
    # a recording: on level 1 x's next value is z's value now; on level 2 it never is
    _record(ag, {"x": FLIP, "z": [1 - v for v in FLIP]})
    rec = _mint(ag, ("take",), operand="z")
    _boundary(ag)
    _record(ag, {"x": FLIP, "z": FLIP})
    on, carry = _fit(ag, "x", True)
    print(f"  one-slot lookup: ON -> {on} {carry}")
    assert on != rec, "a recording that does not re-ground earned credit"
    log = [k for k in ag._carry_log if k[0] == rec]
    assert not log, log


def check_pooled_only_is_refused_on_every_slot() -> None:
    """A GUARD: a term never minted has paid nothing, so it is charged per slot both ways."""
    ag = _agent()
    _record(ag, {"x": FLIP, "y": FLIP})
    t = ag.gamma._install(ag.gamma.build(GENERAL, origin=gamma.IMPORTED), seq=-1, residual=None)
    for arm in (False, True):
        for s in ("x", "y"):
            got, _ = _fit(ag, s, arm)
            assert got != t.name, (arm, s, got)
    print("  pooled-only: refused on x and y, arm OFF and ON")


def check_mf_d3_stale_close_waits_for_a_settle_here() -> None:
    res = {}
    for arm in (False, True):
        ag = _agent()
        _record(ag, {"x": list(range(8)) * 2}, 8)    # x counts up: `inc . dec . inc` explains it
        hist = ag.history("x")
        ag.parked["L0:x"] = {"slot": "x", "level": 0, "hist": hist, "slots": list(ag.slots),
                             "verdict": "depth_exhausted", "units_then": -1}
        _boundary(ag)
        _record(ag, {"w": [0] * 4})
        name = _mint(ag, ("inc", "dec", "inc"))
        tether._CARRY_PRICE = arm
        try:
            ag.sweep(ag.gamma.library[name], "w")
            ag._promote()
            first = sum(r["event"] == "promote" for r in ag.led.rows())
            ag._settled_lvl.add(name)
            ag._promote()
            second = sum(r["event"] == "promote" for r in ag.led.rows())
        finally:
            tether._CARRY_PRICE = False
        res[arm] = (first, second, [r.get("stale") for r in ag.retro])
    print(f"  MF-D3: OFF (promoted, after settle, stale) = {res[False]}; ON = {res[True]}")
    # SINCE P2 (94051f5) the hold is P2's in BOTH arms: no sweep promotion before a settle in this
    # level. What item 3 still adds is the STALE marking of a pre-boundary close, ON only.
    assert res[False][:2] == (0, 1) and res[True][:2] == (0, 1), f"P2's hold: {res}"
    assert res[False][2] == [None] and res[True][2] == [True], f"the STALE marking: {res}"


def check_r_naming_is_not_free() -> None:
    # flips on 9 of 15 transitions: idn leaves 9 bits, the flip rule 6 -- a 3-bit reduction
    seq = [0]
    for f in [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]:
        seq.append(seq[-1] ^ f)
    got = {}
    for ref in (True, False):
        ag = _agent()
        _record(ag, {"x": FLIP})
        gen = _mint(ag, GENERAL)
        _record(ag, {"x": seq})
        h, bits = ag._carry_ref()
        tether._CARRY_REF = ref
        try:
            got[ref] = _fit(ag, "x", True)
        finally:
            tether._CARRY_REF = True
    print(f"  (r): H={h}, log2(H+1)={bits:.3f}; with the reference cost -> {got[True][0]}; "
          f"without -> {got[False][0]} {got[False][1]}")
    assert bits >= 3.0, "the fixture's 3-bit reduction must not exceed the reference cost"
    assert got[False][0] == gen, "the control: at price = left the 3-bit reduction pays"
    assert got[True][0] != gen, "a credited term paid less than it costs to name it"


CHECKS = [check_two_level_rebind, check_mf_d5_no_credit_before_regrounding,
          check_q2_credit_on_another_slot_name, check_one_slot_lookup_earns_nothing,
          check_pooled_only_is_refused_on_every_slot,
          check_mf_d3_stale_close_waits_for_a_settle_here, check_r_naming_is_not_free]

if __name__ == "__main__":
    bad = 0
    for c in CHECKS:
        try:
            c()
            print(f"ok   {c.__name__}")
        except AssertionError as e:
            bad += 1
            print(f"FAIL {c.__name__}: {e}")
    print(f"{len(CHECKS) - bad}/{len(CHECKS)} passed")
    sys.exit(1 if bad else 0)
