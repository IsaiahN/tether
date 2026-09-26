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
    for seed in range(6):
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
        test_the_daydream_precondition_can_refuse()
        print("  shipped generator coverage: ok · residual bound loses nothing: ok"
              " · resolutions are not the answer: ok · atom order pinned: ok"
              " · promotion clause recorded: ok · daydream precondition can refuse: ok")
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
