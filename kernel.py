"""THE KERNEL — the loop, and the conformance suite that reads its record.

One file. Two halves, separated by a seam that is load-bearing:

    ABOVE THE SEAM   the frame. Runs the loop. Records what it did.
    BELOW THE SEAM   the linter. Reads rows. Holds no reference to the frame.

Three properties the linter holds, enforced rather than promised, because a checker is
the thing most likely to certify a system that did nothing:

  IT NEVER TOUCHES THE FRAME.  `Linter.run` takes a list of dicts. It cannot reach into
  the object it grades. A reference sharing state with its subject is not a reference.

  EVERY CHECK CARRIES A WITNESS.  A bad input it MUST reject and a control it MUST
  accept. `selftest` runs both on every invocation, and a check that fails either is
  SUPPRESSED — its live verdict is discarded, not trusted. You cannot add a check that
  always passes: it will suppress itself the first time it runs.

  IT REPORTS WHAT IT DID NOT CHECK.  Four states, never two. PASS · FAIL · VACUOUS
  (it examined no rows) · UNRUNNABLE (the record lacks the field) · UNIMPL (named in
  CONFLATIONS.md, not built). A checker with two states resolves every ambiguity toward
  PASS, and a check with nothing to look at is the commonest way to earn one.

The checks and the record are designed together. That is what makes them checks rather
than guesses: a ledger field is a contract the loop honours, and a missing one is
detectable. Static analysis of identifiers is not — rename the variable and it goes
blind, silently.

    python kernel.py              run the loop, then grade the record
    python kernel.py --selftest   witnesses only
    python kernel.py --cites      what each check enforces
"""

from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from math import log2
from typing import Any

sys.dont_write_bytecode = True

# ---------------------------------------------------------------------------------------
# SYMBOLS
# ---------------------------------------------------------------------------------------

Slot = str
Term = str

K = 10          # anchor: the observation alphabet |V|; a correction costs log2(K) bits
PRIMS: dict[str, Callable[[int], int]] = {
    "idn": lambda v: v, "inc": lambda v: v + 1, "dbl": lambda v: v * 2}

GENUINE, CHANNEL_CLOSED, SLICE_TOO_SMALL = "genuine", "channel_closed", "slice_too_small"
CAUSES = (GENUINE, CHANNEL_CLOSED, SLICE_TOO_SMALL)


@dataclass
class Library:
    """Gamma. `closure` is GENERATED, never stored: a stored closure deadlocks, because
    accept() is its only writer and mint() requires membership."""

    primitives: set[Term] = field(default_factory=set)
    derived: set[Term] = field(default_factory=set)
    grammar: dict[Term, list[Term]] = field(default_factory=dict)
    stamps: dict[Term, dict] = field(default_factory=dict)

    def add(self, term: Term, origin: str, cycle: int) -> None:
        self.derived.add(term)
        self.stamps[term] = {"origin": origin, "cycle": cycle}   # where AND when

    def closure(self) -> set[Term]:
        c, changed = set(self.primitives), True
        while changed:
            changed = False
            for rule, subs in self.grammar.items():
                if rule not in c and all(s in c for s in subs):
                    c.add(rule)
                    changed = True
        return c

    def atoms_of(self, term: Term) -> list[str]:
        if term in self.primitives:
            return [term]
        return [a for s in self.grammar.get(term, []) for a in self.atoms_of(s)]

    def apply(self, term: Term, v: int) -> int:
        for a in self.atoms_of(term):
            v = PRIMS[a](v)
        return v % K


