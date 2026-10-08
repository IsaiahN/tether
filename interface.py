"""The action interface — the one layer that knows a button exists.

**ISAIAH, 2026-09-28:** *"The agent shouldn't really care about what action they choose. It
shouldn't factor in their reasoning at all. They reason first, consider all systems, come to a
conclusion, and then coordinate with the interface that translates that into actions."*

**AND IT IS A CONFORMANCE JOB, NOT A NEW DESIGN.** `TRAINING_PLAN:405` (Isaiah, 2026-09-14, *two
rulings, both binding*) already said *ACTIONS MUST NOT BE BAKED IN*, naming the exact trap:
*"the brute-force enumeration baked actions into the composition space (`slot x action ->
slot`)"*. That was written about TRAINING. The live path never obeyed it, and `slot x action ->
slot` is `PREDICT`.

**F28 DREW HALF THIS SEAM ALREADY** -- `arc_world.actions()`: *only the DIRECTIONAL SEMANTICS
must never reach the agent; availability is legitimate to read.* This carries availability
upward AS REASONING, never as a name.

**THE ONE PROHIBITION, AND EVERYTHING HERE IS MEASURED AGAINST IT:** an interface that silently
DECIDES is the encoded answer relocated rather than removed. It may translate and it may report.
**It may not choose between goals, rank intents, or withhold a capability the board advertises.**
Any decision it appears to make is a defect, and `audit()` is what makes that checkable rather
than promised.
"""

from __future__ import annotations

import math
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

sys.dont_write_bytecode = True

# WHAT THE AGENT CAN MEAN. Deliberately NOT an action vocabulary -- these name what the agent
# wants to be true, and the interface is what knows whether this board can express it.
# **SAID IN THE EXISTING PRIMES, NOT IN NEW WORDS -- Isaiah's *"maybe they speak in nsm"*, and
# the reviewer's check of it, 2026-09-28.** `grammar.PRIMES` holds thirteen: ALL BECAUSE BECOME
# BE_AT CAN EXIST NONE NOT ONE OTHER SAME SOME TOUCH. **`TOUCH`, `BE_AT` and `BECOME` were
# already primes and nobody had noticed; `ELICIT` never was.** So the vocabulary had already been
# extended once, silently, by me -- which is exactly what the check was asked to find.
#
# The CONSTANT NAMES stay, because code is read by people; their VALUES are now the prime
# composition, so what the agent SAYS is in the grammar the agent has. `ELICIT` is *let something
# become other than it is* and `DISTINGUISH` is *not the same* -- both sayable, so neither is an
# extension, and no declared extension is needed after all.
ELICIT = "BECOME OTHER"        # get ANY response from this object, or from the board. The bootstrap
TOUCH = "TOUCH"          # bring a onto b
BE_AT = "BE_AT"          # put a at a region
BECOME = "BECOME"        # a takes an attribute
# **THE FOURTH, AND IT IS NOT A FLAVOUR OF `ELICIT` -- `docs/ACTION_INTERFACE_PLAN.md` 17/18.**
# `ELICIT` asks for ANY response and CANNOT FAIL while a button exists. `DISTINGUISH` asks for a
# response that TELLS THE AGENT'S ALTERNATIVES APART, and **abstains when nothing does** -- which
# is the whole reason it is a separate verb. `_learned_split` did two things: it ranked actions
# by separability (the violation) and it ABSTAINED when nothing separated. Everything below it in
# `choose` runs only because of that abstention, so realising it as `ELICIT` would fire every
# time it was reached and starve three exits.
#
# **AND IT IS THE VERB 18 ALREADY REQUIRED**, rather than one invented for this site: the
# reviewer's ruling is that discrimination returns at the INTENT level -- *the agent picks the
# intent whose predicted outcomes differ most across its hypotheses* -- and that needs a verb
# meaning *separate my alternatives*.
DISTINGUISH = "NOT SAME"
# **THE ONE BUTTON THIS MODULE KNOWS BY NAME, AND THIS IS THE RIGHT HOUSE FOR IT.**
# Isaiah, 2026-09-29: *all actions still must live and be controlled by the interface --
# that separation is what makes this possible.* Reset and undo are FULLY UNGATED here; the
# interface picks them by what it knows they do, like any other action. The single hard
# rule is below, at `realise`.
RESET = "RESET"
# What a known action does here, as reported to the agent when nothing is unknown (F480).
CHANGES, NO_EFFECT, RESTARTS = "changes the board", "no effect", "restarts the level"

# **THE POSITIONED ACTION, NAMED HERE AND NOWHERE ABOVE -- the plan's 19c.** The seam's rule is
# that only the interface may know a button exists, so this string belongs in this file and was
# a violation in `tether.py`, where `choose` read `"ACTION6" if "ACTION6" in self.actions` at two
# sites and `step` keyed the coordinate on `action == "ACTION6"`.
#
# **AND IT IS THE SMALLER LIE, NOT NO LIE.** The honest version is LEARNED: an action that
# ACCEPTED a coordinate and moved something is positioned, which is observable, and `audit`
# already sees every press. Written down as unfinished so nobody reads a hardcoded name below
# the seam as the finished state.
POSITIONED: tuple[str, ...] = ("ACTION6",)

# **ATTRIBUTES THAT ARE NOT THE OBJECT'S OWN -- the reviewer, 2026-09-28, and this is DATA
# rather than logic so it can be pinned and moved without touching a rule.** An object's colour
# and shape are ITS OWN; its `proximity` is a fact about it AND SOMETHING ELSE, so it changes
# for everyone whenever anything moves. Keying the actor off relations made every action read
# `o5`.
#
# **OWN-VERSUS-RELATION IS THE LINE, NOT POSITION-VERSUS-EVERYTHING** -- my first fix counted
# only `row`/`col`, and the reviewer's case against it is a world I built the same evening:
# **fixture B's clicks change COLOUR and move nothing, so a position-only rule finds no actor
# there at all.** Recolour and reshape are among the commonest ARC transformations.
#
# **AND NO WORLD DECLARES THIS YET, WHICH IS WHY IT IS A LIST AND NOT A LOOKUP.** Checked:
# `arc_atoms.ATTRIBUTE_TYPE` types `row col colour shape` and omits `proximity` -- but it also
# omits gridworld's `surface` and `obstacle`, which ARE own attributes, so membership cannot
# carry the distinction; and `slot_types()` returns `EXTENT` for everything on gridworld by
# deliberate under-declaration. **The right home is the world declaring which of its attributes
# are relational. Until one does, this is the convention, named and visible.**
RELATIONAL: tuple[str, ...] = ("proximity",)

# **LAYER 1 -- WHICH OBJECT WAS ACTED ON, AS A KIND AND NEVER AS A NAME. Isaiah, 2026-10-01:
# *"clicking one object can act as a button or trigger something elsewhere on the board"*, and
# `F394` measured that the agent could not express that at all.** The delta key held the button
# and the contact configuration; it had no coordinate for the object acted UPON, so *clicking A
# changes A* and *clicking B changes A* were THE SAME CELL. Measured on `click_only`: 60 presses
# at 6 distinct objects collapsed into 6 cells under ONE context, with zero aimed coordinates in
# any key.
#
# THREE VALUES, PERMANENT VOCABULARY, NO CHURN -- which is `context()`'s own *kinds, never names*
# applied to the cause instead of the contact. `acted` is used to COMPUTE the kind and is never
# stored, so no object name enters a key.
SELF, OTHER, NO_TARGET = "self", "other", "no_target"


def _summed(delta: dict, ctx: tuple, slot: str) -> tuple[int, float]:
    """`(n, tot)` for one `(ctx, slot)`, SUMMED OVER EVERY `rel`.

    **THE READERS ASK A COARSER QUESTION THAN THE AUDIT RECORDS, and this is where the two
    meet.** Layer 1 split the delta key three ways; a reader wanting *which way does this
    action move this slot* wants the whole cell back. Summing a partition recovers the
    original exactly, which is why layer 1 costs the realiser nothing -- and the conservation
    check that pairs with this compares these sums against the pre-layer-1 totals.

    A plain `.get((ctx, slot))` here would return the default against a 3-tuple key and read
    ZERO WITHOUT RAISING -- the silent failure this file already records once, at the delta
    loop. That is why the lookup is a named function rather than a dict access.
    """
    n = tot = 0
    for rel in (SELF, OTHER, NO_TARGET):
        a, b = delta.get((ctx, slot, rel), (0, 0))
        n += a
        tot += b
    return n, tot


def _is_relational(slot: str | None, env: object) -> bool:
    """Is this slot's attribute a RELATION TO ANOTHER OBJECT? **Asked of the world.**

    `env.relational_slots()` is the habitat's own declaration, read exactly as the agent
    reads `slot_owner` and for the reason that one gives: *the loop may not derive this
    from the name.* A world that declares nothing has no relational slots, so every world
    that has not been taught the split behaves exactly as before.

    **IT DOES NOT FALL BACK TO `RELATIONAL`.** That tuple is the stopgap this replaces, and
    quietly reading it when the declaration is absent would reintroduce the name dependency
    while appearing to have removed it.
    """
    if not slot:
        return False
    fn = getattr(env, "relational_slots", None)
    if fn is None:
        return False
    try:
        declared = tuple(fn())
    except Exception:
        return False
    return slot.rsplit(".", 1)[-1] in declared


