"""K1's ALIAS GENERATION (TETHER_KIND_ALIAS; the reviewer 2026-11-03 r886, r887, r902, r903): a
lineage of hand-written saves holding as-seen form codes 11 and 12 of one kind (canonical 10) beside
an untouched 22, then lineage.alias_generation. Game-free, seconds.

MF-K6  the store after the alias generation holds no row under 11 or 12: the rows meet under 10
       with n summed (3 + 4 + the child's 1 = 8), the l_* of the greatest l_seq, total n per table
       unchanged; the kind-keyed counts summed and the action cells joined; a store built save by
       save equals one built from nothing, table by table; the archive read (alias_chain) gives
       the same n and counts as the store.
MF-K7  OFF (a child process, TETHER_KIND_ALIAS=0): the alias generation changes nothing, the store
       equals that of the same saves without it, and alias_chain returns the chain unchanged.
MF-K8  (must-stay) an alias for a code no row holds changes no table and no count.
MF-K10 a map that is not idempotent (11 -> 10 and 10 -> 9) is refused.
MF-K11 a SECOND alias generation re-keys rows already stored under its codes, from before it and
       after the first: total n unchanged, built save by save = built from nothing.
MF-K12 a code already aliased to 10, aliased again to 13, is refused by alias_generation and by
       the store, and the reason names both.

    python tests/test_kind_alias.py
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import lineage  # noqa: E402
import lineage_store  # noqa: E402

PAIRS = [[11, 10, 1], [12, 10, 2], [10, 10, 0]]


def _k(code):
    return ["COLOUR", f"form={code}"]


def _cell(a, tab, code):
    return repr((a, tab, f"('COLOUR', 'form={code}')"))


def _put(d, gen):
    raw = json.dumps(gen, sort_keys=True, indent=1).encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()[:16]
    (Path(d) / f"{lineage.PREFIX}{h}.json").write_bytes(raw)
    return h


def _gen(parent, **f):
    return {"lineage": 1, "parent": parent, "game": "alias", "terms": [], "status": [],
            "evidence": [], "vindication_tail": [], "book": {}, "invented": {}, "dormant": [],
            "dormant_refused": [], **f}


def _root():
    x = ["SHAPE", "form=22"]
    k1, k2, k3 = ["e1", "CAUSE", _k(11), x], ["e1", "CAUSE", _k(12), x], ["e2", "MOVE", _k(10), x]
    return _gen(None, kinds_landed=[k1, k2, k3],
                kinds_landed_n=[[*k1, 3], [*k2, 4], [*k3, 5]],
                kinds_last=[[*k1, "g", 0, 1, 7], [*k2, "g", 0, 2, 9]],
                kinds_landed_dk=[[["d"], "e1", _k(11), 2], [["d"], "e1", _k(12), 1]],
                kinds_dk_last=[[["d"], "e1", _k(12), "g", 0, 2, 9]],
                kinds_offered_dk=[[["d"], "e1", _k(11), 1], [["d"], "e1", _k(12), 6]],
                kind_counts={"s": {"('COLOUR', 'form=11')": 2, "('COLOUR', 'form=12')": 5}},
                cause_kinds={"('COLOUR', 'form=11')|x": 1, "('COLOUR', 'form=12')|x": 2},
                action_kinds={_cell("A1", "delta_kind", 11): [1, 3],
                              _cell("A1", "delta_kind", 12): [2, 4],
                              _cell("A1", "lands_kind", 11): ["a"],
                              _cell("A1", "lands_kind", 12): ["b"]})


def _child(parent, code=12):
    k = ["e1", "CAUSE", _k(code), ["SHAPE", "form=22"]]
    return _gen(parent, kinds_landed=[k], kinds_landed_n=[[*k, 1]],
                kinds_last=[[*k, "g", 1, 3, 11]],
                kind_counts={"s": {f"('COLOUR', 'form={code}')": 1}})


def _alias_gen(parent, pairs):
    """The generation alias_generation writes, by hand (so HEAD, which has no writer, reads it)."""
    return {"lineage": 1, "parent": parent, "game": None, "terms": [], "status": [],
            "evidence": [], "vindication_tail": [], "book": {}, "invented": {}, "dormant": [],
            "dormant_refused": [], "form_aliases": [list(p) for p in sorted(map(tuple, pairs))],
            "alias_rule": 1}


def _catch(d):
    con = lineage_store.open_store(d)
    try:
        return lineage_store.catch_up(con, d)
    finally:
        con.close()


def _decoded(d) -> dict:
    """kind, kind_dk, kind_off, pair and counts with every sym id read back as its text."""
    con = lineage_store.open_store(d)
    try:
        s = dict(con.execute("SELECT id, s FROM sym"))
        out = {
            "kind": sorted((s[e], s[r], s[o], s[x], *v) for e, r, o, x, *v in
                           con.execute("SELECT * FROM kind")),
            "kind_dk": sorted((s[a], s[e], s[t], *v) for a, e, t, *v in
                              con.execute("SELECT * FROM kind_dk")),
            "kind_off": sorted((s[a], s[e], s[t], n) for a, e, t, n in
                               con.execute("SELECT * FROM kind_off")),
            "pair": sorted((s[o], s[x], n, ls) for o, x, n, ls in
                           con.execute("SELECT * FROM pair")),
            "counts": {k: v for k, v in json.loads(con.execute(
                "SELECT v FROM blob WHERE k='counts'").fetchone()[0]).items() if k != "n_saves"},
            "kinds_known": con.execute("SELECT v FROM meta WHERE k='kinds_known'").fetchone()}
    finally:
        con.close()
    return out


def _tables(d) -> dict:
    con = lineage_store.open_store(d)
    try:
        return {t: sorted(map(repr, con.execute(f"SELECT * FROM {t}")))
                for t in (*lineage_store._TABLES, "meta")}
    finally:
        con.close()


def _fresh(d, tmp, name):
    d2 = tmp / name
    d2.mkdir()
    for f in d.glob("gen_*.json"):
        shutil.copy(f, d2 / f.name)
    _catch(d2)
    return d2


def _n(t) -> dict:
    return {"kind": sum(r[5] for r in t["kind"]), "kind_dk": sum(r[3] for r in t["kind_dk"]),
            "kind_off": sum(r[3] for r in t["kind_off"])}


def _forms(t) -> set:
    return {c for k in ("kind", "kind_dk", "kind_off", "pair") for r in t[k] for x in r
            if isinstance(x, str) for c in ("11", "12", "13") if f"form={c}" in x}


def _archive(chain) -> dict:
    """lineage.load's archive sums over a chain (the kind n by key, kind_counts, action cells)."""
    n: dict = {}
    kc: dict = {}
    ak: dict = {}
    for _h, g in chain:
        for e, r, ko, kx, m in g.get("kinds_landed_n", ()):
            key = (e, r, json.dumps(ko), json.dumps(kx))
            n[key] = n.get(key, 0) + m
        for site, d_ in g.get("kind_counts", {}).items():
            for k, m in d_.items():
                kc.setdefault(site, {})[k] = kc.get(site, {}).get(k, 0) + m
        ak.update(g.get("action_kinds", {}))
    return {"n": n, "kind_counts": kc, "action_kinds": ak}


