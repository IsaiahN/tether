"""THE PLANTED LIFE for the pair-table merge fix (the seat 10:25-10:26; the reviewer 10:13 item 3). READ ONLY on a
lineage copy; writes ONLY into an empty output folder. Two memory saves, each named by the sha256 of its own bytes in
lineage._dumps' form, so lineage.load and lineage_store.catch_up accept them:
  G1 = the copy's ROOT save (parent None) as a SET-FORM generation: "kinds_landed_n" removed, all else kept
  G2 = a minimal COUNTED child of G1 (every record field empty) whose kinds are, from G1's kinds_landed:
       A  an existing key, landed again and counted (kinds_landed and kinds_landed_n, n 2)
       B  an existing key, in kinds_landed only (known, no count in this save)
       C  a NEW key (A's entry under a planted role) in kinds_landed only: known with NO count anywhere (has_n 0)
       D  a NEW key (B's entry under a planted role) in kinds_landed and kinds_landed_n, n 3
       kinds_last for A, C and D, with seqs past G1's largest
Printed: the two names, and each planted key.
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
e = [a[0], "PLANTED_E", b[2], b[3]]   # counted, in NO kinds_landed: in_landed 0 (the reviewer 10:31)
seq = max(x[7] for x in root["kinds_last"]) + 1
g2 = {k: ([] if isinstance(v, list) else {} if isinstance(v, dict) else v) for k, v in root.items()}
g2.update({"parent": h1, "kinds_landed": [a, b, c, d], "kinds_landed_n": [[*a, 2], [*d, 3], [*e, 4]],
           "kinds_last": [[*a, "planted", 0, 0, seq], [*c, "planted", 0, 0, seq + 1], [*d, "planted", 0, 0, seq + 2],
                          [*e, "planted", 0, 0, seq + 3]]})
h2 = put(g2)
print("PLANTED", f"G1 gen_{h1}.json (set form, from root)", f"G2 gen_{h2}.json (parent {h1})", sep="\t")
for tag, k in (("A", a), ("B", b), ("C", c), ("D", d), ("E", e)):
    print("KEY", tag, json.dumps(k)[:200], sep="\t")
