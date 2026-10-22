"""The gate's checks, one defect each. Tests only what would silently break.

**THE COUNT IS NOT WRITTEN DOWN HERE ON PURPOSE -- `F416`.** It said EIGHT while the file
held twenty and the runner ran seventeen, and a number in prose is a number nobody
re-derives. The runner prints `run (defined)` and REFUSES when they differ.

Stage 0's done-when: a valid ledger passes, and a ledger with each defect fails naming
that check's fixed token.
"""

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gate

sys.dont_write_bytecode = True


def valid() -> list[dict]:
    m = "specified"
    return [
        {"mode": m, "seq": 0, "cycle": 0, "step": "PERCEIVE", "slot": "s", "event": "bet",
         "detail": {"mass": 1.0}},
        {"mode": m, "seq": 1, "cycle": 0, "step": "ROUTE", "slot": "s", "event": "route",
         "detail": {"bin": "mechanism", "why_not": "not rebinding: nothing fits"}},
        {"mode": m, "seq": 2, "cycle": 0, "step": "MINT", "slot": "s", "event": "mint",
         "detail": {"guards": {"support": True, "reachability": True, "novelty": True},
                    "term": "a . b", "budget_exhausted": False,
                    "cuts": [{"name": "x", "rank": 1, "reversible": True}]}},
        {"mode": m, "seq": 3, "cycle": 0, "step": "ACCEPT", "slot": "s", "event": "accept",
         "detail": {"term": "a . b", "status": "candidate"}},
        {"mode": m, "seq": 4, "cycle": 1, "step": "SETTLE", "slot": "s", "event": "settle",
         "detail": {"term": "a . b", "status": "accepted"}},
    ]


def _refuses(rows, token):
    out = gate.check(rows)
    assert out["verdict"] == gate.REFUSE, f"expected refusal for {token}, got {out}"
    assert out["token"] == token, f"expected {token}, got {out['token']} ({out['note']})"


def test_valid_passes():
    assert gate.check(valid())["verdict"] == gate.PASS


def test_no_mode():
    r = valid()
    del r[0]["mode"]
    _refuses(r, gate.NO_MODE)


def test_no_step():
    r = valid()
    r[1]["step"] = "THINKING"
    _refuses(r, gate.NO_STEP)


def test_step_order():
    r = valid()
    r[1]["step"], r[0]["step"] = "PERCEIVE", "ROUTE"
    _refuses(r, gate.STEP_ORDER)


def test_missing_input():
    r = [x for x in valid() if x["event"] != "bet"]
    _refuses(r, gate.MISSING_INPUT)


def _surprised(slot="s", declared=("s",)):
    """valid() with its bet replaced by a relational surprise on `slot` and an "@derived" row
    declaring `declared` (B2b: a declared-derived slot's input is its surprise, never a bet)."""
    m = "specified"
    r = [x for x in valid() if x["event"] != "bet"]
    return [{"mode": m, "seq": -2, "cycle": 0, "step": "PERCEIVE", "slot": slot,
             "event": "relational_surprise", "detail": {"derived": 0, "actual": 1, "mass": 1.0}},
            {"mode": m, "seq": -1, "cycle": 0, "step": "PERCEIVE", "slot": "@derived",
             "event": "derived", "detail": {"declared_add": list(declared), "declared_drop": []}},
            *r]


def test_a_declared_slots_relational_surprise_is_its_input():
    assert gate.check(_surprised())["verdict"] == gate.PASS


def test_a_declared_slots_route_without_its_surprise_refuses():
    r = [x for x in _surprised() if x["event"] != "relational_surprise"]
    _refuses(r, gate.MISSING_INPUT)


def test_a_surprise_on_an_undeclared_slot_is_no_input():
    _refuses(_surprised(declared=("s.add_n",)), gate.MISSING_INPUT)


def _asked(slot="s", declared=("s",), ask=True):
    """E0-W's want-only mint (the reviewer 2026-10-18 12:34): an "@derived" row declaring
    `declared`, a derived_asked row on `slot` (unless ask is False), then the mint's park on "s"."""
    m = "specified"
    return [{"mode": m, "seq": 0, "cycle": 0, "step": "PERCEIVE", "slot": "@derived",
             "event": "derived", "detail": {"declared_add": list(declared), "declared_drop": []}},
            *([{"mode": m, "seq": 1, "cycle": 0, "step": "MINT", "slot": slot,
                "event": "derived_asked", "detail": {}}] if ask else []),
            {"mode": m, "seq": 2, "cycle": 0, "step": "MINT", "slot": "s", "event": "park",
             "detail": {"verdict": "under_floor",
                        "guards": {"support": True, "reachability": True, "novelty": True}}}]


def test_a_declared_slots_derived_ask_is_its_want_only_input():
    assert gate.check(_asked())["verdict"] == gate.PASS


def test_mf_g1_a_declared_slots_park_with_no_bet_and_no_ask_refuses():
    _refuses(_asked(ask=False), gate.MISSING_INPUT)


def test_mf_g2_an_ask_on_an_undeclared_slot_is_no_input():
    _refuses(_asked(declared=("s.add_n",)), gate.MISSING_INPUT)


