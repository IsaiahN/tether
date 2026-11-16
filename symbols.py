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


def _leftover(ag: Any, slot: str, name: str) -> Any:
    """|R|φ|: Agent._accumulated(slot, term) -- the function mint() itself calls for the held
    term's `base` (cost + left < base, Fig 5 :43): `_left` over the slot's whole history, in bits.
    Called, never reimplemented. Held so no cap head can cut it, and the shared head count is put
    back, so the read leaves the step's purse where it found it."""
    t = _term(ag, name)
    if t is UNBOUND or slot not in ag.alphabet:
        return UNBOUND
    import cap
    heads = cap.HEADS
    try:
        with cap.hold():
            return float(ag._accumulated(slot, t))
    finally:
        cap.HEADS = heads


def _bond(ag: Any, a: str, b: str) -> Any:
    """bond: the junction keys the agent holds between a and b, each with its bond -- read off
    Agent._junction_conds (key -> (bond, u, v)), where _route_junction writes a settled junction
    between two readings and O2's _jk_combine one between two keys. Both orders are read, so an
    ordered bond (⋛, ⇒) keeps its direction in its key. None held: UNBOUND."""
    held = {k: c[0] for k, c in sorted(ag._junction_conds.items())
            if (c[1], c[2]) in ((a, b), (b, a))}
    return held or UNBOUND


def _grammar_operators() -> dict:
    with open(os.path.join(HERE, "library", "grammar.json"), encoding="utf-8") as fh:
        return json.load(fh)["operators"]


def _bond_names() -> tuple[str | None, dict]:
    """Read off grammar.json's operators: the bond a chain IS (the operator whose implemented_by
    names gamma.Term's chain: "→"), and each two-operand bond's AGENT atoms -> (bond, the entry's
    own qualifier or None). Nothing here is written by hand."""
    chain, atoms = None, {}
    for op, row in _grammar_operators().items():
        for imp in row.get("implemented_by", ()):
            if imp.startswith("a chain (gamma.Term)"):
                chain = op
            elif imp.startswith("AGENT|") and row.get("arity") == 2:
                name, _, rest = imp[len("AGENT|"):].partition(" ")
                atoms[name] = (op, rest.strip("() ") or None)
    return chain, atoms


def _arrangement(ag: Any, t: Any, chain: str | None, atoms: dict) -> dict:
    """One node of a term's bonded arrangement, its operand tree nested where 10d nests it
    (Term.operand_term, the same recursion gamma.tree_schema walks and Agent._ops evaluates)."""
    node: dict = {"atoms": [a.name for a in t.atoms],
                  "chain_bond": chain if len(t.atoms) > 1 else None,
                  "operand": t.operand,
                  "operand_bonds": [[a.name, *atoms.get(a.name, (None, None))]
                                    for a in t.atoms if a.reads_operand],
                  "operand_term": (None if t.operand_term is None
                                   else _arrangement(ag, t.operand_term, chain, atoms))}
    if t.guard:
        jc = getattr(ag, "_junction_conds", {}).get(t.guard_ref) if t.guard_ref else None
        node["guard"] = {"kind": t.guard, "ref": t.guard_ref,
                         "bond": None if jc is None else jc[0]}
    return node


def _molecule(ag: Any, name: str) -> Any:
    """molecule: the library term's bonded arrangement -- its atoms in chain order with the chain's
    bond, each operand-reading atom with the bond grammar.json says it implements (None where the
    grammar names none: unknown, never guessed), its guard with the junction's bond where the
    guard is a routed key, and its operand tree nested."""
    t = _term(ag, name)
    if t is UNBOUND:
        return UNBOUND
    chain, atoms = _bond_names()
    return _arrangement(ag, t, chain, atoms)


def _bracket_row(ag: Any) -> Any:
    """The latest PERCEIVE "@bracket" bet row where the agent ran its coarse view (perceive:
    coarse_view=True); a row reporting CHANNEL_CLOSED is no reading."""
    for e in reversed(ag.led.entries):
        if e.step == "PERCEIVE" and e.event == "bet" and e.slot == "@bracket":
            return e if e.detail.get("coarse_view") else UNBOUND
    return UNBOUND


def _round_trip(ag: Any) -> Any:
    """R_T: the bracket row's mass -- perceive's `self._round_trip(self._view[1], before)`, i.e.
    round_trip_gap, the gap between x and T_E(T_A(x)) in bits, recorded each step the world
    offers a coarse view."""
    e = _bracket_row(ag)
    return e if e is UNBOUND else float(e.detail["mass"])


def _abstraction(ag: Any) -> Any:
    """T_A: the view the bracket channel applies going up (Agent._view: its name, recorded on the
    row, and its map), applied to b -- only where the agent ran it (a coarse-view row)."""
    e = _bracket_row(ag)
    if e is UNBOUND or e.detail.get("view") != ag._view[0]:
        return UNBOUND
    return {"view": ag._view[0], "up": dict(ag._view[1](dict(ag.env.observe())))}


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
    "|R|φ|": ("agent._accumulated(slot, term): the bargain's own left(R, φ), the bits φ leaves "
              "unexplained over the slot's history (mint's `base` for the held term); pass slot=, "
              "name=", _leftover),
    "bond": ("agent._junction_conds: the junction keys held between a= and b= (two readings, or "
             "two keys for an O2 junction of conditions), key -> bond", _bond),
    "molecule": ("agent.gamma.library[name]: the term's atoms with the chain bond, its "
                 "operand-reading atoms' bonds (grammar.json operators), its guard's junction "
                 "bond, and its operand tree nested (Term.operand_term, 10d)", _molecule),
    "R_T": ("the last PERCEIVE @bracket bet row's mass where the coarse view ran: "
            "round_trip_gap, x against T_E(T_A(x)), in bits (the ledger)", _round_trip),
    "T_A": ("agent._view, applied to b: the view the bracket channel sends the state up through, "
            "where it ran (a coarse-view @bracket row)", _abstraction),
}

UNBOUND_WHY: dict[str, str] = {
    "T_E": "concretisation exists only inside round_trip_gap, as 'the coarse value taken "
           "literally' (the comparison of t_a(state) with state); no function or reading returns "
           "one step of it, so binding it would write a map the agent does not run",
    "F": "the frame transform needs a pose; the agent holds none. library_runtime crosses an "
         "axis-bound relation across an episode with its axis as a variable (_AXIS_SWAP), an axis "
         "renaming, not an allocentric<->egocentric transform the agent runs on a reading",
    "the ground": "never bound: the Symbols table says it is not in the library and the loop "
                  "cannot modify it. The board's own response is the ground",
    "the habitat": "everything in contact with the residual, enumerated; no single reading lists "
                   "it: no agent reading enumerates what is in contact with a given residual",
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
