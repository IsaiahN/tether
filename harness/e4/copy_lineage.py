"""A BYTE COPY of the E4 lineage for the probe (the reviewer 2026-10-19 00:27 item 4): copy every file, then a
manifest (name, bytes, sha256) of SOURCE and of COPY, each hashed; the two must be identical. argv: src dst"""
import hashlib
import os
import shutil
import sys

src, dst = sys.argv[1], sys.argv[2]
assert os.path.isdir(src) and os.listdir(src), "the source lineage is empty"
assert not os.path.exists(dst), "the copy's folder already exists"
shutil.copytree(src, dst)


def manifest(d):
    rows = []
    for n in sorted(os.listdir(d)):
        p = os.path.join(d, n)
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for b in iter(lambda: fh.read(1 << 20), b""):
                h.update(b)
        rows.append(f"{n}\t{os.path.getsize(p)}\t{h.hexdigest()}")
    text = "\n".join(rows) + "\n"
    return text, hashlib.sha256(text.encode()).hexdigest(), len(rows), sum(os.path.getsize(os.path.join(d, n))
                                                                         for n in os.listdir(d))


ts, hs, ns, bs = manifest(src)
td, hd, nd, bd = manifest(dst)
with open(dst + ".manifest.tsv", "w", encoding="utf-8") as fh:
    fh.write(td)
print(f"source {ns} files {bs} B manifest sha256 {hs}")
print(f"copy   {nd} files {bd} B manifest sha256 {hd}")
print("IDENTICAL" if ts == td else "DIFFER")
sys.exit(0 if ts == td else 1)
