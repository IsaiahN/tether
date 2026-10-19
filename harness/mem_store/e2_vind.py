"""E2, THE APPEND-ONLY TABLES ON A PLANTED LIFE (the reviewer 2026-10-19 11:27 item 2). This life has ZERO vindication
rows, so a planted 2-save chain is written from a lineage COPY's root (read only) into an empty folder: G1 = the root
with vindication_tail [101, 102] and its own seed; G2 = a minimal child (every record field empty) with vindication_tail
[201, 202, 203], two planted evidence rows, and a seed. Each gen_ named by the sha256 of its bytes (lineage._dumps).
A store is built there by lineage_store.open_store + catch_up (REPO's code). Compared N/N with lineage.fold over the
same chain: vindication (ORDER BY k, i) and evidence (ORDER BY k, i); meta n_vindication = len(vindication); the seeds
in save order; and the fold blob holds NO evidence / vindication key and the counts blob NO seeds key. The MUST-FAIL:
the same rows read ORDER BY i, k (the saves interleaved) must DIFFER from fold's list.
argv: repo lineage_copy out_dir"""
import hashlib
import json
import os
import sqlite3
import sys

REPO, LIN, OUT = sys.argv[1:4]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
import lineage  # noqa: E402
import lineage_store as ls  # noqa: E402

assert not os.path.exists(OUT), "the output folder must not exist"
root = None
for f in sorted(os.listdir(LIN)):
    if f.startswith("gen_") and f.endswith(".json"):
        with open(os.path.join(LIN, f), encoding="utf-8") as fh:
            g = json.load(fh)
        if g.get("parent") is None:
            root = g
assert root is not None, "no root"
os.makedirs(OUT)


def put(g: dict) -> str:
    raw = lineage._dumps(g)
    h = hashlib.sha256(raw).hexdigest()[:16]
    with open(os.path.join(OUT, f"gen_{h}.json"), "xb") as fh:
        fh.write(raw)
    return h


g1 = dict(root)
g1.update({"vindication_tail": [101, 102], "seed": "PLANTED_SEED_1"})
h1 = put(g1)
g2 = {k: ([] if isinstance(v, list) else {} if isinstance(v, dict) else v) for k, v in root.items()}
g2.update({"parent": h1, "vindication_tail": [201, 202, 203], "seed": "PLANTED_SEED_2",
           "evidence": [{"planted": 1, "v": "a"}, {"planted": 2, "v": "b"}]})
h2 = put(g2)
con = ls.open_store(OUT)
merged = ls.catch_up(con, OUT)
con.close()
chain = lineage._chain(__import__("pathlib").Path(OUT))
fo = lineage.fold(chain)
c = sqlite3.connect(f"file:{os.path.join(OUT, ls.DB)}?mode=ro", uri=True)
vind = [json.loads(r) for (r,) in c.execute("SELECT row FROM vindication ORDER BY k, i")]
vind_bad = [json.loads(r) for (r,) in c.execute("SELECT row FROM vindication ORDER BY i, k")]
evid = [json.loads(r) for (r,) in c.execute("SELECT row FROM evidence ORDER BY k, i")]
seeds = [json.loads(s) for (s,) in c.execute("SELECT seed FROM seeds ORDER BY k")]
nv = c.execute("SELECT v FROM meta WHERE k='n_vindication'").fetchone()
fold_blob = json.loads(c.execute("SELECT v FROM blob WHERE k='fold'").fetchone()[0])
counts_blob = json.loads(c.execute("SELECT v FROM blob WHERE k='counts'").fetchone()[0])
c.close()
print("PLANTED", f"G1 {h1}", f"G2 {h2}", f"merged {len(merged)}", f"chain {len(chain)}", sep="\t")
print("VINDICATION", f"store {vind}", f"fold {fo['vindication']}", f"EQUAL {vind == fo['vindication']}", sep="\t")
print("N_VINDICATION", f"meta {nv[0] if nv else None}", f"len {len(fo['vindication'])}",
      f"EQUAL {str(nv[0] if nv else None) == str(len(fo['vindication']))}", sep="\t")
print("EVIDENCE", f"store {len(evid)}", f"fold {len(fo['evidence'])}", f"EQUAL {evid == fo['evidence']}", sep="\t")
print("SEEDS", f"store {seeds}", f"chain {[g.get('seed') for _h, g in chain if g.get('seed')]}", sep="\t")
print("BLOBS", f"fold keys {sorted(fold_blob)}", f"counts has seeds {'seeds' in counts_blob}", sep="\t")
print("MUST_FAIL", f"ORDER BY i, k gives {vind_bad}", f"DIFFERS {vind_bad != fo['vindication']}", sep="\t")
