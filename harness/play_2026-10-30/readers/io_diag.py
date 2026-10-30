import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "C:/Users/Admin/Documents/GitHub/tether/tests")
sys.path.insert(0, "C:/Users/Admin/Documents/GitHub/tether")
from test_contact_first import _child, _norm
root = "C:/Users/Admin/Documents/GitHub/tether"
on = [r for r in _norm(_child(root)) if r[3] != "indistinct"]
off = [r for r in _norm(_child(root, {"TETHER_INDIST_ON_CHANGE": "0"})) if r[3] != "indistinct"]
d = [i for i, (x, y) in enumerate(zip(on, off)) if x != y]
print("differing", len(d), "first", d[:10])
for i in d[:3]:
    print("ON ", on[i][:4], on[i][4][:700])
    print("OFF", off[i][:4], off[i][4][:700])
import json, collections
keys = collections.Counter()
events = collections.Counter()
for i in d:
    a, b = json.loads(on[i][4]), json.loads(off[i][4])
    events[on[i][3]] += 1
    for k in set(a) | set(b):
        if a.get(k) != b.get(k):
            keys[k] += 1
print("events", dict(events))
print("keys", dict(keys))
for i in d:
    if on[i][3] in ("promote", "accept"):
        a, b = json.loads(on[i][4]), json.loads(off[i][4])
        print(on[i][3], {k: (a.get(k), b.get(k)) for k in set(a) | set(b) if a.get(k) != b.get(k)})
