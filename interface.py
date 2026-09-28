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
from dataclasses import dataclass
from typing import Any

sys.dont_write_bytecode = True

# WHAT THE AGENT CAN MEAN. Deliberately NOT an action vocabulary -- these name what the agent
# wants to be true, and the interface is what knows whether this board can express it.
ELICIT = "ELICIT"        # get ANY response from this object, or from the board. The bootstrap
TOUCH = "TOUCH"          # bring a onto b
BE_AT = "BE_AT"          # put a at a region
BECOME = "BECOME"        # a takes an attribute


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

    # ---- downward: intent -> action --------------------------------------------------

    def realise(self, intent: Intent, offered: tuple[str, ...],
                ctx: tuple = (), state: dict | None = None) -> Realisation | None:
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
                here = self.table.get(a, {}).get("lands", {}).get((ctx, intent.subject, _now))
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
                n, tot = d.get((ctx, intent.subject), (0, 0))
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
        if intent.kind != ELICIT:
            # WITHOUT A TABLE ENTRY THERE IS NOTHING HONEST TO PICK, and guessing would be the
            # interface deciding. It abstains and the agent learns the intent was unrealisable.
            return None
        unmapped = [a for a in offered if a not in self.table]
        if unmapped:
            return Realisation(unmapped[0], unmapped=True,
                               why="requested exploration: never taken")
        # THE VARIETY CONDITION: prefer an action whose effect IN THIS CONTEXT is unknown.
        fresh = [a for a in offered if ctx not in self.table[a]["by_ctx"]]
        if fresh:
            return Realisation(fresh[0], why="requested exploration: effect here not yet known")
        # everything mapped in this context. Take the one taken LEAST here -- still the agent's
        # call to explore, and refusing would be the interface overruling it.
        least = min(offered, key=lambda a: len(self.table[a]["by_ctx"].get(ctx, ())))
        return Realisation(least, why="requested exploration: all known here, least-seen taken")


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
    def context(env: Any) -> tuple:
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
        """
        fn = getattr(env, "contact_points", None)
        if fn is None:
            return ()
        try:
            pts = fn() or ()
        except Exception:                                  # noqa: BLE001
            return ()
        kinds: dict[str, int] = {}
        for _a, _b, kind in pts:
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
