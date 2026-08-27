"""3a. The four remaining loadable shapes, populated from `ARC_HUMAN_PRIORS.md`.

**LOADING IS NOT ENTERING, and that ruling is what makes this file possible.** §11's two
clauses govern entry into **Γ**; §23.2's test — *does it name what to look at, or what to
do?* — governs **loading into the five non-Γ homes.** Two questions, two tests, no conflict.
SENSOR is `sensors.py`; TERM does not enter at all and lives in `visible.py`.

**EVERY ENTRY CITES A ROW OF THE 130, and that is the whole discipline here.** Nothing below
was chosen because it would help. The catalogue is the source and §12.1's shapes are the
filter, so the question for each is only *which shape is this, and does §23.2 admit it* —
never *is this one useful*. **An invented prior is the move that encodes an answer, and it
would be indistinguishable from a real one after the fact.**

WHAT IS DELIBERATELY ABSENT. The catalogue's §11 (problem solving), §10 (analogical) and §13
(meta-learning) rows are **mostly ROUTINE or ALREADY-THE-LOOP** — means-ends analysis, goal
decomposition, backward chaining are *what to do*; prediction-error learning and uncertainty
monitoring **are the loop already**, and §12.1 names adding them *duplicating the loop inside
the loop*. Neither is loaded.
"""
from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

sys.dont_write_bytecode = True


@dataclass(frozen=True)
class Prior:
    """One catalogue row, in the shape §12.1 says it must take."""

    name: str
    shape: str            # CONSTRAINT | TRACKER | BIAS | BUDGET
    statement: str        # the catalogue's operational statement, not a paraphrase
    citation: str
    fn: Any = None


# -- CONSTRAINT: `prediction -> bool`, a filter BEFORE the bargain (§12.1) ----------------
# §23.2's test: these say which mechanisms are PLAUSIBLE, never which action to take.

def _solidity(state: dict[str, Any]) -> bool:
    """Two objects cannot occupy one location. Reads cell claims, refuses collisions."""
    seen: set = set()
    for slot, v in state.items():
        if not slot.endswith(".cells"):
            continue
        cells = v if isinstance(v, (set, frozenset)) else ()
        if seen & set(cells):
            return False
        seen |= set(cells)
    return True


def _persistence(before: dict[str, Any], after: dict[str, Any]) -> bool:
    """Objects do not cease to exist when unobserved. A slot vanishing is implausible."""
    return not (set(before) - set(after))


CONSTRAINTS = [
    Prior("solidity", "CONSTRAINT", "two objects cannot occupy one location",
          "Baillargeon 1985", _solidity),
    Prior("persistence", "CONSTRAINT", "objects do not cease to exist when unobserved",
          "Baillargeon & DeVos 1991", _persistence),
    Prior("continuity", "CONSTRAINT", "objects travel connected, unobstructed paths",
          "Spelke et al. 1995"),
    Prior("contact", "CONSTRAINT", "objects act only on contact; cannot interpenetrate",
          "Spelke, Phillips & Woodward 1995"),
    Prior("conservation", "CONSTRAINT",
          "a quantity is invariant under appearance-changing transformation",
          "Piaget & Szeminska 1941"),
]


# -- TRACKER: `objs × objs -> ids`, perception's identity rule (§12.1) --------------------

TRACKERS = [
    Prior("numerical_vs_featural", "TRACKER",
          "'same individual' is tracked separately from 'same appearance'",
          "Xu & Carey 1996"),
    Prior("individuation", "TRACKER",
          "track ~3-4 objects in parallel by spatiotemporal index",
          "Pylyshyn 1989; Kahneman, Treisman & Gibbs 1992"),
    Prior("occlusion", "TRACKER", "an occluded object persists behind the occluder",
          "Aguiar & Baillargeon 1999"),
    Prior("amodal_completion", "TRACKER",
          "a partly occluded figure moving as one is one object",
          "Kellman & Spelke 1983"),
]


# -- BIAS: `candidates -> ordering`, and REVERSIBLE BY CONSTRUCTION (§12.1) ---------------
# §12.1: *a prior that reorders search is a cut ... biases enter as ranked, reversible cuts
# or they do not enter.* So each is a key function for `3d`'s rank, never a filter.

def _simplicity(unit: Any) -> tuple:
    """Prefer the shorter hypothesis fitting the evidence. Orders; removes nothing."""
    return (len(unit),)


def _take_the_best(uses: dict[str, int]) -> Callable[[Any], tuple]:
    """Fast-and-frugal: order by the single most-used cue rather than weighting all."""
    def key(unit: Any) -> tuple:
        return (-uses.get(unit.name, 0),)
    return key


BIASES = [
    Prior("simplicity", "BIAS", "prefer the shorter hypothesis fitting the evidence",
          "Chater & Vitanyi", _simplicity),
    Prior("take_the_best", "BIAS", "take-the-best; ecological rationality",
          "Gigerenzer & Goldstein 1996", _take_the_best),
    Prior("contact_first", "BIAS", "contact-then-motion is perceived as causation",
          "Michotte 1946; Leslie & Keeble 1987"),
    Prior("essentialism", "BIAS",
          "a hidden non-obvious property causes observable behaviour and outranks appearance",
          "Gelman & Wellman 1991"),
]


# -- BUDGET: a number with provenance, in the constants block (§12.1 / §22.1) -------------
# **COGNITIVE BOUNDS ONLY.** The termination caps (`max_depth`, `budget`) are seat-side,
# behind the second firewall, and were never one of the six shapes -- the `BUDGET` collision
# recorded as the third A6i instance. Each number here is anchored to a measurement of the
# world that the agent cannot move, which is §22.1's whole distinction.

BUDGETS = [
    Prior("subitizing", "BUDGET", "exact representation of sets <= 3-4",
          "Feigenson & Carey 2003", 4),
    Prior("relational_complexity", "BUDGET", "adult ceiling ~4 related variables",
          "Halford", 4),
    Prior("focus_of_attention", "BUDGET", "4 +/- 1 focus of attention",
          "Cowan 2001", 4),
    Prior("span", "BUDGET", "7 +/- 2 span", "Miller 1956", 7),
]


def load() -> dict[str, list[Prior]]:
    """The four shapes, by home. **Populated, not entered** -- none of this touches Γ."""
    return {"CONSTRAINT": CONSTRAINTS, "TRACKER": TRACKERS,
            "BIAS": BIASES, "BUDGET": BUDGETS}


def report() -> dict:
    got = load()
    return {k: [p.name for p in v] for k, v in got.items()} | {
        "total": sum(len(v) for v in got.values()),
        "cited": sum(1 for v in got.values() for p in v if p.citation),
        "reads": "every row cites ARC_HUMAN_PRIORS; none was chosen for usefulness",
    }
