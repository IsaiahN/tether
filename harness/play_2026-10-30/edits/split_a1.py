"""Write tether.py WITHOUT A1 (A2 only) from the full file; each removal asserted to land once."""
import sys

p = sys.argv[1]
t = open(p, "rb").read().decode("utf-8")
NL = "\r\n"


def drop(old, new=""):
    global t
    o = old.replace("\n", NL)
    n = new.replace("\n", NL)
    assert t.count(o) == 1, (t.count(o), old[:70])
    t = t.replace(o, n)


drop("""# A1, THE GOVERNOR AT THE STEP (Isaiah 2026-10-26 11:25; the reviewer 11:33): route asks
# Agent._think_or_act before a slot's library lookup; "urgent" or "probe_first" defers it, OWED
# through C1's queue and asked first next step, recorded as deferred and never as not found. The
# refuted-bin lookup is not gated. ON; conform/arms.py
_STEP_ACT = armflag.arm("TETHER_STEP_ACT", default=True)
""")
drop("""        self._step_act: Counter = Counter()   # A1: this step's lookups run / deferred by why
""")
i = t.index("    def _defer_lookup(self, slot: str) -> str | None:")
j = t.index("    def route(self, res: dict[str, SlotResidual])")
t = t[:i] + t[j:]
drop("""        self._route_cls = {}
        self._step_act = Counter()
""", """        self._route_cls = {}
""")
drop("""                b, fit = MECHANISM, (None if self._defer_lookup(slot)
                                     else self._fit_tier0(slot, self.bound.get(slot)) if _FIT_TIER0
                                     else self._library_fit(slot, self.bound.get(slot)))
""", """                b, fit = MECHANISM, (self._fit_tier0(slot, self.bound.get(slot)) if _FIT_TIER0
                                     else self._library_fit(slot, self.bound.get(slot)))
""")
drop("""                fit = (None if self._defer_lookup(slot)
                       else self._library_fit(slot, self.bound.get(slot)))
""", """                fit = self._library_fit(slot, self.bound.get(slot))
""")
i = t.index("        if _STEP_ACT and self._step_act:")
j = t.index("        if _STEP_RANK:\r\n            out.sort(key=lambda t: pos[t[0]])")
t = t[:i] + t[j:]
assert "_STEP_ACT" not in t and "_defer_lookup" not in t and "_step_act" not in t
open(p, "wb").write(t.encode("utf-8"))
print("A2 only")
