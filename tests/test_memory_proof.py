"""THE MEMORY PROOF SUITE (the reviewer 2026-10-31 r603; Isaiah 21:31: "prove that library
search, retrieval, and saving is working accurately"). Tests only: each check asserts the property
the library NEEDS, so a check that FAILS is a located defect. Each states its result at 1e9d4d5
(from the audit) before it runs; EXPECTED holds the result at this branch's head. Each in its own
process, by name.
  check_p1_kind_keeps_attribute  AT 1e9d4d5: FAIL. Two instances of one multi-atom chain that
                                 differ only in the attribute (inc . dec<o1.row> and
                                 inc . dec<o1.colour>) must save as TWO kinds; gamma.kind_of keeps
                                 the operand only when the bare chain is a PRIOR atom
                                 (gamma.py 1244-1254), so both become one
  check_p3_decay_across_lives    AT 1e9d4d5: FAIL. A refutation carried from a life that ended at
                                 cycle 250 must decay in the next life; Standing.decay's gap is
                                 max(0, tick - last_tick) (gamma.py 915) and the next life's cycle
                                 starts at 0, so it does not move until that life passes cycle 250
  check_p4_faulted_step_dropped  AT 1e9d4d5: FAIL. A term whose residual names the faulted cycle in
                                 the formats the agent writes ("...@c:stamp") must not be written;
                                 the exclusion is endswith(f"@{fc}") (lineage.py 493), which those
                                 formats never end with
  check_p6_carried_press_term_predicts_at_step_1
                                 AT 1e9d4d5: FAIL. Life 1 (the fake ARC game, written to a fresh
                                 lineage) settles a press term (guard TOUCH / ACTED_SELF); at step
                                 1 of life 2 (loaded from it, its own process) some slot must have
                                 a predictor (_pred_by not None). bound is emptied at every game
                                 and level start (tether.py 4045) and _pred_by is filled from it
                                 (9858), so nothing carried predicts before the first miss
    python tests/test_memory_proof.py [check ...]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import zlib

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
EXPECTED = {"check_p1_kind_keeps_attribute": "FAIL",
            "check_p3_decay_across_lives": "PASS",     # F3a TETHER_DECAY_NEW_LIFE
            "check_p4_faulted_step_dropped": "PASS",   # F4 TETHER_FAULT_FORMATS
            "check_p6_carried_press_term_predicts_at_step_1": "FAIL"}

LIFE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, lin, mode, n = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout
import lineage
from test_entry import FakeWrapper
env, ag, *_ = arc_holdout.wire(FakeWrapper(), "fake", lineage_dir=lin)
out = {"loaded_parent": ag.lineage_parent}
for _ in range(n):
    ag.step()
if mode == "write":
    out["settled"] = sorted(t for t in ag.gamma.library if ag.gamma.is_settled(t)
                            and ag.gamma.library[t].origin != "prior")
    out["settled_press"] = [t for t in out["settled"] if "?TOUCH" in t or "?ACTED" in t]
    ag.end_run("cap")
    out["written"] = lineage.write(lin, ag, "fake")["written"]
else:
    out["pred_by"] = {s: p for s, p in ag._pred_by.items() if p}
    out["slots"] = len(ag._pred_by)
print(json.dumps(out, default=str))
'''


def _gridworld():
    import gamma
    import gridworld
    import world
    env = world.bind(gridworld.family("default", 0))
    return env, gamma.Gamma(env.atoms(), game="fam_default_0")


def check_p1_kind_keeps_attribute() -> None:
    import gamma
    _env, g = _gridworld()
    atoms = ("inc", "dec")      # a multi-atom chain; neither it nor its kind is a PRIOR atom
    assert all(a in g.library for a in atoms), ("the fixture's atoms are not held", atoms)
    objs = tuple(next(x for x in g.atoms if x.name == a) for a in atoms)
    t_row = gamma.Term(objs, operand="o1.row")
    t_col = gamma.Term(objs, operand="o1.colour")
    k_row, k_col = g.kind_of(t_row).name, g.kind_of(t_col).name
    print(f"  {t_row.name} -> kind {k_row}; {t_col.name} -> kind {k_col}")
    assert k_row != k_col, ("one kind for two attributes", k_row)


def check_p3_decay_across_lives() -> None:
    import gamma
    st = gamma.Standing(last_tick=250)
    st.rejections = 2.0
    before = st.rejections
    st.decay(5)                 # the next life, five cycles in: its cycle clock started again at 0
    print(f"  carried rejections {before} at last_tick 250; after decay at the next life's "
          f"cycle 5: {st.rejections}")
    assert st.rejections < before, "a carried refutation did not decay across lives"


def check_p4_faulted_step_dropped() -> None:
    import ledger
    import lineage
    import tether
    env, g = _gridworld()
    ag = tether.Agent(env, g, tether.Config(), ledger.Ledger())
    for _ in range(20):
        ag.step()
    ag.end_run("cap")
    hits = [(c, str(r.get("residual") or "")) for r in ag.gamma.blob(with_names=True)["terms"]
            for c in range(ag.cycle) if f"@{c}:" in str(r.get("residual") or "")]
    assert hits, "PRECONDITION: no residual names a cycle in the '@c:...' form; cannot fire"
    fc, res = hits[0]
    ag._fault_cycle = fc
    with tempfile.TemporaryDirectory() as d:
        out = lineage.write(d, ag, "fam_default_0")
        with open(os.path.join(d, out["written"]), "rb") as fh:
            raw = fh.read()
        gen = json.loads(zlib.decompress(raw) if raw[:1] == b"\x78" else raw)
    written = [t for t in gen["terms"] if str(t.get("residual") or "") == res]
    print(f"  faulted cycle {fc}; a term with residual {res!r}: written {len(written)} time(s)")
    assert not written, ("a term from the faulted step was carried", res)


def _life(lin: str, mode: str, n: int) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    r = subprocess.run([sys.executable, "-B", "-c", LIFE, str(_repo.ROOT), lin, mode, str(n)],
                       env=env, capture_output=True, text=True, timeout=1800,
                       cwd=str(_repo.ROOT), stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def check_p6_carried_press_term_predicts_at_step_1() -> None:
    with tempfile.TemporaryDirectory() as lin:
        one = _life(lin, "write", 40)
        print(f"  life 1: settled non-prior terms {len(one['settled'])} {one['settled'][:3]}, "
              f"of them press terms {len(one['settled_press'])}; wrote {one['written']}")
        # the fake game settles no PRESS term in 40 steps (measured), so the precondition is the
        # audit's general claim: ANY settled carried term, and none predicts at step 1
        assert one["settled"], "PRECONDITION: life 1 settled no term; cannot fire"
        two = _life(lin, "step1", 1)
        print(f"  life 2 (parent {two['loaded_parent']}): after step 1, slots with a predictor "
              f"{len(two['pred_by'])} of {two['slots']} {dict(list(two['pred_by'].items())[:3])}")
        assert two["pred_by"], "nothing carried predicts at step 1 of a new life"


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    got = {}
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        got[n] = "PASS" if r.returncode == 0 else "FAIL"
    for n in names:
        print(f"{n}: expected {EXPECTED.get(n)}, got {got[n]}"
              + ("" if EXPECTED.get(n) == got[n] else "   <-- the audit or the test is wrong"))
    return 0 if all(EXPECTED.get(n) == got[n] for n in names) else 1


if __name__ == "__main__":
    sys.exit(main())
