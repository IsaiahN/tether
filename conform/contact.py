"""7a(5b) the contact reading: per ledger, how many acted steps had a library term feed the choice,
split by exit (`by`) AND by role (goal / route / body), and MC2's resolution pointers split by
whether the matching fed entry was the signal's OWN binding (same slot) or the same term bound on
ANOTHER slot (the reviewer 2026-10-10 14:21Z: two bindings, two loops, never one number). A READING
for the seats; nothing in the agent reads it, and nothing is pooled across ledgers (Fig 1 :22,
Fig 10 :24-26).

    python conform/contact.py runs/panel/*.jsonl
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True


def read(path: Path) -> dict:
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    by_seq = {r["seq"]: r for r in rows if "seq" in r}
    steps, fed, roles, route, missing = Counter(), Counter(), Counter(), Counter(), 0
    for r in rows:
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
            if e["role"] == "route":
                route[e.get("source")] += 1
    # MC2: each [REPEAT seq, role] pair, read back to the fed entry naming the bet's term there.
    # The split comes from the cited REPEAT row's slot; the pointer row itself is unchanged.
    mc2 = Counter()
    for r in rows:
        d = r.get("detail") or {}
        if r.get("event") != "resolution" or not isinstance(d.get("fed"), list):
            continue
        mc2["resolutions"] += 1
        term = ((by_seq.get(d["signal_seq"]) or {}).get("detail") or {}).get("bound")
        for seq, role in d["fed"]:
            rep = ((by_seq.get(seq) or {}).get("detail") or {}).get("gamma_read") or {}
            for e in rep.get("fed", ()):
                if e["name"] == term and e["role"] == role:
                    mc2[("same-slot" if e["slot"] == d["signal_slot"] else "other-slot", role)] += 1
    return {"steps": dict(steps), "fed": dict(fed),
            "roles": {f"{b}/{r}": n for (b, r), n in sorted(roles.items())},
            "no_fed_field": missing,
            "route": {"from-table": route.get("table", 0), "from-term": route.get("term", 0)},
            "mc2_resolutions": mc2.pop("resolutions", 0),
            "mc2": {f"{s}/{r}": n for (s, r), n in sorted(mc2.items())}}


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        p = Path(arg)
        out = read(p)
        total = sum(out["steps"].values())
        with_fed = sum(out["fed"].values())
        print(f"{p.stem}: {with_fed} of {total} acted steps had a term feed the choice; "
              f"by exit {out['fed']} of {out['steps']}; by exit/role {out['roles']}; "
              f"route {out['route']}; "
              f"MC2 {out['mc2_resolutions']} resolutions, matches {out['mc2']}"
              + (f"; {out['no_fed_field']} steps without the field (arm OFF?)"
                 if out["no_fed_field"] else ""))
