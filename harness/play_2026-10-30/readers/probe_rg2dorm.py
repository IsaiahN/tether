"""READ-ONLY PROBE, item 6's R-g2 dormant (named in the 20:28 post): tests/test_lineage_carry.py's
own source, run in its --on child exactly as main() runs it (the same arms, both seeds pinned),
with ONE line replaced: `assert f["dormant"] == ag._dormant, "R-g2 dormant"` prints the counts,
whether the fold equals lineage.dec(lineage.enc(x)) of the agent's record (the write's own round
trip), the first differing item on each side, and the item types; then stops. argv: repo"""
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
OLD = '    assert f["dormant"] == ag._dormant, "R-g2 dormant"\n'
NEW = (
    '    import json as _j\n'
    '    _fa, _ga = f["dormant"], ag._dormant\n'
    '    _rt = [lineage.dec(lineage.enc(x)) for x in _ga]\n'
    '    _i = next((i for i, (a, b) in enumerate(zip(_fa, _ga)) if a != b), None)\n'
    '    print("OUT " + _j.dumps({"n_fold": len(_fa), "n_agent": len(_ga),\n'
    '        "fold_equals_enc_dec_of_agent": _fa == _rt, "first_diff": _i,\n'
    '        "fold_i": repr(_fa[_i])[:700] if _i is not None else None,\n'
    '        "agent_i": repr(_ga[_i])[:700] if _i is not None else None,\n'
    '        "types_fold": sorted({type(x).__name__ for x in _fa}),\n'
    '        "types_agent": sorted({type(x).__name__ for x in _ga})}, default=str), flush=True)\n'
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
r = subprocess.run([sys.executable, "-B", "-c", CHILD, test], env=env,
                   cwd=os.path.join(repo, "tests"), capture_output=True, text=True,
                   stdin=subprocess.DEVNULL)
out = [ln for ln in r.stdout.splitlines() if ln.startswith("OUT ")]
print(out[-1][:6000] if out else "NO OUT LINE")
print("rc", r.returncode, r.stderr[-2500:] if r.returncode else "")
