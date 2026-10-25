# RELATIONS.md (cited below) are docs/library-closure/ files DELETED 2026-10-11 (Section A);
# git holds them at the parent of the deleting commit (DOCS_CONSOLIDATION.md section A).
# RELATIONS.md's live successor: library/given.json (kind RELATION) + LIBRARY_SPEC section 3.
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

import hashlib
import sys
from collections.abc import Callable
from typing import Any

from arcengine import GameAction, GameState

import arc_atoms
import arc_percept
import arc_self
import armflag
import cap
import ledger
import observer
import relations
import sensors

SENSORS = sensors.minimum_set()
# The platform's own actions, accepted in every state whatever the game declares (`actions`).
PLATFORM_UNIVERSAL = (GameAction.RESET.name,)

# THE OBSERVER ARM, SEAT-SIDE SWITCH, DEFAULT ON. Isaiah's mutation observer: the tracker
# carries a wider per-object set, publishes the SEQUENCE of changes rather than the set, and
# writes relations onto the objects so the delta can key the lookup. Built in pieces behind
# ONE switch so the route chart judges the whole thing rather than a fragment -- reviewer,
# 2026-09-22. Item 4 (relations as per-pair slots) is here; it ships only with arm L, which
# bounds the operand axis the wider slot set would otherwise multiply.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_OBSERVER = armflag.arm("TETHER_OBSERVER", default=True)
# ARC B2 (the reviewer 2026-10-11 10:11, 10:20, 11:48 CDT): pair relations as slots over the contact
# pairs and the agent's actor pairs. ON; reason in conform/arms.py.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_RELATION_SET = armflag.arm("TETHER_RELATION_SET", default=True)
# bp35's crowded-board search (Isaiah 2026-10-23; the reviewer 2026-10-25 06:25, 06:31):
# relational_slots kept while the frame's read and pair read are the same objects (its only
# inputs, never written in place after they are built). _CHECK rebuilds on every call and asserts
# the kept tuple equal.
_REL_SLOTS_CACHE = armflag.arm("TETHER_REL_SLOTS_CACHE", default=True)
_REL_SLOTS_CHECK = armflag.arm("TETHER_REL_SLOTS_CHECK", default=False)
REL_SLOTS_N = {"kept": 0, "built": 0, "checked": 0}
# E0: each object attribute the percept derives, and the readings it derives it from (the frame
# deltas from the before-state's readings too). The cell-change attributes (add_* / rem_*) are NOT
# here: they also depend on how the tracker established identity (identity_of), not only on readings
_OBJ_DERIVED = {"h": ("shape",), "w": ("shape",), "dh": ("shape",), "dw": ("shape",),
                "dcells": ("shape",), "dholes": ("shape",), "dperimeter": ("shape",),
                "drow": ("row",), "dcol": ("col",), "speed": ("row", "col"),
                "colour_changed": ("colour",)}
# E0b: the observer-item-4 pair slots (_relation_slots), each a function of both parties' cells
_OBS_PAIR = ("contact", "bbox", "inside")


def _oldest(d: dict) -> int:
    """The age of the oldest object in the frame: no object has been tracked longer."""
    return max((v for k, v in d.items() if k.rsplit(".", 1)[-1] == "age" and isinstance(v, int)),
               default=0)


