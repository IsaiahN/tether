"""The end-of-run summary. **A READER over the ledger and Γ, never a producer.**

Same shape as `behaviour.py`: nothing here accumulates, and every number is a query over rows
that already exist. **A second producer of a fact the ledger holds is A1's defect at the level
of a record**, and it would look like a feature.

**IT INHERITS §14.7 RATHER THAN WRITING A FIFTH SET OF NUMBERS.** Three of the four sections
map exactly, population-to-statistic — the sections are the items and §14.7's numbers are
computed over them:

    CHAINS + reuse column   ->  chunk reuse count      *how often a settled term appears
                                                        inside a later mint. **Zero is the
                                                        failure signature**, and it is the one
                                                        that would otherwise look like progress*
    REUSED with pull counts ->  bench pulls            *which imports the agent actually needed.
                                                        A never-pulled bench item was a guess*
    REACHED-AND-FAILED      ->  unreached rate         *should fall as chunks accumulate*

**MINTED IS THE FOURTH AND §14.7 HAS NO COUNTERPART FOR IT** -- it is the proof rather than a
rate: *terms that did not exist, unnamed at mint time, against a residual that was recorded
first.*

**AND §14.7's `effective atom depth` IS NOT DERIVABLE HERE.** It is `Σ chunk lengths at search
depth 3`, computed over the CLOSURE rather than over what was minted -- **so it needs the
search, and this file does not have one.** Stated so the inheritance is not read as complete.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

# Composition is sequential-only today, so every joint carries the same operator. The column
# is here because the multi-operator space is a recorded gap rather than an oversight, and a
# summary that omitted the joint would make a one-operator space look like the only one.
JOINT = "."


def _chain(term) -> str:
    return f" {JOINT} ".join(a.name for a in term.atoms)


def minted(rows: list[dict], gamma) -> list[dict]:
    """**Terms that did not exist in the library.** The proof section.

    Each carries its handle, its constituent atoms, the residual it was minted AGAINST, and
    the cost/left pair -- **`left_bits` is the delta between what the term predicted and what
    the ground did**, which is already on the mint row and needed no new field.
    """
    # `record(cycle, STEP, slot, EVENT, ...)` -- `MINT` is the STEP and `mint` is the EVENT.
    # Filtering on `event == "MINT"` matched nothing and every column read `None`, which looks
    # exactly like a mint that carried no cost rather than like a lookup that found nothing.
    bits = {r["detail"]["term"]: r["detail"] for r in rows
            if r.get("event") == "mint" and (r.get("detail") or {}).get("term")}
    out = []
    for name, t in gamma.library.items():
        if t.origin == "prior":
            continue
        st = gamma.stamps.get(name) or {}
        d = bits.get(name, {})
        out.append({"handle": gamma.handles.get(name), "term": name,
                    "atoms": [a.name for a in t.atoms], "joints": [JOINT] * (len(t.atoms) - 1),
                    "origin": t.origin, "admitted": st.get("admitted"),
                    "against_residual": st.get("residual"),
                    "cost_bits": d.get("term_bits"), "left_bits": d.get("left_bits"),
                    "closed_it": d.get("closes")})
    return out


def chains(gamma) -> list[dict]:
    """**`atom . atom . atom`, and whether it appeared inside a LATER mint.**

    That last column is §14.7's chunk reuse, and *zero is the failure signature*. A chain
    counts as reused when its atom sequence is contained in a longer term's -- **the chunk IS
    the atom sequence**, which is `units()`'s own rule and the reason the operand is not in it.
    """
    terms = [(n, t) for n, t in gamma.library.items() if t.origin != "prior"]
    out = []
    for name, t in terms:
        seq = tuple(a.name for a in t.atoms)
        inside = [n2 for n2, t2 in terms if n2 != name and len(t2.atoms) > len(seq)
                  and any(tuple(a.name for a in t2.atoms)[i:i + len(seq)] == seq
                          for i in range(len(t2.atoms) - len(seq) + 1))]
        out.append({"handle": gamma.handles.get(name), "chain": _chain(t),
                    "depth": len(t.atoms), "inside_later_mints": inside})
    return out


def reused(rows: list[dict]) -> dict:
    """**Library entries reached for, with pull counts.** §14.7's bench pulls.

    *A never-pulled bench item was a guess* -- so a term absent from this dict is a reading
    about whoever put it there, not only about the run.
    """
    pulls: dict[str, dict] = {}
    for r in rows:
        if r.get("event") == "pull":
            d = r.get("detail") or {}
            n = d.get("term")
            if n:
                e = pulls.setdefault(n, {"pulls": 0, "origin": d.get("origin")})
                e["pulls"] += 1
    return pulls


def transfer(rows: list[dict], gamma) -> dict:
    """**THE IMPORT's EVIDENCE COLUMN.** An imported term that gets pulled on a NEW game is
    transfer; one that never gets pulled **was a guess, by §14.7's own words.**

    **This is why `IMPORTED` had to be a third bucket.** It wipes like `promoted`, so the
    ablation is unaffected -- *the distinction it buys is countability, not survival* -- and
    countability is exactly what makes this number exist. A term entering as `promoted` would
    be indistinguishable from one minted here, and the transfer claim would have no subject.

    **A COUNT CAN BE GOT MANY WAYS; THIS CANNOT.** *This many were minted elsewhere* is
    ambiguous. **A composition that names its parts, carries the game it was born in, and was
    pulled against a residual in a different one** is transfer with a handle on it.
    """
    held = {n: t for n, t in gamma.library.items() if t.origin == "imported"}
    p = reused(rows)
    pulled = {n: p[n]["pulls"] for n in held if n in p}
    return {"imported_held": len(held),
            "imported_pulled": len(pulled), "pulls": pulled,
            "never_pulled": sorted(set(held) - set(pulled)),
            "handles": {n: gamma.handles.get(n) for n in held},
            "reads": ("an imported term pulled here is TRANSFER; one never pulled was a "
                      "guess. The handle's prefix is the game it was born in, so a pull row "
                      "and a handle together say composed there, used here")}


def reached_and_failed(rows: list[dict]) -> dict:
    """**Descriptions that retrieved nothing.** *I looked for something with this shape and
    found nothing* is an `UNREACHED` with a SUBJECT, and it is the half the visible set exists
    to make possible.

    **A retrieval that returns nothing leaves no other trace**, which is why this had to be
    recorded at the pull site rather than derived.
    """
    reach = sum(1 for r in rows if r.get("event") == "reach")
    fail = [r for r in rows if r.get("event") == "reach_failed"]
    return {"reaches": reach, "failed": len(fail),
            "rate": round(len(fail) / reach, 4) if reach else None,
            "slots": sorted({r.get("slot") for r in fail if r.get("slot")})[:12]}


def report(rows: list[dict], gamma) -> dict:
    m, c = minted(rows, gamma), chains(gamma)
    return {
        "MINTED": m,
        "CHAINS": c,
        "REUSED": reused(rows),
        "TRANSFER": transfer(rows, gamma),
        "REACHED_AND_FAILED": reached_and_failed(rows),
        "chunk_reuse_count": sum(len(x["inside_later_mints"]) for x in c),
        "reads": ("14.7's three inherited, MINTED added. `effective atom depth` is NOT here: "
                  "it is computed over the closure, not over what was minted"),
    }
