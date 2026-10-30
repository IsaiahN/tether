import sys
sys.dont_write_bytecode = True
R = "c:/Users/Admin/Documents/GitHub/tether/"
edits = {
 "tether.py": [('            self.led.record(self.cycle, "PLAN", slot, "split_refused", survivors=len(sv),\n',
                '            self.led.record(self.cycle, "PLAN", slot, "ask_unsplit", survivors=len(sv),\n')],
 "conform/arms.py": [('"change is a stop_rule row. SPLIT REFUSED -- 1b abstained -- writes "\n                         "split_refused and adds',
                      '"change is a stop_rule row. SPLIT REFUSED -- 1b abstained -- writes "\n                         "ask_unsplit (never the goal split\'s split_refused) and adds')],
}
for f, pairs in edits.items():
    p = R + f
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (f, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)
p = R + "tests/test_stop_rules.py"
s = open(p, encoding="utf-8", newline="").read()
n = s.count('"split_refused"')
s = s.replace('"split_refused"', '"ask_unsplit"').replace("split_refused, the gap in the", "ask_unsplit, the gap in the").replace("split_refused, aims", "ask_unsplit, aims")
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok", n)
