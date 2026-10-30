"""PREPARED, NOT INSTALLED (the reviewer r344 3): the box variant that pins TETHER_DIVIDE_CREDIT=0 as it pins the seed.
argv: the copy to edit in place."""
import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
a = ('os.environ["TETHER_AGENT_SEED"] = "0"\n'
     'assert os.environ.get("PYTHONHASHSEED") == "0", "the hash seed must be pinned by the launcher"\n'
     'assert not any(k.startswith("TETHER_") and k != "TETHER_AGENT_SEED" for k in os.environ), '
     '"a TETHER_ arm is set"\n')
b = ('assert not any(k.startswith("TETHER_") for k in os.environ), "a TETHER_ arm reached the box"\n'
     'os.environ["TETHER_AGENT_SEED"] = "0"\n'
     "# CREDIT OFF from PLAY19 round 3 (the early cut, Isaiah; the reviewer r344): pinned here as the seed is,\n"
     "# so the round's own arms row records it; every other arm stays at the tree's default\n"
     'os.environ["TETHER_DIVIDE_CREDIT"] = "0"\n'
     'assert os.environ.get("PYTHONHASHSEED") == "0", "the hash seed must be pinned by the launcher"\n')
a, b = a.replace("\n", nl), b.replace("\n", nl)
assert s.count(a) == 1, "the box's seed lines are not as read"
open(p, "w", encoding="utf-8", newline="").write(s.replace(a, b))
print("ok")
