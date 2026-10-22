"""W-4, THE DK KIND STORE KEYED (TETHER_W_DK_KEYED; the reviewer 2026-10-22 05:14 amendment c,
05:52). The fake ARC game, C-seed-X: a two-game lineage in a temp folder, then two agents load it --
A the old way (every carried dk key in RAM), B through the load-time snapshot -- and play the same
script.

  K0   at load, mid-game after landings, and after B's boundary merge: for every carried and landed
       kind, asked alone and with a same-type partner, against every target it has and one it has
       not, _kix_land's land (each rung's Counter, in ITS ORDER) and last are EQUAL for A and B;
       so are the whole index's per-type sums and latest seqs, and the load report's kinds_known_dk
  K1   the landings agree (A's and B's _kind_landed_dk), so the two played the same game
  MF   after B's boundary merge a FRESH snapshot reads a changed kind_dk (the merge happened), and
       B's held snapshot does not (the snapshot holds)
  K2   the game's write (sleep) closes B's snapshot and its checkpoint empties the WAL; MF: a reader
       held open through such a write leaves the WAL unemptied

    python test_w4.py
"""
from __future__ import annotations

import os
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def agent(lineage_dir):
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=lineage_dir)
    return env, ag


def steps(env, ag, n):
    for _ in range(n):
        env.observe()
        ag.step()


def kinds_of(ag) -> dict:
    """Every kind the agent can read (carried or landed) -> its targets."""
    out: dict = {}
    keys = list(ag._known_dk_items()) if ag._dk_snap is not None else list(
        ag._kind_known_dk.items())
    for (d, _k, t), _n in keys + list(ag._kind_landed_dk.items()):
        out.setdefault(d, set()).add(t)
    return out


def same(a, b, where: str) -> int:
    ka, kb = kinds_of(a), kinds_of(b)
    assert ka == kb, (where, len(ka), len(kb))
    a._kix = b._kix = None
    by_type: dict = {}
    for d in ka:
        by_type.setdefault(d[0], []).append(d)
    asks = 0
    for d, tgts in sorted(ka.items(), key=repr):
        partner = next((p for p in by_type[d[0]] if p != d), None)
        for kinds in ((d,), (d, partner) if partner else None):
            if kinds is None:
                continue
            for ko in sorted(tgts, key=repr)[:3] + [("no", "such", "kind")]:
                la, lta = a._kix_land(kinds, ko)
                lb, ltb = b._kix_land(kinds, ko)
                assert (la is None) == (lb is None), (where, kinds, ko)
                if la is not None:
                    for g in "abc":
                        assert list(la[g].items()) == list(lb[g].items()), (where, kinds, ko, g)
                    assert lta == ltb, (where, kinds, ko, "last")
                asks += 1
    ia, ib = a._kix_build(), b._kix_build()
    assert {t: list(c.items()) for t, c in ia["tot_t"].items()} == \
        {t: list(c.items()) for t, c in ib["tot_t"].items()}, (where, "tot_t")
    assert ia["last_k"] == ib["last_k"], (where, "last_k")
    return asks


def main() -> int:
    import lineage
    import lineage_store as ls
    import tether
    d = tempfile.mkdtemp(prefix="w4_")
    for _g in range(2):
        env, ag = agent(d)
        steps(env, ag, 6)
        ag.end_run("cap")
        lineage.write(d, ag, "fake")
    tether._W_DK_KEYED = False
    env_a, a = agent(d)
    tether._W_DK_KEYED = True
    env_b, b = agent(d)
    assert a._dk_snap is None and b._dk_snap is not None
    assert len(a._kind_known_dk) > 0 and len(b._kind_known_dk) == 0, "PRECONDITION: carried rows"
    assert len(a._kdk_last) > 0 and len(b._kdk_last) == 0
    assert b._dk_snap.count == len(a._kind_known_dk)
    # MF right after load: a planted merge (one row's n + 1, committed on another connection) is
    # seen by a fresh read and not by B's held snapshot; then undone
    q0 = next(iter(a._kind_known_dk))[0]
    r0 = b._dk_snap.rows(q0)
    con = ls.open_store(d)
    try:
        dk_id = con.execute("SELECT id FROM sym WHERE s = ?", (ls._j(list(q0)),)).fetchone()[0]
        con.execute("UPDATE kind_dk SET n = n + 1 WHERE dk = ? AND n > 0", (dk_id,))
        fresh = lineage.DkSnapshot(d)
        try:
            seen = fresh.rows(q0) != r0
        finally:
            fresh.close()
        held0 = b._dk_snap.rows(q0) == r0
        con.execute("UPDATE kind_dk SET n = n - 1 WHERE dk = ? AND n > 1", (dk_id,))
    finally:
        con.close()
    assert seen and held0, ("MF at load: planted merge", seen, held0)
    print("  MF at load: a planted merge on kind_dk (n + 1 on one kind's rows, committed) is seen "
          "by a fresh read, not by B's held snapshot; undone")
    n0 = same(a, b, "at load")
    print(f"  K0 at load: {len(a._kind_known_dk)} carried dk keys in A's RAM, 0 in B's (the "
          f"snapshot holds {b._dk_snap.count}); {n0} asks equal, rung order included; tot_t and "
          f"last_k equal")
    steps(env_a, a, 6)
    steps(env_b, b, 6)
    assert a._kind_landed_dk == b._kind_landed_dk and a._kind_landed_dk, "K1"
    n1 = same(a, b, "mid-game")
    print(f"  K1 / K0 mid-game: both landed the same {len(a._kind_landed_dk)} dk keys; {n1} asks "
          f"equal")
    before = {q: b._dk_snap.rows(q) for q in {k[0] for k in b._kind_landed_dk}}
    rep = lineage.boundary(d, b, "fake", "level")
    assert rep and "refused" not in rep, rep
    fresh = lineage.DkSnapshot(d)
    try:
        moved = [q for q, r in before.items() if fresh.rows(q) != r]
        held = [q for q, r in before.items() if b._dk_snap.rows(q) != r]
    finally:
        fresh.close()
    assert moved, "MF: the boundary merge changed no kind_dk row a fresh read can see"
    assert not held, ("the held snapshot moved", held[:2])
    n2 = same(a, b, "after the boundary merge")
    print(f"  MF: after B's boundary merge a fresh snapshot sees {len(moved)} changed kinds, B's "
          f"held snapshot 0; K0 after the merge: {n2} asks equal")
    b.end_run("cap")
    lineage.write(d, b, "fake")
    assert b._dk_snap.closed and ls.wal_bytes(d) == 0, ls.wal_bytes(d)
    env_c, c = agent(d)                     # a third life: its snapshot is the planted reader
    steps(env_c, c, 6)
    assert lineage.boundary(d, c, "fake", "level")
    framed = ls.wal_bytes(d)
    con = ls.open_store(d)
    try:
        busy = con.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchone()
        held = ls.wal_bytes(d)
        c._dk_snap.close()
        free = con.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchone()
    finally:
        con.close()
    assert framed > 0 and busy[0] == 1 and held == framed, ("MF-K2", framed, busy, held)
    assert free[0] == 0 and ls.wal_bytes(d) == 0, ("K2", free, ls.wal_bytes(d))
    print(f"  K2: the game's write closed B's snapshot and its checkpoint emptied the WAL (0 B); "
          f"MF: with a snapshot held, a checkpoint is refused (busy) and the WAL keeps {held} B; "
          f"closed, the same checkpoint empties it")
    print("w4: OK")
    return 0


if __name__ == "__main__":
    tempfile.tempdir = tempfile.mkdtemp(prefix="w4t_")
    sys.exit(main())
