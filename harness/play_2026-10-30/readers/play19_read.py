"""Read-only, PLAY19's 1a columns (the reviewer 2026-10-29 r317 4): per finished round's
stream.jsonl -- the divide rows (searching mints; priced, carried, m1 over the mints that priced,
answered, rows evaluated / avoided, credited), space_closed causes by part, memo_sizes' largest
divide_slot / divide_kind, and the parked mints capped by RANK (candidates_tried at the work
budget) against capped otherwise (the yield cap: budget_exhausted with rank below it).
argv: play dir, round numbers."""
import collections
import json
import statistics
import sys

sys.dont_write_bytecode = True
P = sys.argv[1]
WORK_BUDGET = None      # read from the rows (work_budget is on the stream rows); else 15000 default
for n in sys.argv[2:]:
    rd = f"{P}/round_{int(n):02d}"
    dv, causes, memo = [], collections.Counter(), {"divide_slot": 0, "divide_kind": 0}
    rank_cap = yield_cap = parked = 0
    wb = set()
    for ln in open(f"{rd}/stream.jsonl", encoding="utf-8"):
        if '"event": "divide"' in ln:
            dv.append(json.loads(ln)["detail"])
        elif '"event": "space_closed"' in ln:
            for c in json.loads(ln)["detail"]["cause"].split("+"):
                causes[c] += 1
        elif '"event": "memo_sizes"' in ln:
            a = json.loads(ln)["detail"].get("agent") or {}
            for k in memo:
                memo[k] = max(memo[k], a.get(k, 0))
        elif '"event": "stream"' in ln:
            w = json.loads(ln)["detail"].get("work_budget")
            if w:
                wb.add(w)
        elif '"event": "park"' in ln and '"step": "MINT"' in ln:
            d = json.loads(ln)["detail"]
            if d.get("budget_exhausted"):
                parked += 1
                rank_cap += d.get("candidates_tried", 0) >= (max(wb) if wb else 15000)
    yield_cap = parked - rank_cap
    priced = [d for d in dv if d["priced_now"]]
    m1 = [d["m1"] for d in priced]
    s = lambda k: sum(d.get(k) or 0 for d in dv)  # noqa: E731
    print(f"round {n}: searching mints {len(dv)}, priced {len(priced)}, carried>0 "
          f"{sum(1 for d in priced if d['carried'])}; m1 over priced mints median "
          f"{round(statistics.median(m1), 3) if m1 else None} max {max(m1) if m1 else None}; "
          f"carried {s('carried')} / priced_now {s('priced_now')}; answered {s('answered')}; rows "
          f"evaluated {s('rows_evaluated')} / avoided {s('rows_avoided')}; credited {s('credited')}")
    print(f"  closes by part {dict(causes.most_common())} | memo peak divide_slot "
          f"{memo['divide_slot']} divide_kind {memo['divide_kind']} | budget-exhausted parks "
          f"{parked}: rank-capped {rank_cap}, yield-capped {yield_cap} (work_budget "
          f"{sorted(wb) or 'default 15000'})")