def mf_k6(tmp: Path) -> dict:
    d = tmp / "k6"
    d.mkdir()
    r = _put(d, _root())
    _catch(d)
    before = _n(_decoded(d))
    a = _put(d, _alias_gen(r, PAIRS))
    _catch(d)
    _put(d, _child(a))
    _catch(d)
    t = _decoded(d)
    assert not _forms(t), ("MF-K6 rows under 11/12 remain", sorted(_forms(t)))
    k = {(e, ro): v for e, ro, o, x, *v in t["kind"] if o == json.dumps(_k(10))}
    assert k[("e1", "CAUSE")][1] == 8 and k[("e1", "CAUSE")][6] == 11, ("MF-K6 n / l_seq", k)
    assert k[("e2", "MOVE")][1] == 5, ("MF-K6 the canonical row", k)
    assert t["kind_dk"] == [(json.dumps(["d"]), "e1", json.dumps(_k(10)), 3, "g", 0, 2, 9)], (
        t["kind_dk"])
    assert t["kind_off"] == [(json.dumps(["d"]), "e1", json.dumps(_k(10)), 7)], t["kind_off"]
    assert t["pair"] == [(json.dumps(_k(10)), json.dumps(["SHAPE", "form=22"]), 13, 11)], t["pair"]
    assert _n(t) == {"kind": before["kind"] + 1, "kind_dk": before["kind_dk"],
                     "kind_off": before["kind_off"]}, ("MF-K6 total n", before, _n(t))
    c = t["counts"]
    assert c["kind_counts"] == {"s": {"('COLOUR', 'form=10')": 8}}, c["kind_counts"]
    assert c["cause_kinds"] == {"('COLOUR', 'form=10')|x": 3}, c["cause_kinds"]
    assert c["action_kinds"] == {_cell("A1", "delta_kind", 10): [3, 7],
                                 _cell("A1", "lands_kind", 10): ["a", "b"]}, c["action_kinds"]
    assert t["kinds_known"] == ("2",), ("MF-K6 kinds_known", t["kinds_known"])
    d2 = _fresh(d, tmp, "k6_fresh")
    assert _tables(d) == _tables(d2), "MF-K6 save by save != built from nothing"
    arc = _archive(lineage_store.alias_chain(lineage._chain(d)))
    st = {(e, ro, o, x): v[1] for e, ro, o, x, *v in t["kind"] if v[2]}
    assert arc["n"] == st, ("MF-K6 archive n != store n", arc["n"], st)
    assert arc["kind_counts"] == c["kind_counts"] and arc["action_kinds"] == c["action_kinds"], (
        "MF-K6 archive counts != store", arc, c)
    return {"n_e1": 8, "total_n": _n(t)}


