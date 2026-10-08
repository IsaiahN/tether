"""`M2_STANDARD`'s seven, each REINTRODUCING THE DEFECT it guards against.

The first version of this audit matched source text -- `"Rt.guards(r)" in src` -- which is the
corpus's own corollary inverted: *an exit code is a declaration where a pattern match over
stdout is a guess.* **A rename would have broken it silently, and a behaviour change would not
have broken it at all**, so it could pass while the mechanism was wrong.

`test_gate.py`'s form instead: **one defect per check, constructed, and the mechanism has to
catch it.** *Tests reach, not existence.*
"""

import collections
import contextlib
import copy
import math
import pathlib
import sys

import numpy as np
from arcengine import FrameDataRaw, GameState

import arc_atoms
import arc_percept
import arc_predict
import arc_world
import gamma
import routine as Rt
import tether
from arc_world import ArcWorld
from tether import YES, pays, term_bits

sys.dont_write_bytecode = True

SIDE, PALETTE = 14, 7


class _Two:
    """Two objects, one action that moves them. Enough state for a mint to be attempted."""

    def __init__(self) -> None:
        self.n = 0

    def _frame(self):
        f = FrameDataRaw(game_id="m2test", state=GameState.NOT_FINISHED, levels_completed=0,
                         win_levels=3, available_actions=[1, 2, 3])
        b = np.zeros((SIDE, SIDE), dtype=int)
        b[2][self.n] = 3
        b[4][self.n + 1] = 5
        b[5][self.n + 1] = 5
        f.frame = [b]
        return f

    def reset(self):
        self.n = 0
        return self._frame()

    def step(self, *a, **_k):
        act = a[0] if a else None
        if "1" in getattr(act, "name", str(act)) and self.n < SIDE - 3:
            self.n += 1
        return self._frame()


_SEEN: collections.Counter = collections.Counter()


@contextlib.contextmanager
def _watch():
    """Count the ACT events the suite reaches, from the run it is already doing."""
    import ledger
    real = ledger.Ledger.record

    def spy(self, cycle, step, slot, event, **d):
        if event == "routine_end":
            _SEEN[d.get("outcome")] += 1
        elif "routine" in event:
            _SEEN[event] += 1
        return real(self, cycle, step, slot, event, **d)

    ledger.Ledger.record = spy
    try:
        yield
    finally:
        ledger.Ledger.record = real


_BUILT: dict = {}


def _agent(cycles: int = 25):
    """A warmed agent, built ONCE per cycle count and handed out as a deep copy.

    **THE SEAT COST 41s BEFORE THIS, AGAINST `test_gate.py`'s 195ms**, because every check ran
    a fresh 25-cycle loop. *A hook people wait minutes for is a hook people disable.*

    **AND THE OBVIOUS FIX WAS A FITTED NUMBER.** Ten cycles is usable and 9x faster -- but
    fourteen and eighteen are NOT, and twenty-five is: usability oscillates with the board's
    phase, so choosing ten because it happened to work is a constant fitted to the case that
    prompted it. **Copying is structural instead** -- the cycle count the checks were written
    against is preserved and the loop runs once, with `deepcopy` measured at 60x cheaper than
    rebuilding.
    """
    if cycles not in _BUILT:
        # **`platform=()` IS PINNED FOR THE SAME REASON, DEMONSTRATED 2026-10-06 (F477).** With
        # the platform's RESET in the set, SEVEN checks fail here; pinned out,
        # all pass. A green m2 does not certify RESET in the set. (`_Two` declared RESET as
        # id 0, which no game does -- 22 of 22 -- and the old filter hid it; it declares
        # [1, 2, 3], the set it always effectively offered.)
        env = ArcWorld(_Two(), arc_percept.Objects(),
                       arc_atoms.three_spaces(arc_predict.predict()), palette=PALETTE,
                       platform=())
        # **`system0=False` IS PINNED HERE, AND IT IS THE FIXTURE'S ASSUMPTION MADE EXPLICIT
        # RATHER THAN A CHECK WEAKENED.** System 0 became the default on 2026-09-25 and three
        # checks here failed with `fixture:` -- their OWN guard for *the setup did not reach the
        # state I test*, not for *the mechanism broke*. Contact-seeking changes which actions
        # are taken, which changes which slots carry residual, which is the trajectory these
        # scenarios are built on.
        #
        # AND IT IS WORTH KNOWING RATHER THAN ONLY FIXING: **these M2 checks are
        # TRAJECTORY-DEPENDENT.** They verify the mechanisms against one action policy, so a
        # policy change reads as a fixture failure. That is a real limit on what a green m2
        # seat establishes.
        #
        # **`accumulate=False` IS PINNED FOR THE SAME REASON AND IT WAS DEMONSTRATED, NOT
        # ASSUMED -- 2026-09-25.** Shipping the accumulator ON made FIVE checks fail. FOUR OF
        # THEM PASS when the flag is set on the COPY instead of during this warm-up, so their
        # failures were this trajectory moving and NOT their contracts. Only `check_one_bargain`
        # was a real conflict, and it is migrated rather than pinned around.
        #
        # **THE SHIPPED DEFAULT IS `accumulate=True`.** This pin is the fixture holding one
        # policy still so the OTHER mechanisms can be checked -- exactly what `system0=False`
        # is doing one line up -- and it is the reason a green m2 does not certify the
        # accumulator. `check_the_accumulation_commits_where_the_bargain_refused` does that,
        # with the flag on.
        # **AND THE ACTION POLICY IS PINNED FOR THE SAME REASON, AND IT WAS DEMONSTRATED --
        # 2026-09-28.** Routing `probe`/`draw` through the interface seam made THREE checks
        # fail: `check_can_gates_until`, `check_one_bargain`,
        # `check_shelf_must_be_runnable_here`. **Run with the old draw restored, ALL THREE
        # PASS** -- so their failures are this trajectory moving and NOT their contracts,
        # measured the way the `accumulate` pin was rather than asserted.
        #
        # **A GREEN m2 THEREFORE DOES NOT CERTIFY THE SEAM.**
        # `conform/stateful.py::test_the_seam_varies_what_it_explores_with` does, with the
        # seam live -- because *pinned around* without a certifying check is how a suite keeps
        # a mechanism green by never running it.
        # **AND THE `system0` PIN IS GONE ENTIRELY -- MEASURED, NOT ASSUMED, 2026-09-29.**
        # Isaiah removed the config field (System 0 is always on), so the pin first became a
        # fixture-local patch. Then the reviewer asked the obvious question: do these checks
        # still hold under the policy the agent ACTUALLY RUNS? **They all do -- 30/30 with
        # System 0 live**, and the treatment was confirmed executed rather than inferred:
        # `_system0_active` was asked 19 times and returned True 19 times.
        #
        # **SO THE PIN IS REMOVED RATHER THAN DOCUMENTED.** The three failures that justified
        # it in 2026-09-25 are gone -- most likely absorbed by the `_explore` pin added on
        # 09-28, which holds the action policy directly. **A pin that is no longer needed does
        # not sit harmlessly: it hides the next regression in the thing it pins.**
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="m2test"),
                          tether.Config(accumulate=False))
        # **THE PARAMETER IS `subject`, NOT `_subject`, AND THE NAME IS LOAD-BEARING.**
        # A double whose parameter name differs from the real function's silently forbids
        # calling it by keyword -- `_curiosity_subject` aims `_explore(subject=...)` and this
        # stub raised `TypeError` on a signature that was never the agent's.
        ag._explore = lambda before, subject=None: ag.drive.choose(  # noqa: ARG005
            ag.actions, ag.cycle, tether._where(before))
        for _ in range(cycles):
            ag.step()
        _BUILT[cycles] = ag
    return copy.deepcopy(_BUILT[cycles])


def _wide(ag, slot="o1.dcol"):
    """Widen only the SCOPE, which is the ceiling every fixture hit. Nothing else is touched."""
    real = ag._group
    ag._group = lambda s, st: (tuple(list(real(s, st)) + [7, 8, 9, 11]) if s == slot
                               else real(s, st))
    # A SHRINKING SERIES ON THE AXIS THE SELECTOR ACTUALLY READS. This set `_disc` (the
    # per-slot gap) until the selector was re-keyed onto `_res` (the per-scope residual) --
    # and the fixture kept passing on two checks and silently stopped producing a routine on
    # two others, which is what a helper injecting the wrong quantity looks like.
    # ONE goal hypothesis, on the axis the selector actually reads. Setting only this slot's
    # series left the warm-up's real series on the others, and the selector correctly chose a
    # DIFFERENT slot -- one with a scope of 2 that cannot pay. The helper's job is to isolate
    # the widened slot, so it is the only hypothesis on offer.
    ag._res = {slot: [0.9, 0.87, 0.84]}
    ag.routine = ag.routine_for = None
    ag.refuted, ag.refuted_at = {}, {}
    return slot


def _mint(ag, state):
    n0 = len(ag.led.entries)
    ag._mint_routine(state)
    return [e for e in ag.led.entries[n0:] if "routine" in e.event]


def check_can_gates_until():
    """DEFECT: a NESTED guard nobody re-checked -- the durable contamination §3 names.

    The slot's own guard stays reachable, so the mint's first `CAN` passes and only the
    per-guard sweep can catch this. An earlier version patched `can` outright, which the
    SLOT-level check refused first -- so it passed with the per-guard sweep deleted.
    """
    ag = _agent()
    b = dict(ag.env.observe())
    slot = _wide(ag)
    assert ag.can(slot, b) == YES, "fixture: the slot's own guard must stay reachable"
    dead = Rt.Until("no.such.slot", Rt.Act(ag.actions[0]), 3)
    real_enum = Rt.enumerate_routines
    # every candidate carries the unreachable nested guard
    Rt.enumerate_routines = lambda *_a, **_k: [Rt.Until(slot, dead, 5)]
    try:
        rows = _mint(ag, b)
    finally:
        Rt.enumerate_routines = real_enum
    assert ag.can("no.such.slot", b) != YES, "fixture: the nested guard must be unreachable"
    assert ag.routine is None, "committed to a plan whose nested guard is unreachable"
    assert any(e.detail.get("reason", "").startswith("no candidate") for e in rows), (
        "refused, but not for the guard")


def check_trigger_is_the_residual_not_the_reward():
    """DEFECT: the SPARSE reward channel gating the mint, when it is absent most of a run.

    The first version set the goal residual to zero and asserted no mint -- which passes via
    the BARGAIN, because a zero residual gives a zero base that nothing can afford. It said
    nothing about which channel the trigger reads, and the `rg <= 0.0` early return it aimed at
    turns out to be redundant with `pays` for the same reason.

    So: satisfy the REWARD channel completely while the goal residual stays large. A mint keyed
    on `degree` would fall silent; one keyed on the dense channel must not notice.
    """
    ag = _agent()
    b = dict(ag.env.observe())
    slot = _wide(ag)
    assert (ag.goal_residual(slot, b) or 0) > 0, "fixture: the dense channel must still owe"

    class _RewardWasRead(Exception):
        pass

    def _raises(*_a, **_k):
        raise _RewardWasRead("the trigger reached for the reward channel")

    held, ag.env.objective = ag.env.objective, _raises
    try:
        rows = _mint(ag, b)
    except _RewardWasRead:
        raise AssertionError("THE MINT TRIGGER READ THE REWARD CHANNEL -- "
                             "`_route_reward` bins on `degree`, absent for most of a run, "
                             "so a trigger keyed there fires almost never and cannot be "
                             "told from a broken one") from None
    finally:
        ag.env.objective = held

    # THE TREATMENT-EXECUTED CHECK, INSIDE THE CHECK. Without this the assertion above
    # passes when the trigger is never reached at all, which is how the old version was
    # vacuous: an accessor that is never called cannot raise.
    assert rows, ("fixture: the mint wrote no routine row, so the trigger did not run and "
                  "this check proved nothing")


