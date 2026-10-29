"""(b'-g) THE LINEAGE CARRY: R-g1..R-g3 as registered (the reviewer 2026-10-14 20:18), with notes
N1..N5 (20:22). Real Agents through __init__; the arms are set in the ENVIRONMENT of a child process
at start (TETHER_LINEAGE_CARRY and TETHER_LINEAGE_HOLD, so the dormant round trip is exercised, N5).

Content comes from gridworld, which mints (the fake ARC world minted 0 terms in RL-0's 5 actions, so
R-g1 there would be vacuous); it goes through lineage.load / lineage.write, the two calls wire() and
both runners make. ONE PATH, the plumbing: play() on the fake ARC world writes a generation and the
next play() loads it.

  R-g1  CARRY: game 2 starts holding every non-PRIOR term game 1 ended with (atom chain + guard),
        as IMPORTED naming game 1's generation; a second process given the chain starts the same.
        THE PLANT (the reviewer 2026-10-22 19:47): one real 2-atom chain accepted into game 1's
        Gamma before its write must cross as a COMPOSITION. It tests the CARRY's wiring (written,
        read back by a fresh agent, kept a composition), never that game 1 composes (Fig 11 :70)
  R-g2  ROUND TRIP: terms, evidence, vindication, book, inventions and the dormant record read back
        equal from the fold; the gap on load is exactly the named set (operand bindings, per-slot
        standing values, inventions skipped and counted).
  R-g3  CHAIN: each generation names its parent; one is never overwritten; a generation over an
        unchanged library holds no term rows (written AFTER a load, N1). N3: a second tip raises.

The OFF identity is a lane in RL-0's form, not this fixture.

DETERMINISTIC IN VERDICTS AND CONTENTS, NOT IN BYTES (the reviewer 2026-10-22 20:14): both seeds are
pinned, but with TETHER_AGENT_SEED off a term's handle takes the process's unseeded random suffix
(gamma.Term.handle), so handles, and with them the generation hashes, vary run to run (E8 Q24).

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


_LOADS = []   # each load_blob call lineage.load makes: what R-g1's oracle repeats, guard (a)


def _agent(d, seed):
    env = world.bind(gridworld.family("default", seed))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"fam_default_{seed}"), tether.Config(),
                      ledger.Ledger())
    real = gamma.Gamma.load_blob

    def spy(self, blob, parent=None, hold_unbound=False):
        _LOADS.append({"gamma": self, "env": env, "blob": blob, "parent": parent,
                       "hold_unbound": hold_unbound,
                       "prior": {n for n, t in self.library.items() if t.origin == gamma.PRIOR}})
        return real(self, blob, parent=parent, hold_unbound=hold_unbound)
    gamma.Gamma.load_blob = spy
    try:
        return env, ag, lineage.load(d, ag)
    finally:
        gamma.Gamma.load_blob = real


def _key(t):
    return json.dumps([[a.name for a in t.atoms], t.guard,
                       [a.name for a in t.operand_term.atoms] if t.operand_term else None])


def _held(ag):
    return {_key(t): t for t in ag.gamma.library.values() if t.origin != gamma.PRIOR}


def _gen(d, w):
    return json.loads(lineage_store.file_bytes(Path(d) / w["written"]))


def _installed(rows, ag, label):
    """R-g1's oracle (the reviewer 2026-10-26 03:11, R1): each row loaded ALONE into a fresh Gamma
    by the call game 2's load made (its parent, hold_unbound, invented; aliases dropped, since they
    name other rows), and the name it adds. Guard (a): the oracle's PRIOR atoms are game 2's, and a
    row that adds no name must be in the oracle's own skipped or destroyed report. Returns
    [(row, name or None, the oracle's carried record)]."""
    call = next((c for c in reversed(_LOADS) if c["gamma"] is ag.gamma), None)
    assert call is not None, (label, "(a) game 2's load_blob call was not seen")
    ctx = {k: v for k, v in call["blob"].items() if k not in ("terms", "aliases")}
    out = []
    for r in rows:
        o = gamma.Gamma(call["env"].atoms(), game=ag.gamma.game)
        assert {n for n, t in o.library.items() if t.origin == gamma.PRIOR} == call["prior"], (
            label, "(a) the oracle's PRIOR atoms are not game 2's")
        before = set(o.library)
        rep_o = o.load_blob({**ctx, "terms": [r]}, parent=call["parent"],
                            hold_unbound=call["hold_unbound"])
        new = sorted(set(o.library) - before)
        if not new:
            assert rep_o["built_on_skipped_invention"] or rep_o["destroyed_on_carry"], (
                label, "(a) row installs nothing alone", r["atoms"], r.get("handle"),
                rep_o["refused"])
            out.append((r, None, None))
            continue
        assert len(new) == 1, (label, "(a) one row installed several names", new)
        out.append((r, new[0], o.carried.get(new[0], {})))
    return out


def _one_name(named):
    """Guard (b), the 21:38 reverser as a check: over the rows, row_key -> installed name is a
    function. None, or the message naming the colliding rows."""
    by = {}
    for r, n, _c in named:
        if n is not None:
            by.setdefault(gamma.Gamma.row_key(r), set()).add(n)
    bad = {k: sorted(ns) for k, ns in by.items() if len(ns) > 1}
    return (f"row_key coarser than load: (d) can alias two installed terms: {bad}"
            if bad else None)


def _not_held(named, lib, carried, parent):
    """R-g1 by installed name: each named row's term is in game 2's library, IMPORTED, naming the
    parent, unbound exactly when the oracle's is. The problems, empty when held."""
    bad = []
    for r, n, oc in named:
        if n is None:
            continue
        t, c = lib.get(n), carried.get(n, {})
        if t is None:
            bad.append(("not held", n))
        elif t.origin != gamma.IMPORTED:
            bad.append(("not IMPORTED", n))
        elif c.get("parent") != parent:
            bad.append(("parent", n, c.get("parent")))
        elif ("unbound" in c) != ("unbound" in oc):
            bad.append(("(a) the oracle names it unlike game 2", n, r.get("operand")))
    return bad


def _carries(rows, ag, rep, label, mf=False):
    """R-g1 as registered: every row is held as an IMPORTED term naming the parent, matched by the
    NAME load installs from it (_installed, the reviewer 2026-10-26 03:11), so no two rows share a
    lookup key. A row whose binding was its whole content is held as its UNBOUND entry (carried
    records what it lost). A row that lands on a PRIOR atom was destroyed on carry: R-g1 FAILS.
    Prints the gap (b) and asserts row_key -> name is a function. Returns (held as compositions,
    held as unbound entries)."""
    assert not rep["destroyed_on_carry"], (label, "R-g1 FAILED: terms destroyed on carry",
                                           rep["destroyed_on_carry"])
    named = _installed(rows, ag, label)
    one = _one_name(named)
    assert one is None, (label, one)
    bad = _not_held(named, ag.gamma.library, ag.gamma.carried, rep["parent"])
    assert not bad, (label, "R-g1 FAILED", len(bad), len(rows), bad[:3])
    composed, unbound = 0, 0
    for _r, n, _oc in named:
        if n is None:
            continue
        t = ag.gamma.library[n]
        if "unbound" in ag.gamma.carried[n]:
            assert "?" in t.operand and not any(p.startswith("o") and p[1:].isdigit()
                                                for p in t.operand.replace("~", ".")
                                                .replace("_", ".").split(".")), (
                label, "an unbound entry still names an object", t.name)
            unbound += 1
        else:
            composed += 1
    names = {n for _r, n, _c in named if n is not None}
    print(f"  {label} gap (b): rows {len(rows)}, installed names {len(names)}, row_keys "
          f"{len({gamma.Gamma.row_key(r) for r in rows})}, lineage._keys "
          f"{len({lineage._key(r) for r in rows})}; installing nothing alone "
          f"{sum(1 for _r, n, _c in named if n is None)}", flush=True)
    if mf:
        # MUST-FAILS (03:11): one row's installed name dropped from game 2's library; and the
        # function check fed one row_key with two installed names
        victim = next(n for _r, n, _c in named if n is not None)
        lib = {k: v for k, v in ag.gamma.library.items() if k != victim}
        gone = _not_held(named, lib, ag.gamma.carried, rep["parent"])
        assert ("not held", victim) in gone, ("MF: a dropped name was not caught", gone)
        r0 = next(r for r, n, _c in named if n is not None)
        two = _one_name([(r0, "a", {}), (dict(r0), "b", {})])
        assert two and two.startswith("row_key coarser than load"), ("MF: the function check "
                                                                     "passed a collision", two)
        print(f"  {label} MF: {victim} dropped -> not held; one row_key, two names -> red",
              flush=True)
    return composed, unbound


def _partition(f, blob, names):
    """R-g2's terms under (d), TETHER_SAVE_DEDUP (amends registered refuter R-g2, the reviewer
    2026-10-14 20:18, ruled 2026-10-25 21:03): a term whose load key a written row already holds is
    saved as an alias {was, key}, so the rows and the aliases are the blob's terms. None, or the
    first of (a)-(e) that fails. OFF there are no aliases and it is the old check exactly."""
    folded = [{k: v for k, v in r.items() if k not in ("born", "was")} for r in f["terms"]]
    al = {a["was"]: a["key"] for a in f.get("aliases", [])}
    terms = list(zip(blob["terms"], names, strict=True))
    if not set(al) <= set(names):
        return "(a) an alias names no term"
    if folded != [t for t, n in terms if n not in al]:
        return "(b) the rows are not the blob's terms less the aliased ones"
    if not all(gamma.Gamma.row_key(t) == al[n] for t, n in terms if n in al):
        return "(c) an alias's key is not its own term's"
    if not set(al.values()) <= {gamma.Gamma.row_key(r) for r in f["terms"]}:
        return "(d) an alias's key is no written row's"
    # "was" is R7i's field, which the generation ADDS (lineage.write, TETHER_REPLAY_UNIT): each
    # row's must be that term's own name, checked rather than ignored (the reviewer 20:14 b)
    if [r.get("was") for r in f["terms"]] != [n for n in names if n not in al]:
        return "(e) the rows' was are not the non-aliased names"
    return None


PARTS = ("a", "b", "c", "d")     # by name, one process each at landing, each under 5 min (r299)


def on_checks(parts=PARTS):
    assert lineage._CARRY and tether._LINEAGE_HOLD, "the child must be started with both arms"
    tmp = Path(tempfile.mkdtemp(prefix="lineage_"))
    for p in parts:
        globals()[f"_part_{p}"](tmp)
    shutil.rmtree(tmp, ignore_errors=True)


def _part_a(tmp):
    """R-g1, R-g3, N3 and R-g1's second process."""
    d = tmp / "g"
    # R-g1: game 1 from the root, then game 2 loads its generation.
    env, ag1, rep = _agent(d, 0)
    assert rep["parent"] is None, rep
    for _ in range(N):
        ag1.step()
    plant = next((t for t in ag1.gamma.enumerate_closure("val", "val", 2, 4000, {})
                  if len(t.atoms) == 2 and t.name not in ag1.gamma.library), None)
    assert plant is not None, "fixture: no new 2-atom chain to plant"
    ag1.gamma.accept(plant, seq=len(ag1.led), residual=f"o1.x@{ag1.cycle}")
    ag1.end_run("cap")
    w1 = lineage.write(d, ag1, "default")
    rows1 = ag1.gamma.blob()["terms"]
    assert rows1, "fixture: game 1 minted nothing"
    env, ag2, rep2 = _agent(d, 1)
    assert rep2["parent"] == w1["hash"], ("R-g1 parent", rep2.get("parent"), w1)
    composed, unbound = _carries(rows1, ag2, rep2, "R-g1 carry", mf=True)
    assert composed, ("fixture: nothing crossed as a composition", composed, unbound)
    tp = _held(ag2).get(_key(plant))
    cp = ag2.gamma.carried.get(tp.name, {}) if tp is not None else {}
    assert tp is not None and tp.origin == gamma.IMPORTED and "unbound" not in cp, (
        "R-g1 the planted chain did not cross as a composition", plant.name, cp)
    assert cp.get("parent") == w1["hash"], ("R-g1 the plant's parent", cp, w1["hash"])
    print(f"  R-g1 plant: {plant.name} crossed as a composition, IMPORTED, parent "
          f"{cp['parent']} (w1 {w1['hash']})", flush=True)
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


def _part_b(tmp):
    """R-g2."""
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
    names = [r["name"] for r in ag.gamma.blob(with_names=True)["terms"]]
    assert ag.gamma.evidence and ag._dormant, ("fixture: no evidence or no dormant record",
                                               len(ag.gamma.evidence), len(ag._dormant))
    # R-g2 is ABOUT instance aliases and "was == name" (and the evidence written as held), which
    # TETHER_KIND_SAVE (3) changes by construction: pinned to KIND_SAVE OFF for this write (the
    # reviewer 2026-10-29 r299: per check, in the test). ON TWIN: tests/test_kind_save.py
    # check_gridworld (no instance alias / was / evidence name, and the same library, standing and
    # replay through the load)
    kind_save, lineage._KIND_SAVE = getattr(lineage, "_KIND_SAVE", False), False
    try:
        lineage.write(rr, ag, "default")
    finally:
        lineage._KIND_SAVE = kind_save
    _h, f = lineage.head(rr)
    bad = _partition(f, blob, names)
    assert bad is None, ("R-g2 terms", bad)
    al = f.get("aliases", [])
    assert al, "fixture: the save wrote no alias, so the must-fail below has no occasion"
    # MUST-FAIL (the reviewer 2026-10-25 21:03): one alias dropped, and one pointed at a key no row
    # holds; each must go RED, naming the clause
    drop = _partition({**f, "aliases": al[1:]}, blob, names)
    stray = _partition({**f, "aliases": [{**al[0], "key": json.dumps(["no such"])}] + al[1:]},
                       blob, names)
    assert drop and stray, ("R-g2 MF: a broken save passed", drop, stray)
    print(f"  R-g2 terms: {len(blob['terms'])} = {len(f['terms'])} rows + {len(al)} aliases; "
          f"MF one alias dropped -> {drop}; one alias's key stray -> {stray}", flush=True)
    assert f["evidence"] == ag.gamma.evidence, "R-g2 evidence"
    # (c), the reviewer 20:57: the boundary item is written WHOLE, each Term in its term-row form
    gen_rr = json.loads(lineage_store.file_bytes(Path(rr) / f"gen_{_h}.json"))
    assert gen_rr["dormant_refused"] == [], ("R-g2 dormant refused", gen_rr["dormant_refused"])
    assert f["dormant"] == [lineage.term_form(x) for x in ag._dormant], "R-g2 dormant"
    live = {(i, k): t for i, x in enumerate(ag._dormant)
            for k, t in x["stores"]["want_terms"].items()}
    assert live, "fixture: no Term in the dormant record"
    assert all(f["dormant"][i]["stores"]["want_terms"][k]["__term__"] == t.name
               and f["dormant"][i]["stores"]["want_terms"][k]["atoms"] == [a.name for a in t.atoms]
               for (i, k), t in live.items()), "R-g2 dormant: the record is not the live Term's"
    # MUST-FAIL: OFF, the write's own encoder refuses the item, named (the check above would fire)
    arm = lineage._DORMANT_TERM_FORM
    lineage._DORMANT_TERM_FORM = False
    try:
        off, off_refused = lineage.dormant_items(ag._dormant)
    finally:
        lineage._DORMANT_TERM_FORM = arm
    assert not off and off_refused and off_refused[0]["type"] == "Term", ("R-g2 MF", off_refused)
    print(f"  R-g2 dormant: {len(ag._dormant)} boundary item(s) written whole, {len(live)} Term(s) "
          f"in their term-row form; OFF the write refuses {off_refused}", flush=True)
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


def _part_c(tmp):
    """Identity, (d) OFF and ON."""
    # LINEAGE-UNIQUE IDENTITY (the reviewer 20:45): a per-game COUNTER in place of the handle's
    # random suffix, so two games of one name mint the same handle text; both rows must fold.
    cd = tmp / "same_text"
    real = gamma.Term.handle
    count = [0]

    def counted(_self, game, _seed=None):   # term.handle takes the draw seed (HOLD_SEED)
        count[0] += 1
        return f"{game}_X_term_{count[0]:08x}"
    gamma.Term.handle = counted
    # (d) OFF here: the repeated texts come from game 2 re-minting game 1's compositions, which (d)
    # writes as aliases; the (born, handle) keying under test is the same either way
    dedup = lineage._SAVE_DEDUP
    lineage._SAVE_DEDUP = False
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
        lineage._SAVE_DEDUP = dedup
    _h, fc = lineage.head(cd)
    texts = [r["handle"] for r in fc["terms"]]
    same = len(texts) - len(set(texts))
    assert same, ("fixture: no same-text handles arose", written)
    assert len(fc["terms"]) == sum(w["terms"] for w in written), (
        "R-g2 same-text handles folded together", len(fc["terms"]), written)
    print(f"  identity: two same-name games wrote {[w['terms'] for w in written]} rows, "
          f"{same} handle text(s) repeated across them, all {len(fc['terms'])} folded",
          flush=True)
    # (b), (d) ON, the shipped default (the reviewer 2026-10-25 21:15): two DIFFERENT compositions
    # under one handle text. Game 2 gives a term it minted itself the text of a game 1 row
    assert lineage._SAVE_DEDUP, "(b) runs with (d) ON"
    cb = tmp / "same_text_on"
    env, agx, _r = _agent(cb, 0)
    for _ in range(N):
        agx.step()
    agx.end_run("cap")
    wx = lineage.write(cb, agx, "default")
    row1 = next(r for r in _gen(cb, wx)["terms"] if r.get("handle"))
    env, agy, _r = _agent(cb, 1)
    for _ in range(N):
        agy.step()
    agy.end_run("cap")
    own = next((r for r in agy.gamma.blob(with_names=True)["terms"]
                if r["name"] not in agy.gamma.carried
                and gamma.Gamma.row_key(r) != gamma.Gamma.row_key(row1)), None)
    assert own, "(b) fixture: game 2 minted no composition of its own"
    agy.gamma.handles[own["name"]] = row1["handle"]
    wy = lineage.write(cb, agy, "default")
    gy = _gen(cb, wy)
    # the row is FOUND by the name the save writes in "was": under TETHER_KIND_SAVE an instance's is
    # its kind's (3); (b) is about handle identity, so it runs ON (no pin), only the locator moves
    was = (lineage._kind_name(agy.gamma, own["name"])
           if getattr(lineage, "_KIND_SAVE", False) and own.get("operand") else own["name"])
    row2 = next((r for r in gy["terms"] if r.get("was") == was), None)
    assert row2 and row2["handle"] == row1["handle"], ("(b) OCCASION: no same-text row", row2)
    assert gamma.Gamma.row_key(row2) != gamma.Gamma.row_key(row1), "(b) OCCASION: one composition"
    assert was not in {a["was"] for a in gy.get("aliases", [])}, "(b) the row was aliased"
    _h, fb = lineage.head(cb)
    pair = [r for r in fb["terms"] if r["handle"] == row1["handle"]]
    assert {r["born"] for r in pair} == {wx["hash"], wy["hash"]}, ("(b) both rows fold", pair)
    env, agz, _r = _agent(cb, 2)
    got = {agz.gamma.renamed.get(r["was"]) for r in pair}
    assert None not in got and len(got) == 2, ("(b) each loads to its own term", got)
    # MUST-FAIL: the fold re-keyed by handle text alone (a stand-in here, never the shipped code)
    by_text = {r["handle"]: r for r in fb["terms"]}
    kept = sum(r in by_text.values() for r in pair)
    assert len(by_text) < len(fb["terms"]) and kept == 1, (
        "(b) MF: keyed by text, the pair did not collapse", kept)
    print(f"  identity ON: {row1['handle']} names two compositions ({row1['was']}, {row2['was']}), "
          f"born {wx['hash']} and {wy['hash']}, 0 aliases for them; both fold and load to "
          f"{sorted(got)}; MF keyed by text: {len(fb['terms'])} rows -> {len(by_text)}", flush=True)


def _part_d(tmp):
    """ONE PATH."""
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
    # part names on the command line run only those parts (a b c d); none runs all
    parts = [a for a in sys.argv[1:] if a in PARTS]
    r = subprocess.run([sys.executable, "-B", __file__, "--on", *parts], env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
    sys.stdout.write(r.stdout)
    assert r.returncode == 0, f"--on failed:\n{r.stderr[-3000:]}"
    print("lineage carry: OK")


if __name__ == "__main__":
    if "--second" in sys.argv:
        second(sys.argv[sys.argv.index("--second") + 1])
    elif "--on" in sys.argv:
        on_checks(tuple(a for a in sys.argv[sys.argv.index("--on") + 1:] if a in PARTS) or PARTS)
    else:
        main()
