"""S2's N/N CHECK (the reviewer 2026-10-19 06:13 f, 07:35): one process builds the agent over sc25 with the lineage
COPY loaded through arc_holdout.wire (as e4_stream does), plays NOTHING, and writes a canonical digest of every
structure load() fills: per structure its length and the sha256 of a canonical form (sets and dicts sorted, tuples
kept), plus the full canonical form of the small ones. Run once with TETHER_MEMORY_STORE=0 and once with it set,
in two processes; compare the two digest files structure by structure.
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
    """A canonical, order-free form: sets and dict keys sorted by their repr; values canonical too."""
    if isinstance(x, dict):
        return ["D", sorted(([canon(k), canon(v)] for k, v in x.items()), key=repr)]
    if isinstance(x, (set, frozenset)):
        return ["S", sorted((canon(v) for v in x), key=repr)]
    if isinstance(x, (list, tuple)):
        return ["T" if isinstance(x, tuple) else "L", [canon(v) for v in x]]
    if isinstance(x, (int, float, str, bool)) or x is None:
        return x
    return ["R", repr(x)]


games = sorted(os.listdir(os.path.join(REPO, "environment_files")))
first = random.Random("49b07888").sample(games, len(games))[0]
arc = Arcade(operation_mode=arc_holdout._mode())
env, ag, led, _b, _p, loaded = arc_holdout.wire(arc.make(first), "stream",
                                                led_path=os.path.join(os.path.dirname(OUT), "digest.jsonl"),
                                                lineage_dir=LIN)
S = {
    "lineage_parent": ag.lineage_parent, "seed": getattr(ag, "seed", None),
    "generation": getattr(ag, "generation", None),
    "gamma_blob": ag.gamma.blob(with_names=True),
    "kind_known": ag._kind_known, "kind_known_n": dict(ag._kind_known_n), "kind_last": ag._kind_last,
    "kdk_last": ag._kdk_last, "kind_known_dk": dict(ag._kind_known_dk), "kind_known_off": dict(ag._kind_known_off),
    "kind_pairs": ag._kind_pairs, "kind_seq": ag._kind_seq,
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
out["_loaded_keys"] = sorted((loaded or {}).get("lineage", {}).keys()) if isinstance(loaded, dict) else None
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps(out, sort_keys=True)[:4000], flush=True)