def check_route_is_learned():
    """DEFECT: a routine committing to a step the agent has no evidence for.

    **THE CONTRACT MOVED WITH THE PLAN'S 16 AND THE PROPERTY DID NOT.** This asserted the
    routine's steps ARE the action `_goal_split` returned. A body now holds the INTENT, so that
    comparison is a type mismatch wearing a failure's clothes -- and the seat caught it, which
    is the check doing its job.

    **REINTRODUCED AT THE NEW SHAPE RATHER THAN RELAXED**, and it is now STRICTLY STRONGER,
    because it walks the whole chain instead of one end of it:

        the body holds the intent the agent FORMED
        that intent RESOLVES to the same action the goal exit took

    **Both halves, because either alone passes while the chain is broken** -- the intent can be
    right and unrealisable, or the action right with the body carrying something else entirely.
    """
    ag = _agent()
    b = dict(ag.env.observe())
    _wide(ag)
    _mint(ag, b)
    if ag.routine is not None:
        learned = ag._goal_split(b)       # sets `_goal_want` as it forms it
        want = ag._goal_want
        assert set(Rt.actions(ag.routine)) == {want}, (
            f"routine names {Rt.actions(ag.routine)}, the intent formed is {want}")
        got = ag._realise_step(want, b)
        assert got == learned, (
            f"the body's intent resolves to {got}, the goal exit took {learned}")


def check_shelf_must_be_runnable_here():
    """DEFECT: composing over a settled routine whose action this level does not advertise."""
    ag = _agent()
    b = dict(ag.env.observe())
    slot = _wide(ag)
    ag.routines = [Rt.Until(slot, Rt.Act("ACTION9"), 3)]
    rows = _mint(ag, b)
    # THE ROW, NOT THE OUTCOME. Asserting on what got minted passes vacuously whenever the
    # bargain happens to prefer a valid candidate on price -- which it did, so the earlier
    # version of this check survived the filter being deleted.
    row = next((e.detail for e in rows if e.event in ("routine", "routine_cut")), None)
    assert row is not None and row["shelf"] == 0, (
        f"an unrunnable shelf routine entered the candidate set: shelf={row and row['shelf']}")
    ag2 = _agent()
    b2 = dict(ag2.env.observe())
    s2 = _wide(ag2)
    ag2.routines = [Rt.Until(s2, Rt.Act(ag2.actions[0]), 3)]
    row2 = next((e.detail for e in _mint(ag2, b2)
                 if e.event in ("routine", "routine_cut")), None)
    assert row2 is not None and row2["shelf"] == 1, "a runnable shelf routine was excluded"


def check_one_bargain():
    """DEFECT: a routine bought when it does not pay -- or priced by a second currency.

    **MIGRATED 2026-09-25 UNDER ISAIAH'S RULING, AND THE TEETH ARE UNCHANGED.** He ruled the
    bargain KEEPS ITS PRICE AND LOSES ITS MONOPOLY: `pays` still says whether a plan is worth
    BANKING, and it stops being the only route from wanting to doing, because *the agent is
    always paying with its time* and a refusal that costs nothing lets an agent draft forever
    and look optimal.

    **SO "BOUGHT WITHOUT PAYING" IS NO LONGER THE DEFECT. "BOUGHT WITHOUT PAYING AND WITHOUT
    SAYING WHY" IS**, and that is strictly harder to pass than the original: a plan may now be
    adopted unpaid ONLY IF a `committed_on_accumulation` row names the vector that carried it
    and the bar it crossed. The old version could be satisfied by silence; this one cannot.

    THE SECOND CURRENCY CLAUSE IS UNTOUCHED -- `does-not-pay` must still be the reason on the
    cut row, so the price is still computed and still recorded even when it is overridden.

    **AND IT IS THE ONLY ONE OF THE FIVE THAT WAS A REAL CONFLICT.** With the accumulator on,
    five checks failed; FOUR PASS when the flag is set on the copy rather than during the
    shared warm-up, so their failures were the fixture's TRAJECTORY moving and not their
    contracts. Checked one at a time rather than attributed to a common cause.
    """
    ag = _agent()
    b = dict(ag.env.observe())
    _wide(ag)
    ag.goal_residual = lambda _s, _st, **_k: 0.02  # a real residual, too small to buy a plan
    rows = _mint(ag, b)
    assert any(e.detail.get("reason") == "does-not-pay" for e in rows), "wrong reason"
    if ag.routine is None:
        return                                  # refused on price, as it always could
    crossed = [e.detail for e in rows if e.event == "committed_on_accumulation"]
    assert crossed, "bought a plan the bargain could not afford, and said nothing"
    d = crossed[-1]
    assert d.get("total", 0) >= d.get("threshold", 1e9), (
        f"committed on an accumulation that did not cross: {d}")
    assert d.get("vector"), "committed without naming a single contribution"


def check_until_terminates():
    """DEFECT: `Until` on a guard that never holds, running forever."""
    out, cur = [], Rt.Until("never", Rt.Act("A"), 4)
    for _ in range(50):
        emit, rest = Rt.advance(cur, lambda _g: False)
        if emit in (Rt.DONE, Rt.BLOCKED, Rt.EXHAUSTED):
            break
        out.append(emit)
        cur = rest
    assert emit == Rt.EXHAUSTED, f"ended {emit}, not exhausted"
    assert len(out) == 4, f"ran {len(out)} steps against a budget of 4"


def check_endings_stay_apart():
    """DEFECT: an unreadable guard reported as a satisfied one."""
    assert Rt.advance(Rt.Until("g", Rt.Act("A"), 3), lambda _g: None)[0] == Rt.BLOCKED
    assert Rt.advance(Rt.When("g", Rt.Act("A")), lambda _g: None)[0] == Rt.BLOCKED
    assert Rt.advance(Rt.When("g", Rt.Act("A")), lambda _g: False)[0] == Rt.DONE


def check_the_plan_language_can_hold_a_choice():
    """DEFECT: a two-armed branch that runs an arm it never chose.

    **THE ACT SPACE HAD NO DECISION IN IT.** `When` collapses *the guard is false* into *there
    is nothing to do*, so every plan the agent could write said DO THIS IF ALLOWED and none said
    CHOOSE BETWEEN THESE. Four claims, and the third is the one a branch makes easy to get wrong.
    """
    a, b = Rt.Act("A"), Rt.Act("B")
    ch = Rt.Choose("g", a, b)

    # 1 -- BOTH ARMS ARE REACHABLE, which is the whole of what `When` could not do.
    assert Rt.advance(ch, lambda _g: True)[0] == "A"
    assert Rt.advance(ch, lambda _g: False)[0] == "B", "the false arm is unreachable"

    # 2 -- AN UNREADABLE GUARD BLOCKS. Not the else arm: *I could not read it* is not *it is
    # false*, and here the wrong answer ACTS instead of doing visibly nothing.
    assert Rt.advance(ch, lambda _g: None)[0] == Rt.BLOCKED

    # 3 -- REACH IS THE ARM IT CAN BE HELD TO. `max` would price the branch on the better arm
    # and then take the other, which is the over-statement `reach` exists to refuse.
    wide = Rt.Choose("g", Rt.Seq(a, b), a)
    assert Rt.reach(wide) == 1, f"reach {Rt.reach(wide)} -- priced on the arm it may not take"
    assert Rt.length(wide) == 5, f"length {Rt.length(wide)} -- an arm went uncounted"

    # 4 -- THE ENVIRONMENT CHECK SEES THE ELSE ARM. A routine whose unchosen arm names an
    # unadvertised action must be refusable BEFORE the guard is ever read.
    assert set(Rt.actions(ch)) == {"A", "B"}, "an arm is invisible to the level-boundary check"

    # 5 -- AND THE COMPOSER ACTUALLY BUILDS ONE, so this is not a seventh dead constructor.
    # Two different arms are the precondition; with one action there is no choice to make.
    got = Rt.enumerate_routines(("A",), ("g",), (Rt.Act("B"),), 1, cap=500)
    assert any(isinstance(r, Rt.Choose) for r in got), "the composer never enumerates a branch"
    assert not any(isinstance(r, Rt.Choose) and Rt.render(r.body) == Rt.render(r.otherwise)
                   for r in got), "a branch whose arms are the same routine"


def check_a_guard_can_say_more_than_one_slot():
    """DEFECT: a compound guard that is free, or that loses the slot it could not read.

    **A GUARD WAS ONE SLOT NAME**, so a routine could only ever terminate on *this one
    objective is satisfied*. `condition.py` had the grammar and no importer -- its OTHER half,
    conditions derived from corpus prose, censused at `DRAFTABLE 0` (`F299`/`F300`).
    """
    import condition as C
    slotname = "o1.dcol"

    # 1 -- THE PRICE OF EVERY ROUTINE THE AGENT HAS EVER BUILT IS UNCHANGED. `_guard_excess`
    # charges the EXCESS over one, so a bare slot-name guard still costs what it always did.
    plain = Rt.Until(slotname, Rt.Act("A"), 3)
    assert Rt.length(plain) == 2, f"a plain guard's price moved: {Rt.length(plain)}"
    node = Rt.Until(C.Slot(slotname), Rt.Act("A"), 3)
    assert Rt.length(node) == 2, "a one-slot node is not priced as a leaf"

    # 2 -- AND A GUARD THAT SAYS MORE PAYS MORE. Without this `or` is a free loosening: it is
    # easier to satisfy than either side, so the agent could win the bargain by saying less.
    loose = Rt.Until(C.Bool("or", C.Slot(slotname), C.Slot("o2.dcol")), Rt.Act("A"), 3)
    assert Rt.length(loose) == 4, f"a compound guard costs {Rt.length(loose)}, not 4"
    assert C.size(C.Bool("or", C.Slot("a"), C.Slot("b"))) == 3

    # 3 -- THE WIRE, AND THE TWO MEANINGS KEPT APART. `A6i`, mine: `condition.py`'s grammar
    # makes a bare SLOT an EXPRESSION, so it is the slot's VALUE -- and the first reader
    # returned its SATISFACTION PREDICATE for the same node. Both readings are well-formed,
    # which is why only a `Cmp` would ever have shown it, as a clean wrong answer.
    sat = tether._SAT
    ag = _agent()
    slot = _wide(ag)
    b = dict(ag.env.observe())
    h = ag._holds(b)
    assert h(C.Slot(sat + slot)) == h(slot), "the predicate and its name disagree"
    assert h(C.Slot(slot)) == b.get(slot), "a bare slot is not reading its VALUE"

    # AND THE COMPARISON THE FIX UNLOCKS: a guard that says something about the WORLD rather
    # than about the agent's own objectives, evaluated over numbers and not over booleans.
    assert h(C.Cmp("==", C.Slot(slot), b.get(slot))) is True, "a value comparison is broken"
    gone = h(C.Cmp("==", C.Slot(slot), C.Slot("no.such.slot")))
    assert gone is None, "an absent operand is not UNKNOWN"

    # 4 -- KLEENE SURVIVES THE WIRE. An unreadable conjunct can never produce a satisfied
    # guard: *I could not read it* is not *it holds*, at the site that terminates a loop.
    n0 = len(ag.led.entries)
    both = h(C.Bool("and", C.Slot(sat + slot), C.Slot(sat + "no.such.slot")))
    assert both is not True, "a conjunction held on a conjunct nothing could read"

    # 5 -- AND THE PER-SLOT SIGNAL SURVIVES IT, which is what makes this composition and not
    # aggregation. The unreadable slot is named in its own row rather than averaged away.
    rows = [e.detail for e in ag.led.entries[n0:] if e.event == "guard_unreadable"]
    assert any(e.slot == "no.such.slot" for e in ag.led.entries[n0:]
               if e.event == "guard_unreadable"), f"the conjunct that failed is unnamed: {rows}"

    # 6 -- AND THE COMPOSER FORMS THEM, so this is not a grammar with no producer a second time.
    made = ag._compound_guards(slot, (slot, "o2.dcol"))
    assert made, "no compound guard is ever offered"
    assert all(slot in str(g) for g in made), "a compound guard does not mention its subject"
    # AND THE INVARIANT THE TWO MEANINGS NEED: a bare SLOT is a VALUE, so it may appear only
    # as an OPERAND of a comparison. Anywhere else it is being read as a claim, which is the
    # A6i this pair of commits exists to close.
    def bare(node, in_cmp=False):
        if isinstance(node, C.Slot):
            return [] if (in_cmp or node.name.startswith(sat)) else [str(node)]
        if isinstance(node, C.Cmp):
            return bare(node.left, True) + bare(node.right, True)
        if isinstance(node, C.Not):
            return bare(node.inner)
        if isinstance(node, C.Bool):
            return bare(node.left) + bare(node.right)
        return []
    loose = [x for g in made for x in bare(g)]
    assert not loose, f"a bare slot is read as a claim: {loose}"
    assert any(isinstance(g, C.Cmp) for g in made), "no guard ever says anything about the board"


