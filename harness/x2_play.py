"""X2, PLAY IDENTITY UNDER BOTH STORE FORMS (step (5a); the reviewer 2026-10-25 00:20 E, 00:37,
00:53, 01:41; the design ruled 04:07). memory.db (TETHER_STORE_DB=0) against learned.db (=1), the
same tree, every play in its own child (TETHER_* cleared but the form; PYTHONHASHSEED=0; the seed
from one fixed record through TETHER_SEED_FROM, as test_identity_store plays). Test-only: no agent
module is changed; every plant lives in a child's memory.

  A  fresh lineages, both forms. G1 = the fake game, arc_holdout.play("fake", 12), cold then warm
     (test_identity_store's PLAY); G2 = gridworld_s2, 11 steps (test_gate_ledger's G2; it wires no
     lineage: STORE NOT REACHED). Per play:
     A1 the ledger rows (identity_mod_rows.compare, test_identity_store's masks), with the FORM
        WITNESS (the on/off lists differ by exactly lineage._STORE_DB, off -> on), then on/off
        popped; the result dict, masked as there
     A2 every written file by name and blob id, the store files aside (one-sided by construction)
     A3 the store CONTENT: the view (repr sha256 per field; "merged" for both sides) and the
        snapshot (count, nonpos, tot_t, last_k, rows(d) over every kind, items; dicts as items)
     A4 end_path present after each play on both forms, shaped {"s": float, "sleep_s": float}
     A determinism CONTROL plays G1 under =0 twice; it must be 0 differing.
  B  in place on X1's 33-save folders (OLD the memory side, DB the db side; the old side's save
     files copied into the db side first, so both hold the same 33 saves). B3 at the start, then
     the fake game twice per side, with B1-B3 as A1-A3 after each life.
     E1 ORDER OCCASIONS at the start, on both sides: per ordered output (the view's pairs, koff,
        held, kdk, t2, nocount, wholes; the snapshot's tot_t, last_k, rows(d), items), the
        adjacent pairs whose key TEXT order differs from the order given. Asserted > 0 for every
        non-empty view list and for rows(d).
     E2 ORDER MUST-FAIL: the db view's pairs sort planted as ORDER BY key text (lineage.py's
        source, exactly once): the view must read DIFFERS on pairs and on nothing else.
     E3 READING: per play, the store["wal_bound"] checkpoints (count, seconds), the sleep's
        s_checkpoint, and the -wal bytes after the play.
  M  the writing must-fails, on fresh lineages, db form, each judged on learned.db right after the
     write and before any load (unmerged EMPTY, 'saves' = the folder's gen_ count), occasions
     asserted:
     M5a  the merge no-op'd (store_fold.merge_folder_save, once): unmerged = [h]; the next load's
          "merged" printed (1 expected: the folder heals it)
     M5a2 the write merges into a REPLACED store (a fresh file from _store_base, once)
     M5b  a save written by an agent wired WITHOUT the lineage: the merge Refuses on the parent
     D    the control: every section's store.section_digest equals its manifest row; the
          must-fail no-ops update_manifest inside merge_save: the touched sections disagree
     M6   no learned store: G1 with no lineage_dir under each form (no store file; the lineage
          rows quoted), and a first-ever play into an EMPTY lineage_dir under =1 (learned.db, 1
          save, no memory.db)
  The stray column: each working folder's memory.db / learned.db, after each play.

    python harness/x2_play.py A OUT
    python harness/x2_play.py B OUT OLD_FOLDER DB_FOLDER
    python harness/x2_play.py M OUT
rc 0 iff every identity is 0 differing, every occasion count asserted is > 0, and every must-fail is
red for its named reason only. Nothing is capped: an overrun is reported, never stopped.
"""
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [ROOT, os.path.join(ROOT, "tests"), os.path.join(ROOT, "conform")]
from identity_mod_rows import compare  # noqa: E402

import instruments  # noqa: E402
import test_identity_store as tis  # noqa: E402

