"""landed: the trace's LANDED-ON field says what the press actually hit, every step.

**THIS SEAT EXISTS BECAUSE THE FIRST VERSION OF THE GUARD READ THE WRONG QUANTITY AND
MEASURED CLEAN FOR FIVE HOURS.** `a561fb2` carried `_intent_now.subject` -- what the agent
AIMED AT -- in a field consumed by a guard named *I acted on this object*. On `click_only`
those coincide by construction, so every number taken there was consistent with either
reading and nothing could have shown the difference. On the WIRED world they diverge: the
agent aims at `o0.colour` and the interface presses `o1` to reach it, and the guard read
TRUE on 48 of 60 steps where `o0` was never touched.

**SO THE ASSERTION IS AGAINST THE WORLD AND NOT AGAINST THE AGENT'S OWN RECORD OF ITSELF.**
It reads which object was standing at the pressed coordinate straight off `gw.state`, and
compares that to the fifth trace field. **A check that asked the agent what it pressed would
have passed on the broken build** -- the broken build was perfectly self-consistent.

**THE FAILURE PATH IS EXERCISED, AND IT CORRECTED THIS DOCSTRING.** Reintroducing the
`a561fb2` defect -- the field carrying the intent's subject -- the seat reads 15/25 and
FIRES. This paragraph first claimed `click_only` COULD NOT fail the test, on the reasoning
that aim and landing coincide there. **It fires on `click_only` too, and the reason is
clause 3:** the uninformed draw lands on a round-robin object while the intent still names
a subject, so aim and landing come apart on EVERY fixture, not only the wired one. The
claim was written from the fixture's design and refuted by running it.

**A GUARD WHOSE FAILURE PATH IS NEVER EXERCISED IS INDISTINGUISHABLE FROM ONE THAT CANNOT
FAIL**, which is why that was run before this seat was registered rather than after.
"""
from __future__ import annotations

import pathlib
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import gamma as G  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

# anchor: NOT A SAMPLE SIZE. This is a PER-STEP IDENTITY check -- every step must agree, so
# ONE divergent step fails it and the seat's power does not grow with length. 25 is simply
# the shortest run that reliably contains presses on every fixture; the reintroduced
# `a561fb2` defect shows as 10 mismatches in 25, so there is no threshold to tune and
# nothing here was chosen to make a number come out.
CYCLES = 25


def _owner_at(state: dict, x: int, y: int) -> str | None:
    """Which object is standing at this cell, read off the WORLD."""
    for obj in sorted({k.rsplit(".", 1)[0] for k in state if k.endswith(".row")}):
        if (state.get(f"{obj}.col"), state.get(f"{obj}.row")) == (x, y):
            return obj
    return None


def check(arm: str, seed: int) -> tuple[int, int]:
    gw = gridworld.family(arm, seed, CYCLES)
    env = world.bind(gw)
    ag = tether.Agent(env, G.Gamma(env.atoms()), tether.Config(max_depth=2), ledger.Ledger())
    truth: list[str | None] = []
    real = gw.step

    def step(action, x=None, y=None):
        truth.append(None if x is None or y is None else _owner_at(dict(gw.state), x, y))
        real(action, x, y)

    gw.step = step
    for _ in range(CYCLES):
        ag.step()
    traced = [None if r[4] is None else r[4].rsplit(".", 1)[0] for r in ag.trace]
    n = min(len(truth), len(traced))
    return sum(1 for i in range(n) if truth[i] == traced[i]), n


def main() -> int:
    bad = []
    for arm in ("buttons", "click_only"):
        for seed in (0, 1):
            agree, n = check(arm, seed)
            flag = "" if agree == n else "  <-- MISMATCH"
            print(f"  {arm:11s} seed {seed}: trace agrees with the world on {agree}/{n}{flag}")
            if agree != n:
                bad.append((arm, seed, agree, n))
    if bad:
        print(f"\n  the landed-on field does not say what was pressed: {bad}")
        return 1
    print("\n  the trace says what the press HIT, not what the agent WANTED -- every step")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
