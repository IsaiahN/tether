"""E1 (the reviewer 2026-10-19 11:27 item 2): k1_digest.py with the load report's "replayed" value added.
K1, THE STATE DIGEST after the kind switch (the reviewer 2026-10-19 10:45 item 4). state_digest.py's set-up (the
agent built over sc25 through arc_holdout.wire on a lineage COPY, nothing played), digesting every load structure
EXCEPT the kind trio itself (kind_known, kind_known_n, kind_last), which the switch leaves empty by design, and in
its place WHAT ITS READERS SEE:
  pair_counts   ag._pair_counts() (the 7m pair totals)
  t2_cands      ON: the store snapshot's candidates; OFF: the known keys whose (entry, target) has no landing in
                kind_known_dk (target = kind_x for a CAUSE, kind_o otherwise), each with (n, last) as T2 reads them
  nocount       ON: the snapshot; OFF: the known keys with no kind_known_n entry
  kind_seq, kind_pairs, kinds_known (the load report's count)
Each structure: its length and the sha256 of a canonical, order-free form. Run once ON and once OFF; compare.
argv: repo lineage_copy out_json"""
import hashlib
import json
import os
import random
import sys

sys.dont_write_bytecode = True
REPO, LIN, OUT = sys.argv[1:4]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
os.chdir(REPO)
import arc_holdout  # noqa: E402, I001
import lineage  # noqa: E402
import tether  # noqa: E402
from arc_agi import Arcade  # noqa: E402


def canon(x):
    if isinstance(x, dict):
        return ["D", sorted(([canon(k), canon(v)] for k, v in x.items()), key=repr)]
    if isinstance(x, (set, frozenset)):
        return ["S", sorted((canon(v) for v in x), key=repr)]
    if isinstance(x, (list, tuple)):
        return ["T" if isinstance(x, tuple) else "L", [canon(v) for v in x]]
    if isinstance(x, (int, float, str, bool)) or x is None:
        return x
    return ["R", repr(x)]


def tgt(e):
    return e[3] if e[1] == "CAUSE" else e[2]


games = sorted(os.listdir(os.path.join(REPO, "environment_files")))
first = random.Random("49b07888").sample(games, len(games))[0]
arc = Arcade(operation_mode=arc_holdout._mode())
env, ag, led, _b, _p, loaded = arc_holdout.wire(arc.make(first), "stream",
                                                led_path=os.path.join(os.path.dirname(OUT), "digest.jsonl"),
                                                lineage_dir=LIN)
on = ag._kind_store is not None
if on:
    t2 = {e: (n, (lv[3] if lv[0] is not None else 0)) for e, (n, lv) in ag._kind_store["t2"].items()}
    noc = set(ag._kind_store["nocount"])
else:
    dkk = {e[1:] for e in ag._kind_known_dk}
    t2 = {e: (ag._kind_known_n.get(e, 1), ag._kind_last.get(e, (0, 0, 0, 0))[3])
          for e in ag._kind_known if (e[0], tgt(e)) not in dkk}
    noc = {e for e in ag._kind_known if e not in ag._kind_known_n}
rep = (loaded or {}).get("lineage", {}) if isinstance(loaded, dict) else {}
S = {
    "lineage_parent": ag.lineage_parent, "seed": getattr(ag, "seed", None),
    "generation": getattr(ag, "generation", None),
    "gamma_blob": ag.gamma.blob(with_names=True),
    "replayed": rep.get("replayed"),
    "pair_counts": ag._pair_counts(), "t2_cands": t2, "nocount": noc, "kind_seq": ag._kind_seq,
    "kind_pairs": ag._kind_pairs, "kinds_known": rep.get("kinds_known"),
    "kdk_last": ag._kdk_last, "kind_known_dk": dict(ag._kind_known_dk), "kind_known_off": dict(ag._kind_known_off),
    "line_grade_in": ag._line_grade_in, "root_grade_in": ag._root_grade_in, "kind_carried_in": ag._kind_carried_in,
    "cause_kind_in": ag._cause_kind_in, "entry_use_in": ag._entry_use_in, "3a_in": ag._3a_in,
    "3a_written": ag._3a_written, "carried_used": ag.gamma.carried_used,
    "pending_index": {k[1:]: (v["gen"], [(i, ch, lineage._enc_c(c), lineage._enc_c(t)) for i, ch, c, t in v["items"]])
                      for k, v in lineage._PENDING.items()},
    "ak_wholes": {k[1:]: sorted(map(repr, v["slots"])) for k, v in lineage._AK_PENDING.items() if None in v["slots"]},
    "index_store": len(tether._INDEX_STORE),
}
out = {}
for k, v in S.items():
    c = json.dumps(canon(v), sort_keys=True, default=repr)
    out[k] = {"len": len(v) if hasattr(v, "__len__") else None, "sha": hashlib.sha256(c.encode()).hexdigest()[:16]}
out["_arm_memory_store"] = lineage._MEMORY_STORE
out["_trio_sizes"] = [len(ag._kind_known), len(ag._kind_known_n), len(ag._kind_last)]
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps(out, sort_keys=True)[:4000], flush=True)
