"""K1, ASK BY KIND (TETHER_DELTA_KIND / TETHER_MOLECULES / TETHER_ATTR_INDEX; the reviewer
2026-10-17 20:25, 20:28).

  K     a lineage crossing (the reviewer 2026-10-20 22:20: a PLANTED meeting, never a trajectory):
        process 1 plays the fake ARC game (12 actions) and writes; (a) process 2 loads, its own
        stores emptied, and is asked under the delta kind process 1 OFFERED most: T1 lists exactly
        the carried entries under that kind, first, and today's lit entry after them; (b) process 2
        holds every carried row (known_dk, known_off) and some lookup of its own run lists a T1.
        MF-K-CUT: the same ask on an empty lineage lists no T1. MF-K: TETHER_DELTA_KIND=0 -- no T1
  R     the same move mirrored: a landing under (MOTION, +, 1) is listed in T1c, ahead of T3, for a
        lookup under (MOTION, -, 1). MF-R: T1a and T1b alone do not list it
  OLD   a carried landing with no delta kind, of this object kind, sits in T2 after T1
  S1    (the reviewer 20:43, 21:03) an entry that LANDED and was never OFFERED is outside the probe
        (T1a-c): not lit now, it sits in T1d AFTER T3; lit now, it stays in T3. MF-S1: the same
        entry once offered under the exact kind is in T1a
  M     a lookup whose lit entries are a molecule's operands lists that molecule in T4, and the
        library compiles candidates for it. MF-M: TETHER_MOLECULES off -- not listed
  C     the described readings' clusters list by_cluster entries in T5 after T3, atoms before
        molecules; with the step's budget spent the walk stops at T4 / T5, counts them not asked and
        does not memoise. MF-C: TETHER_ATTR_INDEX off -- none; a changed hash -- none, and why
  S     on the fake, a T1 offer defers T2-T5 (the count shown). MF-S: the same slot asked again
        under the same delta kind is not deferred again
  P     the price rule: A, the @run alphabet and the code's Kraft sum at every step are identical
        with TETHER_MOLECULES on and off
  E     (run apart) all three arms off: the fake ledger is byte-identical to 83d67f7's

    python test_k1.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))


def carried(d: str) -> list:
    """The generation files in `d` that carry kinds_landed_dk, read through lineage's own reader
    (lineage_store.file_bytes): since d5c1b12 a save is a zlib stream, and reading it as text
    failed on every run (the reviewer 2026-10-20 21:58)."""
    from pathlib import Path

    import lineage_store as ls
    out = []
    for f in sorted(Path(d).iterdir()):
        if f.suffix == ".json":
            raw = ls.file_bytes(f)
            if b"kinds_landed_dk" in raw:
                out.append(json.loads(raw))
    return out

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
import arc_holdout, lineage, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
mode, d = sys.argv[1], sys.argv[2]
ask = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
led = os.path.join(tempfile.mkdtemp(), "k.jsonl")
env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", led_path=led,
                               lineage_dir=d if d != "-" else None)
out = {"alphabet": ag.gamma.alphabet, "kraft": [], "units": []}
for i in range({"p2": 3, "p2k": 1}.get(mode, 12)):
    env.observe()
    ag.step()
    out["kraft"].append(round(ag.gamma.code().kraft(), 12))
    out["units"].append(len(ag.gamma.units_held()))
    if env.terminal():
        break
rows = [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()]
out["tiers"] = [[r["slot"], r["detail"]["dk"], r["detail"]["listed"], r["detail"]["deferred"]]
                for r in rows if r["event"] == "lookup_tiers"]
out["run_alphabet"] = next(r["detail"].get("alphabet") for r in rows
                           if r["slot"] == "@run" and r["event"] == "arms")
if mode == "p1":
    ag.end_run("cap")
    lineage.write(d, ag, "fake")
    out["dk_rows"] = len(ag._kind_landed_dk)
    from test_k1 import carried
    gen = carried(d)
    out["dk_carried"] = sum(len(g.get("kinds_landed_dk", ())) for g in gen)
    out["dk_bytes"] = sum(len(json.dumps(g.get("kinds_landed_dk", ()))) for g in gen)
    out["dks"] = sorted({json.dumps(list(k[0])) for k in ag._kind_landed_dk})
    out["off_rows"] = len(ag._kind_offered_dk)
    out["ep_rows"] = sum(len(g.get("episodes", ())) for g in gen)
    out["ep_dk"] = sum(1 for g in gen for e in g.get("episodes", ()) if "dk" in e)
    out["ep_bytes"] = sum(len(json.dumps(g.get("episodes", ()))) for g in gen)
    out["off_bytes"] = sum(len(json.dumps(g.get("kinds_offered_dk", ()))) for g in gen)
    out["off_carried"] = sum(len(g.get("kinds_offered_dk", ())) for g in gen)
    lib = tether._library()
    top = sorted(((m, d_, k, ko) for (d_, k, ko), m in ag._kind_offered_dk.items()
                  if lib.get(k) is not None), key=lambda r: (-r[0], json.dumps(r[1:])))
    out["ask"] = [list(top[0][1]), list(top[0][3])] if top else None
if mode in ("p2", "p2k"):
    out["known_dk"] = len(ag._kind_known_dk)
    out["known_off"] = len(ag._kind_known_off)
if mode == "p2k":
    # the planted meeting: only the carry can feed T1 (this run's own stores emptied)
    from collections import Counter
    lib = tether._library()
    ag._kind_offered_dk, ag._kind_landed_dk = Counter(), Counter()
    dk, ko = tuple(ask[0]), tuple(ask[1])
    owners = sorted(set(env.slot_owner().values()))
    mine = next((o for o in owners if ag._kind(o) == ko), owners[0])
    carried_k = {k for (d_, k, _t) in ag._kind_known_off if d_ == dk and lib.get(k) is not None}
    lit_k = next(k for k in sorted(lib.seed) if k not in carried_k)
    res, n = ag._tiers(lib, [(lit_k, 1.0)], dk, mine, {}, {})
    order = [k for k, _w in res]
    out["planted"] = {"dk": list(dk), "rung": "a" if ag._kind(mine) == ko else "b", "n": n,
                      "head": order[:n.get("T1a", 0) + n.get("T1b", 0)],
                      "carried": sorted(carried_k), "lit_at": order.index(lit_k)}
print("RESULT", json.dumps(out))
'''


def child(mode: str, d: str = "-", arms: dict | None = None, ask: list | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(arms or {})})
    extra = [json.dumps(ask)] if ask is not None else []
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, mode, d, *extra], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    line = next(x for x in p.stdout.splitlines() if x.startswith("RESULT "))
    return json.loads(line[len("RESULT "):])


def t1(listed: dict) -> int:
    return sum(listed.get(t, 0) for t in ("T1a", "T1b", "T1c"))


def in_process() -> None:
    sys.path.insert(0, HERE)
    from collections import Counter

    import arc_holdout
    import inherited
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    lib = tether._library()
    mine = sorted(set(env.slot_owner().values()))[0]
    ko = ag._kind(mine)
    keys = [k for k in lib.seed if not lib.seed[k].get("ingredients")][:5]
    k_mirror, k_t3, k_old, k_lo1, k_lo2 = keys
    ag._kind_landed_dk = Counter({(("MOTION", "+", 1), k_mirror, ko): 2})
    ag._kind_offered_dk = Counter({(("MOTION", "+", 1), k_mirror, ko): 2})
    out, n = ag._tiers(lib, [(k_t3, 1.0)], ("MOTION", "-", 1), mine, {}, {})
    order = [k for k, _w in out]
    assert n["T1c"] == 1 and order.index(k_mirror) < order.index(k_t3), (n, order[:3])   # R
    assert n["T1a"] == n["T1b"] == 0, n                                                     # MF-R
    print("R a landing under (MOTION, +, 1) is listed in T1c, ahead of T3, for (MOTION, -, 1);"
          " MF-R T1a and T1b list nothing")
    ag._kind_known = {(k_old, "STATE", ko, ko)}
    out, n = ag._tiers(lib, [(k_t3, 1.0)], ("MOTION", "-", 1), mine, {}, {})
    order = [k for k, _w in out]
    assert n["T2"] == 1 and order.index(k_mirror) < order.index(k_old) < order.index(k_t3), (
        n, order[:4])                                                                       # OLD
    print("OLD a carried landing with no delta kind sits in T2, after T1, before T3")
    # OLD + T1d, the seam that crashed (the reviewer 2026-10-21 03:05): T2 held AND two landed-only
    # entries, their recency opposite to their names, so T1d must order by the recency dict
    lo_a, lo_b = sorted((k_lo1, k_lo2))
    ag._kind_landed_dk[(("MOTION", "-", 1), lo_a, ko)] = 1
    ag._kind_landed_dk[(("MOTION", "-", 1), lo_b, ko)] = 1
    ag._kdk_last[(("MOTION", "-", 1), lo_a, ko)] = ("fake", 0, 0, 1)
    ag._kdk_last[(("MOTION", "-", 1), lo_b, ko)] = ("fake", 0, 0, 2)
    out, n = ag._tiers(lib, [(k_t3, 1.0)], ("MOTION", "-", 1), mine, {}, {})
    order = [k for k, _w in out]
    assert n["T2"] == 1 and n["T1d"] == 2, n                                               # OLD+T1d
    if tether._CONSOLIDATE:
        assert order.index(lo_b) < order.index(lo_a), (lo_a, lo_b, order)
    print("OLD+T1d T2 and T1d both held: listed, T1d ordered by recency (the later landing first)")
    for k_ in (lo_a, lo_b):
        del ag._kind_landed_dk[(("MOTION", "-", 1), k_, ko)]
        del ag._kdk_last[(("MOTION", "-", 1), k_, ko)]
    ag._kind_known = set()
    ag._kind_landed_dk[(("MOTION", "-", 1), k_old, ko)] = 3
    out, n = ag._tiers(lib, [(k_t3, 1.0)], ("MOTION", "-", 1), mine, {}, {})
    order = [k for k, _w in out]
    probe = order[:n["T1a"] + n["T1b"] + n["T1c"]]
    assert n["T1d"] == 1 and k_old not in probe and order.index(k_old) > order.index(k_t3), (
        n, order[:4])                                                                       # S1
    out, n = ag._tiers(lib, [(k_t3, 1.0), (k_old, 1.0)], ("MOTION", "-", 1), mine, {}, {})
    assert n["T1d"] == 0 and n["T3"] == 2, n
    ag._kind_offered_dk[(("MOTION", "-", 1), k_old, ko)] = 1
    out, n = ag._tiers(lib, [(k_t3, 1.0)], ("MOTION", "-", 1), mine, {}, {})
    assert [k for k, _w in out][0] == k_old and n["T1a"] == 1 and n["T1d"] == 0, n          # MF-S1
    print("S1 a landed, never offered entry is outside the probe: not lit now, T1d after T3; lit "
          "now, T3; MF-S1 once offered under the exact kind it is T1a")
    ag._kind_landed_dk, ag._kind_offered_dk = Counter(), Counter()
    mol = next(k for k, e in lib.seed.items() if e.get("ingredients") and e.get("run")
               and all(lib.get(o["ref"]) for o in e["run"]["operands"]))
    ops = [o["ref"] for o in lib.get(mol)["run"]["operands"]]
    out, n = ag._tiers(lib, [(o, 1.0) for o in ops], None, mine, {}, {})
    assert mol in [k for k, _w in out][n["T3"]:n["T3"] + n["T4"]], (mol, n)                  # M
    cands = sum(len(lib.view(mol, r)) for r in tether.reach.SINGLE)
    assert cands > 0, mol
    print(f"M the operands of {mol} list it in T4 ({n['T4']} molecules there); the library has "
          f"{cands} candidates for it in the single roles")
    was = tether._MOLECULES
    tether._MOLECULES = False
    try:
        out, n = ag._tiers(lib, [(o, 1.0) for o in ops], None, mine, {}, {})
        assert mol not in [k for k, _w in out] and "T4" not in n, n                         # MF-M
    finally:
        tether._MOLECULES = was
    print("MF-M TETHER_MOLECULES off: not listed")
    slot = next(s for s, a in env.attribute_of().items() if a == "row")
    att = env.attribute_of()
    out, n = ag._tiers(lib, [(k_t3, 1.0)], None, mine, {slot: "POSITION"}, att)
    t5 = [k for k, _w in out][n["T3"] + n.get("T4", 0):]
    bc, why = inherited.by_cluster()
    assert why is None and t5 and set(t5) <= set(bc["POSITION"]), (why, n)                 # C
    mol5 = [bool(lib.get(k).get("ingredients")) for k in t5]
    assert mol5 == sorted(mol5), "C: a molecule before an atom in T5"
    print(f"C T5 lists {len(t5)} POSITION-filed entries after T3, atoms first "
          f"({mol5.count(False)} atoms, {mol5.count(True)} molecules)")
    late = frozenset(t5)
    ag._spent, ag._late, ag._k1_trunc = tether.STEP_BUDGET, (0, 0), False
    ag._index_reach(lib, out, slot, mine, (), late=late)
    assert ag._k1_trunc and ag._late == (0, len(t5)), (ag._k1_trunc, ag._late)
    print("C the step's budget spent: the walk stops at T4 / T5,", ag._late[1],
          "counted not asked, the index marked truncated (not memoised)")
    ag._spent = 0
    was = tether._ATTR_INDEX
    tether._ATTR_INDEX = False
    try:
        out, n = ag._tiers(lib, [(k_t3, 1.0)], None, mine, {slot: "POSITION"}, att)
        assert "T5" not in n, n                                                             # MF-C
    finally:
        tether._ATTR_INDEX = was
    sha = inherited.INDEX_SHA
    inherited.INDEX_SHA = "0" * 64
    inherited.by_cluster.cache_clear()
    try:
        out, n = ag._tiers(lib, [(k_t3, 1.0)], None, mine, {slot: "POSITION"}, att)
        assert n["T5"] == 0 and inherited.by_cluster()[1] == "sha256 mismatch", n
    finally:
        inherited.INDEX_SHA = sha
        inherited.by_cluster.cache_clear()
    print("MF-C arm off: no T5; a changed hash: T5 empty, why 'sha256 mismatch'")


def main() -> int:
    import zlib
    from pathlib import Path
    # the reader can still fail (the reviewer 21:58): a planted compressed save WITHOUT
    # kinds_landed_dk carries nothing, so the pre-check below would be red; one with it is read
    plant = tempfile.mkdtemp()
    Path(plant, "gen_planted.json").write_bytes(
        zlib.compress(json.dumps({"episodes": []}).encode()))
    assert carried(plant) == [], carried(plant)
    Path(plant, "gen_with.json").write_bytes(
        zlib.compress(json.dumps({"kinds_landed_dk": [[["x"], "e", "k"]]}).encode()))
    assert [len(g["kinds_landed_dk"]) for g in carried(plant)] == [1], carried(plant)
    print("MF-READ a compressed save without kinds_landed_dk carries 0; with it, 1")
    in_process()
    d = tempfile.mkdtemp()
    p1 = child("p1", d)
    assert p1["dk_rows"] and p1["dk_carried"] == p1["dk_rows"], p1                          # pre
    assert p1["ask"] and p1["off_rows"] and p1["off_carried"] == p1["off_rows"], p1         # pre
    k2 = child("p2k", d, ask=p1["ask"])["planted"]
    nt1 = k2["n"].get("T1a", 0) + k2["n"].get("T1b", 0)
    assert nt1 > 0 and set(k2["head"]) == set(k2["carried"]), k2                            # K (a)
    assert k2["lit_at"] >= t1(k2["n"]), k2
    print(f"K (a) asked under {k2['dk']} (process 1's most offered kind), rung T1{k2['rung']}: "
          f"T1 lists the {nt1} carried entries first ({k2['n']}), today's lit entry at "
          f"{k2['lit_at']}")
    p2 = child("p2", d)
    assert (p2["known_dk"], p2["known_off"]) == (p1["dk_rows"], p1["off_rows"]), (p2, p1)    # K (b)
    reach = [r for r in p2["tiers"] if t1(r[2]) > 0]
    assert reach, p2["tiers"][:3]
    print(f"K (b) process 1's index: {p1['dk_rows']} (delta kind, entry, target kind) rows, "
          f"carried as {p1['dk_bytes']:,} bytes, and {p1['off_rows']} offered rows; its 7l "
          f"episodes "
          f"{p1['ep_rows']} rows ({p1['ep_dk']} with dk), {p1['ep_bytes']:,} bytes; process 2 "
          f"holds {p2['known_dk']} and {p2['known_off']}, and {len(reach)} of its "
          f"{len(p2['tiers'])} lookups list a T1")
    cut = child("p2k", tempfile.mkdtemp(), ask=p1["ask"])["planted"]
    assert cut["n"].get("T1a", 0) + cut["n"].get("T1b", 0) == 0 and not cut["head"], cut  # MF
    print(f"MF-K-CUT the same ask on an empty lineage: no T1 ({cut['n']})")
    q2 = child("p2", tempfile.mkdtemp(), {"TETHER_DELTA_KIND": "0"})
    assert all("T1a" not in r[2] for r in q2["tiers"]), q2["tiers"][:2]                   # MF-K
    print("MF-K TETHER_DELTA_KIND=0: no lookup lists a T1")
    tl = p1["tiers"]
    mean = {t: round(sum(r[2].get(t, 0) for r in tl) / len(tl), 1)
            for t in ("T1a", "T1b", "T1c", "T1d", "T2", "T3", "T4", "T5")}
    probe = round(sum(t1(r[2]) for r in tl) / len(tl), 1)
    print(f"READ {len(tl)} lookups; mean listed {mean}; probe (T1a-c) {probe} beside T3 "
          f"{mean['T3']}; deferred {sum(1 for r in tl if r[3])} of {len(tl)}; offered store "
          f"{p1['off_rows']} rows, {p1['off_bytes']:,} bytes carried")
    defer = [i for i, r in enumerate(p1["tiers"]) if r[3]]
    assert defer, "S: no lookup deferred on the fake"                                       # S
    again = []
    for i in defer:
        nxt = next((r for r in p1["tiers"][i + 1:] if r[0] == p1["tiers"][i][0]
                    and r[1] == p1["tiers"][i][1]), None)
        if nxt is not None:
            again.append(nxt[3])
    assert again and not any(again), (defer, again)                                         # MF-S
    print(f"S {len(defer)} of {len(p1['tiers'])} lookups deferred (e.g. {p1['tiers'][defer[0]][3]}"
          f" entries); MF-S the {len(again)} re-asks of a deferred slot under the same delta kind "
          "walk everything")
    on, off = child("p", "-"), child("p", "-", {"TETHER_MOLECULES": "0"})
    assert (on["alphabet"], on["run_alphabet"], on["kraft"]) == (
        off["alphabet"], off["run_alphabet"], off["kraft"]), (on["kraft"], off["kraft"])     # P
    print(f"P A = {on['alphabet']}, @run alphabet {on['run_alphabet']}, Kraft {set(on['kraft'])} "
          "at every step, identical with TETHER_MOLECULES on and off")
    print("k1: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
