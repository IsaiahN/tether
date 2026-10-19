"""The third element's type in a generation's three dk lists (read only). argv: gen.json result.json"""
import collections
import json
import sys

with open(sys.argv[1], encoding="utf-8") as fh:
    g = json.load(fh)
for k in ("kinds_dk_last", "kinds_landed_dk", "kinds_offered_dk"):
    c = collections.Counter(type(x[0][2]).__name__ for x in g.get(k) or ())
    print(k, len(g.get(k) or ()), dict(c))
with open(sys.argv[2], encoding="utf-8") as fh:
    r = json.load(fh)
print({k: r.get(k) for k in ("error", "agent_steps", "actions", "s_per_step_mean", "s_per_step_max", "step_s",
                             "level_changes", "censored", "won", "wall_s")})
