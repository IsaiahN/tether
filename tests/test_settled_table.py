"""C, THE SETTLED TABLE (the reviewer 2026-10-11 09:28, 13:17 CDT): every entry of
relations.SETTLED is a library entry, and its binding EXECUTES -- an atom Gamma holds, a published
reading, a condition that compiles, a callable that reads it -- or it is named UNBOUND. The orphan
list for ALL-ON is printed, and the MULTI-ATOM bindings (a compiled chain of 2+ atoms, the only
case where settled would change reach through units()) are counted and named.

  s1 every key is a library entry (inherited.entry);
  s2 every bound entry resolves; MUST-FAIL: a broken row (an atom Gamma lacks) is reported;
  s3 the UNBOUND list and the multi-atom list, printed.

    python tests/test_settled_table.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import importlib, json, sys
sys.dont_write_bytecode = True
import arc_atoms, compile_term, inherited, relations
from test_goal_condition import _agent
ag = _agent()
atoms = {a.name: a for a in ag.gamma.atoms}

def resolve(row):
    kind, what = row[0], row[1]
    if kind == "atom":
        return all(n in atoms for n in what), 1
    if kind == "reading":
        return all(r in relations.PAIR_RELATIONS or r in arc_atoms.ATTRIBUTE_TYPE for r in what), 0
    if kind == "compose":
        c = compile_term.compile_candidate({"condition": what}, atoms)
        return isinstance(c, compile_term.Compiled), len(c.term.atoms) if hasattr(c, "term") else 0
    if kind == "agent":
        mod, _, rest = what.partition(".")
        obj = importlib.import_module(mod)
        for part in rest.split("."):
            obj = getattr(obj, part, None)
            if obj is None:
                return False, 0
        return callable(obj), 0
    return None, 0

out = {"missing_entry": [k for k in relations.SETTLED if inherited.entry(k) is None],
       "kinds": {}, "unresolved": [], "unbound": [], "multi": []}
for k, row in relations.SETTLED.items():
    out["kinds"][row[0]] = out["kinds"].get(row[0], 0) + 1
    ok, length = resolve(row)
    if ok is None:
        out["unbound"].append([k, row[1]])
    elif not ok:
        out["unresolved"].append(k)
    elif length >= 2:
        out["multi"].append([k, row[1], length])
out["mustfail"] = resolve(("atom", ("no_such_atom",)))[0]
out["n"] = len(relations.SETTLED)
print(json.dumps(out))
'''


def main() -> int:
    env = dict(os.environ, TETHER_RELATION_SET="1", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=_repo.ROOT, timeout=300)
    assert p.returncode == 0, p.stderr[-2500:]
    out = json.loads(p.stdout.strip().splitlines()[-1])
    assert not out["missing_entry"], out["missing_entry"]
    print(f"  s1 {out['n']} entries, every one a library entry; kinds {out['kinds']}")
    assert out["mustfail"] is False, out
    assert not out["unresolved"], out["unresolved"]
    print("  s2 every bound entry resolves (must-fail: a missing atom is caught)")
    print(f"  s3 UNBOUND, for the ALL-ON orphan check ({len(out['unbound'])}):")
    for k, why in out["unbound"]:
        print(f"       {k}: {why}")
    print(f"     MULTI-ATOM bindings ({len(out['multi'])}): {out['multi']}")
    print("settled table: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
