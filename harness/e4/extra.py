"""E5.2's ruled columns that collect.py does not carry (the reviewer 2026-10-19 02:09 item 2b), one row per E4a game,
never pooled. READ ONLY. Joins collect.py's agent.tsv (carried hits), e4b_estimate's move readings and baseline's
commit-at-first-move against chain GB, and adds the in-flight overrun:
  overrun_s   play time past the 600 s cap: (sum of step_s) - 600 from result.json, exact; for a game with no
              result.json (a supervisor stop), (last sampler row - the last 0-move row) - 600, a LOWER bound
argv: e4_dir out_dir"""
import contextlib
import json
import os
import subprocess
import sys

E4, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def run(script, *args):
    p = subprocess.run([PY, "-B", os.path.join(HERE, script), *args], capture_output=True, text=True, check=True,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return [ln.split("\t") for ln in p.stdout.splitlines() if ln and not ln.startswith("#")]


est = {r[0]: r for r in run("e4b_estimate.py", E4, "120")[1:]}
base = {r[1]: r for r in run("baseline.py", E4)[1:] if len(r) > 6}
agent = {}
with open(os.path.join(OUT, "agent.tsv"), encoding="utf-8") as fh:
    for ln in fh:
        f = ln.rstrip("\n").split("\t")
        if len(f) == 3 and f[0] == "E4a":
            agent[f[1]] = json.loads(f[2])
rows = []
for d in sorted(os.listdir(os.path.join(E4, "public"))):
    idx, g = d.split("_", 1)
    src = os.path.join(E4, "public", d)
    res = None
    with contextlib.suppress(OSError, ValueError), open(os.path.join(src, f"{g}.result.json"), encoding="utf-8") as fh:
        res = json.load(fh)
    with open(os.path.join(src, f"{g}.commit.tsv"), encoding="utf-8") as fh:
        smp = [(float(f[0]), int(f[2])) for f in (ln.split("\t") for ln in fh if ln.strip())]
    first_end = next((t for t, n in smp if n >= 1), None)
    if res and res.get("error"):
        over, how = None, "ended by error"
    elif res and res.get("step_s") and res.get("play_start_s") is not None:
        over, how = round(sum(res["step_s"]) - 600, 1), "exact (7c77689: cap from play start)"
    elif res and res.get("step_s"):
        # 38b2daa: the cap ran from module start, load included; load end = first move's end - its length
        load = first_end - res["step_s"][0] if first_end is not None else 0.0
        over, how = round(load + sum(res["step_s"]) - 600, 1), "approx +-10 s (38b2daa: cap from module start)"
    else:
        t0 = max((t for t, n in smp if n == 0), default=smp[0][0])
        over, how = round(smp[-1][0] - t0 - 600, 1), "lower bound (supervisor stop)"
    e, b, a = est.get(g, [None] * 7), base.get(g, [None] * 10), agent.get(g, {})
    slice_over = round(float(e[4]) - 120, 1) if e[4] not in (None, "None") else None
    rows.append([idx, g, over, how, slice_over, e[1], e[2], e[3], b[2], b[6], a.get("slot_hit_carried"),
                 a.get("whole_hit_carried"), a.get("slot_from_carry")])
with open(os.path.join(OUT, "extra.tsv"), "w", encoding="utf-8") as fh:
    fh.write("# per E4a game, never pooled: overrun (result.json step_s, or the sampler for a supervisor stop); move "
             "p50/p90/max (e4b_estimate.py); commit at the first move vs chain GB (baseline.py); carried hits "
             "(collect.py agent.tsv)\n")
    fh.write("idx\tgame\tcap_overrun_s\tcap_overrun_how\tslice_overrun_s (replay slice - 120)\tmove_p50_s\t"
             "move_p90_s\tmove_max_s\tchain_gb\tcommit_first_gib\tslot_hit_carried\twhole_hit_carried\t"
             "slot_from_carry\n")
    for r in rows:
        fh.write("\t".join(str(x) for x in r) + "\n")
print("rows", len(rows), "missing est", sum(1 for r in rows if r[5] is None), "missing base",
      sum(1 for r in rows if r[8] is None), "missing agent", sum(1 for r in rows if r[10] is None))
