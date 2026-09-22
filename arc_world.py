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

import os
import sys
from collections.abc import Callable
from typing import Any

from arcengine import GameAction, GameState

import arc_atoms
import arc_percept
import arc_self
import sensors

SENSORS = sensors.minimum_set()

# THE OBSERVER ARM, SEAT-SIDE SWITCH, DEFAULT OFF. Isaiah's mutation observer: the tracker
# carries a wider per-object set, publishes the SEQUENCE of changes rather than the set, and
# writes relations onto the objects so the delta can key the lookup. Built in pieces behind
# ONE switch so the route chart judges the whole thing rather than a fragment -- reviewer,
# 2026-09-22. Item 4 (relations as per-pair slots) is here; it ships only with arm L, which
# bounds the operand axis the wider slot set would otherwise multiply.
_OBSERVER = bool(os.environ.get("TETHER_OBSERVER"))

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
        # SEAT-SIDE FRAME TAP, default None. §13 step 4's verifier scores the agent's achieved
        # effect against the human chunk's, and the boards exist only here -- `detail.frames` in
        # the ledger is a COUNT, so an archived run cannot be scored. The agent never reads this
        # and nothing in the loop sets it; `rlvr.py` attaches it for the duration of one run.
        self.on_frame: Any = None
        self._frame = self.w.reset()
        self._read: dict[str, int] | None = None
        self._contacts: dict[str, list[str]] | None = None
        self._contact_pts: list | None = None
        self._prev_contacts: dict[str, list[str]] | None = None
        # 18.3's family lives HERE because the members read BOARDS and the agent may not.
        # What it holds that is episode-scoped is dropped by `boundary()`, which the loop
        # calls at a level change -- see `tether.retarget`.
        self.selves = arc_self.family()
        self._mode_streak: dict[tuple, int] = {}
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
            if _OBSERVER and self._read:
                self._read.update(self._relation_slots())
        return self._read

    def _relation_slots(self) -> dict[str, int]:
        """OBSERVER ITEM 4: contact published as PER-PAIR slots, `a~b.contact`.

        **Measured before it was built, and the cheap shape was the wrong one.** A per-OBJECT
        `objN.touching` boolean reads TRUE FOR 100% OF OBJECTS on sk48, dc22 and m0r0 -- every
        object touches something -- so it discriminates nothing, carries no delta and would
        light no candidate. **The PAIR is the information**, which is what `_bindings`'
        docstring said before any of this was measured: *a relation is between two objects and
        `slot_types` can name neither the pair nor its type, WHICH IS THE BREAK.*

        **AND THE PAIR IS AFFORDABLE BECAUSE CONTACT IS SPARSE.** Mean degree 3.7-4.3 against
        92-99 objects, so the pair set is ~4n: +47-55% slots, against +1170-1259% for a dense
        `n^2` reading. The dense assumption is 23-25x more expensive than the measurement.

        **THE OWNER IS THE PAIR AND THE ATTRIBUTE IS `contact`** -- one attribute, therefore
        ONE type through `ATTRIBUTE_TYPE`. Naming the partner in the ATTRIBUTE would have
        invented a distinct type per pair and blown up `slot_types` and `peers`.

        **SHIPS ONLY WITH THE DELTA OPERAND BOUND.** `_bindings` returns every other slot, so
        +50% slots is +50% binds on an unbounded axis -- a regression that would read as
        *relations made it worse*. Bounded by the delta (arm L, both sites) it costs nothing,
        because the delta does not grow when the slot set does.
        """
        tr = getattr(self._decompose, "tracked", None) or {}
        out: dict[str, int] = {}
        for a, partners in self.contacts().items():
            for b in partners:
                if a < b and a in tr and b in tr:
                    out[f"{a}~{b}.contact"] = arc_percept.contact_faces(tr[a], tr[b])
        return out

    def read_order(self) -> tuple[list[str], str]:
        """Layer 2. The order slots are read in, RECOMPUTED PER FRAME and never settled.

        `(row, col)` is the F-pattern's degenerate form on a dense grid: top sweep, second
        sweep and left stem all collapse into raster order when every row is a sweep. The
        CONDITIONED variants -- layer-cake, spotted, marking -- are deliberately not built:
        their firing conditions are thresholds nobody has measured, and picking one here is
        the invented number. Name order is the fallback where geometry is unreadable, which
        is what the loop had for every slot until now.

        SEAT-SIDE AND NEVER A TERM. §23.2 governs loading it; it produces no atom, enters no
        closure, and leaves nothing behind -- a read-order for a frame not yet seen would be
        a guess.
        """
        tracked = getattr(self._decompose, "tracked", {}) or {}
        seen = False

        def key(s: str) -> tuple:
            nonlocal seen
            o = tracked.get(s.rsplit(".", 1)[0])
            if not isinstance(o, dict) or "row" not in o or "col" not in o:
                return (1, 0, 0, s)
            seen = True
            return (0, int(o["row"]), int(o["col"]), s)

        out = sorted(self._decomposed(), key=key)
        return out, ("raster" if seen else "name")

    def slots(self) -> list[str]:
        return self.read_order()[0]

    def shapes(self) -> dict[int, frozenset]:
        """`{published shape id: the normalised offset frozenset it stands for}`.

        **THE STAND-IN IS INVERTIBLE, WHICH IS WHY THE STRUCTURE NEEDS NO STORING.**
        `arc_percept` assigns the id from a table keyed BY the frozenset, and that table is
        reset nowhere and built once per run -- so an id from ANY frame maps to the same
        structure, and a REPLAYED id resolves exactly as a live one does.

        `RELATIONS.md`: *the structural quantity is computed every frame and the published
        stand-in is what removed* `symmetry`, `similarity`, `rotation`, `spin`, `interlock`
        and `rolling`. This is the structure put back beside the stand-in, not in place of it.
        """
        tbl = getattr(self._decompose, "_shapes", None) or {}
        return {v: k for k, v in tbl.items()}

    def attribute_of(self) -> dict[str, str]:
        """`{slot: which attribute it holds}`. **The loop may not derive this** -- it would
        have to split the slot name, which is `slot_owner`'s reason, one field over."""
        return {s: s.rsplit(".", 1)[1] for s in self._decomposed()}

    def peers(self) -> dict[str, tuple[str, ...]]:
        """`{slot: the SAME attribute on every OTHER object}`. **The loop may not derive this**
        -- it would have to split the slot name, which is reading domain structure, the same
        reason `slot_owner` is declared here.

        This is the population a quantifier ranges over: *do all the objects agree on this
        attribute*, which is the group question the loop could only ask one operand at a time.
        """
        by_attr: dict[str, list[str]] = {}
        for s in self._decomposed():
            by_attr.setdefault(s.rsplit(".", 1)[1], []).append(s)
        return {s: tuple(x for x in group if x != s)
                for group in by_attr.values() for s in group}

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

    def contacts(self) -> dict[str, list[str]]:
        """Which objects touch, this frame. **The loop may not derive this** -- §12.3 sensor 8,
        and §16.5's *you do not invent the list, you read it off the world.*

        **CACHED ON THE FRAME**, for the reason `_decomposed` is: `_bindings` is called per
        candidate, and contact is 210 pairs on a 21-object board. Measured density is ~12%, so
        the answer is small even where the computation is not.
        """
        if self._contacts is None:
            tr = self._decompose.tracked
            names = sorted(tr)
            out: dict[str, list[str]] = {n: [] for n in names}
            for i, a in enumerate(names):
                for b in names[i + 1:]:
                    if arc_percept.touching(tr[a], tr[b]):
                        out[a].append(b)
                        out[b].append(a)
            self._contacts = out
        return self._contacts

    def contact_points(self) -> list[tuple[str, str, str]]:
        """`(a, b, kind)` for every touching pair this frame, kind from RELATIONS.md 1.1.

        **The loop may not derive this** -- the same rule as `contacts()`, §16.5: *you do not
        invent the list, you read it off the world.* System 0 needs contact TYPES rather than
        the boolean, because *the subdivision carries information the boolean does not*: a
        point contact affords pivoting, an edge sliding, a face pushing. Trying one is not
        trying the others.
        """
        # CACHED ON THE FRAME, for the reason `contacts()` is: this is O(n^2) over tracked
        # objects -- 400 of them on m0r0 is 80,000 pairs -- and System 0 asks twice a
        # cycle, once for the switch and once for the target.
        if self._contact_pts is None:
            tr = self._decompose.tracked
            names = sorted(tr)
            out = []
            for i, a in enumerate(names):
                for b in names[i + 1:]:
                    k = arc_percept.contact_kind(tr[a], tr[b])
                    if k is not None:
                        out.append((a, b, k))
            self._contact_pts = out
        return self._contact_pts

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

        F28 (reviewer-steered 2026-09-14): `ACTION6` -- the one POSITIONED action, `ComplexAction`
        carrying `x, y` -- is now advertised, because the loop CAN supply a position: the coordinate
        check passed (the agent perceives object positions via `components`, so it chooses the
        goal-object's position). Advertising a positioned action was only illegitimate while the
        loop could not position it; `step(action, x, y)` now can. Only the DIRECTIONAL SEMANTICS
        must never reach the agent (F28's hard line) -- availability is legitimate to read.

        AND RESET IS WITHHELD, which `is_simple()` would otherwise let through. §21.2:
        `ResetGate` bans THE AGENT CALLING RESET, because a self-inflicted restart is the
        farming path -- `bounds.py` exists because a harness once force-RESET on GAME_OVER
        to farm ~18 unearned attempts. A GAME-INFLICTED restart is the world's own rule
        and reaches the loop as an observation; an agent-callable one is a bypass of it.
        """
        return tuple(GameAction.from_id(i).name
                     for i in (self._frame.available_actions or ())
                     if GameAction.from_id(i) is not GameAction.RESET
                     and (GameAction.from_id(i).is_simple()
                          or GameAction.from_id(i) is GameAction.ACTION6))

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
                # THE COUNT OF LABELS, NOT THE SPACE OF SHAPES. The slot holds an ID, and an
                # id is a label -- arbitrary, comparable, never orderable -- so its alphabet
                # is the number of labels, exactly as `colour`'s is the palette. `2**(h*w)`
                # priced the space of shapes that COULD exist, which is not what the slot
                # holds, and charged 4,096 bits for a full-board object.
                #
                # **IT GROWS WITH OBSERVATION, AND THAT IS STATED RATHER THAN AVOIDED.** Being
                # wrong costs more as the world turns out to be richer -- a fact about the
                # world, not a metric drifting, and colour's would do the same on a board that
                # revealed new colours. **The failure mode to WATCH is unbounded growth**: if
                # the shape count never settles, the cost of a shape miss never settles
                # either. Different from `lib ok here / lib`, which was a RATIO whose
                # denominator the mechanism itself moved.
                out[s] = max(2, len(getattr(self._decompose, "_shapes", ()) or ()))
            elif key == "drow":
                out[s] = 2 * h
            elif key == "dcol":
                out[s] = 2 * w
            elif key in ("row", "h"):
                # THE DELTA FIX, EXTENDED TO WHERE IT STOPPED SHORT. The paragraph above says
                # it for the deltas -- *a displacement ranges over the board, not the palette*
                # -- and `row`, `col`, `h` and `w` fell through to the palette anyway. Same
                # collision, different slot family: 64 rows under a 16-colour palette makes
                # `row 3` and `row 19` read alike under `correction_bits`' modulo.
                out[s] = h
            elif key in ("col", "w"):
                out[s] = w
            else:
                out[s] = self._palette
        return out

    def objective(self) -> tuple[str, float]:
        f = self._frame
        win = f.win_levels or 1
        return "ALL(BECOME(level, completed))", min(1.0, f.levels_completed / win)

    def placements(self) -> dict:
        """The encounter half, read: how many distinct values were met, and which objects
        changed the placement they hold."""
        d = self._decompose
        changes = getattr(d, "changes", {}) or {}
        return {"distinct": len(getattr(d, "placements", {}) or {}),
                "multi": sorted(n for n, h in changes.items() if len(h) > 1),
                "held": {n: list(h) for n, h in sorted(changes.items()) if len(h) > 1}}

    def contact_changes(self) -> dict:
        """WHICH RELATIONS CHANGED, and how certain the identity beneath them is.

        **A RELATION IS NOT A SLOT, so a relational change cannot reach the retrieval key
        through `slot_types`** -- which is what link 2's break amounts to. It does not need to:
        the key crosses on TYPES, not on instances, so *a relation of this type changed* is
        sayable without publishing a slot per pair. **That avoids the pair-slot explosion
        entirely** -- no `o1~o2.touching`, no n-squared slots.

        **AND IT CARRIES THE CONFIDENCE OF THE IDENTITY IT RESTS ON.** Contact CHANGED is a
        claim about two frames, so it depends on the tracker having matched both objects
        across them -- and P2's measurement says that match is sometimes a 0.0625 overlap.
        **A relational change resting on a thin match is a weaker claim than one resting on a
        1.0 match, and the number says which.**
        """
        prev, now = self._prev_contacts, self.contacts()
        if prev is None:
            return {"types": (), "n": 0, "confidence": None}
        changed = {n for n in set(prev) | set(now)
                   if sorted(prev.get(n, ())) != sorted(now.get(n, ()))}
        if not changed:
            return {"types": (), "n": 0, "confidence": None}
        m = self.matches()
        scores = [s for n in changed for r, s in (m.get(n, ("birth", 0.0)),) if r == "overlap"]
        return {"types": (sensors.BOOL,), "n": len(changed),
                "confidence": round(min(scores), 4) if scores else 0.0}

    def matches(self) -> dict[str, tuple[str, float]]:
        """How each object's identity was established this frame, and how certain it was.

        The domain declares it because the tracker computes it: the loop cannot know that
        `overlap` beat `shape` for a given name without re-running the matcher.
        """
        return dict(getattr(self._decompose, "matches", {}) or {})

    def cascade(self) -> tuple:
        """THE WITHIN-STEP STACK -- every frame this action returned, oldest to newest.

        `board()` returns `frame[-1]` and is right to: **the settled board is what the next
        observation corroborates, so betting on `frame[0]` is betting on a board the world has
        already left.** §16.3's point is that this is correct for the PREDICTION TARGET and
        wrong as a general policy -- *the intermediate frames are free evidence about
        MECHANISM, and nothing in the tree reads them.*

        **TWO USES OF ONE FIELD: `frame[-1]` is what you bet against; the whole stack is what
        you learn the mechanism from.** This is the second use, published. What the endpoint
        erases is the WITHIN-STEP ORDER -- *A moved, THEN B reacted* -- and a single settled
        board cannot say which.
        """
        f = self._frame
        if f is None or f.is_empty():
            return ()
        return tuple(f.frame)

    def board(self) -> Any:
        """The SETTLED board, as a numpy ndarray.

        `frame` is a stack played oldest to newest, so acting on frame[0] means betting
        on a board the world has already left. Empty until the first frame arrives, and
        an empty stack is a legal state rather than an error."""
        if self._frame is None or self._frame.is_empty():
            return None
        return self._frame.frame[-1]

    def observe(self) -> dict[str, int]:
        """VALUES ONLY, AND THE NON-READINGS ARE STRIPPED HERE ON PURPOSE -- ruling (b).

        `_decomposed` publishes `NOT_RESOLVED` for a COVERED object's attributes: the object
        exists and cannot be read. Every other reader of `_decomposed` -- `slots`,
        `alphabet`, `slot_types`, `read_order` -- iterates KEYS, so they all learn the object
        is still there, and `_present`'s `gone` loop therefore keys on OBJECT absence rather
        than value absence. **That is the half of the ruling that keeps the binding alive.**

        This reader wants VALUES, and there is no value. Handing the sentinel on would put a
        non-int into a stream typed `dict[str, int]` that is differenced, modulo'd and
        compared by ~48 atoms -- five crash sites in one run before this boundary was moved
        here. Omitting it costs nothing that is wanted: `perceive` bets only over slots
        present in `before`, `history` requires both endpoints, and `_record`'s `pick` is
        `rec.get(key, NOT_RESOLVED)` -- so the agent still READS NOT_RESOLVED, and the
        suspension falls out of machinery that already existed.
        """
        return {k: v for k, v in self._decomposed().items() if v is not sensors.NOT_RESOLVED}

    def step(self, action: str, x: int | None = None, y: int | None = None) -> None:
        act = GameAction[action]
        # F28: a positioned (complex) action carries a coordinate the agent chose from perception.
        # x = column, y = row (screen convention over the row/col grid), each 0-63. The wrapper
        # takes the coordinate as `data` and builds `ActionInput(id=action, data=data or {})` --
        # `GameAction.set_data` is NOT read on this path, so the coordinate MUST go through `data`
        # or the game receives an empty dict (a no-op or a KeyError on `data['x']`).
        data = ({"x": int(x), "y": int(y)}
                if act.is_complex() and x is not None and y is not None else None)
        was = self.board()
        was_objs = {k: dict(v) for k, v in self._decompose.tracked.items()}
        nxt = self.w.step(act, data=data) if data is not None else self.w.step(act)
        if nxt is not None:
            self._frame = nxt
        self._read = None          # a new frame is a new decomposition
        self._prev_contacts = self._contacts
        self._contacts = None      # and a new set of contacts
        self._contact_pts = None   # and a new set of typed contact points
        now = self.board()
        if self.on_frame is not None:
            self.on_frame(was, action, now)
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

    def locus_masks(self) -> dict[str, set]:
        """Each tracked object's cells. The mask a per-locus reading is taken through."""
        tr = getattr(self._decompose, "tracked", {}) or {}
        return {n: set(o["cells"]) for n, o in tr.items() if isinstance(o, dict)
                and "cells" in o}

    def mode(self) -> dict[str, Any]:
        """§16.2's contingent read, PER LOCUS -- and the board reading is a FINDING.

        `embodied` needs a member to explain more of this locus than it leaves unexplained,
        held for `MIN_REPEAT` -- the same condition and the same constant `has_self` uses, not
        a second one. `disembodied` needs the POSITIVE conjunct §16.2 states: no locus holds
        AND the board moved. Everything else is `unknown`, which is `NOT_RESOLVED` at this
        layer rather than a failure.

        THE BOARD VALUE NEVER GATES. It is composed after the fact and reported; the loop
        branches on nothing here. `coupled` is absent on purpose -- it needs the pair
        displacement comparison, which is a different reading.

        **THE TRAJECTORY WAS ENTANGLED WITH IDENTITY AND IS NOT ANY MORE -- FIXED 2026-09-04.**
        The streak was keyed on the tracker's NAME, so it died when the name churned and *the
        mode switched at step 7* was indistinguishable from *the tracker lost the object at
        step 7*. **Measured A/B over 25 steps: name-keyed gives 7 board flips, invariant-keyed
        gives 1.** No single key would have worked -- `hash(shape)` churns twice as often as
        the name here -- because a self-hypothesis IS a claim about what changes. Each member
        now keys its own streak on its OWN invariant, read off its own matching code.

        **STILL UNTESTED ON THIS FIXTURE, AND BOTH ARE PANEL GAPS RATHER THAN CODE GAPS:**
        no streak ever RESET in 25 steps, so demotion -- which is the switch detection -- has
        no case here; and two loci sharing a member's key (two objects of one colour, under
        `growth`) would share a streak, which is right by that member's claim and unexercised.
        """
        masks = self.locus_masks()
        tracked = getattr(self._decompose, "tracked", {}) or {}
        by_member = {m.name: m for m in self.selves.members}

        def key(member: str, locus: str):
            """PER MEMBER, ON THAT MEMBER'S OWN INVARIANT. The tracker's name churns and no
            single invariant is neutral -- picking one would privilege one member's claim,
            which is what the non-simulable family exists to prevent. Falls back to the name
            where a member declares none."""
            m, obj = by_member.get(member), tracked.get(locus)
            k = m.identity_key(obj) if m is not None and isinstance(obj, dict) else None
            return (member, k if k is not None else locus)

        per = self.selves.per_locus(masks)
        for locus, scored in per.items():
            for name, res in scored.items():
                kk = key(name, locus)
                self._mode_streak[kk] = (self._mode_streak.get(kk, 0) + 1
                                         if (1.0 - res) > res else 0)

        # PER LOCUS THE ONLY VALUES ARE `embodied` AND `unknown`. `disembodied` is a claim
        # about the BOARD -- *no slot correlates but the board changes* -- so writing it onto
        # each locus was a board fact overwriting per-locus readings, and it made `hybrid`
        # unreachable: nothing could then disagree.
        by = {locus: [n for n in by_member
                      if self._mode_streak.get(key(n, locus), 0) >= arc_self.MIN_REPEAT]
              for locus in masks}
        per_locus = {locus: ("embodied" if b else "unknown") for locus, b in by.items()}

        moved: set = set()
        for m in self.selves.members:
            moved |= m.changed
        held_cells: set = set()
        for locus, b in by.items():
            if b:
                held_cells |= masks.get(locus, set())
        # CHANGE THE EMBODIED LOCI DO NOT COVER. That residue is what an actuator looks like,
        # and it is what separates `hybrid` from `embodied` rather than a second detector.
        outside = moved - held_cells
        if not moved:
            board = "unknown"
        elif not held_cells:
            board = "disembodied"
        else:
            board = "hybrid" if outside else "embodied"
        return {"board": board, "per_locus": per_locus,
                "by": {k: b for k, b in by.items() if b},
                "outside": len(outside)}

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
        b = getattr(self._decompose, "boundary", None)
        if b is not None:
            b()                    # placements are per play; `_shapes` is not touched
        self._mode_streak = {}
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