ARM = "lineage._STORE_DB"
STORES = ("memory.db", "learned.db")

CHILD = r'''
import json, os, sys, time
sys.dont_write_bytecode = True
tree, mode, folder, out, led, n, plant = sys.argv[1:8]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
os.chdir(tree)
hits = {"plant": 0}


def mutate(name, old, new):
    """An in-memory source mutation of one module, applied exactly once, before any import."""
    import importlib.util
    path = os.path.join(tree, name + ".py")
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    assert src.count(old) == 1, ("the planted line is not unique", name, src.count(old))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(src.replace(old, new), path, "exec"), mod.__dict__)
    hits["plant"] += 1


if plant == "e2":
    mutate("lineage", 'pairs = sorted(sec("pair"), key=lambda r: ids(*r[0]))',
           'pairs = sorted(sec("pair"), key=lambda r: json.dumps(r[0]))')
import arc_holdout, lineage
import store_fold as sf
from test_entry import FakeWrapper


class Arc:
    def make(self, _game):
        return FakeWrapper()


if plant == "nomerge":
    def nomerge(con, folder_, h, g):
        hits["plant"] += 1
        return {"save": h, "k": 0, "planted": "no merge"}
    sf.merge_folder_save = nomerge
elif plant == "replace":
    real_base = lineage._store_base

    def replaced(p, parent):
        sb = real_base(p, parent)
        if isinstance(sb, tuple):
            sb[0].close()
            for f in (sf.DB, sf.DB + "-wal", sf.DB + "-shm"):
                if os.path.exists(os.path.join(p, f)):
                    os.replace(os.path.join(p, f), os.path.join(p, f + ".replaced"))
            hits["plant"] += 1
            return sf.open_new(sf.path(p)), sb[1]
        return sb
    lineage._store_base = replaced
elif plant == "nomanifest":
    real_um, real_ms, inside = sf.update_manifest, sf.merge_save, []

    def um(con, delta):
        if inside:
            hits["plant"] += 1
            return None
        return real_um(con, delta)

    def ms(*a, **k):
        inside.append(1)
        try:
            return real_ms(*a, **k)
        finally:
            inside.pop()
    sf.update_manifest, sf.merge_save = um, ms


def walk(x, key, acc):
    if isinstance(x, dict):
        for k, v in x.items():
            if k == key:
                acc.append(v)
            walk(v, key, acc)
    elif isinstance(x, list):
        for v in x:
            walk(v, key, acc)
    return acc


def text(k):
    return json.dumps(list(k) if isinstance(k, tuple) else k, ensure_ascii=False,
                      sort_keys=True, separators=(",", ":"), default=str)


def occ(keys):
    ks = [text(k) for k in keys]
    return sum(1 for a, b in zip(ks, ks[1:]) if a > b)


def h16(x):
    import hashlib
    return hashlib.sha256(repr(x).encode()).hexdigest()[:16]


def flat(x):
    if isinstance(x, dict):
        return [(k, flat(v)) for k, v in x.items()]
    return x


def key_of(x):
    if isinstance(x, (list, tuple)) and x and isinstance(x[0], (list, tuple)):
        return x[0]
    return x


res = {"plant_hits": None}
if mode == "play":
    lin = None if folder == "-" else folder
    r = arc_holdout.play("fake", int(n), arc=Arc(), led_path=led, lineage_dir=lin)
    res.update(result=r, wal_bound=walk(r, "wal_bound", []), sleep=walk(r, "sleep", []))
elif mode == "noload":
    env, ag, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    for _ in range(int(n)):
        env.observe()
        ag.step()
    ag.end_run("cap")
    res.update(result=lineage.write(folder, ag, "fake"))
elif mode == "gw":
    import gamma, ledger, panel, tether, world
    g, seed = panel._gridworld(0)
    env = world.bind(g)
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"gate_{seed}"), tether.Config(),
                      ledger.Ledger(path=led))
    for _ in range(int(n)):
        ag.step()
    ag.led.close()
elif mode == "view":
    ag = arc_holdout.wire(FakeWrapper(), "fake")[1]
    v = (lineage._store_view_db if lineage._STORE_DB else lineage._store_view)(folder, ag)
    res["merged"] = len(v.get("merged", ()))
    res["fields"] = {k: [h16(v[k]), len(v[k]) if hasattr(v[k], "__len__") else repr(v[k])[:60]]
                     for k in sorted(v) if k not in ("folder", "atoms", "merged", "healed")}
    lists = [k for k in ("pairs", "koff", "held", "kdk", "t2", "nocount", "wholes")
             if isinstance(v.get(k), list)]
    res["occ"] = {k: occ([key_of(x) for x in v[k]]) for k in lists}
    res["len"] = {k: len(v[k]) for k in lists}
elif mode == "snap":
    s = (lineage.DkSnapshotDb if lineage._STORE_DB else lineage.DkSnapshot)(folder)
    kinds = sorted(s.kind_s if lineage._STORE_DB else s.kind_id, key=repr)
    rows = {d: s.rows(d) for d in kinds}
    items = list(s.items())
    res["fields"] = {"count": h16(s.count), "nonpos": h16(s.nonpos), "tot_t": h16(flat(s.tot_t)),
                     "last_k": h16(flat(s.last_k)), "kinds": h16(sorted(map(repr, kinds))),
                     "rows(d)": h16(flat(rows)), "items": h16(items)}
    res["occ"] = {"tot_t": occ(list(s.tot_t)), "last_k": occ(list(s.last_k)),
                  "rows(d)": sum(occ(list(r)) for r in rows.values()),
                  "items": occ([i[0] for i in items])}
    res["n"] = {"kinds": len(kinds), "rows": sum(map(len, rows.values())), "items": len(items)}
    s.close()
res["plant_hits"] = hits["plant"]
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, default=str, sort_keys=True)
print("child done")
'''

