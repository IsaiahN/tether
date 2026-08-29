"""§18.3's independence requirement, MEASURED. SEAT-SIDE — the agent does not import this.

§18.3 states the requirement and attaches no measurement: *"non-simulable" means the members do
not share a failure mode.* **That is a panel property, and the panel law forbids asserting one
from the shape of the generator** — four members described as translation, growth, scalar and
toggle *look* independent, and the DS ladder looked like easing on ten seeds.

**THE INSTRUMENT IS THE PANEL SCREEN**, which §18.3's own correction names: *run each member
across the twenty-five and check they fail on **different** games.*

**RUN AS APPARATUS — NO AGENT, NO Gamma.** The seat drives the actions, so the loop's behaviour
is not a term in a measurement about detectors. Same reason `controlled()` has no agent in it.

**FAILURE IS `has_self()` FALSE — BINARY, AND NOTHING IS CUT.** A residual would need a
threshold; *has a self or does not* is the members' own existential and needs no number.

**AND THE VACUITY CHECK IS STATED BEFORE THE READING, because a null here has two meanings.**
For this panel to be able to show independence at all, **each PAIR must disagree somewhere** —
one member finding a self where the other does not. A pair that never disagrees is
**indistinguishable on this panel**, which is a fact about the panel and not evidence that the
two are one detector. Reported per pair rather than as a single verdict.
"""
from __future__ import annotations

import logging
import sys

from arcengine import GameAction

import arc_self

sys.dont_write_bytecode = True

# The 25 public identifiers. A game IDENTIFIER is a public name; nothing about any game's
# mechanics is here.
PANEL = ("ar25", "bp35", "cd82", "cn04", "dc22", "ft09", "g50t", "ka59", "lf52", "lp85",
         "ls20", "m0r0", "r11l", "re86", "s5i5", "sb26", "sc25", "sk48", "sp80", "su15",
         "tn36", "tr87", "tu93", "vc33", "wa30")

# EXEMPTIONS AS DATA, NOT LOGIC -- a table can be pinned; a predicate widens quietly.
# These six advertise a positioned click and the adapter drops it, because the loop cannot
# supply a position. So THE ADAPTER SURFACES NO ACTION and every member fails for a reason
# external to the members -- a shared failure mode from the HARNESS, which would read as
# correlation. NOT a claim that these games have no actions: what they contain is
# unestablished, and this exclusion expires the moment positioned actions are supplied.
NO_SURFACED_ACTION = ("ft09", "lp85", "r11l", "s5i5", "tn36", "vc33")


def _run(arc, game: str, cycles: int) -> dict:
    w = arc.make(game)
    if w is None:
        return {"error": "did not resolve"}
    fr = w.reset()
    acts = [GameAction.from_id(a).name for a in (fr.available_actions or ())
            if GameAction.from_id(a).is_simple() and GameAction.from_id(a) is not GameAction.RESET]
    if not acts or not fr.frame:
        return {"surfaced_actions": len(acts), "skipped": "no surfaced action"}
    fam = arc_self.family()
    board = fr.frame[-1]
    for i in range(cycles):
        nxt = w.step(GameAction[acts[i % len(acts)]])
        if nxt is None or not nxt.frame:
            break
        fam.observe(board, acts[i % len(acts)], nxt.frame[-1])
        board = nxt.frame[-1]
    r = fam.report()
    return {"surfaced_actions": len(acts), "has_self": r["has_self"],
            "residuals": r["residuals"], "selected": r["selected"],
            "unmodeled": r["unmodeled"]}


def screen(cycles: int = 25, games: tuple = ()) -> dict:
    """Each member across the panel. **Failure sets, then pairwise disagreement.**"""
    logging.disable(logging.INFO)
    from arc_agi import Arcade
    from arc_agi.base import OperationMode

    arc = Arcade(operation_mode=OperationMode.NORMAL)
    panel = games or tuple(g for g in PANEL if g not in NO_SURFACED_ACTION)
    per: dict[str, dict] = {}
    for g in panel:
        per[g] = _run(arc, g, cycles)

    played = [g for g, v in per.items() if "has_self" in v]
    names = [m.name for m in arc_self.family().members]
    found = {n: sorted(g for g in played if n in per[g]["has_self"]) for n in names}
    failed = {n: sorted(g for g in played if n not in per[g]["has_self"]) for n in names}

    pairs = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            only_a = sorted(set(found[a]) - set(found[b]))
            only_b = sorted(set(found[b]) - set(found[a]))
            pairs[f"{a}|{b}"] = {
                "disagree_on": len(only_a) + len(only_b),
                "only_first": only_a, "only_second": only_b,
                # THE VACUITY READING, PER PAIR. Zero here is a fact about the panel: these
                # two were never separated, so this panel cannot say whether they are one
                # detector. It is NOT evidence that they are.
                "separable_here": bool(only_a or only_b),
            }
    return {
        "cycles": cycles, "panel": list(panel), "played": played,
        "excluded": list(NO_SURFACED_ACTION),
        "excluded_reason": ("the adapter surfaces no action -- they advertise a positioned "
                            "click and the adapter drops it. Every member fails there because "
                            "nothing acts, which is a shared failure mode from the HARNESS. "
                            "NOT a claim that these games have no actions"),
        "found_self_on": found, "failed_on": failed,
        "pairs": pairs,
        "all_pairs_separable": all(p["separable_here"] for p in pairs.values()),
        "per_game": per,
        "reads": ("failure is has_self() False -- binary, no threshold. A pair that never "
                  "disagrees is INDISTINGUISHABLE ON THIS PANEL, which is a fact about the "
                  "panel rather than evidence the two are one detector"),
    }


if __name__ == "__main__":
    import json
    r = screen()
    print(json.dumps({k: v for k, v in r.items() if k != "per_game"}, indent=1)[:4000])
