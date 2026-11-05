"""BUILD 3 ITEM 9b (TETHER_ATTR_GROUP; the reviewer 2026-11-04 r1157). Item 9's bridge also reads
FORCE / SIGNAL (inherited.READING_CLUSTER_DERIVED, from the members' own attributes) and the build's
grouping of the PERCEPT atoms the corpus index files under no cluster (index by_cluster_derived).
Seconds: the real library, loaded through tether._library with the arm as set.

MF-G1  a FORCE member gains "contact" and a SIGNAL member gains "press" -- readings item 9 could not
       give them, since K1's table names no reading for either cluster
MF-G2  a formerly unclustered atom is grouped into a cluster with its reason (two or more shared
       attributes, r1159), and gains a reading of that cluster
MF-G3  the grouping accounts for every unclustered PERCEPT atom once (assigned + candidates + new
       clusters + unshared + no attribute) and was derived from the hash-checked corpus file
MF-G4  a candidate (one shared attribute, r1159) is recorded with its reason and gains no reading
The red is behavioural, the arm OFF on this tree: TETHER_ATTR_GROUP=0 fails MF-G1.

    python tests/test_attr_group.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import inherited  # noqa: E402
import tether  # noqa: E402


def gains(lib, raw, cluster, reading):
    """members gaining `reading` that neither held it as built nor sit in a cluster K1's own
    table maps it to -- so item 9's bridge could not have given it"""
    bc, _why = inherited.by_cluster()
    k1 = {k for c in inherited.READING_CLUSTER.get(reading, ()) for k in bc.get(c, ())}
    return [k for k in bc[cluster] if (lib.get(k) or {}).get("kind") == "PERCEPT"
            and k not in k1 and reading not in (raw.get(k).get("reads") or [])
            and (lib.get(k).get("reads_weight") or {}).get(reading) == 0.5]


def main():
    lib = tether._library()
    import library_runtime  # noqa: E402  on sys.path once _library ran
    raw = library_runtime.Library(os.path.join(tether.LIBRARY_HOME, "library")).load()
    tally = getattr(lib, "attr_bridge", {})
    force, signal = gains(lib, raw, "FORCE", "contact"), gains(lib, raw, "SIGNAL", "press")
    assert force and signal, ("MF-G1: FORCE / SIGNAL members gain no reading", tally)
    print(f"  MF-G1 FORCE members gaining contact {len(force)}, SIGNAL members gaining press "
          f"{len(signal)}")
    d = lib.cluster_derived
    bc, _why = inherited.by_cluster()
    filed = {k for ks in bc.values() for k in ks}
    cr = {c: {r for r, cs in inherited.READING_CLUSTER.items() if c in cs}
          | {r for r, (c2, _w) in inherited.READING_CLUSTER_DERIVED.items() if c2 == c}
          for c, _w in d["assigned"].values()}
    k, c, why, r = next((k, c, why, r) for k, (c, why) in sorted(d["assigned"].items())
                        for r in sorted(cr[c]) if r not in (raw.get(k).get("reads") or []))
    assert k not in filed and why.startswith("shares ") and why.count(",") >= 1 and \
        r in lib.get(k)["reads"], ("MF-G2", k, c, why, lib.get(k).get("reads"))
    print(f"  MF-G2 {k} -> {c} ({why}); reads {r}")
    cand = d["candidate"]
    assert cand and all(w.startswith("candidate (1 shared: ") for _c, w in cand.values()) and all(
        (lib.get(k).get("reads") or []) == (raw.get(k).get("reads") or []) for k in cand), (
        "MF-G4", len(cand))
    print(f"  MF-G4 {len(cand)} candidates recorded (one shared), none gains a reading")
    loose = sorted(k for k, e in lib.seed.items() if e.get("kind") == "PERCEPT" and k not in filed)
    seen = sorted([*d["assigned"], *d["candidate"], *(x for v in d["new"].values() for x in v),
                   *d["unshared"], *d["bare"]])
    assert seen == loose and d["sha256"] == inherited.INDEX_SHA, ("MF-G3", len(seen), len(loose))
    print(f"  MF-G3 {len(loose)} unclustered: assigned {len(d['assigned'])}, candidates "
          f"{len(d['candidate'])}, new clusters "
          f"{len(d['new'])} holding {sum(map(len, d['new'].values()))}, unshared "
          f"{len(d['unshared'])}, no attribute {len(d['bare'])}; tally {tally}")
    print("test_attr_group OK")


if __name__ == "__main__":
    main()
