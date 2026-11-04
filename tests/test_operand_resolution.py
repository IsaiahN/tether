"""BUILD 2, OPERAND RESOLUTION (TETHER_OPERAND_COMPILE, TETHER_OPERAND_EVIDENCE; the reviewer
2026-11-03 r940). A junction ingredient that names no held atom resolves through its library
entry's view compiled by compile_term (Fig 6 :21, the closure adds no atom); a held atom bound
nowhere resolves by the agent's own evidence at the bargain; operands pair per object. About 10 s.

MF-A1  an entry whose view compiles resolves to the readings its compiled terms read, on each object
       that has them on the board (compiled); RED on HEAD (no resolution: names_no_atom)
MF-A2  an entry whose every candidate is ill-typed is REFUSED with compile_term's own reason, never
       compiled anyway; a name no entry carries is UNREACHABLE
MF-A3  (r944 a) the refusal is tallied by the missing piece it names: "atom touches"
MF-A4  (r944 b) two keys one name spells in two cases within one domain are one entry, never
       "ambiguous"
MF-B1  per-object pairing: o1.shape against o1's own row, never o2's -- a cross-object co-movement
       (o1.shape with o2.row) reads + False per object, where the unpaired union reads + True
MF-B2  a held atom no bound term names, TRIED at a slot, binds there under the arm and not without
MF-F1  (r946 3) a name in two domains whose entries compile to different readings is a FAMILY of 2
       candidates (Autocatalysis: CHEMICAL / MORPHOGENETIC); RED on HEAD ("ambiguous", unreachable)
MF-F2  two domains compiling to the same readings merge to 1 (Agency: ACTION / EMBODIMENT)
MF-F3  an entry whose view holds no condition is UNREACHABLE "no condition" (was refused)
MF-F4  end to end: a junction Autocatalysis ? Agency is 2 tested candidates and Agency ? Arbitrage
       1, over a hand-built window -- families 1, candidates 3, tested 2; family arm OFF: tested 0
       (both names "ambiguous")
MF-P   (r946 5) a retarget writes a bond_tests row of the board being left (at, board), the run's
       end another; RED on HEAD (no row at the retarget); arm OFF: the run-end row only, no at
MF-OFF both arms OFF (a child process): the gridworld bond_tests row is bd4acfd's -- 17
       names_no_atom + 1 atom_bound_nowhere, no resolved_by -- and nothing is noted at the bargain

    python tests/test_operand_resolution.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import compile_term  # noqa: E402
import composer  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def agent(steps):
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    for _ in range(steps):
        ag.step()
    return ag, led


def off() -> dict:
    ag, led = agent(12)
    ag.end_run("cap")
    d = [r for r in led.rows() if r.get("event") == "bond_tests"][-1]     # the run's end
    d = d.get("detail", d)
    return {"side": d["unbound_by_side"], "resolved_by": "resolved_by" in d,
            "noted": len(ag._atom_ev)}


READS = ("age", "stability", "filled", "h", "w")


def family_row(ag, on: bool) -> dict:
    """r946 3 end to end: two hand-built junctions over a hand-built window of five frames."""
    frames = [{f"o1.{r}": (t * (i + 1)) % 3 for i, r in enumerate(READS)} for t in range(5)]
    tr = [(frames[t], "ACTION1", frames[t + 1]) for t in range(4)]
    mols = [{"molecule": "ZZZ|X", "node": composer.Bonded(composer.UNKNOWN, "Autocatalysis",
                                                          "Agency")},
            {"molecule": "ZZZ|Y", "node": composer.Bonded(composer.UNKNOWN, "Agency",
                                                          "Arbitrage")}]
    was = (composer.candidates, tether._OPERAND_FAMILY, ag.trace, ag._window_at, ag.bound)
    try:
        composer.candidates = lambda *_a, **_k: mols
        tether._OPERAND_FAMILY = on
        ag.trace, ag._window_at, ag.bound = tr, 0, {}
        ag._bond_tests()
    finally:
        composer.candidates, tether._OPERAND_FAMILY, ag.trace, ag._window_at, ag.bound = was
    d = [r for r in ag.led.rows() if r.get("event") == "bond_tests"][-1]
    return d.get("detail", d)


def per_board(on: bool) -> list:
    """r946 5: six steps, a new board, four steps, the run's end -> (at, board, frames) per row."""
    was = tether._BOND_PER_BOARD
    try:
        tether._BOND_PER_BOARD = on
        ag, led = agent(6)
        ag.retarget(ag.env, ag.level, how=tether.NEW_BOARD)
        for _ in range(4):
            ag.step()
        ag.end_run("cap")
    finally:
        tether._BOND_PER_BOARD = was
    rows = [r.get("detail", r) for r in led.rows() if r.get("event") == "bond_tests"]
    return [(d.get("at"), d.get("board"), d["frames"]) for d in rows]


