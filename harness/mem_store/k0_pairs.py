"""K0 (the reviewer 2026-10-19 10:13 item 3, 10:12 design): does the store's PAIR table equal _pair_counts() over the
OLD load's kind trio, on the same saves? (1) Every *.json of a lineage COPY hard-linked into an empty scratch folder
(never written) and a store built there by lineage_store.open_store + catch_up; its pair table read and decoded through
sym: (kind_o, kind_x) -> (n, last_seq). (2) The agent built over sc25 through arc_holdout.wire on the COPY itself with
TETHER_MEMORY_STORE unset (the old load), playing nothing; ag._pair_counts() read: (kind_o, kind_x) -> (landings,
latest seq). Compared N/N on the keys and on (n, last), each key in a canonical json form. Printed: counts, the first
20 differences, and how many differences each field carries.
argv: repo lineage_copy scratch_dir"""
import json
import os
import random
import sqlite3
import sys

REPO, LIN, OUT = sys.argv[1:4]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
os.chdir(REPO)
import lineage_store as ls  # noqa: E402


def canon(x):
    return json.dumps(x, sort_keys=True, default=list)


assert not os.path.exists(OUT), "the scratch folder must not exist"
ARCH = os.path.join(OUT, "arch")
os.makedirs(ARCH)
for f in sorted(os.listdir(LIN)):
    if f.endswith(".json"):
        os.link(os.path.join(LIN, f), os.path.join(ARCH, f))
con = ls.open_store(ARCH)
merged = ls.catch_up(con, ARCH)
con.close()
c = sqlite3.connect(f"file:{os.path.join(ARCH, ls.DB)}?mode=ro", uri=True)
sym = dict(c.execute("SELECT id, s FROM sym"))
store = {canon([json.loads(sym[o]), json.loads(sym[x])]): (n, last)
         for o, x, n, last in c.execute("SELECT kind_o, kind_x, n, last_seq FROM pair")}
c.close()
print("STORE", f"saves merged {len(merged)}", f"pairs {len(store)}", flush=True)

import arc_holdout  # noqa: E402
import lineage  # noqa: E402
from arc_agi import Arcade  # noqa: E402

assert not lineage._MEMORY_STORE, "run with TETHER_MEMORY_STORE unset: the old load"
games = sorted(os.listdir(os.path.join(REPO, "environment_files")))
first = random.Random("49b07888").sample(games, len(games))[0]
arc = Arcade(operation_mode=arc_holdout._mode())
_env, ag, *_rest = arc_holdout.wire(arc.make(first), "stream", led_path=os.path.join(OUT, "k0.jsonl"),
                                    lineage_dir=LIN)
agent = {canon([list(o), list(x)]): tuple(v) for (o, x), v in ag._pair_counts().items()}
print("AGENT", f"pairs {len(agent)}", f"kind_known {len(ag._kind_known)}", f"kind_landed {len(ag._kind_landed)}",
      flush=True)
keys = set(store) | set(agent)
same = sum(1 for k in keys if store.get(k) == agent.get(k))
dn = sum(1 for k in keys if k in store and k in agent and store[k][0] != agent[k][0])
dl = sum(1 for k in keys if k in store and k in agent and store[k][1] != agent[k][1])
print("K0", f"keys {len(keys)}", f"identical {same}", f"only store {len(set(store) - set(agent))}",
      f"only agent {len(set(agent) - set(store))}", f"n differs {dn}", f"last differs {dl}", sep="\t", flush=True)
for k in sorted(k for k in keys if store.get(k) != agent.get(k))[:20]:
    print("DIFF", k[:200], "store", store.get(k), "agent", agent.get(k), sep="\t")