def _reused(term, cycle=0, slot="s", seq=2):
    return {"mode": "specified", "seq": seq, "cycle": cycle, "step": "ROUTE", "slot": slot,
            "event": "reuse_install", "detail": {"term": term}}


def test_a_reuse_install_is_the_terms_acceptance():
    """P1: a reused term enters Gamma by a ROUTE reuse_install row, and may then settle."""
    r = [x for x in valid() if x["event"] not in ("mint", "accept")]
    r.insert(2, _reused("a . b"))
    assert gate.check(r)["verdict"] == gate.PASS, gate.check(r)


def test_a_reuse_install_of_another_term_is_not_an_acceptance():
    r = [x for x in valid() if x["event"] not in ("mint", "accept")]
    r.insert(2, _reused("c . d"))
    _refuses(r, gate.MISSING_INPUT)


def test_a_reuse_install_after_the_settle_is_not_an_acceptance():
    r = [x for x in valid() if x["event"] not in ("mint", "accept")]
    r.append(_reused("a . b", cycle=1, slot="t", seq=5))
    _refuses(r, gate.MISSING_INPUT)


def test_a_candidates_refuted_bet_is_a_row_the_gate_accepts():
    """P3: a candidate the ground refuted before it ever settled is recorded, as a SETTLE row."""
    r = valid()
    r[4] = {"mode": "specified", "seq": 4, "cycle": 1, "step": "SETTLE", "slot": "s",
            "event": "miss_while_candidate",
            "detail": {"term": "a . b", "status": "candidate", "ground_said": False}}
    assert gate.check(r)["verdict"] == gate.PASS, gate.check(r)


def test_unrouted():
    r = [x for x in valid() if x["event"] != "route"]
    _refuses(r, gate.UNROUTED)


def test_no_discriminator():
    r = valid()
    r[1]["detail"]["why_not"] = ""
    _refuses(r, gate.NO_DISCRIMINATOR)


def test_guard_unrecorded():
    r = valid()
    del r[2]["detail"]["guards"]["reachability"]
    _refuses(r, gate.GUARD_UNRECORDED)


def test_unsettled_accept():
    r = [x for x in valid() if x["event"] != "settle"]
    r[-1]["detail"]["status"] = "accepted"
    _refuses(r, gate.UNSETTLED_ACCEPT)


def test_settled_elsewhere_is_not_settled_here():
    """The ground settles a term FOR A SLOT, so a settlement on one licenses nothing on
    another. Keyed on the term alone, one settlement anywhere licenses acceptance
    everywhere -- which is how a term the ground refused goes on being accepted.

    The settle row in `valid()` IS the accepted row, so moving its slot moves both sides
    of the comparison and witnesses nothing. A SECOND slot is what the case needs."""
    r = valid()
    r.append({"mode": "specified", "seq": 5, "cycle": 1, "step": "PROMOTE", "slot": "s2",
              "event": "cite", "detail": {"term": "a . b", "status": "accepted"}})
    _refuses(r, gate.UNSETTLED_ACCEPT)


def test_filter_verdict():
    r = valid()
    r[2]["detail"].update(budget_exhausted=True, verdict="unreachable")
    _refuses(r, gate.FILTER_VERDICT)


def test_irreversible_cut():
    r = valid()
    r[2]["detail"]["cuts"] = [{"name": "x", "rank": 1, "reversible": False}]
    _refuses(r, gate.IRREVERSIBLE_CUT)


def test_unreached_unmeasured():
    """A park with no coverage is `unreachable` smuggled in wearing `unreached`'s word."""
    r = valid()
    r[2]["detail"].update(verdict="depth_exhausted", units=8, depth=2)
    r[2]["detail"].pop("coverage", None)
    _refuses(r, gate.UNREACHED_UNMEASURED)


def test_contract_refuses_a_partial_adapter():
    """BOTH EDGES of the contract's width. An adapter missing a member must be refused
    by name, and a complete one accepted -- so the member set cannot silently shrink
    (the partial is accepted) or grow (the complete one is refused)."""
    from world import REQUIRED, Transitions, bind
    complete = Transitions()
    for member in REQUIRED:
        class Partial:
            pass
        for m in REQUIRED:
            if m != member:
                setattr(Partial, m, getattr(type(complete), m))
        try:
            bind(Partial())
        except TypeError as exc:
            assert member in str(exc), f"refused without naming {member}: {exc}"
        else:
            raise AssertionError(f"bind accepted an adapter with no {member}()")


def test_contract_accepts_a_complete_adapter():
    from world import Transitions, bind
    bind(Transitions())          # must not raise


def test_contract_declares_actions_and_alphabet():
    """The two members the loop was reaching past the contract to get."""
    from world import REQUIRED
    assert "actions" in REQUIRED and "alphabet" in REQUIRED


def _idn(v, _ctx):
    return v


