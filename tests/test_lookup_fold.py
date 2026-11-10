"""TETHER_LOOKUP_FOLD (the reviewer 2026-11-04 r999 2b; the ls20 deep profile: _lookup_stream was
177 of ROUTE's 253 s at c8, one dict per (junction x reading pair)). The lookup read per junction
returns _lookup_stream's own values. Gridworld, seed pinned; about a minute.

MF-F1  MUST-STAY: for every slot of a 12-step gridworld agent, described by every reading of its
       object (the widest description the board gives), and for a two-member event, _lookup_fold
       and _lookup_stream return the same query, offered, junctions, held_n, digest, sample and
       named (insertion order included), each from fresh bond state
MF-F2  ON builds no per-pair dict: composer.lookup_iter is never called under the fold; RED on
       HEAD (no arm: the stream is the only path, lookup_iter is called)
MF-F3  the whole ledger of the 12-step run is the same ON and OFF but for the arms row
       (identity_mod_rows), so no row and no decision moved

    python tests/test_lookup_fold.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import composer  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

HERE = Path(__file__).resolve()


def run(out: str | None, steps: int = 12):
    env = world.bind(gridworld.family("default", 0))
    if out:
        os.makedirs(out, exist_ok=True)
    led = ledger.Ledger(path=os.path.join(out, "run.jsonl") if out else None)
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    for _ in range(steps):
        ag.step()
    ag.end_run("cap")
    return ag


def both(ag, ev, members, described, desc_of, hist, slot):
    out = []
    for f in (ag._lookup_stream, ag._lookup_fold):
        ag._bond_inc = {}
        q, n, j, h, dig, sample, named = f(ev, members, described, desc_of, hist, slot=slot)
        out.append((q, n, j, h, dig.hexdigest(), json.dumps(sample, ensure_ascii=False),
                    json.dumps({m: list(v.items()) for m, v in named.items()},
                               ensure_ascii=False)))
    return out


def main():
    if "--run" in sys.argv:
        run(sys.argv[sys.argv.index("--run") + 1])
        return
    sys.path.insert(0, str(HERE.parent.parent / "conform"))
    import identity_mod_rows
    assert hasattr(tether.Agent, "_lookup_fold"), "MF-F2: no fold (HEAD)"
    ag = run(None)
    own = ag.env.slot_owner()
    slots = sorted(s for s in own if s in ag.slot_types)
    pairs = held = 0
    diff = []
    for slot in slots:
        hist = ag.history(slot)
        if len(hist) < 2:
            continue
        described = {s: ag.slot_types[s] for s, o in own.items()
                     if o == own[slot] and s in ag.slot_types}
        a, b = both(ag, None, (slot,), described, {slot: described}, hist, slot)
        pairs += a[1]
        held += a[3]
        if a != b:
            diff.append((slot, [i for i in range(7) if a[i] != b[i]]))
    objs = sorted({own[s] for s in slots})
    s1, s2 = (next(s for s in slots if own[s] == o and len(ag.history(s)) > 1) for o in objs[:2])
    d1 = {s: ag.slot_types[s] for s in slots if own[s] == own[s1]}
    d2 = {s: ag.slot_types[s] for s in slots if own[s] == own[s2]}
    a, b = both(ag, "e0", (s1, s2), {**d1, **d2}, {s1: d1, s2: d2}, ag.history(s1), s1)
    if a != b:
        diff.append(("event", [i for i in range(7) if a[i] != b[i]]))
    assert pairs and held and not diff, ("MF-F1", pairs, held, diff[:5])

    calls = [0]
    real = composer.lookup_iter

    def spy(*a, **k):
        calls[0] += 1
        return real(*a, **k)
    composer.lookup_iter = spy
    try:
        ag._bond_inc = {}
        ag._lookup_fold(None, (s1,), d1, {s1: d1}, ag.history(s1), slot=s1)
        on_calls = calls[0]
        ag._lookup_stream(None, (s1,), d1, {s1: d1}, ag.history(s1), slot=s1)
    finally:
        composer.lookup_iter = real
    assert on_calls == 0 and calls[0] > 0, ("MF-F2", on_calls, calls[0])

    with tempfile.TemporaryDirectory() as td:
        rows = {}
        for name, extra in (("on", {}), ("off", {"TETHER_LOOKUP_FOLD": "0"})):
            out = str(Path(td) / name)
            env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
                   "TETHER_AGENT_SEED": "0", **extra}
            r = subprocess.run([sys.executable, "-B", str(HERE), "--run", out], env=env,
                               capture_output=True, text=True, timeout=900)
            assert r.returncode == 0, r.stderr[-2000:]
            rows[name] = [json.loads(x) for x in
                          Path(out, "run.jsonl").read_text(encoding="utf-8").splitlines()]
        d3 = identity_mod_rows.compare(rows["off"], rows["on"], set())
        assert all(d.startswith("seq 0 (arms)") for d in d3), ("MF-F3", d3[:3])
        n_lookup = sum(r.get("event") == "lookup" for r in rows["on"])
    print(f"  MF-F1 {len(slots)} slots and an event: fold == stream ({pairs} pairs, {held} held)")
    print(f"  MF-F2 lookup_iter calls: fold {on_calls}, stream {calls[0]}")
    print(f"  MF-F3 ledger ON vs OFF: {len(d3)} difference(s), the arms row only "
          f"({n_lookup} lookup rows)")
    print("test_lookup_fold OK")


if __name__ == "__main__":
    main()