def check_every_book_key_is_declared():
    """DEFECT: a book key that only exists once it increments, so its ZERO is invisible.

    **THREE TIMES IN ONE NIGHT, THE LAST AN HOUR AFTER THE FIRST TWO WERE FIXED** -- gate 1's
    tally, `plan_gate_no_hypothesis`, the bargain book. **A zero is the most informative reading
    a book has** (*not one candidate reached `pays`*, *the agent holds no goal hypothesis*) and
    all three of those zeros read as ABSENT, which cannot be told from never-recorded.

    `tether.BOOKS` removes the class by construction. This stops a NEW key re-entering it, and
    is the arms seat's rule one level down: **a key cannot enter silently, which is how the
    other three got in.**
    """
    import re
    src = (pathlib.Path(tether.__file__)).read_text(encoding="utf-8")
    # BOTH WRITE PATHS. Direct subscripting, and `_book_add`, which exists because a grep
    # cannot guard a CONSTRUCTED key -- the depth buckets evaded this check entirely until the
    # write site started validating them itself.
    lit = set(re.findall(r'book\[\"([a-z_]+)\"\]', src))
    lit |= set(re.findall(r'book\.get\(\"([a-z_]+)\"', src))
    lit |= set(re.findall(r'_book_add\([^,]+,\s*\"([a-z_]+)\"', src))
    missing = sorted(lit - set(tether.BOOKS))
    assert not missing, f"book keys written but not declared in BOOKS: {missing}"

    # AND THE DECLARATION IS NOT A LIST OF NAMES NOBODY WRITES. A stale row is the other half:
    # it would report a zero forever for a quantity nothing measures, which is worse than
    # silence, because it looks like evidence.
    stems = set(re.findall(r'book\[f\"([a-z_]+)\{', src))
    stems |= set(re.findall(r'_book_add\([^,]+,\s*f\"([a-z_]+)\{', src))
    unwritten = [k for k in tether.BOOKS
                 if k not in lit and not any(k.startswith(x) for x in stems)]
    assert not unwritten, f"BOOKS declares keys nothing writes: {unwritten}"

    # AND THE RUNTIME HALF, BECAUSE a CONSTRUCTED key cannot be caught by a grep. The static
    # check above compares LITERALS against BOOKS; `arrived_at_depth_{d}` and `plan_gate_{k}`
    # are assembled at runtime, so removing a declared bucket is INVISIBLE to it -- which is how
    # all nine depth buckets stayed undeclared and uninitialised. `_book_add` validates where
    # the key is built, and that is the only place a constructed key can be checked at all.
    tether._book_add({}, "arrived_at_depth_3")          # declared: accepted
    try:
        tether._book_add({}, "arrived_at_depth_99")
        raise AssertionError("an undeclared book key was accepted at the write site")
    except KeyError:
        pass

    # AND A FRESH AGENT HAS EVERY ONE AT ZERO, which is the property the class needed.
    ag = _agent(cycles=1)
    zero = [k for k in tether.BOOKS if k not in ag.gamma.book]
    assert not zero, f"a declared book key is absent from a live agent: {zero}"

    # AND THEY SURVIVE A LOAD, which is the route the declaration could not close from where
    # it sits. `arc_holdout` constructs the Agent and loads the library AFTER -- so an
    # assignment in `load` wipes every key the saved blob predates. Measured before the fix:
    # 12 keys became 1. **Eleven quantities silently absent for a whole attempt**, which is the
    # silent-zero class arriving through PERSISTENCE.
    import json
    import tempfile
    old_blob = {"terms": [], "invented": [], "vindication": [],
                "book": {"promoted_then_wrong": 3}}
    path = pathlib.Path(tempfile.gettempdir()) / "m2_oldlib.json"
    path.write_text(json.dumps(old_blob), encoding="utf-8")
    ag.gamma.load(str(path))
    gone = [k for k in tether.BOOKS if k not in ag.gamma.book]
    assert not gone, f"an OLD library WIPED declared book keys: {gone}"
    # AND THE CONTROL: what the blob DID carry is restored, not flattened to the default.
    assert ag.gamma.book["promoted_then_wrong"] == 3, "the load stopped restoring"


def check_a_plan_can_have_a_fallback():
    """DEFECT: a fallback that recovers SILENTLY, hiding the ending it recovered from.

    **`F207`: the first routine this project ever formed died at `routine_end: blocked`**, and
    a blocked routine is abandoned -- nothing in the ACT space could say *and if that does not
    work, do this instead*. `Try` branches on the OUTCOME where `Choose` branches on a GUARD
    read before acting; **neither substitutes for the other.**
    """
    a, b = Rt.Act("A"), Rt.Act("B")

    # 1 -- IT RECOVERS FROM BLOCKED, which is the ending that had no answer.
    st: dict = {}
    blocked = Rt.Try(Rt.When("g", a), b)
    assert Rt.advance(blocked, lambda _g: None, None, st)[0] == "B", "no recovery from blocked"

    # 2 -- AND THE RECOVERY IS PUBLISHED. A routine that recovers quietly has destroyed the
    # BLOCKED signal -- the ending F207 was diagnosed from -- while looking like robustness.
    assert st.get("recovered") == [Rt.BLOCKED], f"the failure is unrecorded: {st}"

    # 3 -- AND NEVER FROM `DONE`. Three endings are three claims; folding DONE in would run
    # the fallback after every success.
    st2: dict = {}
    assert Rt.advance(blocked, lambda _g: False, None, st2)[0] == Rt.DONE
    assert "recovered" not in st2, "a succeeding body was reported as recovered"

    # 4 -- EXHAUSTED RECOVERS TOO, and it is a different claim from blocked: the budget went.
    st3: dict = {}
    spent = Rt.Try(Rt.Until("g", a, 0), b)
    assert Rt.advance(spent, lambda _g: False, None, st3)[0] == "B"
    assert st3.get("recovered") == [Rt.EXHAUSTED], f"exhausted is not distinguished: {st3}"

    # 5 -- A FAILED BODY'S CLAIM IS DISCARDED. `Expect` publishes as it is walked, so a body
    # that publishes and THEN fails would leave its claim standing -- and the caller attributes
    # the pending claim to the action the step emits, which by then is the FALLBACK's.
    # Metacognition would record "I expected this to move" about a routine abandoned before
    # acting. A FALSE ROW, which is worse than a missing one.
    st4: dict = {}
    leak = Rt.Try(Rt.Expect("o1.dcol", Rt.When("g", a)), b)
    assert Rt.advance(leak, lambda _g: None, None, st4)[0] == "B"
    assert not st4.get("expect"), f"a failed body's CLAIM survived onto the fallback: {st4}"
    assert st4.get("recovered") == [Rt.BLOCKED], "the recovery went unrecorded"

    # AND A CLAIM FROM A BODY THAT SUCCEEDS IS KEPT -- the control, without which the rule
    # above is a mute rather than a fix.
    st5: dict = {}
    kept = Rt.Try(Rt.Expect("o1.dcol", a), b)
    assert Rt.advance(kept, lambda _g: True, None, st5)[0] == "A"
    assert st5.get("expect") == ["o1.dcol"], f"a live claim was discarded: {st5}"

    # 6 -- PRICED AND REACHED LIKE ANY OTHER OBJECT: both arms counted, reach held to the
    # lesser, and the composer actually builds one.
    assert Rt.length(Rt.Try(a, b)) == 3, "an arm went uncounted"
    assert Rt.reach(Rt.Try(Rt.Seq(a, b), a)) == 1, "priced on the arm it may not take"
    got = Rt.enumerate_routines(("A",), ("g",), (Rt.Act("B"),), 1, cap=500)
    assert any(isinstance(r, Rt.Try) for r in got), "the composer never enumerates a fallback"


def check_the_composer_can_propose_a_fold():
    """DEFECT: the interpreter maps elementwise and the enumerator cannot propose a chain
    that does -- `F347`.

    **`Term.apply` maps ANY non-reducer across a `Cells`** and says so at its own site, so
    `cells . cell_row . parity . count_true` RUNS. `enumerate_closure` walked the type graph,
    where the running type after `cells` is `CELLS` and **`count_true` is the only atom that
    accepts it** -- so **0 of 87,244 enumerated chains contained a per-cell atom**, and the one
    fold on offer was `cells . count_true`, which `count_true` refuses.

    **BUILT WITHOUT A RULING BECAUSE IT IS INERT WITHOUT ONE**: `cells` is the only producer of
    `CELLS` and exists only under `TETHER_ITERATE`, so with the arm off this cannot execute.
    """
    from gamma import CELL, CELLS, Atom, Ctx, Gamma
    from sensors import BOOL, NOT_RESOLVED

    # A STANDALONE TYPE GRAPH, so the claim does not depend on the arm's state in this process.
    cells = Atom("cells_", lambda v, _c: v, "SHAPE", CELLS)
    row = Atom("row_", lambda v, _c: v, CELL, "POSITION")
    par = Atom("par_", lambda v, _c: v, "POSITION", BOOL)
    red = Atom("red_", lambda v, _c: v, CELLS, "EXTENT", elem_type=BOOL)
    g = Gamma([cells, row, par, red])
    names = {c.name for c in g.enumerate_closure("SHAPE", "EXTENT", 4, 500, {})}

    # 1 -- THE FOLD THE MODULE WAS WRITTEN FOR IS NOW CONSTRUCTIBLE.
    assert "cells_ . row_ . par_ . red_" in names, f"the fold is unreachable: {names}"

    # 2 -- AND AN UNCLOSED ITERATION IS NOT A TERM. Its value is a `Cells` whatever the last
    # atom's out_type says, so it may only be emitted once a reducer has closed it.
    open_ = [n for n in names if n.endswith("cells_") or n.endswith("row_")]
    assert not open_, f"an unclosed iteration was emitted: {open_}"

    # 3 -- AND THE REDUCER'S RUNTIME REFUSAL IS NOW A TYPE FACT. `red_` requires BOOL elements,
    # so a chain handing it coordinates is NOT OFFERED rather than offered and abstaining --
    # the same principle as refusing `<` over an unordered type.
    assert "cells_ . red_" not in names, "a fold that must abstain is still offered"
    assert "cells_ . row_ . red_" not in names, "a fold over non-booleans is still offered"

    # 4 -- AND WITH NO COLLECTION IN THE GRAPH NOTHING CHANGES, which is why this needed no
    # ruling: the whole mechanism is unreachable unless an atom produces a `CELLS`.
    flat = Gamma([Atom("a_", lambda v, _c: v, "SHAPE", "POSITION"),
                  Atom("b_", lambda v, _c: v, "POSITION", "EXTENT")])
    plain = {c.name for c in flat.enumerate_closure("SHAPE", "EXTENT", 3, 99, {})}
    assert plain == {"a_ . b_"}, f"the plain type walk changed: {plain}"

    # 5 -- AND IT RUNS, WHICH IS A DIFFERENT CLAIM FROM *IT TYPE-CHECKS*. Everything above is
    # about what the composer can PROPOSE. This is the project's own standing rule -- no arm's
    # readings are generalised until the arm has EXECUTED -- applied to my own work, and it
    # needs no board: build the real chain, hand it a shape, read the number.
    real = {a.name: a for a in arc_atoms._iterate()}
    real.update({a.name: a for a in arc_atoms.three_spaces(arc_predict.predict())})
    shape = frozenset({(0, 0), (0, 1), (1, 0), (2, 2), (3, 1)})     # rows 0 0 1 2 3
    ctx = Ctx(action=None, operands=(), touching=None, group=(), obj=None, shapes={})
    fold = gamma.Term(tuple(real[n] for n in
                            ("cells", "cell_row", "parity", "count_true")))
    assert fold.apply(shape, ctx) == 2, "the fold does not count the odd rows"

    # AND THE DEGENERATE ONES ABSTAIN, which is WHY they must not be offered: they are not
    # wrong, they are silent, and a silent candidate spends budget to say nothing.
    for chain in (("cells", "count_true"), ("cells", "cell_row", "count_true")):
        bad = gamma.Term(tuple(real[n] for n in chain))
        assert bad.apply(shape, ctx) is NOT_RESOLVED, f"{chain} returned a number"


