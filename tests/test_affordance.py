"""AFFORDANCE BET (TETHER_AFFORDANCE, default ON; Isaiah 2026-11-16 "balls can roll, does this
roll?"; write-up 40 "Affordances: shape -> concept -> properties -> predictions"). Fixtures by hand:
nothing here needs wip/shape-names or wip/word-map to have landed.
  A1  a prior row once per new kind, with the chain and its stamp, and no standing field
  A2  the first press moves the object -> affordance_settle (and 'keeps moving' settles a step on)
  A3  it does not move -> affordance_refuse with the condition; the prior kept, except_when grows
  A4  nsm says all of them with only listed capitals
  A0  sources absent -> inert, one affordance_inert row saying why
  MF-A1 TETHER_AFFORDANCE OFF: no rows -> RED as required
  A6  the landed sources: disc -> sphere -> ball predicts moves through a contact verb whose
      WordNet '@' chain reaches verb.motion (TETHER_CONTACT_MOVES, moves_via carried)
  MF-A6 TETHER_CONTACT_MOVES OFF: ball's contact-only priors predict nothing -> RED as required
  A5  gridworld 12 steps ON and OFF both pass the gate
Seconds.
    python tests/test_affordance.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import affordance  # noqa: E402
import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import nsm  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

# the formats read on origin/wip/word-map (word_map["priors"], word_map["shape_bridge"]) and
# origin/wip/shape-names (SHAPE_ATOMS), built by hand: the test does not need either to land
STAMP = {"corpus": "fixture", "sha": "0", "stage": "abstraction"}
PRIORS = [{"concept": "TOPOLOGICAL|Box", "action_verb": "push", "verb_lexname": "verb.motion",
           "source": "gloss", "stamp": {"corpus": "fixture", "sha": "0", "stage": "regularity"},
           "standing": "none"},
          {"concept": "TOPOLOGICAL|Box", "action_verb": "open", "verb_lexname": "verb.stative",
           "source": "gloss", "stamp": {"corpus": "fixture", "sha": "0", "stage": "regularity"}}]
BRIDGE = [{"shape_2d": ["circle", "disc"], "form_3d": [{"name": "sphere"}], "stamp": STAMP,
           "objects": [{"name": "ball", "actions": [
               {"verb": "hit", "verb_lexname": "verb.contact", "source": "gloss"},
               {"verb": "roll", "verb_lexname": "verb.motion", "source": "gloss"},
               {"verb": "roll on", "reading": "keeps moving", "source": "fixture"}]}],
           "standing": "none"}]
ATOMS = {"square": ("TOPOLOGICAL|Box", "AGENT|is_square")}
SHAPES = {"o1": "disc", "o2": "square"}


def agent(src=(ATOMS, BRIDGE, PRIORS, None)):
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    ag.step()
    ag._aff_book = affordance.Book()
    ag._aff_src = src
    ag.env.shape_name = SHAPES.get
    ag._kind_str = lambda o: f"kind<{SHAPES.get(o, 'other')}>"     # one kind per shape here
    return ag, led


def rows(led, n0, prefix="affordance_"):
    return [r for r in led.rows()[n0:] if r["event"].startswith(prefix)]


def main() -> int:
    assert affordance._ON is True, "the arm defaults ON"
    ag, led = agent()
    st = ag.env.observe()
    n0 = len(led.rows())
    ag._aff_see(st)
    ag._aff_see(st)                          # the same kinds again: no new row
    pr = rows(led, n0)
    assert [r["event"] for r in pr] == ["affordance_prior"] * 3, pr
    ball = [r for r in pr if r["detail"]["concept"] == "ball"]
    assert {r["detail"]["property"] for r in ball} == {"moves", "keeps moving"}
    d = ball[0]["detail"]
    assert d["shape_name"] == "disc" and d["form"] == "sphere" and d["via"] == "shape_bridge", d
    mv = next(r["detail"] for r in ball if r["detail"]["property"] == "moves")
    assert mv["action_verb"] == "roll" and mv["stamp"] == {
        "source": "gloss", "stage": "abstraction", "corpus": "fixture", "sha": "0"}, mv
    assert not any("standing" in r["detail"] for r in pr), "a prior carries no standing"
    box = [r for r in pr if r["detail"]["concept"] == "TOPOLOGICAL|Box"]
    assert len(box) == 1 and box[0]["detail"]["via"] == "SHAPE_ATOMS", box
    assert affordance.shape_name_of(True) is None and affordance.shape_name_of("ring") == "ring"
    print("A1 prior rows once per new kind (disc -> sphere -> ball; square -> box), stamped, "
          "no standing:", [(r["slot"], r["detail"]["concept"], r["detail"]["property"])
                           for r in pr], "GREEN")

    n0 = len(led.rows())
    ag._last_landed = None
    ag._aff_felt("o1", ["o1.row", "o3.col"], True)
    st1 = rows(led, n0)
    assert [r["event"] for r in st1] == ["affordance_settle"], st1
    assert "kind<disc>" in ag._aff_book.pending
    st = dict(ag.env.observe())
    st["o1.row"] = (st.get("o1.row") or 0) + 1                   # it moved again, no press on it
    real = ag.env.observe
    ag.env.observe = lambda: st
    ag.cycle += 1
    ag._aff_keeps()
    ag.env.observe = real
    st2 = rows(led, n0)[1:]
    assert [(r["event"], r["detail"]["property"]) for r in st2] == [
        ("affordance_settle", "keeps moving")], st2
    print("A2 the press moved it -> affordance_settle (moves), a step on -> affordance_settle "
          "(keeps moving):", ag._aff_book.counts["kind<disc>"], "GREEN")

    n0 = len(led.rows())
    ag._aff_ctx = ("o2", (("wall", 1),))
    ag._aff_felt("o2", ["o3.col"], True)
    rf = rows(led, n0)
    assert [r["event"] for r in rf] == ["affordance_refuse"], rf
    dr = rf[0]["detail"]
    assert dr["condition"] == "touching ('wall', 1)" and dr["except_when"] == [dr["condition"]]
    rec = ag._aff_book.prior[("kind<square>", "moves")]
    assert rec["except_when"] == [dr["condition"]] and rec["name_now"] == "square", rec
    assert ag._aff_book.counts["kind<square>"] == {"held": 1, "settled": 0, "refused": 1,
                                                   "exceptions": 1}
    n1 = len(led.rows())
    ag._aff_felt("o2", ["o3.col"], True)                         # judged once: no second row
    assert not rows(led, n1)
    print(f"A3 it did not move -> affordance_refuse when {dr['condition']!r}; prior kept, "
          f"except_when {rec['except_when']}, name back to {rec['name_now']!r}: GREEN")

    def motion(on):
        affordance._MOTION_UPPER = on
        try:
            ag7, led7 = agent()
            s0 = dict(ag7.env.observe())
            s0["o1.row"], s0["o1.col"] = 3, 2
            ag7._aff_see(s0)
            s1 = dict(s0, **{"o1.col": 3})                   # dcol > 0 at the press
            ag7.env.observe = lambda: s1
            n7 = len(led7.rows())
            ag7._last_landed = None
            ag7._aff_felt("o1", ["o1.col"], True)
            s2 = dict(s1, **{"o1.col": 4})                   # it moved again, no press on it
            ag7.env.observe = lambda: s2
            ag7.cycle += 1
            ag7._aff_keeps()
            return [r["detail"] for r in rows(led7, n7) if r["event"] == "affordance_settle"]
        finally:
            affordance._MOTION_UPPER = True
    b7 = motion(True)
    assert [d.get("direction") for d in b7] == ["right", "right"], b7
    assert b7[1].get("manner") == "rolls" and "manner" not in b7[0], b7
    assert affordance.direction({"o.row": 2, "o.col": 2}, {"o.row": 1, "o.col": 3}, "o") == \
        "up-right" and affordance.manner(False, ["roll"]) == "is pushed" and \
        affordance.manner(True, ["slide"]) == "glides"
    say7 = nsm.say_row("affordance_settle", b7[1], ("w", "a"))[0][1]
    assert "`ball` `rolls` `to the right`" in say7 and not nsm.unlisted(say7), say7
    print("B7 dcol>0 -> direction right; keeps moving + roll -> rolls:", say7, "GREEN")
    b7off = motion(False)
    assert len(b7off) == 2 and not any("direction" in d or "manner" in d for d in b7off), b7off
    print("MF-B7 TETHER_MOTION_WORDS OFF: no direction/manner fields -> RED as required")

    lines = [nsm.say_row(r["event"], r["detail"], ("win", "advance"))[0][1]
             for r in pr + st1 + st2 + rf]
    inert = nsm.say_row("affordance_inert", {"reads": "no affordance priors"}, ("w", "a"))[0][1]
    for s in lines + [inert]:
        assert not nsm.unlisted(s), (s, nsm.unlisted(s))
    for s in lines + [inert]:
        print("   nsm:", s)
    print("A4 nsm says every affordance row with only listed capitals: GREEN")

    ag0, led0 = agent(src=(None, None, [], "no affordance priors: word_map.json absent"))
    n0 = len(led0.rows())
    ag0._aff_see(ag0.env.observe())
    ag0._aff_see(ag0.env.observe())
    r0 = rows(led0, n0)
    assert [r["event"] for r in r0] == ["affordance_inert"], r0
    print("A0 sources absent -> one affordance_inert row:", r0[0]["detail"]["reads"], "GREEN")

    real = affordance.load_sources()
    try:
        import arc_percept
        names = getattr(arc_percept, "SHAPE_NAMES", None)
    except Exception:                   # noqa: BLE001
        names = None
    if real[3] is None and names and "disc" in names:
        ag6, led6 = agent(src=real)
        st6 = dict(ag6.env.observe())
        st6["o1.shape_name"] = names.index("disc")            # perception's index, as published
        ag6.env.shape_name = lambda _o: None
        n0 = len(led6.rows())
        ag6._aff_see(st6)
        r6 = [r for r in rows(led6, n0) if r["slot"] == "o1"]
        assert r6 and r6[0]["detail"]["concept"] == "ball", r6
        d6 = r6[0]["detail"]
        print("A6 the landed sources: shape_name index", names.index("disc"), "->",
              f"{d6['shape_name']} -> {d6['form']} -> {d6['concept']} ({d6['action_verb']}, "
              f"{d6['verb_lexname']}, stamp {d6['stamp']}): GREEN")
        print("   nsm:", nsm.say_row(r6[0]["event"], d6, ("w", "a"))[0][1])
        chain = affordance.resolve("disc", real[0], real[1], real[2])
        contact = [p for p in chain["priors"] if p.get("verb_lexname") == "verb.contact"
                   and p.get("moves_object") is True]
        assert d6["property"] == "moves" and d6["verb_lexname"] == "verb.contact", d6
        assert d6.get("moves_via") and d6["moves_via"][-1].endswith("(verb.motion)"), d6
        print("A6 the contact prior predicts moves through its WordNet chain:", d6["action_verb"],
              d6["moves_via"], "GREEN")
        affordance._CONTACT_MOVES = False
        # ALSO off: TETHER_RELATIONS_READ. ConceptNet's own verbs predict "moves" through
        # CN_READING, so leaving it on would supply a ball prior for a reason this must-fail is
        # not testing; the arm under test here is TETHER_CONTACT_MOVES alone (2026-11-16 merge).
        _rel_saved = getattr(affordance, "_RELATIONS_READ", None)
        if _rel_saved is not None:
            affordance._RELATIONS_READ = False
        try:
            assert contact and not any(affordance.readings(p) for p in contact), contact
            ag6x, led6x = agent(src=real)
            ag6x.env.shape_name = lambda _o: None
            n0 = len(led6x.rows())
            ag6x._aff_see(st6)
            r6x = [r for r in rows(led6x, n0) if r["slot"] == "o1"]
            assert not any(r["detail"].get("concept") == "ball" for r in r6x), r6x
        finally:
            affordance._CONTACT_MOVES = True
            if _rel_saved is not None:
                affordance._RELATIONS_READ = _rel_saved
        print("MF-A6 TETHER_CONTACT_MOVES OFF: ball's contact-only priors",
              [p["action_verb"] for p in contact], "predict nothing; o1 ->",
              [(r["detail"].get("concept"), r["detail"].get("property")) for r in r6x],
              "-> RED as required")
    else:
        print("A6 SKIP: shape names / word map not on this tree:", real[3])

    affordance._ON = False
    try:
        env = world.bind(gridworld.family("default", 0))
        led2 = ledger.Ledger()
        ag2 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                           led2)
        for _ in range(3):
            ag2.step()
        off = rows(led2, 0)
        assert not off and ag2.__dict__.get("_aff_book") is None, off
    finally:
        affordance._ON = True
    print("MF-A1 TETHER_AFFORDANCE OFF: no affordance rows -> RED as required")

    for on in (True, False):
        affordance._ON = on
        env = world.bind(gridworld.family("default", 0))
        led3 = ledger.Ledger()
        ag3 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                           led3)
        for _ in range(12):
            ag3.step()
        ag3.end_run("cap")
        v = gate.check(led3.rows())["verdict"]
        assert v == "pass", ("A5", on, v)
        if on:
            ev = sorted({r["event"] for r in rows(led3, 0)})
            print("   gridworld ON affordance rows:", ev)
    affordance._ON = True
    print("A5 gridworld 12 steps ON and OFF: both pass the gate: GREEN")
    print("affordance: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
