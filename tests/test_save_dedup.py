"""(d), DEDUP AT SAVE (TETHER_SAVE_DEDUP; Isaiah 2026-10-25 05:33, the reviewer 19:57 and 20:23): a
term row whose load key (gamma.Gamma.row_key) the parent fold or this save already holds as a row is
written as an alias {was, key}, and load_blob sends the alias where that row went.

  D-1  TWO-STEP: gen1 holds row K; gen2 and gen3 each carry an alias of K and no rows. Loaded
       through lineage.load on both load paths (the store and the re-fold), both aliases resolve
       to the term gen1's row installed, and the report counts them.
  D-2  MISSING KEY: an alias whose key no row holds raises, never resolves to nothing.
  D-3  MUST-FAIL: the same fold loaded with its aliases dropped leaves both names unmapped.
  D-4  GRIDWORLD write -> load, ON vs OFF: lives in two folders, one per arm. The ON folder holds
       aliases (the occasion, asserted > 0), and its last load has the same library, the same
       standing for every term, and the same replay as the OFF folder's. With its aliases dropped,
       the ON fold replays more not_held than the ON load (the must-fail at the agent's own scale).

NOT BYTES (the reviewer 2026-10-25 20:57): under the constant seed gamma.draw_seed is None, so
Term.handle draws its suffix at random per process; two processes on one tree write different
handles and generation hashes. Compare saves by content, never by hash, or rename handles first.

    python tests/test_save_dedup.py
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

N, LIVES = 20, 2


def _agent(seed=0):
    env = world.bind(gridworld.family("default", seed))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"), tether.Config(),
                        ledger.Ledger())


def _life(d, n):
    ag = _agent()
    rep = lineage.load(d, ag)
    for _ in range(n):
        ag.step()
    ag.end_run("cap")
    return ag, rep


def _put(d, gen):
    raw = json.dumps(gen, sort_keys=True, indent=1).encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()[:16]
    (Path(d) / f"{lineage.PREFIX}{h}.json").write_bytes(raw)
    return h


def _alias_gen(parent, was, key):
    return {"lineage": 1, "parent": parent, "game": "alias", "terms": [], "status": [],
            "evidence": [], "vindication_tail": [], "book": {}, "invented": {}, "dormant": [],
            "dormant_refused": [], "aliases": [{"was": was, "key": key}]}


def _gens(d):
    return lineage._read(d)


def _standing(gm):
    return {n: dataclasses.asdict(s) for n, s in getattr(gm, "standing", {}).items()}


def two_step(tmp):
    d = tmp / "two"
    d.mkdir()
    a, _ = _life(d, N)
    w = lineage.write(d, a, "default")
    row = next((r for r in _gens(d)[w["hash"]]["terms"] if r.get("was") and not r.get("guard_ref")),
               None)
    assert row, "fixture: gen1 wrote no row with a was and no guard_ref"
    k = gamma.Gamma.row_key(row)
    n1 = len(_gens(d)[w["hash"]].get("aliases", []))   # gen1's own: a composition minted twice
    h2 = _put(d, _alias_gen(w["hash"], "alias_two", k))
    _put(d, _alias_gen(h2, "alias_three", k))
    seen = {}
    for store in (True, False):
        lineage._MEMORY_STORE = store
        b, rep = _life(d, 0)
        got = {n: b.gamma.renamed.get(n) for n in (row["was"], "alias_two", "alias_three")}
        lost = {n for n in ("alias_two", "alias_three") if n in b.gamma.lost_onto_atom}
        if row["was"] in b.gamma.lost_onto_atom:
            assert lost == {"alias_two", "alias_three"}, ("D-1 an alias went another way", store,
                                                          lost)
        else:
            assert got[row["was"]] and got["alias_two"] == got["alias_three"] == got[row["was"]], (
                "D-1 an alias did not resolve to its row's term", store, got)
        assert sum((rep.get("aliases") or {}).values()) == n1 + 2, ("D-1 report", store, n1,
                                                                    rep.get("aliases"))
        seen[store] = got
    lineage._MEMORY_STORE = True
    assert seen[True] == seen[False], ("D-1 the two load paths disagree", seen)
    print(f"  D-1 two-step: {row['was']} -> {seen[True][row['was']]}; alias_two, alias_three -> "
          f"{seen[True]['alias_two']}, {seen[True]['alias_three']} (store and re-fold); gen1's own "
          f"aliases {n1}", flush=True)
    return row, k


def missing_and_mustfail(row, k):
    blob = {"terms": [row], "invented": {}, "vindication": [], "book": {}}
    g = _agent().gamma
    try:
        g.load_blob({**blob, "aliases": [{"was": "alias_lost", "key": json.dumps(["no such"])}]})
    except ValueError as e:
        assert "names a key no saved row holds" in str(e), ("D-2 wrong error", e)
    else:
        raise AssertionError("D-2 an alias naming no row did not raise")
    g = _agent().gamma
    g.load_blob({**blob, "aliases": [{"was": "alias_two", "key": k}]})
    assert "alias_two" in g.renamed or "alias_two" in g.lost_onto_atom, "D-3 control: no mapping"
    g = _agent().gamma
    g.load_blob(blob)
    assert "alias_two" not in g.renamed and "alias_two" not in g.lost_onto_atom, (
        "D-3 must-fail: with the aliases dropped the name still mapped")
    print("  D-2 an alias naming no row raises; D-3 aliases dropped -> the name is unmapped",
          flush=True)


def on_off(tmp):
    # D-4's occasion is an INSTANCE alias, which TETHER_KIND_SAVE (3) stops writing by construction;
    # under the reviewer's standing rule A-D its original runs with that arm OFF, and its ON twin is
    # tests/test_kind_save.py check_gridworld (library, standing, replay equal through the load).
    # PRE-EXISTING RED, r299 AFTER-DEADLINE: D-4's must-fail (aliases dropped, not_held must rise)
    # is red at 6c04c56 unchanged -- renamed fills from the rows' "was" there, so dropping aliases
    # loses nothing; to bisect from the 10-25 pass after the deadline
    kind_save, lineage._KIND_SAVE = lineage._KIND_SAVE, False
    try:
        _on_off(tmp)
    finally:
        lineage._KIND_SAVE = kind_save


def _on_off(tmp):
    out = {}
    for arm in (True, False):
        lineage._SAVE_DEDUP = arm
        d = tmp / ("on" if arm else "off")
        d.mkdir()
        for i in range(LIVES):
            a, _ = _life(d, N + 5 * i)
            lineage.write(d, a, "default")
        b, rep = _life(d, 0)
        out[arm] = (d, b, rep)
    lineage._SAVE_DEDUP = True
    (d_on, b_on, r_on), (d_off, b_off, r_off) = out[True], out[False]
    n_al = sum(len(g.get("aliases", [])) for g in _gens(d_on).values())
    assert n_al > 0, "D-4 precondition: the ON lives wrote no alias, so nothing is tested"
    assert not any(g.get("aliases") for g in _gens(d_off).values()), "D-4 OFF wrote an alias"
    rows_on = sum(len(g["terms"]) for g in _gens(d_on).values())
    rows_off = sum(len(g["terms"]) for g in _gens(d_off).values())
    lib_on, lib_off = set(b_on.gamma.library), set(b_off.gamma.library)
    assert lib_on == lib_off, ("D-4 library", sorted(lib_on ^ lib_off)[:8])
    s_on, s_off = _standing(b_on.gamma), _standing(b_off.gamma)
    diff = [n for n in set(s_on) | set(s_off) if s_on.get(n) != s_off.get(n)]
    assert not diff, ("D-4 standing", diff[:8])
    assert r_on["replayed"] == r_off["replayed"], ("D-4 replay", r_on["replayed"],
                                                   r_off["replayed"])
    h, f = lineage.head(d_on)
    g = _agent().gamma
    g.load_blob({"terms": f["terms"], "invented": f["invented"], "vindication": f["vindication"],
                 "book": f["book"]}, parent=h)
    dropped = g.replay(f["evidence"])
    assert dropped["not_held"] > r_on["replayed"]["not_held"], (
        "D-4 must-fail: aliases dropped and not_held did not rise", dropped, r_on["replayed"])
    print(f"  D-4 gridworld {LIVES} lives: rows ON {rows_on} + aliases {n_al}, OFF {rows_off}; "
          f"library {len(lib_on)} = {len(lib_off)}; standing 0 differing; "
          f"replay {r_on['replayed']}; aliases dropped: not_held "
          f"{r_on['replayed']['not_held']} -> {dropped['not_held']}",
          flush=True)


def main():
    tether._AGENT_SEED = False    # one temperament, so the ON and OFF lives are the same lives
    assert lineage._SAVE_DEDUP and lineage._MEMORY_STORE, "the arms must start ON"
    tmp = Path(tempfile.mkdtemp(prefix="savededup_"))
    row, k = two_step(tmp)
    missing_and_mustfail(row, k)
    on_off(tmp)
    print("save_dedup: OK", flush=True)


if __name__ == "__main__":
    main()
