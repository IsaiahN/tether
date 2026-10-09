"""layers: the agent may not import a world. Per LAYER, never per name.

**ISAIAH, 2026-10-05, ON THE FIX THIS REPLACES:** *"this code should point at whatever world
the agent is in -- that feels like a discontinuity. My leg isn't in one room and I in
another."*

The seam was enforced by `pyproject.toml`'s ruff TID251 table, which bans `world.ACTIONS`,
`world.DELTA`, `world.RULES`, `world.TRUTH`. **Every banned name is the TOY world**, while
`gridworld.py:90` exposes an `ACTIONS` tuple that nothing banned -- in the world all of this
week's work ran in. A correctly built instrument pointed at a world nobody is working in.

**AND EXTENDING THE LIST WAS THE WRONG REPAIR, WHICH IS ISAIAH'S CORRECTION AND THE REASON
THIS FILE EXISTS.** Banning `world.ACTIONS`, then `gridworld.ACTIONS`, then `arc_world`'s
names is the same defect three times: **a rule that ENUMERATES WORLDS protects only the
worlds someone remembered**, so the next fixture, harness adapter or walkthrough-derived
world is unprotected by default.

> **SO THE RULE IS INVERTED. The REASONING side is enumerated -- it is small, slow-moving and
> ours -- and EVERYTHING ELSE IS ENVIRONMENT-SIDE BY DEFAULT. A world nobody has written yet
> is already covered, because nobody has to list it.**

**WHAT MAY CROSS: the bridge.** `world` is the Env contract and `interface` is the action
interface -- the two doors the architecture declares. The agent reaches a world THROUGH them
or not at all.

**TOP-LEVEL IMPORTS ONLY, AND THIS IS NOT AN OPTIMISATION -- IT IS THE DIFFERENCE BETWEEN A
CHECK AND A FALSE ACCUSATION.** A first draft walked the whole AST and flagged `detectors`
and `observer` importing `reverse_engineer`, which is the ANSWER KEY. That reads as a
`KEY_BOUNDARY` breach, the gravest finding available here. **It is not one:** both imports
sit under `if __name__ == "__main__"`, `observer.py:153` says so, and `lint.py` had already
verified it. A module-scope import is a dependency; a function-scope import is a tool a
script reaches for. **An alarm nobody can reproduce teaches people to ignore the alarm**, so
the scope distinction is load-bearing.
"""

from __future__ import annotations

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# THE AGENT. Perception and the library are the agent's OWN faculties and belong here: what
# it senses and what it composes with are not the world's, they are its body.
REASONING = frozenset({
    "tether", "gamma", "grammar", "routine", "condition", "instruments", "retrieval",
    "probe", "ledger", "speak", "summary", "behaviour", "priors",
    "arc_atoms", "arc_predict", "arc_percept", "sensors", "sensors_heavy",
    "composer", "inherited", "self_family", "relations", "observer", "detectors",
    "framepair", "visible",
    # the one parser its arms read through (2026-10-08): the agent reading its own switches,
    # not a world -- it imports only `os`
    "armflag",
    # M4 (2026-10-09): the library's conditions compiled into terms, and the CAUSE test over
    # frames -- the agent reading its own inheritance; they import only condition, gamma, composer
    "compile_term", "reach",
})

# THE TWO DOORS, and nothing else is one.
BRIDGE = frozenset({"world", "interface"})


def _top_level_imports(src: str) -> set[str]:
    """Module-scope imports only. See the docstring: scope is what separates a dependency
    from a tool a `__main__` block reaches for, and conflating them invents breaches."""
    out: set[str] = set()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Import):
            out.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            out.add(node.module.split(".")[0])
    return out


def crossings(root: pathlib.Path = ROOT) -> list[tuple[str, str]]:
    """Every reasoning-side module importing an environment-side one. Empty is the pass."""
    project = {p.stem for p in root.glob("*.py")}
    bad: list[tuple[str, str]] = []
    for name in sorted(REASONING & project):
        try:
            src = (root / f"{name}.py").read_text(encoding="utf-8")
        except OSError:
            continue
        for imported in sorted(_top_level_imports(src)):
            if imported in project and imported not in REASONING and imported not in BRIDGE:
                bad.append((name, imported))
    return bad


def selftest() -> dict[str, str]:
    """THE FAILURE PATH, EXERCISED -- including against a world no rule names.

    **ISAIAH'S CONDITION IS THE LAST CASE AND IT IS THE WHOLE POINT.** A check that refuses
    `gridworld` proves only that someone remembered `gridworld`. One that refuses a world
    invented inside this function, whose name appears nowhere in this file, proves the rule
    is about the LAYER. Reintroduce the defect, never disable the check.
    """
    out: dict[str, str] = {}
    project = {"tether", "world", "interface", "gridworld", "arc_world", "quuxworld"}

    def verdict(src: str) -> list[str]:
        return [i for i in sorted(_top_level_imports(src))
                if i in project and i not in REASONING and i not in BRIDGE]

    for world_name in ("gridworld", "arc_world", "quuxworld"):
        planted = f"import {world_name}\n"
        if verdict(planted) != [world_name]:
            out[f"plant:{world_name}"] = f"a reasoning-side `import {world_name}` was not refused"
    if verdict("from gridworld import ACTIONS\n") != ["gridworld"]:
        out["plant:from"] = "`from gridworld import ACTIONS` was not refused"

    # the bridge passes, or the agent cannot reach any world at all
    if verdict("import world\nimport interface\n"):
        out["bridge"] = "the Env contract or the interface was refused; the agent needs both"

    # scope: a `__main__`-only import is not a dependency
    under_main = 'if __name__ == "__main__":\n    import gridworld\n'
    if verdict(under_main):
        out["scope"] = "a `__main__`-only import was reported as a layer crossing"

    return out


def main() -> int:
    bad = selftest()
    for case, why in sorted(bad.items()):
        print(f"  layers: SELFTEST {case}: {why}")
    found = crossings()
    for mod, imported in found:
        print(f"  layers: {mod}.py imports `{imported}` -- the agent may not import a world; "
              f"reach it through `world` (the Env contract) or `interface`")
    if not bad and not found:
        print(f"  layers: ok -- {len(REASONING)} reasoning modules, 0 crossings, "
              f"4 planted refusals including a world no rule names")
    return 1 if (bad or found) else 0


if __name__ == "__main__":
    sys.exit(main())
