"""Smoke input for clock_read.py: two gridworld 'games' stepped by ONE agent with the clock ON, written as a
round dir (switch.tsv rows in the harness's column positions 0, 1, 3, 14; stream.jsonl). argv: out round dir."""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, "C:/Users/Admin/Documents/GitHub/tether")
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
assert tether._STEP_CLOCK, "the clock is OFF"
env = world.bind(gridworld.family("default", 0, 4))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="clock_fixture"), tether.Config(budget=40),
                  ledger.Ledger())
sw = []
for pos, name in enumerate(("gA", "gB")):
    c0, t0 = ag.cycle, time.perf_counter()
    for i in range(3):
        ag.step()
        if i == 0:
            first = round(time.perf_counter() - t0, 2)
    row = [""] * 18
    row[0], row[1], row[3], row[14] = str(pos), name, str(c0), str(first)
    sw.append("\t".join(row))
open(f"{out}/switch.tsv", "w", encoding="utf-8").write("# fixture\n" + "\n".join(sw) + "\n")
with open(f"{out}/stream.jsonl", "w", encoding="utf-8") as fh:
    for r in ag.led.rows():
        fh.write(json.dumps(r, default=str) + "\n")
print("written", len(ag.led.rows()), "rows")
