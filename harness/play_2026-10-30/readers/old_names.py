"""The old pool's references by ORIGINAL path (the reviewer 2026-10-23 02:13): every git-tracked text file at the frozen
tree (wt_ivv, 665754f) and the main checkout searched for (1) the two session ids and the tether_saves folder, (2) each
moved file's original path tail (from the session's scratchpad/ on; runs/<name> for the Documents root; the bare file
name for tether_saves), with / and \ both tried. Per hit: the file, the line, and the pool files it names.
argv: tombstone_jsonl out_tsv"""
import json, os, re, subprocess, sys
from collections import defaultdict
sys.dont_write_bytecode = True
TOMB, OUT = sys.argv[1:3]
ents = [json.loads(x) for x in open(TOMB, encoding="utf-8") if x.strip()][1:]
tails = {}
for e in ents:
    p = e["path"].replace("\\", "/")
    if "/scratchpad/" in p:
        t = "scratchpad/" + p.split("/scratchpad/", 1)[1]
    elif "/Documents/GitHub/tether/" in p:
        t = p.split("/Documents/GitHub/tether/", 1)[1]
    elif "/tether_saves/" in p:
        t = "tether_saves/" + p.split("/tether_saves/", 1)[1]
    else:
        t = p
    tails[t] = e["holding"]
sessions = sorted({m.group(0) for e in ents for m in [re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", e["path"])] if m})
print("entries", len(ents), "tails", len(tails), "sessions", sessions)
hits = defaultdict(set)
for repo in ("C:/TETHER_RUNS/S6_2026-10-19/wt_ivv", "C:/Users/Admin/Documents/GitHub/tether"):
    files = subprocess.run(["git", "-C", repo, "ls-files"], capture_output=True, text=True).stdout.split("\n")
    for f in files:
        if not f or not f.endswith((".py", ".md", ".txt", ".tsv", ".json", ".jsonl", ".sh", ".toml", ".cfg")):
            continue
        p = os.path.join(repo, f)
        try:
            if os.path.getsize(p) > 8 * 2**20:
                continue
            t = open(p, encoding="utf-8", errors="replace").read().replace("\\\\", "/").replace("\\", "/")
        except OSError:
            continue
        for s in sessions + ["tether_saves"]:
            if s in t:
                hits[(repo, f)].add("token:" + s[:8])
        for tail, hold in tails.items():
            if tail in t:
                hits[(repo, f)].add(tail)
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    for (repo, f), ts in sorted(hits.items()):
        named = sorted(x for x in ts if not x.startswith("token:"))
        toks = sorted(x for x in ts if x.startswith("token:"))
        fh.write(f"{repo}\t{f}\t{len(named)}\t{' '.join(toks)}\t{' | '.join(named)}\n")
        print(f"{os.path.basename(repo)}\t{f}\tpool files named {len(named)}\t{toks}\t{named[:4]}")
