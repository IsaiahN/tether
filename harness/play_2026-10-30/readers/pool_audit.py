"""The old pool's pre-empty check (the reviewer 2026-10-23 00:55), READ ONLY: lists, sizes, sha256 byte reads. Never
opens C:/TETHER_RUNS/E4_2026-10-18/lineage; reads the S3O point's manifest.tsv only (names, sizes, shas).
  HOLDS   per top folder and per subtree: files, bytes
  STEP7   manifest.json: entries, declared bytes; each dst present, its size and sha256 equal to the entry
  LINEAGE any pool file whose size AND sha256 equal a manifest row (the pool holding a lineage file's bytes), and any
          pool file name equal to a manifest name
  TEXT    files in the repo checkouts, the memory folder and C:/TETHER_RUNS (lineage excluded) whose text names the
          holding folder or its two pools; only text files under 5 MB are read
argv: out_json"""
import collections
import ctypes
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000)
H = "C:/TETHER_HOLDING"
LIN = os.path.normcase(os.path.abspath("C:/TETHER_RUNS/E4_2026-10-18/lineage"))
MAN = "C:/TETHER_RUNS/S6_2026-10-19/S3O/run/point/manifest.tsv"
out = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


files = []
for root, _dirs, fs in os.walk(H):
    for f in fs:
        p = os.path.join(root, f)
        files.append((os.path.relpath(p, H).replace("\\", "/"), os.path.getsize(p)))
print(f"HOLDS {len(files)} files, {sum(b for _, b in files)} bytes")
for depth in (1, 2, 3, 4):
    agg = collections.defaultdict(lambda: [0, 0])
    for rel, b in files:
        k = "/".join(rel.split("/")[:depth])
        agg[k][0] += 1
        agg[k][1] += b
    out[f"depth{depth}"] = {k: v for k, v in sorted(agg.items())}
    print(f"-- depth {depth}: {len(agg)} keys")
    for k, (n, b) in sorted(agg.items(), key=lambda kv: -kv[1][1])[:25]:
        print(f"   {b / 2**30:8.3f} GiB {n:6d} files  {k}")
ext = collections.Counter()
extb = collections.Counter()
for rel, b in files:
    e = os.path.splitext(rel)[1].lower() or "(none)"
    ext[e] += 1
    extb[e] += b
print("-- by extension (all):", [(e, ext[e], round(extb[e] / 2**30, 3)) for e in sorted(ext, key=lambda x: -extb[x])])

m = json.load(open(os.path.join(H, "2026-10-16_step7_runs", "manifest.json"), encoding="utf-8"))
bad = []
for e in m:
    d = e["dst"]
    if not os.path.exists(d):
        bad.append(("missing", d))
    elif os.path.getsize(d) != e["bytes"]:
        bad.append(("size", d))
    elif sha(d) != e["sha256"]:
        bad.append(("sha", d))
on_disk = [r for r in files if r[0].startswith("2026-10-16_step7_runs/")]
named = {os.path.normcase(e["dst"]) for e in m}
extra = [r for r, _ in on_disk if os.path.normcase(os.path.join(H, r)) not in named and not r.endswith("manifest.json")]
print(f"STEP7 manifest entries {len(m)}, declared bytes {sum(e['bytes'] for e in m)}; on disk {len(on_disk)} files "
      f"{sum(b for _, b in on_disk)} bytes; entries failing {len(bad)} {bad[:5]}; files on disk not in the manifest "
      f"{len(extra)} {extra[:5]}")
out["step7"] = {"entries": len(m), "declared": sum(e["bytes"] for e in m), "bad": bad, "extra": extra}

man = {}
for ln in open(MAN, encoding="utf-8"):
    if ln.strip():
        n, b, s = ln.rstrip("\n").split("\t")
        man[n] = (int(b), s)
sizes = collections.defaultdict(set)
for n, (b, s) in man.items():
    sizes[b].add(s)
cand = [(r, b) for r, b in files if b in sizes]
same = [(r, b) for r, b in cand if sha(os.path.join(H, r)) in sizes[b]]
names = [r for r, _ in files if os.path.basename(r) in man]
print(f"LINEAGE manifest rows {len(man)}; pool files with a manifest size {len(cand)}; byte-identical to a manifest "
      f"row {len(same)} {same[:5]}; pool names equal to a manifest name {len(names)} {names[:5]}")
out["lineage"] = {"size_candidates": len(cand), "same": same, "names": names}

NEEDLES = ("TETHER_HOLDING", "old_pool", "step7_runs")
roots = ["C:/Users/Admin/Documents/GitHub/tether", "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv",
         "C:/Users/Admin/.claude/projects/c--Users-Admin-Documents-GitHub-tether/memory", "C:/TETHER_RUNS"]
TEXT = (".py", ".md", ".txt", ".tsv", ".json", ".jsonl", ".sh", ".toml", ".cfg", ".ini", ".yaml", ".yml", ".out")
hits, seen, read = [], set(), 0
for R in roots:
    for root, dirs, fs in os.walk(R):
        dirs[:] = [d for d in dirs if d not in (".git", ".venv", "__pycache__")
                   and os.path.normcase(os.path.abspath(os.path.join(root, d))) != LIN]
        for f in fs:
            p = os.path.normcase(os.path.abspath(os.path.join(root, f)))
            if p in seen or not f.lower().endswith(TEXT):
                continue
            seen.add(p)
            try:
                if os.path.getsize(p) > 5 * 2**20:
                    continue
                t = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            read += 1
            for nd in NEEDLES:
                if nd in t:
                    hits.append((p, nd, t.count(nd)))
print(f"TEXT read {read} text files under 5 MB in {roots} (the lineage excluded); files naming the pool: {len(hits)}")
for h in hits:
    print(f"   {h}")
out["text"] = hits
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, default=str)
