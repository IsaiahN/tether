"""panel: the gate over the worlds we measure, not only the demo (F505; the reviewer 2026-10-07).

    python conform/panel.py --produce     run the panel, write runs/panel/<member>.jsonl + .stamp
    python conform/panel.py               the seat: refuse a missing, stale or gate-refused ledger

The panel takes 10-16 minutes and the hook about 4, so the seat JUDGES ledgers and never runs
them. Each stamp binds its ledger to the tree that produced it: the sha256 of the ledger and of
every project file the run imported. A ledger from any other tree is stale by construction.

A stamp hashes LINE-ENDING-NORMALISED bytes (CRLF read as LF), so one code checked out as LF in
one tree and CRLF in another is one stamp (the reviewer 2026-10-08 17:24Z: a raw-bytes stamp read
a worktree's ledgers as STALE over line endings alone). Stamps written before carry no "hash"
key and are still judged on raw bytes, as they were made. The seat proves the normalisation on
every run.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
# conform/ off the path: its module names must not shadow the agent's.
sys.path = [str(ROOT)] + [p for p in sys.path
                          if Path(p or ".").resolve() != Path(__file__).resolve().parent]
OUT = ROOT / "runs" / "panel"
# gridworld_arc_*: the SAME boards with the ARC wiring's vocabulary and honest types, together --
# the only variable against gridworld_*, which stays as the control (the reviewer 2026-10-09
# 11:58Z, A4, route (i)).
MEMBERS = ("gridworld_s0", "gridworld_s1", "gridworld_s2", "fake",
           "gridworld_arc_s0", "gridworld_arc_s1", "gridworld_arc_s2")
CYCLES, ACTIONS = 60, 40
REGENERATE = "python conform/panel.py --produce"


HASH = "sha256-lf"


def _sha(path: Path, scheme: str | None = HASH) -> str:
    b = path.read_bytes()
    return hashlib.sha256(b.replace(b"\r\n", b"\n") if scheme == HASH else b).hexdigest()


def _hash_must_fail() -> list[str]:
    """The same text in LF and in CRLF is ONE stamp; a real content change is a different one."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        lf, crlf, edit = (Path(d) / n for n in ("lf.py", "crlf.py", "edit.py"))
        lf.write_bytes(b"a = 1\nb = 2\n")
        crlf.write_bytes(b"a = 1\r\nb = 2\r\n")
        edit.write_bytes(b"a = 1\r\nb = 3\r\n")
        bad = []
        if _sha(lf) != _sha(crlf):
            bad.append("stamp hash: one text in LF and CRLF gave two stamps")
        if _sha(crlf) == _sha(edit):
            bad.append("stamp hash: a content change gave the same stamp")
        if _sha(lf, None) == _sha(crlf, None):
            bad.append("stamp hash: the raw scheme no longer tells LF from CRLF")
        return bad


def _imported() -> dict[str, str]:
    """Every project file this process ran, hashed -- from sys.modules, never listed by hand."""
    files = {Path(__file__).resolve()}
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", None)
        if f and Path(f).resolve().is_relative_to(ROOT) and ".venv" not in Path(f).parts:
            files.add(Path(f).resolve())
    return {p.relative_to(ROOT).as_posix(): _sha(p) for p in sorted(files)}


def _member(name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    led_path = OUT / f"{name}.jsonl"
    if name == "fake":
        import test_entry
        import tether_agent
        tether_agent.run(test_entry.FakeWrapper(), "fake", max_actions=ACTIONS,
                         led_path=str(led_path))
    else:
        import gamma
        import ledger
        import tether
        import world
        g, seed = _gridworld(name)
        env = world.bind(g)
        led = ledger.Ledger()
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"dt_default_{seed}"),
                          tether.Config(), led)
        for _ in range(CYCLES):
            ag.step()
        ag.end_run("cap")          # MC2: the open level resolves at the game (a stamp change)
        with open(led_path, "w", encoding="utf-8") as fh:
            for r in led.rows():
                fh.write(json.dumps(r, default=str, sort_keys=True) + "\n")
    stamp = {"hash": HASH, "ledger": _sha(led_path), "files": _imported()}
    (OUT / f"{name}.stamp").write_text(json.dumps(stamp, indent=1), encoding="utf-8")


