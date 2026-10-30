import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
reps = [
('    python bp35_move.py TREE LINEAGE OUT [MAX_STEPS]"""', '    python bp35_move.py TREE LINEAGE OUT [MAX_STEPS] [GAME]   (GAME defaults to bp35; the counters of\n    arc_world.REL_SLOTS_N, if the tree has them, are printed at the end)"""'),
('MAX_STEPS = int(sys.argv[4]) if len(sys.argv) > 4 else 3\n', 'MAX_STEPS = int(sys.argv[4]) if len(sys.argv) > 4 else 3\nGAME = sys.argv[5] if len(sys.argv) > 5 else "bp35"\n'),
('w = Counted(arc.make("bp35"))', 'w = Counted(arc.make(GAME))'),
('print(f"bp35_move: load {load_s:.1f} s; steps {i + 1}; acts {w.acts}; memory.db unchanged")',
 'import arc_world  # noqa: E402\nprint(f"bp35_move ({GAME}): load {load_s:.1f} s; steps {i + 1}; acts {w.acts}; memory.db unchanged; "\n      f"REL_SLOTS_N {getattr(arc_world, \'REL_SLOTS_N\', None)}")'),
]
for a, b in reps:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s); print('ok')
