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
import sys

import numpy as np
from arcengine import FrameDataRaw, GameState

import arc_atoms
import arc_percept
import arc_predict
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
                         win_levels=3, available_actions=[0, 1, 2, 3])
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
        env = ArcWorld(_Two(), arc_percept.Objects(),
                       arc_atoms.three_spaces(arc_predict.predict()), palette=PALETTE)
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="m2test"), tether.Config())
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
    ag.env.objective = lambda: ("ALL(BECOME(level, completed))", 1.0)   # reward says: done
    assert (ag.goal_residual(slot, b) or 0) > 0, "fixture: the dense channel must still owe"
    _mint(ag, b)
    assert ag.routine is not None, "a satisfied reward channel suppressed the mint"


def check_route_is_learned():
    """DEFECT: a routine naming an action the agent has no evidence for."""
    ag = _agent()
    b = dict(ag.env.observe())
    _wide(ag)
    _mint(ag, b)
    if ag.routine is not None:
        learned = ag._goal_split(b)
        assert set(Rt.actions(ag.routine)) == {learned}, (
            f"routine names {Rt.actions(ag.routine)}, learned route is {learned}")


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
    """DEFECT: a routine bought when it does not pay -- or priced by a second currency."""
    ag = _agent()
    b = dict(ag.env.observe())
    _wide(ag)
    ag.goal_residual = lambda _s, _st, **_k: 0.02  # a real residual, too small to buy a plan
    rows = _mint(ag, b)
    assert ag.routine is None, "bought a plan the bargain could not afford"
    assert any(e.detail.get("reason") == "does-not-pay" for e in rows), "wrong reason"


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

    # 3 -- THE WIRE: a node routes to the evaluator through the agent's own slot predicate.
    ag = _agent()
    slot = _wide(ag)
    b = dict(ag.env.observe())
    h = ag._holds(b)
    assert h(C.Slot(slot)) == h(slot), "a node and its name disagree about the same slot"

    # 4 -- KLEENE SURVIVES THE WIRE. An unreadable conjunct can never produce a satisfied
    # guard: *I could not read it* is not *it holds*, at the site that terminates a loop.
    n0 = len(ag.led.entries)
    both = h(C.Bool("and", C.Slot(slot), C.Slot("no.such.slot")))
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


def check_strategy_is_emitted_when_a_routine_drives():
    """DEFECT: a multi-step plan executing and being counted as an uninformed probe.

    §22.2 reads transfer off a THREE-phase mix, and `STRATEGY` was structurally zero because
    nothing produced routines. Once one drives an action, a zero there is a gap rather than an
    honest reading -- which is what `tether.py`'s own comment said would happen.
    """
    ag = _agent()
    _wide(ag)
    for _ in range(8):
        ag.step()
    mix = ag.phases.report()["total"]
    assert mix.get("strategy", 0) > 0, f"a routine drove and the mix says {mix}"


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
    # ORPHANS ALONE IS VACUOUS HERE AND THE FIRST VERSION STOPPED THERE. `speak` cited 0 of 2
    # PLAN rows, so there was nothing to orphan and the check passed on an unnarrated space.
    cited = {i for s in said for i in s[0]}
    missed = [r.get("event") for r in plan if r.get("seq") not in cited]
    assert not missed, f"the narration cannot say the ACT space: {missed}"


def check_a_plan_that_succeeds_shelves_itself():
    """DEFECT: `done` treated as any other ending. It is the ONLY path onto the chunk shelf.

    The suite reached `exhausted`, `unadvertised`, `refused` and `cut` and had never once seen a
    plan SUCCEED -- which is why every chunking check has to hand-plant `ag.routines`.
    """
    ag = _agent()
    slot = _wide(ag)
    b = dict(ag.env.observe())
    ag.goal_residual = lambda _s, _st, **_k: 0.0   # the guard holds: the scope is satisfied
    r = Rt.Until(slot, Rt.Act(ag.actions[1]), 3)
    ag.routine, ag.routine_for = r, slot
    n0 = len(ag.led.entries)
    ag.choose(b)
    row = next((e.detail for e in ag.led.entries[n0:] if e.event == "routine_end"), None)
    assert row and row["outcome"] == Rt.DONE, f"ended {row and row['outcome']}, not done"
    assert r in ag.routines, "a plan that achieved its guard was not shelved"
    assert not ag.refuted, "success filed a refutation"


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
    for case in (Rt.DONE, Rt.EXHAUSTED, Rt.BLOCKED, "unadvertised",
                 "routine", "routine_cut", "routine_refused"):
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