def check_the_tree_is_judged_by_its_own_bound():
    """DEFECT: a tree excluded by `_cannot_pay` computed on its FLAT PARENT.

    **ISAIAH'S RULING, 2026-09-24: that is a defect, not a policy.** A tree `f<g(s)>` is a
    DIFFERENT FUNCTION from `f` and can be right where `f` is wrong, so the parent's bound says
    nothing about it -- and the bound's whole value is that it is NECESSARY *for the term it
    was computed on*. `_trees` was called ZERO times because of it (`F348`).

    **AND THE REPAIR IS BYTE-IDENTICAL WHERE THE BOUND WAS ALREADY CORRECT**, which is the
    ruling's condition. The survivor branch now applies the tree's own `_cannot_pay` BEFORE
    `pays` -- and that changes no outcome, because the first IMPLIES the second.
    """
    # 1 -- THE IMPLICATION THAT MAKES IT A SHORT-CIRCUIT RATHER THAN A NEW FILTER.
    # `_cannot_pay` proves `cost + log2(V)*wrong >= base`, and `left` is at least
    # `log2(V)*wrong` -- so anything it refuses, `pays` refuses too. Asserted over the
    # arithmetic rather than asserted in prose.
    for cost, wrong, unit, base in ((3.0, 2, 2.0, 5.0), (1.0, 4, 2.0, 8.0),
                                    (0.5, 1, 3.0, 2.0), (9.0, 0, 2.0, 4.0)):
        proved = cost + unit * wrong >= base
        if proved:
            assert not pays(cost, unit * wrong, base), (
                f"_cannot_pay proved it cannot pay, yet pays() admitted it: "
                f"cost={cost} left={unit * wrong} base={base}")

    # 2 -- AND THE ARM IS GONE. It was a workaround for the defect; the ruling replaced it
    # with the repair, so a reader must not find a switch that no longer gates anything.
    assert not hasattr(tether, "_TREE_BOUND"), "the workaround arm survived the repair"

    # 3 -- THE RULING'S SUBSTANCE, NOT ITS LETTER (decision 2, 2026-10-06): NO TREE THAT COULD PAY
    # IS WITHHELD. This asserted a source string -- that the bounded-out branch calls `_trees` --
    # which any exact cut trips. Now behavioural, on a real mint, in two halves that together
    # imply it: (i) a refused term whose trees were NOT offered already cost `base` on its own;
    # (ii) a tree never costs less than its chain (`gamma.length` adds the operand, or is 1 for
    # a settled unit either way). The planted violation, `withhold`, proves (i) can fire.
    assert _withheld_trees_could_not_pay() > 0, "fixture: no mint refused anything to check"
    try:
        _withheld_trees_could_not_pay(withhold=True)
    except AssertionError as e:
        assert "withheld" in str(e), e
    else:
        raise AssertionError("PLANTED: trees withheld under a payable chain, and nothing fired")


def _withheld_trees_could_not_pay(withhold: bool = False) -> int:
    """Mint every slot of a warmed agent, recording each refused term and each tree request;
    assert (i) and (ii) above. `withhold` plants the violation: no trees offered at all."""
    ag = _agent()
    units = tuple(ag.gamma.units())
    refused, asked = [], set()
    real_cp, real_trees = ag._cannot_pay, ag._trees

    def cp(term, slot, robs, cost, base, *a, **k):
        out = real_cp(term, slot, robs, cost, base, *a, **k)
        if out and term.operand_term is None:
            refused.append((term, cost, base))
        return out

    def trees(cand, bind, g, slot=None):
        if withhold:                  # withheld: asked for, never produced -- not offered
            return []
        asked.add((tuple(a.name for a in cand.atoms), bind, g))
        built = list(real_trees(cand, bind, g, slot))
        chain = tether.term_bits(ag.gamma.length(gamma.Term(cand.atoms), units), ag.gamma.alphabet)
        for bt in built:
            assert tether.term_bits(ag.gamma.length(bt, units), ag.gamma.alphabet) >= chain, (
                f"(ii) a tree is cheaper than its chain: {bt.name}")
        return built
    ag._cannot_pay, ag._trees = cp, trees
    for slot in sorted(ag.slots):
        ag.mint(slot)
    for term, cost, base in refused:
        key = (tuple(a.name for a in term.atoms), term.operand, term.guard)
        assert key in asked or cost >= base, (
            f"(i) trees withheld under a chain that could still pay: {term.name} "
            f"cost {cost:.2f} < base {base:.2f}")
    return len(refused)


def check_chunking_reaches_the_bargain():
    """The ARITHMETIC of chunking: a settled routine counts as one unit and that can flip `pays`.

    **THIS IS NOT A CAPABILITY CHECK AND MUST NOT BE READ AS ONE.** It was, for four ticks: it
    passes on a HAND-BUILT pair and says nothing about whether the agent's own composer ever
    selects a chunk. It even falsifies correctly against the arithmetic, which is why breaking
    the mechanism did not expose it. `check_composer_cannot_yet_win` is the honest companion.
    """
    nav = Rt.Until("g1", Rt.Act("A"), 8)
    plan = Rt.Seq(nav, Rt.Seq(Rt.Act("B"), Rt.Until("g2", Rt.Act("A"), 8)))
    assert Rt.length(plan, (nav,)) < Rt.length(plan), "a settled routine did not count as one unit"
    n, base = 3, 9 * math.log2(3)
    assert not pays(term_bits(Rt.length(plan), n), 0.0, base)
    assert pays(term_bits(Rt.length(plan, (nav,)), n), 0.0, base), (
        "chunking changed the length and not what the bargain affords")


def check_composer_cannot_yet_win():
    """RECORDS A KNOWN LIMITATION AS A CHECK, so it cannot be forgotten or quietly fixed.

    `budget` is derived as `unsat` and `reach(Until) = budget * reach(body)`, so the simplest
    loop's reach EQUALS the residual and its `left` is identically zero. **Nothing the composer
    offers can beat it; the chunked form only ties.** `unsat` is serving as both a BOUND (what
    the agent allows) and an EXPECTATION (what it will achieve) -- `A6i`, and their ratio is 1
    by construction.

    **This check FAILS THE DAY THAT IS FIXED**, which is the point: it is a tripwire on a
    recorded limitation, not an endorsement of it.
    """
    n = 3
    for unsat in (5, 9, 14):
        plain = Rt.Until("g", Rt.Act("A"), unsat)
        best = term_bits(Rt.length(plain), n) + max(0.0, unsat - Rt.reach(plain)) * math.log2(n)
        assert unsat - Rt.reach(plain) <= 0.0, "the plain loop no longer trivially reaches"
        for rival, chunks in ((Rt.Until("g", Rt.Until("g2", Rt.Act("A"), 3), unsat),
                               (Rt.Until("g2", Rt.Act("A"), 3),)),
                              (Rt.Seq(plain, Rt.Act("A")), ()),
                              (Rt.When("g2", plain), ())):
            tot = (term_bits(Rt.length(rival, chunks), n)
                   + max(0.0, unsat - Rt.reach(rival)) * math.log2(n))
            assert tot >= best, (
                f"a composed shape now BEATS the plain loop at unsat={unsat} -- "
                "the limitation is fixed and this tripwire should be retired")


def check_only_a_trial_refutes():
    """DEFECT: `I could not read the guard` recorded as `this plan does not work`."""
    ag = _agent()
    b = dict(ag.env.observe())
    slot = _wide(ag)
    ag.routine = Rt.Until(slot, Rt.Act("NOT_ADVERTISED"), 3)
    ag.routine_for = slot
    n0 = len(ag.led.entries)
    ag.choose(b)                              # ends `unadvertised` -- a non-trial
    assert not ag.refuted, "a non-trial was recorded as a refutation"
    rows = [e for e in ag.led.entries[n0:] if e.event == "routine_end"]
    assert rows and rows[-1].detail.get("status") != "refuted", (
        "a non-trial was RECORDED as a refutation even though none was filed")


def check_a_refutation_is_a_row():
    """DEFECT: a decision input that leaves no trace.

    A TERM's demotion is a first-class event carrying `asked`, `ground_said`, `verdict` and
    `rejections`. A routine's refutation was in-memory state only -- and it GATES FUTURE
    MINTING, so `speak` could not say it, the gate could not check it, and express-before-judge
    was unverifiable from the record.
    """
    ag = _agent()
    slot = _wide(ag)
    b = dict(ag.env.observe())
    ag.routine = Rt.Until(slot, Rt.Act(ag.actions[1]), 1)
    ag.routine_for = slot
    n0 = len(ag.led.entries)
    for _ in range(4):
        if ag.routine is None:
            break
        ag.choose(b)
    row = next((e.detail for e in ag.led.entries[n0:]
                if e.event == "routine_end" and e.detail.get("outcome") == "exhausted"), None)
    assert row is not None, "fixture: the routine did not exhaust"
    assert ag.refuted, "fixture: nothing was refuted in memory"
    for field in ("asked", "ground_said", "verdict", "rejections", "reopens_above"):
        assert field in row, f"the refutation row omits {field!r}, which `demote` carries"
    assert row["status"] == "refuted"


def check_refutations_do_not_cross_a_boundary():
    """DEFECT: rejecting a routine on a new level for what happened to a dead slot."""
    ag = _agent()
    slot = "o1.dcol"
    k = ag._reject_key(slot, Rt.Until(slot, Rt.Act("ACTION2"), 3))
    ag.refuted[k] = gamma.Standing(last_tick=0)
    ag.refuted[k].refute(0)
    ag.refuted_at[k] = 0.5
    ag.retarget(ag.env, ag.level + 1)
    assert not ag.refuted, "a refutation keyed on a dead slot name survived a boundary"


