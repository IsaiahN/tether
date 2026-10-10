"""7a(5b) the contact reading: per ledger, how many acted steps had a library term feed the choice,
split by exit (`by`) AND by role (goal / route / body). A READING for the seats; nothing in the
agent reads it, and nothing is pooled across ledgers (Fig 1 :22, Fig 10 :24-26).

    python conform/contact.py runs/panel/*.jsonl
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True


def read(path: Path) -> dict:
    steps = Counter()
    fed = Counter()
    roles = Counter()
    missing = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if '"repeat"' not in line:
            continue
        r = json.loads(line)
        d = r.get("detail") or {}
        if r.get("event") != "repeat" or not d.get("by") or d["by"] == "given":
            continue
        g = d.get("gamma_read") or {}
        if "fed" not in g:
            missing += 1
            continue
        steps[d["by"]] += 1
        if g["fed"]:
            fed[d["by"]] += 1
        for e in g["fed"]:
            roles[(d["by"], e["role"])] += 1
    return {"steps": dict(steps), "fed": dict(fed), "roles": {f"{b}/{r}": n for (b, r), n
                                                               in sorted(roles.items())},
            "no_fed_field": missing}


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        p = Path(arg)
        out = read(p)
        total = sum(out["steps"].values())
        with_fed = sum(out["fed"].values())
        print(f"{p.stem}: {with_fed} of {total} acted steps had a term feed the choice; "
              f"by exit {out['fed']} of {out['steps']}; by exit/role {out['roles']}"
              + (f"; {out['no_fed_field']} steps without the field (arm OFF?)"
                 if out["no_fed_field"] else ""))
