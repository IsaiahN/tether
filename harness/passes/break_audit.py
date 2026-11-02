"""THE BREAK AUDIT (the reviewer 2026-10-23 13:04 item 2, 13:12 item 2): B's frame breaks against the TRUE game
switches, AFTER a run. HARNESS SIDE ONLY: it reads switch.tsv, which is the harness's knowledge of the order and
is never shown to the agent, so this output never goes back into the agent, its lineage, or any arms row the
agent reads. Read-only.

The true switch-landing step of game i > 0 is the cycle at its switch.tsv cycle_start (e4_stream.py:166-176 and
:126-129: that step plans on the old board, its action is consumed, its outcome is the new board, and B reads a
break on that outcome). A frame_break row there is a HIT; a switch with none is a MISS; a frame_break at any
other cycle is a FALSE ALARM (named with its game and cycle). Also counted from the matches rows' "calls": the
tested calls, the tested calls with exactly one claim (n = 1, the reviewer 13:12 item 4), and the breaks among
those. Per run, per game; never pooled. argv: run dirs"""
import json
import os
import sys

for run in sys.argv[1:]:
    sw = [ln.rstrip("\n").split("\t") for ln in open(os.path.join(run, "switch.tsv"), encoding="utf-8")
          if ln[:1].isdigit()]
    starts = [(f[1], int(f[3])) for f in sw]
    landing = {c: g for g, c in starts[1:]}
    game_at = []
    for i, (g, c) in enumerate(starts):
        end = starts[i + 1][1] if i + 1 < len(starts) else 10 ** 9
        game_at.append((c, end, g))

    def game_of(cyc):
        return next((g for c, e, g in game_at if c <= cyc < e), "?")
    breaks, tested, n1, n1_broke = [], 0, 0, 0
    with open(os.path.join(run, "stream.jsonl"), encoding="utf-8") as fh:
        for ln in fh:
            if '"frame_break"' in ln or '"event": "matches"' in ln:
                r = json.loads(ln)
                if r["event"] == "frame_break":
                    breaks.append((r["cycle"], r["detail"]))
                elif r["event"] == "matches":
                    for c in r["detail"].get("calls", ()):
                        if c.get("tested"):
                            tested += 1
                            if c.get("claimed") == 1:
                                n1 += 1
                                n1_broke += bool(c.get("broke"))
    bc = {c for c, _d in breaks}
    hits = sorted(c for c in landing if c in bc)
    misses = sorted(c for c in landing if c not in bc)
    false = sorted(c for c in bc if c not in landing)
    print(f"== {run}")
    print(f"   switches {len(landing)}  hits {len(hits)}  misses {len(misses)}  false alarms {len(false)}")
    for c in misses:
        print(f"   MISS  cycle {c} (switch to {landing[c]})")
    for c in false:
        d = next(d for cc, d in breaks if cc == c)
        print(f"   FALSE ALARM  cycle {c} in {game_of(c)}: claimed {d.get('claimed')} median {d.get('median')} "
              f"colour {d.get('colour_share')}")
    print(f"   tested calls {tested}; with n = 1 claim {n1}, of which broke {n1_broke}")
