"""BUILD 4 ITEM 16c, BOTH SIDES OF A SYMMETRIC GOAL (TETHER_GOAL_BOTH_SIDES; the reviewer
2026-11-05 r1189; Fig 12 :112; the Operators Table's symmetry test). A held hypothesis whose one
comparison is symmetric is wanted on both operands' slots. Seconds: a gridworld agent stepped
twice, with ARC's comparison atoms so a POSITION equality compiles (as test_inferred_cause's
MF-C3); the condition compiled by compile_term, held through _hyp_hold with its route stubbed (the
route is not what is tested).

MF-B1  "o0.row == o1.row" held: the link's slots are o0.row AND o1.row, both wanted, a mirror
MF-B2  "o0.row < o1.row" (asymmetric) held: one slot, no mirror -- today's link
MF-B3  "o0.row == o1.row" with the mirror's slot already wanting: no mirror, its want untouched
The red is behavioural, the arm OFF on this tree: TETHER_GOAL_BOTH_SIDES=0 fails MF-B1.

    python tests/test_goal_both_sides.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_atoms  # noqa: E402
import arc_predict  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def held(text: str, taken: bool = False):
    env = world.bind(gridworld.family("default", 0))
    atoms = {a.name: a for a in env.atoms()}
    atoms.update({a.name: a for a in arc_atoms.three_spaces(arc_predict.predict())})
    ag = tether.Agent(env, gamma.Gamma(list(atoms.values()), game="fam_default_0"),
                      tether.Config(), ledger.Ledger())
    ag.step()
    ag.step()
    ag.wants.clear()
    ag._hyp_route = lambda *_a: "a route"
    c = tether.compile_term.compile_candidate({"condition": text}, atoms)
    assert not isinstance(c, tether.compile_term.Refusal), (text, c)
    if taken:                       # the mirror's own slot already holds a composed want
        m = tether.compile_term.converse(c, atoms)
        ag.wants[m.slot] = "a composed want"
    link, why = ag._hyp_hold("@test", c, ag.trace[-1][2])
    assert link is not None, (text, why)
    return ag, c, link


def main():
    ag, c, link = held("o0.row == o1.row")
    assert len(link["slots"]) == 2 and link.get("mirror") and link["mirror"] != c.slot and \
        all(s in ag.wants for s in link["slots"]), (
            "MF-B1: the symmetric goal is wanted on one side only", link)
    # the goal exit's next read: the mirror slot's own target is the other operand's value, so
    # BECOME <mirror> +/- is formed toward it by the existing path
    st, mir = dict(ag.trace[-1][2]), link["mirror"]
    st[c.slot] = (st[mir] + 1) % ag.alphabet[c.slot]
    tgt = ag._goal_target(mir, st)
    assert tgt == st[c.slot], ("MF-B1: the mirror slot's goal target is not the other operand",
                               mir, tgt, st[c.slot], ag._gt_which)
    print(f"  MF-B1 'o0.row == o1.row' ({c.term.atoms[0].name}): slots {link['slots']}, "
          f"mirror {mir}, wants {[ag.wants[s] for s in link['slots']]}; {mir}'s target "
          f"{tgt} = {c.slot}'s value")
    _ag2, c2, link2 = held("o0.row < o1.row")
    assert len(link2["slots"]) == 1 and "mirror" not in link2, ("MF-B2", link2)
    print(f"  MF-B2 'o0.row < o1.row' ({c2.term.atoms[0].name}): slots {link2['slots']}, no "
          f"mirror (asymmetric)")
    ag3, c3, link3 = held("o0.row == o1.row", taken=True)
    other = tether.compile_term.converse(c3, {a.name: a for a in ag3.gamma.atoms}).slot
    assert "mirror" not in link3 and ag3.wants[other] == "a composed want", ("MF-B3", link3)
    print(f"  MF-B3 the mirror slot {other} already wants: slots {link3['slots']}, its want "
          f"untouched")
    print("test_goal_both_sides OK")


if __name__ == "__main__":
    main()