def mf_k7(tmp: Path) -> dict:
    """In a child process with TETHER_KIND_ALIAS=0."""
    d, d2 = tmp / "k7", tmp / "k7_plain"
    d.mkdir()
    d2.mkdir()
    r = _put(d, _root())
    a = _put(d, _alias_gen(r, PAIRS))
    _put(d, _child(a))
    _put(d2, _root())
    _put(d2, _child(r))
    _catch(d)
    _catch(d2)
    t, t2 = _decoded(d), _decoded(d2)
    assert t == t2, ("MF-K7 OFF: the alias generation changed the store", t, t2)
    con = lineage_store.open_store(d)
    try:
        assert con.execute("SELECT v FROM meta WHERE k='form_aliases'").fetchone() is None
    finally:
        con.close()
    chain = lineage._chain(d)
    assert lineage_store.alias_chain(chain) is chain, "MF-K7 OFF: alias_chain changed the chain"
    import arc_percept as ap
    import arc_world
    assert not ap._FORM_PAIRS, "the child runs TETHER_FORM_PAIRS OFF"
    turned = ap._images(frozenset({(0, 0), (1, 0), (2, 0), (2, 1)}))[1]

    class Dec:
        tracked = {"o1": {"shape": turned}}

    class Stub:
        _decompose, _shape_codes, form_pairs = Dec(), {}, {}
    st, was = Stub(), ap._KIND_CANON
    try:
        ap._KIND_CANON = True
        code = arc_world.ArcWorld.shape_code(st, "o1")
    finally:
        ap._KIND_CANON = was
    assert code == ap.kind_code(turned) and st.form_pairs == {}, (
        "MF-K7 FORM_PAIRS OFF", st.form_pairs)
    return {"forms_kept": sorted(_forms(t)), "pairs_kept_off": 0}


