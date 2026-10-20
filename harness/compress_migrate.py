"""COMPRESSION MIGRATION (the reviewer 2026-10-20 11:06, 11:45; Isaiah 03:57 "retroactively parse
the previous saves"), one-way.

Every gen_ / idx_ / memo file is written zlib-6 under its SAME name: the name is the hash of the
uncompressed bytes, which do not change. Every ak_ file is re-written in FORM 3 (the shape of
lineage._ak_entries3): a form-2 file becomes form 3 (tally n = summed n, v = rows); an old-form
file (no n) becomes "3-from-1" (tally n = v = rows, as n_variants counts it); its whole rows (slot
None) become whole entries. A converted ak_ is named by the hash of its new uncompressed body.
memory.db is never touched (it rebuilds).

  COPY      argv: tree src dst          -- DST must not exist
  IN PLACE  argv: tree src --in-place   -- the reviewer 11:45, no separate test copy: each gen_ /
            idx_ / memo file is replaced through NAME.part and an atomic rename; each converted ak_
            is written first, then the raw ak_ is RENAMED aside as NAME.dead-<UTC> (never deleted
            here; the loaders read only *.json). A file already compressed (first byte 0x78) is
            left as it is, so a re-run is a no-op.
Prints one line per file and the totals."""
import hashlib
import json
import os
import sys
import time
import zlib
from pathlib import Path

TREE, SRC, DST = sys.argv[1:4]
sys.path.insert(0, TREE)
import lineage  # noqa: E402
import lineage_store as ls  # noqa: E402

INPLACE = DST == "--in-place"
STAMP = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
src = Path(SRC)
dst = src if INPLACE else Path(DST)
assert src.is_dir() and (INPLACE or not dst.exists()), (src, dst)
if not INPLACE:
    dst.mkdir(parents=True)
tot = {"files": 0, "raw_bytes": 0, "out_bytes": 0, "ak": 0, "ak_rows": 0, "ak_entries": 0,
       "skipped": 0}


def put(name: str, raw: bytes) -> int:
    z = zlib.compress(raw, 6)
    if INPLACE:
        tmp = dst / (name + ".part")
        with open(tmp, "xb") as fh:
            fh.write(z)
        os.replace(tmp, dst / name)
    else:
        with open(dst / name, "xb") as fh:
            fh.write(z)
    return len(z)


def form3(f: Path) -> tuple:
    """The converted body of one raw ak_ file, and its counts."""
    a = ls.AkFile(f, f.stem.rsplit("_", 1)[0])
    a.verify()
    tally: dict = {}
    whole: dict = {}
    rows = 0
    for e in a.entries():
        rows += 1
        if "sc" in e or e.get("w"):
            raise SystemExit(f"{f.name}: already form 3")
        n = e.get("n", 1)
        t = tally.setdefault((e["key"], e["role"], lineage._ak_class(e["slot"])), [0, 0])
        t[0] += n
        t[1] += 1
        if e["slot"] is None:
            k = (e["key"], e["role"], json.dumps(e["o"]), json.dumps(e["x"]))
            whole[k] = whole.get(k, 0) + n
    form = a.tail.get("form")
    entries = [{"key": k, "role": r, "sc": sc, "n": n, "v": v}
               for (k, r, sc), (n, v) in sorted(tally.items(), key=repr)]
    entries += [{"key": k, "role": r, "o": json.loads(o), "x": json.loads(x), "slot": None,
                 "n": n, "w": 1} for (k, r, o, x), n in sorted(whole.items(), key=repr)]
    body = {k: v for k, v in a.tail.items() if k != "form"}
    body.update(entries=entries, form=3 if form == 2 else "3-from-1")
    return body, form, rows, len(tally), len(whole)


for f in sorted(src.iterdir()):
    if not f.is_file() or f.name.startswith("memory.db") or not f.name.endswith(".json"):
        continue
    disk = f.stat().st_size
    with open(f, "rb") as fh_:
        compressed = fh_.read(1) == b"\x78"
    if compressed:
        tot["skipped"] += 1
        print(f"SKIP {f.name}: already compressed", flush=True)
        continue
    if f.name.startswith(lineage.AKMEMO):
        body, form, rows, nt, nw = form3(f)
        raw = lineage._dumps(body)
        name = f"{lineage.AKMEMO}{f.stem.split('_')[1]}_{hashlib.sha256(raw).hexdigest()[:16]}.json"
        out = put(name, raw)
        if INPLACE:
            os.rename(f, f.with_name(f"{f.name}.dead-{STAMP}"))
        tot["ak"] += 1
        tot["ak_rows"] += rows
        tot["ak_entries"] += len(body["entries"])
        print(f"AK {f.name} -> {name}: form {form} -> {body['form']}; rows {rows} -> entries "
              f"{len(body['entries'])} ({nt} tally, {nw} whole); bytes {disk} -> {out}", flush=True)
    else:
        out = put(f.name, ls.file_bytes(f))
        print(f"Z {f.name}: bytes {disk} -> {out}", flush=True)
    tot["files"] += 1
    tot["raw_bytes"] += disk
    tot["out_bytes"] += out
print("MIGRATE", json.dumps(tot), flush=True)
