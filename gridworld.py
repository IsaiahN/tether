"""gridworld: an ARC-SHAPED HABITAT. Generated boards, objects, reachable goals. No ARC game.

**ISAIAH, 2026-09-25, and it is the ONLY exception to the board stop:** *"Why can't we make an
ARC-shaped world with randomly generated objects and goals to be reachable? Nothing complex but
good enough to fully test its capabilities."* It replaces both the toy-world patch and the
minimal grid fixture that was queued at 6.5.

    IT IS A HABITAT, NOT A BENCHMARK. What it is for is WHETHER THE MECHANISMS FIRE.
    It is not for a performance number, and a score taken here would be a score of the
    generator.

**WHY IT EXISTS: THREE FINDINGS ARE DEAD FOR ONE REASON AND IT IS THE WORLD, NOT THE CODE.**
`F356` the spectator test reads empty · `F359` the residual precondition refuses nothing because
`robs` is never empty · `F360` the consumer has one kind in contention and no contest. **The toy
world is seven scalar slots under arithmetic where every action moves everything**, so none of
the three can be exhibited there. They are habitat-shaped and this is the habitat.

**THE VOCABULARY IS DELIBERATELY UNCHANGED.** `world._atoms()` is reused verbatim, so the ONLY
variable that moves between the toy world and this one is the HABITAT. A mechanism that fires
here and not there is then a fact about contact rather than about the atom set. Grid-native atoms
are a follow-on and would confound exactly this comparison if taken first.

---

**WHAT THE GENERATOR DOES NOT CONTROL — the reviewer asked for this explicitly, and it is the
guard against the failure I nearly committed with the toy-world patch: *a repair validated on its
own case*, building the habitat that makes your own finding pass.**

    it does NOT read the agent's atom set, bindings, Gamma, or any book
    it does NOT choose goals the agent can express -- a target is a random reachable
      cell, drawn before any agent exists
    it does NOT vary with the finding under test. One generator, one seed -> one board,
      and the seed is the caller's
    it does NOT place the mover at its target, and it does NOT guarantee a SHORT path --
      only that a path EXISTS, because it was walked to build the target

**What it DOES control is the thing that makes the three findings exhibitable at all: SOME SLOTS
DO NOT MOVE UNDER SOME ACTIONS.** That is not tuning -- it is the defining property of a grid
with more than one object, and its absence is what made the toy world unable to show them.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from typing import Any

import observer
import world as _toy
from gamma import Atom

sys.dont_write_bytecode = True

# anchor: DERIVED FROM THE BARGAIN'S OWN PRICING, NOT CHOSEN -- 2026-09-25.
#
# `pays` is `cost + left < base` with `left = max(0, unsat - reach) * log2(n)` and
# `base = unsat * log2(n)`, so `unsat` cancels and the whole condition is
#
#     PAYS  <=>  cost < min(reach, unsat) * log2(n)
#
# Evaluated at n=4 actions: the cheapest routine `term_bits` can price is 4.6439 bits, and
# the only shape whose reach exceeds 1 without a length penalty is `Until(g, Act, budget)`
# at 6.9658. So a plan needs `min(reach, unsat) >= 4`, i.e. **unsat >= 4**.
#
# `unsat = R_goal * scope`. At scope 4 that forces R_goal = 1.0 EXACTLY -- and 1.0 is the
# maximum, so a series that PASSES gate 1 (which requires a real decrease) is necessarily
# below it. **AT FOUR, A QUALIFYING OBJECTIVE CAN NEVER AFFORD A PLAN. Provably, not rarely.**
#
# At scope 5, R_goal 0.8 gives unsat 4 and 0.8 is a legitimate decrease from 1.0. **SCOPE 5
# IS THE SMALLEST THAT ADMITS A PLAN AT ALL, AND SCOPE IS N-1.** Hence six.
#
# The earlier reasoning for five still holds and is subsumed: two steps cannot separate
# "shrinking" from "arrived", four can. This is the same knob turned for a second, stronger
# reason -- and the value came from the inequality rather than from wanting a mint.
N_OBJECTS = 6

# anchor: the objects need room to be non-adjacent and a walk needs somewhere to go; 5x5 is
# the smallest board where both hold, and small enough to sweep exhaustively.
# **AND THE SECOND CLAUSE IS WEAKER AT FIVE OBJECTS THAN IT WAS AT THREE, SAID HERE RATHER
# THAN LEFT TO BE FOUND: five of twenty-five cells are occupied.** The board is still
# walkable and the reachability seat checks it per seed, but the sparsity this anchor
# asserts is now a CHECKED property rather than an obvious one.
GRID = 5
ACTIONS = ("up", "down", "left", "right")
GOAL_SLOT = _toy.GOAL_SLOT                      # one name, and it is the toy world's

_DELTA = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


@dataclass
class GridWorld:
    """One generated board. `seed` selects it; the same seed is the same board, always.

    THREE OBJECT ROLES, and the middle one is why this is not just a bigger toy world:

        o0  THE MOVER      every action moves it (bounded by the wall and the board edge)
        o1  THE PUSHED     moves ONLY when o0 is behind it in the action's direction --
                           so it is action-bearing on SOME actions and a spectator on others
        o2  THE WALL       never moves under any action. A pure spectator, by construction

    Colours never change. They are there because an ARC board has them and because a slot
    that no action can reach is exactly what `F356`'s spectator test needs to find.
    """

    seed: int = 0
    state: dict[str, int] = field(default_factory=dict)
    target: tuple[int, int] = (0, 0)
    # THE HABITAT DOES NOT OWN THE VOCABULARY, and `lint`'s TID251 is what said so: reaching
    # into another module's private atom set is the coupling that makes "one variable moves"
    # unverifiable. Passed in, or taken from the toy world's PUBLIC accessor.
    atom_set: list[Atom] | None = None
    # **FIXTURE B -- NO AVATAR, ONLY CLICKING WORKS. Isaiah's second fixture, and
    # `docs/ACTION_INTERFACE_PLAN.md` 19e made it a PREREQUISITE rather than an option**: it is
    # the only world that can exercise `TOUCH`'s positioned route, which nothing has run. This
    # world advertises ONE action and it takes a coordinate, so there is nothing to walk with
    # and no direction to want -- *"if no avatar what is the cause and effect by clicking on
    # things"*.
    #
    # **A FLAG DEFAULTING TO FALSE, so every existing reading of this world is byte-identical.**
    click_only: bool = False
    # **FIXTURE A -- THE ACTIONS CHANGE UNDER THE AGENT. Isaiah's first fixture, and the half of
    # System 0's job B that NOTHING has ever exercised**: *"lets the interface know how actions
    # work AND IF THEY CHANGE."* After `remap_after` steps `up`/`down` and `left`/`right` swap
    # -- the BOARD still behaves lawfully, the MAPPING is what moved.
    #
    # **THE BUTTONS KEEP THEIR NAMES ON PURPOSE.** A board that renamed them would be caught by
    # the advertised-set check that already exists; one that keeps every name and changes what
    # two of them DO is the case `_runnable`'s string comparison passed and `audit`'s `changed`
    # set was built for. **That detector has never had a true positive.**
    #
    # `None` by default, so every existing reading of this world is byte-identical.
    remap_after: int | None = None

    def __post_init__(self) -> None:
        rng = random.Random(self.seed)
        cells = rng.sample([(r, c) for r in range(GRID) for c in range(GRID)], N_OBJECTS)
        (r0, c0), (r1, c1), (r2, c2) = cells[:3]
        # **o1 IS PLACED WITHIN REACH OF o0, AND THE REASON IS ARC-FIDELITY, NOT A FINDING.**
        # Measured on the first version: ONE slot of ten carried any residual, the integral was
        # 27.86 against the toy world's 128.26, and NOTHING bound -- a slot with no surprise has
        # nothing to buy, so `cost + left < base` cannot hold at `base = 0`.
        #
        # **A BOARD WHERE ONE OBJECT MOVES THROUGH EMPTY SPACE IS A MAZE, NOT AN ARC TASK.** ARC
        # boards have objects that INTERACT. That is the justification and it is independent of
        # any finding -- which matters, because the reviewer's standing warning is that a
        # generated world can be generated until a finding passes.
        near = [(r0 + dr, c0 + dc) for dr in (-2, -1, 1, 2) for dc in (-2, -1, 0, 1, 2)
                if 0 <= r0 + dr < GRID and 0 <= c0 + dc < GRID and (r0 + dr, c0 + dc) != (r2, c2)]
        if near:
            r1, c1 = rng.choice(near)
        self.state = {
            "o0.row": r0, "o0.col": c0, "o0.colour": rng.randrange(4), "o0.shape": 0,
            "o1.row": r1, "o1.col": c1, "o1.colour": rng.randrange(4), "o1.shape": 1,
            "o2.row": r2, "o2.col": c2, "o2.colour": rng.randrange(4), "o2.shape": 2,
        }
        # **THE SCOPE HAS TO BE BIGGER THAN TWO, AND IT IS ARITHMETIC RATHER THAN PREFERENCE.**
        # `R_goal` is the FRACTION OF A SCOPE THAT FAILS. With three objects a peer group is
        # two, so the quantity can only be 0.0, 0.5 or 1.0 -- and the only available real
        # decrease is 0.5 -> 0.0, which IS satisfied.
        #
        # **SO *CONFIDENTLY SHRINKING* AND *ALREADY SATISFIED* WERE THE SAME EVENT**, gate 1
        # passed at the exact moment the next gate became true, and COMPOSE could not fire
        # while both gates were correct. Measured on board 11: `o0.row` ran
        # [0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0] and qualified only by arriving.
        #
        # With five objects a peer group is four and `R_goal` takes quarters, so an objective
        # can be OBSERVABLY SHRINKING WHILE STILL UNSATISFIED -- which is the state a routine
        # exists to act on. **ARC boards carry many objects; three was the fidelity gap.**
        for i in range(3, N_OBJECTS):
            r, c = cells[i]
            self.state[f"o{i}.row"] = r
            self.state[f"o{i}.col"] = c
            self.state[f"o{i}.colour"] = rng.randrange(4)
            self.state[f"o{i}.shape"] = i
        # **THE THREE, PLACED WHERE ISAIAH PUT THEM -- 2026-09-25.** He ruled `Proximity`,
        # `Obstacle` and `Surface` ATTRIBUTE DATA rather than atoms, and my flagging them as my
        # three least-confident entries was the tell: *the doubt was correctly placed and pointed
        # at the wrong shelf.* They are PERCEIVED here rather than composed.
        #
        # `obstacle` and `surface` are fixed per object and `proximity` is not -- it is
        # RECOMPUTED every frame in `observe`, so it is the first attribute here that any action
        # can move. Constants would have added three more spectators and no signal.
        self.state["o0.obstacle"] = 0
        self.state["o1.obstacle"] = 0
        self.state["o2.obstacle"] = 1          # the wall, and the only thing that blocks
        # SURFACE IS AN OPAQUE ID AND THAT IS THE WHOLE POINT. Isaiah: *a HASH DESCRIPTION --
        # texture-like -- which we can only DIFFERENTIATE AND GROUP, never preprogram.* So it
        # carries no order and no meaning; `same`/`other` can compare two of them and nothing
        # can read one. Distinct from `.shape`, which keys contact.
        for i in range(N_OBJECTS):
            self.state[f"o{i}.surface"] = rng.randrange(3)
        # REACHABLE BY CONSTRUCTION, not by assertion. The target is where the mover ends up
        # after a random legal walk from its own start, so a path provably exists and nothing
        # had to be searched to know it. A generator that PICKED a target would have to prove
        # reachability afterwards, and that proof is exactly the thing that tends to be skipped.
        #
        # AND THE WALK IS REJECTED IF IT LANDS BACK HOME. Measured on the first 60 boards:
        # **10 of 60 STARTED ALREADY SOLVED**, because a random walk returns to its origin
        # often on a 5x5. A board whose goal is met at step 0 exercises nothing and would
        # have quietly inflated any later "the goal was reached" reading.
        r, c = r0, c0
        for _ in range(20):
            r, c = r0, c0
            for _ in range(rng.randrange(2, 8)):
                dr, dc = _DELTA[rng.choice(ACTIONS)]
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID and 0 <= nc < GRID and (nr, nc) != (r2, c2):
                    r, c = nr, nc
            if (r, c) != (r0, c0):
                break
        self.target = (r, c)
        # THE MUTATION OBSERVER over this habitat -- the only world inside the board stop
        # that can exercise it, because it is the only one with a board that is not a game.
        self._obs = observer.Live()
        self._cue: dict | None = None
        # FIXTURE A's clock. Counted here rather than read from the agent, because the trigger
        # is a property of the BOARD -- an agent that could see the counter could anticipate the
        # remap, which is the one thing this fixture must not let it do.
        self._steps: int = 0

    # -- the eight -------------------------------------------------------------------

    def substrate(self) -> str:
        return f"objects on a {GRID}x{GRID} grid; each holds row, col and colour"

    def environment(self) -> str:
        return "a board with a wall; the shaping medium is position under bounded movement"

    def actors(self) -> str:
        return f"the actions {ACTIONS}, which move ONE object and leave the rest untouched"

    def currency(self) -> str:
        return "prediction error in bits, per slot"

    def ground(self) -> str:
        return "exact match on the next state. Mechanical, instant, and it does not negotiate"

    def slots(self) -> list[str]:
        return sorted([*self.state, GOAL_SLOT] + [f"o{i}.proximity" for i in range(N_OBJECTS)])

    def atoms(self) -> list[Atom]:
        """THE TOY WORLD'S ATOMS, VERBATIM. See the module docstring: one variable moves."""
        return self.atom_set if self.atom_set is not None else _toy.Transitions().atoms()

    def actions(self) -> tuple[str, ...]:
        # ONE POSITIONED ACTION AND NOTHING ELSE. The agent cannot draw its way to a target
        # here: an unaimed click lands where nothing is, so contact requires the intent.
        return ("ACTION6",) if self.click_only else ACTIONS

    def alphabet(self) -> int | dict[str, int]:
        """PER SLOT. Positions range over the grid, colours over four, shapes over three, the
        goal over 0..1 -- four different sizes, so one number would charge a colour the grid's
        code."""
        a: dict[str, int] = {}
        for k in self.state:
            a[k] = (4 if k.endswith(".colour") else 3 if k.endswith(".shape")
                    else 3 if k.endswith(".surface") else 2 if k.endswith(".obstacle") else GRID)
        a[GOAL_SLOT] = 2
        # PROXIMITY IS A MANHATTAN DISTANCE ON A WRAPPED GRID, so its range is the board's own
        # diameter rather than its width -- stated because charging it GRID would be wrong in
        # the direction that makes its residual look smaller than it is.
        for i in range(N_OBJECTS):
            a[f"o{i}.proximity"] = 2 * GRID
        return a

    def slot_owner(self) -> dict[str, str]:
        """WHICH OBJECT EACH SLOT BELONGS TO. `o1.row` -> `o1`.

        **THE LOOP MAY NOT DERIVE THIS FROM THE NAME** -- `_slot_owners`' own docstring says
        *absent is a reading*, and a world that declares no owners gets `{}` rather than having
        one guessed from a dotted string. So the dot is a convention HERE and never a parser
        there.

        `@goal.completed` is deliberately absent: it is derived from all three objects and
        belongs to none of them.
        """
        return {k: k.split(".")[0] for k in self.slots() if k.startswith("o")}

    def peers(self) -> dict[str, tuple[str, ...]]:
        """`{slot: the SAME attribute on every OTHER object}` -- `o1.row` -> `o0.row`, `o2.row`.

        **THE LOOP MAY NOT DERIVE THIS.** It would have to split the slot name, which is reading
        domain structure -- the same reason `slot_owner` is declared here rather than inferred
        from a dot.

        **AND THIS METHOD IS THE ROOT OF THE DEAD BLOCK, TRACED 2026-09-25.** `_group` reads
        `env.peers()`; with no peers the group is EMPTY; `goal_residual` is *the fraction of a
        SCOPE that fails* and declines `empty-group`; so `_res` -- the discrepancy series --
        never grows; so `_goal_choice` has nothing to select over and returns `None` on every
        call; so `_mint_routine`'s gate 1 refuses; so `enumerate_routines` is never reached and
        **COMPOSE and RUN read dead.**

        Measured before this existed: `goal_residual` declined on all 22 slots -- `unbound` 19,
        `empty-group` 3 -- and the three were EXACTLY the slots holding a want. **The want
        reached the scope question and the scope was empty.**

        Only `arc_world` had ever published it, which is under the board stop -- the same shape
        as `contacts`, found the same way, one layer further in.
        """
        by_attr: dict[str, list[str]] = {}
        for slot in self.slots():
            if "." in slot and slot.startswith("o"):
                by_attr.setdefault(slot.rsplit(".", 1)[1], []).append(slot)
        return {s: tuple(x for x in group if x != s)
                for group in by_attr.values() for s in group}

    def contacts(self) -> dict[str, list[str]]:
        """WHICH OBJECTS TOUCH, THIS FRAME -- the owner-adjacency view of `contact_points`.

        **AND THIS IS THE METHOD THAT WAS MISSING, WHICH IS WHY A BUILT MECHANISM HAS NEVER
        RUN ON A WORLD WE MAY LEGALLY USE.** `_bindings` ranks operand candidates CONTACT FIRST
        -- §16.5's *you do not invent the list, you read it off the world* -- by calling
        `env.contacts()`, and **only `arc_world` has ever published it**, which is under the
        board stop. On the toy world and on this one before now it read `None` and the ranking
        fell back to variance.

        **`contact_points` WAS NOT ENOUGH AND I ASSUMED IT WAS.** `_contact_keys` reads
        `contact_points`; `_bindings` reads `contacts`. **Two names for contact, two consumers,
        and publishing one lit System 0's intake while leaving the operand ranking dark** --
        which I would not have found by reading either site, because each is correct alone.

        Ordering, never exclusion: §12.1 admits a bias only as a ranked, reversible cut, and a
        filter here would make contact decide REACHABILITY rather than order.
        """
        adj: dict[str, list[str]] = {}
        for a, b, _kind in self.contact_points():
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
        return adj

    def contact_points(self) -> list[tuple[str, str, str]]:
        """**WHAT IS TOUCHING WHAT. The architecture already consumes this and NO WORLD HAS EVER
        PUBLISHED IT** -- `_contact_keys` reads `env.contact_points` and returns `{}` when the
        method is absent, which is the case in the toy world and was the case here.

        **SO SYSTEM 0's CONTACT INTAKE HAS BEEN DEAD IN EVERY WORLD THE AGENT HAS EVER RUN**,
        independently of `Config.system0` being off -- two separate reasons for one silence, and
        the flag is the one that gets noticed.

        A grid is where contact actually exists, so this is the natural place to supply it.
        `orthogonal` and `diagonal` are distinct KINDS because they afford different things, and
        `_contact_keys` keys on `(kind, sorted shape ids)` -- vocabulary permanent, instances
        transient, which is its own rule and not mine.
        """
        out: list[tuple[str, str, str]] = []
        objs = tuple(f"o{i}" for i in range(N_OBJECTS))
        for i, a in enumerate(objs):
            for b in objs[i + 1:]:
                dr = abs(self.state[a + ".row"] - self.state[b + ".row"])
                dc = abs(self.state[a + ".col"] - self.state[b + ".col"])
                if dr + dc == 1:
                    out.append((a, b, "orthogonal"))
                elif dr == 1 and dc == 1:
                    out.append((a, b, "diagonal"))
        return out

    def slot_types(self) -> dict[str, str]:
        """EXTENT THROUGHOUT, AND IT IS A DELIBERATE UNDER-DECLARATION -- stated so no reader
        mistakes it for an oversight. `POSITION` and `COLOUR` are the honest types, and the
        reused atom set consumes `EXTENT`, so declaring them would type-starve every candidate
        and the world would read dead for a reason that has nothing to do with the habitat.
        Richer typing lands with grid-native atoms, together, or neither."""
        return dict.fromkeys(self.slots(), "EXTENT")

    def transform(self) -> Any:
        """No coarse view is defined here, so the bracket channel is inert. Stated, not omitted."""
        return None

    # -- running ---------------------------------------------------------------------

    def _blocked(self, r: int, c: int) -> bool:
        """Only the WALL blocks. Edges wrap -- see `_wrap`."""
        return (r % GRID, c % GRID) == (self.state["o2.row"], self.state["o2.col"])

    @staticmethod
    def _wrap(r: int, c: int) -> tuple[int, int]:
        """**POSITIONS WRAP, AND REAL ARC GRIDS DO NOT. Stated as a limit, not hidden.**

        The first version CLAMPED at the edges. **CLAMPING IS NOT MODULAR ARITHMETIC**, so no
        chain of `inc`/`dec` can express it; a wrapped step IS `inc`/`dec` mod the slot's
        alphabet, exactly.

        **AND I FIRST WROTE THIS UP ON A FALSE PREMISE -- that the atoms bake in `world.M = 7`
        and therefore could not speak about a 5-wide grid at all.** They do not: `_value_of`
        normalises every prediction `% self.alphabet[slot]`, so `dec(0)` reads as 4 on a
        5-alphabet slot. **The conclusion survived and the reasoning did not**, which is worth
        the two lines because the false version is the more persuasive one.

        **A WORLD THE AGENT'S VOCABULARY CANNOT EXPRESS PRODUCES AN UNINTERPRETABLE NULL** --
        *the mechanism is broken* and *the agent has no words for this place* read identically.
        That is the panel precondition, and it is the reason for the wrap rather than
        convenience: `inc` and `dec` mod GRID express a wrapped step EXACTLY, so movement
        becomes sayable and what remains unexplained is the WALL and the PUSH, which are the
        parts worth discovering.

        **THE HONEST COST: a real ARC board has edges and this one has none.** An agent that
        learns *position wraps* has learned something false about ARC. It is a habitat for
        exercising mechanisms, never a benchmark, and this is the sharpest way it differs.
        """
        return r % GRID, c % GRID

    def _proximity(self, who: str) -> int:
        """**`o1.proximity` AS AN ATTRIBUTE ON THE OBJECT -- Isaiah's placement, verbatim:**
        *"`proximity` is an attribute ON an object (`o1.proximity`, e.g. to the avatar)."*

        Manhattan distance to o0, the avatar. **DERIVED EVERY FRAME, NEVER STORED** -- it is a
        function of where things are, so storing it would let a rule write it and would let it
        drift from the positions it describes.

        **AND THE FUNCTION FORM IS NOT THIS AND IS STILL OWED.** He also named
        `ProximityToAnotherObject` -- a FUNCTION, *likely an atom taking objects*, giving
        distance between ANY pair. That is a vocabulary change rather than a perception one, so
        it belongs with valence and the attribute set, not here. Recorded so it is not lost.
        """
        return (abs(self.state[who + ".row"] - self.state["o0.row"])
                + abs(self.state[who + ".col"] - self.state["o0.col"]))

    def _completed(self) -> int:
        """ONE SITE. `objective()` and the published `@goal.completed` slot are one quantity,
        and computing it twice is the `A6i` collision this repo keeps filing."""
        return int((self.state["o0.row"], self.state["o0.col"]) == self.target)

    def objective(self) -> tuple[str, float]:
        return "BECOME(o0, target)", float(self._completed())

    def observe(self) -> dict[str, int]:
        """DERIVED, NEVER STORED -- no rule can write the goal; the agent only perceives it."""
        return {**self.state, GOAL_SLOT: self._completed(),
                **{f"o{i}.proximity": self._proximity(f"o{i}") for i in range(N_OBJECTS)}}

    def attribute_of(self) -> dict[str, str]:
        """Slot -> the attribute it holds. `ArcWorld` publishes this and this habitat did not,
        so a consumer written against the contract abstained here and could not be exercised --
        the same shape of hole that kept the observer off the agent path.

        Derived from the slot name because that is where the habitat puts it: slots are
        `o{i}.{attr}` by construction in `__post_init__`, so the suffix IS the attribute rather
        than a guess about it. `@goal.completed` is included on the same rule.
        """
        return {s: s.split(".", 1)[1] for s in self.slots() if "." in s}

    def board(self) -> Any:
        """THE STATE, RASTERED. Every object is one cell at its own row/col, carrying its colour;
        empty cells are 0. **A PROJECTION OF WHAT IS ALREADY HELD, introducing nothing** -- the
        rows, columns and colours are `state`'s own, and no rule reads this.

        It exists because the mutation observer takes a GRID and this habitat stores SLOTS, and
        those are two shapes of the same board. Without it the observer could only be verified on
        a real ARC game, which the board stop forbids -- so the wire would ship unexercised, which
        is the class of defect that put `observer.py` off the agent path for five months.

        **COLOURS ARE SHIFTED BY ONE AND THE REASON IS A DEFECT I WROTE AND CAUGHT.** This
        comment first claimed objects never carry the field colour. They do: `__post_init__`
        draws each from `rng.randrange(4)`, which includes 0. A colour-0 object rasters as
        background and VANISHES -- perception silently one object short, on some seeds and not
        others. So the raster writes `colour + 1` and the field keeps 0 to itself. The reading
        the observer gets is RELATIVE colour, which is all `relations.colour_source` asks of it.
        """
        g = [[0] * GRID for _ in range(GRID)]
        for i in range(N_OBJECTS):
            r, c = self.state.get(f"o{i}.row"), self.state.get(f"o{i}.col")
            if r is None or c is None:
                continue
            if 0 <= r < GRID and 0 <= c < GRID:
                # LAST WRITER WINS ON A SHARED CELL, and that is the honest raster: two objects
                # on one cell IS one cell, and pretending otherwise would publish a board the
                # habitat does not have.
                g[r][c] = int(self.state.get(f"o{i}.colour", 0)) + 1
        return g

    def cues(self) -> dict | None:
        """The mutation observer over this habitat, same contract as `ArcWorld.cues`.

        Driven once per frame and cached on the step counter rather than on a frame object,
        because this world has no frame object -- `step` invalidates it. Two calls in one step
        would match the board against itself and report every mutation as absent.
        """
        if self._cue is None:
            self._cue = self._obs.see(self.board())
        return self._cue

    def _click(self, action: str, x: int | None, y: int | None) -> None:
        """CLICK AT A CELL: whatever is there advances its colour. **Nothing moves, ever.**

        Recolour-on-click is among the commonest ARC mechanics and it is chosen for that rather
        than for convenience -- it makes the reachable attribute an UNORDERED one, which is the
        arm `BECOME` gained a value table for and which gridworld's POSITION slots cannot
        exercise.

        **AN UNAIMED CLICK IS A NO-OP AND THAT IS THE POINT.** `(x, y)` is `None` unless the
        interface aimed it, so a drawn action changes nothing and the uniform draw is a real
        control rather than a weaker version of the same thing.
        """
        if action != "ACTION6":
            raise ValueError(f"unknown action: {action}")
        self._cue = None
        if x is None or y is None:
            return
        for i in range(N_OBJECTS):
            if (self.state.get(f"o{i}.row"), self.state.get(f"o{i}.col")) == (int(y), int(x)):
                self.state[f"o{i}.colour"] = (self.state[f"o{i}.colour"] + 1) % 4
                return

    def _delta(self, action: str) -> tuple[int, int]:
        """What this action does NOW. **Fixture A's whole mechanism, and it is four lines.**

        Before the trigger it is `_DELTA`. After it, the two axes are reflected -- `up` goes
        down and `left` goes right. Nothing is random and nothing is hidden: the board is as
        lawful after as before, and an agent that had learned the mapping is now wrong about it
        in a way no amount of re-reading the action LIST would reveal.
        """
        dr, dc = _DELTA[action]
        if self.remap_after is not None and self._steps >= self.remap_after:
            return -dr, -dc
        return dr, dc

    def step(self, action: str, x: int | None = None, y: int | None = None) -> None:
        self._steps += 1
        if self.click_only:
            self._click(action, x, y)
            return
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        self._cue = None           # a new board is a new set of mutations to read off it
        dr, dc = self._delta(action)
        r0, c0 = self.state["o0.row"], self.state["o0.col"]
        r1, c1 = self.state["o1.row"], self.state["o1.col"]
        nr0, nc0 = self._wrap(r0 + dr, c0 + dc)
        nr1, nc1 = self._wrap(r1 + dr, c1 + dc)

        # THE PUSH IS RESOLVED BEFORE THE MOVE, because o1's rule reads o0's OLD cell. Resolving
        # it after would make the mover's new position the cause of its own push.
        if (nr0, nc0) == (r1, c1) and not self._blocked(r1 + dr, c1 + dc):
            self.state["o1.row"], self.state["o1.col"] = nr1, nc1
            r1, c1 = nr1, nc1

        if not self._blocked(r0 + dr, c0 + dc) and (nr0, nc0) != (r1, c1):
            self.state["o0.row"], self.state["o0.col"] = nr0, nc0
            r0, c0 = nr0, nc0

        # CONTACT PAINTS. Adjacent after the move -> o1 takes o0's colour. One of the most
        # common ARC mechanics, and it makes an ATTRIBUTE conditionally action-bearing where
        # every attribute was previously a pure spectator.
        #
        # **o0.colour AND ALL THREE o2 SLOTS STAY UNREACHABLE BY ANY ACTION**, deliberately:
        # the spectator property is what `F356`/`F359` need, and enriching the world until
        # nothing is a spectator would destroy the thing it was built to exhibit.
        if abs(r0 - self.state["o1.row"]) + abs(c0 - self.state["o1.col"]) == 1:
            self.state["o1.colour"] = self.state["o0.colour"]


def boards(n: int, start: int = 0) -> list[GridWorld]:
    """MANY BOARDS, so nothing can be overfitted to one. Seeds are consecutive and the caller's;
    a finding read on one board is a finding about that board until it is read on the rest."""
    return [GridWorld(seed=s) for s in range(start, start + n)]