def mf_k8(tmp: Path) -> dict:
    d, d2 = tmp / "k8", tmp / "k8_plain"
    d.mkdir()
    d2.mkdir()
    r = _put(d, _root())
    _put(d2, _root())
    _catch(d)
    _put(d, _alias_gen(r, [[99, 98, 3], [98, 98, 0]]))
    _catch(d)
    _catch(d2)
    assert _decoded(d) == _decoded(d2), "MF-K8 an alias for an absent code changed the store"
    return {"ok": True}


def mf_k10(tmp: Path) -> dict:
    d = tmp / "k10"
    d.mkdir()
    _put(d, _root())
    res = lineage.alias_generation(d, [[11, 10, 1], [10, 9, 0]])
    assert "not idempotent" in res.get("refused", ""), ("MF-K10", res)
    assert len(list(d.glob("gen_*.json"))) == 1, "MF-K10 a refused map was written"
    return {"refused": res["refused"]}


def mf_k11(tmp: Path) -> dict:
    d = tmp / "k11"
    d.mkdir()
    r = _put(d, _root())
    _catch(d)
    before = _n(_decoded(d))
    a1 = lineage.alias_generation(d, [[11, 10, 1], [10, 10, 0]])["hash"]
    _catch(d)
    c = _put(d, _child(a1))
    _catch(d)
    mid = _decoded(d)
    assert any("form=12" in str(x) for x in mid["kind"]), "MF-K11 precondition: 12 still stored"
    res = lineage.alias_generation(d, [[12, 10, 2]])
    assert res.get("hash") and res["pairs"] == 1, ("MF-K11 second alias", res)
    _catch(d)
    t = _decoded(d)
    assert not _forms(t), ("MF-K11 rows under 12 remain after the second alias", sorted(_forms(t)))
    assert _n(t) == {"kind": before["kind"] + 1, "kind_dk": before["kind_dk"],
                     "kind_off": before["kind_off"]}, ("MF-K11 total n", before, _n(t))
    d2 = _fresh(d, tmp, "k11_fresh")
    assert _tables(d) == _tables(d2), "MF-K11 save by save != built from nothing"
    return {"gens": [r, a1, c, res["hash"]], "total_n": _n(t)}


def mf_k12(tmp: Path) -> dict:
    d = tmp / "k12"
    d.mkdir()
    r = _put(d, _root())
    lineage.alias_generation(d, [[11, 10, 1], [10, 10, 0]])
    res = lineage.alias_generation(d, [[11, 13, 0], [13, 13, 0]])
    why = res.get("refused", "")
    assert "10" in why and "13" in why, ("MF-K12 alias_generation", res)
    _catch(d)
    tip = lineage._tips(lineage._scan(d))[0]
    _put(d, _alias_gen(tip, [[11, 13, 0], [13, 13, 0]]))
    try:
        _catch(d)
        raise AssertionError("MF-K12 the store took a second canonical")
    except lineage_store.Refused as e:
        assert "10" in str(e) and "13" in str(e), ("MF-K12 store reason", str(e))
        store_why = str(e)
    return {"root": r, "refused": why, "store": store_why}


def _routine(code, standing):
    key = json.dumps({"kind": f"form={code}"}, sort_keys=True)
    return {"key": key, "form": {"kind": f"form={code}"}, "standing": standing}


def _installed(d, store: bool) -> dict:
    """What lineage.load installs from d into a fresh gridworld agent, by the store or (store
    False) by the archive fallback, as comparable text."""
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    was = lineage._MEMORY_STORE
    lineage._MEMORY_STORE = store
    try:
        lineage.load(d, ag)
    finally:
        lineage._MEMORY_STORE = was
    snap = getattr(ag, "_dk_snap", None)
    dk = (dict(snap.items()) if store and snap is not None and tether._W_DK_KEYED
          else {k: n for k, n in ag._kind_known_dk.items() if n})
    out = {"routines": ag._routines_in, "action": ag.iface.carried_kind,
           "kind_counts": ag._kind_carried_in, "cause": ag._cause_kind_in,
           "pairs": ag._pair_counts(), "dk": dk,
           "off": {k: n for k, n in ag._kind_known_off.items() if n}}
    if snap is not None:
        snap.close()
    return {k: sorted(map(repr, v.items())) for k, v in out.items()}


