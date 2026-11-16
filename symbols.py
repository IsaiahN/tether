"""THE SYMBOL BINDING TABLE (item 2b; the reviewer 2026-11-13 r1948/r1949, Isaiah 23:28
"compete 1-9 and put into development"; design docs/04-PLANS_AHEAD/02-BUILD_SEQUENCE_FUTURE_STATE
.md item 2b).

library/grammar.json holds the formula's symbols as text only. A symbol the agent cannot evaluate
is a name with nothing behind it (Fig 9 :30 "your words are borrowed too, so describe the
effect"), so the cards' do_sym forms could not run. This module ties each symbol to the agent
reading that evaluates it. The meanings are the Symbols table's own (grammar.json "symbols", from
the figure); a binding says WHERE the value is read.

Rules:
  - evaluate() never invents a value. A symbol with no reading yet returns UNBOUND, with the
    reason in UNBOUND_WHY, and so does any binding whose reading is absent on this agent or world.
  - nothing here changes behaviour: it only reads. The agenda reader (item 2a, TETHER_AGENDA) is
    the first caller; until it lands, no code calls this module.
  - kind_of_reading() tags a reading as a STATE (space, time, energy) or a STRUCTURE (spectrum,
    gradient, network), the Symbols table's six, so the reader picks "A state asks for its
    structure" or "A structure asks for its states" correctly (cards v4 (a); the hand test's #9).
    A reading it can't place is (None, None): unknown, never guessed.

    python -c "import symbols; print(symbols.table())"
"""
from __future__ import annotations

import json
import os
import sys
from collections.abc import Callable
from typing import Any

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))


class _Unbound:
    """The non-reading: the symbol (or this world) has no value for it here."""

    def __repr__(self) -> str:
        return "UNBOUND"

    def __bool__(self) -> bool:
        return False


UNBOUND = _Unbound()


def _grammar_symbols() -> dict:
    with open(os.path.join(HERE, "library", "grammar.json"), encoding="utf-8") as fh:
        return json.load(fh)["symbols"]


def _last_mass(ag: Any, slot: str) -> Any:
    """The slot's latest transition residual: the mass on its last PERCEIVE "bet" row (the agent
    keeps no per-slot copy past the step; the ledger is the record)."""
    for e in reversed(ag.led.entries):
        if e.step == "PERCEIVE" and e.event == "bet" and e.slot == slot and "mass" in e.detail:
            return float(e.detail["mass"])
    return UNBOUND


def _live_mass(ag: Any, slot: str) -> Any:
    m = _last_mass(ag, slot)
    return m if m is UNBOUND else max(0.0, m)


def _term(ag: Any, name: str) -> Any:
    return ag.gamma.library.get(name, UNBOUND)


def _cost(ag: Any, name: str) -> Any:
    t = _term(ag, name)
    if t is UNBOUND:
        return UNBOUND
    import tether
    return float(tether.term_bits(ag.gamma.length(t), ag.gamma.alphabet))


def _reach(ag: Any, slot: str) -> Any:
    out = getattr(ag, "_out_of_reach", None)
    return UNBOUND if out is None else (not out(slot))


def _predict(ag: Any, slot: str, action: str) -> Any:
    v = ag._predict(slot, ag.env.observe(), action)
    return UNBOUND if v is None else v