SEED: list = []
FAIL: list = []


def load(p: str):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def child(form: str, mode: str, folder: str, out: str, led: str = "-", n: int = 12,
          plant: str = "-") -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_SEED_FROM=SEED[0],
               TETHER_STORE_DB=form)
    t0 = time.time()
    r = subprocess.run([sys.executable, "-B", "-c", CHILD, ROOT, mode, folder, out, led, str(n),
                        plant], env=env, capture_output=True, text=True, cwd=ROOT,
                       stdin=subprocess.DEVNULL, check=False)
    dt = time.time() - t0
    if r.returncode:
        raise SystemExit(f"child {mode} {plant} ({form}) failed after {dt:.0f} s:\n"
                         f"{r.stderr[-3000:]}")
    print(f"    child {mode}{'' if plant == '-' else ' plant ' + plant} form {form}: {dt:.0f} s",
          flush=True)
    return load(out)


def check(ok: bool, what: str) -> None:
    print(f"  {'OK  ' if ok else 'FAIL'} {what}", flush=True)
    if not ok:
        FAIL.append(what)


def strays(*folders) -> None:
    for d in folders:
        if d and os.path.isdir(d):
            have = [f for f in STORES if os.path.exists(os.path.join(d, f))]
            print(f"    stray column {d}: {have or 'no store'}", flush=True)


def wal(d: str) -> dict:
    return {f: os.path.getsize(os.path.join(d, f + "-wal")) for f in STORES
            if os.path.exists(os.path.join(d, f + "-wal"))}


def arms_row(rows: list) -> dict:
    return next(r["detail"] for r in rows if r.get("slot") == "@run" and r.get("event") == "arms")


def form_witness(b: dict, c: dict) -> bool:
    on = [set(b.get("on") or ()), set(c.get("on") or ())]
    off = [set(b.get("off") or ()), set(c.get("off") or ())]
    diff = (on[0] ^ on[1]) | (off[0] ^ off[1])
    print(f"    form witness: ON diff {sorted(on[0] ^ on[1])}, OFF diff {sorted(off[0] ^ off[1])}",
          flush=True)
    return diff == {ARM} and ARM in off[0] and ARM in on[1]


