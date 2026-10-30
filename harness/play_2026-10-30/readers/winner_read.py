import json, sys
rows = [json.loads(x) for x in open(sys.argv[1], encoding="utf-8") if x.strip()]
print("stream_share rows with a winner (cycle, slot, winner, winner_rank, walked_total, work_budget):")
for r in rows:
    d = r["detail"]
    if r["event"] == "stream" and d.get("site") == "stream_share" and (d.get("stop") or {}).get("found"):
        print(f"  c{r['cycle']} {r['slot']}: winner {str(d.get('winner'))[:50]} rank {d.get('winner_rank')} walked {d.get('walked_total')} of {d.get('work_budget')}")
print("other keys on a stream_share row:", sorted(next(r for r in rows if r['event'] == 'stream' and r['detail'].get('site') == 'stream_share')['detail'].keys()))
acc = [r for r in rows if r["step"] == "ACCEPT"]
print("ACCEPT rows:", [(r["cycle"], r["slot"], r["event"], str(r["detail"].get("term") or r["detail"].get("status"))[:40]) for r in acc][:40])
