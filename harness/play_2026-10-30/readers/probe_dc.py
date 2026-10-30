import copy, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1]); sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import arc_holdout
from test_entry import FakeWrapper
g = arc_holdout.ResetGuard(FakeWrapper(script={}))
try:
    copy.deepcopy(g)
    print("deepcopy ok")
except RecursionError:
    print("deepcopy of ResetGuard: RecursionError")
w2 = arc_holdout.ResetGuard(copy.deepcopy(g.w))
print("inner copy ok", w2.w.calls)
