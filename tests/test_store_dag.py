"""A2, THE STORE READS A BRANCHED LINEAGE (TETHER_STORE_DAG; the reviewer 2026-11-02 r784): a
root, two branches grown by real gridworld agents in separate folders, a status and a book key each
branch sets differently, and lineage.merge over the tips. ON: a fresh agent's load takes the store
path (no store_refused row), and the store's fold equals the archive's fold row for row, in order
(born, handle, admitted, contested), with the same book, contested book, invented and save count;
the rows are the union of every generation's, a composition held on both branches held twice.
MUST-FAIL: the same lineage with the arm OFF writes store_refused and refolds the archive.

    python tests/test_store_dag.py
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import shutil
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

# r1736 (Isaiah 2026-11-11 02:55: a still board ages nothing): on default seed 0 the newborn's W
# goes flat at cycle 2, its refusals never fade, and the root writes no term: nothing to contest. On
# seed 1, 30 steps, the root and both branches write terms (as test_lineage_merge's fixture)
N = 30
SEED = 1


def _run(d, seed, n):
    env = world.bind(gridworld.family("default", seed))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"), tether.Config(),
                      ledger.Ledger())
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


def _status(parent, born, handle, admitted, book):
    return {"lineage": 1, "parent": parent, "game": "status", "terms": [],
            "status": [{"born": born, "handle": handle, "admitted": admitted}], "evidence": [],
            "vindication_tail": [], "book": book, "invented": {}, "dormant": [],
            "dormant_refused": []}


def _peak_mb() -> float:
    class PMC(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong)] + [
            (n, ctypes.c_size_t) for n in ("PeakWorkingSetSize", "WorkingSetSize",
                                           "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage",
                                           "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage",
                                           "PagefileUsage", "PeakPagefileUsage")]
    if not hasattr(ctypes, "windll"):
        return -1.0
    k32 = ctypes.windll.kernel32
    k32.GetCurrentProcess.restype = ctypes.c_void_p
    gpmi = k32.K32GetProcessMemoryInfo
    gpmi.argtypes = [ctypes.c_void_p, ctypes.POINTER(PMC), ctypes.c_ulong]
    c = PMC()
    c.cb = ctypes.sizeof(PMC)
    assert gpmi(k32.GetCurrentProcess(), ctypes.byref(c), c.cb), "GetProcessMemoryInfo failed"
    assert c.PeakPagefileUsage > 0, "a zero peak is a broken reading"
    return round(c.PeakPagefileUsage / 2**20, 1)


def _fixture(tmp: Path) -> tuple[Path, dict]:
    d, side = tmp / "main", tmp / "side"
    d.mkdir()
    side.mkdir()
    a, _ = _run(d, SEED, N)
    wa = lineage.write(d, a, "default")
    for f in d.glob(f"*{wa['hash']}*"):
        shutil.copy(f, side / f.name)
    b1, _ = _run(d, SEED, N)
    w1 = lineage.write(d, b1, "default")
    b2, _ = _run(side, SEED, N + 5)
    w2 = lineage.write(side, b2, "default")
    for f in side.glob(f"*{w2['hash']}*"):
        shutil.copy(f, d / f.name)
    gens = lineage._read(d)
    touched = {(s["born"], s["handle"]) for g in gens.values() for s in g["status"]}
    root = [r for r in gens[wa["hash"]]["terms"]
            if r.get("handle") and (wa["hash"], r["handle"]) not in touched]
    assert root and w1["hash"] != w2["hash"], ("fixture: nothing to contest", len(root))
    bk = "fixture.dag_probe"
    s1 = _put(d, _status(w1["hash"], wa["hash"], root[0]["handle"], "necessary", {bk: "b1"}))
    s2 = _put(d, _status(w2["hash"], wa["hash"], root[0]["handle"], "promoted", {bk: "b2"}))
    m = lineage.merge(d)
    assert "hash" in m, ("fixture: merge refused", m)
    return d, {"root": wa["hash"], "b1": w1["hash"], "b2": w2["hash"], "s1": s1, "s2": s2,
               "merge": m["hash"], "row": (wa["hash"], root[0]["handle"]), "bk": bk}


def _refused(rep_rows) -> list:
    return [r for r in rep_rows if r["event"] == "store_refused"]


def _gen(parent, terms=(), status=(), book=None, parents=None):
    g = {"lineage": 1, "game": "dag", "terms": list(terms), "status": list(status),
         "evidence": [], "vindication_tail": [], "book": book or {}, "invented": {},
         "dormant": [], "dormant_refused": []}
    if parents:
        g.update(parents=sorted(parents), merge=True)
    else:
        g["parent"] = parent
    return g


def _same(d: Path) -> tuple[int, int]:
    """The store, caught up, against the archive fold: rows in order, book, contested book."""
    con = lineage_store.open_store(d)
    try:
        lineage_store.catch_up(con, d)
        fs = json.loads(con.execute("SELECT v FROM blob WHERE k='fold'").fetchone()[0])
    finally:
        con.close()
    _h, fa = lineage.head(d)
    a = [(r["born"], r["handle"], r.get("admitted"), r.get("contested")) for r in fa["terms"]]
    s = [(r["born"], r["handle"], r.get("admitted"), r.get("contested"))
         for r in fs["rows"].values()]
    assert s == a, ("store != archive", len(s), len(a),
                    next(((x, y) for x, y in zip(s, a, strict=False) if x != y), None))
    assert fs["book"] == fa["book"] and fs.get("contested_book") == fa.get("contested_book"), (
        "book", fs["book"], fa["book"])
    return len(s), sum(1 for x in s if x[3])


def _synthetic(tmp: Path) -> dict:
    """Hand-written saves: the store merges one branch linearly, the other branch and the merge
    then arrive (the rebuild), and a child of the merge settles a contested row (linear again)."""
    d = tmp / "synthetic"
    d.mkdir()

    def row(i, tag):
        return {"handle": f"{tag}{i}", "atoms": [f"a{i % 7}"], "admitted": "candidate"}

    r = _put(d, _gen(None, [row(i, "h") for i in range(30)], book={"k0": "r"}))
    a1 = _put(d, _gen(r, [row(i, "a") for i in range(10)],
                      [{"born": r, "handle": "h1", "admitted": "necessary"},
                       {"born": r, "handle": "h2", "admitted": "necessary"}], {"k1": "a"}))
    a2 = _put(d, _gen(a1, status=[{"born": r, "handle": "h3", "admitted": "promoted"}]))
    stage1 = _same(d)                                     # a linear store: R, A1, A2
    b1 = _put(d, _gen(r, [row(i, "b") for i in range(10)],
                      [{"born": r, "handle": "h1", "admitted": "promoted"},
                       {"born": r, "handle": "h4", "admitted": "necessary"}], {"k1": "b"}))
    m = lineage.merge(d)["hash"]
    stage2 = _same(d)                                     # B1 and the merge: the rebuild
    c = _put(d, _gen(m, status=[{"born": r, "handle": "h1", "admitted": "necessary"}],
                     book={"k1": "c"}))
    stage3 = _same(d)                                     # a child of the merge: linear again
    assert stage2[1] >= 1 and stage3[0] == stage2[0], ("contested rows", stage2, stage3)
    return {"rows": stage3[0], "contested_at_merge": stage2[1], "stage1": stage1[0],
            "ids": (r, a1, a2, b1, m, c)}


def _tables(d: Path) -> dict:
    con = lineage_store.open_store(d)
    try:
        out = {t: sorted(map(repr, con.execute(f"SELECT * FROM {t}")))
               for t in (*lineage_store._TABLES, "meta")}
    finally:
        con.close()
    return out


def _hash(g: dict) -> str:
    return hashlib.sha256(json.dumps(g, sort_keys=True, indent=1).encode("utf-8")).hexdigest()[:16]


def _continue_case(tmp: Path, name: str, where: str, contest: bool, seed: bool) -> dict:
    """A2c (r792): a linear store R, A1..A3; then a branch B off R, its hash picked so fold's
    _topo puts it AFTER the chain or INSIDE it, and the merge. The store caught up through
    catch_up (continue when it may) against a copy caught up with the continue arm OFF (the full
    rebuild), table by table; and what each part of the rule prevents: `seed`, the continue forced
    past the topo check (its FoldState seeded from the chain); else the seed removed, i.e. the
    linear body (_fold_apply, a plain update) over the same order, its fold against the store's."""
    d = tmp / name
    d.mkdir()

    def row(i, tag):
        return {"handle": f"{tag}{i}", "atoms": [f"a{i % 5}"], "admitted": "candidate"}
    r = _put(d, _gen(None, [row(i, "h") for i in range(12)], book={"k0": "r"}))
    a1 = _put(d, _gen(r, [row(i, "a") for i in range(4)],
                      [{"born": r, "handle": "h1", "admitted": "necessary"}], {"k1": "a"}))
    a2 = _put(d, _gen(a1, status=[{"born": a1, "handle": "a2", "admitted": "promoted"}]))
    a3 = _put(d, _gen(a2, [row(i, "c") for i in range(3)], book={"k2": "a"}))
    con = lineage_store.open_store(d)
    try:
        lineage_store.catch_up(con, d)
    finally:
        con.close()
    b = _gen(r, [row(i, "b") for i in range(4)],
             [{"born": r, "handle": "h1" if contest else "h5", "admitted": "promoted"}],
             {"k1" if contest else "k3": "b"})
    ok = ((lambda h: h > max(a1, a2, a3)) if where == "after" else (lambda h: h < a1))
    for i in range(10_000):
        b["game"] = f"dag{i}"
        if ok(_hash(b)):
            break
    assert ok(_put(d, b)), ("fixture: no hash in place", where)
    m = lineage.merge(d)["hash"]
    d_off, d_forced = tmp / f"{name}_rebuild", tmp / f"{name}_forced"
    for x in (d_off, d_forced):
        x.mkdir()
        for f in d.glob(f"{lineage.PREFIX}*.json"):
            shutil.copy(f, x / f.name)
    con = lineage_store.open_store(d)
    try:
        paths = [x.get("dag") for x in lineage_store.catch_up(con, d)]
    finally:
        con.close()
    lineage_store._CONTINUE = False
    try:
        for x in (d_off, d_forced):
            con = lineage_store.open_store(x)
            try:
                if x == d_off:
                    lineage_store.catch_up(con, x)
                    continue
                # the forced continue: the chain linear, then the new saves in _topo order
                gx, state = lineage._read(x), lineage.FoldState(lists=False)
                for h in (r, a1, a2, a3):
                    lineage_store.merge_save(con, x, h, gx[h])
                    state.step(h, gx[h])
                for h in [h for h in lineage._topo(gx) if h not in (r, a1, a2, a3)]:
                    lineage_store.merge_save(con, x, h, gx[h], state)
            finally:
                con.close()
    finally:
        lineage_store._CONTINUE = True
    order = lineage._topo(lineage._read(d))
    _n, contested = _same(d)
    forced = _tables(d_forced) == _tables(d_off)
    if not seed:
        gd, plain = lineage._read(d), {}
        for h in order:
            if not gd[h].get("merge"):
                lineage_store._fold_apply(plain, h, gd[h])
        con = lineage_store.open_store(d)
        try:
            fs = json.loads(con.execute("SELECT v FROM blob WHERE k='fold'").fetchone()[0])
        finally:
            con.close()
        forced = (plain["rows"], plain["book"]) == (fs["rows"], fs["book"])
    return {"paths": paths, "b_at": order.index(_hash(b)), "of": len(order), "merge": m,
            "contested": contested,
            "equal": _tables(d) == _tables(d_off),
            "forced_equal": forced}


