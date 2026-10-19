"""S5 (c)'s SYNTHETIC COUNTER, prepared once (the reviewer 2026-10-19 09:36 item 3c). READ ONLY on a real ak_ file:
E4a's bp35 save (ak_74097298538ebcfe_*.json, 2,338,760 rows). Its first 2,267,962 rows (bp35's counter at the
probe's save) become counter keys (tok "T", sig, key, role, o, x, slot), every string interned through one pool so
they are shared as the agent's are. n follows bp35's measured distribution (999 at 7, 999 at 5, 960 at 3, 1,546 at
2, the rest 1), placed by random.Random(20261019). sig = (that file's sig_arm, tuple of its sig_atoms): its repr is
as long as the real signature's. Pickled (protocol 5) for synth_ak.py, so no measured process parses the json.
argv: ak_file out_pickle"""
import json
import pickle
import random
import sys

AK, OUT = sys.argv[1:3]
N = 2267962
DIST = [(7, 999), (5, 999), (3, 960), (2, 1546)]
with open(AK, encoding="utf-8") as fh:
    body = json.load(fh)
ents = body["entries"]
assert len(ents) >= N, f"{len(ents)} rows < {N}"
pool: dict = {}


def s(x):
    return None if x is None else pool.setdefault(x, x)


sig = (body["sig_arm"], tuple(body["sig_atoms"]))
keys = [("T", sig, s(e["key"]), s(e["role"]), s(e["o"]), s(e["x"]), s(e["slot"])) for e in ents[:N]]
del body, ents
ns = [1] * N
idx = list(range(N))
random.Random(20261019).shuffle(idx)
i = 0
for n, c in DIST:
    for j in idx[i:i + c]:
        ns[j] = n
    i += c
assert len(set(keys)) == N, "the rows must be distinct"
with open(OUT, "wb") as fh:
    pickle.dump({"sig": sig, "items": list(zip(keys, ns, strict=True))}, fh, protocol=5)
print("PREP", f"entries {N}", f"sum n {sum(ns)}", f"strings pooled {len(pool)}",
      f"sig repr chars {len(repr(sig))}", sep="\t")
