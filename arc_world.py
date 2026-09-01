"""2a. The eight members over `arc_agi`. The ADAPTER, and deliberately nothing more.

THE DECOMPOSITION IS NOT HERE. ARC has no named slots -- finding them is perception, which
is 2b -- so `slots()` returns whatever the injected `decompose` says. The adapter's job is
the API boundary; what counts as a slot is 2b's, and injecting it is how 2a declines to
answer a question that belongs to the next item. Same for the atom set, which is 3d's.

WHAT THIS FILE MAY READ. It is the domain side of the TID251 wall, so importing `arc_agi`
is its job and not a breach. It reads the FRAME and the wrapper's own surface. It does not
read game internals, and there is nothing here that knows what any board means.
"""
from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

from arcengine import GameAction, GameState

import arc_atoms
import arc_percept
import arc_self
import sensors

SENSORS = sensors.minimum_set()

sys.dont_write_bytecode = True

# the board is a numpy ndarray, NOT `list[list[int]]`: `FrameDataRaw.frame` is a
# property over a PrivateAttr holding `List[ndarray]`, runtime-only and unserialized.
# The HARNESS converts with `arr.tolist()`; the TOOLKIT path -- this one -- does not,
# so a decomposition written against the harness's lists would silently receive arrays.
Decompose = Callable[[Any], dict[str, int]]


