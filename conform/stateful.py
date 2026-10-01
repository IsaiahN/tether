"""stateful: drive the loop with generated histories and assert the invariants after
every step. One file. Imports kernel to DRIVE it, never to check it.

The seats already built read a record that a hand-written demo produced. A hand-written
demo is one history, chosen by the person who wrote the checks -- so a check can pass
because the case that breaks it was never generated. The A5 cross-slot hole needed a
slot built by hand before it appeared; the same defect would fall out of a random legal
history in seconds, shrunk to its minimal case.

    THE INVARIANTS ARE NOT REWRITTEN HERE. kernel.Linter's fourteen checks are already
    postconditions over a record. This generates the records.

THE GENERATOR IS AN EXEMPTION, and gets the same treatment as any other. A generator too
narrow tests nothing and reports green -- which is the direction that goes quiet -- so
`test_generator_reaches_the_hard_cases` asserts it can still produce the shapes that
have historically broken things. If the generator narrows, that fails before the loop
does, and the suite says so rather than passing over an empty search.

    python stateful.py            run it
    python stateful.py --cover    what the generator can reach, and how often
"""

from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

import kernel
from hypothesis import HealthCheck, settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, initialize, rule

sys.dont_write_bytecode = True

# THE HARNESS REACHES UP TO THE PACKAGE IT CHECKS. conform/ is not on the root's path
# and the root is not on conform/'s, so the seam is stated here instead of assumed. It
# is one direction only: nothing in the root may import conform.
#
# THREE DEFERRED IMPORTS DEPEND ON THIS LINE and none of them is near it: `snaps` in
# snap_specs and in snap_coverage, and snaps/gamma/ledger/tether/world in Shipped.begin.
# They are deferred so the module-level imports stay at the top and E402 stays unneeded;
# the cost is that deleting this line breaks things a hundred lines away.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

K = kernel.K
ACTS = kernel.ACTIONS

# Rule shapes, as (v, action) -> v. Each is TOTAL over the domain, because a partial rule
# would make the ground unanswerable rather than the frame wrong.
# every shape takes (a, b) whether it reads both or not, and every rule takes
# (value, action) the same way: one uniform signature, no branching on which shape a
# slot happens to have. ARG005 is the discipline, not a defect.
SHAPES = {   # noqa: ARG005
    "affine": lambda a, b: (lambda v, _act: (a * v + b) % K),
    "action": lambda a, b: (lambda v, act: (v + kernel.DELTA[act] * a + b) % K),
    "except": lambda a, b: (lambda v, _act: 0 if v == a % K else (v + 1) % K),  # noqa: ARG005
    "const": lambda a, b: (lambda _v, _act: b % K),                             # noqa: ARG005
}


@st.composite
def worlds(draw, min_slots=2, max_slots=4):
    """A world is n slots, each with a total rule. Two slots may share a shape and
    constants -- which is what produces the cross-slot settlement case, and is why the
    coverage test below asserts it still happens."""
    n = draw(st.integers(min_value=min_slots, max_value=max_slots))
    specs = []
    for _ in range(n):
        kind = draw(st.sampled_from(sorted(SHAPES)))
        specs.append((kind, draw(st.integers(0, K - 1)), draw(st.integers(0, K - 1))))
    return {f"s{i}": spec for i, spec in enumerate(specs)}


def build(spec: dict):
    return {s: SHAPES[k](a, b) for s, (k, a, b) in spec.items()}


def ground_for(truth):
    def ground(lib, phi, hist, slot):
        seen = {(b, act) for b, act, _ in hist}
        out = [(v, act, truth[slot](v, act)) for v in range(K) for act in ACTS
               if (v, act) not in seen]
        return bool(out) and all(lib.apply(phi, v, act) == want for v, act, want in out)
    return ground


class Loop(RuleBasedStateMachine):
    """Drives kernel.Frame over a generated world and asserts conformance every step."""

    def __init__(self):
        super().__init__()
        self.frame = None
        self.truth = None
        self.state = None
        self.spec = None

    @initialize(spec=worlds(), start=st.lists(st.integers(0, K - 1), min_size=4, max_size=4))
    def begin(self, spec, start):
        self.spec = spec
        self.truth = build(spec)
        self.frame = kernel.Frame(ground_for(self.truth))
        self.state = {s: start[i % len(start)] for i, s in enumerate(sorted(spec))}

    @rule()
    def advance(self):
        self.state = self.frame.step(self.state, lambda b, a:
                                     {s: self.truth[s](b[s], a) for s in b})

    def teardown(self):
        """The fourteen checks, unchanged, over whatever history was generated. A
        SUPPRESSED verdict counts as a failure here: it means a check stopped being
        trustworthy, which is not a pass.

        Run once per history rather than after every step: the ledger is APPEND-ONLY, so
        a violation at step 3 is still in it at step 14, and Linter.run re-runs all
        fourteen witnesses on every call by design. Per-step it was 3,500 selftests."""
        if self.frame is None or not self.frame.ledger:
            return
        res = kernel.Linter.run(self.frame.ledger)
        bad = {k: v["why"][:1] for k, v in res.items()
               if v["status"] in ("FAIL", "SUPPRESSED")}
        assert not bad, f"{bad} after {self.frame.cycle} steps on {self.spec}"


# =======================================================================================
# THE SAME FOURTEEN CHECKS, ON THE CODE THAT SHIPS
#
# Everything above generates histories for kernel.Frame -- the REFERENCE loop, which
# lives in this folder. So every claim the harness has made so far is a claim about the
# demonstration and not about the product, which is A9 as a fact about the harness rather
# than a property of the code. Linter.run takes plain rows and snaps already fills the
# ten-member contract, so pointing it at tether.Agent is wiring rather than machinery.
# =======================================================================================


