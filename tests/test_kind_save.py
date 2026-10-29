"""3, THE SAVE CARRIES THE KIND, NEVER THE INSTANCE (TETHER_KIND_SAVE, default ON; the reviewer
2026-10-29 r292, r294). lineage.write: an instance row (one with an operand) writes no alias and its
"was" is its kind's name (gamma.Gamma.kind_of); an evidence row naming an instance is written under
the kind name. Each check runs in its own process, by name.
  check_gridworld     gridworld lives written and loaded in two folders, one per arm. MUST-FAIL OFF:
                      the OFF folder holds aliases whose "was" names an object (the occasion).
                      ON: no alias and no evidence row names an instance. MUST-HOLD: the last
                      load has the same library, the same standing for every term and the same
                      replay counts in both folders
  check_two_by_three  the reviewer's 2x3 check: on the fake ARC game, instances retired at a
                      break (TETHER_INSTANCE_RETIRE), then saved and loaded into a fresh agent:
                      the kind's settle and refute counts after the load equal those after the
                      in-life retire
  check_off_identity  the arm OFF writes the same generation (content, handles aside) and the same
                      load report as 6b6c5bb on a gridworld life
    python tests/test_kind_save.py [check ...]
"""
from __future__ import annotations

import dataclasses
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

BASE = "6b6c5bb"      # the tree before the arm
N, LIVES = 20, 2
OID = re.compile(r"\bo\d+\b")


def _gridworld_agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        ledger.Ledger())


def _life(d, n):
    import lineage
    ag = _gridworld_agent()
    rep = lineage.load(d, ag)
    for _ in range(n):
        ag.step()
    ag.end_run("cap")
    return ag, rep


def _standing(gm):
    return {n: dataclasses.asdict(s) for n, s in getattr(gm, "standing", {}).items()}


def check_gridworld() -> None:
    import lineage
    import tether
    tether._AGENT_SEED = False
    tmp = Path(tempfile.mkdtemp(prefix="kindsave_"))
    out = {}
    for arm in (True, False):
        lineage._KIND_SAVE = arm
        d = tmp / ("on" if arm else "off")
        d.mkdir()
        for i in range(LIVES):
            a, _ = _life(d, N + 5 * i)
            lineage.write(d, a, "default")
        b, rep = _life(d, 0)
        out[arm] = (d, b, rep)
    lineage._KIND_SAVE = True
    (d_on, b_on, r_on), (d_off, b_off, r_off) = out[True], out[False]
    g_on, g_off = lineage._read(d_on), lineage._read(d_off)
    inst_al = [a["was"] for g in g_off.values() for a in g.get("aliases", [])
               if OID.search(a["was"])]
    assert inst_al, "MUST-FAIL occasion: the OFF lives wrote no instance alias"
    on_al = [a["was"] for g in g_on.values() for a in g.get("aliases", []) if OID.search(a["was"])]
    on_ev = [e[1] for g in g_on.values() for e in g.get("evidence", []) if OID.search(str(e[1]))]
    on_was = [r["was"] for g in g_on.values() for r in g["terms"] if OID.search(str(r.get("was")))]
    assert not on_al and not on_ev and not on_was, ("ON wrote an instance name", on_al[:3],
                                                    on_ev[:3], on_was[:3])
    lib_on, lib_off = set(b_on.gamma.library), set(b_off.gamma.library)
    assert lib_on == lib_off, ("MUST-HOLD library", sorted(lib_on ^ lib_off)[:8])
    s_on, s_off = _standing(b_on.gamma), _standing(b_off.gamma)
    diff = [n for n in set(s_on) | set(s_off) if s_on.get(n) != s_off.get(n)]
    assert not diff, ("MUST-HOLD standing", diff[:8])
    rp_on, rp_off = dict(r_on["replayed"]), dict(r_off["replayed"])
    assert (rp_on["settle"], rp_on["refute"]) == (rp_off["settle"], rp_off["refute"]), (rp_on,
                                                                                         rp_off)
    print(f"  gridworld {LIVES} lives per arm: OFF wrote {len(inst_al)} instance aliases (e.g. "
          f"{inst_al[0]!r}); ON 0 instance aliases, 0 instance evidence names, 0 instance 'was'; "
          f"last load: library {len(lib_on)} = {len(lib_off)}, standing 0 differing; replay "
          f"ON {rp_on} / OFF {rp_off}")