def _continue_cases(tmp: Path) -> dict:
    after = _continue_case(tmp, "c_after", "after", contest=False, seed=True)
    assert after["paths"] == ["continue", "continue"], ("(ii) the exact case did not continue",
                                                        after)
    assert after["equal"], ("(ii) continue != the full rebuild, table by table", after)
    inside = _continue_case(tmp, "c_inside", "inside", contest=False, seed=True)
    assert set(inside["paths"]) == {"rebuild"}, ("(i) a save inside the chain was not refused",
                                                 inside)
    assert inside["equal"] and not inside["forced_equal"], (
        "(i) the refusal is load-bearing: forced, the continue differs from the rebuild", inside)
    contest = _continue_case(tmp, "c_contest", "after", contest=True, seed=False)
    assert contest["paths"] == ["continue", "continue"], ("(iii) a contest did not continue",
                                                          contest)
    assert contest["equal"] and contest["contested"] >= 1, (
        "(iii) continue over a contest != the full rebuild, table by table", contest)
    assert not contest["forced_equal"], ("(iii) the seed is load-bearing: removed, it differs",
                                         contest)
    return {"after": after, "inside": inside, "contest": contest}


def _fold_rules() -> dict:
    """fold's merge rules (the reviewer 2026-11-02 r800 2): a root R, branches A and B off it, and
    their merge, folded in _topo order. MF-F1 agreeing statuses and MF-F2 a running counter were
    contests before (the row fell back to "promoted", the counter to 100); MF-F3..F5 must stay."""
    def run(ra, rb, root=None, field="status"):
        r = _gen(None, [{"handle": "h1", "atoms": ["a"], "admitted": "promoted"}])
        r[field if field != "status" else "book"] = root or {}
        a, b = _gen("R"), _gen("R")
        if field == "status":
            a["status"] = [{"born": "R", "handle": "h1", "admitted": ra}]
            b["status"] = [{"born": "R", "handle": "h1", "admitted": rb}]
        else:
            a[field], b[field] = ra, rb
        gens = {"R": r, "A": a, "B": b, "M": _gen(None, parents=["A", "B"])}
        return lineage.fold([(h, gens[h]) for h in lineage._topo(gens)])
    f1 = run("accepted", "accepted")
    row = f1["terms"][0]
    assert row["admitted"] == "accepted" and "contested" not in row, ("MF-F1 agreement", row)
    f2 = run({"c": 130}, {"c": 115}, {"c": 100}, "book")
    assert f2["book"]["c"] == 145 and "contested_book" not in f2, ("MF-F2 counter", f2["book"])
    f3 = run("accepted", "necessary")
    row = f3["terms"][0]
    assert row["admitted"] == "promoted" and {x["admitted"] for x in row["contested"]} == {
        "accepted", "necessary"}, ("MF-F3 a real contest", row)
    f4 = run({"c": 130}, {"c": 90}, {"c": 100}, "book")
    assert f4["book"]["c"] == 100 and len(f4["contested_book"]["c"]) == 2, ("MF-F4", f4["book"])
    # MF-F6 (r801 4): a counter both branches created after the split (no pre-split value) sums
    f6 = run({"c": 7}, {"c": 5}, {}, "book")
    assert f6["book"].get("c") == 12 and "contested_book" not in f6, ("MF-F6 absent pre",
                                                                     f6["book"])
    f5 = run({"x": {"r": 1}, "y": 7}, {"x": {"r": 2}, "y": 9}, {"y": 3}, "invented")
    assert "x" not in f5["invented"] and f5["invented"]["y"] == 3, ("MF-F5 never summed", f5)
    assert set(f5["contested_invented"]) == {"x", "y"}, ("MF-F5 contested", f5)
    # MF-F7 (r881 4 (i); the 2026-11-03 re-merge, try_first_owed 746 for 3232): three heads forking
    # BELOW a prior merge M1 whose counter (145) no generation wrote. Each wrote its running total
    # from the loaded 145; the sum is 145 + 5 + 10 + 3. RED: p0 is the last raw write (115), and
    # each head beyond the first adds the gap again (223)
    g7 = {"R": _gen(None, book={"c": 100}), "A": _gen("R", book={"c": 130}),
          "B": _gen("R", book={"c": 115}), "M1": _gen(None, parents=["A", "B"]),
          "X": _gen("M1", book={"c": 150}), "Y": _gen("M1", book={"c": 155}),
          "Z": _gen("M1", book={"c": 148}), "M2": _gen(None, parents=["X", "Y", "Z"])}
    f7 = lineage.fold([(h, g7[h]) for h in lineage._topo(g7)])
    assert f7["book"]["c"] == 163 and "contested_book" not in f7, ("MF-F7 fork below a merge",
                                                                   f7["book"])
    # MF-F8 (r881 4 (ii), r882 3): at a merge of fold_rule 2, two game series that each moved a
    # counter
    # 64 -> 66 are two increments, not one agreement (68; RED 66), and a head that did not move
    # adds 0 (27 / 28 / 28 -> 29)
    def equal_moves(books, root, rule):
        m = _gen(None, parents=[chr(65 + i) for i in range(len(books))])
        if rule:
            m["fold_rule"] = rule
        gs = {"R": _gen(None, book=root), "M": m,
              **{chr(65 + i): _gen("R", book=b) for i, b in enumerate(books)}}
        return lineage.fold([(h, gs[h]) for h in lineage._topo(gs)])["book"]["c"]
    f8 = [equal_moves([{"c": 66}, {"c": 66}], {"c": 64}, lineage.FOLD_RULE),
          equal_moves([{"c": 28}, {"c": 28}, {"c": 27}], {"c": 27}, lineage.FOLD_RULE)]
    assert f8 == [68, 29], ("MF-F8 equal moves sum at a fold_rule 2 merge", f8)
    # MF-F9 (r882 3): a merge written before, with no fold_rule, folds exactly as it did (66), so
    # central's past fold is unchanged
    f9 = equal_moves([{"c": 66}, {"c": 66}], {"c": 64}, None)
    assert f9 == 66, ("MF-F9 a merge without fold_rule folds as before", f9)
    return {"F1": row and f1["terms"][0]["admitted"], "F2": f2["book"]["c"], "F6": f6["book"]["c"],
            "F4": f4["book"]["c"], "F5": sorted(f5["contested_invented"]), "F7": f7["book"]["c"],
            "F8": f8, "F9": f9}


