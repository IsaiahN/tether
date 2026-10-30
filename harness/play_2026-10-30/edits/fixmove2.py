import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
reps = [
('    python bp35_move.py TREE LINEAGE OUT [MAX_STEPS] [GAME]   (GAME defaults to bp35; the counters of\n    arc_world.REL_SLOTS_N, if the tree has them, are printed at the end)"""',
 '    python bp35_move.py TREE LINEAGE OUT [MAX_STEPS] [GAME] [ACTS]   (GAME defaults to bp35; it stops once ACTS actions\n    (default 1) have reached the game; the counters of arc_world.REL_SLOTS_N, if the tree has them, are printed at the end).\n    CORRECTED 2026-10-25 07:35: round 1\'s slow bp35 step was its SECOND (first_act_s 25.7, slice 6,262 s, 2 steps), so the\n    bp35 record runs with ACTS 2."""'),
('GAME = sys.argv[5] if len(sys.argv) > 5 else "bp35"\n', 'GAME = sys.argv[5] if len(sys.argv) > 5 else "bp35"\nACTS = int(sys.argv[6]) if len(sys.argv) > 6 else 1\n'),
('    if w.acts > 0:\n        break', '    if w.acts >= ACTS:\n        break'),
]
for a, b in reps:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s); print('ok')