def mf_k13(tmp: Path) -> dict:
    """r904 2: two alias generations and a collision; the store load and the archive load install
    one state. The routines of 11 (settled, save 1) and 12 (candidate, save 3) meet at the second
    alias: contested, both kept, and the later save's row is read."""
    d = tmp / "k13"
    d.mkdir()
    r = _put(d, {**_root(), "routines_by_kind": [_routine(11, "settled")]})
    a1 = _put(d, _alias_gen(r, [[11, 10, 1], [10, 10, 0]]))
    c = _put(d, {**_child(a1), "routines_by_kind": [_routine(12, "candidate")],
                 "action_kinds": {_cell("A1", "delta_kind", 12): [5, 6]}})
    _put(d, _alias_gen(c, [[12, 10, 2]]))
    _catch(d)
    st, ar = _installed(d, True), _installed(d, False)
    diff = {k: (st[k], ar[k]) for k in st if st[k] != ar[k]}
    assert not diff, ("MF-K13 the store load != the archive load", diff)
    counts = _decoded(d)["counts"]
    key10 = _routine(10, "x")["key"]
    assert [x["standing"] for x in counts["contested_routines"][key10]] == [
        "settled", "candidate"], ("MF-K13 contest record", counts.get("contested_routines"))
    assert counts["routines_by_kind"] == {key10: {**_routine(10, "candidate")}}, (
        "MF-K13 the later save's row is read", counts["routines_by_kind"])
    assert not any("form=11" in x or "form=12" in x for v in st.values() for x in v), (
        "MF-K13 an as-seen code was installed", st)
    return {"fields": len(st), "rows": sum(len(v) for v in st.values())}


def mf_k9(tmp: Path) -> dict:
    """K4, the alias at arrival (r888, r903, r906). (a) code_pair: the as-seen code is form_code
    with K1 OFF, the canonical is kind_code and form_code with K1 ON, the pose is canon's. (b)
    ArcWorld.shape_code under K1 keeps as_seen -> (canonical, pose) for a turned shape, nothing for
    one in its canonical pose. (c) the save: a gridworld agent loaded from a lineage storing kinds
    under 11, perception having met 11 (stored) and 33 (not stored), writes form_aliases [[11, 10,
    1]] only, and its action cell under 10 is the carried 10 and 11 summed; the store then holds
    that cell and no row under 11."""
    import arc_percept as ap
    import arc_world
    ell = frozenset({(0, 0), (1, 0), (2, 0), (2, 1)})
    seen, canon_c, pose = ap.code_pair(ell)
    best, pose0 = ap.canon(ell)
    was = ap._KIND_CANON
    try:
        ap._KIND_CANON = False
        off = ap.form_code(ell)
        ap._KIND_CANON = True
        on = ap.form_code(ell)
    finally:
        ap._KIND_CANON = was
    assert (seen, canon_c, pose) == (off, ap.kind_code(ell), pose0) and on == canon_c, (
        "MF-K9a code_pair", seen, canon_c, pose, off, on)
    turned = ap._images(ell)[1]
    if ap._hash(turned) == ap._hash(best):
        turned = ap._images(ell)[2]

    class Dec:
        tracked = {"o1": {"shape": turned}, "o2": {"shape": best}, "o3": {"shape": turned}}

    class Stub:
        _decompose, _shape_codes, form_pairs = Dec(), {}, {}
    st = Stub()
    calls = [0]
    real = ap._canon

    def spy(cells):
        calls[0] += 1
        return real(cells)
    try:
        ap._KIND_CANON, ap._canon = True, spy
        c1, c2, c3 = (arc_world.ArcWorld.shape_code(st, o) for o in ("o1", "o2", "o3"))
        c1b = arc_world.ArcWorld.shape_code(st, "o1")
    finally:
        ap._KIND_CANON, ap._canon = was, real
    assert c1 == c2 == c3 == c1b == canon_c and st.form_pairs == {
        ap._hash(turned): (canon_c, ap.canon(turned)[1])}, ("MF-K9b shape_code", st.form_pairs)
    assert calls[0] == 2, ("MF-K9b (r909) a cell set seen again computes canon once", calls[0])
    d = tmp / "k9"
    d.mkdir()
    root = _root()
    root["action_kinds"][_cell("A1", "delta_kind", 10)] = [4, 4]
    _put(d, root)
    _catch(d)
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    lineage.load(d, ag)
    assert 11 in ag._stored_forms and 33 not in ag._stored_forms, ("K9 load", ag._stored_forms)
    ag.env.form_pairs = {11: (10, 1), 33: (30, 2)}
    out = lineage.write(d, ag, "k9")
    g = lineage._read(d)[out["hash"]]
    assert g.get("form_aliases") == [[11, 10, 1]], ("MF-K9c the pairs written",
                                                    g.get("form_aliases"))
    assert g["action_kinds"].get(_cell("A1", "delta_kind", 10)) == [5, 7], (
        "MF-K9c the action cell", g.get("action_kinds"))
    _catch(d)
    t = _decoded(d)
    assert t["counts"]["action_kinds"][_cell("A1", "delta_kind", 10)] == [5, 7], (
        "MF-K9c the store's cell: the re-keyed 4 + 1, replaced by the save's equal sum",
        t["counts"]["action_kinds"])
    assert not any("form=11" in x for r in t["kind"] for x in r if isinstance(x, str)), t["kind"]
    snap = getattr(ag, "_dk_snap", None)
    if snap is not None:
        snap.close()
    return {"pairs": g["form_aliases"], "cell": g["action_kinds"][_cell("A1", "delta_kind", 10)]}


