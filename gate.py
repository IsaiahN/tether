"""The checker.

IMPORTS NOTHING FROM THIS BUILD. It reads rows of plain data and knows nothing about the
domain, the loop, or the library. That non-access is what makes it sound: a verifier that
can reconstruct the claim cannot verify it.

It checks FORM. A pass means the derivation is well-formed. It never means the answer is
right -- the ground does that, and a gate is not the ground.

Every refusal names the failing check and a fixed token, never prose.
"""

from __future__ import annotations

import json
import sys

sys.dont_write_bytecode = True

PASS, REFUSE = "pass", "refuse"

NO_STEP = "no-step"
STEP_ORDER = "step-order"
MISSING_INPUT = "missing-input"
UNROUTED = "unrouted"
DOUBLE_ROUTED = "double-routed"
NO_DISCRIMINATOR = "no-discriminator"
GUARD_UNRECORDED = "guard-unrecorded"
UNSETTLED_ACCEPT = "unsettled-accept"
NO_MODE = "no-mode"
FILTER_VERDICT = "filter-verdict"
IRREVERSIBLE_CUT = "irreversible-cut"

STEPS = ("PERCEIVE", "ROUTE", "MINT", "ACCEPT", "SETTLE", "PROMOTE", "IMPORT", "REPEAT")
MODES = ("general", "specified", "grounded")
GUARDS = ("support", "reachability", "novelty")

# A budget-limited search may report only that it did not find. These words claim more.
ABSOLUTE = ("unreachable", "absent", "impossible", "none-exists", "proved-absent")


def _v(check: str, token: str, seq: int | None = None, note: str = "") -> dict:
    return {"verdict": REFUSE, "check": check, "token": token, "seq": seq, "note": note}


def check(rows: list[dict]) -> dict:
    """Returns {"verdict": pass|refuse, ...}. The FIRST refusal is the named one."""
    for fn in (_mode, _steps, _inputs, _routing, _guards, _settlement, _filters, _cuts):
        out = fn(rows)
        if out is not None:
            return out
    return {"verdict": PASS, "check": None, "token": None, "rows": len(rows)}


def _mode(rows: list[dict]) -> dict | None:
    """6. A mode is declared, on every row."""
    for r in rows:
        if r.get("mode") not in MODES:
            return _v("mode", NO_MODE, r.get("seq"))
    return None


def _steps(rows: list[dict]) -> dict | None:
    """1. Every entry names a loop step, and a slot's own chain does not run backwards.

    The order is per (cycle, slot): the loop runs one chain per slot and the chains are
    independent within a cycle, so slot A minting does not constrain slot B's routing.
    """
    last: dict[tuple[int, str], int] = {}
    for r in rows:
        step = r.get("step")
        if step not in STEPS:
            return _v("steps", NO_STEP, r.get("seq"), str(step))
        k, i = (r.get("cycle", 0), r.get("slot")), STEPS.index(step)
        if k in last and i < last[k]:
            return _v("steps", STEP_ORDER, r.get("seq"),
                      f"{k[1]}: {step} after {STEPS[last[k]]}")
        last[k] = i
    return None


def _inputs(rows: list[dict]) -> dict | None:
    """2. No step consumed an input that never arrived."""
    bets: set[tuple[int, str]] = set()
    minted: set[tuple[int, str]] = set()
    accepted: set[str] = set()
    for r in rows:
        c, slot, ev = r.get("cycle", 0), r.get("slot"), r.get("event")
        if ev == "bet":
            bets.add((c, slot))
        elif ev == "route" and (c, slot) not in bets:
            return _v("inputs", MISSING_INPUT, r.get("seq"), f"route without bet: {slot}")
        elif ev in ("mint", "park", "accept") and (c, slot) not in bets:
            return _v("inputs", MISSING_INPUT, r.get("seq"), f"{ev} without bet: {slot}")
        elif ev in ("mint", "park", "accept"):
            minted.add((c, slot))
            if ev == "accept":
                accepted.add(str(r.get("detail", {}).get("term")))
        elif ev == "settle" and str(r.get("detail", {}).get("term")) not in accepted:
            return _v("inputs", MISSING_INPUT, r.get("seq"), "settle without accept")
    return None


def _routing(rows: list[dict]) -> dict | None:
    """3. Every slot with live mass routed into exactly one bin, with its discriminator."""
    live: set[tuple[int, str]] = set()
    routed: dict[tuple[int, str], int] = {}
    for r in rows:
        c, slot, d = r.get("cycle", 0), r.get("slot"), r.get("detail", {})
        if r.get("event") == "bet" and float(d.get("mass", 0)) > 0:
            live.add((c, slot))
        if r.get("event") == "route":
            k = (c, slot)
            routed[k] = routed.get(k, 0) + 1
            if routed[k] > 1:
                return _v("routing", DOUBLE_ROUTED, r.get("seq"), slot)
            if not d.get("why_not"):
                return _v("routing", NO_DISCRIMINATOR, r.get("seq"), slot)
    for k in live:
        if k not in routed:
            return _v("routing", UNROUTED, None, f"cycle {k[0]} slot {k[1]}")
    return None


def _guards(rows: list[dict]) -> dict | None:
    """4. All three guards evaluated and recorded -- including the ones that passed."""
    for r in rows:
        if r.get("event") in ("mint", "park"):
            g = r.get("detail", {}).get("guards") or {}
            for name in GUARDS:
                if name not in g:
                    return _v("guards", GUARD_UNRECORDED, r.get("seq"), name)
    return None


def _settlement(rows: list[dict]) -> dict | None:
    """5. Nothing is labelled ACCEPTED without a settle event. A gate is not the ground."""
    settled = {str(r.get("detail", {}).get("term")) for r in rows if r.get("event") == "settle"}
    for r in rows:
        d = r.get("detail", {})
        if (str(d.get("status", "")).lower() == "accepted"
                and str(d.get("term")) not in settled):
            return _v("settlement", UNSETTLED_ACCEPT, r.get("seq"), str(d.get("term")))
    return None


def _filters(rows: list[dict]) -> dict | None:
    """7. No filter has issued a verdict. A budget that ran out did not prove absence."""
    for r in rows:
        d = r.get("detail", {})
        if d.get("budget_exhausted"):
            v = str(d.get("verdict", "")).lower()
            if v in ABSOLUTE or v == "":
                return _v("filters", FILTER_VERDICT, r.get("seq"), v or "(none)")
    return None


def _cuts(rows: list[dict]) -> dict | None:
    """8. Every cut is ranked and reversible. A wrong cut removes the answer and speeds up."""
    for r in rows:
        for cut in r.get("detail", {}).get("cuts") or []:
            if "rank" not in cut or not cut.get("reversible", False):
                return _v("cuts", IRREVERSIBLE_CUT, r.get("seq"), str(cut.get("name")))
    return None


def check_file(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        rows = [json.loads(ln) for ln in fh if ln.strip()]
    return check(rows)


if __name__ == "__main__":
    print(json.dumps(check_file(sys.argv[1]), indent=2))
