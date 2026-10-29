"""1a DIVIDE, A CARRIED SPACE PER OPEN GAP (TETHER_DIVIDE, default ON; the reviewer 2026-10-29 r279,
r308, r311, r312). Each check runs in its own process, under 5 minutes.
  check_exact_grid    T1/K1: gridworld default seed 0, 24 steps. At every REUSE of a cell an earlier
                      mint wrote, the shadow recomputes its stored prefix (rows, charged, first
                      refuting row) from row 0 over the same rows; 0 differences. Occasions: reuses,
                      lookups (answered) and carried > 0
  check_exact_fake    K1/B3: the fake ARC game, 24 steps, under SHAPE_DECODE: the same shadow, 0
                      differences; occasions: reuses > 0, a peer close, and (1b) unstamped cells
                      reused across a decoder growth; "decoder" is no close cause
  check_b1_unmarked_encoder  B1 (1b): an atom defined only here that re-encodes through
                      _to_shape_id is stamped by observation; after the shape is published its cell
                      is recomputed; CONTROL with the stamp suppressed the reused cell is wrong
  check_b2_rotate     B2 = K2 under 1b: the same for rotate
  check_b4_handles    B4 legs 1 and 3 (r314, r315): the shape table is read only in HANDLES, and
                      none dict-tests its handle; MUST-FAIL a planted reader is caught on both
  check_peers         K3, constructed: a peer leaving flips an old row's group reading; the key's
                      peers part moves; MUST-FAIL as K2
  check_window        K4, constructed: a break moving the window drops rows from history; the key's
                      window part moves; MUST-FAIL as K2
  check_reversal      T3: a term the record refused (a lookup) is re-priced over the new rows once
                      the base passes its bound and then passes the bound; MUST-FAIL: with
                      elimination made permanent (a refuted cell always answered) none does
  check_off_identity_grid, check_off_identity_fake   T4: TETHER_DIVIDE=0 writes the same ledger as
                      549f403 (arms rows aside, wall timings masked)
  check_t2_reach      T2 (CREDIT, restated 05:06, r317): some enumerate_closure call on the fake
                      yields more than its budget -- met chains credited back, past the old cut
  check_t2_mustfail   T2 MUST-FAIL: CREDIT OFF (DIVIDE ON), no call yields more than its budget
  check_credit_off_identity_grid, check_credit_off_identity_fake   TETHER_DIVIDE_CREDIT=0 writes
                      the same ledger as d6a4055 (1b)
  check_store         T5: memo_sizes rows carry both records' sizes ON, neither OFF
  check_cond_a        r312 (a): every space ends in a space_closed row, and no _cannot_pay reads a
                      closed space's cells; the lineage save carries neither record
  check_cond_b        r312 (b): a slot's cells are never handed to another slot's pricing
  check_cond_c        r312 (c): no gap kind holds an object id or a slot name
    python tests/test_divide.py [check ...]
"""
from __future__ import annotations

import collections
import io
import json
import os
import pathlib
import subprocess
import sys
import tarfile
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

BASE = "549f403"      # the tree before the arm


def _agent(which: str, steps: int):
    """A fresh agent on the fixture, stepped; returns (env, agent, ledger)."""
    import tether
    tether._AGENT_SEED = False
    if which == "fake":
        import arc_holdout
        from test_entry import FakeWrapper
        env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    else:
        import gamma
        import gridworld
        import ledger
        import world
        env = world.bind(gridworld.family("default", 0))
        led = ledger.Ledger()
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), led)
    for _ in range(steps):
        if which == "fake":
            env.observe()
        ag.step()
        if which == "fake" and env.terminal():
            break
    return env, ag, led


