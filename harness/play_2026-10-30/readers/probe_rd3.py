"""READ-ONLY PROBE, item 6's R-d3 (named in the 19:03 post): test_index_carry's role a through the
test's own child, then role b with _fresh replaced by a comparison of the carried compile
(tether._INDEX_STORE) against (0) the test's reference, compiled with no subject, and (1) the
compile as tether._held_index makes it (subject PH_O / PH_X under TETHER_LIBRARY_ABDUCE).
CONTROL: (1) compiled twice must be equal to itself, or == on a compile is identity and every
comparison reads 'differs' for the wrong reason. argv: repo"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo = sys.argv[1]
tmp = Path(tempfile.mkdtemp(prefix="rd3_")) / "same"
env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
env.update(TETHER_LINEAGE_CARRY="1", TETHER_INDEX_HOLD="1", PYTHONDONTWRITEBYTECODE="1")
r = subprocess.run([sys.executable, "-B", os.path.join(repo, "tests", "test_index_carry.py"),
                    "--role", "a", str(tmp)], env=env, cwd=repo, capture_output=True, text=True,
                   stdin=subprocess.DEVNULL)
print(r.stdout.strip())
assert r.returncode == 0, r.stderr[-2000:]

CHILD = r'''
import json, os, sys
sys.dont_write_bytecode = True
repo, d = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(repo, "tests"))
sys.path.insert(0, repo)
os.chdir(repo)
import test_index_carry as T
import compile_term, tether
res = {"pairs": 0, "diff_nosubj": 0, "diff_subj": 0, "self_diff": 0, "first_subj": None,
       "first_nosubj": None, "abduce": tether._LIBRARY_ABDUCE}


def fresh2(ag, sig, pairs, label):
    lib, atoms = tether._library(), {a.name: a for a in ag.gamma.atoms}

    def c0(cond):
        return compile_term.compile_candidate({"condition": cond}, atoms)

    def c1(cond, subject):
        return compile_term.compile_candidate(
            {"condition": cond}, atoms, subject=subject if tether._LIBRARY_ABDUCE else None)

    def build(f, subj):
        out = []
        for c in lib.view(key, role, tether.PH_O, tether.PH_X):
            if role == "CAUSE":
                out.append((c, f(c["if"], tether.PH_O) if subj else f(c["if"]),
                            f(c["then"], tether.PH_X) if subj else f(c["then"])))
            else:
                out.append((c, None if "quantifier" in c else
                            (f(c["condition"], tether.PH_O) if subj else f(c["condition"])), None))
        return out
    for key, role in sorted(pairs):
        held = tether._INDEX_STORE[(sig, key, role)]
        f0, f1, f1b = build(c0, False), build(c1, True), build(c1, True)
        res["pairs"] += 1
        if f1 != f1b:
            res["self_diff"] += 1
        if held != f0:
            res["diff_nosubj"] += 1
            res["first_nosubj"] = res["first_nosubj"] or [key, role]
        if held != f1:
            res["diff_subj"] += 1
            res["first_subj"] = res["first_subj"] or [key, role]


T._fresh = fresh2
T.role_b(d)
print("OUT " + json.dumps(res))
'''
r = subprocess.run([sys.executable, "-B", "-c", CHILD, repo, str(tmp)], env=env, cwd=repo,
                   capture_output=True, text=True, stdin=subprocess.DEVNULL)
print(r.stdout.strip()[-3000:])
assert r.returncode == 0, r.stderr[-3000:]
