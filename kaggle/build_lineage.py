"""THE LINEAGE DATASET (the reviewer 2026-10-30 r465 2, Isaiah 21:28 "yes thats fine"): ONE frozen copy of a lineage
folder, taken while no run writes it, with a marker the notebook finds it by and a manifest of every file's sha256. The
source is read as bytes only -- never opened through the store -- and the copy's head (lineage.head over the COPY) must
equal the head the caller names, the verified head of the run that last wrote it. Every text line is scanned for key-
shaped values and for this machine's paths, printed for reading before any upload. Nothing is uploaded here.
    python kaggle/build_lineage.py LINEAGE_DIR EXPECTED_HEAD OUT_DIR
Writes OUT_DIR/lineage/ (the copy), OUT_DIR/TETHER_KAGGLE_LINEAGE.json (the marker), OUT_DIR/MANIFEST.sha256 and
OUT_DIR/scan.txt. Refuses an OUT_DIR that already holds one."""
import hashlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
MARK = "TETHER_KAGGLE_LINEAGE.json"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET = re.compile(r"(?i)(api[_-]?key|secret|passw(or)?d|bearer)\w*[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-./+]{12,}")
PATHS = re.compile(r"(?i)[a-z]:[\\/]+users[\\/]|tether_runs|@gmail")


def _sha(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tip(d: str) -> str:
    """The chain's one tip, read one generation at a time: each file hashed against its name, its
    parents collected, the generation no other names as a parent. lineage.head folds every
    generation at once, O(life) in memory, and ran out of it on a 1.3 GB lineage."""
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    import lineage
    import lineage_store as ls
    names, parents = [], set()
    for f in sorted(os.listdir(d)):
        if not (f.startswith(lineage.PREFIX) and f.endswith(".json")):
            continue
        raw = ls.file_bytes(Path(d) / f)
        h = hashlib.sha256(raw).hexdigest()[:16]
        assert f == f"{lineage.PREFIX}{h}.json", (f, "does not hash to its name", h)
        names.append(h)
        parents.update(lineage._parents(json.loads(raw)))
        del raw
    tips = [h for h in names if h not in parents]
    assert len(tips) == 1, ("not one tip", tips)
    return tips[0]


def build(src: str, want: str, out: str) -> dict:
    assert not os.path.exists(os.path.join(out, MARK)), ("the out dir already holds a lineage", out)
    dst = os.path.join(out, "lineage")
    before = {f: (os.stat(os.path.join(src, f)).st_size, _sha(os.path.join(src, f))) for f in sorted(os.listdir(src))}
    if not os.path.isdir(dst):      # else a copy left by a build that stopped later: checked below, never re-made
        shutil.copytree(src, dst)
    after = {f: (os.stat(os.path.join(dst, f)).st_size, _sha(os.path.join(dst, f))) for f in sorted(os.listdir(dst))}
    again = {f: (os.stat(os.path.join(src, f)).st_size, _sha(os.path.join(src, f))) for f in sorted(os.listdir(src))}
    assert before == after == again, "the source moved during the copy, or the copy differs"
    head = tip(dst)
    assert head == want, ("the copy's head is not the expected head", head, want)
    hits = []
    for f in after:
        if f.endswith((".json", ".jsonl", ".txt")):
            with open(os.path.join(dst, f), encoding="utf-8", errors="replace") as fh:
                for i, ln in enumerate(fh, 1):
                    if SECRET.search(ln) or PATHS.search(ln):
                        hits.append(f"{f}:{i}: {ln.strip()[:200]}")
        else:   # a binary (the store): the same two patterns over its bytes, each hit with its offset
            with open(os.path.join(dst, f), "rb") as fh:
                blob = fh.read()
            for rx in (re.compile(SECRET.pattern.encode()), re.compile(PATHS.pattern.encode())):
                for m in rx.finditer(blob):
                    hits.append(f"{f}@{m.start()}: {blob[max(0, m.start() - 60):m.end() + 60]!r}"[:300])
    manifest = "".join(f"{h}  {f}\n" for f, (_n, h) in after.items())
    with open(os.path.join(out, "MANIFEST.sha256"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(manifest)
    with open(os.path.join(out, "scan.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("".join(h + "\n" for h in hits))
    mark = {"head": head, "names": len(after), "bytes": sum(n for n, _h in after.values()),
            "manifest_sha256": hashlib.sha256(manifest.encode()).hexdigest(),
            "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with open(os.path.join(out, MARK), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(mark, fh, indent=1)
    return {**mark, "scan_hits": len(hits)}


if __name__ == "__main__":
    print(json.dumps(build(*sys.argv[1:4]), indent=1))
