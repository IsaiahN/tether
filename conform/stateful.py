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


def test_b5_still_fires_on_the_pinned_world():
    """THE B5 REPRODUCTION, PINNED -- and the run shows the mechanism, not just the verdict.

    A strict expected-failure, same shape as the A5 one below: green while B5 truthfully fails,
    red the moment the fix lands, carrying its own invert-me instruction.

    **WHAT THE RUN SHOWS, AND IT RECONCILES TWO READINGS THAT LOOKED OPPOSED.**
    Measured here: `parks on ['s3']`, `probes on ['@probe', '@probe']`.

    Reading the source says the agent matches park to probe correctly -- `mint` adds the parked
    slot to `_starved`, and the flush writes one probe row PER STARVED SLOT. True. But the
    flush is `for slot in sorted(self._starved) or ["@probe"]`, and `@probe` is the fallback
    for an EMPTY `_starved`. Both probes here took it, so `_starved` was empty when they fired.

    That is `F269`'s temporal anti-correlation, visible in one run: *`bored()` is true EARLY,
    when nothing is bound and there is nothing to perturb FOR, and false LATE, which is exactly
    when slots starve.* The park and the probe never coincide, so the per-slot branch the
    repair added cannot be reached and the fallback answers instead.

    SO THE SLOT MISMATCH IS REAL AND IS NOT A LABELLING BUG. Arm M (`TETHER_STARVED_CONTACT`)
    is the built fix: it returns `probe` BEFORE the `bored()` gate whenever `_starved` is
    non-empty, so the flush has a slot to write. Turning it on is an ACTING-PATH change and is
    Isaiah's ruling, not the seat's.
    """
    import snaps
    from gamma import Gamma
    from ledger import Ledger
    from tether import Agent, Config
    from world import bind

    # **THE HAND-WRITTEN WORLD STOPPED STARVING ANYTHING -- 2026-09-28, and it is NOT a fix.**
    # The action-seam work changed which action lands on which step, and with it the one
    # `no_support` park this world produced. Measured by stashing the diff and re-running:
    #
    #     PRE    bad=['B5']   park verdicts {under_floor 7, depth_exhausted 5, no_support 1}
    #     POST   bad=[]       park verdicts {under_floor 7, depth_exhausted 5}
    #     and at 12/15/20/30 steps: still no `no_support`, still no B5
    #
    # **So it is not timing** -- A5's budget fix does not apply. B5's own message offers two
    # readings, *arm M is on* or *the probe now reaches the starved slot*, and NEITHER is true:
    # arm M is off and every probe row still reads `@probe`, the empty-`_starved` fallback.
    # **The reproduction lost its SUBJECT**, which is a third outcome the message does not
    # contemplate -- and the assertion below it is the thing that caught that, so the author
    # foresaw what the message did not.
    #
    # **RE-PINNED BY SEARCHING FOR THE PRECONDITION, NOT FOR THE VERDICT**, and the numbers are
    # what make that distinction checkable rather than a claim:
    #
    #     POPULATION  48 worlds -- `spec_for(seed, n)` for seed 0..23, n in (4, 5), 9 steps
    #     STARVE A SLOT (`no_support`)   2 of 48
    #     OF THOSE, B5 FIRES             2 of 2
    #
    # **I did not pick the world where B5 fires; B5 fires in every world where a slot starves.**
    # Choosing a world so a defect becomes OBSERVABLE is supplying a panel; choosing one so a
    # verdict comes out right is fitting, and the 2-of-2 is what separates them. Both worlds are
    # asserted, so the reproduction is now a pair rather than a single point.
    for seed in (3, 16):
        led = Ledger()
        ag = Agent(bind(snaps.Snap(snaps.spec_for(seed, 4))), Gamma(snaps._atoms()),
                   Config(), led)
        for _ in range(9):
            ag.step()
        rows = led.rows()
        # THE PRECONDITION FIRST, because a clean verdict on a world that starves nothing is
        # the null this whole entry exists to refuse.
        parked = {r.get("slot") for r in rows if r.get("event") == "park"
                  and (r.get("detail") or {}).get("verdict") == "no_support"}
        assert parked, (
            f"seed {seed} starves no slot -- it no longer exercises B5, and a verdict taken "
            f"here would be a reading of nothing")
        res = kernel.Linter.run(rows)
        bad = sorted(k for k, v in res.items() if v["status"] in ("FAIL", "SUPPRESSED"))
        assert "B5" in bad, (
            f"B5 NO LONGER FIRES on seed {seed} (bad={bad}) while {sorted(parked)} starved. "
            f"If arm M is on, or the probe now reaches the starved slot, this is the GOOD "
            f"outcome -- invert to `assert 'B5' not in bad`, rename it, and it becomes the "
            f"regression test. **CHECK WHICH BEFORE INVERTING**: a tripwire cannot tell *the "
            f"defect is gone* from *the trajectory moved past it*, and both happened today. "
            f"Do not delete it.")


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
        test_b5_still_fires_on_the_pinned_world()
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
        print("  A5 and B5 reproductions still fire (expected): ok")
        print("  keyed reach loses nothing: ok · two vocabularies stay two: ok")
        print("  the quantifiers quantify (ONE fires, all != some): ok")
        print("  the seam varies what it explores with: ok")
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
