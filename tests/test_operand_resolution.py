"""BUILD 2, OPERAND RESOLUTION (TETHER_OPERAND_COMPILE, TETHER_OPERAND_EVIDENCE; the reviewer
2026-11-03 r940). A junction ingredient that names no held atom resolves through its library
entry's view compiled by compile_term (Fig 6 :21, the closure adds no atom); a held atom bound
nowhere resolves by the agent's own evidence at the bargain; operands pair per object. About 10 s.

MF-A1  an entry whose view compiles resolves to the readings its compiled terms read, on each object
       that has them on the board (compiled); RED on HEAD (no resolution: names_no_atom)
MF-A2  an entry whose every candidate is ill-typed is REFUSED with compile_term's own reason, never
       compiled anyway; a name no entry carries is UNREACHABLE
MF-B1  per-object pairing: o1.shape against o1's own row, never o2's -- a cross-object co-movement
       (o1.shape with o2.row) reads + False per object, where the unpaired union reads + True
MF-B2  a held atom no bound term names, TRIED at a slot, binds there under the arm and not without
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
    d = next(r for r in led.rows() if r.get("event") == "bond_tests")
    d = d.get("detail", d)
    return {"side": d["unbound_by_side"], "resolved_by": "resolved_by" in d,
            "noted": len(ag._atom_ev)}


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
    got, how, why = ag._ingredient_operand("ACOUSTIC|X", "20kHz", held, board, lib, atoms, sig)
    assert how == "compiled" and got == {"o1": {"o1.age", "o1.stability"},
                                         "o2": {"o2.stability"}}, ("MF-A1", how, got, why)
    _g, how2, why2 = ag._ingredient_operand("ACOUSTIC|X", "Surface hard", held, board, lib,
                                            atoms, sig)
    assert how2 == "refused" and "does not accept" in why2, ("MF-A2 refused", how2, why2)
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
    print(f"  MF-B1 cross-object co-movement: per object + {paired[0]}, the union + {union[0]}")
    print(f"  MF-B2 {free!r} tried at o1.row: {how_b} ON, {how_off} OFF")
    print(f"  MF-OFF the gridworld row as at bd4acfd: {o}")
    print("test_operand_resolution OK")


if __name__ == "__main__":
    main()