def rows_compare(la: str, lb: str, label: str, forms_differ: bool = True) -> None:
    ra, rb = tis._rows(la), tis._rows(lb)
    aa, ab = arms_row(ra), arms_row(rb)
    if forms_differ:
        check(form_witness(aa, ab), f"{label} form witness: exactly {ARM}, off -> on")
    for a in (aa, ab):
        a.pop("on", None)
        a.pop("off", None)
    bad = compare(ra, rb, set())
    print(f"    {label}: rows {len(ra)} / {len(rb)}, {len(bad)} differing"
          + "".join(f"\n      {x}" for x in bad[:20]), flush=True)
    check(len(ra) > 50 and not bad, f"{label} rows 0 differing")


def result_compare(a: dict, b: dict, label: str) -> None:
    a = tis._mask_result(json.loads(json.dumps(a)))
    b = tis._mask_result(json.loads(json.dumps(b)))
    leaves = [x for k in sorted(set(a) | set(b), key=str) if a.get(k) != b.get(k)
              for x in tis._leaves(a.get(k), b.get(k), k)]
    for path, bv, cv in leaves[:20]:
        print(f"      {label} result {path}: {json.dumps(bv, default=str)[:300]} -> "
              f"{json.dumps(cv, default=str)[:300]}", flush=True)
    check(not leaves, f"{label} result 0 differing")


def blobs(d: str) -> dict:
    out = {}
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if os.path.isfile(p) and not f.startswith(STORES) and ".replaced" not in f:
            with open(p, "rb") as fh:
                out[f] = instruments.Attribution.blob_id(fh.read())
    return out


def files_compare(da: str, db: str, label: str) -> None:
    a, b = blobs(da), blobs(db)
    bad = sorted(f for f in set(a) | set(b) if a.get(f) != b.get(f))
    print(f"    {label} files: {len(a)} / {len(b)} (store files aside), {len(bad)} differing "
          f"{bad[:10]}", flush=True)
    check(len(a) > 0 and not bad, f"{label} files 0 differing")


def content_compare(da: str, db: str, work: str, label: str, plant_db: str = "-") -> tuple:
    va = child("0", "view", da, os.path.join(work, "view_old.json"))
    vb = child("1", "view", db, os.path.join(work, "view_db.json"), plant=plant_db)
    print(f"    {label} view: merged old {va['merged']} / db {vb['merged']}", flush=True)
    vbad = sorted(k for k in set(va["fields"]) | set(vb["fields"])
                  if va["fields"].get(k) != vb["fields"].get(k))
    for k in sorted(va["fields"]):
        print(f"      {k:12} old {va['fields'][k]} | db {vb['fields'].get(k)} "
              f"{'DIFFERS' if k in vbad else 'EQUAL'}", flush=True)
    if plant_db != "-":
        return va, vb, vbad
    check(not vbad and va["merged"] == 0 and vb["merged"] == 0,
          f"{label} view {len(va['fields'])} fields EQUAL, merged 0 / 0")
    sa = child("0", "snap", da, os.path.join(work, "snap_old.json"))
    sb = child("1", "snap", db, os.path.join(work, "snap_db.json"))
    sbad = sorted(k for k in sa["fields"] if sa["fields"][k] != sb["fields"].get(k))
    print(f"    {label} snapshot: {sa['n']} | {sb['n']}; differing {sbad}", flush=True)
    check(not sbad, f"{label} snapshot {len(sa['fields'])} fields EQUAL (ordered)")
    return va, vb, sa, sb


def end_path(d: str, form: str) -> dict | None:
    f = os.path.join(d, STORES[1] if form == "1" else STORES[0])
    con = sqlite3.connect(f"file:{f}?mode=ro", uri=True)
    try:
        if form == "1":
            r = con.execute("SELECT body FROM learned WHERE section = 'meta' AND key = ?",
                            (json.dumps(["end_path"]),)).fetchone()
            return json.loads(json.loads(r[0])["v"]) if r else None
        r = con.execute("SELECT v FROM meta WHERE k = 'end_path'").fetchone()
        return json.loads(r[0]) if r else None
    finally:
        con.close()


