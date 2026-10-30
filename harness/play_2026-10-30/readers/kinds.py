import json, sys, collections
c = collections.Counter(); keys = {}
for ln in open(sys.argv[1], encoding='utf-8'):
    try: r = json.loads(ln)
    except ValueError: continue
    k = (r.get('step') or r.get('kind'), r.get('what') or r.get('event') or r.get('name'))
    c[k] += 1; keys.setdefault(k, sorted(r)[:14])
for k, n in c.most_common(60): print(n, k, keys[k])
