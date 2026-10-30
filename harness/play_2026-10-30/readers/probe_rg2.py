"""READ-ONLY PROBE, item 6's R-g2 (named in the 20:00 post): tests/test_lineage_carry.py's own source,
run in its --on child exactly as main() runs it (the same arms, both seeds pinned), with ONE line
replaced: the bare `assert folded == blob["terms"], "R-g2 terms"` prints what differs (counts,
the keys by lineage._key on each side, and for each differing row the fields that differ with
both values) and stops. The repo file is not touched. argv: repo"""
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
OLD = '    assert folded == blob["terms"], "R-g2 terms"\n'
NEW = (
    '    import json as _j\n'
    '    _kf = [lineage._key(x) for x in f["terms"]]\n'
    '    _kb = [lineage._key(x) for x in blob["terms"]]\n'
    '    _d = []\n'
    '    for _i, (_a, _b) in enumerate(zip(folded, blob["terms"])):\n'
    '        if _a != _b:\n'
    '            _ks = sorted(k for k in set(_a) | set(_b) if _a.get(k) != _b.get(k))\n'
    '            _d.append({"i": _i, "keys": _ks, "fold": {k: _a.get(k) for k in _ks},\n'
    '                       "blob": {k: _b.get(k) for k in _ks}})\n'
    '    print("OUT " + _j.dumps({"n_fold": len(folded), "n_blob": len(blob["terms"]),\n'
    '                             "same_keys_in_order": _kf == _kb,\n'
    '                             "same_key_sets": sorted(_kf) == sorted(_kb),\n'
    '                             "fold_only": sorted(set(_kf) - set(_kb))[:5],\n'
    '                             "blob_only": sorted(set(_kb) - set(_kf))[:5],\n'
    '                             "n_diff": len(_d), "diffs": _d[:6]}, default=str), flush=True)\n'
    '    raise SystemExit(0)\n')
assert src.count(OLD) == 1, "the probe's anchor line moved"
src = src.replace(OLD, NEW)
sys.argv = [path, "--on"]
g = {"__name__": "__main__", "__file__": path}
exec(compile(src, path, "exec"), g)
'''
env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
env.update(TETHER_LINEAGE_CARRY="1", TETHER_LINEAGE_HOLD="1", TETHER_AGENT_SEED="0",
           PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
test = os.path.join(repo, "tests", "test_lineage_carry.py")
r = subprocess.run([sys.executable, "-B", "-c", CHILD, test], env=env, cwd=os.path.join(repo, "tests"),
                   capture_output=True, text=True, stdin=subprocess.DEVNULL)
out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
print("\n".join(ln for ln in r.stdout.splitlines() if not ln.startswith("OUT "))[-2000:])
print(out[-1][:8000] if out else "NO OUT LINE")
print("rc", r.returncode, r.stderr[-2500:] if r.returncode else "")
