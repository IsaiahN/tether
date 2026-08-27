"""2a's fixture, and the consumer that exercises `arc_world`.

WHAT IT TESTS: the adapter's eight members, the loop running end to end over the REAL frame
types, and that values cross the boundary with the right shapes.

WHAT IT CANNOT TEST: whether perception works on a real board, whether slots are stable, or
anything about ARC's actual structure. **A synthetic solve proves wiring and never
capability** -- Figure 11, and this is where its SECOND failure mode bites hardest, because
the same hand authored both sides. What was not reproduced is invisible until the goal
fails; what was unintentionally introduced is invisible until it acts.

The game's rule is trivial and mine. No real task, no real board, nothing from a game -- and
a rule with structure would invite reading a result off a fixture that cannot carry one.
"""
from __future__ import annotations

import collections
import math
import sys

import numpy as np
from arcengine import FrameDataRaw, GameState

import arc_lens
import arc_percept
import gamma
import gate
import ledger
import tether
from arc_world import ArcWorld
from gamma import Atom
from world import bind

sys.dont_write_bytecode = True

# anchor: a 4x4 board over 7 colours is the smallest that exercises a 2-D stack and a
# non-trivial palette at once. Nothing is read off the size; it is a fixture dimension.
SIDE, PALETTE = 4, 7


class FakeWrapper:
    """The wrapper surface the adapter consumes: `reset` and `step` returning FrameDataRaw.

    Real frame types, synthetic contents -- so the type contract is genuinely exercised
    while the game is not a game.
    """

    def __init__(self) -> None:
        self.n = 0

    def _frame(self) -> FrameDataRaw:
        # a trivial GATE, so §16.8's sensors 1 and 2 have something to see: ACTION4 is
        # available only after five steps. The condition is mine and carries no meaning --
        # what is being tested is that a change is DETECTED and ATTRIBUTED, not what gates.
        acts = [0, 1, 2, 3] + ([4] if self.n >= 5 else [])
        f = FrameDataRaw(game_id="fixture", state=GameState.NOT_FINISHED,
                         levels_completed=0, win_levels=3,
                         available_actions=acts)
        board = np.zeros((SIDE, SIDE), dtype=int)
        board[0][0] = self.n % PALETTE
        f.frame = [board]
        return f

    def reset(self) -> FrameDataRaw:
        self.n = 0
        return self._frame()

    def step(self, _action, _data=None, _reasoning=None) -> FrameDataRaw:
        self.n += 1
        return self._frame()


def _atoms() -> list[Atom]:
    """THE FIXTURE DECLARES ITS OWN ATOMS, because reaching `world._atoms` is banned by
    TID251 and rightly: a private name across a module boundary is another domain's
    business. ARC's real atom set is grid transforms and arrives at 3d; these three are
    a plumbing set and nothing is read off them."""
    return [Atom("idn", lambda v, _c: v, "val", "val"),
            Atom("inc", lambda v, _c: v + 1, "val", "val"),
            Atom("act", lambda v, c: v + len(str(c.action)), "val", "val")]


def cells(board) -> dict[str, int]:
    """One slot per cell. 2b replaces this: it is the IDENTITY decomposition, which assumes
    no structure -- and assuming none is the only honest placeholder before perception."""
    return {f"c{r}{c}": int(board[r][c]) % PALETTE
            for r in range(SIDE) for c in range(SIDE)}


def _fidelity(state, palette):
    """1 - R_T/ceiling, where the ceiling is a whole restatement of every slot. The units
    are the caller's, which is why `arc_lens` takes this rather than computing it: the lens
    knows about shape and the loop knows about bits."""
    ceiling = len(state) * math.log2(palette)
    alpha = dict.fromkeys(state, palette)
    return lambda t_a: 1.0 - tether.round_trip_gap(t_a, state, alpha) / ceiling


def main() -> None:
    atoms = _atoms()
    probe_board = FakeWrapper().reset().frame[-1]
    names = sorted(cells(probe_board))

    # BOTH OUTCOMES, because `None` is the one that matters most. The uniform board IS
    # representable at stride 2; the speckled one is not, and one differing cell per block
    # is enough -- which is the point, since that cell is exactly what a coarse view loses.
    flat = dict.fromkeys(names, 3)
    committed = arc_lens.lens(names, SIDE, _fidelity(flat, PALETTE))
    print(f"  lens, uniform board : {[n for n, _ in committed] if committed else None}"
          "   (coarse-representable -> commits)")

    speckled = {n: (3 if n in ("c00", "c02", "c20", "c22") else 5) for n in names}
    offered = arc_lens.lens(names, SIDE, _fidelity(speckled, PALETTE))
    print(f"  lens, speckled board: {[n for n, _ in offered] if offered else None}"
          "   (NOT a rendering of anything coarser -> None)")

    # 2b: segmented objects as slots, replacing the identity decomposition. The lens is
    # computed over the CELL naming because a stride view is a fact about the board's
    # geometry, not about the objects found on it.
    real = arc_lens.lens(names, SIDE, _fidelity(cells(probe_board), PALETTE))
    seg = arc_percept.Objects()
    env = ArcWorld(FakeWrapper(), seg, atoms, palette=PALETTE, views=real)

    print("  the eight fill      :", end=" ")
    bind(env)
    print(f"{len(env.slots())} slots, {len(env.atoms())} atoms, transform={env.transform()}")
    acts = env.actions()
    print(f"  actions advertised  : {acts}   RESET withheld: {'RESET' not in acts}")
    print(f"  board type          : {type(env.board()).__name__}   alphabet: {env.alphabet()}")
    print(f"  objective           : {env.objective()}")

    led = ledger.Ledger()
    agent = tether.Agent(env, gamma.Gamma(atoms), tether.Config(), led)
    agent.run(12)
    c = collections.Counter(r["event"] for r in led.rows())
    verdict = gate.check(led.rows())
    print(f"  loop                : {agent.cycle} cycles, {len(led.rows())} rows, {dict(c)}")
    print(f"  gate                : {verdict['verdict']}")
    br = [r for r in led.rows() if r["detail"].get("channel") == "bracket"]
    pres = [r for r in led.rows() if r["event"] == "present"]
    print(f"  perception          : {len(env.slots())} object slots, "
          f"{len(seg.tracked)} tracked objects")
    print(f"  slot-set changes    : {len(pres)} rows"
          + (f", came={pres[0]['detail']['came'][:3]}" if pres else ""))
    adv = [r for r in led.rows() if r["event"] == "advertised"]
    print(f"  action-set delta    : {len(adv)} rows"
          + (f", came={adv[0]['detail']['came']} after={adv[0]['detail']['after']}" if adv else ""))
    print(f"  precondition edges  : {agent.pre.report()['came_after']}")
    print(f"  bracket channel     : {len(br)} rows, "
          f"cause={br[0]['detail']['cause'] if br else None}, "
          f"R_T={br[0]['detail']['mass'] if br else None}, "
          f"view={br[0]['detail'].get('view') if br else None}")

    assert "RESET" not in acts, "RESET reached the loop: the farming path is open"
    assert verdict["verdict"] == "pass", verdict
    print("  A SYNTHETIC SOLVE PROVES WIRING AND NEVER CAPABILITY -- this fixture authored")
    print("  both sides, so it says nothing about perception, slot stability or ARC.")


if __name__ == "__main__":
    main()