def test_minted_separates_an_operand_bound_atom_from_a_real_mint():
    """`F412`: an atom carrying an operand binding is not an adoption, and the old
    name comparison counted nine of them into `F410`'s unguarded column.

    Both halves asserted, because a classifier that answers one correctly and the
    other by accident reads identical. PLANTED, not harvested from a run -- a run
    cannot be made to contain the negative case on demand.

    AND PLANTED THROUGH `accept()`, NOT BY WRITING `library` DIRECTLY. The first
    version assigned into `gamma.library` and the `lint` seat refused it: accept()
    must stay its only writer or a stored reach is indistinguishable from the
    library. The seat was right and the test is the better for obeying it.
    """
    import gamma as G
    from instruments import Attribution
    take, inc = G.Atom("take", _idn, "val", "val"), G.Atom("inc", _idn, "val", "val")
    gam = G.Gamma([take, inc], game="t")
    for i, t in enumerate((G.Term(atoms=(take,), operand="o0.col"),
                           G.Term(atoms=(inc,), guard=G.ACTED_SELF),
                           G.Term(atoms=(take, inc)))):
        gam.accept(t, seq=i, residual="s@0")
    m = Attribution.minted(gam)
    assert "take<o0.col>" in m["operand_bound"], "an operand-bound atom must not be a mint"
    assert "take<o0.col>" not in m["minted"]
    assert "inc?ACTED_SELF" in m["minted"], "a guarded single-atom term IS a mint"
    assert "take . inc" in m["minted"]
    # the old reading is kept beside the new one, and here they must disagree
    assert m["n_minted"] == 2 and m["n_by_name"] == 3




def test_a_guarded_term_arrives_with_its_guard_and_a_duplicate_still_dedups():
    """`F420`: `save` wrote atom NAMES only, so `inc?ACTED_SELF` was saved as `["inc"]`,
    arrived as the bare prior atom, and was discarded as a duplicate -- a LOSS reported
    as `already_held`. Measured: `click_only` seed 6 carried 2 terms and arrived with 0.

    BOTH DIRECTIONS, because every guard hole found this week was found on the ACCEPT
    path and none by a refusal test. A carry that refuses everything would pass a
    loss-only assertion, and a carry that accepts everything would pass a dedup-only
    one. The reviewer required both (2026-10-03).

    THE DEFECT IS REINTRODUCED BY DELETING THE `guard=` ARGUMENT IN `load`, not by
    disabling this check.

    OFF IDENTITY: the operand-only LOSS asserted under the default load (hold_unbound False)
    is the pre-flip behavior, retired when CARRY is flipped. It pins OFF; it does not endorse
    the loss. The ON twin (hold_unbound=True, what wire passes under the carry) asserts the
    HOLD (the reviewer 2026-10-15 01:51).
    """
    import pathlib
    import tempfile

    import gamma as G
    take, inc = G.Atom("take", _idn, "val", "val"), G.Atom("inc", _idn, "val", "val")
    src_g = G.Gamma([take, inc], game="A")
    for i, t in enumerate((G.Term(atoms=(inc,), guard=G.ACTED_SELF),
                           G.Term(atoms=(take,), operand="o1.colour"),
                           G.Term(atoms=(take, inc)))):
        src_g.accept(t, seq=i, residual="s@0")
        src_g.handles.setdefault(t.name, t.handle(src_g.game))
    with tempfile.TemporaryDirectory() as d:
        path = str(pathlib.Path(d) / "lib.json")
        src_g.save(path)
        # PROVENANCE CROSSES: every accepted term is written with its clause and residual.
        import json
        rows = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))["terms"]
        minted = [r for r in rows if r["origin"] != G.PRIOR]
        assert minted and all(r["admitted"] == G.ACCEPTED and r["residual"] == "s@0"
                              for r in minted), [(r["admitted"], r["residual"]) for r in minted]
        dst = G.Gamma([take, inc], game="B")
        rep = dst.load(path)
        # ACCEPT: the guarded term crosses, as itself, with its birth game recorded.
        assert "inc?ACTED_SELF" in dst.library, "a guarded term must ARRIVE with its guard"
        assert dst.carried["inc?ACTED_SELF"]["from"] == "A"
        # OFF IDENTITY (the pre-flip behavior, retired when CARRY is flipped): the operand-only
        # term still collapses, and SAYS SO rather than reporting the benign-sounding
        # `already_held`.
        assert rep["destroyed_on_carry"] == 1, rep
        assert rep["destroyed"][0]["collapsed_to"] == "take"
        assert rep["destroyed"][0]["lost"] == "o1.colour"
        # DEDUP: loading the same file again is a real duplicate, not a loss.
        again = dst.load(path)
        assert again["loaded"] == 0 and again["deduped_onto_composition"] == 2, again
        assert again["destroyed_on_carry"] == 1, "the collapse is not a dedup"
        # ON (hold_unbound=True, what wire passes under TETHER_LINEAGE_CARRY): HELD unbound
        on = G.Gamma([take, inc], game="B")
        rep = on.load(path, hold_unbound=True)
        assert rep["destroyed_on_carry"] == 0 and "take<?.colour>" in on.library, rep
        assert on.carried["take<?.colour>"]["unbound"] == "o1.colour", on.carried
        again = on.load(path, hold_unbound=True)
        assert again["deduped_onto_composition"] == 3 and again["destroyed_on_carry"] == 0, again


