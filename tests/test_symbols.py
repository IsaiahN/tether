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
import symbols  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


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
    assert set(got) | {"w"} == set(symbols.BOUND), "S2: a bound symbol is not exercised"
    print(f"  S2: 13 bound symbols read on gridworld after 6 steps (slot {slot}: R {got['R']:.3f} "
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
    print("symbols: OK")


if __name__ == "__main__":
    main()