def main():
    if "--off" in sys.argv:
        assert not (tether._OPERAND_COMPILE or tether._OPERAND_EVIDENCE), "the child runs OFF"
        print(json.dumps(off()))
        return
    assert tether._OPERAND_COMPILE and tether._OPERAND_EVIDENCE, "both arms are ON by default"
    ag, _led = agent(2)
    lib = tether._library()
    atoms = {a.name: a for a in ag.gamma.atoms}
    sig = compile_term.signature(atoms)
    held = {tether._norm_name(a.name) for a in ag.gamma.atoms}
    board = {"o1.stability", "o1.age", "o2.stability", "o1.row"}
    wide = {f"o1.{r}" for r in READS}
    got, how, why = ag._ingredient_operand("ACOUSTIC|X", "20kHz", held, board, lib, atoms, sig)
    assert how == "compiled" and got == {"o1": {"o1.age", "o1.stability"},
                                         "o2": {"o2.stability"}}, ("MF-A1", how, got, why)
    _g, how2, why2 = ag._ingredient_operand("ACOUSTIC|X", "Surface hard", held, board, lib,
                                            atoms, sig)
    assert how2 == "refused" and "does not accept" in why2, ("MF-A2 refused", how2, why2)
    tally = dict(ag._refusal_tally)
    assert tally.get("atom touches", 0) >= 1, ("MF-A3 the tally names the missing atom", tally)
    _g, how4, why4 = ag._ingredient_operand("PHENOMENOLOGICAL|X", "Lived meaning", held, board,
                                            lib, atoms, sig)
    assert how4 != "unreachable" and "ambiguous" not in why4, ("MF-A4 name case", how4, why4)
    _g, how3, _w = ag._ingredient_operand("X|Y", "No Such Entry Anywhere", held, board, lib,
                                          atoms, sig)
    assert how3 == "unreachable", ("MF-A2 unreachable", how3)
    left = {"o1": ["o1.shape"], "o2": ["o2.shape"]}
    right = {"o1": ["o1.row"], "o2": ["o2.row"]}
    frames = [{"o1.shape": t, "o2.shape": 0, "o1.row": 0, "o2.row": t, "o3.col": 0}
              for t in range(5)]
    paired = tether.Agent._per_object("+", left, right, ["o1", "o2"], frames, ["o3.col"], ())
    union = composer.window_test("+", [(f["o1.shape"], f["o2.shape"]) for f in frames],
                                 [(f["o1.row"], f["o2.row"]) for f in frames], [True] * 5)
    assert paired[0] is False and union[0] is True, ("MF-B1 per object", paired[:2], union[:2])
    free = next(a.name for a in ag.gamma.atoms if ag._ingredient_slots(a.name) == ())
    ag._atom_ev[tether._norm_name(free)] = {"o1.row": 1}
    got_b, how_b, _w = ag._ingredient_operand("X|Y", free, held, board, lib, atoms, sig)
    was = tether._OPERAND_EVIDENCE
    try:
        tether._OPERAND_EVIDENCE = False
        _g, how_off, _w = ag._ingredient_operand("X|Y", free, held, board, lib, atoms, sig)
    finally:
        tether._OPERAND_EVIDENCE = was
    assert (how_b, got_b, how_off) == ("tried", {"o1": {"o1.row"}}, "atom_bound_nowhere"), (
        "MF-B2 tried", how_b, got_b, how_off)
    fam, how_f, why_f = ag._ingredient_operand("ZZZ|X", "Autocatalysis", held, wide, lib, atoms,
                                               sig)
    assert how_f == "compiled" and isinstance(fam, list) and len(fam) == 2, (
        "MF-F1 family", how_f, fam, why_f)
    one, how_s, why_s = ag._ingredient_operand("ZZZ|X", "Agency", held, wide, lib, atoms, sig)
    assert how_s == "compiled" and isinstance(one, dict), ("MF-F2 merged", how_s, one, why_s)
    _g, how_n, why_n = ag._ingredient_operand("ACOUSTIC|X", "Chladni pattern", held, wide, lib,
                                              atoms, sig)
    assert how_n == "unreachable" and "no condition" in why_n, ("MF-F3", how_n, why_n)
    f4 = family_row(ag, True)
    f4_off = family_row(ag, False)
    assert (f4["families"], f4["candidates"], f4["tested"]) == (1, 3, 2), ("MF-F4", f4)
    assert f4_off["tested"] == 0 and "families" not in f4_off, ("MF-F4 OFF", f4_off)
    p_on, p_off = per_board(True), per_board(False)
    assert p_on[0][:2] == ("new_board", 0) and p_on[0][2] > 0 and p_on[-1][:2] == ("run", 1) \
        and len(p_on) == 2, ("MF-P", p_on)
    assert p_off == [(None, None, p_off[0][2])], ("MF-P OFF", p_off)
    env = {**os.environ, "TETHER_OPERAND_COMPILE": "0", "TETHER_OPERAND_EVIDENCE": "0",
           "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run([sys.executable, "-B", __file__, "--off"], env=env, capture_output=True,
                         text=True, timeout=300)
    assert out.returncode == 0, out.stderr[-2000:]
    o = json.loads(out.stdout.strip().splitlines()[-1])
    assert o == {"side": {"names_no_atom": 17, "atom_bound_nowhere": 1}, "resolved_by": False,
                 "noted": 0}, ("MF-OFF", o)
    print(f"  MF-A1 20kHz compiles to {sorted(got['o1'])} on o1, {sorted(got['o2'])} on o2")
    print(f"  MF-A2 refused: {why2[:90]}; a name no entry carries: {how3}")
    print(f"  MF-A3 refusals by missing piece: {sorted(tally)[:4]}")
    print(f"  MF-A4 'Lived Meaning' / 'Lived meaning' (one domain) resolve as one entry: {how4}")
    print(f"  MF-F1 Autocatalysis: a family of {len(fam)} ({why_f})")
    print(f"  MF-F2 Agency: one candidate {sorted(one['o1'])}; MF-F3 {why_n}")
    print(f"  MF-F4 ON families {f4['families']}, candidates {f4['candidates']}, tested "
          f"{f4['tested']}; family OFF tested {f4_off['tested']}")
    print(f"  MF-P (at, board, frames) ON {p_on}; OFF {p_off}")
    print(f"  MF-B1 cross-object co-movement: per object + {paired[0]}, the union + {union[0]}")
    print(f"  MF-B2 {free!r} tried at o1.row: {how_b} ON, {how_off} OFF")
    print(f"  MF-OFF the gridworld row as at bd4acfd: {o}")
    print("test_operand_resolution OK")


if __name__ == "__main__":
    main()