def check_two_by_three() -> None:
    import numpy as np
    from arcengine import GameState

    import arc_holdout
    import lineage
    import tether
    sys.path.insert(0, os.path.join(str(_repo.ROOT), "tests"))
    from gamma import Term
    from test_entry import FakeWrapper
    tether._AGENT_SEED = False
    assert tether._INSTANCE_RETIRE and lineage._KIND_SAVE, "both arms must be ON"

    def after_board():
        g = np.zeros((64, 64), dtype=int)
        g[5:9, 5:9] = 1
        g[50:52, 50:56] = 4
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

    d = Path(tempfile.mkdtemp(prefix="kind2x3_"))
    w = Two()
    env, ag, _led, *_ = arc_holdout.wire(w, "fake")
    for _ in range(3):
        ag.step()
    ag.gamma.keep_evidence = True
    lib = ag.gamma.library
    atoms = lib["translate"].atoms + lib["recolour"].atoms
    for o in ("o0", "o1", "o2", "o3"):
        n = ag._install_reuse(Term(atoms, operand=f"{o}.row"), f"{o}.col")
        ag.gamma.settle(n, "w", f"{o}.col")
    one = ag._install_reuse(Term(lib["translate"].atoms, operand="o1.row"), "o1.colour")
    ag.gamma.settle(one, "w", "o1.colour")
    kinds = [Term(atoms).name, ag.gamma.kind_of(ag.gamma.library[one]).name]
    w.new = after_board
    w._frame(GameState.NOT_FINISHED)
    assert env.arrive()
    ag.step()
    ret = [r for r in ag.led.rows() if r["event"] == "instance_retired"]
    assert ret and ret[0]["detail"]["retired"] >= 5, ("occasion: nothing retired", ret)

    def counts(g, k):
        # the twin of test_replay_unit (paid by reloaded term) and test_settled_core I2b / I6b
        # (settled, not innate), pinned to KIND_SAVE OFF there (the reviewer r299)
        s = g.standing.get(k)
        return None if s is None else (round(s.confirmations, 6), round(s.refusals, 6),
                                       round(s.rejections, 6), round(sum(s.paid.values()), 6),
                                       g.is_settled(k), k in g.innate)
    in_life = {k: counts(ag.gamma, k) for k in kinds}
    assert all(v and v[0] > 0 for v in in_life.values()), ("the kinds took no evidence", in_life)
    lineage.write(d, ag, "fake")
    gens = lineage._read(d)
    assert not any(OID.search(a["was"]) for g in gens.values() for a in g.get("aliases", []))
    w2 = Two()
    _env2, ag2, *_ = arc_holdout.wire(w2, "fake")
    rep = lineage.load(d, ag2)
    after_load = {k: counts(ag2.gamma, k) for k in kinds}
    assert after_load == in_life, ("2x3: the break and the load disagree", in_life, after_load)
    print(f"  2x3: {ret[0]['detail']['retired']} instances retired at the break; kinds "
          f"(confirmations, refusals, rejections) in life {in_life} == after save + fresh load "
          f"{after_load}; replay {rep.get('replayed')}")


PROBE = r'''
import dataclasses, json, sys, tempfile
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, gridworld, ledger, lineage, tether, world
tether._AGENT_SEED = False
def agent():
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        ledger.Ledger())
from pathlib import Path
d = Path(tempfile.mkdtemp(prefix="ksid_"))
for i in range(2):
    ag = agent()
    lineage.load(d, ag)
    for _ in range(20 + 5 * i):
        ag.step()
    ag.end_run("cap")
    lineage.write(d, ag, "default")
b = agent()
rep = lineage.load(d, b)
def scrub(x):
    if isinstance(x, dict):
        return {k: scrub(v) for k, v in x.items() if k not in ("handle", "born", "parent", "h")}
    if isinstance(x, list):
        return [scrub(v) for v in x]
    return x
gens = sorted(json.dumps(scrub(g), sort_keys=True, default=str)
              for g in lineage._read(d).values())
print(json.dumps({"gens": gens, "library": sorted(b.gamma.library),
                  "replayed": rep.get("replayed")}, default=str))
'''


def check_off_identity() -> None:
    root = str(_repo.ROOT)

    def child(tree, extra):
        env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
        env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0", **extra)
        out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree], env=env,
                             capture_output=True, text=True, timeout=900, cwd=root,
                             stdin=subprocess.DEVNULL)
        assert out.returncode == 0, out.stderr[-3000:]
        return json.loads(out.stdout.strip().splitlines()[-1])
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = child(d, {})
    cur = child(root, {"TETHER_KIND_SAVE": "0"})
    assert base["gens"] and base == cur, ("OFF identity", len(base["gens"]), len(cur["gens"]),
                                          base["replayed"], cur["replayed"])
    print(f"  OFF identity: {len(base['gens'])} generations equal in content (handles aside), "
          f"library {len(base['library'])} equal, replay {base['replayed']} equal, vs {BASE}")


def main() -> int:
    want = set(sys.argv[1:])
    checks = [v for k, v in globals().items() if k.startswith("check_")
              and (not want or k in want)]
    assert not want or len(checks) == len(want), ("unknown check name", sorted(want))
    for c in checks:
        c()
        print("ok  ", c.__name__)
    print(f"kind_save: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
