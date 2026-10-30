import glob
import json
import os
import sys
import zlib

L = sys.argv[1]
for pre in ("gen_", "ak_", "idx_"):
    fs = sorted(glob.glob(os.path.join(L, pre + "*")), key=os.path.getmtime)
    sizes = [os.path.getsize(f) for f in fs]
    f = fs[-1]
    b = open(f, "rb").read()
    try:
        raw = zlib.decompress(b)
        comp = "zlib"
    except zlib.error:
        raw, comp = b, "none"
    d = json.loads(raw)
    keys = list(d)[:20] if isinstance(d, dict) else type(d).__name__
    print(f"{pre}: {len(fs)} files, {sum(sizes) / 1e6:.1f} MB total, newest {os.path.basename(f)} "
          f"{len(b) / 1e6:.2f} MB on disk ({comp}) -> {len(raw) / 1e6:.2f} MB raw JSON; keys {keys}")