def _gridworld(name: str):
    """One gridworld member's board; an `_arc_` member gets the ARC atoms and their types."""
    import gridworld
    seed = int(name.rsplit("s", 1)[1])
    g = gridworld.family("default", seed, CYCLES)
    if "_arc_" in name:
        import arc_atoms
        import arc_predict
        g.atom_set = arc_atoms.three_spaces(arc_predict.predict())
        g.attribute_types = dict(arc_atoms.ATTRIBUTE_TYPE)
    return g, seed


def _arc_vocabulary(g) -> list[str]:
    """What gridworld-arc must hold, read off the board as built: same/other/above accept POSITION
    and COLOUR where the types say so, sign and abs_delta are present, and row/col/colour are
    typed POSITION/COLOUR."""
    import gamma
    atoms = {a.name: a for a in g.atoms()}
    types = g.slot_types()
    need = ("same", "other", "above", "sign", "abs_delta")
    bad = [f"no atom {n}" for n in need if n not in atoms]
    if bad:
        return bad
    for n, ty in (("same", "POSITION"), ("same", "COLOUR"), ("other", "POSITION"),
                  ("other", "COLOUR"), ("above", "POSITION")):
        if not gamma.accepts_type(atoms[n], ty):
            bad.append(f"{n} does not accept {ty}")
    for attr, ty in (("row", "POSITION"), ("col", "POSITION"), ("colour", "COLOUR")):
        if not any(s.endswith("." + attr) and t == ty for s, t in types.items()):
            bad.append(f"no slot .{attr} typed {ty}")
    return bad


def _arc_must_fail() -> list[str]:
    """gridworld-arc passes; the control (toy atoms, EXTENT throughout) and gridworld-arc with its
    types dropped are both caught."""
    arc, _ = _gridworld("gridworld_arc_s0")
    ctrl, _ = _gridworld("gridworld_s0")
    out = [f"gridworld-arc: {b}" for b in _arc_vocabulary(arc)]
    if not _arc_vocabulary(ctrl):
        out.append("gridworld-arc check: the control passed it, so it reads nothing")
    arc.attribute_types = None
    if not _arc_vocabulary(arc):
        out.append("gridworld-arc check: types dropped and it still passed")
    return out


def _produce() -> int:
    """Every member through the throttle (Isaiah 2026-10-09 21:16 CDT; the reviewer 04:31Z).
    Loaded here, by path, not at the top: a member run never loads it, so it stays outside the
    stamp, and conform/ stays off the path."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("throttle", Path(__file__).parent / "throttle.py")
    throttle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(throttle)
    logs = ROOT / "runs" / "panel_logs"
    logs.mkdir(parents=True, exist_ok=True)
    return throttle.run([([sys.executable, __file__, "--member", m], ROOT, logs / f"{m}.log")
                         for m in MEMBERS])


def _seat() -> int:
    import gate
    bad = _hash_must_fail() + _arc_must_fail()
    for name in MEMBERS:
        led_path, stamp_path = OUT / f"{name}.jsonl", OUT / f"{name}.stamp"
        if not (led_path.exists() and stamp_path.exists()):
            bad.append(f"{name}: MISSING")
            continue
        stamp = json.loads(stamp_path.read_text(encoding="utf-8"))
        scheme = stamp.get("hash")
        moved = [f for f, h in stamp["files"].items()
                 if not (ROOT / f).exists() or _sha(ROOT / f, scheme) != h]
        if _sha(led_path, scheme) != stamp["ledger"]:
            moved.append(led_path.name)
        if moved:
            bad.append(f"{name}: STALE ({', '.join(moved[:4])}{' ...' if len(moved) > 4 else ''})")
            continue
        v = gate.check_file(str(led_path))
        if v["verdict"] != gate.PASS:
            bad.append(f"{name}: REFUSED {v['check']} {v['token']} at seq {v['seq']}")
    for b in bad:
        print(b)
    if bad:
        print(f"regenerate: {REGENERATE}")
        return 1
    print(f"{len(MEMBERS)} panel ledgers current and passing")
    return 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--member"]:
        _member(sys.argv[2])
    elif sys.argv[1:2] == ["--produce"]:
        sys.exit(_produce())
    else:
        sys.exit(_seat())
