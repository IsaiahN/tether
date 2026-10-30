import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
reps = [
("    def step(self, act, data=None):\n        self.acts += 1\n",
 "    def step(self, act, data=None):\n        self.acts += 1\n        self.log.append([str(act), None if data is None else str(data)])\n"),
("        self.w, self.acts = w, 0\n", "        self.w, self.acts, self.log = w, 0, []\n"),
('        fh.write(json.dumps({"step": i, "wall_s": round(time.perf_counter() - t, 2), "acts": w.acts - a0}) + "\n")',
 '        fh.write(json.dumps({"step": i, "wall_s": round(time.perf_counter() - t, 2), "acts": w.acts - a0,\n                             "actions": w.log[a0:]}) + "\n")'),
("f\"HYP_SLOTSET_N {getattr(sys.modules.get('tether'), 'HYP_SLOTSET_N', None)}\")",
 "f\"HYP_SLOTSET_N {getattr(sys.modules.get('tether'), 'HYP_SLOTSET_N', None)}; \"\n      f\"KIND_FALLBACK_N {dict(getattr(sys.modules.get('interface'), 'KIND_FALLBACK_N', {}))}\")"),
]
for a, b in reps:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s); print('ok')
