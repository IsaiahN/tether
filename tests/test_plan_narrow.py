"""4 PLAN_NARROW (TETHER_PLAN_NARROW, default ON; the reviewer 2026-10-29 r325 ASK 3, r365).
The won shelf entry is CONSTRUCTED in the test (record won 1, the method behind the fake's first
library pick), never read from a learned store. Each check in its own process, under 5 minutes.
  check_no_win_identity_fake   no shelf: ON equals OFF whole-run, masking only the new fields; every
                               ON row is one phase with nothing left uncompiled
  check_run_identity_fake      a won shelf entry: ON equals OFF whole-run, masking only the fields
                               phase 1 leaves partial; OCCASIONS: an ON row picked in phase 1 with
                               texts left uncompiled, and an ON row where phase 2 ran
  check_run_identity_grid      the same on gridworld, where nothing routes: the won group yields
                               no pick and phase 2 runs (OCCASION: an ON row with phases 2)
  check_mustfail_compiles_fewer   MUST-FAIL: at the fake's first narrowed pick, ON reads the
                               compile cache for fewer texts than OFF; OFF (narrowing off) reads
                               all of them
  check_cap_record_phases      a cut inside the proposal writes the cap record with "phases"
  check_off_identity_grid, check_off_identity_fake   TETHER_PLAN_NARROW=0 (off_env) against a228a09
    python tests/test_plan_narrow.py [check ...]
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

from _batch import off_env  # noqa: E402  the batch's arms (r348)

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

BASE = "a228a09"        # wip/ask-stop after 1e, the tree before the arm
TEMPLATE = "{o}.row == {x}.row"     # the method behind the fake's first library pick (r365 2(a))
PARTIAL = ("open", "ranked", "refused", "self_moving", "compiled", "uncompiled", "phases",
           "wall_s")

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, which, shelf = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
if which == "fake":
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
else:
    import gamma, gridworld, ledger, tether, world
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
if shelf:
    ag._goal_shelf["narrow_fixture"] = {"name": "narrow_fixture", "text": None,
                                        "templates": [sys.argv[4]],
                                        "record": {"won": 1, "lost": 0}}
for _ in range(24):
    ag.step()
ag.end_run("cap")
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''


def _child(tree: str, which: str, extra: dict | None = None, shelf: bool = False) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree, which, "1" if shelf else "0",
                          TEMPLATE], env=env, capture_output=True, text=True, timeout=900,
                         cwd=str(_repo.ROOT), stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])["rows"]


def _norm(rows: list, partial: tuple = ()) -> list:
    sys.path.insert(0, os.path.join(str(_repo.ROOT), "conform"))
    from identity_mod_rows import mask_timings
    out = []
    for r in mask_timings(json.loads(json.dumps(rows))):
        if r["event"] == "arms":
            continue
        d = r["detail"]
        if r["event"] == "goal_hypotheses":
            d = {k: v for k, v in d.items() if k not in partial}
            if isinstance(d.get("capped"), dict):
                d["capped"] = {k: v for k, v in d["capped"].items() if k != "phases"}
        out.append((r["cycle"], r["step"], r["slot"], r["event"],
                    json.dumps(d, sort_keys=True, default=str)))
    return out


def _same(a: list, b: list, what: str) -> None:
    diff = sum(1 for x, y in zip(a, b, strict=False) if x != y) + abs(len(a) - len(b))
    assert len(a) > 50 and diff == 0, (what, len(a), len(b), next(
        (i for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y), None))


def _hyp(rows: list) -> list:
    return [r["detail"] for r in rows if r["event"] == "goal_hypotheses"]


def _run_identity(w: str, shelf: bool) -> tuple:
    root = str(_repo.ROOT)
    on = _child(root, w, shelf=shelf)
    off = _child(root, w, {"TETHER_PLAN_NARROW": "0"}, shelf=shelf)
    new = ("compiled", "uncompiled", "phases")
    _same(_norm(on, PARTIAL if shelf else new + ("wall_s",)),
          _norm(off, PARTIAL if shelf else new + ("wall_s",)), f"run identity {w}")
    return _hyp(on), _hyp(off), len(on)


def check_no_win_identity_fake() -> None:
    on, _off, n = _run_identity("fake", False)
    assert on and all(d.get("phases") in (1, None) and not d.get("uncompiled") for d in on), on
    print(f"  fake, no shelf: {n} rows ON = OFF (new fields masked); {len(on)} proposals, every "
          "one a single phase with nothing uncompiled")


def check_run_identity_fake() -> None:
    on, off, n = _run_identity("fake", True)
    narrowed = [d for d in on if d.get("pick") and d.get("phases") == 1 and d.get("uncompiled")]
    assert narrowed, ("occasion: a phase-1 pick with texts left uncompiled", on)
    two = [d for d in on if d.get("phases") == 2]
    assert two, ("occasion: a proposal where the won group held no route and phase 2 ran", on)
    picks_on = [d.get("pick") for d in on]
    assert picks_on == [d.get("pick") for d in off], (picks_on, [d.get("pick") for d in off])
    d = narrowed[0]
    print(f"  fake, a won shelf entry ({TEMPLATE}): {n} rows ON = OFF (phase-1 fields masked); "
          f"{len(narrowed)} phase-1 picks, e.g. {d['pick']!r} with {d['compiled']} compiled, "
          f"{d['uncompiled']} left uncompiled; {len(two)} ran phase 2; picks {picks_on}")


def check_run_identity_grid() -> None:
    on, off, n = _run_identity("grid", True)
    two = [d for d in on if d.get("phases") == 2]
    assert two, ("occasion: the won group held no route and phase 2 ran", on)
    assert [d.get("pick") for d in on] == [d.get("pick") for d in off]
    print(f"  grid, a won shelf entry: {n} rows ON = OFF (phase-1 fields masked); {len(two)} "
          f"proposals ran phase 2 after the won group held no route; picks "
          f"{[d.get('pick') for d in on]}")


def _first_pick_reads(narrow: bool) -> tuple:
    import arc_holdout
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    tether._PLAN_NARROW = narrow
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    ag._goal_shelf["narrow_fixture"] = {"name": "narrow_fixture", "text": None,
                                        "templates": [TEMPLATE], "record": {"won": 1, "lost": 0}}
    reads = []

    class Spy(dict):
        def get(self, k, default=None):
            reads.append(k)
            return super().get(k, default)

    ag._compile_cache = Spy()
    for _ in range(24):
        n0 = len(reads)
        env.observe()
        ag.step()
        rows = [r for r in led.rows()
                if r["event"] == "goal_hypotheses" and r["detail"].get("pick")]
        if rows:
            return len(reads) - n0, rows[0]["detail"]
    raise AssertionError("occasion: no pick in 24 fake steps")


def check_mustfail_compiles_fewer() -> None:
    n_on, d_on = _first_pick_reads(True)
    n_off, d_off = _first_pick_reads(False)
    assert d_on["pick"] == d_off["pick"], (d_on["pick"], d_off["pick"])
    assert d_on["phases"] == 1 and d_on["uncompiled"] > 0, d_on
    assert n_on < n_off, ("MUST-FAIL: narrowing off compiles every text", n_on, n_off)
    print(f"  first pick {d_on['pick']!r}: ON read the compile cache {n_on} times, OFF {n_off}; "
          f"ON left {d_on['uncompiled']} uncompiled")


def check_cap_record_phases() -> None:
    import arc_holdout
    import cap
    import tether
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    ag._goal_shelf["narrow_fixture"] = {"name": "narrow_fixture", "text": None,
                                        "templates": [TEMPLATE], "record": {"won": 1, "lost": 0}}
    real = ag._hyp_propose_body

    def cut(_before):
        ag._hyp_phases = 1
        raise cap.CapReached("test cut")
    ag._hyp_propose_body = cut
    with contextlib.suppress(cap.CapReached):
        ag._hyp_propose(env.observe())
    ag._hyp_propose_body = real
    rows = [r for r in led.rows() if r["event"] == "goal_hypotheses" and r["detail"].get("capped")]
    assert rows and rows[-1]["detail"]["capped"].get("phases") == 1, rows
    print(f"  a cut in the proposal: capped {rows[-1]['detail']['capped']}")


def _off_identity(w: str) -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d, w))
    cur = _norm(_child(root, w, off_env("TETHER_PLAN_NARROW")))   # and every later batch arm
    _same(base, cur, f"OFF identity {w}")
    print(f"  OFF identity (TETHER_PLAN_NARROW=0, {w}): {len(base)} rows against {BASE}, "
          "0 differences")


def check_off_identity_grid() -> None:
    _off_identity("grid")


def check_off_identity_fake() -> None:
    _off_identity("fake")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        assert r.returncode == 0, n
    print(f"plan_narrow: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