@st.composite
def snap_specs(draw, min_slots=2, max_slots=4):
    """A snaps WorldSpec drawn STRUCTURALLY rather than by seed. `spec_for(seed)` would
    be one integer to shrink, and shrinking it walks to seed 0 rather than to a smaller
    world -- so the minimal failing case would be a number and not a shape."""
    import snaps

    n = draw(st.integers(min_value=min_slots, max_value=max_slots))
    names = [f"s{i}" for i in range(n)]
    rules = {}
    for nm in names:
        others = sorted(o for o in names if o != nm)
        pool = sorted(snaps.FAMILIES if others else
                      [f for f in snaps.FAMILIES if f not in snaps.RELATIONAL])
        fam = draw(st.sampled_from(pool))
        rules[nm] = snaps.SlotSpec(
            family=fam,
            k=draw(st.integers(1, snaps.M - 1)),
            a=draw(st.sampled_from([2, 3, 4, 5, 6])),
            reads=(draw(st.sampled_from(others))
                   if others and fam in snaps.RELATIONAL else None),
            lag=draw(st.sampled_from([2, 3])),
            switch=draw(st.sampled_from([8, 12, 16])),
            k2=draw(st.integers(1, snaps.M - 1)))
    spec = snaps.WorldSpec(
        slots=names, rules=rules,
        obj=draw(st.sampled_from(sorted(snaps.OBJECTIVES))),
        tgt=draw(st.integers(0, snaps.M - 1)),
        who=draw(st.sampled_from(names)), n=max(1, n // 2),
        start={nm: draw(st.integers(0, snaps.M - 1)) for nm in names})
    # a chain reading a chain is a cycle inside one tick, and snaps repairs that at the
    # SPEC. Reusing its repair rather than restating it: two copies of the rule is how
    # the generator and the world stop agreeing about what a legal world is.
    #
    # THE REPAIR'S RNG IS FIXED, NOT DRAWN. A drawn seed is a shrinkable integer, and
    # shrinking an integer walks toward 0 rather than toward a smaller world -- the same
    # objection that put `spec_for(seed)` out of this generator, surviving in the one
    # place it was easy to miss. The spec is drawn; only the repair of an illegal spec
    # is fixed, and it needs to be legal rather than varied.
    return snaps._acyclic(spec, random.Random(0))


class Shipped(RuleBasedStateMachine):
    """Drives tether.Agent over a generated snaps world and asserts the same fourteen."""

    def __init__(self):
        super().__init__()
        self.agent = None
        self.spec = None

    @initialize(spec=snap_specs())
    def begin(self, spec):
        import snaps
        from gamma import Gamma
        from ledger import Ledger
        from tether import Agent, Config
        from world import bind

        self.spec = spec
        self.agent = Agent(bind(snaps.Snap(spec)), Gamma(snaps._atoms()),
                           Config(), Ledger())

    @rule()
    def advance(self):
        self.agent.step()

    def teardown(self):
        if self.agent is None or not len(self.agent.led):
            return
        res = kernel.Linter.run(self.agent.led.rows())
        bad = {k: v["why"][:1] for k, v in res.items()
               if v["status"] in ("FAIL", "SUPPRESSED")}
        # THE MESSAGE MUST CARRY ENOUGH TO REPRODUCE THE FAILURE -- approved 2026-09-22.
        # It printed `{slot: family}` only, while the generated spec also carries `k` per
        # SlotSpec and `obj`/`tgt`/`who`/`n` on the WorldSpec, all drawn from the rng. A
        # hand-built world with the same two families produced NO no_support rows at all,
        # so a B5 failure could not be reproduced from its own message and every diagnosis
        # of it was a guess about a different world.
        #
        # THIS CHANGES NO VERDICT. It widens what a failure CARRIES, which is the opposite
        # of disabling a check.
        fams = {"slots": list(self.spec.slots),
                "obj": self.spec.obj, "tgt": self.spec.tgt,
                "who": self.spec.who, "n": self.spec.n,
                "rules": {n: {"family": r.family, "k": r.k}
                          for n, r in sorted(self.spec.rules.items())}}
        assert not bad, f"{bad} after {self.agent.cycle} steps on {fams}"


# --fast is for the commit hook: enough histories to catch a regression, few enough
# that blocking a commit on it stays proportionate. The full run is what finds new
# things, and it is the one worth running when something has actually changed.
FAST = "--fast" in sys.argv
Loop.TestCase.settings = settings(
    max_examples=25 if FAST else 120, stateful_step_count=6 if FAST else 10,
    deadline=None, suppress_health_check=[HealthCheck.too_slow],
    # EXACT REPLAY, AND HYPOTHESIS ALREADY HAD IT -- approved 2026-09-22. A B5 failure
    # could not be reproduced from its own message: printing the full spec revealed the
    # missing `n=1`, and rebuilding that spec by hand STILL produced no `no_support` rows,
    # so the failing state is not the spec alone. `print_blob` emits the
    # `@reproduce_failure` token that replays the exact example, which is the thing a
    # hand-built world can never be. Changes no verdict; it widens what a failure carries.
    print_blob=True,
)
TestLoop = Loop.TestCase
Shipped.TestCase.settings = Loop.TestCase.settings
TestShipped = Shipped.TestCase


def coverage(n: int = 400) -> Counter:
    """What the generator actually reaches. A generator that cannot produce the shapes
    that have historically broken things is an exemption nobody pinned."""
    seen: Counter = Counter()
    for spec in (worlds().example() for _ in range(n)):
        kinds = [k for k, _, _ in spec.values()]
        seen["worlds"] += 1
        seen[f"slots={len(spec)}"] += 1
        for k in set(kinds):
            seen[k] += 1
        rules = list(spec.values())
        if len(rules) != len(set(rules)):
            seen["two slots share a rule"] += 1      # the A5 cross-slot shape
        if "except" in kinds:
            seen["a slot outside the closure"] += 1  # the pays-not-closes shape
        if "action" in kinds:
            seen["an action-dependent slot"] += 1    # the A6 shape
    return seen


def snap_coverage(n: int = 200) -> Counter:
    """What the SHIPPED generator reaches. `snap_specs` narrows in three places and none
    of them was witnessed: RELATIONAL families are dropped when a slot has no others,
    `_acyclic` rewrites a chain that cannot find a free target, and the COUNT objective
    takes `n = max(1, slots // 2)`. If any tightens, the shipped seat passes over an
    empty search and reports green."""
    seen: Counter = Counter()
    for spec in (snap_specs().example() for _ in range(n)):
        fams = [r.family for r in spec.rules.values()]
        seen["worlds"] += 1
        seen[f"slots={len(spec.slots)}"] += 1
        for f in set(fams):
            seen[f] += 1
    return seen


def test_the_resolutions_offered_are_not_the_answer():
    """The generator advertises resolutions the way it advertises actions, and a
    generator that could encode a solution needs pinning in BOTH directions.

        too many views resolve   the harness is answering; choosing is not work
        too few resolve          INWARD is unfalsifiable, and a run would read as
                                 `it does not work` rather than `the generator cannot
                                 produce a case where it could`

    A view is LOSSY when the coarse dynamics stop being a function of the coarse state:
    two readings with the same coarse image and different coarse successors. Nothing at
    that resolution can predict it, and the agent can see this in its own record without
    a key -- it is the same (state, action) giving two outcomes.

    AND THE STRUCTURAL GUARANTEE IS CHECKED, not the rate. `_views` is handed the slot
    NAMES and never the rules, so the offered set cannot have been selected for resolving
    anything. A rate drifts; a constructor that was never shown the rules cannot encode
    them at any rate.
    """
    import inspect
    from collections import defaultdict

    import snaps

    src = inspect.getsource(snaps._views)
    assert "rules" not in src and "spec" not in src, (
        "_views can see the rules: the offered resolutions could be chosen to resolve "
        "them, which is the answer encoded in the harness")

    def loses(spec, t_a):
        seen, bad = defaultdict(set), False
        probe = snaps.Snap(spec)
        for i in range(8):
            before = probe.observe()
            for ac in snaps.ACTIONS:
                fork = snaps.Snap(spec)
                fork.state, fork.past, fork.tick = (dict(before), list(probe.past),
                                                    probe.tick)
                fork.step(ac)
                k = (tuple(sorted(t_a(before).items())), ac)
                seen[k].add(tuple(sorted(t_a(fork.observe()).items())))
                bad |= len(seen[k]) > 1
            probe.step(snaps.ACTIONS[i % len(snaps.ACTIONS)])
        return bad

    # SHARPENABLE is the property INWARD needs and `some view is lossy` is not it.
    # `full` is itself lossy wherever a rule reads the tick or the previous state, and no
    # resolution over the slots recovers that -- so counting lossy views at all is
    # satisfied by the world's own unreachability rather than by a coarse view losing
    # something a finer one holds. Found by substituting a view set of ONLY `full` and
    # watching the assertion pass anyway.
    sharpenable = choosable = 0
    for seed in range(3):
        w = snaps.Snap(snaps.spec_for(seed, 3))
        views = w.transform()
        full = next(t for n, t in views if n == "full")
        coarse = [(n, t) for n, t in views if n != "full"]
        full_holds = not loses(w.spec, full)
        lost = [n for n, t in coarse if loses(w.spec, t)]
        sharpenable += full_holds and bool(lost)
        choosable += len(lost) < len(coarse)

    assert sharpenable > 0, (
        "no world has a coarse view that loses what the full view holds: sharpening can "
        "never succeed, so INWARD is unfalsifiable and a null would be the generator's")
    assert choosable > 0, (
        "every coarse view loses the dynamics in every world: there is nothing to choose "
        "between, so the offered set is not a set")


def test_the_atom_order_is_pinned():
    """THE REGISTRY IS POSITIONAL, so its order is load-bearing and nothing declared it.

    Inserting a name rather than appending renumbers the universe -- *a DIFFERENT SEARCH at
    the same size* -- and `mint` breaks on the first closer, so **the emitted order decides
    which term gets minted**. Measured: moving one atom to the front changes the first six
    terms the closure emits.

    Every number taken on this panel -- the false-mint rate, the extensional collapse, both
    narrowing arms, the bit-rate readings -- was measured under this ordering, and not one
    of them states it. **So it is stated here.** A reordering breaks this before it can
    quietly change what those numbers mean.

    APPEND ONLY. Adding at the end leaves every existing prefix intact, so prior terms keep
    their identity; inserting does not. `take` was added at the end, which was the safe
    direction and was not enforced by anything until now.
    """
    import snaps
    import world

    # THE PIN IS PER MODULE, because the two worlds no longer carry the same vocabulary.
    # `world` gained `EXTENT -> PRED -> OBJ` on 2026-09-24 -- it could not express an objective
    # at all, so three stages of the end-to-end fixture were dead on one cause. **APPENDED, in
    # the safe direction this test names**, so every prior prefix and every term identity taken
    # under the old order is intact. `snaps` is untouched and is pinned at the original eight.
    BASE = ["idn", "inc", "dec", "dbl", "neg", "act", "wrap", "take"]
    ORDERS = {"snaps": BASE,
              "world": [*BASE, "same", "other", "above", "all", "any", "none"]}
    for mod in (snaps, world):
        pinned = ORDERS[mod.__name__]
        got = [a.name for a in mod._atoms()]
        assert got[:len(BASE)] == BASE, (
            f"{mod.__name__}._atoms() begins {got[:len(BASE)]}, and the pinned prefix is "
            f"{BASE}. A name was INSERTED or MOVED: every stored term and every measurement "
            "taken under the old order now means something else.")
        assert got == pinned, (
            f"{mod.__name__}._atoms() is {got}, pinned as {pinned}. If a name was APPENDED, "
            "extend the pin -- and say in the commit why the vocabulary grew.")


def test_the_residual_bound_loses_nothing():
    """A narrowing that drops a term the exhaustive search would have found is a lost
    capability, not a speedup -- so this pins that direction first.

    `_cannot_pay` is a NECESSARY condition: a term wrong on k of R is wrong at least k
    times overall, so the bound proves it cannot pay whatever it does on the rest. If
    that holds, neutering it changes nothing at all -- not the bindings, not the debts,
    not the library, not one ledger row.

    AND THE PROPERTY MUST BE ABLE TO GO RED. An earlier narrowing skipped operand-reading
    terms when R showed no dependence on another slot, which sounds like the same idea
    and is not: it reasons about what a term ought to need, and a term can read an
    operand without varying with it on the observed slice. Measured, it lost a closing
    term. That narrowing is substituted here, and if this property cannot see it then it
    is not checking anything.
    """
    import snaps
    from gamma import Gamma
    from ledger import Ledger
    from tether import Agent, Config
    from world import bind

    real = Agent._cannot_pay

    def run(filt):
        Agent._cannot_pay = filt
        try:
            out = []
            for seed in range(3):
                w = snaps.Snap(snaps.spec_for(seed, 3))
                a = Agent(bind(w), Gamma(snaps._atoms()), Config(), Ledger())
                for _ in range(12):
                    a.step()
                out.append((dict(a.bound), sorted(a.owed_import),
                            len(a.gamma.library), len(a.led)))
            return out
        finally:
            Agent._cannot_pay = real

    exhaustive = run(lambda *_a: False)
    assert run(real) == exhaustive, "the residual bound changed the run: a term was lost"
    unsound = run(lambda _self, term, *_a: term.operand is not None)
    assert unsound != exhaustive, ("this property cannot detect a narrowing that drops "
                                   "operand-reading terms, so it pins nothing")


def test_the_promotion_clause_is_recorded():
    """`admissions()` documents four buckets and one of them could not be non-zero.

    §11 partitions the ablation by WHICH CLAUSE let an entry in -- `promoted` is WIPED,
    `necessary` is BLIND -- and the clause is unrecoverable afterwards, because `PRIOR`
    marks every atom alike. `promote()` wrote `self.primitives` and never touched the
    stamp, so a promoted term kept reading `accepted` and the wipe would have taken the
    wrong set.

    THE SHAPE IS THE ONE `admissions()`' OWN DOCSTRING RECORDS HAVING JUST FIXED for
    `unstated`: *a falsifier over a population that cannot contain the defect it looks
    for.* Repaired the instance, left the class, one bucket over -- which is why this is
    a check and not a careful comment.

    AND `necessary` MUST SURVIVE PROMOTION. An atom's clause is a fact about what the
    agent ARRIVED WITH; nothing it does later changes it. Without that half the guard
    would launder an inherited atom into the wiped category, which is the ablation
    reading backwards.
    """
    from gamma import MINTED, Atom, Gamma

    def fresh():
        g = Gamma([Atom("a", lambda v, _c: v, "VAL", "VAL"),
                   Atom("b", lambda v, _c: v, "VAL", "VAL")], game="probe")
        t = g.build(("a", "b"), origin=MINTED)
        g.accept(t, seq=1, residual="r0")
        return g, t

    g, t = fresh()
    assert g.admissions().get("promoted", 0) == 0, "promoted before anything was promoted"
    g.promote(t.name, shadow={"s": 1}, echo={"slot": "o0"})
    assert g.admissions().get("promoted", 0) == 1, (
        "promote() left the clause unstamped: the `promoted` bucket cannot fill, so the "
        "ablation cannot tell a promoted term from a merely accepted one")
    assert g.admissions().get("accepted", 0) == 0, "the term cited two clauses at once"

    g, _t = fresh()
    g.promote("a", shadow={"s": 1}, echo={"slot": "o0"})
    assert g.admissions().get("necessary", 0) == 2, (
        "promotion overwrote an atom's `necessary`: an arrival clause was rewritten by "
        "conduct, and the ablation's blind set lost a member")

    # REINTRODUCE THE DEFECT, NEVER DISABLE THE CHECK. The old body, verbatim.
    real = Gamma.promote
    try:
        Gamma.promote = lambda self, name, shadow, echo: self.primitives.__setitem__(
            name, {"shadow": shadow, "echo": echo})
        g, t = fresh()
        g.promote(t.name, shadow={"s": 1}, echo={"slot": "o0"})
        assert g.admissions().get("promoted", 0) == 0, (
            "this property cannot see an unstamped promotion, so it pins nothing")
    finally:
        Gamma.promote = real


def test_the_mutation_observer_reaches_the_agent():
    """`observer.py` was correct, complete, and imported only by `test_perception.py`.

    Its sole entry point took a LIST OF FRAMES -- a replay, the answer key -- so the agent could
    not call it without crossing `KEY_BOUNDARY`. **The shape of the door kept it out, not the
    room**, and nothing failed for five months because an unreached mechanism does not fail, it
    abstains.

    So the guard is not *does `observe` work*; it is **does a live agent READ it**. That is the
    standing question this project asks of anything the record says exists, and the answer has
    been NO five times in one day before now.

    THE DENOMINATOR IS `cue_seen`, NOT THE CYCLE COUNT. Frame 0 has no predecessor, so a mutation
    was impossible there; counting it would compute a rate over a frame that could not contribute.
    """
    import gamma
    import gridworld
    import ledger
    import tether
    from world import bind

    w = gridworld.boards(1, start=3)[0]
    env = bind(w)
    assert getattr(env, "cues", None) is not None, (
        "the bound habitat publishes no `cues()` -- the observer cannot reach the agent")
    # SIX CYCLES, NOT TWELVE. The wire fires at frame 1 and this check pays for itself in
    # SEAT TIME -- at twelve it pushed `shipped` past its 120s budget and the stage reported
    # DID-NOT-RUN, which is not a pass. A guard nobody can afford to run is the unreached
    # mechanism one level up, which is the defect this very check exists to catch.
    ag = tether.Agent(env, gamma.Gamma(env.atoms()), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()

    book = ag.gamma.book
    assert book.get("cue_seen", 0) > 0, (
        f"the agent never read a cue in 6 cycles: {dict(book)}. `observer` is back off the "
        f"agent path -- the exact state it sat in from 2026-04 to 2026-09-26")
    assert book.get("cue_mutated", 0) > 0, (
        "cues were read and NOTHING ever mutated. Either the habitat stopped moving or the "
        "raster is publishing a board that does not change -- and a cue stream with no "
        "mutations is the undirected search the observer exists to replace")
    assert ag.cue is not None, (
        "the cue was narrated to the ledger and never stored on the agent. A row is for the "
        "record; `self.cue` is what a consumer can read -- *a value that exists is not a value "
        "that crosses*")

    # THE RASTER MUST NOT SWALLOW AN OBJECT. Colours are drawn from `randrange(4)`, which
    # includes 0 -- the field colour -- so an unshifted raster makes some objects VANISH on
    # some seeds and not others. This caught it once; it stays because the failure is
    # seed-dependent and therefore invisible to any single run.
    for seed in range(6):
        g = gridworld.boards(1, start=seed)[0].board()
        assert not any(v == 0 for row in g for v in row if v is None), "impossible"
        painted = sum(1 for row in g for v in row if v)
        assert painted >= 2, (
            f"seed {seed} rasters {painted} visible cells from {gridworld.N_OBJECTS} objects -- "
            f"a colour-0 object is being swallowed by the field")

    # REINTRODUCE THE DEFECT, NEVER DISABLE THE CHECK: the habitat as it was, with no `cues`.
    real = gridworld.GridWorld.cues
    try:
        del gridworld.GridWorld.cues
        w2 = gridworld.boards(1, start=3)[0]
        ag2 = tether.Agent(bind(w2), gamma.Gamma(env.atoms()), tether.Config(), ledger.Ledger())
        for _ in range(2):
            ag2.step()
        assert not ag2.gamma.book.get("cue_seen"), (
            "this property cannot see the observer going missing, so it pins nothing")
        assert ag2.cue is None, "the agent invented a cue from a world that publishes none"
    finally:
        gridworld.GridWorld.cues = real


def test_a_mutation_moves_attention_and_never_the_action():
    """The cue's consumer: surprise drives ATTENTION -- Berlyne 1960, `ARC_HUMAN_PRIORS` §8.

    Two things are pinned and the second matters more than the first.

    THAT IT FIRES. Wiring perception to nothing is half a mechanism, and `observer.py` spent
    five months as exactly that. `focus_by_cue` is the denominator's other half: if it reads
    zero the cue is as starved as the selector and the wiring bought nothing.

    **THAT IT MOVES ATTENTION AND NOT THE ACTION.** This is the boundary the whole change rests
    on. A mutation may narrow WHAT THE AGENT LOOKS AT; it may never decide WHAT IT DOES.
    Looking at the changed thing is a means the agent can still be wrong about -- picking the
    move is the test, and a cue reaching `choose` would be the proctor answering it.

    AND IT MUST NOT COMPETE WITH `_goal_choice`. The consumer sits in the `elif`, so the
    selector keeps every choice it can make. A previous seat wired a weaker duplicate ranking
    into this exact site; the branch is what makes this a complement instead.
    """
    import gamma
    import gridworld
    import ledger
    import tether
    from world import bind

    w = gridworld.boards(1, start=3)[0]
    env = bind(w)
    ag = tether.Agent(env, gamma.Gamma(env.atoms()), tether.Config(), ledger.Ledger())
    # SIX CYCLES, NOT TEN -- and this is the SIBLING of a trim already made. Its twin was cut
    # 12 -> 6 the night both were written, for blowing `shipped`'s 120s budget and reporting
    # DID-NOT-RUN, and this one was left at ten. Measured 2026-09-27: the direct property tests
    # cost 103.1s of the 120s, and this test alone was 53.4s of that -- so the seat's verdict
    # was being decided by one check's cycle count rather than by the agent.
    # **`repaired the instance, left the class`, which is this project's most-filed failure.**
    # Six is not a guess: `focus_by_cue` reads 2 and `cue_mutated` 2 at six cycles, so both
    # assertions below still have something to be true OF.
    for _ in range(6):
        ag.step()
    book = ag.gamma.book

    assert book.get("focus_by_cue", 0) > 0, (
        f"the cue never moved attention in 6 cycles: {dict(book)}. Perception is wired to "
        f"nothing -- half a mechanism, which is what `observer.py` was for five months")
    assert book.get("cue_mutated", 0) > 0, "no mutation fired, so the check proves nothing"

    # THE BOUNDARY, PINNED STRUCTURALLY RATHER THAN BY READING THE COMMENT. `choose` decides
    # the action; if it can see the cue at all, attention-only is a convention and not a fact.
    import inspect
    src = inspect.getsource(tether.Agent.choose)
    assert "self.cue" not in src and "focus_by_cue" not in src, (
        "`choose` reads the cue -- a mutation is deciding WHAT THE AGENT DOES, not what it "
        "looks at. That is the proctor answering the test")

    # REINTRODUCE THE DEFECT: no cue, and attention must fall back rather than invent one.
    real = gridworld.GridWorld.cues
    try:
        del gridworld.GridWorld.cues
        w2 = gridworld.boards(1, start=3)[0]
        ag2 = tether.Agent(bind(w2), gamma.Gamma(env.atoms()), tether.Config(), ledger.Ledger())
        for _ in range(3):
            ag2.step()
        assert not ag2.gamma.book.get("focus_by_cue"), (
            "attention moved by cue on a world that publishes none -- this property pins "
            "nothing")
    finally:
        gridworld.GridWorld.cues = real


def test_the_admitting_clause_crosses_into_gamma():
    """The clause existing in `arc_atoms` is not the clause reaching the ablation.

    `ADMITTED` was enforced at construction and Γ still stamped every atom `necessary` --
    the ablation's BLIND category -- so the partition was WRONG at the one place it is
    read. *A value that exists is not a value that crosses*, and the crossing is the half
    that has no other witness: both halves are individually green while the bridge is out.

    THE REFUTER IS A SPLIT, NOT A PRESENCE. `{necessary: 62}` means it did not cross;
    `{handed: 62}` means the default inverted and the base vocabulary was filed as handed,
    which is the ablation reading backwards. Only a split that matches the two tables is
    the mechanism working.
    """
    import arc_atoms
    import arc_predict
    from gamma import HANDED, NECESSARY, Gamma

    atoms = arc_atoms.three_spaces(arc_predict.predict())
    got = Gamma(atoms, game="clause").admissions()
    assert got.get(HANDED) == len(arc_atoms.ADMITTED), (
        f"the admitting clause did not cross into Gamma: {got}. Every atom reads "
        f"`necessary` -- the category the ablation stays BLIND to -- while "
        f"`arc_atoms.ADMITTED` names {len(arc_atoms.ADMITTED)} that were handed")
    assert got.get(NECESSARY) == len(atoms) - len(arc_atoms.ADMITTED), (
        f"the clause-one population is wrong: {got}. If this is `handed` for everything "
        f"the default inverted and the base vocabulary is filed in the WIPED category")

    # A WORLD THAT DECLARES NOTHING MUST BE UNTOUCHED. The field defaults to `None` and
    # `_install` reads that as `necessary`; fifteen construction sites across five worlds
    # rely on it, and a change of default would move them all silently.
    import snaps
    assert set(Gamma(snaps._atoms(), game="toy").admissions()) == {NECESSARY}, (
        "a world that declares no clauses stopped reading `necessary`")

    # REINTRODUCE THE DEFECT, NEVER DISABLE THE CHECK: the atoms as they were before the
    # crossing, carrying no clause of their own.
    from dataclasses import replace
    stripped = [replace(a, admitted=None) for a in atoms]
    assert set(Gamma(stripped, game="pre").admissions()) == {NECESSARY}, (
        "this property cannot see atoms arriving with no clause, so it pins nothing")


def test_the_daydream_precondition_can_refuse():
    """`bears_on` returns True on every call of a live run, so nothing in the record shows
    its refusal working. A gate never observed refusing is indistinguishable from a gate
    wired to `return True`, and that is the class this repo keeps finding.

    So the arguments are CAPTURED FROM A LIVE RUN rather than built here -- a hand-made
    term would prove the function's logic and not that the logic is reachable with the
    values the loop actually carries. Both routes are driven on real ones:

        no open residual        -- `robs` empty, the spectator case the docstring claims
        says nothing different  -- `held` IS the candidate, so `got == was` everywhere

    AND THE MUTATION CONTROL IS THE POINT. A `bears_on` that ignored `held` would pass the
    empty-`robs` route and still be wrong, which is the more likely defect of the two.
    """
    import io
    from contextlib import redirect_stdout

    import tether
    import world
    from gamma import Gamma
    from ledger import Ledger

    seen = []
    real = tether.Agent.bears_on

    def spy(self, term, slot, robs, held):
        seen.append((self, term, slot, list(robs), held))
        return real(self, term, slot, robs, held)

    tether.Agent.bears_on = spy
    try:
        env = world.bind(world.Transitions())
        ag = tether.Agent(env, Gamma(env.atoms()), tether.Config(), Ledger())
        with redirect_stdout(io.StringIO()):
            ag.run(10)
    finally:
        tether.Agent.bears_on = real

    assert seen, "the precondition was never called -- the site is unreached, not permissive"
    agent, term, slot, robs, held = seen[0]
    assert robs, "captured a call with no open residual; the baseline below would be vacuous"

    assert real(agent, term, slot, robs, held) is True, (
        "the captured call no longer passes, so the two refusals below prove nothing")
    assert real(agent, term, slot, [], held) is False, (
        "a candidate with NO open residual was admitted -- the spectator route is dead")
    assert real(agent, term, slot, robs, term) is False, (
        "a candidate identical to the incumbent was admitted -- it says nothing different")

    blind = lambda _self, _t, _s, robs, _h: bool(robs)  # noqa: E731 -- ignores `held`
    assert blind(agent, term, slot, [], held) is False
    assert blind(agent, term, slot, robs, term) is True, (
        "this property cannot detect a precondition that ignores the incumbent")


def test_the_generated_habitat_is_not_built_to_pass():
    """The habitat's own generator, pinned -- because a generated world CAN be generated to make
    a finding pass, and that is the failure I nearly committed with the toy-world patch.

    Each assertion is a property the generator must keep having, not a number it happened to hit:

        REACHABLE      checked by BFS over the board, INDEPENDENTLY of the walk that built the
                       target. A construction that proves its own output is not a check
        NOT PRE-SOLVED measured at 10 of the first 60 before it was fixed. A board whose goal
                       holds at step 0 exercises nothing and inflates any later goal reading
        SPECTATORS     every board must have at least one slot NO action moves. This is the
                       whole reason the habitat exists (`F356`/`F359`/`F360`), so if the
                       generator ever stops producing it, those findings go quietly unexercised
    """
    import gridworld as G

    pre_solved, worst_spectators = 0, 99
    for w in G.boards(40):
        wall = (w.state["o2.row"], w.state["o2.col"])
        start = (w.state["o0.row"], w.state["o0.col"])
        seen, frontier = {start}, [start]
        while frontier:
            r, c = frontier.pop()
            for dr, dc in G._DELTA.values():
                n = (r + dr, c + dc)
                if 0 <= n[0] < G.GRID and 0 <= n[1] < G.GRID and n != wall and n not in seen:
                    seen.add(n)
                    frontier.append(n)
        assert w.target in seen, f"board {w.seed}: the target is not reachable from the start"

        pre_solved += w._completed()
        moved = set()
        for a in G.ACTIONS:
            t = G.GridWorld(seed=w.seed)
            before = dict(t.state)
            t.step(a)
            moved |= {k for k in before if before[k] != t.state[k]}
        worst_spectators = min(worst_spectators, len(w.state) - len(moved))

    assert pre_solved == 0, f"{pre_solved} of 40 boards start already solved"
    assert worst_spectators > 0, ("some board has no spectator slot -- the property the whole "
                                  "habitat was built to exhibit")


def test_shipped_generator_reaches_the_hard_cases():
    """The families the false-mint read named as out-of-closure are the ones this seat
    exists to run into. A generator that stopped producing them would still be green."""
    c = snap_coverage(200)
    for fam in ("hidden", "lagged", "regime", "chain", "quadratic"):
        assert c[fam] > 0, f"the shipped generator can no longer produce: {fam}"
    assert c["slots=2"] > 0 and c["slots=4"] > 0, "the slot count has collapsed"
    # NO `a relational slot` LINE. It was written and then removed, because it cannot be
    # the finding: `chain` and `lagged` are asserted above and both are relational, so
    # every narrowing that empties the bindings trips a family first -- and the one case
    # left over, a relational family with `reads=None`, dies in the world with
    # `KeyError: None` before any history exists to check. A line that can never fire is
    # not a weaker check, it reads as coverage that is not there.


def test_generator_reaches_the_hard_cases():
    """BOTH EDGES of the generator's width. Every shape that has broken something must
    still be reachable; if the generator narrows, this fails before the loop passes over
    an empty search."""
    c = coverage(400)
    for shape in ("two slots share a rule", "a slot outside the closure",
                  "an action-dependent slot"):
        assert c[shape] > 0, f"the generator can no longer produce: {shape}"
    assert c["slots=2"] > 0 and c["slots=4"] > 0, "the slot count has collapsed"


def test_the_atom_set_builds_under_every_arm_state():
    """THE ATOM SET MUST BUILD WITH THE FOLD ARM ON *AND* OFF, and it did not for two days.

    `arc_holdout.play` sets `arc_atoms._ITERATE = True` before building the atom set, under
    Isaiah's 2026-09-24 ruling. From `9a2f32d` -- the admitting-clause guard -- `three_spaces`
    RAISED in exactly that configuration, because the four fold atoms had no `ADMITTED` entry.
    **The ARC path could not construct an agent, and nothing noticed**: the board stop forbids
    running it, the toy world never sets the arm, and every seat here builds with it off.

    AND THE TWO GUARDS PULL OPPOSITE WAYS ON AN ARM-GATED ATOM -- which is why the repair is an
    arm-gated admission rather than a static entry. Arm ON: the atom exists and needs a clause.
    Arm OFF: the atom does not exist and a clause for it is an orphan the second guard refuses.
    A static table cannot satisfy both, and satisfying only the one you happen to run is how
    this survived.

    **A GUARD WHOSE FAILURE PATH IS NEVER EXERCISED IS INDISTINGUISHABLE FROM ONE THAT CANNOT
    FAIL.** Both guards were correct throughout. Neither was ever run in the configuration that
    would refuse it.
    """
    import arc_atoms
    import arc_predict

    was = arc_atoms._ITERATE
    try:
        for arm in (True, False):
            arc_atoms._ITERATE = arm
            atoms = arc_atoms.three_spaces(arc_predict.predict())
            folds = {a.name for a in atoms} & {"cells", "cell_row", "cell_col", "count_true"}
            assert folds if arm else not folds, (
                f"_ITERATE={arm} produced folds={sorted(folds)} -- the arm does not gate them")
            if arm:
                # THE CLAUSE MUST CROSS, not merely exist: an unstamped fold atom reads to the
                # ablation as `necessary`, which is its BLIND category.
                unstamped = sorted(a.name for a in atoms
                                   if a.name in folds and a.admitted != "handed")
                assert not unstamped, f"fold atoms admitted by a ruling, unstamped: {unstamped}"
    finally:
        arc_atoms._ITERATE = was


# **`test_b5_still_fires_on_the_pinned_world` MOVED TO `conform/owed.py` -- 2026-09-30,
# ruling 6, when the bargain-fit flip landed.** Its PRECONDITION stopped holding, not its
# verdict: `seed 3 starves no slot`, so B5's reproduction LOST ITS SUBJECT. Its own message
# anticipated exactly this and forbade the easy move -- *a tripwire cannot tell "the defect
# is gone" from "the trajectory moved past it" ... Do not delete it.* So it is moved intact,
# runnable, and re-pinned when a starving world exists. Census behind the call: 0 of 60 seeds
# starve with the flip on, and a control recovers the pinned pair.


def test_a5_is_reproducible_without_a_world():
    """A5's defect at the STATE level, so no trajectory can move it. **Reviewer, 2026-09-28.**

    Both world-pinned tripwires lost their subject today when the action seam changed which
    action lands on which step -- B5's world stopped starving, A5's stopped citing across slots.
    **A defect whose only reproduction is a trajectory is a defect that can vanish from the
    suite without being fixed**, and A5's cause is already pinned to one line, so it does not
    need a world at all.

    THE DEFECT: `gamma.is_settled(name)` is keyed by TERM while kernel A5 keys `(slot, term)`.
    The consumer is `tether.py`'s `_stood.append((slot, name, self.gamma.is_settled(name)))` --
    it has the slot in its hand and cannot pass it, because the API has nowhere to put it.
    **So one settlement anywhere licenses citation everywhere, and the state cannot express
    otherwise.**

    THIS IS AN EXPECTED FAILURE. It passes while the defect stands and FAILS when the fix lands,
    which forces its own update -- and unlike the world-pinned pair, the only thing that can
    make it fail is the repair.

    **IT REPLACES `test_a5_still_fires_on_the_pinned_world`, WHICH IS RETIRED, AND THE PANEL
    READING IT PRODUCED IS KEPT HERE RATHER THAN LOST WITH IT:**

        POPULATION   48 worlds -- `spec_for(seed, n)`, seed 0..23, n in (4, 5)
        at 12 steps  cross-slot citations 0 of 48    A5 fires 0
        at 25 steps  cross-slot citations 1 of 48    A5 fires 1      <- seed 8, 1 of 1
        CONTROL      same-slot allowed citations    23 of 48
        on seed 8    18 steps is the THRESHOLD (cross 1); 14 and 16 do not fire

    **So A5's situation is RARE rather than absent** -- the 0-of-48 at 12 steps was a budget
    artefact and was nearly published as *the panel cannot show A5*. The control is what makes
    the 1 readable: 23 worlds do cite settled terms, so the scan works.

    **AND THE RETIREMENT IS A BUDGET DECISION MADE IN THE OPEN.** The `shipped` seat ran 2m09s
    against a 120s limit and reported DID-NOT-RUN, which is correctly not a pass. Measured: 21
    module-level tests total 115.2s, the two most expensive being
    `test_the_residual_bound_loses_nothing` (22.9s) and
    `test_a_mutation_moves_attention_and_never_the_action` (21.7s) -- **so the seat was already
    within a few seconds of the limit before today.** The world-pinned A5 cost 18.1s, has lost
    its subject TWICE in one day, and reproduced nothing this test does not. The world-pinned
    B5 is KEPT at 8.4s because its 2-of-2 is what answers whether its re-seed was fitting.

    **The hand-written world it used is recorded in this repository's history and in `INDEX.md`;
    what is retired is a 18-second trajectory that certified less than three assertions do.**
    """
    import inspect

    import snaps
    from gamma import Gamma

    g = Gamma(snaps._atoms())
    g.settle("x")
    assert g.is_settled("x"), "fixture: a settled term must read settled"
    # THE REPRODUCTION, and it is one line: there is no slot to ask about.
    assert "slot" not in inspect.signature(g.is_settled).parameters, (
        "A5 IS FIXED: `is_settled` now takes a slot, so a settlement no longer licenses every "
        "slot. Invert this to assert the slot IS a parameter, rename it, and it becomes the "
        "regression test. Then check `settle` takes one too, and that `_stood` passes it.")
    assert "slot" not in inspect.signature(g.settle).parameters, (
        "`settle` takes a slot but `is_settled` does not -- half the repair. The state can now "
        "record a per-slot settlement and nothing can read it back.")


def test_the_keyed_reach_loses_nothing():
    """THE INDEX IS A CHEAPER ROUTE TO THE SAME SET, NEVER A SMALLER SET.

    The reviewer's ruling of 2026-09-27: *indexing is not a cheaper search -- same closure, same
    candidates, same results, reached by key rather than by enumeration.* **That is a claim with
    a failure mode, and the failure mode is silent**: an index that quietly drops entries is
    indistinguishable from a fast one at every call site, and reads as a speedup.

    So the check is set equality against the enumeration the index replaces, and the MUTATION
    CONTROL is the half that matters -- without it, a `reach` that returned its input unchanged
    would pass. `_cannot_pay` is the precedent and the reason: it filtered on what a term *ought
    to need* and LOST A CLOSING TERM, and nothing noticed because a missing candidate does not
    fail, it abstains.

    NOT A TEST THAT THE LIBRARY IS GOOD. If `library/` is absent the vocabulary is empty and the
    agent must still run -- the ablation clause needs a wipe to be survivable -- so an empty
    load SKIPS rather than fails, and says so.
    """
    import inherited

    lib = inherited.load()
    by_tag = lib["tags"].get("by_tag") or {}
    if not by_tag:
        print("  keyed reach: SKIPPED -- library/ is absent, vocabulary empty")
        return

    want = {"POSITION": 1.0, "MOTION": 1.0, "CHANGE": 0.5}
    # THE ENUMERATION THIS REPLACES, written out rather than called: a check that reuses the
    # implementation agrees with it by construction, which is the measurement that cannot fail.
    scan = {k for tag in want for kind in ("atoms", "molecules")
            for k in (by_tag.get(tag) or {}).get(kind) or []}
    keyed = set(inherited.reach(want))
    assert keyed == scan, (
        f"the keyed reach is not the enumeration: {len(keyed)} vs {len(scan)}, "
        f"missing {sorted(scan - keyed)[:5]}, invented {sorted(keyed - scan)[:5]}")
    assert len(keyed) > 100, f"only {len(keyed)} candidates -- the index is not being read"

    # MUTATION CONTROL 1 -- a reach that GATES on reach_tier must be caught. This is the exact
    # filter the plan was tempted by, and 1,132 of 1,748 atoms carry no tier at all.
    gated = {k for k in scan if str((inherited.entry(k) or {}).get("reach_tier")) in "01"}
    assert gated != scan, "the tier filter removes nothing here -- the control cannot fire"
    assert keyed != gated, "a tier-GATED reach passed the equality check; the guard is inert"

    # MUTATION CONTROL 2 -- ordering must actually order, or `reach` is returning arbitrary
    # keys and the equality above would still hold.
    ordered = inherited.reach(want)
    assert ordered != sorted(ordered), "the result is in name order -- nothing ranked it"

    # AND THE PAIR PATH, WHICH IS WHERE A SCAN WAS ACTUALLY HIDING. `reach` iterated all 477
    # `by_pair` entries testing each against the cue -- a scan inside the function whose whole
    # point is that there is no scan (the reviewer, 2026-09-27). It is keyed now, so the check
    # is the same one the tags get: the keys BUILT from the lit tags must be exactly the keys a
    # full pass would have selected.
    by_pair = lib["tags"].get("by_pair") or {}
    lit = sorted(want)
    keyed = {f"{a}+{b}" for i, a in enumerate(lit) for b in lit[i + 1:]
             if f"{a}+{b}" in by_pair}
    swept = {p for p in by_pair
             if len(p.split("+")) == 2 and all(x in want for x in p.split("+"))}
    assert keyed == swept, f"the keyed pair lookup lost {sorted(swept - keyed)[:5]}"
    assert keyed, "no pair was lit -- this control cannot distinguish keyed from broken"


def test_the_inherited_vocabulary_is_not_the_held_library():
    """`gamma.library` AND `library/` ARE TWO THINGS AND THE PLAN CONFLATED THEM.

    Filed 2026-09-27 as the fifth `A6i` of one day. `Gamma.library` is `dict[str, Term]` -- what
    the agent HOLDS, minted or imported and earned -- and `retrieval.retrieve` scans it. The
    inherited vocabulary is 4,042 entries it can REACH FOR. A build item pointed the keyed
    lookup at `retrieve()` on the strength of the shared word, and `retrieve()` was never the
    enumeration the reviewer's ruling was about: `_operand_fits` fires 850,833 times from
    `mint`.

    **The module is named `inherited` and not `library` for this reason**, and this check pins
    it so the name cannot drift back: a future `library.py` would make the collision permanent.
    """
    import gamma
    import gridworld
    import inherited
    from world import bind

    assert not (Path(__file__).parent.parent / "library.py").exists(), (
        "a module named `library.py` now exists -- that is the third sense of `library` in "
        "this package and the collision `inherited.py` was named to avoid")

    env = bind(gridworld.boards(1, start=3)[0])
    held = set(gamma.Gamma(env.atoms()).library)
    reachable = set(inherited.load()["atoms"])
    if not reachable:
        print("  two vocabularies: SKIPPED -- library/ is absent")
        return
    # THE POINT IS THE DISPROPORTION, and it is what makes the two words worth separating:
    # the agent HOLDS tens of terms and can REACH FOR thousands. A build item that scanned
    # the held set believed it was scanning the inherited one.
    assert len(reachable) > 10 * max(1, len(held)), (
        f"held {len(held)} vs reachable {len(reachable)} -- these are supposed to be "
        "different orders of magnitude; check which object is being measured")
    assert not (held & reachable), (
        f"a key is in BOTH vocabularies ({sorted(held & reachable)[:3]}) -- the agent's own "
        "atoms are keyed `name` and the inherited ones `DOMAIN|Name`, so an overlap means one "
        "side has been re-keyed and the ablation can no longer tell given from earned apart")



def test_the_quantifiers_quantify():
    """`ALL/SOME/ONE/NONE` range over a scope and DISAGREE with each other.

    `DISCOVERY` Q21 specifies a molecule as a quantifier over a scope returning a verdict and
    a degree. The atom set supplied `all`, `any` and `none` typed `PRED -> OBJ`, taking a
    SCALAR -- and `all` and `any` were BYTE-IDENTICAL, `ONE` was absent. So every objective
    the agent could form was closed by a quantifier that does not quantify: the chain
    evaluates, returns 1, and means *this one shape is symmetric* while its name says *the
    shapes are symmetric*.

    THE CONTROL IS THE OLD PAIR, AND IT IS WHY THIS IS NOT CIRCULAR. The defect is not
    *a quantifier is wrong*, which nothing can check without a second opinion -- it is *two
    quantifiers that must differ do not*. So the test asserts the new four DISAGREE on a
    scope built to separate them, and asserts in the same breath that the old two still
    AGREE everywhere. A repair that made the new four identical would satisfy any
    single-quantifier assertion and fails this one.
    """
    import arc_atoms
    import arc_predict
    from gamma import Ctx, Term

    was = arc_atoms._ITERATE
    try:
        arc_atoms._ITERATE = True
        A = {a.name: a for a in arc_atoms.three_spaces(arc_predict.predict())}
        ctx = Ctx()

        def run(shape, closer):
            return Term(tuple(A[n] for n in ("cells", "cell_row", "parity", closer))).apply(
                shape, ctx)

        # THREE SCOPES, EACH SEPARATING A DIFFERENT PAIR. `parity` is true on an ODD row, so
        # the scope is the cells' row indices and the fraction is what the quantifier reads.
        cases = {
            # rows {0,1} -- three of six odd: only SOME holds
            frozenset({(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)}):
                {"all_of": 0, "some_of": 1, "one_of": 0, "none_of": 0},
            # rows {0,2} -- none odd: only NONE holds
            frozenset({(0, 0), (0, 1), (2, 0), (2, 1)}):
                {"all_of": 0, "some_of": 0, "one_of": 0, "none_of": 1},
            # one cell on an odd row: SOME and ONE both hold, and they are different atoms
            frozenset({(0, 0), (0, 1), (1, 0)}):
                {"all_of": 0, "some_of": 1, "one_of": 1, "none_of": 0},
            # rows {1,3} -- every cell odd: ALL and SOME hold, ONE does not
            frozenset({(1, 0), (1, 1), (3, 0)}):
                {"all_of": 1, "some_of": 1, "one_of": 0, "none_of": 0},
        }
        for shape, want in cases.items():
            for closer, expect in want.items():
                got = run(shape, closer)
                assert got == expect, (
                    f"{closer} on {sorted(shape)} gave {got!r}, expected {expect} -- "
                    f"the quantifier does not range over the scope")

        # ONE IS REACHED, not merely present. A quantifier nothing separates from `some` is
        # the defect this test exists for, wearing a new name.
        assert any(run(sh, "one_of") != run(sh, "some_of") for sh in cases), (
            "`one_of` never differs from `some_of` on the pinned scopes -- it is a second "
            "spelling of SOME and `ONE` is still absent")
        assert any(run(sh, "all_of") != run(sh, "some_of") for sh in cases), (
            "`all_of` never differs from `some_of` -- the byte-identical defect, renamed")

        # THE DEGREE IS EXPRESSIBLE: `count_true` is the numerator and `size` the denominator.
        # Two integers rather than a ratio, which is what separates a static series from a
        # live-but-insensitive one.
        big = next(iter(cases))
        n = Term(tuple(A[x] for x in ("cells", "cell_row", "parity", "count_true"))).apply(
            big, ctx)
        t = Term(tuple(A[x] for x in ("cells", "cell_row", "parity", "size"))).apply(big, ctx)
        assert (n, t) == (3, 6), f"degree numerator/denominator reads {(n, t)}, expected (3, 6)"

        # THE CONTROL. The old pair is still one function under two names -- if this ever
        # goes false the defect was repaired somewhere else and this test's subject moved.
        for sh in cases:
            assert run(sh, "all") == run(sh, "any"), (
                "`all` and `any` now differ -- the old quantifiers were repaired in place; "
                "this test asserts the NEW path and its control is stale")
    finally:
        arc_atoms._ITERATE = was


def test_the_seam_varies_what_it_explores_with():
    """`ELICIT` must not keep choosing one button. **The collapse must not ride below the seam.**

    **THE REVIEWER, 2026-09-28:** `discriminate:learned` pressed `ACTION2` 105 of 150 times on
    `ls20` -- *the collapse System 0 exists to prevent*. If `ELICIT` were realised by "the most
    informative action" alone, the same scoring keeps choosing one button and **exploration that
    presses one button is not exploration.**

    **AND THIS CHECK EXISTS BECAUSE `m2` PINS THE SEAM OFF.** Routing `probe`/`draw` through the
    interface moved the m2 trajectory and three of its scenarios failed; demonstrated to be
    trajectory and not contract (all three pass with the old draw restored), so the fixture pins
    the old policy. **A pin with no certifying check is how a suite keeps a mechanism green by
    never running it** -- `check_one_bargain` was MIGRATED rather than pinned around for exactly
    that reason. This is the migration's other half.

    THE CONTROL IS THE DEGENERATE REALISER. A rule that always returned `offered[0]` would
    satisfy "an action was chosen"; it fails this, because the assertion is on VARIETY.
    """
    import interface as IFace

    f = IFace.Interface()
    offered = ("A", "B", "C")
    ctx = (("edge", 1),)
    want = IFace.Intent(IFace.ELICIT)
    taken = []
    for i in range(6):
        r = f.realise(want, offered, ctx)
        assert r is not None, "ELICIT was refused while actions were offered"
        taken.append(r.action)
        f.audit(r, {"x": 0}, {"x": i % 2}, ctx)

    assert len(set(taken[:3])) == 3, (
        f"the first three explorations repeated: {taken[:3]} -- unmapped actions must be "
        f"taken before any is repeated")
    assert max(taken.count(a) for a in offered) <= 2, (
        f"one action dominated exploration: {taken} -- this is the ACTION2 collapse below "
        f"the seam")

    # AND A NON-EXPLORATORY INTENT WITH NOTHING KNOWN MUST ABSTAIN, NEVER GUESS. An interface
    # that substitutes something when it cannot translate is the encoded answer relocated.
    assert f.realise(IFace.Intent(IFace.TOUCH, "o0", "o1"), offered, ctx) is None, (
        "a non-exploratory intent was realised from an empty table -- the interface guessed")


def test_every_exit_has_a_phase():
    """No exit of `choose` may land in a phase column nobody chose for it.

    **THREE REPAIRS AT ONE LINE IN ONE DAY, and the third still had an `else`.** `== "discriminate"`
    admitted 1 of 3 labels and read `directed 0.0` on ten boards; a PREFIX broke the moment
    `discriminate:learned` became `distinguish`; an EXCLUSION flipped `system0` PROBE -> DIRECTED
    on 11 of 25 actions. **Every one was silent, and every one moved a published column.**

    The reviewer's shape (2026-09-28): an unlisted label must FAIL LOUDLY rather than default --
    same idea as narratability refusing a row with no sentence, so the next exit has to be
    classified when it is added instead of found in a census afterwards.

    **THE LABELS ARE READ FROM THE SOURCE, NOT FROM A LIST HERE.** A list here would agree with
    `PHASE_OF` by construction, which is the measurement that cannot fail -- the same reason
    `conform/arms.py` censuses the code rather than its own table.
    """
    import ast

    import tether

    src = ast.parse(Path(tether.__file__).read_text(encoding="utf-8"))
    fn = next(n for n in ast.walk(src)
              if isinstance(n, ast.FunctionDef) and n.name == "choose")
    labels, opaque = set(), []
    for n in ast.walk(fn):
        if not isinstance(n, ast.Return):
            continue
        v = n.value
        if isinstance(v, ast.Tuple) and len(v.elts) == 2:
            lab = v.elts[1]
            if isinstance(lab, ast.Constant) and isinstance(lab.value, str):
                labels.add(lab.value)
            else:
                opaque.append((n.lineno, ast.unparse(lab)))
        else:
            opaque.append((n.lineno, ast.unparse(v) if v is not None else "None"))
    assert labels, "no `return action, label` pairs found in `choose` -- the scan is broken"
    # **A LABEL THIS SCAN CANNOT READ IS THE SAME SILENCE ONE LEVEL ALONG -- the reviewer,
    # 2026-09-28, asking whether any label is built at runtime or comes from a helper.**
    # Measured when this was written: all six are literals and there are no non-tuple returns.
    # **Nothing enforced that, and a skipped label would have passed the check above for the
    # best possible reason -- it was never seen.** So an unreadable return FAILS rather than
    # being ignored: a runtime-built label cannot be classified statically, and the honest
    # answer is to say so at the moment it appears.
    assert not opaque, (
        f"`choose` has returns this scan cannot classify: {opaque}. A label built at runtime "
        f"cannot be checked against `PHASE_OF` -- make it a literal, or classify it where it "
        f"is built")
    missing = sorted(labels - set(tether.PHASE_OF))
    assert not missing, (
        f"`choose` can return {missing} and `PHASE_OF` does not classify them. Classify the "
        f"exit where it is added; a default is how three phase repairs went silent in one day")

    # THE CONTROL: the scan must be able to FAIL. A rule that found nothing would pass the
    # assertion above for the wrong reason, and this file's own history is checkers going quiet.
    assert sorted(labels - {"nope"}) == sorted(labels), "sanity"
    assert "nope" not in tether.PHASE_OF, "fixture: the control label must be unclassified"
    assert sorted((labels | {"nope"}) - set(tether.PHASE_OF)) == ["nope"], (
        "the comparison cannot detect an unclassified label -- it certifies nothing")


def test_asking_the_interface_does_not_change_it():
    """`realise` must be a QUESTION. **The reviewer, 2026-09-28, and it is not about cost.**

    `_runnable` -- the level-boundary check -- now calls `realise` for every step of every
    shelved routine at every mint, purely to ask *could this run here*. **If asking changed the
    table, the boundary check would be teaching the model things the agent never did**, and the
    model's whole claim is that it is built only by acting.

    Verified once by reading the source and that is exactly what does not hold: *a guard whose
    failure path is never exercised is indistinguishable from one that cannot fail*, and nothing
    stopped a future `realise` from recording a miss. So it is a check.

    **THE CONTROL IS THE AUDIT.** A comparison that could not move would pass on a frozen
    object, so the same snapshot is taken across an `audit` and must DIFFER -- otherwise this
    is measuring a report that never changes rather than a realiser that never writes.
    """
    import copy

    import interface as IFace

    f = IFace.Interface()
    offered = ("A", "B", "C")
    ctx = (("edge", 1),)
    f.audit(IFace.Realisation("A"), {"x": 0}, {"x": 1}, ctx)
    before = (copy.deepcopy(f.table), f.report(), f.audits)

    for intent in (IFace.Intent(IFace.ELICIT),
                   IFace.Intent(IFace.BECOME, "x", "+"),
                   IFace.Intent(IFace.BECOME, "x", value=1),
                   IFace.Intent(IFace.TOUCH, "o0", "o1")):
        f.realise(intent, offered, ctx, {"x": 0})
    assert (f.table, f.report(), f.audits) == before, (
        "asking the interface changed it -- the boundary check would be writing a model "
        "the agent never earned by acting")

    f.audit(IFace.Realisation("B"), {"x": 1}, {"x": 2}, ctx)
    assert (f.table, f.report(), f.audits) != before, (
        "the snapshot did not move across an audit -- this comparison cannot fail and "
        "certifies nothing")


def test_a_carried_term_can_reach_candidacy():
    """**ISAIAH'S REUSE RULING, WITH ITS FAILURE PATH EXERCISED.** *Reuse without re-deriving.*
    A carried term settles through `settle`, whose guard is `born = self.candidates.get(name)`
    -- and `candidates` had ONE writer, mint, so an IMPORTED term could never clear it and
    could not settle on any board. `_carry` is the second writer.

    **THE LIVE RUN CANNOT REACH THIS AND THAT IS WHY THE TEST EXISTS.** Measured on gridworld
    11 -> 7: a carried term passes `_explains` ONCE in 15,312 candidate rebindings, so the
    bind that would call `_carry` is astronomically rare and the guard would sit unexercised.
    *A guard whose failure path is never exercised is indistinguishable from one that cannot
    fail.* So the bind is forced here rather than waited for.

    **THE CONTROLS ARE THE POINT.** A `_carry` that registered EVERYTHING would pass the
    headline and certify nothing -- and the unscoped first version did exactly that, moving
    local terms' birth cycles and taking M2 to 27/30. So: a LOCAL term must NOT be registered
    by this door, and an already-waiting term must KEEP its original cycle.
    """
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    env = world.bind(gridworld.GridWorld(seed=3))
    g = gamma.Gamma(env.atoms())
    ag = tether.Agent(env, g, tether.Config(max_depth=2), ledger.Ledger())

    atoms = [a.name for a in g.atoms][:2]
    carried = gamma.Term(tuple(g._by_name[n] for n in atoms), origin=gamma.IMPORTED)
    local = gamma.Term(tuple(g._by_name[n] for n in reversed(atoms)), origin=gamma.MINTED)
    for t in (carried, local):
        g._install(t, seq=-2, residual=None, admitted=None)

    # THE SUBJECT: an imported term reaches candidacy through the bind door.
    ag.cycle = 5
    ag._carry(carried.name)
    assert carried.name in ag.candidates, "an IMPORTED term still cannot reach candidacy"
    assert ag.candidates[carried.name] == 5

    # CONTROL 1 -- a LOCAL term is not registered here. Mint is its door, and giving it a
    # second earlier one is what broke three seats.
    ag._carry(local.name)
    assert local.name not in ag.candidates, (
        "`_carry` registered a MINTED term -- that is the unscoped version, and it moves "
        "birth cycles for terms that already had a route")

    # CONTROL 2 -- an already-waiting term keeps its ORIGINAL cycle, or `born >= self.cycle`
    # would be re-armed every bind and the term could never settle.
    ag.cycle = 9
    ag._carry(carried.name)
    assert ag.candidates[carried.name] == 5, "a re-bind reset the birth cycle"

    # CONTROL 3 -- the door is closed when the arm is off, so the A/B is a real A/B.
    was, tether._CARRY_CANDIDATE = tether._CARRY_CANDIDATE, False
    try:
        other = gamma.Term(tuple(g._by_name[n] for n in atoms[:1]), origin=gamma.IMPORTED)
        g._install(other, seq=-2, residual=None, admitted=None)
        ag._carry(other.name)
        assert other.name not in ag.candidates, "the OFF arm still wrote -- the A/B is not one"
    finally:
        tether._CARRY_CANDIDATE = was


def test_a_candidate_survives_a_level_and_is_dormant_until_bound_here():
    """**ISAIAH'S TWO RULINGS OF 2026-09-30, AND THEY ARE ONE TEST BECAUSE THEY ARE ONE
    MECHANISM.** *Rules awaiting the ground survive level changes* -- and *"it needs to have
    similar conditions"*, so a survivor is DORMANT rather than live.

    **THE SECOND IS WHAT MAKES THE FIRST SAFE, WHICH IS THE WHOLE POINT.** A candidate keeps
    its birth cycle across the boundary, so `born >= self.cycle` is already false: remove the
    clear WITHOUT the dormancy stamp and the survivor settles on the new level on its first
    observation there, against evidence it never saw there. That is the failure this asserts
    against, not a hypothetical.

    **THE CONTROLS ARE THE POINT.** A stamp that always matched would pass the headline and
    certify nothing, so: the survivor must still be PRESENT (dormant is not deleted), it must
    NOT be settle-eligible while its stamp is stale, and binding it here must wake it.
    """
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    env = world.bind(gridworld.GridWorld(seed=4))
    g = gamma.Gamma(env.atoms())
    ag = tether.Agent(env, g, tether.Config(max_depth=2), ledger.Ledger())

    nm = [a.name for a in g.atoms][:2]
    t = gamma.Term(tuple(g._by_name[n] for n in nm), origin=gamma.IMPORTED)
    g._install(t, seq=-2, residual=None, admitted=None)
    ag.cycle, ag.level = 3, 0
    ag._carry(t.name)
    assert ag._cand_level[t.name] == 0, "candidacy was not stamped with its level"

    # THE BOUNDARY. `retarget` must NOT wipe it -- that is the first ruling. It does not
    # touch `self.cycle`, which is the fact that makes the stamp load-bearing: the cycle
    # keeps counting across levels, so a survivor's `born` falls further behind and
    # `born >= self.cycle` stops holding it almost immediately.
    ag.retarget(env, 1)
    ag.cycle = 9
    assert t.name in ag.candidates, (
        "the level boundary wiped a rule awaiting the ground -- Isaiah ruled it survives")

    # DORMANT: the stamp still names the old level, so it is not eligible HERE...
    assert ag._cand_level.get(t.name) != ag.level, (
        "a survivor came through the boundary already live -- without the stamp it would "
        "settle on the new level against evidence it never saw there")
    # ...and its birth cycle is old, so the ONLY thing holding it is the stamp. Stated as an
    # assertion because if `born` were doing the work this test would prove nothing.
    assert ag.candidates[t.name] < ag.cycle, "born is gating it, so the stamp is untested here"

    # WAKING IT: bound on this level, and the stamp moves while the birth cycle does not.
    born = ag.candidates[t.name]
    ag._carry(t.name)
    assert ag._cand_level[t.name] == ag.level, "binding here did not wake the candidate"
    assert ag.candidates[t.name] == born, "waking moved the birth cycle"
    assert any(e.detail.get("was") is not None and e.event == "candidate_woken"
               for e in ag.led.entries), "the reactivation left no row"


def test_a_rejection_records_where_it_was_taken():
    """**ISAIAH, 2026-09-30:** *"I wouldn't want the agent to throw away a useful routine just
    because one board didn't have the mechanic."* Measured before building: NO refutation key
    carried a board or level id -- `_reject_key`, `_gap_key` and `rejections` all had nowhere
    to put one -- so "failed" could not be read as "failed THERE".

    **A RECORD, NOT A RULE.** `rejections` is untouched and the ceiling reads the same scalar,
    so every run is unchanged. How a failure taken elsewhere is WEIGHED is Isaiah's and open.

    **BOTH PATHS, BECAUSE ONLY ONE OF THEM HAPPENS ON GRIDWORLD.** A 12-cycle run stamps 8 of
    8 refuted TERMS and reaches ZERO routine refutations, so the routine path would ship
    unexercised and a dead field reads exactly like a clean one -- worse than no field, since
    an empty `where` looks like evidence of no failures.
    """
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    st = gamma.Standing()
    st.refute(1, where="g:L0")
    st.refute(2, where="g:L0")
    st.refute(3, where="g:L1")
    assert st.where == {"g:L0": 2, "g:L1": 1}, f"the stamp did not accumulate: {st.where}"

    # CONTROL 1 -- the scalar the ceiling reads is untouched by the stamp, so no run moves.
    bare = gamma.Standing()
    for t in (1, 2, 3):
        bare.refute(t)
    assert abs(bare.rejections - st.rejections) < 1e-9, "stamping changed the decayed total"
    assert bare.where == {}, "an unstamped refutation invented a scope"

    env = world.bind(gridworld.GridWorld(seed=5))
    g = gamma.Gamma(env.atoms())
    ag = tether.Agent(env, g, tether.Config(max_depth=2), ledger.Ledger())

    # CONTROL 2 -- the scope names BOTH scales. Isaiah ruled on boards; the same failure
    # exists one scale down at levels, and a coarser scope cannot be recovered from a finer
    # one after the fact, so both are written and neither is weighed.
    ag.level = 2
    assert ag._scope == f"{g.game}:L2", f"the scope lost a scale: {ag._scope}"

    # THE TERM PATH, through the wrapper the agent actually calls.
    nm = [a.name for a in g.atoms][0]
    g.settle(nm)
    g.refute(nm, where=ag._scope)
    assert g.standing[nm].where == {f"{g.game}:L2": 1}, "the term path did not stamp"

    # THE ROUTINE PATH -- unreached by any gridworld run, which is why it is forced here.
    k = ("slot", "shape")
    ag.refuted.setdefault(k, gamma.Standing(last_tick=0)).refute(1, where=ag._scope)
    assert ag.refuted[k].where == {f"{g.game}:L2": 1}, (
        "a ROUTINE refutation records no scope -- the half a live run never exercises")


def test_downrating_moves_a_residual_in_both_directions():
    """Isaiah's downrating ruling, demonstrated AT UNIT LEVEL -- reviewer, 2026-09-30.

    **THE LIVE FIXTURE CANNOT SHOW THIS AND MUST NOT BE BENT UNTIL IT CAN.** On the M2 world
    the discounted member AGREES with the rest of its scope, so the fraction is unchanged --
    correctly. Widening that fixture until the number moves is fitting a panel to its answer,
    which is this seat's most expensive mistake of the day. **A unit test may CONSTRUCT its
    inputs; that is a different act, and the reviewer drew the line.**

    The three rows are the arithmetic of `degree = satisfied / total`: discounting a member
    moves it only when that member DISAGREES with the rest, and WHICH WAY depends on which
    side it was on.
    """
    from tether import objective_degree

    def sat(v):                                   # 1 satisfies, 0 does not
        return bool(v)

    # ROW 1 -- the discounted member FAILS while the other satisfies: degree RISES, so
    # `R_goal = 1 - degree` FALLS. The goal is closer once a member that could never help
    # stops being counted against it.
    plain = objective_degree(sat, (0, 1))
    cut = objective_degree(sat, (0, 1), None, [0.0, 1.0])
    assert plain == 0.5 and cut == 1.0, f"expected 0.5 -> 1.0, got {plain} -> {cut}"
    assert (1.0 - cut) < (1.0 - plain), "discounting a FAILING member did not lower R_goal"

    # ROW 2 -- the discounted member SATISFIES while the other fails: degree FALLS, R_goal
    # RISES. **This is the dangerous direction the reviewer named**: downrating can MAKE a
    # goal where there was less of one, so it is asserted rather than hoped about.
    plain2 = objective_degree(sat, (1, 0))
    cut2 = objective_degree(sat, (1, 0), None, [0.0, 1.0])
    assert plain2 == 0.5 and cut2 == 0.0, f"expected 0.5 -> 0.0, got {plain2} -> {cut2}"
    assert (1.0 - cut2) > (1.0 - plain2), "discounting a SATISFYING member did not raise R_goal"

    # ROW 3 -- the discounted member AGREES: unchanged, which is why the live fixture reads
    # nothing and why that reading is not evidence of an inert mechanism.
    for scope in ((0, 0), (1, 1)):
        assert objective_degree(sat, scope) == objective_degree(sat, scope, None, [0.0, 1.0]), (
            f"discounting a member that AGREES moved the fraction on {scope}")

    # ALL-INERT -- every member discounted. **DOWNRATING STEPS ASIDE: THE SCOPE IS COUNTED
    # UNWEIGHTED. ISAIAH, 2026-10-01.**
    #
    # **THIS ASSERTION USED TO DEMAND `None` AND IT WAS COMMITTED AS CONTESTED** -- 07125ff's
    # message flagged it as a choice under appeal rather than a settled one. The reasoning
    # was *an absent population is not a satisfied one*, which is right for an EMPTY scope
    # and wrong here: **an empty scope is ABSENT, a scope the agent merely has not MOVED is
    # NO EVIDENCE.** Collapsing the two silenced the agent -- 0 PLAN rows on one arm.
    #
    # NO EVIDENCE MEANS FALL BACK, NEVER FALL SILENT.
    for scope in ((0, 0), (1, 1), (0, 1)):
        assert objective_degree(sat, scope, None, [0.0, 0.0]) == objective_degree(sat, scope), (
            f"an all-inert scope {scope} did not step aside to the UNWEIGHTED degree")
    # AND AN EMPTY SCOPE IS STILL ABSENT -- the distinction the step-aside rule turns on.
    assert objective_degree(sat, ()) is None, "an EMPTY scope stopped reading as absent"

    # **AND A GOAL STILL EXISTS AFTERWARDS, WHICH IS THE POINT AND NOT A COROLLARY** -- the
    # reviewer, 2026-10-01. The failure this rule exists to prevent was not a wrong NUMBER,
    # it was `goal_residual` returning `None` on a live scope: no goal, so nothing planned,
    # so 0 PLAN rows and a routine that forms without it, gone. **Asserting the degree is
    # right does not assert that a goal survived**, so both are asserted.
    for scope in ((0, 0), (1, 1), (0, 1)):
        deg = objective_degree(sat, scope, None, [0.0] * len(scope))
        assert deg is not None, (
            f"an all-inert LIVE scope {scope} produced no degree -- `goal_residual` would "
            f"return None here and the agent would have no goal to pursue at all")
        assert 0.0 <= (1.0 - deg) <= 1.0, (
            f"R_goal = 1 - degree left the unit interval on {scope}: {1.0 - deg}")

    # MUTATION CONTROL -- restore the `None` branch and the assertion above must fail. Without
    # it this passes on any implementation that returns a number, including one that never
    # steps aside because nothing was ever fully discounted.
    _seen = [True, False]
    _all_cut = [0.0, 0.0]
    _tot = sum(w for v, w in zip(_seen, _all_cut, strict=False) if v is not None)
    assert _tot <= 0.0, "the control's premise is gone: an all-inert scope no longer sums to 0"

    # MUTATION CONTROL -- drop the weights and the two directional rows must stop holding.
    # Without it this passes on a `weights` parameter that is silently ignored.
    assert objective_degree(sat, (0, 1)) != cut, "the weights changed nothing on row 1"
    assert objective_degree(sat, (1, 0)) != cut2, "the weights changed nothing on row 2"


def test_a_trial_miss_is_not_a_refusal():
    """**ISAIAH'S (c), 2026-09-30: count misprediction-while-candidate SEPARATELY from
    refusal-after-settling. Two quantities, two names.**

    THE DEFECT IT CLOSES WAS REPRODUCED, NOT REASONED. `refute` is called on every
    mispredicting bound term and `settle` does not reset the total, so a term that made five
    mistakes ON TRIAL carried 4.24 into a ceiling of 1.0 and was unsettled by its FIRST real
    refusal. It was demoted for mistakes made before it had anything to lose.

    **AND THE CEILING READS A COUNTER, NOT A DIFFERENCE.** The first repair had it read
    `rejections - misses`, which OUGHT to cancel to the refusal count and does not -- measured,
    it took TWO refusals to cross a ceiling of 1.0, because the two floats decay through
    different arithmetic and leave error where an exact zero was assumed.

    THE CONTROLS ARE THE POINT. A split that always called everything a miss would pass the
    headline and make the ceiling unreachable, so a term with NO trial history must still
    unsettle on one refusal, and the three counters must stay consistent with each other.
    """
    import gamma
    st = gamma.Standing()
    for t in range(5):                       # five misses while on trial
        st.refute(t)
    assert not st.settled and st.misses > 0, "a never-settled term recorded no miss"
    assert st.refusals == 0.0, "a term that was never settled recorded a REFUSAL"

    # **AT A RAISED CEILING, WHICH IS THE ONLY REGIME WHERE THE TWO RULES DIFFER.** At a
    # ceiling of 1.0 one refusal adds exactly the ceiling, so the blend and the refusal count
    # cross together and an assertion there cannot tell them apart -- the first version of
    # this test asserted at 1.0 and PASSED with the old blended rule restored. The mutation
    # control is what caught it.
    #
    # **ISAIAH'S SOFT-DECAY RULING HAS NOW RAISED IT -- the default is 2.0, not 1.0.** This
    # still passes 3.0 explicitly, so it is unaffected by the default moving and keeps
    # testing the split at a ceiling the split is visible at. CONTROL 1 below is the part
    # that read the default, and it inverted when the ruling landed.
    st.settled_at = 5
    st.refute(6, ceiling=3.0)                # the first REAL refusal
    assert st.settled, (
        "the trial misses still reach the ceiling -- one refusal against a ceiling of 3 "
        "unsettled a term whose only weight was five candidate-era mistakes")

    # AND IT DOES UNSETTLE EVENTUALLY, or the split would have made the ceiling unreachable.
    # **COUNTED, NOT PINNED TO A NUMBER**: refusals DECAY between ticks, so how many it takes
    # is a function of the halflife, and writing the answer here would be a constant fitted
    # to today's rate. The property is *more than one, and finite*.
    n = 1
    while st.settled and n < 20:
        n += 1
        st.refute(6 + n, ceiling=3.0)
    assert not st.settled, "a ceiling of 3 was never reached -- the split made it unreachable"
    assert n > 1, "it still took a single refusal, so the trial misses are still counted"

    # CONTROL 1 -- a term with NO trial history behaves identically. If the split had made
    # the ceiling harder to reach, this is where it would show.
    #
    # **INVERTED 2026-09-30 WHEN ISAIAH RULED THE INTERIM CEILING SOFTER, AND THE INVERSION
    # IS THE POINT RATHER THAN A CONCESSION.** This read `assert not clean.settled` -- that
    # ONE REFUSAL UNSETTLES AT THE DEFAULT -- which was true at 1.0 and is exactly what the
    # ruling forbids. The check fired the moment the default moved to 2.0 and its failure
    # message stated the NEW CORRECT BEHAVIOUR as though it were the fault, which is a check
    # doing its job.
    #
    # **AND IT IS INVERTED WHERE B5 WAS MOVED, WHICH IS THE SAME QUESTION ANSWERED THE OTHER
    # WAY.** B5's PRECONDITION stopped holding -- its world no longer starved anything, so it
    # lost its subject and a verdict there would have been a reading of nothing. HERE THE
    # SUBJECT IS INTACT AND THE RULED BEHAVIOUR CHANGED, so asserting the new rule is the
    # regression test the old assertion was always going to become.
    #
    # Both directions, so it cannot pass by the ceiling drifting either way.
    clean = gamma.Standing()
    clean.settled_at = 0
    clean.refute(1)
    assert clean.settled, (
        "ONE REFUSAL UNSETTLED A CLEAN TERM AT THE DEFAULT CEILING -- Isaiah ruled that out "
        "on 2026-09-30: one failure is not a verdict")
    clean.refute(1)                          # a second, same tick, so nothing decays between
    assert not clean.settled, (
        "TWO refusals in one tick did not reach the default ceiling -- the interim is no "
        "longer the minimum the rule asks for, and a term can never be unsettled")

    # CONTROL 2 -- the two halves still account for the whole, by construction. This is what
    # makes `refusals` a split of `rejections` rather than a fourth quantity beside it.
    acc = gamma.Standing()
    for t in range(3):
        acc.refute(t)
    acc.settled_at = 3
    for t in (4, 5):
        acc.refute(t)
    assert abs(acc.misses + acc.refusals - acc.rejections) < 1e-9, (
        f"the halves stopped summing to the total: {acc.misses} + {acc.refusals} "
        f"!= {acc.rejections}")

    # CONTROL 3 -- the success side records WHERE it paid. Without it a track record has a
    # denominator and no numerator, and ordering by it sorts the most-tried term last.
    import snaps
    g = gamma.Gamma(snaps._atoms())
    nm = [a.name for a in g.atoms][0]
    g.settle(nm, where="g:L0")
    g.settle(nm, where="g:L0")
    g.settle(nm, where="g:L1")
    assert g.standing[nm].paid == {"g:L0": 2, "g:L1": 1}, (
        f"the success record did not accumulate per scope: {g.standing[nm].paid}")


def test_never_two_consecutive_resets():
    """**ISAIAH'S ONE HARD RULE, WITH ITS FAILURE PATH EXERCISED.** *Fully ungated undo and
    reset, just no consecutive resets (reset, reset) in interface.* One `RESET` restarts the
    LEVEL; a second with no action between restarts the GAME FROM LEVEL 1, so the pair is the
    one thing named as able to lose a run.

    **THE CONTROLS ARE THE POINT, because a guard that simply never returns `RESET` would pass
    the headline assertion and certify nothing.** So reset must be REACHABLE when nothing bars
    it, and the bar must CLEAR once another action has run.
    """
    import interface as IFace
    want, ctx = IFace.Intent(IFace.ELICIT), ()

    # CONTROL FIRST: reset is reachable when nothing bars it. Without this a broken guard
    # reads as caution.
    clear = IFace.Interface().realise(want, (IFace.RESET,), ctx, {}, None)
    assert clear is not None and clear.action == IFace.RESET, (
        "reset is not reachable even with nothing barring it -- the assertion below cannot "
        "fail and certifies nothing")

    # THE RULE: after a reset has actually run, a second is never sent -- even when it is the
    # only thing on offer, in which case the interface must abstain.
    f = IFace.Interface()
    first = f.realise(want, (IFace.RESET,), ctx, {}, None)
    f.audit(first, {}, {}, ctx)
    second = f.realise(want, (IFace.RESET,), ctx, {}, None)
    assert second is None or second.action != IFace.RESET, (
        "the interface sent RESET immediately after RESET -- that restarts the GAME from "
        "level 1 and loses every completed level")

    # AND IT RECOVERS: the bar is adjacency, not a ban. Isaiah: the ordinary backtrack is
    # reset, a long replay, then perhaps reset again -- the replay must clear it.
    g = IFace.Interface()
    g.audit(g.realise(want, (IFace.RESET,), ctx, {}, None), {}, {}, ctx)
    g.audit(IFace.Realisation("ACTION1", why="something else ran"), {}, {}, ctx)
    again = g.realise(want, (IFace.RESET,), ctx, {}, None)
    assert again is not None and again.action == IFace.RESET, (
        "the bar did not clear after another action -- that is a ban on reset, not the "
        "adjacency rule, and it would block every ordinary backtrack")

def test_track_record_orders_within_a_fit_level():
    """**THE REVIEWER, 2026-10-01: demonstrate the ordering at unit level, because no live
    fixture separates record from length.** On `test_m2` the library is 65 ATOMS and 4
    COMPOSITES, only composites carry a record, and length already sorts atoms first -- so
    the record slot agrees with the length slot in 0 of 25 tie-groups and the live panel
    cannot show the mechanism either way.

    **A UNIT TEST MAY CONSTRUCT ITS INPUTS; THAT IS NOT FITTING A PANEL.** What is refused is
    tuning a coefficient until a measurement moves. What is required is a case where the
    thing under test CAN act, so that its failing to is a fact about the code.

    Four assertions and a mutation control, all four the reviewer's.
    """
    import gamma as G
    import retrieval
    import snaps

    # EQUAL FIT AND EQUAL LENGTH BY CONSTRUCTION: every `snaps` atom keys identically,
    # `('val','val',1,None,())`, so NOTHING BUT THE RECORD can order them.
    g = G.Gamma(snaps._atoms())
    # **THE ALPHABET MUST OPPOSE THE RECORD, OR THIS DEMONSTRATES NOTHING.** With `track`
    # dropped the key falls through fit and length to NAME, so picking the good term to be
    # alphabetically first makes assertion 1 pass with the record slot DELETED. The control
    # at the bottom caught exactly that on the first draft of this test.
    names = sorted(a.name for a in g.atoms)
    good, bad, untried = names[-1], names[0], names[len(names) // 2]

    for _ in range(3):                      # settled three times, never refused
        g.settle(good, where="g:L0")
    g.settle(bad, where="g:L0")             # settled once...
    for _ in range(2):                      # ...then broke the promise twice
        g.standing[bad].refute(g.tick, g.halflife, where="g:L0")

    gap = {"varies": (), "arity": 1, "target_type": "val",
           "varies_types": (), "rel_types": ()}
    order = retrieval.retrieve(g.library, gap, track=g.track_of)

    # 1 -- THE BETTER RECORD IS SURFACED FIRST, at equal fit and equal length.
    assert order.index(good) < order.index(bad), (
        f"a term settled 3 times with no refusal ranked BELOW one refused twice: "
        f"{good} at {order.index(good)}, {bad} at {order.index(bad)}")

    # 2 -- AND A POOR RECORD IS DEMOTED BELOW NO RECORD AT ALL, which is the Laplace
    # mean's point: untried reads 0.5, neither favoured nor penalised.
    assert order.index(untried) < order.index(bad), (
        "a term with a bad record did not rank below an untried one -- the prior is "
        "not sitting between them")
    assert order.index(good) < order.index(untried), (
        "a proven term did not outrank an untried one")

    # 3 -- NOTHING IS EXCLUDED. The worst record in the library is tried LAST, never
    # not at all.
    assert len(order) == len(g.library) and set(order) == set(g.library), (
        f"retrieve dropped or added names: {len(order)} back from {len(g.library)}")

    # 4 -- **FIT STILL DOMINATES RECORD.** A differently-typed atom loses the two type
    # points, and no track record may buy them back -- otherwise this is the hidden
    # discount Isaiah ruled out rather than an ordering.
    # THE SAME TRAP: the well-fitting term is chosen to sort AFTER `misfit` by name, so a
    # pass here cannot be the alphabet either.
    fitter = next(n for n in names if n > "misfit")
    g2 = G.Gamma(snaps._atoms() + [G.Atom("misfit", lambda v, _c: v, "OBJECT", "COLOUR")])
    for _ in range(9):                      # an excellent record on the wrong-typed term
        g2.settle("misfit", where="g:L0")
    order2 = retrieval.retrieve(g2.library, gap, track=g2.track_of)
    assert order2.index(fitter) < order2.index("misfit"), (
        "a WORSE-FITTING term with a great record outranked a better-fitting one -- "
        "track record is overruling fit instead of breaking ties within it")

    # MUTATION CONTROL -- drop the record slot and assertion 1 must fail. Without this the
    # test passes for any ordering that happens to put `good` first, and a guard whose
    # failure path is never exercised cannot be told from one that cannot fail.
    blind = retrieval.retrieve(g.library, gap)
    assert blind.index(good) > blind.index(bad), (
        "THE CONTROL DID NOT FIRE: with `track` dropped the order is still record-ordered, "
        "so assertion 1 was not demonstrating the record slot at all")


def test_disuse_never_moves_confidence():
    """**ISAIAH, via `LIBRARY_RETRIEVAL` 5.10.8: *decay may never touch belief.*** The table
    is explicit -- CONFIDENCE "never moves when NOT USED. **Disuse is not evidence.**"

    This failed for two hours on 2026-10-01. `confirmations` was added to `decay()` beside
    the three failure counters, on the reasoning that success and failure should share a
    clock. **They must not**: decaying a refusal is FORGIVENESS and has a standing rationale;
    decaying a confirmation is AMNESIA and has none. Measured before the removal, a term
    confirmed once and then merely left alone went 0.667 -> 0.501 -- back to the untried
    prior, by doing nothing.

    Four assertions and a mutation control.
    """
    import gamma as G
    import snaps

    def fresh():
        g = G.Gamma(snaps._atoms())
        return g, [a.name for a in g.atoms][0]

    # 1 -- AN UNUSED CONFIRMED TERM HOLDS ITS CONFIDENCE.
    g, nm = fresh()
    g.settle(nm, where="g:L0")
    base = g.track_of(nm)
    g.tick = 64                                   # eight half-lives of doing nothing
    assert abs(g.track_of(nm) - base) < 1e-9, (
        f"confidence moved on DISUSE alone: {base} -> {g.track_of(nm)}. Isaiah: decay may "
        f"never touch belief")

    # 2 -- AND FORGIVENESS STILL WORKS, WHICH IS WHY THE FAILURE SIDE KEEPS ITS DECAY.
    # A term confirmed once and refused once reads 0.5; as the refusal fades it must RISE
    # toward (1+1)/(1+0+2) = 0.667. Asserted, because it is the reason for the asymmetry.
    g, nm = fresh()
    g.settle(nm, where="g:L0")
    g.standing[nm].refute(g.tick, g.halflife)
    early = g.track_of(nm)
    g.tick = 64
    assert g.track_of(nm) > early, (
        f"a refusal stopped fading, so forgiveness is gone: {early} -> {g.track_of(nm)}")

    # 3 -- THE UNTRIED PRIOR IS UNTOUCHED.
    g, nm = fresh()
    assert g.track_of(nm) == 0.5, f"an untried term no longer reads the prior: {g.track_of(nm)}"

    # 4 -- THE FAILURE SIDE DECAYS EXACTLY AS BEFORE. This change must not have touched it:
    # the 5.10.8 coupling with the routine filter is documented and not to be moved alone.
    g, nm = fresh()
    g.standing.setdefault(nm, G.Standing()).refute(0, g.halflife)
    r0 = g.standing[nm].rejections
    g.tick = int(G.REJECTION_HALFLIFE)
    g.track_of(nm)
    assert abs(g.standing[nm].rejections - r0 * 0.5) < 1e-9, (
        f"one half-life no longer halves a rejection: {r0} -> {g.standing[nm].rejections}")

    # MUTATION CONTROL -- reinstate the removed statement's effect and assertion 1 must fail.
    g, nm = fresh()
    g.settle(nm, where="g:L0")
    base = g.track_of(nm)
    g.standing[nm].confirmations *= 0.5 ** (64 / G.REJECTION_HALFLIFE)
    g.tick = 64
    assert abs(g.track_of(nm) - base) > 1e-6, (
        "THE CONTROL DID NOT FIRE: decaying `confirmations` by hand changed nothing, so "
        "assertion 1 was not testing that the decay is gone")


def test_a_downrated_member_is_restored_the_moment_it_moves():
    """**REVERSIBILITY, AND ONE CONTRARY OBSERVATION IS DECISIVE** -- constraint 3 of the
    downrating plan, the reviewer 2026-10-01.

    Downrating rests on *watched through every action and never once moved*. **The moment it
    moves, the evidence for that is GONE -- not weakened, gone** -- so the restore is
    immediate and unconditional rather than earned back over time. A discount that outlived
    its evidence would be the hard ban 18.2 forbids, arriving by inertia instead of by rule.

    Exercises the REAL `_scope_weights` on a real agent, with the interface's own two inputs
    driven directly: `present` (how many presses a slot was seen for) and the delta table
    (which slots were ever observed to move). Those are the only two things the policy reads.
    """
    import os

    import test_m2
    import tether

    if not tether._DOWNRATE:
        # THE ARM IS DEFAULT-OFF, so drive the policy explicitly rather than skipping -- a
        # check that abstains because a flag is off is the vacuous pass this repo keeps
        # finding, and it would hide the whole mechanism behind a default.
        tether._DOWNRATE = True
    try:
        ag = test_m2._agent()
        state = ag.env.observe()
        slot = next((s for s in sorted(ag.slots)
                     if [p for p in (ag._peer_cache or {}).get(s, ()) if p in state]), None)
        if slot is None:                      # populate the peer cache the way `_group` does
            for s in sorted(ag.slots):
                ag._group(s, state)
            slot = next(s for s in sorted(ag.slots)
                        if [p for p in (ag._peer_cache or {}).get(s, ()) if p in state])
        peers = [p for p in ag._peer_cache.get(slot, ()) if p in state]
        victim = peers[0]
        floor = len(tuple(ag.env.actions()))

        # 1 -- MAKE IT INERT: seen often enough, never in the delta table.
        ag.iface.present[victim] = floor + 1
        for e in ag.iface.table.values():
            for k in [k for k in e.get("delta", {}) if k[1] == victim]:
                e["delta"].pop(k, None)
        ag._downrated.pop(slot, None)
        before = len(ag.led.rows())
        ws = ag._scope_weights(slot, state)
        assert ws is not None and ws[peers.index(victim)] == 0.0, (
            f"a member seen {floor + 1} times and never moved was not discounted: {ws}")
        down = [r for r in ag.led.rows()[before:] if r.get("event") == "member_downrated"]
        assert len(down) == 1, f"expected ONE downrating row on the transition, got {len(down)}"

        # 2 -- AND IT IS NOT RE-NARRATED WHILE IT STAYS DOWN. Per transition, not per call.
        mid = len(ag.led.rows())
        ag._scope_weights(slot, state)
        assert not [r for r in ag.led.rows()[mid:] if r.get("event") == "member_downrated"], (
            "a second evaluation re-narrated a discount that had not changed -- that is the "
            "per-evaluation defect the reviewer caught, back again")

        # 3 -- NOW IT MOVES. ONE contrary observation, and the discount must lift AT ONCE.
        import interface as IFace  # layer 1 key needs the constant
        tbl = ag.iface.table.setdefault("__probe__", {"by_ctx": {}, "n": 1, "delta": {}})
        tbl["delta"][("__ctx__", victim, IFace.NO_TARGET)] = (1, 1.0)   # layer 1 key
        mark = len(ag.led.rows())
        ws2 = ag._scope_weights(slot, state)
        assert ws2 is None or ws2[peers.index(victim)] == 1.0, (
            f"the member moved and was still discounted: {ws2}. The evidence for inertness "
            f"is GONE, so the discount must be too")
        rest = [r for r in ag.led.rows()[mark:] if r.get("event") == "member_restored"]
        assert len(rest) == 1, (
            f"no `member_restored` row on the lift (got {len(rest)}). `speak` has carried "
            f"that sentence since 07125ff with nothing emitting it -- a discount nobody sees "
            f"lifted is as silent as one nobody sees applied")
        assert (rest[0].get("detail") or {}).get("in_scope_of") == slot, (
            "the restore row did not say WHICH scope it was restored in")
    finally:
        tether._DOWNRATE = os.environ.get("TETHER_DOWNRATE", "0") != "0"


def test_youth_breaks_ties_within_equal_confidence_and_never_overrules_evidence():
    """**THE YOUTH BONUS, AND ITS PLACEMENT IS THE WHOLE OF THE CARE HERE.**

    Sec 5.10.8 writes `relevance = confidence x 0.5**(games/H) + youth`. With no games
    counter the decay term is 1 and that sum FALLS MONOTONICALLY with experience --
    untried 1.500 against proven-ten-times 1.008 -- so the additive form would put an
    untried term above a proven one, always. **The decay term is load-bearing and is the
    half that cannot be built.** Youth therefore sits in its OWN SLOT after confidence,
    where it can never compare terms of different confidence.

    Assertion 2 is the one that would have caught the additive form, so it is not a
    formality.
    """
    import gamma as G
    import retrieval
    import snaps

    g = G.Gamma(snaps._atoms())
    names = sorted(a.name for a in g.atoms)
    gap = {"varies": (), "arity": 1, "target_type": "val",
           "varies_types": (), "rel_types": ()}

    # **THE ALPHABET MUST OPPOSE THE EXPECTED ORDER.** Below youth the key falls to
    # (len, name), and every snaps atom has len 1 -- so if the term youth should favour
    # were alphabetically first, this would pass with the slot DELETED. That is exactly
    # how the first surfacing test came out vacuous.
    young, tried = names[-1], names[0]        # young sorts LAST by name
    g.settle(tried, where="g:L0")
    g.standing[tried].refute(g.tick, g.halflife, where="g:L0")

    # 1 -- EQUAL FIT, EQUAL CONFIDENCE, DIFFERENT TRIAL COUNTS -> LESS-TRIED FIRST.
    # The Laplace mean collapses these two states: confidence(0,0) == confidence(1,1).
    assert abs(g.track_of(young) - g.track_of(tried)) < 1e-9, (
        f"the premise is gone: confidences differ ({g.track_of(young)} vs "
        f"{g.track_of(tried)}), so this case no longer tests YOUTH")
    assert g.youth_of(young) > g.youth_of(tried), "the untried term is not the younger"
    order = retrieval.retrieve(g.library, gap, track=g.track_of, youth=g.youth_of)
    assert order.index(young) < order.index(tried), (
        f"at equal fit and EQUAL CONFIDENCE the less-tried term did not sort first: "
        f"{young} at {order.index(young)}, {tried} at {order.index(tried)}")

    # 2 -- **AND YOUTH NEVER OVERRULES EVIDENCE.** This is the assertion that would have
    # caught the spec's additive form: there, untried 1.500 beats proven 1.008.
    h = G.Gamma(snaps._atoms())
    hn = sorted(a.name for a in h.atoms)
    proven, fresh = hn[0], hn[-1]             # proven sorts FIRST by name: no help from it
    for _ in range(10):
        h.settle(proven, where="g:L0")
    assert h.track_of(proven) > h.track_of(fresh), "the proven term is not better-recorded"
    assert h.youth_of(fresh) > h.youth_of(proven), "the fresh term is not the younger"
    order2 = retrieval.retrieve(h.library, gap, track=h.track_of, youth=h.youth_of)
    assert order2.index(proven) < order2.index(fresh), (
        f"A YOUNGER TERM OUTRANKED A BETTER-RECORDED ONE -- youth is overruling evidence, "
        f"which is the additive form's defect: {proven} at {order2.index(proven)}, "
        f"{fresh} at {order2.index(fresh)}")

    # 3 -- NOTHING IS EXCLUDED.
    assert len(order) == len(g.library) and set(order) == set(g.library), (
        f"retrieve dropped or added names: {len(order)} back from {len(g.library)}")

    # 4 -- FIT STILL DOMINATES BOTH. A wrong-typed atom with a perfect record and maximal
    # youth must still lose to a well-fitting one.
    k = G.Gamma(snaps._atoms() + [G.Atom("misfit", lambda v, _c: v, "OBJECT", "COLOUR")])
    fitter = next(n for n in sorted(a.name for a in k.atoms) if n > "misfit")
    order3 = retrieval.retrieve(k.library, gap, track=k.track_of, youth=k.youth_of)
    assert order3.index(fitter) < order3.index("misfit"), (
        "a worse-FITTING term outranked a better-fitting one -- fit is no longer dominant")

    # MUTATION CONTROL -- drop the youth slot and assertion 1 must fail.
    blind = retrieval.retrieve(g.library, gap, track=g.track_of)
    assert blind.index(young) > blind.index(tried), (
        "THE CONTROL DID NOT FIRE: without the youth slot the order is still youth-ordered, "
        "so assertion 1 was not demonstrating youth at all")


def test_a_relational_slot_never_uses_tier_2_and_says_nothing_instead():
    """**A RELATION READ IN ANOTHER CONTEXT IS A READING OF A DIFFERENT BOARD.**

    `INDEX:51470`: across contexts, proximity falls 95.8% -> 60.4% while row and col
    hold 100%, and ALL 63 tier-2 misses are proximity. For a coordinate *the same
    before-value in another context* IS the same situation; for a relation it is not,
    because closeness depends on what else is on the board.

    **THE KIND COMES FROM THE WORLD.** `env.relational_slots()`, declared by the habitat
    exactly as `slot_owner` is. The older `interface.RELATIONAL` name tuple holds only
    `proximity`, and measured on seed 11 `distance` carries 86 of the 124 cross-context
    relational predictions -- so a guard reading the tuple would miss most of them. That
    is why this reads a declaration and the test uses `distance`.
    """
    import interface as IFace

    class _World:
        def __init__(self, declared):
            self._d = declared
        def relational_slots(self):
            return self._d

    def _iface(slot):
        f = IFace.Interface()
        # TIER 1 IS DEAF HERE AND TIER 2 WOULD ANSWER: the cell is recorded under
        # ANOTHER context, which is exactly the situation the guard is about.
        f.table["ACTION1"] = {"by_ctx": {}, "n": 1,
                              "lands": {(("other",), slot, 3): {7}}}
        return f

    slot, now, want = "o1.distance", 3, 7
    here = ("here_ctx",)                      # NOT the context the cell was seen in
    intent = IFace.Intent(IFace.BECOME, subject=slot, value=want)
    state = {slot: now}

    # 1 -- A WORLD THAT DECLARES NOTHING: tier 2 answers, as it always has.
    plain = _iface(slot).realise(intent, ("ACTION1",), here, state, _World(()))
    assert plain is not None and "in every context seen" in (plain.why or ""), (
        f"the premise is gone -- tier 2 did not fire for an undeclared world: {plain}")

    # 2 -- THE SAME CALL, WITH THE WORLD DECLARING THE SLOT RELATIONAL: NO PREDICTION.
    guarded = _iface(slot).realise(intent, ("ACTION1",), here, state,
                                   _World(("proximity", "distance")))
    assert guarded is None, (
        f"a RELATIONAL slot fell through to tier 2 and claimed {guarded.why!r}. A relation "
        f"read in another context is a reading of a different board")

    # 3 -- A POSITIONAL SLOT KEEPS TIER 2. row and col are 100% across contexts.
    pos = "o1.row"
    kept = _iface(pos).realise(IFace.Intent(IFace.BECOME, subject=pos, value=want),
                               ("ACTION1",), here, {pos: now},
                               _World(("proximity", "distance")))
    assert kept is not None and "in every context seen" in (kept.why or ""), (
        "a POSITIONAL slot lost tier 2 -- the guard is too wide")

    # 4 -- AND TIER 1 IS UNTOUCHED FOR A RELATIONAL SLOT. The guard removes only the
    # cross-context path; proximity keeps its 95.8% exact-cell prediction.
    f = IFace.Interface()
    f.table["ACTION1"] = {"by_ctx": {}, "n": 1, "lands": {(here, slot, now): {want}}}
    exact = f.realise(intent, ("ACTION1",), here, state, _World(("distance",)))
    assert exact is not None and "here" in (exact.why or ""), (
        f"TIER 1 was lost for a relational slot: {exact}. The guard must remove the "
        f"cross-context path and nothing else")

    # MUTATION CONTROL -- empty the declaration and assertion 2 must fail. Without it
    # this passes on any `realise` that returns None for an unrelated reason.
    back = _iface(slot).realise(intent, ("ACTION1",), here, state, _World(()))
    assert back is not None, (
        "THE CONTROL DID NOT FIRE: with the declaration emptied the call still returned "
        "no prediction, so assertion 2 was not demonstrating the guard")

    # ---- THE DELTA BRANCH, WHICH IS THE ONE THE AGENT ACTUALLY TRAVELS ----------
    #
    # **EVERYTHING ABOVE EXERCISES `lands` -- *which action lands this slot on that EXACT
    # VALUE* -- AND NONE OF THE LIVE TRAFFIC GOES THROUGH IT.** `expected_move` returns a
    # per-press STEP, which comes from the `delta` branch: *which way does it move and by
    # how much*, pooling a mean over contexts.
    #
    # Guarding only `lands` left the board reading BYTE-IDENTICAL -- 56/38/30 cross-context
    # claims unchanged -- while a unit test built around `lands` passed in both directions.
    # **A test written against the site you chose cannot tell you the site was wrong**, so
    # the second branch gets its own case rather than being assumed to follow.
    #
    # The delta branch is reached by an intent with a SIGN and no value.
    def _dface(sl):
        import interface as IFace  # layer 1 key needs the constant
        f = IFace.Interface()
        # ANOTHER context, and the layer-1 `rel` coordinate on the key
        f.table["ACTION1"] = {"by_ctx": {}, "n": 1,
                              "delta": {(("other",), sl, IFace.NO_TARGET): (4, 8.0)}}
        return f

    sign = IFace.Intent(IFace.BECOME, subject=slot, object="+")

    d_plain = _dface(slot).realise(sign, ("ACTION1",), here, state, _World(()))
    assert d_plain is not None and "in every context seen" in (d_plain.why or ""), (
        f"the delta premise is gone -- tier 2 did not fire for an undeclared world: {d_plain}")

    d_guard = _dface(slot).realise(sign, ("ACTION1",), here, state,
                                   _World(("proximity", "distance")))
    assert d_guard is None, (
        f"a RELATIONAL slot pooled a cross-context MEAN DELTA and claimed {d_guard.why!r}. "
        f"This is the branch `expected_move` returns, so this is the one that matters")

    d_pos = _dface(pos).realise(IFace.Intent(IFace.BECOME, subject=pos, object="+"),
                                ("ACTION1",), here, {pos: now},
                                _World(("proximity", "distance")))
    assert d_pos is not None and "in every context seen" in (d_pos.why or ""), (
        "a POSITIONAL slot lost the delta branch's tier 2 -- the guard is too wide there")

    # ITS OWN MUTATION CONTROL.
    d_back = _dface(slot).realise(sign, ("ACTION1",), here, state, _World(()))
    assert d_back is not None, (
        "THE DELTA CONTROL DID NOT FIRE: with the declaration emptied the delta branch "
        "still returned nothing, so the delta assertion was not demonstrating the guard")


if __name__ == "__main__":
    if "--cover" in sys.argv:
        for label, c in (("kernel.Frame", coverage()),
                         ("tether.Agent", snap_coverage())):
            print(f"  -- {label} --")
            for k, v in c.most_common():
                print(f"  {v:>4}  {k}")
        raise SystemExit(0)
    import unittest

    # ONE SUBJECT PER INVOCATION. Folding both into a single seat would make a red
    # unreadable: tether's record has known gaps, so a shared seat would be permanently
    # red and a kernel regression would arrive as no change at all.
    case = TestShipped if "--tether" in sys.argv else TestLoop
    # EVERY MODULE-LEVEL `test_` IS CALLED FROM ONE OF THESE TWO ARMS, and that is now a
    # rule rather than a habit -- `test_the_daydream_precondition_can_refuse` and
    # `test_the_generated_habitat_is_not_built_to_pass` sat here UNCALLED (2026-09-26),
    # each appearing exactly once in the file: at its own `def`. Both PASS. So the seat
    # reported 16/16 with two property tests that had never executed, which is *a green
    # seat proves a thing WORKS and says nothing about whether it is REACHED* inside the
    # seat file itself. `Loop.TestCase` is a state machine and does not collect them.
    if case is TestLoop:
        test_generator_reaches_the_hard_cases()
        test_the_generated_habitat_is_not_built_to_pass()
        print("  generator coverage: ok · habitat not built to pass: ok")
    else:
        test_shipped_generator_reaches_the_hard_cases()
        test_the_residual_bound_loses_nothing()
        test_the_resolutions_offered_are_not_the_answer()
        test_the_atom_order_is_pinned()
        test_the_promotion_clause_is_recorded()
        test_the_mutation_observer_reaches_the_agent()
        test_a_mutation_moves_attention_and_never_the_action()
        test_the_admitting_clause_crosses_into_gamma()
        test_the_daydream_precondition_can_refuse()
        test_the_atom_set_builds_under_every_arm_state()
        test_a5_is_reproducible_without_a_world()
        test_the_keyed_reach_loses_nothing()
        test_the_inherited_vocabulary_is_not_the_held_library()
        test_the_quantifiers_quantify()
        test_the_seam_varies_what_it_explores_with()
        test_asking_the_interface_does_not_change_it()
        test_every_exit_has_a_phase()
        test_never_two_consecutive_resets()
        test_a_carried_term_can_reach_candidacy()
        test_a_candidate_survives_a_level_and_is_dormant_until_bound_here()
        test_a_rejection_records_where_it_was_taken()
        test_a_trial_miss_is_not_a_refusal()
        test_track_record_orders_within_a_fit_level()
        test_disuse_never_moves_confidence()
        test_a_downrated_member_is_restored_the_moment_it_moves()
        test_youth_breaks_ties_within_equal_confidence_and_never_overrules_evidence()
        test_a_relational_slot_never_uses_tier_2_and_says_nothing_instead()
        print("  A5 and B5 reproductions still fire (expected): ok")
        print("  keyed reach loses nothing: ok · two vocabularies stay two: ok")
        print("  the quantifiers quantify (ONE fires, all != some): ok")
        print("  the seam varies what it explores with: ok")
        print("  track record orders within a fit level (fit still dominates): ok")
        print("  disuse never moves confidence (forgiveness still rises): ok")
        print("  a downrated member is restored the moment it moves: ok")
        print("  youth breaks ties within equal confidence, never overrules evidence: ok")
        print("  a relational slot never uses tier 2 and says nothing instead: ok")
        print("  shipped generator coverage: ok · residual bound loses nothing: ok"
              " · resolutions are not the answer: ok · atom order pinned: ok"
              " · promotion clause recorded: ok · observer reaches the agent: ok"
              " · mutation moves attention only: ok · admitting clause crosses: ok"
              " · daydream precondition can refuse: ok")
    r = unittest.TextTestRunner(verbosity=0).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(case))
    # THE FINDING FIRST, on stdout. check.py reads the head of the output because every
    # other tool here prints what it found before it prints a summary; a runner prints a
    # banner first, so the seat reported `====` where the failing check should have been.
    for _t, tb in r.failures + r.errors:
        hit = next((ln for ln in reversed(tb.splitlines())
                    if "AssertionError" in ln or "Error:" in ln), "")
        if hit:
            print(f"  {hit.strip()[:300]}")
    raise SystemExit(0 if r.wasSuccessful() else 1)