# EVERY PUBLISHED ATTRIBUTE DECLARES ITS RANGE -- F495, the reviewer 2026-10-07: an undeclared one
# fell to the palette and was read modulo it, three times (`drow`, F494, and these twelve, two of
# them -- `dholes`, `dperimeter` -- live on every ARC run). Each range is what the attribute can
# take on an h x w board; a signed change needs both signs. `alphabet()` raises on anything else.
ALPHABET: dict[str, Callable[[int, int, dict], int]] = {
    "dh": lambda h, _w, _d: 2 * h, "dw": lambda _h, w, _d: 2 * w,         # as `drow`/`dcol`
    "dcells": lambda h, w, _d: 2 * h * w + 1,                           # +-hw cells
    "dholes": lambda h, w, _d: 2 * h * w + 1,                           # +-hw enclosed regions
    "dperimeter": lambda h, w, _d: 8 * h * w + 1,                       # a perimeter is <= 4hw
    "speed": lambda h, w, _d: max(h, w) + 1,                             # Chebyshev, one frame
    "bbox": lambda h, w, _d: h * w + 1,                                 # an intersection area
    "contact": lambda h, w, _d: 2 * h * w + 1,                          # shared faces < 2hw
    "colour_changed": lambda _h, _w, _d: 2, "inside": lambda _h, _w, _d: 2,  # BOOL
    # FRAMES, which no board quantity bounds: no object is older than the oldest, and
    # `stability` (frames unchanged) never exceeds its `age`. Varies per call, as `shape` does.
    "age": lambda _h, _w, d: _oldest(d) + 1, "stability": lambda _h, _w, d: _oldest(d) + 1,
}
PALETTE_BY_DESIGN = {"colour": "a colour IS a palette index"}

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
                 palette: int, views: Any = None, name: str = "arc",
                 platform: tuple[str, ...] = PLATFORM_UNIVERSAL) -> None:
        self.w = wrapper
        # The platform's own actions. A synthetic world with no platform passes () -- declared
        # at its construction, never inferred.
        self.platform = tuple(platform)
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
        # THE MUTATION OBSERVER, ON THE AGENT PATH -- reviewer's ruling, 2026-09-26. Distinct from
        # `on_frame` above, which is a SEAT tap the agent never reads. This one the agent reads.
        #
        # It is fed one live GRID per frame and never a tape, so `KEY_BOUNDARY` holds by shape
        # rather than by care. `conform/lint.py` moved `observer` out of `_CUE_MODULES` on
        # 2026-09-22 on the checkable fact that its `reverse_engineer` import is under `__main__`.
        self._obs = observer.Live()
        self._cue: dict | None = None
        # THE WRAPPER HAS ALREADY RESET -- 2026-10-06. Both arc_agi wrappers call `self.reset()` in
        # their own `__init__`, so a reset here was the SECOND of two consecutive RESETs on every
        # ARC run: the one sequence Isaiah ruled must never be issued (2026-09-29; INDEX:51466).
        # Take the frame it already holds; reset only a wrapper that holds none (`ReplayTape`).
        self._frame = getattr(self.w, "observation_space", None) or self.w.reset()
        self._read: dict[str, int] | None = None
        self._contacts: dict[str, list[str]] | None = None
        self._contact_pts: list | None = None
        self._shape_codes: dict = {}   # 3c-CANON: normalised cells -> their stable code
        self._prev_contacts: dict[str, list[str]] | None = None
        self._actors: frozenset = frozenset()          # ARC B2: set by the agent's `relate`
        self._pair_read: dict[str, int] | None = None  # ARC B2: this frame's pair slots
        self._rel_kept: tuple | None = None   # (read, pair read, relational_slots' tuple)
        self._pair_src: dict[str, tuple] = {}          # ARC B2: each pair slot's sources
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
            if _OBSERVER and not self.blind:
                self._walk_cascade()
            self._read = {} if self.blind else dict(self._decompose(b))
            if _OBSERVER and self._read:
                self._read.update(self._relation_slots())
                # NULL-PERSISTENCE FOR DEPARTED OBJECTS WAS BUILT HERE AND REVERTED -- reviewer,
                # 2026-09-22, and the second of their two reasons is the one I had missed. Extending
                # ruling (b) from COVERED objects to DEPARTED ones makes `came`/`gone` readable as
                # ordinary value transitions (`NOT_RESOLVED -> int` is `=>`, the reverse is
                # `-`) with no second channel, and it was verified firing on sk48 -- 497 slots
                # turning NULL at frame 8, `o5.row` 5 -> NOT_RESOLVED. Measured affordable: +13%
                # over PEAK readable with relations on, bounded by peak not churn because objects
                # do not come back.
                #
                # IT IS REVERTED ANYWAY, AND NOT BECAUSE IT IS WRONG. (1) Its only consumer is
                # the bond tests, at step 4, so it would sit unread through steps 1-3 -- the
                # silent code the checker forbids. (2) IT IS AN OBJECT-LIFETIME CHANGE INSIDE
                # THE OBSERVER A/B AND WOULD CONFOUND THE ROUTE CHART: one change at a time. The
                # second reason is the reviewer's and it is the better one.
                #
                # ONE CHECK IS OWED BEFORE IT SHIPS AT STEP 4: the bound rests on *objects do not
                # come back*, true on sk48/dc22/m0r0. A board with REAPPEARING objects tests
                # it: if a returning object RECLAIMS its old slot the set stays bounded; if the
                # tracker issues it a NEW name, it does not. Measure ever-seen against peak there
                # first. Commit `d8ae6ea` carries the implementation.
            # THE GOAL BECOMES A SLOT -- Isaiah 2026-09-24: *the agent needs to want what the
            # RLVR provides, which is the board giving the win condition and the level
            # completion increases.* It already DID provide it: `objective()` returns the same
            # number as a FLOAT. **A float the agent can read is not a quantity it can compose
            # with** -- it had no type, no alphabet, no residual, so nothing could bet on it,
            # mint against it, or want it.
            #
            # AS A SLOT IT IS ORDINARY, AND THAT IS THE ENTIRE POINT. Perception, the residual,
            # the bargain and `objective_step` all reach it with no new machinery: the last of
            # those already turns a want about a slot into *step one unit toward the nearest
            # satisfying value*, which is the decomposition that was said to be missing and is
            # merely unreachable from a float.
            #
            # A MEANS, NEVER A MEANING. The board says what winning is and still does; this
            # gives the agent the ABILITY TO HOLD IT. **Nothing here says what raises the
            # number** -- no hint, no shaping, no sub-goal written by us -- and finding that is
            # the agent's whole job.
            if self._read and not self.blind:
                f = self._frame
                self._read["@goal.completed"] = int(getattr(f, "levels_completed", 0) or 0)
        return self._read

    def _walk_cascade(self) -> None:
        """OBSERVER ITEM 2: advance the tracker over the INTERMEDIATE frames, oldest first.

        One action returns a STACK of frames and the loop has only ever read `frame[-1]`, so a
        relation forming and breaking mid-response was invisible. The ORDER of changes is the
        one thing `+` cannot be told from `→` without (`5.4`), and it lives here.

        **OPTION B, CHOSEN ON A MEASUREMENT AND NOT A PREFERENCE.** The alternative was to
        anchor identity on the settled frame and use the intermediates only to ANNOTATE order
        (`F275`). That keeps identity perfect by construction and then has to re-derive which
        settled object each intermediate component belongs to -- **which works for objects that
        held still (99.6-99.9%) and collapses on objects that MOVED (52.7-65.8%)**, i.e. on
        exactly the objects whose ordering carries information.

        **WALKING COSTS 0 TO 3.5 POINTS OF IDENTITY STABILITY** (`F274`: sk48 -1.6, su15 -3.5,
        tn36 -0.1) **AND ON THE DEEPEST-CASCADE BOARD IT BEATS THE CONTROL** -- `g50t` at 94%
        multi-frame re-issues ZERO names against the settled-only tracker's five. That is the
        direction the mechanism predicts rather than a surprise: more intermediate frames means
        smaller per-frame displacement, so `F247`'s overlap-first matcher has MORE to work with.

        **THE SETTLED BOARD IS STILL WHAT `board()` RETURNS AND WHAT THE AGENT BETS ON.** This
        advances the tracker's STATE through the cascade; the caller decomposes `frame[-1]`
        immediately after, so the published slots are the settled ones either way.
        """
        # LENGTH, NEVER TRUTHINESS. `if g and g[0]` crashed the FIRST live run with
        # *"the truth value of an array with more than one element is ambiguous"* -- the
        # ReplayTape hands LISTS, where truthiness is fine, and arcengine hands NUMPY ARRAYS,
        # where it raises. **So this arm had never once executed on the ground path**, and no
        # tape measurement could have found it: the two harnesses differ in the type of the
        # thing, not in its content. `len()` is true of both.
        fr = getattr(self._frame, "frame", None)
        if fr is None or len(fr) < 2:
            return
        for g in fr[:-1]:
            cap.head()
            if g is not None and len(g) and len(g[0]):
                self._decompose(g)

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
            cap.head()
            for b in partners:
                cap.head()
                if a < b and a in tr and b in tr:
                    out[f"{a}~{b}.contact"] = arc_percept.contact_faces(tr[a], tr[b])
        # THE BOUNDING-BOX OVERLAP SENSOR. `RELATIONS.md` Part 6 names it as the FIRST of three
        # blockers and calls it "a BUILD rather than a publish": *bounding-box overlap is not
        # computed anywhere, and containment and its five dependents wait on it.* Those six moved
        # from composable to blocked when `overlap` was checked -- so the ladder's condition is
        # met by the corpus's own record: composition tried and could not.
        #
        # THE RAW AREA, NOT BBOX CONTAINMENT. Bbox containment is `overlap == area(A)`, which the
        # agent can compose once it holds the overlap; publishing it would hand the composition
        # rather than the instrument, and that is the discovery this is meant to enable rather
        # than replace. **THAT REFUSAL STANDS AND IS ABOUT THE BOUNDING BOX.**
        #
        # AND IT IS NOT THE SAME QUANTITY AS `inside`, WHICH IS ALSO PUBLISHED HERE -- reviewer,
        # 2026-09-23, closing a name collision at both sites. `inside` is HOLE containment,
        # admitted by Isaiah as *pegs in holes* and justified as NOT derivable from `touching`,
        # because a ring touches its interior and its exterior identically. **The distinguishing
        # case: a peg overlapping a ring's WALL satisfies bbox containment and NOT hole
        # containment.** Two quantities, and the bare word `containment` is retired from both
        # sites so nothing re-derives the conflict.
        #
        # AND IT IS SPARSE, MEASURED BEFORE BUILDING: overlapping-bbox pairs run 0.6-1.4x the
        # CONTACT pairs and 1.4% of all pairs on `bp35` (582 of 41,328). Fewer than contact on
        # some boards, because two objects touching edge-to-edge have ABUTTING boxes that do not
        # overlap -- so this is not the n^2 the pair space allows.
        names = sorted(tr)
        for i, a in enumerate(names):
            cap.head()
            A = tr[a]
            for b in names[i + 1:]:
                cap.head()
                B = tr[b]
                r = min(A["row"] + A["h"], B["row"] + B["h"]) - max(A["row"], B["row"])
                c = min(A["col"] + A["w"], B["col"] + B["w"]) - max(A["col"], B["col"])
                if r > 0 and c > 0:          # sparse: absent = 0, declared in relations.SPARSE_PAIR
                    out[f"{a}~{b}.bbox"] = r * c
        # `inside` -- HOLE CONTAINMENT, the admitted atom finally built. ADMITTED 2026-09-08 and
        # absent from the registry until now: the only entry in `arc_atoms.ADMITTED` that was
        # never constructed, and it carried the batch's best reach number (+15 chains at depth 3).
        #
        # SPARSE BY CONSTRUCTION, which is what makes it affordable on the pair axis: only an
        # object WITH AN ENCLOSED REGION can contain anything, and most objects have none. The
        # dense `n^2` reading this site refuses elsewhere is +1170-1259% slots; this emits a row
        # only where a hole exists AND something sits in it.
        #
        # DIRECTED, so both orders are asked: `a~b` means B IS INSIDE A. Containment is not
        # symmetric and a single unordered row would have made it so.
        for a in names:
            cap.head()
            hole = arc_percept.enclosed_of(tr[a]["cells"])
            if not hole:
                continue
            for b in names:
                cap.head()
                if b == a:
                    continue
                cb = {tuple(c) for c in tr[b]["cells"]}
                if cb and cb <= hole:        # sparse: absent = 0, declared in relations.SPARSE_PAIR
                    out[f"{a}~{b}.inside"] = 1
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

        out = sorted(self._all(), key=key)
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
        inv = {v: k for k, v in tbl.items()}
        # APPEND-ONLY, CHECKED: ids exactly 0..n-1. A rewritten, deleted or colliding entry breaks
        # it, and the mint's frontier key reads this table by its size alone.
        assert inv.keys() == set(range(len(tbl))), "shape table is not append-only"
        return inv

    def attribute_of(self) -> dict[str, str]:
        """`{slot: which attribute it holds}`. **The loop may not derive this** -- it would
        have to split the slot name, which is `slot_owner`'s reason, one field over."""
        return {s: s.rsplit(".", 1)[1] for s in self._all()}

    def peers(self) -> dict[str, tuple[str, ...]]:
        """`{slot: the SAME attribute on every OTHER object}`. **The loop may not derive this**
        -- it would have to split the slot name, which is reading domain structure, the same
        reason `slot_owner` is declared here.

        This is the population a quantifier ranges over: *do all the objects agree on this
        attribute*, which is the group question the loop could only ask one operand at a time.
        """
        by_attr: dict[str, list[str]] = {}
        for s in self._all():
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
        return {s: self._type_of(s.rsplit(".", 1)[-1]) for s in self._all()}

    @staticmethod
    def _type_of(attr: str) -> str:
        rel = relations.pair_attr(attr)        # ARC B2: a pair slot is typed by its relation
        if rel is not None:
            return relations.PAIR_RELATIONS[rel]
        return arc_atoms.ATTRIBUTE_TYPE.get(attr, attr)

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
                cap.head()
                for b in names[i + 1:]:
                    cap.head()
                    if arc_percept.touching(tr[a], tr[b]):
                        out[a].append(b)
                        out[b].append(a)
            self._contacts = out
        return self._contacts

    def shape_code(self, owner: str) -> int | None:
        """3c-CANON: the object's CANONICAL form as a stable number -- a hash of its cells
        normalised to the bounding box's corner (arc_percept 203), so the same form reads the
        same code on any board, unlike the published `.shape`, an encounter index. None when
        the object is not tracked this frame."""
        obj = self._decompose.tracked.get(owner)
        cells = obj.get("shape") if isinstance(obj, dict) else None
        if not cells:
            return None
        code = self._shape_codes.get(cells)
        if code is None:
            raw = repr(sorted(tuple(c) for c in cells)).encode()
            code = self._shape_codes[cells] = int.from_bytes(
                hashlib.blake2b(raw, digest_size=6).digest(), "big")
        return code

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
                cap.head()
                for b in names[i + 1:]:
                    cap.head()
                    k = arc_percept.contact_kind(tr[a], tr[b])
                    if k is not None:
                        out.append((a, b, k))
            self._contact_pts = out
        return self._contact_pts

    def relational_slots(self) -> tuple[str, ...]:
        """WHICH ATTRIBUTES ARE A RELATION TO ANOTHER OBJECT. See `gridworld`'s.

        **EMPTY, AND THAT IS A DECLARATION RATHER THAN A STUB.** This world's attributes are
        read off one object -- colour, row, col, h, w, shape. `touching` and `inside` ARE
        relations, and they are RELATIONS BETWEEN A PAIR rather than attributes ON an
        object, so they are not slots here and cannot be returned by this method. **If a
        relation is ever published AS a slot it belongs in this tuple**, and the consumer
        will pick it up with no further change.
        """
        # ARC B2: the pair attributes ARE relations published as slots, declared here.
        kept = self._rel_kept
        if (_REL_SLOTS_CACHE and not _REL_SLOTS_CHECK and kept is not None
                and kept[0] is self._read and kept[1] is self._pair_read):
            REL_SLOTS_N["kept"] += 1
            return kept[2]
        out = tuple(sorted({k.rsplit(".", 1)[1] for k in self._all()
                            if relations.pair_attr(k.rsplit(".", 1)[1])}))
        REL_SLOTS_N["built"] += 1
        if _REL_SLOTS_CHECK and kept is not None and kept[0] is self._read \
                and kept[1] is self._pair_read:
            assert kept[2] == out, "TETHER_REL_SLOTS_CHECK: the kept relational_slots differ"
            REL_SLOTS_N["checked"] += 1
        if _REL_SLOTS_CACHE:
            self._rel_kept = (self._read, self._pair_read, out)
        return out

    def slot_owner(self) -> dict[str, str]:
        """Which SUBJECT each slot is an attribute of. **The loop may not derive this.**

        §12.4's trigger is over *slots with the same attribute VECTOR*, and a vector needs
        several slots to belong to one thing. `slot_types` already establishes the pattern and
        the reason: a slot name is `{object}.{attribute}` here, **and a loop that split on `.`
        would be reading domain structure.** Grouping is that same split, so the domain
        declares it and the loop only compares.
        """
        return {s: s.rsplit(".", 1)[0] for s in self._all()}

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

        AND RESET IS THE PLATFORM'S, NOT THE GAME'S (Isaiah 2026-09-29, "fully ungated undo and
        reset, just no consecutive resets"; the reviewer 2026-10-06, F477). No game declares it
        -- 22 of 22 public declarations omit id 0 -- because the engine accepts it in EVERY
        state as the universal restart. So it is offered after the declared actions, in every
        state, and `provenance` says which is which. This replaced a filter that removed RESET
        from the declared list and never once fired. The interface's adjacency rule is what
        stops RESET,RESET; the entry point never presses it.
        """
        # A game that DID declare RESET would not make it the game's: it is still the platform's,
        # still last, still `platform-universal`.
        declared = tuple(GameAction.from_id(i).name
                         for i in (self._frame.available_actions or ())
                         if GameAction.from_id(i).name not in self.platform
                         and (GameAction.from_id(i).is_simple()
                              or GameAction.from_id(i) is GameAction.ACTION6))
        return declared + self.platform

    def provenance(self, action: str) -> str | None:
        """Who offers this action: the PLATFORM in every state, or THIS GAME by declaration."""
        if action in self.platform:
            return "platform-universal"
        return "declared" if action in self.actions() else None

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
        d = self._all()
        b = self.board()
        # `b is None`, NEVER `if b`: the board is a numpy array and its truth value raises.
        # 8 seats read clean with this wrong, because no conform world hands back an array.
        h = len(b) if b is not None else self._palette
        w = len(b[0]) if b is not None and len(b) else self._palette
        out: dict[str, int] = {}
        for s in d:
            key = s.rsplit(".", 1)[-1]
            rel = relations.pair_attr(key)
            if rel is not None:
                # ARC B2: a box gap and an offset range over the board, as `drow`/`dcol` do; a
                # containment or contact is 0/1.
                out[s] = (max(h, w) if rel == "dist" else 2 * h if rel == "drow"
                          else 2 * w if rel == "dcol" else 2)
                continue
            if key == "completed":
                # THE BOARD DECLARES ITS OWN RANGE. `win_levels` is what the game says winning
                # takes, so the code over the goal slot is exactly as wide as the task is --
                # not a constant chosen here. `+1` because 0 completed is a value.
                out[s] = max(1, int(getattr(self._frame, "win_levels", 0) or 1)) + 1
                continue
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
            elif key in ("h", "w"):
                # AN EXTENT IS 0..side INCLUSIVE: an object can fill the board, and a
                # full-width object's 64 read as 0 under 64 and every miss on it was HELD.
                out[s] = (h if key == "h" else w) + 1
            elif key in ("row", "add_row", "rem_row"):
                # THE DELTA FIX, EXTENDED TO WHERE IT STOPPED SHORT. The paragraph above says
                # it for the deltas -- *a displacement ranges over the board, not the palette*
                # -- and `row`, `col`, `h` and `w` fell through to the palette anyway. Same
                # collision, different slot family: 64 rows under a 16-colour palette makes
                # `row 3` and `row 19` read alike under `correction_bits`' modulo.
                out[s] = h
            elif key in ("col", "add_col", "rem_col"):
                out[s] = w
            elif key in ("add_n", "rem_n"):
                out[s] = h * w + 1          # a cell count, 0 to the whole board
            elif key in ALPHABET:
                out[s] = ALPHABET[key](h, w, d)
            elif key in PALETTE_BY_DESIGN:
                out[s] = self._palette
            else:
                raise KeyError(f"`{s}` has no declared alphabet: declare `{key}` in ALPHABET, "
                               "or it is read modulo a number unrelated to it (F494, F495)")
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

    def frame_breaks(self) -> list[dict]:
        """B: the frame breaks the tracker read since the last call, then cleared. The agent reads
        them after its action's outcome is perceived, and at its step's head for a frame that
        arrived with no action (arrive()); nothing tells it a game changed (E4b)."""
        out = list(getattr(self._decompose, "breaks", ()) or ())
        if out:
            self._decompose.breaks = []
        return out

    def decomp_log(self) -> list[dict]:
        """B's record: every board-changed decomposition since the last call (or none), then
        cleared, so the matches row can report the first new-frame call, not only the last."""
        out = list(getattr(self._decompose, "call_log", ()) or ())
        if out:
            self._decompose.call_log = []
        return out

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
        return {k: v for k, v in self._all().items() if v is not sensors.NOT_RESOLVED}

    # -- ARC B2: pair relations as DERIVED slots ----------------------------------------------

    def relate(self, subjects: Any) -> None:
        """ARC B2 (the reviewer 2026-10-11 11:48 CDT): the agent's ACTOR SET -- the owners of its
        own `Agency.contingent` slots -- steers which pairs this world measures: every pair whose
        subject is an actor, beside the contact pairs. Attention steering perception; the world
        still names, types and owns every slot.

        AGENT-SIDE ONLY. It changes what the agent's own sensors compute over frames already
        received, and is never forwarded to the game, the harness action channel or the gateway.

        THE LAG, BY CONSTRUCTION: the agent calls this at the top of its step, before it
        observes, with what its LAST step made contingent -- so actor pairs light one step after
        contingency first appears. A changed set re-measures the current frame's pairs (computed
        from the read; the tracker is not touched), so the agent's observe sees them."""
        new = frozenset(subjects)
        if new != self._actors:
            self._actors = new
            self._pair_read = None

    def _pair_list(self) -> list[tuple[str, str]]:
        """The ordered pairs measured this frame: contact pairs both ways, and actor pairs."""
        tr = getattr(self._decompose, "tracked", None) or {}
        names = sorted(tr)
        pairs = {(a, b) for a, bs in self.contacts().items() for b in bs if a in tr and b in tr}
        pairs |= {(a, b) for a in self._actors if a in tr for b in names if b != a}
        return sorted(pairs)

    def _boxes(self, state: dict, objs: set) -> dict[str, dict]:
        """Each object's box read from SLOT values, so a predicted state derives as a seen one."""
        out = {}
        for o in objs:
            cap.head()
            vals = [state.get(f"{o}.{k}") for k in ("row", "col", "h", "w")]
            if all(isinstance(v, int) for v in vals):
                out[o] = dict(zip(("row", "col", "h", "w"), vals, strict=True))
        return out

    def _pairs_now(self) -> list[tuple[str, str]]:
        return sorted({(src[0].rsplit(".", 1)[0], src[4].rsplit(".", 1)[0])
                       for src in self._pair_src.values()})

    def derive(self, state: dict, before: dict | None = None) -> dict[str, int]:
        """The pair slots computed from any state of slot values -- the instrument applied to a
        predicted state (B2b (c)). A pair with an unreadable party is omitted. Under
        TETHER_DERIVED_PERCEPT also the object attributes (_obj_derive), and the boxes read h / w
        from the state's shape, so a predicted shape moves the pair slots too."""
        objd = ({**self._obj_derive(state, before), **self._obs_pair_derive(state)}
                if relations._DERIVED_PERCEPT else {})
        if not _RELATION_SET:
            return objd
        if objd:
            state = {**state, **{k: v for k, v in objd.items()
                                 if k.rsplit(".", 1)[1] in ("h", "w")}}
        pairs = self._pairs_now()
        boxes = self._boxes(state, {o for p in pairs for o in p})
        return {**objd, **relations.pair_slots_over(boxes, [(a, b) for a, b in pairs
                                                             if a in boxes and b in boxes])}

    def boxes(self, state: dict) -> dict[str, dict]:
        """B4: each object's box read from a state's slot values (row, col, h, w). The caller passes
        a COMPLETE state: a source its prediction does not carry (h, w under a position-only
        predictor) holds its before value, never absent -- or B4 never fires on such a world."""
        return self._boxes(state, {k.rsplit(".", 1)[0] for k in state if k.endswith(".row")})

    def derived(self) -> dict[str, tuple[str, ...]]:
        """Each pair slot and the slots it is computed from (both boxes' row, col, h, w). Under
        TETHER_DERIVED_PERCEPT also each object attribute the percept computes from readings it
        publishes (_OBJ_DERIVED), and a pair slot's h / w resolved through to the shape they come
        from, so "every source held" means row, col and shape held."""
        d = self._all()
        out = dict(self._pair_src) if _RELATION_SET else {}
        if not relations._DERIVED_PERCEPT:
            return out

        def through(src):
            got = []
            for s_ in src:
                o, a = s_.rsplit(".", 1)
                s2 = f"{o}.shape" if a in ("h", "w") else s_
                if s2 not in got:
                    got.append(s2)
            return tuple(got)
        out = {k: through(v) for k, v in out.items()}
        for k in d:
            cap.head()
            o, a = k.rsplit(".", 1)
            if a in _OBJ_DERIVED and f"{o}.shape" in d:
                out[k] = tuple(f"{o}.{x}" for x in _OBJ_DERIVED[a])
            elif a in _OBS_PAIR and "~" in o:
                out[k] = tuple(f"{p}.{s}" for p in o.split("~", 1) for s in ("row", "col", "shape"))
        return out

    def _obs_pair_derive(self, state: dict) -> dict[str, int]:
        """E0b: the observer-item-4 pair slots of this frame from a state's readings, each party's
        cells rebuilt as its shape key placed at (row, col) -- the key is the cells less exactly
        that origin (arc_percept 199-203) -- and measured by _relation_slots' own rules. Keys from
        the frame's read, never derived() (_all calls derive before its pair read exists)."""
        cells: dict[str, frozenset | None] = {}

        def cells_of(o: str) -> frozenset | None:
            if o not in cells:
                key = self._shape_key(state.get(f"{o}.shape"))
                r, c = state.get(f"{o}.row"), state.get(f"{o}.col")
                cells[o] = (frozenset((r + dr, c + dc) for dr, dc in key)
                            if key is not None and isinstance(r, int) and isinstance(c, int)
                            else None)
            return cells[o]
        out: dict[str, int] = {}
        for k in getattr(self, "_read", None) or {}:
            cap.head()
            own, a = k.rsplit(".", 1)
            if a not in _OBS_PAIR or "~" not in own:
                continue
            x, y = own.split("~", 1)
            A, B = cells_of(x), cells_of(y)
            if A is None or B is None:
                continue
            if a == "contact":
                out[k] = arc_percept.contact_faces({"cells": A}, {"cells": B})
            elif a == "bbox":
                r = (min(max(p for p, _q in A), max(p for p, _q in B)) + 1
                     - max(min(p for p, _q in A), min(p for p, _q in B)))
                c = (min(max(q for _p, q in A), max(q for _p, q in B)) + 1
                     - max(min(q for _p, q in A), min(q for _p, q in B)))
                out[k] = r * c if r > 0 and c > 0 else 0
            else:
                out[k] = int(bool(B) and B.issubset(arc_percept.enclosed_of(A)))
        return out

    def _shape_key(self, label: Any) -> frozenset | None:
        """The percept's own shape key (the cell set at the origin) for a published label."""
        tab = getattr(self._decompose, "_shapes", None) or {}
        inv = self.__dict__.get("_shape_inv")
        if inv is None or len(inv) != len(tab):
            inv = self._shape_inv = {v: k for k, v in tab.items()}
        return inv.get(label) if isinstance(label, int) else None

    def _obj_derive(self, state: dict, before: dict | None) -> dict[str, int]:
        """E0: the object attributes derived from a state's (and the before-state's) readings,
        by the percept's own rules: h / w are the shape key's extent (arc_percept 202-203), the
        frame deltas are differences of those and of holes_of / perimeter_of / the cell count,
        drow / dcol of row / col (delta_of), speed their larger magnitude, colour_changed the
        colour compared."""
        out: dict[str, int] = {}
        for k, lab in state.items():
            cap.head()
            o, a = k.rsplit(".", 1)
            if a != "shape":
                continue
            key = self._shape_key(lab)
            if key is None:
                continue
            out[f"{o}.h"] = max(r for r, _c in key) + 1
            out[f"{o}.w"] = max(c for _r, c in key) + 1
            if before is None:
                continue
            bkey = self._shape_key(before.get(k))
            if bkey is not None:
                bh, bw = max(r for r, _c in bkey) + 1, max(c for _r, c in bkey) + 1
                out[f"{o}.dh"], out[f"{o}.dw"] = out[f"{o}.h"] - bh, out[f"{o}.w"] - bw
                out[f"{o}.dcells"] = len(key) - len(bkey)
                out[f"{o}.dholes"] = arc_percept.holes_of(key) - arc_percept.holes_of(bkey)
                out[f"{o}.dperimeter"] = (arc_percept.perimeter_of(key)
                                          - arc_percept.perimeter_of(bkey))
            pos = [state.get(f"{o}.row"), state.get(f"{o}.col"),
                   before.get(f"{o}.row"), before.get(f"{o}.col")]
            if all(isinstance(v, int) for v in pos):
                dr, dc = pos[0] - pos[2], pos[1] - pos[3]
                out[f"{o}.drow"], out[f"{o}.dcol"] = dr, dc
                out[f"{o}.speed"] = max(abs(dr), abs(dc))
            c1, c0 = state.get(f"{o}.colour"), before.get(f"{o}.colour")
            if isinstance(c1, int) and isinstance(c0, int):
                out[f"{o}.colour_changed"] = int(c1 != c0)
        return out

    def _all(self) -> dict[str, int]:
        """The frame's read plus its pair slots, computed FROM the read and never inside its
        cache (the tracker advances once per frame). A pair whose party is covered stays, as
        NOT_RESOLVED, like any covered attribute; it leaves when an object does."""
        d = self._decomposed()
        if not _RELATION_SET or not d or self.blind:
            return d
        if self._pair_read is None:
            self._pair_src = {f"{a}.{rel}_{b}": tuple(f"{o}.{k}" for o in (a, b)
                                                        for k in ("row", "col", "h", "w"))
                              for a, b in self._pair_list() for rel in relations.PAIR_RELATIONS}
            got = self.derive(d)
            self._pair_read = {k: got.get(k, sensors.NOT_RESOLVED) for k in self._pair_src}
        return {**d, **self._pair_read}

    def cues(self) -> dict | None:
        """WHAT MUTATED, AND WHICH PRIMITIVES ARE LIT ON EACH OBJECT -- the directed cue.

        `observe()` publishes VALUES; this publishes WHAT CHANGED and WHAT IS FIRING. They are
        different facts and the agent had only the first: it could see that a slot now reads 4,
        never that `position` mutated on two objects while `holes` mutated on none. The mutation
        is what makes a search DIRECTED rather than undirected -- `RELATIONS.md` Part 6.

        DRIVEN ONCE PER FRAME, cached, for `_decomposed`'s reason exactly: the tracker inside
        `Live` is stateful, so two calls in one step would match a frame against itself and
        report every mutation as absent. The frame is what changes, so it keys the cache.

        Returns `None` on a blind frame -- an ABSTENTION, not an empty reading. A blind
        instrument reporting `no mutations` is the confabulation `_decomposed` names one screen
        up, and this reader is no more entitled to it.
        """
        if self._cue is None:
            b = self.board()
            if b is None or self.blind:
                return None
            self._cue = self._obs.see(b)
        return self._cue

    def _take_frame(self, nxt: Any) -> None:
        """The per-frame intake, shared by step() and arrive()."""
        if nxt is not None:
            self._frame = nxt
        self._read = None          # a new frame is a new decomposition
        arc_atoms.new_frame()      # and its shape readings are perceived afresh (F481)
        self._cue = None           # and a new set of mutations to read off it
        self._prev_contacts = self._contacts
        self._contacts = None      # and a new set of contacts
        self._contact_pts = None   # and a new set of typed contact points
        self._pair_read = None     # and a new set of pair relations (ARC B2)

    def arrive(self) -> bool:
        """THE HARNESS SWITCH (the reviewer 2026-10-25 10:47, 11:03, 11:25; Fig 11 :66, :70): a
        frame that came with no action of the agent's -- a new game's first frame, the one its
        wrapper already holds (both ARC wrappers reset in their own __init__). The same intake and
        re-track as step(), and nothing that pairs an action with it: no on_frame, no
        selves.observe, no aff.note, and the own clock reads no action took it. A break the
        tracker reads here waits in frame_breaks() for the agent's next step's head. NEVER a
        reset: a reset here would be the second of two (Isaiah 2026-09-29), so a wrapper holding
        no frame takes nothing and returns False for the harness to record. Only the stream
        harness calls it; nothing names a game."""
        frame = getattr(self.w, "observation_space", None)
        if frame is None:
            return False
        self._take_frame(frame)
        self._decomposed()
        self._own = ({}, 0)
        return True

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
        u0 = getattr(self._decompose, "updates", None)
        nxt = self.w.step(act, data=data) if data is not None else self.w.step(act)
        # AN EMPTY STACK IS "NOTHING RENDERED", NOT "NO BOARD". At GAME_OVER and WIN the engine
        # answers every non-RESET action with `frame=[]` (a bare FrameData, levels unset), so
        # taking it whole left no board, no slots and no action ever again -- short of the RESET
        # the agent may now choose (Isaiah, 2026-09-29). The last frame stands; only the state
        # is the answer's. ONLY in the two states the engine answers this way: an empty stack
        # anywhere else may be a dead channel, and keeps reading as no board (`no_slots`,
        # CHANNEL_CLOSED) rather than as "nothing changed".
        if (nxt is not None and nxt.is_empty() and self._frame is not None
                and nxt.state in (GameState.GAME_OVER, GameState.WIN)
                and not self._frame.is_empty()):
            keep = self._frame.model_copy()
            keep.state = nxt.state
            nxt = keep
        self._take_frame(nxt)
        now = self.board()
        if self.on_frame is not None:
            self.on_frame(was, action, now)
        self._decomposed()          # re-track before reading contact on the new frame
        # OWN CLOCK: the settled objects before this action and how many tracker advances it took
        # (the response's frame count, read, never assumed)
        self._own = (was_objs, (self._decompose.updates - u0) if u0 is not None else 0)
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

    def own_expected(self) -> dict[str, int]:
        """OWN CLOCK (the reviewer 2026-10-17 10:05; the reafference principle, von Holst &
        Mittelstaedt 1950): the slots this perception writes BY ITS OWN RULE, with the value that
        rule gives from the settled readings, formed when the frames arrive. `age` of a continuing
        track = its previous settled age + F, the tracker advances this action took; `stability` =
        its previous settled stability + F if the settled cells and colour are those of the previous
        settled frame, else 0 (so only a mid-cascade change that reverted leaves a residual). None
        at birth, on a covered object, a blind frame, or before the first action. It says what our
        own bookkeeping did, never what the board will do; F stays a reading."""
        was, f = getattr(self, "_own", ({}, 0))
        if f <= 0 or self.blind:
            return {}
        out: dict[str, int] = {}
        for o, obj in self._decompose.tracked.items():
            p = was.get(o)
            if p is None or obj.get("covered") or p.get("covered"):
                continue
            if isinstance(p.get("age"), int) and "age" in obj:
                out[f"{o}.age"] = p["age"] + f
            if isinstance(p.get("stability"), int) and "stability" in obj:
                same = p.get("cells") == obj.get("cells") and p.get("colour") == obj.get("colour")
                out[f"{o}.stability"] = p["stability"] + f if same else 0
        return out

    def own_counted(self) -> frozenset[str]:
        """The slots this perception writes by its own rule (own_expected's age and stability), on
        every tracked object whether or not the rule can predict them this step: counters of our own
        bookkeeping, whose change is a change already read on the object's other slots."""
        tracked = getattr(getattr(self, "_decompose", None), "tracked", None) or {}
        return frozenset(f"{o}.{a}" for o, obj in tracked.items() for a in ("age", "stability")
                         if a in obj)

    def identity(self, obj: str) -> str | None:
        """How `obj` was re-found on the latest frame: "overlap", "unique-shape", "look-alike",
        "birth", or None when it is not tracked. F479 reads it at a restart.

        The rule is `arc_percept.identity_of`, shared with the cell-change readings."""
        return arc_percept.identity_of(obj, getattr(self._decompose, "matches", {}) or {},
                                       getattr(self._decompose, "tracked", {}) or {},
                                       getattr(self._decompose, "refused_identity", ()))

    def refuse_identity(self, obj: str) -> None:
        """Not-identity (F496, R2): `obj` may be two things the tracker took for one. Add-only;
        from now on `identity_of` reads it unsure, so nothing carried by identity trusts it."""
        refused = getattr(self._decompose, "refused_identity", None)
        if refused is not None:
            refused.add(obj)

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
            return ledger.WIN    # the game won (F1b; Isaiah 08:30)
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
