"""THE KERNEL — the loop, and the conformance suite that reads its record.

One file. Two halves, separated by a seam that is load-bearing:

    ABOVE THE SEAM   the frame. Runs the loop. Records what it did.
    BELOW THE SEAM   the linter. Reads rows. Holds no reference to the frame.

Three properties the linter holds, enforced rather than promised, because a checker is
the thing most likely to certify a system that did nothing:

  IT NEVER TOUCHES THE FRAME.  `Linter.run` takes a list of dicts. It cannot reach into
  the object it grades. A reference sharing state with its subject is not a reference.

  EVERY CHECK CARRIES A WITNESS, AND SO DOES ITS DENOMINATOR.  A bad input it MUST
  reject, a control it MUST accept, and a row count on each that the FIXTURE states.
  `selftest` runs all three on every invocation, and a check failing any is SUPPRESSED —
  its live verdict discarded, not trusted. You cannot add a check that always passes: it
  suppresses itself the first time it runs. Nor one that fabricates how much it looked
  at, which would put a real-looking denominator under an empty subject.

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
ACTIONS = ("a", "b")
DELTA = {"a": 1, "b": 3}        # anchor: two actions that must be distinguishable, and
#                                 a spread wide enough that one does not alias the other

# An atom may read the action. Without one, no term can express an action-dependent
# transition, no action can be chosen for a reason, and `directed` is a label with no
# mechanism behind it -- which is what A6 was reporting.
# every atom takes (value, action) whether it reads the action or not: one uniform
# signature, no branching on whether an atom is action-dependent. ARG005 is the
# discipline, not a defect -- an atom that took a different shape could not compose.
PRIMS: dict[str, Callable[[int, str], int]] = {   # noqa: ARG005
    "idn": lambda v, a: v,        # noqa: ARG005
    "inc": lambda v, a: v + 1,    # noqa: ARG005
    "dbl": lambda v, a: v * 2,    # noqa: ARG005
    "act": lambda v, a: v + DELTA[a]}

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

    def apply(self, term: Term, v: int, action: str) -> int:
        for at in self.atoms_of(term):
            v = PRIMS[at](v, action)
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
    def __init__(self, ground: Callable, actions: tuple[str, ...] = ACTIONS):
        self.G = Library(primitives=set(PRIMS))
        self.ground = ground                     # injected; the loop cannot modify it
        self.actions = actions
        self.R = Residual()
        # (before, action, after): the action is part of the evidence, because a term
        # that reads it cannot be scored against a history that dropped it
        self.hist: dict[Slot, list[tuple[int, str, int]]] = defaultdict(list)
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

    def rec(self, step: str, slot: str, event: str, of: tuple = (), **d: Any) -> None:
        """`of` names the slots a recorded quantity was derived from. A magnitude drawn
        from more than one slot is an aggregation, and this is what makes that visible
        in the record rather than only in the source."""
        self.ledger.append({"seq": len(self.ledger), "cycle": self.cycle,
                            "step": step, "slot": slot, "event": event,
                            "of": list(of) if of else ([slot] if not slot.startswith("@")
                                                       else []),
                            "mode": "specified", "detail": d})

    # -- the code, declared. Both halves of the bargain are lengths under it -----------
    def correction_bits(self, pred: int, actual: int) -> float:
        return 0.0 if pred == actual else log2(K)

    def term_bits(self, term: Term) -> float:
        return (len(self.G.atoms_of(term)) + 1) * log2(len(self.G.primitives) + 1)

    def left(self, term: Term, slot: Slot) -> float:
        """|R|phi| accumulated over the slot's history: the model cost is paid once and
        the savings scale with n, which is what makes the bargain discriminate."""
        return sum(self.correction_bits(self.G.apply(term, b, act), aft)
                   for b, act, aft in self.hist[slot])

    # -- step 1 ------------------------------------------------------------------------
    def perceive(self, action: str, before: dict, after: dict) -> None:
        self.R = Residual()
        for slot, obs in after.items():
            term = self.bound.get(slot, "idn")
            pred = self.G.apply(term, before[slot], action)
            self.hist[slot].append((before[slot], action, obs))
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
            # `from_value` is the input the prediction was computed from. Without it
            # the record cannot distinguish a bet placed on the belief from one placed
            # on the observation, and the second has no model that could be wrong.
            self.rec("PERCEIVE", slot, "bet", mass=bits, cause=cause, action=action,
                     from_value=before[slot], predicted=pred, actual=obs, bound=term)
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
            if mass == 0.0 and slot not in self.owed:
                out[slot] = ("TRANSFERRED", "the invariant held; nothing owed")
            elif mass == 0.0:
                # a slice reading zero while the accumulated residual is live. Routing
                # this as TRANSFERRED would retire a debt on the strength of one step.
                out[slot] = ("BROKEN_MECHANISM",
                             "this step read zero and the slot still owes")
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
        # support is checked at step level, where the whole residual is visible; by the
        # time route() has sent a slot here, this slot's base is necessarily > 0
        guards = {"support": True, "reachability": False, "novelty": False}
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
        # what the ground was ASKED and what it ANSWERED, both recorded. Without the
        # answer on the row, a frame reporting `accepted` cannot be distinguished from
        # one that never asked -- and a gate passing is not the ground.
        held = self.ground(self.G, phi, self.hist[slot], slot)
        if held:
            self.candidates.discard(phi)
        else:
            # YOU CAN PROPOSE ON A CANDIDATE; YOU CANNOT STAND ON ONE. Accepting keeps
            # it in the library -- held, defeasibly -- but the ground refused it HERE,
            # so it stops driving this slot's prediction. Leaving it bound is the only
            # place the citation discipline can actually be broken.
            self.bound.pop(slot, None)
            self.owed.add(slot)
        self.rec("SETTLE", slot, "settle" if held else "hold", term=phi,
                 asked=(phi, slot), ground_said=held,
                 status="accepted" if held else "candidate",
                 verdict=("held on a transition it was not fitted to" if held
                          else "the ground has not paid; it stays a candidate"))
        return "SETTLED" if held else "CANDIDATE"

    def cite(self, phi: Term, slot: Slot) -> bool:
        """An unsettled term used as evidence is how a wrong term compounds."""
        ok = phi not in self.candidates
        self.rec("PROMOTE", slot, "cite", term=phi, allowed=ok)
        return ok

    # -- choosing the action ------------------------------------------------------------
    def choose(self, before: dict) -> tuple[str, str]:
        """(action, by). `by` names the site that chose it, so the label can be checked
        against the mechanism instead of believed.

        DISCRIMINATE: some slot owes, and the candidates disagree about what an action
        will produce there. An outcome every candidate predicts alike teaches nothing,
        so the action worth taking is the one that separates them most -- which is the
        difference between a probe and an experiment, and it is derived from Gamma
        rather than from any knowledge of the answer.

        DRAW: nothing owes, or no action separates anything. Then the draw is
        uninformed BY CONSTRUCTION, which is the safety property: a probe chosen by the
        current model can only confirm the current model.
        """
        owed = sorted(self.owed & set(before))
        if owed:
            cands = self._compose()
            spread = {act: sum(len({self.G.apply(phi, before[slot], act) for phi in cands})
                               for slot in owed)
                      for act in self.actions}
            # an action discriminates when it separates the candidates MORE THAN ANOTHER
            # ACTION DOES. Comparing the best against the spread at actions[0] instead
            # makes actions[0] unchoosable -- best > best is false -- so the verdict
            # would turn on which key happens to sort first rather than on the world.
            if max(spread.values()) > min(spread.values()):
                return max(self.actions, key=lambda a: spread[a]), "discriminate"
        return self.actions[self.cycle % len(self.actions)], "draw"

    # -- step 8 ----------------------------------------------------------------------------
    def step(self, before: dict, world: Callable[[dict, str], dict]) -> dict:
        """The world responds to the action, so the action is chosen before the outcome
        exists. Bet, act, observe -- in that order, which is what step 1 says."""
        self.cycle += 1
        action, by = self.choose(before)
        # the phase is READ OFF the site that chose, never asserted alongside it
        phase = "directed" if by == "discriminate" else "probe"
        after = world(before, action)
        self.perceive(action, before, after)
        if not any(m > 0.0 for m in self.R.mass.values()):
            # SUPPORT AT ZERO IS AN INSTRUCTION, NOT A STOP. You cannot compress what
            # you never observed, so perturb; the outcome re-enters as an observation.
            g = {"support": False, "reachability": False, "novelty": False}
            # carries no magnitude: SUPPORT is a predicate over slots ("|R+_s| > 0 for
            # SOME slot s"), not a quantity averaged across them
            self.rec("MINT", "@loop", "park", of=tuple(sorted(self.R.mass)),
                     guards=g, verdict="no_support")
            self.rec("MINT", "@loop", "probe", guards=g,
                     note="density(R) at zero on every slot; perturbing")
        for slot, (b, _why) in self.route().items():
            if b == "BROKEN_MECHANISM":
                phi = self.mint(slot)
                if phi:
                    self.accept(phi, slot, "minted")
                    self.settle(phi, slot)
        self.rec("REPEAT", "@loop", "repeat", phase=phase, by=by, action=action,
                 owed=sorted(self.owed), gamma=len(self.G.derived),
                 integral=round(self.integral, 3))
        return after


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
    reads: tuple[str, ...] = ()    # documentation only; the count comes from the check
    n_bad: int = 0                 # rows the fixtures say it should have examined --
    n_ok: int = 0                  # stated by the fixture author, never by the check

    # A check returns (findings, examined). `examined` is what it actually predicated
    # on, never the count of a declared event type: a check over two mint rows neither
    # of which could have triggered it has examined nothing, and "2 rows examined" would
    # put a real denominator under an empty subject. The scope predicate must BE the
    # check predicate.


MAGNITUDES = ("mass", "base_bits", "term_bits", "left_bits")


class Unrunnable(Exception):
    """The record lacks the field this check needs. Emphatically not a pass."""


CHECKS: list[Check] = []


def _check(cid, cite, bad, ok, reads=(), *, n_bad: int, n_ok: int):
    """n_bad/n_ok are required: a check added without stating what its fixtures hold
    would report an unwitnessed denominator, which is the hole this closes."""
    def deco(fn):
        CHECKS.append(Check(cid, cite, fn, bad, ok, reads, n_bad, n_ok))
        return fn
    return deco


def _rows(rows, event):
    return [r for r in rows if r.get("event") == event]


_M = "MINT"


@_check("A2", "Step 3: 'a bargain, not a threshold: |phi| + |R|phi| < |R|. DECLARE THE CODE'",
        [{"event": "mint", "detail": {"term_bits": 9.0, "left_bits": 9.0, "base_bits": 1.0}}],
        [{"event": "mint",
      "detail": {"term_bits": 6.0, "left_bits": 0.0, "base_bits": 6.6}}], ("mint",),
              n_bad=1, n_ok=1)
def _a2(rows):
    out, seen = [], 0
    for r in _rows(rows, "mint"):
        d = r["detail"]
        if not all(k in d for k in ("term_bits", "left_bits", "base_bits")):
            raise Unrunnable("mint rows lack term_bits/left_bits/base_bits")
        seen += 1
        if not d["term_bits"] + d["left_bits"] < d["base_bits"]:
            out.append(f"{d.get('term')}: {d['term_bits']}+{d['left_bits']} !< {d['base_bits']}")
    return out, seen


@_check("A3", "Step 3: 'PAYS IS NOT CLOSES ... step 7 fires on failure to CLOSE R'",
        [{"event": "mint", "slot": "s", "detail": {"left_bits": 2.0, "closes": True}}],
        [{"event": "mint", "slot": "s", "detail": {"left_bits": 2.0, "closes": False}}], ("mint",),
                n_bad=1, n_ok=1)
def _a3(rows):
    out, seen = [], 0
    for r in _rows(rows, "mint"):
        d = r["detail"]
        if "left_bits" not in d or "closes" not in d:
            raise Unrunnable("mint rows lack left_bits/closes")
        if d["left_bits"] <= 0:
            continue                     # not the subject: this mint closed R
        seen += 1
        if d["closes"]:
            out.append(f"{r.get('slot')}: leftover > 0 yet marked closing")
    return out, seen


@_check("A4", "Step 1: 'a low reading has three causes and only two of them are about R "
              "stopping'",
        [{"event": "bet", "slot": "s", "detail": {"mass": 0.0}}],
        [{"event": "bet", "slot": "s", "detail": {"mass": 0.0, "cause": GENUINE}}], ("bet",),
                n_bad=1, n_ok=1)
def _a4(rows):
    out, seen = [], 0
    for r in _rows(rows, "bet"):
        d = r["detail"]
        if d.get("mass", 1.0) != 0.0:
            continue                     # not the subject: only a LOW reading has causes
        seen += 1
        if d.get("cause") not in CAUSES:
            out.append(f"{r.get('slot')}: zero mass, cause={d.get('cause')!r}")
    return out, seen


@_check("A5", "Step 5: 'until the ground settles it, a term is CANDIDATE: it may be held "
              "and it may not be cited'",
        [{"event": "settle", "slot": "s1", "detail": {"term": "x"}},
         {"event": "cite", "slot": "s2", "detail": {"term": "x", "allowed": True}}],
        [{"event": "settle", "slot": "s1", "detail": {"term": "x"}},
         {"event": "cite", "slot": "s1", "detail": {"term": "x", "allowed": True}},
         {"event": "cite", "slot": "s1", "detail": {"term": "x", "allowed": True}}],
        ("cite", "settle"), n_bad=1, n_ok=2)
def _a5(rows):
    # keyed on (slot, term): the ground settles a term FOR A SLOT -- `ground()` takes
    # the slot -- so a settlement on one slot licenses nothing on another. Keying on the
    # term alone lets one settlement anywhere license citation everywhere, which is how
    # a term the ground REFUSED goes on predicting.
    settled, out, seen = set(), [], 0
    for r in rows:
        d = r.get("detail", {})
        key = (r.get("slot"), d.get("term"))
        if r.get("event") == "settle":
            settled.add(key)
        elif r.get("event") == "cite" and d.get("allowed"):
            seen += 1
            if key not in settled:
                out.append(f"{d.get('term')} on {r.get('slot')}: cited where the ground "
                           "has not settled it")
    return out, seen


@_check("A6", "Step 2: 'a bin without its discriminator is a label, not a diagnosis'",
        [{"event": "repeat", "detail": {"phase": "probe", "by": "draw"}},
         {"event": "repeat", "detail": {"phase": "directed", "by": "draw"}}],
        [{"event": "repeat", "detail": {"phase": "probe", "by": "draw"}},
         {"event": "repeat", "detail": {"phase": "directed", "by": "term"}}], ("repeat",),
                 n_bad=1, n_ok=1)
def _a6(rows):
    sites = defaultdict(set)
    for r in _rows(rows, "repeat"):
        d = r["detail"]
        if "phase" not in d:
            continue
        if "by" not in d:
            raise Unrunnable("repeat rows carry no `by` (the site that chose the action)")
        sites[d["phase"]].add(d["by"])
    labels, out, seen = sorted(sites), [], 0
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            seen += 1            # a PAIR of labels is the subject; one label alone is not
            if sites[a] == sites[b]:
                out.append(f"{a} and {b} share every producing site {sorted(sites[a])}: "
                           "one of them is decoration")
    return out, seen


@_check("A8", "Step 4: 'stamped with where it came from and when'",
        [{"event": "accept", "detail": {"term": "x"}}],
        [{"event": "accept", "detail": {"term": "x", "origin": "minted"}}], ("accept",),
                n_bad=1, n_ok=1)
def _a8(rows):
    acc = _rows(rows, "accept")
    return ([f"{r['detail'].get('term')}: accept without origin"
             for r in acc if "origin" not in r["detail"]], len(acc))


@_check("B1", "Step 3: 'REACHABILITY HAS NO NEGATIVE ... an exhausted budget proves "
              "UNREACHED, which is not unreachable'",
        [{"event": "park", "detail": {"verdict": "unreachable"}}],
        [{"event": "park", "detail": {"verdict": "depth_exhausted", "coverage": 1.0,
                                      "units": 3, "depth": 2}}], ("park",), n_bad=1, n_ok=1)
def _b1(rows):
    out, seen = [], 0
    for r in _rows(rows, "park"):
        d = r["detail"]
        if d.get("verdict") not in ("unreachable", "depth_exhausted"):
            continue                     # not the subject: only a reach claim is graded
        seen += 1
        if d["verdict"] == "unreachable":
            out.append(f"{r.get('slot')}: claims unreachable; no frame certifies its own limit")
        elif not all(k in d for k in ("coverage", "units", "depth")):
            out.append(f"{r.get('slot')}: abstains without stating its denominator")
    return out, seen


@_check("B4", "Step 3: 'THE GUARDS -- a product, not a checklist. Any factor at zero "
              "forces inertness'",
        [{"event": "mint", "detail": {"guards": {"support": True, "reachability": False,
                                                 "novelty": True}}}],
        [{"event": "mint", "detail": {"guards": {"support": True, "reachability": True,
                                                 "novelty": True}}}], ("mint",), n_bad=1, n_ok=1)
def _b4(rows):
    out, seen = [], 0
    for r in _rows(rows, "mint"):
        g = r["detail"].get("guards")
        if g is None:
            raise Unrunnable("mint rows record no guards")
        seen += 1
        if not all(g.values()):
            out.append(f"{r.get('slot')}: minted with a guard at zero {g}")
    return out, seen


@_check("B5", "Step 3: 'SUPPORT AT ZERO IS AN INSTRUCTION, NOT A STOP ... perturb'",
        [{"event": "park", "slot": "s", "detail": {"verdict": "no_support"}}],
        [{"event": "probe", "slot": "s", "detail": {}},
         {"event": "park", "slot": "s", "detail": {"verdict": "no_support"}}], ("park", "probe"),
                 n_bad=1, n_ok=1)
def _b5(rows):
    probed = {r.get("slot") for r in _rows(rows, "probe")}
    subject = [r for r in _rows(rows, "park")
               if r["detail"].get("verdict") == "no_support"]
    return ([f"{r.get('slot')}: support at zero and no probe followed"
             for r in subject if r.get("slot") not in probed], len(subject))


@_check("B6", "Notes: 'the time-integral of prediction error is monotone: a drive may "
              "read it and may never reduce it'",
        [{"event": "repeat", "detail": {"integral": 5.0}},
         {"event": "repeat", "detail": {"integral": 2.0}}],
        [{"event": "repeat", "detail": {"integral": 2.0}},
         {"event": "repeat", "detail": {"integral": 5.0}},
         {"event": "repeat", "detail": {"integral": 9.0}}], ("repeat",),
        n_bad=2, n_ok=3)
def _b6(rows):
    out, last, seen = [], 0.0, 0
    for r in _rows(rows, "repeat"):
        v = r["detail"].get("integral")
        if v is None:
            raise Unrunnable("repeat rows carry no integral")
        seen += 1
        if v < last:
            out.append(f"integral fell {last} -> {v}: a surprise record was forgotten")
        last = v
    return out, seen


@_check("B15", "DECLARING THE MODE: 'three legitimate modes, and the mode must be stated'",
        [{"event": "bet", "detail": {}}],
        [{"event": "bet", "mode": "specified", "detail": {}}], n_bad=1, n_ok=1)
def _b15(rows):
    return ([f"seq {r.get('seq')}: no mode declared" for r in rows
             if r.get("mode") not in ("general", "specified", "grounded")], len(rows))


@_check("A7", "SYMBOLS + Step 1: 'R is measured per slot, never as a single global "
              "number' / 'averaging across slots is how a live signal disappears'",
        [{"event": "bet", "slot": "s0", "of": ["s0", "s1"], "detail": {"mass": 3.3}}],
        [{"event": "bet", "slot": "s0", "of": ["s0"], "detail": {"mass": 3.3}}],
        (), n_bad=1, n_ok=1)
def _a7(rows):
    """A magnitude is per slot. A predicate over slots is not a magnitude -- SUPPORT is
    'for SOME slot s' -- so only rows carrying a residual quantity are the subject."""
    out, seen = [], 0
    for r in rows:
        d = r.get("detail", {})
        mags = [k for k in MAGNITUDES if k in d]
        if not mags:
            continue
        seen += 1
        if "of" not in r:
            raise Unrunnable("rows carrying a magnitude do not record `of`")
        if len(r["of"]) != 1:
            out.append(f"seq {r.get('seq')}: {mags} derived from {r['of']}")
    return out, seen


@_check("B2", "Step 5: 'the ground settles it' · 'a gate passing is not the ground'",
        [{"event": "settle", "detail": {"term": "x", "status": "accepted"}}],
        [{"event": "settle", "detail": {"term": "x", "status": "accepted",
                                        "asked": ["x", "s0"], "ground_said": True}},
         {"event": "hold", "detail": {"term": "y", "status": "candidate",
                                      "asked": ["y", "s0"], "ground_said": False}}],
        ("settle", "hold"), n_bad=1, n_ok=2)
def _b2(rows):
    """A settlement must carry what the ground was asked and what it answered, and the
    status must match the answer. Otherwise a frame that never asked, or one that
    overrode the reply, is indistinguishable from one the ground paid."""
    out, seen = [], 0
    for r in rows:
        if r.get("event") not in ("settle", "hold"):
            continue
        d, seen = r["detail"], seen + 1
        if "ground_said" not in d or "asked" not in d:
            out.append(f"{d.get('term')}: status {d.get('status')!r} with no answer "
                       "from the ground on the row")
        elif d["ground_said"] != (d.get("status") == "accepted"):
            out.append(f"{d.get('term')}: ground said {d['ground_said']}, "
                       f"status {d.get('status')!r}")
    return out, seen


@_check("B3", "Step 1: 'the bet is placed on b, the belief -- not on the observation. A "
              "system that predicts from what it just saw has no model to be wrong'",
        [{"event": "bet", "slot": "s0", "detail": {"from_value": 1, "actual": 4}},
         {"event": "bet", "slot": "s0", "detail": {"from_value": 9, "actual": 9}}],
        [{"event": "bet", "slot": "s0", "detail": {"from_value": 1, "actual": 4}},
         {"event": "bet", "slot": "s0", "detail": {"from_value": 4, "actual": 6}}],
        ("bet",), n_bad=1, n_ok=1)
def _b3(rows):
    """The before-state of step n is the after-state of step n-1. A bet whose input is
    not the previous outcome was computed from something else -- and the only other
    thing available is this step's observation. The first bet on a slot has no
    predecessor and is not the subject."""
    prev, out, seen = {}, [], 0
    for r in rows:
        if r.get("event") != "bet":
            continue
        d, slot = r["detail"], r.get("slot")
        if "from_value" not in d:
            raise Unrunnable("bet rows do not record `from_value`")
        if slot in prev:
            seen += 1
            if d["from_value"] != prev[slot]:
                out.append(f"{slot}: predicted from {d['from_value']}, but the previous "
                           f"outcome was {prev[slot]}")
        prev[slot] = d.get("actual")
    return out, seen


# Named in CONFLATIONS.md and not built. Three different facts were wearing one label,
# and only the middle pile is actionable -- separating them is what makes the report say
# something. Silence here is how coverage shrinks.

NO_BEHAVIOUR = {           # the frame does not do this yet; nothing to check
    "B7": "F requires a pose -- step 6 is not built",
    "B8": "shadow then echo -- step 6 is not built",
    "B9": "generators cross, playback never -- step 6 is not built",
    "B10": "import passes through step 7 -- step 7 is not built",
    "B11": "the library is restructured -- no refactor operator exists",
    "B12": "the habitat is enumerated -- no habitat in this frame",
}
NO_EVIDENCE: dict[str, str] = {}   # emptied: A7, B2 and B3 are built, each on one
#                                    field added to a row the frame already wrote
STRUCTURAL = {             # a property of the code or the type, invisible to any record
    "A1": "closure generated not stored -- a property of the type",
    "A9": "the reference is not the subject -- the seam; a record cannot prove it",
    "B13": "the ground is not a frame -- the record sees its answers, never its nature",
}
NOT_CHECKABLE = {          # a reading discipline. Pretending otherwise is the decoration
    "B14": "a seat is not a person",
    "B16": "R is always a slice",
}
UNIMPL_KIND = {**{k: ("NO-BEHAVIOUR", v) for k, v in NO_BEHAVIOUR.items()},
               **{k: ("NO-EVIDENCE", v) for k, v in NO_EVIDENCE.items()},
               **{k: ("STRUCTURAL", v) for k, v in STRUCTURAL.items()},
               **{k: ("NOT-CHECKABLE", v) for k, v in NOT_CHECKABLE.items()}}
UNIMPL = {k: v for k, (_kind, v) in UNIMPL_KIND.items()}


class Linter:
    """Reads rows. Holds no reference to any frame."""

    @staticmethod
    def selftest() -> dict[str, str]:
        out = {}
        for c in CHECKS:
            try:
                bad, nb = c.fn(c.bad)
                ok, no = c.fn(c.ok)
            except Exception as e:                              # noqa: BLE001
                out[c.cid] = f"UNWITNESSED ({type(e).__name__}: {e})"
                continue
            if not bad:
                out[c.cid] = "UNWITNESSED (the witness produced no finding)"
            elif ok:
                out[c.cid] = f"UNWITNESSED (the control produced {len(ok)})"
            elif (nb, no) != (c.n_bad, c.n_ok):
                # the count is self-reported, so it needs a witness of its own: without
                # this a check can fabricate a denominator and pass both fixtures, and
                # a real-looking number under an empty subject is exactly what VACUOUS
                # was added to prevent.
                out[c.cid] = (f"UNWITNESSED (counted {nb}/{no}, "
                              f"the fixtures hold {c.n_bad}/{c.n_ok})")
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
                found, seen = c.fn(rows)
            except Unrunnable as e:
                res[c.cid] = {"status": "UNRUNNABLE", "why": [str(e)]}
                continue
            if found:
                res[c.cid] = {"status": "FAIL", "why": found}
            elif seen == 0:
                # a pass over nothing is a guaranteed number. The discipline may be
                # sound and simply never exercised, which is not the same as upheld.
                res[c.cid] = {"status": "VACUOUS",
                              "why": ["examined 0 rows -- the discipline may be sound "
                                      "and simply never exercised, which is not upheld"]}
            else:
                res[c.cid] = {"status": "PASS", "why": [f"{seen} rows examined"]}
        for cid, (kind, why) in UNIMPL_KIND.items():
            res[cid] = {"status": "UNIMPL", "kind": kind, "why": [why]}
        return res

    @classmethod
    def report(cls, rows: list[dict]) -> int:
        res = cls.run(rows)
        rank = {"FAIL": 0, "SUPPRESSED": 1, "UNRUNNABLE": 2, "VACUOUS": 3,
                "PASS": 4, "UNIMPL": 5}
        for cid in sorted(res, key=lambda c: (rank[res[c]["status"]], c)):
            k = res[cid].get("kind")
            print(f"  {cid:<5} {res[cid]['status']}{' · ' + k if k else ''}")
            for w in res[cid]["why"][:3]:
                print(f"        {w}")
        n = {s: sum(1 for r in res.values() if r["status"] == s) for s in rank}
        print(f"\n  {n['PASS']} pass · {n['FAIL']} fail · {n['VACUOUS']} vacuous "
              f"· {n['UNRUNNABLE']} unrunnable · {n['SUPPRESSED']} suppressed "
              f"· {n['UNIMPL']} unimplemented")
        print(f"  {len(CHECKS)} checks carry a witness; {len(UNIMPL)} named and not built:")
        print(f"    {len(NO_EVIDENCE)} NO-EVIDENCE  the property is real, the record "
              "lacks the field -- actionable now")
        print(f"    {len(NO_BEHAVIOUR)} NO-BEHAVIOUR the frame does not do this yet "
              "-- a build, not a fix")
        print(f"    {len(STRUCTURAL)} STRUCTURAL   invisible to any record")
        print(f"    {len(NOT_CHECKABLE)} NOT-CHECKABLE a reading discipline")
        return 1 if n["FAIL"] else 0


# ---------------------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------------------

# same uniform signature on the ground's side, for the same reason
TRUTH = {"s0": lambda v, a: (2 * v + 1) % K,       # noqa: ARG005
         "s1": lambda v, a: (v + 2) % K,           # noqa: ARG005
         # reads the action. Expressible only through `act`, and the only slot for which
         # one action is more informative than another -- so it is what makes a directed
         # step possible at all.
         "s3": lambda v, a: (v + DELTA[a]) % K,
         # increment with one exception. Every atom here is affine, so no composition
         # covers the exception: the best available term pays on the bulk and leaves the
         # exception as residue. That is PAYS IS NOT CLOSES arising on the merits rather
         # than from a history too short to falsify a wrong term.
         "s2": lambda v, a: 0 if v == 5 else (v + 1) % K}   # noqa: ARG005


def ground(lib: Library, phi: Term, hist, slot: Slot) -> bool:
    """Held-out payment over (value, action) pairs the term was never fitted to. The
    slot is passed, never read from mutable outside state: a ground that depends on the
    world around it is not a ground, it is another frame."""
    seen = {(b, act) for b, act, _ in hist}
    out = [(v, act, TRUTH[slot](v, act)) for v in range(K) for act in ACTIONS
           if (v, act) not in seen]
    return bool(out) and all(lib.apply(phi, v, act) == want for v, act, want in out)


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
    state = {"s0": 1, "s1": 3, "s2": 2, "s3": 0}

    def world(bef, act):
        return {s: TRUTH[s](bef[s], act) for s in bef}

    for _ in range(12):
        # the outcome comes back from step, so the state is advanced from one place and
        # the caller does not have to read the action back out of the record
        state = f.step(state, world)
    print(f"bound    : {f.bound}")
    print(f"library  : {sorted(f.G.derived)}")
    print(f"candidate: {sorted(f.candidates)}")
    print(f"integral : {f.integral:.2f} (monotone)")
    # extensional equality over the WHOLE domain, not one sampled point. A term fitted
    # to a short history can agree at a single value and be wrong everywhere else, and a
    # one-point oracle reports that as correct -- which is the false mint, undetected by
    # the thing put there to detect it.
    correct = {s: all(f.G.apply(f.bound.get(s, "idn"), v, act) == TRUTH[s](v, act)
                      for v in range(K) for act in ACTIONS)
               for s in TRUTH}
    print(f"correct  : {correct}   (over all {K} values, not a sample)")
    print(f"\nLINTER over {len(f.ledger)} rows:")
    return Linter.report(f.ledger)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
