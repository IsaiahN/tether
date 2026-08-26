"""The world, and the eight-slot contract an adapter must satisfy.

If a domain cannot fill all eight members, the framework has not been instantiated there;
it has been mentioned there. So a partial adapter fails at construction, not at run time.

The env here is a symbolic transition world: named slots holding typed values, each with a
hidden per-slot rule, and a ground that is exact match on the next state -- mechanical,
instant, constitutive. There is deliberately no perception layer: a gridworld would test
perception and the loop at once, and then a failure is ambiguous.

One slot's rule is provably outside closure(Gamma) for any budget: every atom below is
affine-with-a-modulus, and OPAQUE is quadratic. The agent is told nothing about this.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from gamma import Atom, Ctx

sys.dont_write_bytecode = True

M = 7   # anchor: prime, and small enough that the harness can sweep the whole
#         domain exhaustively -- which is what makes unreachable_slots a proof
ACTIONS = ("A", "B", "C")
DELTA = {"A": 1, "B": 2, "C": 4}

# Ten members. `actions` and `alphabet` were the two the loop used to reach past the
# contract for, which is why its action set could not grow: a language-level import is a
# step-7 IMPORT executed by the import system instead of by the loop.
REQUIRED = ("substrate", "environment", "actors", "currency", "ground",
            "slots", "atoms", "transform", "actions", "alphabet")


@runtime_checkable
class Env(Protocol):
    """The eight members. Q26 as an import error rather than a paragraph."""

    def substrate(self) -> str: ...
    def environment(self) -> str: ...
    def actors(self) -> str: ...
    def currency(self) -> str: ...
    def ground(self) -> str: ...
    def slots(self) -> list[str]: ...
    def atoms(self) -> list[Atom]: ...
    def transform(self) -> Any: ...
    def actions(self) -> tuple[str, ...]: ...
    def alphabet(self) -> int | dict[str, int]: ...


def bind(env: Any) -> Any:
    """Refuse an adapter that cannot fill all eight."""
    missing = [m for m in REQUIRED if not callable(getattr(env, m, None))]
    if missing:
        raise TypeError(f"env fills {len(REQUIRED) - len(missing)}/{len(REQUIRED)} "
                        f"of the contract; missing: {missing}")
    return env


def _atoms() -> list[Atom]:
    def idn(v, _c):
        return v

    def inc(v, _c):
        return v + 1

    def dec(v, _c):
        return v - 1

    def dbl(v, _c):
        return v * 2

    def neg(v, _c):
        return -v

    def act(v, c):
        return v + DELTA.get(c.action, 0)

    def wrap(v, _c):
        return v % M

    fns = [idn, inc, dec, dbl, neg, act, wrap]
    out = [Atom(f.__name__, f, "val", "val") for f in fns]

    def take(v, c):
        """Read the bound operand slot instead of my own value. The one atom that makes
        an interaction expressible at all."""
        return c.operands[0] if c.operands else v

    out.append(Atom("take", take, "val", "val", reads_operand=True))
    return out


# the hidden rules. Names are for the harness's report, never shown to the agent.
def _steady(v, _a, _s):
    return v


def _climb(v, _a, _s):
    return (v + 1) % M


def _swing(v, _a, _s):
    return (-v + 1) % M


def _driven(v, a, _s):
    return (v + DELTA[a]) % M


def _opaque(v, _a, _s):
    return (v * v + 3) % M      # quadratic: no composition of affine atoms reaches it


def _ladder(v, _a, _s):
    """Four atoms deep -- `dbl . neg . inc . wrap` -- which is PAST max_depth, so it is
    unreachable in atoms. It is `dbl` applied to SWING's rule, so once swing settles and
    becomes one unit it is two units deep and reachable. Nothing was added to the closure;
    only the grain of the search changed. This slot is the chunking claim's falsifier."""
    return (-(v * 2) + 1) % M


def _chase(_v, _a, s):
    """An INTERACTION: this slot's next value is a function of ANOTHER slot's current one,
    and its own value is irrelevant. Unreachable without operand arity, by construction."""
    return (s["climb"] + 1) % M


RULES = {"steady": _steady, "climb": _climb, "swing": _swing,
         "driven": _driven, "opaque": _opaque, "chase": _chase, "ladder": _ladder}