def check_slot_keyed_state_does_not_cross_a_boundary():
    """DEFECT: `retarget` clears the bindings and trends because *the slots did not survive*, and
    kept seven stores keyed by those same slots -- so a want formed on the old level's `o1.dcol`
    was read on the new level's `o1.dcol`."""
    ag = _agent()
    slot = "o1.dcol"
    k = ag._reject_key(slot, Rt.Until(slot, Rt.Act("ACTION2"), 3))
    ag.wants[slot] = "idn"
    ag._want_terms[slot] = ag.gamma.library["idn"]
    ag._reach_tested[k] = "tested_no"
    ag._prev_gap[slot], ag._gap_delta[slot] = 3, -1
    ag._undone[((), "BECOME o1.dcol +", slot, 0.5)] = 2
    ag._undone_across[("BECOME o1.dcol +", slot)] = 2
    ag.retarget(ag.env, ag.level + 1)
    held = {n: getattr(ag, n) for n in ("wants", "_want_terms", "_reach_tested", "_prev_gap",
                                         "_gap_delta", "_undone", "_undone_across")}
    crossed = [n for n, v in held.items() if v]
    assert not crossed, f"slot-keyed state crossed a boundary: {crossed}"


def check_one_clock_at_the_agents_rate():
    """DEFECT: two clocks. Terms decayed on the trace length, which a level boundary resets, so a
    rejection FROZE at every boundary; routines decayed on the cycle at the module's seed rate,
    while the agent's own halflife is measured in cycles (Isaiah 2026-09-30: the rate is its).
    """
    ag = _agent()
    name = next(iter(ag.gamma.library))
    ag.gamma.refute(name)
    r0 = ag.gamma.rejection_of(name)
    ag.retarget(ag.env, ag.level + 1)
    for _ in range(3):
        ag.step()
    assert ag.gamma.rejection_of(name) < r0, "a term's rejection froze at a level boundary"
    slot = _wide(ag)
    k = ag._reject_key(slot, Rt.Until(slot, Rt.Act(ag.actions[1]), 1))
    ag.refuted[k] = gamma.Standing(last_tick=ag.cycle, rejections=1.0)
    ag.gamma.halflife = 2.0
    ag.cycle += 2
    assert abs(ag._rejection(k) - 0.5) < 1e-9, (
        "a routine refutation decayed at a seed, not the agent's rate")


def check_a_refusal_holds_until_the_scope_grows():
    """DEFECT: a refused plan readmitted by a clock, with nothing new to try it with (Fig 6:
    *it becomes reachable again only if something new is minted, which is growth*).

    The exhaustion is driven through `choose`, as `check_a_refutation_is_a_row` drives it, so the
    refusal is filed by the code that files it. The OLD filter is read beside the new one: one
    cycle on, `_rejection` has decayed under 1.0 and would have readmitted the plan, which is
    what makes the first half of this check non-vacuous.
    """
    ag = _agent()
    slot = _wide(ag)
    b = dict(ag.env.observe())
    plan = Rt.Until(slot, Rt.Act(ag.actions[1]), 1)
    ag.routine, ag.routine_for = plan, slot
    for _ in range(4):
        if ag.routine is None:
            break
        ag.choose(b)
    assert ag._refusals, "fixture: the routine did not exhaust, so nothing was refused"
    key, n_held = next((k, len(v)) for k, v in ag._refusals.items())
    assert ag._refused(key), "a plan was not refused under the scope it failed in"
    k = ag._reject_key(slot, plan, ag.routine_lib)
    ag.cycle += 1
    assert ag._rejection(k) < 1.0, "fixture: the old filter would not have readmitted it"
    assert ag._refused(key), "a refused plan came back with the clock, nothing having grown"
    ag.retarget(ag.env, ag.level + 1)
    assert ag._refused(key), "an advance lifted a refusal about a plan's shape"
    lib = ag.gamma.library
    new = next(ag.gamma.build((a.name, a.name)) for t in list(lib.values()) for a in t.atoms[:1]
               if f"{a.name} . {a.name}" not in lib)
    ag.gamma.accept(new, seq=0, residual="fixture")
    assert not ag._refused(key), "the scope grew and the refusal still excluded"
    assert len(ag._refusals[key]) == n_held, "lifting a refusal removed it from the record"



def check_the_act_space_stays_narratable():
    """DEFECT: a new ledger step that the whitebox narration cannot trace.

    `speak.verify` is the legibility guarantee -- every sentence traces to a record -- and the
    only seat that exercises it is `demo`, whose toy world **never mints a routine**. So the
    `PLAN` step and every routine row have never been narrated by anything that gates a commit.
    """
    import json

    import speak
    ag = _agent()
    _wide(ag)
    for _ in range(8):
        ag.step()
    rows = [json.loads(json.dumps(r, default=str)) for r in ag.led.rows()]
    plan = [r for r in rows if r.get("step") == "PLAN"]
    assert plan, "fixture: no PLAN row was written"
    said = speak.sentences(rows)
    v = speak.verify(rows, said)
    assert v["orphans"] == 0, f"{v['orphans']} sentences trace to no record: {v['examples'][:2]}"
    assert v["traceable"], "the narration stopped being traceable with the ACT space present"

    # AND THE OTHER DIRECTION, WHICH `orphans` CANNOT SEE. `verify` counts SENTENCES that trace
    # to no record; an EVENT that no sentence covers is invisible to it, so the narration can
    # go quiet about a whole kind of thing and still score perfectly. **Measured when this was
    # written: `routine_recovered` (ten minutes old, mine) and `guard_unreadable` -- the row
    # `F207` was diagnosed from -- had no sentence at all.**
    #
    # A DENOMINATOR, NOT AN ERROR HUNT: every ACT-space event tether can write is the
    # population, and the assertion is that the population is covered.
    # **THE POPULATION IS DECLARED AND PARTIAL, AND SAYING SO IS THE POINT.** `speak` does not
    # narrate every ledger event and should not -- most are internal bookkeeping. What it MUST
    # narrate is the agent's ACCOUNT OF ITSELF, and that is a list, not a rule.
    #
    # **IT WAS `routine`/`guard` ONLY, AND THE BOOKS WERE MISSING.** The books are what let the
    # agent set a term instead of guessing one, and `speak` could not say one of them -- so the
    # narration described what the agent DID and never what it KNOWS ABOUT ITSELF. I fixed the
    # ACT-space instance two hours earlier and left the class, which is `I25` again.
    #
    # A TABLE, NOT LOGIC, for `conform/lint.py`'s reason: *a table can be pinned; logic widens
    # quietly.* A new self-account event is added HERE, deliberately, or it is not covered --
    # and a reader can see which it is.
    SELF_ACCOUNT = ("routine", "guard", "books")
    import re
    tsrc = pathlib.Path(tether.__file__).read_text(encoding="utf-8")
    events = {e for e in re.findall(r'led\.record\([^)]*?"([a-z_]+)"\s*[,)]', tsrc, re.S)
              if e.startswith(SELF_ACCOUNT)}
    ssrc = pathlib.Path(speak.__file__).read_text(encoding="utf-8")
    narrated = set(re.findall(r'ev == "([a-z_]+)"', ssrc))
    silent = sorted(events - narrated)
    assert not silent, f"every ACT-space event has a sentence -- these do not: {silent}"
    # ORPHANS ALONE IS VACUOUS HERE AND THE FIRST VERSION STOPPED THERE. `speak` cited 0 of 2
    # PLAN rows, so there was nothing to orphan and the check passed on an unnarrated space.
    cited = {i for s in said for i in s[0]}
    missed = [r.get("event") for r in plan if r.get("seq") not in cited]
    assert not missed, f"the narration cannot say the ACT space: {missed}"


def check_a_plan_that_succeeds_shelves_itself():
    """DEFECT: `done` treated as any other ending. It is the ONLY path onto the chunk shelf.

    The suite reached `exhausted`, `unadvertised`, `refused` and `cut` and had never once seen a
    plan SUCCEED -- which is why every chunking check has to hand-plant `ag.routines`.

    **AND THE FIXTURE WAS A NO-OP, WHICH THIS CHECK'S OWN NAME REFUSES -- 2026-09-25.** It
    stubbed `goal_residual` at 0.0 FROM THE FIRST CALL, so the guard held before the routine
    ran: `advance` returned `DONE` having emitted NOTHING. The assertion says *a plan that
    ACHIEVED ITS GUARD* and the check is named *a plan that SUCCEEDS* -- **a plan whose guard
    was already true did not achieve anything, it arrived.**

    The assertion is UNCHANGED and now has a fixture that implements it: the guard is FALSE on
    the first read and TRUE afterwards, so the routine emits one action and then succeeds. The
    no-op case gets its own check below rather than being deleted -- `reintroduce the defect,
    never disable the check`.
    """
    ag = _agent()
    slot = _wide(ag)
    b = dict(ag.env.observe())
    seen = []

    def _rg(_s, _st, **_k):
        seen.append(1)
        return 0.0 if len(seen) > 1 else 1.0   # unsatisfied once, then satisfied
    ag.goal_residual = _rg
    r = Rt.Until(slot, Rt.Act(ag.actions[1]), 3)
    ag.routine, ag.routine_for = r, slot
    n0 = len(ag.led.entries)
    ag.choose(b)                                # emits the action; guard still false
    ag.choose(dict(ag.env.observe()))           # guard now true -> DONE, having acted
    row = next((e.detail for e in ag.led.entries[n0:] if e.event == "routine_end"), None)
    assert row and row["outcome"] == Rt.DONE, f"ended {row and row['outcome']}, not done"
    assert r in ag.routines, "a plan that achieved its guard was not shelved"
    assert not ag.refuted, "success filed a refutation"


def check_the_accumulation_commits_where_the_bargain_refused():
    """DEFECT: the accumulator built and never reached -- the class this record is full of.

    **Isaiah, 2026-09-25: the bargain KEEPS ITS PRICE AND LOSES ITS MONOPOLY.** `pays` still
    says whether a plan is worth banking; it stops being the only route from wanting to doing,
    because *the agent is always paying with its time* and a refusal that costs nothing lets an
    agent draft forever and look optimal.

    **THIS CHECK EXISTS BECAUSE THE FLAG DEFAULTS OFF.** Five standards encode the older
    contract and fail with it on, so the mechanism ships dark -- and a mechanism nobody
    exercises is exactly what this suite keeps finding. It is exercised HERE, with the flag on,
    on the path a real refusal takes.

    THE THRESHOLD FALLS WITH IDLE TIME, so the same vector that is short at cycle 0 commits
    later. That is the honeybee quorum: under pressure the bar drops and the decision arrives
    faster and worse.
    """
    ag = _agent()
    ag.cfg.accumulate = True        # the fixture is shared and copied; the flag is per-agent
    slot = _wide(ag)
    # a want this agent has wanted before -- the LEAN's own input
    ag.wants[slot] = "w"
    ag._want_seen["w"] = 6
    # reached only after `pays` refused; since item 6 the bargain's inputs do not enter it
    acc = ag._accumulate(slot, gkey=None)
    assert acc["vector"]["lean"] > 0, "recurrence contributed nothing"
    assert acc["total"] >= acc["threshold"], (
        f"a six-times-recurring want did not cross: {acc}")

    # AND THE OTHER DIRECTION, WHICH IS WHAT MAKES IT A GATE AND NOT A RUBBER STAMP
    ag2 = _agent()
    ag2.cfg.accumulate = True
    slot2 = _wide(ag2)
    ag2._last_commit = ag2.cycle                   # no idle relief
    # **AND NO RECURRENCE EITHER -- SET, NOT INHERITED. Isaiah's isolation ruling, 2026-09-30.**
    # This case used to take whatever the 25-cycle warm-up happened to leave in `wants`, and
    # that DECIDED IT: measured, `wants[o1.dcol]` is None on the default arm, so `lean` was
    # 0.0 BY THE `else` BRANCH at tether.py:4531 -- the case passed on an ABSENT WANT, not on
    # a price decision. Under the flip a want existed with 6 sightings, `lean` read 2.5, and
    # the same assertion failed. Four of the five inputs were fixed and the fifth was
    # whatever the world left lying about.
    #
    # **A WANT WITH ZERO HISTORY, NOT NO WANT.** Popping it would give `lean` 0.0 again by the
    # else-branch -- the original defect, re-entered through the repair. Naming a want the
    # agent has never seen keeps the recurrence term LIVE and contributing nothing, so the
    # verdict turns on the price and on nothing else, which is what this check is named for.
    ag2.wants[slot2] = "cold"
    ag2._want_seen["cold"] = 0
    cold = ag2._accumulate(slot2, gkey=None)
    assert cold["vector"]["lean"] == 0, (
        f"the cold case is not isolated -- recurrence leaked in: {cold['vector']}")
    assert not cold["commits"], f"a hopeless plan with no history committed: {cold}"

    # AND THE CLOCK MOVES THE BAR, WHICH IS THE "ALWAYS PAYING" RULING
    ag2.cycle += 40
    warm = ag2._accumulate(slot2, gkey=None)
    assert warm["threshold"] < cold["threshold"], (
        "forty idle cycles did not lower the bar -- refusing is still free")


