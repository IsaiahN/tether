import json
import sys

sys.dont_write_bytecode = True
path = sys.argv[1]
WANT_ON = ["ARRIVAL_GAP", "INSTANCE_RETIRE", "KIND_SAVE", "SETTLE_PRED", "DIVIDE", "ASK", "OWED_REJUDGE",
           "S1_REPRICE", "STOP_RULES", "NAMED_REMAINDER", "PLAN_NARROW"]
WANT_OFF = ["DIVIDE_CREDIT"]
with open(path, encoding="utf-8") as fh:
    for line in fh:
        r = json.loads(line)
        if r.get("event") == "arms":
            break
    else:
        sys.exit("no arms row")
d = r["detail"]
on, off = set(d["on"]), set(d["off"])
print("row cycle", r.get("cycle"), "head", d.get("head"), "dirty", d.get("dirty"), "on", len(on), "off", len(off))
bad = 0
for name in WANT_ON + WANT_OFF:
    hits_on = sorted(a for a in on if a.split(".", 1)[1] == "_" + name)
    hits_off = sorted(a for a in off if a.split(".", 1)[1] == "_" + name)
    want = "ON" if name in WANT_ON else "OFF"
    got = "ON" if hits_on and not hits_off else "OFF" if hits_off and not hits_on else "MIXED/ABSENT"
    bad += got != want
    print(f"  {name:16} want {want:3} got {got:3}  on={hits_on} off={hits_off}")
print("TETHER_ env keys in row:", sorted(k for k in d if k.startswith("TETHER_")) or "none")
print("MISMATCHES", bad)