def _shadow(ag, term, slot: str, robs: list, rows: int) -> tuple:
    """The stored prefix recomputed from row 0: (charged, first refuting row). The test's own copy
    of `_cannot_pay`'s row rules, so a stored cell is checked against a count it did not write."""
    from tether import NOT_RESOLVED
    wrong, ref = 0, None
    for i in range(rows):
        state, action, actual, intent, landed = robs[i]
        if not ag._applies(term, state):
            wrong += 1
        elif ag._out_of_step_range(term, slot, state, actual):
            wrong += 1
            ref = i if ref is None else ref
        else:
            ops = ag._ops(term, state)
            if ops is None:
                wrong += 1
                continue
            got = ag._value_of(term, slot, state, ag._eval_ctx(
                slot, state, action=action, operands=ops, intent=intent, landed=landed,
                guard_ref=term.guard_ref))
            if got is NOT_RESOLVED:
                wrong += 1
            elif got % ag.alphabet[slot] != actual % ag.alphabet[slot]:
                wrong += 1
                ref = i if ref is None else ref
    return wrong, ref


def _spy(stats: collections.Counter, closed: set, by_slot: dict) -> None:
    """Wrap _cannot_pay: shadow every reuse of an earlier mint's cell; note which dicts each slot
    is handed and whether a closed space's dicts are read again."""
    import tether
    cp0, close0 = tether.Agent._cannot_pay, tether.Agent._divide_close
    written: dict = {}      # (slot, term) -> the decoder size its cell was last written at

    def cp(self, term, slot, robs, cost, base, rkey=None):
        if self._dv is not None and isinstance(rkey, tuple):
            ids = (id(rkey[0]), id(rkey[1]))
            by_slot.setdefault(ids, set()).add(slot)
            if ids[0] in closed or ids[1] in closed:
                stats["read_after_close"] += 1
            c = rkey[0].get(term) or rkey[1].get(term)
            size = self._decoder_size()
            if c is not None and c[5] is not None and c[5] != size:
                stats["stale_stamp"] += 1        # 1b: must be recomputed, never reused
            elif (c is not None and (c[3] is None or c[3] == self.cycle)
                    and c[4] < self._dv["mint"] and c[0] <= len(robs)):
                stats["reused"] += 1
                if c[5] is None and written.get((slot, term), size) != size:
                    stats["survived_growth"] += 1   # 1b: an unstamped cell across a growth
                if _shadow(self, term, slot, robs, c[0]) != (c[1], c[2]):
                    stats["differ"] += 1
        r = cp0(self, term, slot, robs, cost, base, rkey)
        if self._dv is not None and isinstance(rkey, tuple):
            c = rkey[0].get(term)
            if c is not None:
                # r314 (3): a stored cell is unstamped or stamped at the size it was read at
                assert c[5] is None or c[5] == self._decoder_size(), ("mixed sizes", c)
                written[(slot, term)] = self._decoder_size()
        return r

    def close(self, slot, cause, seen):
        closed.update((id(seen[1]), id(seen[2])))
        return close0(self, slot, cause, seen)
    tether.Agent._cannot_pay, tether.Agent._divide_close = cp, close


def _rows(led, ev: str) -> list:
    return [r for r in led.rows() if r["event"] == ev]


def check_exact_grid() -> None:
    stats: collections.Counter = collections.Counter()
    _spy(stats, set(), {})
    _env, ag, led = _agent("grid", 24)
    dv = [r["detail"] for r in _rows(led, "divide")]
    assert stats["reused"] > 0, ("occasion: no carried cell reused", dict(stats))
    assert sum(d["answered"] for d in dv) > 0 and sum(d["carried"] for d in dv) > 0, dv[-1]
    assert stats["differ"] == 0, ("T1: a carried cell differs from its recompute", dict(stats))
    best = max(d["m1"] or 0 for d in dv)
    print(f"  T1 gridworld: {stats['reused']} reused cells, 0 differ; answered "
          f"{sum(d['answered'] for d in dv)}, carried {sum(d['carried'] for d in dv)}, "
          f"best m1 {best}")


