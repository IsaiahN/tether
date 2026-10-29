"""C-lineage-1, THE BOUNDARY WRITE (the reviewer 2026-10-15 07:30, 07:32). WRITTEN, NOT RUN: it runs
in the end-of-step-7 checklist (Isaiah 05:25). Real gridworld Agents; each role its own process with
TETHER_LINEAGE_CARRY, TETHER_LINEAGE_BOUNDARY and TETHER_INDEX_HOLD set at start. Gridworld has no
level edge, so a role crosses K boundaries by calling lineage.boundary between plays, as both
runners do at a level clear or a terminal edge.

  L1   one game: generations written == K boundaries + 1 for the game end.
  L2   one line: each generation's parent is the one written before it; _chain loads with no N3.
  L3   no duplicates: the fold holds each term the instance wrote once, and its evidence equals
       the instance's evidence list, in order.
  L4   a stop after boundary k (no game-end write) loses at most the current level: a new
       instance loads the tip written at k; every term written up to k is taken at load
       (loaded + already_held == the terms the reps wrote; the reviewer 2026-10-15 07:41); and at
       least one memo entry is pending when the stopped game had bound answers.
  MF-L MUST-FAIL: the parent left at the loaded one after each write -> N3 (L2 red).
  MF-D MUST-FAIL: the written map cleared after each write -> a term written twice (L3 red).

    python tests/test_lineage_boundary.py
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import lineage_store  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

K, N = 3, 8
N_ON = 8   # MF-D (ii)'s steps a level under seed 0, lengthened only if its occasion is absent


def _agent(seed):
    env = world.bind(gridworld.family("default", seed))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"),
                        tether.Config(), ledger.Ledger())


def role_game(d, stop, mf, n=N):
    """Play K levels with a boundary after each; `stop` >= 0 stops after that boundary with no
    game-end write. `mf` removes the parent move ("parent") or the written map ("written")."""
    assert lineage._BOUNDARY and lineage._CARRY and tether._INDEX_HOLD, "arms must be ON at start"
    ag = _agent(0)
    lineage.load(d, ag)
    loaded = ag.lineage_parent
    reps = []
    for k in range(K):
        for _ in range(n):
            ag.step()
        reps.append(lineage.boundary(d, ag, "default", "level"))
        if mf == "parent":
            ag.lineage_parent = loaded
        elif mf == "written":
            ag._lineage_written = {}
        if k == stop:
            break
    else:
        ag.end_run("cap")
        reps.append(lineage.write(d, ag, "default"))
    # L3 compares the fold's evidence with the agent's, under the names the SAVE writes: with
    # TETHER_KIND_SAVE (3) an instance's evidence is written under its kind's name, so the
    # expected list is mapped the same way (the reviewer 2026-10-29 r301: map, don't pin; L3 is
    # about the evidence crossing whole and in order, which keeps being tested ON)
    ev = ([[e[0], lineage._kind_name(ag.gamma, e[1]), *e[2:]] for e in ag.gamma.evidence]
          if getattr(lineage, "_KIND_SAVE", False) else ag.gamma.evidence)
    print("REPORT " + json.dumps({"reps": [{k: r.get(k) for k in ("hash", "parent", "terms",
                                                                   "refused")} for r in reps],
                                  "evidence": ev,
                                  "bound": len(ag._bound_cache) + len(tether._BOUND_MEMO)}),
          flush=True)


def role_load(d):
    ag = _agent(1)
    rep = lineage.load(d, ag)
    lib = sorted(n for n, t in ag.gamma.library.items() if t.origin != gamma.PRIOR)
    st = json.dumps({n: dataclasses.asdict(ag.gamma.standing[n]) for n in lib
                     if n in ag.gamma.standing}, sort_keys=True, default=str)
    print("LOAD " + json.dumps({"parent": rep.get("parent"), "loaded": rep.get("loaded", 0),
                                "already_held": rep.get("already_held", 0),
                                "deduped": rep.get("deduped_onto_composition", 0),
                                "onto_atom": rep.get("destroyed_on_carry", 0),
                                "memo_pending": (rep.get("memo") or {}).get("pending", 0),
                                "library": lib, "replayed": rep.get("replayed"),
                                "standing": hashlib.sha256(st.encode()).hexdigest()[:16]}),
          flush=True)


def _occasion(d):
    """The life's seed, the term rows it wrote before its last generation, and its aliases."""
    chain = lineage._chain(Path(d))
    return (chain[0][1].get("seed"), sum(len(g["terms"]) for _h, g in chain[:-1]),
            sum(len(g.get("aliases", [])) for _h, g in chain))


def _aliases(d):
    return sum(len(json.loads(lineage_store.file_bytes(p)).get("aliases", []))
               for p in Path(d).glob(f"{lineage.PREFIX}*.json"))


