"""test_gate_ledger: every row is labelled with the step actually running, the running steps keep
the ladder's order, and the gate passes a fresh ALL-ON ledger (the reviewer 2026-10-16 07:40, 07:45,
09:18, 09:23, 10:42, 10:52). test_gate passed 43/43 while every ALL-ON ledger from 0996891 failed
the gate, because no smoke ran the gate over a real ledger; and the gate's ordering sees a mislabel
only when it follows a later step of the same slot, so both halves are checked directly.

  GUARD   Ledger.record is wrapped. LABEL: every row an Agent writes carries its _running_step,
          except the ALLOW sites (rows by design labelled with a later step the method itself
          carries out). LADDER: within each (cycle, slot) the running steps never go back on
          ledger.STEPS, so a helper that runs out of the loop's order is caught even when its
          label agrees with it. Lineage's load-time IMPORT rows are written outside an agent and
          are out of scope.
  G1      a fake game (12 actions, C-seed-X): both guards hold; gate.py exits 0.
  G2      gridworld_s2, 11 steps, under C-seed-X: precondition, one inline-phase row; both
          guards hold; gate.py exits 0. Then a second 11-step run with TETHER_DERIVED_PERCEPT
          off, the one member where the MINT-site sweep is reached (step 3): precondition, at
          least one sweep row under MINT; LABEL holds.
  MF1     G1's stream rows put back at PLAN: gate.py refuses step-order.
  MF2     G1's slot-bound choice rows put back at PLAN: gate.py refuses step-order.
  MF3     G2's arm-off sweep rows (pull, reuse_install written in MINT) put back at ROUTE:
          LABEL flags them.
  MF4     _narrate_cues decorated PERCEIVE again (f4a48c4's error: the top-of-step block runs
          before choose, in PLAN): 11 steps of gridworld_s2 and LADDER flags it.

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

# 12, not 6, since E0 (TETHER_DERIVED_PERCEPT, 2026-10-17): the precondition needs one mint SEARCH
# (a stream row). At 6 actions the only searches had been on drow / dcol / speed, the double
# charges E0 declares derived; without them every mint there parks under the floor (42 of 42);
# 12 actions give 111 stream rows
MAX_ACTIONS = 12
# MF4_STEPS 11, not 5, since E0: LADDER catches the misplaced cue row only once a PLAN row
# follows it on "*" (note_goals); with E0 its first is at cycle 10 (cycle 4 with the arm off)
GW_MEMBER, GW_STEPS, MF4_STEPS = "gridworld_s2", 11, 11
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
    """LABEL: writes whose label is not the running step, outside ALLOW."""
    return [w for w in writes if w[2] != w[3] and (w[0], w[1]) not in ALLOW]


def ladder(writes: list, steps: tuple) -> list:
    """LADDER: writes whose running step goes back on the ladder within their (cycle, slot)."""
    last, out = {}, []
    for w in writes:
        k, i = (w[5], w[6]), steps.index(w[3])
        if k in last and i < last[k]:
            out.append(w[:4] + w[5:])
        last[k] = i
    return out


def main() -> int:
    assert not [k for k in os.environ if k.startswith("TETHER_")], "run with no TETHER vars"
    import panel

    import gamma
    import ledger
    import relations
    import tether
    import tether_agent
    import world
    from test_entry import FakeWrapper

    writes: list = []           # (function, event, label, running, detail, cycle, slot)
    real = ledger.Ledger.record

    def spy(self, cycle, step, slot, event, of=None, **detail):
        f = sys._getframe(1)
        ag = f.f_locals.get("self")
        if isinstance(ag, tether.Agent):
            writes.append((f.f_code.co_name, event, step, ag._running_step, detail, cycle, slot))
        return real(self, cycle, step, slot, event, of, **detail)

    def gridworld(steps: int, path: Path | None):
        seed_was, tether._AGENT_SEED = tether._AGENT_SEED, False     # C-seed-X
        try:
            g, seed = panel._gridworld(GW_MEMBER)
            env = world.bind(g)
            ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"gate_{seed}"), tether.Config(),
                              ledger.Ledger(path=str(path) if path else None))
            for _ in range(steps):
                ag.step()
        finally:
            tether._AGENT_SEED = seed_was

    ledger.Ledger.record = spy
    try:
        with tempfile.TemporaryDirectory() as d:
            led = Path(d) / "fake.jsonl"
            # C-seed-X for G1 too (2026-10-16): under the per-birth seed the fake run's path
            # varied by the draw, and with it whether a slot-bound choice row was written, so
            # the precondition below passed or failed by the draw
            seed_was, tether._AGENT_SEED = tether._AGENT_SEED, False
            try:
                tether_agent.run(FakeWrapper(script={}), "fake", max_actions=MAX_ACTIONS,
                                 lineage_dir=d, led_path=str(led))
            finally:
                tether._AGENT_SEED = seed_was
            assert writes, "precondition: the guard saw no row"
            assert not bad(writes), ("G1 LABEL: rows labelled with a step not running",
                                     bad(writes)[:5])
            assert not ladder(writes, ledger.STEPS), ("G1 LADDER: running steps go back",
                                                      ladder(writes, ledger.STEPS)[:5])
            rows = [json.loads(ln) for ln in led.read_text(encoding="utf-8").splitlines()
                    if ln.strip()]
            stream = [r for r in rows if r.get("event") == "stream"]
            chosen = [r for r in rows if r.get("event") == "choice" and r["slot"] != "@choice"
                      and r["step"] != "PLAN"]
            assert stream, "precondition: no stream row on the fake game"
            assert chosen, "precondition: no slot-bound choice row outside PLAN on the fake game"
            code, out = gate(led)
            assert code == 0, out[-600:]
            print(f"  G1 {len(rows)} rows, {len(writes)} guarded writes, 0 mislabelled, "
                  "0 ladder breaks; gate exit 0")
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
            gled = Path(d) / "gw.jsonl"
            gridworld(GW_STEPS, gled)
            inline = [w for w in writes if w[0] == "step" and w[3] != "PLAN"]
            assert inline, "precondition: no row from step()'s inline phases"
            assert not bad(writes), ("G2 LABEL: rows labelled with a step not running",
                                     bad(writes)[:5])
            assert not ladder(writes, ledger.STEPS), ("G2 LADDER: running steps go back",
                                                      ladder(writes, ledger.STEPS)[:5])
            code, out = gate(gled)
            assert code == 0, out[-600:]
            print(f"  G2 {GW_MEMBER} {GW_STEPS} steps: {len(writes)} guarded writes, "
                  f"{len(inline)} inline-phase rows, 0 mislabelled, 0 ladder breaks; gate exit 0")

            # THE MINT-SITE SWEEP WITH TETHER_DERIVED_PERCEPT OFF (the reviewer 2026-10-17 14:00):
            # its label does not depend on the arm, but with the arm on gridworld_s2 never
            # reaches it (0 in 40 steps; its early sweeps were on proximity / distance, the
            # double charges E0 declares derived), so it is checked where it is reached
            writes.clear()
            arm_was, relations._DERIVED_PERCEPT = relations._DERIVED_PERCEPT, False
            try:
                gridworld(GW_STEPS, None)
            finally:
                relations._DERIVED_PERCEPT = arm_was
            sweep = [w for w in writes if w[1] in ("pull", "reuse_install") and w[3] == "MINT"]
            assert sweep, f"precondition: no MINT sweep row in {GW_STEPS} steps, arm off"
            assert not bad(writes), ("G2 LABEL, arm off: rows labelled with a step not running",
                                     bad(writes)[:5])
            print(f"  G2 arm off: {len(sweep)} sweep rows under MINT, 0 mislabelled")
            planted = [(f, e, "ROUTE" if (e in ("pull", "reuse_install") and r == "MINT") else s,
                        r, *rest) for f, e, s, r, *rest in writes]
            assert bad(planted), "MF3: sweep rows put back at ROUTE were not flagged"
            print(f"  MF3 sweep rows put back at ROUTE: LABEL flags {len(bad(planted))}")

            writes.clear()
            cues = tether.Agent._narrate_cues
            tether.Agent._narrate_cues = tether._in_step("PERCEIVE")(cues)
            try:
                gridworld(MF4_STEPS, None)
            finally:
                tether.Agent._narrate_cues = cues
            assert ladder(writes, ledger.STEPS), ("MF4: a top-of-step helper in PERCEIVE was not "
                                                  "flagged")
            print(f"  MF4 _narrate_cues back in PERCEIVE: LADDER flags "
                  f"{len(ladder(writes, ledger.STEPS))} in {MF4_STEPS} steps")
    finally:
        ledger.Ledger.record = real
    print("gate_ledger: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