def shape_ok(e) -> bool:
    return (isinstance(e, dict) and set(e) == {"s", "sleep_s"}
            and all(isinstance(e[k], (int, float)) for k in e))


def store_state(d: str) -> dict:
    """learned.db read right after a write and before any load: unmerged, the 'saves' count, the
    folder's gen_ count, and the sections whose digest is off their manifest row."""
    import store
    import store_fold as sf
    con = sqlite3.connect(f"file:{os.path.join(d, sf.DB)}?mode=ro", uri=True)
    try:
        unm = sf.unmerged(con, d)
        saves = con.execute("SELECT count(*) FROM learned WHERE section = 'saves'").fetchone()[0]
        man = {s: [n, sha] for s, n, sha in con.execute("SELECT section, n, sha FROM manifest")}
        rows: dict = {}
        for part in store.PARTS:
            for s, k, b in con.execute(f"SELECT section, key, body FROM {part}"):
                rows.setdefault(s, {})[k] = b
    finally:
        con.close()
    gens = sum(1 for f in os.listdir(d) if f.startswith("gen_") and f.endswith(".json"))
    off = sorted(s for s in man if store.section_digest(rows.get(s, {})) != man[s])
    return {"unmerged": unm, "saves": saves, "gens": gens, "digest_off": off}


def lineage_rows(led: str) -> list:
    with open(led, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh]
    return [{"slot": r.get("slot"), "event": r.get("event"), "detail": r.get("detail")}
            for r in rows
            if "lineage" in str(r.get("slot", "")) or "lineage" in str(r.get("event", ""))][:6]


def walk_store(r: dict) -> list:
    out: list = []

    def go(x):
        if isinstance(x, dict):
            if isinstance(x.get("store"), dict):
                out.append(x["store"])
            for v in x.values():
                go(v)
        elif isinstance(x, list):
            for v in x:
                go(v)
    go(r)
    return out


def part_a(out: str) -> None:
    print("== PART A: fresh lineages; G1 = arc_holdout.play fake 12 cold then warm; G2 gridworld",
          flush=True)
    dirs = {}
    for tag, form in (("ctl", "0"), ("old", "0"), ("db", "1")):
        w = os.path.join(out, f"A_{tag}")
        d = os.path.join(w, "lineage")
        os.makedirs(d)
        dirs[tag] = d
        for which in ("cold", "warm"):
            child(form, "play", d, os.path.join(w, f"{which}.res.json"),
                  os.path.join(w, f"{which}.jsonl"))
            if tag != "ctl":
                e = end_path(d, form)
                print(f"    A4 {tag} {which} end_path {e}", flush=True)
                check(shape_ok(e), f"A4 {tag} {which} end_path present, shaped {{s, sleep_s}}")
            strays(d)
    for which in ("cold", "warm"):
        ctl, old, db = (os.path.join(out, f"A_{t}", which) for t in ("ctl", "old", "db"))
        rows_compare(ctl + ".jsonl", old + ".jsonl", f"CONTROL G1 {which} (=0 vs =0)",
                     forms_differ=False)
        rows_compare(old + ".jsonl", db + ".jsonl", f"A1 G1 {which}")
        result_compare(load(old + ".res.json")["result"], load(db + ".res.json")["result"],
                       f"A1 G1 {which}")
    files_compare(dirs["old"], dirs["db"], "A2 G1")
    content_compare(dirs["old"], dirs["db"], os.path.join(out, "A_db"), "A3 G1")
    for tag, form in (("gw_old", "0"), ("gw_db", "1")):
        os.makedirs(os.path.join(out, tag))
        child(form, "gw", "-", os.path.join(out, tag, "res.json"),
              os.path.join(out, tag, "g2.jsonl"), 11)
    rows_compare(os.path.join(out, "gw_old", "g2.jsonl"), os.path.join(out, "gw_db", "g2.jsonl"),
                 "A1 G2 (STORE NOT REACHED)")


