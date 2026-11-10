"""TETHER_MINT_HOIST (the reviewer 2026-11-04; the ls20 self-time profile: _operand_fits 14.9M
calls, _guard_refs 34,637, _round_of 44.8M, _separates 2.29M in one 306 s mint, every one fixed
for the mint). The demo world (world.Transitions, which mints) and gridworld; about two minutes.

MF-H1  MUST-STAY: the 16-cycle demo-world ledger and the 12-step gridworld ledger are the same ON
       and OFF but for the arms row (identity_mod_rows): the minted terms, the park rows with
       their cut_counts and priced, and the books
MF-H2  ON, _operand_fits is called once per (typing signature, pass, bind) per mint, so fewer
       times than OFF on the demo world; RED on HEAD (no hoist: the counts are equal)

    python tests/test_mint_hoist.py
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

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

HERE = Path(__file__).resolve()


def run(which: str, out: str | None) -> int:
    calls = [0]
    real = tether.Agent._operand_fits

    def spy(self, *a):
        calls[0] += 1
        return real(self, *a)
    tether.Agent._operand_fits = spy
    try:
        if which == "demo":
            env = world.bind(world.Transitions())
            led = ledger.Ledger()
            ag = tether.Agent(env, gamma.Gamma(env.atoms()), tether.Config(), led)
            ag.run(16)
        else:
            env = world.bind(gridworld.family("default", 0))
            led = ledger.Ledger()
            ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"),
                              tether.Config(), led)
            for _ in range(12):
                ag.step()
        ag.end_run("cap")
    finally:
        tether.Agent._operand_fits = real
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            for r in led.rows():
                fh.write(json.dumps(r, sort_keys=True, default=str) + "\n")
    return calls[0]


def child(which: str, out: str, extra: dict) -> int:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
           "TETHER_AGENT_SEED": "0", **extra}
    r = subprocess.run([sys.executable, "-B", str(HERE), "--run", which, out], env=env,
                       capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stderr[-2000:]
    return int(r.stdout.strip().splitlines()[-1])


def rows(p: str) -> list:
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def main():
    if "--run" in sys.argv:
        i = sys.argv.index("--run")
        print(run(sys.argv[i + 1], sys.argv[i + 2]))
        return
    sys.path.insert(0, str(HERE.parent.parent / "conform"))
    import identity_mod_rows
    out = {}
    with tempfile.TemporaryDirectory() as td:
        for which in ("demo", "grid"):
            on, off = str(Path(td) / f"{which}_on"), str(Path(td) / f"{which}_off")
            c_on = child(which, on, {})
            c_off = child(which, off, {"TETHER_MINT_HOIST": "0"})
            d = identity_mod_rows.compare(rows(off), rows(on), set())
            mints = sum(r.get("event") == "mint" for r in rows(on))
            out[which] = (c_on, c_off, len(rows(on)), mints, d)
            assert all(x.startswith("seq 0 (arms)") for x in d), ("MF-H1", which, d[:3])
    c_on, c_off, n, mints, _d = out["demo"]
    assert mints and c_on < c_off, ("MF-H2", c_on, c_off, mints)
    for which, (c_on, c_off, n, mints, d) in out.items():
        print(f"  MF-H1 {which}: {n} rows, {mints} mints, ON vs OFF {len(d)} difference(s), "
              f"the arms row only")
        print(f"  MF-H2 {which}: _operand_fits calls ON {c_on} vs OFF {c_off}")
    print("test_mint_hoist OK")


if __name__ == "__main__":
    main()
