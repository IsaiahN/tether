"""K1, ASK BY KIND (TETHER_DELTA_KIND / TETHER_MOLECULES / TETHER_ATTR_INDEX; the reviewer
2026-10-17 20:25, 20:28).

  K     a lineage crossing: process 1 plays the fake ARC game (12 actions, C-seed-X) and writes;
        process 2 loads, and its first lookup whose delta kind process 1 landed lists those entries
        in T1 before any landing of its own. MF-K: TETHER_DELTA_KIND=0 -- no T1 at all
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

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
import arc_holdout, lineage, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
mode, d = sys.argv[1], sys.argv[2]
led = os.path.join(tempfile.mkdtemp(), "k.jsonl")
env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", led_path=led,
                               lineage_dir=d if d != "-" else None)
out = {"alphabet": ag.gamma.alphabet, "kraft": [], "units": []}
for i in range(12 if mode != "p2" else 3):
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
    gen = [json.load(open(os.path.join(d, f), encoding="utf-8")) for f in os.listdir(d)
           if f.endswith(".json") and "kinds_landed_dk" in open(os.path.join(d, f),
                                                                 encoding="utf-8").read()]
    out["dk_carried"] = sum(len(g.get("kinds_landed_dk", ())) for g in gen)
    out["dk_bytes"] = sum(len(json.dumps(g.get("kinds_landed_dk", ()))) for g in gen)
    out["dks"] = sorted({json.dumps(list(k[0])) for k in ag._kind_landed_dk})
    out["off_rows"] = len(ag._kind_offered_dk)
    out["ep_rows"] = sum(len(g.get("episodes", ())) for g in gen)
    out["ep_dk"] = sum(1 for g in gen for e in g.get("episodes", ()) if "dk" in e)
    out["ep_bytes"] = sum(len(json.dumps(g.get("episodes", ()))) for g in gen)
    out["off_bytes"] = sum(len(json.dumps(g.get("kinds_offered_dk", ()))) for g in gen)
if mode == "p2":
    out["known_dk"] = len(ag._kind_known_dk)
print("RESULT", json.dumps(out))
'''


def child(mode: str, d: str = "-", arms: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(arms or {})})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, mode, d], capture_output=True,
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
    keys = [k for k in lib.seed if not lib.seed[k].get("ingredients")][:3]
    k_mirror, k_t3, k_old = keys
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
    in_process()
    d = tempfile.mkdtemp()
    p1 = child("p1", d)
    assert p1["dk_rows"] and p1["dk_carried"] == p1["dk_rows"], p1                          # pre
    p2 = child("p2", d)
    dks = set(p1["dks"])
    first = next((r for r in p2["tiers"] if r[1] is not None and json.dumps(r[1]) in dks), None)
    assert p2["known_dk"] == p1["dk_rows"] and first and t1(first[2]) > 0, (p2["known_dk"], first)
    print(f"K process 1's index: {p1['dk_rows']} (delta kind, entry, target kind) rows, carried "
          f"as {p1['dk_bytes']:,} bytes; its 7l episodes {p1['ep_rows']} rows ({p1['ep_dk']} with "
          f"dk), {p1['ep_bytes']:,} bytes; process 2 loads {p2['known_dk']} and its first lookup "
          f"under {first[1]} lists {t1(first[2])} in T1a-c ({first[2]})")                  # K
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
