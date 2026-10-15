"""(b'-q) THE INDEX HOLD (the reviewer 2026-10-14 11:46, 12:19, 12:23): a held role's view compiled
ONCE under the placeholders and bound per question must be the compile of the named text.

  R'-1 every library entry x held role, for each sample pair of two worlds, under the relation arm
       OFF and ON: bound == named (slot, term name, atom chain, operand, guard, guard_ref, origin,
       operand tree, compiled operand, parties, absent; refusals by reason); the bound Term holds
       THIS Gamma's atoms. Sample (registered 12:17): per world, the first frame's plain owners
       sorted by id, every ordered pair of the first three, plus (o9, o10).
  O2   (o9, o10) reverses the placeholders' sort: at least one bbox compile is compared.
  F1   a second question differing only in names compiles nothing.
  F2   a second Agent (a new Gamma over the same world) compiles nothing and binds ITS atoms.
  F4   an atom outside T leaves the key unchanged (a Gamma's atom set is fixed at construction,
       gamma 779-780, so growth is a Gamma built with one more atom).
  F4'  an atom inside T ("below") changes the key, and R'-1 holds under each atom set.
  O1   MUST-FAIL in process: tokens that a world can produce ("o1", "o2") break R'-1.
  M1   the bound memo (the reviewer 2026-10-15 04:57): the same (entry, role, o, x) asked again
       is served without _bound, equal to the first and to the named compile; a list the caller
       altered does not reach the memo. M2: the pair reversed is bound, not served (an
       order-losing key). M3: the same o with a new x is bound (x in the key; the reviewer
       2026-10-15 05:11).
  MEM  3 sequential fake games in one fresh process, index hold ON, then OFF: held size,
       traced and peak memory per game.
  F1, F2 and F4 go through Agent._compiled, the path _index_reach calls. Phase 2 (R'-1 on the
  ARC world built with the relation arm, F4', O1) and each MEM read run in their OWN process,
  arms set in the environment at start: every TETHER_ line of --env FILE, or without it the
  relation arm alone, printed as the one-arm variant.

    python test_index_hold.py [--env FILE]
"""
from __future__ import annotations

import gc
import os
import subprocess
import sys
import tracemalloc
from dataclasses import replace
from pathlib import Path

sys.dont_write_bytecode = True

import arc_holdout  # noqa: E402
import compile_term  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import tether_agent  # noqa: E402
import world  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402


def _form(c):
    if c is None:
        return None
    if isinstance(c, compile_term.Refusal):
        return ("R", c.reason)
    t = c.term
    return ("C", c.slot, t.name, tuple(a.name for a in t.atoms), t.operand, t.guard, t.guard_ref,
            t.origin, t.operand_term.name if t.operand_term is not None else None, c.operand,
            c.parties, c.absent)


def _named(lib, key, role, o, x, atoms):
    """Today's compile of the named text, fresh (no cache)."""
    def comp(cond):
        return compile_term.compile_candidate({"condition": cond}, atoms)
    out = []
    for cand in lib.view(key, role, o, x):
        if role == "CAUSE":
            out.append((cand, comp(cand["if"]), comp(cand["then"])))
        else:
            out.append((cand, None if "quantifier" in cand else comp(cand["condition"]), None))
    return out


def _bound(ag, lib, key, role, o, x, atoms, sig):
    sub = lambda s: tether._ph_sub(s, o, x)  # noqa: E731
    return [(cand, tether._bound(a, sub, atoms), tether._bound(b, sub, atoms))
            for cand, a, b in ag._held_index(lib, key, role, atoms, sig)]


def _real(ag, lib, key, o, x, atoms, sig) -> list:
    """The agent's own path (Agent._compiled) for a held role; a named compile raises."""
    def named(_cond):
        raise AssertionError("the held path made a named compile")
    return list(ag._compiled(lib, key, "STATE", o, x, named, atoms, sig))