def check_the_commitment_bar_is_the_agents_own():
    """DEFECT: the height an override must reach was `MIN_REPEAT` and a relief rate of 8 -- seat
    constants deciding commitment, where Isaiah ruled that *your current standing ... history*
    sets it (2026-09-25, relayed verbatim). The bar is now read from how the agent's own
    overrides ended: both ways, fading at its halflife, a ratio -- never a ratchet."""
    from self_family import MIN_REPEAT
    ag = _agent()
    ag._last_commit = ag.cycle                    # idle 0, so relief cannot mask the bar
    ag._overrides = []
    assert ag._commit_bar() == (float(MIN_REPEAT), False), "no history did not read the seed"
    assert ag._accumulate(_wide(ag), gkey=None)["bar_is"] == "SEED", "the seed was not marked"
    hi, lo = MIN_REPEAT + 1.0, MIN_REPEAT - 0.25
    ag._overrides = [(hi, False, ag.cycle)]
    bar, earned = ag._commit_bar()
    assert earned and bar > hi, "a failure at a total did not lift the bar above it"
    assert ag._accumulate(_wide(ag), gkey=None)["bar"] > hi, "the row hides the bar above it"
    ag._overrides = [(lo, True, ag.cycle), (lo + 0.1, True, ag.cycle)]
    assert ag._commit_bar()[0] == lo, "successes did not let the bar fall to what worked"
    ag._overrides = [(hi, False, ag.cycle - 10), (lo, True, ag.cycle)]
    assert ag._commit_bar()[0] < hi, "one old failure held the bar up against fresh success"
    ag._commit_cycles = [0, 4, 8]
    assert ag._relief_rate() == (4.0, True), "the relief rate is not the agent's own interval"


def check_the_fresh_read_qualifies_a_want_that_has_failed():
    """DEFECT: an accumulator that counts a pattern which FAILED every time it was tried as
    evidence FOR acting.

    **Isaiah, 2026-09-25: the fresh read must VOTE and QUALIFY.** Recurrence counts how often a
    want came back; IT DOES NOT KNOW WHETHER ACTING ON IT EVER WORKED. Transfer makes that
    dangerous in a new way -- a structure that matched but should not have, right neighbourhood
    and wrong house -- so prior outcomes under the SAME SIGNATURE have to price the lean.

    KEYED ON `_gap_key`, NOT ON THE BOARD: arity, the types that varied, the relation types, no
    slot names. A lesson learned on one arrangement prices a want on another, which is the
    transfer half and the reason a fingerprint would not do.
    """
    ag = _agent()
    ag.cfg.accumulate = True
    slot = _wide(ag)
    ag.wants[slot] = "w"
    ag._want_seen["w"] = 6
    sig = ("shape-under-test",)

    clean = ag._accumulate(slot, gkey=sig)
    # three episodes under this shape, all of which ended without acting
    ag._episodes[sig] = [((ag.actions[1],), "done", "tested_no")] * 3
    burnt = ag._accumulate(slot, gkey=sig)

    assert burnt["vector"]["episodes"] < 0, "failed episodes did not vote against"
    assert burnt["vector"]["lean"] < clean["vector"]["lean"], (
        "the lean was not qualified down by a shape that has never worked")
    assert burnt["total"] < clean["total"], f"{burnt} not below {clean}"

    # AND FAVOURABLE HISTORY MUST WEIGH THE OTHER WAY, or this is a damper and not a qualifier
    ag._episodes[sig] = [((ag.actions[1],), "done", "tested_yes")] * 3
    proven = ag._accumulate(slot, gkey=sig)
    assert proven["total"] > clean["total"], "a shape that has worked three times weighed nothing"


def check_a_plan_that_ends_without_acting_is_not_shelved():
    """DEFECT: `DONE` banked as a success when the routine never emitted an action.

    **`Until` ends the moment its guard reads true, so a plan whose guard ALREADY HOLDS
    returns `DONE` on its first advance having done nothing** -- and `DONE` is the only path
    onto the shelf. Shelving it installs a permanent cheap lie: `Call(r0)` costs a NAME
    (4.6439 bits at four actions, against 6.9658 for the `Until` inline) and `reach(Call)`
    returns the callee's BUDGET. A no-op would be reusable forever at a discount, claiming a
    reach it has never had.

    That is `FALSE_MINT`'s shape one layer up, and it is the exact fixture this suite used to
    demonstrate success with until 2026-09-25.
    """
    ag = _agent()
    slot = _wide(ag)
    b = dict(ag.env.observe())
    ag.goal_residual = lambda _s, _st, **_k: 0.0   # the guard holds BEFORE the routine runs
    r = Rt.Until(slot, Rt.Act(ag.actions[1]), 3)
    ag.routine, ag.routine_for = r, slot
    n0 = len(ag.led.entries)
    ag.choose(b)
    row = next((e.detail for e in ag.led.entries[n0:] if e.event == "routine_end"), None)
    assert row and row["outcome"] == Rt.DONE, f"ended {row and row['outcome']}, not done"
    assert r not in ag.routines, "a routine that emitted NOTHING was shelved as settled"
    tested = next((e.detail for e in ag.led.entries[n0:] if e.event == "reach_tested"), None)
    assert tested, "no `reach_tested` row: the assumed->tested upgrade did not fire"
    assert tested["verdict"] == "tested_no", f"verdict {tested['verdict']}, not tested_no"
    assert tested["emitted"] == 0, f"emitted {tested['emitted']}, not 0"


def check_an_unreadable_guard_blocks_at_execution():
    """DEFECT: a guard that cannot be read treated as one that is false -- check 3, at run time."""
    ag = _agent()
    slot = _wide(ag)
    b = dict(ag.env.observe())
    ag.routine = Rt.Until("no.such.slot", Rt.Act(ag.actions[1]), 3)
    ag.routine_for = slot
    n0 = len(ag.led.entries)
    ag.choose(b)
    row = next((e.detail for e in ag.led.entries[n0:] if e.event == "routine_end"), None)
    assert row and row["outcome"] == Rt.BLOCKED, f"ended {row and row['outcome']}, not blocked"
    assert not ag.refuted, "an unreadable guard was recorded as a refutation"


def check_the_suite_reaches_the_hard_cases():
    """BOTH EDGES OF THE ACT SPACE, in `conform/stateful.py`'s own form.

    Its comment is the rule: *a line that can never fire is not a weaker check, it reads as
    coverage that is not there.* **Measured before this existed: the suite reached `exhausted`
    and `unadvertised` and never `done` or `blocked`** -- so two of the four endings were
    asserted nowhere, and no falsification would have said so, because each check that DID run
    was falsifiable on its own.

    **IT OBSERVES THE RUN THAT ALREADY HAPPENS RATHER THAN REPEATING IT.** A first version
    called every other check from inside itself and took the suite from 8.5s to 19.7s -- the
    same cost mistake as putting the suite in a seat, one week smaller. `_watch()` installs a
    ledger spy for the whole run; this reads what it saw, and only falls back to running the
    others when called on its own.
    """
    seen = _SEEN
    if not seen:                                  # standalone: no runner spy is installed
        with _watch():
            for fn in CHECKS:
                if fn is not check_the_suite_reaches_the_hard_cases:
                    with contextlib.suppress(AssertionError):
                        fn()
        seen = _SEEN
    # **`"routine"` IS NOT IN THIS LIST -- ruling 6, Isaiah 2026-09-30.** The suite reached it
    # only on a PHANTOM-PADDED scope: `_wide` appends four members no object carries, and of
    # the five failing at 0.8333 exactly one was real. Strip them and the routine is refused
    # UPSTREAM on both arms -- OFF because the objective is already satisfied (discrepancy 0),
    # ON because there is no objective at all. So a `routine` event here would assert that the
    # suite reaches a state it only ever reached against members nothing can satisfy.
    #
    # NOT DELETED AND NOT LOOSENED: it moves to `conform/owed.py` intact, and comes back when
    # a world with a REAL gap exists. `routine_cut` and `routine_refused` STAY -- those are
    # reached honestly and they are what the fixture can actually show.
    for case in (Rt.DONE, Rt.EXHAUSTED, Rt.BLOCKED, "unadvertised",
                 "routine_cut", "routine_refused"):
        assert seen[case] > 0, f"the M2 suite no longer reaches: {case}"


def check_the_agent_owns_the_refutation_halflife():
    """DEFECT: the decay rate fixed by us, so an EARNED value could not reach the site.

    The executes-check showed the dial exists and starts UNEARNED -- correct, and it leaves the
    EARNED path unexercised, because a demotion has to happen first. **This exercises it
    without a board**, which is the only honest way to claim the path works: a unit test is
    allowed where a panel is not.

    TWO CLAIMS, and the second is the one that matters:
      the SHAPE honours a passed rate -- a different halflife decays differently
      the AGENT'S value REACHES it -- `Gamma.halflife` is what `Standing.decay` uses
    """
    fast = gamma.Standing(rejections=1.0, last_tick=0)
    slow = gamma.Standing(rejections=1.0, last_tick=0)
    fast.decay(8, halflife=1.0)
    slow.decay(8, halflife=64.0)
    assert fast.rejections < slow.rejections, (
        f"the rate is ignored: {fast.rejections} vs {slow.rejections}")

    # AND THE AGENT'S VALUE REACHES THE SITE. `Gamma.refute` passes `self.halflife` through, so
    # setting it is the whole of turning the dial -- no second path, no copy.
    g = gamma.Gamma(arc_atoms.three_spaces(arc_predict.predict()), game="unit")
    assert g.halflife is None, "a fresh Gamma must start UNEARNED, not on a number we picked"
    name = next(iter(g.library))
    g.halflife = 1.0
    g.tick = 0
    g.refute(name)
    g.tick = 8
    quick = g.rejection_of(name)          # `rejection_of` decays to `tick` before reporting
    g2 = gamma.Gamma(arc_atoms.three_spaces(arc_predict.predict()), game="unit")
    g2.halflife = 64.0
    g2.tick = 0
    g2.refute(name)
    g2.tick = 8
    held = g2.rejection_of(name)
    assert quick < held, (
        f"the agent's halflife does not reach the decay site: {quick} vs {held}")


