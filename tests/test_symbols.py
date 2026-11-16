"""THE SYMBOL BINDING TABLE (symbols.py; item 2b, the reviewer r1948/r1949).
  S1  every symbol in library/grammar.json is in the table: bound with where it is read, or
      unbound with its reason; none missing, none extra
  S2  on a gridworld agent after 6 steps, every bound symbol evaluates to a value (w may be
      UNBOUND where no term carries a weighting, o′ needs after=), with the type it promises
  S3  never invents: an unbound symbol, an unknown symbol, a missing slot and a missing term
      all return UNBOUND, never raise. MF-S3: "the ground" is UNBOUND by definition
  S4  kind_of_reading: position is a state (space), age a state (time), dcells a state (energy),
      scale a structure (spectrum), contact a structure (network); colour and shape are unknown
  S5  only agenda.py (the agenda reader, 2a) imports symbols; nothing else in the agent reads it
  S6  the symbols bound since: |R|φ| (the bargain's _accumulated, idn checked by hand), bond
      (junctions routed by _route_junction and an O2 key pair), molecule (a hand-built two-deep
      operand tree), R_T and T_A (snaps' coarse-view row; UNBOUND on gridworld, channel closed).
      MF-S6: each returns UNBOUND with its binding removed
Seconds.
    python tests/test_symbols.py
"""
from __future__ import annotations

import os
import subprocess
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import snaps  # noqa: E402
import symbols  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

NEW = ("|R|φ|", "bond", "molecule", "R_T", "T_A")    # bound since 2b; exercised in S6


def main() -> None:
    gram = symbols._grammar_symbols()
    tab = symbols.table()
    assert set(tab) == set(gram), ("S1: the table and grammar.json differ",
                                   set(tab) ^ set(gram))
    assert all(v["bound"] == (k in symbols.BOUND) for k, v in tab.items())
    assert all(v.get("reads") or v.get("why") for v in tab.values()), "S1: a row says nothing"
    nb = sum(v["bound"] for v in tab.values())
    print(f"  S1: {len(tab)} symbols, {nb} bound, {len(tab) - nb} unbound with reasons")

    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    for _ in range(6):
        ag.step()
    slots = symbols.evaluate("s", ag)
    assert slots, "S2: no slots"
    slot = next((s for s in slots if symbols.evaluate("R", ag, slot=s) is not symbols.UNBOUND),
                None)
    assert slot is not None, "S2 occasion: no slot with a bet row"
    act = symbols.evaluate("a", ag)[0]
    name = next(iter(ag.gamma.library))
    got = {
        "Γ": symbols.evaluate("Γ", ag),
        "atoms(Γ)": symbols.evaluate("atoms(Γ)", ag),
        "closure(Γ)": symbols.evaluate("closure(Γ)", ag, slot=slot),
        "b": symbols.evaluate("b", ag),
        "a": symbols.evaluate("a", ag),
        "o′": symbols.evaluate("o′", ag, after=ag.env.observe()),
        "Γ(b,a)": symbols.evaluate("Γ(b,a)", ag, slot=slot, action=act),
        "R": symbols.evaluate("R", ag, slot=slot),
        "s": slots,
        "R⁺_s": symbols.evaluate("R⁺_s", ag, slot=slot),
        "φ": symbols.evaluate("φ", ag, name=name),
        "|φ|": symbols.evaluate("|φ|", ag, name=name),
    }
    w = symbols.evaluate("w", ag, name=name)
    for k, v in got.items():
        assert v is not symbols.UNBOUND, ("S2: a bound symbol read nothing", k)
    assert got["Γ"]["atoms"] > 0 and got["Γ"]["terms"] > 0
    assert isinstance(got["closure(Γ)"], bool) and isinstance(got["R"], float)
    assert got["R⁺_s"] >= 0.0 and got["|φ|"] > 0 and isinstance(got["b"], dict)
    assert set(got) | {"w"} | set(NEW) == set(symbols.BOUND), "S2: a bound symbol is not exercised"
    print(f"  S2: 13 bound symbols of 2b read on gridworld after 6 steps (slot {slot}: R "
          f"{got['R']:.3f} "
          f"bits, reach {got['closure(Γ)']}; |{name}| {got['|φ|']:.2f} bits; w {w!r})")

    for sym in symbols.UNBOUND_WHY:
        assert symbols.evaluate(sym, ag) is symbols.UNBOUND, ("S3", sym)
    assert symbols.evaluate("no such symbol", ag) is symbols.UNBOUND
    assert symbols.evaluate("R", ag, slot="no.such.slot") is symbols.UNBOUND
    assert symbols.evaluate("φ", ag, name="no such term") is symbols.UNBOUND
    assert symbols.evaluate("|φ|", ag, name="no such term") is symbols.UNBOUND
    assert symbols.evaluate("o′", ag) is symbols.UNBOUND
    assert symbols.evaluate("the ground", ag) is symbols.UNBOUND, "MF-S3"
    print("  S3: unbound, unknown, missing slot and missing term all UNBOUND; the ground never "
          "bound")

    cases = {"o3.row": ("state", "space"), "age": ("state", "time"),
             "o1.dcells": ("state", "energy"), "scale": ("structure", "spectrum"),
             "contact_faces": ("structure", "network"), "o2.colour": (None, None),
             "shape": (None, None)}
    for r, want in cases.items():
        assert symbols.kind_of_reading(r) == want, ("S4", r, symbols.kind_of_reading(r))
    print("  S4: position/age/dcells are states, scale/contact structures, colour/shape unknown")

    hits = subprocess.run(["git", "-C", _repo.ROOT, "grep", "-l", "-E",
                           r"^\s*(import symbols|from symbols import)", "--", "*.py"],
                          capture_output=True, text=True).stdout.split()
    callers = [h for h in hits if not h.startswith("tests/")]
    assert callers == ["agenda.py"], ("S5: only the agenda reader imports symbols", callers)
    print("  S5: only agenda.py (the reader, 2a) imports symbols")
    s6(ag, slot)
    print("symbols: OK")