def _round_trip(ag, lib, keys, pairs, atoms) -> tuple[int, int, list]:
    """R'-1 over every entry x held role x pair. Returns (compared, bbox compared, differences)."""
    sig = compile_term.signature(atoms)
    compared, bbox, diffs = 0, 0, []
    for k in keys:
        for role in tether._HELD_ROLES:
            for o, x in pairs:
                named = _named(lib, k, role, o, x, atoms)
                got = _bound(ag, lib, k, role, o, x, atoms, sig)
                if len(named) != len(got):
                    diffs.append((k, role, o, x, "count", len(named), len(got)))
                    continue
                for (nc, na, nb), (bc, ga, gb) in zip(named, got, strict=True):
                    for n_, g_ in ((na, ga), (nb, gb)):
                        compared += n_ is not None
                        if _form(n_) != _form(g_):
                            diffs.append((k, role, o, x, _form(n_), _form(g_)))
                        elif isinstance(g_, compile_term.Compiled):
                            if any(a is not atoms[a.name] for a in g_.term.atoms):
                                diffs.append((k, role, o, x, "not this Gamma's atoms"))
                            bbox += g_.slot.endswith(".bbox") and (o, x) == ("o9", "o10")
                    if {f: v for f, v in nc.items() if f not in ("condition", "if", "then")} != \
                            {f: v for f, v in bc.items() if f not in ("condition", "if", "then")}:
                        diffs.append((k, role, o, x, "candidate fields"))
    return compared, bbox, diffs


def _pairs(env) -> list:
    ids = sorted({o for o in env.slot_owner().values() if tether._PLAIN.fullmatch(o)},
                 key=lambda s: int(s[1:]) if s[1:].isdigit() else 10 ** 9)[:3]
    return [(o, x) for o in ids for x in ids if o != x] + [("o9", "o10")]


def _worlds():
    env = world.bind(gridworld.family("default", 0))
    gw = tether.Agent(env, gamma.Gamma(env.atoms(), game="index_hold_gw"), tether.Config(),
                      ledger.Ledger())
    arc_env, arc_ag, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    return [("gridworld", env, gw), ("fake ARC", arc_env, arc_ag)]


