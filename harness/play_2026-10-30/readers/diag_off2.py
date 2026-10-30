import io, json, subprocess, sys, tarfile, tempfile, time
sys.dont_write_bytecode = True
ROOT = "C:/Users/Admin/Documents/GitHub/tether"
sys.path[:0] = [ROOT + "/tests", ROOT + "/conform"]
import test_arrival_gap as T
from identity_mod_rows import mask_timings
def norm(rows):
    return [(r["cycle"], r["step"], r["slot"], r["event"], json.dumps(r["detail"], sort_keys=True, default=str))
            for r in mask_timings(json.loads(json.dumps(rows))) if r["event"] != "arms"]
t0 = time.time()
with tempfile.TemporaryDirectory() as d:
    tar = subprocess.run(["git", "-C", ROOT, "archive", "d12c74e"], capture_output=True, check=True)
    with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
        tf.extractall(d, filter="data")
    runs = []
    while time.time() - t0 < 420:
        runs.append(norm(T.child(d if len(runs) % 2 == 0 else ROOT, "plain", 0,
                                 None if len(runs) % 2 == 0 else {"TETHER_ARRIVAL_GAP": "0"})["rows"]))
        ref = runs[0]
        x = runs[-1]
        idx = [i for i, (p, q) in enumerate(zip(ref, x)) if p != q]
        print(f"run {len(runs)} ({'base' if len(runs) % 2 else 'off'}): rows {len(x)}, differing vs run 1: {len(idx)} {idx[:8]}", flush=True)
        if idx:
            for i in idx[:3]:
                print("  R1", ref[i][:4], ref[i][4][:900]); print("  RX", x[i][:4], x[i][4][:900])
            break
