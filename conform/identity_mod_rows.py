"""identity_mod_rows: OFF identity for an instrument that ADDS rows.

The reviewer 2026-10-12 02:13 CDT.

A new row moves every later ledger position, and rows carry positions in their details, so a
byte check cannot pass by construction. This one drops the named new events, maps every NAMED
position field through the row shift, checks the one row-count field exactly, and then compares
byte for byte. Any other difference FAILS. A field that carries a position and is not named here
fails the check, which is the point: a new position field must be added to the list on purpose.

    python conform/identity_mod_rows.py base.jsonl new.jsonl goal_choice[,event] [event:field,...]

The optional last argument names fields the instrument ADDS to existing rows on purpose; each is
removed from the new row only where the base row lacks it, so a changed value still fails.
"""
from __future__ import annotations

import json
import sys

# Fields whose value is a ledger seq. Paths are under the row; "*" is every list element.
POSITIONS = (
    ("detail", "seq"),
    ("detail", "bet_seq"),
    ("detail", "plan_seq"),
    ("detail", "signal_seq"),
    ("detail", "shadow", "recorded_before"),
    ("detail", "fed", "*", 0),                    # resolution: [[seq, role], ...]
    ("detail", "gamma_read", "fed", "*", "seq"),  # may be None
)
# Fields whose value is a COUNT of rows: (event, path, how the counted span starts).
# completion_sweep.segment_rows = len(led) - start at record time, so its span is
# [own seq - value, own seq).
COUNTS = (("completion_sweep", ("detail", "segment_rows")),)
# The @run arms row's seed is the BIRTH seed, drawn per process; a lineage replaces it with a later
# @run seed row (tether._seed_from_lineage). So the arms row's seed fields are masked and the
# EFFECTIVE seed is compared instead (the reviewer 2026-10-20 12:23: one mask, every comparer
# imports it).
BIRTH = ("seed", "seed_source")


def effective_seed(rows: list[dict]) -> tuple:
    """(seed, generation, seed_source) of the last @run seed row, else of the @run arms row."""
    s = [r["detail"] for r in rows if r.get("slot") == "@run" and r.get("event") == "seed"]
    d = s[-1] if s else next((r["detail"] for r in rows
                              if r.get("slot") == "@run" and r.get("event") == "arms"), {})
    return d.get("seed"), d.get("generation"), d.get("seed_source")


def _get(node, path):
    """Every (parent, key) the path reaches, so the value can be read and replaced."""
    out = [(None, None, node)]
    for k in path:
        nxt = []
        for _p, _k, v in out:
            if k == "*":
                if isinstance(v, list):
                    nxt += [(v, i, x) for i, x in enumerate(v)]
            elif ((isinstance(v, dict) and k in v)
                  or (isinstance(v, list) and isinstance(k, int) and k < len(v))):
                nxt.append((v, k, v[k]))
        out = nxt
    return [(p, k) for p, k, _v in out if p is not None]


def compare(a: list[dict], b: list[dict], drop: set[str],
            new_fields: set[str] = frozenset()) -> list[str]:
    """Differences between base A and new B once B's `drop` events are removed; empty is
    identity."""
    kept = [r for r in b if r["event"] not in drop]
    if len(kept) != len(a):
        return [f"row count: base {len(a)}, new {len(kept)} after dropping {sorted(drop)}"]
    amap = {x["seq"]: y["seq"] for x, y in zip(a, kept, strict=True)}   # base seq -> new seq
    dropped = sorted(r["seq"] for r in b if r["event"] in drop)
    bad = []
    ea, eb = effective_seed(a), effective_seed(kept)
    if ea != eb:
        bad.append(f"effective seed: base {ea}, new {eb}")
    for x, y in zip(a, kept, strict=True):
        x = json.loads(json.dumps(x))
        y = json.loads(json.dumps(y))
        if x.get("slot") == "@run" and x["event"] == "arms" == y["event"]:
            for k in BIRTH:
                x["detail"].pop(k, None)
                y["detail"].pop(k, None)
        for f in new_fields:
            ev, _, field = f.partition(":")
            if y["event"] == ev and field in y["detail"] and field not in x["detail"]:
                del y["detail"][field]
        for path in POSITIONS:
            for parent, key in _get(x, path):
                v = parent[key]
                if isinstance(v, int) and not isinstance(v, bool):
                    if v not in amap:
                        where = ".".join(map(str, path))
                        bad.append(f"seq {x['seq']}: {where}={v} names no base row")
                        continue
                    parent[key] = amap[v]
        for event, path in COUNTS:
            if x["event"] != event:
                continue
            for (px, kx), (py, ky) in zip(_get(x, path), _get(y, path), strict=False):
                start = y["seq"] - py[ky]
                gone = sum(1 for s in dropped if start <= s < y["seq"])
                if py[ky] - gone != px[kx]:
                    bad.append(f"seq {x['seq']}: {'.'.join(path)} base {px[kx]}, new {py[ky]} "
                               f"with {gone} dropped rows in its span")
                px[kx] = py[ky]
        x["seq"] = y["seq"]
        if json.dumps(x, sort_keys=True, default=str) != json.dumps(y, sort_keys=True, default=str):
            keys = sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
            sub = ""
            if keys == ["detail"]:
                d1, d2 = x["detail"], y["detail"]
                sub = " " + str(sorted(k for k in set(d1) | set(d2) if d1.get(k) != d2.get(k)))
            bad.append(f"seq {x['seq']} ({y['event']}): {keys}{sub}")
    return bad


def _load(p):
    with open(p, encoding="utf-8") as fh:
        rows = [json.loads(line) for line in fh]
    if not rows:
        raise SystemExit(f"{p}: empty ledger")
    return rows


if __name__ == "__main__":
    a, b = _load(sys.argv[1]), _load(sys.argv[2])
    drop = set(sys.argv[3].split(","))
    new_fields = set(sys.argv[4].split(",")) if len(sys.argv) > 4 else set()
    n = sum(1 for r in b if r["event"] in drop)
    bad = compare(a, b, drop, new_fields)
    for line in bad[:20]:
        print(" ", line)
    print(f"identity_mod_rows: base {len(a)} rows, new {len(b)} ({n} {sorted(drop)} dropped): "
          f"{'IDENTICAL' if not bad else f'{len(bad)} DIFFERENCE(S)'}")
    sys.exit(1 if bad else 0)