def check_exact_fake() -> None:
    stats: collections.Counter = collections.Counter()
    _spy(stats, set(), {})
    _env, ag, led = _agent("fake", 24)
    causes = collections.Counter(c for r in _rows(led, "space_closed")
                                 for c in r["detail"]["cause"].split("+"))
    assert stats["reused"] > 0, ("occasion: no carried cell reused", dict(stats))
    assert causes["peers"] > 0, ("occasion: no peer close", dict(causes))
    assert stats["survived_growth"] > 0, ("B3 occasion: no unstamped cell met a growth",
                                          dict(stats))
    assert "decoder" not in causes, ("1b: the decoder still closes spaces", dict(causes))
    assert stats["differ"] == 0, ("K1: a carried cell differs from its recompute", dict(stats))
    print(f"  K1/B3 fake (SHAPE_DECODE): {stats['reused']} reused cells, 0 differ; "
          f"{stats['survived_growth']} reuses of unstamped cells across a decoder growth; "
          f"{stats['stale_stamp']} stamped cells met a grown table and were recomputed; closes "
          f"{dict(causes)}")


def _masked(ag, slot: str, held, *parts: int) -> tuple:
    k = list(ag._divide_key(slot, held))
    for p in parts:
        k[p] = None
    return tuple(k)


def _fresh_frame(ag) -> None:
    """After a test edits the frame's tables: the per-frame caches and the Ctx memo re-read them."""
    ag._shape_cache, ag._frame_cache, ag._decomp_cache = (None, None), {}, None
    if ag._memo is not None:
        ag._memo.clear()


def _stamp_case(make_atom, label: str) -> None:
    """1b: a cell whose rows re-encode a shape is stamped with the table's size; once the frame
    publishes the shape its old row reads differently, and the stamped cell is recomputed, not
    reused. CONTROL: the same cell with its stamp suppressed is reused as it stands: wrong."""
    import arc_atoms
    from gamma import Term
    env, ag, _led = _agent("fake", 12)
    rot = next(a for a in ag.gamma.atoms if a.name == "rotate")
    atom = make_atom(rot)
    table = ag.env._decompose._shapes
    hit = None
    for slot in ag.alphabet:
        if not slot.endswith(".shape"):
            continue
        hist = ag.history(slot)
        for i, (state, *_r) in enumerate(hist):
            s = ag.env.shapes().get(state.get(slot))
            if s and arc_atoms._rotated(s) not in table:
                hit = (slot, hist, i, arc_atoms._rotated(s))
                break
        if hit:
            break
    assert hit, (label, "occasion: no old row whose rotated shape is unpublished")
    slot, hist, i, shape = hit
    robs, term, cells, inf = hist[: i + 1], Term((atom,)), ({}, {}), float("inf")
    size0 = ag._decoder_size()
    ag._cannot_pay(term, slot, robs, 0.0, inf, cells)
    c1 = cells[0][term]
    assert c1[5] == size0, (label, "the cell was not stamped", c1)
    table.setdefault(shape, len(table))                 # the frame publishes it, append-only
    _fresh_frame(ag)
    ag.alphabet = ag._with_last(ag._alphabets(ag.env))
    truth = _shadow(ag, term, slot, robs, len(robs))
    assert truth != (c1[1], c1[2]), (label, "occasion: the growth changed no row", truth, c1)
    ag._cannot_pay(term, slot, robs, 0.0, inf, cells)
    c2 = cells[0][term]
    assert (c2[1], c2[2]) == truth and c2[5] == ag._decoder_size(), (label, "not recomputed", c2)
    cells[0][term] = (*c1[:5], None)
    ag._cannot_pay(term, slot, robs, 0.0, inf, cells)
    c3 = cells[0][term]
    assert (c3[1], c3[2]) == (c1[1], c1[2]) != truth, (label, "control", c3, truth)
    print(f"  {label}: {term.name} on {slot} rows 0..{i} stamped at size {size0}, read "
          f"{(c1[1], c1[2])}; the shape published (size {ag._decoder_size()}), the row reads "
          f"{truth} and the cell was recomputed to it; CONTROL with the stamp suppressed the cell "
          f"is reused at {(c3[1], c3[2])}, wrong")