def _flip_child():
    """Run in a subprocess with TETHER_LINEAGE_CARRY=1 (test_wire_under_the_carry): (a) library=
    with a lineage folder is refused before anything is touched; (b) library= alone holds an
    operand-only row unbound through wire, which passes the arm to gamma.load."""
    import pathlib
    import tempfile

    import arc_holdout
    import gamma as G
    import lineage
    from test_entry import FakeWrapper
    assert lineage._CARRY, "the child must be started with TETHER_LINEAGE_CARRY=1"
    with tempfile.TemporaryDirectory() as d:
        a0 = arc_holdout.wire(FakeWrapper(), "fake")[1].gamma.atoms[0]
        src = G.Gamma([a0], game="A")
        src.accept(G.Term(atoms=(a0,), operand="o1.colour"), seq=0, residual="s@0")
        path = str(pathlib.Path(d) / "lib.json")
        src.save(path)
        lin = str(pathlib.Path(d) / "lin")
        try:
            arc_holdout.wire(FakeWrapper(), "fake", library=path, lineage_dir=lin)
            raise AssertionError("FLIP (a): library= with a lineage folder was not refused")
        except ValueError as e:
            assert path in str(e) and lin in str(e), ("FLIP (a): the refusal names both", e)
        ag, loaded = (lambda r: (r[1], r[5]))(arc_holdout.wire(FakeWrapper(), "fake",
                                                                 library=path))
        name = f"{a0.name}<?.colour>"
        assert loaded["destroyed_on_carry"] == 0 and name in ag.gamma.library, (
            "FLIP (b): the row was not held unbound through wire", loaded)
        assert ag.gamma.carried[name]["unbound"] == "o1.colour", ag.gamma.carried[name]
    print("flip child: OK")


def test_wire_under_the_carry():
    """The flip-commit list (the reviewer 2026-10-15 01:56): in ONE subprocess with the arm in its
    environment, never a patched arm, (a) wire refuses library= with a lineage folder, and (b) wire
    holds an operand-only library= row unbound."""
    import os
    import pathlib
    import subprocess
    here = pathlib.Path(__file__).parent
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(TETHER_LINEAGE_CARRY="1", PYTHONHASHSEED="0")
    r = subprocess.run([sys.executable, "-B", "-c", "import test_gate; test_gate._flip_child()"],
                       cwd=str(here), env=env, stdin=subprocess.DEVNULL, capture_output=True,
                       text=True)
    assert r.returncode == 0 and "flip child: OK" in r.stdout, r.stderr[-2000:]


def test_a_chain_that_loses_its_operand_is_not_reported_as_a_clean_arrival():
    """An operand names a slot of THIS board, so it does not re-bind -- but a term that
    arrives without it is not the term that left. Counted among `loaded` with nothing
    said, that is `already_held`'s silence one step milder.

    THE FIELD CAN FIRE, which is why this test exists separately: only a term with BOTH
    a chain of 2+ and an operand can arrive AND be unbound, so a single-atom case would
    have left `crossed_without_binding` structurally zero and untestable.
    """
    import pathlib
    import tempfile

    import gamma as G
    take, inc = G.Atom("take", _idn, "val", "val"), G.Atom("inc", _idn, "val", "val")
    src_g = G.Gamma([take, inc], game="A")
    t = G.Term(atoms=(take, inc), operand="o1.colour")
    src_g.accept(t, seq=0, residual="s@0")
    with tempfile.TemporaryDirectory() as d:
        path = str(pathlib.Path(d) / "lib.json")
        src_g.save(path)
        dst = G.Gamma([take, inc], game="B")
        rep = dst.load(path)
        assert rep["loaded"] == 1 and rep["crossed_without_binding"] == 1, rep
        assert "take . inc" in dst.library and "take . inc<o1.colour>" not in dst.library


def test_a_merge_keeps_the_birth_handle_of_every_instance_it_absorbed():
    """`F420.1`: fourteen `same . all<...>` compositions on default seed 6 all reduce to
    the atom chain ("same","all"), so one installs and thirteen vanish. That may be RIGHT
    for transfer -- one law, many instances -- but Isaiah's condition is that we can prove
    where everything in the library came from, and a merge that forgets its members fails
    it (the reviewer, 2026-10-03).

    THE DEFECT IS REINTRODUCED by dropping the `self.merged.setdefault(...)` line in
    `load`, not by disabling this check. Four terms in, one survivor, THREE recorded.
    """
    import pathlib
    import tempfile

    import gamma as G
    take, inc = G.Atom("take", _idn, "val", "val"), G.Atom("inc", _idn, "val", "val")
    src_g = G.Gamma([take, inc], game="A")
    for i, slot in enumerate(("o1.colour", "o2.row", "o3.distance", "o4.proximity")):
        t = G.Term(atoms=(take, inc), operand=slot)
        src_g.accept(t, seq=i, residual="s@0")
        src_g.handles.setdefault(t.name, t.handle(src_g.game))
    with tempfile.TemporaryDirectory() as d:
        path = str(pathlib.Path(d) / "lib.json")
        src_g.save(path)
        dst = G.Gamma([take, inc], game="B")
        rep = dst.load(path)
        assert rep["loaded"] == 1, rep
        assert rep["merged_into"] == {"take . inc": 3}, rep
        absorbed = dst.merged["take . inc"]
        # EVERY member is accounted for, with the operand that distinguished it.
        assert {m["operand"] for m in absorbed} == {"o2.row", "o3.distance", "o4.proximity"}
        assert all(m["handle"] and m["from"] == "A" for m in absorbed), absorbed
        # and the survivor itself is recorded as carried, so all FOUR are traceable
        assert dst.carried["take . inc"]["from"] == "A"