def check_the_goal_is_a_slot_the_agent_can_perceive():
    """THE BOARD'S WIN CONDITION IS A QUANTITY, NOT A SENTENCE -- Isaiah, 2026-09-24.

    *The agent needs to want what the RLVR provides.* It always provided it: `objective()`
    returns `levels_completed / win_levels` every cycle. **A float the agent can READ is not a
    quantity it can COMPOSE WITH** -- no type, no alphabet, no residual -- so nothing could bet
    on it, mint against it or want it, and `OBJ` was a sink because the goal that matters was
    never an `OBJ` at all.

    **THE EXECUTES-CHECK ON A BOARD IS OWED AND BLOCKED** by a live hard stop on game runs. This
    is the half that needs no board: given a frame, does the slot APPEAR, TYPE and take its
    RANGE FROM THE BOARD. A unit test cannot say it is reached; it can say it is not broken.
    """
    import arc_atoms
    import arc_world

    class _Frame:
        levels_completed = 3
        win_levels = 7

    # A WORLD THAT NEVER TOUCHES A GAME. **AND `_read` MUST BE `None`, WHICH THE FIRST VERSION
    # OF THIS TEST GOT WRONG AND THE TEST CAUGHT:** the publish sits inside the cache-FILL
    # branch, so seeding `_read` to fake *after a frame* skips the whole block and reads as
    # *the slot is not published*. The placement is right -- once per frame -- and the premise
    # was wrong. Left recorded because a cache makes a live mechanism look absent.
    w = arc_world.ArcWorld.__new__(arc_world.ArcWorld)
    w._read = None
    w.blind = False
    w._frame = _Frame()
    w._palette = 16
    w.board = lambda: [[0, 1], [1, 0]]
    w._decompose = lambda _b: {"o0.row": 2, "o0.col": 5}

    got = arc_world.ArcWorld._decomposed(w)
    assert "@goal.completed" in got, "the goal slot is not published"
    assert got["@goal.completed"] == 3, got["@goal.completed"]

    # 2 -- IT TYPES ITSELF THROUGH THE SAME TABLE EVERY OTHER SLOT USES, which is the whole
    # reason the name ends in a declared attribute rather than being special-cased.
    assert arc_atoms.ATTRIBUTE_TYPE["completed"] == arc_atoms.EXTENT

    # 3 -- THE RANGE IS THE BOARD'S, NOT A CONSTANT. `win_levels` 7 -> 8 values, 0..7. If this
    # ever reads a number nobody can point at on the board, the slot has stopped being the
    # domain's and started being ours.
    alpha = arc_world.ArcWorld.alphabet(w)
    assert alpha["@goal.completed"] == 8, alpha["@goal.completed"]

    # 4 -- A BLIND FRAME PUBLISHES NOTHING. Confabulating progress off an unreadable board is
    # the one failure that would be worse than the float: a goal reading nobody measured.
    w2 = arc_world.ArcWorld.__new__(arc_world.ArcWorld)
    w2._read, w2.blind, w2._frame, w2._palette = None, True, _Frame(), 16
    w2.board = lambda: None
    w2._decompose = lambda _b: {}
    assert "@goal.completed" not in arc_world.ArcWorld._decomposed(w2)


def check_the_toy_world_meets_the_goal_contract():
    """THE HARNESS THE SEATS ACTUALLY RUN ON, AND IT WAS THE ONE WITHOUT A TEST.

    `@goal.completed`, the per-slot alphabet and `slot_types` all went into `world.py` on
    2026-09-24 and **only the `arc_world` half was checked.** The toy world is what `demo`,
    `gate`, `m2` and the fixture all run against, so it is the half that breaks things -- and
    it did: turning `alphabet()` from one number into a dict broke `demo.py`, which had been
    handing `correction_bits` the alphabet OF THE WORLD while charging ONE slot's correction.
    **That worked only while every slot shared a number, and nothing tested it.**

    FOUR CLAUSES, EACH ONE A THING THAT WENT WRONG OR COULD:
      the goal is PUBLISHED and DERIVED, never stored -- no rule can write it
      the alphabet is PER SLOT and the goal's is the BOARD's, not `M`
      the goal is TYPED, so the objective stream is asked for at all
      `objective()` and the slot are ONE quantity -- the `A6i` this pairing invites
    """
    import world

    env = world.Transitions()
    obs, slots = env.observe(), env.slots()
    assert world.GOAL_SLOT in obs, "the toy world does not publish the goal"
    assert world.GOAL_SLOT in slots, "the goal is published and not advertised"

    # 1 -- DERIVED, NEVER STORED. If it ever enters `state`, `step`'s `% M` mutates it and a
    # rule can write the agent's own progress -- which is the one thing that must not happen.
    assert world.GOAL_SLOT not in env.state, "the goal slot is STORED; a rule could write it"

    # 2 -- ONE QUANTITY. `objective()`'s degree and the slot are the same count or they will
    # drift, which is `A6i` with two producers of one fact.
    _name, degree = env.objective()
    assert abs(degree - obs[world.GOAL_SLOT] / len(env.state)) < 1e-9, (
        f"objective() says {degree} and the slot says {obs[world.GOAL_SLOT]}")

    # 3 -- THE RANGE IS THE BOARD'S. `M` would be WRONG, not merely loose: `correction_bits`
    # normalises mod the alphabet, so a full solve would wrap to zero and read as no progress.
    alpha = env.alphabet()
    assert isinstance(alpha, dict), "the alphabet must be per slot once the goal is a slot"
    assert alpha[world.GOAL_SLOT] == len(env.state) + 1, alpha[world.GOAL_SLOT]
    # **NOT `world.M` -- THE LAYER BOUNDARY BANS IT** (`TID251`: *the loop may not read the
    # value space; the env declares its own code*), and ruff refused the first version of this
    # line. The property wanted was never the constant anyway: **the STATE slots share one
    # alphabet and the GOAL's is different**, which is the shape the per-slot change created
    # and is checkable without naming a number.
    state_alphas = {alpha[s] for s in env.state}
    assert len(state_alphas) == 1, f"state slots disagree on their alphabet: {state_alphas}"
    assert alpha[world.GOAL_SLOT] not in state_alphas, (
        "the goal's alphabet collapsed onto the state's -- a full solve would wrap to zero")

    # 4 -- TYPED, or `mint` never asks for the objective stream at all and the whole OBJ path
    # is unreachable on this harness -- which is exactly how it was until today.
    types = env.slot_types()
    assert types[world.GOAL_SLOT] == "EXTENT", types.get(world.GOAL_SLOT)
    assert set(types) == set(slots), "a slot is advertised without a declared type"


def check_the_precondition_refuses_a_spectator():
    """DEFECT: minting a term that says nothing different about anything still OPEN.

    **ISAIAH, 2026-09-24: *minted against the residual.* NO OPEN RESIDUAL THE TERM BEARS ON ->
    NO MINT.** A precondition, not a threshold, and it needs no figure from anyone.

    **`F354` IS WHY.** Five of seven paid predictors sit on slots the agent's action cannot move,
    and one of them READS THE ACTION to predict a slot the action does not reach -- *a spectator
    wearing the costume of an actor.* **The bargain cannot see it:** `cost + left < base` reads
    EXPLANATION and never asks whether the explained thing was in play.

    **AND THE FAILURE PATH IS EXERCISED HERE, NOT ASSUMED** -- the reviewer's condition. A gate
    that only ever passes is indistinguishable from one that cannot fire, which is this project's
    most-repeated finding and was true of the focus seat for its whole life.
    """
    from gamma import Atom, Gamma
    from ledger import Ledger
    from tether import Agent, Config, Term
    from world import Transitions, bind

    ag = Agent(bind(Transitions()), Gamma(Transitions().atoms()), Config(), Ledger())
    idn = ag.gamma.library["idn"]

    # 1 -- NO OPEN RESIDUAL AT ALL. Nothing is in question, so nothing bears on it. This is the
    # settled-spectator case: a slot the incumbent already predicts perfectly buys nothing more.
    assert ag.bears_on(idn, "climb", [], idn) is False, (
        "an empty residual is no open question -- a mint there is a daydream by definition")

    # 2 -- A CANDIDATE INDISTINGUISHABLE FROM THE INCUMBENT. The residual is open and the term
    # says nothing different about it, which is the same defect wearing a candidate's clothes.
    # FIVE-TUPLE, WHICH IS WHAT `history()` HAS RETURNED SINCE `intent` AND `landed` WERE
    # ADDED. This fixture carried THREE and nothing noticed, because `bears_on` unpacked
    # with `*_` and accepted any row of length >= 3. That tolerance is what hid the
    # missing `landed` for as long as it hid this. The CHECK is unchanged -- same term,
    # same incumbent, same assertion -- only the row shape is the live one.
    hist = [({"climb": 2, "opaque": 1}, "A", 5, None, None)]
    twin = Term((Atom("idn2", lambda v, _c: v, "val", "val"),))
    assert ag.bears_on(twin, "climb", hist, idn) is False, (
        "a term that reproduces the incumbent on every open observation bears on nothing")

    # 3 -- AND IT MUST BE ABLE TO SAY YES, or it is a gate that refuses everything and the run
    # would go silent rather than selective. THE SAME PROPERTY THE BOUND'S OWN TEST INSISTS ON.
    differs = Term((Atom("plus1", lambda v, _c: v + 1, "val", "val"),))
    assert ag.bears_on(differs, "climb", hist, idn) is True, (
        "a term that answers the open observation differently MUST pass, or nothing ever mints")



def check_an_unreadable_reading_is_suspended_not_charged():
    """DEFECT: a reading that turned unreadable while its object was still there was billed a full
    code as a vanished OBJECT (`observe` strips NOT_RESOLVED; the bet loop read the absence as
    death). Measured: `o0.rem_row` charged 3.0 bits on a no-move frame (F493). Fig 10: a missing
    reading is a channel fact. CONTROL: an object whose key leaves the listing is still charged."""
    def run(drop_key: bool):
        ag = _agent()
        env = ag.env
        slot = next(s for s in sorted(env.observe()) if s.endswith(".row"))
        state = {"after": False}
        obs, stp, lst = env.observe, env.step, env.slots
        env.step = lambda *a, **k: (state.update(after=True), stp(*a, **k))[1]
        env.observe = lambda: {k: v for k, v in obs().items()
                               if not (state["after"] and k == slot)}
        env.slots = lambda: [k for k in lst() if not (drop_key and state["after"] and k == slot)]
        n0 = len(ag.led.entries)
        ag.step()
        rows = [e for e in ag.led.entries[n0:]
                if e.slot == slot and e.step == "PERCEIVE" and e.event == "bet"]
        assert rows, f"fixture: no bet on {slot} this cycle, so nothing was tested"
        return rows[-1].detail
    kept = run(drop_key=False)
    assert kept.get("suspended") and not kept.get("vanished") and kept.get("mass") == 0.0, (
        f"a reading the channel could not take was charged: {kept}")
    gone = run(drop_key=True)
    assert gone.get("vanished") and not gone.get("suspended") and gone.get("mass", 0) > 0, (
        f"an object whose key left the listing was not charged: {gone}")



def check_a_cell_change_reading_fits_its_alphabet():
    """DEFECT: the cell-change attributes were not declared in `ArcWorld.alphabet`, so they took the
    palette and the agent read every centroid modulo it, and a count equal to it as 0 (F494)."""
    was = arc_percept._CELL_CHANGE
    arc_percept._CELL_CHANGE = True
    try:
        env = ArcWorld(_Two(), arc_percept.Objects(),
                       arc_atoms.three_spaces(arc_predict.predict()), palette=PALETTE, platform=())
        seen = 0
        for _ in range(8):
            env.step(env.actions()[0])
            alpha = env.alphabet()
            for s, v in env.observe().items():
                if s.rsplit(".", 1)[-1] in arc_percept._CHANGE_ATTRS:
                    seen += 1
                    assert 0 <= v < alpha[s], f"{s}={v} aliases under an alphabet of {alpha[s]}"
        assert seen, "fixture: no cell-change reading was published, so nothing was tested"
    finally:
        arc_percept._CELL_CHANGE = was



