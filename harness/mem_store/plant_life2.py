"""THE PLANTED LIFE v2 for the kind switch (the reviewer 2026-10-19 10:45 item 2 (d), (e)). plant_life.py's two saves
(G1 = the root as SET-FORM; G2 with A, B, C (known, no count), D, E (counted, in no kinds_landed)), PLUS three T2
CANDIDATES in G2 on three DISTINCT REAL entries (from the root's kinds_landed, so the library holds them) under a
PLANTED target kind ["PLANTED_KIND"], which no dk landing names:
  F  (entry1, "MEASURE", PLANTED, PLANTED)     counted, n 5, with a last          target kind_o
  G  (entry2, "MEASURE", PLANTED, PLANTED)     in kinds_landed only: known with NO count (has_n 0)
  H  (entry3, "CAUSE",   A's kind_o, PLANTED)  counted, n 1, with a last          target kind_x (the CAUSE rule)
READ ONLY on the lineage copy; writes ONLY into an empty output folder: the two gen_ files (named by the sha256 of
their bytes in lineage._dumps' form) and planted.json (every planted key, for the harness).
argv: repo lineage_copy out_dir"""
import hashlib
import json
import os
import sys

REPO, LIN, OUT = sys.argv[1:4]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
import lineage  # noqa: E402

assert not os.path.exists(OUT), "the output folder must not exist"
root = None
for f in sorted(os.listdir(LIN)):
    if f.startswith("gen_") and f.endswith(".json"):
        with open(os.path.join(LIN, f), encoding="utf-8") as fh:
            g = json.load(fh)
        if g.get("parent") is None:
            assert root is None, "two roots"
            root = g
assert root is not None, "no root"


def put(g: dict) -> str:
    raw = lineage._dumps(g)
    h = hashlib.sha256(raw).hexdigest()[:16]
    with open(os.path.join(OUT, f"gen_{h}.json"), "xb") as fh:
        fh.write(raw)
    return h


os.makedirs(OUT)
g1 = dict(root)
del g1["kinds_landed_n"]
h1 = put(g1)
a, b = root["kinds_landed"][0], root["kinds_landed"][1]
c = [a[0], "PLANTED_C", a[2], a[3]]
d = [b[0], "PLANTED_D", b[2], b[3]]
e = [a[0], "PLANTED_E", b[2], b[3]]
ents: list = []
for k in root["kinds_landed"]:
    if k[0] not in ents:
        ents.append(k[0])
    if len(ents) == 3:
        break
assert len(ents) == 3, "three distinct entries"
pk = ["PLANTED_KIND"]
f_ = [ents[0], "MEASURE", pk, pk]
g_ = [ents[1], "MEASURE", pk, pk]
h_ = [ents[2], "CAUSE", a[2], pk]
seq = max(x[7] for x in root["kinds_last"]) + 1
g2 = {k: ([] if isinstance(v, list) else {} if isinstance(v, dict) else v) for k, v in root.items()}
g2.update({"parent": h1,
           "kinds_landed": [a, b, c, d, f_, g_, h_],
           "kinds_landed_n": [[*a, 2], [*d, 3], [*e, 4], [*f_, 5], [*h_, 1]],
           "kinds_last": [[*a, "planted", 0, 0, seq], [*c, "planted", 0, 0, seq + 1],
                          [*d, "planted", 0, 0, seq + 2], [*e, "planted", 0, 0, seq + 3],
                          [*f_, "planted", 0, 0, seq + 4], [*h_, "planted", 0, 0, seq + 5]]})
h2 = put(g2)
keys = {"A": a, "B": b, "C": c, "D": d, "E": e, "F": f_, "G": g_, "H": h_, "PLANTED_KIND": pk}
with open(os.path.join(OUT, "planted.json"), "x", encoding="utf-8") as fh:
    json.dump({"G1": h1, "G2": h2, "keys": keys}, fh)
print("PLANTED", f"G1 gen_{h1}.json (set form, from root)", f"G2 gen_{h2}.json (parent {h1})", sep="\t")
for tag, k in keys.items():
    print("KEY", tag, json.dumps(k)[:200], sep="\t")