def test_agency_cannot_see_a_mode_switch_and_inverts_the_reading():
    """THE MODE-SWITCH FIXTURE. `THE_MISSION`: the only legitimate distinction is topical
    I/O -- avatar or click actuator -- *and even that BLENDS mid-game, so it must be
    detected CONTINGENTLY PER STEP, never used to label the game.*

    **THIS FIXTURE PINS A DEFECT, NOT THE DESIRED BEHAVIOUR, AND SAYS SO.** `Agency.moved`
    and `Agency.tried` are LIFETIME counters, and `contingent()` needs SOME action to have
    ALWAYS moved a slot and SOME OTHER to have NEVER moved it. A mid-game body swap makes
    both halves false at once, so the predicate collapses.

    AND IT DOES NOT MERELY GO BLIND -- IT INVERTS. A world that is still unambiguously
    AVATAR reads `actuator`, which is the claim that nothing responds to the agent directly
    and it is acting at a distance. The OPPOSITE diagnosis, stated confidently.

    `arc_world.py:736` records the same class for the tracker: *"mode switched at step 7"
    was indistinguishable from "the tracker lost the object"*.

    WHEN THE FIX LANDS, THIS TEST FLIPS: phase 2 must read `avatar` on `o0.row`. It is
    written to fail loudly at that moment rather than silently keep passing, which is why
    it asserts the fresh-reader control too -- that control proves the world IS readable
    and the accumulation is what loses it.

    NO FIX IS TAKEN HERE. Every repair needs a WINDOW, and this sensor's docstring claims
    its distinction: *"no rate, no cutoff and no window to tune"*. Choosing one is a design
    decision about that claim, not a bug fix, and it is the reviewer's.
    """
    from instruments import Agency
    slots = ["o0.row"]

    def phase(ag, mover, other, n):
        for _ in range(n):
            ag.note(mover, {"o0.row"}, slots)
            ag.note(other, set(), slots)

    a = Agency()
    phase(a, "up", "click", 10)
    assert a.mode() == "avatar" and a.contingent() == ["o0.row"], "phase 1 must read avatar"

    phase(a, "click", "up", 10)          # the body is swapped; the world is STILL avatar
    # THE DEFECT, pinned: the accumulated counters make neither action always-or-never.
    assert a.moved[("o0.row", "up")] == 10 and a.tried[("o0.row", "up")] == 20
    assert a.moved[("o0.row", "click")] == 10 and a.tried[("o0.row", "click")] == 20
    assert a.contingent() == [], "the predicate collapses -- if this fails, the fix landed"
    assert a.mode() == "actuator", "and it INVERTS to acting-at-a-distance, not to unread"

    # THE CONTROL that makes the above a defect rather than an unreadable world: a reader
    # over phase 2 ALONE gets it right, so the signal is there and accumulation loses it.
    b = Agency()
    phase(b, "click", "up", 10)
    assert b.mode() == "avatar" and b.contingent() == ["o0.row"]


def test_arm_state_is_read_from_the_module_not_the_environment():
    """`F424`: the agent ships with 14 of 18 declared capabilities OFF, so a measurement
    that does not say which were on describes a different agent than the architecture
    does. `Attribution.arms()` is that line.

    THE ASSERTION THAT MATTERS IS THE SECOND ONE. Every flag resolves ONCE at import, so
    reading `os.environ` would report the INTENTION and not the RUN -- and the two differ
    exactly when someone sets a variable after import, which is the case a provenance line
    exists to catch. Setting the variable here must change NOTHING.

    Reintroduce by making `arms()` read os.environ, not by disabling this.
    """
    import os

    import tether
    from instruments import Attribution
    before = Attribution.arms()
    assert before["n_on"] + before["n_off"] >= 18, before
    assert "tether._ACTED_GUARD" in before["on"] + before["off"]
    # the flag's live value and the report must agree, whichever way it is set
    live = "tether._ACTED_GUARD" in before["on"]
    assert live == tether._ACTED_GUARD

    os.environ["TETHER_ACTED_GUARD"] = "1" if not live else "0"
    try:
        after = Attribution.arms()
        assert after == before, "arms() must read the MODULE -- the env changed and it did not"
    finally:
        os.environ.pop("TETHER_ACTED_GUARD", None)


