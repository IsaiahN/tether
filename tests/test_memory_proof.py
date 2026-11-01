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
EXPECTED = {"check_p1_kind_keeps_attribute": "FAIL", "check_p3_decay_across_lives": "FAIL",
            "check_p4_faulted_step_dropped": "FAIL"}


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