def _child(*args, **arms):
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(TETHER_LINEAGE_CARRY="1", TETHER_LINEAGE_BOUNDARY="1", TETHER_INDEX_HOLD="1",
               **arms)
    return subprocess.run([sys.executable, "-B", __file__, "--role", *map(str, args)], env=env,
                          stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)


def _out(r, tag):
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads(next(ln for ln in r.stdout.splitlines() if ln.startswith(tag + " "))
                      [len(tag) + 1:])


def _l3_fold(f, evidence):
    rids = [lineage._rid(r) for r in f["terms"]]
    assert len(rids) == len(set(rids)), ("L3: a term written twice", len(rids) - len(set(rids)))
    # keyed by what load installs by, the operand's unbound form included (amends registered
    # refuter L3, the reviewer 2026-10-15 07:30, keyed by row_key, ruled 2026-10-25 21:38):
    # take<?.drow_?> and take<?.dist_?> are two compositions
    keys = [gamma.Gamma.row_key(r) for r in f["terms"]]
    assert len(keys) == len(set(keys)), ("L3: one composition in two rows",
                                         len(keys) - len(set(keys)))
    assert f["evidence"] == evidence, ("L3: evidence differs", len(f["evidence"]), len(evidence))
    over = {}
    for r in f["terms"]:
        if len(r["atoms"]) == 1 and r.get("operand"):
            over.setdefault(lineage._key(r), set()).add(gamma.Gamma.row_key(r))
    return len(keys), len(set(keys)), sum(len(v) > 1 for v in over.values())


def _l3(d, evidence):
    chain = lineage._chain(Path(d))
    n, m, k = _l3_fold(lineage.fold(chain), evidence)
    if k:
        print(f"  L3: {n} rows, {m} distinct row_keys, {k} one-atom terms over >1 operand")
    return chain


PARTS = ("l1", "l4", "mfl", "mfd", "mfdon")   # by name, one process each, under 5 min (r299)


def main(parts=PARTS):
    tmp = Path(tempfile.mkdtemp(prefix="bound_"))
    for p in parts:
        globals()[f"_part_{p}"](tmp)
    print("lineage boundary: OK")


def _part_l1(tmp):
    """L1, L2, L3 and L3's must-fail."""
    out = _out(_child("game", tmp / "full", -1, "none"), "REPORT")
    hs = [r["hash"] for r in out["reps"]]
    gens = sorted(Path(tmp / "full").glob(f"{lineage.PREFIX}*.json"))
    assert len(gens) == K + 1 and all(hs), ("L1", len(gens), out["reps"])
    print(f"  L1 one game, {K} boundaries: {len(gens)} generations")
    assert [r["parent"] for r in out["reps"]] == [None, *hs[:-1]], ("L2", out["reps"])
    chain = _l3(tmp / "full", out["evidence"])
    print(f"  L2 one line, {len(chain)} generations load in order; L3 no term twice, evidence "
          f"equal ({len(out['evidence'])} rows)")
    # L3 MUST-FAIL (the reviewer 2026-10-25 21:38): one row written twice, the same row_key under
    # another handle, as a bypassed written map would; L3 must name the composition clause
    f = lineage.fold(chain)
    assert f["terms"], "fixture: the full run wrote no term row"
    twin = {**f["terms"][0], "handle": f"{f['terms'][0].get('handle')}_twin"}
    try:
        _l3_fold({**f, "terms": [*f["terms"], twin]}, out["evidence"])
    except AssertionError as e:
        assert e.args[0][0] == "L3: one composition in two rows", ("L3 MF the wrong clause", e)
        print(f"  L3 must-fail fired: {e.args[0][0]}")
    else:
        raise AssertionError("L3 MUST-FAIL did not fail: a row written twice passed")
    # L3 EVIDENCE MUST-FAIL (the reviewer 2026-10-29 r301): the fold with one evidence row dropped
    # goes red on the evidence clause, so the mapped compare can still fail
    assert f["evidence"], "fixture: the full run kept no evidence"
    try:
        _l3_fold({**f, "evidence": f["evidence"][:-1]}, out["evidence"])
    except AssertionError as e:
        assert e.args[0][0] == "L3: evidence differs", ("L3 evidence MF the wrong clause", e)
        print(f"  L3 evidence must-fail fired: {e.args[0][0]} ({len(f['evidence']) - 1} against "
              f"{len(out['evidence'])})")
    else:
        raise AssertionError("L3 evidence MUST-FAIL did not fail: a dropped row passed")


