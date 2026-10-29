"""2, INSTANCE TERMS LEAVE THE LIVE SET AT THE AGENT'S OWN BREAK (TETHER_INSTANCE_RETIRE, default
ON; the reviewer 2026-10-29 r292, r294). A fake game (test_entry.FakeWrapper plus two pieces) plays
3 steps; one "reuse:" composition is installed per object through Agent._install_reuse and settled
once (evidence kept); the board is then replaced between steps with ONE piece left exactly in
place, and env.arrive() takes it (decision 5 breaks it). Each check runs in its own process.
  check_retire_on      the terms naming objects the break did not re-find leave gamma.library for
                       gamma.retired (still in blob); the exact piece's term stays; the kind (no
                       operand, origin the instance's, residual kind:...) is live and took the
                       instances' evidence by replay; gamma.evidence gains no row; one row
  check_retire_off     MUST-FAIL OFF: every term stays live, no instance_retired row
  check_rebind_kind    ROUTE's _rebindings re-binds the live kind onto a slot of the new board
  check_refound_none   the rule on a board where every named object is re-found: 0 retired, the
                       row written with retired 0 (the seam case with nothing gone)
  check_off_identity   the arm OFF writes the same ledger as 6c04c56 on the plain fake and on the
                       arrival, arms rows aside and wall timings masked
    python tests/test_instance_retire.py [check ...]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

BASE = "6c04c56"      # the tree before the arm

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, mode = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import numpy as np
from arcengine import GameState
import arc_holdout, gate
from gamma import Term
from test_entry import FakeWrapper

def after_board():
    g = np.zeros((64, 64), dtype=int)
    g[5:9, 5:9] = 1          # the static piece, recoloured: not re-found
    g[50:52, 50:56] = 4      # left exactly in place: re-found
    g[15:20, 40:45] = 5
    g[20:22, 20:30] = 6
    return g

class Two(FakeWrapper):
    def __init__(self):
        self.new = None
        super().__init__()

    def _frame(self, state):
        f = super()._frame(state)
        if self.new is None:
            g = f.frame[0].copy()
            g[40:43, 10:15] = 2
            g[50:52, 50:56] = 4
        else:
            g = self.new()
        f.frame = [g]
        return f

w = Two()
env, ag, led, *_ = arc_holdout.wire(w, "fake")
for _ in range(3):
    ag.step()
out = {"mode": mode}
if mode in ("retire", "refound", "bind", "bind_norepoint"):
    ag.gamma.keep_evidence = True
    lib = ag.gamma.library
    atoms = lib["translate"].atoms + lib["recolour"].atoms
    owners = sorted({s.split(".")[0] for s in ag.slots if "." in s and "~" not in s
                     and not s.startswith("@")})
    names = {}
    for o in owners:
        if f"{o}.row" in ag.slots and f"{o}.col" in ag.slots:
            names[o] = ag._install_reuse(Term(atoms, operand=f"{o}.row"), f"{o}.col")
            ag.gamma.settle(names[o], "w", f"{o}.col")
    kind = Term(atoms).name
    # a ONE-ATOM instance: its kind is not the prior atom but the unbound form, as load gives it
    one = ag._install_reuse(Term(lib["translate"].atoms, operand="o1.row"), "o1.colour")
    ag.gamma.settle(one, "w", "o1.colour")
    kind1 = ag.gamma.kind_of(ag.gamma.library[one]).name
    out.update(names=names, kind=kind, ev0=len(ag.gamma.evidence),
               kind_live0=kind in lib, one=one, kind1=kind1)
    if mode == "refound":
        ag._retire_due = ag.cycle          # the rule on this board: every object re-found
        ag._retire_instances()
    else:
        if mode.startswith("bind"):
            # FIXTURE-ONLY SPIES (never an arm): just before the retire, a surviving slot (the
            # re-found piece's) holds the instance naming o1, which the break does not re-find;
            # "bind_norepoint" also disables the re-point, so the invariant has a violation
            real_retire = type(ag)._retire_instances
            def spied(self, *a, **k):
                self.bound["o4.col"] = names["o1"]
                if mode == "bind_norepoint":
                    self._repoint_retired = lambda kind_of: (0, {})
                return real_retire(self, *a, **k)
            type(ag)._retire_instances = spied
        w.new = after_board
        w._frame(GameState.NOT_FINISHED)
        assert env.arrive()
        if mode == "bind_norepoint":
            import traceback
            try:
                ag.step()
            except KeyError as e:           # the hazard r295 names, left un-repointed
                tb = traceback.extract_tb(e.__traceback__)[-1]
                out["raised"] = [repr(e), f"{tb.name}:{tb.lineno}", tb.line]
        else:
            ag.step()
        out["bound_o4"] = ag.bound.get("o4.col")
        if mode == "bind":
            ag.step()                       # the next step's sweep and route read the bindings
            out["stepped"] = True
    st = ag.gamma.standing.get(kind)
    out.update(live={o: n in ag.gamma.library for o, n in names.items()},
               retired=sorted(getattr(ag.gamma, "retired", {})),
               kind_live=kind in ag.gamma.library,
               kind_stamp=ag.gamma.stamps.get(kind),
               kind_origin=getattr(ag.gamma.library.get(kind), "origin", None),
               inst_origin=getattr(ag.gamma.retired.get(names.get("o1", "")) if hasattr(
                   ag.gamma, "retired") else None, "origin", None),
               kind_conf=getattr(st, "confirmations", None), ev1=len(ag.gamma.evidence),
               kind1_live=out["kind1"] in ag.gamma.library,
               kind1_conf=getattr(ag.gamma.standing.get(out["kind1"]), "confirmations", None),
               blob_names=sorted(r["name"] for r in ag.gamma.blob(with_names=True)["terms"]),
               identity={o: env.identity(o) for o in names})
    if mode == "retire" and kind in ag.gamma.library:
        k = ag.gamma.library[kind]
        out["rebind"] = sorted({t.operand for t in ag._rebindings(k, sorted(ag.slots)[0])
                                if t.operand})[:5]
        out["slots_now"] = sorted({s.split(".")[0] for s in ag.slots})
elif mode == "arrive":
    w.new = after_board
    w._frame(GameState.NOT_FINISHED)
    assert env.arrive()
    for _ in range(3):
        ag.step()
else:
    for _ in range(5):
        ag.step()
rows = ag.led.rows()
v = gate.check(rows)
out.update(gate=[v["verdict"], v.get("check"), v.get("token")], rows=rows)
print(json.dumps(out, default=str))
'''


def child(tree: str, mode: str, extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree, mode], env=env,
                         capture_output=True, text=True, timeout=900, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def ev(rows: list, name: str) -> list:
    return [r for r in rows if r["event"] == name]


def check_retire_on() -> None:
    r = child(str(_repo.ROOT), "retire")
    gone = [o for o, idn in r["identity"].items() if idn not in ("overlap", "unique-shape")]
    kept = [o for o in r["identity"] if o not in gone]
    assert gone and kept, ("occasion: the break must leave some objects un-re-found and some "
                           "re-found", r["identity"])
    assert r["kind_live0"] is False, ("occasion: the kind was already live", r["kind"])
    assert all(not r["live"][o] for o in gone) and all(r["live"][o] for o in kept), r["live"]
    # the agent's own reuse installs during play may retire too; none may name a re-found object
    assert {r["names"][o] for o in gone} <= set(r["retired"]), (r["retired"], r["names"])
    assert not any(f"<{o}." in n or f"({o}." in n for n in r["retired"] for o in kept), r["retired"]
    assert set(r["retired"]) <= set(r["blob_names"]), "a retired term left the save (blob)"
    assert r["kind_live"] and str(r["kind_stamp"]["residual"]).startswith("kind:"), r["kind_stamp"]
    assert r["kind_origin"] == r["inst_origin"] is not None, (r["kind_origin"], r["inst_origin"])
    assert r["kind_conf"] and r["kind_conf"] > 0, ("the kind took no evidence", r["kind_conf"])
    assert r["ev1"] == r["ev0"], ("replay wrote evidence rows", r["ev0"], r["ev1"])
    # the one-atom instance: kind = the unbound form load installs, live, holding its evidence
    assert r["one"] in r["retired"] and r["kind1"] == "translate<?.row>", (r["one"], r["kind1"])
    assert r["kind1_live"] and r["kind1_conf"] and r["kind1_conf"] > 0, (r["kind1_live"],
                                                                         r["kind1_conf"])
    row = ev(r["rows"], "instance_retired")
    assert len(row) == 1 and row[0]["detail"]["retired"] == len(r["retired"]), row
    assert row[0]["detail"]["dangling"] == [], ("the invariant", row[0]["detail"]["dangling"])
    assert row[0]["detail"]["kinds_new"] >= 1 and row[0]["detail"]["evidence_replayed"] >= len(gone)
    assert r["gate"][0] == "pass", r["gate"]
    print(f"  ON: break kept {kept}, did not re-find {gone}; {len(r['retired'])} terms retired "
          f"(the fixture's {len(gone)} and the agent's own; all in blob), "
          f"{len(kept)} stays; kind {r['kind']!r} live, origin {r['kind_origin']}, residual "
          f"{r['kind_stamp']['residual']!r}, confirmations {r['kind_conf']:.3f} from "
          f"{row[0]['detail']['evidence_replayed']} replayed rows; evidence {r['ev0']} -> "
          f"{r['ev1']}; one row; gate pass")


def check_retire_off() -> None:
    r = child(str(_repo.ROOT), "retire", {"TETHER_INSTANCE_RETIRE": "0"})
    gone = [o for o, idn in r["identity"].items() if idn not in ("overlap", "unique-shape")]
    assert gone, ("MUST-FAIL occasion: nothing un-re-found", r["identity"])
    assert all(r["live"].values()) and not r["retired"], (r["live"], r["retired"])
    assert not ev(r["rows"], "instance_retired"), "OFF wrote an instance_retired row"
    print(f"  MUST-FAIL OFF: {len(gone)} objects not re-found, all {len(r['live'])} terms stay "
          "live, no row")


def check_invariant_hold() -> None:
    """MUST-HOLD (r295): a surviving slot bound to a retired instance is re-pointed to its kind;
    nothing live names a retired term; the next step (sweep, route) runs without raising."""
    r = child(str(_repo.ROOT), "bind")
    inst = r["names"]["o1"]
    assert inst in r["retired"], ("occasion: the bound instance was not retired", r["retired"])
    row = ev(r["rows"], "instance_retired")
    assert len(row) == 1 and row[0]["detail"]["repointed"] >= 1, row
    assert row[0]["detail"]["dangling"] == [], row[0]["detail"]["dangling"]
    assert r["bound_o4"] == r["kind"], ("not re-pointed to the kind", r["bound_o4"], r["kind"])
    assert r.get("stepped") and r["gate"][0] == "pass", (r.get("stepped"), r["gate"])
    print(f"  INVARIANT HOLDS: o4.col bound to {inst!r} (retired) -> re-pointed to {r['kind']!r}; "
          f"repointed {row[0]['detail']['repointed']}, dropped {row[0]['detail']['dropped']}, "
          f"dangling []; the next step ran; gate pass")


def check_invariant_fail() -> None:
    """MUST-FAIL (r295): with the re-point disabled by a fixture-only spy, the same fixture leaves
    the binding dangling and the invariant check names it."""
    r = child(str(_repo.ROOT), "bind_norepoint")
    inst = r["names"]["o1"]
    row = ev(r["rows"], "instance_retired")
    assert len(row) == 1 and inst in r["retired"], ("occasion", r["retired"])
    dang = row[0]["detail"]["dangling"]
    assert f"bound o4.col: {inst}" in dang, ("the check did not name it", dang)
    print(f"  MUST-FAIL (re-point disabled by a spy): the check names {dang[:2]}; "
          f"the step then raised {r.get('raised')}")


def check_rebind_kind() -> None:
    r = child(str(_repo.ROOT), "retire")
    assert r["kind_live"] and r.get("rebind"), ("ROUTE cannot re-bind the kind", r.get("rebind"))
    owners = {b.split(".")[0] for b in r["rebind"]}
    assert owners <= set(r["slots_now"]), (owners, r["slots_now"])
    print(f"  REBIND: _rebindings re-binds the live kind onto the new board's slots, e.g. "
          f"{r['rebind'][:3]}")


def check_refound_none() -> None:
    r = child(str(_repo.ROOT), "refound")
    assert all(idn in ("overlap", "unique-shape") for idn in r["identity"].values()), (
        "occasion: an object not re-found", r["identity"])
    assert all(r["live"].values()) and not r["retired"], (r["live"], r["retired"])
    row = ev(r["rows"], "instance_retired")
    assert len(row) == 1 and row[0]["detail"]["retired"] == 0, row
    print(f"  ALL RE-FOUND: {len(r['live'])} terms, every object re-found: 0 retired, the row "
          "written with retired 0")


def check_off_identity() -> None:
    root = str(_repo.ROOT)
    sys.path.insert(0, os.path.join(root, "conform"))
    from identity_mod_rows import mask_timings

    def norm(rows):
        return [(r["cycle"], r["step"], r["slot"], r["event"],
                 json.dumps(r["detail"], sort_keys=True, default=str))
                for r in mask_timings(json.loads(json.dumps(rows))) if r["event"] != "arms"]
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        for mode in ("plain", "arrive"):
            base = norm(child(d, mode)["rows"])
            cur = norm(child(root, mode, {"TETHER_INSTANCE_RETIRE": "0"})["rows"])
            diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base)
                                                                                  - len(cur))
            assert len(base) > 50 and diff == 0, ("OFF identity", mode, len(base), len(cur),
                                                 next((i for i, (x, y) in enumerate(
                                                     zip(base, cur, strict=False)) if x != y),
                                                     None))
            print(f"  OFF identity ({mode}): {len(base)} rows against {BASE}, 0 differences")


def main() -> int:
    want = set(sys.argv[1:])
    checks = [v for k, v in globals().items() if k.startswith("check_")
              and (not want or k in want)]
    assert not want or len(checks) == len(want), ("unknown check name", sorted(want))
    for c in checks:
        c()
        print("ok  ", c.__name__)
    print(f"instance_retire: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
