"""test_gate_ledger: every row is labelled with the step actually running, and the gate passes a
fresh ALL-ON ledger (the reviewer 2026-10-16 07:40, 07:45, 09:18, 09:23). test_gate passed 43/43
while every ALL-ON ledger from 0996891 failed the gate, because no smoke ran the gate over a real
ledger; and the gate's ordering sees a mislabel only when it follows a later step of the same slot,
so the label is checked directly (THE CLASS GUARD).

  GUARD Ledger.record is wrapped: for every row an Agent writes, its label must equal the agent's
        _running_step at the write, except the ALLOW sites, rows by design labelled with a later
        step the method itself carries out. Lineage's load-time IMPORT rows are written outside
        an agent and are out of scope.
  G1    a fake game (6 actions, the agent's own seed): the guard holds; gate.py exits 0.
  G2    gridworld_s2, 11 steps, under C-seed-X (the old constant seed, so its cycle-10 sweep
        lands): preconditions, at least one sweep row and one inline-phase row; the guard holds;
        gate.py exits 0.
  MF1   G1's stream rows put back at PLAN: gate.py refuses step-order.
  MF2   G1's slot-bound choice rows put back at PLAN: gate.py refuses step-order.
  MF3   G2's sweep rows (pull, reuse_install written in MINT) put back at ROUTE: the guard flags
        them.

    python test_gate_ledger.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

MAX_ACTIONS = 6
GW_MEMBER, GW_STEPS = "gridworld_s2", 11
ALLOW = {("_hold_invention", "accept"), ("_mint", "accept"), ("sweep", "retro"),
         ("_carry", "candidate_woken"), ("_route_reward", "route")}
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "conform"))


def gate(path: Path) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(HERE / "gate.py"), str(path)], capture_output=True,
                       text=True, stdin=subprocess.DEVNULL, cwd=HERE)
    return p.returncode, p.stdout + p.stderr


def put_back(rows: list, out: Path, pick) -> None:
    out.write_text("".join(json.dumps({**r, "step": "PLAN"} if pick(r) else r) + "\n"
                           for r in rows), encoding="utf-8")


def bad(writes: list) -> list:
    return [w for w in writes if w[2] != w[3] and (w[0], w[1]) not in ALLOW]


def main() -> int:
    assert not [k for k in os.environ if k.startswith("TETHER_")], "run with no TETHER vars"
    import panel

    import gamma
    import ledger
    import tether
    import tether_agent
    import world
    from test_entry import FakeWrapper

    writes: list = []           # (function, event, label, running, detail)
    real = ledger.Ledger.record

    def spy(self, cycle, step, slot, event, of=None, **detail):
        f = sys._getframe(1)
        ag = f.f_locals.get("self")
        if isinstance(ag, tether.Agent):
            writes.append((f.f_code.co_name, event, step, ag._running_step, detail))
        return real(self, cycle, step, slot, event, of, **detail)

    ledger.Ledger.record = spy
    try:
        with tempfile.TemporaryDirectory() as d:
            led = Path(d) / "fake.jsonl"
            tether_agent.run(FakeWrapper(script={}), "fake", max_actions=MAX_ACTIONS,
                             lineage_dir=d, led_path=str(led))
            assert writes, "precondition: the guard saw no row"
            assert not bad(writes), ("G1 guard: rows labelled with a step not running",
                                     bad(writes)[:5])
            rows = [json.loads(ln) for ln in led.read_text(encoding="utf-8").splitlines()
                    if ln.strip()]
            stream = [r for r in rows if r.get("event") == "stream"]
            chosen = [r for r in rows if r.get("event") == "choice" and r["slot"] != "@choice"
                      and r["step"] != "PLAN"]
            assert stream, "precondition: no stream row on the fake game"
            assert chosen, "precondition: no slot-bound choice row outside PLAN on the fake game"
            code, out = gate(led)
            assert code == 0, out[-600:]
            print(f"  G1 {len(rows)} rows, {len(writes)} guarded writes, 0 mislabelled; "
                  "gate exit 0")
            badf = Path(d) / "bad.jsonl"
            put_back(rows, badf, lambda r: r.get("event") == "stream")
            code, out = gate(badf)
            assert code != 0 and "step-order" in out, "MF1: stream rows at PLAN were not refused"
            print("  MF1 stream rows put back at PLAN: gate refuses step-order")
            put_back(rows, badf, lambda r: r.get("event") == "choice" and r["slot"] != "@choice")
            code, out = gate(badf)
            assert code != 0 and "step-order" in out, "MF2: choice rows at PLAN were not refused"
            print("  MF2 slot choice rows put back at PLAN: gate refuses step-order")

            writes.clear()
            seed_was, tether._AGENT_SEED = tether._AGENT_SEED, False     # C-seed-X
            try:
                g, seed = panel._gridworld(GW_MEMBER)
                env = world.bind(g)
                gled = Path(d) / "gw.jsonl"
                ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"gate_{seed}"),
                                  tether.Config(), ledger.Ledger(path=str(gled)))
                for _ in range(GW_STEPS):
                    ag.step()
            finally:
                tether._AGENT_SEED = seed_was
            sweep = [w for w in writes if w[1] in ("pull", "reuse_install") and w[3] == "MINT"]
            inline = [w for w in writes if w[0] == "step" and w[3] != "PLAN"]
            assert sweep, f"precondition: no sweep row in {GW_STEPS} steps of {GW_MEMBER}"
            assert inline, "precondition: no row from step()'s inline phases"
            assert not bad(writes), ("G2 guard: rows labelled with a step not running",
                                     bad(writes)[:5])
            code, out = gate(gled)
            assert code == 0, out[-600:]
            print(f"  G2 {GW_MEMBER} {GW_STEPS} steps: {len(writes)} guarded writes, "
                  f"{len(sweep)} sweep rows under MINT, {len(inline)} inline-phase rows, "
                  "0 mislabelled; gate exit 0")
            planted = [(f, e, "ROUTE" if (e in ("pull", "reuse_install") and r == "MINT") else s,
                        r, x) for f, e, s, r, x in writes]
            assert bad(planted), "MF3: sweep rows put back at ROUTE were not flagged"
            print(f"  MF3 sweep rows put back at ROUTE: the guard flags {len(bad(planted))}")
    finally:
        ledger.Ledger.record = real
    print("gate_ledger: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
