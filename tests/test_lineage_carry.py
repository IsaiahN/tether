"""(b'-g) THE LINEAGE CARRY: R-g1..R-g3 as registered (the reviewer 2026-10-14 20:18), with notes
N1..N5 (20:22). Real Agents through __init__; the arms are set in the ENVIRONMENT of a child process
at start (TETHER_LINEAGE_CARRY and TETHER_LINEAGE_HOLD, so the dormant round trip is exercised, N5).

Content comes from gridworld, which mints (the fake ARC world minted 0 terms in RL-0's 5 actions, so
R-g1 there would be vacuous); it goes through lineage.load / lineage.write, the two calls wire() and
both runners make. ONE PATH, the plumbing: play() on the fake ARC world writes a generation and the
next play() loads it.

  R-g1  CARRY: game 2 starts holding every non-PRIOR term game 1 ended with (atom chain + guard),
        as IMPORTED naming game 1's generation; a second process given the chain starts the same.
  R-g2  ROUND TRIP: terms, evidence, vindication, book, inventions and the dormant record read back
        equal from the fold; the gap on load is exactly the named set (operand bindings, per-slot
        standing values, inventions skipped and counted).
  R-g3  CHAIN: each generation names its parent; one is never overwritten; a generation over an
        unchanged library holds no term rows (written AFTER a load, N1). N3: a second tip raises.

The OFF identity is a lane in RL-0's form, not this fixture.

    python tests/test_lineage_carry.py
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_holdout  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import lineage_store  # noqa: E402  item 6: a lineage file read as the lineage reads it
import tether  # noqa: E402
import world  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402

N = 20


def _agent(d, seed):
    env = world.bind(gridworld.family("default", seed))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"), tether.Config(),
                      ledger.Ledger())
    return env, ag, lineage.load(d, ag)


def _key(t):
    return json.dumps([[a.name for a in t.atoms], t.guard,
                       [a.name for a in t.operand_term.atoms] if t.operand_term else None])


def _held(ag):
    return {_key(t): t for t in ag.gamma.library.values() if t.origin != gamma.PRIOR}


def _gen(d, w):
    return json.loads(lineage_store.file_bytes(Path(d) / w["written"]))


def _carries(rows, ag, rep, label):
    """R-g1 as registered: every row is held as an IMPORTED term naming the parent, by atom chain
    and guard. A row whose binding was its whole content is held as its UNBOUND entry (carried
    records what it lost). A row that lands on a PRIOR atom was destroyed on carry: R-g1 FAILS.
    Returns (held as compositions, held as unbound entries)."""
    assert not rep["destroyed_on_carry"], (label, "R-g1 FAILED: terms destroyed on carry",
                                           rep["destroyed_on_carry"])
    held = _held(ag)
    skipped = {json.dumps([r["atoms"], None, None]) for r in rep["built_on_skipped_invention"]}
    composed, unbound = 0, 0
    missing = []
    for r in rows:
        k = lineage._key(r)
        if k in held:
            t = held[k]
            c = ag.gamma.carried[t.name]
            assert t.origin == gamma.IMPORTED, (label, "not IMPORTED", r["atoms"])
            assert c.get("parent") == rep["parent"], (label, "parent")
            if "unbound" in c:
                assert "?" in t.operand and not any(p.startswith("o") and p[1:].isdigit()
                                                    for p in t.operand.replace("~", ".")
                                                    .replace("_", ".").split(".")), (
                    label, "an unbound entry still names an object", t.name)
                unbound += 1
            else:
                composed += 1
        elif k not in skipped:
            missing.append(r)
    assert not missing, (label, "R-g1 FAILED: not held", len(missing), len(rows), missing[:2])
    return composed, unbound


def on_checks():
    assert lineage._CARRY and tether._LINEAGE_HOLD, "the child must be started with both arms"
    tmp = Path(tempfile.mkdtemp(prefix="lineage_"))
    d = tmp / "g"
    # R-g1: game 1 from the root, then game 2 loads its generation.
    env, ag1, rep = _agent(d, 0)
    assert rep["parent"] is None, rep
    for _ in range(N):
        ag1.step()
    ag1.end_run("cap")
    w1 = lineage.write(d, ag1, "default")
    rows1 = ag1.gamma.blob()["terms"]
    assert rows1, "fixture: game 1 minted nothing"
    env, ag2, rep2 = _agent(d, 1)
    assert rep2["parent"] == w1["hash"], ("R-g1 parent", rep2.get("parent"), w1)
    composed, unbound = _carries(rows1, ag2, rep2, "R-g1 carry")
    assert composed, ("fixture: nothing crossed as a composition", composed, unbound)
    print(f"  R-g1: game 1 wrote {w1['written']} with {len(rows1)} term rows; game 2 holds "
          f"{composed} as IMPORTED compositions from {rep2['parent']} and {unbound} as "
          f"unbound entries; destroyed on carry 0", flush=True)
    # R-g3: game 2's generation names game 1's.
    for _ in range(N):
        ag2.step()
    ag2.end_run("cap")
    w2 = lineage.write(d, ag2, "default")
    assert _gen(d, w2)["parent"] == w1["hash"], ("R-g3 parent", _gen(d, w2)["parent"], w1)
    # R-g3: over an unchanged library, after a load (N1), no term rows and no status rows.
    env, ag3, _rep3 = _agent(d, 2)
    ag3.end_run("cap")
    w3 = lineage.write(d, ag3, "default")
    g3 = _gen(d, w3)
    assert not g3["terms"] and not g3["status"], ("R-g3 a full copy", len(g3["terms"]),
                                                  len(g3["status"]))
    # a second write by the same agent EXTENDS its first under TETHER_LINEAGE_BOUNDARY
    # (lineage.py, F2): a child of w3, measured, never assumed (the reviewer 19:12 a, b)
    again = lineage.write(d, ag3, "default")
    assert "written" in again and again["parent"] == w3["hash"], ("R-g3 child of w3", again, w3)
    assert lineage.head(d)[0] == again["hash"], "R-g3 one chain"
    # NEVER OVERWRITE, direct (19:12 c): a write whose bytes are w3's aims at w3's own name through
    # the "xb" open; it is refused, naming w3's file, and w3's bytes are unchanged
    p3 = Path(d) / w3["written"]
    before = hashlib.sha256(p3.read_bytes()).hexdigest()
    raw3, real_dumps, used = lineage_store.file_bytes(p3), lineage._dumps, []

    def once(x):
        if used:
            return real_dumps(x)
        used.append(1)
        return raw3
    lineage._dumps = once
    try:
        same = lineage.write(d, ag3, "default")
    finally:
        lineage._dumps = real_dumps
    assert used and w3["written"] in str(same.get("refused")), ("R-g3 never overwrite", same)
    assert hashlib.sha256(p3.read_bytes()).hexdigest() == before, "R-g3 w3's bytes changed"
    print(f"  R-g3: {w2['hash']} -> parent {w1['hash']}; unchanged {w3['hash']} holds 0 term "
          f"rows; a second write is its child {again['hash']} (parent {again['parent']}); a write "
          f"aimed at {w3['written']} refused ({same['refused']}), its bytes unchanged", flush=True)
    # N3: a second tip is loud.
    e = tmp / "branch"
    shutil.copytree(d, e)
    ag3.lineage_parent = w1["hash"]
    lineage.write(e, ag3, "default")
    try:
        lineage.head(e)
        raise AssertionError("N3 a second tip was picked silently")
    except ValueError as err:
        assert "tips" in str(err), ("N3", str(err))
    # R-g1, a second process given the chain.
    r = subprocess.run([sys.executable, "-B", __file__, "--second", str(d)], env=os.environ.copy(),
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
    sys.stdout.write(r.stdout)
    assert r.returncode == 0, f"R-g1 second process:\n{r.stderr[-2000:]}"
    # R-g2: the round trip, with a dormant record (HOLD on, a real retarget).
    rr = tmp / "rt"
    env, ag, _ = _agent(rr, 3)
    for _ in range(N):
        ag.step()
    ag.retarget(env, ag.level + 1, how="level_advance")
    for _ in range(3):
        ag.step()
    ag.end_run("cap")
    blob = ag.gamma.blob()
    assert ag.gamma.evidence and ag._dormant, ("fixture: no evidence or no dormant record",
                                               len(ag.gamma.evidence), len(ag._dormant))
    lineage.write(rr, ag, "default")
    _h, f = lineage.head(rr)
    folded = [{k: v for k, v in r.items() if k != "born"} for r in f["terms"]]
    assert folded == blob["terms"], "R-g2 terms"
    assert f["evidence"] == ag.gamma.evidence, "R-g2 evidence"
    assert f["dormant"] == ag._dormant, "R-g2 dormant"
    for k in ("vindication", "book", "invented"):
        assert f[k] == blob[k], ("R-g2", k)
    env, agb, repb = _agent(rr, 4)
    _carries(blob["terms"], agb, repb, "R-g2 gap beyond the named set")
    assert not repb["refused"], ("R-g2 gap", repb["refused"])
    for t in _held(agb).values():
        st = agb.gamma.standing.get(t.name)
        assert st is None or not st.settled_on, ("R-g2 standing crossed", t.name)
    print(f"  R-g2: {len(blob['terms'])} terms, {len(ag.gamma.evidence)} evidence events, "
          f"{len(ag._dormant)} dormant record(s) read back equal; on load: unbound "
          f"{repb['crossed_without_binding']}, skipped inventions "
          f"{len(repb['skipped_invented'])}", flush=True)
    # LINEAGE-UNIQUE IDENTITY (the reviewer 20:45): a per-game COUNTER in place of the handle's
    # random suffix, so two games of one name mint the same handle text; both rows must fold.
    cd = tmp / "same_text"
    real = gamma.Term.handle
    count = [0]

    def counted(_self, game):
        count[0] += 1
        return f"{game}_X_term_{count[0]:08x}"
    gamma.Term.handle = counted
    try:
        written = []
        for _ in range(2):
            count[0] = 0
            env, agc, _r = _agent(cd, 0)
            for _ in range(N):
                agc.step()
            agc.end_run("cap")
            written.append(lineage.write(cd, agc, "default"))
    finally:
        gamma.Term.handle = real
    _h, fc = lineage.head(cd)
    texts = [r["handle"] for r in fc["terms"]]
    same = len(texts) - len(set(texts))
    assert same, ("fixture: no same-text handles arose", written)
    assert len(fc["terms"]) == sum(w["terms"] for w in written), (
        "R-g2 same-text handles folded together", len(fc["terms"]), written)
    print(f"  identity: two same-name games wrote {[w['terms'] for w in written]} rows, "
          f"{same} handle text(s) repeated across them, all {len(fc['terms'])} folded",
          flush=True)
    # ONE PATH, the plumbing: play() writes a generation and the next play() loads it.
    pd = tmp / "play"

    class Arc:
        def make(self, _game):
            return FakeWrapper()
    a = arc_holdout.play("fake", 5, arc=Arc(), lineage_dir=str(pd))["persistence"]
    b = arc_holdout.play("fake", 5, arc=Arc(), lineage_dir=str(pd))["persistence"]
    assert a["lineage"]["written"] and b["loaded"]["lineage"]["parent"] == a["lineage"]["hash"], (
        "ONE PATH", a["lineage"], b["loaded"])
    assert b["lineage"]["parent"] == a["lineage"]["hash"], ("ONE PATH parent", b["lineage"])
    print(f"  ONE PATH: play wrote {a['lineage']['hash']}, the next play loaded it and wrote "
          f"{b['lineage']['hash']}", flush=True)
    shutil.rmtree(tmp, ignore_errors=True)


def second(d):
    assert lineage._CARRY, "the second process must be started with the arm"
    _h, f = lineage.head(d)
    env, ag, rep = _agent(d, 5)
    composed, unbound = _carries(f["terms"], ag, rep, "R-g1 second process")
    print(f"  R-g1 second process: holds all {len(f['terms'])} folded rows from {rep['parent']} "
          f"({composed} compositions, {unbound} unbound entries)",
          flush=True)


def main():
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    # both seeds pinned (the reviewer 2026-10-22 19:39): R-g1's precondition rode the birth seed
    env.update(TETHER_LINEAGE_CARRY="1", TETHER_LINEAGE_HOLD="1", TETHER_AGENT_SEED="0",
               PYTHONHASHSEED="0")
    r = subprocess.run([sys.executable, "-B", __file__, "--on"], env=env, stdin=subprocess.DEVNULL,
                       capture_output=True, text=True, check=False)
    sys.stdout.write(r.stdout)
    assert r.returncode == 0, f"--on failed:\n{r.stderr[-3000:]}"
    print("lineage carry: OK")


if __name__ == "__main__":
    if "--second" in sys.argv:
        second(sys.argv[sys.argv.index("--second") + 1])
    elif "--on" in sys.argv:
        on_checks()
    else:
        main()
