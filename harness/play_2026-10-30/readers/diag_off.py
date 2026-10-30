import io, json, os, subprocess, sys, tarfile, tempfile
sys.dont_write_bytecode = True
ROOT = "C:/Users/Admin/Documents/GitHub/tether"
sys.path[:0] = [ROOT + "/tests", ROOT + "/conform"]
import test_arrival_gap as T
from identity_mod_rows import mask_timings
def norm(rows):
    return [(r["cycle"], r["step"], r["slot"], r["event"], json.dumps(r["detail"], sort_keys=True, default=str))
            for r in mask_timings(json.loads(json.dumps(rows))) if r["event"] != "arms"]
with tempfile.TemporaryDirectory() as d:
    tar = subprocess.run(["git", "-C", ROOT, "archive", "d12c74e"], capture_output=True, check=True)
    with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
        tf.extractall(d, filter="data")
    b1 = norm(T.child(d, "plain", 0)["rows"]); b2 = norm(T.child(d, "plain", 0)["rows"])
    c1 = norm(T.child(ROOT, "plain", 0, {"TETHER_ARRIVAL_GAP": "0"})["rows"])
for name, x, y in (("base vs base", b1, b2), ("base vs off", b1, c1)):
    idx = [i for i, (p, q) in enumerate(zip(x, y)) if p != q]
    print(name, "differing rows:", len(idx), idx[:10])
    for i in idx[:2]:
        print("  A", x[i]); print("  B", y[i])