@dataclass(frozen=True)
class Repeat:
    """How many times, until what -- and the gap between them is a residual.

    **ISAIAH, 2026-09-28:** *"upright is subjective and transitory but rotate five times is
    specific."* Both, because they fail in opposite directions. `routine.Until` already carries
    `guard` and `budget`, but `budget` is a SAFETY CAP -- *derived at construction, never
    picked*. **`expect` is what the agent MEANS**, and missing it teaches.

    **A BARE COUNT CANNOT BE SURPRISED. A BARE CONDITION CANNOT BE WRONG ABOUT MAGNITUDE.**
    Not a magic number: the agent emits it from its own model and the world falsifies it.
    """

    guard: Any | None = None
    expect: int | None = None
    budget: int | None = None

    def __post_init__(self) -> None:
        if self.guard is None and self.expect is None:
            raise ValueError("a Repeat with neither a guard nor an expectation says nothing")


@dataclass(frozen=True)
class Intent:
    """What the agent wants to be true. **It names no action and carries no button.**

    Multi-step is a TUPLE of these -- the same emission at a different length, which is
    Isaiah's *"single or multistep plan"*.
    """

    kind: str
    subject: str | None = None
    object: str | None = None
    repeat: Repeat | None = None
    # **A SIGN AND A VALUE ARE TWO QUANTITIES AND THEY DO NOT SHARE A FIELD.** `object` holds
    # `"+"`/`"-"` on an ORDERED slot; `value` holds *make it 3* where no order exists to want a
    # direction in. `A6i` is one name carrying two quantities, and it is free to avoid here and
    # expensive once anything reads the field. `docs/ACTION_INTERFACE_PLAN.md` §15.
    value: int | None = None

    def says(self) -> str:
        core = " ".join(x for x in (self.kind, self.subject, self.object) if x)
        if self.value is not None:
            core = f"{core} = {self.value}"
        if self.repeat is None:
            return core
        bits = []
        if self.repeat.expect is not None:
            bits.append(f"expecting {self.repeat.expect}")
        if self.repeat.guard is not None:
            bits.append("until the guard holds")
        return f"{core} ({', '.join(bits)})"


@dataclass(frozen=True)
class Realisation:
    """What the interface actually did, recorded BESIDE the intent and never inside it.

    **THE REVIEWER, 2026-09-28, and Isaiah's own wording is *"instead OR WITH the action set"*:**
    intent alone leaves `audit()` nothing to check the table against. Intent above the seam,
    realisation below it, both recorded.
    """

    action: str
    coord: tuple[int, int] | None = None
    unmapped: bool = False        # taken to LEARN what it does, not because the table said so
    why: str = ""
    # **THE MODE IS HERE BECAUSE THE SENTENCE CANNOT CARRY IT.** The floor draw and `ELICIT`
    # are THE SAME WANT -- *let something become other than it is* -- and differ only in how
    # the interface picks. A fifth intent would be one sentence under two names, which is the
    # silent vocabulary extension the 2026-09-28 prime check exists to catch. So the
    # distinction lives in the RECORD of what was done, never in what the agent said.
    mode: str = ""                # "undirected" on the floor draw; empty on every other path


@dataclass
class Capability:
    """A change in what the board affords, **stated as reasoning and never as a button.**

    Isaiah: *"the board has enabled us to move to the left or right after doing xyz"*, *"we are
    now no longer able to go that way"*, *"we are now able to click freely around the board on
    any object"*. **Systems 0, 1 and 2 learn that something opened without being told what it
    is** -- which is F28's line held: availability crosses, semantics does not.
    """

    opened: tuple[str, ...] = ()
    closed: tuple[str, ...] = ()

    def moved(self) -> bool:
        return bool(self.opened or self.closed)


@dataclass
class Preconditions:
    """§16.8 sensor 2: pairwise `a became available after b`, with counts.

    An action appearing is a CONDITION MET, and the action just taken is the only candidate
    for having met it. This counts the pairs and nothing else -- it does not rank them, name
    a cause, or gate anything. **A count is not a claim**: `b` preceding `a` many times is
    evidence the agent can read, and reading it is the agent's job rather than this table's.

    Cheap by construction: at most |actions| squared cells, 49 for ARC's seven.
    """

    after: Counter = field(default_factory=Counter)
    gone_after: Counter = field(default_factory=Counter)
    # THE DENOMINATOR, AND WITHOUT IT `after` CANNOT SAY WHETHER AN EDGE IS A RULE. `b -> a`
    # seen four times is four out of four or four out of ninety, and only the second is a
    # condition. It counts every step, not only the steps where the set changed, which is why
    # `note` is now called unconditionally.
    taken: Counter = field(default_factory=Counter)

    def note(self, prev: str | None, came: list[str], gone: list[str]) -> None:
        if prev is None:
            return                      # nothing preceded the first frame
        self.taken[prev] += 1
        for a in came:
            self.after[(prev, a)] += 1
        for a in gone:
            self.gone_after[(prev, a)] += 1

    def report(self) -> dict:
        return {"came_after": {f"{b}->{a}": n for (b, a), n in sorted(self.after.items())},
                "gone_after": {f"{b}->{a}": n for (b, a), n in sorted(self.gone_after.items())},
                "taken": dict(sorted(self.taken.items())),
                # CONDITIONAL, AS TWO COUNTS RATHER THAN A VERDICT. An edge that fires on
                # EVERY `b` is a rule; one that fires on SOME is gated by something else --
                # which is the fifth topology, and it is a reading over the denominator
                # rather than an instrument of its own.
                "sometimes": {f"{b}->{a}": [n, self.taken[b]]
                              for (b, a), n in sorted(self.after.items())
                              if 0 < n < self.taken[b]},
                "reads": ("counts, not claims: what followed what, out of how many. "
                          "`sometimes` is an edge that did not fire every time its "
                          "predecessor was taken -- the same action, a different outcome")}


