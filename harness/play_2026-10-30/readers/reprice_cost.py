"""(I2)'s cost and effect: N steps on a world in the given tree; per ask row the stored and re-priced survivors,
the skipped gaps, re-priced cells / rows and reprice_s; ask_none rows; the run wall. argv: tree, world, steps."""
import statistics
import sys
import time

sys.dont_write_bytecode = True
tree, which, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path[:0] = [tree, tree + "/tests"]
import tether  # noqa: E402

tether._AGENT_SEED = False
t0 = time.time()
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
for _ in range(n):
    if which == "fake":
        env.observe()
    ag.step()
    if which == "fake" and env.terminal():
        break
rows = led.rows()
asks = [r for r in rows if r["event"] == "ask"]
none = [r for r in rows if r["event"] == "ask_none"]
rs = [r["detail"]["reprice_s"] for r in asks + none]
print(f"{which} {n} ({tree}): wall {time.time() - t0:.1f} s; asks {len(asks)}; ask_none {len(none)}; reprice_s max "
      f"{max(rs) if rs else None} median {statistics.median(rs) if rs else None}")
for r in asks + none:
    d = r["detail"]
    print(f"  c{r['cycle']} {r['slot']} {r['event']}: stored {d.get('stored_survivors')} -> {d.get('survivors')}; "
          f"skipped {d.get('skipped')}; cells {d.get('repriced_cells')} rows {d.get('repriced_rows')} "
          f"reprice_s {d.get('reprice_s')}; chosen {d.get('chosen')} largest {d.get('largest')}")
