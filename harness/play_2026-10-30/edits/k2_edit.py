p = "test_k1.py"
s = open(p, encoding="utf-8", newline="").read()
# test_k1.py is LF in git; df76d13 left one stray CR (a hand-wrapped line): drop it
assert s.count("\r") == 1, s.count("\r")
s = s.replace("\r\n", "\n")
nl = "\n"


def rep(old, new):
    global s
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)


rep('''  K     a lineage crossing: process 1 plays the fake ARC game (12 actions, C-seed-X) and writes;
        process 2 loads, and its first lookup whose delta kind process 1 landed lists those entries
        in T1 before any landing of its own. MF-K: TETHER_DELTA_KIND=0 -- no T1 at all
''', '''  K     a lineage crossing (the reviewer 2026-10-20 22:20: a PLANTED meeting, never a trajectory):
        process 1 plays the fake ARC game (12 actions) and writes; (a) process 2 loads, its own
        stores emptied, and is asked under the delta kind process 1 OFFERED most: T1 lists exactly
        the carried entries under that kind, first, and today's lit entry after them; (b) process 2
        holds every carried row (known_dk, known_off) and some lookup of its own run lists a T1.
        MF-K-CUT: the same ask on an empty lineage lists no T1. MF-K: TETHER_DELTA_KIND=0 -- no T1
''')
rep('''mode, d = sys.argv[1], sys.argv[2]
''', '''mode, d = sys.argv[1], sys.argv[2]
ask = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
''')
rep('''for i in range(12 if mode != "p2" else 3):
''', '''for i in range({"p2": 3, "p2k": 1}.get(mode, 12)):
''')
rep('''    out["off_bytes"] = sum(len(json.dumps(g.get("kinds_offered_dk", ()))) for g in gen)
''', '''    out["off_bytes"] = sum(len(json.dumps(g.get("kinds_offered_dk", ()))) for g in gen)
    out["off_carried"] = sum(len(g.get("kinds_offered_dk", ())) for g in gen)
    lib = tether._library()
    top = sorted(((m, d_, k, ko) for (d_, k, ko), m in ag._kind_offered_dk.items()
                  if lib.get(k) is not None), key=lambda r: (-r[0], json.dumps(r[1:])))
    out["ask"] = [list(top[0][1]), list(top[0][3])] if top else None
''')
rep('''if mode == "p2":
    out["known_dk"] = len(ag._kind_known_dk)
''', '''if mode in ("p2", "p2k"):
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
''')
rep('''    p2 = child("p2", d)
    dks = set(p1["dks"])
    first = next((r for r in p2["tiers"] if r[1] is not None and json.dumps(r[1]) in dks), None)
    assert p2["known_dk"] == p1["dk_rows"] and first and t1(first[2]) > 0, (p2["known_dk"], first)
    print(f"K process 1's index: {p1['dk_rows']} (delta kind, entry, target kind) rows, carried "
          f"as {p1['dk_bytes']:,} bytes; its 7l episodes {p1['ep_rows']} rows ({p1['ep_dk']} with "
          f"dk), {p1['ep_bytes']:,} bytes; process 2 loads {p2['known_dk']} and its first lookup "
          f"under {first[1]} lists {t1(first[2])} in T1a-c ({first[2]})")                  # K
''', '''    assert p1["ask"] and p1["off_rows"] and p1["off_carried"] == p1["off_rows"], p1         # pre
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
          f"carried as {p1['dk_bytes']:,} bytes, and {p1['off_rows']} offered rows; its 7l episodes "
          f"{p1['ep_rows']} rows ({p1['ep_dk']} with dk), {p1['ep_bytes']:,} bytes; process 2 "
          f"holds {p2['known_dk']} and {p2['known_off']}, and {len(reach)} of its "
          f"{len(p2['tiers'])} lookups list a T1")
    cut = child("p2k", tempfile.mkdtemp(), ask=p1["ask"])["planted"]
    assert cut["n"].get("T1a", 0) + cut["n"].get("T1b", 0) == 0 and not cut["head"], cut   # MF-K-CUT
    print(f"MF-K-CUT the same ask on an empty lineage: no T1 ({cut['n']})")
''')
rep('''def child(mode: str, d: str = "-", arms: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(arms or {})})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, mode, d], capture_output=True,
''', '''def child(mode: str, d: str = "-", arms: dict | None = None, ask: list | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(arms or {})})
    extra = [json.dumps(ask)] if ask is not None else []
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, mode, d, *extra], capture_output=True,
''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
