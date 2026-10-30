import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
a = ("                extra = {\"cause\": cause, \"owes\": cause == \"bound\",\n"
 "                         \"bound_before\": {n: round(b, 4) for n, b in sorted(prev[0].items())},\n"
 "                         \"bound_after\": {n: None if low.get(n) is None else round(low[n], 4)\n"
 "                                         for n in sorted(prev[0])},\n"
 "                         \"bar_before\": round(prev[1], 4), \"bar_after\": round(bar, 4)}\n")
b = ("                rose = {n: [round(v, 4), round(low[n], 4)] for n, v in sorted(prev[0].items())\n"
 "                        if low.get(n) is not None and low[n] > v}\n"
 "                after = [low[n] for n in prev[0] if low.get(n) is not None]\n"
 "                # the last survivors can number thousands: their count, the lowest bound before\n"
 "                # and after, the bar before and after, and in full the ones whose bound rose\n"
 "                extra = {\"cause\": cause, \"owes\": cause == \"bound\", \"last_survivors\": len(prev[0]),\n"
 "                         \"bound_rose\": rose, \"low_before\": round(min(prev[0].values()), 4),\n"
 "                         \"low_after\": round(min(after), 4) if after else None,\n"
 "                         \"bar_before\": round(prev[1], 4), \"bar_after\": round(bar, 4)}\n")
a, b = a.replace("\n", nl), b.replace("\n", nl)
assert s.count(a) == 1
s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
