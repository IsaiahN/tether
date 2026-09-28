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

import sys
from collections import Counter
from dataclasses import dataclass
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


class Interface:
    """Translates intent down, reports capability up. **Knows nothing about goals.**

    It holds one table: what each action has been OBSERVED to do, keyed by the action and built
    only from what `audit()` saw. **Nothing is closed over at construction** -- which is the
    defect `tether.py:2876` names in the toy world's `act` atom, where *"the primitive it was
    given already knew"* and discriminate became a property of the atom set rather than a model
    the agent built. **This table starts empty on every board and is filled only by acting.**
    """

    def __init__(self) -> None:
        self.table: dict[str, dict] = {}       # action -> what it was observed to do
        self._seen: tuple[str, ...] = ()       # last frame's advertised set, for capability
        self.audits = 0
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

    # ---- downward: intent -> action --------------------------------------------------

    def realise(self, intent: Intent, offered: tuple[str, ...], ctx: tuple = (),
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

        def _key(a: str) -> tuple:
            """The key THIS action's rows were written under. **The audit and the realiser must
            agree or every same-context lookup misses.**

            `audit` keys on the ACTOR's contacts (v2), so a query keyed on the whole board would
            fall through to the across-context prior on every hit -- a silent degradation that
            would read as *the table has not seen this yet*. With no `env` the caller gets `ctx`
            as passed, which is what a fixture with no contacts wants.
            """
            if env is None:
                return ctx
            return Interface.context(env, self.actor_of(a))
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
                    (_key(a), intent.subject, _now))
                if here and set(here) == {intent.value}:
                    best, how = a, "here"
                    break
            if best is None:
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
                n, tot = d.get((_key(a), intent.subject), (0, 0))
                where = "here"
                if not n:
                    n = sum(v[0] for (c, k), v in d.items() if k == intent.subject)
                    tot = sum(v[1] for (c, k), v in d.items() if k == intent.subject)
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
                for (_c, k), (n, tot) in self.table.get(a, {}).get("delta", {}).items():
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
            coord = self._unclicked(state) if a in POSITIONED else None
            if coord is not None:
                why = f"{why}, aimed where nothing has been clicked"
            return Realisation(a, coord=coord, unmapped=(a not in self.table), why=why)

        asked = "exploration" if intent.kind == ELICIT else "something that separates"
        unmapped = [a for a in offered if a not in self.table]
        if unmapped:
            return _made(_pick(unmapped), f"requested {asked}: never taken")
        # THE VARIETY CONDITION: prefer an action whose effect IN THIS CONTEXT is unknown.
        fresh = [a for a in offered if _key(a) not in self.table[a]["by_ctx"]]
        if fresh:
            return _made(_pick(fresh), f"requested {asked}: effect here not yet known")
        # everything mapped in this context. Take the one taken LEAST here -- still the agent's
        # call to explore, and refusing would be the interface overruling it.
        seen = {a: len(self.table[a]["by_ctx"].get(_key(a), ())) for a in offered}
        fewest = min(seen.values())
        band = [a for a in offered if seen[a] == fewest]
        return _made(_pick(band), f"requested {asked}: all known here, least-seen taken")


    # ---- upward: what changed, in reasoning terms -------------------------------------

    def capability(self, offered: tuple[str, ...]) -> Capability:
        """What the board opened or closed since the last frame, **named as affordance.**

        The names here are the interface's own words for what became possible, and they are
        deliberately not the action identifiers -- `F28`'s line: availability is legitimate to
        read, directional semantics never.
        """
        was, now = set(self._seen), set(offered)
        self._seen = offered
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

    def actor_of(self, action: str) -> str | None:
        """Which object this action has been observed to move most. **From the table, learned.**

        The reviewer's route out of v2's bootstrap, 2026-09-28: *the delta table already knows
        which object each action moves.* Slots are `{object}.{attribute}`, the delta table is
        keyed by slot, so the actor is the owner of the slots this action shifts -- **read off
        what acting produced, never declared.**

        `None` until the table has seen this action move something, and `None` is the honest
        answer rather than a guess: the caller then keys on the whole board, which is v1.

        **PROXIMITY IS NOT MOVEMENT, AND THE FIRST VERSION OF THIS RETURNED `o5` FOR EVERY
        ACTION -- 2026-09-28.** It summed observations over ALL moved slots, and every press
        shifts `o0.row` or `o0.col` AND the `proximity` slot of every other object -- **a
        relation changes for everyone whenever anything moves.** Six objects tied on proximity
        and the tie-break was `max(key=(count, name))`, so the answer was ALPHABETICAL and the
        key was built on a spectator. It measured cleanly, it had a plausible mechanism, and it
        was a fact about sorting.

        **SO THE DEFINITION IS THE FIX: an object's `.row`/`.col` are ITS OWN, and its
        `proximity` is a fact about it AND SOMETHING ELSE.** Only intrinsic position counts as
        being moved. `_at` and `_gap` already privilege the same two, so this adds no taxonomy
        the interface was not already using.
        """
        moved: dict[str, int] = {}
        for (_c, k, *_r), (n, _tot) in self.table.get(action, {}).get("delta", {}).items():
            if "." not in k:
                continue
            obj, attr = k.rsplit(".", 1)
            if attr not in ("row", "col"):
                continue
            moved[obj] = moved.get(obj, 0) + n
        return max(moved, key=lambda o: (moved[o], o)) if moved else None

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
        for obj in sorted(rows & cols):
            at = self._at(obj, state)
            if at is not None and at not in self.clicked:
                return at
        return None

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
        self.audits += 1
        if r.coord is not None:
            self.clicked.add(r.coord)
        changed = tuple(sorted(k for k in before if before.get(k) != after.get(k)))
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
            n, tot = e["delta"].get((ctx, k), (0, 0))
            e["delta"][(ctx, k)] = (n + 1, tot + d)
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
        seen = e["by_ctx"].setdefault(ctx, set())
        # WITHIN one context a second effect is the first real evidence the MAPPING CHANGED.
        # ACROSS contexts it is CONDITIONALITY. That is the whole point of the key, and with
        # v1's coarser key a genuine change can still land in the conditional bucket.
        changed_here = bool(seen) and changed not in seen
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
        return {"mapped": len(self.table), "audits": self.audits,
                "conditional": sorted(self.conditional),
                "changed": sorted(self.changed),
                "unreliable": sorted(self.unreliable),
                "value_cells": cells, "value_cells_multi": multi,
                "note": "conditional = more than one observed effect ACROSS contexts; "
                        "changed = more than one WITHIN one, which is the context key doing "
                        "its job. value_cells_multi against value_cells is the plan's 15c refuter: "
                        "a cell with several values is a history, not a capability"}