def part_b(out: str, old: str, db: str) -> None:
    print("== PART B: in place on X1's 33-save folders", flush=True)
    copied = 0
    for f in sorted(os.listdir(old)):
        if f.startswith(("gen_", "ak_", "idx_")):
            src, dst = os.path.join(old, f), os.path.join(db, f)
            if os.path.exists(dst):
                with open(src, "rb") as a, open(dst, "rb") as b:
                    assert a.read() == b.read(), ("a save file differs between the folders", f)
            else:
                shutil.copyfile(src, dst)
                copied += 1
    gens = [sum(f.startswith("gen_") for f in os.listdir(x)) for x in (old, db)]
    print(f"    the db folder given the old folder's save files: {copied} copied; gen_ {gens}",
          flush=True)
    w = os.path.join(out, "B")
    os.makedirs(w)
    va, vb, sa, sb = content_compare(old, db, w, "B3 at the start")
    for side, v, s in (("old", va, sa), ("db", vb, sb)):
        print(f"    E1 {side}: view {v['occ']} (lengths {v['len']}); snapshot {s['occ']}",
              flush=True)
    check(all(vb["occ"][k] > 0 for k in vb["occ"] if vb["len"][k] > 0)
          and sb["occ"]["rows(d)"] > 0,
          "E1 order occasions > 0 for every non-empty view list and for rows(d)")
    _a, e2b, e2bad = content_compare(old, db, w, "E2 (the db view's pairs sorted by key text)",
                                     "e2")
    print(f"    E2: plant hits {e2b['plant_hits']}, pairs occasions {e2b['occ'].get('pairs')}, "
          f"differing {e2bad}", flush=True)
    check(e2b["plant_hits"] == 1 and e2bad == ["pairs"],
          "E2 MUST-FAIL red on pairs alone (the one named field, nothing else)")
    for life in ("life1", "life2"):
        for side, d, form in (("old", old, "0"), ("db", db, "1")):
            r = child(form, "play", d, os.path.join(w, f"{life}_{side}.res.json"),
                      os.path.join(w, f"{life}_{side}.jsonl"))
            sl = [{k: s.get(k) for k in ("s_checkpoint", "quick_check")} for s in r["sleep"]]
            print(f"    E3 {life} {side}: wal_bound {r['wal_bound']} (n {len(r['wal_bound'])}); "
                  f"sleep {sl}; -wal after {wal(d)}", flush=True)
            strays(d)
        a, b = (os.path.join(w, f"{life}_{s}") for s in ("old", "db"))
        rows_compare(a + ".jsonl", b + ".jsonl", f"B1 {life}")
        result_compare(load(a + ".res.json")["result"], load(b + ".res.json")["result"],
                       f"B1 {life}")
        files_compare(old, db, f"B2 {life}")
        content_compare(old, db, w, f"B3 after {life}")


def two(out: str, tag: str, plant_warm: str = "-") -> tuple:
    d = os.path.join(out, tag, "lineage")
    os.makedirs(d)
    r = None
    for which, plant in (("cold", "-"), ("warm", plant_warm)):
        r = child("1", "play", d, os.path.join(out, tag, f"{which}.res.json"),
                  os.path.join(out, tag, f"{which}.jsonl"), plant=plant)
    return d, r