class Interface:
    """Translates intent down, reports capability up. **Knows nothing about goals.**

    It holds one table: what each action has been OBSERVED to do, keyed by the action and built
    only from what `audit()` saw. **Nothing is closed over at construction** -- which is the
    defect `tether.py:2876` names in the toy world's `act` atom, where *"the primitive it was
    given already knew"* and discriminate became a property of the atom set rather than a model
    the agent built. **This table starts empty on every board and is filled only by acting.**
    """

    def __init__(self) -> None:
        self.pre = Preconditions()       # section 16.8 sensor 2; below the seam since 2026-10-05
        # THE AGENT'S CHOICE WHEN NOTHING IS UNKNOWN HERE (F480): handed the KNOWN effects, never
        # the buttons, it returns an index and its reason. None = no agent attached.
        self.chooser: Any = None
        self.table: dict[str, dict] = {}       # action -> what it was observed to do
        # `probe.Drive`'s seed, which is `crc32(b"") & 0xFFFF == 0` at both construction sites
        # in `tether`. Held here so the moved sweep is byte-identical rather than merely alike.
        self._draw_seed = 0
        self._seen: tuple[str, ...] = ()       # last frame's advertised set, for capability
        self.audits = 0
        # slot -> how many audited presses it was PRESENT for. See `audit`.
        self.present: dict[str, int] = {}
        self.conditional: set[str] = set()     # more than one effect, ACROSS contexts
        self.changed: set[str] = set()         # more than one effect WITHIN one context
        self.unreliable: set[str] = set()      # lands a slot on more than one value in a ctx
        # THE CONTINGENCY INSTRUMENTS, MOVED WITH THE COMPUTATION. `Agent.members()` published
        # these and its numbers are the reason the gates below are trusted, so leaving them
        # behind would have made the relocation unreadable at exactly the moment it needs
        # reading. **The agent still REPORTS them; it no longer computes them.**
        self.member_gates: Counter = Counter()   # "<member>:no_coverage" / ":unstable" / ":passed"
        self.sep_passes: Counter = Counter()     # how many members contributed, per call
        self.sep_log: list = []
        # WHERE A POSITIONED ACTION HAS ALREADY LANDED. Filled by `audit` from the coordinates
        # this interface itself aimed, so *unclicked* means *I have not tried there*, never
        # *the board says nothing is there*.
        self.clicked: set[tuple[int, int]] = set()
        # WHAT KINDS HAVE BEEN PRESSED -- an object's perceived (shape, colour). The walk
        # presses one of each kind before a second of any (Fig 5: seek the gap that is large
        # and compressible; the reviewer 2026-10-08 05:55Z). An order, never a filter.
        self.pressed_kinds: set[tuple] = set()
        self.new_kind = False
        # **LAYER 1's OTHER HALF -- INSTANCE MEMORY, AND IT IS DELIBERATELY NOT A KEY.**
        # `rel` says WHETHER acting on one object changes another in this world; it cannot say
        # WHICH object to press to move slot Y. That question is answered by what this agent
        # has actually observed on THIS board: aimed here -> these slots moved.
        #
        # A RECORDING, NOT A METHOD, so it must not cross: never persisted, never in a term,
        # never in a delta key, never in a handle. It is `clicked` with effects attached and it
        # has exactly `clicked`'s lifetime -- a coordinate is only a referent while the board
        # holds still.
        self.aimed_effect: dict[tuple[int, int], set[str]] = {}
        # **EVERY ATTRIBUTE THE ACTOR CODE HAS EVER JUDGED, so `RELATIONAL` cannot silently
        # miss one -- the reviewer, 2026-09-28.** That list is short, so anything not on it
        # counts as the object's OWN by default, and a new relational attribute (`contact`,
        # `adjacency`, `distance`) would quietly cast an actor vote. **Recorded rather than
        # guarded**: the guard would need the taxonomy the list is standing in for, and this
        # puts the unlisted name in the record where a reader meets it.
        self.attrs_seen: set[str] = set()

        # **SET FROM `audit`, NEVER FROM `realise`.** `realise` is called speculatively at
        # several branches and most of those results are discarded, so a flag set there
        # would count presses that never happened. `audit` sees what ACTUALLY ran.
        self._last_was_reset = False

    # ---- downward: intent -> action --------------------------------------------------

    def realise(self, intent: Intent, offered: tuple[str, ...], ctx: tuple = (),
                state: dict | None = None, env: Any = None) -> Realisation | None:
        """**THE ONE DOOR, SO NO EXIT CAN SEND A SECOND CONSECUTIVE `RESET`.**

        **ISAIAH, 2026-09-29, AND IT IS A HARD CONSTRAINT RATHER THAN A PREFERENCE:** *fully
        ungated undo and reset, just no consecutive resets (reset, reset) in interface.* One
        `RESET` restarts the LEVEL; a second with no action between restarts the GAME FROM
        LEVEL 1, so the pair is the one thing named as able to lose the run.

        **NOT A WHITELIST.** An earlier draft of mine proposed serving reset only for a
        *go back* intent and never for `ELICIT` -- **overruled, and rightly**: gating by intent
        is the interface deciding what the agent may mean. The control is KNOWLEDGE of what
        each action does, plus this one adjacency rule.

        **IT RE-CHOOSES BEFORE IT ABSTAINS.** Barred from `RESET`, it asks the same question of
        the same intent with `RESET` withheld -- *choose something else, or abstain; never send
        it.* An abstention here is still a reading, as everywhere else in this module.

        **AND THIS GUARD'S SAFETY RESTS ON AN ABSENCE, WHICH IS WRITTEN HERE BECAUSE A READER OF
        THE GUARD IS WHO NEEDS TO KNOW IT.** The flag is set from `audit`, so it sees resets
        THIS module issued. A reset reaching the board by any other route is invisible to it,
        and the next choice could then be a second adjacent `RESET` -- the full-game restart.

        **Checked 2026-09-29: no such route exists today.** `arc_world` has NO `restart()`; one
        was built and removed the same day, its own comment calling a method there *a trapdoor
        to the version that does*, and `terminal()` only REPORTS a game over. The two resets
        that do bypass `audit` are benign -- construction and the bench, both at level 1 with
        no agent in the run.

        > **SO THE GUARD IS SAFE BECAUSE NOBODY HAS RE-ADDED `restart()`.** That is a guarantee
        > by absence, and this record distrusts those. **The robust fix is to set the flag from
        > THE FRAME THE PLATFORM RETURNS on any reset**, not only from this module's own
        > realisations. **HELD, NOT FORGOTTEN** -- the reviewer, 2026-09-29: it lands on the ARC
        > path, which the board stop makes unrunnable, and shipping an unexercised change to the
        > one mechanism that can lose a run is worse than carrying a named dependency.
        """
        r = self._choose(intent, offered, ctx, state, env)
        if r is not None and r.action == RESET and self._last_was_reset:
            _alt = tuple(a for a in offered if a != RESET)
            r = self._choose(intent, _alt, ctx, state, env) if _alt else None
        return r

    def _choose(self, intent: Intent, offered: tuple[str, ...], ctx: tuple = (),
                state: dict | None = None, env: Any = None) -> Realisation | None:
        """Pick an action that serves this intent, or abstain.

        **ABSTENTION IS A READING** -- §12.2. `None` means *this board's vocabulary cannot
        express that*, and the agent is entitled to know its intent was unrealisable rather
        than silently receiving something else.

        **THE BOOTSTRAP STAYS ABOVE THE SEAM.** On a new board the table is empty, so nothing
        can be translated from knowledge -- and an interface inventing exploratory presses would
        be this module's one prohibition on turn one. So the DECISION to explore is the agent's:
        it emits `ELICIT`, and only then does the interface try what it has not mapped.

        **AND THE VARIETY RULE -- THE REVIEWER, 2026-09-28, AND IT IS WHY THIS IS NOT JUST
        INFORMATIVENESS.** `discriminate:learned` pressed `ACTION2` 105 of 150 times on `ls20`:
        *the collapse System 0 exists to prevent*. If `ELICIT` were realised by "the most
        informative action" alone, **the same scoring keeps choosing one button and the collapse
        rides below the seam wearing the word exploration.** So: **never realise `ELICIT` with
        an action already known to do the same thing in this context.** Unmapped first, then
        anything whose effect here is not yet known, and only then a repeat.
        """
        if not offered:
            return None

        if intent.kind == BECOME and intent.subject and intent.value is not None:
            # **THE UNORDERED HALF -- `objective_step`'s COMPARABLE arm, which had no home below
            # the seam until now.** A sign says nothing on a slot with no order, so the question
            # is not *which way* but *what has this action been observed to LEAVE it at*.
            #
            # **IT SAYS `THIS HAS HAPPENED`, NEVER `THIS WILL`.** An action whose cell holds more
            # than one value has not been shown to reach any of them reliably -- that is §15c's
            # refutation, and it is REFUSED here rather than averaged away, because serving a
            # once-observed landing as a capability is the superstition the table exists to not
            # be.
            #
            # **THE CELL IS ASKED FROM WHERE THE SLOT ACTUALLY IS.** With `before` in the key
            # the question is not *what does this action produce* but *what does it produce FROM
            # HERE* -- which is the only form a cycle can answer. Without a reading of the
            # current state there is no cell to look in, and guessing one would be the interface
            # choosing.
            if state is None or intent.subject not in state:
                return None
            _now = int(state[intent.subject])
            # TWO PASSES, NOT ONE WITH A TIEBREAK -- same shape as the signed half below: this
            # context's evidence wherever it exists, and only then the across-context prior.
            # Written as two loops because one loop with a `best is None` guard makes the
            # answer depend on the order `offered` arrives in, which is the board's and not a
            # thing to build a preference out of.
            best, how = None, ""
            for a in offered:
                here = self.table.get(a, {}).get("lands", {}).get(
                    (ctx, intent.subject, _now))
                if here and set(here) == {intent.value}:
                    best, how = a, "here"
                    break
            # **TIER 2 IS FOR POSITIONAL SLOTS ONLY -- the reviewer, 2026-10-01, on the
            # measurement at `INDEX:51470`: proximity falls 95.8% -> 60.4% across contexts
            # while row and col hold 100%, and ALL 63 tier-2 misses are proximity.**
            #
            # For a coordinate, *the same before-value in another context* IS the same
            # situation. For a relation it is not: **closeness depends on what else is on
            # the board**, so a reading taken elsewhere is a reading of a different board.
            #
            # **THE KIND COMES FROM THE WORLD, NEVER FROM THE NAME.** `env.relational_slots()`
            # is declared by the habitat exactly as `slot_owner` is, and for the same stated
            # reason. `RELATIONAL` above is the older name-tuple stopgap whose own comment
            # asks for this -- *until a world declares the split itself* -- and it holds only
            # `proximity`: measured on seed 11, `distance` carries 86 of the 124 cross-context
            # relational predictions, so a guard on the tuple would have missed most of them.
            #
            # **THE FALLTHROUGH IS NO PREDICTION, AND THAT IS THE POINT RATHER THAN A GAP.**
            # A relational slot with no tier-1 entry says NOTHING; it does not drop to tier 2.
            # Abstaining beats being wrong two times in five, because a wrong prediction that
            # CHANGES a choice is worse than no prediction that leaves the default.
            if best is None and not _is_relational(intent.subject, env):
                for a in offered:
                    lands = self.table.get(a, {}).get("lands", {})
                    seen = {v for (_c, k, b), vs in lands.items()
                            if k == intent.subject and b == _now for v in vs}
                    if seen == {intent.value}:
                        best, how = a, "in every context seen"
                        break
            if best is None:
                return None
            return Realisation(best, why=f"observed to take {intent.subject} from {_now} to "
                                         f"{intent.value}, and to nothing else, {how}")
        if intent.kind == BECOME and intent.subject:
            # **THE AGENT SAID WHICH SLOT AND WHICH WAY. The interface knows which action did
            # that here, because it watched.** `intent.object` is the desired sign: +1 up,
            # -1 down. Abstain when nothing observed moves it -- an unrealisable intent is a
            # reading the agent is entitled to, not a substitution.
            want_sign = 1 if (intent.object or "+") == "+" else -1
            best, score, how = None, 0.0, ""
            for a in offered:
                d = self.table.get(a, {}).get("delta", {})
                # **THIS CONTEXT FIRST, THEN ACROSS ALL OF THEM -- AND THE FALLBACK IS THE
                # POINT.** Measured 2026-09-28: the interface learned `down -> o0.row +1.00`,
                # `up -> -1.00`, `left -> o0.col -1.00`, `right -> +1.00` -- a correct action
                # model from acting alone -- and then ABSTAINED on every `BECOME`, because the
                # query context had never been seen. **The cells were populated and the key was
                # too fine.**
                #
                # **THE AUDIT AND THE REALISER WANT DIFFERENT KEYS AND I HAD GIVEN THEM ONE.**
                # The audit NEEDS the context (without it, *conditional* and *the mapping
                # changed* are one thing -- the reviewer's 13:16). The realiser is STARVED by
                # it. So: same-context evidence when it exists, the across-context prior
                # otherwise. **Being wrong about the prior is a residual, not a fault**, and
                # widening the AUDIT's key instead would have traded away the separation that
                # stopped gridworld crying wolf.
                # SUMMED ACROSS `rel`, AND THAT IS NOT A CONVENIENCE. This asks *which way
                # does this action move this slot* -- a question about the SLOT, never about
                # whether the mover was the object acted on. Aggregating the layer-1 partition
                # back together recovers exactly the pre-layer-1 totals, so the realiser's
                # evidence is unchanged BY CONSTRUCTION rather than by hope. The comment above
                # records that this reader is the one starved by a finer key; it is not
                # starved by this one.
                n, tot = _summed(d, ctx, intent.subject)
                where = "here"
                # **THE SECOND TIER-2 SITE, AND THE ONE THE AGENT ACTUALLY TRAVELS.** The
                # `lands` branch above answers "which action lands this slot on that exact
                # value"; THIS one answers "which way does it move, and by how much", and it
                # is what `expected_move` returns -- the per-press step a routine's length is
                # computed from. **Measured: guarding only the `lands` branch left the
                # before/after reading BYTE-IDENTICAL**, 56/38/30 cross-context claims
                # unchanged, because none of that traffic goes through `lands` at all.
                #
                # Same rule, same reason: a MEAN DELTA pooled over other contexts is a mean
                # over other boards when the slot is a relation, because closeness depends
                # on what else is there. A relational slot takes its exact-cell reading or
                # says nothing.
                if not n and not _is_relational(intent.subject, env):
                    # `(ctx, slot, rel)` since layer 1 -- indexed, not unpacked. THIS IS THE
                    # SITE MY OWN DEPENDENCY MAP MISSED: I grepped for the unpack shapes I
                    # expected and this one is spelled differently, so the published map said
                    # five consumers and there were six. The `shipped` seat found it.
                    n = sum(v[0] for key, v in d.items() if key[1] == intent.subject)
                    tot = sum(v[1] for key, v in d.items() if key[1] == intent.subject)
                    where = "in every context seen"
                if not n:
                    continue
                mean = tot / n
                if mean * want_sign > score:
                    best, score, how = a, mean * want_sign, where
            if best is None:
                return None
            return Realisation(best, why=f"observed to move {intent.subject} that way {how}")
        if intent.kind == TOUCH and intent.object:
            # **BRING ME INTO CONTACT WITH `object`. The agent does not say how, and that
            # indifference IS the seam -- the plan's 19.** Two routes and an abstention; the
            # agent learns which only as *what changed*, never as *which button*.
            #
            # ROUTE 1, THE POSITIONED ACTION. `F28` permits reading availability; what it
            # forbids is the directional semantics reaching the agent. The coordinate comes
            # from PERCEPTION -- the target's own row/col -- and rides back in the
            # `Realisation`, which has always had the field and which `perceive` already
            # accepts. `step` was recomputing it from the button's name instead.
            here = self._at(intent.object, state)
            pos = [a for a in offered if a in POSITIONED]
            if pos and here is not None:
                return Realisation(pos[0], coord=here,
                                   why=f"a positioned action, aimed at {intent.object} "
                                       f"where it is")
            # ROUTE 2, MOVE WHATEVER I CAN MOVE TOWARD IT -- **and there is no `_avatar()` in
            # it, which is the whole of Isaiah's *"it shouldn't matter if there is an avatar"*.**
            # `_toward` above the seam asked *which way does the AVATAR go*; this asks *which
            # action have I seen move ANY position slot the way the gap points*, which is the
            # delta table answering a question it already holds.
            best, gain, why = None, 0.0, ""
            for a in offered:
                # `(ctx, slot, rel)` since layer 1. This scan reads the SLOT and ignores both
                # the context and the relation, so it widens by index rather than aggregating.
                for (_c, k, _rel), (n, tot) in self.table.get(a, {}).get("delta", {}).items():
                    step = self._gap(k, intent.object, state)
                    if step is None or not n:
                        continue
                    mean = tot / n
                    if mean * step <= 0:
                        continue            # this action moves it the wrong way, or not at all
                    got = min(abs(mean), abs(step))
                    if got > gain:
                        best, gain, why = a, got, f"{k} toward {intent.object} by {mean:+.2f}"
            if best is not None:
                return Realisation(best, why=f"observed to move {why}")
            # NEITHER ROUTE. **An unreachable contact is a reading the agent is entitled to**,
            # and substituting a draw here would be the interface deciding to explore on the
            # agent's behalf while wearing the word contact.
            return None
        if intent.kind not in (ELICIT, DISTINGUISH):
            # WITHOUT A TABLE ENTRY THERE IS NOTHING HONEST TO PICK, and guessing would be the
            # interface deciding. It abstains and the agent learns the intent was unrealisable.
            return None
        rank: dict[str, int] = {}
        if intent.kind == DISTINGUISH:
            rank = self.separability(env, offered)
            # **THE ABSTENTION IS THE POINT OF THE VERB.** No member separates anything here, so
            # there is no action to offer that answers what was asked. Returning SOMETHING would
            # turn *tell my alternatives apart* into *press a button*, which is the downgrade
            # from discrimination to exploration the reviewer refused for `spread`.
            if not rank or max(rank.values()) == min(rank.values()):
                return None
        unmapped = [a for a in offered if a not in self.table]
        # **VARIETY IS THE CONSTRAINT AND SEPARABILITY IS A RANKING INSIDE IT -- 17c.** The
        # bands below are unchanged and still decide WHICH SET may be drawn from; `rank` only
        # orders within whichever band was already selected, and is empty for `ELICIT`. **A
        # score can always be maximised by one button; a constraint on repetition cannot be**,
        # which is what stops `learned`'s collapse (`ACTION2`, 105 of 150 on `ls20`) travelling
        # below the seam wearing the word exploration.
        def _pick(band: list[str]) -> str:
            return max(band, key=lambda a: (rank.get(a, 0), -band.index(a)))

        def _made(a: str, why: str) -> Realisation:
            """**A POSITIONED ACTION IS ALWAYS AIMED, WHATEVER THE INTENT ASKED FOR.**

            Fixture B caught this: on a world whose only action is a positioned click, `ELICIT`
            returned it UNAIMED and the step was a guaranteed no-op -- **24 steps, zero
            contact.** The interface knows which actions are positioned; handing back a press
            it knows will do nothing is it failing at its one job. *An exploration that cannot
            produce an observation is not an exploration.*

            **AT AN UNCLICKED OBJECT -- the reviewer, 2026-09-28, per Isaiah's *"clicking on
            things"*.** Not an arbitrary cell: a cell with nothing in it teaches nothing on a
            board where clicking acts on objects. **This is a choice about the BUTTON'S
            PARAMETER and needs nothing from above the seam** -- the agent asked to explore and
            did not say where, because where is not its business.
            """
            # **LAYER 1 AT THE AIM, AND THIS IS WHERE `rel` BECOMES BEHAVIOUR.** Before this,
            # the aim was pure exploration: a cell nobody had clicked, `None` once they all
            # had. An agent that WANTS a slot moved could not press the thing that moves it.
            #
            # TWO HALVES, AND NEITHER DOES THE OTHER'S JOB. `rel` is asked first -- has acting
            # on one object EVER changed another in this world? -- and only if it has is the
            # instance record consulted for WHICH coordinate. In a world where every effect is
            # SELF, hunting for a button is wasted presses and the sweep is right.
            coord = (self._aim_for(intent, state) if a in POSITIONED else None)
            if coord is None and a in POSITIONED:
                coord = self._unclicked(state)
                if coord is not None:
                    why = (f"{why}, aimed where nothing has been clicked"
                           f"{', at a kind not yet pressed' if self.new_kind else ''}")
                else:
                    # CLAUSE 3. Every object has been clicked once, so there is nothing
                    # UNCLICKED left -- but a positioned press with no coordinate is a
                    # guaranteed no-op, and handing one back is the interface failing at
                    # its one job. Uninformed, and it still lands.
                    coord = self._any_object(state)
                    if coord is not None:
                        why = f"{why}, uninformed draw over the objects present"
            elif coord is not None:
                why = f"{why}, aimed at what moves this slot"
            return Realisation(a, coord=coord, unmapped=(a not in self.table), why=why)

        asked = "exploration" if intent.kind == ELICIT else "something that separates"
        unmapped = [a for a in offered if a not in self.table]
        if unmapped:
            return _made(_pick(unmapped), f"requested {asked}: never taken")
        # THE VARIETY CONDITION: prefer an action whose effect IN THIS CONTEXT is unknown.
        fresh = [a for a in offered if ctx not in self.table[a]["by_ctx"]]
        # A POSITIONED ACTION IS NOT KNOWN HERE WHILE AN OBJECT IS UNPRESSED -- the verdict carries
        # its closure (Fig 13; the reviewer 2026-10-08 02:30Z). Its effect is recorded per context,
        # not per target, so one press filed "no effect" for every object, and ft09 said
        # "nothing unknown here" while objects it had never pressed remained.
        fresh += [a for a in offered if a in POSITIONED and a not in fresh
                  and self._unclicked(state) is not None]
        if fresh:
            return _made(_pick(fresh), f"requested {asked}: effect here not yet known")
        # everything mapped in this context. Take the one taken LEAST here -- still the agent's
        # call to explore, and refusing would be the interface overruling it.
        seen = {a: len(self.table[a]["by_ctx"].get(ctx, ())) for a in offered}
        # **DESIGN A -- the reviewer, 2026-10-06 (F480).** For ELICIT, least-seen among KNOWN
        # effects was curiosity with no target (Fig 5) and an unpriced cost (Fig 12), decided
        # here. So the interface REPORTS what each action is known to do here and the AGENT
        # prices and chooses; nothing is refused and nothing is pressed for it.
        if intent.kind == ELICIT and self.chooser is not None:
            known = [(self._known_effect(a, ctx), seen[a]) for a in offered]
            i, why = self.chooser(known)
            return _made(offered[i], f"requested {asked}: nothing unknown here; {why}")
        fewest = min(seen.values())
        band = [a for a in offered if seen[a] == fewest]
        return _made(_pick(band), f"requested {asked}: all known here, least-seen taken")


    def _known_effect(self, a: str, ctx: tuple) -> str:
        """What `a` is KNOWN to do in this context, as a kind the agent can price. RESET's is the
        platform's documented consequence, inherited like ACTION6 taking a position."""
        if a == RESET:
            return RESTARTS
        sigs = self.table.get(a, {}).get("by_ctx", {}).get(ctx, ())
        return CHANGES if any(sigs) else NO_EFFECT

    # ---- upward: what changed, in reasoning terms -------------------------------------

    def moved_slots(self) -> set[str]:
        """Every SLOT ever observed to move under any action. Slots, never actions.

        **THE ACCESSOR EXISTS SO THE ACTION KEY IS UNREACHABLE RATHER THAN MERELY UNREAD.**
        `tether` computed this by reaching into `self.table` -- `{k[1] for e in table.values()
        for k in e["delta"]}` -- which is the interface's INTERNALS, and the reviewer names
        that as a leak shape in its own right even when the content is clean. It was clean:
        the delta key is `(ctx, slot, rel)` so `k[1]` is a slot, and `.values()` discarded the
        action on purpose. **But nothing stopped a later edit taking `k[0]`, or iterating
        `.items()` and getting the action, and no check would have noticed.**

        **IT HAS NEVER RUN.** Its one caller sits behind `_DOWNRATE`, parked OFF by Isaiah
        2026-10-01 until ARC-style boards -- so this is a no-op today and the route is correct
        for the day the park lifts, which is the only day it would have mattered.
        """
        return {key[1] for entry in self.table.values() for key in entry.get("delta", {})}

    def undirected(self, offered: tuple[str, ...], cycle: int) -> Realisation | None:
        """THE FLOOR DRAW, MOVED BELOW THE SEAM. The agent asks for *something, no preference*;
        which button serves it is the interface's business and never the agent's.

        **THE FORMULA IS `probe.Drive.choose`'s, UNCHANGED, AND THAT IS THE POINT.** It is NOT
        a uniform random draw -- it is a DETERMINISTIC COPRIME-STRIDE SWEEP, and the
        reproducibility is load-bearing (*no wall clock, no RNG state*). Replacing it with a
        uniform draw would have had the same long-run frequencies and a different ORDER, which
        is why the pre-registered frequency test could not have caught the substitution.

        **S6 TRAVELS WITH IT:** the stride must be COPRIME to the action count or the sweep is
        not a sweep -- a fixed 7 against seven advertised actions returns the same action every
        cycle for the whole run, silently.

        Returns `None` on an empty offer rather than raising: nothing to draw from is a reading,
        not an error.
        """
        if not offered:
            return None
        stride = next(k for k in range(7, 7 + len(offered))
                      if math.gcd(k, len(offered)) == 1)
        pick = sorted(offered)[(cycle * stride + self._draw_seed) % len(offered)]
        return Realisation(action=pick, mode="undirected", why="undirected")

    def capability(self, offered: tuple[str, ...], after: str | None = None) -> Capability:
        """What the board opened or closed since the last frame, **named as affordance.**

        The names here are the interface's own words for what became possible, and they are
        deliberately not the action identifiers -- `F28`'s line: availability is legitimate to
        read, directional semantics never.
        """
        was, now = set(self._seen), set(offered)
        self._seen = offered
        # SECTION 16.8 SENSOR 2 LIVES HERE: which ACTION preceded a change in what is offered is
        # action identity, the interface's business. Noted on every call, no-change ones too,
        # because the denominator is how often the predecessor was taken.
        self.pre.note(after, sorted(now - was) if was else [], sorted(was - now) if was else [])
        if not was:
            return Capability()            # the first frame opens everything; that is not news
        opened = tuple("a way to act that was not there before" for _ in (now - was))
        closed = tuple("a way to act that is gone" for _ in (was - now))
        return Capability(opened=opened, closed=closed)

    @staticmethod
    def _at(obj: str, state: dict | None) -> tuple[int, int] | None:
        """Where `obj` is, as `(x=col, y=row)`. **`_action6_coord` moved, not rewritten.**

        `F28`: the coordinate is chosen from PERCEPTION -- the object's own perceived row/col --
        and `None` where it has no position slots, so a positioned action stays unpositioned
        rather than being aimed at nothing.

        **THE `.row`/`.col` CONVENTION IS PARSED HERE RATHER THAN IN THE LOOP, WHICH IS WHERE IT
        BELONGS.** `slot_types` says the loop may not split a slot name because that is reading
        domain structure -- and `tether._action6_coord` was doing exactly that, above the seam.
        Below it, knowing how this domain spells a position is the job.
        """
        if not obj or state is None:
            return None
        col, row = state.get(f"{obj}.col"), state.get(f"{obj}.row")
        if col is None or row is None:
            return None
        return int(col), int(row)

    @staticmethod
    def _acted(coord: tuple[int, int] | None, state: dict | None) -> str | None:
        """Which object is AT `coord` -- `_at`'s inverse, and here for the same reason.

        Knowing how this domain spells a position is the interface's job, so the `.row`/`.col`
        parse stays below the seam rather than being repeated by a caller.

        `None` when the action was not aimed, or was aimed where no object is -- and those two
        are the same answer on purpose: in both cases there is no object to attribute the cause
        to, and inventing one would be a guess.
        """
        if coord is None or state is None:
            return None
        rows = {k.rsplit(".", 1)[0] for k in state if k.endswith(".row")}
        for obj in sorted(rows & {k.rsplit(".", 1)[0] for k in state if k.endswith(".col")}):
            if Interface._at(obj, state) == (int(coord[0]), int(coord[1])):
                return obj
        return None

    def _remote_seen(self) -> bool:
        """Has acting on one object EVER changed another, in this world? **The `rel` gate.**

        Read off the delta key, which is where layer 1 put it -- a general fact about the
        world (*remote causation happens here*) rather than about any object, so it is the
        half that would cross if anything did.

        **IT IS A PREDICATE AND NOT A RATE.** One observed OTHER is enough: *it can happen*
        is an existence claim, and a threshold would be a number nobody chose.
        """
        return any(k[2] == OTHER
                   for e in self.table.values() for k in e.get("delta", {}) if len(k) > 2)

    def _aim_for(self, intent: Intent, state: dict | None) -> tuple[int, int] | None:
        """Where to press to move the slot this intent is about. `None` when there is no
        evidence, so the caller falls back to the exploratory sweep.

        **GATED ON `rel` FIRST.** Without an OTHER anywhere in this world, the instance record
        can only ever name the slot's own object, which the sweep reaches anyway -- so
        consulting it buys nothing and the gate keeps the exploratory default.

        **AND THE RECORD IS CONSULTED FOR *WHICH*, NEVER FOR *WHETHER*.** That split is the
        whole design: `rel` transfers and the coordinates do not.
        """
        slot = getattr(intent, "subject", None)
        if not slot or state is None or not self._remote_seen():
            return None
        # The agent's own observations, most-specific first: a coordinate whose presses have
        # moved exactly this slot. Ties broken by fewest side effects -- a press that moves
        # one thing is better evidence about that thing than a press that moves five.
        best = [c for c, slots in self.aimed_effect.items() if slot in slots]
        if not best:
            return None
        return min(best, key=lambda c: (len(self.aimed_effect[c]), c))

    def _any_object(self, state: dict | None) -> tuple[int, int] | None:
        """CLAUSE 3: an UNINFORMED press that is still a real press -- the reviewer,
        2026-10-01. `None` only when the board shows no positioned object at all.

        `_unclicked` goes `None` the moment every object has been aimed at once, and after
        that every positioned press went out with no coordinate. `_click` returns early on a
        `None` coordinate, so those presses were GUARANTEED no-ops: `F403` measured the agent
        bored on ~88% of reads on `click_only` seeds 1-2, taking the uninformed branch 51 of
        60 cycles and never reaching the aimed exit again after cycle 8.

        **UNINFORMED IS PRESERVED AND IT IS THE WHOLE CONSTRAINT.** The draw reads only WHICH
        OBJECTS ARE PRESENT -- never the delta table, never `aimed_effect`, never a slot's
        value, never V. *A probe chosen by the current model can only confirm the current
        model*, and nothing here is chosen by it. What changes is that the press LANDS.

        **ROUND-ROBIN RATHER THAN AN RNG, and the file's own reason.** `drive.choose` is
        "deterministic in the cycle so a run is reproducible; no wall clock, no RNG state".
        Uniform over the objects present and not model-chosen is the property the safety
        argument needs; reproducibility is free, so it is taken.
        """
        if state is None:
            return None
        rows = {k.rsplit(".", 1)[0] for k in state if k.endswith(".row")}
        cols = {k.rsplit(".", 1)[0] for k in state if k.endswith(".col")}
        here = [at for obj in sorted(rows & cols)
                if (at := self._at(obj, state)) is not None]
        if not here:
            return None
        self._rr = getattr(self, "_rr", 0) + 1
        return here[self._rr % len(here)]

    def _unclicked(self, state: dict | None) -> tuple[int, int] | None:
        """An OBJECT this interface has not aimed at yet, as `(x=col, y=row)`.

        Objects are the things with both a row and a col -- the same convention `_at` reads,
        parsed here rather than in the loop because knowing how this domain spells a position
        is the interface's job. `None` when every object has been clicked or none has a
        position, and **`None` means the press goes out unaimed rather than aimed at a guess.**
        """
        if state is None:
            return None
        rows = {k.rsplit(".", 1)[0] for k in state if k.endswith(".row")}
        cols = {k.rsplit(".", 1)[0] for k in state if k.endswith(".col")}
        open_ = [(obj, at) for obj in sorted(rows & cols)
                 if (at := self._at(obj, state)) is not None and at not in self.clicked]
        fresh = [at for obj, at in open_ if self._kind(obj, state) not in self.pressed_kinds]
        self.new_kind = bool(fresh)
        return (fresh or [at for _obj, at in open_] or [None])[0]

    @staticmethod
    def _kind(obj: str, state: dict) -> tuple:
        """An object's perceived kind: its shape and colour readings, nothing named."""
        return (state.get(f"{obj}.shape"), state.get(f"{obj}.colour"))

    @staticmethod
    def _gap(slot: str, target: str, state: dict | None) -> int | None:
        """How far `slot` is from its counterpart on `target`, signed. `None` if not comparable.

        Pairs a position slot with the SAME attribute on the target -- `o3.row` against
        `o7.row` -- so *reduce the distance* is well defined without anything being an avatar.
        Refuses the target's own slots: moving a thing cannot be approaching it.
        """
        if state is None or "." not in slot:
            return None
        obj, attr = slot.rsplit(".", 1)
        if obj == target or attr not in ("row", "col"):
            return None
        cur, tgt = state.get(slot), state.get(f"{target}.{attr}")
        if cur is None or tgt is None:
            return None
        return int(tgt) - int(cur)

    def separability(self, env: Any, offered: tuple[str, ...]) -> dict[str, int]:
        """How many self-members find each action DISTINCTIVE. **Relocated, not rewritten.**

        This was `tether._learned_split`, above the seam, ending in
        `max(self.actions, key=lambda a: sep[a])` -- the agent ranking buttons. The DATA was
        never the problem: `env.contingency()` is an action-effect record built by acting, and
        its own docstring says *"THIS IS THE HALF `act` WOULD HAVE HANDED ... the difference is
        provenance."* **Same kind of thing `audit` builds, a different producer.** So the read
        belongs here and only the argmax moved.

        THE TWO GATES ARE CARRIED VERBATIM and each was earned. COVERAGE: a member contributes
        only when every offered action appears in ITS OWN dict -- without it a member separates
        on partial evidence, which is the claim whose own falsifier caught it (*every action
        observed at step 22, first fire at step 2*). STABLE: without it four single observations
        are trivially all-different and `sep` credits noise, **which is a non-flat spread on
        nothing and worse than a flat one.**

        DISTINCTIVE MEANS DIFFERENT FROM EVERY ALTERNATIVE, NOT FROM SOME -- the first version
        asked *differs from at least one*, which nearly everything satisfies. And NOTHING IS
        SUMMED ACROSS MEMBERS' SIGNALS: the comparison is always WITHIN one member, because
        three report a fraction and one reports a signed count and they are not commensurable.
        """
        fn = getattr(env, "contingency", None)
        if fn is None:
            return {}
        sep = dict.fromkeys(offered, 0)
        passed = 0
        # `.items()`, NOT `.values()`: the member's NAME is half the question, and the two gates
        # are counted APART because coverage and stability are different causes with different
        # repairs -- one number asked to carry two questions.
        for name, rec in fn().items():
            per_action, stable = rec["per_action"], rec["stable"]
            if not set(sep) <= set(per_action):
                self.member_gates[f"{name}:no_coverage"] += 1
                continue
            if not stable:
                self.member_gates[f"{name}:unstable"] += 1
                continue
            self.member_gates[f"{name}:passed"] += 1
            passed += 1
            vals = {a: v for a, v in per_action.items() if a in sep}
            for a, v in vals.items():
                if all(w != v for b, w in vals.items() if b != a):
                    sep[a] += 1
        self.sep_passes[passed] += 1
        # **`at_audit`, NOT `cycle` -- AND THE RENAME IS THE POINT.** The agent's version logged
        # `cycle`; the interface has no cycle and counts PRESSES. Publishing a press count under
        # the name `cycle` is `A6i` at a published field, and this instrument's whole job is to
        # be read by someone who did not write it.
        self.sep_log.append({"at_audit": self.audits, "passed": passed,
                             "sep": tuple(sorted(sep.values(), reverse=True))})
        return sep

    @staticmethod
    def context(env: Any, actor: str | None = None) -> tuple:
        """THE CONTEXT KEY, v1 -- the contact configuration at press time, name-free.

        **THE REVIEWER'S LEAD, 2026-09-28, verified at `RELATIONS.md:182-184` (Part 4.1):**
        *normal -- perpendicular to the contact -- **a blocked move***; *static friction -- a
        move that fails while touching*. **So a blocked move is not a quirk to model: it is a
        relation the corpus already names**, and keying an effect by the contact present when
        it was taken is what separates *conditional* from *the mapping changed*.

        **v1 AND v2, AND v1 IS NOT A PLACEHOLDER.** The reviewer's key is contact ON THE AXIS OF
        THE ATTEMPTED MOTION, which is sharper -- and it has a bootstrap: **you need the axis to
        key by it, and the axis is what the interface is learning.** So v1 keys on the WHOLE
        configuration, computable from frame one, and refines to the sided key once displacement
        has been observed. **It sharpens by acting, like everything else here.**

        **KINDS, NEVER NAMES.** `_contact_keys` settled this once: *names churn every frame and
        would leave everything permanently unexplored; vocabulary permanent, instances
        transient.* So the key is the multiset of contact KINDS.

        **AND THE COST IS IN THE SAFE DIRECTION:** two situations sharing a v1 key make a real
        mapping change read as conditionality. **The audit under-claims rather than
        over-claims**, which is the right way for a guard to be wrong.

        **THAT LAST CLAIM WAS WRONG IN ONE DIRECTION AND FIXTURE A MEASURED IT -- 2026-09-28.**
        The whole-board key ALSO over-claims: gridworld's `left` is sometimes blocked by the
        wall while the board-wide multiset reads identical, so `changed` -- the LOUDER claim --
        fired on an action whose mapping never moved. **1 of 2 flagged actions was real.**

        **v2 IS THE ACTOR'S OWN CONTACTS, and the reviewer's route to the bootstrap is that the
        DELTA TABLE ALREADY KNOWS WHICH OBJECT EACH ACTION MOVES.** So the axis does not have to
        be guessed: ask the table who this action moves, and key on what THAT object is
        touching. Before the table knows, `actor` is `None` and this is v1 exactly -- **it
        sharpens by acting, which is what the v1/v2 note above promised and could not yet do.**
        """
        fn = getattr(env, "contact_points", None)
        if fn is None:
            return ()
        try:
            pts = fn() or ()
        except Exception:                                  # noqa: BLE001
            return ()
        kinds: dict[str, int] = {}
        for a, b, kind in pts:
            # THE ACTOR'S OWN CONTACTS, not the board's. *`left` while against the wall* and
            # *`left` in open space* are different situations and the whole-board multiset
            # cannot tell them apart -- which is exactly the false positive fixture A produced.
            if actor is not None and actor not in (a, b):
                continue
            kinds[kind] = kinds.get(kind, 0) + 1
        return tuple(sorted(kinds.items()))

    def expected_move(self, intent: Intent, offered: tuple[str, ...], ctx: tuple = (),
                      state: dict | None = None, env: Any = None) -> float | None:
        """HOW FAR THE AGENT EXPECTS ONE PRESS OF THIS INTENT TO MOVE ITS SUBJECT.

        **ASKED IN INTENTS, BECAUSE THAT IS WHAT THE AGENT HOLDS.** The first version of the
        caller looked the movement up BY ACTION and got `None` 76 times out of 76 -- a routine
        body carries an `Intent`, never a button, and the delta table is keyed by the REALISED
        action, which lives below the seam. It did not fail loudly; it returned the same
        `None` that means *no reading*, so the agent's own model read as absent.

        **ONE SELECTION RULE, NOT A SECOND COPY OF IT.** This CALLS `realise` rather than
        re-implementing *which action best serves this intent* -- that rule is the seam's
        centre and a duplicate of it is `A6i` in its guaranteed form. Reviewer, 2026-09-30:
        share the selection and reuse the existing prediction path, two callers.

        **SAFE TO ASK, AND THAT IS PROVEN RATHER THAN ASSUMED.** Calling `realise`
        hypothetically changes nothing -- `test_asking_the_interface_does_not_change_it` is
        the seat for exactly this, and `_last_was_reset` is written in `audit`, not here.

        `None` WHEN THERE IS NO READING -- no intent subject, no action realised, or nothing
        observed to move that slot. Honest, not missing.
        """
        if intent.subject is None:
            return None
        r = self.realise(intent, offered, ctx, state, env)
        return None if r is None else self.step_of(r.action, intent.subject)

    def step_of(self, action: str, slot: str) -> float | None:
        """HOW FAR THIS ACTION MOVES THIS SLOT, per press, from what the agent has watched.

        **A READING OF THE AGENT'S OWN OBSERVATIONS, NOT A FACT ABOUT THE BOARD.** The delta
        table is filled by `audit` from presses the agent made and frames it saw, so this
        returns nothing until it has watched -- which is the honest state and not a gap.

        ACROSS CONTEXTS ON PURPOSE. The per-context cells are sparse by design, and the
        question here is *how much does this move* rather than *what happens in exactly this
        configuration* -- the same fallback `realise` already makes, and for the same measured
        reason: keyed too finely, the cells are populated and every query abstains.
        """
        n = tot = 0
        # `(ctx, slot, rel)` since layer 1 -- the relation is not what this reads.
        for (_ctx, k, _rel), (cn, ct) in self.table.get(action, {}).get("delta", {}).items():
            if k == slot:
                n += cn
                tot += ct
        return None if n == 0 else tot / n

    def recurrence(self, slot: str) -> int:
        """HOW MANY TIMES THIS SLOT HAS BEEN SEEN TO MOVE, over every action and every
        `(ctx, rel)` key. The COMPRESSIBLE half of Figure 5's *large and compressible*.

        **A PROXY, AND LABELLED ONE HERE RATHER THAN IN A NOTE -- the reviewer, 2026-10-01.**
        Recurrence is EVIDENCE OF repeatable structure; it is not a compression reading. A
        gap seen once is not incompressible, it is unassessed.

        AND IT IS NOT INDEPENDENT OF MAGNITUDE ON EVERY WORLD. `F400` measured the ratio
        `outstanding/recurrence` per slot: one distinct value on `buttons` (the two are one
        count scaled, so a product is a square), two on `click_only`, twelve on `default`.
        **Do not read a second factor's contribution off a world where that ratio is
        constant.**
        """
        n = 0
        for e in self.table.values():
            for key, (cn, _ct) in e.get("delta", {}).items():
                if len(key) > 1 and key[1] == slot:
                    n += cn
        return n

    def audit(self, r: Realisation, before: dict, after: dict, ctx: tuple = ()) -> bool:
        """Record what this action did, and report when it does not have ONE fixed effect.

        **RETURNS `True` FOR *CONDITIONAL*, NOT FOR *CHANGED*, AND THE DIFFERENCE IS ISAIAH'S
        OWN -- CORRECTED 2026-09-28 BY RUNNING IT.** The first version returned "the table was
        wrong" and I commented at the wiring site that it *cannot fire on gridworld*, because
        `actions()` is a module constant and `step` resolves a fixed `_DELTA`.

        **IT FIRED FOUR TIMES IN EIGHT STEPS.** Measured: `down` has TWO distinct effects over
        six presses -- `('o0.row', 'o1.proximity', ...)` and *nothing changed*. **Gridworld's
        RULE is invariant and its OUTCOME is not**: the mover is sometimes blocked. That is
        CONDITIONALITY, which Isaiah named as its own question -- *is it conditional?* -- beside
        *do the actions change*.

        **SO THIS REPORTS CONDITIONALITY HONESTLY AND DOES NOT CLAIM THE OTHER.** Separating
        *conditional* from *the mapping changed* needs the effect keyed by the CONTEXT it was
        observed in, and no such key exists yet. **Filed, not faked** -- a mechanism that
        announced "the mapping changed" on every wall would be crying wolf, and a green reading
        from it would have meant nothing.

        And the conditionality is worth having on its own: *`down` sometimes does nothing* is
        System 0 job A's **is that a wall?**, answered by acting.
        """
        # **THE ADJACENCY FLAG, SET WHERE THE PRESS ACTUALLY HAPPENED.** `realise`
        # refuses a second consecutive `RESET`; this is the only thing that tells it
        # there was a first one.
        self._last_was_reset = (r.action == RESET)
        self.audits += 1
        if r.coord is not None:
            self.clicked.add(r.coord)
            _on = self._acted(r.coord, before)
            if _on is not None:
                self.pressed_kinds.add(self._kind(_on, before))
        # READ OFF `before`, NOT `after`. The cause is whatever was at the coordinate WHEN THE
        # PRESS LANDED -- on a board where the press moves things, reading `after` would
        # attribute the effect to whatever has since arrived there.
        _acted_on = self._acted(r.coord, before)
        # The instance record, written from the agent's OWN press and its OWN audit. Keyed by
        # the coordinate it aimed at, which is the only handle it has on "the thing I pressed".
        if r.coord is not None:
            self.aimed_effect.setdefault(r.coord, set()).update(
                k for k in before if before.get(k) != after.get(k))
        # **THE EFFECT IS WHAT THE ACTION DID TO OWN ATTRIBUTES, NOT EVERY SLOT THAT MOVED --
        # 2026-09-28, and it is the `actor_of` defect one level along.** Measured on gridworld
        # with no remap, `left` was flagged CHANGED because one context held these two:
        #
        #     ('o0.col', 'o1.proximity', 'o2.proximity', 'o3.proximity', 'o4.proximity', ...)
        #     ('o0.col',                 'o2.proximity',                 'o4.proximity', ...)
        #
        # **Both move `o0.col`. The real effect is IDENTICAL.** The difference is entirely in
        # which PROXIMITY slots happened to shift -- and a relation changes according to where
        # everything else is, not according to what the action does. So *the mapping changed*
        # fired on an action whose mapping never moved, for the second time from the same root.
        # **AND THE EFFECT IS SIGNED, BECAUSE A REFLECTION CHANGES THE SIGN AND NOT THE SLOT
        # SET -- 2026-09-28, and this is why the earlier "true positives" were accidental.**
        # With names alone, `left` produces `('o0.col',)` before AND after a remap: it still
        # moves the same slot, just the other way. So a reflected mapping is INVISIBLE to a
        # name-set comparison, and the remap was only ever detected through proximity churn
        # that happened to differ -- **the right answer for the wrong reason, which stopped
        # being any answer the moment the noise was filtered out.**
        #
        # Signed, `left` is `(('o0.col', -1),)` and then `(('o0.col', +1),)`: two effects in one
        # context, which is exactly what `changed_here` exists to notice.
        def _eff(k: str) -> tuple[str, int]:
            try:
                d = int(after.get(k, 0)) - int(before.get(k, 0))
            except (TypeError, ValueError):
                return (k, 0)
            return (k, (d > 0) - (d < 0))

        # **TWO QUANTITIES, TWO NAMES -- AND I GAVE THEM ONE AND BROKE THE DELTA TABLE.**
        # `changed` feeds BOTH the delta loop below (which needs SLOT NAMES to look up
        # `after[k]`) and the effect comparison (which needs the SIGNED effect). Making it
        # signed made the delta loop call `after.get(('o0.col', -1))`, which is `None`, which
        # raises, which `continue`s -- **so the delta table silently stopped filling and no
        # routine could be minted.** `A6i` in its purest form, in code minutes old, caught by
        # the m2 seat rather than by me.
        # **THE DENOMINATOR THE DELTA TABLE LACKS -- Isaiah's downrating ruling, 2026-09-30.**
        # `delta` is written `for k in changed`, so a slot that NEVER MOVES gets no entry and
        # `step_of` returns `None` for it -- the same answer it gives for a slot never seen.
        # Those are different states and downrating turns on telling them apart: *observed N
        # times and never moved* is evidence of inertness, *never observed* is no evidence.
        #
        # Counting presence here costs one increment at a site already iterating `before`, and
        # it puts the denominator AT THE SAME SITE AS THE NUMERATOR, which is this project's
        # rule for counts. It reads nothing and decides nothing -- the weighting is elsewhere.
        for _k in before:
            self.present[_k] = self.present.get(_k, 0) + 1
        changed = tuple(sorted(k for k in before if before.get(k) != after.get(k)))
        signature = tuple(sorted(_eff(k) for k in changed
                                 if k.rsplit(".", 1)[-1] not in RELATIONAL))
        e = self.table.setdefault(r.action, {"by_ctx": {}, "n": 0, "delta": {}})
        e["n"] += 1
        # **WHICH WAY, NOT ONLY WHICH SLOT.** A changed-set says an action touches `o0.row`; it
        # does not say whether it raises or lowers it, and *raise this slot* is the commonest
        # thing an agent can want. So the table keeps a running mean of the SIGNED change per
        # slot, per context -- learned by acting, nothing closed over at construction.
        #
        # **THIS IS `_move_map` DONE RIGHT AND IN THE RIGHT PLACE.** That one keyed
        # action -> AVATAR displacement, so it never filled on a board with no avatar and it
        # lived above the seam where the agent could reason about buttons. This is any slot,
        # no body required, and below the seam where knowing about buttons is the job.
        for k in changed:
            try:
                d = int(after.get(k, 0)) - int(before.get(k, 0))
            except (TypeError, ValueError):
                continue
            # LAYER 1. `rel` says whether the slot that moved belongs to the object that was
            # ACTED ON or to another one -- the coordinate that makes *acting on A changes B*
            # expressible at all. Derived per changed slot, because one press can move both.
            rel = (NO_TARGET if _acted_on is None
                   else SELF if k.rsplit(".", 1)[0] == _acted_on else OTHER)
            n, tot = e["delta"].get((ctx, k, rel), (0, 0))
            e["delta"][(ctx, k, rel)] = (n + 1, tot + d)
            # **THE VALUE COLUMN -- §15, and it is a COLUMN rather than a mechanism.** The same
            # row, the same key, the same provenance: what this action was observed to LEAVE the
            # slot at. Only on a CHANGE, because *it was already 3 and I did nothing* is not
            # evidence that anything reaches 3.
            #
            # **THE SET IS KEPT WHOLE AND NEVER COLLAPSED TO THE LAST MEMBER.** A cell holding
            # more than one value is the refutation of the whole idea -- the action has a
            # HISTORY there and not a capability -- and a table that overwrote would look
            # correct forever. `unreliable` is that count, published rather than left to be
            # re-derived.
            #
            # **AND THE KEY CARRIES THE VALUE BEFORE THE PRESS -- the reviewer, 2026-09-28, and
            # it was caught before the first multiplicity count was read.** Keyed `(ctx, slot)`
            # alone, a CYCLING action -- colour 3 -> 4 -> 5, or a rotation -- leaves a different
            # value every press, so its cell fills with values and the singleton rule refuses
            # it. **But a cycle is perfectly reproducible, and it is one of the things System 0
            # exists to recognise.** With `before` in the key, a cycle and a fixed recolour are
            # BOTH singletons, and only a genuinely unreliable action shows multiplicity.
            vals = e.setdefault("lands", {}).setdefault((ctx, k, int(before.get(k, 0))), set())
            vals.add(int(after.get(k, 0)))
            if len(vals) > 1:
                self.unreliable.add(r.action)
        # **THE SIGN IS JUDGED PER CELL, KEYED BY THE VALUE BEFORE THE PRESS -- the reviewer,
        # 2026-09-28, and it is the fix already built for the value table applied here.**
        #
        # The wrap made `left` read `+1` and `-1` in one context with nothing remapped, and the
        # signs are TRUE DATA -- but the conclusion drawn from them, *the mapping of `left`
        # changed*, is false, and System 0 would report it every time anything crossed an edge.
        # **A standing false alarm is not a reading.**
        #
        # Keyed `(ctx, slot, before)` the wrap is CONSISTENT: from column 0 `left` always gives
        # `+(GRID-1)`, from column 5 always `-1`. **A real reflection still flips the sign
        # within the same cell**, which is the only thing that now counts as the mapping having
        # changed. Same shape as `lands`, same reason a cycle is reproducible rather than
        # unreliable.
        flipped = False
        for k, sign in signature:
            cell = e.setdefault("signs", {}).setdefault((ctx, k, int(before.get(k, 0))), set())
            if sign and cell and sign not in cell:
                flipped = True
            cell.add(sign)
        seen = e["by_ctx"].setdefault(ctx, set())
        changed = signature          # the by_ctx record stays the signed effect
        # WITHIN one context a second effect is the first real evidence the MAPPING CHANGED.
        # ACROSS contexts it is CONDITIONALITY. That is the whole point of the key, and with
        # v1's coarser key a genuine change can still land in the conditional bucket.
        # **DOING NOTHING IS NOT DOING SOMETHING ELSE.** A blocked move produces an EMPTY
        # effect, and comparing it against a real one made *the mapping changed* fire on every
        # wall -- the last false positive on fixture A's control arm, where nothing ever
        # remapped. **An action that sometimes does nothing is CONDITIONAL; an action that does
        # two DIFFERENT things is CHANGED**, and that is the distinction Isaiah asked System 0
        # for. `RELATIONS.md` already names the blocked move as a relation (*normal -- a blocked
        # move*; *static friction -- a move that fails while touching*), so it belongs in the
        # conditional bucket by the corpus's own account and not merely by convenience.
        # **`flipped` IS THE CLAIM NOW, not a set comparison.** Comparing whole effect SETS
        # made every difference in which slots moved read as a mapping change; the per-cell
        # sign is the narrow thing that actually means it.
        changed_here = flipped
        # **AND THE ONE SURVIVING FLAG ON FIXTURE A's CONTROL IS THE BOARD, NOT THE DETECTOR --
        # measured, not reasoned.** `left` there holds BOTH `(('o0.col', +1),)` and
        # `(('o0.col', -1),)` in one context while nothing ever remapped. **gridworld WRAPS**:
        # moving left from column 0 lands at column GRID-1, which is a POSITIVE delta.
        #
        # So on a torus the SIGN of a positional delta is not a property of the action, and the
        # detector is reporting the data correctly against an abstraction the world does not
        # satisfy. **Left as it is on purpose**: special-casing the wrap would put board
        # knowledge in the interface to make a number look better, and the honest statement is
        # that this reading is a true one about a wrapped board. Recorded so the next reader
        # does not try to fix a world property.
        seen.add(changed)
        if len({x for v in e["by_ctx"].values() for x in v}) > 1:
            self.conditional.add(r.action)
        if changed_here:
            self.changed.add(r.action)
        return changed_here

    def report(self) -> dict:
        cells = sum(len(e.get("lands", {})) for e in self.table.values())
        multi = sum(1 for e in self.table.values()
                    for v in e.get("lands", {}).values() if len(v) > 1)
        # THE ATTRIBUTES THE ACTOR RULE HAS JUDGED, SPLIT THE WAY IT JUDGED THEM. A reader
        # who sees a relational name under `own` has found the stopgap's blind spot, which is
        # the only way it can be found until a world declares the split itself.
        own = sorted(self.attrs_seen - set(RELATIONAL))
        return {"mapped": len(self.table), "audits": self.audits,
                "attrs_own": own,
                "attrs_relational": sorted(self.attrs_seen & set(RELATIONAL)),
                "conditional": sorted(self.conditional),
                "changed": sorted(self.changed),
                "unreliable": sorted(self.unreliable),
                "value_cells": cells, "value_cells_multi": multi,
                "note": "conditional = more than one observed effect ACROSS contexts; "
                        "changed = more than one WITHIN one, which is the context key doing "
                        "its job. value_cells_multi against value_cells is the plan's 15c refuter: "
                        "a cell with several values is a history, not a capability"}
