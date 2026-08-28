"""The gate's eight checks, one defect each. Tests only what would silently break.

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


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
    print(f"{len(fns)} gate checks pass")


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