def _graft_cases(tmp: Path) -> dict:
    """lineage.graft (the reviewer 2026-11-02 r802): a main line R -> A1 in d (A1 sets h1
    "refuted", counter c 100 -> 160), a branch X off R in its own folder (h1 and h2 "accepted",
    c 130, an idx_ file beside it), grafted onto A1. MF-G1 the counter reads 190, not X's 130;
    MF-G2 h1 keeps "refuted" with X's "accepted" in the record, h2 carries "accepted"; MF-G3 the
    store appends it (no rebuild, no refusal); MF-G4 that store equals one rebuilt from nothing,
    table by table; MF-G5 X's folder is byte-identical after."""
    d, src = tmp / "graft", tmp / "graft_src"
    d.mkdir()
    src.mkdir()
    r = _put(d, _gen(None, [{"handle": f"h{i}", "atoms": ["a"], "admitted": "candidate"}
                            for i in range(3)], book={"c": 100}))
    a1 = _put(d, _gen(r, status=[{"born": r, "handle": "h1", "admitted": "refuted"}],
                      book={"c": 160}))
    x = _put(src, _gen(r, [{"handle": "x0", "atoms": ["b"], "admitted": "candidate"}],
                       [{"born": r, "handle": "h1", "admitted": "accepted"},
                        {"born": r, "handle": "h2", "admitted": "accepted"}], {"c": 130}))
    idx = json.dumps({"entries": [], "sig_arm": "t", "sig_atoms": [], "sig_names": []}).encode()
    (src / f"{lineage.IDX}{x}_{hashlib.sha256(idx).hexdigest()[:16]}.json").write_bytes(idx)
    con = lineage_store.open_store(d)
    try:
        lineage_store.catch_up(con, d)
    finally:
        con.close()

    def shas(p):
        return {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.iterdir())}
    before = shas(src)
    res = lineage.graft(d, src, x, "test")
    g2 = lineage._read(d)[res["hash"]]
    assert g2["book"]["c"] == 190, ("MF-G1 counter", g2["book"], "X wrote", 130)
    kept = g2["graft"]["kept_tip"]
    assert [s["handle"] for s in g2["status"]] == ["h2"] and kept == [
        {"status": [r, "h1"], "tip": "refuted", "graft": "accepted"}], ("MF-G2", g2["status"], kept)
    assert g2["parent"] == a1 and g2["graft"]["old_parent"] == r, ("graft parents", g2["graft"])
    con = lineage_store.open_store(d)
    try:
        paths = [y.get("dag") for y in lineage_store.catch_up(con, d)]
        fs = json.loads(con.execute("SELECT v FROM blob WHERE k='fold'").fetchone()[0])
    finally:
        con.close()
    assert paths == [None], ("MF-G3 appended linearly, no rebuild", paths)
    adm = {r_["handle"]: r_.get("admitted") for r_ in fs["rows"].values()}
    assert adm["h1"] == "refuted" and adm["h2"] == "accepted" and fs["book"]["c"] == 190, (
        "MF-G3 the store reads the graft", adm, fs["book"])
    d2 = tmp / "graft_rebuilt"
    d2.mkdir()
    for f in d.glob("*_*.json"):
        shutil.copy(f, d2 / f.name)
    con = lineage_store.open_store(d2)
    try:
        lineage_store.catch_up(con, d2)
    finally:
        con.close()
    assert _tables(d) == _tables(d2), "MF-G4 the appended store != one rebuilt from nothing"
    assert shas(src) == before, "MF-G5 the source folder changed"
    assert res["side_files"] == 1 and len(list(d.glob(f"{lineage.IDX}{res['hash']}_*.json"))) == 1
    return {"hash": res["hash"], "counts": res["counts"], "kept": len(kept)}