def check_b1_unmarked_encoder() -> None:
    """B1 (r313): an atom that re-encodes through _to_shape_id, defined here and named in no list or
    declaration anywhere, is stamped by observation -- the cell keys on the decoder anyway."""
    import arc_atoms
    from gamma import NOT_RESOLVED, Atom

    def make(rot):
        def fn(v, c):
            s = arc_atoms._as_shape(v, c)
            if not isinstance(s, frozenset) or not s:
                return NOT_RESOLVED
            return arc_atoms._to_shape_id(arc_atoms._rotated(s), c)
        return Atom("unmarked_turn", fn, rot.in_type, rot.out_type)
    _stamp_case(make, "B1 unmarked encoder")


def check_b2_rotate() -> None:
    """B2 = K2 under 1b: rotate's cell is stamped and refused reuse after the shape is published."""
    _stamp_case(lambda rot: rot, "B2 rotate")


HANDLES = {("arc_atoms.py", "_as_shape"), ("arc_atoms.py", "_to_shape_id"),
           ("tether.py", "_decomp"), ("tether.py", "_shapes_now")}


def check_b4_handles() -> None:
    """B4 (r314 (4), r315), legs 1 and 3; leg 2 is the quick set run with the arm ON. Leg 1: every
    read of a shape table in tracked code outside the tests is one of HANDLES -- a new site fails
    here by name until it is routed through the view. Leg 3: no isinstance(x, dict) or
    type(x) is dict on a shape handle inside those functions (a dict test is quiet on the view)."""
    import ast
    import re
    root = pathlib.Path(_repo.ROOT)
    files = subprocess.run(["git", "-C", str(root), "ls-files", "*.py"], capture_output=True,
                           text=True, check=True).stdout.split()
    read = re.compile(r"""getattr\([^)]*["']shapes["']|\.shapes\(\)|\bc\.shapes\b""")
    dict_test = re.compile(r"isinstance\(\s*\w+\s*,\s*dict\s*\)|type\(\s*\w+\s*\)\s+is\s+dict")
    def scan(fname: str, src: str, found: set, quiet: list) -> None:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            body = ast.get_source_segment(src, node) or ""
            code = "\n".join(ln for ln in body.splitlines() if not ln.strip().startswith("#"))
            code = re.sub(r'""".*?"""', "", code, flags=re.S)
            inner = {n.name for n in ast.walk(node) if n is not node
                     and isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
            if read.search(code) and not inner:
                found.add((fname, node.name))
                if dict_test.search(code):
                    quiet.append((fname, node.name))
    found, quiet = set(), []
    for f in files:
        if f.startswith("tests/") or "/" in f and f.split("/")[0] in ("conform", "harness"):
            continue
        scan(pathlib.Path(f).name, (root / f).read_text(encoding="utf-8"), found, quiet)
    assert found == HANDLES, ("leg 1: a shape table read outside the handles",
                              sorted(found - HANDLES), "missing", sorted(HANDLES - found))
    assert not quiet, ("leg 3: a dict test on a shape handle", quiet)
    # MUST-FAIL: a planted reader with a dict test is caught on both legs, by name
    pf, pq = set(), []
    scan("planted.py", "def planted(c):\n    m = getattr(c, 'shapes', None)\n"
                       "    return m.get(1) if isinstance(m, dict) else None\n", pf, pq)
    assert pf == {("planted.py", "planted")} and pq == [("planted.py", "planted")], (pf, pq)
    print(f"  B4 legs 1 and 3: the shape table is read in exactly {sorted(HANDLES)}; none tests "
          "its handle with isinstance(..., dict) or type(...) is dict; MUST-FAIL a planted reader "
          "with a dict test is caught on both legs")


def check_peers() -> None:
    """K3: an old row's group reading flips when a peer leaves the slot's peer set."""
    from gamma import Term
    from tether import _DIVIDE_PARTS, IDN
    for which, steps in (("fake", 12), ("grid", 12)):
        env, ag, _led = _agent(which, steps)
        ag._divide_key(next(iter(ag.alphabet)), ag.gamma.library[IDN])   # fills the frame's caches
        full = dict(ag._peer_cache)
        readers = [a for a in ag.gamma.atoms if "group" in getattr(a, "reads_ctx", ())]

        def with_peers(slot, peers, term, hist, _ag=ag, _full=full):
            _fresh_frame(_ag)
            _ag._peer_cache = {**_full, slot: peers}
            return _shadow(_ag, term, slot, hist, len(hist))
        hit = None
        for slot in ag.alphabet:
            peers, hist = tuple(full.get(slot, ())), ag.history(slot)
            if len(peers) < 2 or not hist:
                continue
            for a in readers:
                term = Term((a,))
                for p in peers:
                    b0 = with_peers(slot, peers, term, hist)
                    b1 = with_peers(slot, tuple(q for q in peers if q != p), term, hist)
                    if b0 != b1:
                        hit = (slot, hist, p, term, b0, b1)
                        break
                if hit:
                    break
            if hit:
                break
        if hit:
            break
    assert readers, "K3: no atom reads the group"
    assert hit, "K3 occasion: no old row whose charge flips when one peer leaves"
    slot, hist, p, term, b0, b1 = hit
    held = ag.gamma.library[ag.bound.get(slot, IDN)]
    _fresh_frame(ag)
    ag._peer_cache = full
    k0, m0 = ag._divide_key(slot, held), _masked(ag, slot, held, _DIVIDE_PARTS.index("peers"))
    _fresh_frame(ag)
    ag._peer_cache = {**full, slot: tuple(q for q in full[slot] if q != p)}
    k1, m1 = ag._divide_key(slot, held), _masked(ag, slot, held, _DIVIDE_PARTS.index("peers"))
    moved = [n for n, a, b in zip(_DIVIDE_PARTS, k0, k1, strict=True) if a != b]
    assert moved == ["peers"], ("K3: the key did not refuse on peers alone", moved)
    assert m0 == m1, "K3 MUST-FAIL: with peers masked the key should have held"
    print(f"  K3 peers ({which}): {slot}, {term.name} over {len(hist)} rows reads {b0} then {b1} "
          f"when {p} leaves; the key moved on {moved}; MUST-FAIL with peers masked the key holds "
          "and the carried cell would be wrong")


def check_window() -> None:
    """K4: a break moves the window, history drops the rows before it, and robs shifts."""
    from tether import _BREAK_WINDOW, _DIVIDE_PARTS, IDN
    assert _BREAK_WINDOW, "K4 needs TETHER_BREAK_WINDOW (default ON)"
    env, ag, _led = _agent("grid", 10)
    slot = next(s for s in ag.alphabet if len(ag.history(s)) >= 4)
    held = ag.gamma.library[ag.bound.get(slot, IDN)]
    idn = ag.gamma.library[IDN]
    h0 = ag.history(slot)
    before = (_shadow(ag, idn, slot, h0, len(h0)), ag._divide_key(slot, held),
              _masked(ag, slot, held, _DIVIDE_PARTS.index("window")))
    ag._window_at = len(ag.trace) - 2                    # a break two frames back
    h1 = ag.history(slot)
    after = (_shadow(ag, idn, slot, h1, min(len(h1), len(h0))), ag._divide_key(slot, held),
             _masked(ag, slot, held, _DIVIDE_PARTS.index("window")))
    assert len(h1) < len(h0), "K4 occasion: the window dropped no row"
    moved = [n for n, a, b in zip(_DIVIDE_PARTS, before[1], after[1], strict=True) if a != b]
    assert moved == ["window"], ("K4: the key did not refuse on the window alone", moved)
    assert before[2] == after[2], "K4 MUST-FAIL: with the window masked the key should have held"
    assert h1[0] is not h0[0], "K4 occasion: row 0 is the same row"
    print(f"  K4 window: {slot}: history {len(h0)} -> {len(h1)} rows, row 0 is another frame "
          f"(idn charged {before[0][0]} over {len(h0)} vs {after[0][0]} over {len(h1)}); the key "
          f"moved on {moved}; MUST-FAIL with the window masked it holds and a cell's prefix would "
          "count other rows")


def _reversal(permanent: bool) -> collections.Counter:
    import tether
    seen: dict = {}
    out: collections.Counter = collections.Counter()
    cp0 = tether.Agent._cannot_pay

    def cp(self, term, slot, robs, cost, base, rkey=None):
        if self._dv is not None and isinstance(rkey, tuple) and permanent:
            c = rkey[0].get(term) or rkey[1].get(term)
            if c is not None and len(c) > 2 and c[2] is not None:
                self._dv_answered = True             # the must-fail: refuted means refused for good
                return True
        r = cp0(self, term, slot, robs, cost, base, rkey)
        k = (slot, term)
        if self._dv is not None:
            if r and self._dv_answered:
                seen[k] = "answered"
            elif not r and seen.get(k) == "answered":
                out["returned"] += 1                 # refused by the record, then passed the bound
                seen[k] = "returned"
        return r
    tether.Agent._cannot_pay = cp
    _env, _ag, led = _agent("grid", 24)
    out["reopened"] = sum(r["detail"]["terms_reopened"] for r in _rows(led, "divide"))
    return out


def check_reversal() -> None:
    got = _reversal(False)
    assert got["reopened"] > 0 and got["returned"] > 0, ("T3 occasion", dict(got))
    print(f"  T3 reversal: {got['reopened']} eliminated terms re-priced over the new rows; "
          f"{got['returned']} terms the record had refused passed the bound once the base passed "
          "it")


def check_reversal_mustfail() -> None:
    got = _reversal(True)
    assert got["returned"] == 0, ("T3 MUST-FAIL: a permanently refuted term came back", dict(got))
    print("  T3 MUST-FAIL: with elimination permanent, no refused term passes the bound again")


PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, which = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
if which == "fake":
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    n = 16
else:
    import gamma, gridworld, ledger, tether, world
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    n = 24
for _ in range(n):
    ag.step()
ag.end_run("cap")
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''


def _child(tree: str, which: str, extra: dict | None = None) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree, which], env=env,
                         capture_output=True, text=True, timeout=900, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])["rows"]