def test_a_ledger_states_the_arms_its_run_had():
    """The run header (the reviewer 2026-10-08 18:56Z): every agent writes its arm state,
    from the live module values, ONCE before any step, in its own `@run` slot. Three
    plants: the header stripped is refused; a flag set differently after the run started
    is reported as a disagreement; and the header leaves the gate's verdict alone.

    Reintroduce by removing the header write in `Agent.__init__`, not by disabling this.
    """
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    from instruments import Attribution
    env = world.bind(gridworld.family("default", 0, 3))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="arms_header"), tether.Config(),
                      ledger.Ledger())
    ag.step()
    rows = ag.led.rows()
    head = rows[0]
    assert (head["slot"], head["step"], head["event"], head["cycle"]) == ("@run", "PLAN", "arms", 0)
    assert sum(1 for r in rows if r.get("event") == "arms") == 1, "the header is written once"
    recorded = Attribution.arms_row(rows)
    assert not Attribution.arms_disagree(recorded, Attribution.arms())
    # EVERY ARM-DECLARING MODULE IS IN THE HEADER, checked here because test_arm_modules is run
    # by nothing: it failed on lineage from 7d1a689 to 2026-10-15 unseen (the reviewer
    # 2026-10-15 02:37)
    import instruments
    import test_arm_modules
    assert not test_arm_modules.missing(instruments.ARM_MODULES), (
        "an arm-declaring module is missing from the header", test_arm_modules.missing(
            instruments.ARM_MODULES))
    assert "lineage._CARRY" in recorded["on"] + recorded["off"], "the carry arm is not recorded"
    assert gate.check(rows)["verdict"] == gate.PASS, "the header must not move the gate"
    # PLANT 1: the header stripped
    try:
        Attribution.arms_row(rows[1:])
        raise AssertionError("a ledger with no arms header was read as if it said which arms ran")
    except ValueError:
        pass
    # PLANT 2: a flag set differently after the run began
    was = tether._ACTED_GUARD
    tether._ACTED_GUARD = not was
    try:
        off = Attribution.arms_disagree(recorded, Attribution.arms())
        assert off == [f"tether._ACTED_GUARD: recorded {was}, live {not was}"], off
    finally:
        tether._ACTED_GUARD = was
    # WHICH CODE RAN (the reviewer 2026-10-12 12:41 CDT, item 4): the same row carries it
    import os
    import subprocess
    import tempfile
    assert {"files_sha", "n_files", "head", "tree", "dirty",
            "pythonhashseed"} <= recorded.keys(), recorded.keys()
    assert recorded["pythonhashseed"] == os.environ.get("PYTHONHASHSEED"), recorded
    assert recorded["n_files"] > 0 and len(recorded["files_sha"]) == 64
    # WHAT RAN (the reviewer 2026-10-15 00:09, 01:05): world, wrapper, game, entry, patched
    d = head["detail"]
    assert (d["world"], d["wrapper"], d["game"]) == ("gridworld.GridWorld", None,
                                                     "arms_header"), d
    assert d["entry"] and d["entry"].endswith(".py") and isinstance(d["patched_seen"], list) \
        and isinstance(d["patched_declared"], list), d
    # PLANT 5: a plain function, and (ii) a functools.wraps spy, from this file, put into a project
    # class, are both seen (wraps copies __module__, never co_filename)
    import functools
    real_h = gamma.Term.handle
    here = os.path.basename(__file__)

    def _plain(self, g):
        return real_h(self, g)

    @functools.wraps(real_h)
    def _wrapped(self, g):
        return real_h(self, g)
    for spy in (_plain, _wrapped):
        gamma.Term.handle = spy
        try:
            seen = Attribution.run(env, ag.gamma)["patched_seen"]
        finally:
            gamma.Term.handle = real_h
        assert f"gamma.Term.handle <- {here}" in seen, (spy.__name__, seen)
    assert f"gamma.Term.handle <- {here}" not in Attribution.run(env, ag.gamma)["patched_seen"], (
        "a restored function must not stay listed")
    # PLANT 3: one hashed file's bytes changed -> files_sha changes
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "m.py")
        with open(f, "wb") as fh:
            fh.write(b"x = 1\n")
        a = Attribution.files_sha([f], d)
        with open(f, "wb") as fh:
            fh.write(b"x = 2\n")
        assert Attribution.files_sha([f], d) != a, "a changed file must change files_sha"
    # PLANT 4: git absent -> None with a reason, never raised
    real = subprocess.run

    def _no_git(*_a, **_k):
        raise FileNotFoundError("git")
    subprocess.run = _no_git
    try:
        c = Attribution.code()
    finally:
        subprocess.run = real
    assert c["head"] is None and c["tree"] is None and c["dirty"] is None, c
    assert c["git_unknown"].startswith("FileNotFoundError") and len(c["files_sha"]) == 64, c
    # THE LIBRARY ON DISK (the reviewer 2026-10-14 03:41): the header stamps it, and the list names
    # exactly the files the three agent-path loaders read
    import builtins
    import io
    import shutil

    import compile_term
    import inherited
    import instruments
    root = os.path.dirname(os.path.abspath(instruments.__file__))
    assert (recorded["library_sha"], recorded["library_n_files"]) == Attribution.library_sha(root)
    # the spy sits at the open level: Path.read_text reaches io.open, a bare open() builtins.open;
    # the three loaders are cached (tether._library, inherited.load, compile_term.readings), so each
    # cache is cleared first or a loader already run would read nothing under the spy
    seen: set = set()
    real_open = io.open

    def _spy(file, *a, **k):
        if isinstance(file, (str, os.PathLike)):
            rel = os.path.relpath(os.fspath(file), root).replace(os.sep, "/")
            if rel.startswith("library/") and not rel.endswith(".py"):
                seen.add(rel)
        return real_open(file, *a, **k)
    loaders = (tether._library, inherited.load, compile_term.readings)
    for f in loaders:
        f.cache_clear()
    builtins.open = io.open = _spy
    try:
        inherited.load()
        compile_term.readings()
        tether._library()
    finally:
        builtins.open = io.open = real_open
        for f in loaders:
            f.cache_clear()
    data = {p for p in Attribution.LIBRARY_FILES
            if not p.endswith(".py") and os.path.isfile(os.path.join(root, *p.split("/")))}
    assert seen == data, (sorted(seen - data), sorted(data - seen))
    # PLANT 5: the same files under another root -> the same stamp; one byte more -> another
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "library"))
        for p in Attribution.LIBRARY_FILES:
            if os.path.isfile(src := os.path.join(root, *p.split("/"))):
                shutil.copyfile(src, os.path.join(d, *p.split("/")))
        a = Attribution.library_sha(d)
        assert a == Attribution.library_sha(root), "the stamp must not depend on where it sits"
        with open(os.path.join(d, "library", "library_runtime.py"), "ab") as fh:
            fh.write(b"\n")
        assert Attribution.library_sha(d)[0] != a[0], "a changed library file must change it"


