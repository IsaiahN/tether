"""Read-only (the reviewer r274): su15's cycle-84 derived asks in PLAY15 r3. For the non-echo asks: the slots, their
object ids, and whether each object id is named by any row of cycle 83 (bp35's last cycle) -- carried over by the
tracker -- and by su15's matches/present rows; plus any row at 83/84 carrying a value for a sampled slot."""
import collections
import json
import re
import sys

sys.dont_write_bytecode = True
R = "C:/TETHER_RUNS/S6_2026-10-19/PLAY15/round_03/stream.jsonl"
OBJ = re.compile(r"\bo\d+\b")
asked, rows83, rows84 = [], [], []
for ln in open(R, encoding="utf-8"):
    if '"cycle": 83,' in ln:
        rows83.append(ln)
    elif '"cycle": 84,' in ln:
        rows84.append(ln)
        if '"event": "derived_asked"' in ln:
            asked.append(json.loads(ln))
mint_asks = [r for r in asked if not (r.get("detail") or {}).get("echo")]
print(f"cycle 84 derived_asked {len(asked)}; non-echo (minted) {len(mint_asks)}")
ids83 = collections.Counter(o for ln in rows83 for o in set(OBJ.findall(ln)))
present84 = [json.loads(ln) for ln in rows84 if '"event": "present"' in ln]
print("present rows at 84:", [{k: (v if not isinstance(v, list) else len(v))
                                for k, v in (p.get("detail") or {}).items()
                                if k in ("gone", "came", "was", "now", "blind", "orphaned")} for p in present84][:3])
objs = [OBJ.findall(r["slot"]) for r in mint_asks]
carried = sum(1 for os_ in objs if os_ and all(o in ids83 for o in os_))
print(f"non-echo asks whose object ids ALL appear in cycle-83 rows (bp35's last cycle): {carried} of {len(mint_asks)}")
print(f"distinct objects among them: {len({o for os_ in objs for o in os_})}; of those named at 83: "
      f"{len({o for os_ in objs for o in os_ if o in ids83})}")
print("sample of 10 (slot | object ids | named at 83?):")
for r in mint_asks[:: max(1, len(mint_asks) // 10)][:10]:
    os_ = OBJ.findall(r["slot"])
    vals = []
    for c, rs in (("83", rows83), ("84", rows84)):
        for ln in rs:
            if f'"slot": "{r["slot"]}"' in ln and any(k in ln for k in ('"observed"', '"before"', '"after"',
                                                                         '"value"', '"was"')):
                d = json.loads(ln).get("detail") or {}
                vals.append((c, json.loads(ln)["event"], {k: d[k] for k in ("before", "after", "observed",
                                                                           "value", "was", "now") if k in d}))
                break
    print(f"  {r['slot']} | {os_} | {[o in ids83 for o in os_]} | {vals[:2]}")
