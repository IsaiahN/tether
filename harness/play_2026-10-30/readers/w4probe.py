import os, sys, tempfile, sqlite3
sys.dont_write_bytecode = True
HERE = sys.argv[1]; sys.path.insert(0, HERE); os.chdir(HERE)
import lineage, lineage_store as ls, tether
from test_w4 import agent, steps
d = tempfile.mkdtemp(prefix="w4p_")
for _g in range(2):
    env, ag = agent(d); steps(env, ag, 6); ag.end_run("cap"); lineage.write(d, ag, "fake")
print("wal after 2 games", ls.wal_bytes(d))
env, b = agent(d)
print("B snapshot open; wal", ls.wal_bytes(d))
steps(env, b, 6)
q = next(iter({k[0] for k in b._kind_landed_dk}))
r0 = b._dk_snap.rows(q)
rep = lineage.boundary(d, b, "fake", "level")
print("boundary store:", {k: v for k, v in (rep.get("store") or {}).items() if k != "sleep"} if isinstance(rep.get("store"), dict) else rep.get("store"))
print("wal after merge", ls.wal_bytes(d))
con = ls.open_store(d)
print("checkpoint TRUNCATE with B's reader open:", con.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchone())
con.close()
print("wal after checkpoint", ls.wal_bytes(d))
r1 = b._dk_snap.rows(q)
print("B's held rows unchanged after the checkpoint:", r0 == r1)
fresh = lineage.DkSnapshot(d); print("fresh differs:", fresh.rows(q) != r0); fresh.close()