def check_every_attribute_declares_its_alphabet():
    """DEFECT: an attribute with no declared alphabet fell to the palette and was read modulo it --
    `drow`, then F494, then twelve more, `dholes`/`dperimeter` live on every ARC run (F495). Every
    registered attribute is published once and `alphabet()` must range it without the palette
    fall-through, which now raises."""
    env = ArcWorld(_Two(), arc_percept.Objects(),
                   arc_atoms.three_spaces(arc_predict.predict()), palette=PALETTE, platform=())
    env.step(env.actions()[0])
    keys = set(arc_atoms.ATTRIBUTE_TYPE) | set(arc_percept._CHANGE_ATTRS)
    env._decomposed = lambda: {f"o0.{k}": 0 for k in keys}
    try:
        alpha = env.alphabet()
    except KeyError as exc:
        raise AssertionError(f"an attribute has no declared alphabet: {exc}") from None
    assert len(alpha) == len(keys), "fixture: not every attribute was ranged"
    exempt = getattr(arc_world, "PALETTE_BY_DESIGN", {})
    fell = sorted(k for k in keys if k not in exempt
                  and alpha[f"o0.{k}"] == PALETTE)
    assert not fell, f"ranged by the palette with no stated reason: {fell}"



class _Ring:
    """A synthetic fixture, no ARC content: one 3x3 object that opens a hole and closes it again,
    so its hole count and perimeter change by +1/+4 and then -1/-4."""

    def __init__(self) -> None:
        self.n = 0

    def _frame(self):
        f = FrameDataRaw(game_id="m2ring", state=GameState.NOT_FINISHED, levels_completed=0,
                         win_levels=3, available_actions=[1, 2, 3])
        b = np.zeros((SIDE, SIDE), dtype=int)
        b[4:7, 4:7] = 3
        if self.n % 2:
            b[5][5] = 0
        f.frame = [b]
        return f

    def reset(self):
        self.n = 0
        return self._frame()

    def step(self, *_a, **_k):
        self.n += 1
        return self._frame()


def check_a_signed_shape_delta_is_not_aliased():
    """DEFECT: `dholes`/`dperimeter` -- on for every ARC run -- were ranged by the palette, so a
    closing hole (-1) read as the palette minus one and a bet on that value was scored correct
    (F495). On the synthetic ring, the closing frame's deltas are negative and must stay distinct
    from every non-negative reading under the declared alphabet."""
    was = arc_percept._SHAPE_DELTA
    arc_percept._SHAPE_DELTA = True
    try:
        env = ArcWorld(_Ring(), arc_percept.Objects(),
                       arc_atoms.three_spaces(arc_predict.predict()), palette=PALETTE, platform=())
        env.step(env.actions()[0])
        env.step(env.actions()[0])          # the hole closes
        st, alpha = env.observe(), env.alphabet()
        ring = next(s.split(".")[0] for s, v in st.items() if s.endswith(".colour") and v == 3)
        slot = f"{ring}.dholes"
        per = slot.replace("dholes", "dperimeter")
        assert st[slot] == -1 and st[per] == -4, f"fixture: the ring did not close: {st}"
        for s in (slot, per):
            alias = st[s] % PALETTE
            assert tether.correction_bits(alias, st[s], alpha[s]) > 0, (
                f"{s}={st[s]} read as {alias} under an alphabet of {alpha[s]}: "
                "a bet on the wrong value would be scored correct")
    finally:
        arc_percept._SHAPE_DELTA = was



def _minted(ag, k: int = 2):
    """A held, non-atom term of at least `k` atoms, or None."""
    return next((n for n, t in sorted(ag.gamma.library.items())
                 if len(t.atoms) >= k and not ag.gamma.is_atom(t)), None)


def check_a_refusal_adds_and_lifts_only_on_growth():
    """not-t (F496; Fig 6): a refusal ADDS and removes nothing (P1); a never-held term cannot be
    refused (P5); it holds across any number of cycles and lifts only when the scope grows (P4)."""
    ag = _agent()
    name = _minted(ag, 1)
    assert name, "fixture: no held term to refuse"
    slot = _wide(ag)
    lib = dict(ag.gamma.library)
    assert not ag.refuse_term("never_held_term", slot), "a never-held term was refused"
    assert not ag._not, "refusing a never-held term left a record"
    assert ag.refuse_term(name, slot)
    gk = ag._term_gkey(slot)
    assert ag.gamma.library == lib, "a refusal removed or changed a library term"
    assert ag._term_refused(name, gk)
    ag.cycle += 50
    assert ag._term_refused(name, gk), "a refusal faded with time"
    a0, a1 = ag.gamma.atoms[0], ag.gamma.atoms[-1]
    ag.gamma.accept(gamma.Term((a0, a1, a0)), seq=999, residual="fixture growth")
    assert not ag._term_refused(name, gk), "growth did not lift the refusal"
    assert ag.refuse_term(name, slot)
    assert len(ag._not[(name, gk)]) == 2, "the record is not add-only"


def check_a_refused_term_is_not_retrieved():
    """P2: while not-t stands, t is not offered as a rebinding for that gap shape. The toy library
    holds no term that explains a slot, so the explanation test is stubbed to accept and the
    filter is what is tested: the first term retrieved, refused, must not be retrieved again."""
    ag = _agent()
    ag._rebindings = lambda t, *_a: [t]
    ag._explains = lambda *_a: True
    was, tether._BARGAIN_FIT = tether._BARGAIN_FIT, False
    try:
        slot = _wide(ag)
        name = ag._library_fit(slot, None)
        assert name, "fixture: nothing was retrieved even with the explanation test open"
        ag.refuse_term(name, slot)
        assert ag._library_fit(slot, None) != name, f"{name} was retrieved after its refusal"
    finally:
        tether._BARGAIN_FIT = was


def check_a_refused_term_is_no_shortcut_by_containment():
    """P3, by SEQUENCE CONTAINMENT (no lineage is kept): a settled t is one unit; refused, it is
    not, so terms that paid only through it re-price at full length -- reach falls by derivation."""
    ag = _agent()
    name = _minted(ag, 2)
    assert name, "fixture: no held term of two or more atoms"
    st = ag.gamma.standing.setdefault(name, gamma.Standing())
    st.settled_at = ag.gamma.tick
    slot = _wide(ag)
    seq = ag.gamma.library[name].atoms
    assert any(u.atoms == seq for u in ag._units_for(slot)), "fixture: the settled term is no unit"
    ag.refuse_term(name, slot)
    assert not any(u.atoms == seq for u in ag._units_for(slot)), "a refused term is still a unit"
    assert name in ag.gamma.library, "the refused term left the library"


def check_a_refused_settled_term_is_a_contradiction():
    """P6 (open in Fig 6): a settled term refused is written down as a contradiction and decided
    nowhere -- its standing is untouched."""
    ag = _agent()
    name = _minted(ag, 1)
    st = ag.gamma.standing.setdefault(name, gamma.Standing())
    st.settled_at = ag.gamma.tick
    n0 = len(ag.led.entries)
    ag.refuse_term(name, _wide(ag))
    rows = [e for e in ag.led.entries[n0:] if e.event == "contradiction"]
    assert rows and rows[0].detail.get("term") == name, "no contradiction row for a settled refusal"
    assert ag.gamma.is_settled(name), "the contradiction was decided by unsettling the term"



def check_a_refused_identity_reads_unsure():
    """R2, not-identity -- "two names, two referents" (F496): once an object's identity is
    refused, the one identity rule reads it unsure on every later frame, so restart carry and the
    cell-change readings stop trusting it. Nothing else about the object changes."""
    env = ArcWorld(_Two(), arc_percept.Objects(),
                   arc_atoms.three_spaces(arc_predict.predict()), palette=PALETTE, platform=())
    env.observe()
    env.step(env.actions()[0])
    env.observe()
    obj = next((n for n in sorted(env._decompose.tracked) if env.identity(n) == "overlap"), None)
    assert obj, "fixture: no object was re-found by overlap, so there is no sure identity to refuse"
    env.refuse_identity(obj)
    env.step(env.actions()[0])
    env.observe()
    assert env.identity(obj) not in ("overlap", "unique-shape"), (
        f"{obj}'s identity was refused and still reads sure: {env.identity(obj)}")
    other = next((n for n in sorted(env._decompose.tracked) if n != obj), None)
    assert other is None or env.identity(other) != "refused", "a refusal spread to another object"



def check_not_t_pays_only_when_t_does_worse_than_nothing():
    """Step 3 (F496; Fig 5's amendment): not-t pays iff its price plus what stays unexplained with
    t withdrawn (the persistence prior) is under what t leaves. The price names WHICH predicting
    term is wrong, agent-wide (the reviewer 2026-10-07). With arm J on, the filled bin refuses."""
    ag = _agent()
    name = _minted(ag, 1)
    slot = _wide(ag)
    left = {"t": 50.0, "nothing": 1.0}
    ag._left = lambda term, *_a, **_k: left["t"] if term.name == name else left["nothing"]
    ag._pred_by = {"a": name, "b": "other", "c": name}
    ok, d = ag._price_not(name, slot)
    assert ok and d["predicting"] == 2, f"t far worse than nothing was not refused: {d}"
    left.update(t=1.0, nothing=50.0)
    ok, d = ag._price_not(name, slot)
    assert not ok, f"t better than nothing was refused: {d}"
    left.update(t=50.0, nothing=1.0)
    was = tether._REFUTED_BIN
    tether._REFUTED_BIN = True
    try:
        ag._refuted_slot[slot] = name
        n0 = len(ag.led.entries)
        ag.route({slot: tether.SlotResidual(slot, tether.TRANSITION, 0, 1, 1.0)})
        rows = [e for e in ag.led.entries[n0:] if e.event == "refuse" and e.slot == slot]
        assert rows and rows[0].detail.get("predicting") == 2, "the filled bin did not refuse"
        assert ag._term_refused(name, ag._term_gkey(slot)), "the refusal was not recorded"
    finally:
        tether._REFUTED_BIN = was



def check_a_bound_want_can_be_refused():
    """R1, the mechanisable half of Fig 5's direction limit (F496): a sought-for shape bound as an
    ORDINARY term -- an objective-typed term on the goal slot -- is bet on like any other and is
    priced and refused by the same path. Nothing here claims the frame checks its own direction."""
    ag = _agent()
    goal = next(s for s in ag.slots if s.startswith("@goal"))
    want = next(n for n, t in sorted(ag.gamma.library.items())
                if getattr(t, "out_type", None) == tether.OBJ_TYPE and not ag.gamma.is_atom(t))
    ag.bound[goal] = want
    n0 = len(ag.led.entries)
    ag.step()
    bets = [e for e in ag.led.entries[n0:] if e.event == "bet" and e.slot == goal]
    assert bets, f"fixture: the bound want on {goal} was not bet on"
    ag._left = lambda term, *_a, **_k: 50.0 if term.name == want else 1.0
    ok, d = ag._price_not(want, goal)
    assert ok, f"a want doing worse than nothing was not refusable: {d}"
    assert ag.refuse_term(want, goal, **d) and ag._term_refused(want, ag._term_gkey(goal)), (
        "a bound want could not be refused by the ordinary path")


CHECKS = [v for k, v in sorted(globals().items()) if k.startswith("check_")]

if __name__ == "__main__":
    # THE COVERAGE CHECK RUNS LAST AND WATCHES THE OTHERS, so the suite is not run twice.
    # `_watch` counts what the ACT space actually reached during the ordinary pass.
    bad: list[str] = []
    coverage = check_the_suite_reaches_the_hard_cases
    ordered = [f for f in CHECKS if f is not coverage] + [coverage]
    with _watch():
        for fn in ordered[:-1]:
            try:
                fn()
            except AssertionError as exc:
                bad.append(f"{fn.__name__}: {exc}")
    try:
        coverage()
    except AssertionError as exc:
        bad.append(f"{coverage.__name__}: {exc}")
    for line in bad:
        print("  FAIL", line)
    print(f"\n  {len(ordered) - len(bad)}/{len(ordered)} M2 checks pass")
    sys.exit(1 if bad else 0)