@dataclass
class Residual:
    """R, indexed per slot. Never a single global number."""

    mass: dict[Slot, float] = field(default_factory=dict)
    cause: dict[Slot, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------------------
# THE FRAME
# ---------------------------------------------------------------------------------------


class Frame:
    def __init__(self, ground: Callable, actions: tuple[str, ...] = ("a", "b")):
        self.G = Library(primitives=set(PRIMS))
        self.ground = ground                     # injected; the loop cannot modify it
        self.actions = actions
        self.R = Residual()
        self.hist: dict[Slot, list[tuple[int, int]]] = defaultdict(list)
        self.bound: dict[Slot, Term] = {}
        self.owed: set[Slot] = set()
        self.candidates: set[Term] = set()       # accepted, unsettled: held, not citable
        self.ledger: list[dict] = []
        self.cycle = 0
        self._integral = 0.0

    # -- the surprise integral is append-only: += is the only writer -------------------
    @property
    def integral(self) -> float:
        return self._integral

    def _surprise(self, bits: float) -> None:
        self._integral += bits

    def rec(self, step: str, slot: str, event: str, **d: Any) -> None:
        self.ledger.append({"seq": len(self.ledger), "cycle": self.cycle,
                            "step": step, "slot": slot, "event": event,
                            "mode": "specified", "detail": d})

    # -- the code, declared. Both halves of the bargain are lengths under it -----------
    def correction_bits(self, pred: int, actual: int) -> float:
        return 0.0 if pred == actual else log2(K)

    def term_bits(self, term: Term) -> float:
        return (len(self.G.atoms_of(term)) + 1) * log2(len(self.G.primitives) + 1)

    def left(self, term: Term, slot: Slot) -> float:
        """|R|phi| accumulated over the slot's history: the model cost is paid once and
        the savings scale with n, which is what makes the bargain discriminate."""
        return sum(self.correction_bits(self.G.apply(term, b), a) for b, a in self.hist[slot])

    # -- step 1 ------------------------------------------------------------------------
    def perceive(self, action: str, before: dict, after: dict) -> None:
        self.R = Residual()
        for slot, obs in after.items():
            term = self.bound.get(slot, "idn")
            pred = self.G.apply(term, before[slot])
            self.hist[slot].append((before[slot], obs))
            bits = self.correction_bits(pred, obs)
            if bits > 0:
                cause = GENUINE
                self._surprise(bits)
            elif len(self.hist[slot]) <= 2:
                cause = SLICE_TOO_SMALL      # too little evidence to call it explained
            elif slot in self.owed:
                cause = CHANNEL_CLOSED       # owes, yet reads zero: the channel, not the model
            else:
                cause = GENUINE
            self.R.mass[slot] = bits
            self.R.cause[slot] = cause
            self.rec("PERCEIVE", slot, "bet", mass=bits, cause=cause, action=action,
                     predicted=pred, actual=obs, bound=term)
            # STANDING ON A TERM IS CITING IT. The bet at step 1 is derived from the
            # bound term, so binding a candidate and predicting from it is exactly
            # "an unsettled term used as evidence in a later bet". The discipline was
            # attached to `cite`, a verb the loop never called; a prior is exempt
            # because the ground never owed anything for it.
            if term not in self.G.primitives:
                self.rec("PROMOTE", slot, "cite", term=term, allowed=True,
                         via="bound: it drove this step's prediction")

    # -- step 2 ------------------------------------------------------------------------
    def route(self) -> dict[Slot, tuple[str, str]]:
        out = {}
        for slot, mass in self.R.mass.items():
            if mass == 0.0:
                out[slot] = ("TRANSFERRED", "the invariant held; nothing owed")
            else:
                # REBINDING searches the LIBRARY. A term in the closure that is not in
                # the library has not been minted, so refitting to it would be a mint.
                fit = next((t for t in sorted(self.G.derived)
                            if self.left(t, slot) == 0.0 and t != self.bound.get(slot)), None)
                out[slot] = (("BROKEN_REBINDING", "`" + fit + "` in the library explains it")
                             if fit else
                             ("BROKEN_MECHANISM", "no library term explains the history"))
            self.rec("ROUTE", slot, "route", bin=out[slot][0], why_not=out[slot][1])
        return out

    # -- step 3 ------------------------------------------------------------------------
    def mint(self, slot: Slot) -> Term | None:
        base = self.left(self.bound.get(slot, "idn"), slot)
        guards = {"support": base > 0.0, "reachability": False, "novelty": False}
        if not guards["support"]:
            self.rec("MINT", slot, "probe", guards=guards,
                     note="density(R) at zero: perturb, the outcome re-enters as observation")
            self.rec("MINT", slot, "park", guards=guards, base_bits=base,
                     coverage=0.0, units=len(self.G.closure()), depth=2,
                     verdict="no_support")
            return None
        best, seen = None, 0
        for phi in self._compose():
            seen += 1
            guards["reachability"] = True                 # a witness proves reachable
            if phi in self.G.primitives:
                continue
            guards["novelty"] = True
            cost, lo = self.term_bits(phi), self.left(phi, slot)
            if cost + lo < base and (best is None or lo < best[2]):
                best = (phi, cost, lo)
        if best is None:
            self.owed.add(slot)
            self.rec("MINT", slot, "park", guards=guards, base_bits=base,
                     coverage=round(seen / max(seen, 1), 4), units=len(self.G.closure()),
                     depth=2, verdict="depth_exhausted",
                     note="the whole space at this depth was seen; not at this depth, "
                          "NOT unreachable")
            return None
        phi, cost, lo = best
        closes = lo == 0.0
        if not closes:
            self.owed.add(slot)                           # PAYS IS NOT CLOSES
        else:
            self.owed.discard(slot)
        self.rec("MINT", slot, "mint", guards=guards, term=phi, term_bits=cost,
                 left_bits=lo, base_bits=base, closes=closes)
        return phi

    def _compose(self) -> list[Term]:
        """Compose from the closure AND declare the composition, so the generator and the
        reachability check mean the same thing by `composition`."""
        cl = sorted(self.G.closure())
        out = []
        for t1 in cl:
            for t2 in cl:
                if len(self.G.atoms_of(t1)) + len(self.G.atoms_of(t2)) > 3:
                    continue
                name = t1 + " . " + t2
                self.G.grammar.setdefault(name, [t1, t2])
                out.append(name)
        return out

    # -- steps 4 and 5 -------------------------------------------------------------------
    def accept(self, phi: Term, slot: Slot, origin: str) -> None:
        self.G.add(phi, origin, self.cycle)
        self.candidates.add(phi)
        self.bound[slot] = phi
        self.rec("ACCEPT", slot, "accept", term=phi, origin=origin,
                 status="candidate", note="held, and not citable until the ground settles it")

    def settle(self, phi: Term, slot: Slot) -> str:
        held = self.ground(self.G, phi, self.hist[slot], slot)
        if held:
            self.candidates.discard(phi)
        self.rec("SETTLE", slot, "settle" if held else "hold", term=phi,
                 status="accepted" if held else "candidate",
                 verdict=("held on a transition it was not fitted to" if held
                          else "the ground has not paid; it stays a candidate"))
        return "SETTLED" if held else "CANDIDATE"

    def cite(self, phi: Term, slot: Slot) -> bool:
        """An unsettled term used as evidence is how a wrong term compounds."""
        ok = phi not in self.candidates
        self.rec("PROMOTE", slot, "cite", term=phi, allowed=ok)
        return ok

    # -- step 8 ----------------------------------------------------------------------------
    def step(self, before: dict, after: dict) -> None:
        self.cycle += 1
        # THE ACTION. `by` names the site that chose it, so a label can be checked against
        # the mechanism rather than believed. Both branches draw today -- and the check
        # below will say so rather than letting the label stand.
        action, by = self.actions[self.cycle % len(self.actions)], "draw"
        phase = "directed" if any(self.bound.get(s) for s in after) else "probe"
        self.perceive(action, before, after)
        for slot, (b, _why) in self.route().items():
            if b == "BROKEN_MECHANISM":
                phi = self.mint(slot)
                if phi:
                    self.accept(phi, slot, "minted")
                    self.settle(phi, slot)
        self.rec("REPEAT", "@loop", "repeat", phase=phase, by=by, action=action,
                 owed=sorted(self.owed), gamma=len(self.G.derived),
                 integral=round(self.integral, 3))


# =========================================================================================
# THE SEAM. Nothing below holds a reference to anything above.
# =========================================================================================


@dataclass
class Check:
    cid: str
    cite: str
    fn: Callable[[list], list]
    bad: list                      # MUST produce a finding
    ok: list                       # MUST NOT
    reads: tuple[str, ...] = ()    # the events it examines; () means every row

    def scope(self, rows: list) -> int:
        """How many rows this check actually looked at. Zero is not a pass."""
        return len(rows) if not self.reads else sum(
            1 for r in rows if r.get("event") in self.reads)


class Unrunnable(Exception):
    """The record lacks the field this check needs. Emphatically not a pass."""


CHECKS: list[Check] = []


def _check(cid, cite, bad, ok, reads=()):
    def deco(fn):
        CHECKS.append(Check(cid, cite, fn, bad, ok, reads))
        return fn
    return deco


def _rows(rows, event):
    return [r for r in rows if r.get("event") == event]


_M = "MINT"


@_check("A2", "Step 3: 'a bargain, not a threshold: |phi| + |R|phi| < |R|. DECLARE THE CODE'",
        [{"event": "mint", "detail": {"term_bits": 9.0, "left_bits": 9.0, "base_bits": 1.0}}],
        [{"event": "mint",
      "detail": {"term_bits": 6.0, "left_bits": 0.0, "base_bits": 6.6}}], ("mint",))
def _a2(rows):
    out = []
    for r in _rows(rows, "mint"):
        d = r["detail"]
        if not all(k in d for k in ("term_bits", "left_bits", "base_bits")):
            raise Unrunnable("mint rows lack term_bits/left_bits/base_bits")
        if not d["term_bits"] + d["left_bits"] < d["base_bits"]:
            out.append(f"{d.get('term')}: {d['term_bits']}+{d['left_bits']} !< {d['base_bits']}")
    return out


@_check("A3", "Step 3: 'PAYS IS NOT CLOSES ... step 7 fires on failure to CLOSE R'",
        [{"event": "mint", "slot": "s", "detail": {"left_bits": 2.0, "closes": True}}],
        [{"event": "mint", "slot": "s", "detail": {"left_bits": 2.0, "closes": False}}], ("mint",))
def _a3(rows):
    out = []
    for r in _rows(rows, "mint"):
        d = r["detail"]
        if "left_bits" not in d or "closes" not in d:
            raise Unrunnable("mint rows lack left_bits/closes")
        if d["left_bits"] > 0 and d["closes"]:
            out.append(f"{r.get('slot')}: leftover > 0 yet marked closing")
    return out


@_check("A4", "Step 1: 'a low reading has three causes and only two of them are about R "
              "stopping'",
        [{"event": "bet", "slot": "s", "detail": {"mass": 0.0}}],
        [{"event": "bet", "slot": "s", "detail": {"mass": 0.0, "cause": GENUINE}}], ("bet",))
def _a4(rows):
    out = []
    for r in _rows(rows, "bet"):
        d = r["detail"]
        if d.get("mass", 1.0) != 0.0:
            continue
        if d.get("cause") not in CAUSES:
            out.append(f"{r.get('slot')}: zero mass, cause={d.get('cause')!r}")
    return out


@_check("A5", "Step 5: 'until the ground settles it, a term is CANDIDATE: it may be held "
              "and it may not be cited'",
        [{"event": "cite", "detail": {"term": "x", "allowed": True}}],
        [{"event": "settle", "detail": {"term": "x"}},
         {"event": "cite", "detail": {"term": "x", "allowed": True}}], ("cite", "settle"))
def _a5(rows):
    settled, out = set(), []
    for r in rows:
        d = r.get("detail", {})
        if r.get("event") == "settle":
            settled.add(d.get("term"))
        elif r.get("event") == "cite" and d.get("allowed") and d.get("term") not in settled:
            out.append(f"{d.get('term')}: cited before the ground settled it")
    return out


@_check("A6", "Step 2: 'a bin without its discriminator is a label, not a diagnosis'",
        [{"event": "repeat", "detail": {"phase": "probe", "by": "draw"}},
         {"event": "repeat", "detail": {"phase": "directed", "by": "draw"}}],
        [{"event": "repeat", "detail": {"phase": "probe", "by": "draw"}},
         {"event": "repeat", "detail": {"phase": "directed", "by": "term"}}], ("repeat",))
def _a6(rows):
    sites = defaultdict(set)
    for r in _rows(rows, "repeat"):
        d = r["detail"]
        if "phase" not in d:
            continue
        if "by" not in d:
            raise Unrunnable("repeat rows carry no `by` (the site that chose the action)")
        sites[d["phase"]].add(d["by"])
    labels, out = sorted(sites), []
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            if sites[a] == sites[b]:
                out.append(f"{a} and {b} share every producing site {sorted(sites[a])}: "
                           "one of them is decoration")
    return out


@_check("A8", "Step 4: 'stamped with where it came from and when'",
        [{"event": "accept", "detail": {"term": "x"}}],
        [{"event": "accept", "detail": {"term": "x", "origin": "minted"}}], ("accept",))
def _a8(rows):
    return [f"{r['detail'].get('term')}: accept without origin"
            for r in _rows(rows, "accept") if "origin" not in r["detail"]]


@_check("B1", "Step 3: 'REACHABILITY HAS NO NEGATIVE ... an exhausted budget proves "
              "UNREACHED, which is not unreachable'",
        [{"event": "park", "detail": {"verdict": "unreachable"}}],
        [{"event": "park", "detail": {"verdict": "depth_exhausted", "coverage": 1.0,
                                      "units": 3, "depth": 2}}], ("park",))
def _b1(rows):
    out = []
    for r in _rows(rows, "park"):
        d = r["detail"]
        if d.get("verdict") == "unreachable":
            out.append(f"{r.get('slot')}: claims `unreachable`; no frame certifies its own limit")
        elif d.get("verdict") == "depth_exhausted" and not all(
                k in d for k in ("coverage", "units", "depth")):
            out.append(f"{r.get('slot')}: abstains without stating its denominator")
    return out


@_check("B4", "Step 3: 'THE GUARDS -- a product, not a checklist. Any factor at zero "
              "forces inertness'",
        [{"event": "mint", "detail": {"guards": {"support": True, "reachability": False,
                                                 "novelty": True}}}],
        [{"event": "mint", "detail": {"guards": {"support": True, "reachability": True,
                                                 "novelty": True}}}], ("mint",))
def _b4(rows):
    out = []
    for r in _rows(rows, "mint"):
        g = r["detail"].get("guards")
        if g is None:
            raise Unrunnable("mint rows record no guards")
        if not all(g.values()):
            out.append(f"{r.get('slot')}: minted with a guard at zero {g}")
    return out


@_check("B5", "Step 3: 'SUPPORT AT ZERO IS AN INSTRUCTION, NOT A STOP ... perturb'",
        [{"event": "park", "slot": "s", "detail": {"verdict": "no_support"}}],
        [{"event": "probe", "slot": "s", "detail": {}},
         {"event": "park", "slot": "s", "detail": {"verdict": "no_support"}}], ("park", "probe"))
def _b5(rows):
    probed = {r.get("slot") for r in _rows(rows, "probe")}
    return [f"{r.get('slot')}: support at zero and no probe followed"
            for r in _rows(rows, "park")
            if r["detail"].get("verdict") == "no_support" and r.get("slot") not in probed]


@_check("B6", "Notes: 'the time-integral of prediction error is monotone: a drive may "
              "read it and may never reduce it'",
        [{"event": "repeat", "detail": {"integral": 5.0}},
         {"event": "repeat", "detail": {"integral": 2.0}}],
        [{"event": "repeat", "detail": {"integral": 2.0}},
         {"event": "repeat", "detail": {"integral": 5.0}}], ("repeat",))
def _b6(rows):
    out, last = [], 0.0
    for r in _rows(rows, "repeat"):
        v = r["detail"].get("integral")
        if v is None:
            raise Unrunnable("repeat rows carry no integral")
        if v < last:
            out.append(f"integral fell {last} -> {v}: a surprise record was forgotten")
        last = v
    return out


@_check("B15", "DECLARING THE MODE: 'three legitimate modes, and the mode must be stated'",
        [{"event": "bet", "detail": {}}],
        [{"event": "bet", "mode": "specified", "detail": {}}])
def _b15(rows):
    return [f"seq {r.get('seq')}: no mode declared" for r in rows
            if r.get("mode") not in ("general", "specified", "grounded")]


# named in CONFLATIONS.md and deliberately not built. Silence here is how coverage shrinks.
UNIMPL = {
    "A1": "closure generated not stored -- a property of the type, not of the record",
    "A7": "R never aggregated -- needs per-slot provenance on every recorded quantity",
    "A9": "the reference is not the subject -- structural; see THE SEAM above",
    "B2": "the gate is not the ground -- the ground is injected, not recorded",
    "B3": "the bet is on b, not o' -- needs dataflow",
    "B7": "F requires a pose -- step 6 is not built",
    "B8": "shadow then echo -- step 6 is not built",
    "B9": "generators cross, playback never -- step 6 is not built",
    "B10": "import passes through step 7 -- step 7 is not built",
    "B11": "the library is restructured -- no refactor operator exists",
    "B12": "the habitat is enumerated -- no habitat in this frame",
    "B13": "the ground is not a frame -- structural; injected at construction",
    "B14": "a seat is not a person -- not code-checkable",
    "B16": "R is always a slice -- a reading discipline, not a code property",
}


class Linter:
    """Reads rows. Holds no reference to any frame."""

    @staticmethod
    def selftest() -> dict[str, str]:
        out = {}
        for c in CHECKS:
            try:
                bad, ok = c.fn(c.bad), c.fn(c.ok)
            except Exception as e:                              # noqa: BLE001
                out[c.cid] = f"UNWITNESSED ({type(e).__name__}: {e})"
                continue
            if not bad:
                out[c.cid] = "UNWITNESSED (the witness produced no finding)"
            elif ok:
                out[c.cid] = f"UNWITNESSED (the control produced {len(ok)})"
            else:
                out[c.cid] = "ok"
        return out

    @classmethod
    def run(cls, rows: list[dict]) -> dict[str, dict]:
        trusted = {k for k, v in cls.selftest().items() if v == "ok"}
        res: dict[str, dict] = {}
        for c in CHECKS:
            if c.cid not in trusted:
                res[c.cid] = {"status": "SUPPRESSED", "why": ["its witness did not fire"]}
                continue
            try:
                found = c.fn(rows)
            except Unrunnable as e:
                res[c.cid] = {"status": "UNRUNNABLE", "why": [str(e)]}
                continue
            seen = c.scope(rows)
            if found:
                res[c.cid] = {"status": "FAIL", "why": found}
            elif seen == 0:
                # a pass over nothing is a guaranteed number. The discipline may be
                # sound and simply never exercised, which is not the same as upheld.
                res[c.cid] = {"status": "VACUOUS",
                              "why": [f"examined 0 rows of {c.reads or 'any'}"]}
            else:
                res[c.cid] = {"status": "PASS", "why": [f"{seen} rows examined"]}
        for cid, why in UNIMPL.items():
            res[cid] = {"status": "UNIMPL", "why": [why]}
        return res

    @classmethod
    def report(cls, rows: list[dict]) -> int:
        res = cls.run(rows)
        rank = {"FAIL": 0, "SUPPRESSED": 1, "UNRUNNABLE": 2, "VACUOUS": 3,
                "PASS": 4, "UNIMPL": 5}
        for cid in sorted(res, key=lambda c: (rank[res[c]["status"]], c)):
            print(f"  {cid:<5} {res[cid]['status']}")
            for w in res[cid]["why"][:3]:
                print(f"        {w}")
        n = {s: sum(1 for r in res.values() if r["status"] == s) for s in rank}
        print(f"\n  {n['PASS']} pass · {n['FAIL']} fail · {n['UNRUNNABLE']} unrunnable "
              f"· {n['SUPPRESSED']} suppressed · {n['UNIMPL']} unimplemented")
        print(f"  {len(CHECKS)} checks carry a witness; {len(UNIMPL)} are named and not built.")
        return 1 if n["FAIL"] else 0


# ---------------------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------------------

TRUTH = {"s0": lambda v: (2 * v + 1) % K, "s1": lambda v: (v + 2) % K}


def ground(lib: Library, phi: Term, hist, slot: Slot) -> bool:
    """Held-out payment. The slot is passed, never read from mutable outside state: a
    ground that depends on the world around it is not a ground, it is another frame."""
    seen = {b for b, _ in hist}
    out = [(v, TRUTH[slot](v)) for v in range(K) if v not in seen]
    return bool(out) and all(lib.apply(phi, b) == a for b, a in out)


def main(argv: list[str]) -> int:
    if "--cites" in argv:
        for c in CHECKS:
            print(f"{c.cid:<5} {c.cite}")
        return 0
    if "--selftest" in argv:
        for cid, v in sorted(Linter.selftest().items()):
            print(f"  {cid:<5} {v}")
        return 0
    f = Frame(ground)
    state = {"s0": 1, "s1": 3}
    for _ in range(5):
        before = dict(state)
        after = {s: TRUTH[s](before[s]) for s in state}
        f.step(before, after)
        state = after
    print(f"bound    : {f.bound}")
    print(f"library  : {sorted(f.G.derived)}")
    print(f"candidate: {sorted(f.candidates)}")
    print(f"integral : {f.integral:.2f} (monotone)")
    print(f"correct  : {({s: f.G.apply(f.bound.get(s, 'idn'), 4) == TRUTH[s](4) for s in TRUTH})}")
    print(f"\nLINTER over {len(f.ledger)} rows:")
    return Linter.report(f.ledger)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