def test_undeclared_death():
    """A CHOSEN death with no disproof is farming wearing an experiment's word (§21.2)."""
    r = valid()
    r.append({"mode": "specified", "seq": 5, "cycle": 1, "step": "IMPORT", "slot": "@loop",
              "event": "ending", "detail": {"how": "death", "deliberate": True}})
    _refuses(r, gate.UNDECLARED_DEATH)


def _refusal(term):
    r = valid()
    r[0]["detail"]["bound"] = "t"
    r.insert(2, {"mode": "specified", "seq": 9, "cycle": 0, "step": "MINT", "slot": "s",
                 "event": "not_t", "detail": {"term": term, "verdict": "did not pay"}})
    return r


def test_a_refusal_of_the_bound_term_passes():
    """F498: the refused term is the one the slot's bet this cycle was made by."""
    assert gate.check(_refusal("t"))["verdict"] == gate.PASS


def test_refused_unbound():
    """F498: a refusal of a term the slot had already replaced blames what did not predict."""
    _refuses(_refusal("an_old_term"), gate.REFUSED_UNBOUND)


def _abandoned(set_by, held, set_on=3, judged=3):
    r = valid()
    r.insert(4, {"mode": "specified", "seq": 8, "cycle": 0, "step": "SETTLE", "slot": "s",
                 "event": "routine_abandoned",
                 "detail": {"set_by": "p", "set_by_plan": set_by, "held_plan": held,
                            "set_on_act": set_on, "judged_after_act": judged}})
    return r


def test_an_abandonment_on_its_own_claim_passes():
    """F502: the plan abandoned is the plan that made the failed claim."""
    assert gate.check(_abandoned(7, 7))["verdict"] == gate.PASS


def test_abandoned_on_anothers_claim():
    """F502: an ended routine's expectation dropped its successor."""
    _refuses(_abandoned(7, 9), gate.ABANDONED_ON_ANOTHERS_CLAIM)


def test_judged_on_another_act():
    """F502: a claim is about ONE act; judged after a later one, it is stale."""
    _refuses(_abandoned(7, 7, set_on=3, judged=4), gate.JUDGED_ON_ANOTHER_ACT)


def _observed(*pairs):
    r = valid()
    for i, (actual, alphabet) in enumerate(pairs):
        r.insert(1 + i, {"mode": "specified", "seq": 20 + i, "cycle": 0, "step": "PERCEIVE",
                         "slot": "o0.shape", "event": "bet",
                         "detail": {"mass": 0.0, "actual": actual, "alphabet": alphabet}})
    return r


def test_distinct_observations_under_one_residue_are_aliased():
    """A shape label 0 and a label 8 priced under 8 labels read as one (2026-10-07)."""
    _refuses(_observed((0, 8), (8, 8)), gate.ALIASED)


def test_the_value_before_is_an_observation():
    """The first reading arrives as a bet's value-before, never as an actual (ar25, cycle 0)."""
    r = valid()
    r.insert(1, {"mode": "specified", "seq": 20, "cycle": 0, "step": "PERCEIVE",
                 "slot": "o0.shape", "event": "bet",
                 "detail": {"mass": 0.0, "from_value": 0, "actual": 8, "alphabet": 8}})
    _refuses(r, gate.ALIASED)


def _predicted(predicted, code, alphabet, bound="t"):
    r = valid()
    r.insert(1, {"mode": "specified", "seq": 20, "cycle": 0, "step": "PERCEIVE",
                 "slot": "o0.shape", "event": "bet",
                 "detail": {"mass": 0.0, "actual": predicted % alphabet, "alphabet": alphabet,
                            "predicted": predicted, "predicted_code": code, "bound": bound}})
    return r


def test_a_prediction_coded_under_another_alphabet_is_aliased():
    """F2: 59 predicted, coded 0 (under the bet-time 59), priced under 61 (sp80 c11)."""
    _refuses(_predicted(59, 0, 61), gate.ALIASED)


def test_a_prediction_coded_under_its_own_alphabet_passes():
    """F2: the same bet coded under 61; a wrap on purpose (4 under 4 is 0); an own-clock reading."""
    for args in ((59, 59, 61), (4, 0, 4), (70, 70, 61, "own_clock")):
        assert gate.check(_predicted(*args))["verdict"] == gate.PASS, args


