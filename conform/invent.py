"""invent: `_invent` EXECUTES, once per family, without raising.

THE REVIEWER, 2026-10-04: *an arm that has never executed cannot be flipped on.* Isaiah ruled
`_INVENT` ON by default -- *composition is inherent to agency* -- and the mechanism behind
that flag **raised `ValueError` on its first call**: it unpacked three fields from
`_residual_obs`' five. `_INVENT` had been default-OFF since `history()` widened, so the arm
had never run and nothing could notice. **Every earlier "`_INVENT` off" reading was also
"`_INVENT` could not run".**

SO THE TEST IS EXECUTION, NOT BEHAVIOUR. It makes no claim about whether an invented atom is
good, reused, or worth its price -- those are measurements the pre-registration owes. It
claims only that the arm completes a run on each family it will be turned on for.

**AND IT ASSERTS `_invent` WAS ACTUALLY CALLED, which is the half that stops it being
theatre.** A run that completes without ever reaching `_invent` passes a
"returns-without-error" test while proving nothing -- *a control that examines nothing cannot
demonstrate a clean state*. The call count is the denominator and a zero is a FAILURE here,
not a pass.

PER FAMILY, NEVER POOLED. A mechanism that runs on one family and dies on another is the
thing this is for, and a pooled "it works" would hide exactly that.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

sys.dont_write_bytecode = True

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAMILIES = ("click_only", "buttons", "default")
# anchor: 12 is a budget at which ALL THREE families are MEASURED to reach `_invent` --
# 2026-10-04, click_only 53 calls, buttons 25, default 91. NOT the smallest such budget:
# 11 was never tried, and writing `smallest` would have been precision I did not earn.
# The check asserts
# a non-zero call count, so a budget too small to reach the mechanism would fail loudly
# rather than pass while examining nothing. Not chosen for the clock: `default` is what
# makes this the slowest seat in the suite at ~2m13s.
CYCLES = 12

CHILD = r'''
import sys
sys.dont_write_bytecode = True
fam, cycles = sys.argv[1], int(sys.argv[2])
import gamma as G, gridworld, ledger, tether, world as _w
assert tether._INVENT, "TETHER_INVENT did not take -- this arm would run as its opposite"
real = tether.Agent._invent
calls = [0]
def spy(self, slot, licence, hist):
    calls[0] += 1
    return real(self, slot, licence, hist)
tether.Agent._invent = spy
env = _w.bind(gridworld.family(fam, 3, cycles))
gam = G.Gamma(env.atoms(), game="inv")
ag = tether.Agent(env, gam, tether.Config(max_depth=2), ledger.Ledger())
for _ in range(cycles):
    ag.step()
print(f"{calls[0]} {len(gam.invented)} {gam.alphabet}")
'''


def main() -> int:
    bad = []
    rows = []
    for fam in FAMILIES:
        env = dict(os.environ, TETHER_INVENT="1", PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, "-c", CHILD, fam, str(CYCLES)],
                           cwd=ROOT, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            last = (r.stderr.strip().splitlines() or ["?"])[-1][:160]
            bad.append(f"`_invent` DIED on `{fam}`: {last}")
            continue
        calls, made, alpha = r.stdout.strip().split()
        rows.append((fam, int(calls), int(made), int(alpha)))
        # A ZERO HERE IS A FAILURE, NOT A PASS. Without it this test is a control that
        # examines nothing: the run completes, `_invent` is never reached, and the green
        # says only that the rest of the loop works.
        if int(calls) == 0:
            bad.append(f"`_invent` was never CALLED on `{fam}` in {CYCLES} cycles -- this "
                       f"check examined nothing there, so it cannot report the arm works.")
    if bad:
        for b in bad:
            print(f"  invent: {b}")
        return 1
    for fam, calls, made, alpha in rows:
        print(f"  invent {fam:<11s} calls {calls:>4d}  invented {made:>4d}  alphabet {alpha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
