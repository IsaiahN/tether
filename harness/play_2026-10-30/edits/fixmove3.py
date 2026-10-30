import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
a = 'f"REL_SLOTS_N {getattr(arc_world, \'REL_SLOTS_N\', None)}")'
b = 'f"REL_SLOTS_N {getattr(arc_world, \'REL_SLOTS_N\', None)}; "\n      f"HYP_SLOTSET_N {getattr(sys.modules.get(\'tether\'), \'HYP_SLOTSET_N\', None)}")'
assert s.count(a) == 1
s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s); print('ok')
