import sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import gamma, gridworld, world
env = world.bind(gridworld.family("default", 0))
g = gamma.Gamma(env.atoms(), game="g")
at = list(g.atoms)
pairs = [(a.name, b.name) for a in at for b in at if a.out_type == b.in_type]
print("atoms", [(a.name, a.in_type, a.out_type) for a in at][:13])
print("chainable pairs", pairs[:5])
