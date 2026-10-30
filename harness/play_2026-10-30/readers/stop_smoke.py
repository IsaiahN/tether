"""1c smoke: N steps on a world; stop_rule rows by rule, split_refused, split_aim_left, the aim map's
peak, probes aimed at a refused gap's owner, owed_import entries from rule (ii). argv: world, steps."""
import collections
import sys

sys.dont_write_bytecode = True
sys.path[:0] = ["c:/Users/Admin/Documents/GitHub/tether", "c:/Users/Admin/Documents/GitHub/tether/tests"]
import tether  # noqa: E402

tether._AGENT_SEED = False
which, n = sys.argv[1], int(sys.argv[2])
if which == "fake":
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
else:
    import gamma
    import gridworld
    import ledger
    import world
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), led)
peak = 0
for _ in range(n):
    if which == "fake":
        env.observe()
    ag.step()
    peak = max(peak, len(ag._split_aim))
    if which == "fake" and env.terminal():
        break
rows = led.rows()
rules = collections.Counter((r["detail"]["rule"], r["detail"].get("cause")) for r in rows if r["event"] == "stop_rule")
ref = [r for r in rows if r["event"] == "ask_unsplit"]
left = collections.Counter(r["detail"]["why"] for r in rows if r["event"] == "split_aim_left")
risky = len(ag._risky)
print(f"{which} {n}: rows {len(rows)}; stop_rule {dict(rules)}; split_refused {len(ref)}; "
      f"split_aim_left {dict(left)}; aim peak {peak}; risky (slot,term) {risky}; asks "
      f"{sum(1 for r in rows if r['event'] == 'ask')}")
for r in rows:
    if r["event"] in ("stop_rule", "ask_unsplit", "split_aim_left"):
        print(" ", r["cycle"], r["step"], r["slot"], r["event"],
              {k: v for k, v in r["detail"].items() if k != "reads"})