def _off_identity(w: str, base_tree: str = BASE, arm: str = "TETHER_DIVIDE") -> None:
    root = str(_repo.ROOT)
    sys.path.insert(0, os.path.join(root, "conform"))
    from identity_mod_rows import mask_timings

    def norm(rows):
        return [(r["cycle"], r["step"], r["slot"], r["event"],
                 json.dumps(r["detail"], sort_keys=True, default=str))
                for r in mask_timings(json.loads(json.dumps(rows))) if r["event"] != "arms"]
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", base_tree], capture_output=True,
                             check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = norm(_child(d, w))
    cur = norm(_child(root, w, {arm: "0"}))
    diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base) - len(cur))
    assert len(base) > 50 and diff == 0, ("OFF identity", w, len(base), len(cur),
                                         next((i for i, (x, y) in enumerate(
                                             zip(base, cur, strict=False)) if x != y), None))
    print(f"  OFF identity ({arm}=0, {w}): {len(base)} rows against {base_tree}, 0 differences")


def check_off_identity_grid() -> None:
    _off_identity("grid")


def check_off_identity_fake() -> None:
    _off_identity("fake")


CREDIT_BASE = "d6a4055"     # 1b, the tree before TETHER_DIVIDE_CREDIT


def check_credit_off_identity_grid() -> None:
    _off_identity("grid", CREDIT_BASE, "TETHER_DIVIDE_CREDIT")