def _mf(sym: str, ag, **kw) -> None:
    """MF: with the binding removed, the symbol reads UNBOUND."""
    held = symbols.BOUND.pop(sym)
    try:
        assert symbols.evaluate(sym, ag, **kw) is symbols.UNBOUND, ("MF-S6", sym)
    finally:
        symbols.BOUND[sym] = held


def s6(ag, slot: str) -> None:
    """S6 the symbols bound since 2b, each on a fixture with its expected value, and each MF."""
    import math
    # |R|φ|: the bargain's own left(R, φ). For idn the value is checkable by hand: one code's
    # length (log2 of the slot's alphabet) per history row whose after-value is not the before.
    idn = ag.gamma.library[tether.IDN]
    hist = ag.history(slot)
    want = sum(math.log2(ag.alphabet[slot]) for s, _a, v, *_r in hist
               if s[slot] % ag.alphabet[slot] != v % ag.alphabet[slot])
    got = symbols.evaluate("|R|φ|", ag, slot=slot, name=tether.IDN)
    assert got == want == ag._accumulated(slot, idn), ("S6 |R|φ|", got, want)
    assert symbols.evaluate("|R|φ|", ag, slot="no.such.slot", name=tether.IDN) is symbols.UNBOUND
    assert symbols.evaluate("|R|φ|", ag, slot=slot, name="no such term") is symbols.UNBOUND
    _mf("|R|φ|", ag, slot=slot, name=tether.IDN)

    # bond: junctions routed by the agent's own writer, and an O2 junction of two keys
    s1, s2, s3 = sorted(ag.env.slots())[:3]
    assert symbols.evaluate("bond", ag, a=s1, b=s2) is symbols.UNBOUND, "S6 bond: none held yet"
    ag._route_junction("≡", s2, s1)
    ag._route_junction("⋛", s1, s3)
    k12, k13, k31 = f"≡:{s1}|{s2}", f"⋛:{s1}|{s3}", f"⋛:{s3}|{s1}"
    nest = f"+:({k12})|({k13})"
    ag._junction_conds[nest] = ("+", k12, k13)          # the shape _jk_combine stores (O2)
    assert symbols.evaluate("bond", ag, a=s1, b=s2) == {k12: "≡"}
    assert symbols.evaluate("bond", ag, a=s2, b=s1) == {k12: "≡"}
    assert symbols.evaluate("bond", ag, a=s3, b=s1) == {k13: "⋛", k31: "⋛"}
    assert symbols.evaluate("bond", ag, a=k12, b=k13) == {nest: "+"}
    assert symbols.evaluate("bond", ag, a=s2, b=s3) is symbols.UNBOUND
    _mf("bond", ag, a=s1, b=s2)

    # molecule: a hand-built two-deep operand tree under a guard on a routed key
    at = {a.name: a for a in ag.gamma.atoms}
    t = gamma.Term((at["inc"], at["same"]), operand=s1, guard=tether.JUNCTION_GUARD,
                   guard_ref=k12, operand_term=gamma.Term((at["dec"],),
                                                          operand_term=gamma.Term((at["neg"],))))
    ag.gamma.library[t.name] = t
    leaf = {"atoms": ["neg"], "chain_bond": None, "operand": None, "operand_bonds": [],
            "operand_term": None}
    want_m = {"atoms": ["inc", "same"], "chain_bond": "→", "operand": s1,
              "operand_bonds": [["same", "≡", "test"]],
              "operand_term": {"atoms": ["dec"], "chain_bond": None, "operand": None,
                               "operand_bonds": [], "operand_term": leaf},
              "guard": {"kind": tether.JUNCTION_GUARD, "ref": k12, "bond": "≡"}}
    got_m = symbols.evaluate("molecule", ag, name=t.name)
    assert got_m == want_m, ("S6 molecule", got_m)
    assert symbols.evaluate("molecule", ag, name=tether.IDN) == {
        "atoms": [tether.IDN], "chain_bond": None, "operand": None, "operand_bonds": [],
        "operand_term": None}
    assert symbols.evaluate("molecule", ag, name="no such term") is symbols.UNBOUND
    _mf("molecule", ag, name=t.name)
    del ag.gamma.library[t.name]

    # R_T and T_A: gridworld offers no coarse view (CHANNEL_CLOSED), so both are UNBOUND there;
    # a snaps world offers one, and the view the agent runs is `full`, measured lossless
    assert symbols.evaluate("R_T", ag) is symbols.UNBOUND
    assert symbols.evaluate("T_A", ag) is symbols.UNBOUND
    sp = snaps.WorldSpec(slots=["s0", "s1"], rules={"s0": snaps.SlotSpec("action", k=1),
                                                    "s1": snaps.SlotSpec("identity")},
                         obj="AVOID", tgt=3, who="s0", start={"s0": 0, "s1": 0})
    sn = tether.Agent(world.bind(snaps.Snap(sp)), gamma.Gamma(snaps._atoms(), game="sym_fixture"),
                      tether.Config(), ledger.Ledger())
    for _ in range(3):
        sn.step()
    rt, ta = symbols.evaluate("R_T", sn), symbols.evaluate("T_A", sn)
    row = next(e for e in reversed(sn.led.entries) if e.slot == "@bracket")
    assert rt == row.detail["mass"] == 0.0, ("S6 R_T", rt)
    assert ta == {"view": "full", "up": dict(sn.env.observe())}, ("S6 T_A", ta)
    _mf("R_T", sn)
    _mf("T_A", sn)
    print(f"  S6: |R|φ| {got} bits (idn on {slot}, by hand {want}); bond ≡/⋛/O2 + read off "
          f"_junction_conds; molecule nested two deep with →, ≡ and the guard's bond; R_T {rt} "
          "and T_A 'full' on snaps, UNBOUND on gridworld; MF each UNBOUND with its binding "
          "removed")


if __name__ == "__main__":
    main()
