"""world2d: a typed 2-D habitat, and the wiring artifacts it must produce.

A TEST WORLD standing in for a capability -- the agent's perception and composition over
typed objects, relations and cross-frame deltas. It is not an ARC game and no answer is
encoded. Everything is drawn from the caller's seed before any agent exists.

THREE CLAIMS, EACH WITH A REFUTER
---------------------------------
1. THE WORLD IS WELL FORMED. slots/observe/step/derived/contacts agree and never crash; the
   relations are derived from positions, and the GOAL IS A RELATION (o0 aligned with o1),
   published only through the hooks.
2. THE AGENT PRODUCES ARTIFACTS. A 15-cycle run at TETHER_AGENT_SEED=0 must write mint rows
   and at least 8 distinct producer atom names appear as minted/accepted in conform.wiring.scan.
3. THE HOOKS ARE LOAD-BEARING (MUST-FAIL). With the relation/derived hooks removed the agent
   cannot perceive the goal relation and fewer names occur. If not, print 'RED as required'
   and fail rather than pass on a world where the hooks are decorative.

MEASUREMENT DISCIPLINE -- fresh process PER EPISODE. cap.HEADS (and other module globals)
accumulate across Agent constructions in one interpreter, so two agents built in one process
are different arms; their mint counts are not comparable and a same-process ON/OFF pair is a
mirror, not a finding. The helper tests/_w2d_run.py is launched anew for each measurement.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["TETHER_AGENT_SEED"] = "0"   # the agent's own seed; OFF => constant 0

import conform.wiring as wiring  # noqa: E402
import world2d  # noqa: E402
from world import bind  # noqa: E402

SEED = 8
STEPS = 15
MIN_NAMES = 8
RUNNER = ROOT / "tests" / "_w2d_run.py"


def _run_fresh(hooks: bool):
    """Run ONE episode in a NEW process; return (ledger rows, wiring.scan result, receipt)."""
    fd, name = tempfile.mkstemp(suffix=".jsonl")
    os.close(fd)
    p = Path(name)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "TETHER_AGENT_SEED": "0"}
    cmd = [sys.executable, str(RUNNER), str(SEED), str(STEPS), "1" if hooks else "0", str(p)]
    done = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=180)
    assert done.returncode == 0, (
        f"world2d episode crashed (rc={done.returncode}):\n{done.stdout}\n{done.stderr}")
    try:
        rows = [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
        scan = wiring.scan([p])
    finally:
        p.unlink(missing_ok=True)
    return rows, scan, done.stdout.strip()


def _minted_names(scan):
    return sorted(n for n, rec in scan.items()
                  if any(s in rec["statuses"] for s in ("minted", "accepted")))


def test_world_is_well_formed():
    """The Env contract and the optional hooks agree; relations are derived, not stored."""
    w = world2d.World2D(seed=SEED, hooks=True)
    env = bind(w)                                   # all ten Env members present
    slots = env.slots()
    obs = env.observe()
    assert slots == sorted(obs), "slots() and observe() must name the same quantities"
    assert set(slots) >= set(w.state) | {world2d.GOAL_SLOT}
    assert len({a.name for a in env.atoms()}) == len(env.atoms()), "atom names unique"

    # A relation is a function of position: recomputing from the same state is identical,
    # and the goal relation itself is published as a hook slot, never a stored field.
    d0 = w.derive(w.state)
    assert d0 == w._derived(w.state)
    assert set(d0) <= set(slots), "derived quantities must be perceivable"
    rel_any = any(k.endswith((".above", ".aligned", ".contact")) for k in d0)
    assert rel_any, "no above/aligned/contact relation was derived"
    assert any(k.endswith(".aligned") for k in d0) and any(
        k.endswith((".grew", ".shrank", ".turned", ".scale")) for k in d0), (
        "the goal relation (aligned) and a cross-frame delta must both be derivable")
    delta_any = any(k.endswith((".grew", ".shrank", ".turned", ".scale")) for k in d0)
    assert delta_any, "no cross-frame delta was derived"
    name, deg = w.objective()
    assert name == "ALIGN(o0, o1)" and deg in (0.0, 1.0), (
        "the objective must be the relation the hooks publish")

    ca = w.contacts()
    for a, b, _kind in w.contact_points():
        assert b in ca.get(a, []) and a in ca.get(b, [])
    assert set(w.relational_slots()) >= {"above", "aligned", "contact"}

    # With the hooks removed the relation is NOT perceivable, but the ground (o0.col ==
    # o1.col) is still computed from positions -- the agent is judged, not told.
    bare = world2d.World2D(seed=SEED, hooks=False)
    assert not bare.derive(bare.state), "no-hook world must publish no derived relation"
    assert bare.contact_points() == []
    assert bare._completed() == int(bare.state["o0.col"] == bare.state["o1.col"])

    before = dict(w.state)
    w.step(w.actions()[SEED % len(w.actions())])
    after = env.observe()
    assert set(after) == set(slots)
    assert after != before, "a press must change something"
    w2 = world2d.World2D(seed=SEED, hooks=True)
    w2.step(w2.actions()[SEED % len(w2.actions())])
    assert w2.state == w.state, "same seed + same action must be the same board"
    assert world2d.World2D(seed=SEED + 1).state != world2d.World2D(seed=SEED).state


def test_agent_produces_wiring_artifacts():
    """Mint rows exist and >= 8 distinct producer atom names occur as minted/accepted."""
    rows, scan, receipt = _run_fresh(hooks=True)
    events = [r.get("event") for r in rows]
    mints = [r for r in rows if r.get("event") == "mint"]
    accepts = [r for r in rows if r.get("event") == "accept"]
    assert mints, "no mint rows: the composition loop never ran"
    assert accepts, "no accept rows: a mint never settled into a binding"
    assert "recognised_inert" in events or "recognised" in events or "board_desc" in events, (
        "no perception row reached the ledger: this world is not legible to the agent")

    names = _minted_names(scan)
    w = world2d.World2D(seed=SEED, hooks=True)
    atom_names = {at.name for at in w.atoms()}
    world_atoms = [n for n in names if n in atom_names]

    print("\n=== FULL WORLD (hooks ON) ===")
    print(receipt)
    print("mint rows:", len(mints), "accept rows:", len(accepts))
    print("distinct minted/accepted names:", len(names))
    print("  ALL:", names)
    print("world atom names among them:", len(world_atoms), world_atoms)

    assert len(names) >= MIN_NAMES, (
        f"only {len(names)} distinct producer names as minted/accepted (< {MIN_NAMES}): {names}. "
        "Panel precondition: inspect this world's hooks before weakening -- the residue must "
        "be sayable in this vocabulary and the occasions present.")


def test_must_fail_hooks_removed_fewer_names():
    """NEGATIVE CONTROL: without relations/derivations, fewer names occur.

    Each run is a fresh process (see module docstring). The goal is a relation published only
    by the hooks, so the no-hook agent is blind to it; a world where removing the hooks did
    not reduce the names would make the wiring seat's artifacts decorative -- refuse that.
    """
    _, full_scan, full_receipt = _run_fresh(hooks=True)
    _, bare_scan, bare_receipt = _run_fresh(hooks=False)
    full_names = _minted_names(full_scan)
    bare_names = _minted_names(bare_scan)

    print("\n=== MUST-FAIL: hooks removed ===")
    print("  ON :", full_receipt, "->", len(full_names), full_names)
    print("  OFF:", bare_receipt, "->", len(bare_names), bare_names)
    if not (len(bare_names) < len(full_names)):
        print("RED as required: removing the relation/derived hooks did not reduce the "
              "distinct producer names (the hooks are not load-bearing in this world).")
    assert len(bare_names) < len(full_names), "RED as required: hooks are decorative"
