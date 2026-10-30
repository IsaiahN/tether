import json, sys
want = set(sys.argv[2].split(','))
seen = {}
for ln in open(sys.argv[1], encoding='utf-8'):
    try: r = json.loads(ln)
    except ValueError: continue
    k = f"{r.get('step')}/{r.get('event')}"
    if k in want and seen.get(k, 0) < 2:
        seen[k] = seen.get(k, 0) + 1
        print(k, json.dumps(r)[:700]); print()