def main():
    tether._AGENT_SEED = False
    gr = _graft_cases(Path(tempfile.mkdtemp(prefix="store_graft_")))
    print(f"  graft: MF-G1 counter 100 -> main 160 / branch 130 -> 190; MF-G2 h1 keeps 'refuted' "
          f"({gr['kept']} kept_tip), h2 carries 'accepted'; MF-G3 appended linearly; MF-G4 = a "
          f"store rebuilt from nothing, table by table; MF-G5 source byte-identical; counts "
          f"{gr['counts']}", flush=True)
    fr = _fold_rules()
    print(f"  fold rules: MF-F1 agreeing heads -> {fr['F1']!r}, no contest; MF-F2 counter 100 -> "
          f"130 / 115 -> {fr['F2']}; MF-F3 differing statuses -> pre-split + both contested; "
          f"MF-F4 a head below pre -> {fr['F4']}, contested; MF-F5 invented {fr['F5']} contested, "
          f"never summed; MF-F6 absent pre, 7 / 5 -> {fr['F6']}; MF-F7 three heads below a merge "
          f"(145 + 5 + 10 + 3) -> {fr['F7']}; MF-F8 fold_rule 2, equal moves 64 -> 66 / 66 and "
          f"27 -> 28 / 28 / 27 -> {fr['F8']}; MF-F9 no fold_rule, 64 -> 66 / 66 -> {fr['F9']}",
          flush=True)
    cc = _continue_cases(Path(tempfile.mkdtemp(prefix="store_cont_")))
    print("  A2c continue: (ii) B after the chain at {}/{} -> paths {}, equal to the rebuild table "
          "by table; (i) B inside at {}/{} -> REFUSED (paths {}), forced continue differs; "
          "(iii) B contesting a status and a book key -> continue, equal to the rebuild table by "
          "table ({} contested row), and with the seed removed it differs".format(
              cc["after"]["b_at"] + 1, cc["after"]["of"], cc["after"]["paths"],
              cc["inside"]["b_at"] + 1, cc["inside"]["of"], sorted(set(cc["inside"]["paths"])),
              cc["contest"]["contested"]),
          flush=True)
    assert lineage._MEMORY_STORE and getattr(lineage_store, "_DAG", True), "the store arms are ON"
    tmp = Path(tempfile.mkdtemp(prefix="store_dag_"))
    syn = _synthetic(tmp)
    print(f"  synthetic: {syn['stage1']} rows linear, then the second branch + merge -> "
          f"{syn['rows']} rows, {syn['contested_at_merge']} contested at the merge, and a child "
          f"of the merge settling one: store = archive fold at each stage", flush=True)
    d, ids = _fixture(tmp)
    d_off = tmp / "main_off"
    shutil.copytree(d, d_off)
    # ON: the load reads the store, which rebuilds over the merge
    c, rep = _run(d, 0, 0)
    assert rep["parent"] == ids["merge"], ("the load's parent is not the merge", rep.get("parent"))
    ref = _refused(c.led.rows())
    assert not ref, ("ON: the store refused the merged lineage", ref[:1])
    assert "store_merged_at_load" in rep, ("ON: the load did not come from the store", sorted(rep))
    con = lineage_store.open_store(d)
    try:
        fs = json.loads(con.execute("SELECT v FROM blob WHERE k='fold'").fetchone()[0])
        cs = json.loads(con.execute("SELECT v FROM blob WHERE k='counts'").fetchone()[0])
        tip = con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone()[0]
    finally:
        con.close()
    h, fa = lineage.head(d)
    assert tip == h == ids["merge"], ("the store's tip", tip, h)
    a_rows = [(r["born"], r.get("handle"), r.get("admitted"), r.get("contested"))
              for r in fa["terms"]]
    s_rows = [(r["born"], r.get("handle"), r.get("admitted"), r.get("contested"))
              for r in fs["rows"].values()]
    assert s_rows == a_rows, ("the store's rows differ from the archive fold",
                              len(s_rows), len(a_rows),
                              next(((x, y) for x, y in zip(s_rows, a_rows, strict=False)
                                    if x != y), None))
    for k in ("book", "invented"):
        assert fs[k] == fa[k], (k, "differs")
    assert fs.get("contested_book") == fa.get("contested_book"), "contested_book differs"
    assert cs["n_saves"] == len(lineage._read(d)), ("n_saves", cs["n_saves"])
    row = next(r for r in fs["rows"].values() if (r["born"], r.get("handle")) == ids["row"])
    vals = {(x["gen"], x["admitted"]) for x in row.get("contested", [])}
    assert vals == {(ids["s1"], "necessary"), (ids["s2"], "promoted")}, ("contested", row)
    gens = lineage._read(d)
    n_in = sum(len(g["terms"]) for g in gens.values())
    keys = [gamma.Gamma.row_key(r) for r in fa["terms"]]
    twice = len(keys) - len(set(keys))
    assert len(s_rows) == n_in, ("rows are not the union", len(s_rows), n_in)
    peak = _peak_mb()
    # MUST-FAIL: the arm OFF refuses the same lineage and refolds the archive
    lineage_store._DAG = False
    try:
        c2, rep2 = _run(d_off, 0, 0)
    finally:
        lineage_store._DAG = True
    ref2 = _refused(c2.led.rows())
    assert ref2 and "store_merged_at_load" not in rep2, ("must-fail: OFF did not refuse", rep2)
    print(f"test_store_dag: root {ids['root']}, branches {ids['b1']} / {ids['b2']}, merge "
          f"{ids['merge']}; ON the store holds {len(s_rows)} rows = the union of "
          f"{len(gens)} generations' terms ({twice} compositions held more than once), equal to "
          f"the archive fold in order; contested {sorted(vals)}; book contested "
          f"{sorted((x['gen'], x['value']) for x in fs['contested_book'][ids['bk']])}; peak "
          f"commit {peak} MB. OFF: store_refused ({ref2[0]['detail']['reason'][:70]!r})")


if __name__ == "__main__":
    main()