# symbol -> (where it is read, the reading); the reading takes the agent and the named arguments
BOUND: dict[str, tuple[str, Callable[..., Any]]] = {
    "Γ": ("agent.gamma: the atoms and the library's terms, counted",
          lambda ag: {"atoms": len(ag.gamma.atoms), "terms": len(ag.gamma.library)}),
    "atoms(Γ)": ("agent.gamma.atoms: the primitives' names",
                 lambda ag: sorted(a.name for a in ag.gamma.atoms)),
    "closure(Γ)": ("agent._out_of_reach(slot), negated: can a term for this slot's residual be "
                   "composed from the vocabulary as it stands (the walkthrough's reach check)",
                   _reach),
    "b": ("agent.env.observe() read before acting: what the agent takes to be the case",
          lambda ag: dict(ag.env.observe())),
    "w": ("agent.gamma.term_w[name]: the weighting carried with a term, where one is held",
          lambda ag, name: ag.gamma.term_w.get(name, UNBOUND)),
    "a": ("agent.env.actions(): the actions offered now",
          lambda ag: tuple(ag.env.actions())),
    "o′": ("the observation after the action, as perceive() reads it: pass after=",
           lambda _ag, after=None: UNBOUND if after is None else dict(after)),
    "Γ(b,a)": ("agent._predict(slot, b, action): what the library predicts for the slot",
               _predict),
    "R": ("the slot's last PERCEIVE bet row's mass, in bits (the ledger)", _last_mass),
    "s": ("agent.env.slots(): the slots tracked now", lambda ag: list(ag.env.slots())),
    "R⁺_s": ("max(0, R) on the slot: the part the prediction missed", _live_mass),
    "φ": ("agent.gamma.library[name]: a term, by name", _term),
    "|φ|": ("term_bits(gamma.length(term), gamma.alphabet): its length under the uniform code",
            _cost),
}

UNBOUND_WHY: dict[str, str] = {
    "|R|φ|": "computed inside the mint pipeline's bargain (left(R, φ)) at minting; no standalone "
             "reading yet",
    "bond": "the seven bond types are priced (BONDS) but no reading names the bond between two "
            "given operands yet (O3, bond pricing, is planned)",
    "molecule": "terms are compositions, but no reading returns a term's bonded arrangement",
    "T_A": "abstraction (going up) runs inside carry and kind; no reading names one step of it",
    "T_E": "concretisation (coming back) runs inside re-invention; no reading names one step of it",
    "R_T": "the round-trip gap is not measured as a quantity yet",
    "F": "the frame transform needs a pose; the agent has none to run it with",
    "the ground": "never bound: the Symbols table says it is not in the library and the loop "
                  "cannot modify it. The board's own response is the ground",
    "the habitat": "everything in contact with the residual, enumerated; no single reading lists "
                   "it yet",
}


def table() -> dict[str, dict]:
    """Every grammar symbol: its meaning, and where it is read or why it is unbound."""
    out = {}
    for sym, meaning in _grammar_symbols().items():
        if sym in BOUND:
            out[sym] = {"meaning": meaning, "bound": True, "reads": BOUND[sym][0]}
        else:
            out[sym] = {"meaning": meaning, "bound": False,
                        "why": UNBOUND_WHY.get(sym, "no binding written")}
    return out


def evaluate(sym: str, ag: Any, **kw: Any) -> Any:
    """The symbol's value on this agent now, or UNBOUND. Never raises, never invents."""
    b = BOUND.get(sym)
    if b is None:
        return UNBOUND
    try:
        return b[1](ag, **kw)
    except (AttributeError, KeyError, TypeError, ValueError, IndexError):
        return UNBOUND


# the Symbols table's six, read off the attribute a reading publishes (the part after the slot's
# name and its dot). A reading not listed is unknown.
_STATE = {
    "space": ("row", "col", "h", "w", "drow", "dcol", "add_row", "add_col", "rem_row", "rem_col",
              "free", "blocked", "pass"),
    "time": ("age", "stability"),
    "energy": ("dcells", "add_n", "rem_n"),
}
_STRUCTURE = {
    "spectrum": ("scale", "grew", "shrank"),
    "network": ("contact", "touching", "touch", "adjacent", "link", "group", "corridor", "path"),
}


def kind_of_reading(reading: str) -> tuple[str | None, str | None]:
    """("state", "space") ... ("structure", "network"), or (None, None) for a reading it can't
    place. `reading` may be "o3.row" or just "row"."""
    attr = reading.rsplit(".", 1)[-1]
    for which, table_ in (("state", _STATE), ("structure", _STRUCTURE)):
        for kind, names in table_.items():
            if attr in names or any(attr.startswith(n + "_") for n in names):
                return which, kind
    return None, None