def part_m(out: str) -> None:
    print("== PART M: the writing must-fails on fresh lineages (db form), read before any load",
          flush=True)
    d, _r = two(out, "M_control")
    st = store_state(d)
    print(f"    M control: {st}", flush=True)
    check(not st["unmerged"] and st["saves"] == st["gens"] == 2 and not st["digest_off"],
          "M control: unmerged EMPTY, saves = gen_ = 2, every digest = its manifest (D green)")
    d, r = two(out, "M5a", "nomerge")
    st = store_state(d)
    print(f"    M5a: plant hits {r['plant_hits']}; {st}", flush=True)
    check(r["plant_hits"] == 1 and len(st["unmerged"]) == 1 and st["saves"] == 1
          and st["gens"] == 2, "M5a MUST-FAIL red: unmerged = [h] (1 occasion), saves 1 vs 2")
    v = child("1", "view", d, os.path.join(out, "M5a", "view.json"))
    print(f"    M5a: the next load's merged {v['merged']} (1 expected: the folder heals it)",
          flush=True)
    d, r = two(out, "M5a2", "replace")
    st = store_state(d)
    print(f"    M5a2: plant hits {r['plant_hits']}; store report "
          f"{json.dumps(walk_store(r), default=str)[:300]}; {st}", flush=True)
    check(r["plant_hits"] == 1 and st["saves"] != st["gens"],
          "M5a2 MUST-FAIL red: the replaced store's saves differ from the folder's gen_ count")
    d = os.path.join(out, "M5b", "lineage")
    os.makedirs(d)
    child("1", "play", d, os.path.join(out, "M5b", "cold.res.json"),
          os.path.join(out, "M5b", "cold.jsonl"))
    r = child("1", "noload", d, os.path.join(out, "M5b", "noload.res.json"), n=6)
    st = store_state(d)
    rep = json.dumps(r["result"], default=str)
    print(f"    M5b: the write's report {rep[:400]}; {st}", flush=True)
    check("refused" in rep and "parent" in rep and len(st["unmerged"]) == 1 and st["saves"] == 1,
          "M5b MUST-FAIL red: the merge Refused on the parent; no row of the save (1 occasion)")
    d, r = two(out, "D", "nomanifest")
    st = store_state(d)
    print(f"    D: plant hits {r['plant_hits']}; sections off their manifest {st['digest_off']}",
          flush=True)
    check(r["plant_hits"] >= 1 and len(st["digest_off"]) > 0,
          "D MUST-FAIL red: the touched sections' digests disagree with the manifest, named")
    for tag, form in (("M6_old", "0"), ("M6_db", "1")):
        w = os.path.join(out, tag)
        os.makedirs(w)
        child(form, "play", "-", os.path.join(w, "res.json"), os.path.join(w, "g1.jsonl"))
        made = [f for _dp, _ds, fs in os.walk(w) for f in fs if f in STORES]
        print(f"    M6 {tag}: no lineage_dir; store files made {made}; lineage rows "
              f"{lineage_rows(os.path.join(w, 'g1.jsonl'))}", flush=True)
        check(not made, f"M6 {tag}: no store file is made with no lineage")
    w = os.path.join(out, "M6_empty")
    d = os.path.join(w, "lineage")
    os.makedirs(d)
    child("1", "play", d, os.path.join(w, "res.json"), os.path.join(w, "g1.jsonl"))
    have = [f for f in STORES if os.path.exists(os.path.join(d, f))]
    st = store_state(d)
    print(f"    M6 an empty lineage_dir under =1: {have}; {st}", flush=True)
    check(have == ["learned.db"] and st["saves"] == st["gens"] == 1,
          "M6: a first-ever play builds learned.db (1 save), no memory.db")


def main() -> int:
    part, out = sys.argv[1], os.path.realpath(sys.argv[2])
    os.makedirs(out)
    SEED.append(os.path.join(out, "seed.jsonl"))
    with open(SEED[0], "w", encoding="utf-8") as fh:
        fh.write(json.dumps(tis.SEED_ROW) + "\n")
    t0 = time.time()
    if part == "A":
        part_a(out)
    elif part == "B":
        part_b(out, os.path.realpath(sys.argv[3]), os.path.realpath(sys.argv[4]))
    elif part == "M":
        part_m(out)
    else:
        raise SystemExit(f"no part {part}")
    print(f"x2 {part}: {'OK' if not FAIL else 'FAIL ' + str(FAIL)} ({time.time() - t0:.0f} s)")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
