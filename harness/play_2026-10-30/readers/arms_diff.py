import json
import sys

sys.dont_write_bytecode = True


def first_arms(path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r.get("event") == "arms":
                return r["detail"]
    sys.exit(f"no arms row in {path}")


a, b = first_arms(sys.argv[1]), first_arms(sys.argv[2])
print("A", sys.argv[1], "head", a.get("head"), "on", len(a["on"]), "off", len(a["off"]))
print("B", sys.argv[2], "head", b.get("head"), "on", len(b["on"]), "off", len(b["off"]))
print("OFF equal verbatim (as lists):", a["off"] == b["off"])
print("OFF only in A:", sorted(set(a["off"]) - set(b["off"])))
print("OFF only in B:", sorted(set(b["off"]) - set(a["off"])))
print("ON only in A:", sorted(set(a["on"]) - set(b["on"])))
print("ON only in B:", sorted(set(b["on"]) - set(a["on"])))
new = (set(sys.argv[3].split(",")) if len(sys.argv) > 3 else
       {"tether._" + n for n in ("ASK", "OWED_REJUDGE", "S1_REPRICE", "STOP_RULES",
                                 "NAMED_REMAINDER", "PLAN_NARROW")})
print("ON(B) == ON(A) + the six:", set(b["on"]) == set(a["on"]) | new and not (set(a["on"]) & new))
