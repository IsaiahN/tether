"""THE KAGGLE DATASET (the reviewer 2026-10-30 r464 3): the tree at one commit, exactly, as files -- the agent's code,
library/ and requirements.lock -- with a marker the notebook finds it by, and a manifest of every file's sha256 the
notebook checks after its copy. No lineage (it waits on Isaiah) and no key: the scan prints every line that assigns a
key-, secret- or password-shaped value, for reading before any upload. Nothing is uploaded here.
    python kaggle/build_dataset.py SHA OUT_DIR
Writes OUT_DIR/code/ (git archive SHA), OUT_DIR/TETHER_KAGGLE_DATASET.json (the marker), OUT_DIR/MANIFEST.sha256 and
OUT_DIR/scan.txt. Refuses an OUT_DIR that already holds a dataset."""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import time

sys.dont_write_bytecode = True
MARK = "TETHER_KAGGLE_DATASET.json"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET = re.compile(r"(?i)(api[_-]?key|secret|passw(or)?d|bearer|token)\w*[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-./+]{12,}")


def git(*a: str) -> bytes:
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, check=True).stdout


def build(sha: str, out: str) -> dict:
    assert not os.path.exists(os.path.join(out, MARK)), ("the out dir already holds a dataset", out)
    full = git("rev-parse", sha).decode().strip()
    tree = git("rev-parse", f"{full}^{{tree}}").decode().strip()
    code = os.path.join(out, "code")
    with tarfile.open(fileobj=io.BytesIO(git("archive", full))) as tf:
        tf.extractall(code, filter="data")
    rows, hits = [], []
    for d, _dirs, files in os.walk(code):
        for f in files:
            p = os.path.join(d, f)
            rel = os.path.relpath(p, code).replace(os.sep, "/")
            with open(p, "rb") as fh:
                blob = fh.read()
            rows.append(f"{hashlib.sha256(blob).hexdigest()}  {rel}")
            for i, ln in enumerate(blob.decode("utf-8", errors="replace").splitlines(), 1):
                if SECRET.search(ln):
                    hits.append(f"{rel}:{i}: {ln.strip()[:200]}")
    rows.sort(key=lambda r: r.split("  ", 1)[1])
    manifest = "\n".join(rows) + "\n"
    with open(os.path.join(out, "MANIFEST.sha256"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(manifest)
    with open(os.path.join(out, "scan.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(hits) + ("\n" if hits else ""))
    assert os.path.isfile(os.path.join(code, "requirements.lock")), "the tree holds no requirements.lock"
    assert os.path.isdir(os.path.join(code, "library")), "the tree holds no library/"
    mark = {"commit": full, "tree": tree, "files": len(rows),
            "manifest_sha256": hashlib.sha256(manifest.encode()).hexdigest(), "lineage": None,
            "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with open(os.path.join(out, MARK), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(mark, fh, indent=1)
    return {**mark, "scan_hits": len(hits)}


if __name__ == "__main__":
    print(json.dumps(build(sys.argv[1], sys.argv[2]), indent=1))
