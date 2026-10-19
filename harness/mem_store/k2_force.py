"""THE FORCED T2 / PAIR CALL (the reviewer 2026-10-19 10:45 item 2 (c), (d), (e)). One agent per process, built over
sc25 through arc_holdout.wire on a COPY of the planted life v2 (its gen_ files copied into <out>/lin), with
TETHER_MEMORY_STORE set (mode on) or unset (mode off) before any import. Agent._kind is stubbed to answer the planted
target kind, so T2 asks about the planted candidates. Then, in this order:
  land F (a counted candidate) -- its last moves this run, condition (c)
  land G with a planted dk -- G is known with NO count (the -1) and gets a dk landing THIS RUN (the run-dk filter)
  variant boundary / mf_reread: lineage.write(<out>/lin, ag, ..., sleep=False), a mid-game boundary save
  variant mf_reread (on only): ag._kind_store re-read from the store AFTER that save -- the MUST-FAIL for (e)
  variant mf_nofilter (on only): ag._kind_landed_dk emptied before the call -- the MUST-FAIL for (d)
  the forced call: ag._tiers(the real library, [], a planted dk, "o0", {}, {}) and ag._pair_counts()
Written to <out>/force.json: the tier sizes, the T2 slice of the output list (key, weight), the whole output list, and
the pair counts. Compare two runs with k2_compare.py.
argv: repo planted_dir out_dir mode variant"""
import json
import os
import random
import shutil
import sys

REPO, PL, OUT, MODE, VAR = sys.argv[1:6]
assert MODE in ("on", "off") and VAR in ("normal", "mf_nofilter", "boundary", "mf_reread")
if MODE == "on":
    os.environ["TETHER_MEMORY_STORE"] = "1"
else:
    os.environ["TETHER_MEMORY_STORE"] = "0"   # explicit: the default is ON (17:03)
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
os.chdir(REPO)
assert not os.path.exists(OUT), "the out folder must not exist"
LIN = os.path.join(OUT, "lin")
os.makedirs(LIN)
for f in os.listdir(PL):
    if f.startswith("gen_") and f.endswith(".json"):
        shutil.copy2(os.path.join(PL, f), os.path.join(LIN, f))
with open(os.path.join(PL, "planted.json"), encoding="utf-8") as fh:
    P = json.load(fh)
import arc_holdout  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
from arc_agi import Arcade  # noqa: E402

assert bool(lineage._MEMORY_STORE) is (MODE == "on"), "the arm is not as the mode says"


def kt(k):
    return (k[0], k[1], tuple(k[2]), tuple(k[3]))


games = sorted(os.listdir(os.path.join(REPO, "environment_files")))
first = random.Random("49b07888").sample(games, len(games))[0]
arc = Arcade(operation_mode=arc_holdout._mode())
_env, ag, _led, _b, _p, loaded = arc_holdout.wire(arc.make(first), "stream",
                                                  led_path=os.path.join(OUT, "force.jsonl"), lineage_dir=LIN)
pk = tuple(P["keys"]["PLANTED_KIND"])
ag._kind = lambda _owner: pk
ag._dk_this = set()
F, G = kt(P["keys"]["F"]), kt(P["keys"]["G"])
ag._land_kind(F)
ag._land_kind(G, dk=("PLANTED_DK", "+", 0))
wrote = None
if VAR in ("boundary", "mf_reread"):
    wrote = lineage.write(LIN, ag, "planted", sleep=False)
if VAR == "mf_reread":
    assert MODE == "on"
    v = lineage._store_view(LIN, ag)
    ag._kind_store = {"pairs": v["pairs"], "nocount": v["nocount"], "t2": v["t2"]}
    ag._kind_store_ver += 1
if VAR == "mf_nofilter":
    assert MODE == "on"
    ag._kind_landed_dk.clear()
ag._dk_this = set()
out, sizes = ag._tiers(tether._library(), [], ("PLANTED_DK_ASK", "+", 0), "o0", {}, {})
i = 0
t2 = []
for tier, c in sizes.items():
    if tier == "T2":
        t2 = out[i:i + c]
    i += c
pc = sorted([list(o), list(x), n, last] for (o, x), (n, last) in ag._pair_counts().items())
res = {"mode": MODE, "variant": VAR, "sizes": sizes, "t2": t2, "out": out, "pair_counts": pc,
       "store_snapshot": ({"t2": sorted(map(repr, ag._kind_store["t2"])),
                           "nocount": sorted(map(repr, ag._kind_store["nocount"]))}
                          if ag._kind_store is not None else None),
       "kind_known": len(ag._kind_known), "wrote": str(wrote)[:300] if wrote else None,
       "loaded_kinds_known": (loaded or {}).get("lineage", {}).get("kinds_known")
       if isinstance(loaded, dict) else None}
with open(os.path.join(OUT, "force.json"), "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1, default=repr)
print("FORCE", MODE, VAR, f"sizes {sizes}", f"t2 {t2}", f"pairs {len(pc)}", sep="\t", flush=True)
