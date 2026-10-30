import hashlib
import os

R = "C:/TETHER_RUNS/S6_2026-10-19"
for f in ("library_runtime.py", "readings.json", "atoms.json", "molecules.json", "agent_atoms.json",
          "relations.json", "index.json", "tag_index.json", "domains.json", "runtime.json", "learnings.json"):
    out = []
    for t in ("wt_ivv", "ctl_920dfc7"):
        p = os.path.join(R, t, "library", f)
        if os.path.isfile(p):
            b = open(p, "rb").read()
            out.append((t, hashlib.sha256(b).hexdigest()[:12], len(b), b.count(b"\r\n")))
        else:
            out.append((t, None))
    print(f, out)
