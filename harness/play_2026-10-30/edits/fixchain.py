import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
reps = [
 ('sum((sr, k, r) in oldC == ((sr, k, r) in newC) for k, r in keys)', 'sum(((sr, k, r) in oldC) == ((sr, k, r) in newC) for k, r in keys)'),
 ('sum(("x" + sr, k, r) in oldC == (("x" + sr, k, r) in newC) for k, r in keys)', 'sum((("x" + sr, k, r) in oldC) == (("x" + sr, k, r) in newC) for k, r in keys)'),
 ('sum(k in oldC == (k in newC) for k in (kx, kd))', 'sum((k in oldC) == (k in newC) for k in (kx, kd))'),
]
for a, b in reps:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s); print('fixed', len(reps))
