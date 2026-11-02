"""E4b's reader (dry runs and the run), read only: every field the run writes, named.
  LOAD     load_report.json: the head the load read, library_n (B2: head 01e8a078795df27f, library_n 141 on the run)
  LAUNCH   launcher.txt: max_s, margin, deadline_at, its distance from the launch
  SLICES   switch.tsv: every row, each column named (the 13 old + acts, first_act_s, extended, unreached, overrun_s);
           the "unreached at this budget" lines
  RESULT   stream.result.json: every key; sup/sup.json: rc, ending, wall, peak commit
  FAULTS   stream.jsonl: agent_fault / fault_recovered / KeyError-bearing rows; @cap rows by event; traceback file
argv: out_dir"""
import collections
import json
import os
import sys

sys.dont_write_bytecode = True
OUT = sys.argv[1]
COLS = ["idx", "game", "wall_start_s", "cycle_start", "wall_s", "steps", "levels_in_slice", "ending", "endings",
        "commit_mb_end", "seq0", "seqP", "seq1", "acts", "first_act_s", "extended", "unreached", "overrun_s"]


def load(p):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as x:  # noqa: BLE001 -- a missing or partial file is the reading
        return {"__unreadable__": repr(x)}


print("LOAD", json.dumps(load(os.path.join(OUT, "load_report.json")), default=str)[:600])
try:
    with open(os.path.join(OUT, "launcher.txt"), encoding="utf-8") as fh:
        lt = fh.read()
    head = json.loads(lt[:lt.rindex("}") + 1])
    print("LAUNCH", {k: head[k] for k in ("max_s", "margin_s", "deadline_at", "deadline_after_launch_s")},
          "|", lt[lt.rindex("}") + 1:].strip())
except Exception as x:  # noqa: BLE001
    print("LAUNCH unreadable", repr(x))
sw = os.path.join(OUT, "switch.tsv")
if os.path.exists(sw):
    with open(sw, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\n")
            if ln.startswith("# idx"):
                continue
            if ln.startswith("#"):
                print("SLICES", ln[:400])
                continue
            f = ln.split("\t")
            print("SLICE", {c: (f[i] if i < len(f) else "<MISSING>") for i, c in enumerate(COLS)},
                  "" if len(f) == len(COLS) else f"<{len(f)} fields, want {len(COLS)}>")
else:
    print("SLICES no switch.tsv")
res = load(os.path.join(OUT, "stream.result.json"))
print("RESULT", json.dumps(res, default=str)[:900])
sup = load(os.path.join(OUT, "sup", "sup.json"))
print("SUP", {k: sup.get(k) for k in ("rc", "ending", "wall_s", "peak_process_commit_gib", "peak_job_commit_gib",
                                      "ceiling_gib", "memcap_pids")})
led = os.path.join(OUT, "stream.jsonl")
ev, faults, cap = collections.Counter(), [], collections.Counter()
if os.path.exists(led):
    with open(led, encoding="utf-8") as fh:
        for ln in fh:
            r = json.loads(ln)
            ev[r["event"]] += 1
            if r["event"] in ("agent_fault", "fault_recovered", "carry_refused") or "KeyError" in ln:
                faults.append((r.get("cycle"), r["event"], json.dumps(r.get("detail"), default=str)[:200]))
            if r.get("slot") == "@cap":
                cap[r["event"]] += 1
print("FAULTS", len(faults), faults[:10])
print("CAP rows", dict(cap), "| ledger rows", sum(ev.values()))
for n in ("stream.traceback.txt",):
    print("TRACEBACK", n, os.path.exists(os.path.join(OUT, n)))
