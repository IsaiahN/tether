"""Exercise census_heap.point on a small stand-in agent (no tether module loaded): the code paths run, rows appear."""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import census_heap as ch  # noqa: E402


class L:
    def __init__(self):
        self._entries = [{"detail": {"i": i, "s": "x" * (i % 50)}} for i in range(3000)]


class G:
    def __init__(self):
        self.library = {f"t{i}": [i, str(i)] for i in range(5000)}
        self.invented = {}
        self.evidence = [[i] for i in range(10)]


class A:
    def __init__(self):
        self.led, self.gamma = L(), G()
        self._ak_kept = {(i, "k") for i in range(2500)}
        self._kind_landed = set(range(100))
        self.other = {i: {"deep": list(range(20))} for i in range(1500)}


ag = A()
for lab in ("after_load", "after_step1"):
    ch.point(lab, ag, sys.argv[2])
print(open(sys.argv[2] + "/census.tsv", encoding="utf-8").read())
