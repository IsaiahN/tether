"""The gate's checks, one defect each. Tests only what would silently break.

**THE COUNT IS NOT WRITTEN DOWN HERE ON PURPOSE -- `F416`.** It said EIGHT while the file
held twenty and the runner ran seventeen, and a number in prose is a number nobody
re-derives. The runner prints `run (defined)` and REFUSES when they differ.

Stage 0's done-when: a valid ledger passes, and a ledger with each defect fails naming
that check's fixed token.
"""

import sys

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
        dst = G.Gamma([take, inc], game="B")
        rep = dst.load(path)
        # ACCEPT: the guarded term crosses, as itself, with its birth game recorded.
        assert "inc?ACTED_SELF" in dst.library, "a guarded term must ARRIVE with its guard"
        assert dst.carried["inc?ACTED_SELF"]["from"] == "A"
        # LOSS: the operand-only term still collapses, and SAYS SO rather than
        # reporting the benign-sounding `already_held`.
        assert rep["destroyed_on_carry"] == 1, rep
        assert rep["destroyed"][0]["collapsed_to"] == "take"
        assert rep["destroyed"][0]["lost"] == "o1.colour"
        # DEDUP: loading the same file again is a real duplicate, not a loss.
        again = dst.load(path)
        assert again["loaded"] == 0 and again["deduped_onto_composition"] == 2, again
        assert again["destroyed_on_carry"] == 1, "the collapse is not a dedup"


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


def test_a_typed_operand_placeholder_separates_kinds_and_still_merges_within_one():
    """`F420.1`/`F420.3`: fourteen compositions separated ONLY by their operand all arrive
    spelled `same . all` and thirteen are deduped away. The operand's BINDING cannot cross
    -- `o1.colour` names an object another board lacks -- but its KIND can, and that is
    what tells two of them apart (the reviewer, 2026-10-03).

    BOTH DIRECTIONS IN ONE TEST, because a placeholder that separates everything is as
    wrong as one that separates nothing: DIFFERENT kinds must arrive as different terms,
    and the SAME kind must still merge -- one law, many instances.

    AND `operand` MUST BE None ON EVERY ARRIVAL. The kind is a record of what the operand
    read, not a binding; leaving a stale slot name on a carried term would hand the next
    board an operand naming an object it does not have.

    Reintroduce by dropping `operand_kind=` in `load`, not by disabling this.
    """
    import pathlib
    import tempfile

    import gamma as G
    take, inc = G.Atom("take", _idn, "val", "val"), G.Atom("inc", _idn, "val", "val")
    src_g = G.Gamma([take, inc], game="A")
    # what the Agent hands over: two EXTENT slots, one COLOUR, one POSITION
    src_g.slot_kinds = {"o1.colour": "COLOUR", "o2.row": "POSITION",
                        "o3.distance": "EXTENT", "o4.proximity": "EXTENT"}
    for i, slot in enumerate(("o1.colour", "o2.row", "o3.distance", "o4.proximity")):
        t = G.Term(atoms=(take, inc), operand=slot)
        src_g.accept(t, seq=i, residual="s@0")
        src_g.handles.setdefault(t.name, t.handle(src_g.game))
    with tempfile.TemporaryDirectory() as d:
        path = str(pathlib.Path(d) / "lib.json")
        src_g.save(path)
        dst = G.Gamma([take, inc], game="B")
        rep = dst.load(path)
        got = {n for n, t in dst.library.items() if t.origin != G.PRIOR}
        # THREE, not one: the kinds separate COLOUR from POSITION from EXTENT.
        assert got == {"take . inc<:COLOUR>", "take . inc<:POSITION>",
                       "take . inc<:EXTENT>"}, got
        assert rep["loaded"] == 3, rep
        # and the two EXTENT slots DO merge, with the absorbed one named.
        assert rep["merged_into"] == {"take . inc<:EXTENT>": 1}, rep
        assert dst.merged["take . inc<:EXTENT>"][0]["operand"] == "o4.proximity"
        # no arrival carries a slot name from the board it came from
        assert all(dst.library[n].operand is None for n in got)


def test_undeclared_death():
    """A CHOSEN death with no disproof is farming wearing an experiment's word (§21.2)."""
    r = valid()
    r.append({"mode": "specified", "seq": 5, "cycle": 1, "step": "IMPORT", "slot": "@loop",
              "event": "ending", "detail": {"how": "death", "deliberate": True}})
    _refuses(r, gate.UNDECLARED_DEATH)


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
