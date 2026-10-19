"""E5.1 PACKAGE, LOCAL (the reviewer 2026-10-19 02:09 item 2a): E4a's 25 games plus the probe in one folder with an
index. READ ONLY on the run folders: the small files are COPIED into the package; the ledgers are REFERENCED by path,
size and sha256 (not copied). Nothing is uploaded. argv: e4_dir out_dir"""
import hashlib
import json
import os
import shutil
import sys

E4, OUT = sys.argv[1], sys.argv[2]
assert not os.path.exists(OUT), "the package folder already exists"
os.makedirs(OUT)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


rows = {}
with open(os.path.join(E4, "results.tsv"), encoding="utf-8") as fh:
    for ln in fh:
        f = ln.rstrip("\n").split("\t")
        if f[0] == "public" and len(f) > 2:
            rows.setdefault((f[1], f[2]), []).append(ln.rstrip("\n"))   # EVERY row kept; none chosen silently
index = ["# E5.1 package (local), built from " + E4,
         "# kind\tidx\tgame\tfile\tbytes\tsha256\tnote"]
for d in sorted(os.listdir(os.path.join(E4, "public"))):
    idx, g = d.split("_", 1)
    src = os.path.join(E4, "public", d)
    dst = os.path.join(OUT, "games", d)
    os.makedirs(dst)
    for n in (f"{g}.result.json", "sup/sup.json", "sup.json", f"{g}.commit.tsv", "sup.log", "mem.tsv"):
        p = os.path.join(src, n)
        if os.path.isfile(p):
            shutil.copy2(p, os.path.join(dst, os.path.basename(n)))
            index.append(f"copy\t{idx}\t{g}\t{os.path.join('games', d, os.path.basename(n))}\t{os.path.getsize(p)}\t"
                         f"{sha(p)}\t")
    led = os.path.join(src, f"{g}.jsonl")
    if os.path.isfile(led):
        index.append(f"ref\t{idx}\t{g}\t{led}\t{os.path.getsize(led)}\t{sha(led)}\tledger, not copied")
    gen = None
    try:
        with open(os.path.join(src, f"{g}.result.json"), encoding="utf-8") as fh:
            gen = str(json.load(fh).get("lineage"))[:120]
    except (OSError, ValueError):
        gen = "no result.json (no lineage written)"
    for row in rows.get((str(int(idx)), g)) or rows.get((idx, g)) or ["NO ROW"]:
        index.append(f"row\t{idx}\t{g}\tresults.tsv\t\t\t{row}")
    index.append(f"lineage\t{idx}\t{g}\t\t\t\t{gen}")
P = os.path.join(E4, "stream_probe")
pd = os.path.join(OUT, "probe")
os.makedirs(pd)
for n in ("switch.tsv", "stream.jsonl.body.jsonl", "launcher.txt", "pyspy_a.txt", "pyspy_b.txt", "sup/sup.json",
          "sup/sup.log", "sup/mem.tsv"):
    p = os.path.join(P, n)
    if os.path.isfile(p):
        shutil.copy2(p, os.path.join(pd, n.replace("/", "_")))
        index.append(f"copy\tprobe\t-\t{os.path.join('probe', n.replace('/', '_'))}\t{os.path.getsize(p)}\t{sha(p)}\t")
pl = os.path.join(P, "stream.jsonl")
index.append(f"ref\tprobe\t-\t{pl}\t{os.path.getsize(pl)}\t{sha(pl)}\tledger, not copied")
with open(pl, encoding="utf-8") as fh, open(os.path.join(pd, "fold_rows.jsonl"), "w", encoding="utf-8") as out:
    nf = 0
    for ln in fh:
        if '"@consolidate"' in ln and '"consolidate"' in ln:
            out.write(ln)
            nf += 1
index.append(f"extract\tprobe\t-\tprobe/fold_rows.jsonl\t\t\t{nf} ledger @consolidate rows")
for n in ("results.tsv", "NOTES.md", "e4b_seed.txt", "lineage_probe_copy.manifest.tsv"):
    p = os.path.join(E4, n)
    if os.path.isfile(p):
        shutil.copy2(p, os.path.join(OUT, n))
        index.append(f"copy\trun\t-\t{n}\t{os.path.getsize(p)}\t{sha(p)}\t")
with open(os.path.join(OUT, "INDEX.tsv"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(index) + "\n")
print("games", len(os.listdir(os.path.join(OUT, "games"))), "index rows", len(index) - 2, "fold rows", nf)