class ArcWorld:
    """One ARC environment, wearing the eight-member contract.

    `decompose` turns the settled board into named slots and is 2b's to supply.
    `atoms` is 3d's. Both are arguments because neither is the adapter's to decide, and a
    default for either would be this file answering a question it was built to defer.
    """

    def __init__(self, wrapper: Any, decompose: Decompose, atoms: list,
                 palette: int, views: Any = None, name: str = "arc") -> None:
        self.w = wrapper
        self._decompose = decompose
        self.blind = False
        self._atoms = list(atoms)
        # 2c's lens, injected for the same reason the decomposition is: the coarse views a
        # board offers depend on what a slot IS, and that is not the adapter's to decide.
        self._views = views
        # no default: the palette size is the DOMAIN's fact, and a number invented here
        # would be a magic constant wearing an adapter's clothes.
        self._palette = int(palette)
        self._name = name
        self._frame = self.w.reset()
        self._read: dict[str, int] | None = None
        # 18.3's family lives HERE because the members read BOARDS and the agent may not.
        # What it holds that is episode-scoped is dropped by `boundary()`, which the loop
        # calls at a level change -- see `tether.retarget`.
        self.selves = arc_self.family()
        # 16.4's profile table. Here for the same reason: it reads OBJECTS, and its per-episode
        # bindings drop through `boundary()` rather than living past a level change.
        self.aff = arc_percept.Affordances()
        # HOW MANY STEPS NOBODY OBSERVED. A skipped read that is not counted is the silent
        # half of an abstention -- the flag says WHY, this says HOW MUCH.
        self.unobserved = 0

    # -- the eight -----------------------------------------------------------------------

    def substrate(self) -> str:
        return (f"a stack of 2-D grids of colour indices mod {self._palette}; "
                "the settled board is frame[-1]")

    def environment(self) -> str:
        return "a hidden per-game rule set; the shaping medium is the board"

    def actors(self) -> str:
        return ("the actions the frame advertises, which change per frame because "
                "availability is a condition met or unmet")

    def currency(self) -> str:
        return "prediction error in bits, per slot"

    def ground(self) -> str:
        return ("levels_completed, read off the frame. There is no score field, and "
                "levels_completed == win_levels is the win")

    def _decomposed(self) -> dict[str, int]:
        """ONCE PER FRAME. The decomposition is a function OF THE FRAME, and 2b's is
        STATEFUL because tracking is -- so calling it from both `slots()` and `observe()`
        advanced the tracker twice per step and the two disagreed, which surfaced as a
        `KeyError` on a slot that existed in one call and not the other.

        **The eight-member contract assumes purity and perception cannot be pure.** Caching
        per frame is where the two meet: the frame is what changes, so it is what the cache
        is keyed on."""
        if self._read is None:
            b = self.board()
            # THROUGH THE TYPED REGISTRY. `{}` from an unreadable board asserts *this board
            # has no slots*, so the loop reads zero residual and reports a clean bill of
            # health FROM A BLIND INSTRUMENT -- the confabulation §12.2's totality exists to
            # stop, one level below where abstention is implemented. `blind` is the reading;
            # an empty dict is a guess.
            seen = SENSORS.read("components", b)
            self.blind = seen is sensors.NOT_RESOLVED
            self._read = {} if self.blind else dict(self._decompose(b))
        return self._read

    def slots(self) -> list[str]:
        return sorted(self._decomposed())

    def slot_types(self) -> dict[str, str]:
        """What KIND of quantity each slot holds. **The loop may not derive this.**

        A slot name is `{object}.{attribute}` and a loop that split on `.` would be reading
        domain structure. Same shape as `alphabet()`: the domain declares, the loop compares.

        **THE ATTRIBUTE IS NOT THE TYPE, AND RETURNING THE KEY SAID IT WAS.** §12.2's set is
        `COLOUR COUNT POSITION EXTENT SHAPE BOOL DELTA AXIS RATIO` and *the attribute types
        are what make the join sound* -- `row` and `col` are one POSITION. Typed through
        `arc_atoms.ATTRIBUTE_TYPE`, which is the same table `_extract` types its atoms with,
        because a slot IS an object's attribute and two tables would drift.
        """
        return {s: arc_atoms.ATTRIBUTE_TYPE.get(s.rsplit(".", 1)[-1], s.rsplit(".", 1)[-1])
                for s in self._decomposed()}

    def sensors(self) -> Any:
        """The typed registry. `atoms()` declares Γ's vocabulary; this declares perception's.

        §12.1 puts SENSOR in *a typed registry, which is not Γ*, and §12.4 has the agent
        compose new sensors from it -- so the loop has to be able to reach it, the same way it
        reaches the atoms. The domain supplies the instrument set; the loop composes.
        """
        return SENSORS

    def slot_owner(self) -> dict[str, str]:
        """Which SUBJECT each slot is an attribute of. **The loop may not derive this.**

        §12.4's trigger is over *slots with the same attribute VECTOR*, and a vector needs
        several slots to belong to one thing. `slot_types` already establishes the pattern and
        the reason: a slot name is `{object}.{attribute}` here, **and a loop that split on `.`
        would be reading domain structure.** Grouping is that same split, so the domain
        declares it and the loop only compares.
        """
        return {s: s.rsplit(".", 1)[0] for s in self._decomposed()}

    def atoms(self) -> list:
        return list(self._atoms)

    def transform(self) -> Any:
        """The coarse views this board offers, or None if the lens committed to nothing.

        2c supplies them. `None` is a READING rather than an absence: the loop records it as
        `channel_closed` with `env.transform() returned None` as the cause, which is the
        honest state for a board that is not a rendering of anything coarser."""
        return self._views

    # -- running -------------------------------------------------------------------------

    def actions(self) -> tuple[str, ...]:
        """What the FRAME advertises, re-read every call.

        SIMPLE ACTIONS ONLY. `ACTION6` is complex and carries `x, y` -- a POSITIONED
        action, which is §17.1's arity question and 2c's to answer. Advertising it here
        without the position would be advertising an action the loop cannot actually take.

        AND RESET IS WITHHELD, which `is_simple()` would otherwise let through. §21.2:
        `ResetGate` bans THE AGENT CALLING RESET, because a self-inflicted restart is the
        farming path -- `bounds.py` exists because a harness once force-RESET on GAME_OVER
        to farm ~18 unearned attempts. A GAME-INFLICTED restart is the world's own rule
        and reaches the loop as an observation; an agent-callable one is a bypass of it.
        """
        return tuple(GameAction.from_id(i).name
                     for i in (self._frame.available_actions or ())
                     if GameAction.from_id(i).is_simple()
                     and GameAction.from_id(i) is not GameAction.RESET)

    def alphabet(self) -> dict[str, int]:
        """PER SLOT, AND FOR SOME SLOTS PER STEP. `_alphabets` has always accepted a dict --
        *a domain whose slots differ declares the difference* -- and every slot that existed
        when it was written had a constant range, so a single number was enough.

        **A SHAPE SLOT DOES NOT, AND THAT IS A PROPERTY OF SHAPE.** A shape is a subset of its
        own bounding box, so the uniform code over what it could have been is `h*w` bits and
        the alphabet is `2**(h*w)` -- derived from two attributes already published, nothing
        tuned. It changes when the object resizes, so **this function returns different values
        on different calls for the same slot, by design**: the next reader will find that and
        take it for a defect without this line beside it. The line stays where it was -- the
        domain declares, the loop compares -- and only WHEN the declaration is read has moved.

        **AND THE DELTAS ARE FIXED HERE TOO.** They were published against the palette, so
        `drow = -5` and `drow = 8` both read as 8 under `correction_bits`' modulo on a
        13-colour board -- a collision introduced with the sensor and found while implementing
        this. A displacement ranges over the board, not the palette.
        """
        d = self._decomposed()
        b = self.board()
        # `b is None`, NEVER `if b`: the board is a numpy array and its truth value raises.
        # 8 seats read clean with this wrong, because no conform world hands back an array.
        h = len(b) if b is not None else self._palette
        w = len(b[0]) if b is not None and len(b) else self._palette
        out: dict[str, int] = {}
        for s in d:
            key = s.rsplit(".", 1)[-1]
            if key == "shape":
                o = self._decompose.tracked.get(s.rsplit(".", 1)[0], {})
                out[s] = 2 ** max(1, int(o.get("h", 1)) * int(o.get("w", 1)))
            elif key == "drow":
                out[s] = 2 * h
            elif key == "dcol":
                out[s] = 2 * w
            else:
                out[s] = self._palette
        return out

    def objective(self) -> tuple[str, float]:
        f = self._frame
        win = f.win_levels or 1
        return "ALL(BECOME(level, completed))", min(1.0, f.levels_completed / win)

    def board(self) -> Any:
        """The SETTLED board, as a numpy ndarray.

        `frame` is a stack played oldest to newest, so acting on frame[0] means betting
        on a board the world has already left. Empty until the first frame arrives, and
        an empty stack is a legal state rather than an error."""
        if self._frame is None or self._frame.is_empty():
            return None
        return self._frame.frame[-1]

    def observe(self) -> dict[str, int]:
        return dict(self._decomposed())

    def step(self, action: str) -> None:
        act = GameAction[action]
        was = self.board()
        was_objs = {k: dict(v) for k, v in self._decompose.tracked.items()}
        nxt = self.w.step(act)
        if nxt is not None:
            self._frame = nxt
        self._read = None          # a new frame is a new decomposition
        now = self.board()
        self._decomposed()          # re-track before reading contact on the new frame
        # BOTH READERS ABSTAIN ON A BLIND FRAME, AND ONLY ONE OF THEM USED TO. When `blind`,
        # `_decomposed` never calls the tracker, so `tracked` KEEPS ITS LAST READABLE STATE --
        # and `note` then compared stale to stale and wrote 15 bindings in a single step,
        # measured. That is `_decomposed`'s own warning at a sibling site: a reading taken
        # FROM A BLIND INSTRUMENT. The loop was already safe by a different route (`{}` slots
        # trip `no_slots`), so the flag protected nothing that a new caller could inherit.
        if self.blind:
            self.unobserved += 1
        else:
            if was is not None and now is not None:
                self.selves.observe(was, action, now)
            self.aff.note(was_objs, dict(self._decompose.tracked), mover=None)

    def contingency(self) -> dict[str, dict[str, float]]:
        """What each self-hypothesis MEASURED under each action. **Learned, never handed.**

        `{member: {action: mean of that member's own signal}}` -- action names and scalars,
        the same class as `actions()` and `alphabet()`. No board crosses, and nothing here
        says what any action MEANS: a member reports what moved when it acted.

        **THIS IS THE HALF `act` WOULD HAVE HANDED.** `ARC_AGENT`: *it has never had to learn
        what pressing something does, because the primitive it was given already knew.* The
        difference is provenance, and provenance is the whole of it -- an empty dict before
        anything is observed is what a closed-over effect table can never produce.
        """
        return {m.name: {"per_action": m.contingency(), "stable": m.stable()}
                for m in self.selves.members}

    def boundary(self) -> None:
        """Drop what was bound to THIS episode. Colours permute on a refresh, so a colour
        identity is valid only for the episode it was read in."""
        self.selves.boundary()
        self.aff.boundary()

    # -- read by the harness, never by the loop --------------------------------------------

    def terminal(self) -> str:
        f = self._frame
        if f.state == GameState.WIN:
            return "advance"
        if f.state == GameState.GAME_OVER:
            return "death"
        return ""

    # NO `restart()`. One was built here and removed the same day: its only caller
    # restarted into a LIVE agent, and `retarget` keeps `gamma`, so it handed the level back
    # with what had been learned -- an ATTEMPT, whoever pressed the button. The ruling is that
    # the seat may restart for its OWN measurement and not to help the agent learn, and the
    # check is carriage rather than intent: does anything cross the restart? A method here
    # would be a trapdoor to the version that does. `arc_holdout.controlled()` resets the
    # wrapper directly, with no agent in the run at all.

    def levels(self) -> tuple[int, int]:
        return self._frame.levels_completed, self._frame.win_levels

    # `reset_kind` -- RESET vs ADVANCE, which invert the meaning of a residual spike
    # (§21.5) -- is NOT here. The frame carries `full_reset` and `levels_completed`, so the
    # discriminator is recoverable, and 2e is what consumes it. Building it now would be a
    # mechanism ahead of its consumer, which ISOLATED caught on the first run.
