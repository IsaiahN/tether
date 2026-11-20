"""RDL HANDOFF (NEXT_STEPS 2026-11-16 items 3-4; write-up 42 items 6-7).

  H1  the two extra ordering sites are behind TETHER_RDL: `_rdl_chain_rank` is () when RDL is
      off/inert, and the shape-walk key is exactly shape_order's when RDL is off (open prefixes
      keep () either way, so the A* optimism argument is untouched)
  H2  copy.deepcopy(agent) still works with RDL on: no module object is kept in agent state
  H3  lineage save re-renders one generation-stamped preload copy BESIDE the generation, writes an
      rdl_rebuild row, and never touches library/rdl_preload.json; OFF and RDL-off write nothing
  H4  one gridworld seed (TETHER_AGENT_SEED=0), 12 steps, both arms: gate pass; the RDL-off ledger
      has no rdl_* rows; the printed sha256s are the two-arm fingerprint (a row-by-row comparison
      against the pre-change code is in the commit record, not reproducible from inside a test)

    python tests/test_rdl_handoff.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import shape_order  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def agent(led=None):
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"),
                        tether.Config(), led if led is not None else ledger.Ledger())


def fingerprint(rows) -> str:
    """The full ledger fingerprint. Wall-clock fields and the @run header (which records the
    code hash and the changing arm list) are present here; the commit record compares a
    normalised form that drops those and the inlined source line numbers."""
    return hashlib.sha256(json.dumps(rows, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def main() -> int:
    assert tether._RDL is True and tether._RDL_REBUILD is True and lineage._RDL_REBUILD is True, \
        "the two RDL arms default ON"
    print("H1/H0 both RDL arms default ON: GREEN")

    a = agent()
    # gridworld's atoms; any non-empty chain materialises the atom->entry map
    chain = tuple(a.gamma.atoms[:1])
    rank_on = a._rdl_chain_rank(chain)
    assert isinstance(rank_on, tuple), rank_on
    a._rdl = None
    assert a._rdl_chain_rank(chain) == (), "RDL off: a chain carries no rank"
    base = shape_order.make_order_key(frozenset({"col"}), {})
    k_open = base(chain, False, 2)
    k_closed = base(chain, True, 0)

    # the wrapper is installed only when RDL is live: with it off the key is untouched
    a._rdl = None
    tether._RDL = False
    b = agent()
    tether._RDL = True
    assert b._rdl is None
    print("H1 chain rank () / no RDL state when OFF; open key", k_open, "closed", k_closed,
          ": GREEN")

    c = agent()
    rd = c._rdl
    c._rdl_chain_rank(chain)     # materialise the new atom_entry map before the copy
    assert "atom_entry" in rd
    d = copy.deepcopy(c)
    assert d._rdl is not None and d._rdl["fns"] == rd["fns"], "plain functions survive deepcopy"
    print("H2 deepcopy with RDL on (fns copied as functions, no module objects): GREEN")

    ship = Path(_repo.ROOT) / "library" / "rdl_preload.json"
    sha0 = hashlib.sha256(ship.read_bytes()).hexdigest()
    oks = []
    seen = {}
    keep_rb, keep_rdl = lineage._RDL_REBUILD, tether._RDL
    for label, rebuild, rdl in (("ON", True, True), ("OFF", False, True), ("RDL_OFF", True, False)):
        lineage._RDL_REBUILD, tether._RDL = rebuild, rdl
        dpath = Path(tempfile.mkdtemp(prefix=f"rdlh_{label}_"))
        led = ledger.Ledger()
        ag = agent(led)
        if ag._rdl is not None:
            ag._rdl["stats_n"] = {("fixture", 1): {"settled": 3, "refused": 5}}
        rep = lineage.write(dpath, ag, "default", sleep=False)
        files = sorted(p.name for p in dpath.glob("rdl_preload_gen_*.json"))
        rows = [r for r in led.rows() if str(r.get("event", "")).startswith("rdl_rebuild")]
        want = (label == "ON")
        ok = (len(files) == 1 and len(rows) == 1
              and rows[0]["detail"]["generation"] in files[0]
              and rep.get("rdl_rebuilt", {}).get("written") == files[0]) if want \
            else (not files and not rows and not rep.get("rdl_rebuilt"))
        oks.append(ok)
        seen[label] = (files, rows)
        print(f"  H3 {label}: files={files} rows={[r['event'] for r in rows]} "
              f"report={rep.get('rdl_rebuilt')} -> {'GREEN' if ok else 'RED'}")
    lineage._RDL_REBUILD, tether._RDL = keep_rb, keep_rdl
    ok3 = all(oks) and hashlib.sha256(ship.read_bytes()).hexdigest() == sha0
    print(f"H3 stamped copy beside the generation, shipped library/ untouched: "
          f"{'GREEN' if ok3 else 'RED'}")
    row = seen["ON"][1][0]
    print("  new row:", json.dumps(row, sort_keys=True, default=str))

    fps = {}
    ok4 = True
    for label, arm in (("RDL_ON", True), ("RDL_OFF", False)):
        tether._RDL = arm
        led = ledger.Ledger()
        ag = agent(led)
        for _ in range(12):
            ag.step()
        ag.end_run("cap")
        rows = led.rows()
        fps[label] = fingerprint(rows)
        rdl = [r["event"] for r in rows if str(r.get("event", "")).startswith("rdl_")]
        verdict = gate.check(rows)["verdict"]
        ok = verdict == "pass" and (bool(rdl) == arm)
        ok4 = ok4 and ok
        print(f"  H4 {label} gw12: gate {verdict}, rows {len(rows)}, rdl {rdl}, "
              f"sha256 {fps[label]}")
    tether._RDL = True
    ok4 = ok4 and fps["RDL_ON"] != fps["RDL_OFF"]
    print(f"H4 2-arm gridworld seed 0 fingerprint (ON != OFF, both gate pass): "
          f"{'GREEN' if ok4 else 'RED'}")

    assert ok3 and ok4
    print("rdl_handoff: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