def check_credit_off_identity_fake() -> None:
    _off_identity("fake", CREDIT_BASE, "TETHER_DIVIDE_CREDIT")


def check_store() -> None:
    root = str(_repo.ROOT)
    on = [r["detail"]["agent"] for r in _child(root, "grid") if r["event"] == "memo_sizes"]
    off = [r["detail"]["agent"] for r in _child(root, "grid", {"TETHER_DIVIDE": "0"})
           if r["event"] == "memo_sizes"]
    assert on and off, "T5 occasion: no memo_sizes row"
    assert all("divide_slot" in a and "divide_kind" in a for a in on), on[-1]
    assert max(a["divide_slot"] for a in on) > 0 and max(a["divide_kind"] for a in on) > 0, on
    assert not any("divide_slot" in a or "divide_kind" in a for a in off), off[-1]
    print(f"  T5 store: ON memo_sizes carries divide_slot (max "
          f"{max(a['divide_slot'] for a in on)}) and divide_kind (max "
          f"{max(a['divide_kind'] for a in on)}); OFF carries neither")


def check_store_bound() -> None:
    """T5 (r313 4): the SPEED-2 bound holds under the arm -- at each searching mint of an open space
    the tally keeps exactly two generations, this mint's and the last searching mint's (the dict it
    wrote), and nothing older; the peak cells per slot and per agent are reported."""
    import tether
    op0 = tether.Agent._divide_open
    out = collections.Counter()
    peak = {"slot": 0, "agent": 0}

    def op(self, slot, tri, kind, base, units):
        before = self._tally[slot]
        cont = slot in self._space and self._space[slot]["kind"] == kind
        r = op0(self, slot, tri, kind, base, units)
        after = self._tally[slot]
        if cont and tether._SPEED2_BOUND:
            out["rotations"] += 1
            assert after[2] is before[1], "the previous generation is not the last mint's dict"
            assert not after[1], "this mint's generation did not start empty"
        peak["slot"] = max(peak["slot"], len(after[1]) + len(after[2]))
        peak["agent"] = max(peak["agent"], sum(len(v[1]) + len(v[2])
                                               for v in self._tally.values()))
        return r
    tether.Agent._divide_open = op
    _agent("grid", 24)
    assert out["rotations"] > 0, "occasion: no continuing space rotated"
    print(f"  T5 bound: {out['rotations']} generation rotations, each keeping only the last "
          f"searching mint's dict; peak {peak['slot']} cells in one slot, {peak['agent']} in the "
          "agent")