def _part_l4(tmp):
    """L4."""
    k = 1
    out = _out(_child("game", tmp / "stop", k, "none"), "REPORT")
    assert len(out["reps"]) == k + 1, ("L4: boundaries written before the stop", out["reps"])
    got = _out(_child("load", tmp / "stop"), "LOAD")
    assert got["parent"] == out["reps"][-1]["hash"], ("L4: the tip is not boundary k", got)
    _l3(tmp / "stop", out["evidence"])   # the stop came right after boundary k
    wrote = sum(r["terms"] or 0 for r in out["reps"])
    assert got["loaded"] + got["already_held"] == wrote, ("L4: terms written vs taken", wrote,
                                                          got)
    assert out["bound"] == 0 or got["memo_pending"] > 0, ("L4: no memo carried", out, got)
    print(f"  L4 stopped after boundary {k}: the next instance loads its tip and all {wrote} "
          f"terms written ({got['loaded']} installed; already held {got['already_held']}: "
          f"{got['deduped']} onto a composition, {got['onto_atom']} onto an atom); "
          f"memo pending "
          f"{got['memo_pending']} (the stopped game bound {out['bound']})")


def _part_mfl(tmp):
    """MF-L."""
    r = _child("game", tmp / "mfl", -1, "parent")
    assert r.returncode != 0 and "tip" in r.stderr, "MF-L MUST-FAIL did not fail: no N3"
    print("  MF-L must-fail fired: the parent left behind gives two tips (N3)")


def _part_mfd(tmp):
    """MF-D (i), (d) OFF."""
    # (i) MF-D verbatim with (d) OFF (amends registered refuter MF-D, the reviewer 2026-10-15
    # 07:30, ruled 2026-10-25 21:27): under (d) the re-write a cleared map lets through is an
    # alias, so L3 cannot see it
    # THE OCCASION (the reviewer 2026-10-25 21:52, (m)): a free-seed life that writes no term row
    # before its last generation gives a cleared map nothing to write twice. A fresh birth is
    # drawn, up to 5, selected on the occasion ONLY, never on the outcome
    for birth in range(1, 6):
        mfd = tmp / f"mfd_{birth}"
        out = _out(_child("game", mfd, -1, "written", TETHER_SAVE_DEDUP="0"), "REPORT")
        seed, rows, al = _occasion(mfd)
        print(f"  MF-D birth {birth}: seed {seed}, rows before the last generation {rows}, "
              f"aliases {al}")
        if rows:
            break
    else:
        raise AssertionError("MF-D: no occasion in 5 births")
    try:
        _l3(mfd, out["evidence"])
    except AssertionError as e:
        print(f"  MF-D must-fail fired: {e.args[0][0]}")
    else:
        raise AssertionError("MF-D MUST-FAIL did not fail: the written map is not what dedups")


def _part_mfdon(tmp):
    """MF-D (ii) ON."""
    # (ii) MF-D ON, the shipped default: one seed and the same steps, the map intact and cleared.
    # The cleared map must show as aliases beyond the intact run's, and cost bytes, not meaning.
    # Its occasion is checked once under seed 0 at N_ON steps a level (lengthened, never re-seeded)
    # MF-D ON is ABOUT the aliases a cleared map adds, and TETHER_KIND_SAVE (3) writes no instance
    # alias by construction: pinned to KIND_SAVE OFF for these runs (the reviewer 2026-10-29 r299:
    # per check, in the test). ON TWIN: tests/test_kind_save.py check_gridworld (no instance alias,
    # and the same library and standing load: bytes, not meaning)
    pin = {"TETHER_AGENT_SEED": "0", "TETHER_KIND_SAVE": "0"}
    _out(_child("game", tmp / "on_full", -1, "none", N_ON, **pin), "REPORT")
    seed, rows, _al = _occasion(tmp / "on_full")
    print(f"  MF-D ON occasion: seed {seed}, {N_ON} steps a level, rows before the last "
          f"generation {rows}")
    assert rows, ("MF-D ON: no occasion under seed 0 at N_ON steps; lengthen N_ON", N_ON)
    _out(_child("game", tmp / "on_cleared", -1, "written", N_ON, **pin), "REPORT")
    n_full, n_cleared = _aliases(tmp / "on_full"), _aliases(tmp / "on_cleared")
    lf = _out(_child("load", tmp / "on_full", **pin), "LOAD")
    lc = _out(_child("load", tmp / "on_cleared", **pin), "LOAD")
    assert n_cleared > n_full, ("MF-D ON: the cleared map wrote no alias beyond the intact run's",
                                n_full, n_cleared)
    assert lf["library"] == lc["library"] and lf["standing"] == lc["standing"], (
        "MF-D ON: the cleared map changed what loads", lf, lc)
    print(f"  MF-D ON: aliases intact {n_full}, cleared {n_cleared}; the same library "
          f"({len(lf['library'])}) and standing ({lf['standing']}) load from both")


if __name__ == "__main__":
    if "--role" in sys.argv:
        a = sys.argv[sys.argv.index("--role") + 1:]
        if a[0] == "game":
            role_game(a[1], int(a[2]), a[3], int(a[4]) if len(a) > 4 else N)
        else:
            role_load(a[1])
    else:
        # part names on the command line run only those parts; none runs all
        main(tuple(a for a in sys.argv[1:] if a in PARTS) or PARTS)
