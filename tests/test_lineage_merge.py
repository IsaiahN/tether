"""D1, THE MERGE FORMAT (the reviewer 2026-10-15 00:00, 00:13): branches join through a MERGE
generation naming every tip; no tip is picked, nothing is copied or removed. Real gridworld Agents
through lineage.load / lineage.write; the branches grow in separate folders, as K workers would,
and their generation files are then laid side by side.

  R-m3  "a branch was dropped": two tips raise N3; after lineage.merge the merge generation names
        both tips, load succeeds, the fold holds both tips' rows, and a contested status keeps both
        values; with the merge generation's file removed, N3 raises again.
  R-m1  (its merge clauses) "a row was lost": every input row is in the fold by (born, handle);
        rows in = rows out; the same composition from both branches is held twice, not deduped.
R-m2 and R-m1's recovery clauses wait with the recovery item (the reviewer 00:13).

    python tests/test_lineage_merge.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import lineage_store  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

N = 20


def _run(d, seed, n):
    env = world.bind(gridworld.family("default", seed))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"), tether.Config(),
                      ledger.Ledger())
    rep = lineage.load(d, ag)
    for _ in range(n):
        ag.step()
    ag.end_run("cap")
    return ag, rep


def _put(d, gen):
    """A hand-written generation, named by its own hash as lineage writes one."""
    raw = json.dumps(gen, sort_keys=True, indent=1).encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()[:16]
    (Path(d) / f"{lineage.PREFIX}{h}.json").write_bytes(raw)
    return h


def _status(parent, born, handle, admitted, book):
    return {"lineage": 1, "parent": parent, "game": "status", "terms": [],
            "status": [{"born": born, "handle": handle, "admitted": admitted}], "evidence": [],
            "vindication_tail": [], "book": book, "invented": {}, "dormant": [],
            "dormant_refused": []}


def _n3(d):
    try:
        lineage.head(d)
    except ValueError as e:
        return "not one chain" in str(e)
    return False


def main():
    # C-seed-X (the reviewer 2026-10-20 13:10): the fixture needs the two branches to share a
    # term, so one temperament: the old constant seed. Unpinned it failed its own guard in 2 of
    # 5 runs under a per-process birth seed
    tether._AGENT_SEED = False
    tmp = Path(tempfile.mkdtemp(prefix="merge_"))
    d, side = tmp / "main", tmp / "side"
    d.mkdir()
    side.mkdir()
    a, _ = _run(d, 0, N)
    wa = lineage.write(d, a, "default")
    shutil.copy(d / wa["written"], side / wa["written"])
    b1, _ = _run(d, 0, N)
    w1 = lineage.write(d, b1, "default")
    b2, _ = _run(side, 0, N + 5)
    w2 = lineage.write(side, b2, "default")
    shutil.copy(side / w2["written"], d / w2["written"])
    gens = lineage._read(d)
    rows = {h: g["terms"] for h, g in gens.items()}
    # a root row no branch has set a status on, so the contested pair below is the only one
    touched = {(s["born"], s["handle"]) for g in gens.values() for s in g["status"]}
    root = [r for r in rows[wa["hash"]]
            if r.get("handle") and (wa["hash"], r["handle"]) not in touched]
    # keyed by gamma.Gamma.row_key, what load installs by (the reviewer 2026-10-26 03:11, R2): finer
    # than lineage._key on a bound row, so it only narrows the shared set; both counts printed
    old = ({lineage._key(r) for r in rows[w1["hash"]]}
           & {lineage._key(r) for r in rows[w2["hash"]]})
    k1 = {gamma.Gamma.row_key(r) for r in rows[w1["hash"]]}
    both = k1 & {gamma.Gamma.row_key(r) for r in rows[w2["hash"]]}
    assert root and both and w1["hash"] != w2["hash"], ("fixture: the branches give R-m1/R-m3 "
                                                        "nothing to test", len(root), len(both))
    # MUST-FAIL: w2's operands with their attribute changed; `both` shrinks by exactly those keys
    opk = {k for k in both if json.loads(k)[3] is not None}
    assert opk, "R-m1 MF: no shared row has an operand, so the MF has no occasion"
    mut = [{**r, "operand": r["operand"] + "_mf"} if r.get("operand") else r
           for r in rows[w2["hash"]]]
    both_mf = k1 & {gamma.Gamma.row_key(r) for r in mut}
    assert both_mf == both - opk, ("R-m1 MF: changed operands did not leave the shared set",
                                   len(both), len(both_mf), len(opk))
    # a contested status and a contested book key: each branch sets them differently. The key is
    # one the root set and no branch touched, so its pre-split value is the root's
    r0 = root[0]
    bk = next((k for k in gens[wa["hash"]]["book"]
               if k not in gens[w1["hash"]]["book"] and k not in gens[w2["hash"]]["book"]),
              "fixture.merge_probe")   # no such key: one the root never set (pre-split absent)
    pre = gens[wa["hash"]]["book"].get(bk)
    s1 = _put(d, _status(w1["hash"], wa["hash"], r0["handle"], "necessary", {bk: "b1"}))
    s2 = _put(d, _status(w2["hash"], wa["hash"], r0["handle"], "promoted", {bk: "b2"}))
    assert _n3(d), "fixture: two tips did not raise N3 before the merge"

    m = lineage.merge(d)
    mg = json.loads(lineage_store.file_bytes(d / m["written"]))
    assert sorted(mg["parents"]) == sorted([s1, s2]), ("R-m3 a branch was dropped", mg["parents"])
    h, f = lineage.head(d)
    assert h == m["hash"], ("R-m3 a branch was dropped", h, m)
    rows_in = {(g, r.get("handle")) for g, rs in rows.items() for r in rs}
    rows_out = {(r["born"], r.get("handle")) for r in f["terms"]}
    assert rows_in == rows_out and len(f["terms"]) == len(rows_in), (
        "R-m1 a row was lost", len(rows_in), len(rows_out), len(f["terms"]))
    for k in both:
        held = [r for r in f["terms"] if gamma.Gamma.row_key(r) == k]
        assert {r["born"] for r in held} >= {w1["hash"], w2["hash"]}, ("R-m1 a row was lost", k)
    row = next(r for r in f["terms"] if (r["born"], r.get("handle")) == (wa["hash"],
                                                                       r0["handle"]))
    vals = {(c["gen"], c["admitted"]) for c in row.get("contested", [])}
    assert vals == {(s1, "necessary"), (s2, "promoted")}, ("R-m3 a branch was dropped",
                                                           "contested", row)
    assert row["admitted"] == r0.get("admitted"), ("R-m3 a contested status was decided",
                                                   row["admitted"], r0.get("admitted"))
    got = {(c["gen"], c["value"]) for c in f.get("contested_book", {}).get(bk, [])}
    assert got == {(s1, "b1"), (s2, "b2")} and f["book"].get(bk) == pre, (
        "R-m3 a branch was dropped", "book", bk, got, f["book"].get(bk), pre)
    c, rep = _run(d, 0, 0)
    assert rep["parent"] == m["hash"], ("R-m3 a branch was dropped", "load", rep.get("parent"))
    (d / m["written"]).unlink()
    assert _n3(d), "R-m3: with the merge generation removed, N3 did not raise"
    print(f"  branches: root {wa['hash']}, tips {s1} / {s2}; same composition in both: "
          f"{len(both)} by row_key ({len(old)} by lineage._key); MF {len(opk)} operand key(s) "
          f"changed -> {len(both_mf)} shared", flush=True)
    print(f"  R-m3: merge {m['hash']} names both tips; load parent {rep['parent']}; contested "
          f"{sorted(vals)}, admitted kept {row['admitted']!r}; book {bk!r} contested "
          f"{sorted(got)}, kept {pre!r}; N3 again without it", flush=True)
    print(f"  R-m1: rows in {len(rows_in)} = rows out {len(rows_out)}; held twice {len(both)}",
          flush=True)
    print("lineage merge: OK")


if __name__ == "__main__":
    main()
