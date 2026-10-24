"""STEP (4), THE LEARNED MIGRATION (Isaiah 2026-10-24 08:22, 08:29 "make both"; the reviewer
08:49, 16:19 WATSON ruling 12). The live lineage's memory.db tables and save files become the
learned store's (section, key, body) rows in BOTH forms through store.learned_save. The live folder
is only READ: memory.db by an immutable read-only open, every file's sha256 before and after the
read (they must be equal, or nothing is written), the save files by plain reads. Every other check
works on copies. Nothing in play imports this.

    build LIVE OUT [--saves=skip]   both forms into OUT/json and OUT/db (the saves: Q1' (a))
    m2a LIVE OUT                    every table: the store (both forms) == table_rows on the live db
    m2b FOLDER OUT                  every save file in FOLDER == its save row, bytes, name hash
    m2c LIVE OUT SCRATCH            lineage._store_view: a copy of LIVE == a rebuild from rows
    m2d LIVE SCRATCH                the saves replayed by catch_up, empty store == live tables
    s1 OUT | s2 OUT SCRATCH | s3 OUT SCRATCH | b1 OUT FMT | b6 OUT
B3: m2a compares in the DECODED space (table_rows decodes both sides' ids), so it checks the write
and read path; m2c's rebuild encodes back (encode_rows) and is read by the agent's own load view,
the independent gate."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
import zlib
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import store  # noqa: E402

# the columns holding sym ids (lineage_store's INSERTs through Syms)
SYM_COLS = {
    "kind": ("entry", "role", "kind_o", "kind_x"),
    "pair": ("kind_o", "kind_x"),
    "kind_dk": ("dk", "entry", "tgt"),
    "kind_off": ("dk", "entry", "ko"),
    "asked_tally": ("entry", "role", "slot_class"),
    "held": ("key", "role"),
}
GB = 2**30


def j(x) -> str:
    return json.dumps(x, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def shas(folder: Path) -> dict:
    out = {}
    for f in sorted(os.listdir(folder)):
        h = hashlib.sha256()
        with open(folder / f, "rb") as fh:
            for b in iter(lambda: fh.read(1 << 20), b""):
                h.update(b)
        out[f] = h.hexdigest()
    return out


def ro(folder: Path) -> sqlite3.Connection:
    return sqlite3.connect(
        f"file:{(folder / 'memory.db').as_posix()}?mode=ro&immutable=1", uri=True
    )


def tables(con) -> list:
    return sorted(
        r[0]
        for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    )


def columns(con, t: str) -> tuple:
    info = list(con.execute(f"PRAGMA table_info({t})"))
    cols = [r[1] for r in info]
    keys = [r[1] for r in sorted((r for r in info if r[5]), key=lambda r: r[5])]
    return cols, keys


def table_rows(con, t: str, sym: dict) -> dict:
    """One table as {key: body}: the primary-key columns the key, the rest the body, sym decoded."""
    cols, keys = columns(con, t)
    sc = SYM_COLS.get(t, ())
    out = {}
    n = 0
    for r in con.execute(f"SELECT {', '.join(cols)} FROM {t}"):
        n += 1
        d = dict(zip(cols, r, strict=True))
        assert not any(isinstance(v, bytes) for v in d.values()), (t, "a BLOB value")
        for c in sc:
            d[c] = sym[d[c]]
        out[j([d[c] for c in keys])] = j({c: d[c] for c in cols if c not in keys})
    assert len(out) == n, (t, "a key is not unique", n, len(out))
    return out


def encode_rows(t: str, rows: dict, ids: dict, cols: list, keys: list) -> list:
    """The inverse of table_rows (M2c's rebuild): {key: body} back to column tuples, text -> id."""
    sc = SYM_COLS.get(t, ())
    out = []
    for k, b in rows.items():
        d = {**dict(zip(keys, json.loads(k), strict=True)), **json.loads(b)}
        for c in sc:
            d[c] = ids[d[c]]
        out.append(tuple(d[c] for c in cols))
    return out


def save_rows(folder: Path) -> dict:
    """Q1': each save file WHOLE as its exact stored bytes (zlib, base64), its name hash checked."""
    import lineage_store as ls

    out = {}
    for f in sorted(os.listdir(folder)):
        if f == "memory.db":
            continue
        raw = (folder / f).read_bytes()
        h = hashlib.sha256(ls.file_bytes(folder / f)).hexdigest()[:16]
        assert Path(f).stem.endswith(h), (f, "does not hash to its name", h)
        enc = "zlib_b64" if raw[:1] == b"\x78" else "b64"
        out[j([f])] = j({"name": f, enc: base64.b64encode(raw).decode("ascii"), "sha16": h})
    return out


def save_bytes(body: str) -> bytes:
    b = json.loads(body)
    return base64.b64decode(b.get("zlib_b64") or b["b64"])


def build(live: Path, out: Path, saves: str) -> None:
    t = time.time()
    before = shas(live)
    con = ro(live)
    sym = dict(con.execute("SELECT id, s FROM sym"))
    rows = {tb: table_rows(con, tb, sym) for tb in tables(con)}
    con.close()
    if saves == "zlib":
        rows["save"] = save_rows(live)
    after = shas(live)
    print(
        f"read: {len(before)} live files, {sum(map(len, rows.values())):,} rows, "
        f"{time.time() - t:.1f} s; sha before == after: {before == after}"
    )
    if before != after:
        raise SystemExit("STOP: the live folder changed during the read; nothing written")
    for fmt in ("json", "db"):
        t = time.time()
        man = store.learned_save(fmt, out / fmt, rows)
        size = sum(f.stat().st_size for f in (out / fmt).iterdir())
        print(f"{fmt}: {len(man)} sections written, {size:,} B, {time.time() - t:.1f} s")
    for s, (n, h) in sorted(man.items()):
        print(f"  {store.part_of(s):10} {s:12} {n:>10,} rows  {h[:16]}")


def m2a(live: Path, out: Path) -> int:
    con = ro(live)
    sym = dict(con.execute("SELECT id, s FROM sym"))
    bad = 0
    for fmt in ("json", "db"):
        got = store.learned_load(fmt, out / fmt)
        for tb in tables(con):
            want = table_rows(con, tb, sym)
            have = got.get(tb)
            ok = have == want
            bad += not ok
            if not ok:
                miss = sorted(set(want) - set(have or {}))[:2]
                diff = [k for k in want if have and k in have and have[k] != want[k]][:2]
                print(
                    f"M2a {fmt} {tb}: DIFFERS ({len(want)} live, {len(have or {})} stored; "
                    f"missing {miss}; changed {diff})"
                )
            else:
                print(f"M2a {fmt} {tb}: EQUAL, {len(want):,} rows")
        extra = sorted(set(got) - set(tables(con)) - {"save"})
        bad += bool(extra)
        print(f"M2a {fmt}: sections not in memory.db: {extra} (the save section is M2b's)")
        del got
    con.close()
    return 1 if bad else 0


def m2b(folder: Path, out: Path) -> int:
    import lineage_store as ls

    total = 0
    for fmt in ("json", "db"):
        bad = 0
        saves = store.learned_load(fmt, out / fmt).get("save", {})
        files = sorted(f for f in os.listdir(folder) if f != "memory.db")
        for f in files:
            b = saves.get(j([f]))
            raw = (folder / f).read_bytes()
            why = "no row" if b is None else None
            if b is not None:
                body = json.loads(b)
                mine = save_bytes(b)
                try:   # 16:44: the body's own bytes decompress and hash to sha16 and the name
                    u = zlib.decompress(mine) if "zlib_b64" in body else mine
                    h = hashlib.sha256(u).hexdigest()[:16]
                except zlib.error as e:
                    h, why = None, f"the body does not decompress: {e}"
                if why is None and not (h == body["sha16"] and Path(f).stem.endswith(h)
                                        and body["name"] == f):
                    why = f"hash {h} vs sha16 {body['sha16']} vs name"
                if why is None and hashlib.sha256(mine).digest() != hashlib.sha256(raw).digest():
                    why = "its bytes differ from the file's"
            if why is None and not Path(f).stem.endswith(
                    hashlib.sha256(ls.file_bytes(folder / f)).hexdigest()[:16]):
                why = "the file does not hash to its name"
            if why:
                bad += 1
                print(f"M2b {fmt} {f}: DIFFERS ({why})")
        extra = sorted(set(saves) - {j([f]) for f in files})
        bad += len(extra)
        total += bad
        print(f"M2b {fmt}: {len(files)} files, {len(saves)} save rows, {bad} differing, "
              f"extra rows {extra[:3]}")
    return 1 if total else 0


VIEW = r"""
import hashlib, json, sys
sys.dont_write_bytecode = True
sys.path[:0] = [sys.argv[1], sys.argv[1] + "/tests"]
import arc_holdout, lineage
from test_entry import FakeWrapper
ag = arc_holdout.wire(FakeWrapper(), "fake")[1]
v = lineage._store_view(sys.argv[2], ag)
out = {}
for k in sorted(v):
    if k in ("folder", "atoms"):
        continue
    out[k] = [hashlib.sha256(repr(v[k]).encode()).hexdigest(),
              len(v[k]) if hasattr(v[k], "__len__") else repr(v[k])[:80]]
print(json.dumps(out))
"""


def view(folder: Path) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    r = subprocess.run(
        [sys.executable, "-B", "-c", VIEW, str(ROOT), str(folder)],
        env=env,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    if r.returncode:
        raise SystemExit(f"the view child failed on {folder}:\n{r.stderr[-2000:]}")
    return json.loads(r.stdout.strip().splitlines()[-1])


def rebuild(out: Path, dst: Path, drop_meta: str | None = None) -> None:
    """A lineage folder from the store's rows: the 99 save files byte for byte, memory.db in
    lineage_store's own schema with every table's rows encoded back (encode_rows)."""
    import lineage_store as ls

    got = store.learned_load("json", out / "json")
    dst.mkdir(parents=True)
    for k, b in got.pop("save").items():
        (dst / json.loads(k)[0]).write_bytes(save_bytes(b))
    ids = {json.loads(b)["s"]: json.loads(k)[0] for k, b in got["sym"].items()}
    con = ls.open_store(dst)
    con.execute("BEGIN")
    for tb, rows in got.items():
        cols, keys = columns(con, tb)
        if tb == "meta" and drop_meta:
            rows = {k: b for k, b in rows.items() if json.loads(k) != [drop_meta]}
        verb = "INSERT OR REPLACE" if tb == "meta" else "INSERT"
        con.executemany(
            f"{verb} INTO {tb}({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
            encode_rows(tb, rows, ids, cols, keys),
        )
    con.execute("COMMIT")
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    con.close()


def m2c(live: Path, out: Path, scratch: Path, drop_meta: str | None = None) -> int:
    a, b = scratch / "live_copy", scratch / "rebuilt"
    assert not a.exists() and not b.exists(), scratch
    t = time.time()
    shutil.copytree(live, a)
    assert shas(a) == shas(live), "the copy differs from the live folder"
    rebuild(out, b, drop_meta)
    print(f"M2c: copied and rebuilt, {time.time() - t:.1f} s")
    va, vb = view(a), view(b)
    bad = [k for k in sorted(set(va) | set(vb)) if va.get(k) != vb.get(k)]
    for k in sorted(set(va) | set(vb)):
        print(
            f"M2c {k}: {'EQUAL' if va.get(k) == vb.get(k) else 'DIFFERS'} {va.get(k, ['-'])[1]} / "
            f"{vb.get(k, ['-'])[1]}"
        )
    print(f"M2c: {len(va)} fields, {len(bad)} differing {bad}")
    return 1 if bad else 0


def m2d(live: Path, scratch: Path) -> int:
    import lineage_store as ls

    r = scratch / "replay"
    r.mkdir(parents=True)
    for f in os.listdir(live):
        if f != "memory.db":
            shutil.copyfile(live / f, r / f)
    t = time.time()
    con = ls.open_store(r)
    merged = ls.catch_up(con, r)
    con.close()
    print(f"M2d: {len(merged)} saves merged from an empty store, {time.time() - t:.1f} s")
    a, b = ro(live), ro(r)
    sa, sb = dict(a.execute("SELECT id, s FROM sym")), dict(b.execute("SELECT id, s FROM sym"))
    bad = []
    for tb in sorted(set(tables(a)) | set(tables(b))):
        wa, wb = table_rows(a, tb, sa), table_rows(b, tb, sb)
        if wa != wb:
            bad.append(tb)
            only = sorted(set(wa) ^ set(wb))[:3]
            chg = [(k, wa[k], wb[k]) for k in wa if k in wb and wa[k] != wb[k]][:3]
            print(f"M2d {tb}: DIFFERS ({len(wa)} live, {len(wb)} replayed; in one only {only}; "
                  f"changed {chg})")
        else:
            print(f"M2d {tb}: EQUAL, {len(wa):,} rows")
    a.close()
    b.close()
    print(f"M2d: {len(bad)} tables differing {bad}")
    return 1 if bad else 0


def s1(out: Path) -> int:
    a = store.learned_load("json", out / "json")
    da = {s: store.section_digest(r) for s, r in a.items()}
    del a
    b = store.learned_load("db", out / "db")
    db = {s: store.section_digest(r) for s, r in b.items()}
    bad = [s for s in sorted(set(da) | set(db)) if da.get(s) != db.get(s)]
    for s in sorted(da):
        print(
            f"S1 {s}: json {da[s][0]:,} {da[s][1][:16]} | db {db.get(s, [0, '-'])[0]:,} "
            f"{db.get(s, [0, '-'])[1][:16]}"
        )
    print(f"S1: {len(da)} sections, {len(bad)} differing {bad}")
    return 1 if bad else 0


def s2(out: Path, scratch: Path) -> int:
    bad = 0
    for first, second in (("json", "db"), ("db", "json")):
        a = store.learned_load(first, out / first)
        for i in range(100):
            a.setdefault("evidence", {})[j(["s2", i])] = j({"row": f"probe {i}"})
            a.setdefault("kind_dk", {})[j(["s2", i, "x"])] = j({"n": i})
        want = {s: store.section_digest(r) for s, r in a.items()}
        d1, d2 = scratch / f"s2_{first}_{second}", scratch / f"s2_{first}_{second}_{first}"
        store.learned_save(second, d1 / second, a)
        del a
        b = store.learned_load(second, d1 / second)
        got1 = {s: store.section_digest(r) for s, r in b.items()}
        store.learned_save(first, d2 / first, b)
        del b
        c = store.learned_load(first, d2 / first)
        got2 = {s: store.section_digest(r) for s, r in c.items()}
        del c
        ok = want == got1 == got2
        bad += not ok
        print(
            f"S2 {first} -> {second} -> {first}: {'EQUAL' if ok else 'DIFFERS'} including the "
            f"100 + 100 added (evidence {want['evidence'][0]:,}, kind_dk {want['kind_dk'][0]:,})"
        )
    return 1 if bad else 0


def s3(out: Path, scratch: Path) -> int:
    import gzip

    cases = []
    for fmt in ("json", "db"):
        src = out / fmt
        for case in ("missing", "empty", "body"):
            d = scratch / f"s3_{fmt}_{case}"
            shutil.copytree(src, d)
            if fmt == "json":
                p = d / store.JSON_FILES["perception"]
                if case == "missing":
                    p.unlink()
                elif case == "empty":
                    p.write_bytes(gzip.compress(b"", mtime=0))
                else:
                    lines = gzip.decompress(p.read_bytes()).split(b"\n")
                    s, k, b = json.loads(lines[1])
                    lines[1] = json.dumps(
                        [s, k, b[:-2] + ("1" if b[-2] != "1" else "2") + b[-1]], ensure_ascii=False
                    ).encode()
                    p.write_bytes(gzip.compress(b"\n".join(lines), mtime=0))
            else:
                p = d / store.DB_FILE
                if case == "missing":
                    p.unlink()
                else:
                    con = sqlite3.connect(p)
                    if case == "empty":
                        con.execute("DELETE FROM manifest")
                        con.execute("DELETE FROM learned")
                        con.execute("DELETE FROM perception")
                    else:
                        k, b = con.execute("SELECT key, body FROM perception LIMIT 1").fetchone()
                        con.execute(
                            "UPDATE perception SET body=? WHERE key=?",
                            (b[:-2] + ("1" if b[-2] != "1" else "2") + b[-1], k),
                        )
                    con.commit()
                    con.close()
            try:
                store.learned_load(fmt, d)
            except store.StoreError as e:
                cases.append((fmt, case, True, str(e)))
            else:
                cases.append((fmt, case, False, "loaded"))
    for fmt, case, red, msg in cases:
        print(f"S3 {fmt} {case}: {'StoreError' if red else 'NOT RAISED'}: {msg[:160]}")
    return 0 if all(c[2] for c in cases) else 1


B1 = r"""
import ctypes, sys, threading, time, os
from ctypes import wintypes
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
class PMC(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t)] + [
                (f"x{i}", ctypes.c_size_t) for i in range(6)]
k = ctypes.windll.kernel32
k.GetCurrentProcess.restype = wintypes.HANDLE
ps = ctypes.windll.psapi
ps.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(PMC), wintypes.DWORD]
def mem():
    m = PMC(); m.cb = ctypes.sizeof(PMC)
    ps.GetProcessMemoryInfo(k.GetCurrentProcess(), ctypes.byref(m), m.cb)
    return m.PeakWorkingSetSize, m.WorkingSetSize
CAP = 8 * 2 ** 30
def guard():
    while True:
        p, w = mem()
        if w > CAP:
            print(f"B1 STOPPED AT THE CAP: working set {w / 2**30:.3f} GiB", flush=True)
            os._exit(9)
        time.sleep(0.05)
threading.Thread(target=guard, daemon=True).start()
import store
t = time.time()
s = store.learned_load(sys.argv[3], sys.argv[2])
print(f"B1 {sys.argv[3]}: {sum(map(len, s.values())):,} rows, {time.time() - t:.1f} s, peak "
      "working set "
      f"{mem()[0] / 2**30:.3f} GiB", flush=True)
"""


def b1(out: Path, fmt: str) -> int:
    r = subprocess.run(
        [sys.executable, "-B", "-c", B1, str(ROOT), str(out / fmt), fmt],
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    print((r.stdout + r.stderr).strip()[-600:])
    return r.returncode


def b6(out: Path) -> int:
    for fmt in ("json", "db"):
        for verify in (True, False, True, False):
            t = time.time()
            s = store.learned_load(fmt, out / fmt, verify=verify)
            print(
                f"B6 {fmt} verify={verify}: {time.time() - t:.1f} s, "
                f"{sum(map(len, s.values())):,} rows"
            )
            del s
    return 0


def main(argv: list) -> int:
    cmd, rest = argv[0], [Path(a) if not a.startswith("--") else a for a in argv[1:]]
    if cmd == "build":
        build(rest[0], rest[1], "skip" if "--saves=skip" in argv else "zlib")
        return 0
    if cmd == "m2c":
        drop = next((a.split("=", 1)[1] for a in argv if a.startswith("--drop-meta=")), None)
        return m2c(rest[0], rest[1], rest[2], drop)
    fn = {"m2a": m2a, "m2b": m2b, "m2d": m2d, "s1": s1, "s2": s2, "s3": s3, "b6": b6}.get(cmd)
    if cmd == "b1":
        return b1(rest[0], argv[2])
    return fn(*[p for p in rest if isinstance(p, Path)])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