def main():
    if "--off" in sys.argv:
        assert not lineage_store._ALIAS, "the child runs OFF"
        with tempfile.TemporaryDirectory() as t:
            print(json.dumps(mf_k7(Path(t))))
        return
    assert lineage_store._ALIAS, "TETHER_KIND_ALIAS is ON by default"
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        k6 = mf_k6(tmp)
        print(f"  MF-K6 11 and 12 meet under 10: e1 n 3 + 4 + 1 = {k6['n_e1']}, total n "
              f"{k6['total_n']}; counts summed, action cells joined; save by save = from nothing; "
              f"archive = store")
        print(f"  MF-K8 an alias for an absent code: {mf_k8(tmp)}")
        print(f"  MF-K10 refused: {mf_k10(tmp)['refused']}")
        k11 = mf_k11(tmp)
        print(f"  MF-K11 a second alias re-keys rows already stored: total n {k11['total_n']}; "
              f"save by save = from nothing")
        k12 = mf_k12(tmp)
        print(f"  MF-K12 refused: {k12['refused']}; the store: {k12['store']}")
        k9 = mf_k9(tmp)
        print(f"  MF-K9 code_pair = form_code OFF / ON, pose = canon's; shape_code keeps the "
              f"turned shape's pair; the save writes {k9['pairs']} (33 not stored), its action "
              f"cell 4 + 1 / 4 + 3 = {k9['cell']}, and the store holds it")
        k13 = mf_k13(tmp)
        print(f"  MF-K13 store load = archive load: {k13['fields']} installed fields, "
              f"{k13['rows']} rows; routines 11 (settled) and 12 (candidate) contested, both "
              f"kept, the later save's read")
    env = {**os.environ, "TETHER_KIND_ALIAS": "0", "TETHER_FORM_PAIRS": "0",
           "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run([sys.executable, "-B", __file__, "--off"], env=env, capture_output=True,
                         text=True, timeout=120)
    assert out.returncode == 0, ("MF-K7 OFF child", out.stdout[-2000:], out.stderr[-2000:])
    print(f"  MF-K7 OFF: the store equals the same saves without the alias generation; "
          f"{json.loads(out.stdout.strip().splitlines()[-1])}")
    print("test_kind_alias OK")


if __name__ == "__main__":
    main()