# what the harness knows and the agent does not. Used only to score the demo.
TRUTH = {"steady": "idn (an atom: the answer was already known)",
         "climb": "inc . wrap",
         "swing": "neg . inc . wrap",
         "driven": "act . wrap",
         "opaque": "UNREACHABLE from these atoms -- quadratic, they are all affine",
         "chase": "take<climb> . inc -- an interaction; needs operand arity",
         "ladder": "dbl . neg . inc . wrap -- 4 atoms, past max_depth; 2 units after swing"}


@dataclass
class Transitions:
    """The symbolic transition world."""

    start: dict[str, int] | None = None

    def __post_init__(self) -> None:
        self.state: dict[str, int] = dict(self.start or
                                          {"steady": 3, "climb": 0, "swing": 2,
                                           "driven": 1, "opaque": 2, "chase": 5,
                                           "ladder": 4})

    # -- the eight -------------------------------------------------------------------

    def substrate(self) -> str:
        return f"named slots holding integers mod {M}"

    def environment(self) -> str:
        return f"a hidden per-slot rule; the shaping medium is arithmetic mod {M}"

    def actors(self) -> str:
        return f"the actions {ACTIONS}, which move one slot and are contact for the rest"

    def currency(self) -> str:
        return "prediction error in bits, per slot"

    def ground(self) -> str:
        return "exact match on the next state. Mechanical, instant, and it does not negotiate"

    def slots(self) -> list[str]:
        return sorted(self.state)

    def atoms(self) -> list[Atom]:
        return _atoms()

    def actions(self) -> tuple[str, ...]:
        """What the domain advertises. Growth in this set is an IMPORT, and it can only
        be one if the loop asks rather than reads a module global."""
        return ACTIONS

    def alphabet(self) -> int | dict[str, int]:
        """|V|, the number of distinguishable values. The loop declares the code's FORM
        -- uniform over the alphabet -- and the domain supplies its size; a correction
        therefore costs log2(alphabet) bits and a value normalises mod alphabet.

        ONE NUMBER OR ONE PER SLOT. Every slot here holds an integer mod M, so one number
        says it. A domain whose slots differ -- a position, a colour, a boolean -- says so
        per slot, and each is then charged its own code rather than the widest one in the
        world. Charging a boolean log2(7) inflates its residual by the factor its
        information was reduced, and the bargain comes out loosest where least is at
        stake."""
        return M

    def transform(self) -> Any:
        """No coarse view is defined for this env, so the bracket channel is inert here.
        Stated rather than omitted: the channel exists and this world does not feed it."""
        return None

    # -- running ---------------------------------------------------------------------

    def objective(self) -> tuple[str, float]:
        """ALL slots at zero. Returns (name, degree in [0,1]); R_goal is 1 - degree."""
        hit = sum(1 for v in self.state.values() if v % M == 0)
        return "ALL(BECOME(slot, 0))", hit / len(self.state)

    def observe(self) -> dict[str, int]:
        return dict(self.state)

    def step(self, action: str) -> None:
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        before = dict(self.state)
        self.state = {k: RULES[k](v, action, before) % M for k, v in before.items()}


def unreachable_slots(env: Transitions, gam, max_depth: int, budget: int) -> list[str]:
    """What the HARNESS knows by exhaustive check, and the agent never sees. Used only to
    score abstention: a slot no term in the enumerated closure predicts on every action,
    under any operand binding."""
    slots = env.slots()
    out = []
    for slot in slots:
        rule = RULES[slot]
        binds = [None] + [s for s in slots if s != slot]
        ok = False
        for term in gam.enumerate_closure("val", "val", max_depth, budget):
            for b in binds:
                good = True
                for v in range(M):
                    for a in ACTIONS:
                        st = {s: (v if s == slot else (v + 1) % M) for s in slots}
                        ops = (st[b],) if b else ()
                        if term.apply(v, Ctx(action=a, operands=ops)) % M != rule(v, a, st) % M:
                            good = False
                            break
                    if not good:
                        break
                if good:
                    ok = True
                    break
            if ok:
                break
        if not ok:
            out.append(slot)
    return out