def test_observations_the_alphabet_separates_pass():
    """The same two labels once the count includes the new one; and a signed value is its own."""
    assert gate.check(_observed((0, 9), (8, 9), (-2, 9)))["verdict"] == gate.PASS


def test_declared_death_passes():
    """The same death WITH its disproof stated is the experiment §21.2 licenses."""
    r = valid()
    r.append({"mode": "specified", "seq": 5, "cycle": 1, "step": "IMPORT", "slot": "@loop",
              "event": "ending",
              "detail": {"how": "death", "deliberate": True,
                         "disproof": {"live": 40, "splits": 3, "refuted_at_least": 12}}})
    assert gate.check(r)["verdict"] == gate.PASS


def test_world_inflicted_death_is_not_the_subject():
    """An UNCHOSEN death is not a bypass of anything, so declaring it would be theatre."""
    r = valid()
    r.append({"mode": "specified", "seq": 5, "cycle": 1, "step": "IMPORT", "slot": "@loop",
              "event": "ending", "detail": {"how": "death"}})
    assert gate.check(r)["verdict"] == gate.PASS


def _resolved(target_detail, *, twice=False):
    r = valid()
    r.insert(1, {"mode": "specified", "seq": 30, "cycle": 0, "step": "PERCEIVE", "slot": "o0.row",
                 "event": "bet", "detail": target_detail})
    for i in range(2 if twice else 1):
        r.append({"mode": "specified", "seq": 40 + i, "cycle": 0, "step": "SETTLE",
                  "slot": "@signal", "event": "resolution",
                  "detail": {"signal_seq": 30, "kind": "game", "how": "cap", "fed": None}})
    return r


def test_a_resolution_of_a_signal_passes():
    """MC2: one resolution row pointing at a TRANSITION bet the ground answered."""
    assert gate.check(_resolved({"channel": "transition", "mass": 0.0}))["verdict"] == gate.PASS


def test_a_resolution_of_a_non_signal_is_refused():
    """MC1/13.3: the @bracket row (mass 0 on a closed channel) is not a signal."""
    _refuses(_resolved({"channel": "bracket", "mass": 0.0}), gate.RESOLVED_NON_SIGNAL)


def test_a_signal_resolved_twice_is_refused():
    """MC2: exactly one resolution per signal, never a third row."""
    _refuses(_resolved({"channel": "transition", "mass": 0.0}, twice=True), gate.RESOLVED_TWICE)


def test_the_cli_exit_code_carries_the_verdict():
    """A refusal exits non-zero (the reviewer 2026-10-11 22:56 CDT). gate.py printed its verdict
    and always exited 0, and conform/check.py's gate stage passes on returncode 0 -- so that
    stage could not fail. The refused ledger must turn the stage, read through check.py's own
    run_stage, to something other than ok."""
    import pathlib
    import subprocess
    import tempfile
    here = pathlib.Path(_repo.ROOT)
    sys.path.insert(0, str(here / "conform"))
    import check
    bad = valid()
    bad[3], bad[2] = dict(bad[2], seq=3), dict(bad[3], seq=2)     # ACCEPT before MINT
    assert gate.check(bad)["token"] == gate.STEP_ORDER
    with tempfile.TemporaryDirectory() as d:
        for name, rows, want in (("ok", valid(), 0), ("bad", bad, 1)):
            f = pathlib.Path(d) / f"{name}.jsonl"
            f.write_text("".join(gate.json.dumps(r) + chr(10) for r in rows), encoding="utf-8")
            rc = subprocess.run([sys.executable, str(here / "gate.py"), str(f)],
                                capture_output=True, text=True).returncode
            assert rc == want, f"{name}: exit {rc}, want {want}"
            status, _ = check.run_stage([sys.executable, str(here / "gate.py"), str(f)])
            assert (status == "ok") == (want == 0), f"{name}: check.py stage read {status}"


# **THE RUNNER GOES LAST, AND IT COUNTS ITSELF -- `F416`.** It used to sit mid-file and
# collect `globals()` at the moment it ran, so THREE test functions defined BELOW it did not
# exist yet and were never collected: 20 defined, 17 run, and the seat reported green. The
# three were the section 21.2 UNDECLARED_DEATH / farming guards. All three PASS when called
# directly, so nothing was hiding -- what there was, was a guard never exercised by the seat
# that reports it.
#
# THE COUNT ASSERTION IS THE PART THAT CANNOT GO QUIET AGAIN. Collecting after all definitions
# fixes today's file; asserting that the number RUN equals the number DEFINED IN THE SOURCE
# fixes the next one, because a function added below the runner would now FAIL rather than be
# skipped in silence.
if __name__ == "__main__":
    import pathlib
    import re as _re

    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    src = pathlib.Path(__file__).read_text(encoding="utf-8")
    declared = len(_re.findall(r"^def (test_\w+)", src, _re.M))
    if len(fns) != declared:
        missed = sorted(set(_re.findall(r"^def (test_\w+)", src, _re.M)) - set(globals()))
        raise AssertionError(
            f"{declared} tests defined in the source and {len(fns)} collected -- "
            f"{missed} are defined after the runner and would never run")
    for fn in fns:
        fn()
    print(f"{len(fns)} gate checks pass ({declared} defined)")
