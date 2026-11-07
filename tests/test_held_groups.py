"""TETHER_HELD_GROUPS (the reviewer 2026-11-06 r1313, r1336): a lookup row's held_groups (WHAT, the
held distinct pairs; WHEN, their readings' changed frame indices; WHERE, the description's types and
an event's member readings, a list in member order) rebuild the row's per-junction lines and its
EXISTING held_digest exactly, with the library, FROM THE DISK ROW: every row is first round-tripped
through the ledger's own writer (json.dumps(sort_keys=True), ledger.py:236; r1339). A gridworld
agent, seed pinned, 3 steps: c1 o0.col and the c2 o0.row event (about 5 s per run).

check_rebuild  every lookup row with held lines, round-tripped: the lines rebuilt from held_groups
               hash to held_digest, and their count is held_n. MF: drop one group and the digest
               differs. MF: the event's members as a dict (406d55d's form) differ on disk, since
               sort_keys re-sorts its member order (o0.row, o0.col)
check_paths    the stream path (TETHER_LOOKUP_FOLD off) and the list path (TETHER_LOOKUP_STREAM off)
               write the same held_groups as the fold
check_off      OFF: no held_groups field, and every row is otherwise the ON row

    python tests/test_held_groups.py [check ...]
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

sys.path.insert(0, os.path.join(_repo.ROOT, "conform"))
from identity_mod_rows import compare  # noqa: E402  the one identity reader

import composer  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def run(**flags) -> list:
    keep = {k: getattr(tether, k) for k in flags}
    try:
        for k, v in flags.items():
            setattr(tether, k, v)
        env = world.bind(gridworld.family("default", 0))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="hg"), tether.Config(),
                          ledger.Ledger())
        for _ in range(3):
            ag.step()
        return ag.led.rows()
    finally:
        for k, v in keep.items():
            setattr(tether, k, v)


def lookups(rows: list) -> list:
    return [r for r in rows if r["event"] == "lookup" and "held_digest" in r["detail"]]


def disk(row: dict) -> dict:
    """The row as the ledger writes it (ledger.py:236, sort_keys) and a later reader loads it."""
    return json.loads(json.dumps(row, sort_keys=True, default=str))


def rebuild(g: dict) -> tuple:
    """The per-junction lines from held_groups and the library: (sha256 hex[:16], count)."""
    held = {(x, y): h for x, y, h in g["pairs"]}
    ch = {r: set(v) for r, v in g["changed"].items()}
    types = g["types"]
    srcs = ([types] if "members" not in g
            else [{r: types[r] for r in rs} for rs in (g["members"].values()
                                                        if isinstance(g["members"], dict)
                                                        else (v for _m, v in g["members"]))])
    dig, n, seen = hashlib.sha256(), 0, set()
    for d_ in srcs:
        for mol, a, b, ra, rb, via in composer.lookup_junctions(d_):
            for x in ra:
                for y in rb:
                    if x == y:
                        continue
                    if "members" in g:
                        if (mol, a, b, x, y) in seen:
                            continue
                        seen.add((mol, a, b, x, y))
                    if (x, y) in held:
                        occ = {"+": len(ch[x] | ch[y]), "−": len(ch[x]),
                               "→": len(ch[y]), "⇒": len(ch[y])}
                        line = {"molecule": mol, "left": a, "right": b, "left_reading": x,
                                "right_reading": y, "held": held[(x, y)], "via": via,
                                "occasions": occ}
                        dig.update(json.dumps(line, sort_keys=True, ensure_ascii=False).encode())
                        dig.update(b"\n")
                        n += 1
    return dig.hexdigest()[:16], n


def check_rebuild() -> None:
    lk = [disk(r) for r in lookups(run()) if r["detail"]["held_n"]]
    assert lk, "no lookup with held lines: the fixture reaches nothing"
    assert all("held_groups" in r["detail"] for r in lk), "MF: no held_groups (a5d20ac)"
    ev = [r for r in lk if "members" in r["detail"]["held_groups"]]
    assert ev, "no event lookup: the member-order MF reaches nothing"
    for r in lk:
        d = r["detail"]
        got = rebuild(d["held_groups"])
        assert got == (d["held_digest"], d["held_n"]), ("MF: rebuild", r["cycle"], r["slot"],
                                                        got, d["held_digest"], d["held_n"])
        cut = dict(d["held_groups"], pairs=d["held_groups"]["pairs"][1:])
        assert rebuild(cut)[0] != d["held_digest"], ("MUST-FAIL: a dropped group went unseen",
                                                     r["slot"])
        print(f"  c{r['cycle']} {r['slot']}{' (event)' if 'members' in d['held_groups'] else ''}:"
              f" {len(d['held_groups']['pairs'])} groups rebuild {d['held_n']} lines from disk, "
              f"digest {d['held_digest']}; one group dropped -> differs")
    for r in ev:
        d = r["detail"]
        mem = d["held_groups"]["members"]
        assert [m for m, _v in mem] != sorted(m for m, _v in mem), ("MF: member order already "
                                                                    "sorted", r["slot"])
        as_dict = disk(dict(d["held_groups"], members=dict(mem)))
        assert rebuild(as_dict)[0] != d["held_digest"], ("MUST-FAIL: the dict form rebuilt on "
                                                         "disk", r["slot"])
        print(f"  c{r['cycle']} {r['slot']} (event): members {[m for m, _v in mem]}; as a dict "
              "on disk (406d55d) -> differs")


def check_paths() -> None:
    fold = [r["detail"]["held_groups"] for r in lookups(run())]
    stream = [r["detail"]["held_groups"] for r in lookups(run(_LOOKUP_FOLD=False))]
    lists = [r["detail"]["held_groups"] for r in lookups(run(_LOOKUP_STREAM=False))]
    assert fold == stream == lists, ("the paths' held_groups differ", fold, stream, lists)
    print(f"  fold, stream and list paths: the same held_groups on {len(fold)} lookup rows")


def check_off() -> None:
    on, off = run(), run(_HELD_GROUPS=False)
    assert not any("held_groups" in r["detail"] for r in off), "OFF wrote held_groups"
    # the arms row records the live arm state, which is the flag this check moves
    bad = compare([r for r in off if r["event"] != "arms"],
                  [r for r in on if r["event"] != "arms"], set(), {"lookup:held_groups"})
    assert not bad, ("OFF: a row differs beyond held_groups", bad[:5])
    print(f"  OFF: no field; {len(off)} rows identical to ON's beyond held_groups "
          "(identity_mod_rows.compare: timings masked, the arms row apart)")


def main() -> int:
    want = set(sys.argv[1:])
    for c in (check_rebuild, check_paths, check_off):
        if not want or c.__name__ in want:
            c()
            print("ok  ", c.__name__)
    print("test_held_groups OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
