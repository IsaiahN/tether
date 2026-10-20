"""test_gate_ledger: the gate over a fresh ALL-ON ledger (the reviewer 2026-10-16 07:40, 07:45).
test_gate passed 43/43 while every ALL-ON ledger from 0996891 failed the gate, because no smoke ran
the gate over a real ledger.

  G1   a fake game (defaults ON, no TETHER vars) writes a ledger with at least one "stream" row and
       one slot-bound "choice" row (preconditions); gate.py over it exits 0.
  MF1  the stream rows put back at PLAN: gate.py refuses step-order.
  MF2  the slot-bound choice rows put back at PLAN: gate.py refuses step-order.

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
HERE = Path(__file__).parent


def gate(path: Path) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(HERE / "gate.py"), str(path)], capture_output=True,
                       text=True, stdin=subprocess.DEVNULL, cwd=HERE)
    return p.returncode, p.stdout + p.stderr


def put_back(rows: list, out: Path, pick) -> None:
    out.write_text("".join(json.dumps({**r, "step": "PLAN"} if pick(r) else r) + "\n"
                           for r in rows), encoding="utf-8")


def main() -> int:
    assert not [k for k in os.environ if k.startswith("TETHER_")], "run with no TETHER vars"
    import tether_agent
    from test_entry import FakeWrapper
    with tempfile.TemporaryDirectory() as d:
        led = Path(d) / "fake.jsonl"
        tether_agent.run(FakeWrapper(script={}), "fake", max_actions=MAX_ACTIONS, lineage_dir=d,
                         led_path=str(led))
        rows = [json.loads(ln) for ln in led.read_text(encoding="utf-8").splitlines() if ln.strip()]
        stream = [r for r in rows if r.get("event") == "stream"]
        chosen = [r for r in rows if r.get("event") == "choice" and r["slot"] != "@choice"
                  and r["step"] != "PLAN"]
        assert stream, "precondition: no stream row on the fake game"
        assert chosen, "precondition: no slot-bound choice row outside PLAN on the fake game"
        assert all(r["step"] == "MINT" for r in stream), {r["step"] for r in stream}
        code, out = gate(led)
        assert code == 0, out[-600:]
        print(f"  G1 {len(rows)} rows: {len(stream)} stream rows under MINT, {len(chosen)} slot "
              f"choice rows under {sorted({r['step'] for r in chosen})}; gate exit 0")
        bad = Path(d) / "bad.jsonl"
        put_back(rows, bad, lambda r: r.get("event") == "stream")
        code, out = gate(bad)
        assert code != 0 and "step-order" in out, "MF1: stream rows at PLAN were not refused"
        print("  MF1 stream rows put back at PLAN: gate refuses step-order")
        put_back(rows, bad, lambda r: r.get("event") == "choice" and r["slot"] != "@choice")
        code, out = gate(bad)
        assert code != 0 and "step-order" in out, "MF2: choice rows at PLAN were not refused"
        print("  MF2 slot choice rows put back at PLAN: gate refuses step-order")
    print("gate_ledger: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