def main() -> None:
    lib = tether._library()
    assert lib is not None, "no library"
    keys = list(dict.fromkeys([*lib.seed, *lib.runtime, *lib.learnings]))
    worlds = _worlds()
    total_bbox = 0
    for rel in (False, True):
        compile_term._RELATION_SET = rel
        for name, env, ag in worlds:
            tether._INDEX_STORE.clear()
            atoms = {a.name: a for a in ag.gamma.atoms}
            pairs = _pairs(env)
            n, bbox, diffs = _round_trip(ag, lib, keys, pairs, atoms)
            assert not diffs, f"R'-1 REFUTED ({name}, relation arm {rel}): {diffs[:3]}"
            assert n, f"R'-1 compared nothing ({name}, relation arm {rel})"
            total_bbox += bbox
            print(f"  R'-1 {name}, relation arm {'ON' if rel else 'OFF'}: {n} compiles equal over "
                  f"{len(keys)} entries x {len(tether._HELD_ROLES)} roles x {len(pairs)} pairs "
                  f"{pairs[:2]}..; bbox at (o9, o10): {bbox}", flush=True)
    assert total_bbox, "O2: no bbox compile was compared at (o9, o10)"
    print(f"  O2 bbox re-sort exercised at (o9, o10): {total_bbox} compiles")

    name, env, ag = worlds[0]
    atoms = {a.name: a for a in ag.gamma.atoms}
    sig = compile_term.signature(atoms)
    k = next(k for k in keys if lib.view(k, "STATE", "o1", "o2"))
    calls = []
    real = compile_term.compile_candidate
    compile_term.compile_candidate = lambda c, a: calls.append(1) or real(c, a)
    try:
        tether._INDEX_STORE.clear()
        _real(ag, lib, k, "o1", "o2", atoms, sig)
        first = len(calls)
        _real(ag, lib, k, "o3", "o4", atoms, sig)
        assert first and len(calls) == first, ("F1", first, len(calls))
        print(f"  F1 a second question, names only changed: {len(calls) - first} compiles "
              f"(the first: {first})")
        ag2 = tether.Agent(env, gamma.Gamma(env.atoms(), game="index_hold_gw2"), tether.Config(),
                           ledger.Ledger())
        atoms2 = {a.name: a for a in ag2.gamma.atoms}
        got = _real(ag2, lib, k, "o1", "o2", atoms2, compile_term.signature(atoms2))
        assert len(calls) == first, ("F2", first, len(calls))
        assert all(a is atoms2[a.name] for _c, c, _b in got
                   if isinstance(c, compile_term.Compiled) for a in c.term.atoms), "F2 atoms"
        print("  F2 a second Agent: 0 compiles, its own Gamma's atoms bound")
        outside = replace(next(a for n_, a in atoms.items()
                               if n_ not in compile_term.TEMPLATE_ATOMS), name="index_hold_extra")
        assert compile_term.signature({**atoms, outside.name: outside}) == sig, "F4: the key moved"
        grown = {**atoms, outside.name: outside}
        _real(ag, lib, k, "o1", "o2", grown, compile_term.signature(grown))
        assert len(calls) == first, ("F4", first, len(calls))
        print("  F4 an atom outside T: the key unchanged, 0 compiles")
    finally:
        compile_term.compile_candidate = real
    # M1 / M2 after the compile spy is restored: M1 compares with the named compile, which would
    # move F4's count. Agent._compiled is the path; R'-1 calls tether._bound directly (72-75).
    nb = []
    real_bound = tether._bound
    tether._bound = lambda *a: nb.append(1) or real_bound(*a)
    try:
        ag._bound_cache.clear()
        hits = tether._INDEX_N["bound_memo_hit"]
        r1 = _real(ag, lib, k, "o1", "o2", atoms, sig)
        assert nb, ("M1: the first ask bound nothing", len(nb))
        before = len(nb)
        r2 = _real(ag, lib, k, "o1", "o2", atoms, sig)
        assert len(nb) == before and tether._INDEX_N["bound_memo_hit"] == hits + 1, (
            "M1: a repeated question was bound again", len(nb) - before)
        named = _named(lib, k, "STATE", "o1", "o2", atoms)
        form = [[(_form(a), _form(b)) for _c, a, b in r] for r in (r2, r1, named)]
        assert form[0] == form[1] == form[2], "M1: the memo's answer differs"
        # mutate the list _compiled ITSELF returns: _real copies it (85), which hid MF-3
        raw = ag._compiled(lib, k, "STATE", "o1", "o2", None, atoms, sig)
        raw.append("M1 sentinel")
        r3 = _real(ag, lib, k, "o1", "o2", atoms, sig)
        assert "M1 sentinel" not in r3 and len(r3) == len(r1), (
            "M1: a caller's list reached the memo")
        print(f"  M1 the bound memo: a repeat served without _bound ({before} binds once), equal "
              "to the named compile; a caller's list does not reach it")
        before = len(nb)
        _real(ag, lib, k, "o2", "o1", atoms, sig)
        assert len(nb) > before, ("M2: another (o, x) was served from the memo", len(nb) - before)
        print(f"  M2 another (o, x): bound afresh ({len(nb) - before} binds)")
        before, hits = len(nb), tether._INDEX_N["bound_memo_hit"]
        _real(ag, lib, k, "o1", "o3", atoms, sig)
        assert len(nb) > before and tether._INDEX_N["bound_memo_hit"] == hits, (
            "M3: x not in the memo key", len(nb) - before)
        print(f"  M3 the same o, a new x: bound afresh ({len(nb) - before} binds)")
    finally:
        tether._bound = real_bound

    # PHASE 2 AND THE MEMORY READS, EACH IN ITS OWN PROCESS, ARMS SET AT START (the reviewer
    # 2026-10-14 12:56). "below" exists only when the relation arm is ON AT IMPORT (arc_atoms
    # 892-894; its admitting clause registers at import, 298). Given --env FILE, every TETHER_ line
    # of it is in the environment (the flipped ARC state); without it, the relation arm alone.
    for mode, added in (("--relation", {}), ("--mem", {"TETHER_INDEX_HOLD": "1"}),
                        ("--mem", {"TETHER_INDEX_HOLD": "0"})):
        r = subprocess.run([sys.executable, "-B", __file__, mode],
                           env={**_child_env(), **added}, cwd=os.getcwd(),
                           stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
        sys.stdout.write(r.stdout)
        assert r.returncode == 0, f"{mode} {added} failed:\n{r.stderr[-3000:]}"
    print("index hold: OK")


def _child_env() -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    if "--env" in sys.argv:
        path = sys.argv[sys.argv.index("--env") + 1]
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            k, sep, v = line.strip().partition("=")
            if sep and k.startswith("TETHER_"):
                env[k] = v
        env["INDEX_HOLD_ENV"] = path
    else:
        env["TETHER_RELATION_SET"] = "1"
        env["INDEX_HOLD_ENV"] = "TETHER_RELATION_SET=1 only (the one-arm variant)"
    return env


def _header(ag) -> str:
    h = next(e.detail for e in ag.led.by_event("arms") if e.slot == "@run")
    rel = [f for f in h["on"] if f.endswith("._RELATION_SET")]
    hold = [f for f in (*h["on"], *h["off"]) if f.endswith("._INDEX_HOLD")]
    return (f"env {os.environ.get('INDEX_HOLD_ENV')}; header on {len(h['on'])} off "
            f"{len(h['off'])}; relation arm ON in {rel}; index hold "
            f"{'ON' if any(f in h['on'] for f in hold) else 'OFF'}")


def relation_phase() -> None:
    """The flipped tree's ARC state: atoms built with the relation arm, compiled under it."""
    assert compile_term._RELATION_SET, "phase 2 must be started with TETHER_RELATION_SET=1"
    lib = tether._library()
    keys = list(dict.fromkeys([*lib.seed, *lib.runtime, *lib.learnings]))
    env, ag, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    atoms = {a.name: a for a in ag.gamma.atoms}
    print(f"  PHASE 2: {_header(ag)}; 'below' in the atom set: {'below' in atoms}", flush=True)
    assert "below" in atoms, "F4': the world holds no 'below'"
    pairs = _pairs(env)
    tether._INDEX_STORE.clear()
    n, bbox, diffs = _round_trip(ag, lib, keys, pairs, atoms)
    assert not diffs and n, ("R'-1 REFUTED, fake ARC built with the relation arm", diffs[:3])
    print(f"  R'-1 fake ARC, built and compiled with the relation arm ('below' held): {n} compiles "
          f"equal over {len(keys)} entries x {len(tether._HELD_ROLES)} roles x {len(pairs)} pairs; "
          f"bbox at (o9, o10): {bbox}", flush=True)
    without = {n_: a for n_, a in atoms.items() if n_ != "below"}
    assert compile_term.signature(without) != compile_term.signature(atoms), "F4': key unchanged"
    tether._INDEX_STORE.clear()
    n, _, diffs = _round_trip(ag, lib, keys, pairs[:2], without)
    assert not diffs and n, ("F4' R'-1 without 'below'", diffs[:3])
    print(f"  F4' 'below' is in T: the key moves; R'-1 holds without it ({n} compiles)")

    o_, x_ = tether.PH_O, tether.PH_X
    tether.PH_O, tether.PH_X = "o1", "o2"
    try:
        tether._INDEX_STORE.clear()
        _, _, diffs = _round_trip(ag, lib, keys[:400], [("o2", "o1")], atoms)
    finally:
        tether.PH_O, tether.PH_X = o_, x_
        tether._INDEX_STORE.clear()
    assert diffs, "O1 MUST-FAIL did not fail: tokens a world produces were not caught"
    print(f"  O1 must-fail fired: tokens o1/o2 give {len(diffs)} differences, e.g. {diffs[0][:5]}")


def mem_phase() -> None:
    """MEM: 3 sequential fake games in ONE fresh process, the index hold as the environment set it,
    so ON and OFF are read the same way (the reviewer 12:19, add 1; 12:56). Each read follows a
    gc.collect() and counts the Agents still alive: the after-collection profile (14:24)."""
    tracemalloc.start()
    for g in range(3):
        rep = tether_agent.run(FakeWrapper(), "fake", 2)
        gc.collect()
        alive = sum(isinstance(o, tether.Agent) for o in gc.get_objects())
        cur, peak = tracemalloc.get_traced_memory()
        print(f"  MEM index hold {'ON' if tether._INDEX_HOLD else 'OFF'}, after game {g + 1}: "
              f"Agents alive after gc {alive}; {len(tether._INDEX_STORE)} held (entry, role); "
              f"traced {cur / 2**20:.1f} MiB, peak "
              f"{peak / 2**20:.1f} MiB; counts {dict(tether._INDEX_N)}; acted {rep['acted']}",
              flush=True)
    tracemalloc.stop()


if __name__ == "__main__":
    (relation_phase if "--relation" in sys.argv else mem_phase if "--mem" in sys.argv
     else main)()