def check_cond_a() -> None:
    import lineage
    stats: collections.Counter = collections.Counter()
    closed: set = set()
    _spy(stats, closed, {})
    _env, ag, led = _agent("grid", 24)
    ag.end_run("cap")
    opened = {(r["slot"], r["detail"]["opened"]) for r in _rows(led, "divide")}
    ended = {(r["slot"], r["detail"]["opened"]) for r in _rows(led, "space_closed")}
    assert opened and opened == ended, ("(a) a space with no space_closed row", opened - ended)
    assert not ag._space, ("(a) a space still open after the run's end", list(ag._space))
    assert stats["read_after_close"] == 0, dict(stats)
    with tempfile.TemporaryDirectory() as d:
        lineage.write(d, ag, "default")
        gens = lineage._read(pathlib.Path(d))
        assert gens, "(a) occasion: the save wrote no generation"
        text = json.dumps(gens, default=str)
    assert "space_closed" not in text and "kind_space" not in text and '"divide' not in text
    print(f"  (a) {len(opened)} spaces, each ended by a space_closed row; 0 reads of a closed "
          "space's cells; the lineage save carries neither record")


def check_cond_b() -> None:
    by: dict = {}
    _spy(collections.Counter(), set(), by)
    _agent("grid", 24)
    shared = {k: v for k, v in by.items() if len(v) > 1}
    assert by, "(b) occasion: no pricing call"
    assert len({s for v in by.values() for s in v}) > 1, "(b) occasion: one slot only"
    assert not shared, ("(b) one slot's cells handed to another", shared)
    print(f"  (b) {len(by)} cell dicts over {len({s for v in by.values() for s in v})} slots, "
          "each handed to one slot only")


def _reach(credit: bool) -> list:
    """Per enumerate_closure call on the fake game: (yields, the budget it was given)."""
    import gamma
    import tether
    tether._DIVIDE_CREDIT = credit
    calls: list = []
    ec0 = gamma.Gamma.enumerate_closure

    def ec(self, in_type, out_type, max_depth, budget, stats=None, order=None):
        rec = [0, budget]
        calls.append(rec)
        for t in ec0(self, in_type, out_type, max_depth, budget, stats, order):
            rec[0] += 1
            yield t
    gamma.Gamma.enumerate_closure = ec
    _agent("fake", 24)
    return calls


