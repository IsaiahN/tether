"""READ-ONLY PROBE, item 6's R-g2 WIDENED (the reviewer 2026-10-22 20:32): tests/test_lineage_carry.py's
own source, run in its --on child exactly as main() runs it (the same arms, both seeds pinned).
R-g2's remaining asserts (dormant, vindication, book, invented, the gap set, refused, standing:
lines 215-223) are replaced by a block that RECORDS each one's result with what differs and
prints it, then the rest of the test runs on unchanged, so any later section's failure shows in
the same run. The repo file is not touched. argv: repo"""
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo = sys.argv[1]
CHILD = r'''
import os, sys
sys.dont_write_bytecode = True
path = sys.argv[1]
src = open(path, encoding="utf-8").read().replace("\r\n", "\n")
OLD = """    assert f["dormant"] == ag._dormant, "R-g2 dormant"
    for k in ("vindication", "book", "invented"):
        assert f[k] == blob[k], ("R-g2", k)
    env, agb, repb = _agent(rr, 4)
    _carries(blob["terms"], agb, repb, "R-g2 gap beyond the named set")
    assert not repb["refused"], ("R-g2 gap", repb["refused"])
    for t in _held(agb).values():
        st = agb.gamma.standing.get(t.name)
        assert st is None or not st.settled_on, ("R-g2 standing crossed", t.name)
"""
NEW = """    import json as _j
    _R = {}

    def _cmp(a, b):
        out = {"equal": a == b, "types": [type(a).__name__, type(b).__name__]}
        if hasattr(a, "__len__") and hasattr(b, "__len__"):
            out["n"] = [len(a), len(b)]
        if out["equal"]:
            return out
        if isinstance(a, dict) and isinstance(b, dict):
            ks = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
            out["keys_differ"] = len(ks)
            out["first"] = [{"k": repr(k)[:120], "fold": repr(a.get(k))[:300],
                             "agent": repr(b.get(k))[:300]} for k in ks[:3]]
        elif isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
            i = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
            out["first_i"] = i
            if i is not None:
                out["fold_i"], out["agent_i"] = repr(a[i])[:500], repr(b[i])[:500]
                out["types_i"] = [type(a[i]).__name__, type(b[i]).__name__]
        return out
    _R["dormant"] = _cmp(f["dormant"], ag._dormant)

    def _where(x, path=()):
        # the key path to the first value lineage.enc has no form for
        try:
            lineage.enc(x)
            return None
        except lineage.Unencodable:
            pass
        if isinstance(x, dict):
            for k, v in x.items():
                p = _where(v, path + (repr(k)[:60],))
                if p is not None:
                    return p
        elif isinstance(x, (list, tuple, set, frozenset)):
            for i, v in enumerate(x):
                p = _where(v, path + (i,))
                if p is not None:
                    return p
        return list(path) + [type(x).__name__]
    _ok, _bad = [], []
    for _i2, _x in enumerate(ag._dormant):
        try:
            _ok.append(lineage.dec(lineage.enc(_x)))
        except lineage.Unencodable as _u:
            _bad.append({"i": _i2, "why": str(_u), "path": _where(_x),
                         "item_keys": sorted(map(str, _x))[:20] if isinstance(_x, dict) else None,
                         "item": repr(_x)[:400]})
    _R["dormant"]["unencodable_n"] = len(_bad)
    _R["dormant"]["unencodable"] = _bad[:4]
    _R["dormant"]["fold_equals_encodable_part"] = f["dormant"] == _ok
    _gfile = _j.loads(lineage_store.file_bytes(Path(rr) / f"gen_{_h}.json"))
    _R["dormant"]["gen_dormant_refused"] = _gfile.get("dormant_refused")
    for k in ("vindication", "book", "invented"):
        _R[k] = _cmp(f[k], blob[k])
    env, agb, repb = _agent(rr, 4)
    try:
        _carries(blob["terms"], agb, repb, "R-g2 gap beyond the named set")
        _R["gap"] = "ok"
    except AssertionError as _e:
        _R["gap"] = repr(_e)[:800]
    _R["refused"] = repr(repb.get("refused"))[:500]
    _R["standing_crossed"] = [t.name for t in _held(agb).values()
                              if (agb.gamma.standing.get(t.name) is not None
                                  and agb.gamma.standing.get(t.name).settled_on)][:10]
    print("OUT " + _j.dumps(_R, default=str), flush=True)
"""
assert src.count(OLD) == 1, "the probe's anchor block moved"
src = src.replace(OLD, NEW)
sys.argv = [path, "--on"]
g = {"__name__": "__main__", "__file__": path}
exec(compile(src, path, "exec"), g)
print("PROBE-END reached the test's end")
'''
env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
env.update(TETHER_LINEAGE_CARRY="1", TETHER_LINEAGE_HOLD="1", TETHER_AGENT_SEED="0",
           PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
test = os.path.join(repo, "tests", "test_lineage_carry.py")
r = subprocess.run([sys.executable, "-B", "-c", CHILD, test], env=env,
                   cwd=os.path.join(repo, "tests"), capture_output=True, text=True,
                   stdin=subprocess.DEVNULL)
print(r.stdout[-9000:])
print("rc", r.returncode)
print(r.stderr[-3000:] if r.returncode else "")