def check_t2_reach() -> None:
    """T2 (r312 ask 3, restated 05:06): with CREDIT, some closure walk yields MORE than its budget
    -- the met chains it re-met were credited back and it went past the old cut."""
    calls = _reach(True)
    past = [c for c in calls if c[0] > c[1]]
    assert calls, "occasion: no closure walk"
    assert past, ("T2: no walk went past its budget", max(c[0] for c in calls))
    print(f"  T2: {len(past)} of {len(calls)} closure walks yielded past their budget (most "
          f"{max(c[0] for c in past)} against {past[0][1]})")


def check_t2_mustfail() -> None:
    """T2 MUST-FAIL: CREDIT OFF (DIVIDE ON), no walk yields more than its budget."""
    calls = _reach(False)
    assert calls and max(c[0] for c in calls) >= min(c[1] for c in calls), (
        "occasion: no walk reached its budget", max(c[0] for c in calls))
    assert not [c for c in calls if c[0] > c[1]], "T2 MUST-FAIL: a walk passed its budget"
    most = max(c[0] for c in calls)
    print(f"  T2 MUST-FAIL: CREDIT OFF, {len(calls)} walks, the most yields {most} = the budget; "
          "none past it")


def check_kind_multiset() -> None:
    """r313 1: two gaps differing only in how many slots of a type varied share ONE kind record
    (the same object), and the shadow holds at every reuse on both."""
    import retrieval
    import tether
    stats: collections.Counter = collections.Counter()
    _spy(stats, set(), {})
    last: dict = {}
    ch0, op0 = retrieval.characterise, tether.Agent._divide_open

    def ch(*a, **k):
        g = ch0(*a, **k)
        last["raw"] = tuple(g.get("varies_types") or ())
        return g

    opens: list = []

    def op(self, slot, tri, kind, base, units):
        r = op0(self, slot, tri, kind, base, units)
        opens.append((kind, last.get("raw"), id(self._dv["krec"])))
        return r
    retrieval.characterise, tether.Agent._divide_open = ch, op
    for which in ("grid", "fake"):
        _agent(which, 24)
        pairs = [(a, b) for a in opens for b in opens
                 if a[0] == b[0] and a[1] != b[1] and sorted(set(a[1])) == sorted(set(b[1]))]
        if pairs:
            break
    assert pairs, "occasion: no two gaps differing only in multiplicity"
    assert all(a[2] == b[2] for a, b in pairs), "two such gaps met different kind records"
    assert stats["reused"] > 0 and stats["differ"] == 0, dict(stats)
    a, b = pairs[0]
    print(f"  kind multiset ({which}): {len(pairs)} pairs of gaps differ only in multiplicity "
          f"(e.g. {len(a[1])} vs {len(b[1])} varying of {sorted(set(a[1]))}) and share one kind "
          f"record; {stats['reused']} reuses, 0 differ")


def check_cond_c() -> None:
    import re
    _env, ag, led = _agent("fake", 16)
    pat = re.compile(r"\bo\d+\b")
    kinds = [tuple(k) for k in ag._kind_space] + [
        tuple(json.dumps(r["detail"]["kind"])) for r in _rows(led, "space_closed")]
    slots = set(ag.alphabet)
    assert ag._kind_space, "(c) occasion: no kind record"
    bad = [k for k in ag._kind_space
           if pat.search(json.dumps(k)) or any(s in json.dumps(k) for s in slots)]
    assert not bad, ("(c) a kind holds an object id or slot name", bad[:3])
    print(f"  (c) {len(ag._kind_space)} kinds ({len(kinds)} with the closed rows' kinds): none "
          "holds an object id or a slot name")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    for n in names:             # one process per check: each patches the Agent class
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        assert r.returncode == 0, n
    print(f"divide: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
